#!/usr/bin/env python3
"""
Setup verification script for Nurses CSV Processor.
Run this after installing dependencies to verify everything is working.
"""

import sys

def check_python_version():
    """Check if Python version is adequate."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7+ required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_polars():
    """Check if Polars is installed."""
    try:
        import polars as pl
        print(f"✅ Polars {pl.__version__} (recommended - fast processing)")
        return True
    except ImportError:
        print("⚠️  Polars not installed (optional but recommended)")
        return False

def check_pandas():
    """Check if Pandas is installed."""
    try:
        import pandas as pd
        print(f"✅ Pandas {pd.__version__} (fallback)")
        return True
    except ImportError:
        print("❌ Pandas not installed (required)")
        return False

def check_scripts():
    """Check if main scripts exist."""
    import os
    files = {
        'process_nurses.py': 'Main processor script',
        'config.py': 'Configuration file',
        'README.md': 'Documentation',
    }
    
    all_exist = True
    for file, desc in files.items():
        if os.path.exists(file):
            print(f"✅ {file} - {desc}")
        else:
            print(f"❌ {file} missing - {desc}")
            all_exist = False
    
    return all_exist

def main():
    """Run all verification checks."""
    print("=" * 60)
    print("Nurses CSV Processor - Setup Verification")
    print("=" * 60)
    print()
    
    print("Checking Python version...")
    python_ok = check_python_version()
    print()
    
    print("Checking dependencies...")
    polars_ok = check_polars()
    pandas_ok = check_pandas()
    print()
    
    print("Checking project files...")
    files_ok = check_scripts()
    print()
    
    print("=" * 60)
    
    if python_ok and (polars_ok or pandas_ok) and files_ok:
        print("✅ Setup verified! You're ready to process CSV files.")
        print()
        print("Quick start:")
        print("  python process_nurses.py your_file.csv --output nurses.csv")
        print()
        if not polars_ok and pandas_ok:
            print("Note: For better performance, install Polars:")
            print("  pip install polars")
        print("=" * 60)
        return 0
    else:
        print("❌ Setup incomplete. Please fix the issues above.")
        print()
        if not (polars_ok or pandas_ok):
            print("Install dependencies:")
            print("  pip install -r requirements.txt")
        print("=" * 60)
        return 1

if __name__ == '__main__':
    sys.exit(main())

