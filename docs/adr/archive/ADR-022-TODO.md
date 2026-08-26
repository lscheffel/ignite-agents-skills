---
id: ADR-022-TODO
type: todo
title: "Execução - Pipeline RAG Quádruplo SOTA"
created: 2026-08-24
updated: 2026-08-24
adr_ref: ADR-022
---

# ADR-022-TODO: Execução - Pipeline RAG Quádruplo SOTA

> Referência: [ADR-022](./ADR-022-rag-sota-quad-optimizations.md) | [ADR-022-BP](./ADR-022-BP.md) | Status: ✅ CONCLUÍDO

## Legenda

- ✅ Concluído
- ⬜ Pendente
- 🔄 Em Andamento
- ❌ Bloqueado
- ⏸️ Pausado

**Prioridade:** 🔴 Alta | 🟡 Média | 🟢 Baixa

---

## Fase A: Cache Persistente & Expansão de Siglas

### A1: Módulo de Cache SQLite3 e Expansão Lexical

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|---|:---:|:---:|---|:---:|
| A1.1 | Criar tabela `rerank_cache` no `skills_mcp_server.py` e `skills_rag_indexer.py` | ✅ | 🔴 | — | ~15 min |
| A1.2 | Implementar hash SHA-256 e lookup/save de cache no `skills_router.py` | ✅ | 🔴 | A1.1 | ~20 min |
| A1.3 | Adicionar dicionário `ACRONYM_EXPANSION_DICT` e expansão de termos no FTS5 | ✅ | 🔴 | — | ~15 min |
| A1.4 | Implementar invalidação de cache durante a execução do `skills_rag_indexer.py` | ✅ | 🟡 | A1.1 | ~10 min |

**Checkpoint A1:**
- [x] Consultas repetidas retornam instantaneamente do cache em 0ms.
- [x] Query como `"RBAC"` ou `"TDD"` ativa corretamente as skills associadas.

---

## Fase B: Embeddings Densos Nemotron-3 (2048-dim)

### B1: Ingestão e Vetorização com NVIDIA NIM

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|---|:---:|:---:|---|:---:|
| B1.1 | Implementar função `get_nemotron_embedding` via endpoint NIM no indexador | ✅ | 🔴 | — | ~25 min |
| B1.2 | Adicionar coluna `vector_embedding_2048` na tabela `skills` e `skill_chunks` | ✅ | 🔴 | B1.1 | ~15 min |
| B1.3 | Atualizar busca vetorial do `skills_router.py` para operar em 2048-dim quando disponível | ✅ | 🔴 | B1.2 | ~20 min |
| B1.4 | Garantir fallback estrito para 512-dim hash quando offline | ✅ | 🔴 | B1.3 | ~15 min |

**Checkpoint B1:**
- [x] Banco armazena e consulta vetores densos de 2048 dimensões.
- [x] Fallback offline 100% funcional.

---

## Fase C: Injeção Dinâmica por Chunks (Token Economy)

### C1: Foco em Seções Específicas no Prompt XML

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|---|:---:|:---:|---|:---:|
| C1.1 | Implementar método `get_best_matching_chunk(skill_id, query_vec)` no roteador | ✅ | 🔴 | B1.3 | ~20 min |
| C1.2 | Atualizar `generate_prompt_payload` para injetar o bloco `<focused_chunk>` | ✅ | 🔴 | C1.1 | ~15 min |
| C1.3 | Atualizar `route_task` no MCP Server para fornecer telemetria de tokens economizados | ✅ | 🟡 | C1.2 | ~15 min |

**Checkpoint C1:**
- [x] XML gerado contém o trecho exato da seção relevante sem inflar o contexto.

---

## Resumo Geral

| Fase | Tarefas | Horas Est. | Status |
|---|---|:---:|:---:|
| **Fase A: Cache Persistente & Expansão de Siglas** | 4 | ~1h 00m | ✅ |
| **Fase B: Embeddings Densos Nemotron-3 (2048-dim)** | 4 | ~1h 15m | ✅ |
| **Fase C: Injeção Dinâmica por Chunks (Token Economy)** | 3 | ~50m | ✅ |
| **Total** | **11** | **~3h 05m** | ✅ CONCLUÍDO |

---

*Documento gerado em 2026-08-24. Referência: ADR-022.*
