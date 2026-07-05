# Agent Role Card

Card de papel do agente para orquestração multi-agente.

## Informações do Agente

| Campo | Valor |
|-------|-------|
| **Nome** | `{agent_name}` |
| **Papel** | `{role: orchestrator, specialist, reviewer, formatter}` |
| **Modelo** | `{model: lightweight, standard, advanced}` |
| **Responsabilidade** | `{responsibility}` |

## Contrato I/O

### Input

```yaml
schema: {InputSchemaName}
fields:
  - name: {field1}
    type: {string|number|object|array}
    required: {true|false}
    description: {description}
  - name: {field2}
    type: {type}
    required: {true|false}
    description: {description}
```

### Output

```yaml
schema: {OutputSchemaName}
fields:
  - name: {field1}
    type: {type}
    required: {true|false}
    description: {description}
  - name: {field2}
    type: {type}
    required: {true|false}
    description: {description}
```

## Validação

- [ ] Input válido antes de executar
- [ ] Output válido após executar
- [ ] Erros tratados conforme fallback

## Fallback

| Cenário | Ação |
|---------|------|
| Input inválido | `{fallback_action}` |
| Timeout | `{fallback_action}` |
| Output inválido | `{fallback_action}` |
| Erro inesperado | `{fallback_action}` |

## Dependências

- **Depende de**: `{upstream_agents}`
- **Alimenta**: `{downstream_agents}`
- **Paralelo com**: `{parallel_agents}`

## Métricas

| Métrica | Target |
|---------|--------|
| Taxa de sucesso | `{success_rate}` |
| Latência média | `{latency}` |
| Custo estimado | `{cost}` |
