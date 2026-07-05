# Branch Naming Convention

Formato: `{tipo}/{nome-curto}`

## Tipos

| Tipo | Prefixo | Uso | Exemplo |
|------|---------|-----|---------|
| Feature | `feature/` | Nova funcionalidade | `feature/user-authentication` |
| Bug fix | `fix/` | Correção de bug | `fix/login-validation-error` |
| Hotfix | `hotfix/` | Correção urgente em produção | `hotfix/security-patch` |
| Release | `release/` | Preparação de release | `release/v2.1.0` |
| Refactor | `refactor/` | Refatoração sem mudança de comportamento | `refactor/order-service-cleanup` |
| Docs | `docs/` | Documentação | `docs/api-endpoints-update` |
| Test | `test/` | Testes | `test/integration-scenarios` |
| Chore | `chore/` | Manutenção geral | `chore/update-dependencies` |

## Regras

1. Use kebab-case (não snake_case ou camelCase)
2. Nome curto mas descritivo (máximo 50 caracteres)
3. Evite caracteres especiais: `/ \ # $ @`
4. Não use espaços

## Exemplos Válidos

```
feature/payment-integration
fix/user-id-null-pointer
hotfix/critical-security-patch
release/v1.2.0
refactor/cleanup-user-service
```

## Exemplos Inválidos

```
# ERRADO - muito longo
feature/implement-user-authentication-with-jwt-and-refresh-tokens

# ERRADO - caracteres especiais
feature/fix#123

# ERRADO - espaços
feature/user auth
```