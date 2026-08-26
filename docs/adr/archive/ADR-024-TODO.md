---
id: ADR-024-TODO
type: todo
title: "Execução - Otimização RICE: Lazy Loading, Unificação Code Review e Telemetria MCP"
created: 2026-08-24
updated: 2026-08-24
adr_ref: ADR-024
---

# ADR-024-TODO: Execução - Otimização RICE: Lazy Loading, Unificação Code Review e Telemetria MCP

> Referência: [ADR-024](./ADR-024-rice-optimizations-telemetry.md) | [ADR-024-BP](./ADR-024-BP.md) | Status: ✅ CONCLUIDO

## Legenda

- ✅ Concluído
- ⬜ Pendente
- 🔄 Em Andamento
- ❌ Bloqueado
- ⏸️ Pausado

**Prioridade:** 🔴 Alta | 🟡 Média | 🟢 Baixa

---

## Fase A: Telemetria em Memória no Servidor MCP (`skills_mcp_server.py`)

### A1: Implementação da Estrutura de Telemetria e Tool MCP

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|---|:---:|:---:|---|:---:|
| A1.1 | Criar classe `RAGTelemetryTracker` com contadores voláteis em memória | ✅ | 🔴 | — | ~10 min |
| A1.2 | Integrar registro de métricas nos métodos `search_skills` e `route_task` | ✅ | 🔴 | A1.1 | ~15 min |
| A1.3 | Registrar a ferramenta `get_rag_telemetry` em `MCP_TOOLS` e `handle_rpc_request` | ✅ | 🔴 | A1.2 | ~10 min |
| A1.4 | Criar suíte de testes unitários `test_mcp_telemetry.py` validando JSON-RPC e contadores | ✅ | 🔴 | A1.3 | ~15 min |

**Checkpoint A1:**
- [x] Tool `get_rag_telemetry` exposta e respondendo via Stdio JSON-RPC.
- [x] Testes unitários passando com 100% de sucesso.

---

## Fase B: Unificação do Motor de Code Review

### B1: Consolidação em `skills/code-review/` e Atualização de Aliases

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|---|:---:|:---:|---|:---:|
| B1.1 | Atualizar `skills/code-review/SKILL.md` com modos `lite` e `full` | ✅ | 🔴 | — | ~15 min |
| B1.2 | Atualizar `skills/code-review-lite/SKILL.md` como alias canônico apontando para `code-review` | ✅ | 🔴 | B1.1 | ~10 min |
| B1.3 | Validar resolução semântica no roteador para queries de revisão rápida e profunda | ✅ | 🟡 | B1.2 | ~10 min |

**Checkpoint B1:**
- [x] Triggers de code review unificados sem sobreposição ambígua.
- [x] Modo `lite` e modo `full` operando de forma determinística.

---

## Fase C: Lazy Loading de Referências Densas

### C1: Isolamento de Payloads Estáticos em `references/`

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|---|:---:|:---:|---|:---:|
| C1.1 | Criar diretório `skills/database-architecture/references/` e mover esquemas SQL extensos | ✅ | 🔴 | — | ~15 min |
| C1.2 | Refatorar `skills/database-architecture/SKILL.md` para formato conciso com lazy loading | ✅ | 🔴 | C1.1 | ~15 min |
| C1.3 | Criar diretório `skills/ui-ux-pro-max/references/` e mover tabelas de tokens de design | ✅ | 🔴 | — | ~15 min |
| C1.4 | Refatorar `skills/ui-ux-pro-max/SKILL.md` para formato conciso com lazy loading | ✅ | 🔴 | C1.3 | ~15 min |

**Checkpoint C1:**
- [x] Footprint dos arquivos `SKILL.md` reduzido em > 50%.
- [x] Instruções explícitas de `view_file` configuradas para carregamento sob demanda.

---

## Fase D: Re-indexação, Auditoria Forense e Certificação

### D1: Validação de Qualidade e Governança

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|---|:---:|:---:|---|:---:|
| D1.1 | Executar re-indexação vetorial RAG (`skills_rag_indexer.py`) | ✅ | 🔴 | C1.4 | ~10 min |
| D1.2 | Executar todas as suítes de testes (`test_mcp_telemetry.py`, `test_rag_federated.py`, `test_rag_quad_sota.py`) | ✅ | 🔴 | D1.1 | ~10 min |
| D1.3 | Executar motor de auditoria forense (`audit_engine.py`) garantindo conformidade 100% | ✅ | 🔴 | D1.2 | ~10 min |
| D1.4 | Emitir Evidence Record `ADR-024-ER.md` e sincronizar `ADR-INDEX.md` | ✅ | 🔴 | D1.3 | ~10 min |

**Checkpoint Final:**
- [x] 100% das tarefas concluídas e certificadas.
