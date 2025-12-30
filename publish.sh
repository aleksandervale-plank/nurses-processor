#!/bin/bash
# Script helper para publicar no GitHub
# Uso: ./publish.sh

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Publicando Nurses CSV Processor no GitHub${NC}"
echo "=========================================="
echo ""

# Verificar se está em um repositório git
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Repositório Git não encontrado.${NC}"
    echo "Inicializando repositório..."
    git init
    echo -e "${GREEN}✅ Repositório inicializado${NC}"
fi

# Verificar status
echo -e "${BLUE}📊 Status do repositório:${NC}"
git status --short

echo ""
echo -e "${BLUE}📝 Arquivos que serão commitados:${NC}"
git status --porcelain | grep "^[AM]" | head -20

echo ""
read -p "Continuar com o commit? (s/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[SsYy]$ ]]; then
    echo "Cancelado."
    exit 0
fi

# Adicionar arquivos
echo -e "${BLUE}📦 Adicionando arquivos...${NC}"
git add .

# Verificar se há mudanças
if git diff --staged --quiet; then
    echo -e "${YELLOW}⚠️  Nenhuma mudança para commitar.${NC}"
    exit 0
fi

# Fazer commit
echo -e "${BLUE}💾 Fazendo commit...${NC}"
git commit -m "Initial commit: Nurses CSV Processor

- Memory-efficient CSV processor for 10GB+ NPI files
- Interactive viewer for filtering and exploring nurse data
- Comprehensive documentation in Portuguese and English
- Supports filtering by name, city, state, and taxonomy codes
- Beautiful terminal-based interface"

echo -e "${GREEN}✅ Commit realizado!${NC}"
echo ""

# Verificar remote
if git remote | grep -q "^origin$"; then
    echo -e "${BLUE}🔗 Remote 'origin' encontrado${NC}"
    git remote -v
    echo ""
    read -p "Fazer push para origin? (s/n): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[SsYy]$ ]]; then
        echo -e "${BLUE}🚀 Fazendo push...${NC}"
        CURRENT_BRANCH=$(git branch --show-current)
        git push -u origin "$CURRENT_BRANCH"
        echo -e "${GREEN}✅ Push realizado com sucesso!${NC}"
    else
        echo "Push cancelado. Execute manualmente:"
        echo "  git push -u origin main"
    fi
else
    echo -e "${YELLOW}⚠️  Remote 'origin' não configurado.${NC}"
    echo ""
    echo "Para adicionar o remote, execute:"
    echo "  git remote add origin https://github.com/SEU_USUARIO/nurses-processor.git"
    echo ""
    echo "Depois faça o push:"
    echo "  git push -u origin main"
    echo ""
    echo -e "${BLUE}📖 Veja PUBLICAR_GITHUB.md para instruções completas${NC}"
fi

echo ""
echo -e "${GREEN}✅ Processo concluído!${NC}"

