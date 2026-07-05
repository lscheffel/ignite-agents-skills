# Exemplo: Testes de um OrderService

## Cenário
OrderService com regras de negócio complexas.

## Order Entity

```typescript
class Order {
  private items: OrderItem[] = [];
  private status: OrderStatus = OrderStatus.Draft;
  
  addItem(item: OrderItem): void {
    if (this.status !== OrderStatus.Draft) {
      throw new DomainError("Cannot modify completed order");
    }
    this.items.push(item);
  }
  
  getTotal(): number {
    return this.items.reduce((sum, item) => sum + item.price, 0);
  }
}
```

## Testes Unitários

```typescript
describe('Order', () => {
  describe('addItem', () => {
    it('should add item to draft order', () => {
      const order = new Order();
      const item = { id: 1, price: 100 };
      order.addItem(item);
      expect(order.getTotal()).toBe(100);
    });
    
    it('should throw when order is completed', () => {
      const order = new Order();
      order.status = OrderStatus.Completed;
      expect(() => order.addItem({ id: 1, price: 100 }))
        .toThrow(DomainError);
    });
  });
});
```

## Testes de Integração

```typescript
describe('OrderRepository Integration', () => {
  it('should persist order with items', async () => {
    const order = new Order();
    order.addItem({ id: 1, price: 100 });
    
    await repository.save(order);
    const loaded = await repository.findById(order.id);
    
    expect(loaded.items).toHaveLength(1);
    expect(loaded.getTotal()).toBe(100);
  });
});
```

## Resultado
- 100% coverage do Order
- Testes isolados e rápidos
- Documentação viva do comportamento