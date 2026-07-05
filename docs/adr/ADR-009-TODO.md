# TODO — ADR-009: Resolução de Débitos da Auditoria v2.1.0

> Referência: [ADR-009](./ADR-009.md) | [Blueprint](./ADR-009-BP.md)

## Status

**Progresso:** 0/8 tarefas concluídas
**Início:** 2026-07-05
**Previsão:** 2026-07-05

## Tarefas

### Fase 1: Validação CI — Version Sync Check

- [ ] 1.1 Extrair versão do `skills/index.json` via jq
  - **Comando de validação:** `jq -r '.version' skills/index.json`
- [ ] 1.2 Extrair versão do `README.md` via grep
  - **Comando de validação:** `grep -oP 'v\K[0-9]+\.[0-9]+\.[0-9]+' README.md | head -1`
- [ ] 1.3 Comparar e reportar erro se divergente
  - **Comando de validação:** `bash scripts/validate-index.sh`
- [ ] 1.4 Testar com versão consistente e inconsistente
  - **Comando de validação:** `echo "Teste manual: alterar README.md e rodar validate-index.sh"`

### Fase 2: Atualização de Skills

- [ ] 2.1 Adicionar seção "Solo + Agentes" em `governance/SKILL.md`
  - **Comando de validação:** `bash scripts/validate-skill.sh skills/governance`
- [ ] 2.2 Atualizar referência "Claude Opus 3" em `agent-orchestration/SKILL.md`
  - **Comando de validação:** `bash scripts/validate-skill.sh skills/agent-orchestration`
- [ ] 2.3 Validar skills com `validate-skill.sh`
  - **Comando de validação:** `bash scripts/validate-skill.sh skills/governance && bash scripts/validate-skill.sh skills/agent-orchestration`

### Fase 3: Documentação e Ciclo de Vida

- [ ] 3.1 Verificar que AGENTS.md documenta ciclo ADR → Arquivamento → Deploy
  - **Comando de validação:** `grep -c "Ciclo de Vida de uma ADR" AGENTS.md`
- [ ] 3.2 Adicionar exemplo multi-stack em `api-design/examples/`
  - **Comando de validação:** `ls skills/api-design/examples/ | grep -c ".md"`
- [ ] 3.3 Atualizar CHANGELOG com entries desta iteração
  - **Comando de validação:** `grep -c "ADR-009" CHANGELOG.md`

## Critérios de Finalização

Todas as tarefas devem estar `[x]` e todos os comandos de validação devem passar.

```bash
# Validação final
grep -c "\[ \]" docs/adr/ADR-009-TODO.md
# Esperado: 0
```

## Referências

- ADR: [ADR-009](./ADR-009.md)
- Blueprint: [ADR-009-BP](./ADR-009-BP.md)
