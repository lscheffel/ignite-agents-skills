# Regras de Alerta

## Visão Geral
Documento de referência para regras de alerta com severidade e runbooks.

## Severidade

| Severidade | Descrição | Tempo de Resposta | Notificação |
|------------|-----------|-------------------|-------------|
| **Critical** | Sistema indisponível ou dados corrompidos | 5 minutos | PagerDuty + Slack |
| **Warning** | Degradção de performance ou risco iminente | 30 minutos | Slack |
| **Info** | Evento significativo sem impacto | Próximo business day | Email |

## Regras de Alerta

### Critical

#### HighErrorRate
```yaml
- alert: HighErrorRate
  expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.05
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "Taxa de erro > 5%"
    description: "Taxa de erro de {{ $value | humanizePercentage }} nos últimos 5 minutos"
    runbook_url: "https://wiki/runbooks/high-error-rate"
    steps: |
      1. Verificar logs de erro no Kibana
      2. Identificar endpoint com maior taxa de erro
      3. Verificar dependências externas
      4. Escalar se necessário
```

#### ServiceDown
```yaml
- alert: ServiceDown
  expr: up{job="api-gateway"} == 0
  for: 1m
  labels:
    severity: critical
  annotations:
    summary: "Serviço indisponível"
    description: "Serviço {{ $labels.instance }} está down há mais de 1 minuto"
    runbook_url: "https://wiki/runbooks/service-down"
    steps: |
      1. Verificar se o processo está rodando
      2. Verificar recursos do sistema (CPU, memória, disco)
      3. Verificar logs de startup
      4. Reiniciar serviço se necessário
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
    summary: "Latência p99 > 1s"
    description: "Latência p99 de {{ $value }}s nos últimos 5 minutos"
    runbook_url: "https://wiki/runbooks/high-latency"
    steps: |
      1. Verificar dashboards de performance
      2. Identificar queries lentas
      3. Verificar conexões com banco de dados
      4. Considerar escalar horizontalmente
```

#### HighMemoryUsage
```yaml
- alert: HighMemoryUsage
  expr: process_resident_memory_bytes / 1024 / 1024 > 1024
  for: 10m
  labels:
    severity: warning
  annotations:
    summary: "Uso de memória > 1GB"
    description: "Serviço {{ $labels.instance }} usando {{ $value }}MB de memória"
    runbook_url: "https://wiki/runbooks/high-memory"
    steps: |
      1. Verificar se há memory leak
      2. Analisar heap dumps
      3. Verificar configurações de GC
      4. Considerar aumentar memória ou escalar
```

### Info

#### DeployCompleted
```yaml
- alert: DeployCompleted
  expr: changes(deploy_timestamp[5m]) > 0
  labels:
    severity: info
  annotations:
    summary: "Deploy realizado"
    description: "Versão {{ $labels.version }} implantada em {{ $labels.environment }}"
```

## Runbooks

### Runbook: HighErrorRate
1. **Investigar**
   - Acesse Kibana e filtre por erros 5xx
   - Identifique o endpoint com maior taxa de erro
   - Verifique se há padrão (horário, usuário, região)

2. **Diagnosticar**
   - Verifique logs do serviço afetado
   - Analise traces para identificar onde o erro ocorre
   - Verifique dependências externas (DB, cache, APIs)

3. **Resolver**
   - Se erro de dependência: verificar status do serviço externo
   - Se erro de código: hotfix ou rollback
   - Se erro de infra: escalar ou reiniciar

4. **Documentar**
   - Registre incidente no post-mortem
   - Atualize runbook se necessário
   - Crie task para correção definitiva

### Runbook: ServiceDown
1. **Verificar Status**
   ```bash
   # Verificar se processo está rodando
   ps aux | grep <service-name>
   
   # Verificar portas
   netstat -tlnp | grep <port>
   ```

2. **Verificar Logs**
   ```bash
   # Últimas linhas de log
   tail -100 /var/log/<service>/error.log
   ```

3. **Reiniciar**
   ```bash
   # Reiniciar serviço
   systemctl restart <service-name>
   ```

4. **Monitorar**
   - Acompanhe métricas após reinício
   - Verifique se erros persistem

## Escalonamento

| Nível | Tempo | Responsável | Contato |
|-------|-------|-------------|---------|
| L1 | 0-5 min | On-call | PagerDuty |
| L2 | 5-15 min | Tech Lead | Slack #incidents |
| L3 | 15-30 min | Engineering Manager | Phone |
| L4 | 30+ min | VP Engineering | Executive |

## Checklist de Alertas
- [ ] Alertas definidos com severidade
- [ ] Runbooks anexados a cada alerta
- [ ] Escalonamento configurado
- [ ] Notificações testadas
- [ ] Alertas review quarterly
- [ ] Freqüência de alertas monitorada
