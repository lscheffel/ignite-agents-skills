// Domain Event Template
// Immutable, past tense, contains relevant data

export abstract class DomainEvent {
  public readonly occurredAt: Date = new Date();
  
  abstract get eventName(): string;
}

export class OrderCreated extends DomainEvent {
  get eventName(): string {
    return "OrderCreated";
  }
  
  constructor(
    public readonly orderId: OrderId,
    public readonly userId: UserId,
    public readonly total: Money
  ) {
    super();
  }
}

export class OrderConfirmed extends DomainEvent {
  get eventName(): string {
    return "OrderConfirmed";
  }
  
  constructor(
    public readonly orderId: OrderId
  ) {
    super();
  }
}

// Handler (separate file)
export class SendOrderConfirmationHandler {
  constructor(private readonly emailService: EmailService) {}
  
  async handle(event: OrderConfirmed): Promise<void> {
    const order = await this.orderRepository.findById(event.orderId);
    if (order) {
      await this.emailService.sendConfirmation(order.userId);
    }
  }
}