# 🏥 Processador de Enfermeiras - NPI CSV

**Processa arquivos CSV NPI de 10GB+ para extrair registros de enfermeiras de forma eficiente**

---

## ⚡ Início Rápido

### 1️⃣ Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2️⃣ Verificar Instalação

```bash
python3 verify_setup.py
```

### 3️⃣ Processar o CSV

```bash
# Forma mais fácil - usa data.csv automaticamente!
python process_nurses.py --output enfermeiras.csv
```

**Pronto!** O script vai processar seu arquivo de 10GB em 10-20 minutos usando apenas 200-500 MB de RAM.

---

## 📁 Seu Arquivo Está Pronto!

✅ **data.csv** (10GB) - Já está na raiz do projeto e será usado automaticamente!

---

## 🎯 O Que Faz

Extrai enfermeiras de arquivos NPI massivos filtrando por estes códigos de taxonomia:

- **363L00000X** - Enfermeira de Prática Avançada (Nurse Practitioner)
- **163W00000X** - Enfermeira Registrada (RN) - Mais comum
- **164W00000X** - Enfermeira Prática Licenciada (LPN)

**Entrada**: 10 GB, ~7.5M registros  
**Saída**: 1-2 GB, ~800K-1M enfermeiras (10-13%)  
**Tempo**: 10-20 minutos  
**Memória**: 200-500 MB (não 10 GB!)

---

## 🔍 Visualizar e Filtrar Resultados

Depois de processar o CSV, use o visualizador interativo para explorar os dados **SEM criar novos arquivos**:

```bash
python view_nurses.py
```

**Menu interativo** com opções para:
- Filtrar por nome, sobrenome, cidade, estado
- Ver estatísticas
- Exportar resultados (opcional)
- Busca rápida

📖 **[Ver guia completo do visualizador](GUIA_VISUALIZADOR.md)**

---

## 💡 Exemplos Comuns

### Extrair todas as enfermeiras
```bash
python process_nurses.py --output enfermeiras.csv
```

### Filtrar por estado (Califórnia)
```bash
python process_nurses.py --output enfermeiras_ca.csv --state CA
```

### Filtrar por cidade
```bash
python process_nurses.py --output enfermeiras_la.csv --city "Los Angeles"
```

### Buscar por nome
```bash
python process_nurses.py --output resultados.csv --last-name Garcia
```

### Combinar múltiplos filtros
```bash
python process_nurses.py --output resultados.csv \
  --state CA \
  --city "San Francisco" \
  --last-name Garcia
```

### Menu interativo (mais fácil!)
```bash
./example_commands.sh
```

---

## 🔍 Filtros Disponíveis

| Filtro | Descrição | Exemplo |
|--------|-----------|---------|
| `--state` | Código do estado (2 letras) | `--state CA` |
| `--city` | Nome da cidade (parcial) | `--city "Los Angeles"` |
| `--first-name` | Primeiro nome (parcial) | `--first-name Maria` |
| `--last-name` | Sobrenome (parcial) | `--last-name Garcia` |
| `--chunk-size` | Tamanho do bloco (performance) | `--chunk-size 250000` |
| `--output` | Arquivo de saída | `--output minhas_enfermeiras.csv` |

**Nota**: Todos os filtros são combinados com lógica AND (todos devem corresponder).

---

## 📊 O Que Esperar

Quando você executar o processador, verá:

```
Using Polars for processing (optimized)

Processing file: /Users/.../nurses-processor/data.csv
File size: 10.00 GB
Output file: enfermeiras.csv
Chunk size: 100,000 rows

Processing chunks...
  Chunk 1: 100,000 rows → 12,345 nurses (Total: 12,345)
  Chunk 2: 100,000 rows → 11,892 nurses (Total: 24,237)
  Chunk 3: 100,000 rows → 13,124 nurses (Total: 37,361)
  ...

============================================================
PROCESSING COMPLETE
============================================================
Total rows processed: 7,523,456
Nurses found: 892,445
Chunks processed: 76
Percentage: 11.86%

Output saved to: enfermeiras.csv
Output size: 1.45 GB
============================================================
```

---

## ⚙️ Ajuste de Performance

### Computador com mais memória (8GB+ RAM)
```bash
python process_nurses.py --output enfermeiras.csv --chunk-size 250000
```
*Processa mais rápido (8-12 minutos)*

### Computador com menos memória (4GB RAM)
```bash
python process_nurses.py --output enfermeiras.csv --chunk-size 50000
```
*Processa mais devagar mas usa menos RAM*

---

## 📚 Documentação Completa

| Documento | Propósito |
|-----------|-----------|
| **[START_HERE.md](START_HERE.md)** | Visão geral rápida (inglês) |
| **[QUICKSTART.md](QUICKSTART.md)** | Guia de início rápido |
| **[README.md](README.md)** | Documentação completa |
| **[INDEX.md](INDEX.md)** | Índice de toda documentação |

---

## 🆘 Precisa de Ajuda?

### Problemas de instalação?
```bash
python3 verify_setup.py
```

### Ver todas as opções?
```bash
python process_nurses.py --help
```

### Menu interativo?
```bash
./example_commands.sh
```

---

## ✨ Características Principais

✅ **Eficiente** - Usa apenas 200-500 MB de RAM (não 10 GB!)  
✅ **Rápido** - 5-10x mais rápido com biblioteca Polars  
✅ **Flexível** - Filtre por nome, cidade, estado  
✅ **Inteligente** - Verifica todas as 15 colunas de taxonomia  
✅ **Fácil** - Apenas coloque data.csv e execute!  
✅ **Confiável** - Trata dados malformados graciosamente  

---

## 🎓 Casos de Uso Comuns

### 1. Extrair todas as enfermeiras da Califórnia
```bash
python process_nurses.py --output enfermeiras_california.csv --state CA
```

### 2. Enfermeiras em San Francisco
```bash
python process_nurses.py --output enfermeiras_sf.csv \
  --state CA \
  --city "San Francisco"
```

### 3. Enfermeiras com sobrenome Silva
```bash
python process_nurses.py --output silva.csv --last-name Silva
```

### 4. Enfermeiras chamadas Maria em NY
```bash
python process_nurses.py --output maria_ny.csv \
  --first-name Maria \
  --state NY
```

---

## 🔧 Requisitos do Sistema

- **Python**: 3.7 ou superior ✅
- **RAM**: 2GB mínimo (4GB+ recomendado)
- **Espaço**: Para entrada (10GB) + saída (~1-2GB)
- **SO**: Linux, macOS, ou Windows

---

## 📦 Estrutura do Projeto

```
nurses-processor/
├── data.csv                   ← Seu arquivo de 10GB (já está aqui!)
├── nurses.csv                 ← Arquivo processado (gerado)
│
├── LEIA-ME.md                 ← Você está aqui
├── GUIA_VISUALIZADOR.md       ← Guia do visualizador
├── START_HERE.md              ← Início (inglês)
├── QUICKSTART.md              ← Guia rápido
├── README.md                  ← Documentação completa
│
├── process_nurses.py          ← Script de processamento
├── view_nurses.py             ← Visualizador interativo ⭐
├── config.py                  ← Configuração
├── verify_setup.py            ← Verificador de setup
├── example_commands.sh        ← Menu interativo
│
└── requirements.txt           ← Dependências Python
```

---

## ✅ Status do Projeto

**Status**: ✅ Pronto para Produção  
**Arquivo de dados**: ✅ data.csv (10GB) pronto para processar  
**Código**: 1,900+ linhas  
**Documentação**: Completa  

---

## 🚀 Próximos Passos

### Workflow Completo:

1. ✅ Você leu este arquivo
2. ✅ data.csv já está na raiz do projeto (10GB)
3. → Instale as dependências: `pip install -r requirements.txt`
4. → Verifique a instalação: `python3 verify_setup.py`
5. → **Processar dados**: `python process_nurses.py --output nurses.csv`
6. → **Visualizar resultados**: `python view_nurses.py` ⭐

---

## 💪 Vamos Começar!

### 1️⃣ Processar o arquivo grande (uma vez)

**Comando mais simples** (extrai todas as enfermeiras):
```bash
python process_nurses.py --output nurses.csv
```

**Com filtro de estado** (só Califórnia):
```bash
python process_nurses.py --output nurses_ca.csv --state CA
```

### 2️⃣ Visualizar e explorar os resultados (quantas vezes quiser!)

**Visualizador interativo** ⭐ (sem criar novos arquivos):
```bash
python view_nurses.py
```

**Menu de processamento** (para criar novos filtros):
```bash
./example_commands.sh
```

---

## 🎯 Comandos Essenciais

| Comando | O Que Faz |
|---------|-----------|
| `python process_nurses.py --output nurses.csv` | Processa data.csv e extrai enfermeiras |
| `python view_nurses.py` | Visualiza/filtra nurses.csv interativamente ⭐ |
| `./example_commands.sh` | Menu interativo para processar |
| `python verify_setup.py` | Verifica se tudo está instalado |

---

**Pronto para começar?** Execute um dos comandos acima! 🏥💉

**Dúvidas?** 
- Processamento: Veja este arquivo
- Visualização: Veja [GUIA_VISUALIZADOR.md](GUIA_VISUALIZADOR.md)
- Docs completas: [README.md](README.md)

**Boa sorte com seu processamento e visualização!** 🎯

