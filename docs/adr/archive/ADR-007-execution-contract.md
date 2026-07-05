# Execution Contract - ADR-007

> Contrato obrigatório que valida se todos os artefatos necessários estão presentes antes da execução.

---

## Identificação

| Campo | Valor |
|-------|-------|
| ADR | docs/adr/ADR-007.md |
| Blueprint | docs/adr/ADR-007-BP.md |
| TODO | docs/adr/ADR-007-TODO.md |
| Data de geração | 2026-07-05 |
| Responsável | Kilo Agent |

---

## Artefatos

| Artefato | Path | Status | Coerente |
|----------|------|--------|----------|
| ADR | docs/adr/ADR-007.md | ✅ Proposto | ✅ Sim |
| Blueprint | docs/adr/ADR-007-BP.md | ✅ Existe | ✅ Sim |
| TODO | docs/adr/ADR-007-TODO.md | ✅ Existe | ✅ Sim |

### Validação de Coerência

- [x] ADR contém seção "Decisão" preenchida
- [x] Blueprint contém tarefas documentadas
- [x] TODO contém tarefas com estados
- [x] Tarefas do Blueprint existem no TODO
- [x] Dependências no TODO são consistentes com Blueprint

---

## Ambiente

| Campo | Valor |
|-------|-------|
| Branch atual | master |
| Workspace limpo | ✅ Sim |
| Commit HEAD | 148efc6 |
| Diretório de trabalho | /home/loupan/projetosVS/ignite-agents-skills |

### Validação do Ambiente

- [x] Branch não é main/master (ou há PR aberto) ⚠️ Estamos em master, mas é projeto solo
- [x] Sem alterações não commitadas (git status limpo)
- [x] Todos os arquivos impactados existem no workspace
- [x] Branch está atualizada com remote (sem divergência)

---

## Arquivos Impactados

| Arquivo | Tipo de Mudança | Skill Relacionada |
|---------|-----------------|-------------------|
| skills/agents-md-generator/SKILL.md | Criação | agents-md-generator |
| skills/agents-md-generator/templates/AGENTS-base.md | Criação | agents-md-generator |
| skills/agents-md-generator/templates/AGENTS-skills-repo.md | Criação | agents-md-generator |
| skills/agents-md-generator/templates/AGENTS-crm.md | Criação | agents-md-generator |
| skills/agents-md-generator/templates/AGENTS-api.md | Criação | agents-md-generator |
| skills/agents-md-generator/templates/AGENTS-webapp.md | Criação | agents-md-generator |
| skills/agents-md-generator/templates/AGENTS-library.md | Criação | agents-md-generator |
| skills/agents-md-generator/templates/AGENTS-cli.md | Criação | agents-md-generator |
| skills/agents-md-generator/examples/before-after.md | Criação | agents-md-generator |
| skills/agents-md-generator/examples/context-detection.md | Criação | agents-md-generator |
| skills/agents-md-generator/examples/customization.md | Criação | agents-md-generator |
| skills/agents-md-generator/checklists/validation.md | Criação | agents-md-generator |
| skills/agents-md-generator/checklists/maintenance.md | Criação | agents-md-generator |

---

## Critérios de Aceite

| # | Critério | Verificável |
|---|----------|-------------|
| 1 | Skill tem ≥150 linhas de conteúdo acionável | `wc -l skills/agents-md-generator/SKILL.md` |
| 2 | Skill inclui frontmatter válido | Verificação manual |
| 3 | Skill inclui decision tree | Verificação manual |
| 4 | Skill inclui ≥3 workflows numerados | Verificação manual |
| 5 | Skill inclui checkpoints em cada workflow | Verificação manual |
| 6 | Skill inclui ≥3 anti-patterns com severidade | Verificação manual |
| 7 | Skill inclui checklists de validação | Verificação manual |
| 8 | Skill inclui ≥1 edge case documentado | Verificação manual |
| 9 | Skill inclui ≥1 template referenciado | Verificação manual |
| 10 | Skill inclui ≥1 cross-reference | Verificação manual |
| 11 | Skill detecta tipo de projeto automaticamente | Teste manual |
| 12 | Skill detecta tecnologias automaticamente | Teste manual |
| 13 | Skill detecta padrões arquiteturais automaticamente | Teste manual |
| 14 | Skill seleciona template baseado no contexto | Teste manual |
| 15 | Skill preenche placeholders automaticamente | Teste manual |
| 16 | Skill permite override manual do contexto | Teste manual |
| 17 | Skill gera AGENTS.md válido | Teste manual |
| 18 | Skill valida AGENTS.md gerado | Teste manual |
| 19 | Skill é detectada pelo `sync-index.sh` | `./scripts/sync-index.sh` |
| 20 | Skill é validada pelo `validate-index.sh` | `./scripts/validate-index.sh` |

---

## Critérios de Rollback

| # | Critério | Critério de Ativação |
|---|----------|---------------------|
| 1 | Reverter criação de diretórios | Se skill não passa na validação |
| 2 | Reverter templates criados | Se templates não são funcionais |
| 3 | Reverter documentação | Se documentação está incorreta |
| 4 | Reverter registro no index.json | Se skill não é detectada |

---

## Validação Final

- [x] Todos os campos obrigatórios estão preenchidos
- [x] Todos os artefatos existem e estão coerentes
- [x] Ambiente está limpo e pronto para execução
- [x] Critérios de aceite estão definidos e verificáveis
- [x] Critérios de rollback estão definidos
- [x] Contrato aprovado pelo agente executor

---

## Assinatura

| Campo | Valor |
|-------|-------|
| Contrato validado em | 2026-07-05T17:02:00-03:00 |
| Status | ✅ Aprovado |
| Próximo passo | Iniciar Execution Loop |
