# 🚀 Como Publicar no GitHub - Guia Rápido

## ⚡ Passo a Passo Rápido

### 1️⃣ Criar Repositório no GitHub

1. Acesse [github.com](https://github.com) e faça login
2. Clique no **"+"** → **"New repository"**
3. Nome: `nurses-processor`
4. Descrição: `High-performance Python tool to process large NPI CSV files and extract nurse records`
5. Escolha **Public** ou **Private**
6. **NÃO marque** "Initialize with README"
7. Clique em **"Create repository"**

---

### 2️⃣ Conectar ao GitHub

Copie o URL do repositório (ex: `https://github.com/SEU_USUARIO/nurses-processor.git`) e execute:

```bash
cd /Users/aleksanderribeirovale/projects/nurses-processor

# Adicionar remote (substitua SEU_USUARIO)
git remote add origin https://github.com/SEU_USUARIO/nurses-processor.git

# Verificar
git remote -v
```

---

### 3️⃣ Fazer Commit e Push

**Opção A - Script Automático** (mais fácil):

```bash
./publish.sh
```

**Opção B - Manual**:

```bash
# Adicionar arquivos
git add .

# Fazer commit
git commit -m "Initial commit: Nurses CSV Processor

- Memory-efficient CSV processor for 10GB+ NPI files
- Interactive viewer for filtering and exploring nurse data
- Comprehensive documentation in Portuguese and English
- Supports filtering by name, city, state, and taxonomy codes"

# Enviar para GitHub
git push -u origin main
```

---

## 🔐 Autenticação

Se pedir senha, use um **Personal Access Token**:

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token (classic)
3. Nome: "nurses-processor"
4. Escopos: marque **repo** (todos)
5. Generate e **COPIE o token**
6. Use o token como senha quando o Git pedir

---

## ✅ Verificar

Acesse seu repositório:
```
https://github.com/SEU_USUARIO/nurses-processor
```

Você deve ver todos os arquivos!

---

## 📦 O Que Será Publicado

### ✅ Incluído:
- Scripts Python (`.py`)
- Documentação (`.md`)
- Configuração (`requirements.txt`, `config.py`)
- Scripts shell (`.sh`)

### ❌ NÃO Incluído (por .gitignore):
- `data.csv` (10GB - muito grande!)
- `nurses.csv` (418MB - muito grande!)
- Cache Python (`__pycache__/`)
- Arquivos temporários

---

## 🆘 Problemas?

### "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/SEU_USUARIO/nurses-processor.git
```

### "authentication failed"
Use Personal Access Token em vez de senha

### "failed to push"
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

---

## 📚 Documentação Completa

Veja **[PUBLICAR_GITHUB.md](PUBLICAR_GITHUB.md)** para guia detalhado.

---

**Pronto!** Seu repositório estará no GitHub! 🎉

