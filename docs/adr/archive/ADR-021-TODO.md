---
id: ADR-021-TODO
type: todo
title: "Execução - Arquitetura Tri-Stage com Neural Cross-Encoder Reranking"
created: 2026-08-24
updated: 2026-08-24
adr_ref: ADR-021
---

# ADR-021-TODO: Execução - Arquitetura Tri-Stage com Neural Cross-Encoder Reranking

> Referência: [ADR-021](./ADR-021-dual-engine-neural-rerank.md) | [ADR-021-BP](./ADR-021-BP.md) | Status: ✅ CONCLUÍDO

## Legenda

- ✅ Concluído
- ⬜ Pendente
- 🔄 Em Andamento
- ❌ Bloqueado
- ⏸️ Pausado

**Prioridade:** 🔴 Alta | 🟡 Média | 🟢 Baixa

---

## Fase A: Motor de Reranking Cross-Encoder Neural

### A1: Integração com Endpoint NVIDIA NIM

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|---|:---:|:---:|---|:---:|
| A1.1 | Implementar cliente HTTP para o endpoint `retrieval/nvidia/reranking` | ✅ | 🔴 | — | ~20 min |
| A1.2 | Implementar serialização do pool de candidatos (nome, descrição, triggers, resumo) | ✅ | 🔴 | A1.1 | ~15 min |
| A1.3 | Adicionar tratamento de timeout (4s) e tratamento de códigos HTTP de erro | ✅ | 🔴 | A1.1 | ~15 min |
| A1.4 | Implementar fallback resiliente para o algoritmo local quando a API estiver indisponível | ✅ | 🔴 | A1.3 | ~15 min |

**Checkpoint A1:**
- [x] Reranker neural responde com sucesso para consultas em ambiente com NVIDIA_API_KEY.
- [x] Fallback local ativa sem falha quando a chave não está presente ou em modo offline.

---

## Fase B: Guardrails Forenses e Calibração

### B1: Filtros e Normalização de Confiança

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|---|:---:|:---:|---|:---:|
| B1.1 | Implementar gatekeeper de corte de logits ($\text{logit} < -10.0$) | ✅ | 🔴 | A1.2 | ~15 min |
| B1.2 | Implementar calibração sigmoidal para estimativa de probabilidade percentual | ✅ | 🔴 | B1.1 | ~10 min |
| B1.3 | Implementar cálculo de similaridade de Jaccard e poda de candidatos redundantes (>0.70) | ✅ | 🟡 | B1.2 | ~20 min |

**Checkpoint B1:**
- [x] Candidatos com logit abaixo do corte são sumariamente descartados.
- [x] Candidatos redundantes têm suas posições rebaixadas preservando a diversidade.

---

## Fase C: Integração no Servidor MCP e Roteador CLI

### C1: Exposição de Interfaces

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|---|:---:|:---:|---|:---:|
| C1.1 | Integrar reranker neural ao comando `skills_router.py "<query>"` | ✅ | 🔴 | B1.3 | ~20 min |
| C1.2 | Integrar pipeline neural aos métodos `search_skills` e `route_task` no servidor MCP | ✅ | 🔴 | C1.1 | ~20 min |
| C1.3 | Adicionar flag `--no-neural` no CLI para testes e benchmarking local offline | ✅ | 🟡 | C1.1 | ~10 min |

**Checkpoint C1:**
- [x] CLI e MCP server operam com pipeline neural ativo por padrão e fallback transparente.
- [x] Suíte de testes executa com 100% de aprovação.
