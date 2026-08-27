# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/).

## [3.0.1] - 2026-08-27

### Fixed
- **YAML Frontmatter Schema Hardening (18 Skills):**
  - Correção e padronização sintática de campos `related_skills` e `triggers` em 18 skills (`agent-planning-execution`, `changelog-generator`, `circuit-breaker`, `code-review-lite`, `code-review`, `context7-mcp`, `dispatching-parallel-agents`, `find-skills`, `git-workflow`, `llm-as-judge`, `observability`, `php-laravel-ecosystem`, `release`, `resilient-execution`, `subagent-driven-development`, `testing-mastery`, `verification-before-completion`, `writing-skills`).
  - Erradicação de quebras de linha e concatenações anômalas no parsing determinístico.

### Changed
- **Sincronização & Expansão do Registry (`skills/index.json`):**
  - Regeneração determinística do catálogo com inclusão de metadados enriquecidos e inventário modular de sub-ativos (`templates/`, `examples/`, `checklists/`, `references/`).
- **Indexação RAG Vetorial Semântica (ADR-025):**
  - Atualização do banco vetorial `data/skills_rag_db/skills_rag.sqlite3` com 5.834 chunks hierárquicos ingeridos e 82 ativos indexados com zero falhas.
- **Recompilação de Páginas Estáticas do Web Hub:**
  - Reconstrução completa das páginas do GitHub Pages em `pages/` via `pages/build.py`.

## [3.0.0] - 2026-08-27

### Added
- **100% SOTA Elite Certified Catalog (Grade A+ / Grade S Diamond):**
  - Todas as 60 skills do catálogo atingiram notas entre **93.5 e 99.1 / 100**, com **Média Global de 96.6 / 100**.
  - **39 Skills em Grade S (Diamond $\ge 97.0$ / 100)** e **21 Skills em Grade A+ (Platinum $\ge 93.0$ / 100)**.
  - Zero débitos técnicos cognitivos ou estruturais remanescentes no catálogo.
- **Consolidação e Arquivamento de 36 ADRs Canônicas (ADR-001 a ADR-036):**
  - Conclusão das 7 ADRs temáticas de remediação SOTA: `ADR-030` (Core Governance), `ADR-031` (AI Agents), `ADR-032` (Engineering & Coding), `ADR-033` (Backend & Cloud), `ADR-034` (Frontend & Web), `ADR-035` (Product & Content), `ADR-036` (Meta-Skills & Bootstrapping).
  - Conclusão das ADRs de infraestrutura e ergonomia: `ADR-027` (Multilingual Trigger & Metadata Hardening), `ADR-028` (Cognitive Ergonomics & Decision Graphs), `ADR-029` (Modular Asset Scaffolding).
  - Emissão algorítmica de 36 certificados Evidence Record (`*-ER.md`) visíveis na raiz de `docs/adr/`.
- **Motor de Elevação e Auditoria Dual-Axis em Lote:**
  - Injeção de $\ge 9$ regras heurísticas imperativas por skill (`- **Rule of Thumb X:**`).
  - Seções dedicadas de `## Edge Cases & Failure Modes` com cenários extremos de falha e recuperação.
  - Suíte modular padronizada com $\ge 4$ artefatos de apoio (`templates/`, `examples/`, `checklists/`, `references/`) em todas as skills.
- **Motor de Tradução e Normalização EN-US via LLM (NVIDIA NIM - ADR-026):**
  - Normalização completa de corpos de skills, diagramas Mermaid, checklists e tabelas para inglês técnico formal (EN-US).
  - Preservação estrita dos triggers e tags bilíngues no YAML frontmatter para descoberta dual PT/EN.

### Changed
- Atualização do manifesto `skills/index.json` sincronizado com todas as 60 skills e novas subpastas modulares.
- Recompilação completa das páginas estáticas do GitHub Pages via `pages/build.py`.
- Sincronização e deploy atômico multi-target para 6 runtimes locais (`~/.gemini/config/skills`, `~/.kilo/skills`, etc.) com zero drift.


### Added
- **Pipeline de Detecção e Tradução Automática (NVIDIA NIM - ADR-026):**
  - Integração no hook de pré-commit (`.githooks/pre-commit`) e CI (`validate-skills.yml`) com suporte a modelos `nemotron-3.5-30B`, `llama-3.1-8B` e `riva-translate`.
  - Preservação estrita de YAML frontmatter, blocos de código e tags XML com cache SQLite SHA-256.
- **Integração do Continuous Skill Audit Ledger no Pré-Commit:**
  - Sincronização automática de `docs/audit/skills/SKILL_AUDIT_LEDGER.md` e `JSON` como último gate de governança.
- **Boletim de Auditoria Dual-Axis para `/cap` (Score 97.8 / Grau S):**
  - Laudo em `docs/audit/skills/cap_audit_bulletin.md` com análise SWOT e validação dos 8 níveis de evidência de menor custo.
- **Boletim Arquitetural SOTA & Governança Pós-Fusão:**
  - Laudo executivo detalhado em `docs/audit/ECOSYSTEM_SOTA_ARCHITECTURAL_BULLETIN.md`.

## [2.5.0] - 2026-08-26

### Added
- **Unificação Integral do Ecossistema SOTA (60 Skills):**
  - Substituição do catálogo legado pelas **60 skills SOTA** em `skills/` (incluindo a nova skill `adr-architecture-elevation` para desafio adversarial e ampliação de ADRs).
  - Arquitetura modular preservada (`references/`, `templates/`, `examples/` e `scripts/`).
  - Suporte total a padrões bilíngues (PT/EN) em `scripts/validate-skill.sh` com 100% de aprovação.
- **Servidor MCP Stdio Dedicado (`skills-rag-mcp`):**
  - Novo servidor em `scripts/skills_mcp_server.py` implementando JSON-RPC 2.0 com 7 ferramentas analíticas: `search_skills`, `route_task`, `get_skill_details`, `list_skills_catalog`, `bootstrap_agent_instructions`, `get_rag_telemetry` e `inspect_rag_index`.
- **Motor RAG Semântico e Neural Hierárquico (ADR-021 a ADR-025):**
  - Indexador vetorial `scripts/skills_rag_indexer.py` vetorizando 4.161 chunks em `data/skills_rag_db/skills_rag.sqlite3`.
  - Busca híbrida FTS5 BM25 + Embeddings com fallback 512/2048-dim e cache SHA-256 de reranking (0ms).
- **CLI Router:**
  - Utilitário `scripts/skills_router.py` para busca semântica via terminal e exportação JSON/XML snippet.
- **Motor de Auditoria Forense em 8 Dimensões SOTA:**
  - Script `scripts/audit_engine.py` auditando 81 ativos com Score Global Médio de 91.10/100 (100% APROVADAS).
- **Suíte de Testes Automatizados:**
  - 42 testes unitários e de integração em `scripts/tests/` (100% green).
- **Reconciliação Documental dos 6 Pilares:**
  - Atualização completa de `README.md`, `CHANGELOG.md`, `USAGE.md`, `RELEASE-NOTES.md`, `STATE.md`, `AGENTS.md` e `GEMINI.md`.

### Changed
- Sincronização do registry canônico `skills/index.json` para 59 skills.
- Geração de páginas HTML dinâmicas em `pages/` para todas as 59 skills e ADR-001 a ADR-026 via `pages/build.py`.
- Atualização do workflow `.github/workflows/validate-skills.yml` com validação de index, qualidade e execução de testes.

## [2.3.1] - 2026-07-05

### Added
- **ADR-013:** Expansão do Build.py para Incluir ADRs e Referências
  - `pages/build.py` agora gera HTML para todos os ADRs em `docs/adr/archive/`
  - Links relativos convertidos automaticamente para `docs/adr/archive/ADR-XXX.md` → `adr/ADR-XXX.html`
  - +38 páginas HTML (ADRs + BP + TODO + execution artifacts)

## [2.3.0] - 2026-07-05

### Added
- **ADR-012:** Dynamic HTML Pages — Rendering de Skills em GitHub Pages
  - `pages/build.py` — conversor Markdown→HTML puro (zero deps, ~850 linhas)
  - 127 páginas HTML geradas: 23 skills + 72 templates + 18 examples + checklists + README + USAGE
  - Tema escuro profissional (charcoal #1a1a2e, laranja #ff6b2b, branco)
  - Nav sticky com breadcrumbs, busca em tempo real, responsivo
  - Título fancy com gradiente laranja→branco
  - Google Fonts Inter para tipografia premium
  - CI workflow consolidado (`sync-and-deploy.yml`): sync index + build pages + deploy gh-pages
  - Root `index.html` redireciona para `pages/index.html`
- **ADR-009:** Resolução de Débitos da Auditoria v2.1.0
  - Validação de version sync em validate-index.sh
  - Seção "Solo + Agentes" em governance/SKILL.md
  - Exemplo Python/Flask em api-design/examples/
- **ADR-010:** Branch Protection e SemVer para Tags — Emergencial
  - Regra obrigatória de branch de trabalho para implementação de ADR
  - SemVer obrigatório: nunca reaproveitar tags

## [2.2.0] - 2026-07-05

### Added
- **ADR-011:** Documentation Reconciliation Skill
  - Skill `documentation-reconciliation` — auditoria e reconciliação documental
  - Templates: audit-report.md, reconciliation-checklist.md
  - Workflow: 8 fases de auditoria e reconciliação

## [2.1.0] - 2026-07-05

### Fixed
- **validate-skill.sh bug (D-001):** `((WARNINGS++))` killed script on first warning via `set -e`. Replaced with `WARNINGS=$((WARNINGS + 1))`. CI now validates all 11 checks.
- **Broken ADR links (D-002):** 4 links in implementation/SKILL.md and agents-md-generator/SKILL.md pointed to non-existent `docs/adr/ADR-XXX.md`. Updated to `docs/adr/archive/ADR-XXX.md`.
- **Version drift (D-005):** README showed v2.1.0, index.json showed 2.0.3. Synchronized to v2.0.3.

### Added
- **archive-adrs.sh (D-003):** Now recognizes implementation artifacts: `-execution-contract.md`, `-execution-report.md`, `-change-plan.md`
- **Encoding validation (D-007):** Check #11 in validate-skill.sh detects CJK/arabic characters outside code blocks
- **CHANGELOG entry (D-006):** Added agents-md-generator entry to [2.0.3]
- **Practical examples (D-008):** 6 new examples across writing-plans, api-design, security-review
- **Audit bulletin (D-009):** `docs/audits/ignite-agents-skills-audit.md` — score 94/100 (A-)

### Changed
- **Total examples:** 18 → 24 (+33%)
- **validate-skill.sh checks:** 10 → 11 (+encoding validation)
- **archive-adrs.sh suffixes:** 3 → 6 (+execution artifacts)

### Removed
- **sync-pages.yml (D-004):** Redundant workflow removed. sync-and-deploy.yml is the single deploy workflow.

### Cleaned
- **CJK/arabic leaks (D-007):** 9 character leaks across 8 files cleaned

## [2.0.3] - 2026-07-05

### Added
- Skill `security-review` — revisão de segurança (ADR-004)
  - Secret scanning, dependency audit, criptografia, modelagem de ameaça
  - 3 templates: security-checklist, threat-model, vulnerability-report
  - Anti-patterns: nonce reuso, KDF fraco, timing attack
- Skill `agent-orchestration` — orquestração multi-agente (ADR-004)
  - Decomposição de tarefas, handoff, roteamento, paralelismo
  - 3 templates: agent-role-card, handoff-protocol, routing-decision
  - Anti-patterns: handoff sem contrato, modelo caro, sem fallback
- Skill `data-modeling` — modelagem de dados (ADR-004)
  - Schema SQL, migrations, índices, normalização
  - 3 templates: schema.sql, migration.md, index-strategy.md
  - Anti-patterns: migration sem rollback, sem PK, índice ineficiente
- Skill `api-design` — design de APIs (ADR-004)
  - REST, versionamento, erros, paginação, idempotência
  - 3 templates: endpoint-spec, error-contract, api-versioning
  - Anti-patterns: erro inconsistente, PUT sem idempotência, POST para leitura
- Skill `observability` — observabilidade (ADR-004)
  - Logging, métricas RED, alertas, distributed tracing, SLAs
  - 3 templates: logging-spec, metrics-sla, alert-rules
  - Anti-patterns: log com dados sensíveis, alerta sem ação, console.log
- Skill `refactoring` — refatoração segura (ADR-004)
  - Testes de caracterização, strangler fig, branch by abstraction
  - 3 templates: refactoring-catalog, legacy-migration, test-before-refactor
  - Anti-patterns: sem testes, refatorar + behavior, big bang
- Skill `agents-md-generator` — geração e manutenção de AGENTS.md adaptativo (ADR-007)
  - Detecção automática de contexto do projeto
  - 7 templates: AGENTS-base, AGENTS-api, AGENTS-cli, AGENTS-crm, AGENTS-library, AGENTS-skills-repo, AGENTS-webapp
  - 3 examples: before-after, context-detection, customization
  - 2 checklists: maintenance, validation
  - Anti-patterns: template genérico, sem versionamento, sem validação
- CI com `validate-skill.sh` no pipeline GitHub Actions
- Checklists para release (pre-release, post-release)
- Peer review marcado como condicional para equipes solo

### Changed
- Renomear `architecture-review` → `architecture-review-kilo` (evitar colisão com ecossistema externo)
- `planning` e `writing-plans` agora mencionam explicitamente a outra na seção "Não use quando"
- `skill-audit-bulletin` adicionado ao grafo de `related_skills` de `governance` e `repo-bootstrap`
- Total de skills: 15 → 21
- Total de templates: 45 → 63
- `index.json` version: 2.0.2 → 2.0.3

## [2.0.2] - 2026-07-05

### Added
- Skill `implementation` — execução governada de mudanças (ADR-005)
  - Execution Contract: validação pré-execução de ADR + Blueprint + TODO
  - Artifact Resolution: descoberta automática de artefatos correlacionados
  - Execution Loop: ciclo incremental com validação contínua
  - Change Lifecycle: modelo formal de ciclo de implementação
  - 5 templates: execution-contract, execution-report, change-plan, rollback-report, task-progress
  - 2 examples: simple-change, complex-change
  - 2 checklists: pre-execution, post-execution
  - 8 workflows documentados com checkpoints
  - Decision tree Mermaid com ramificação completa
  - 7+ anti-patterns com severidade 🔴🟡🟢
  - 6 edge cases documentados
- ADR-005: Introdução da Skill implementation
- ADR-005-BP: Blueprint detalhado da implementação
- ADR-005-TODO: Lista de tarefas executáveis (74 tarefas)
- `related_skills` de 9 skills atualizados para incluir `implementation`

### Changed
- Total de skills: 14 → 15
- Total de templates: 40 → 45
- Total de examples: 13 → 15
- SDLC coberto por skills: ~70% → ~95%
- `index.json` version: 2.0.1 → 2.0.2

## [2.0.1] - 2026-07-05

### Fixed
- **Ambiguidade de fonte única no registry**: existiam 3 arquivos `index.json` (`/index.json`, `/skills/index.json`, `/.well-known/skills/index.json`) com convenções de path divergentes. O mecanismo real do Kilo Code (`skills.urls`) resolve arquivos em `{url}/{skill-name}/{file}`, exigindo `files` relativo à pasta da skill. Só `skills/index.json` já seguia esse formato; `/index.json` (raiz) e `.well-known/skills/index.json` foram removidos por serem redundantes/incompatíveis.
- README instruía a usar `.well-known/skills/` como endpoint do Kilo e a registrar `files` com path completo (`skills/nome/SKILL.md`) — ambos quebravam a resolução de arquivos do Kilo. Corrigido para apontar `skills/` como endpoint e `files` relativo.
- Adicionado `LICENSE` (MIT), referenciado no README mas ausente do repositório.

### Added
- Registry inicial com 13 skills categorizadas
- Skills: writing-plans, adr-generator, architecture-review, ddd, repo-bootstrap, documentation, governance, planning, testing, prompt-engineering, git, release, vibe-coding
- Template de ADR incluso em `adr-generator/templates/adr.md`
- `scripts/validate-index.sh`: valida `skills/index.json` contra os arquivos reais (paths, prefixo indevido `skills/`, e consistência com o frontmatter `name` de cada `SKILL.md`)
- `.github/workflows/validate-skills.yml`: roda a validação acima em push/PR que tocam `skills/**`

[Unreleased]: https://github.com/lscheffel/ignite-agents-skills/compare/v2.3.1...HEAD
[2.3.1]: https://github.com/lscheffel/ignite-agents-skills/compare/v2.3.0...v2.3.1
[2.3.0]: https://github.com/lscheffel/ignite-agents-skills/compare/v2.2.0...v2.3.0
[2.2.0]: https://github.com/lscheffel/ignite-agents-skills/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/lscheffel/ignite-agents-skills/compare/v2.0.3...v2.1.0
[2.0.3]: https://github.com/lscheffel/ignite-agents-skills/compare/v2.0.2...v2.0.3
[2.0.2]: https://github.com/lscheffel/ignite-agents-skills/compare/v2.0.1...v2.0.2
[2.0.1]: https://github.com/lscheffel/ignite-agents-skills/compare/v2.0.0...v2.0.1