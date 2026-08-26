# Routing Decision

Model-based routing decision for agents.

## Context

| Field | Value |
|-------|-------|
| **Task** | `{task_description}` |
| **Complexity** | `{low, medium, high}` |
| **Requirements** | `{requirements}` |

## Routing Matrix

### By Complexity

| Complexity | Model | Cost | Latency | Use |
|------------|--------|-------|----------|-----|
| **Low** | `{lightweight_model}` | $ | Low | Extraction, simple formatting, and classification |
| **Medium** | `{standard_model}` | $$ | Medium | Analysis, synthesis, and structured generation |
| **High** | `{advanced_model}` | $$$ | High | Complex reasoning, code, and architecture |

### By Role

| Role | Recommended Model | Justification |
|------|-------------------|---------------|
| **Orchestrator** | `{model}` | Needs broad reasoning |
| **Specialist** | `{model}` | Needs focused expertise |
| **Reviewer** | `{model}` | Needs attention to detail |
| **Formatter** | `{model}` | Simple task, lightweight model |

## Decision

```yaml
selected_model: "{model_name}"
reason: "{justification}"
cost_estimate: "{estimated_cost}"
latency_estimate: "{estimated_latency}"
fallback_model: "{fallback_model_name}"
fallback_reason: "{when_to_use_fallback}"
```

## Scenarios

### Scenario 1: Data Extraction
- **Complexity**: Low
- **Model**: `{lightweight_model}`
- **Justification**: Simple task, no complex reasoning needed

### Scenario 2: Code Analysis
- **Complexity**: Medium
- **Model**: `{standard_model}`
- **Justification**: Needs to understand context, but not trivial

### Scenario 3: Architecture Generation
- **Complexity**: High
- **Model**: `{advanced_model}`
- **Justification**: Complex reasoning, multiple considerations

## Checklist

- [ ] Complexity evaluated
- [ ] Model selected by complexity
- [ ] Estimated cost documented
- [ ] Fallback defined
- [ ] Acceptable latency
- [ ] Adequate throughput