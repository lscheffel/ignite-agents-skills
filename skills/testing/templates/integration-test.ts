# Integration Test Template

```typescript
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { setupTestDatabase, teardownTestDatabase } from '../test-utils';
import { UserService } from '../src/services/user-service';
import { UserRepository } from '../src/repositories/user-repository';

describe('UserService Integration', () => {
  let userService: UserService;
  let userRepository: UserRepository;
  
  beforeAll(async () => {
    await setupTestDatabase();
    userRepository = new UserRepository(testDb);
    userService = new UserService(userRepository);
  });
  
  afterAll(async () => {
    await teardownTestDatabase();
  });
  
  describe('createUser', () => {
    it('should persist user when valid data provided', async () => {
      // Arrange
      const userData = {
        name: 'John Doe',
        email: 'john@example.com'
      };
      
      // Act
      const user = await userService.createUser(userData);
      
      // Assert
      expect(user.id).toBeDefined();
      expect(user.email).toBe(userData.email);
      
      // Verify persistence
      const persisted = await userRepository.findById(user.id);
      expect(persisted).not.toBeNull();
    });
    
    it('should rollback transaction when database fails', async () => {
      // Arrange
      const userData = { email: 'invalid-email' };
      
      // Act & Assert
      await expect(userService.createUser(userData))
        .rejects.toThrow(ValidationError);
    });
  });
});
```

## Setup

1. Configure banco de dados de teste (SQLite, Docker, ou mock)
2. Use `beforeAll` para setup
3. Use `afterAll` para teardown
4. Não compartilhe estado entre testes