#!/usr/bin/env python3
"""
Script to compare Phoenix nurses from JSON with CMS nurses.csv database.
Uses multiple matching strategies: license numbers, names, and contact info.
"""

import json
import sys
import pandas as pd
import re
from typing import List, Dict, Any, Tuple, Optional

def load_phoenix_nurses(json_file: str) -> List[Dict[str, Any]]:
    """Load Phoenix nurses from JSON file."""
    print(f"📂 Loading {json_file}...")
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"✅ {len(data)} Phoenix nurses loaded\n")
    return data

def load_nurses_csv(csv_file: str) -> pd.DataFrame:
    """Load CMS nurses database."""
    print(f"📂 Loading {csv_file}...")
    df = pd.read_csv(csv_file, low_memory=False)
    print(f"✅ {len(df):,} CMS records loaded\n")
    return df

def normalize_name(name: str) -> str:
    """Normalize a name for comparison."""
    if pd.isna(name) or name == '':
        return ''
    return str(name).strip().upper()

def normalize_license(license_num: str) -> str:
    """Normalize a license number for comparison."""
    if pd.isna(license_num) or license_num == '':
        return ''
    # Remove common prefixes and normalize
    license_str = str(license_num).strip().upper()
    # Remove prefixes like RN, LP, PN
    license_str = re.sub(r'^(RN|LP|PN|TEMP)', '', license_str)
    return license_str

def extract_phone_numbers(pdl_data: Optional[Dict]) -> List[str]:
    """Extract phone numbers from People Data Labs data."""
    if not pdl_data or 'phone_numbers' not in pdl_data:
        return []
    
    phones = []
    for phone in pdl_data.get('phone_numbers', []):
        if phone:
            # Clean and normalize phone number
            phone_clean = re.sub(r'\D', '', str(phone))
            if len(phone_clean) >= 10:
                phones.append(phone_clean[-10:])  # Last 10 digits
    return phones

def normalize_phone(phone: Any) -> str:
    """Normalize a phone number to last 10 digits."""
    if pd.isna(phone) or phone == '':
        return ''
    phone_str = re.sub(r'\D', '', str(phone))
    if len(phone_str) >= 10:
        return phone_str[-10:]
    return ''

def match_by_license(phoenix_nurse: Dict, cms_df: pd.DataFrame) -> Tuple[Optional[pd.Series], str]:
    """
    Try to match by license number.
    Returns: (matched_row, match_method) or (None, '')
    """
    nursys_licenses = phoenix_nurse.get('nursys', {}).get('licenses', [])
    
    if not nursys_licenses:
        return None, ''
    
    # Get all license columns
    license_cols = [f'Provider License Number_{i}' for i in range(1, 16)]
    
    for license_info in nursys_licenses:
        license_num = license_info.get('license', '')
        if not license_num:
            continue
        
        normalized_license = normalize_license(license_num)
        if not normalized_license:
            continue
        
        # Search across all license columns
        for col in license_cols:
            if col in cms_df.columns:
                matches = cms_df[
                    cms_df[col].apply(lambda x: normalize_license(x) == normalized_license if pd.notna(x) else False)
                ]
                
                if len(matches) > 0:
                    return matches.iloc[0], f'LICENSE:{license_num}'
    
    return None, ''

def match_by_name(phoenix_nurse: Dict, cms_df: pd.DataFrame) -> List[pd.Series]:
    """
    Try to match by name (first + last).
    Returns: list of potential matches
    """
    first_name = normalize_name(phoenix_nurse.get('firstName', ''))
    last_name = normalize_name(phoenix_nurse.get('lastName', ''))
    
    if not first_name or not last_name:
        return []
    
    # Try exact match first
    matches = cms_df[
        (cms_df['Provider First Name'].str.upper().str.strip() == first_name) &
        (cms_df['Provider Last Name (Legal Name)'].str.upper().str.strip() == last_name)
    ]
    
    if len(matches) > 0:
        return matches.to_dict('records')
    
    # Try partial match (contains)
    matches = cms_df[
        (cms_df['Provider First Name'].str.upper().str.contains(first_name, na=False, regex=False)) &
        (cms_df['Provider Last Name (Legal Name)'].str.upper().str.contains(last_name, na=False, regex=False))
    ]
    
    return matches.to_dict('records') if len(matches) > 0 else []

def validate_with_contact(phoenix_nurse: Dict, cms_row: Any) -> bool:
    """
    Validate a name match using contact information from People Data Labs.
    Returns: True if contact info matches
    """
    pdl_data = phoenix_nurse.get('peopleDataLabs')
    if not pdl_data:
        return False
    
    # Extract phones from PDL
    pdl_phones = extract_phone_numbers(pdl_data)
    if not pdl_phones:
        return False
    
    # Get CMS phones
    cms_phones = []
    practice_phone = normalize_phone(cms_row.get('Provider Business Practice Location Address Telephone Number'))
    mailing_phone = normalize_phone(cms_row.get('Provider Business Mailing Address Telephone Number'))
    
    if practice_phone:
        cms_phones.append(practice_phone)
    if mailing_phone and mailing_phone != practice_phone:
        cms_phones.append(mailing_phone)
    
    # Check if any PDL phone matches any CMS phone
    for pdl_phone in pdl_phones:
        if pdl_phone in cms_phones:
            return True
    
    return False

def extract_cms_data(cms_row: Any) -> Dict[str, Any]:
    """Extract relevant CMS data from a matched row."""
    # Get license numbers and states
    license_numbers = []
    license_states = []
    
    for i in range(1, 16):
        lic_num = cms_row.get(f'Provider License Number_{i}')
        lic_state = cms_row.get(f'Provider License Number State Code_{i}')
        
        if pd.notna(lic_num) and str(lic_num).strip():
            license_numbers.append(str(lic_num))
            if pd.notna(lic_state):
                license_states.append(str(lic_state))
    
    # Build practice address
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

def find_matches(phoenix_nurses: List[Dict], cms_df: pd.DataFrame) -> Tuple[List[Dict], List[Dict]]:
    """
    Find matches between Phoenix nurses and CMS database.
    Returns: (matches, no_matches)
    """
    matches = []
    no_matches = []
    
    print("🔍 Matching Phoenix nurses with CMS database...\n")
    
    for idx, nurse in enumerate(phoenix_nurses, 1):
        fb_name = nurse.get('name', '')
        fb_id = nurse.get('id', '')
        
        # Progress indicator
        if idx % 10 == 0:
            print(f"  Processed: {idx}/{len(phoenix_nurses)} ({len(matches)} matches so far)")
        
        match_result = {
            'fb_id': fb_id,
            'fb_name': fb_name,
            'fb_profile_url': nurse.get('profileUrl', ''),
            'city': nurse.get('city', ''),
            'state': nurse.get('state', ''),
            'has_nursys_licenses': len(nurse.get('nursys', {}).get('licenses', [])) > 0,
            'has_pdl_data': 'peopleDataLabs' in nurse and nurse['peopleDataLabs'] is not None,
            'match_found': False,
            'match_confidence': '',
            'match_method': '',
            'cms_data': None
        }
        
        # Strategy 1: Try license match (CONFIRMED)
        matched_row, match_method = match_by_license(nurse, cms_df)
        if matched_row is not None:
            match_result['match_found'] = True
            match_result['match_confidence'] = 'CONFIRMED'
            match_result['match_method'] = match_method
            match_result['cms_data'] = extract_cms_data(matched_row)
            matches.append(match_result)
            continue
        
        # Strategy 2: Try name match
        name_matches = match_by_name(nurse, cms_df)
        if name_matches:
            # If we have PDL data, try to validate with contact info
            if match_result['has_pdl_data']:
                contact_validated = False
                for name_match in name_matches:
                    if validate_with_contact(nurse, name_match):
                        match_result['match_found'] = True
                        match_result['match_confidence'] = 'HIGH'
                        match_result['match_method'] = 'NAME+CONTACT'
                        match_result['cms_data'] = extract_cms_data(name_match)
                        contact_validated = True
                        break
                
                if contact_validated:
                    matches.append(match_result)
                    continue
            
            # Name match only (medium confidence)
            match_result['match_found'] = True
            match_result['match_confidence'] = 'MEDIUM'
            match_result['match_method'] = 'NAME_ONLY'
            match_result['cms_data'] = extract_cms_data(name_matches[0])
            matches.append(match_result)
            continue
        
        # No match found
        no_matches.append(match_result)
    
    print(f"\n✅ Matching complete!")
    return matches, no_matches

def save_csv_results(matches: List[Dict], no_matches: List[Dict]):
    """Save results to CSV files."""
    print(f"\n💾 Saving CSV results...")
    
    # Prepare matches data
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
        matches_df.to_csv('phoenix_matches.csv', index=False)
        print(f"  ✅ phoenix_matches.csv ({len(matches)} records)")
    
    # Prepare no matches data
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
        no_matches_df.to_csv('phoenix_no_matches.csv', index=False)
        print(f"  ✅ phoenix_no_matches.csv ({len(no_matches)} records)")

def enrich_json(phoenix_nurses: List[Dict], matches: List[Dict]) -> List[Dict]:
    """Enrich the original JSON with CMS match data."""
    print(f"\n🔧 Enriching JSON with CMS data...")
    
    # Create a lookup dictionary by Facebook ID
    match_lookup = {m['fb_id']: m for m in matches}
    
    enriched_nurses = []
    for nurse in phoenix_nurses:
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
    
    # Save enriched JSON
    with open('phoenix_nurses_enriched.json', 'w', encoding='utf-8') as f:
        json.dump(enriched_nurses, f, indent=2, ensure_ascii=False)
    
    print(f"  ✅ phoenix_nurses_enriched.json saved")
    return enriched_nurses

def display_statistics(matches: List[Dict], no_matches: List[Dict], total: int):
    """Display comprehensive statistics about the matching results."""
    print("\n" + "="*100)
    print("📊 MATCHING STATISTICS")
    print("="*100)
    
    print(f"\n📈 Overall Summary:")
    print(f"  Total Phoenix nurses: {total}")
    print(f"  Matches found: {len(matches)} ({len(matches)/total*100:.1f}%)")
    print(f"  No matches: {len(no_matches)} ({len(no_matches)/total*100:.1f}%)")
    
    # Breakdown by confidence level
    confirmed = [m for m in matches if m['match_confidence'] == 'CONFIRMED']
    high = [m for m in matches if m['match_confidence'] == 'HIGH']
    medium = [m for m in matches if m['match_confidence'] == 'MEDIUM']
    
    print(f"\n🎯 Matches by Confidence Level:")
    print(f"  CONFIRMED (License match): {len(confirmed)}")
    print(f"  HIGH (Name + Contact): {len(high)}")
    print(f"  MEDIUM (Name only): {len(medium)}")
    
    # Nursys licenses
    with_nursys = sum(1 for n in matches + no_matches if n['has_nursys_licenses'])
    without_nursys = sum(1 for n in matches + no_matches if not n['has_nursys_licenses'])
    
    print(f"\n📜 Nursys License Information:")
    print(f"  With Nursys licenses: {with_nursys} ({with_nursys/total*100:.1f}%)")
    print(f"  Without Nursys licenses: {without_nursys} ({without_nursys/total*100:.1f}%)")
    
    # PDL enrichment
    with_pdl = sum(1 for n in matches + no_matches if n['has_pdl_data'])
    without_pdl = sum(1 for n in matches + no_matches if not n['has_pdl_data'])
    
    print(f"\n🔍 People Data Labs Enrichment:")
    print(f"  With PDL data: {with_pdl} ({with_pdl/total*100:.1f}%)")
    print(f"  Without PDL data: {without_pdl} ({without_pdl/total*100:.1f}%)")
    
    # Sample matches
    if confirmed:
        print(f"\n✨ Sample CONFIRMED Matches:")
        for match in confirmed[:3]:
            print(f"  • {match['fb_name']} → {match['cms_data']['full_name']} (NPI: {match['cms_data']['npi']})")
    
    if high:
        print(f"\n✨ Sample HIGH Confidence Matches:")
        for match in high[:3]:
            print(f"  • {match['fb_name']} → {match['cms_data']['full_name']} (NPI: {match['cms_data']['npi']})")
    
    print("\n" + "="*100)

def main():
    """Main execution function."""
    phoenix_json = 'phoenix_nurses.json'
    cms_csv = 'nurses.csv'
    
    # Load data
    phoenix_nurses = load_phoenix_nurses(phoenix_json)
    cms_df = load_nurses_csv(cms_csv)
    
    # Find matches
    matches, no_matches = find_matches(phoenix_nurses, cms_df)
    
    # Save CSV results
    save_csv_results(matches, no_matches)
    
    # Enrich JSON
    enrich_json(phoenix_nurses, matches)
    
    # Display statistics
    display_statistics(matches, no_matches, len(phoenix_nurses))
    
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
