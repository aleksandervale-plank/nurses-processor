#!/usr/bin/env python3
"""
Visualizador Interativo de Enfermeiras
Permite visualizar e filtrar o arquivo nurses.csv de forma bonita e interativa.
"""

import sys
import os
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# Try to import required libraries
try:
    import pandas as pd
except ImportError:
    print("Erro: pandas não está instalado.")
    print("Instale com: pip install pandas")
    sys.exit(1)

try:
    from tabulate import tabulate
except ImportError:
    print("⚠️  tabulate não está instalado (recomendado para melhor visualização)")
    print("Instale com: pip install tabulate")
    print("\nContinuando com visualização básica...\n")
    tabulate = None


def clear_screen():
    """Limpa a tela do terminal."""
    os.system('clear' if os.name != 'nt' else 'cls')


def format_value(value, max_length=30):
    """Formata um valor para exibição, truncando se necessário."""
    if pd.isna(value) or value == '':
        return '-'
    value_str = str(value)
    if len(value_str) > max_length:
        return value_str[:max_length-3] + '...'
    return value_str


def format_phone(value):
    """Formata um número de telefone para exibição."""
    if pd.isna(value) or value == '':
        return '-'
    
    # Se for número (int, float, numpy int64, etc), converter para inteiro primeiro
    # Isso evita notação científica
    try:
        if isinstance(value, (int, float)) or str(type(value)).find('int') != -1 or str(type(value)).find('float') != -1:
            phone_num = int(value)
            return str(phone_num)
    except (ValueError, OverflowError, TypeError):
        pass
    
    # Converter para string
    phone_str = str(value)
    
    # Se for notação científica em string, converter para inteiro primeiro
    if 'e+' in phone_str.lower() or 'e-' in phone_str.lower():
        try:
            phone_num = int(float(phone_str))
            phone_str = str(phone_num)
        except (ValueError, OverflowError):
            pass
    
    # Remover '.0' no final se existir (de floats convertidos)
    if phone_str.endswith('.0'):
        phone_str = phone_str[:-2]
    
    # Remover 'nan' string
    if phone_str.lower() == 'nan':
        return '-'
    
    return phone_str


def display_results(df, page_size=20, page=1):
    """Exibe os resultados de forma paginada e formatada."""
    if len(df) == 0:
        print("\n❌ Nenhum resultado encontrado com os filtros aplicados.\n")
        return
    
    total_pages = (len(df) - 1) // page_size + 1
    start_idx = (page - 1) * page_size
    end_idx = min(start_idx + page_size, len(df))
    
    # Selecionar colunas importantes para exibir
    display_columns = [
        'NPI',
        'Provider First Name',
        'Provider Last Name (Legal Name)',
        'Provider Credential Text',
        'Provider License Number_1',
        'Provider License Number State Code_1',
        'Provider Business Practice Location Address Telephone Number'
    ]
    
    # Filtrar apenas colunas que existem no DataFrame
    available_columns = [col for col in display_columns if col in df.columns]
    
    df_page = df.iloc[start_idx:end_idx][available_columns].copy()
    
    # Renomear colunas para exibição mais limpa
    column_names = {
        'NPI': 'NPI',
        'Provider First Name': 'Nome',
        'Provider Last Name (Legal Name)': 'Sobrenome',
        'Provider Credential Text': 'Tipo Licença',
        'Provider License Number_1': 'Licença',
        'Provider License Number State Code_1': 'Estado Licença',
        'Provider Business Practice Location Address Telephone Number': 'Telefone'
    }
    
    df_page = df_page.rename(columns={k: v for k, v in column_names.items() if k in df_page.columns})
    
    # Formatar valores
    for col in df_page.columns:
        if col == 'NPI':
            continue  # Manter NPI completo
        if col == 'Telefone':
            # Formatação especial para telefone: remove '.0' se for número float convertido
            df_page[col] = df_page[col].apply(lambda x: format_phone(x))
        else:
            df_page[col] = df_page[col].apply(lambda x: format_value(x, 25 if col in ['Nome', 'Sobrenome'] else 20))
    
    print("\n" + "="*100)
    print(f"📊 RESULTADOS: Mostrando {start_idx+1}-{end_idx} de {len(df)} enfermeiras")
    print("="*100 + "\n")
    
    if tabulate:
        print(tabulate(df_page, headers='keys', tablefmt='grid', showindex=False))
    else:
        print(df_page.to_string(index=False))
    
    print("\n" + "="*100)
    print(f"Página {page} de {total_pages}")
    print("="*100 + "\n")


def get_filter_summary(filters):
    """Retorna um resumo dos filtros aplicados."""
    if not any(filters.values()):
        return "Nenhum filtro aplicado"
    
    parts = []
    if filters.get('first_name'):
        parts.append(f"Nome: '{filters['first_name']}'")
    if filters.get('last_name'):
        parts.append(f"Sobrenome: '{filters['last_name']}'")
    if filters.get('city'):
        parts.append(f"Cidade: '{filters['city']}'")
    if filters.get('state'):
        parts.append(f"Estado: '{filters['state']}'")
    if filters.get('license_number'):
        parts.append(f"Licença: '{filters['license_number']}'")
    if filters.get('different_addresses'):
        parts.append("Endereços diferentes (practice ≠ mailing)")
    if filters.get('no_practice_address'):
        parts.append("Sem endereço de prática")
    if filters.get('recent_update'):
        parts.append("Atualizado nos últimos 3 meses")
    
    return " | ".join(parts)


def apply_filters(df, filters):
    """Aplica os filtros ao DataFrame."""
    filtered_df = df.copy()
    
    if filters.get('first_name'):
        col = 'Provider First Name'
        if col in filtered_df.columns:
            filtered_df = filtered_df[
                filtered_df[col].str.lower().str.contains(filters['first_name'].lower(), na=False)
            ]
    
    if filters.get('last_name'):
        col = 'Provider Last Name (Legal Name)'
        if col in filtered_df.columns:
            filtered_df = filtered_df[
                filtered_df[col].str.lower().str.contains(filters['last_name'].lower(), na=False)
            ]
    
    if filters.get('city'):
        col = 'Provider Business Practice Location Address City Name'
        if col in filtered_df.columns:
            filtered_df = filtered_df[
                filtered_df[col].str.lower().str.contains(filters['city'].lower(), na=False)
            ]
    
    if filters.get('state'):
        col = 'Provider Business Practice Location Address State Name'
        if col in filtered_df.columns:
            filtered_df = filtered_df[
                filtered_df[col].str.upper() == filters['state'].upper()
            ]
    
    # Filter by license number (searches across all 15 license columns)
    if filters.get('license_number'):
        license_cols = [f'Provider License Number_{i}' for i in range(1, 16)]
        license_mask = pd.Series([False] * len(filtered_df), index=filtered_df.index)
        
        for col in license_cols:
            if col in filtered_df.columns:
                # Convert to string and do partial match (case-insensitive)
                license_mask |= filtered_df[col].astype(str).str.lower().str.contains(
                    filters['license_number'].lower(), na=False, regex=False
                )
        
        filtered_df = filtered_df[license_mask]
    
    # Filter by different addresses (practice vs mailing)
    if filters.get('different_addresses'):
        practice_addr = 'Provider First Line Business Practice Location Address'
        mailing_addr = 'Provider First Line Business Mailing Address'
        if practice_addr in filtered_df.columns and mailing_addr in filtered_df.columns:
            # Compare addresses (normalize for comparison)
            filtered_df = filtered_df[
                filtered_df[practice_addr].notna() &
                filtered_df[mailing_addr].notna() &
                (filtered_df[practice_addr].astype(str).str.strip() != filtered_df[mailing_addr].astype(str).str.strip())
            ]
    
    # Filter by no practice address (not working)
    if filters.get('no_practice_address'):
        practice_addr_col = 'Provider First Line Business Practice Location Address'
        if practice_addr_col in filtered_df.columns:
            filtered_df = filtered_df[
                filtered_df[practice_addr_col].isna() | 
                (filtered_df[practice_addr_col].astype(str).str.strip() == "")
            ]
    
    # Filter by recent update (last 3 months) - for newly graduated/registered nurses
    if filters.get('recent_update'):
        update_col = 'Last Update Date'
        if update_col in filtered_df.columns:
            # Calculate date 3 months ago
            three_months_ago = datetime.now() - relativedelta(months=3)
            
            # Convert date strings to datetime, handling MM/DD/YYYY format
            def parse_date(date_str):
                if pd.isna(date_str) or date_str == '':
                    return None
                try:
                    # Try MM/DD/YYYY format
                    return datetime.strptime(str(date_str).strip(), '%m/%d/%Y')
                except (ValueError, TypeError):
                    return None
            
            # Filter rows where update date is within last 3 months
            filtered_df['_parsed_date'] = filtered_df[update_col].apply(parse_date)
            filtered_df = filtered_df[
                filtered_df['_parsed_date'].notna() &
                (filtered_df['_parsed_date'] >= three_months_ago)
            ]
            # Remove temporary column
            filtered_df = filtered_df.drop(columns=['_parsed_date'], errors='ignore')
    
    return filtered_df


def show_statistics(df):
    """Mostra estatísticas do dataset."""
    print("\n" + "="*60)
    print("📊 ESTATÍSTICAS DO ARQUIVO")
    print("="*60)
    print(f"Total de enfermeiras: {len(df):,}")
    
    # Estatísticas por estado
    state_col = 'Provider Business Practice Location Address State Name'
    if state_col in df.columns:
        print("\n🗺️  Top 10 Estados:")
        top_states = df[state_col].value_counts().head(10)
        for state, count in top_states.items():
            if pd.notna(state):
                print(f"  {state}: {count:,}")
    
    # Estatísticas por código de taxonomia
    taxonomy_col = 'Healthcare Provider Taxonomy Code_1'
    if taxonomy_col in df.columns:
        print("\n🏥 Tipos de Enfermeiras:")
        taxonomy_map = {
            '363L00000X': 'Nurse Practitioner (NP)',
            '163W00000X': 'Registered Nurse (RN)',
            '164W00000X': 'Licensed Practical Nurse (LPN)'
        }
        for code, name in taxonomy_map.items():
            count = (df[taxonomy_col] == code).sum()
            if count > 0:
                percentage = (count / len(df)) * 100
                print(f"  {name}: {count:,} ({percentage:.1f}%)")
    
    print("="*60 + "\n")


def export_filtered(df, filename="filtered_results.csv"):
    """Exporta resultados filtrados para um arquivo."""
    try:
        df.to_csv(filename, index=False)
        print(f"\n✅ Resultados exportados para: {filename}")
        print(f"   Total de registros: {len(df):,}\n")
        return True
    except Exception as e:
        print(f"\n❌ Erro ao exportar: {e}\n")
        return False


def main():
    """Main function."""
    # Get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_file = os.path.join(script_dir, 'nurses.csv')
    
    # Check if file exists
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    else:
        csv_file = default_file
    
    if not os.path.exists(csv_file):
        print(f"❌ Erro: Arquivo '{csv_file}' não encontrado.")
        print(f"\nUso: python view_nurses.py [caminho_para_nurses.csv]")
        print(f"Padrão: {default_file}")
        sys.exit(1)
    
    print("\n🏥 Carregando arquivo de enfermeiras...")
    print(f"📁 Arquivo: {os.path.basename(csv_file)}")
    
    try:
        df = pd.read_csv(csv_file, low_memory=False)
        print(f"✅ {len(df):,} registros carregados!\n")
    except Exception as e:
        print(f"❌ Erro ao carregar arquivo: {e}")
        sys.exit(1)
    
    # Initialize filters
    filters = {
        'first_name': None,
        'last_name': None,
        'city': None,
        'state': None,
        'license_number': None,
        'different_addresses': False,
        'no_practice_address': False,
        'recent_update': False
    }
    
    current_page = 1
    filtered_df = df.copy()
    
    while True:
        clear_screen()
        print("\n" + "="*60)
        print("🏥 VISUALIZADOR DE ENFERMEIRAS")
        print("="*60)
        print(f"\n📊 Total no arquivo: {len(df):,} enfermeiras")
        print(f"🔍 Filtros ativos: {get_filter_summary(filters)}")
        print(f"📋 Resultados filtrados: {len(filtered_df):,} enfermeiras")
        print("\n" + "="*60)
        print("\nOPÇÕES:")
        print("  1) Ver resultados")
        print("  2) Filtrar por nome")
        print("  3) Filtrar por sobrenome")
        print("  4) Filtrar por cidade")
        print("  5) Filtrar por estado")
        print("  6) Filtrar por número de licença")
        print("  7) Limpar filtros")
        print("  8) Ver estatísticas")
        print("  9) Exportar resultados filtrados")
        print(" 10) Busca rápida (nome completo)")
        print(" 11) Filtrar: endereços diferentes (practice ≠ mailing)")
        print(" 12) Filtrar: sem endereço de prática (não está trabalhando)")
        print(" 13) Filtrar: atualizado nos últimos 3 meses (recém-formados/cadastrados)")
        print("  0) Sair")
        print("="*60)
        
        choice = input("\nEscolha uma opção: ").strip()
        
        if choice == '0':
            print("\n👋 Até logo!\n")
            break
        
        elif choice == '1':
            while True:
                clear_screen()
                display_results(filtered_df, page_size=20, page=current_page)
                
                total_pages = (len(filtered_df) - 1) // 20 + 1
                if total_pages > 1:
                    nav = input("\nNavegação: [n]próxima [p]anterior [v]voltar: ").strip().lower()
                    if nav == 'n' and current_page < total_pages:
                        current_page += 1
                    elif nav == 'p' and current_page > 1:
                        current_page -= 1
                    elif nav == 'v':
                        current_page = 1
                        break
                    # Se não foi 'v', continua no loop mostrando a nova página
                else:
                    input("\nPressione Enter para continuar...")
                    break
        
        elif choice == '2':
            first_name = input("\nDigite o nome (ou Enter para limpar): ").strip()
            filters['first_name'] = first_name if first_name else None
            filtered_df = apply_filters(df, filters)
            current_page = 1
        
        elif choice == '3':
            last_name = input("\nDigite o sobrenome (ou Enter para limpar): ").strip()
            filters['last_name'] = last_name if last_name else None
            filtered_df = apply_filters(df, filters)
            current_page = 1
        
        elif choice == '4':
            city = input("\nDigite a cidade (ou Enter para limpar): ").strip()
            filters['city'] = city if city else None
            filtered_df = apply_filters(df, filters)
            current_page = 1
        
        elif choice == '5':
            state = input("\nDigite o código do estado (ex: CA, NY) ou Enter para limpar: ").strip()
            filters['state'] = state if state else None
            filtered_df = apply_filters(df, filters)
            current_page = 1
        
        elif choice == '6':
            license_num = input("\nDigite o número de licença (ou Enter para limpar): ").strip()
            filters['license_number'] = license_num if license_num else None
            filtered_df = apply_filters(df, filters)
            current_page = 1
        
        elif choice == '7':
            filters = {
                'first_name': None,
                'last_name': None,
                'city': None,
                'state': None,
                'license_number': None,
                'different_addresses': False,
                'no_practice_address': False,
                'recent_update': False
            }
            filtered_df = df.copy()
            current_page = 1
            print("\n✅ Filtros limpos!")
            input("Pressione Enter para continuar...")
        
        elif choice == '8':
            clear_screen()
            if len(filtered_df) > 0:
                show_statistics(filtered_df)
            else:
                print("\n❌ Nenhum resultado para mostrar estatísticas.\n")
            input("Pressione Enter para continuar...")
        
        elif choice == '8':
            if len(filtered_df) > 0:
                filename = input("\nNome do arquivo (Enter para 'filtered_results.csv'): ").strip()
                if not filename:
                    filename = "filtered_results.csv"
                if not filename.endswith('.csv'):
                    filename += '.csv'
                export_filtered(filtered_df, filename)
                input("Pressione Enter para continuar...")
            else:
                print("\n❌ Nenhum resultado para exportar.\n")
                input("Pressione Enter para continuar...")
        
        elif choice == '10':
            clear_screen()
            print("\n🔍 BUSCA RÁPIDA")
            print("="*60)
            search_term = input("Digite nome ou sobrenome para buscar: ").strip()
            if search_term:
                quick_filters = filters.copy()
                quick_filters['first_name'] = search_term
                quick_df = apply_filters(df, quick_filters)
                
                if len(quick_df) == 0:
                    quick_filters['first_name'] = None
                    quick_filters['last_name'] = search_term
                    quick_df = apply_filters(df, quick_filters)
                
                display_results(quick_df, page_size=20, page=1)
            input("\nPressione Enter para continuar...")
        
        elif choice == '11':
            filters['different_addresses'] = not filters.get('different_addresses', False)
            status = "ATIVADO" if filters['different_addresses'] else "DESATIVADO"
            print(f"\n✅ Filtro de endereços diferentes {status}")
            filtered_df = apply_filters(df, filters)
            current_page = 1
            input("Pressione Enter para continuar...")
        
        elif choice == '12':
            filters['no_practice_address'] = not filters.get('no_practice_address', False)
            status = "ATIVADO" if filters['no_practice_address'] else "DESATIVADO"
            print(f"\n✅ Filtro de sem endereço de prática {status}")
            filtered_df = apply_filters(df, filters)
            current_page = 1
            input("Pressione Enter para continuar...")
        
        elif choice == '13':
            filters['recent_update'] = not filters.get('recent_update', False)
            status = "ATIVADO" if filters['recent_update'] else "DESATIVADO"
            three_months_ago = datetime.now() - relativedelta(months=3)
            print(f"\n✅ Filtro de atualização recente (últimos 3 meses) {status}")
            print(f"   Data de corte: {three_months_ago.strftime('%d/%m/%Y')}")
            filtered_df = apply_filters(df, filters)
            current_page = 1
            input("Pressione Enter para continuar...")
        
        else:
            print("\n❌ Opção inválida!")
            input("Pressione Enter para continuar...")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrompido. Até logo!\n")
        sys.exit(0)


