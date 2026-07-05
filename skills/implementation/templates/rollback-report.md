# Rollback Report

> Relatório produzido quando uma implementação requer reversão parcial ou total.

---

## Identificação

| Campo | Valor |
|-------|-------|
| ADR referência | {{adr_path}} |
| Data do rollback | {{rollback_date}} |
| Motivo | {{reason}} |
| Escopo | {{scope}} (parcial/total) |

---

## Motivo do Rollback

### Descrição

{{reason_description}}

### Classificação

| Critério | Valor |
|----------|-------|
| Tipo | {{type}} (erro de implementação / incompatibilidade / requisito alterado) |
| Severidade | {{severity}} (crítica / alta / média / baixa) |
| Impacto | {{impact}} (bloqueia produção / degrada funcionalidade / cosmético) |

---

## Tarefas Revertidas

| # | Tarefa | Commits Revertidos | Arquivos Afetados |
|---|--------|-------------------|-------------------|
{{#each reverted_tasks}}
| {{number}} | {{task}} | {{commits}} | {{files}} |
{{/each}}

---

## Commits Revertidos

| Hash | Mensagem | Data Original | Autor |
|------|----------|---------------|-------|
{{#each reverted_commits}}
| {{hash}} | {{message}} | {{date}} | {{author}} |
{{/each}}

---

## Estado Final

| Campo | Valor |
|-------|-------|
| Branch | {{branch}} |
| Commit final | {{final_commit}} |
| Build | {{build_status}} |
| Lint | {{lint_status}} |
| Testes | {{test_status}} |
| Workspace limpo | {{workspace_clean}} |

---

## Impacto no Progresso

| Tarefa | Estado Antes | Estado Depois |
|--------|-------------|---------------|
{{#each task_impact}}
| {{task}} | {{before}} | {{after}} |
{{/each}}

---

## Ações Corretivas

| # | Ação | Responsável | Prazo | Status |
|---|------|-------------|-------|--------|
{{#each corrective_actions}}
| {{number}} | {{action}} | {{owner}} | {{deadline}} | {{status}} |
{{/each}}

---

## Lições Aprendidas

| # | Lição | Aplicável a |
|---|-------|-------------|
{{#each lessons}}
| {{number}} | {{lesson}} | {{applicable_to}} |
{{/each}}

---

## Próximos Passos

1. {{next_step_1}}
2. {{next_step_2}}
3. {{next_step_3}}

---

## Validação do Rollback

- [ ] Todos os commits revertidos confirmados
- [ ] Build passa após rollback
- [ ] Testes passam após rollback
- [ ] Workspace está limpo
- [ ] Ações corretivas documentadas
- [ ] Lições aprendidas registradas

---

## Assinatura

| Campo | Valor |
|-------|-------|
| Rollback executado em | {{execution_date}} |
| Status do rollback | {{rollback_status}} |
| Implementação pode prosseguir | {{can_proceed}} |
