# Exemplo: ADR para Escolha de Database

## Contexto
Precisávamos escolher entre PostgreSQL, MongoDB e DynamoDB para novo serviço.

## Decisão
Escolhemos PostgreSQL por:
- Equipe já tem experiência
- Suporte a JSONB para flexibilidade
- Replicação síncrona para HA

## Alternativas
- **MongoDB**: Schema flexível, mas operação mais cara
- **DynamoDB**: Serverless, mas vendor lock-in

## Resultado
```
# ADR-003: Database Choice
## Status
Aceito

## Contexto
Novo serviço de pedidos precisa de database.

## Decisão
PostgreSQL com replicação síncrona.

## Consequências
### Positivas
- Equipe produtiva desde início
- Consultas flexíveis com JSONB

### Negativas
- Operacional mais complexo que DynamoDB
```