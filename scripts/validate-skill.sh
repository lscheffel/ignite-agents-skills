#!/bin/bash
# validate-skill.sh - Validação automática de skills ultra-high quality grade
# Uso: bash scripts/validate-skill.sh <skill-directory>

set -e

SKILL_DIR="${1:-.}"
SKILL_NAME=$(basename "$SKILL_DIR")
ERRORS=0
WARNINGS=0

echo "🔍 Validando skill: $SKILL_NAME"
echo "======================================"

# Função para erro
error() {
    echo "❌ ERRO: $1"
    ERRORS=$((ERRORS + 1))
}

# Função para warning
warn() {
    echo "⚠️  WARNING: $1"
    WARNINGS=$((WARNINGS + 1))
}

# Função para success
success() {
    echo "✅ $1"
}

# 1. Verificar SKILL.md existe
if [[ ! -f "$SKILL_DIR/SKILL.md" ]]; then
    error "SKILL.md não encontrado em $SKILL_DIR"
else
    success "SKILL.md encontrado"
fi

# 2. Verificar frontmatter
if [[ -f "$SKILL_DIR/SKILL.md" ]]; then
    if grep -q "^---$" "$SKILL_DIR/SKILL.md" && grep -q "^name:" "$SKILL_DIR/SKILL.md"; then
        success "Frontmatter presente"
        
        # Verificar campos obrigatórios
        for field in "name:" "description:" "version:" "tags:" "related_skills:"; do
            if grep -q "^$field" "$SKILL_DIR/SKILL.md"; then
                success "Campo '$field' presente"
            else
                error "Campo '$field' ausente no frontmatter"
            fi
        done
    else
        error "Frontmatter inválido ou ausente"
    fi
fi

# 3. Verificar SKILL.md tem ≥150 linhas
if [[ -f "$SKILL_DIR/SKILL.md" ]]; then
    LINES=$(wc -l < "$SKILL_DIR/SKILL.md")
    if [[ $LINES -ge 150 ]]; then
        success "SKILL.md tem $LINES linhas (mínimo: 150)"
    else
        error "SKILL.md tem apenas $LINES linhas (mínimo: 150)"
    fi
fi

# 4. Verificar seções obrigatórias
REQUIRED_SECTIONS=(
    "## Quando Usar"
    "## Workflow"
    "## Anti-patterns"
    "## Checklists"
    "## Edge Cases"
)

for section in "${REQUIRED_SECTIONS[@]}"; do
    if grep -q "$section" "$SKILL_DIR/SKILL.md" 2>/dev/null; then
        success "Seção '$section' presente"
    else
        error "Seção '$section' ausente"
    fi
done

# 5. Verificar templates/ existe
if [[ -d "$SKILL_DIR/templates" ]]; then
    TEMPLATE_COUNT=$(find "$SKILL_DIR/templates" -type f | wc -l)
    if [[ $TEMPLATE_COUNT -ge 1 ]]; then
        success "Pasta templates/ existe com $TEMPLATE_COUNT arquivo(s)"
    else
        warn "Pasta templates/ existe mas está vazia"
    fi
else
    error "Pasta templates/ não existe"
fi

# 6. Verificar examples/ existe (warning)
if [[ -d "$SKILL_DIR/examples" ]]; then
    success "Pasta examples/ existe"
else
    warn "Pasta examples/ não existe (recomendado)"
fi

# 7. Verificar cross-references
if grep -q "\`[a-z-]*\`" "$SKILL_DIR/SKILL.md" 2>/dev/null; then
    success "Cross-references presentes"
else
    warn "Nenhum cross-reference encontrado"
fi

# 8. Verificar decision tree
if grep -q "## Decision Tree" "$SKILL_DIR/SKILL.md" 2>/dev/null || grep -q "graph TD" "$SKILL_DIR/SKILL.md" 2>/dev/null; then
    success "Decision tree presente"
else
    warn "Decision tree ausente (obrigatório exceto skills conceituais)"
fi

# 9. Verificar anti-patterns com severidade
if grep -q "🔴\|🟡\|🟢" "$SKILL_DIR/SKILL.md" 2>/dev/null; then
    success "Anti-patterns com severidade presentes"
else
    error "Anti-patterns sem severidade (use 🔴🟡🟢)"
fi

# 10. Verificar checkpoints nos workflows
if grep -q "Checkpoint" "$SKILL_DIR/SKILL.md" 2>/dev/null; then
    success "Checkpoints nos workflows presentes"
else
    error "Checkpoints nos workflows ausentes"
fi

# Resumo
echo ""
echo "======================================"
echo "📊 Resumo: $ERRORS erros, $WARNINGS warnings"

if [[ $ERRORS -gt 0 ]]; then
    echo "❌ Skill $SKILL_NAME FALHOU na validação"
    exit 1
else
    echo "✅ Skill $SKILL_NAME PASSOU na validação"
    exit 0
fi