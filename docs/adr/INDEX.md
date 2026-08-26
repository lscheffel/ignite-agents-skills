# Architecture Decision Records (ADR) Index

> Índice canônico de registros de decisão arquitetural (ADR) do repositório `ignite-agents-skills`.

---

## 1. Status das Decisões

| Status | Descrição |
|:---|:---|
| 🟢 **Ativo** | ADR em discussão ou implementação ativa |
| 📦 **Consolidado / Arquivado** | ADR concluída e arquivada com Evidence Record (`*-ER.md`) |
| ⏸️ **Proposto** | ADR em fase de proposta preliminar |

---

## 2. Decisões Arquiteturais Consolidadas (ADR-001 a ADR-026)

| ADR | Título | Status | Data | Evidence Record / Arquivo |
|:---|:---|:---:|:---:|:---|
| **ADR-001** | Consolidar registry de skills em único index.json | 📦 Consolidado | 2026-07-05 | [`archive/ADR-001.md`](./archive/ADR-001.md) |
| **ADR-002** | Refatoração de Skills para Ultra-High Quality Grade | 📦 Consolidado | 2026-07-05 | [`archive/ADR-002.md`](./archive/ADR-002.md) |
| **ADR-003** | Retrospectiva da Implementação Ultra-High Quality Grade | 📦 Consolidado | 2026-07-05 | [`archive/ADR-003.md`](./archive/ADR-003.md) |
| **ADR-004** | Implementação das Recomendações da Ultra-Auditoria v2.0.2 | 📦 Consolidado | 2026-07-05 | [`archive/ADR-004.md`](./archive/ADR-004.md) |
| **ADR-005** | Introdução da Skill `implementation` para Execução Governada de Mudanças | 📦 Consolidado | 2026-07-05 | [`archive/ADR-005.md`](./archive/ADR-005.md) |
| **ADR-006** | Workflow CI para Auto-sync do Index e Deploy GitHub Pages | 📦 Consolidado | 2026-07-05 | [`archive/ADR-006.md`](./archive/ADR-006.md) |
| **ADR-007** | Skill para Geração de AGENTS.md Adaptativo | 📦 Consolidado | 2026-07-05 | [`archive/ADR-007.md`](./archive/ADR-007.md) |
| **ADR-008** | Ultra-Avaliação v2.0.3 — Correção de Débitos Estruturais | 📦 Consolidado | 2026-07-05 | [`archive/ADR-008.md`](./archive/ADR-008.md) |
| **ADR-009** | Resolução de Débitos da Auditoria v2.1.0 | 📦 Consolidado | 2026-07-05 | [`archive/ADR-009.md`](./archive/ADR-009.md) |
| **ADR-010** | Branch Protection e SemVer para Tags — Emergencial | 📦 Consolidado | 2026-07-05 | [`archive/ADR-010.md`](./archive/ADR-010.md) |
| **ADR-011** | Documentation Reconciliation Skill | 📦 Consolidado | 2026-07-05 | [`archive/ADR-011.md`](./archive/ADR-011.md) |
| **ADR-012** | Dynamic HTML Pages — Rendering de Skills em GitHub Pages | 📦 Consolidado | 2026-07-05 | [`archive/ADR-012.md`](./archive/ADR-012.md) |
| **ADR-013** | Expansão do Build.py para Incluir ADRs e Referências | 📦 Consolidado | 2026-07-05 | [`archive/ADR-013.md`](./archive/ADR-013.md) |
| **ADR-014** | Fix Workflow sync-and-deploy — Sync Completo de master para gh-pages | 📦 Consolidado | 2026-07-06 | [`archive/ADR-014.md`](./archive/ADR-014.md) |
| **ADR-015** | Fix Caminhos Relativos Depth-Aware no Build.py | 📦 Consolidado | 2026-07-06 | [`archive/ADR-015.md`](./archive/ADR-015.md) |
| **ADR-021** | Dual-Engine Neural Rerank com GPU NVIDIA e Cutoff Gate | 📦 Consolidado | 2026-08-24 | [`ADR-021-ER.md`](./ADR-021-ER.md) |
| **ADR-022** | RAG SOTA Quad Optimizations: Embeddings 2048-dim, Cache Rerank, Chunks Focalizados | 📦 Consolidado | 2026-08-24 | [`ADR-022-ER.md`](./ADR-022-ER.md) |
| **ADR-023** | Federated Multi-Scope RAG com Descoberta em 12 Convenções de Agentes | 📦 Consolidado | 2026-08-24 | [`ADR-023-ER.md`](./ADR-023-ER.md) |
| **ADR-024** | Consolidação RICE: Telemetria de Runtime no MCP e Lazy Loading de Referências | 📦 Consolidado | 2026-08-24 | [`ADR-024-ER.md`](./ADR-024-ER.md) |
| **ADR-025** | Hierarchical Multi-Asset Ingestion com Damping e Parent Linking | 📦 Consolidado | 2026-08-24 | [`ADR-025-ER.md`](./ADR-025-ER.md) |
| **ADR-026** | Automação SSOT de Instruções via `bootstrap_agent_instructions` | 📦 Consolidado | 2026-08-25 | [`ADR-026-ER.md`](./ADR-026-ER.md) |

---

## 3. Processo de Arquivamento & Janitor

O ciclo de vida de ADRs é governado pelo script `scripts/archive-adrs.sh` ou pela skill `adr-archive`:
1. Uma vez implementada e validada, a ADR emite seu Evidence Record (`ADR-XXX-ER.md`).
2. Os artefatos operacionais (`ADR-XXX-BP.md`, `ADR-XXX-TODO.md`, `ADR-XXX-PI.md`) são movidos para `docs/adr/archive/`.
3. O Evidence Record permanece visível no diretório `docs/adr/` como comprovante canônico de conclusão.
