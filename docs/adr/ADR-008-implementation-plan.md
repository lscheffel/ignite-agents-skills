# Plano de Implementação: Ultra-Avaliação v2.0.3 — Correção de Débitos

> ADR: [ADR-008](./docs/adr/ADR-008.md)
> Prioridade: Alta — bugs de CI e links mortos afetam operação real
> Total estimado: ~8-11h de trabalho

## Visão Geral

9 débitos organizados em 3 fases incrementais. Cada fase é atomicamente commitável e verificável.

| Fase | Débitos | Esforço | Dependências |
|------|---------|---------|--------------|
| 1 — Bugs de CI e Links | D-001, D-002 | ~1h | Nenhuma |
| 2 — Automação e Governança | D-003, D-004, D-005, D-006, D-007 | ~3-4h | Fase 1 |
| 3 — Completude e Dogfooding | D-008, D-009 | ~4-6h | Fase 2 |

---

## Fase 1: Bugs de CI e Links Mortos

### Tarefa 1.1: Corrigir `((WARNINGS++))` em validate-skill.sh [D-001]

**Arquivos:** `scripts/validate-skill.sh`
**Complexidade:** S
**Dependências:** Nenhuma
**Critérios de aceitação:**
- [ ] `((ERRORS++))` e `((WARNINGS++))` substituídos por `ERRORS=$((ERRORS + 1))` e `WARNINGS=$((WARNINGS + 1))`
- [ ] Script roda todos os 10 checks (1-10) mesmo com warnings, sem morrer antes do resumo
- [ ] Exit code é 0 quando só há warnings, 1 quando há errors
- [ ] Resumo imprime sempre (não é truncado)

**Comandos de validação:**
```bash
# Teste 1: skill com warning (exemplo: sem examples/)
bash scripts/validate-skill.sh skills/writing-plans
# Deve: imprimir resumo com 1+ warnings E exit 0

# Teste 2: skill inexistente (deve dar error)
bash scripts/validate-skill.sh skills/NONEXISTENT
# Deve: imprimir resumo com errors E exit 1

# Teste 3: rodar em todas as 22 skills e verificar que nenhuma morre
for skill in skills/*/; do
  [ -f "$skill/SKILL.md" ] || continue
  bash scripts/validate-skill.sh "$skill" > /dev/null 2>&1
  echo "$skill: exit $?"
done
```

**Detalhe da correção:**
```bash
# ANTES (linhas 18 e 24):
((ERRORS++))
((WARNINGS++))

# DEPOIS:
ERRORS=$((ERRORS + 1))
WARNINGS=$((WARNINGS + 1))
```

---

### Tarefa 1.2: Corrigir links quebrados para ADRs arquivadas [D-002]

**Arquivos:**
- `skills/implementation/SKILL.md` (3 links)
- `skills/agents-md-generator/SKILL.md` (1 link)

**Complexidade:** S
**Dependências:** Nenhuma
**Critérios de aceitação:**
- [ ] Todos os links em Referências apontam para caminhos que existem
- [ ] Zero ocorrências de `../../docs/adr/ADR-XXX.md` onde XXX não está em archive/
- [ ] Validação: `grep -r 'docs/adr/ADR-' skills/ | grep -v archive` retorna vazio

**Comandos de validação:**
```bash
# Verificar que nenhum link aponta para docs/adr/ADR-XXX.md (fora de archive)
grep -rn '../../docs/adr/ADR-' skills/
# Deve: retornar ZERO resultados (todos devem apontar para ../../docs/adr/archive/ADR-XXX.md)

# Verificar que os arquivos-alvo existem
for f in docs/adr/archive/ADR-002.md docs/adr/archive/ADR-005.md docs/adr/archive/ADR-005-BP.md docs/adr/archive/ADR-007.md; do
  [ -f "$f" ] && echo "OK: $f" || echo "FALTA: $f"
done
```

**Links a corrigir:**

| Arquivo | Link atual (quebrado) | Link correto |
|---------|----------------------|--------------|
| `skills/implementation/SKILL.md:401` | `../../docs/adr/ADR-005.md` | `../../docs/adr/archive/ADR-005.md` |
| `skills/implementation/SKILL.md:402` | `../../docs/adr/ADR-005-BP.md` | `../../docs/adr/archive/ADR-005-BP.md` |
| `skills/implementation/SKILL.md:403` | `../../docs/adr/ADR-002.md` | `../../docs/adr/archive/ADR-002.md` |
| `skills/agents-md-generator/SKILL.md:292` | `../../docs/adr/ADR-007.md` | `../../docs/adr/archive/ADR-007.md` |

---

## Fase 2: Automação e Governança

### Tarefa 2.1: Atualizar archive-adrs.sh para reconhecer artefatos de implementation [D-003]

**Arquivos:** `scripts/archive-adrs.sh`
**Complexidade:** S
**Dependências:** Tarefa 1.1 (CI funcional)
**Critérios de aceitação:**
- [ ] Script reconhece sufixos: `-execution-contract.md`, `-execution-report.md`, `-change-plan.md`
- [ ] Ao arquivar ADR-XXX, move também estes 3 novos sufixos (além de `-BP.md`, `-TODO.md`, `-implementation-plan.md`)
- [ ] Os 3 arquivos órfãos existentes (`ADR-007-change-plan.md`, `ADR-007-execution-contract.md`, `ADR-007-execution-report.md`) são movidos para `docs/adr/archive/`
- [ ] `docs/adr/INDEX.md` atualizado para incluir os 3 artefatos movidos

**Comandos de validação:**
```bash
# Dry run deve mostrar os artefatos órfãos sendo arquivados
./scripts/archive-adrs.sh --dry-run

# Após execução, verificar que docs/adr/ só tem INDEX.md e archive/
ls docs/adr/
# Deve: INDEX.md archive/

# Verificar que os artefatos estão em archive/
ls docs/adr/archive/ADR-007-*
# Deve: ADR-007-change-plan.md ADR-007-execution-contract.md ADR-007-execution-report.md ADR-007.md ...
```

**Mudança no script (linha 60):**
```bash
# ANTES:
for suffix in "-BP.md" "-TODO.md" "-implementation-plan.md"; do

# DEPOIS:
for suffix in "-BP.md" "-TODO.md" "-implementation-plan.md" "-execution-contract.md" "-execution-report.md" "-change-plan.md"; do
```

---

### Tarefa 2.2: Consolidar workflows de CI — remover sync-pages.yml [D-004]

**Arquivos:**
- `.github/workflows/sync-pages.yml` (REMOVER)
- `.github/workflows/sync-and-deploy.yml` (manter como canônico)
- `docs/adr/INDEX.md` (atualizar documentação do processo)

**Complexidade:** S
**Dependências:** Nenhuma
**Critérios de aceitação:**
- [ ] `sync-pages.yml` removido
- [ ] `sync-and-deploy.yml` é o único workflow que dispara em push em master tocando `skills/**`
- [ ] Referência a `sync-pages.yml` não existe em nenhum arquivo do repo
- [ ] Documentação do CI em `AGENTS.md` e/ou README reflete apenas `sync-and-deploy.yml`

**Comandos de validação:**
```bash
# Verificar que sync-pages.yml não existe mais
[ ! -f .github/workflows/sync-pages.yml ] && echo "OK: removido" || echo "FALHA: ainda existe"

# Verificar que sync-and-deploy.yml é único trigger de deploy
grep -rn "sync-pages" .github/ skills/ docs/ README.md AGENTS.md
# Deve: retornar ZERO resultados

# Verificar que o evento trigger não colide
grep -A5 "on:" .github/workflows/sync-and-deploy.yml
# Deve: mostrar só skills/** no push master
```

---

### Tarefa 2.3: Sincronizar versão entre README, index.json e CHANGELOG [D-005]

**Arquivos:**
- `README.md` (cabeçalho de versão)
- `skills/index.json` (campo `version`)
- `CHANGELOG.md` (se não houver entry, adicionar)

**Complexidade:** S
**Dependências:** Nenhuma
**Critérios de aceitação:**
- [ ] Versão consistente em todos os 3 arquivos (decidir: 2.1.0 ou 2.0.3 — ver nota abaixo)
- [ ] CHANGELOG tem entrada para a versão atual
- [ ] Se 2.0.3: README (L153) corrigido de v2.1.0 para v2.0.3
- [ ] Se 2.1.0: index.json atualizado para 2.1.0 E CHANGELOG ganha entry [2.1.0]

**Nota:** O correto é decidir qual versão é a real. Dado que:
- index.json (fonte de verdade para o Kilo) diz 2.0.3
- CHANGELOG último entry é [2.0.3]
- README (L153) diz v2.1.0 (sem respaldo)

A versão real é **2.0.3**. O README (L153) está errado.

**Comandos de validação:**
```bash
# Verificar consistência de versão
echo "README: $(grep -oP 'v[0-9]+\.[0-9]+\.[0-9]+' README.md | head -1)"
echo "index.json: $(jq -r '.version' skills/index.json)"
echo "CHANGELOG: $(grep -oP '\[[0-9]+\.[0-9]+\.[0-9]+\]' CHANGELOG.md | head -1)"
# Todos devem ser iguais
```

---

### Tarefa 2.4: Adicionar entry do agents-md-generator ao CHANGELOG [D-006]

**Arquivos:** `CHANGELOG.md`
**Complexidade:** S
**Dependências:** Tarefa 2.3
**Critérios de aceitação:**
- [ ] CHANGELOG tem entry `[2.0.3]` que inclui `agents-md-generator` na seção Added
- [ ] Entry menciona ADR-007, versão 1.0.0, 13 arquivos (7 templates, 3 examples, 2 checklists, 1 SKILL.md)

**Comandos de validação:**
```bash
grep -A5 "agents-md-generator" CHANGELOG.md
# Deve: mostrar entry descrevendo a skill
```

---

### Tarefa 2.5: Adicionar validação de encoding ao pipeline [D-007]

**Arquivos:**
- `scripts/validate-skill.sh` (adicionar check #11)
- `.github/workflows/validate-skills.yml` (já roda validate-skill.sh, sem mudança)

**Complexidade:** S
**Dependências:** Tarefa 1.1
**Critérios de aceitação:**
- [ ] Novo check #11 em `validate-skill.sh` detecta caracteres CJK (U+4E00-U+9FFF), árabe (U+0600-U+06FF), e outros non-Latin-1-extended fora de code blocks
- [ ] Script reporta warning (não error) para não quebrar CI existente — ou error se preferir enforcement estrito
- [ ] Os 8 pontos de vazamento existentes são corrigidos nos arquivos-fonte

**Arquivos a limpar (vazamentos CJK/árabe):**
| Arquivo | Linha | Vazamento | Substituição |
|---------|-------|-----------|--------------|
| `AGENTS.md` | 77 | `空行` | `linhas vazias` |
| `skills/agents-md-generator/templates/AGENTS-skills-repo.md` | 41 | `空行` | `linhas vazias` |
| `skills/refactoring/templates/test-before-refactor.md` | 116 | `分支` | `branches` |
| `skills/refactoring/SKILL.md` | 216 | `难以` | `difícil de` |
| `skills/refactoring/SKILL.md` | 231 | `难以` | `difícil de` |
| `skills/refactoring/SKILL.md` | 305 | `替换` | `substituir` |
| `skills/data-modeling/SKILL.md` | 56 | `Sنقem no commit` | `Sigma no commit` (corrigir Mermaid) |
| `skills/data-modeling/SKILL.md` | 239 | `覆盖索covers` | `covering index` |
| `skills/agents-md-generator/templates/AGENTS-webapp.md` | 226 | `难 de refactor` | `difícil de refatorar` |

**Comandos de validação:**
```bash
# Verificar que nenhum arquivo .md contém caracteres CJK/árabe (fora de code blocks)
# Script simplificado:
for f in $(find skills/ -name "*.md"); do
  if perl -ne 'print "$ARGV:$.: $_" if /[\x{4E00}-\x{9FFF}\x{0600}-\x{06FF}]/' "$f" 2>/dev/null; then
    echo "VAZAMENTO: $f"
  fi
done
# Deve: retornar ZERO resultados

# Ou mais simples com grep:
grep -rnP '[\x{4E00}-\x{9FFF}\x{0600}-\x{06FF}]' skills/ AGENTS.md
# Deve: retornar ZERO resultados
```

**Regex para o novo check #11 em validate-skill.sh:**
```bash
# 11. Verificar encoding (CJK/árabe fora de code blocks)
# Remove code blocks antes de verificar
if [[ -f "$SKILL_DIR/SKILL.md" ]]; then
    # Extrair texto fora de code blocks (entre ``` ... ```)
    non_code=$(sed '/^```/,/^```/d' "$SKILL_DIR/SKILL.md")
    if echo "$non_code" | grep -qP '[\x{4E00}-\x{9FFF}\x{0600}-\x{06FF}]' 2>/dev/null; then
        warn "Caracteres CJK/árabe detectados fora de code blocks (verificar encoding)"
    else
        success "Encoding limpo (sem caracteres CJK/árabe)"
    fi
fi
```

---

## Fase 3: Completude e Dogfooding

### Tarefa 3.1: Adicionar exemplos práticos a skills com templates ricos [D-008]

**Arquivos:**
- `skills/writing-plans/examples/` (criar 1-2 exemplos)
- `skills/api-design/examples/` (criar 1-2 exemplos)
- `skills/security-review/examples/` (criar 1-2 exemplos)
- `skills/ddd/examples/` (já tem 1, verificar se suficiente)

**Complexidade:** M
**Dependências:** Fase 2 completa
**Critérios de aceitação:**
- [ ] writing-plans tem ≥2 exemplos em `examples/`
- [ ] api-design tem ≥2 exemplos em `examples/`
- [ ] security-review tem ≥2 exemplos em `examples/`
- [ ] ddd tem ≥1 exemplo (já existe `order-modeling.md`)
- [ ] Cada exemplo tem ≥30 linhas com contexto, código, e output esperado

**Comandos de validação:**
```bash
# Contar exemplos por skill
for skill in writing-plans api-design security-review ddd; do
  count=$(find "skills/$skill/examples" -name "*.md" 2>/dev/null | wc -l)
  echo "$skill: $count exemplos"
done
# writing-plans: >=2, api-design: >=2, security-review: >=2, ddd: >=1
```

---

### Tarefa 3.2: Executar skill-audit-bulletin no próprio repo [D-009]

**Arquivos:**
- `docs/audits/` (criar diretório)
- `docs/audits/ignite-agents-skills-audit.md` (gerar bulletin)

**Complexidade:** M
**Dependências:** Tarefas 1.1, 1.2, 2.1-2.5, 3.1
**Critérios de aceitação:**
- [ ] Diretório `docs/audits/` existe
- [ ] Pelo menos 1 audit bulletin gerado seguindo o template em `skills/skill-audit-bulletin/templates/audit-bulletin.md`
- [ ] Bulletin cobre pelo menos as 5 skills mais críticas (implementation, adr-generator, writing-plans, governance, skill-audit-bulletin)
- [ ] Score do bulletin ≥ 90/100 (reflete as correções feitas)

**Comandos de validação:**
```bash
# Verificar que o diretório existe
[ -d docs/audits ] && echo "OK" || echo "FALTA"

# Verificar que o bulletin existe
ls docs/audits/
# Deve: mostrar pelo menos 1 arquivo .md
```

---

## Resumo de Dependências

```
Tarefa 1.1 (validate-skill.sh bug) ──┐
Tarefa 1.2 (links quebrados) ────────┤
                                      │
Tarefa 2.1 (archive-adrs.sh) ────────┤── Fase 2
Tarefa 2.2 (remover sync-pages.yml) ─┤
Tarefa 2.3 (versão) ─────────────────┤
Tarefa 2.4 (CHANGELOG) ──────────────┤
Tarefa 2.5 (encoding) ───────────────┘
                                      │
Tarefa 3.1 (exemplos) ───────────────┤── Fase 3
Tarefa 3.2 (dogfooding) ─────────────┘
```

## Ordem de Execução Recomendada

1. **Tarefa 1.1** — Corrige o bug que afeta todo o CI
2. **Tarefa 1.2** — Corrige links que agentes usam hoje
3. **Tarefa 2.2** — Remove workflow redundante (zero dependências)
4. **Tarefa 2.3** — Sincroniza versão
5. **Tarefa 2.4** — Atualiza CHANGELOG
6. **Tarefa 2.1** — Atualiza archive-adrs.sh + move órfãos
7. **Tarefa 2.5** — Adiciona validação de encoding + limpa arquivos
8. **Tarefa 3.1** — Adiciona exemplos
9. **Tarefa 3.2** — Dogfooding final

## Validação Final

Após todas as tarefas, rodar:

```bash
# 1. CI passa
./scripts/validate-index.sh && echo "index OK"

# 2. Todas as skills passam no validate-skill.sh (agora com todos os 10+ checks)
for skill in skills/*/; do
  [ -f "$skill/SKILL.md" ] || continue
  bash scripts/validate-skill.sh "$skill"
done

# 3. Sem links quebrados
grep -rn '../../docs/adr/ADR-' skills/ | grep -v archive
# Deve: ZERO

# 4. Sem vazamentos de encoding
grep -rnP '[\x{4E00}-\x{9FFF}\x{0600}-\x{06FF}]' skills/ AGENTS.md
# Deve: ZERO

# 5. Versão consistente
echo "README: $(grep -oP 'v[0-9]+\.[0-9]+\.[0-9]+' README.md | head -1)"
echo "index.json: $(jq -r '.version' skills/index.json)"
echo "CHANGELOG: $(grep -oP '\[[0-9]+\.[0-9]+\.[0-9]+\]' CHANGELOG.md | head -1)"

# 6. Sem workflow duplicado
[ ! -f .github/workflows/sync-pages.yml ] && echo "sync-pages.yml removido OK"

# 7. archive-adrs.sh reconhece artefatos novos
grep -q "execution-contract" scripts/archive-adrs.sh && echo "OK" || echo "FALTA"

# 8. Exemplos existem
for skill in writing-plans api-design security-review; do
  count=$(find "skills/$skill/examples" -name "*.md" 2>/dev/null | wc -l)
  echo "$skill: $count exemplos"
done

# 9. Audit existe
[ -f docs/audits/ignite-agents-skills-audit.md ] && echo "Audit OK" || echo "FALTA"
```

---

*Gerado por `writing-plans` seguindo ADR-008*
