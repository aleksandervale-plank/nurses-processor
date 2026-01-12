"""
Configuration constants for the Nurses CSV Processor.
"""
# ============================================================================
# NURSE TAXONOMY CODES - Comprehensive List
# ============================================================================
# Based on NUCC (National Uniform Claim Committee) Healthcare Provider Taxonomy
# Updated: January 2026
# 
# Strategy: Use prefixes to match ALL specializations within each category
# Example: '163W' matches all RN specializations (163W00000X, 163WA0400X, etc.)
#
# CATEGORIES INCLUDED:
# -------------------
# 163W - Registered Nurses (RN) - All 56+ specializations
#        Examples: General RN, Pediatric, Critical Care, Ambulatory, etc.
#
# 164W - Licensed Practical Nurse (LPN)
# 164X - Licensed Vocational Nurse (LVN)
#
# 363L - Nurse Practitioners (NP/APRN) - Advanced Practice (18+ specializations)
#        Examples: Family NP, Adult Health, Pediatric, Psychiatric, etc.
#
# 364S - Clinical Nurse Specialists (CNS) - 33+ specializations
#        Examples: Adult Health, Pediatric, Psychiatric, Critical Care, etc.
#
# 367  - Nurse Anesthetists and Midwives
#   3675 - Certified Registered Nurse Anesthetist (CRNA)
#   367A - Advanced Practice Midwife (APRN-CNM)
#   367H - Certified Nurse Midwife (CNM)
#
# CATEGORIES EXCLUDED:
# -------------------
# 363A - Physician Assistant (PA) - NOT a nurse
# 372  - Nursing Assistants/Aides - NOT licensed nurses
# 373  - Nursing Attendants - NOT licensed nurses
# 374  - Technicians (EMT, Radiology, etc) - NOT nurses
# 376  - Support roles (Administrators, IT) - NOT clinical nurses
#
# ============================================================================

# Use prefixes to match all specializations automatically
NURSE_TAXONOMY_CODES = [
    # Registered Nurses (RN) - all specializations
    '163W',  # Matches: 163W00000X, 163WA0400X, 163WC0200X, etc. (56+ codes)
    
    # Licensed Practical/Vocational Nurses
    '164W',  # Licensed Practical Nurse (LPN)
    '164X',  # Licensed Vocational Nurse (LVN)
    
    # Advanced Practice Registered Nurses (APRN)
    '363L',  # Nurse Practitioners - all specializations (18+ codes)
    '364S',  # Clinical Nurse Specialists - all specializations (33+ codes)
    
    # Nurse Anesthetists and Midwives
    '3675',  # Certified Registered Nurse Anesthetist (CRNA)
    '367A',  # Advanced Practice Midwife
    '367H',  # Certified Nurse Midwife (CNM)
]

# Optional: Include nursing assistants and technicians (currently excluded)
# Uncomment these if you want to include non-licensed nursing staff:
# NURSING_SUPPORT_CODES = [
#     '3725',  # Nursing Assistant
#     '3726',  # Nursing Aide
#     '373H',  # Nursing Attendant
#     '374J',  # Nursing Technician
# ]

# Column names for taxonomy codes (15 possible taxonomy columns)
TAXONOMY_CODE_COLUMNS = [
    'Healthcare Provider Taxonomy Code_1',
    'Healthcare Provider Taxonomy Code_2',
    'Healthcare Provider Taxonomy Code_3',
    'Healthcare Provider Taxonomy Code_4',
    'Healthcare Provider Taxonomy Code_5',
    'Healthcare Provider Taxonomy Code_6',
    'Healthcare Provider Taxonomy Code_7',
    'Healthcare Provider Taxonomy Code_8',
    'Healthcare Provider Taxonomy Code_9',
    'Healthcare Provider Taxonomy Code_10',
    'Healthcare Provider Taxonomy Code_11',
    'Healthcare Provider Taxonomy Code_12',
    'Healthcare Provider Taxonomy Code_13',
    'Healthcare Provider Taxonomy Code_14',
    'Healthcare Provider Taxonomy Code_15',
]

# Column names for filtering
FILTER_COLUMNS = {
    'first_name': 'Provider First Name',
    'last_name': 'Provider Last Name (Legal Name)',
    'city': 'Provider Business Practice Location Address City Name',
    'state': 'Provider Business Practice Location Address State Name',
}

# Phone number columns
PHONE_MAILING_COLUMN = 'Provider Business Mailing Address Telephone Number'
PHONE_PRACTICE_COLUMN = 'Provider Business Practice Location Address Telephone Number'

# Useful columns to keep in output (removes ~200+ useless columns)
USEFUL_COLUMNS = [
    # Basic identification
    'NPI',
    'Entity Type Code',
    'Provider First Name',
    'Provider Middle Name',
    'Provider Last Name (Legal Name)',
    'Provider Name Prefix Text',
    'Provider Name Suffix Text',
    'Provider Credential Text',
    
    # Practice location (where they work)
    'Provider First Line Business Practice Location Address',
    'Provider Second Line Business Practice Location Address',
    'Provider Business Practice Location Address City Name',
    'Provider Business Practice Location Address State Name',
    'Provider Business Practice Location Address Postal Code',
    'Provider Business Practice Location Address Country Code (If outside U.S.)',
    'Provider Business Practice Location Address Telephone Number',
    'Provider Business Practice Location Address Fax Number',
    
    # Mailing address (personal address)
    'Provider First Line Business Mailing Address',
    'Provider Second Line Business Mailing Address',
    'Provider Business Mailing Address City Name',
    'Provider Business Mailing Address State Name',
    'Provider Business Mailing Address Postal Code',
    'Provider Business Mailing Address Country Code (If outside U.S.)',
    'Provider Business Mailing Address Telephone Number',
    'Provider Business Mailing Address Fax Number',
    
    # Taxonomy codes (all 15 - needed to identify nurse types)
    'Healthcare Provider Taxonomy Code_1',
    'Healthcare Provider Taxonomy Code_2',
    'Healthcare Provider Taxonomy Code_3',
    'Healthcare Provider Taxonomy Code_4',
    'Healthcare Provider Taxonomy Code_5',
    'Healthcare Provider Taxonomy Code_6',
    'Healthcare Provider Taxonomy Code_7',
    'Healthcare Provider Taxonomy Code_8',
    'Healthcare Provider Taxonomy Code_9',
    'Healthcare Provider Taxonomy Code_10',
    'Healthcare Provider Taxonomy Code_11',
    'Healthcare Provider Taxonomy Code_12',
    'Healthcare Provider Taxonomy Code_13',
    'Healthcare Provider Taxonomy Code_14',
    'Healthcare Provider Taxonomy Code_15',
    
    # License information (all 15 - nurses can have multiple licenses)
    'Provider License Number_1',
    'Provider License Number State Code_1',
    'Provider License Number_2',
    'Provider License Number State Code_2',
    'Provider License Number_3',
    'Provider License Number State Code_3',
    'Provider License Number_4',
    'Provider License Number State Code_4',
    'Provider License Number_5',
    'Provider License Number State Code_5',
    'Provider License Number_6',
    'Provider License Number State Code_6',
    'Provider License Number_7',
    'Provider License Number State Code_7',
    'Provider License Number_8',
    'Provider License Number State Code_8',
    'Provider License Number_9',
    'Provider License Number State Code_9',
    'Provider License Number_10',
    'Provider License Number State Code_10',
    'Provider License Number_11',
    'Provider License Number State Code_11',
    'Provider License Number_12',
    'Provider License Number State Code_12',
    'Provider License Number_13',
    'Provider License Number State Code_13',
    'Provider License Number_14',
    'Provider License Number State Code_14',
    'Provider License Number_15',
    'Provider License Number State Code_15',
    
    # Important dates
    'Provider Enumeration Date',
    'Last Update Date',
    'Provider Sex Code',
]

# Processing configuration
DEFAULT_CHUNK_SIZE = 100000  # Process 100K rows at a time
DEFAULT_OUTPUT_FILE = 'nurses_filtered.csv'

