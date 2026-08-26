# Example: ADR for Database Choice

## Context
We needed to choose between PostgreSQL, MongoDB, and DynamoDB for the new service.

## Decision
We chose PostgreSQL for:
- The team already has experience
- Support for JSONB for flexibility
- Synchronous replication for HA

## Alternatives
- **MongoDB**: Flexible schema, but more expensive operation
- **DynamoDB**: Serverless, but vendor lock-in

## Result
```markdown
# ADR-003: Database Choice
## Status
Accepted

## Context
The new order service requires a database.

## Decision
PostgreSQL with synchronous replication.

## Consequences
### Positive
- The team is productive from the start
- Flexible queries with JSONB

### Negative
- More operationally complex than DynamoDB
```