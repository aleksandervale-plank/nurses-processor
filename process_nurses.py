#!/usr/bin/env python3
"""
Nurses CSV Processor - Efficiently process large NPI healthcare provider CSV files
to extract and filter nurse records.

This script uses chunked processing to handle very large CSV files (11GB+) without
loading them entirely into memory.
"""

import argparse
import sys
import os
from pathlib import Path
from typing import Optional, List

# Try to import polars first (faster), fall back to pandas
try:
    import polars as pl
    USE_POLARS = True
    print("Using Polars for processing (optimized)")
except ImportError:
    import pandas as pd
    USE_POLARS = False
    print("Using Pandas for processing (Polars not found)")

from config import (
    NURSE_TAXONOMY_CODES,
    TAXONOMY_CODE_COLUMNS,
    FILTER_COLUMNS,
    DEFAULT_CHUNK_SIZE,
    DEFAULT_OUTPUT_FILE
)


def get_file_size(file_path: str) -> int:
    """Get file size in bytes."""
    return os.path.getsize(file_path)


def format_size(bytes_size: int) -> str:
    """Format bytes to human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"


def filter_nurses_polars(
    input_file: str,
    output_file: str,
    chunk_size: int,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
) -> dict:
    """
    Filter nurses from CSV using Polars (faster for large files).
    
    Args:
        input_file: Path to input CSV file
        output_file: Path to output CSV file
        chunk_size: Number of rows to process at a time
        first_name: Filter by provider first name (case-insensitive partial match)
        last_name: Filter by provider last name (case-insensitive partial match)
        city: Filter by city (case-insensitive partial match)
        state: Filter by state code (exact match, case-insensitive)
    
    Returns:
        Dictionary with processing statistics
    """
    total_rows = 0
    filtered_rows = 0
    first_chunk = True
    
    print(f"\nProcessing file: {input_file}")
    print(f"File size: {format_size(get_file_size(input_file))}")
    print(f"Output file: {output_file}")
    print(f"Chunk size: {chunk_size:,} rows")
    
    # Build filter description
    filters_applied = []
    if first_name:
        filters_applied.append(f"First name contains '{first_name}'")
    if last_name:
        filters_applied.append(f"Last name contains '{last_name}'")
    if city:
        filters_applied.append(f"City contains '{city}'")
    if state:
        filters_applied.append(f"State = '{state}'")
    
    if filters_applied:
        print(f"Filters: {', '.join(filters_applied)}")
    
    print("\nProcessing chunks...")
    
    # Process CSV in chunks using Polars
    reader = pl.read_csv_batched(
        input_file,
        batch_size=chunk_size,
        low_memory=True,
        ignore_errors=True,
    )
    
    chunk_num = 0
    while True:
        try:
            # Read next chunk
            chunk = reader.next_batches(1)
            if chunk is None or len(chunk) == 0:
                break
            
            df = chunk[0]
            chunk_num += 1
            total_rows += len(df)
            
            # Filter for nurses: check if ANY taxonomy code column contains a nurse code
            nurse_filter = pl.lit(False)
            for col in TAXONOMY_CODE_COLUMNS:
                if col in df.columns:
                    for code in NURSE_TAXONOMY_CODES:
                        nurse_filter = nurse_filter | (df[col] == code)
            
            df_filtered = df.filter(nurse_filter)
            
            # Apply additional filters
            if first_name and FILTER_COLUMNS['first_name'] in df_filtered.columns:
                df_filtered = df_filtered.filter(
                    pl.col(FILTER_COLUMNS['first_name']).str.to_lowercase().str.contains(first_name.lower())
                )
            
            if last_name and FILTER_COLUMNS['last_name'] in df_filtered.columns:
                df_filtered = df_filtered.filter(
                    pl.col(FILTER_COLUMNS['last_name']).str.to_lowercase().str.contains(last_name.lower())
                )
            
            if city and FILTER_COLUMNS['city'] in df_filtered.columns:
                df_filtered = df_filtered.filter(
                    pl.col(FILTER_COLUMNS['city']).str.to_lowercase().str.contains(city.lower())
                )
            
            if state and FILTER_COLUMNS['state'] in df_filtered.columns:
                df_filtered = df_filtered.filter(
                    pl.col(FILTER_COLUMNS['state']).str.to_uppercase() == state.upper()
                )
            
            chunk_filtered = len(df_filtered)
            filtered_rows += chunk_filtered
            
            # Write to output file
            if chunk_filtered > 0:
                if first_chunk:
                    df_filtered.write_csv(output_file)
                    first_chunk = False
                else:
                    # Append to existing file
                    with open(output_file, 'ab') as f:
                        df_filtered.write_csv(f, include_header=False)
            
            print(f"  Chunk {chunk_num}: {len(df):,} rows → {chunk_filtered:,} nurses (Total: {filtered_rows:,})")
            
        except StopIteration:
            break
        except Exception as e:
            print(f"  Warning: Error processing chunk {chunk_num}: {e}")
            continue
    
    return {
        'total_rows': total_rows,
        'filtered_rows': filtered_rows,
        'chunks_processed': chunk_num
    }


def filter_nurses_pandas(
    input_file: str,
    output_file: str,
    chunk_size: int,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
) -> dict:
    """
    Filter nurses from CSV using Pandas (fallback method).
    
    Args:
        input_file: Path to input CSV file
        output_file: Path to output CSV file
        chunk_size: Number of rows to process at a time
        first_name: Filter by provider first name (case-insensitive partial match)
        last_name: Filter by provider last name (case-insensitive partial match)
        city: Filter by city (case-insensitive partial match)
        state: Filter by state code (exact match, case-insensitive)
    
    Returns:
        Dictionary with processing statistics
    """
    total_rows = 0
    filtered_rows = 0
    first_chunk = True
    
    print(f"\nProcessing file: {input_file}")
    print(f"File size: {format_size(get_file_size(input_file))}")
    print(f"Output file: {output_file}")
    print(f"Chunk size: {chunk_size:,} rows")
    
    # Build filter description
    filters_applied = []
    if first_name:
        filters_applied.append(f"First name contains '{first_name}'")
    if last_name:
        filters_applied.append(f"Last name contains '{last_name}'")
    if city:
        filters_applied.append(f"City contains '{city}'")
    if state:
        filters_applied.append(f"State = '{state}'")
    
    if filters_applied:
        print(f"Filters: {', '.join(filters_applied)}")
    
    print("\nProcessing chunks...")
    
    # Process CSV in chunks using Pandas
    chunk_num = 0
    for chunk in pd.read_csv(input_file, chunksize=chunk_size, low_memory=False, on_bad_lines='skip'):
        chunk_num += 1
        total_rows += len(chunk)
        
        # Filter for nurses: check if ANY taxonomy code column contains a nurse code
        nurse_mask = pd.Series([False] * len(chunk), index=chunk.index)
        for col in TAXONOMY_CODE_COLUMNS:
            if col in chunk.columns:
                for code in NURSE_TAXONOMY_CODES:
                    nurse_mask |= (chunk[col] == code)
        
        df_filtered = chunk[nurse_mask]
        
        # Apply additional filters
        if first_name and FILTER_COLUMNS['first_name'] in df_filtered.columns:
            df_filtered = df_filtered[
                df_filtered[FILTER_COLUMNS['first_name']].str.lower().str.contains(first_name.lower(), na=False)
            ]
        
        if last_name and FILTER_COLUMNS['last_name'] in df_filtered.columns:
            df_filtered = df_filtered[
                df_filtered[FILTER_COLUMNS['last_name']].str.lower().str.contains(last_name.lower(), na=False)
            ]
        
        if city and FILTER_COLUMNS['city'] in df_filtered.columns:
            df_filtered = df_filtered[
                df_filtered[FILTER_COLUMNS['city']].str.lower().str.contains(city.lower(), na=False)
            ]
        
        if state and FILTER_COLUMNS['state'] in df_filtered.columns:
            df_filtered = df_filtered[
                df_filtered[FILTER_COLUMNS['state']].str.upper() == state.upper()
            ]
        
        chunk_filtered = len(df_filtered)
        filtered_rows += chunk_filtered
        
        # Write to output file
        if chunk_filtered > 0:
            df_filtered.to_csv(
                output_file,
                mode='w' if first_chunk else 'a',
                header=first_chunk,
                index=False
            )
            first_chunk = False
        
        print(f"  Chunk {chunk_num}: {len(chunk):,} rows → {chunk_filtered:,} nurses (Total: {filtered_rows:,})")
    
    return {
        'total_rows': total_rows,
        'filtered_rows': filtered_rows,
        'chunks_processed': chunk_num
    }


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Process large NPI CSV files to extract nurse records.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract all nurses (usando data.csv da raiz do projeto)
  python process_nurses.py --output nurses.csv
  
  # Ou especifique um arquivo
  python process_nurses.py npi_data.csv --output nurses.csv
  
  # Filter nurses in California
  python process_nurses.py --output nurses_ca.csv --state CA
  
  # Filter by name and city
  python process_nurses.py --output results.csv --last-name Smith --city "Los Angeles"
  
  # Use custom chunk size for better performance
  python process_nurses.py --output nurses.csv --chunk-size 250000

Nurse Taxonomy Codes Filtered:
  - 363L00000X: Nurse Practitioner
  - 163W00000X: Registered Nurse (RN)
  - 164W00000X: Licensed Practical Nurse (LPN)
        """
    )
    
    parser.add_argument(
        'input_file',
        nargs='?',
        default='data.csv',
        help='Path to input CSV file (default: data.csv na raiz do projeto)'
    )
    
    parser.add_argument(
        '--output', '-o',
        dest='output_file',
        default=DEFAULT_OUTPUT_FILE,
        help=f'Path to output CSV file (default: {DEFAULT_OUTPUT_FILE})'
    )
    
    parser.add_argument(
        '--chunk-size',
        type=int,
        default=DEFAULT_CHUNK_SIZE,
        help=f'Number of rows to process at a time (default: {DEFAULT_CHUNK_SIZE:,})'
    )
    
    parser.add_argument(
        '--first-name',
        help='Filter by provider first name (case-insensitive partial match)'
    )
    
    parser.add_argument(
        '--last-name',
        help='Filter by provider last name (case-insensitive partial match)'
    )
    
    parser.add_argument(
        '--city',
        help='Filter by city (case-insensitive partial match)'
    )
    
    parser.add_argument(
        '--state',
        help='Filter by state code (e.g., CA, NY, TX)'
    )
    
    args = parser.parse_args()
    
    # Get the script directory (project root)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # If input_file is relative, make it relative to script directory
    if not os.path.isabs(args.input_file):
        args.input_file = os.path.join(script_dir, args.input_file)
    
    # Validate input file
    if not os.path.exists(args.input_file):
        print(f"Erro: Arquivo '{args.input_file}' não encontrado.")
        print(f"\nDica: Coloque o arquivo 'data.csv' na raiz do projeto:")
        print(f"  {script_dir}/data.csv")
        print(f"\nOu especifique o caminho completo do arquivo:")
        print(f"  python process_nurses.py /caminho/para/arquivo.csv --output nurses.csv")
        sys.exit(1)
    
    # Check if output file already exists
    if os.path.exists(args.output_file):
        response = input(f"Warning: Output file '{args.output_file}' already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Aborted.")
            sys.exit(0)
    
    # Process the file
    try:
        if USE_POLARS:
            stats = filter_nurses_polars(
                args.input_file,
                args.output_file,
                args.chunk_size,
                args.first_name,
                args.last_name,
                args.city,
                args.state
            )
        else:
            stats = filter_nurses_pandas(
                args.input_file,
                args.output_file,
                args.chunk_size,
                args.first_name,
                args.last_name,
                args.city,
                args.state
            )
        
        # Print summary
        print("\n" + "="*60)
        print("PROCESSING COMPLETE")
        print("="*60)
        print(f"Total rows processed: {stats['total_rows']:,}")
        print(f"Nurses found: {stats['filtered_rows']:,}")
        print(f"Chunks processed: {stats['chunks_processed']:,}")
        
        if stats['total_rows'] > 0:
            percentage = (stats['filtered_rows'] / stats['total_rows']) * 100
            print(f"Percentage: {percentage:.2f}%")
        
        if stats['filtered_rows'] > 0:
            print(f"\nOutput saved to: {args.output_file}")
            print(f"Output size: {format_size(get_file_size(args.output_file))}")
        else:
            print("\nNo matching records found.")
            if os.path.exists(args.output_file):
                os.remove(args.output_file)
        
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n\nProcessing interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

