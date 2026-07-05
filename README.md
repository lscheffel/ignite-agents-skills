# ignite-agents-skills

Registro centralizado de skills para agentes compatíveis com o padrão [Agent Skills](https://agentskills.io).

Hospedado como GitHub Pages, este repositório serve como registry remoto para múltiplos projetos que usam **Kilo**, **OpenCode** e outros agentes compatíveis.

> **Nota de compatibilidade (Kilo Code):** o mecanismo `skills.urls` do Kilo busca `{url}/index.json` e resolve cada arquivo em `{url}/{skill-name}/{file}`, onde `file` é **relativo à pasta da própria skill** (ex.: `"SKILL.md"`, não `"skills/nome/SKILL.md"`). Por isso o manifesto canônico é `skills/index.json` (paths relativos), e a URL configurada no Kilo deve apontar para a pasta `skills/`, não para `.well-known/skills/`. Uma tentativa anterior de seguir a convenção `.well-known/` usava paths completos no `files`, o que quebra a resolução do Kilo (duplicação de path) — por isso foi removida.

## Estrutura

```
.
├── LICENSE
├── skills/
│   ├── index.json            # Registry de skills (fonte única)
│   ├── adr-generator/
│   ├── architecture-review/
│   ├── ddd/
│   ├── documentation/
│   ├── git/
│   ├── governance/
│   ├── planning/
│   ├── prompt-engineering/
│   ├── release/
│   ├── repo-bootstrap/
│   ├── skill-audit-bulletin/
│   ├── testing/
│   ├── vibe-coding/
│   └── writing-plans/
└── scripts/
    └── validate-index.sh     # Valida index.json contra arquivos reais
```

## Categorias

| Categoria | Skills |
|-----------|--------|
| Architecture | `architecture-review`, `ddd` |
| Documentation | `documentation`, `adr-generator` |
| Governance | `governance`, `repo-bootstrap` |
| Planning | `planning`, `writing-plans` |
| Quality | `testing`, `architecture-review` |
| AI | `prompt-engineering`, `vibe-coding` |
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
6. Commit e push

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
- **Templates** — 37 templates disponíveis em `skills/*/templates/`
- **Examples** — 13 exemplos em `skills/*/examples/`

## Status da Implementação

**v2.0.1 — Skills Ultra-High Quality Grade**

| Métrica | Status |
|---------|--------|
| Skills refatoradas | 15/15 ✅ |
| Templates criados | 37 ✅ |
| Examples criados | 13 ✅ |
| Validação automática | ✅ |
| GitHub Pages | ✅ |

## Decisões Arquiteturais

Decisões arquiteturais significativas são documentadas em [docs/adr/](./docs/adr/):

- [ADR-001: Consolidar registry de skills em único index.json](./docs/adr/ADR-001.md)
- [ADR-002: Padrão de Skill Ultra-High Quality Grade](./docs/adr/ADR-002.md)

## Licença

MIT — ver [LICENSE](./LICENSE).
