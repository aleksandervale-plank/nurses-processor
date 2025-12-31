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

# Processing configuration
DEFAULT_CHUNK_SIZE = 100000  # Process 100K rows at a time
DEFAULT_OUTPUT_FILE = 'nurses_filtered.csv'

