# ignite-agents-skills

Registro centralizado de skills para agentes compatíveis com o padrão [Agent Skills](https://agentskills.io).

Hospedado como GitHub Pages, este repositório serve como registry remoto para múltiplos projetos que usam **Kilo**, **OpenCode** e outros agentes compatíveis.

> **Nota de compatibilidade (Kilo Code):** o mecanismo `skills.urls` do Kilo busca `{url}/index.json` e resolve cada arquivo em `{url}/{skill-name}/{file}`, onde `file` é **relativo à pasta da própria skill** (ex.: `"SKILL.md"`, não `"skills/nome/SKILL.md"`). Por isso o manifesto canônico é `skills/index.json` (paths relativos), e a URL configurada no Kilo deve apontar para a pasta `skills/`, não para `.well-known/skills/`. Uma tentativa anterior de seguir a convenção `.well-known/` usava paths completos no `files`, o que quebra a resolução do Kilo (duplicação de path) — por isso foi removida.

## Estrutura

```
.
├── LICENSE
├── USAGE.md                          # Guia completo de uso das skills
├── skills/
│   ├── index.json                    # Registry de skills (fonte única)
│   ├── adr-archive/
│   ├── adr-generator/
│   ├── agent-orchestration/
│   ├── agents-md-generator/          # 🆕 Skill para AGENTS.md adaptativo
│   ├── api-design/
│   ├── architecture-review-kilo/
│   ├── data-modeling/
│   ├── ddd/
│   ├── documentation/
│   ├── documentation-reconciliation/
│   ├── git/
│   ├── governance/
│   ├── implementation/
│   ├── observability/
│   ├── planning/
│   ├── prompt-engineering/
│   ├── refactoring/
│   ├── release/
│   ├── repo-bootstrap/
│   ├── security-review/
│   ├── skill-audit-bulletin/
│   ├── testing/
│   ├── vibe-coding/
│   └── writing-plans/
├── scripts/
│   ├── archive-adrs.sh               # Arquiva ADRs implementadas
│   ├── sync-index.sh                 # Auto-gera index.json
│   ├── validate-index.sh             # Valida index.json contra arquivos reais
│   └── validate-skill.sh             # Valida qualidade Ultra-High Quality Grade
└── docs/
    └── adr/
        ├── INDEX.md                  # Índice de ADRs (active + archived)
        └── archive/                  # Cold storage (ADRs implementadas)
            ├── ADR-001.md
            ├── ADR-002.md
            ├── ADR-003.md
            ├── ADR-004.md
            ├── ADR-005.md
            ├── ADR-006.md
            └── ADR-007.md
```

## Categorias

| Categoria | Skills |
|-----------|--------|
| Architecture | `architecture-review-kilo`, `ddd` |
| Documentation | `documentation`, `adr-generator`, `documentation-reconciliation` |
| Governance | `governance`, `repo-bootstrap`, `agents-md-generator` |
| Planning | `planning`, `writing-plans` |
| Implementation | `implementation` |
| Quality | `testing` |
| Security | `security-review` |
| AI | `prompt-engineering`, `vibe-coding` |
| Orchestration | `agent-orchestration` |
| Data | `data-modeling` |
| API | `api-design` |
| Operations | `observability` |
| Code Quality | `refactoring` |
| Tools | `git`, `release` |
| Audit | `skill-audit-bulletin` |

## Publicação (GitHub Pages)

1. Habilite GitHub Pages em **Settings → Pages**
2. Source: **Deploy from a branch**
3. Branch: `main` (ou `master`) — repositório precisa ser **público** (Pages privado exige plano pago do GitHub, e o Kilo faz fetch simples, sem autenticação)
4. Após deploy, o registry estará disponível em:

```
https://<usuario>.github.io/ignite-agents-skills/skills/
```

Confirme que está no ar antes de configurar o Kilo:

```
curl -I https://<usuario>.github.io/ignite-agents-skills/skills/index.json
```

## Configuração no Kilo

No Kilo Code (VS Code): **Kilo Settings → Comportamento do Agente → Habilidades → URLs de Habilidades**, adicione:

```
https://<usuario>.github.io/ignite-agents-skills/skills/
```

(com a barra final). Se preferir configurar via arquivo, use `skills.urls` no seu `kilo.json`:

```json
{
  "skills": {
    "urls": [
      "https://<usuario>.github.io/ignite-agents-skills/skills/"
    ]
  }
}
```

O Kilo busca `{url}/index.json`, e para cada skill listada baixa os arquivos de `{url}/{skill-name}/{file}`. Por isso `files` no `index.json` **deve ser relativo à pasta da skill** — nunca inclua o prefixo `skills/nome-da-skill/`.

## Como Adicionar uma Nova Skill

1. Crie o diretório: `skills/nova-skill/`
2. Adicione o `SKILL.md` com frontmatter `name` e `description`
3. Adicione arquivos auxiliares se necessário
4. O `skills/index.json` é sincronizado **automaticamente** via workflow de CI/CD
5. Rode `scripts/validate-index.sh` localmente para confirmar que os paths resolvem
6. Rode `bash scripts/validate-skill.sh skills/nova-skill` para validar qualidade
7. Commit e push para `master`

**Nota:** O workflow `sync-and-deploy.yml` sincroniza automaticamente o index.json e faz deploy para GitHub Pages quando há alterações na pasta `skills/`.

## Padrão de Skill

Cada `SKILL.md` deve conter:

```yaml
---
name: nome-da-skill
description: Descrição curta para o agente decidir quando usar.
---
```

### Ultra-High Quality Grade

Skills refatoradas seguem o padrão Ultra-High Quality Grade (v2.0.0+) com:

- **Decision Trees** — Mermaid graphs para decisão automática
- **Workflows** — Passos executáveis com critérios de aceitação
- **Anti-patterns** — Indicadores de severidade (🔴 crítico, 🟡 alerta, 🟢 suave)
- **Checklists** — Verificação de qualidade antes/depois
- **Edge Cases** — Cobertura de cenários excepcionais
- **Templates** — 72 templates disponíveis em `skills/*/templates/`
- **Examples** — 18 exemplos em `skills/*/examples/`

## Status da Implementação

**v2.3.1 — Skills Ultra-High Quality Grade**

| Métrica | Status |
|---------|--------|
| Skills total | 25 ✅ |
| Skills refatoradas | 25/25 ✅ |
| Templates criados | 72+ ✅ |
| Examples criados | 18+ ✅ |
| Páginas HTML geradas | 140+ ✅ |
| ADRs renderizadas | 38 ✅ |
| Validação automática | ✅ |
| CI pipeline | ✅ (`validate-skill.sh` + `validate-index.sh`) |
| Auto-sync index.json | ✅ (`sync-and-deploy.yml`) |
| GitHub Pages | ✅ |
| Dynamic HTML Pages | ✅ (`pages/build.py`) |
| SDLC completo | ✅ |

## Decisões Arquiteturais

Decisões arquiteturais significativas são documentadas em [docs/adr/](./docs/adr/):

**Ativas:**
- *Nenhuma ADR ativa*

**Arquivadas (Cold Storage):**
- [ADR-001: Consolidar registry de skills em único index.json](./docs/adr/archive/ADR-001.md) ✅
- [ADR-002: Padrão de Skill Ultra-High Quality Grade](./docs/adr/archive/ADR-002.md) ✅
- [ADR-003: Retrospectiva da Implementação Ultra-High Quality Grade](./docs/adr/archive/ADR-003.md) ✅
- [ADR-004: Implementação das Recomendações da Ultra-Auditoria v2.0.2](./docs/adr/archive/ADR-004.md) ✅
- [ADR-005: Introdução da Skill `implementation` para Execução Governada de Mudanças](./docs/adr/archive/ADR-005.md) ✅
- [ADR-006: Workflow CI para Auto-sync do Index e Deploy GitHub Pages](./docs/adr/archive/ADR-006.md) ✅
- [ADR-007: Skill para Geração de AGENTS.md Adaptativo](./docs/adr/archive/ADR-007.md) ✅
- [ADR-008: Ultra-Avaliação v2.0.3 — Correção de Débitos Estruturais](./docs/adr/archive/ADR-008.md) ✅
- [ADR-009: Resolução de Débitos da Auditoria v2.1.0](./docs/adr/archive/ADR-009.md) ✅
- [ADR-010: Branch Protection e SemVer para Tags — Emergencial](./docs/adr/archive/ADR-010.md) ✅
- [ADR-011: Documentation Reconciliation Skill](./docs/adr/archive/ADR-011.md) ✅
- [ADR-012: Dynamic HTML Pages — Rendering de Skills em GitHub Pages](./docs/adr/archive/ADR-012.md) ✅
- [ADR-013: Expansão do Build.py para Incluir ADRs e Referências](./docs/adr/archive/ADR-013.md) ✅
- [ADR-014: Fix Workflow sync-and-deploy — Sync Completo de master para gh-pages](./docs/adr/archive/ADR-014.md) ✅
- [ADR-015: Fix Caminhos Relativos Depth-Aware no Build.py](./docs/adr/archive/ADR-015.md) ✅

> 📦 ADRs implementadas são movidas para `docs/adr/archive/` como referência. Veja [docs/adr/INDEX.md](./docs/adr/INDEX.md) para o índice completo.

## Licença

MIT — ver [LICENSE](./LICENSE).