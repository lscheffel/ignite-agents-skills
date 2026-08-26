# Agent Role Card

Multi-Agent Orchestrator Agent Role Card.

## Agent Information

| Field | Value |
|-------|-------|
| **Name** | `{agent_name}` |
| **Role** | `{role: orchestrator, specialist, reviewer, formatter}` |
| **Model** | `{model: lightweight, standard, advanced}` |
| **Responsibility** | `{responsibility}` |

## I/O Contract

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

## Validation

- [ ] Valid input before execution
- [ ] Valid output after execution
- [ ] Errors handled according to fallback

## Fallback

| Scenario | Action |
|---------|------|
| Invalid input | `{fallback_action}` |
| Timeout | `{fallback_action}` |
| Invalid output | `{fallback_action}` |
| Unexpected error | `{fallback_action}` |

## Dependencies

- **Depends on**: `{upstream_agents}`
- **Feeds**: `{downstream_agents}`
- **Parallel with**: `{parallel_agents}`

## Metrics

| Metric | Target |
|---------|--------|
| Success rate | `{success_rate}` |
| Average latency | `{latency}` |
| Estimated cost | `{cost}` |