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

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Verify Setup (Optional)

```bash
python3 verify_setup.py
```

### 3. Process Your CSV

Place your NPI CSV file as `data.csv` in the project root, or specify any file:

```bash
# Uses data.csv automatically (recommended)
python process_nurses.py --output nurses.csv

# Or specify a different file
python process_nurses.py your_file.csv --output nurses.csv
```

### 4. Explore Results

Use the interactive viewer to explore and filter results:

```bash
python view_nurses.py
```

## Installation

### System Requirements

- **Python**: 3.7 or higher
- **Memory**: Minimum 2GB RAM (4GB+ recommended)
- **Storage**: Space for input CSV (11GB) + output CSV (~1-2GB)
- **OS**: Linux, macOS, or Windows

### Step-by-Step Installation

1. **Verify Python Installation**

```bash
python3 --version
```

If not installed, download from [python.org](https://www.python.org/downloads/)

2. **Install Dependencies**

**Recommended (with Polars - faster)**:

```bash
pip install -r requirements.txt
```

**Or manually**:

```bash
pip install polars pandas tabulate
```

**Fallback (Pandas only - slower)**:

```bash
pip install pandas tabulate
```

3. **Verify Installation**

```bash
python3 verify_setup.py
```

### Using Virtual Environments (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Deactivate when done
deactivate
```

### Dependencies

- **polars** (recommended): Fast DataFrame library for large file processing - 5-10x faster than pandas
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
# Uses data.csv automatically if placed in project root (recommended)
python process_nurses.py --output nurses.csv

# Or specify a different file
python process_nurses.py your_file.csv --output nurses.csv
```

**Note**: If you place your NPI CSV file as `data.csv` in the project root, the script will use it automatically without needing to specify the filename.

### Interactive Viewer

After processing, use the interactive viewer to explore results **without creating new files**:

```bash
python view_nurses.py
```

**Features:**

- Filter by name, city, state
- View statistics (distribution by state, city, nurse types)
- Beautiful formatted tables with pagination
- Quick search functionality
- Export filtered results (optional)
- No new files created unless you explicitly export

**Menu Options:**

1. View results - Display data in formatted table
2. Filter by first name - Search by first name (partial match)
3. Filter by last name - Search by last name (partial match)
4. Filter by city - Search by city (partial match)
5. Filter by state - Search by state code (exact match)
6. Clear filters - Remove all active filters
7. View statistics - See distribution statistics
8. Export results - Save filtered results to CSV (optional)
9. Quick search - Fast search by full name
10. Exit - Close the program

**Example Workflow:**

```
1. Run: python view_nurses.py
2. Choose option 4 (Filter by city)
3. Enter: "Los Angeles"
4. Choose option 5 (Filter by state)
5. Enter: "CA"
6. Choose option 1 (View results)
7. Browse through the filtered results
```

The viewer automatically uses `nurses.csv` from the project root. All filters are combined with AND logic (all must match).

### Filter by State

Extract nurses in a specific state:

```bash
# Using default data.csv
python process_nurses.py --output nurses_ca.csv --state CA

# Or with specific file
python process_nurses.py your_file.csv --output nurses_ca.csv --state CA
```

### Filter by City

Extract nurses in a specific city:

```bash
python process_nurses.py --output nurses_la.csv --city "Los Angeles"
```

### Filter by Name

Extract nurses by first name:

```bash
python process_nurses.py --output nurses_john.csv --first-name John
```

Extract nurses by last name:

```bash
python process_nurses.py --output nurses_smith.csv --last-name Smith
```

### Combine Multiple Filters

All filters are applied as AND conditions (all must match):

```bash
python process_nurses.py --output results.csv \
  --state CA \
  --city "San Francisco" \
  --last-name Smith
```

### Common Use Cases

**Extract all nurses:**

```bash
python process_nurses.py --output nurses.csv
```

**California nurses:**

```bash
python process_nurses.py --output nurses_ca.csv --state CA
```

**Nurses in Los Angeles:**

```bash
python process_nurses.py --output nurses_la.csv --city "Los Angeles"
```

**Nurses with last name Garcia in California:**

```bash
python process_nurses.py --output results.csv --last-name Garcia --state CA
```

### Adjust Performance

For systems with more memory (8GB+ RAM), increase chunk size for faster processing:

```bash
python process_nurses.py --output nurses.csv --chunk-size 250000
```

_Processes faster (8-12 minutes)_

For systems with less memory (4GB RAM), decrease chunk size:

```bash
python process_nurses.py --output nurses.csv --chunk-size 50000
```

_Processes slower but uses less RAM_

## Command-Line Options

```
positional arguments:
  input_file            Path to input CSV file (optional, defaults to data.csv in project root)

optional arguments:
  -h, --help            Show help message and exit
  --output, -o          Path to output CSV file (default: nurses_filtered.csv)
  --chunk-size          Number of rows to process at a time (default: 100,000)
  --first-name          Filter by provider first name (case-insensitive partial match)
  --last-name           Filter by provider last name (case-insensitive partial match)
  --city                Filter by city (case-insensitive partial match)
  --state               Filter by state code (e.g., CA, NY, TX)

Examples:
  python process_nurses.py --output nurses.csv
  python process_nurses.py --output nurses_ca.csv --state CA
  python process_nurses.py file.csv --output output.csv --city "Los Angeles"
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

- Make sure `data.csv` exists in the project root, or
- Specify the correct path to your CSV file:

```bash
python process_nurses.py /full/path/to/npi_data.csv --output nurses.csv
```

### Memory Issues

If you encounter memory errors, reduce the chunk size:

```bash
python process_nurses.py --output nurses.csv --chunk-size 50000
```

Or install dependencies with `--user` flag:

```bash
pip install --user -r requirements.txt
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
4. Run `python process_nurses.py --help` to verify filter syntax

### "tabulate not installed" (Viewer)

If the viewer shows a warning about tabulate:

```bash
pip install tabulate
```

The viewer will work without it, but table formatting will be simpler.

### "nurses.csv not found" (Viewer)

Make sure you've processed the CSV first:

```bash
python process_nurses.py --output nurses.csv
```

Then run the viewer:

```bash
python view_nurses.py
```

### Installation Issues

**"pip: command not found"**

- Try `pip3` instead of `pip`
- Or install pip: `python3 -m ensurepip --upgrade`

**"Permission denied"**

- Use `--user` flag: `pip install --user -r requirements.txt`
- Or use a virtual environment (recommended)

## File Structure

```
nurses-processor/
│
├── data.csv             # Input NPI CSV file (place your file here, optional)
├── nurses.csv           # Output file (generated after processing)
│
├── process_nurses.py    # Main processing script
├── view_nurses.py       # Interactive viewer for exploring results
├── config.py            # Configuration constants and column mappings
├── verify_setup.py      # Setup verification script
├── example_commands.sh  # Interactive command helper (optional)
│
├── requirements.txt     # Python dependencies
└── README.md           # This file (complete documentation)
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

## Expected Results

### Typical Processing Output

**Input**: 11 GB, ~7.5M records  
**Output**: 1-2 GB, ~800K-1M nurses (10-13%)  
**Processing Time**:

- With Polars: 10-15 minutes
- With Pandas: 20-30 minutes
  **Memory Usage**: 200-500 MB (not 11 GB!)

### Processing Output Example

```
Using Polars for processing (optimized)

Processing file: data.csv
File size: 10.00 GB
Output file: nurses.csv
Chunk size: 100,000 rows

Processing chunks...
  Chunk 1: 100,000 rows → 12,345 nurses (Total: 12,345)
  Chunk 2: 100,000 rows → 11,892 nurses (Total: 24,237)
  ...

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

## Support

For issues or questions:

1. Check the Troubleshooting section above
2. Run `python3 verify_setup.py` to verify your installation
3. Verify your CSV file structure matches the expected NPI format
4. Review error messages for specific guidance
5. Check `python process_nurses.py --help` for command syntax

## Credits

Developed for efficient processing of CMS National Provider Identifier (NPI) registry data files.
