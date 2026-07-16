# ADR Archive Report Template

> Relatório de auditoria de arquivamento de ADRs gerado por `adr-archive/scripts/audit.py`

---

## Repository State

- **Data:** {{DATE}}
- **Branch:** {{BRANCH}}
- **Commit:** {{COMMIT}}
- **Total ADRs:** {{TOTAL_ADRS}}
- **ADRs Ativas (raiz):** {{ACTIVE_ADRS}}
- **ADRs Arquivadas:** {{ARCHIVED_ADRS}}

---

## Flags de Ação

| Flag | ADR | Descrição | Ação Requerida |
|------|-----|-----------|----------------|
{{#each FLAGS}}
| {{FLAG}} | {{ADR}} | {{DESCRIPTION}} | {{ACTION}} |
{{/each}}

---

## ADRs Prontas para Arquivamento (READY_TO_ARCHIVE)

{{#each READY_TO_ARCHIVE}}
### {{ADR}} - {{TITLE}}
- **Status:** Implementado ✅
- **ER Existente:** {{HAS_ER}}
- **Comando:** `python3 audit.py . --archive {{ADR}}`
{{/each}}

---

## ADRs Arquivadas Precisando de ER (ARCHIVED_NEEDS_ER)

{{#each ARCHIVED_NEEDS_ER}}
### {{ADR}} - {{TITLE}}
- **Problema:** ADR arquivada e implementada mas sem ER na raiz
- **Ação:** Criar `docs/adr/{{ADR}}-ER.md` com relatório de conclusão
- **Template:** Usar `templates/execution-report.md` da skill `implementation`
{{/each}}

---

## ADRs Arquivadas por Erro (ARCHIVED_MISTAKE_RETURN)

{{#each ARCHIVED_MISTAKE_RETURN}}
### {{ADR}} - {{TITLE}}
- **Problema:** ADR arquivada mas TODO tem pendências (parciais ou totais)
- **Ação:** Devolver para raiz: `mv docs/adr/archive/{{ADR}}* docs/adr/`
- **Pendências:** {{PENDING_TASKS}}
{{/each}}

---

## Débitos Técnicos Consolidados

{{#each TECH_DEBTS}}
### {{ADR}} - {{TITLE}}
**Severidade:** {{SEVERITY}}
**Descrição:** {{DESCRIPTION}}
**Arquivos Afetados:** {{FILES}}
**Sugestão:** {{SUGGESTION}}
{{/each}}

---

## Resumo de Ações Tomadas

{{#each ACTIONS_TAKEN}}
- [x] {{ACTION}}
{{/each}}

---

## Próximos Passos Recomendados

1. {{NEXT_STEP_1}}
2. {{NEXT_STEP_2}}
3. {{NEXT_STEP_3}}

---

*Gerado automaticamente por `adr-archive` skill*