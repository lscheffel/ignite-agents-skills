// Example: Strangler Fig Pattern - Gradual Migration

// ❌ BEFORE - monolithic with everything together
class LegacyPaymentService {
  processPayment(order: Order) {
    // old payment logic
    const gateway = new LegacyGateway();
    return gateway.charge(order.total, order.creditCard);
  }
}

// ✅ AFTER - Strangler Fig with feature flag

// 1. Create interface
interface PaymentProcessor {
  process(order: Order): Promise<PaymentResult>;
}

// 2. Implement new version
class StripePaymentProcessor implements PaymentProcessor {
  async process(order: Order): Promise<PaymentResult> {
    const stripe = new Stripe(process.env.STRIPE_KEY);
    const result = await stripe.charges.create({
      amount: order.total * 100,
      currency: 'usd',
      source: order.creditCard,
    });
    return { success: true, transactionId: result.id };
  }
}

// 3. Keep legacy as fallback
class LegacyPaymentProcessor implements PaymentProcessor {
  async process(order: Order): Promise<PaymentResult> {
    const gateway = new LegacyGateway();
    const result = gateway.charge(order.total, order.creditCard);
    return { success: result.ok, transactionId: result.id };
  }
}

// 4. Use feature flag to toggle
class PaymentService {
  private processor: PaymentProcessor;

  constructor() {
    if (featureFlags.isEnabled('stripe-payment')) {
      this.processor = new StripePaymentProcessor();
    } else {
      this.processor = new LegacyPaymentProcessor();
    }
  }

  async processPayment(order: Order): Promise<PaymentResult> {
    return this.processor.process(order);
  }
}

// 5. When migration is complete, remove legacy
// - Remove LegacyPaymentProcessor
// - Remove feature flag
// - Simplify PaymentService