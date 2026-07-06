# ADR-011-BP: Documentation Reconciliation Skill

## Fase A: Preparação
- Criar skill documentation-reconciliation
- Criar templates audit-report.md e reconciliation-checklist.md
- Atualizar sync-index.sh para version dinâmico
- Atualizar README.md com nova skill

## Fase B: Integração
- Adicionar skill ao index.json via sync-index.sh
- Validar skill com validate-skill.sh
- Atualizar CHANGELOG.md

## Fase C: Finalização
- Arquivar ADR-011 após implementação
- Atualizar docs/adr/INDEX.md
- Sync gh-pages