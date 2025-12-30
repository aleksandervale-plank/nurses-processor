# Nurses CSV Processor

A high-performance Python tool for processing large NPI (National Provider Identifier) healthcare provider CSV files to extract and filter nurse records. Designed to efficiently handle very large files (11GB+) using chunked streaming processing.

## Features

- **Memory Efficient**: Processes files in chunks, never loading the entire file into memory
- **Fast Processing**: Uses Polars library (5-10x faster than pandas) with automatic fallback to pandas
- **Flexible Filtering**: Filter by nurse taxonomy codes, name, city, and state
- **Progress Tracking**: Real-time progress updates during processing
- **Multiple Nurse Types**: Filters for Nurse Practitioners, Registered Nurses (RN), and Licensed Practical Nurses (LPN)
- **Interactive Viewer**: Beautiful terminal-based viewer to explore and filter results without creating new files
- **Statistics**: View distribution by state, city, and nurse types
- **Bilingual Documentation**: Complete documentation in English and Portuguese

## Installation

1. Clone or download this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

### Dependencies

- **polars** (recommended): Fast DataFrame library for large file processing
- **pandas** (fallback): Alternative DataFrame library if polars is unavailable
- **tabulate** (optional): For beautiful table formatting in the interactive viewer

## Nurse Taxonomy Codes

The script filters for the following nurse taxonomy codes across all 15 possible taxonomy columns:

- `363L00000X` - Nurse Practitioner (Advanced Practice)
- `163W00000X` - Registered Nurse (RN) - Most common for graduate nurses
- `164W00000X` - Licensed Practical Nurse (LPN)

## Usage

### Workflow Overview

1. **Process the large CSV file** (one time):
   ```bash
   python process_nurses.py --output nurses.csv
   ```

2. **Explore and filter results** (as many times as you want):
   ```bash
   python view_nurses.py
   ```

### Basic Usage

Extract all nurses from a CSV file:

```bash
# Uses data.csv automatically (or specify a file)
python process_nurses.py --output nurses.csv
```

### Interactive Viewer

After processing, use the interactive viewer to explore results:

```bash
python view_nurses.py
```

Features:
- Filter by name, city, state
- View statistics
- Beautiful formatted tables
- No new files created (unless you export)

### Filter by State

Extract nurses in a specific state:

```bash
python process_nurses.py npi_data.csv --output nurses_ca.csv --state CA
```

### Filter by City

Extract nurses in a specific city:

```bash
python process_nurses.py npi_data.csv --output nurses_la.csv --city "Los Angeles"
```

### Filter by Name

Extract nurses by first name:

```bash
python process_nurses.py npi_data.csv --output nurses_john.csv --first-name John
```

Extract nurses by last name:

```bash
python process_nurses.py npi_data.csv --output nurses_smith.csv --last-name Smith
```

### Combine Multiple Filters

All filters are applied as AND conditions (all must match):

```bash
python process_nurses.py npi_data.csv --output results.csv \
  --state CA \
  --city "San Francisco" \
  --last-name Smith
```

### Adjust Performance

For systems with more memory, increase chunk size for faster processing:

```bash
python process_nurses.py npi_data.csv --output nurses.csv --chunk-size 250000
```

For systems with less memory, decrease chunk size:

```bash
python process_nurses.py npi_data.csv --output nurses.csv --chunk-size 50000
```

## Command-Line Options

```
positional arguments:
  input_file            Path to input CSV file (e.g., npi_data.csv)

optional arguments:
  -h, --help            Show help message and exit
  --output, -o          Path to output CSV file (default: nurses_filtered.csv)
  --chunk-size          Number of rows to process at a time (default: 100,000)
  --first-name          Filter by provider first name (case-insensitive partial match)
  --last-name           Filter by provider last name (case-insensitive partial match)
  --city                Filter by city (case-insensitive partial match)
  --state               Filter by state code (e.g., CA, NY, TX)
```

## How It Works

### Architecture

```
┌─────────────┐
│  Input CSV  │ (11GB)
│  (NPI Data) │
└──────┬──────┘
       │
       │ Stream in chunks (100K rows)
       ▼
┌─────────────────┐
│ Chunk Processor │
│                 │
│ 1. Read chunk   │
│ 2. Check 15     │
│    taxonomy     │
│    columns      │
│ 3. Apply name/  │
│    city/state   │
│    filters      │
└──────┬──────────┘
       │
       │ Write matches incrementally
       ▼
┌─────────────┐
│  Output CSV │ (Filtered nurses)
│  (~1-2 GB)  │
└─────────────┘
```

### Processing Strategy

1. **Streaming**: Reads the CSV file in chunks, not loading the entire file into memory
2. **Taxonomy Checking**: For each row, checks all 15 taxonomy code columns for nurse codes
3. **Additional Filtering**: Applies optional name, city, and state filters
4. **Incremental Output**: Writes matching records to the output file as they're found

### Memory Usage

- **Traditional approach**: Would require 11+ GB of RAM
- **This tool**: Uses only 200-500 MB of RAM regardless of file size

### Performance

Processing an 11GB file typically takes:
- **With Polars**: ~10-15 minutes (depending on hardware)
- **With Pandas**: ~20-30 minutes (fallback)

Output file size is typically 1-2 GB (if ~10-15% of providers are nurses).

## CSV Column Reference

The script processes the following key columns from the NPI CSV:

### Filter Columns

- `Provider First Name` - First name of the provider
- `Provider Last Name (Legal Name)` - Last name of the provider
- `Provider Business Practice Location Address City Name` - City where provider practices
- `Provider Business Practice Location Address State Name` - State code (e.g., CA, NY)

### Taxonomy Code Columns (15 total)

- `Healthcare Provider Taxonomy Code_1` through `Healthcare Provider Taxonomy Code_15`
  - Each provider can have up to 15 different taxonomy codes
  - The script checks ALL 15 columns to find nurse codes

## Output

The output CSV file contains all original columns from the input file, but only includes rows where:

1. At least ONE of the 15 taxonomy code columns contains a nurse taxonomy code
2. ALL additional filter criteria are met (if specified)

### Example Output Statistics

```
============================================================
PROCESSING COMPLETE
============================================================
Total rows processed: 7,523,456
Nurses found: 892,445
Chunks processed: 76
Percentage: 11.86%

Output saved to: nurses.csv
Output size: 1.45 GB
============================================================
```

## Troubleshooting

### Error: "Input file not found"

Make sure the path to your CSV file is correct. Use absolute paths if needed:

```bash
python process_nurses.py /full/path/to/npi_data.csv --output nurses.csv
```

### Memory Issues

If you encounter memory errors, reduce the chunk size:

```bash
python process_nurses.py input.csv --output nurses.csv --chunk-size 50000
```

### Slow Processing

If processing is too slow, try:

1. Install Polars for better performance: `pip install polars`
2. Increase chunk size (if you have enough RAM): `--chunk-size 250000`
3. Remove unnecessary filters to process more data faster

### No Results Found

If no nurses are found, check:

1. Verify the input CSV has the correct column names
2. Try without additional filters to see if nurses exist at all
3. Check if the taxonomy code columns are present in your CSV

## File Structure

```
nurses-processor/
│
├── process_nurses.py    # Main processing script
├── config.py            # Configuration constants and column mappings
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Technical Details

### Why Polars over Pandas?

- **Speed**: 5-10x faster for large CSV files
- **Memory**: More efficient memory usage with lazy evaluation
- **Multi-threading**: Native support for parallel processing
- **Modern**: Built in Rust for performance

### Filter Logic

**Nurse Detection**: Uses OR logic across taxonomy columns

```python
# A provider is identified as a nurse if ANY taxonomy column contains a nurse code
is_nurse = (Code_1 in NURSE_CODES) OR (Code_2 in NURSE_CODES) OR ... OR (Code_15 in NURSE_CODES)
```

**Additional Filters**: Uses AND logic

```python
# Additional filters must ALL match
result = is_nurse AND name_matches AND city_matches AND state_matches
```

### Name Matching

- **First Name / Last Name**: Case-insensitive partial match (contains)
  - Example: `--first-name "john"` matches "John", "Johnny", "Johnathan"
  
### Location Matching

- **City**: Case-insensitive partial match (contains)
  - Example: `--city "francisco"` matches "San Francisco", "Francisco City"
  
- **State**: Exact match on state code, case-insensitive
  - Example: `--state CA` matches only "CA" (not "California")

## License

This is a utility tool for processing NPI healthcare provider data. Use in accordance with CMS NPI data usage guidelines.

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Verify your CSV file structure matches the expected NPI format
3. Review error messages for specific guidance

## Credits

Developed for efficient processing of CMS National Provider Identifier (NPI) registry data files.

