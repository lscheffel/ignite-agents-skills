# Execution Report

> Relatório final produzido ao término da implementação governada.

---

## Resumo

| Campo | Valor |
|-------|-------|
| ADR referência | {{adr_path}} |
| Data de início | {{start_date}} |
| Data de término | {{end_date}} |
| Duração total | {{total_duration}} |
| Tarefas totais | {{total_tasks}} |
| Tarefas concluídas | {{completed_tasks}} |
| Tarefas adiadas | {{deferred_tasks}} |
| Tarefas bloqueadas | {{blocked_tasks}} |
| Taxa de conclusão | {{completion_rate}} |

---

## Tarefas Concluídas

| # | Tarefa | Duração | Tentativas | Validações |
|---|--------|---------|------------|------------|
{{#each completed}}
| {{number}} | {{task}} | {{duration}} | {{attempts}} | {{validations}} |
{{/each}}

---

## Tarefas Adiadas

| # | Tarefa | Justificativa | Data Revisão |
|---|--------|---------------|--------------|
{{#each deferred}}
| {{number}} | {{task}} | {{reason}} | {{review_date}} |
{{/each}}

---

## Tarefas Bloqueadas

| # | Tarefa | Bloqueador | Ação Necessária |
|---|--------|------------|-----------------|
{{#each blocked}}
| {{number}} | {{task}} | {{blocker}} | {{required_action}} |
{{/each}}

---

## Validações Executadas

| Validação | Resultado | Tentativa | Observações |
|-----------|-----------|-----------|-------------|
| Build | {{build_result}} | {{build_attempt}} | {{build_notes}} |
| Lint | {{lint_result}} | {{lint_attempt}} | {{lint_notes}} |
| Typecheck | {{typecheck_result}} | {{typecheck_attempt}} | {{typecheck_notes}} |
| Testes unitários | {{unit_test_result}} | {{unit_test_attempt}} | {{unit_test_notes}} |
| Testes integração | {{integration_test_result}} | {{integration_test_attempt}} | {{integration_test_notes}} |

---

## Alterações Realizadas

| Arquivo | Tipo | Tarefa | Linhas Adicionadas | Linhas Removidas |
|---------|------|--------|--------------------|--------------------|
{{#each changes}}
| {{file}} | {{type}} | {{task}} | {{added}} | {{removed}} |
{{/each}}

---

## Documentação Atualizada

| Documento | Tipo de Atualização | Status |
|-----------|---------------------|--------|
{{#each docs_updated}}
| {{document}} | {{update_type}} | {{status}} |
{{/each}}

---

## Riscos Remanescentes

| # | Risco | Impacto | Probabilidade | Mitigação Recomendada |
|---|-------|---------|---------------|----------------------|
{{#each remaining_risks}}
| {{number}} | {{risk}} | {{impact}} | {{probability}} | {{mitigation}} |
{{/each}}

---

## Dívida Técnica Criada

| # | Débito | Criticidade | Justificativa |
|---|--------|-------------|---------------|
{{#each tech_debt}}
| {{number}} | {{debt}} | {{criticality}} | {{justification}} |
{{/each}}

---

## Recomendações Futuras

| # | Recomendação | Prioridade | Contexto |
|---|-------------|------------|----------|
{{#each recommendations}}
| {{number}} | {{recommendation}} | {{priority}} | {{context}} |
{{/each}}

---

## Métricas da Implementação

| Métrica | Valor |
|---------|-------|
| Tempo médio por tarefa | {{avg_time_per_task}} |
| Número de rollbacks | {{rollback_count}} |
| Número de correções durante execução | {{fix_count}} |
| Cobertura de testes final | {{final_coverage}} |

---

## Conclusão

{{conclusion}}

---

## Assinatura

| Campo | Valor |
|-------|-------|
| Relatório gerado em | {{report_date}} |
| Implementação considerada | {{implementation_status}} |
| Próximos passos | {{next_steps}} |
