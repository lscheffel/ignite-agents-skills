# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/).

## [Unreleased]

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
