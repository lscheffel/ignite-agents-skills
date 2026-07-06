# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/).

## [Unreleased]

### Added
- (nenhuma mudança desde v2.3.0)

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

[Unreleased]: https://github.com/lscheffel/ignite-agents-skills/compare/v2.3.0...HEAD
[2.3.0]: https://github.com/lscheffel/ignite-agents-skills/compare/v2.2.0...v2.3.0
[2.2.0]: https://github.com/lscheffel/ignite-agents-skills/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/lscheffel/ignite-agents-skills/compare/v2.0.3...v2.1.0
[2.0.3]: https://github.com/lscheffel/ignite-agents-skills/compare/v2.0.2...v2.0.3
[2.0.2]: https://github.com/lscheffel/ignite-agents-skills/compare/v2.0.1...v2.0.2
[2.0.1]: https://github.com/lscheffel/ignite-agents-skills/compare/v2.0.0...v2.0.1
