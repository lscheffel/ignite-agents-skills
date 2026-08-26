# Example: Error Contract — Payment API

## Context

High-criticality payment processing API. Errors must be clear, actionable, and secure (without leaking sensitive data).

## Error Category Definitions

### 1. Validation Errors (4xx)

```json
{
  "type": "https://pay.example.com/errors/invalid-request",
  "title": "Invalid Request",
  "status": 400,
  "detail": "The 'amount' field must be a positive number",
  "instance": "/payments",
  "request_id": "req_abc123",
  "timestamp": "2026-07-05T18:00:00Z",
  "errors": [
    {
      "field": "amount",
      "code": "INVALID_VALUE",
      "message": "must be a positive number",
      "rejected_value": -100
    }
  ]
}
```

### 2. Authentication Errors (401/403)

```json
{
  "type": "https://pay.example.com/errors/unauthorized",
  "title": "Unauthorized",
  "status": 401,
  "detail": "Access token expired or invalid",
  "instance": "/payments",
  "request_id": "req_def456",
  "timestamp": "2026-07-05T18:00:00Z"
}
```

**Security Rule:** Never include details about why authentication failed (invalid vs expired vs non-existent token).

### 3. Business Errors (422)

```json
{
  "type": "https://pay.example.com/errors/insufficient-funds",
  "title": "Insufficient Funds",
  "status": 422,
  "detail": "The available balance (USD 50.00) is less than the requested amount (USD 100.00)",
  "instance": "/payments",
  "request_id": "req_ghi789",
  "timestamp": "2026-07-05T18:00:00Z",
  "metadata": {
    "available_balance": 50.00,
    "requested_amount": 100.00,
    "currency": "USD"
  }
}
```

### 4. Rate Limit Errors (429)

```json
{
  "type": "https://pay.example.com/errors/rate-limited",
  "title": "Rate Limit Exceeded",
  "status": 429,
  "detail": "Rate limit of 100 requests/minute exceeded. Try again in 30 seconds.",
  "instance": "/payments",
  "request_id": "req_jkl012",
  "timestamp": "2026-07-05T18:00:00Z",
  "retry_after": 30
}
```

### 5. Server Errors (5xx)

```json
{
  "type": "https://pay.example.com/errors/gateway-error",
  "title": "Payment Gateway Error",
  "status": 502,
  "detail": "The payment gateway returned an unexpected response",
  "instance": "/payments",
  "request_id": "req_mno345",
  "timestamp": "2026-07-05T18:00:00Z"
}
```

**Security Rule:** Never expose stack traces, internal IDs, or infrastructure details in 5xx errors.

## General Rules

1. **Consistency:** All errors follow RFC 7807
2. **Security:** Never leak sensitive data (tokens, passwords, internal IDs)
3. **Actionability:** The `detail` field must explain what to do to correct the error
4. **Traceability:** `request_id` and `timestamp` are mandatory
5. **Language:** Messages are in Portuguese (for Brazilian APIs) or English (for international APIs)
6. **Logging:** 4xx errors log at WARN, 5xx errors log at ERROR
7. **Alerting:** 5xx errors trigger an alert if the rate > 1% in 5 minutes