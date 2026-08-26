---
id: ADR-024-PI
type: pi
title: "Plano de Implementação Granular - Otimização RICE: Lazy Loading, Unificação Code Review e Telemetria MCP"
created: 2026-08-24
updated: 2026-08-24
adr_ref: ADR-024
---

# Plano de Implementação (PI) — ADR-024: Otimização RICE: Lazy Loading, Unificação Code Review e Telemetria MCP

> Referência: [ADR-024](./ADR-024-rice-optimizations-telemetry.md) | [ADR-024-BP](./ADR-024-BP.md) | [ADR-024-TODO](./ADR-024-TODO.md)

---

## 1. Visão Geral (Overview)

Este plano detalha as etapas microscópicas de código, refatoração de conteúdo e desenvolvimento guiado por testes (TDD) para entregar as três frentes da ADR-024.

---

## 2. Padrões de Aceitação e Qualidade

- **Schema da Tool `get_rag_telemetry`:** Integrada ao padrão JSON-RPC 2.0 sem dependências externas adicionais.
- **Isolamento de Lazy Loading:** `SKILL.md` reduzido em pelo menos 50% de linhas mantendo 100% da precisão técnica através de ponteiros `view_file` para `references/`.
- **Compatibilidade Retroativa:** Preservação de compatibilidade de triggers em `code-review-lite`.
- **Cobertura de Testes:** Suíte de testes `test_mcp_telemetry.py` cobrindo chamadas normais, incrementos de contadores, métricas de cache e cálculo de tempo de uptime.

---

## 3. Plano de Execução Granular (Step-by-Step)

### Fase A: Telemetria em Memória no Servidor MCP (`skills_mcp_server.py`)

#### Passo A.1: Implementação da Classe `RAGTelemetryTracker`
1. Adicionar classe `RAGTelemetryTracker` no topo de `skills_mcp_server.py`.
2. Implementar métodos:
   - `record_query(latency_ms, cache_hit, neural_call, scope)`
   - `get_metrics() -> dict`

#### Passo A.2: Adição da Tool MCP `get_rag_telemetry`
1. Inserir schema formal em `MCP_TOOLS`:
   ```json
   {
     "name": "get_rag_telemetry",
     "description": "Retorna métricas em tempo real de latência, taxa de cache hits, chamadas neurais e escopos ativos.",
     "inputSchema": {
       "type": "object",
       "properties": {}
     }
   }
   ```
2. Adicionar roteamento em `handle_rpc_request`.

#### Passo A.3: Testes Automatizados (`test_mcp_telemetry.py`)
1. Testar resposta inicial da tool com métricas zeradas.
2. Testar incremento correto após invocação de `search_skills` e `route_task`.
3. Testar formato JSON-RPC 2.0.

---

### Fase B: Unificação do Motor de Code Review

#### Passo B.1: Refatoração de `skills/code-review/SKILL.md`
1. Inserir seção formal de seleção de modo (`mode: "lite" | "full"`).
2. Documentar diretrizes rápidas para vibe-coding e protocolo estrito para security/enterprise.

#### Passo B.2: Ajuste em `skills/code-review-lite/SKILL.md`
1. Configurar frontmatter e instrução apontando para `code-review (mode: lite)`.

---

### Fase C: Lazy Loading de Referências Densas

#### Passo C.1: Modularização de `database-architecture`
1. Criar `skills/database-architecture/references/antipatterns-and-schemas.md`.
2. Mover tabelas DDL e diagramas extensos.
3. Atualizar `SKILL.md` mantendo regras de modelagem e instrução de lazy loading.

#### Passo C.2: Modularização de `ui-ux-pro-max`
1. Criar `skills/ui-ux-pro-max/references/design-tokens-and-palettes.md`.
2. Mover tabelas de cores, espaçamentos e escalas tipográficas.
3. Atualizar `SKILL.md` com as regras centrais de design system e instrução de leitura sob demanda.

---

## 4. Estratégia de Rollback

Como todas as mudanças são puramente aditivas ou de desacoplamento modular em diretórios isolados, caso ocorra qualquer regressão semântica nos testes, a restauração via Git pode ser realizada de forma atômica por arquivo.
