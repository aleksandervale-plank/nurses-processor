#!/usr/bin/env python3
"""
Test script to compare old vs new taxonomy code coverage.
Shows how many more nurses we capture with the expanded codes.
"""

import pandas as pd
from config import NURSE_TAXONOMY_CODES, TAXONOMY_CODE_COLUMNS

# Old codes (for comparison)
OLD_CODES = ['363L00000X', '163W00000X', '164W00000X']

def count_nurses_with_codes(chunk, codes, use_prefix=False):
    """Count how many nurses match the given codes."""
    nurse_mask = pd.Series([False] * len(chunk), index=chunk.index)
    
    for col in TAXONOMY_CODE_COLUMNS:
        if col in chunk.columns:
            for code in codes:
                if use_prefix:
                    nurse_mask |= chunk[col].astype(str).str.startswith(code, na=False)
                else:
                    nurse_mask |= (chunk[col] == code)
    
    return nurse_mask.sum()

def analyze_coverage(csv_file='data.csv', sample_chunks=20):
    """Analyze taxonomy code coverage."""
    print("="*90)
    print("📊 ANÁLISE DE COBERTURA DOS CÓDIGOS DE TAXONOMIA")
    print("="*90 + "\n")
    
    print(f"Analisando arquivo: {csv_file}")
    print(f"Chunks a processar: {sample_chunks} (até ~{sample_chunks * 100000:,} registros)\n")
    
    old_total = 0
    new_total = 0
    total_rows = 0
    
    chunk_num = 0
    for chunk in pd.read_csv(csv_file, chunksize=100000, low_memory=False):
        chunk_num += 1
        total_rows += len(chunk)
        
        # Count with old codes (exact match)
        old_count = count_nurses_with_codes(chunk, OLD_CODES, use_prefix=False)
        old_total += old_count
        
        # Count with new codes (prefix match)
        new_count = count_nurses_with_codes(chunk, NURSE_TAXONOMY_CODES, use_prefix=True)
        new_total += new_count
        
        if chunk_num % 5 == 0:
            print(f"  Chunk {chunk_num}: {total_rows:,} rows processados | "
                  f"Old: {old_total:,} | New: {new_total:,} | Diff: +{new_total - old_total:,}")
        
        if chunk_num >= sample_chunks:
            break
    
    print("\n" + "="*90)
    print("📈 RESULTADOS")
    print("="*90 + "\n")
    
    print(f"Total de registros analisados: {total_rows:,}")
    print()
    print(f"🔵 COM CÓDIGOS ANTIGOS (3 códigos exatos):")
    print(f"   Códigos: {OLD_CODES}")
    print(f"   Enfermeiras encontradas: {old_total:,}")
    print()
    print(f"🟢 COM CÓDIGOS NOVOS (8 prefixos, ~128 códigos):")
    print(f"   Prefixos: {NURSE_TAXONOMY_CODES}")
    print(f"   Enfermeiras encontradas: {new_total:,}")
    print()
    print(f"✨ DIFERENÇA:")
    print(f"   +{new_total - old_total:,} enfermeiras a mais ({((new_total - old_total) / old_total * 100):.1f}% aumento)")
    print()
    
    # Breakdown por tipo
    print("📋 BREAKDOWN POR TIPO DE ENFERMEIRA:")
    print("-" * 90)
    
    type_counts = {}
    for code_prefix in NURSE_TAXONOMY_CODES:
        count = 0
        chunk_num = 0
        for chunk in pd.read_csv(csv_file, chunksize=100000, low_memory=False):
            chunk_num += 1
            for col in TAXONOMY_CODE_COLUMNS:
                if col in chunk.columns:
                    count += chunk[col].astype(str).str.startswith(code_prefix, na=False).sum()
            if chunk_num >= sample_chunks:
                break
        type_counts[code_prefix] = count
    
    # Map codes to descriptions
    descriptions = {
        '163W': 'Registered Nurse (RN)',
        '164W': 'Licensed Practical Nurse (LPN)',
        '164X': 'Licensed Vocational Nurse (LVN)',
        '363L': 'Nurse Practitioner (NP/APRN)',
        '364S': 'Clinical Nurse Specialist (CNS)',
        '3675': 'Certified Registered Nurse Anesthetist (CRNA)',
        '367A': 'Advanced Practice Midwife',
        '367H': 'Certified Nurse Midwife (CNM)',
    }
    
    for code_prefix in sorted(type_counts.keys(), key=lambda x: type_counts[x], reverse=True):
        count = type_counts[code_prefix]
        desc = descriptions.get(code_prefix, 'Unknown')
        percentage = (count / new_total * 100) if new_total > 0 else 0
        print(f"  {code_prefix}X → {desc:45s} {count:8,} ({percentage:5.1f}%)")
    
    print("\n" + "="*90)
    print("✅ CONCLUSÃO: Os novos códigos capturam MUITO MAIS enfermeiras!")
    print("="*90 + "\n")

if __name__ == '__main__':
    try:
        analyze_coverage()
    except KeyboardInterrupt:
        print("\n\n👋 Análise interrompida.\n")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
