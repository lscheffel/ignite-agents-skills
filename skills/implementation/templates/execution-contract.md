# Execution Contract

> Contrato obrigatório que valida se todos os artefatos necessários estão presentes antes da execução.

---

## Identificação

| Campo | Valor |
|-------|-------|
| ADR | {{adr_path}} |
| Blueprint | {{blueprint_path}} |
| TODO | {{todo_path}} |
| Data de geração | {{date}} |
| Responsável | {{agent_name}} |

---

## Artefatos

| Artefato | Path | Status | Coerente |
|----------|------|--------|----------|
| ADR | {{adr_path}} | {{adr_status}} | {{adr_coherent}} |
| Blueprint | {{blueprint_path}} | {{bp_exists}} | {{bp_coherent}} |
| TODO | {{todo_path}} | {{todo_exists}} | {{todo_coherent}} |

### Validação de Coerência

- [ ] ADR contém seção "Decisão" preenchida
- [ ] Blueprint contém tarefas documentadas
- [ ] TODO contém tarefas com estados
- [ ] Tarefas do Blueprint existem no TODO
- [ ] Dependências no TODO são consistentes com Blueprint

---

## Ambiente

| Campo | Valor |
|-------|-------|
| Branch atual | {{branch_name}} |
| Workspace limpo | {{workspace_clean}} |
| Commit HEAD | {{head_commit}} |
| Diretório de trabalho | {{working_dir}} |

### Validação do Ambiente

- [ ] Branch não é main/master (ou há PR aberto)
- [ ] Sem alterações não commitadas (git status limpo)
- [ ] Todos os arquivos impactados existem no workspace
- [ ] Branch está atualizada com remote (sem divergência)

---

## Arquivos Impactados

| Arquivo | Tipo de Mudança | Skill Relacionada |
|---------|-----------------|-------------------|
{{#each affected_files}}
| {{path}} | {{change_type}} | {{related_skill}} |
{{/each}}

---

## Critérios de Aceite

| # | Critério | Verificável |
|---|----------|-------------|
{{#each acceptance_criteria}}
| {{number}} | {{criterion}} | {{verifiable}} |
{{/each}}

---

## Critérios de Rollback

| # | Critério | Critério de Ativação |
|---|----------|---------------------|
{{#each rollback_criteria}}
| {{number}} | {{criterion}} | {{trigger}} |
{{/each}}

---

## Validação Final

- [ ] Todos os campos obrigatórios estão preenchidos
- [ ] Todos os artefatos existem e estão coerentes
- [ ] Ambiente está limpo e pronto para execução
- [ ] Critérios de aceite estão definidos e verificáveis
- [ ] Critérios de rollback estão definidos
- [ ] Contrato aprovado pelo agente executor

---

## Assinatura

| Campo | Valor |
|-------|-------|
| Contrato validado em | {{validation_date}} |
| Status | {{contract_status}} |
| Próximo passo | {{next_step}} |
