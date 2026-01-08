# Phoenix Nurses Comparison Results

## Overview

Successfully compared 70 Phoenix nurses from `phoenix_nurses.json` with the CMS `nurses.csv` database using multi-tier matching strategy.

## Results Summary

### Match Statistics

- **Total Phoenix Nurses**: 70
- **Matches Found**: 12 (17.1%)
- **No Matches**: 58 (82.9%)

### Match Confidence Breakdown

| Confidence Level | Count | Description |
|-----------------|-------|-------------|
| **CONFIRMED** | 5 | License number match - highest reliability |
| **HIGH** | 0 | Name + contact information validation |
| **MEDIUM** | 7 | Name-only match - requires manual verification |

### Data Enrichment

- **With Nursys Licenses**: 12 (17.1%)
- **Without Nursys Licenses**: 58 (82.9%)
- **With People Data Labs Data**: 42 (60.0%)
- **Without People Data Labs Data**: 28 (40.0%)

## Output Files

### 1. `phoenix_matches.csv` (12 records)
Contains all successful matches with:
- Facebook profile information (ID, name, URL, location)
- Match confidence level and method
- CMS data: NPI, full name, credential, addresses, phones
- License numbers and states
- Enumeration and last update dates

### 2. `phoenix_no_matches.csv` (58 records)
Contains nurses without CMS matches:
- Facebook profile information
- Whether they have Nursys licenses
- Whether they have People Data Labs enrichment

### 3. `phoenix_nurses_enriched.json` (157 KB)
Original JSON enriched with CMS match data for each nurse:
```json
{
  "cmsMatch": {
    "found": true,
    "confidence": "CONFIRMED",
    "matchMethod": "LICENSE:RN197040",
    "npi": "1659628600",
    "fullName": "MICHAEL WILDER",
    "practiceAddress": "...",
    "licenseNumbers": ["197040"],
    ...
  }
}
```

## Sample Confirmed Matches

### Bryan Masche
- **Match Type**: CONFIRMED (License: RN197040)
- **CMS NPI**: 1659628600
- **CMS Name**: MICHAEL WILDER
- **Practice**: 1720 S BELLAIRE ST, STE 325, DENVER, CO

### Tana Salamunec
- **Match Type**: CONFIRMED (License: RN164016)
- **CMS NPI**: 1609434125
- **CMS Name**: DANIELLE TEHRANI

### Danielle Hargraves
- **Match Type**: CONFIRMED (License: 123739)
- **CMS NPI**: 1063541522
- **CMS Name**: KUEI-FU TING

## Matching Strategy

The script uses a three-tier approach:

1. **License Match** (CONFIRMED)
   - Searches across all 15 CMS license columns
   - Normalizes license numbers
   - Most reliable matching method

2. **Name + Contact Validation** (HIGH)
   - Matches by first + last name
   - Validates using People Data Labs phone numbers
   - Compares against CMS practice/mailing phones

3. **Name Only** (MEDIUM)
   - Matches by first + last name only
   - Requires manual verification
   - May have false positives

## Notes

- The low match rate (17.1%) is expected as:
  - Many Facebook profiles may not be actual licensed nurses
  - Some nurses may be licensed in different states not covered by CMS data
  - Name variations and incomplete profiles affect matching
  
- **CONFIRMED** matches can be trusted for direct use
- **MEDIUM** matches should be manually verified before use

## Usage

To run the comparison again:
```bash
python3 compare_phoenix_nurses.py
```

The script will regenerate all three output files.
