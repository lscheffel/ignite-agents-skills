# ignite-agents-skills

Registro centralizado de skills para agentes compatíveis com o padrão [Agent Skills](https://agentskills.io).

Hospedado como GitHub Pages, este repositório serve como registry remoto para múltiplos projetos que usam **Kilo**, **OpenCode** e outros agentes compatíveis.

> **Nota de compatibilidade (Kilo Code):** o mecanismo `skills.urls` do Kilo busca `{url}/index.json` e resolve cada arquivo em `{url}/{skill-name}/{file}`, onde `file` é **relativo à pasta da própria skill** (ex.: `"SKILL.md"`, não `"skills/nome/SKILL.md"`). Por isso o manifesto canônico é `skills/index.json` (paths relativos), e a URL configurada no Kilo deve apontar para a pasta `skills/`, não para `.well-known/skills/`. Uma tentativa anterior de seguir a convenção `.well-known/` usava paths completos no `files`, o que quebra a resolução do Kilo (duplicação de path) — por isso foi removida.

## Estrutura

```
.
├── LICENSE
├── skills/
│   ├── index.json              # Registry de skills (fonte única)
│   ├── adr-generator/
│   ├── agent-orchestration/
│   ├── api-design/
│   ├── architecture-review-kilo/
│   ├── data-modeling/
│   ├── ddd/
│   ├── documentation/
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
└── scripts/
    ├── validate-index.sh       # Valida index.json contra arquivos reais
    └── validate-skill.sh       # Valida qualidade Ultra-High Quality Grade
```

## Categorias

| Categoria | Skills |
|-----------|--------|
| Architecture | `architecture-review-kilo`, `ddd` |
| Documentation | `documentation`, `adr-generator` |
| Governance | `governance`, `repo-bootstrap` |
| Planning | `planning`, `writing-plans` |
| Implementation | `implementation` |
| Quality | `testing`, `architecture-review-kilo` |
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
4. Registre no `skills/index.json` — **paths relativos à pasta da skill**:

```json
{
  "name": "nova-skill",
  "files": [
    "SKILL.md",
    "templates/example.md"
  ]
}
```

5. Rode `scripts/validate-index.sh` localmente para confirmar que os paths resolvem
6. Rode `bash scripts/validate-skill.sh skills/nova-skill` para validar qualidade
7. Commit e push

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
- **Templates** — 63 templates disponíveis em `skills/*/templates/`
- **Examples** — 15 exemplos em `skills/*/examples/`

## Status da Implementação

**v2.0.3 — Skills Ultra-High Quality Grade**

| Métrica | Status |
|---------|--------|
| Skills total | 21 ✅ |
| Skills refatoradas | 21/21 ✅ |
| Templates criados | 63 ✅ |
| Examples criados | 15 ✅ |
| Validação automática | ✅ |
| CI pipeline | ✅ (`validate-skill.sh` + `validate-index.sh`) |
| GitHub Pages | ✅ |
| SDLC completo | ✅ |

## Decisões Arquiteturais

Decisões arquiteturais significativas são documentadas em [docs/adr/](./docs/adr/):

- [ADR-001: Consolidar registry de skills em único index.json](./docs/adr/ADR-001.md)
- [ADR-002: Padrão de Skill Ultra-High Quality Grade](./docs/adr/ADR-002.md)
- [ADR-003: Retrospectiva da Implementação](./docs/adr/ADR-003.md)
- [ADR-004: Implementação das Recomendações da Ultra-Auditoria](./docs/adr/ADR-004.md)
- [ADR-005: Introdução da Skill implementation](./docs/adr/ADR-005.md)

## Licença

MIT — ver [LICENSE](./LICENSE).
