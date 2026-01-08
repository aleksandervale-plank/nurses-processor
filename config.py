"""
Configuration constants for the Nurses CSV Processor.
"""

# Nurse taxonomy codes to filter
NURSE_TAXONOMY_CODES = [
    '363L00000X',  # Nurse Practitioner
    '163W00000X',  # Registered Nurse (RN)
    '164W00000X',  # Licensed Practical Nurse (LPN)
]

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

