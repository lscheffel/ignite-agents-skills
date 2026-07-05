# Exemplo: Modelagem DDD de Order

## Antes
```typescript
// Order anêmico
class Order {
  id: string;
  items: any[];
  total: number;
  status: string;
  // só getters/setters
}
```

## Depois
```typescript
// Order rico
class Order {
  private items: OrderItem[] = [];
  private status: OrderStatus = OrderStatus.Draft;
  
  addItem(item: OrderItem): void {
    if (this.status !== OrderStatus.Draft) {
      throw new DomainError("Cannot modify paid order");
    }
    this.items.push(item);
    this.recalculateTotal();
  }
  
  confirm(): void {
    if (this.items.length === 0) {
      throw new DomainError("Empty order");
    }
    this.status = OrderStatus.Pending;
  }
}
```

## Resultado
- Invariantes garantidas
- Comportamento encapsulado
- Testes mais simples