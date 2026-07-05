# Pull Request Template

## Descrição

{Resumo claro e conciso da mudança}

## Tipo de Mudança

- [ ] Bug fix (correção que não quebra a API)
- [ ] Feature (nova funcionalidade)
- [ ] Breaking change (mudança que quebra a API)
- [ ] Documentation (mudança apenas em docs)
- [ ] Refactor (melhoria sem mudança de comportamento)

## Checklist

### Code Quality
- [ ] Código segue padrões do projeto
- [ ] Não há código comentado ou debug
- [ ] Variáveis e funções têm nomes claros
- [ ] Complexidade ciclomática < 10

### Testing
- [ ] Testes unitários adicionados/atualizados
- [ ] Testes de integração adicionados (se aplicável)
- [ ] Todos os testes passam (`npm test`)
- [ ] Coverage ≥ 80% (se aplicável)

### Documentation
- [ ] README.md atualizado (se necessário)
- [ ] Comentários de código adicionados
- [ ] CHANGELOG.md atualizado (se necessário)

### Security
- [ ] Nenhuma credencial exposta
- [ ] Input validado
- [ ] Dependências verificadas (`npm audit`)

## Screenshots (se aplicável)

{Adicione screenshots da UI ou mudanças visuais}

## Related Issues

Fixes #{issue-number}
Closes #{issue-number}
Relates to #{issue-number}