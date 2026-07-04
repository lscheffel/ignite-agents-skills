---
name: governance
description: Define diretrizes de governança para repositórios e equipes. Cobre processos de revisão, aprovação, branching strategy, versionamento semântico e gestão de issues/PRs. Use quando definir processos de equipe, implementar governance-as-code ou padronizar workflows de desenvolvimento.
---

# Governance

Define diretrizes de governança para projetos e equipes.

## Quando Usar

- Definição de processos de equipe
- Implementação de governance-as-code
- Padronização de branching strategy
- Definição de processos de revisão e aprovação

## Branching Strategy

### GitFlow (recomendado para releases agendadas)
- `main`: código em produção
- `develop`: branch de integração
- `feature/*`: novas features
- `release/*`: preparação de release
- `hotfix/*`: correções urgentes

### Trunk-Based (recomendado para CI/CD contínuo)
- `main`: trunk sempre deployável
- `feature/*`: branches curtas (< 1 dia)
- `release/*`: branches de release opcionais

## Versionamento Semântico

Formato: `MAJOR.MINOR.PATCH`

- **MAJOR**: mudanças incompatíveis
- **MINOR`: funcionalidades novas, compatível
- **PATCH**: correções, compatível

## Processo de PR

1. Feature branch a partir de `main` ou `develop`
2. Commits pequenos e focados
3. Abre PR com descrição completa
4. Pelo menos 1 aprovação (2 para mudanças arquiteturais)
5. CI verde (lint, testes, build)
6. Merge com squash ou rebase

## Políticas

### CODEOWNERS
```
# Padrão
* @org/core-team

# Áreas específicas
/docs/ @org/docs-team
/src/infrastructure/ @org/infra-team
```

### Branch Protection
- Require PR reviews
- Dismiss stale reviews
- Require status checks
- No force pushes to main
- Require linear history
