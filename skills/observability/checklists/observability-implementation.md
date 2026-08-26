# Implementation Checklist for Observability

## Prerequisites
- [ ] Define log format (JSON recommended)
- [ ] Choose observability stack (ELK/Datadog/Grafana)
- [ ] Define SLAs/SLOs for the system
- [ ] Map critical services

## Logging
- [ ] Centralized logger configured
- [ ] JSON format defined
- [ ] Mandatory fields implemented
- [ ] Sensitive data sanitized
- [ ] Log levels configured by environment
- [ ] Log retention documented
- [ ] Centralized logs (ELK/Datadog)

## Metrics
- [ ] RED metrics implemented (Rate, Errors, Duration)
- [ ] Business metrics defined
- [ ] Dashboards configured
- [ ] Metric-based alerts
- [ ] Metric retention defined

## Tracing
- [ ] OpenTelemetry configured
- [ ] Trace propagation between services
- [ ] Spans instrumented at key points
- [ ] Exporter configured (Jaeger/Zipkin)
- [ ] Sampling rate defined

## Alerts
- [ ] Alerts defined with severity
- [ ] Runbooks attached to each alert
- [ ] Escalation configured
- [ ] Notifications tested
- [ ] Quarterly alert review

## Testing
- [ ] Instrumentation testing
- [ ] Metric mocks configured
- [ ] Alert testing
- [ ] Tracing testing

## Documentation
- [ ] Logging specification documented
- [ ] Metrics and SLAs documented
- [ ] Alert rules documented
- [ ] Runbooks documented
- [ ] Incident playbook