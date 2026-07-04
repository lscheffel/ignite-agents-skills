---
name: vibe-coding
description: Modalidade de desenvolvimento onde o desenvolvedor guia o agente de IA com intenção e direção, não comandos detalhados. Foca em resultado, velocidade e fluxo contínuo. Use quando o usuário mencionar vibe coding, pair programming com IA, ou desenvolvimento assistido por IA.
---

# Vibe Coding

Desenvolvimento orientado por intenção com agentes de IA.

## Quando Usar

- Desenvolvimento rápido de protótipos
- Exploração de soluções
- Pair programming com IA
- Geração de scaffolding inicial

## Princípios

1. **Intenção sobre Implementação**: Descreva o que quer, não como fazer
2. **Feedback Rápido**: Iterações curtas, validação constante
3. **Confie, mas Verifique**: Revise o código gerado
4. **Contexto é Tudo**: Quanto mais contexto, melhor o resultado

## Padrão de Interação

### 1. Briefing
```
Quero uma API de pedidos com:
- CRUD de produtos
- Carrinho de compras
- Checkout com cálculo de frete
```

### 2. Refinamento
```
Agora adicione validação de estoque no checkout
```

### 3. Validação
```
Rode os testes e mostre o resultado
```

### 4. Ajuste
```
O cálculo de frete está errado para peso > 10kg. Corrija.
```

## Quando Usar vs Quando Evitar

### Use
- Prototipação rápida
- Exploração de soluções
- Geração de boilerplate
- Refatorações guiadas

### Evite
- Código de produção sem revisão
- Sistemas críticos sem testes
- Decisões arquiteturais sem compreensão
- Segredos/credenciais em prompts
