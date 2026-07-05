# TODO — ADR-{{id}}: {{title}}

> Referência: [ADR-{{id}}](./ADR-{{id}}.md) | [Blueprint](./ADR-{{id}}-BP.md)

## Status

**Progresso:** 0/{{total}} tarefas concluídas
**Início:** {{date}}
**Previsão:** {{estimated-date}}

## Tarefas

### Fase 1: {{phase-1-title}}

- [ ] 1.1 {{task-description}}
  - **Comando de validação:** `{{validation-command}}`
- [ ] 1.2 {{task-description}}
  - **Comando de validação:** `{{validation-command}}`

### Fase 2: {{phase-2-title}}

- [ ] 2.1 {{task-description}}
  - **Comando de validação:** `{{validation-command}}`
- [ ] 2.2 {{task-description}}
  - **Comando de validação:** `{{validation-command}}`

### Fase N: {{phase-n-title}}

- [ ] N.1 {{task-description}}
  - **Comando de validação:** `{{validation-command}}`

## Critérios de Finalização

Todas as tarefas devem estar `[x]` e todos os comandos de validação devem passar.

```bash
# Validação final
grep -c "\[ \]" docs/adr/ADR-{{id}}-TODO.md
# Esperado: 0
```

## Referências

- ADR: [ADR-{{id}}](./ADR-{{id}}.md)
- Blueprint: [ADR-{{id}}-BP](./ADR-{{id}}-BP.md)
