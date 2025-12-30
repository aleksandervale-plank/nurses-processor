# Quick Start Guide

Get up and running with the Nurses CSV Processor in minutes.

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Basic Workflow

### Step 1: Place your CSV file

**Opção 1** (Recomendado): Coloque seu arquivo como `data.csv` na raiz do projeto

```bash
# Copie ou renomeie seu arquivo para data.csv
cp seu_arquivo_npi.csv data.csv
```

**Opção 2**: Use qualquer arquivo especificando o caminho

### Step 2: Run the processor

```bash
# Se você colocou o arquivo como data.csv (mais fácil!)
python process_nurses.py --output nurses.csv

# Ou especifique o caminho do arquivo
python process_nurses.py seu_arquivo.csv --output nurses.csv
```

### Step 3: Wait for processing

You'll see real-time progress:

```
Using Polars for processing (optimized)

Processing file: data.csv
File size: 11.23 GB
Output file: nurses.csv
Chunk size: 100,000 rows

Processing chunks...
  Chunk 1: 100,000 rows → 12,345 nurses (Total: 12,345)
  Chunk 2: 100,000 rows → 11,892 nurses (Total: 24,237)
  ...
```

### Step 4: Get your results

The filtered CSV will be saved with summary statistics:

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

## Common Use Cases

### Extract all nurses (usando data.csv padrão)

```bash
python process_nurses.py --output nurses.csv
```

### Extract nurses in your state

```bash
# California
python process_nurses.py --output nurses_ca.csv --state CA

# New York
python process_nurses.py --output nurses_ny.csv --state NY

# Texas
python process_nurses.py --output nurses_tx.csv --state TX
```

### Search by city

```bash
# Find nurses in Los Angeles
python process_nurses.py --output nurses_la.csv --city "Los Angeles"

# Find nurses in New York City
python process_nurses.py --output nurses_nyc.csv --city "New York"
```

### Search by name

```bash
# Find all nurses with last name "Garcia"
python process_nurses.py --output garcia_nurses.csv --last-name Garcia

# Find all nurses named "Maria"
python process_nurses.py --output maria_nurses.csv --first-name Maria
```

### Combine filters for precise results

```bash
# Nurses named Smith in California
python process_nurses.py --output results.csv --last-name Smith --state CA

# Nurses in San Francisco named Johnson
python process_nurses.py --output results.csv \
  --city "San Francisco" \
  --last-name Johnson \
  --state CA
```

## Performance Tips

### For faster processing (if you have 4GB+ RAM available)

```bash
python process_nurses.py --output nurses.csv --chunk-size 250000
```

### For slower computers (less than 4GB RAM)

```bash
python process_nurses.py --output nurses.csv --chunk-size 50000
```

## What Gets Filtered?

The processor finds providers with these taxonomy codes in ANY of the 15 taxonomy columns:

| Code | Type | Description |
|------|------|-------------|
| `363L00000X` | NP | Nurse Practitioner (Advanced Practice) |
| `163W00000X` | RN | Registered Nurse (most common) |
| `164W00000X` | LPN | Licensed Practical Nurse |

## Typical Results

From an 11GB NPI file with ~7.5 million records:
- **Nurses found**: ~800,000 - 1,000,000 (10-13%)
- **Processing time**: 10-20 minutes
- **Output size**: 1-2 GB
- **Memory used**: 200-500 MB (not 11 GB!)

## Next Steps

1. **Analyze results**: Open the output CSV in Excel, Python, or your preferred tool
2. **Further filtering**: Use the output as input for more specific searches
3. **Export subsets**: Process the filtered file again with additional criteria

## Getting Help

- Full documentation: See [README.md](README.md)
- Check all options: `python process_nurses.py --help`
- Common issues: See Troubleshooting section in README

## Example Output File

The output CSV will have the same columns as input, including:

- NPI number
- Provider names (first, last, middle)
- Business addresses
- Practice location addresses
- All 15 taxonomy codes
- License numbers
- And 100+ other fields from the original NPI data

You can then open this in any spreadsheet software or database for further analysis.
