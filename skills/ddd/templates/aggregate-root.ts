// Aggregate Root Template
// Single entry point, enforces invariants

export class Order {
  private items: OrderItem[] = [];
  private status: OrderStatus = OrderStatus.Draft;
  private domainEvents: DomainEvent[] = [];
  
  // Private constructor - use factory method
  private constructor(
    private readonly id: OrderId,
    private readonly userId: UserId
  ) {}
  
  // Factory method
  static create(userId: UserId): Order {
    const order = new Order(OrderId.generate(), userId);
    order.addDomainEvent(new OrderCreated(order.id, userId));
    return order;
  }
  
  // Invariant enforcement
  addItem(item: OrderItem): void {
    if (this.status !== OrderStatus.Draft) {
      throw new DomainError("Cannot modify non-draft order");
    }
    this.items.push(item);
    this.recalculateTotal();
  }
  
  removeItem(itemId: ItemId): void {
    if (this.status !== OrderStatus.Draft) {
      throw new DomainError("Cannot modify non-draft order");
    }
    this.items = this.items.filter(i => i.id !== itemId);
    this.recalculateTotal();
  }
  
  confirm(): void {
    if (this.items.length === 0) {
      throw new DomainError("Cannot confirm empty order");
    }
    this.status = OrderStatus.Pending;
    this.addDomainEvent(new OrderConfirmed(this.id));
  }
  
  // Only expose what's needed
  get total(): Money {
    return this.calculateTotal();
  }
  
  get orderId(): OrderId {
    return this.id;
  }
  
  // Domain events
  private addDomainEvent(event: DomainEvent): void {
    this.domainEvents.push(event);
  }
  
  pullDomainEvents(): DomainEvent[] {
    const events = [...this.domainEvents];
    this.domainEvents = [];
    return events;
  }
  
  // Private methods for invariants
  private recalculateTotal(): void {
    // ...
  }
  
  private calculateTotal(): Money {
    // ...
  }
}