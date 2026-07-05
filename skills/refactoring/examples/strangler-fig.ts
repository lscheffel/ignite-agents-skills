// Exemplo: Strangler Fig Pattern - Migração gradual

// ❌ ANTES - monolito com tudo junto
class LegacyPaymentService {
  processPayment(order: Order) {
    // lógica de pagamento antiga
    const gateway = new LegacyGateway();
    return gateway.charge(order.total, order.creditCard);
  }
}

// ✅ DEPOIS - Strangler Fig com feature flag

// 1. Criar interface
interface PaymentProcessor {
  process(order: Order): Promise<PaymentResult>;
}

// 2. Implementar nova versão
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

// 3. Manter legado como fallback
class LegacyPaymentProcessor implements PaymentProcessor {
  async process(order: Order): Promise<PaymentResult> {
    const gateway = new LegacyGateway();
    const result = gateway.charge(order.total, order.creditCard);
    return { success: result.ok, transactionId: result.id };
  }
}

// 4. Usar feature flag para alternar
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

// 5. Quando migration estiver completa, remover legado
// - Remover LegacyPaymentProcessor
// - Remover feature flag
// - Simplificar PaymentService
