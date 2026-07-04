---
name: testing
description: Guia para escrita de testes automatizados de qualidade. Define padrões para testes unitários, de integração, E2E e contratuais. Inclui pirâmide de testes, naming conventions e boas práticas. Use quando escrever testes, revisar cobertura ou definir estratégia de testes.
---

# Testing

Guia para escrita de testes automatizados robustos.

## Quando Usar

- Escrita de testes automatizados
- Revisão de cobertura de testes
- Definição de estratégia de testes
- Padronização de testes entre projetos

## Pirâmide de Testes

```
        /\
       /  \      E2E (poucos)
      /____\
     /      \    Integração (médio)
    /________\
   /          \  Unitários (muitos)
  /____________\
```

### Testes Unitários
- Rápidos (< 100ms)
- Sem dependências externas
- Um cenário por teste
- Isolados (mocks quando necessário)

### Testes de Integração
- Validam comunicação entre módulos
- Usam dependências reais quando possível
- Validam contratos

### Testes E2E
- Simulam usuário real
- Ambientes controlados
- Poucos, focados em fluxos críticos

## Naming Convention

```typescript
describe('Order', () => {
  describe('addItem', () => {
    it('should add item to draft order', () => {});
    it('should throw when order is completed', () => {});
    it('should recalculate total', () => {});
  });
});
```

Padrão: `should [expected behavior] when [condition]`

## Boas Práticas

- AAA: Arrange, Act, Assert
- Um conceito por teste
- Evite lógica em testes
- Testes devem ser legíveis como documentação
- Teste edge cases e error paths
