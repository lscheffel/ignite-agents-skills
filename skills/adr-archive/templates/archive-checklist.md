# ADR Archive Checklist Template

> Checklist para validação antes de arquivar ADR

---

## Pré-requisitos de Arquivamento

### ADR Principal
- [ ] Status é "Implementado" ou "Aceito"
- [ ] ADR tem data de arquivamento
- [ ] Referências a BP, TODO, PI (se aplicável) atualizadas

### Blueprint (BP)
- [ ] BP existe: `ADR-XXX-BP.md`
- [ ] Todas as fases marcadas como concluídas
- [ ] Critérios de aceitação atendidos

### TODO
- [ ] TODO existe: `ADR-XXX-TODO.md`
- [ ] **Zero tarefas pendentes** (`[ ]` → todas `[x]`)
- [ ] Todos os comandos de validação passam

### Implementation Plan (PI) — se Tier 2/3
- [ ] PI existe: `ADR-XXX-PI.md`
- [ ] Tasks microscópicas todas concluídas
- [ ] Testes TDD passando

### Execution Report (ER)
- [ ] ER existe na raiz: `docs/adr/ADR-XXX-ER.md`
- [ ] ER documenta: o que foi feito, testes, métricas, lições
- [ ] ER linkado no ADR principal

---

## Validação de Execução

- [ ] `./scripts/archive-adrs.sh --dry-run` mostra ADR como "Ready to Archive"
- [ ] Nenhuma flag `ARCHIVED_MISTAKE_RETURN` para esta ADR
- [ ] Branch de trabalho mergeada para master
- [ ] Tag SemVer criada (se feature completa)

---

## Comando de Arquivamento

```bash
python3 audit.py . --archive ADR-XXX
# OU
./scripts/archive-adrs.sh
```

---

## Pós-Arquivamento

- [ ] `docs/adr/INDEX.md` atualizado (movido para "Archived ADRs")
- [ ] ADR + BP + TODO + PI movidos para `docs/adr/archive/`
- [ ] ER permanece em `docs/adr/` (raiz)
- [ ] Deploy gh-pages sincronizado

---

## Exceções (Não Arquivar)

- [ ] ADR com status "Proposto" ou "Em Progresso"
- [ ] ADR com TODO contendo `[ ]` (pendências)
- [ ] ADR sem ER na raiz (criar ER primeiro)
- [ ] ADR marcando débito técnico ativo (manter visível)

---

*Template: `skills/adr-archive/templates/archive-checklist.md`*