#!/usr/bin/env python3
"""
Script to compare Denver nurses from JSON with CMS data.csv database (9.2M records).
Uses streaming approach - processes chunks and matches on-the-fly without loading everything into memory.
"""

import json
import sys
import pandas as pd
import re
import time
from typing import List, Dict, Any, Tuple, Optional

def load_denver_nurses(json_file: str) -> List[Dict[str, Any]]:
    """Load Denver nurses from JSON file."""
    print(f"📂 Loading {json_file}...")
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"✅ {len(data)} Denver nurses loaded\n")
    return data

def normalize_name(name: str) -> str:
    """Normalize a name for comparison."""
    if pd.isna(name) or name == '':
        return ''
    return str(name).strip().upper()

def normalize_license(license_num: str) -> str:
    """Normalize a license number for comparison."""
    if pd.isna(license_num) or license_num == '':
        return ''
    license_str = str(license_num).strip().upper()
    license_str = re.sub(r'^(RN|LP|PN|TEMP)', '', license_str)
    return license_str

def extract_phone_numbers(pdl_data: Optional[Dict]) -> List[str]:
    """Extract phone numbers from People Data Labs data."""
    if not pdl_data or 'phone_numbers' not in pdl_data:
        return []
    
    phones = []
    for phone in pdl_data.get('phone_numbers', []):
        if phone:
            phone_clean = re.sub(r'\D', '', str(phone))
            if len(phone_clean) >= 10:
                phones.append(phone_clean[-10:])
    return phones

def normalize_phone(phone: Any) -> str:
    """Normalize a phone number to last 10 digits."""
    if pd.isna(phone) or phone == '':
        return ''
    phone_str = re.sub(r'\D', '', str(phone))
    if len(phone_str) >= 10:
        return phone_str[-10:]
    return ''

def extract_cms_data(cms_row: pd.Series) -> Dict[str, Any]:
    """Extract relevant CMS data from a matched row."""
    license_numbers = []
    license_states = []
    
    for i in range(1, 16):
        lic_num = cms_row.get(f'Provider License Number_{i}')
        lic_state = cms_row.get(f'Provider License Number State Code_{i}')
        
        if pd.notna(lic_num) and str(lic_num).strip():
            license_numbers.append(str(lic_num))
            if pd.notna(lic_state):
                license_states.append(str(lic_state))
    
    practice_addr_parts = []
    addr1 = cms_row.get('Provider First Line Business Practice Location Address')
    addr2 = cms_row.get('Provider Second Line Business Practice Location Address')
    city = cms_row.get('Provider Business Practice Location Address City Name')
    state = cms_row.get('Provider Business Practice Location Address State Name')
    zip_code = cms_row.get('Provider Business Practice Location Address Postal Code')
    
    if pd.notna(addr1):
        practice_addr_parts.append(str(addr1))
    if pd.notna(addr2):
        practice_addr_parts.append(str(addr2))
    
    city_state_zip = []
    if pd.notna(city):
        city_state_zip.append(str(city))
    if pd.notna(state):
        city_state_zip.append(str(state))
    if pd.notna(zip_code):
        city_state_zip.append(str(zip_code))
    
    if city_state_zip:
        practice_addr_parts.append(', '.join(city_state_zip))
    
    practice_address = ', '.join(practice_addr_parts) if practice_addr_parts else ''
    
    return {
        'npi': str(cms_row.get('NPI', '')) if pd.notna(cms_row.get('NPI')) else '',
        'full_name': f"{cms_row.get('Provider First Name', '')} {cms_row.get('Provider Last Name (Legal Name)', '')}".strip(),
        'credential': str(cms_row.get('Provider Credential Text', '')) if pd.notna(cms_row.get('Provider Credential Text')) else '',
        'practice_address': practice_address,
        'practice_phone': str(cms_row.get('Provider Business Practice Location Address Telephone Number', '')) if pd.notna(cms_row.get('Provider Business Practice Location Address Telephone Number')) else '',
        'mailing_phone': str(cms_row.get('Provider Business Mailing Address Telephone Number', '')) if pd.notna(cms_row.get('Provider Business Mailing Address Telephone Number')) else '',
        'license_numbers': license_numbers,
        'license_states': license_states,
        'enumeration_date': str(cms_row.get('Provider Enumeration Date', '')) if pd.notna(cms_row.get('Provider Enumeration Date')) else '',
        'last_update_date': str(cms_row.get('Last Update Date', '')) if pd.notna(cms_row.get('Last Update Date')) else ''
    }

def prepare_denver_nurse_data(nurse: Dict) -> Dict:
    """Prepare Denver nurse search data."""
    # Get license numbers to search
    licenses_to_search = []
    nursys_licenses = nurse.get('nursys', {}).get('licenses', [])
    for lic in nursys_licenses:
        lic_num = lic.get('license', '')
        if lic_num:
            normalized = normalize_license(lic_num)
            if normalized:
                licenses_to_search.append((normalized, lic_num))
    
    # Get name to search
    first_name = normalize_name(nurse.get('firstName', ''))
    last_name = normalize_name(nurse.get('lastName', ''))
    
    # Get phones for validation
    pdl_phones = []
    pdl_data = nurse.get('peopleDataLabs')
    if pdl_data:
        pdl_phones = extract_phone_numbers(pdl_data)
    
    return {
        'fb_id': nurse.get('id', ''),
        'fb_name': nurse.get('name', ''),
        'fb_profile_url': nurse.get('profileUrl', ''),
        'city': nurse.get('city', ''),
        'state': nurse.get('state', ''),
        'has_nursys_licenses': len(nursys_licenses) > 0,
        'has_pdl_data': pdl_data is not None,
        'licenses_to_search': licenses_to_search,
        'first_name': first_name,
        'last_name': last_name,
        'pdl_phones': pdl_phones,
        'match_found': False,
        'match_confidence': '',
        'match_method': '',
        'cms_data': None
    }

def match_chunk_against_nurses(chunk: pd.DataFrame, denver_data: List[Dict], license_cols: List[str]) -> int:
    """Match a chunk of CMS data against Denver nurses. Returns number of new matches found."""
    matches_found = 0
    
    for idx, row in chunk.iterrows():
        # Check licenses first (CONFIRMED matches)
        for nurse in denver_data:
            if nurse['match_found']:
                continue
            
            for normalized_lic, original_lic in nurse['licenses_to_search']:
                for col in license_cols:
                    if col in row and pd.notna(row[col]):
                        if normalize_license(row[col]) == normalized_lic:
                            nurse['match_found'] = True
                            nurse['match_confidence'] = 'CONFIRMED'
                            nurse['match_method'] = f'LICENSE:{original_lic}'
                            nurse['cms_data'] = extract_cms_data(row)
                            matches_found += 1
                            break
                if nurse['match_found']:
                    break
            if nurse['match_found']:
                continue
        
        # Check names (HIGH/MEDIUM matches)
        first_name = normalize_name(row.get('Provider First Name', ''))
        last_name = normalize_name(row.get('Provider Last Name (Legal Name)', ''))
        
        if not first_name or not last_name:
            continue
        
        for nurse in denver_data:
            if nurse['match_found']:
                continue
            
            if nurse['first_name'] == first_name and nurse['last_name'] == last_name:
                # Try contact validation if we have PDL data
                if nurse['has_pdl_data'] and nurse['pdl_phones']:
                    cms_phones = []
                    practice_phone = normalize_phone(row.get('Provider Business Practice Location Address Telephone Number'))
                    mailing_phone = normalize_phone(row.get('Provider Business Mailing Address Telephone Number'))
                    
                    if practice_phone:
                        cms_phones.append(practice_phone)
                    if mailing_phone and mailing_phone != practice_phone:
                        cms_phones.append(mailing_phone)
                    
                    # Check if any PDL phone matches
                    contact_match = any(pdl_phone in cms_phones for pdl_phone in nurse['pdl_phones'])
                    
                    if contact_match:
                        nurse['match_found'] = True
                        nurse['match_confidence'] = 'HIGH'
                        nurse['match_method'] = 'NAME+CONTACT'
                        nurse['cms_data'] = extract_cms_data(row)
                        matches_found += 1
                        continue
                
                # Name only match
                nurse['match_found'] = True
                nurse['match_confidence'] = 'MEDIUM'
                nurse['match_method'] = 'NAME_ONLY'
                nurse['cms_data'] = extract_cms_data(row)
                matches_found += 1
    
    return matches_found

def find_matches_streaming(denver_nurses: List[Dict], csv_file: str, chunk_size: int = 50000) -> Tuple[List[Dict], List[Dict]]:
    """
    Find matches using streaming approach - processes chunks without storing in memory.
    """
    print("🔍 Preparing Denver nurses data for matching...\n")
    denver_data = [prepare_denver_nurse_data(nurse) for nurse in denver_nurses]
    
    license_cols = [f'Provider License Number_{i}' for i in range(1, 16)]
    
    print("📊 Processing data.csv in streaming mode...")
    print("   (Memory-efficient: processes and discards each chunk)\n")
    
    start_time = time.time()
    total_rows = 0
    chunk_num = 0
    total_matches = 0
    
    for chunk in pd.read_csv(csv_file, chunksize=chunk_size, low_memory=False):
        chunk_num += 1
        total_rows += len(chunk)
        
        # Match this chunk against Denver nurses
        new_matches = match_chunk_against_nurses(chunk, denver_data, license_cols)
        total_matches += new_matches
        
        # Progress report
        if chunk_num % 10 == 0:
            elapsed = time.time() - start_time
            rate = total_rows / elapsed
            still_searching = sum(1 for n in denver_data if not n['match_found'])
            print(f"  Chunk {chunk_num}: {total_rows:,} rows | {rate:,.0f} rows/sec | Matches: {total_matches} | Still searching: {still_searching} | Elapsed: {elapsed:.1f}s")
        
        # Early exit if all nurses found
        if all(n['match_found'] for n in denver_data):
            print(f"\n🎉 All Denver nurses matched! Stopping early at row {total_rows:,}")
            break
    
    elapsed = time.time() - start_time
    print(f"\n✅ Processing complete!")
    print(f"  Total rows processed: {total_rows:,}")
    print(f"  Total matches found: {total_matches}")
    print(f"  Time: {elapsed:.1f}s ({elapsed/60:.1f} minutes)\n")
    
    # Separate matches and no matches
    matches = [n for n in denver_data if n['match_found']]
    no_matches = [n for n in denver_data if not n['match_found']]
    
    return matches, no_matches

def save_csv_results(matches: List[Dict], no_matches: List[Dict]):
    """Save results to CSV files."""
    print(f"💾 Saving CSV results...")
    
    if matches:
        matches_data = []
        for match in matches:
            row = {
                'Facebook ID': match['fb_id'],
                'Facebook Name': match['fb_name'],
                'Profile URL': match['fb_profile_url'],
                'City': match['city'],
                'State': match['state'],
                'Match Confidence': match['match_confidence'],
                'Match Method': match['match_method'],
                'Has Nursys Licenses': match['has_nursys_licenses'],
                'Has PDL Data': match['has_pdl_data']
            }
            
            if match['cms_data']:
                row.update({
                    'CMS NPI': match['cms_data']['npi'],
                    'CMS Full Name': match['cms_data']['full_name'],
                    'CMS Credential': match['cms_data']['credential'],
                    'CMS Practice Address': match['cms_data']['practice_address'],
                    'CMS Practice Phone': match['cms_data']['practice_phone'],
                    'CMS Mailing Phone': match['cms_data']['mailing_phone'],
                    'CMS License Numbers': ', '.join(match['cms_data']['license_numbers']),
                    'CMS License States': ', '.join(match['cms_data']['license_states']),
                    'CMS Enumeration Date': match['cms_data']['enumeration_date'],
                    'CMS Last Update Date': match['cms_data']['last_update_date']
                })
            
            matches_data.append(row)
        
        matches_df = pd.DataFrame(matches_data)
        matches_df.to_csv('denver_matches.csv', index=False)
        print(f"  ✅ denver_matches.csv ({len(matches)} records)")
    
    if no_matches:
        no_matches_data = []
        for nm in no_matches:
            no_matches_data.append({
                'Facebook ID': nm['fb_id'],
                'Facebook Name': nm['fb_name'],
                'Profile URL': nm['fb_profile_url'],
                'City': nm['city'],
                'State': nm['state'],
                'Has Nursys Licenses': nm['has_nursys_licenses'],
                'Has PDL Data': nm['has_pdl_data']
            })
        
        no_matches_df = pd.DataFrame(no_matches_data)
        no_matches_df.to_csv('denver_no_matches.csv', index=False)
        print(f"  ✅ denver_no_matches.csv ({len(no_matches)} records)")

def enrich_json(denver_nurses: List[Dict], matches: List[Dict]) -> List[Dict]:
    """Enrich the original JSON with CMS match data."""
    print(f"\n🔧 Enriching JSON with CMS data...")
    
    match_lookup = {m['fb_id']: m for m in matches}
    
    enriched_nurses = []
    for nurse in denver_nurses:
        enriched_nurse = nurse.copy()
        fb_id = nurse.get('id', '')
        
        if fb_id in match_lookup:
            match = match_lookup[fb_id]
            enriched_nurse['cmsMatch'] = {
                'found': True,
                'confidence': match['match_confidence'],
                'matchMethod': match['match_method'],
                'npi': match['cms_data']['npi'] if match['cms_data'] else '',
                'fullName': match['cms_data']['full_name'] if match['cms_data'] else '',
                'credential': match['cms_data']['credential'] if match['cms_data'] else '',
                'practiceAddress': match['cms_data']['practice_address'] if match['cms_data'] else '',
                'practicePhone': match['cms_data']['practice_phone'] if match['cms_data'] else '',
                'mailingPhone': match['cms_data']['mailing_phone'] if match['cms_data'] else '',
                'licenseNumbers': match['cms_data']['license_numbers'] if match['cms_data'] else [],
                'licenseStates': match['cms_data']['license_states'] if match['cms_data'] else [],
                'enumerationDate': match['cms_data']['enumeration_date'] if match['cms_data'] else '',
                'lastUpdateDate': match['cms_data']['last_update_date'] if match['cms_data'] else ''
            }
        else:
            enriched_nurse['cmsMatch'] = {
                'found': False
            }
        
        enriched_nurses.append(enriched_nurse)
    
    with open('denver_nurses_enriched.json', 'w', encoding='utf-8') as f:
        json.dump(enriched_nurses, f, indent=2, ensure_ascii=False)
    
    print(f"  ✅ denver_nurses_enriched.json saved")
    return enriched_nurses

def display_statistics(matches: List[Dict], no_matches: List[Dict], total: int, elapsed_time: float):
    """Display comprehensive statistics."""
    print("\n" + "="*100)
    print("📊 MATCHING STATISTICS")
    print("="*100)
    
    print(f"\n📈 Overall Summary:")
    print(f"  Total Denver nurses: {total}")
    print(f"  Matches found: {len(matches)} ({len(matches)/total*100:.1f}%)")
    print(f"  No matches: {len(no_matches)} ({len(no_matches)/total*100:.1f}%)")
    print(f"  Processing time: {elapsed_time:.1f}s ({elapsed_time/60:.1f} minutes)")
    
    confirmed = [m for m in matches if m['match_confidence'] == 'CONFIRMED']
    high = [m for m in matches if m['match_confidence'] == 'HIGH']
    medium = [m for m in matches if m['match_confidence'] == 'MEDIUM']
    
    print(f"\n🎯 Matches by Confidence Level:")
    print(f"  CONFIRMED (License match): {len(confirmed)}")
    print(f"  HIGH (Name + Contact): {len(high)}")
    print(f"  MEDIUM (Name only): {len(medium)}")
    
    with_nursys = sum(1 for n in matches + no_matches if n['has_nursys_licenses'])
    without_nursys = sum(1 for n in matches + no_matches if not n['has_nursys_licenses'])
    
    print(f"\n📜 Nursys License Information:")
    print(f"  With Nursys licenses: {with_nursys} ({with_nursys/total*100:.1f}%)")
    print(f"  Without Nursys licenses: {without_nursys} ({without_nursys/total*100:.1f}%)")
    
    with_pdl = sum(1 for n in matches + no_matches if n['has_pdl_data'])
    without_pdl = sum(1 for n in matches + no_matches if not n['has_pdl_data'])
    
    print(f"\n🔍 People Data Labs Enrichment:")
    print(f"  With PDL data: {with_pdl} ({with_pdl/total*100:.1f}%)")
    print(f"  Without PDL data: {without_pdl} ({without_pdl/total*100:.1f}%)")
    
    if confirmed:
        print(f"\n✨ CONFIRMED Matches (License):")
        for match in confirmed:
            print(f"  • {match['fb_name']} → {match['cms_data']['full_name']} (NPI: {match['cms_data']['npi']})")
            print(f"    Method: {match['match_method']}")
    
    if high:
        print(f"\n✨ HIGH Confidence Matches (Name + Contact):")
        for match in high[:5]:
            print(f"  • {match['fb_name']} → {match['cms_data']['full_name']} (NPI: {match['cms_data']['npi']})")
    
    if medium:
        print(f"\n✨ MEDIUM Confidence Matches (Name Only):")
        for match in medium[:5]:
            print(f"  • {match['fb_name']} → {match['cms_data']['full_name']} (NPI: {match['cms_data']['npi']})")
    
    print("\n" + "="*100)

def main():
    """Main execution function."""
    denver_json = 'denver.json'
    cms_csv = 'data.csv'
    
    overall_start = time.time()
    
    denver_nurses = load_denver_nurses(denver_json)
    matches, no_matches = find_matches_streaming(denver_nurses, cms_csv)
    save_csv_results(matches, no_matches)
    enrich_json(denver_nurses, matches)
    
    overall_elapsed = time.time() - overall_start
    display_statistics(matches, no_matches, len(denver_nurses), overall_elapsed)
    
    print("\n✅ All operations completed successfully!\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Program interrupted. Goodbye!\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
