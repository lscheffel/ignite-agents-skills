# Handoff Protocol

Protocolo de handoff entre agentes de IA.

## Identificação

| Campo | Valor |
|-------|-------|
| **Handoff ID** | `{handoff_id}` |
| **Agente Origem** | `{source_agent}` |
| **Agente Destino** | `{target_agent}` |
| **Descrição** | `{description}` |

## Contrato de Dados

### Schema de Input

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

### Schema de Output

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

## Regras de Validação

1. **Input validation**: `{validation_rules}`
2. **Output validation**: `{validation_rules}`
3. **Timeout**: `{timeout_seconds}s`
4. **Max retries**: `{max_retries}`

## Processo de Handoff

```
1. Agente origem completa tarefa
2. Valida output com schema
3. Serializa dados no formato contratado
4. Envia para agente destino
5. Agente destino valida input
6. Se válido: processa tarefa
7. Se inválido: aciona fallback
```

## Fallback

| Erro | Ação |
|------|------|
| Schema inválido | Rejeitar e retornar erro estruturado |
| Timeout | Retry com backoff exponencial |
| Agente indisponível | Usar agente alternativo |
| Dados corrompidos | Solicitar reprocessamento |

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

- [ ] Schema de input definido
- [ ] Schema de output definido
- [ ] Validação implementada
- [ ] Fallback documentado
- [ ] Logging configurado
- [ ] Teste de handoff executado
