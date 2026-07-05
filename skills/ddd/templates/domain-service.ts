// Domain Service Template
// Stateless logic that doesn't belong to an entity

export class CurrencyConverter {
  // Stateless - no instance variables
  convert(amount: Money, toCurrency: string): Money {
    const rate = this.getExchangeRate(amount.currency, toCurrency);
    return new Money(amount.amount * rate, toCurrency);
  }
  
  private getExchangeRate(from: string, to: string): number {
    // Logic that involves multiple aggregates or external data
    // This doesn't belong to Money because Money is immutable
    // and this involves external exchange rates
  }
}

export class OrderPricingService {
  calculateTotal(items: OrderItem[], coupon?: Coupon): Money {
    const subtotal = items.reduce(
      (sum, item) => sum.add(item.price), 
      new Money(0, "USD")
    );
    
    if (coupon) {
      return this.applyDiscount(subtotal, coupon);
    }
    
    return subtotal;
  }
  
  private applyDiscount(total: Money, coupon: Coupon): Money {
    // Complex pricing logic involving multiple concepts
  }
}