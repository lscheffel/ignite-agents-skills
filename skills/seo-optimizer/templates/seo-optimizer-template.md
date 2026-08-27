# Production Implementation Template: seo-optimizer

## Domain & Purpose
- **Target Domain:** Technical SEO, Core Web Vitals & Structured Data
- **Core Focus:** Core Web Vitals (LCP, INP, CLS), JSON-LD Schema.org, OpenGraph, sitemap.xml, robots.txt
- **Artifact Type:** Production-ready actionable specification and implementation template.

---

## 1. Technical SEO Audit Matrix
Define the contextual boundaries, primary objectives, and strict non-functional constraints for this execution.

```yaml
context:
  module_name: "<target-component>"
  version: "1.0.0"
  execution_mode: "strict"
  invariants:
    - "Zero regressions against existing baseline test suite"
    - "Strict type compliance and schema validation"
    - "Complete decoupling from external infrastructure"
```

---

## 2. Meta Tags & OpenGraph Spec
Detailed technical specification, schema structure, or contract definitions.

```python
# Canonical typed specification template
from dataclasses import dataclass
from typing import List, Dict, Optional, Any

@dataclass(frozen=True)
class ExecutionConfig:
    component_id: str
    enabled_features: List[str]
    timeout_ms: int = 5000
    retry_limit: int = 3
    parameters: Optional[Dict[str, Any]] = None

def validate_configuration(config: ExecutionConfig) -> bool:
    """Validate configuration integrity against domain invariants."""
    if not config.component_id.strip():
        raise ValueError("component_id cannot be empty")
    if config.timeout_ms <= 0:
        raise ValueError("timeout_ms must be positive")
    return True
```

---

## 3. Schema.org JSON-LD Structured Data
Operational execution rules, transformation pipeline, and state transitions.

| Step | Action | Expected Output | Verification Mechanism |
|:---|:---|:---|:---|
| **01** | Input Validation & Schema Sanitization | Clean verified payload | Schema validator (exit code 0) |
| **02** | Core Domain Execution / Transform | Immutable state transition | Unit test assertion |
| **03** | Error Boundary & Exception Handling | Graceful fallback / retry | Failure injection test |
| **04** | Telemetry & Evidence Recording | Structured log trace | Audit ledger persistence |

---

## 4. Core Web Vitals Optimization Plan
Final verification gates that must be satisfied before declaring completion.

```bash
# Verification test execution command
$ python3 -m unittest discover -s tests -p "test_*.py"
```

- [ ] All automated tests pass with 0 failures and 0 errors.
- [ ] Code strictly follows Clean Architecture and SOLID principles.
- [ ] No temporary placeholders, TODO comments, or hardcoded mock values remain.
