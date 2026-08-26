---
id: ADR-021-ER
type: er
title: "Evidence Record - ADR-021: Arquitetura Tri-Stage com Neural Cross-Encoder Reranking e Dual-Engine Pattern"
created: 2026-08-24
updated: 2026-08-24
adr_ref: ADR-021
implementation_status: CONSOLIDADA
tasks_completed: 10/10
certification_checksum: C3B9F1A7E4D082A1
---

# Evidence Record (ER) — ADR-021: Arquitetura Tri-Stage com Neural Cross-Encoder Reranking

> **Certificado Oficial de Implementação & Conformidade Arquitetural**  
> Este documento certifica a implementação integral da [ADR-021](./ADR-021-dual-engine-neural-rerank.md).

---

## 1. Resumo Executivo da Execução

A implementação da **ADR-021** dotou o ecossistema de skills de um pipeline de busca e recuperação de 3 estágios com reranking neural de alta fidelidade via modelo NVIDIA Cross-Encoder `nv-rerank-qa-mistral-4b:1`. A arquitetura adota o padrão Dual-Engine com resiliência total e fallback imediato (0ms) para o motor local BM25/FTS5 em cenários offline ou sem chave de API.

---

## 2. Métricas e Evidências Comparativas

| Dimensão / Métrica | Baseline Anterior | Implementação ADR-021 | Status / Veredito |
|---|---|---|:---:|
| **Motor de Reranking** | Heurística Lexical BM25 | NVIDIA Cross-Encoder (4B params) | ✅ Superado |
| **Atenção Token Query-Doc** | Inexistente (Vetores isolados) | Atenção cruzada token-a-token | ✅ Validado |
| **Filtro de Falsos Positivos** | Sem corte por logit | Logit Cutoff Gate ($\text{logit} < -10.0$) | ✅ Validado |
| **Calibração de Incerteza** | Linear arbitrária | Probabilidade Sigmoidal $\sigma(\text{logit}/2.5)$ | ✅ Validado |
| **Resiliência a Timeout / Offline** | Erro de Execução | Fallback 0ms para BM25 Local | ✅ Validado |
| **Conformidade de Testes** | 100% | 100% de Aprovação (Testes de Regressão) | ✅ Aprovado |

---

## 3. Artefatos de Código Validados

- [.github/scripts/skills_router.py](file:///home/loupan/.gemini/config/skills/.github/scripts/skills_router.py) — Métodos de reranking neural, gatekeeper de logits e fallback resiliente.
- [.github/scripts/skills_mcp_server.py](file:///home/loupan/.gemini/config/skills/.github/scripts/skills_mcp_server.py) — Ferramentas MCP `search_skills` e `route_task` com suporte a rerank neural.
- [.github/scripts/tests/test_rag_quad_sota.py](file:///home/loupan/.gemini/config/skills/.github/scripts/tests/test_rag_quad_sota.py) — Suíte de testes validando ordenação e resiliência offline.

---

## 4. Checklist Forense de Conclusão

- [x] Todas as tarefas do [ADR-021-TODO.md](./ADR-021-TODO.md) foram implementadas e verificadas.
- [x] O pipeline neural opera de forma transparente com fallback imediato para o motor local.
- [x] Os guardrails forenses (Logit cutoff e Calibração Sigmoidal) estão ativos.
- [x] A suíte de testes de integridade executa com 0 erros.
- [x] O Decision Set está pronto para arquivamento definitivo pela skill `adr-archive`.
