---
id: ADR-024
type: adr
title: "Otimização de Context Budget via Lazy Loading, Unificação do Motor de Code Review e Telemetria de Runtime no MCP"
created: 2026-08-24
updated: 2026-08-24
implementation_status: CONSOLIDADA
depends_on:
  - ADR-021
  - ADR-022
  - ADR-023
---

# ADR-024: Otimização de Context Budget via Lazy Loading, Unificação do Motor de Code Review e Telemetria de Runtime no MCP

## Status

**Implementado / Consolidado**

## Contexto

### Diagnóstico

A auditoria arquitetural forense baseada no Framework de 8 Dimensões SOTA (Score 91.10/100) identificou três oportunidades de alto retorno (Matriz RICE) para otimizar o consumo de contexto, a precisão semântica de roteamento e a observabilidade do servidor MCP:

1. **Footprint Estático Excessivo em Skills Densas (D3 - Token Economy):**
   Skills como [`database-architecture`](../../skills/database-architecture/SKILL.md) e [`ui-ux-pro-max`](../../skills/ui-ux-pro-max/SKILL.md) mantêm tabelas extensas de design tokens, esquemas SQL, scripts DDL e regras de migração embutidas diretamente no corpo do `SKILL.md` (ultrapassando 7.000 a 11.000 tokens em repouso). Mesmo com a injeção por chunks (ADR-022), o parsing inicial e o tamanho do índice no banco SQLite são inflados desnecessariamente.

2. **Concorrência e Ambiguidade Semântica no Cluster de Code Review (D6 - Modularidade):**
   A divisão entre `code-review` (multi-agent rigoroso) e `code-review-lite` (focado em agilidade e vibe-coding) gera 68% de sobreposição funcional em triggers. O roteador semântico (ADR-021) sofre dispersão de probabilidades Top-1 para instruções genéricas como *"revise esse código antes do commit"*.

3. **Ausência de Observabilidade de Runtime no MCP Stdio (D5 - Resiliência & Telemetria):**
   O servidor `skills-rag-mcp` opera em background via Stdio JSON-RPC sem expor uma ferramenta para inspeção em tempo de execução da taxa de cache hits (`rerank_cache`), latência dos estágios de busca e status de conectividade com a API da NVIDIA.

---

## Decisão

Adotamos a **Consolidação de Governança e Otimizações RICE (ADR-024)**, estruturada em 3 frentes arquiteturais:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        ARQUITETURA DE OTIMIZAÇÕES RICE (ADR-024)                       │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│  1. OBSERVABILIDADE RUNTIME         2. UNIFICAÇÃO CODE REVIEW       3. LAZY LOADING    │
│  ┌─────────────────────────┐       ┌─────────────────────────┐     ┌─────────────────┐ │
│  │   get_rag_telemetry()   │       │   skills/code-review/   │     │  SKILL.md Core  │ │
│  │   - Cache Hit Ratio     │       │   - mode: "lite"        │     │  (<2000 tokens) │ │
│  │   - Average Latency     │       │     (rápido/vibe-coding)│     └────────┬────────┘ │
│  │   - Scopes (Global/Loc) │       │   - mode: "full"        │              │view_file │
│  │   - NVIDIA NIM Status   │       │     (multi-agent audit) │              ▼          │
│  └─────────────────────────┘       └─────────────────────────┘     ┌─────────────────┐ │
│                                                                    │  references/    │ │
│                                                                    │  - tokens.md    │ │
│                                                                    │  - schemas.sql  │ │
│                                                                    └─────────────────┘ │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### Módulo 1: Observabilidade de Runtime via MCP Tool `get_rag_telemetry`
- Implementar a ferramenta `get_rag_telemetry` no `skills_mcp_server.py`.
- Rastrear contadores voláteis em memória: `total_queries`, `cache_hits`, `cache_misses`, `neural_calls`, `fallback_calls`, `avg_latency_ms` e `scope_distribution` (`global` vs `workspace_local`).

### Módulo 2: Unificação Modular do Motor de Code Review
- Consolidar as diretrizes de `code-review-lite` dentro de `skills/code-review/SKILL.md`.
- Adicionar suporte a parâmetro de intensidade:
  - **`mode: lite`** (padrão rápido para inspeção de regressões, security sanity check e broken assumptions).
  - **`mode: full`** (inspeção exaustiva multi-agente, verificação formal de cadeia de suprimentos e matriz de consenso).
- Atualizar `code-review-lite` com apontamento explícito para o motor consolidado, eliminando duplicidade de triggers.

### Módulo 3: Padrão Lazy Loading de Referências Densas
- Isolar catálogos estáticos e templates longos em subpastas `references/` para `database-architecture` e `ui-ux-pro-max`.
- Reduzir os `SKILL.md` principais para < 2.000 tokens, mantendo apenas contratos, heurísticas de decisão e workflows.
- Orientar o agente explicitamente a utilizar `view_file` para consultar arquivos em `references/` apenas quando estritamente necessário.

---

## Alternativas Consideradas

### Alternativa A: Manter os dois motores de Code Review separados
- **Prós:** Nenhum esforço de refatoração de skills existentes.
- **Contras:** Manutenção de 68% de sobreposição funcional e dispersão de scores no Cross-Encoder Top-1.

### Alternativa B: Não isolar referências em subpastas e confiar apenas na injeção por chunks
- **Prós:** Mantém arquivo único por skill.
- **Contras:** Indexador vetorial precisa processar arquivos desnecessariamente gigantes e o system prompt consome tokens a mais ao carregar a skill completa.

### Alternativa C: Consolidação RICE Integral com Telemetria MCP (Escolhida)
- **Prós:** Redução de até 60% no footprint de skills densas, unificação do fluxo de code review e transparência operacional instantânea em tempo real.
- **Contras:** Pequena refatoração nos diretórios das skills afetadas.

---

## Consequências

### Positivas
- **Economia de Tokens:** Redução de mais de 50% no footprint de ativação de `database-architecture` e `ui-ux-pro-max`.
- **Precisão Semântica Aumentada:** 0% de ambiguidade entre code review lite e completo.
- **Observabilidade em Tempo Real:** Capacidade de inspecionar a saúde e performance do RAG sob demanda através da tool `get_rag_telemetry`.

### Considerações Operacionais
- Os agentes deverão utilizar a tool `view_file` para carregar dados de `references/` quando precisarem de exemplos aprofundados ou listas completas de design tokens.

---

## Referências

- Evidence Record: (pendente - execução via skill `implementation`)
- Blueprint: [ADR-024-BP.md](./ADR-024-BP.md)
- Checklist de Execução: [ADR-024-TODO.md](./ADR-024-TODO.md)
- Implementation Plan: [ADR-024-PI.md](./ADR-024-PI.md)
