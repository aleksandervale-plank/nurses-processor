# 🏥 Visualizador Interativo de Enfermeiras

## 📖 Sobre

Script interativo para visualizar e filtrar o arquivo `nurses.csv` de forma bonita e organizada, **sem criar novos arquivos** (exceto se você quiser exportar).

## ⚡ Início Rápido

### 1. Instalar Dependência Extra (para visualização bonita)

```bash
pip install tabulate
```

Ou instale todas as dependências atualizadas:

```bash
pip install -r requirements.txt
```

### 2. Executar o Visualizador

```bash
python view_nurses.py
```

O script automaticamente usa o arquivo `nurses.csv` da raiz do projeto!

## 🎯 Funcionalidades

### ✅ O Que Você Pode Fazer

1. **Ver Resultados** - Exibe os dados em tabela formatada e paginada
2. **Filtrar por Nome** - Busca por primeiro nome (parcial)
3. **Filtrar por Sobrenome** - Busca por sobrenome (parcial)
4. **Filtrar por Cidade** - Busca por cidade (parcial)
5. **Filtrar por Estado** - Busca por código do estado (exato)
6. **Limpar Filtros** - Remove todos os filtros aplicados
7. **Ver Estatísticas** - Mostra estatísticas dos dados filtrados
8. **Exportar Resultados** - Salva resultados filtrados em novo CSV (opcional)
9. **Busca Rápida** - Busca rápida por nome completo

### 📊 Colunas Exibidas

- **NPI** - Número do provedor
- **Nome** - Primeiro nome
- **Sobrenome** - Sobrenome legal
- **Cidade** - Cidade de prática
- **Estado** - Estado de prática
- **Código** - Código de taxonomia (tipo de enfermeira)
- **Telefone** - Telefone de contato

## 💡 Exemplos de Uso

### Exemplo 1: Buscar Enfermeiras em uma Cidade

```
1. Execute: python view_nurses.py
2. Escolha opção: 4 (Filtrar por cidade)
3. Digite: Los Angeles
4. Escolha opção: 1 (Ver resultados)
```

### Exemplo 2: Buscar Enfermeiras por Nome em um Estado

```
1. Execute: python view_nurses.py
2. Escolha opção: 3 (Filtrar por sobrenome)
3. Digite: Garcia
4. Escolha opção: 5 (Filtrar por estado)
5. Digite: CA
6. Escolha opção: 1 (Ver resultados)
```

### Exemplo 3: Busca Rápida

```
1. Execute: python view_nurses.py
2. Escolha opção: 9 (Busca rápida)
3. Digite: Maria
```

### Exemplo 4: Ver Estatísticas de um Estado

```
1. Execute: python view_nurses.py
2. Escolha opção: 5 (Filtrar por estado)
3. Digite: NY
4. Escolha opção: 7 (Ver estatísticas)
```

## 🎨 Exemplo de Interface

```
============================================================
🏥 VISUALIZADOR DE ENFERMEIRAS
============================================================

📊 Total no arquivo: 384,746 enfermeiras
🔍 Filtros ativos: Cidade: 'Los Angeles' | Estado: 'CA'
📋 Resultados filtrados: 12,345 enfermeiras

============================================================

OPÇÕES:
  1) Ver resultados
  2) Filtrar por nome
  3) Filtrar por sobrenome
  4) Filtrar por cidade
  5) Filtrar por estado
  6) Limpar filtros
  7) Ver estatísticas
  8) Exportar resultados filtrados
  9) Busca rápida (nome completo)
  0) Sair
============================================================

Escolha uma opção:
```

## 📊 Exemplo de Saída (Ver Resultados)

```
====================================================================================================
📊 RESULTADOS: Mostrando 1-20 de 12,345 enfermeiras
====================================================================================================

+------------+--------+-----------+-------------+--------+-----------+--------------+
| NPI        | Nome   | Sobrenome | Cidade      | Estado | Código    | Telefone     |
+============+========+===========+=============+========+===========+==============+
| 1234567890 | Maria  | Garcia    | Los Angeles | CA     | 163W00000X| 310-555-0123 |
| 1234567891 | John   | Smith     | Los Angeles | CA     | 363L00000X| 310-555-0124 |
| 1234567892 | Ana    | Martinez  | Los Angeles | CA     | 163W00000X| 323-555-0125 |
+------------+--------+-----------+-------------+--------+-----------+--------------+

====================================================================================================
Página 1 de 618
====================================================================================================

Navegação: [n]próxima [p]anterior [v]voltar:
```

## 📈 Exemplo de Estatísticas

```
============================================================
📊 ESTATÍSTICAS DO ARQUIVO
============================================================
Total de enfermeiras: 384,746

🗺️  Top 10 Estados:
  CA: 52,341
  TX: 38,920
  NY: 35,678
  FL: 32,109
  PA: 24,567
  IL: 22,341
  OH: 21,098
  MI: 19,234
  NC: 18,567
  GA: 17,890

🏥 Tipos de Enfermeiras:
  Nurse Practitioner (NP): 156,789 (40.8%)
  Registered Nurse (RN): 198,234 (51.5%)
  Licensed Practical Nurse (LPN): 29,723 (7.7%)
============================================================
```

## 🔍 Tipos de Filtros

### Filtro por Nome/Sobrenome/Cidade
- **Busca parcial** (case-insensitive)
- Exemplo: "Maria" encontra "Maria", "Mariana", "Ana Maria"

### Filtro por Estado
- **Busca exata** do código do estado
- Use códigos de 2 letras: CA, NY, TX, FL, etc.

### Combinação de Filtros
- Todos os filtros são aplicados com lógica **AND**
- Exemplo: Nome="Maria" + Estado="CA" = Todas as Marias na Califórnia

## 💾 Exportar Resultados (Opcional)

Se você quiser salvar os resultados filtrados:

1. Aplique seus filtros
2. Escolha opção: 8 (Exportar resultados filtrados)
3. Digite o nome do arquivo (ou Enter para usar padrão)
4. Arquivo será salvo na raiz do projeto

**Nota**: Esta é a ÚNICA opção que cria arquivo. Todas as outras apenas exibem!

## ⌨️ Navegação

### Menu Principal
- Digite o número da opção desejada
- Pressione Enter

### Visualização de Resultados
- **[n]** - Próxima página
- **[p]** - Página anterior
- **[v]** - Voltar ao menu
- **Enter** - Continuar (se apenas 1 página)

### Sair do Programa
- Escolha opção **0** no menu
- Ou pressione **Ctrl+C** a qualquer momento

## 🎯 Casos de Uso Comuns

### 1. Encontrar todas as enfermeiras em sua cidade

```bash
python view_nurses.py
# Opção 4: Filtrar por cidade
# Digite sua cidade
# Opção 1: Ver resultados
```

### 2. Encontrar enfermeiras específicas por nome

```bash
python view_nurses.py
# Opção 9: Busca rápida
# Digite o nome
```

### 3. Analisar distribuição por estado

```bash
python view_nurses.py
# Opção 7: Ver estatísticas
```

### 4. Criar uma lista de enfermeiras em uma região

```bash
python view_nurses.py
# Opção 5: Filtrar por estado (ex: CA)
# Opção 4: Filtrar por cidade (ex: San Francisco)
# Opção 1: Ver resultados
# Opção 8: Exportar (se quiser salvar)
```

## 🔧 Requisitos

- Python 3.7+
- pandas (já instalado)
- tabulate (recomendado para visualização bonita)

## 📁 Arquivos

- **view_nurses.py** - Script principal
- **nurses.csv** - Arquivo de dados (gerado pelo process_nurses.py)

## 🆘 Solução de Problemas

### "Arquivo nurses.csv não encontrado"

**Solução**: Execute primeiro o processador para gerar o arquivo:
```bash
python process_nurses.py --output nurses.csv
```

### "tabulate não está instalado"

**Solução**: Instale a biblioteca:
```bash
pip install tabulate
```

O script funcionará sem tabulate, mas a visualização será mais simples.

### "pandas não está instalado"

**Solução**: Instale as dependências:
```bash
pip install -r requirements.txt
```

### Tabela não cabe na tela

**Solução**: 
- Maximize sua janela do terminal
- Ou reduza o tamanho da fonte
- A tabela se ajusta automaticamente ao conteúdo

## 💡 Dicas

1. **Use a busca rápida (opção 9)** para buscas simples por nome
2. **Combine filtros** para buscas mais específicas
3. **Limpe os filtros (opção 6)** antes de fazer uma nova busca
4. **Veja estatísticas (opção 7)** para entender a distribuição dos dados
5. **Exporte apenas quando necessário** - o objetivo é visualizar sem criar arquivos!

## 🎉 Pronto para Usar!

Execute o visualizador:

```bash
python view_nurses.py
```

**Divirta-se explorando seus dados!** 🏥💉

---

*Para voltar ao processamento de dados, veja [LEIA-ME.md](LEIA-ME.md)*

