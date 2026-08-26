# Release Notes — ignite-agents-skills

> Notas oficiais de lançamento com foco em valor arquitetural, automação de governança, robustez operacional e guias de migração.

---

## Release v2.5.0 (2026-08-26) — Unificação SOTA do Ecossistema de Skills

### 🌟 Destaques da Versão (Highlights)

- **Unificação Integral do Ecossistema SOTA (59 Skills):** Consolidação definitiva de 59 skills State of the Art com padrão modular (`references/`, `templates/`, `examples/`, `scripts/`), abrangendo Arquitetura, Modelagem de Dados, Governança, RAG, Engenharia de Prompts, Frontend, Operações e Auditoria Forense.
- **Servidor MCP Stdio Dedicado (`skills-rag-mcp`):** Implementação JSON-RPC 2.0 em [`scripts/skills_mcp_server.py`](./scripts/skills_mcp_server.py) expondo 7 ferramentas analíticas (`search_skills`, `route_task`, `get_skill_details`, `list_skills_catalog`, `bootstrap_agent_instructions`, `get_rag_telemetry`, `inspect_rag_index`).
- **Motor RAG Semântico e Neural com Reranking (ADR-021 a ADR-025):** Indexador vetorial hierárquico em [`scripts/skills_rag_indexer.py`](./scripts/skills_rag_indexer.py) vetorizando 3.941 chunks com FTS5 BM25, embeddings 512/2048-dim, cache persistente SHA-256 e damping ponderado por tipo de ativo.
- **CLI Router para Descoberta no Terminal:** Ferramenta [`scripts/skills_router.py`](./scripts/skills_router.py) permitindo consultas em linguagem natural, filtros por categoria e exportação JSON/XML snippet.
- **Motor de Auditoria Forense em 8 Dimensões SOTA:** Script [`scripts/audit_engine.py`](./scripts/audit_engine.py) auditando 100% dos 81 ativos com **Score Médio de 91.10 / 100** e geração determinística de manifestos e grafos de dependência em `.github/governance/`.
- **Registry Remoto Canônico (`skills/index.json`):** Compatibilidade total com Kilo Code e OpenCode (`skills.urls`) via sincronizador determinístico [`scripts/sync-index.sh`](./scripts/sync-index.sh).
- **Static Documentation Hub (GitHub Pages):** Compilador [`pages/build.py`](./pages/build.py) gerando páginas HTML estilizadas para todas as 59 skills e todo o histórico de ADRs (ADR-001 a ADR-026).
- **Suíte de Testes Automatizados (42/42 Aprovados):** 7 suítes unitárias e de integração em [`scripts/tests/`](./scripts/tests/) com 100% de cobertura operacional.

---

## Release v2.4.0 (2026-08-24) — Ingestão Hierárquica Multi-Asset

### 🌟 Destaques da Versão (Highlights)

- **Skill Bundles e AssetParser (ADR-025):** Indexação tipada de referências, templates e docstrings de scripts com eliminação de ruído de código bruto.
- **Parent Linking & Damping Factor:** Chunks secundários vinculados à skill-mãe (`parent_skill_id`) com multiplicadores de relevância calibrados.
- **Payload XML Tipado:** Estruturação de respostas MCP/CLI com atributos semânticos para prompt injection.

---

## Release v2.3.1 (2026-07-05) — Expansão de Renderização HTML de ADRs

### 🌟 Destaques da Versão (Highlights)

- **ADR-013:** Renderização HTML automática para todo o histórico de ADRs em `docs/adr/archive/`.
- **ADR-015:** Resolução de caminhos relativos depth-aware em `pages/build.py`.

---

## Release v2.3.0 (2026-07-05) — Dynamic HTML Pages & GitHub Pages Hub

### 🌟 Destaques da Versão (Highlights)

- **ADR-012:** Conversor Markdown→HTML estático gerando documentação interativa para GitHub Pages.
- **CI Deploy Automático:** Workflow `sync-and-deploy.yml` para sincronização contínua de master para gh-pages.

---

## Release v2.2.0 (2026-07-05) — Documentation Reconciliation Hub

### 🌟 Destaques da Versão (Highlights)

- **ADR-011:** Criação da skill `technical-documentation` e governança da suíte canônica de 6 pilares (`README`, `CHANGELOG`, `USAGE`, `RELEASE-NOTES`, `STATE`, `AGENTS`).

---

## Release v2.0.0 a v2.1.0 — Fundação do Registry & Ultra-High Quality Grade

- Padronização de skills com YAML Frontmatter, Decision Trees Mermaid, Anti-patterns com severidade e Checklists.
- Criação do registry canônico `skills/index.json` para Kilo Code.
