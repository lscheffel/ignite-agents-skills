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
        for field in "name:" "description:"; do
            if grep -q "^$field" "$SKILL_DIR/SKILL.md"; then
                success "Campo '$field' presente"
            else
                error "Campo '$field' ausente no frontmatter"
            fi
        done
        # Campos recomendados
        for field in "version:" "tags:" "related_skills:"; do
            if grep -q "^$field" "$SKILL_DIR/SKILL.md"; then
                success "Campo '$field' presente"
            else
                warn "Campo recomendado '$field' ausente no frontmatter"
            fi
        done
    else
        error "Frontmatter inválido ou ausente"
    fi
fi

# 3. Verificar SKILL.md tem conteúdo substancial (≥80 linhas)
if [[ -f "$SKILL_DIR/SKILL.md" ]]; then
    LINES=$(wc -l < "$SKILL_DIR/SKILL.md")
    if [[ $LINES -ge 80 ]]; then
        success "SKILL.md tem $LINES linhas (mínimo: 80)"
    else
        warn "SKILL.md tem apenas $LINES linhas (mínimo recomendado: 80)"
    fi
fi

# 4. Verificar seções principais (suporte a Português e Inglês)
check_section() {
    local pt_sec="$1"
    local en_sec="$2"
    if grep -iq "$pt_sec" "$SKILL_DIR/SKILL.md" 2>/dev/null || grep -iq "$en_sec" "$SKILL_DIR/SKILL.md" 2>/dev/null; then
        success "Seção '$pt_sec / $en_sec' presente"
    else
        warn "Seção '$pt_sec / $en_sec' ausente ou com nomenclatura customizada"
    fi
}

check_section "Quando Usar" "When to Use"
check_section "Workflow" "Process"
check_section "Anti-patterns" "Pitfalls"
check_section "Checklists" "Verification"
check_section "Edge Cases" "Troubleshooting"

# 5. Verificar assets adicionais (templates/, references/, examples/, scripts/)
ASSET_COUNT=0
if [[ -d "$SKILL_DIR/templates" ]]; then
    COUNT=$(find "$SKILL_DIR/templates" -type f | wc -l)
    ASSET_COUNT=$((ASSET_COUNT + COUNT))
fi
if [[ -d "$SKILL_DIR/references" ]]; then
    COUNT=$(find "$SKILL_DIR/references" -type f | wc -l)
    ASSET_COUNT=$((ASSET_COUNT + COUNT))
fi
if [[ -d "$SKILL_DIR/examples" ]]; then
    COUNT=$(find "$SKILL_DIR/examples" -type f | wc -l)
    ASSET_COUNT=$((ASSET_COUNT + COUNT))
fi
if [[ -d "$SKILL_DIR/scripts" ]]; then
    COUNT=$(find "$SKILL_DIR/scripts" -type f -not -path "*/__pycache__/*" -not -name "*.pyc" | wc -l)
    ASSET_COUNT=$((ASSET_COUNT + COUNT))
fi

if [[ $ASSET_COUNT -ge 1 ]]; then
    success "Bundle de assets modulares presente ($ASSET_COUNT arquivos adicionais)"
else
    warn "Skill auto-contida sem assets modulares em subpastas"
fi

# 6. Verificar cross-references
if grep -q "\`[a-z-]*\`" "$SKILL_DIR/SKILL.md" 2>/dev/null; then
    success "Cross-references presentes"
else
    warn "Nenhum cross-reference encontrado"
fi

# 7. Verificar decision tree / workflow diagram
if grep -q "## Decision Tree" "$SKILL_DIR/SKILL.md" 2>/dev/null || grep -q "graph TD\|graph LR\|flowchart" "$SKILL_DIR/SKILL.md" 2>/dev/null; then
    success "Diagrama de decisão / fluxo presente"
else
    warn "Decision tree ausente (recomendado para workflows complexos)"
fi

# 8. Verificar anti-patterns / mitigação
if grep -q "🔴\|🟡\|🟢\|Anti-pattern\|Warning\|Caution\|Pitfall" "$SKILL_DIR/SKILL.md" 2>/dev/null; then
    success "Identificação de riscos e anti-patterns presente"
else
    warn "Anti-patterns sem taxonomia explícita"
fi

# 9. Verificar encoding (CJK/árabe fora de code blocks)
if [[ -f "$SKILL_DIR/SKILL.md" ]]; then
    non_code=$(sed '/^```/,/^```/d' "$SKILL_DIR/SKILL.md")
    if echo "$non_code" | grep -qP '[\x{4E00}-\x{9FFF}\x{0600}-\x{06FF}]' 2>/dev/null; then
        warn "Caracteres CJK/árabe detectados fora de code blocks (verificar encoding)"
    else
        success "Encoding limpo (sem caracteres CJK/árabe)"
    fi
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