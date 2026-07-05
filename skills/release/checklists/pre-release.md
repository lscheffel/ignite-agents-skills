# Pre-Release Checklist

Execute antes de iniciar qualquer release.

## Versionamento
- [ ] Versão semântica incrementada corretamente (MAJOR.MINOR.PATCH)
- [ ] `index.json` reflete a nova versão
- [ ] `version` no frontmatter de todas as skills atualizada (se aplicável)

## CHANGELOG
- [ ] Entrada `[Unreleased]` movida para nova versão
- [ ] Data da release atualizada
- [ ] Todas as mudanças documentadas (Added, Changed, Fixed, Removed)
- [ ] Formato Keep a Changelog mantido

## Qualidade
- [ ] `validate-index.sh` passa: 0 erros
- [ ] `validate-skill.sh` passa para todas as skills: 0 erros
- [ ] Nenhum `related_skills` apontando para skill inexistente
- [ ] README.md atualizado com nova contagem de skills

## Git
- [ ] Branch limpa (sem uncommitted changes)
- [ ] Todos os commits seguem Conventional Commits
- [ ] Merge em master via PR (se aplicável)
- [ ] Tag criada: `v{MAJOR}.{MINOR}.{PATCH}`

## Deploy
- [ ] GitHub Pages build disparado
- [ ] Site atualizado com novas skills

---

*Checklist de pré-release para ignite-agents-skills.*
