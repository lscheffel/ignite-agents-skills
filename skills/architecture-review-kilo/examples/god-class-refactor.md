# Exemplo: Review de Arquitetura

## Problema
UserService com 500 linhas, múltiplas responsabilidades.

## Análise
```
# God Class detectado
- UserService tem: createUser, validateUser, sendEmail, calculateDiscount, generateReport
- SRP violado em múltiplos pontos
```

## Solução
Quebra em:
- UserService (criar usuário)
- UserValidator (validação)
- EmailService (notificação)
- PricingService (cálculo)

## Resultado
- 4 classes com responsabilidade única
- Testes mais focados
- Manutenção simplificada