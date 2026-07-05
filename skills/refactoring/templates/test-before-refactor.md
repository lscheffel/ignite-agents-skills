# Testes Antes de Refatorar

## Visão Geral

| Campo | Valor |
|-------|-------|
| Módulo | {module-path} |
| Responsável | {your-name} |
| Data | {date} |
| Status | Em andamento/Concluído |

## Contexto

### Código a ser refatorado
- **Arquivo(s):** {file-paths}
- **Função/Classe:** {function-or-class-name}
- **Code Smell identificado:** {code-smell}

### Por que testar primeiro?
- Código sem cobertura de testes
- Refatoração sem safety net é arriscada
- Testes documentam comportamento atual

## Plano de Testes

### Testes de Caracterização

Testes que documentam comportamento atual, sem validar se é "correto":

```typescript
// Caracterização - documentar comportamento existente
describe('{module-name} - Characterization', () => {
  it('should return X when input is Y', () => {
    // Arrange
    const input = { /* dados reais do caso de uso */ };
    
    // Act
    const result = functionUnderTest(input);
    
    // Assert - documentar comportamento atual
    expect(result).toBe({expected-output});
  });
});
```

### Testes de Unidade

Testes que validam lógica específica:

```typescript
describe('{module-name} - Unit', () => {
  it('should calculate total correctly', () => {
    // Arrange
    const items = [{ price: 10, qty: 2 }, { price: 5, qty: 3 }];
    
    // Act
    const total = calculateTotal(items);
    
    // Assert
    expect(total).toBe(35);
  });
});
```

### Testes de Integração

Testes que validam pontos de integração:

```typescript
describe('{module-name} - Integration', () => {
  it('should persist order to database', async () => {
    // Arrange
    const order = { items: [{ id: 1, qty: 2 }] };
    
    // Act
    await orderService.create(order);
    
    // Assert
    const saved = await db.orders.findOne({ where: { id: order.id } });
    expect(saved).toBeDefined();
    expect(saved.items).toHaveLength(1);
  });
});
```

## Checklist de Execução

### Antes de criar testes
- [ ] Código fonte identificado e acessível
- [ ] Dependências mapeadas
- [ ] Casos de uso principais documentados

### Criando testes
- [ ] Testes de caracterização criados para comportamento atual
- [ ] Testes unitários criados para lógica principal
- [ ] Testes de integração criados para pontos de integração
- [ ] Todos os testes passam

### Validação
- [ ] Testes cobrem caminho feliz
- [ ] Testes cobrem caminhos de erro
- [ ] Testes cobrem edge cases conhecidos
- [ ] Nenhum teste depende de estado externo
- [ ] Testes são independentes entre si

### Commit
- [ ] Testes commitados ANTES da refatoração
- [ ] Mensagem de commit clara: "test: add characterization tests for {module}"
- [ ] CI passando com novos testes

## Métricas

| Métrica | Antes | Depois | Meta |
|---------|-------|--------|------|
| Cobertura de linhas | {before}% | {after}% | >= 80% |
| Cobertura de分支 | {before}% | {after}% | >= 70% |
| Número de testes | {before} | {after} | - |

## Referências

- `testing` - para padrões de testes
- [Characterization Tests](https://martinfowler.com/bliki/CharacterizationTest.html)
