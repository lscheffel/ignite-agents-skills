# Blueprint: ADR-029 — Modular Multi-Asset Scaffolding & Edge Cases Baseline

## 1. Topologia de Diretórios de um Skill Bundle Canônico

```
skills/{skill-name}/
├── SKILL.md                 # SSOT da Skill com YAML Frontmatter e Instruções
├── templates/               # Artefatos e modelos reutilizáveis
│   └── {skill-name}-template.md
├── examples/                # Casos práticos e sessões de exemplo
│   └── {skill-name}-example.md
└── scripts/                 # (Opcional) Utilitários automatizados
```

## 2. Padrão da Seção de Edge Cases & Failure Modes

```markdown
## Edge Cases & Failure Modes

- **Ambiente Restrito / Read-Only:** Se o filesystem ou sandbox estiver bloqueado contra escrita, reportar o bloqueio com evidência imediata e gerar o patch em markdown diff.
- **Conflito de Especificação:** Caso encontre contradições entre a intenção do usuário e o SSOT (`AGENTS.md`), interromper e sinalizar as opções com trade-offs.
- **Timeout ou Exaustão de Contexto:** Em tarefas volumosas, decompor em sub-lotes atômicos utilizando a skill `subagent-driven-development`.
```
