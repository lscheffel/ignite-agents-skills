# Exemplo: Sessão de Vibe Coding

## Briefing
```
Quero API de produtos com:
- CRUD completo
- Validação de preço
- Testes
```

## Interações
1. IA gera estrutura básica
2. IA implementa CRUD
3. IA adiciona validação
4. IA cria testes

## Resultado
```typescript
// src/products/product-service.ts
export class ProductService {
  async create(data: CreateProductDTO) {
    if (data.price < 0) throw new Error("Invalid price");
    return this.repo.create(data);
  }
}
```

## Validação
- Testes passam ✅
- Lint passa ✅
- Build funciona ✅