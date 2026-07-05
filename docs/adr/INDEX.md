# Architecture Decision Records (ADR) Index

> Última atualização: 2026-07-05

## Status Definitions

| Status | Descrição |
|--------|-----------|
| 🟢 **Ativo** | ADR em discussão ou implementação |
| 📦 **Implementado** | ADR concluída, movida para cold storage |
| ⏸️ **Proposto** | ADR ainda não aprovada |

---

## Active ADRs

| ADR | Título | Status | Data |
|-----|--------|--------|------|
| [ADR-008](./ADR-008.md) | Ultra-Avaliação v2.0.3 — Correção de Débitos Estruturais | 🟢 Proposto | 2026-07-05 |

---

## Archived ADRs (Cold Storage)

ADR's implementadas são movidas para `docs/adr/archive/` como referência.

| ADR | Título | Status | Arquivado |
|-----|--------|--------|-----------|
| [ADR-001](./archive/ADR-001.md) | Consolidar registry de skills em único index.json | ✅ Implementado | 2026-07-05 |
| [ADR-002](./archive/ADR-002.md) | Refatoração de Skills para Ultra-High Quality Grade | ✅ Implementado | 2026-07-05 |
| [ADR-003](./archive/ADR-003.md) | Retrospectiva da Implementação Ultra-High Quality Grade | ✅ Implementado | 2026-07-05 |
| [ADR-004](./archive/ADR-004.md) | Implementação das Recomendações da Ultra-Auditoria v2.0.2 | ✅ Implementado | 2026-07-05 |
| [ADR-005](./archive/ADR-005.md) | Introdução da Skill `implementation` para Execução Governada de Mudanças | ✅ Implementado | 2026-07-05 |
| [ADR-006](./archive/ADR-006.md) | Workflow CI para Auto-sync do Index e Deploy GitHub Pages | ✅ Implementado | 2026-07-05 |
| [ADR-007](./archive/ADR-007.md) | Skill para Geração de AGENTS.md Adaptativo | ✅ Implementado | 2026-07-05 |

---

## Archive Process

Para arquivar uma ADR:

1. Verificar que o status é "Implementado"
2. Executar: `./scripts/archive-adrs.sh`
3. O script move automaticamente:
   - `ADR-XXX.md` → `archive/ADR-XXX.md`
   - `ADR-XXX-BP.md` → `archive/ADR-XXX-BP.md`
   - `ADR-XXX-TODO.md` → `archive/ADR-XXX-TODO.md`
   - `ADR-XXX-implementation-plan.md` → `archive/ADR-XXX-implementation-plan.md`

Para verificar quais ADRs seriam arquivadas (dry run):
```bash
./scripts/archive-adrs.sh --dry-run
```
