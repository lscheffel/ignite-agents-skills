# Threat Model Template

Simplified threat model based on STRIDE.

## System Information

- **System Name:** {{system_name}}
- **Version:** {{version}}
- **Date:** {{date}}
- **Reviewer:** {{reviewer}}

## Endpoints/Exposed Components

| # | Endpoint/Component | Description | Sensitive Data |
|---|---------------------|-----------|-----------------|
| 1 | {{endpoint_1}} | {{description_1}} | {{sensitive_1}} |
| 2 | {{endpoint_2}} | {{description_2}} | {{sensitive_2}} |

## STRIDE Analysis

For each endpoint, evaluate:

### Spoofing (Falsification)
- **Question:** Is authentication adequate?
- **Findings:** {{findings_spoofing}}
- **Risk:** 🔴 / 🟡 / 🟢

### Tampering (Adulteration)
- **Question:** Are data integrity protections in place?
- **Findings:** {{findings_tampering}}
- **Risk:** 🔴 / 🟡 / 🟢

### Repudiation (Denial)
- **Question:** Is an audit trail present?
- **Findings:** {{findings_repudiation}}
- **Risk:** 🔴 / 🟡 / 🟢

### Information Disclosure (Leakage)
- **Question:** Are sensitive data exposed?
- **Findings:** {{findings_disclosure}}
- **Risk:** 🔴 / 🟡 / 🟢

### Denial of Service (Unavailability)
- **Question:** Are rate limiting and abuse protection in place?
- **Findings:** {{findings_dos}}
- **Risk:** 🔴 / 🟡 / 🟢

### Elevation of Privilege (Privilege Escalation)
- **Question:** Is access control adequate?
- **Findings:** {{findings_elevation}}
- **Risk:** 🔴 / 🟡 / 🟢

## Risk Summary

| Severity | Quantity | Actions |
|------------|------------|-------|
| 🔴 Critical | {{critical_count}} | Fix before merge |
| 🟡 Medium | {{medium_count}} | Fix in current sprint |
| 🟢 Low | {{low_count}} | Document and plan |

---

*Threat model template for ignite-agents-skills.*