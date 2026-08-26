---
id: ADR-022
type: adr
title: "Pipeline RAG Quádruplo SOTA: Cache de Reranking, Embeddings Nemotron-3, Injeção por Chunks e Expansão de Siglas"
created: 2026-08-24
updated: 2026-08-24
implementation_status: CONSOLIDADA
depends_on:
  - ADR-021
---

# ADR-022: Pipeline RAG Quádruplo SOTA: Cache de Reranking, Embeddings Nemotron-3, Injeção por Chunks e Expansão de Siglas

## Status
**Proposto**

## Contexto

### Diagnóstico

O ecossistema de skills atingiu o patamar de recuperação neural híbrida através da [ADR-021](./ADR-021-dual-engine-neural-rerank.md) (FTS5 BM25 + NVIDIA Reranker `nv-rerank-qa-mistral-4b:1`). Contudo, com a escala de chamadas frequentes de agentes de IA e a complexidade de queries técnicas curtas, foram identificadas quatro oportunidades críticas de otimização de latência, custo e economia de contexto:

| Capacidade / Gargalo | Status Atual | Evidência / Impacto |
|---|---|---|
| **Latência de Consultas Repetidas** | Inexistente (Cache Miss = 100%) | Toda consulta repetida consome ~200ms de roundtrip de rede e quota de API da NVIDIA. |
| **Recall Semântico Inicial (Estágio 1)** | Feature Hashing 512-dim | Termos conceituais abstratos dependem excessivamente do BM25 antes do Reranker. |
| **Orçamento de Contexto (Tokens)** | Injeção da Descrição Geral Fixa | Skills densas consomem tokens desnecessários com seções irrelevantes para a query. |
| **Queries com Siglas / Acrônimos** | Dependência de correspondência literal | Siglas técnicas curtas (RBAC, XSS, TDD, DDD, CI/CD) podem ter baixo recall no FTS5. |

### Consequências da Lacuna
- Desperdício de quotas em chamadas repetidas da mesma intenção.
- Risco de recall imperfeito no Estágio 1 para perguntas metafóricas ou com jargões técnicos ultracurtos.
- Overhead de tokens no System Prompt de agentes autônomos.

---

## Decisão

Adotamos a **Quadra de Otimizações SOTA do Pipeline RAG (ADR-022)**, composta por quatro módulos integrados:

```
                  ┌────────────────────────────────────────────────────────┐
                  │                 Query do Desenvolvedor                 │
                  └───────────────────────────┬────────────────────────────┘
                                              │
                                   [Módulo 4: Expansão Siglas]
                                              │
                                   [Módulo 1: Cache Rerank Hit?]
                                   ├── Sim ➔ Resposta em 0ms
                                   └── Não ➔ Continua Pipeline
                                              │
                    ┌─────────────────────────┴────────────────────────┐
                    │                                                  │
                    ▼                                                  ▼
     ┌─────────────────────────────┐                    ┌─────────────────────────────┐
     │      BM25 Léxico FTS5       │                    │  [Módulo 2: Nemotron Embed] │
     │  (Expandido com Sinônimos)  │                    │ (nvidia/nemotron-3-embed-1b)│
     │      SQLite3 Local          │                    │     2048-dim Vetor Denso    │
     └──────────────┬──────────────┘                    └──────────────┬──────────────┘
                    │                                                  │
                    └─────────────────────────┬────────────────────────┘
                                              │
                                              ▼
                             ┌─────────────────────────────────┐
                             │       Pool de Candidatos        │
                             │      (Top 15 mais densos)       │
                             └────────────────┬────────────────┘
                                              │
                                              ▼
                             ┌─────────────────────────────────┐
                             │    NVIDIA Cross-Encoder Rerank  │
                             │    (nv-rerank-qa-mistral-4b:1)  │
                             │    ➔ Salva no Cache SQLite3     │
                             └────────────────┬────────────────┘
                                              │
                                              ▼
                             ┌─────────────────────────────────┐
                             │      Guardrails Forenses        │
                             │  - Logit Cutoff (< -10.0)       │
                             │  - Jaccard Overlap (> 0.70)     │
                             └────────────────┬────────────────┘
                                              │
                                              ▼
                             ┌─────────────────────────────────┐
                             │ [Módulo 3: Chunk Focused Inject]│
                             │ Retorna apenas o chunk pontual  │
                             │ Economia de até 70% de tokens   │
                             └─────────────────────────────────┘
```

### 1. Módulo 1: Cache Local de Reranking Persistente
- Implementação de tabela `rerank_cache` no SQLite3 (`skills_rag.sqlite3`) com chave composta `SHA256(query + candidate_ids)`.
- Resposta instantânea (**0ms**) para consultas repetidas ou ligeiramente reordenadas, com TTL configurável e invalidação automática na reindexação de skills.

### 2. Módulo 2: Dual-Model Embeddings (NVIDIA Nemotron-3 2048-dim + Fallback ONNX/Hashing)
- Suporte a geração e busca de embeddings de 2.048 dimensões via `nvidia/nemotron-3-embed-1b` no endpoint `https://integrate.api.nvidia.com/v1/embeddings`.
- Fallback automático para `bge-small-en-v1.5` (ONNX local) ou Feature Hashing 512-dim quando offline.

### 3. Módulo 3: Injeção Dinâmica por Chunks (Token Economy)
- O roteador identifica a seção mais relevante (`section_title` e `chunk_text`) da skill selecionada e gera um payload XML enxuto contendo apenas o trecho focalizado (`<focused_chunk>`), reduzindo até 70% do consumo de contexto do System Prompt.

### 4. Módulo 4: Expansão Semântica de Siglas e Acrônimos (Lexical Expansion)
- Dicionário determinístico de termos de engenharia (ex: `RBAC`, `XSS`, `TDD`, `DDD`, `ADR`, `CI/CD`, `SOTA`) injetado transparentemente na query do FTS5 como cláusulas `OR` ponderadas.

---

## Alternativas Consideradas

### Alternativa A: Manter apenas SQLite + Reranker sem Cache nem Embeddings Densos
- **Prós**: Zero código novo, pipeline já funcional.
- **Contras**: Custo desnecessário de chamadas repetidas, latência de rede em todas as requisições, sem compressão de tokens por chunk.

### Alternativa B: Migrar toda a base para Vector Database gerenciado em Nuvem (Pinecone / Qdrant Cloud)
- **Prós**: Alta escalabilidade para milhões de documentos.
- **Contras**: Cria dependência externa obrigatória, quebra o pre-commit local offline e adiciona custo de infraestrutura para uma base de 81 skills.

### Alternativa C: Quadra SOTA Local-First com NVIDIA NIM & SQLite3 Híbrido (Escolhida)
- **Prós**: 0ms de latência em cache hits, 100% de operação offline preservada, máxima fidelidade semântica via Nemotron-3 e economia agressiva de tokens de prompt.
- **Contras**: Requer implementação de novas tabelas de cache e mapeamento de chunks no SQLite3.

---

## Consequências

### Positivas
- **Latência Zero em Cache Hits:** 0ms para buscas repetidas de agentes no mesmo loop de trabalho.
- **Precisão Semântica End-to-End:** Estágio 1 (Nemotron-3) e Estágio 2 (Mistral Rerank) unificados no ecossistema NVIDIA NIM.
- **Eficiência de Prompt:** Redução drástica de tokens injetados via foco seletivo em chunks.
- **Alta Resiliência:** Preserva 100% de funcionamento offline quando `NVIDIA_API_KEY` não estiver disponível.

### Riscos e Mitigações
- **Risco**: Invalidação de cache após edição de uma skill.
  - **Mitigação**: O script `skills_rag_indexer.py` limpa automaticamente a tabela `rerank_cache` durante a reindexação.
- **Risco**: Estouro de tamanho do banco SQLite devido ao cache.
  - **Mitigação**: Política de retenção LRU com teto de 5.000 entradas.

---

## Referências
- [ADR-021: Arquitetura Tri-Stage com Neural Cross-Encoder Reranking](./ADR-021-dual-engine-neural-rerank.md)
- [NVIDIA Nemotron-3-Embed-1B Model Card](https://build.nvidia.com/nvidia/nemotron-3-embed-1b/modelcard)
- [NVIDIA Reranking Mistral 4B Model Card](https://build.nvidia.com/nvidia/reranking-qa-mistral-4b)
- Evidence Record: (pendente)
