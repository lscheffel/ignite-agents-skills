---
id: ADR-021-PI
type: pi
title: "Plano de Implementação Granular - Arquitetura Tri-Stage com Neural Cross-Encoder Reranking"
created: 2026-08-24
updated: 2026-08-24
adr_ref: ADR-021
---

# Plano de Implementação (PI) — ADR-021: Arquitetura Tri-Stage com Neural Cross-Encoder Reranking

> Referência: [ADR-021](./ADR-021-dual-engine-neural-rerank.md) | [ADR-021-BP](./ADR-021-BP.md) | [ADR-021-TODO](./ADR-021-TODO.md)

---

## 1. Visão Geral (Overview)

Este plano detalha o roteiro de implementação do motor de recuperação e reranking neural em 3 estágios (`skills_router.py` e `skills_mcp_server.py`), integrando o modelo NVIDIA `nv-rerank-qa-mistral-4b:1` com guardrails de corte e calibração estatística.

---

## 2. Padrões de Aceitação e Qualidade

- **Latência do Fallback Local:** 0ms de espera em caso de ausência de credenciais.
- **Precisão Semântica:** Re-ordenação dos 15 candidatos do estágio 1 utilizando atenção token-a-token.
- **Logit Gatekeeper:** Descarte determinístico de itens com logit < -10.0.
- **Cobertura de Testes:** Teste end-to-end com mock de API e teste em modo offline `--no-neural`.

---

## 3. Plano de Execução Granular

### Fase A: Cliente de Reranking NVIDIA & Dual-Engine Router

#### Passo A.1: Construção do Pipeline Tri-Stage no `skills_router.py`
- Criar método `rerank_candidates_with_nvidia(query, candidate_skills)` com payload JSON formatado.
- Adicionar parsing dos campos `index` e `logit` retornados pelo endpoint.
- Aplicar fórmula sigmoidal $\sigma(\text{logit} / 2.5)$.

#### Passo A.2: Guardrails e Diversidade
- Implementar verificação de tokens sobrepostos via Jaccard similarity.
- Aplicar fallback para a ordenação prévia do SQLite caso a API retorne erro ou timeout (>4s).

### Fase B: Integração no Servidor MCP
- Integrar a chamada de reranking dentro de `route_task` e `search_skills`.
- Gerar o payload XML final com metadados de confiança.

---

## 4. Estratégia de Rollback

Caso haja instabilidade ou descontinuação do endpoint NVIDIA NIM, a flag `--no-neural` ou o fallback automático garantem 100% de disponibilidade contínua através do algoritmo local de BM25 + Feature Hashing.
