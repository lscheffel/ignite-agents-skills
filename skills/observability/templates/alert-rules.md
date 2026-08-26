# Alert Rules

## Overview
Reference document for alert rules with severity and runbooks.

## Severity

| Severity | Description | Response Time | Notification |
|----------|-------------|----------------|---------------|
| **Critical** | System unavailable or data corrupted | 5 minutes | PagerDuty + Slack |
| **Warning** | Performance degradation or imminent risk | 30 minutes | Slack |
| **Info** | Significant event with no impact | Next business day | Email |

## Alert Rules

### Critical

#### HighErrorRate
```yaml
- alert: HighErrorRate
  expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.05
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "Error rate > 5%"
    description: "Error rate of {{ $value | humanizePercentage }} in the last 5 minutes"
    runbook_url: "https://wiki/runbooks/high-error-rate"
    steps: |
      1. Check error logs in Kibana
      2. Identify the endpoint with the highest error rate
      3. Check external dependencies
      4. Scale if necessary
```

#### ServiceDown
```yaml
- alert: ServiceDown
  expr: up{job="api-gateway"} == 0
  for: 1m
  labels:
    severity: critical
  annotations:
    summary: "Service unavailable"
    description: "Service {{ $labels.instance }} has been down for more than 1 minute"
    runbook_url: "https://wiki/runbooks/service-down"
    steps: |
      1. Check if the process is running
      2. Check system resources (CPU, memory, disk)
      3. Check startup logs
      4. Restart the service if necessary
```

### Warning

#### HighLatency
```yaml
- alert: HighLatency
  expr: histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 1
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "p99 latency > 1s"
    description: "p99 latency of {{ $value }}s in the last 5 minutes"
    runbook_url: "https://wiki/runbooks/high-latency"
    steps: |
      1. Check performance dashboards
      2. Identify slow queries
      3. Check database connections
      4. Consider horizontal scaling
```

#### HighMemoryUsage
```yaml
- alert: HighMemoryUsage
  expr: process_resident_memory_bytes / 1024 / 1024 > 1024
  for: 10m
  labels:
    severity: warning
  annotations:
    summary: "Memory usage > 1GB"
    description: "Service {{ $labels.instance }} using {{ $value }}MB of memory"
    runbook_url: "https://wiki/runbooks/high-memory"
    steps: |
      1. Check for memory leaks
      2. Analyze heap dumps
      3. Check GC configurations
      4. Consider increasing memory or scaling
```

### Info

#### DeployCompleted
```yaml
- alert: DeployCompleted
  expr: changes(deploy_timestamp[5m]) > 0
  labels:
    severity: info
  annotations:
    summary: "Deploy completed"
    description: "Version {{ $labels.version }} deployed in {{ $labels.environment }}"
```

## Runbooks

### Runbook: HighErrorRate
1. **Investigate**
   - Access Kibana and filter by 5xx errors
   - Identify the endpoint with the highest error rate
   - Check for patterns (time, user, region)

2. **Diagnose**
   - Check logs of the affected service
   - Analyze traces to identify where the error occurs
   - Check external dependencies (DB, cache, APIs)

3. **Resolve**
   - If error is due to dependency: check status of external service
   - If error is due to code: hotfix or rollback
   - If error is due to infrastructure: scale or restart

4. **Document**
   - Record incident in post-mortem
   - Update runbook if necessary
   - Create task for definitive correction

### Runbook: ServiceDown
1. **Check Status**
   ```bash
   # Check if process is running
   ps aux | grep <service-name>
   
   # Check ports
   netstat -tlnp | grep <port>
   ```

2. **Check Logs**
   ```bash
   # Last lines of log
   tail -100 /var/log/<service>/error.log
   ```

3. **Restart**
   ```bash
   # Restart service
   systemctl restart <service-name>
   ```

4. **Monitor**
   - Monitor metrics after restart
   - Check if errors persist

## Escalation

| Level | Time | Responsible | Contact |
|-------|------|-------------|---------|
| L1 | 0-5 min | On-call | PagerDuty |
| L2 | 5-15 min | Tech Lead | Slack #incidents |
| L3 | 15-30 min | Engineering Manager | Phone |
| L4 | 30+ min | VP Engineering | Executive |

## Alert Checklist
- [ ] Alerts defined with severity
- [ ] Runbooks attached to each alert
- [ ] Escalation configured
- [ ] Notifications tested
- [ ] Alerts reviewed quarterly
- [ ] Frequency of alerts monitored