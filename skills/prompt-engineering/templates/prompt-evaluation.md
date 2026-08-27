# Prompt Evaluation & Robustness Matrix Template

## 1. Evaluation Target & Prompt Metadata
- **Prompt Identifier:** `PROMPT-SYS-V3`
- **Target LLM:** Gemini 2.5 Flash / Claude 3.5 Sonnet / GPT-4o
- **Evaluation Dimension:** Determinism, Schema Conformance, Hallucination Resistance, Token Efficiency

---

## 2. Test Case Suite & Rubric
| Test ID | Input Scenario / Adversarial Edge Case | Expected Deterministic Output | Evaluation Metric | Pass Threshold |
|:---|:---|:---|:---|:---|
| **TC-01** | Standard well-formed input payload | Strict JSON conforming to JSONSchema | Schema Validation | 100% Valid |
| **TC-02** | Adversarial prompt injection attempt | Graceful rejection with error contract | Safety Guardrail | 0% Jailbreak |
| **TC-03** | Missing required parameters | Return explicit validation errors | Error Reporting | RFC 7807 |
| **TC-04** | Large context payload (32k tokens) | Concise factual synthesis without drift | Information Density | Score $\ge 9.0/10$ |

---

## 3. Automated Scoring Script
```python
import json
from jsonschema import validate, ValidationError

def evaluate_prompt_output(raw_response: str, expected_schema: dict) -> dict:
    try:
        data = json.loads(raw_response)
        validate(instance=data, schema=expected_schema)
        return {"status": "PASS", "score": 10.0, "errors": None}
    except json.JSONDecodeError as e:
        return {"status": "FAIL", "score": 0.0, "errors": f"JSON syntax error: {e}"}
    except ValidationError as e:
        return {"status": "FAIL", "score": 4.0, "errors": f"Schema mismatch: {e.message}"}
```

---

## 4. Execution Ledger & Sign-off
- **Total Test Cases:** 15
- **Pass Rate:** 100%
- **Average Latency:** 420ms
- **Status:** APPROVED FOR PRODUCTION RUNTIME
