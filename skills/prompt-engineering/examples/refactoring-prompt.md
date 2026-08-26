# Example: Refactoring Prompt

## Context
You are a senior developer specializing in Clean Code.

## Task
Refactor this class to follow the Single Responsibility Principle.

## Original Code
```typescript
class UserService {
  createUser() {}
  validateEmail() {}
  sendWelcomeEmail() {}
  calculateDiscount() {}
}
```

## Output Format
```typescript
// Separate classes
class UserService {}
class EmailValidator {}
class EmailService {}
class DiscountCalculator {}
```

## Result
4 classes with single responsibility, more focused tests.