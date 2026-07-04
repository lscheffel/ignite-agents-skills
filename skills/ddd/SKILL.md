---
name: ddd
description: Guia para modelagem de domínio com Domain-Driven Design (DDD). Define diretrizes para Entidades, Value Objects, Agregados, Repositórios, Domain Events, Serviços de Domínio e Contextos Delimitados. Use quando modelar domínios ricos, refatorar entidades anêmicas ou estruturar contextos delimitados.
---

# Domain-Driven Design (DDD)

Guia para modelagem de domínio orientada a negócios.

## Quando Usar

- Modelagem de domínio rico
- Refatoração de entidades anêmicas
- Estruturação de Contextos Delimitados (Bounded Contexts)
- Definição de contratos de domínio
- Eventos de domínio e integração entre contextos

## Conceitos Fundamentais

### Entidade
Objeto com identidade própria, ciclos de vida e persistência.
- Possui ID único
- Imutabilidade de identidade
- Encapsula comportamento, não apenas dados

```typescript
class Order {
  constructor(
    private id: OrderId,
    private items: OrderItem[],
    private status: OrderStatus
  ) {}
  
  addItem(item: OrderItem): void {
    if (this.status !== OrderStatus.Draft) {
      throw new DomainError("Cannot modify completed order");
    }
    this.items.push(item);
  }
}
```

### Value Object
Objeto imutável definido por seus atributos, sem identidade própria.
- Comparação por valor, não referência
- Imutável
- Validação no construtor

```typescript
class Money {
  constructor(
    private amount: Decimal,
    private currency: CurrencyCode
  ) {
    if (amount < 0) throw new DomainError("Amount cannot be negative");
  }
}
```

### Agregado
Cluster de entidades e value objects com boundary e root.
- Aggregate Root é a única porta de entrada
- Regras de consistência dentro do agregado
- Referências externas apenas por ID

### Repositório
Abstração de coleção para acesso a agregados.
- Interface no domínio
- Implementação na infraestrutura
- Métodos: add, remove, byId, matching

### Domain Event
Registro de algo relevante que aconteceu no domínio.
- Nome no passado: OrderCreated, PaymentFailed
- Imutável
- Contém dados relevantes para o evento

### Serviço de Domínio
Lógica que não pertence naturalmente a uma entidade.
- Operações que envolvem múltiplos agregados
- Funções puras do domínio
- Sem estado

## Anti-patterns

- **Entidades Anêmicas**: apenas getters/setters sem comportamento
- **Anemic Domain Model**: regras de negócio em controllers/services
- **Transaction Script**: procedural em vez de orientado a objetos
