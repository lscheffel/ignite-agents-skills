# Test Plan Template

## Coverage Goals

| Tipo | Meta | Atual |
|------|------|-------|
| Unitários | ≥80% | % |
| Integração | ≥70% | % |
| E2E | ≥60% | % |

## Test Matrix

| Funcionalidade | Tipo | Status | Prioridade |
|----------------|------|--------|------------|
| Autenticação | Unitário | ✅ | Alta |
| Autenticação | Integração | ✅ | Alta |
| Autenticação | E2E | ⬜ | Média |
| CRUD Usuários | Unitário | ✅ | Alta |
| CRUD Usuários | Integração | ⬜ | Alta |

## Test Cases

### Happy Path
- [ ] Usuário cria conta com dados válidos
- [ ] Usuário faz login com credenciais válidas
- [ ] Usuário atualiza perfil

### Edge Cases
- [ ] Email já cadastrado
- [ ] Senha muito curta
- [ ] Campo obrigatório vazio

### Error Paths
- [ ] Database connection failure
- [ ] Invalid token
- [ ] Rate limit exceeded

## Automation

```bash
# Executar todos os testes
npm test

# Executar com coverage
npm run test:coverage

# Executar E2E
npm run test:e2e
```

## Definition of Done

- [ ] Todos os testes passam
- [ ] Coverage ≥ meta definida
- [ ] Nenhum test flaky
- [ ] Documentação de testes atualizada