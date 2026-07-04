# ignite-agents-skills

Registro centralizado de skills para agentes compatíveis com o padrão [Agent Skills](https://agentskills.io).

Hospedado como GitHub Pages, este repositório serve como registry remoto para múltiplos projetos que usam **Kilo**, **OpenCode** e outros agentes compatíveis.

## Estrutura

```
.
├── .well-known/
│   └── skills/
│       └── index.json        # Registry de skills
└── skills/
    ├── adr-generator/
    ├── architecture-review/
    ├── ddd/
    ├── documentation/
    ├── git/
    ├── governance/
    ├── planning/
    ├── prompt-engineering/
    ├── release/
    ├── repo-bootstrap/
    ├── testing/
    ├── vibe-coding/
    └── writing-plans/
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

## Publicação (GitHub Pages)

1. Habilite GitHub Pages em **Settings → Pages**
2. Source: **Deploy from a branch**
3. Branch: `main` (ou `master`)
4. Após deploy, o registry estará disponível em:

```
https://<usuario>.github.io/ignite-agents-skills/.well-known/skills/
```

## Configuração no Kilo

Adicione a URL do registry no seu `kilo.json` ou via TUI:

```json
{
  "skillRegistryUrls": [
    "https://<usuario>.github.io/ignite-agents-skills/.well-known/skills/"
  ]
}
```

O Kilo consultará o `index.json`, baixará apenas os arquivos das skills solicitadas e injetará no contexto do agente.

## Como Adicionar uma Nova Skill

1. Crie o diretório: `skills/nova-skill/`
2. Adicione o `SKILL.md` com frontmatter `name` e `description`
3. Adicione arquivos auxiliares se necessário
4. Registre no `index.json`:

```json
{
  "name": "nova-skill",
  "files": [
    "skills/nova-skill/SKILL.md",
    "skills/nova-skill/templates/example.md"
  ]
}
```

5. Commit e push

## Padrão de Skill

Cada `SKILL.md` deve conter:

```yaml
---
name: nome-da-skill
description: Descrição curta para o agente decidir quando usar.
---
```

## Licença

MIT
