# Pre-Refactoring Tests

## Overview

| Field | Value |
|-------|-------|
| Module | {module-path} |
| Responsible | {your-name} |
| Date | {date} |
| Status | In Progress/Completed |

## Context

### Code to be Refactored
- **Files:** {file-paths}
- **Function/Class:** {function-or-class-name}
- **Identified Code Smell:** {code-smell}

### Why Test First?
- Code without test coverage
- Refactoring without a safety net is risky
- Tests document current behavior

## Testing Plan

### Characterization Tests

Tests that document current behavior without validating if it's "correct":

```typescript
// Characterization - document current behavior
describe('{module-name} - Characterization', () => {
  it('should return X when input is Y', () => {
    // Arrange
    const input = { /* actual usage data */ };
    
    // Act
    const result = functionUnderTest(input);
    
    // Assert - document current behavior
    expect(result).toBe({expected-output});
  });
});
```

### Unit Tests

Tests that validate specific logic:

```typescript
describe('{module-name} - Unit', () => {
  it('should calculate total correctly', () => {
    // Arrange
    const items = [{ price: 10, qty: 2 }, { price: 5, qty: 3 }];
    
    // Act
    const total = calculateTotal(items);
    
    // Assert
    expect(total).toBe(35);
  });
});
```

### Integration Tests

Tests that validate integration points:

```typescript
describe('{module-name} - Integration', () => {
  it('should persist order to database', async () => {
    // Arrange
    const order = { items: [{ id: 1, qty: 2 }] };
    
    // Act
    await orderService.create(order);
    
    // Assert
    const saved = await db.orders.findOne({ where: { id: order.id } });
    expect(saved).toBeDefined();
    expect(saved.items).toHaveLength(1);
  });
});
```

## Execution Checklist

### Before Creating Tests
- [ ] Source code identified and accessible
- [ ] Dependencies mapped
- [ ] Primary use cases documented

### Creating Tests
- [ ] Characterization tests created for current behavior
- [ ] Unit tests created for main logic
- [ ] Integration tests created for integration points
- [ ] All tests pass

### Validation
- [ ] Tests cover happy path
- [ ] Tests cover error paths
- [ ] Tests cover known edge cases
- [ ] No test depends on external state
- [ ] Tests are independent of each other

### Commit
- [ ] Tests committed BEFORE refactoring
- [ ] Commit message clear: "test: add characterization tests for {module}"
- [ ] CI passing with new tests

## Metrics

| Metric | Before | After | Target |
|---------|-------|--------|------|
| Line coverage | {before}% | {after}% | >= 80% |
| Branch coverage | {before}% | {after}% | >= 70% |
| Number of tests | {before} | {after} | - |

## References

- `testing` - for testing standards
- [Characterization Tests](https://martinfowler.com/bliki/CharacterizationTest.html)