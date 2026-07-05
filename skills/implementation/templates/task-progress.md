# Task Progress

> Progresso individual de uma tarefa durante a execução governada.

---

## Identificação

| Campo | Valor |
|-------|-------|
| Tarefa | {{task_name}} |
| Número | {{task_number}} |
| TODO | {{todo_path}} |
| Data início | {{start_date}} |

---

## Estado

| Campo | Valor |
|-------|-------|
| Estado atual | {{current_state}} |
| Data início | {{start_date}} |
| Data término | {{end_date}} |
| Duração | {{duration}} |
| Tentativas | {{attempts}} |

### Transições de Estado

| Data | De | Para | Motivo |
|------|----|------|--------|
{{#each transitions}}
| {{date}} | {{from}} | {{to}} | {{reason}} |
{{/each}}

---

## Descrição da Tarefa

{{task_description}}

---

## Dependências

| # | Dependência | Estado | Pode iniciar? |
|---|-------------|--------|---------------|
{{#each dependencies}}
| {{number}} | {{dependency}} | {{status}} | {{can_start}} |
{{/each}}

---

## Alterações Realizadas

| # | Arquivo | Tipo | Descrição | Linhas |
|---|---------|------|-----------|--------|
{{#each changes}}
| {{number}} | {{file}} | {{type}} | {{description}} | {{lines}} |
{{/each}}

---

## Validações

| # | Validação | Resultado | Tentativa | Timestamp | Observações |
|---|-----------|-----------|-----------|-----------|-------------|
{{#each validations}}
| {{number}} | {{validation}} | {{result}} | {{attempt}} | {{timestamp}} | {{notes}} |
{{/each}}

---

## Bloqueadores

| # | Bloqueador | Data Identificação | Data Resolução | Ação |
|---|------------|-------------------|----------------|------|
{{#each blockers}}
| {{number}} | {{blocker}} | {{identified}} | {{resolved}} | {{action}} |
{{/each}}

---

## Critérios de Aceite

| # | Critério | Atendido | Evidência |
|---|----------|----------|-----------|
{{#each acceptance_criteria}}
| {{number}} | {{criterion}} | {{met}} | {{evidence}} |
{{/each}}

---

## Observações

{{#each notes}}
- {{note}}
{{/each}}

---

## Resumo

| Campo | Valor |
|-------|-------|
| Tarefa concluída | {{completed}} |
| Validações passaram | {{validations_passed}} |
| Documentação atualizada | {{docs_updated}} |
| Próxima tarefa | {{next_task}} |
