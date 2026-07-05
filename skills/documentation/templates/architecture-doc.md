# Architecture Documentation Template

## Visão Geral

{Descrição do sistema}

## Componentes

```
┌─────────────┐     ┌─────────────┐
│   Client    │────▶│   API       │
└─────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  Database   │
                    └─────────────┘
```

## Decisões Arquiteturais

- ADR-001: Database Choice
- ADR-002: Auth Strategy