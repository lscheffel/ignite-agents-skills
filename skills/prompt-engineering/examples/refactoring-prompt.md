# Exemplo: Prompt para Refatoração

## Contexto
Você é um desenvolvedor sênior especializado em Clean Code.

## Tarefa
Refatore esta classe para seguir Single Responsibility Principle.

## Código Original
```typescript
class UserService {
  createUser() {}
  validateEmail() {}
  sendWelcomeEmail() {}
  calculateDiscount() {}
}
```

## Formato de Saída
```typescript
// Classes separadas
class UserService {}
class EmailValidator {}
class EmailService {}
class DiscountCalculator {}
```

## Resultado
4 classes com responsabilidade única, testes mais focados.