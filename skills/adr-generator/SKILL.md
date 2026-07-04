---
name: adr-generator
description: Cria Architecture Decision Records (ADRs) para documentar decisões arquiteturais importantes. Gera templates padronizados com contexto, decisão, consequências e status. Use quando o usuário mencionar ADR, decisão arquitetural, ou precisar documentar trade-offs técnicos.
---

# ADR Generator

Gera Architecture Decision Records (ADRs) seguindo o formato MADR ou similar.

## Quando Usar

- Decisão arquitetural significativa precisa ser documentada
- Usuário solicita criação de ADR
- Registro de trade-offs técnicos
- Decisões que afetam múltiplos módulos ou equipes

## Estrutura do ADR

Use o template disponível em `templates/adr.md` como base.

Campos obrigatórios:

```markdown
# ADR-XXX: [Título da Decisão]

## Status
Proposto | Aceito | Rejeitado | Suspenso | Substituído

## Contexto
Descreva o problema, motivação e restrições.

## Decisão
Descreva a solução escolhida de forma clara e objetiva.

## Alternativas Consideradas
- Alternativa A: descrição, prós e contras
- Alternativa B: descrição, prós e contras

## Consequências
### Positivas
- Consequência 1
- Consequência 2

### Negativas
- Custo 1
- Custo 2

## Referências
- Link para discussão
- ADRs relacionados
```

## Boas Práticas

- Numeração sequencial: ADR-001, ADR-002, etc.
- Um ADR por decisão significativa
- Nunca modifique ADRs aceitos (crie um novo ADR para substituir)
- Seja honesto sobre trade-offs
