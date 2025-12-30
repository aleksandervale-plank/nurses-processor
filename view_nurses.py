#!/usr/bin/env python3
"""
Visualizador Interativo de Enfermeiras
Permite visualizar e filtrar o arquivo nurses.csv de forma bonita e interativa.
"""

import sys
import os

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
        'Provider Business Practice Location Address City Name',
        'Provider Business Practice Location Address State Name',
        'Healthcare Provider Taxonomy Code_1',
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
        'Provider Business Practice Location Address City Name': 'Cidade',
        'Provider Business Practice Location Address State Name': 'Estado',
        'Healthcare Provider Taxonomy Code_1': 'Código',
        'Provider Business Practice Location Address Telephone Number': 'Telefone'
    }
    
    df_page = df_page.rename(columns={k: v for k, v in column_names.items() if k in df_page.columns})
    
    # Formatar valores
    for col in df_page.columns:
        if col == 'NPI':
            continue  # Manter NPI completo
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
        'state': None
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
        print("  6) Limpar filtros")
        print("  7) Ver estatísticas")
        print("  8) Exportar resultados filtrados")
        print("  9) Busca rápida (nome completo)")
        print("  0) Sair")
        print("="*60)
        
        choice = input("\nEscolha uma opção: ").strip()
        
        if choice == '0':
            print("\n👋 Até logo!\n")
            break
        
        elif choice == '1':
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
            else:
                input("\nPressione Enter para continuar...")
        
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
            filters = {
                'first_name': None,
                'last_name': None,
                'city': None,
                'state': None
            }
            filtered_df = df.copy()
            current_page = 1
            print("\n✅ Filtros limpos!")
            input("Pressione Enter para continuar...")
        
        elif choice == '7':
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
        
        elif choice == '9':
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
        
        else:
            print("\n❌ Opção inválida!")
            input("Pressione Enter para continuar...")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrompido. Até logo!\n")
        sys.exit(0)

