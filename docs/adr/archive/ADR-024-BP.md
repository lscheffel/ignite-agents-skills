---
id: ADR-024-BP
type: bp
title: "Blueprint - Otimização RICE: Lazy Loading, Unificação Code Review e Telemetria MCP"
created: 2026-08-24
updated: 2026-08-24
adr_ref: ADR-024
---

# Blueprint — ADR-024: Otimização de Context Budget, Unificação de Code Review e Telemetria MCP

> Referência: [ADR-024](./ADR-024-rice-optimizations-telemetry.md)

---

## 1. Visão Geral

### Objetivo
Executar as três iniciativas estruturais de alta prioridade (P1/P2) da Matriz RICE:
1. **Telemetria de Runtime no MCP:** Exposição da ferramenta `get_rag_telemetry` com contadores de latência, cache hits e distribuição de escopo.
2. **Unificação de Code Review:** Consolidação de `code-review` e `code-review-lite` em um motor único com modos `lite` e `full`.
3. **Lazy Loading de Referências:** Isolamento de catálogos e schemas em subpastas `references/` para `database-architecture` e `ui-ux-pro-max`.

### Métricas de Sucesso

| Métrica | Antes | Depois (Alvo) | Status |
|---|---|---|:---:|
| **Footprint de `ui-ux-pro-max` (Tokens)** | ~7.200 tokens | < 2.000 tokens no core | ⬜ |
| **Footprint de `database-architecture` (Tokens)** | ~6.800 tokens | < 2.000 tokens no core | ⬜ |
| **Sobreposição Semântica em Code Review** | 68% de sobreposição | 0% (motor unificado) | ⬜ |
| **Visibilidade de Métricas MCP em Tempo Real** | 0% (Invisível) | 100% via `get_rag_telemetry` | ⬜ |
| **Cobertura de Testes Automatizados** | 100% | 100% com novos testes | ⬜ |

---

## 2. Estrutura de Artefatos Afetados

```text
skills/
├── code-review/
│   └── SKILL.md                  # Atualização: Motor unificado com mode: lite | full
├── code-review-lite/
│   └── SKILL.md                  # Atualização: Apontamento para o motor unificado
├── database-architecture/
│   ├── SKILL.md                  # Refatoração: Núcleo conciso de regras e decisões
│   └── references/               # Novo: Schemas DDL, migration patterns e antipatterns
└── ui-ux-pro-max/
    ├── SKILL.md                  # Refatoração: Núcleo conciso de diretrizes e workflows
    └── references/               # Novo: Design tokens completos e tabelas de paletas

.github/scripts/
├── skills_mcp_server.py          # Atualização: Classe de telemetria e tool get_rag_telemetry
└── tests/
    └── test_mcp_telemetry.py     # Novo: Suíte de testes unitários para a tool de telemetria
```

---

## 3. Especificação Técnica por Módulo

### 3.1 Módulo 1: Telemetria em Memória (`skills_mcp_server.py`)

#### Estrutura de Dados Volátil em Memória
```python
class RAGTelemetry:
    def __init__(self):
        self.total_queries = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.neural_calls = 0
        self.fallback_calls = 0
        self.latencies_ms = []
        self.scope_counts = {"global": 0, "workspace_local": 0}
        self.start_time = time.time()
```

#### Retorno da Tool `get_rag_telemetry`
```json
{
  "uptime_seconds": 1420.5,
  "total_queries": 45,
  "cache_hit_ratio_percent": 64.4,
  "cache_hits": 29,
  "cache_misses": 16,
  "neural_calls": 14,
  "fallback_calls": 2,
  "average_latency_ms": 32.4,
  "scope_distribution": {
    "global": 38,
    "workspace_local": 7
  },
  "nvidia_api_configured": true
}
```

### 3.2 Módulo 2: Unificação de Code Review

- **`code-review`**:
  - Aceita chamadas genéricas de revisão com trigger primário.
  - Se o usuário pedir velocidade, PR pequeno ou vibe-coding, ativa o **`mode: lite`**.
  - Se o usuário pedir rigor, segurança profunda ou auditoria formal, ativa o **`mode: full`**.
- **`code-review-lite`**:
  - Redireciona de forma canônica para `code-review (mode: lite)`.

### 3.3 Módulo 3: Lazy Loading em `database-architecture` & `ui-ux-pro-max`

- **Diretriz Canônica no Frontmatter e Corpo do `SKILL.md`:**
  ```markdown
  ### Lazy Loading de Referências Estáticas
  Para consultar a tabela exata de design tokens ou esquemas avançados de modelagem, leia sob demanda os artefatos especializados em `references/` através da ferramenta `view_file`:
  - Design Tokens: `references/design-tokens.md`
  - Migration Patterns & DDL: `references/migration-patterns.md`
  ```

---

## 4. Riscos e Mitigações

| Risco | Impacto | Mitigação Arquitetural |
|---|---|---|
| Quebra de compatibilidade em agentes buscando `code-review-lite` | Baixo | `code-review-lite` é mantido como alias compatível direcionando para `code-review` |
| Agente não encontrar design tokens após refatoração | Baixo | Menção explícita do caminho relativo em `references/` no corpo do `SKILL.md` |
