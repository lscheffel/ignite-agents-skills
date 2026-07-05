# Métricas e SLAs

## Visão Geral
Documento de referência para métricas RED e SLAs/SLOs do sistema.

## Métricas RED

### Rate (Taxa de Requisições)
- **Métrica:** Requisições por segundo
- **Fórmula:** `rate(http_requests_total[5m])`
- **Dimensões:** method, route, status_code

### Errors (Taxa de Erros)
- **Métrica:** Requisições com erro por segundo
- **Fórmula:** `rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])`
- **Dimensões:** method, route, error_type

### Duration (Duração/Latência)
- **Métrica:** Tempo de resposta em segundos
- **Percentis:** p50, p95, p99
- **Histograma buckets:** 0.1s, 0.5s, 1s, 2s, 5s

## Métricas de Negócio

| Métrica | Descrição | Tipo | Exemplo |
|---------|-----------|------|---------|
| `orders_created_total` | Total de pedidos criados | Counter | Contagem por período |
| `revenue_total` | Receita total | Counter | Valor acumulado |
| `active_users` | Usuários ativos | Gauge | Valor atual |

## SLAs/SLOs

### Disponibilidade
- **SLO:** 99.9% disponibilidade mensal
- **Cálculo:** `(total - erros) / total * 100`
- **Error Budget:** 43 minutos de downtime por mês

### Latência
- **SLO:** p99 < 500ms
- **Cálculo:** `histogram_quantile(0.99, http_request_duration_seconds)`
- **Exceção:** Endpoints de upload podem ter latência maior

### Throughput
- **SLO:** Suportar 1000 RPS
- **Cálculo:** `max(rate(http_requests_total[5m]))`
- **Monitoramento:** Alerta quando > 80% da capacidade

## Dashboards

### Dashboard de Saúde do Sistema
- Taxa de requisições (Rate)
- Taxa de erros (Errors)
- Latência (Duration)
- Uso de CPU/Memória

### Dashboard de Negócio
- Pedidos por minuto
- Receita acumulada
- Usuários ativos
- Conversão

## Exemplos de Implementação

### Counter (Prometheus)
```typescript
import { Counter } from 'prom-client';

const httpRequestTotal = new Counter({
  name: 'http_requests_total',
  help: 'Total de requisições HTTP',
  labelNames: ['method', 'route', 'status_code'],
});

// Uso
httpRequestTotal.inc({ method: 'GET', route: '/api/users', status_code: 200 });
```

### Histogram (Prometheus)
```typescript
import { Histogram } from 'prom-client';

const httpRequestDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duração de requisições HTTP',
  labelNames: ['method', 'route'],
  buckets: [0.1, 0.5, 1, 2, 5],
});

// Uso
const end = httpRequestDuration.startTimer({ method: 'GET', route: '/api/users' });
// ... processar request
end();
```

### Gauge (Prometheus)
```typescript
import { Gauge } from 'prom-client';

const activeConnections = new Gauge({
  name: 'active_connections',
  help: 'Conexões ativas',
});

// Uso
activeConnections.inc(); // Nova conexão
activeConnections.dec(); // Conexão fechada
```

## Alertas Baseados em Métricas

| Métrica | Condição | Severidade |
|---------|----------|------------|
| Error Rate | > 5% por 5min | Critical |
| Latência p99 | > 1s por 5min | Warning |
| Disponibilidade | < 99.9% | Critical |
| Throughput | > 80% capacidade | Warning |

## Checklist de Métricas
- [ ] Métricas RED implementadas
- [ ] Métricas de negócio definidas
- [ ] SLAs/SLOs documentados
- [ ] Dashboards configurados
- [ ] Alertas baseados em métricas
- [ ] Retenção de métricas definida
