# Example: DDD Modeling of Order

## Before
```typescript
// Anemic Order
class Order {
  id: string;
  items: any[];
  total: number;
  status: string;
  // only getters/setters
}
```

## After
```typescript
// Rich Order
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

## Result
- Invariants ensured
- Encapsulated behavior
- Simpler tests