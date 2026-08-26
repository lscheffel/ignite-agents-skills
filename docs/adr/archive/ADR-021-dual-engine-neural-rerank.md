---
id: ADR-021
type: adr
title: "Arquitetura Tri-Stage com Neural Cross-Encoder Reranking e Dual-Engine Pattern"
created: 2026-08-24
updated: 2026-08-24
implementation_status: CONSOLIDADA
---

# ADR-021: Arquitetura Tri-Stage com Neural Cross-Encoder Reranking e Dual-Engine Pattern

## Status

**Aceito** (Implementado na Release v2.0.0+)

## Contexto

### Diagnóstico

O ecossistema de 81 skills do repositório necessita de alta precisão no roteamento dinâmico e na descoberta contextual por agentes de IA.
A estratégia baseada puramente em SQLite3 + BM25 + Feature Hashing fornece um bootstrap rápido, determinístico e local (zero-network), ideal para validações pré-commit e ambientes isolados. Contudo, em consultas densas com nuances semânticas complexas e terminologia cruzada, abordagens baseadas exclusivamente em contagem lexical ou hashes estáticos sofrem com:

1. **Falta de Atenção Cruzada Query-Documento:** Vetores isolados não capturam a relação direta de atenção token-a-token entre a pergunta do usuário e os parágrafos de documentação.
2. **Poluição de Contexto:** A ausência de filtros forenses (corte por logit) pode introduzir falsos positivos no System Prompt de agentes autônomos.
3. **Redundância Informativa:** Skills com propósitos sobrepostos podem disputar espaço no orçamento de contexto do modelo.

## Decisão

Adotamos a **Arquitetura Tri-Stage SOTA com Padrão Dual-Engine**:

```
                  ┌────────────────────────────────────────┐
                  │          Query / Instrução IA          │
                  └───────────────────┬────────────────────┘
                                      │
                 ┌────────────────────┴───────────────────┐
                 │                                        │
        [Se NVIDIA_API_KEY setada]                 [Modo Local / Fallback]
                 │                                        │
                 ▼                                        ▼
    ┌─────────────────────────┐              ┌─────────────────────────┐
    │  ADR-021 SOTA Pipeline  │              │    SQLite3 Hashing      │
    │  - FTS5 BM25 + Vector   │              │    - BM25 FTS5          │
    │  - nv-rerank-qa-mistral │              │    - Feature Hashing    │
    │  - Guardrails & Logits  │              │    - Zero-Dep Local     │
    └─────────────────────────┘              └─────────────────────────┘
```

### Estágio 1: Recuperação Híbrida Paralela (Candidate Pool Generation)
- Extração de candidatos ($top\_k \times 5$ ou mínimo de 15) através da combinação do embedding denso max-pooled por chunks com o índice léxico FTS5 BM25 e boosting de triggers exatos.

### Estágio 2: Cross-Encoding Neural com NVIDIA Reranker
- Envio do pool deduplicado de candidatos para o modelo `nv-rerank-qa-mistral-4b:1` via endpoint `https://ai.api.nvidia.com/v1/retrieval/nvidia/reranking`.
- Avaliação de atenção token-level entre query e os metadados canônicos da skill (nome, categoria, descrição, gatilho, resumo).

### Estágio 3: Guardrails Forenses e Desduplicação de Contexto
- **Logit Cutoff Gate:** Rejeição determinística de qualquer candidato com $\text{logit} < -10.0$.
- **Calibração de Probabilidade Sigmoidal:** $\text{confidence} = \sigma\left(\frac{\text{logit}}{2.5}\right) \times 100\%$.
- **Anti-Redundancy Diversity Filtering:** Cálculo de Jaccard token overlap ($> 0.70$) para impedir que skills redundantes saturem o prompt.

## Alternativas Consideradas

### Alternativa A: Manter puramente BM25 + Feature Hashing Local
- **Prós:** Zero dependências de rede, custo zero de API.
- **Contras:** Baixo recall para queries semânticas abstratas e ausência de atenção token-level query-documento.

### Alternativa B: Usar Embeddings Locais Densos com PyTorch / HuggingFace
- **Prós:** Execução local sem dependência de chaves de API externas.
- **Contras:** Dependências pesadas (>2GB), lentidão de inicialização no Stdio MCP e alto consumo de memória RAM.

### Alternativa C: Dual-Engine Híbrido com NVIDIA Cross-Encoder e Fallback Local (Escolhida)
- **Prós:** Máxima precisão semântica via modelo de 4 bilhões de parâmetros na nuvem, com resiliência total e 0ms de bloqueio no fallback local offline.
- **Contras:** Requer configuração de `NVIDIA_API_KEY` para ativação do estágio neural.

## Consequências

### Positivas
- **Precisão SOTA:** Rerank com compreensão semântica profunda das intenções do desenvolvedor.
- **Resiliência Total:** Fallback silencioso e imediato para o motor local caso haja timeout ($> 4$s), ausência de chave ou falha de conexão.
- **Zero Overhead em Hooks Locais:** Pre-commit hooks continuam operando de forma 100% offline e ultra-rápida.

### Considerações Operacionais
- Requer `NVIDIA_API_KEY` (configurada via variável de ambiente ou injetada no ambiente do servidor MCP).

## Referências

- Evidence Record: [ADR-021-ER.md](./ADR-021-ER.md)
- Blueprint: [ADR-021-BP.md](./ADR-021-BP.md)
- Implementation Plan: [ADR-021-PI.md](./ADR-021-PI.md)
- Checklist de Execução: [ADR-021-TODO.md](./ADR-021-TODO.md)
