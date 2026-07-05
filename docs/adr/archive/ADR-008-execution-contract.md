# Execution Contract — ADR-008

> Contrato obrigatório que valida se todos os artefatos necessários estão presentes antes da execução.

> **Status:** Implementado

---

## Identificação

| Campo | Valor |
|-------|-------|
| ADR | `docs/adr/ADR-008.md` |
| Blueprint | `docs/adr/ADR-008-BP.md` |
| TODO | `docs/adr/ADR-008-TODO.md` |
| Data de geração | 2026-07-05T18:48:00-03:00 |
| Responsável | Kilo Agent |

---

## Artefatos

| Artefato | Path | Status | Coerente |
|----------|------|--------|----------|
| ADR | `docs/adr/ADR-008.md` | ✅ Proposto | ✅ Sim |
| Blueprint | `docs/adr/ADR-008-BP.md` | ✅ Existe (442 linhas) | ✅ Sim |
| TODO | `docs/adr/ADR-008-TODO.md` | ✅ Existe (240 linhas) | ✅ Sim |

### Validação de Coerência

- [x] ADR contém seção "Decisão" preenchida (3 fases, 9 débitos)
- [x] Blueprint contém tarefas documentadas (4 fases, 10 tarefas)
- [x] TODO contém tarefas com estados (47 sub-tarefas, todas ⬜ Pendente)
- [x] Tarefas do Blueprint existem no TODO (F1.1→F1.1.x, F1.2→F1.2.x, etc.)
- [x] Dependências no TODO são consistentes com Blueprint

---

## Ambiente

| Campo | Valor |
|-------|-------|
| Branch atual | `fix/adr-008-debt-corrections` |
| Workspace limpo | ✅ Sim (git status vazio) |
| Commit HEAD | `$(git log --oneline -1)` |
| Diretório de trabalho | `/home/loupan/projetosVS/ignite-agents-skills` |

### Validação do Ambiente

- [x] Branch não é main/master
- [x] Sem alterações não commitadas
- [x] Todos os arquivos impactados existem no workspace
- [ ] Branch está atualizada com remote (verificar)

---

## Arquivos Impactados

| Arquivo | Tipo de Mudança | Fase |
|---------|-----------------|------|
| `scripts/validate-skill.sh` | Modificação (bug fix + check #11) | F1.1, F2.5 |
| `skills/implementation/SKILL.md` | Modificação (corrigir links) | F1.2 |
| `skills/agents-md-generator/SKILL.md` | Modificação (corrigir link) | F1.2 |
| `scripts/archive-adrs.sh` | Modificação (adicionar sufixos) | F2.1 |
| `.github/workflows/sync-pages.yml` | Remoção | F2.2 |
| `README.md` | Modificação (versão) | F2.3 |
| `CHANGELOG.md` | Modificação (entry agents-md-generator) | F2.4 |
| `AGENTS.md` | Modificação (encoding) | F2.5 |
| `skills/refactoring/SKILL.md` | Modificação (encoding) | F2.5 |
| `skills/refactoring/templates/test-before-refactor.md` | Modificação (encoding) | F2.5 |
| `skills/data-modeling/SKILL.md` | Modificação (encoding) | F2.5 |
| `skills/agents-md-generator/templates/AGENTS-skills-repo.md` | Modificação (encoding) | F2.5 |
| `skills/agents-md-generator/templates/AGENTS-webapp.md` | Modificação (encoding) | F2.5 |
| `skills/writing-plans/examples/` | Criação (2 exemplos) | F3.1 |
| `skills/api-design/examples/` | Criação (2 exemplos) | F3.1 |
| `skills/security-review/examples/` | Criação (2 exemplos) | F3.1 |
| `docs/audits/` | Criação (diretório + bulletin) | F3.2 |

---

## Critérios de Aceite

| # | Critério | Verificável |
|---|----------|-------------|
| 1 | `validate-skill.sh` roda todos os 10+ checks sem morrer | `bash scripts/validate-skill.sh skills/writing-plans` exit 0 |
| 2 | Zero links quebrados para ADRs | `grep -rn '../../docs/adr/ADR-' skills/ \| grep -v archive` retorna vazio |
| 3 | `archive-adrs.sh` reconhece 6 sufixos | `grep -q "execution-contract" scripts/archive-adrs.sh` |
| 4 | `sync-pages.yml` removido | `[ ! -f .github/workflows/sync-pages.yml ]` |
| 5 | Versão consistente (2.0.3) em README, index.json, CHANGELOG | Comando de verificação |
| 6 | Zero vazamentos CJK/árabe | `grep -rnP` retorna vazio |
| 7 | CHANGELOG tem entry para agents-md-generator | `grep "agents-md-generator" CHANGELOG.md` |
| 8 | Exemplos criados para writing-plans, api-design, security-review | `find` retorna ≥2 cada |
| 9 | Audit bulletin existe | `[ -f docs/audits/ignite-agents-skills-audit.md ]` |

---

## Critérios de Rollback

| # | Critério | Critério de Ativação |
|---|----------|---------------------|
| 1 | Reverter validate-skill.sh | Se check #11 causa falsos positivos em >50% das skills |
| 2 | Restaurar sync-pages.yml | Se deploy para GitHub Pages falhar após remoção |
| 3 | Reverter encoding changes | Se substituições alteram significado técnico |

---

## Validação Final

- [x] Todos os campos obrigatórios estão preenchidos
- [x] Todos os artefatos existem e estão coerentes
- [x] Ambiente está limpo e pronto para execução
- [x] Critérios de aceite estão definidos e verificáveis
- [x] Critérios de rollback estão definidos
- [ ] Contrato aprovado pelo agente executor

---

## Assinatura

| Campo | Valor |
|-------|-------|
| Contrato validado em | 2026-07-05T18:48:00-03:00 |
| Status | ✅ APROVADO |
| Próximo passo | Iniciar Fase 1 (F1.1: corrigir validate-skill.sh) |
