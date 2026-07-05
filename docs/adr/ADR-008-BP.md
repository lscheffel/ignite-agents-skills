# Blueprint: Ultra-Avaliação v2.0.3 — Correção de Débitos Estruturais

> ADR-008 | Versão 1.0 | 2026-07-05 | **Status: PENDENTE**

---

## 1. Visão Geral

### Objetivo
Corrigir 9 débitos técnicos identificados pela Ultra-Avaliação v2.0.3 (88/100), incluindo 2 bugs reais no CI, links quebrados que afetam agentes em uso, e 3 débitos de recorrência direta da ADR-004. Fechar o loop de governança para que os mesmos padrões de débito não reapareçam.

### Métricas de Sucesso

| Métrica | Antes | Depois | Status |
|---------|-------|--------|--------|
| `validate-skill.sh` roda todos os 10 checks | Não (para no 1º warning) | Sim | ⬜ |
| Links quebrados para ADRs arquivadas | 4 | 0 | ⬜ |
| Artefatos implementation órfãos em docs/adr/ | 3 | 0 | ⬜ |
| Workflows de CI duplicados | 2 | 1 | ⬜ |
| Versão consistente (README/index/CHANGELOG) | Não (v2.1.0 vs 2.0.3) | Sim (2.0.3) | ⬜ |
| CHANGELOG inclui agents-md-generator | Não | Sim | ⬜ |
| Vazamentos CJK/árabe em arquivos .md | 9 | 0 | ⬜ |
| Skills com ≥2 exemplos práticos | 1/4 (só ddd) | 4/4 | ⬜ |
| Audit bulletin real no repo | 0 | ≥1 | ⬜ |

---

## 2. Fase 1: Bugs de CI e Links Mortos

### F1.1: Corrigir `((WARNINGS++))` em validate-skill.sh [D-001]

**Arquivo:** `scripts/validate-skill.sh`

**Bug:** Em bash, `((VAR++))` retorna o valor antigo de `VAR` como status de saída. Quando `WARNINGS` sai de 0, a expressão avalia pra 0 (falso), e `set -e` mata o script antes de rodar os checks 7-10 e antes de imprimir o resumo. Isso transforma qualquer warning em falha silenciosa de CI.

**Mudança:**
```bash
# Linha 18: ((ERRORS++)) → ERRORS=$((ERRORS + 1))
# Linha 24: ((WARNINGS++)) → WARNINGS=$((WARNINGS + 1))
```

**Estrutura proposta (linhas 16-25):**
```bash
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
```

**Critérios de aceitação:**
- [ ] `((ERRORS++))` substituído por `ERRORS=$((ERRORS + 1))`
- [ ] `((WARNINGS++))` substituído por `WARNINGS=$((WARNINGS + 1))`
- [ ] Script roda todos os 10 checks mesmo com warnings
- [ ] Resumo é impresso sempre (não truncado)
- [ ] Exit code = 0 quando só há warnings, 1 quando há errors

**Validação:**
```bash
bash scripts/validate-skill.sh skills/writing-plans
# Deve: imprimir resumo com warnings E exit 0
echo "Exit: $?"
```

---

### F1.2: Corrigir links quebrados para ADRs arquivadas [D-002]

**Arquivos:** `skills/implementation/SKILL.md`, `skills/agents-md-generator/SKILL.md`

**Mudança:** Adicionar `archive/` ao path de todos os links para ADRs arquivadas.

**Links a corrigir:**

| Arquivo | Linha | Link atual | Link correto |
|---------|-------|------------|--------------|
| `skills/implementation/SKILL.md` | 401 | `../../docs/adr/ADR-005.md` | `../../docs/adr/archive/ADR-005.md` |
| `skills/implementation/SKILL.md` | 402 | `../../docs/adr/ADR-005-BP.md` | `../../docs/adr/archive/ADR-005-BP.md` |
| `skills/implementation/SKILL.md` | 403 | `../../docs/adr/ADR-002.md` | `../../docs/adr/archive/ADR-002.md` |
| `skills/agents-md-generator/SKILL.md` | 292 | `../../docs/adr/ADR-007.md` | `../../docs/adr/archive/ADR-007.md` |

**Critérios de aceitação:**
- [ ] Todos os 4 links apontam para `archive/ADR-XXX.md`
- [ ] Zero ocorrências de `../../docs/adr/ADR-` sem `archive/` em skills/
- [ ] Arquivos-alvo existem em `docs/adr/archive/`

**Validação:**
```bash
grep -rn '../../docs/adr/ADR-' skills/ | grep -v archive
# Deve: ZERO resultados
```

---

## 3. Fase 2: Automação e Governança

### F2.1: Atualizar archive-adrs.sh para artefatos de implementation [D-003]

**Arquivo:** `scripts/archive-adrs.sh`

**Mudança:** Adicionar sufixos `-execution-contract.md`, `-execution-report.md`, `-change-plan.md` ao loop de arquivamento (linha 60).

**Estrutura proposta (linha 60):**
```bash
# ANTES:
for suffix in "-BP.md" "-TODO.md" "-implementation-plan.md"; do

# DEPOIS:
for suffix in "-BP.md" "-TODO.md" "-implementation-plan.md" "-execution-contract.md" "-execution-report.md" "-change-plan.md"; do
```

**Mudança adicional:** Mover os 3 arquivos órfãos existentes para archive:
```bash
mv docs/adr/ADR-007-change-plan.md docs/adr/archive/
mv docs/adr/ADR-007-execution-contract.md docs/adr/archive/
mv docs/adr/ADR-007-execution-report.md docs/adr/archive/
```

**Critérios de aceitação:**
- [ ] Script reconhece os 6 sufixos
- [ ] Os 3 arquivos órfãos de ADR-007 estão em `docs/adr/archive/`
- [ ] `docs/adr/` só contém `INDEX.md` e `archive/`

**Validação:**
```bash
ls docs/adr/
# Deve: INDEX.md archive/
ls docs/adr/archive/ADR-007-*
# Deve: ADR-007-change-plan.md ADR-007-execution-contract.md ADR-007-execution-report.md
```

---

### F2.2: Remover sync-pages.yml redundante [D-004]

**Arquivo:** `.github/workflows/sync-pages.yml` (REMOVER)

**Mudança:** Deletar `sync-pages.yml`. O `sync-and-deploy.yml` (formalizado na ADR-006) já cobre o mesmo evento com strategy mais completa.

**Critérios de aceitação:**
- [ ] `sync-pages.yml` não existe mais
- [ ] Nenhum arquivo referencia `sync-pages`
- [ ] `sync-and-deploy.yml` é o único workflow de deploy

**Validação:**
```bash
[ ! -f .github/workflows/sync-pages.yml ] && echo "OK"
grep -rn "sync-pages" .github/ skills/ docs/ README.md AGENTS.md
# Deve: ZERO resultados
```

---

### F2.3: Sincronizar versão README ↔ index.json [D-005]

**Arquivo:** `README.md` (L153)

**Mudança:** Corrigir `v2.1.0` para `v2.0.3` no cabeçalho de status.

**Linha 153 atual:**
```markdown
**v2.1.0 — Skills Ultra-High Quality Grade**
```

**Linha 153 corrigida:**
```markdown
**v2.0.3 — Skills Ultra-High Quality Grade**
```

**Critérios de aceitação:**
- [ ] README diz `v2.0.3`
- [ ] index.json diz `2.0.3`
- [ ] CHANGELOG tem entry `[2.0.3]`

**Validação:**
```bash
echo "README: $(grep -oP 'v[0-9]+\.[0-9]+\.[0-9]+' README.md | head -1)"
echo "index.json: $(jq -r '.version' skills/index.json)"
echo "CHANGELOG: $(grep -oP '\[[0-9]+\.[0-9]+\.[0-9]+\]' CHANGELOG.md | head -1)"
# Todos devem ser 2.0.3
```

---

### F2.4: Adicionar agents-md-generator ao CHANGELOG [D-006]

**Arquivo:** `CHANGELOG.md`

**Mudança:** Adicionar entrada na seção `Added` da versão `[2.0.3]` documentando a skill `agents-md-generator`.

**Entrada a adicionar (após a linha 12, dentro de `[2.0.3]`):**
```markdown
- Skill `agents-md-generator` — geração e manutenção de AGENTS.md adaptativo (ADR-007)
  - Detecção automática de contexto do projeto
  - 7 templates: AGENTS-base, AGENTS-api, AGENTS-cli, AGENTS-crm, AGENTS-library, AGENTS-skills-repo, AGENTS-webapp
  - 3 examples: before-after, context-detection, customization
  - 2 checklists: maintenance, validation
  - Anti-patterns: template genérico, sem versionamento, sem validação
```

**Critérios de aceitação:**
- [ ] CHANGELOG tem entrada para `agents-md-generator` dentro de `[2.0.3]`
- [ ] Entrada menciona ADR-007, 7 templates, 3 examples

**Validação:**
```bash
grep -A3 "agents-md-generator" CHANGELOG.md
# Deve: mostrar entry descrevendo a skill
```

---

### F2.5: Adicionar validação de encoding + limpar vazamentos [D-007]

**Arquivos:**
- `scripts/validate-skill.sh` (novo check #11)
- 8 arquivos com 9 vazamentos CJK/árabe

#### Parte A: Novo check em validate-skill.sh

**Inserir após o check #10 (linhas 125-129), antes do resumo:**

```bash
# 11. Verificar encoding (CJK/árabe fora de code blocks)
if [[ -f "$SKILL_DIR/SKILL.md" ]]; then
    # Remove code blocks antes de verificar
    non_code=$(sed '/^```/,/^```/d' "$SKILL_DIR/SKILL.md")
    if echo "$non_code" | grep -qP '[\x{4E00}-\x{9FFF}\x{0600}-\x{06FF}]' 2>/dev/null; then
        warn "Caracteres CJK/árabe detectados fora de code blocks (verificar encoding)"
    else
        success "Encoding limpo (sem caracteres CJK/árabe)"
    fi
fi
```

#### Parte B: Limpar os 9 vazamentos

| # | Arquivo | Linha | Vazamento | Substituição |
|---|---------|-------|-----------|--------------|
| 1 | `AGENTS.md` | 77 | `空行` | `linhas vazias` |
| 2 | `skills/agents-md-generator/templates/AGENTS-skills-repo.md` | 41 | `空行` | `linhas vazias` |
| 3 | `skills/refactoring/templates/test-before-refactor.md` | 116 | `分支` | `branches` |
| 4 | `skills/refactoring/SKILL.md` | 216 | `难以` | `difícil de` |
| 5 | `skills/refactoring/SKILL.md` | 231 | `难以` | `difícil de` |
| 6 | `skills/refactoring/SKILL.md` | 305 | `替换` | `substituir` |
| 7 | `skills/data-modeling/SKILL.md` | 56 | `Sنقem no commit` | `Sigma no commit` |
| 8 | `skills/data-modeling/SKILL.md` | 239 | `覆盖索covers` | `covering index` |
| 9 | `skills/agents-md-generator/templates/AGENTS-webapp.md` | 226 | `难 de refactor` | `difícil de refatorar` |

**Critérios de aceitação:**
- [ ] Check #11 existe em validate-skill.sh
- [ ] Zero vazamentos CJK/árabe em .md (fora de code blocks)
- [ ] Todos os 9 pontos corrigidos

**Validação:**
```bash
grep -rnP '[\x{4E00}-\x{9FFF}\x{0600}-\x{06FF}]' skills/ AGENTS.md
# Deve: ZERO resultados
```

---

## 4. Fase 3: Completude e Dogfooding

### F3.1: Adicionar exemplos práticos [D-008]

**Arquivos a criar:**
- `skills/writing-plans/examples/api-migration-plan.md`
- `skills/writing-plans/examples/feature-breakdown.md`
- `skills/api-design/examples/rest-crud-spec.md`
- `skills/api-design/examples/error-handling-contract.md`
- `skills/security-review/examples/dependency-audit.md`
- `skills/security-review/examples/crypto-validation.md`

**Critérios de aceitação:**
- [ ] writing-plans tem ≥2 exemplos (atual: 0)
- [ ] api-design tem ≥2 exemplos (atual: 0)
- [ ] security-review tem ≥2 exemplos (atual: 0)
- [ ] Cada exemplo tem ≥30 linhas com contexto, código, output esperado

**Validação:**
```bash
for skill in writing-plans api-design security-review; do
  count=$(find "skills/$skill/examples" -name "*.md" 2>/dev/null | wc -l)
  echo "$skill: $count exemplos"
done
```

---

### F3.2: Executar skill-audit-bulletin no repo [D-009]

**Arquivos a criar:**
- `docs/audits/` (diretório)
- `docs/audits/ignite-agents-skills-audit.md`

**Critérios de aceitação:**
- [ ] Diretório `docs/audits/` existe
- [ ] Audit bulletin gerado seguindo template `skills/skill-audit-bulletin/templates/audit-bulletin.md`
- [ ] Bulletin cobre ≥5 skills críticas
- [ ] Score ≥ 90/100

**Validação:**
```bash
[ -d docs/audits ] && echo "OK" || echo "FALTA"
ls docs/audits/
```

---

## 5. Fase 4: Validação Final

### F4.1: Validação cruzada completa

**Critérios de aceitação:**
- [ ] `validate-index.sh` passa: 22/22 skills, 0 erros
- [ ] `validate-skill.sh` passa para todas as 22 skills: 0 erros (com check #11)
- [ ] Zero links quebrados para ADRs
- [ ] Zero vazamentos CJK/árabe
- [ ] Versão consistente em README, index.json, CHANGELOG
- [ ] `sync-pages.yml` removido
- [ ] `archive-adrs.sh` reconhece 6 sufixos
- [ ] Exemplos existem para writing-plans, api-design, security-review
- [ ] Audit bulletin existe em docs/audits/

**Validação:**
```bash
# 1. Index
./scripts/validate-index.sh

# 2. Todas as skills
for skill in skills/*/; do
  [ -f "$skill/SKILL.md" ] || continue
  bash scripts/validate-skill.sh "$skill"
done

# 3. Links
grep -rn '../../docs/adr/ADR-' skills/ | grep -v archive

# 4. Encoding
grep -rnP '[\x{4E00}-\x{9FFF}\x{0600}-\x{06FF}]' skills/ AGENTS.md

# 5. Versão
echo "README: $(grep -oP 'v[0-9]+\.[0-9]+\.[0-9]+' README.md | head -1)"
echo "index: $(jq -r '.version' skills/index.json)"

# 6. Workflow
[ ! -f .github/workflows/sync-pages.yml ] && echo "sync-pages OK"

# 7. Sufixos
grep -q "execution-contract" scripts/archive-adrs.sh && echo "archive OK"

# 8. Exemplos
for skill in writing-plans api-design security-review; do
  count=$(find "skills/$skill/examples" -name "*.md" 2>/dev/null | wc -l)
  echo "$skill: $count"
done

# 9. Audit
[ -f docs/audits/ignite-agents-skills-audit.md ] && echo "audit OK"
```

---

## 6. Dependências e Sequenciamento

```
F1.1 (validate-skill.sh bug) ──┐
F1.2 (links quebrados) ────────┤
                                │
F2.1 (archive-adrs.sh) ────────┤── Fase 2
F2.2 (remover sync-pages.yml) ─┤
F2.3 (versão) ─────────────────┤
F2.4 (CHANGELOG) ──────────────┤
F2.5 (encoding) ───────────────┘
                                │
F3.1 (exemplos) ───────────────┤── Fase 3
F3.2 (dogfooding) ─────────────┘
                                │
F4.1 (validação) ──────────────┘── Fase 4
```

### Ordem de Execução Recomendada

```
Fase 1 (~1h) — paralelizável:
  ├── F1.1: Corrigir ((WARNINGS++)) ─────────────┐
  └── F1.2: Corrigir links quebrados ─────────────┘

Fase 2 (~3-4h) — sequencial:
  ├── F2.2: Remover sync-pages.yml ──────────────┐  (zero deps)
  ├── F2.3: Sincronizar versão ──────────────────┤  (independente)
  ├── F2.4: Atualizar CHANGELOG ─────────────────┤  (após F2.3)
  ├── F2.1: Atualizar archive-adrs.sh ───────────┤  (após F1.1)
  └── F2.5: Validação encoding + limpar ─────────┘  (após F1.1)

Fase 3 (~4-6h) — após Fase 2:
  ├── F3.1: Criar exemplos ──────────────────────┐
  └── F3.2: Dogfooding audit ────────────────────┘  (após F3.1)

Fase 4 — validação final:
  └── F4.1: Validação cruzada ────────────────────  (após tudo)
```

---

## 7. Riscos e Mitigações

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Correção de D-001 expõe warnings reais em skills que "passavam" | Médio | Alta | Rodar validate-skill.sh em todas as 22 skills após correção para mapear warnings |
| Validação de encoding (D-007) dá falsos positivos em code blocks | Baixo | Média | Usar `sed` para remover code blocks antes de grep |
| Remoção de sync-pages.yml quebra deploy se sync-and-deploy.yml tem bug | Alto | Baixa | Verificar que sync-and-deploy.yml funciona antes de remover |
| Exemplos (D-008) ficam genéricos demais | Médio | Média | Usar casos reais do repo (Secure Notes, MestreCuca, FAISS) |

---

## 8. Estimativas Detalhadas

| Tarefa | Complexidade | Horas Est. | Dependências |
|--------|-------------|------------|--------------|
| F1.1: Corrigir ((WARNINGS++)) | S | 15min | — |
| F1.2: Corrigir links quebrados | S | 15min | — |
| F2.1: Atualizar archive-adrs.sh | S | 20min | F1.1 |
| F2.2: Remover sync-pages.yml | S | 5min | — |
| F2.3: Sincronizar versão | S | 5min | — |
| F2.4: Atualizar CHANGELOG | S | 10min | F2.3 |
| F2.5: Validação encoding | S | 30min | F1.1 |
| F3.1: Criar exemplos | M | 3-4h | Fase 2 |
| F3.2: Dogfooding audit | M | 1-2h | F3.1 |
| F4.1: Validação cruzada | S | 30min | Todas |
| **Total** | | **~6-8h** | |

---

*Documento gerado em 2026-07-05. Referência: ADR-008.*
