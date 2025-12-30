# 🚀 Como Publicar no GitHub

Guia passo a passo para publicar este repositório no GitHub.

---

## 📋 Pré-requisitos

- ✅ Conta no GitHub (crie em [github.com](https://github.com))
- ✅ Git instalado (já está instalado ✅)
- ✅ Repositório Git inicializado (já está ✅)

---

## 🔧 Passo 1: Criar Repositório no GitHub

1. Acesse [github.com](https://github.com) e faça login
2. Clique no botão **"+"** no canto superior direito
3. Selecione **"New repository"**
4. Preencha:
   - **Repository name**: `nurses-processor` (ou outro nome)
   - **Description**: `High-performance Python tool to process large NPI healthcare provider CSV files and extract nurse records`
   - **Visibility**: Escolha **Public** ou **Private**
   - **NÃO marque** "Initialize with README" (já temos um)
5. Clique em **"Create repository"**

---

## 🔗 Passo 2: Conectar Repositório Local ao GitHub

Após criar o repositório no GitHub, você verá uma página com instruções. Use estes comandos:

### Opção A: Se o repositório está vazio (recomendado)

```bash
cd /Users/aleksanderribeirovale/projects/nurses-processor

# Adicionar remote (substitua SEU_USUARIO pelo seu username do GitHub)
git remote add origin https://github.com/SEU_USUARIO/nurses-processor.git

# Verificar se foi adicionado
git remote -v
```

### Opção B: Se já tem commits no GitHub

```bash
# Fazer pull primeiro (se necessário)
git pull origin main --allow-unrelated-histories
```

---

## 📝 Passo 3: Adicionar e Fazer Commit dos Arquivos

```bash
# Verificar status
git status

# Adicionar todos os arquivos (exceto os ignorados pelo .gitignore)
git add .

# Ver o que será commitado
git status

# Fazer commit
git commit -m "Initial commit: Nurses CSV Processor

- Memory-efficient CSV processor for 10GB+ NPI files
- Interactive viewer for filtering and exploring nurse data
- Comprehensive documentation in Portuguese and English
- Supports filtering by name, city, state, and taxonomy codes"
```

---

## 🚀 Passo 4: Enviar para o GitHub

```bash
# Enviar para o GitHub (primeira vez)
git push -u origin main

# Ou se sua branch se chama 'master':
# git push -u origin master
```

**Nota**: Se pedir autenticação:
- **Token**: Use um Personal Access Token (veja Passo 5)
- **Username**: Seu username do GitHub
- **Password**: Cole o token (não sua senha)

---

## 🔐 Passo 5: Configurar Autenticação (se necessário)

### Criar Personal Access Token

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Clique em **"Generate new token (classic)"**
3. Dê um nome (ex: "nurses-processor")
4. Selecione escopos: **repo** (todos os sub-itens)
5. Clique em **"Generate token"**
6. **COPIE O TOKEN** (você só verá uma vez!)

### Usar o Token

Quando o Git pedir senha, use o token no lugar da senha.

---

## ✅ Passo 6: Verificar

1. Acesse seu repositório no GitHub
2. Você deve ver todos os arquivos
3. O README.md deve aparecer formatado

---

## 📦 O Que Será Publicado

### ✅ Arquivos que SERÃO incluídos:

- ✅ Todos os scripts Python (`.py`)
- ✅ Documentação (`.md`)
- ✅ Configuração (`requirements.txt`, `config.py`)
- ✅ Scripts shell (`.sh`)
- ✅ `.gitignore`

### ❌ Arquivos que NÃO serão incluídos (por .gitignore):

- ❌ `data.csv` (10GB - muito grande!)
- ❌ `nurses.csv` (418MB - muito grande!)
- ❌ `__pycache__/` (cache Python)
- ❌ Arquivos temporários
- ❌ Arquivos de output (`*_filtered.csv`)

---

## 🔄 Comandos Úteis para o Futuro

### Fazer alterações e atualizar

```bash
# Ver mudanças
git status

# Adicionar arquivos modificados
git add .

# Fazer commit
git commit -m "Descrição das mudanças"

# Enviar para GitHub
git push
```

### Ver histórico

```bash
git log --oneline
```

### Ver diferenças

```bash
git diff
```

---

## 🎯 Checklist de Publicação

- [ ] Conta no GitHub criada
- [ ] Repositório criado no GitHub
- [ ] Remote adicionado (`git remote add origin ...`)
- [ ] Arquivos adicionados (`git add .`)
- [ ] Commit feito (`git commit -m "..."`)
- [ ] Push realizado (`git push -u origin main`)
- [ ] Repositório visível no GitHub ✅

---

## 🆘 Problemas Comuns

### "remote origin already exists"

**Solução**: Remover e adicionar novamente
```bash
git remote remove origin
git remote add origin https://github.com/SEU_USUARIO/nurses-processor.git
```

### "authentication failed"

**Solução**: Use Personal Access Token em vez de senha

### "failed to push some refs"

**Solução**: Fazer pull primeiro
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### "large files detected"

**Solução**: Verifique se `.gitignore` está funcionando
```bash
git status
# Se data.csv ou nurses.csv aparecerem, eles estão sendo rastreados
# Remova-os:
git rm --cached data.csv nurses.csv
git commit -m "Remove large data files"
```

---

## 📚 Recursos Adicionais

- [GitHub Docs](https://docs.github.com)
- [Git Handbook](https://guides.github.com/introduction/git-handbook/)
- [GitHub CLI](https://cli.github.com) (alternativa à interface web)

---

## 🎉 Pronto!

Após seguir estes passos, seu repositório estará público no GitHub!

**URL do seu repositório será**:
```
https://github.com/SEU_USUARIO/nurses-processor
```

---

*Última atualização: 30 de dezembro de 2025*

