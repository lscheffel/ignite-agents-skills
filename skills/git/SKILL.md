---
name: git
description: Padrões e workflows para Git. Cobre Conventional Commits, branching strategies, merge vs rebase, resolução de conflitos e boas práticas. Use quando fazer commits, criar branches, resolver conflitos ou ensinar Git.
---

# Git

Padrões e workflows para versionamento com Git.

## Quando Usar

- Criação de commits
- Branching e merging
- Resolução de conflitos
- Ensino de Git para equipes

## Conventional Commits

Formato: `<tipo>(<escopo>): <descrição>`

### Tipos
- `feat`: nova funcionalidade
- `fix`: correção de bug
- `docs`: documentação
- `style`: formatação, sem mudança de lógica
- `refactor`: refatoração de código
- `perf`: melhoria de performance
- `test`: adição/modificação de testes
- `chore`: mudanças de build, dependências

### Exemplos
```
feat(auth): add JWT refresh token
fix(api): handle null response in user endpoint
docs(readme): update installation instructions
refactor(domain): extract OrderCalculator from Order
```

## Branching

### Feature Branches
```
git checkout -b feature/add-user-avatar
```

### Commits Atômicos
- Um conceito por commit
- Mensagem clara e descritiva
- Commits pequenos e frequentes

## Merge vs Rebase

### Merge
- Preserva histórico completo
- Seguro para branches compartilhados
- Cria merge commit

### Rebase
- Histórico linear limpo
- Apenas para branches locais/privados
- Nunca rebase branches compartilhados

## Resolução de Conflitos

1. Identifique arquivos conflitantes
2. Edite manualmente marcadores `<<<<<<<`, `=======`, `>>>>>>>`
3. Teste após resolução
4. Complete com `git add` e `git rebase --continue` ou `git merge --continue`
