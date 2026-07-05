// Value Object Template
// Immutable, defined by attributes

export abstract class ValueObject<T> {
  abstract equals(other: T): boolean;
  
  // Override in subclass
  // equals must compare by value, not reference
}

export class Money extends ValueObject<Money> {
  constructor(
    private readonly _amount: number,
    private readonly _currency: string
  ) {
    super();
    this.validate();
  }
  
  private validate(): void {
    if (this._amount < 0) {
      throw new DomainError("Amount cannot be negative");
    }
    if (!this._currency) {
      throw new DomainError("Currency is required");
    }
  }
  
  get amount(): number {
    return this._amount;
  }
  
  get currency(): string {
    return this._currency;
  }
  
  equals(other: Money): boolean {
    return this._amount === other._amount && 
           this._currency === other._currency;
  }
  
  // Always return new instance
  add(other: Money): Money {
    if (this._currency !== other._currency) {
      throw new DomainError("Cannot add different currencies");
    }
    return new Money(this._amount + other._amount, this._currency);
  }
  
  multiply(factor: number): Money {
    return new Money(this._amount * factor, this._currency);
  }
}