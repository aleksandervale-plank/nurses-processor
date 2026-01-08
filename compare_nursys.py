#!/usr/bin/env python3
"""
Script para comparar dados do nursys.json com o CSV de nurses.
Encontra matches baseado em nome, sobrenome e número de licença.
"""

import json
import sys
import pandas as pd
from typing import List, Dict, Any

def load_nursys_data(json_file: str) -> List[Dict[str, Any]]:
    """Carrega dados do arquivo JSON do Nursys."""
    print(f"📂 Carregando {json_file}...")
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"✅ {len(data)} registros carregados do JSON\n")
    return data

def load_nurses_csv(csv_file: str) -> pd.DataFrame:
    """Carrega o CSV de nurses."""
    print(f"📂 Carregando {csv_file}...")
    df = pd.read_csv(csv_file, low_memory=False)
    print(f"✅ {len(df):,} registros carregados do CSV\n")
    return df

def normalize_name(name: str) -> str:
    """Normaliza um nome para comparação."""
    if pd.isna(name) or name == '':
        return ''
    return str(name).strip().upper()

def find_matches(nursys_data: List[Dict], nurses_df: pd.DataFrame) -> List[Dict]:
    """
    Encontra matches entre os dados do Nursys e o CSV de nurses.
    
    Critérios de match:
    1. Nome + Sobrenome
    2. Número de licença (se disponível no Nursys)
    """
    matches = []
    no_matches = []
    
    print("🔍 Procurando matches...\n")
    
    for idx, person in enumerate(nursys_data, 1):
        first_name = normalize_name(person.get('firstName', ''))
        last_name = normalize_name(person.get('lastName', ''))
        state = person.get('state', '')
        city = person.get('city', '')
        profile_url = person.get('profileUrl', '')
        
        # Pular se não tiver nome
        if not first_name or not last_name:
            continue
        
        # Buscar por nome no CSV
        name_matches = nurses_df[
            (nurses_df['Provider First Name'].str.upper().str.contains(first_name, na=False)) &
            (nurses_df['Provider Last Name (Legal Name)'].str.upper().str.contains(last_name, na=False))
        ]
        
        # Se encontrou matches por nome
        if len(name_matches) > 0:
            # Verificar se tem licenças no Nursys para confirmar
            nursys_licenses = person.get('nursys', {}).get('individuals', [])
            
            if len(nursys_licenses) > 0:
                # Tem licenças no Nursys, tentar match por licença
                license_confirmed = False
                
                for license_info in nursys_licenses:
                    license_number = str(license_info.get('licenseNumber', '')).strip()
                    license_state = license_info.get('state', '')
                    license_type = license_info.get('licenseType', '')
                    
                    if license_number:
                        # Buscar número de licença nas 15 colunas possíveis
                        license_cols = [f'Provider License Number_{i}' for i in range(1, 16)]
                        
                        for col in license_cols:
                            if col in name_matches.columns:
                                license_match = name_matches[
                                    name_matches[col].astype(str).str.contains(license_number, na=False, regex=False)
                                ]
                                
                                if len(license_match) > 0:
                                    license_confirmed = True
                                    matches.append({
                                        'facebook_name': person.get('name', ''),
                                        'firstName': first_name,
                                        'lastName': last_name,
                                        'city': city,
                                        'state': state,
                                        'profileUrl': profile_url,
                                        'match_type': 'NAME + LICENSE',
                                        'license_number': license_number,
                                        'license_state': license_state,
                                        'license_type': license_type,
                                        'csv_matches': len(license_match),
                                        'csv_npi': license_match.iloc[0]['NPI'] if len(license_match) > 0 else None,
                                        'csv_full_name': f"{license_match.iloc[0]['Provider First Name']} {license_match.iloc[0]['Provider Last Name (Legal Name)']}" if len(license_match) > 0 else None
                                    })
                                    break
                        
                        if license_confirmed:
                            break
                
                # Se não confirmou por licença mas tem match de nome
                if not license_confirmed:
                    matches.append({
                        'facebook_name': person.get('name', ''),
                        'firstName': first_name,
                        'lastName': last_name,
                        'city': city,
                        'state': state,
                        'profileUrl': profile_url,
                        'match_type': 'NAME ONLY (has Nursys license but not found in CSV)',
                        'license_number': nursys_licenses[0].get('licenseNumber', '') if nursys_licenses else '',
                        'license_state': nursys_licenses[0].get('state', '') if nursys_licenses else '',
                        'license_type': nursys_licenses[0].get('licenseType', '') if nursys_licenses else '',
                        'csv_matches': len(name_matches),
                        'csv_npi': name_matches.iloc[0]['NPI'] if len(name_matches) > 0 else None,
                        'csv_full_name': f"{name_matches.iloc[0]['Provider First Name']} {name_matches.iloc[0]['Provider Last Name (Legal Name)']}" if len(name_matches) > 0 else None
                    })
            else:
                # Não tem licenças no Nursys, match apenas por nome
                matches.append({
                    'facebook_name': person.get('name', ''),
                    'firstName': first_name,
                    'lastName': last_name,
                    'city': city,
                    'state': state,
                    'profileUrl': profile_url,
                    'match_type': 'NAME ONLY (no Nursys license)',
                    'license_number': '',
                    'license_state': '',
                    'license_type': '',
                    'csv_matches': len(name_matches),
                    'csv_npi': name_matches.iloc[0]['NPI'] if len(name_matches) > 0 else None,
                    'csv_full_name': f"{name_matches.iloc[0]['Provider First Name']} {name_matches.iloc[0]['Provider Last Name (Legal Name)']}" if len(name_matches) > 0 else None
                })
        else:
            # Não encontrou match
            nursys_licenses = person.get('nursys', {}).get('individuals', [])
            no_matches.append({
                'facebook_name': person.get('name', ''),
                'firstName': first_name,
                'lastName': last_name,
                'city': city,
                'state': state,
                'profileUrl': profile_url,
                'has_nursys_license': len(nursys_licenses) > 0,
                'nursys_license_count': len(nursys_licenses)
            })
        
        # Progress
        if idx % 10 == 0:
            print(f"  Processados: {idx}/{len(nursys_data)} ({len(matches)} matches até agora)")
    
    return matches, no_matches

def display_results(matches: List[Dict], no_matches: List[Dict]):
    """Exibe os resultados da comparação."""
    print("\n" + "="*100)
    print("📊 RESULTADOS DA COMPARAÇÃO")
    print("="*100)
    
    print(f"\n✅ MATCHES ENCONTRADOS: {len(matches)}")
    print("-"*100)
    
    if len(matches) > 0:
        # Agrupar por tipo de match
        name_license = [m for m in matches if 'NAME + LICENSE' in m['match_type']]
        name_only_with_license = [m for m in matches if 'has Nursys license but not found' in m['match_type']]
        name_only_no_license = [m for m in matches if 'no Nursys license' in m['match_type']]
        
        print(f"\n🎯 Matches confirmados por NOME + LICENÇA: {len(name_license)}")
        for match in name_license[:10]:  # Mostrar primeiros 10
            print(f"  • {match['facebook_name']}")
            print(f"    Nome: {match['firstName']} {match['lastName']}")
            print(f"    Licença: {match['license_number']} ({match['license_state']}, {match['license_type']})")
            print(f"    NPI no CSV: {match['csv_npi']}")
            print(f"    Profile: {match['profileUrl']}")
            print()
        
        if len(name_license) > 10:
            print(f"  ... e mais {len(name_license) - 10} matches confirmados\n")
        
        print(f"\n⚠️  Matches por NOME apenas (tem licença Nursys mas não encontrada no CSV): {len(name_only_with_license)}")
        for match in name_only_with_license[:5]:
            print(f"  • {match['facebook_name']}")
            print(f"    Licença Nursys: {match['license_number']} ({match['license_state']})")
            print(f"    Possível NPI: {match['csv_npi']}")
            print()
        
        print(f"\n📝 Matches por NOME apenas (sem licença no Nursys): {len(name_only_no_license)}")
        for match in name_only_no_license[:5]:
            print(f"  • {match['facebook_name']} - NPI: {match['csv_npi']}")
    
    print(f"\n\n❌ NÃO ENCONTRADOS NO CSV: {len(no_matches)}")
    print("-"*100)
    
    if len(no_matches) > 0:
        with_license = [m for m in no_matches if m['has_nursys_license']]
        without_license = [m for m in no_matches if not m['has_nursys_license']]
        
        print(f"\n  Com licença no Nursys: {len(with_license)}")
        for person in with_license[:5]:
            print(f"    • {person['facebook_name']} ({person['city']}, {person['state']})")
        
        print(f"\n  Sem licença no Nursys: {len(without_license)}")
        for person in without_license[:5]:
            print(f"    • {person['facebook_name']} ({person['city']}, {person['state']})")

def save_results(matches: List[Dict], no_matches: List[Dict]):
    """Salva os resultados em arquivos CSV."""
    if len(matches) > 0:
        matches_df = pd.DataFrame(matches)
        matches_df.to_csv('nursys_matches.csv', index=False)
        print(f"\n💾 Matches salvos em: nursys_matches.csv")
    
    if len(no_matches) > 0:
        no_matches_df = pd.DataFrame(no_matches)
        no_matches_df.to_csv('nursys_no_matches.csv', index=False)
        print(f"💾 Não encontrados salvos em: nursys_no_matches.csv")

def main():
    """Função principal."""
    json_file = 'nursys.json'
    csv_file = 'nurses.csv'
    
    # Verificar se os arquivos existem
    import os
    if not os.path.exists(json_file):
        print(f"❌ Erro: {json_file} não encontrado")
        sys.exit(1)
    
    if not os.path.exists(csv_file):
        print(f"❌ Erro: {csv_file} não encontrado")
        sys.exit(1)
    
    # Carregar dados
    nursys_data = load_nursys_data(json_file)
    nurses_df = load_nurses_csv(csv_file)
    
    # Encontrar matches
    matches, no_matches = find_matches(nursys_data, nurses_df)
    
    # Exibir resultados
    display_results(matches, no_matches)
    
    # Salvar resultados
    save_results(matches, no_matches)
    
    print("\n" + "="*100)
    print("✅ Comparação concluída!")
    print("="*100 + "\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrompido. Até logo!\n")
        sys.exit(0)

