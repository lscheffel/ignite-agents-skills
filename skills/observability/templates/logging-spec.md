# Logging Specification

## Overview
Reference document for structured logging in the project.

## Format
All logs must be emitted in JSON format.

## Required Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `timestamp` | ISO 8601 | Event timestamp | `2025-01-15T10:30:00Z` |
| `level` | string | Log level | `info`, `error`, `warn`, `debug` |
| `message` | string | Descriptive message | `User created successfully` |
| `service` | string | Service name | `user-service` |

## Context Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `traceId` | string | Distributed trace ID | `abc123def456` |
| `userId` | string | User ID (when applicable) | `user_123` |
| `environment` | string | Execution environment | `production`, `staging` |
| `requestId` | string | Request ID | `req_789` |

## Log Levels

### ERROR
- **Usage:** Critical failures requiring immediate action
- **Examples:** Connection failure, timeout, critical validation error
- **Action:** Investigate immediately

### WARN
- **Usage:** Anomalies without failure
- **Examples:** Retry, fallback, deprecation
- **Action:** Monitor, may require future action

### INFO
- **Usage:** Significant business events
- **Examples:** User creation, payment processing
- **Action:** Audit and trackability

### DEBUG
- **Usage:** Development details
- **Examples:** SQL queries, payloads, variables
- **Action:** Only in dev/staging environments

## Data Sanitization

### Data that MUST NOT be logged:
- Passwords or authentication tokens
- Personal data (CPF, RG, full email)
- Credit card numbers
- API keys

### Sanitization Rules:
```typescript
function sanitize(data: Record<string, any>): Record<string, any> {
  const sensitiveFields = ['password', 'token', 'secret', 'cpf', 'creditCard'];
  const sanitized = { ...data };
  
  for (const field of sensitiveFields) {
    if (sanitized[field]) {
      sanitized[field] = '***';
    }
  }
  
  return sanitized;
}
```

## Examples

### Request Log
```json
{
  "timestamp": "2025-01-15T10:30:00Z",
  "level": "info",
  "message": "Request processed",
  "service": "api-gateway",
  "traceId": "abc123def456",
  "method": "POST",
  "path": "/api/users",
  "statusCode": 201,
  "duration": 45
}
```

### Error Log
```json
{
  "timestamp": "2025-01-15T10:30:00Z",
  "level": "error",
  "message": "Database connection failed",
  "service": "user-service",
  "traceId": "abc123def456",
  "error": "ECONNREFUSED",
  "host": "postgres-primary",
  "retryCount": 3
}
```

## Environment Configuration

| Environment | Level | Retention | Destination |
|-------------|-------|----------|-------------|
| Development | debug | 7 days | Console |
| Staging | info | 30 days | ELK Stack |
| Production | info | 90 days | ELK + S3 |

## Implementation Checklist
- [ ] Centralized logger configured
- [ ] JSON format defined
- [ ] Required fields implemented
- [ ] Sensitive data sanitized
- [ ] Log levels configured by environment
- [ ] Log retention documented