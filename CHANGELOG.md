# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/).

## [Unreleased]

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
