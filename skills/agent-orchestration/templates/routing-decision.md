# Routing Decision

Decisão de roteamento de modelo para agentes.

## Contexto

| Campo | Valor |
|-------|-------|
| **Tarefa** | `{task_description}` |
| **Complexidade** | `{low, medium, high}` |
| **Requisitos** | `{requirements}` |

## Matriz de Roteamento

### Por Complexidade

| Complexidade | Modelo | Custo | Latência | Uso |
|-------------|--------|-------|----------|-----|
| **Baixa** | `{lightweight_model}` | $ | Baixa | Extração, formatação, classificação simples |
| **Média** | `{standard_model}` | $$ | Média | Análise, síntese, geração estruturada |
| **Alta** | `{advanced_model}` | $$$ | Alta | Raciocínio complexo, código, arquitetura |

### Por Papel

| Papel | Modelo Recomendado | Justificativa |
|-------|-------------------|---------------|
| **Orchestrator** | `{model}` | Precisa de raciocínio ampla |
| **Specialist** | `{model}` | Precisa de expertise focada |
| **Reviewer** | `{model}` | Precisa de atenção a detalhes |
| **Formatter** | `{model}` | Tarefa simples, modelo leve |

## Decisão

```yaml
selected_model: "{model_name}"
reason: "{justification}"
cost_estimate: "{estimated_cost}"
latency_estimate: "{estimated_latency}"
fallback_model: "{fallback_model_name}"
fallback_reason: "{when_to_use_fallback}"
```

## Cenários

### Cenário 1: Extração de Dados
- **Complexidade**: Baixa
- **Modelo**: `{lightweight_model}`
- **Justificativa**: Tarefa simples, não precisa de raciocínio complexo

### Cenário 2: Análise de Código
- **Complexidade**: Média
- **Modelo**: `{standard_model}`
- **Justificativa**: Precisa entender contexto, mas não é trivial

### Cenário 3: Geração de Arquitetura
- **Complexidade**: Alta
- **Modelo**: `{advanced_model}`
- **Justificativa**: Raciocínio complexo, múltiplas considerações

## Checklist

- [ ] Complexidade avaliada
- [ ] Modelo selecionado por complexidade
- [ ] Custo estimado documentado
- [ ] Fallback definido
- [ ] Latência aceitável
- [ ] Throughput adequado
