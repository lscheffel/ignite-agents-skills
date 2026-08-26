# Metrics and SLAs

## Overview
Reference document for RED metrics and SLAs/SLOs of the system.

## RED Metrics

### Rate (Request Rate)
- **Metric:** Requests per second
- **Formula:** `rate(http_requests_total[5m])`
- **Dimensions:** method, route, status_code

### Errors (Error Rate)
- **Metric:** Error requests per second
- **Formula:** `rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])`
- **Dimensions:** method, route, error_type

### Duration (Latency)
- **Metric:** Response time in seconds
- **Percentiles:** p50, p95, p99
- **Histogram buckets:** 0.1s, 0.5s, 1s, 2s, 5s

## Business Metrics

| Metric | Description | Type | Example |
|---------|-------------|------|---------|
| `orders_created_total` | Total orders created | Counter | Count by period |
| `revenue_total` | Total revenue | Counter | Accumulated value |
| `active_users` | Active users | Gauge | Current value |

## SLAs/SLOs

### Availability
- **SLO:** 99.9% monthly availability
- **Calculation:** `(total - errors) / total * 100`
- **Error Budget:** 43 minutes of downtime per month

### Latency
- **SLO:** p99 < 500ms
- **Calculation:** `histogram_quantile(0.99, http_request_duration_seconds)`
- **Exception:** Upload endpoints may have higher latency

### Throughput
- **SLO:** Support 1000 RPS
- **Calculation:** `max(rate(http_requests_total[5m]))`
- **Monitoring:** Alert when > 80% capacity

## Dashboards

### System Health Dashboard
- Request rate (Rate)
- Error rate (Errors)
- Latency (Duration)
- CPU/Memory usage

### Business Dashboard
- Orders per minute
- Accumulated revenue
- Active users
- Conversion rate

## Implementation Examples

### Counter (Prometheus)
```typescript
import { Counter } from 'prom-client';

const httpRequestTotal = new Counter({
  name: 'http_requests_total',
  help: 'Total HTTP requests',
  labelNames: ['method', 'route', 'status_code'],
});

// Usage
httpRequestTotal.inc({ method: 'GET', route: '/api/users', status_code: 200 });
```

### Histogram (Prometheus)
```typescript
import { Histogram } from 'prom-client';

const httpRequestDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration',
  labelNames: ['method', 'route'],
  buckets: [0.1, 0.5, 1, 2, 5],
});

// Usage
const end = httpRequestDuration.startTimer({ method: 'GET', route: '/api/users' });
// ... process request
end();
```

### Gauge (Prometheus)
```typescript
import { Gauge } from 'prom-client';

const activeConnections = new Gauge({
  name: 'active_connections',
  help: 'Active connections',
});

// Usage
activeConnections.inc(); // New connection
activeConnections.dec(); // Closed connection
```

## Metric-Based Alerts

| Metric | Condition | Severity |
|---------|-----------|-----------|
| Error Rate | > 5% for 5min | Critical |
| Latency p99 | > 1s for 5min | Warning |
| Availability | < 99.9% | Critical |
| Throughput | > 80% capacity | Warning |

## Metric Checklist
- [ ] RED metrics implemented
- [ ] Business metrics defined
- [ ] SLAs/SLOs documented
- [ ] Dashboards configured
- [ ] Metric-based alerts
- [ ] Metric retention defined