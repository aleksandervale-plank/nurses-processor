# 🎯 Como Usar - Guia Rápido

## 📋 Resumo Executivo

Você tem 2 scripts principais:

1. **`process_nurses.py`** - Processa o arquivo grande e cria filtros
2. **`view_nurses.py`** - Visualiza e explora os resultados (SEM criar arquivos) ⭐

---

## 🔄 Workflow Completo

```
┌─────────────┐
│  data.csv   │ (10GB - Arquivo original)
│  (uma vez)  │
└──────┬──────┘
       │
       │ python process_nurses.py --output nurses.csv
       │ (Demora 10-20 min - faça UMA vez)
       ▼
┌─────────────┐
│ nurses.csv  │ (1-2GB - Enfermeiras extraídas)
└──────┬──────┘
       │
       │ python view_nurses.py
       │ (Rápido! Use VÁRIAS vezes)
       ▼
┌─────────────┐
│ Visualização│ (Filtros, busca, estatísticas)
│  Interativa │ (NÃO cria arquivos!)
└─────────────┘
```

---

## 1️⃣ Primeiro Uso (Uma Vez)

### Instalar Dependências

```bash
pip install -r requirements.txt
```

### Processar o Arquivo Grande

```bash
python process_nurses.py --output nurses.csv
```

**Aguarde**: 10-20 minutos  
**Resultado**: Arquivo `nurses.csv` com ~400K enfermeiras

---

## 2️⃣ Uso Diário (Várias Vezes)

### Visualizar e Filtrar

```bash
python view_nurses.py
```

**É rápido!** Carrega em segundos  
**É interativo!** Menu com várias opções  
**NÃO cria arquivos!** Apenas exibe

---

## 🎯 Casos de Uso

### Caso 1: "Quero ver todas as enfermeiras em Los Angeles"

```bash
python view_nurses.py
```

No menu:
1. Digite `4` (Filtrar por cidade)
2. Digite `Los Angeles`
3. Digite `1` (Ver resultados)

### Caso 2: "Quero encontrar uma enfermeira específica"

```bash
python view_nurses.py
```

No menu:
1. Digite `9` (Busca rápida)
2. Digite o nome da pessoa
3. Veja os resultados instantaneamente

### Caso 3: "Quero ver quantas enfermeiras tem em cada estado"

```bash
python view_nurses.py
```

No menu:
1. Digite `7` (Ver estatísticas)
2. Veja o Top 10 estados

### Caso 4: "Quero criar uma lista de enfermeiras na Califórnia"

**Opção A** - Processar de novo (mais lento):
```bash
python process_nurses.py --output nurses_ca.csv --state CA
```

**Opção B** - Usar visualizador e exportar (mais rápido):
```bash
python view_nurses.py
# No menu: 5 (Filtrar CA) → 1 (Ver) → 8 (Exportar)
```

---

## 📊 Comparação dos Scripts

| Característica | process_nurses.py | view_nurses.py |
|----------------|-------------------|----------------|
| **Entrada** | data.csv (10GB) | nurses.csv (1-2GB) |
| **Saída** | Cria novo arquivo CSV | Apenas exibe (não cria) |
| **Velocidade** | Lento (10-20 min) | Rápido (segundos) |
| **Quando usar** | Uma vez ou para novos filtros permanentes | Várias vezes para explorar dados |
| **Filtros** | Via argumentos | Via menu interativo |
| **Visualização** | Não tem | Tabelas formatadas |
| **Estatísticas** | Não tem | Sim (Top estados, tipos, etc) |
| **Exportar** | Sim (sempre) | Opcional |

---

## 🎨 Interface do Visualizador

```
============================================================
🏥 VISUALIZADOR DE ENFERMEIRAS
============================================================

📊 Total no arquivo: 384,746 enfermeiras
🔍 Filtros ativos: Nenhum filtro aplicado
📋 Resultados filtrados: 384,746 enfermeiras

============================================================

OPÇÕES:
  1) Ver resultados              ← Ver dados em tabela
  2) Filtrar por nome            ← Buscar por primeiro nome
  3) Filtrar por sobrenome       ← Buscar por sobrenome
  4) Filtrar por cidade          ← Buscar por cidade
  5) Filtrar por estado          ← Buscar por estado
  6) Limpar filtros              ← Recomeçar
  7) Ver estatísticas            ← Ver números e gráficos
  8) Exportar resultados         ← Salvar em arquivo (opcional)
  9) Busca rápida                ← Busca rápida por nome
  0) Sair                        ← Fechar programa

Escolha uma opção: _
```

---

## 💡 Dicas Importantes

### ✅ FAÇA

- ✅ Use `view_nurses.py` para explorar e buscar dados
- ✅ Use `process_nurses.py` apenas uma vez ou para criar novos filtros permanentes
- ✅ Combine múltiplos filtros no visualizador
- ✅ Use busca rápida (opção 9) para buscas simples

### ❌ NÃO FAÇA

- ❌ Não processe o data.csv toda vez que quiser buscar algo
- ❌ Não crie múltiplos arquivos pequenos desnecessariamente
- ❌ Não use `process_nurses.py` para buscas rápidas

---

## 🆘 Problemas Comuns

### "nurses.csv não encontrado"

**Solução**: Processe primeiro:
```bash
python process_nurses.py --output nurses.csv
```

### "tabulate não está instalado"

**Solução**: Instale:
```bash
pip install tabulate
```

### "Arquivo muito grande/lento"

- Use `view_nurses.py` que é rápido!
- Se precisar reprocessar, use filtros no `process_nurses.py`

---

## 📚 Documentação

| Documento | O Que É |
|-----------|---------|
| **[LEIA-ME.md](LEIA-ME.md)** | Guia geral do projeto |
| **[GUIA_VISUALIZADOR.md](GUIA_VISUALIZADOR.md)** | Detalhes do visualizador |
| **COMO_USAR.md** | Este arquivo (guia rápido) |

---

## 🎉 Resumo

**Para processar (uma vez)**:
```bash
python process_nurses.py --output nurses.csv
```

**Para visualizar (várias vezes)**:
```bash
python view_nurses.py
```

**Simples assim!** 🏥💉

---

*Última atualização: 30 de dezembro de 2025*

