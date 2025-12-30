# Installation Guide

Quick guide to get the Nurses CSV Processor up and running.

## System Requirements

- **Python**: 3.7 or higher
- **Memory**: Minimum 2GB RAM (4GB+ recommended)
- **Storage**: Space for input CSV (11GB) + output CSV (~1-2GB)
- **OS**: Linux, macOS, or Windows

## Step-by-Step Installation

### 1. Verify Python Installation

Check if Python 3.7+ is installed:

```bash
python3 --version
```

If not installed, download from [python.org](https://www.python.org/downloads/)

### 2. Navigate to Project Directory

```bash
cd /Users/aleksanderribeirovale/projects/nurses-processor
```

Or wherever you've placed the project.

### 3. Install Dependencies

#### Option A: With Polars (Recommended - Faster)

```bash
pip install polars pandas
```

Or using the requirements file:

```bash
pip install -r requirements.txt
```

#### Option B: Pandas Only (Fallback)

```bash
pip install pandas
```

**Note**: Polars is 5-10x faster than pandas for large CSV files. Highly recommended for 11GB files.

### 4. Verify Installation

Run the verification script:

```bash
python3 verify_setup.py
```

Expected output:

```
============================================================
Nurses CSV Processor - Setup Verification
============================================================

Checking Python version...
✅ Python 3.x.x

Checking dependencies...
✅ Polars x.x.x (recommended - fast processing)
✅ Pandas x.x.x (fallback)

Checking project files...
✅ process_nurses.py - Main processor script
✅ config.py - Configuration file
✅ README.md - Documentation

============================================================
✅ Setup verified! You're ready to process CSV files.
============================================================
```

## Troubleshooting Installation

### "pip: command not found"

Try using `pip3` instead:

```bash
pip3 install -r requirements.txt
```

### "Permission denied"

Use `--user` flag:

```bash
pip install --user -r requirements.txt
```

Or use a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### "Python not found" or wrong version

#### macOS/Linux:

```bash
# Install Python 3 using homebrew (macOS)
brew install python3

# Or using apt (Ubuntu/Debian)
sudo apt update
sudo apt install python3 python3-pip
```

#### Windows:

Download and install from [python.org](https://www.python.org/downloads/)

### Polars Installation Fails

If Polars installation fails (e.g., on older systems), you can still use pandas:

1. Edit `requirements.txt` and remove the polars line
2. Install just pandas: `pip install pandas`
3. The script will automatically use pandas as fallback

## Using Virtual Environments (Recommended)

Virtual environments keep dependencies isolated:

### Create Virtual Environment

```bash
# Navigate to project
cd /Users/aleksanderribeirovale/projects/nurses-processor

# Create virtual environment
python3 -m venv venv
```

### Activate Virtual Environment

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```cmd
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Deactivate When Done

```bash
deactivate
```

## Upgrading Dependencies

To upgrade to the latest versions:

```bash
pip install --upgrade polars pandas
```

## Uninstallation

To remove the dependencies:

```bash
pip uninstall polars pandas
```

To remove the entire project:

```bash
rm -rf /Users/aleksanderribeirovale/projects/nurses-processor
```

## Next Steps

After successful installation:

1. Read **QUICKSTART.md** for usage examples
2. Place your NPI CSV file in an accessible location
3. Run your first extraction:
   ```bash
   python process_nurses.py your_file.csv --output nurses.csv
   ```

## Getting Help

- **Setup issues**: Run `python3 verify_setup.py` for diagnosis
- **Usage help**: Run `python process_nurses.py --help`
- **Examples**: See QUICKSTART.md
- **Full docs**: See README.md

