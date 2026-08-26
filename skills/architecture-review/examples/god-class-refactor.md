# Example: Architecture Review

## Problem
UserService with 500 lines, multiple responsibilities.

## Analysis
```
# God Class detected
- UserService has: createUser, validateUser, sendEmail, calculateDiscount, generateReport
- SRP violated at multiple points
```

## Solution
Break into:
- UserService (create user)
- UserValidator (validation)
- EmailService (notification)
- PricingService (calculation)

## Result
- 4 classes with single responsibility
- More focused tests
- Simplified maintenance