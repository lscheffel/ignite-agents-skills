# Release Notes — ignite-agents-skills

> Notas oficiais de lançamento com foco em valor arquitetural, automação de governança, robustez operacional e guias de migração.

---

## Release v3.0.1 (2026-08-27) — Pipeline Integrity & YAML Schema Hardening 🛡️

### 🌟 Destaques da Versão (Highlights)

- **YAML Frontmatter Schema Hardening (18 Skills):**
  - Padronização sintática e blindagem contra erros de parsing em 18 skills do catálogo (`related_skills` e `triggers` estritamente formatados como listas canônicas).
- **Regeneração Determinística do Registry Remoto (`skills/index.json`):**
  - Expansão estrutural do `index.json` incluindo mapeamento recursivo completo de sub-ativos modulares (`templates/`, `examples/`, `checklists/`, `references/`) com 100% de paridade com o filesystem.
- **Indexação RAG Vetorial Hierárquica Massiva (ADR-025):**
  - Vetorização e ingestão completa de **5.834 chunks** e **82 ativos** no SQLite3 (`data/skills_rag_db/skills_rag.sqlite3`) com tempo de busca sub-milissegundo.
- **Validação E2E 100% Green de Governança:**
  - Aprovação unânime no `audit_engine.py` (82/82 ativos), `validate-skill.sh` (60/60 skills), `unittest` (42/42 testes) e recompilação do Web Hub (`pages/build.py`).

---

## Release v3.0.0 (2026-08-27) — SOTA Ultra-High Quality Diamond Release 💎

### 🌟 Destaques da Versão (Highlights)

- **100% SOTA Elite Certified Catalog (Grade A+ / Grade S Diamond):**
  - Todas as 60 skills do catálogo atingiram pontuações entre **93.5 e 99.1 / 100**, com **Média Global de 96.6 / 100** (+21.2 pts desde o início).
  - **39 Skills em Grau S (Diamond $\ge 97.0$)** (65% do catálogo) e **21 Skills em Grau A+ (Platinum $\ge 93.0$)** (35% do catálogo).
  - Erradicação de 100% dos débitos técnicos cognitivos e estruturais do catálogo.
- **Consolidação e Arquivamento de 36 ADRs Canônicas (ADR-001 a ADR-036):**
  - Conclusão das 7 ADRs temáticas de remediação SOTA: `ADR-030` a `ADR-036`.
  - Conclusão das ADRs de infraestrutura e ergonomia: `ADR-027`, `ADR-028`, `ADR-029`.
  - Emissão algorítmica de 36 certificados Evidence Record (`*-ER.md`) auditáveis em `docs/adr/`.
- **Motor de Elevação e Auditoria Dual-Axis em Lote:**
  - Padronização de $\ge 9$ regras heurísticas quantitativas (`- **Rule of Thumb X:**`) por skill com vocabulário de engenharia SOTA (SOLID, DDD, AST, Idempotência, Zero-Trust, Circuit Breakers, etc.).
  - Seções dedicadas `## Edge Cases & Failure Modes` cobrindo cenários extremos em 100% das skills.
  - Suíte modular completa com $\ge 4$ artefatos de apoio (`templates/`, `examples/`, `checklists/`, `references/`) em todas as skills.
- **Normalização EN-US via LLM (NVIDIA NIM - ADR-026):**
  - Tradução e higienização formal de todos os corpos de skills, tabelas, diagramas e checklists para inglês técnico, com preservação de triggers bilíngues no YAML frontmatter.
- **Deploy Atômico Multi-Target & Purge de Runtimes:**
  - Propagação simultânea e sem drift de 360 skills para 6 diretórios de runtime (`~/.gemini/config/skills`, `~/.kilo/skills`, `~/.agents/skills`, etc.).

---

## Release v2.6.0 (2026-08-26) — Esteira de Tradução NIM & Ledger de Auditoria SOTA

### 🌟 Destaques da Versão (Highlights)

- **Pipeline de Detecção e Tradução Automática (NVIDIA NIM - ADR-026):** Integração no hook de pré-commit e CI (`validate-skills.yml`) com modelos `nemotron-3.5-30B`, `llama-3.1-8B` e `riva-translate`. Protege YAML Frontmatter, blocos de código e tags XML com cache SQLite SHA-256 (33.15% de economia de tokens).
- **Integração do Continuous Skill Audit Ledger no Pré-Commit:** Sincronização automática de `docs/audit/skills/SKILL_AUDIT_LEDGER.md` e `JSON` como 5º gate de governança ininterrupta.
- **Boletim de Auditoria Dual-Axis para `/cap` (Score 97.8 / Grau S):** Laudo canônico em `docs/audit/skills/cap_audit_bulletin.md` com análise SWOT e validação dos 8 níveis de evidência de menor custo.
- **Boletim Arquitetural SOTA Pós-Fusão:** Laudo executivo publicado em `docs/audit/ECOSYSTEM_SOTA_ARCHITECTURAL_BULLETIN.md`.

---

## Release v2.5.0 (2026-08-26) — Unificação SOTA do Ecossistema de Skills

### 🌟 Destaques da Versão (Highlights)

- **Unificação Integral do Ecossistema SOTA (60 Skills):** Consolidação definitiva de 60 skills State of the Art com padrão modular (`references/`, `templates/`, `examples/`, `scripts/`), incluindo a nova skill `adr-architecture-elevation` (Desafio Adversarial Independente de ADRs e Ampliação de Decision Sets), abrangendo Arquitetura, Modelagem de Dados, Governança, RAG, Engenharia de Prompts, Frontend, Operações e Auditoria Forense.
- **Servidor MCP Stdio Dedicado (`skills-rag-mcp`):** Implementação JSON-RPC 2.0 em [`scripts/skills_mcp_server.py`](./scripts/skills_mcp_server.py) expondo 7 ferramentas analíticas (`search_skills`, `route_task`, `get_skill_details`, `list_skills_catalog`, `bootstrap_agent_instructions`, `get_rag_telemetry`, `inspect_rag_index`).
- **Motor RAG Semântico e Neural com Reranking (ADR-021 a ADR-025):** Indexador vetorial hierárquico em [`scripts/skills_rag_indexer.py`](./scripts/skills_rag_indexer.py) vetorizando 4.161 chunks com FTS5 BM25, embeddings 512/2048-dim, cache persistente SHA-256 e damping ponderado por tipo de ativo.
- **CLI Router para Descoberta no Terminal:** Ferramenta [`scripts/skills_router.py`](./scripts/skills_router.py) permitindo consultas em linguagem natural, filtros por categoria e exportação JSON/XML snippet.
- **Motor de Auditoria Forense em 8 Dimensões SOTA:** Script [`scripts/audit_engine.py`](./scripts/audit_engine.py) auditando 100% dos 82 ativos com **Score Médio de 91.10 / 100** e geração determinística de manifestos e grafos de dependência em `.github/governance/`.
- **Registry Remoto Canônico (`skills/index.json`):** Compatibilidade total com Kilo Code e OpenCode (`skills.urls`) via sincronizador determinístico [`scripts/sync-index.sh`](./scripts/sync-index.sh) indexando 60 skills.
- **Static Documentation Hub (GitHub Pages):** Compilador [`pages/build.py`](./pages/build.py) gerando páginas HTML estilizadas para todas as 60 skills e todo o histórico de ADRs (ADR-001 a ADR-026).
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
