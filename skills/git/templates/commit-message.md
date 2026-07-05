# Commit Message Template

Formato: `<tipo>(<escopo>): <descrição>`

## Tipos

- `feat`: nova funcionalidade
- `fix`: correção de bug
- `docs`: documentação
- `style`: formatação, sem mudança de lógica
- `refactor`: refatoração de código
- `perf`: melhoria de performance
- `test`: adição/modificação de testes
- `chore`: mudanças de build, dependências

## Exemplos

```
feat(auth): add JWT refresh token
fix(api): handle null response in user endpoint
docs(readme): update installation instructions
refactor(domain): extract OrderCalculator from Order
```

## Escopo

- Nome curto do módulo afetado
- Use kebab-case: `user-service`, `api-gateway`
- Se afeta múltiplos módulos, use escopo genérico: `core`, `infra`

## Descrição

- Máximo 50 caracteres
- Imperativo: "add" não "added" ou "adds"
- Sem ponto final
- Em português ou inglês (consistência com o projeto)