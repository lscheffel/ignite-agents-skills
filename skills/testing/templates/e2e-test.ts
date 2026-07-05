# E2E Test Template

```typescript
import { test, expect } from '@playwright/test';

test.describe('User Registration Flow', () => {
  test('should register user successfully', async ({ page }) => {
    // Arrange
    await page.goto('/register');
    
    // Act
    await page.fill('[data-testid="email"]', 'john@example.com');
    await page.fill('[data-testid="password"]', 'SecurePass123!');
    await page.click('[data-testid="submit"]');
    
    // Assert
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('[data-testid="welcome"]'))
      .toContainText('Welcome, john@example.com');
  });
  
  test('should show error for invalid email', async ({ page }) => {
    // Arrange
    await page.goto('/register');
    
    // Act
    await page.fill('[data-testid="email"]', 'invalid-email');
    await page.click('[data-testid="submit"]');
    
    // Assert
    await expect(page.locator('[data-testid="error"]'))
      .toContainText('Invalid email format');
  });
});
```

## Best Practices

- Use `data-testid` attributes para seletores estáveis
- Teste fluxos críticos, não todos os caminhos
- Limpe estado antes/depois do teste
- Use `test.beforeEach` para setup
- Mantenha testes independentes