# Unit Test Template

```typescript
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { {{ClassName}} } from '../src/{{path}}';

describe('{{ClassName}}', () => {
  describe('{{methodName}}', () => {
    // Arrange
    const input = {};
    
    // Act
    const result = {{ClassName}}.{{methodName}}(input);
    
    // Assert
    it('should {{expectedBehavior}} when {{condition}}', () => {
      expect(result).toBeDefined();
      expect(result).toEqual(expected);
    });
    
    it('should throw {{ErrorType}} when {{invalidCondition}}', () => {
      expect(() => {{ClassName}}.{{methodName}}(invalidInput))
        .toThrow({{ErrorType}});
    });
  });
});
```

## Placeholders

- `{{ClassName}}` — Nome da classe a ser testada
- `{{path}}` — Caminho relativo do arquivo fonte
- `{{methodName}}` — Nome do método a ser testado
- `{{expectedBehavior}}` — Comportamento esperado
- `{{condition}}` — Condição de teste
- `{{ErrorType}}` — Tipo de erro esperado
- `{{invalidCondition}}` — Condição inválida

## Naming Convention

Padrão: `should [expected behavior] when [condition]`

Exemplos:
- `should return user when id exists`
- `should throw NotFoundError when user not found`
- `should calculate total when items provided`