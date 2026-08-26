# Handoff Protocol

Handoff protocol between AI agents.

## Identification

| Field | Value |
|-------|-------|
| **Handoff ID** | `{handoff_id}` |
| **Source Agent** | `{source_agent}` |
| **Target Agent** | `{target_agent}` |
| **Description** | `{description}` |

## Data Contract

### Input Schema

```json
{
  "type": "object",
  "required": ["{required_field_1}", "{required_field_2}"],
  "properties": {
    "{field_1}": {
      "type": "{type}",
      "description": "{description}"
    },
    "{field_2}": {
      "type": "{type}",
      "description": "{description}"
    }
  }
}
```

### Output Schema

```json
{
  "type": "object",
  "required": ["{required_field_1}"],
  "properties": {
    "{field_1}": {
      "type": "{type}",
      "description": "{description}"
    }
  }
}
```

## Validation Rules

1. **Input validation**: `{validation_rules}`
2. **Output validation**: `{validation_rules}`
3. **Timeout**: `{timeout_seconds}s`
4. **Max retries**: `{max_retries}`

## Handoff Process

```
1. Source agent completes task
2. Validates output with schema
3. Serializes data in contracted format
4. Sends to target agent
5. Target agent validates input
6. If valid: processes task
7. If invalid: triggers fallback
```

## Fallback

| Error | Action |
|------|------|
| Invalid schema | Reject and return structured error |
| Timeout | Retry with exponential backoff |
| Agent unavailable | Use alternative agent |
| Corrupted data | Request reprocessing |

## Logging

```json
{
  "timestamp": "{ISO8601}",
  "handoff_id": "{handoff_id}",
  "source": "{source_agent}",
  "target": "{target_agent}",
  "status": "{success|failure}",
  "latency_ms": "{latency}",
  "error": "{error_message | null}"
}
```

## Checklist

- [ ] Input schema defined
- [ ] Output schema defined
- [ ] Validation implemented
- [ ] Fallback documented
- [ ] Logging configured
- [ ] Handoff test executed