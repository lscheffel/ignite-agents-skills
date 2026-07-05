# Exemplo: Workflow Completo de Feature

## Cenário
Adicionar autenticação JWT a uma API existente.

## Passo a Passo

### 1. Criar branch
```bash
git checkout -b feature/jwt-authentication
```

### 2. Desenvolver
```bash
# Após cada mudança significativa
git add src/auth/jwt.ts
git commit -m "feat(auth): implement JWT token generation"

git add src/middleware/auth.ts
git commit -m "feat(auth): add authentication middleware"

git add tests/auth.test.ts
git commit -m "test(auth): add JWT authentication tests"
```

### 3. Atualizar com main
```bash
git fetch origin
git rebase origin/main
# Resolve conflitos se houver
```

### 4. Push e criar PR
```bash
git push origin feature/jwt-authentication
gh pr create --title "feat(auth): JWT authentication" --body "Implementa..."
```

## Resultado
- 3 commits atônicos
- Histórico limpo (rebase)
- PR com descrição clara
- Testes incluídos