import { Counter, Histogram, Gauge, register } from 'prom-client';

// Métricas RED
export const httpRequestTotal = new Counter({
  name: 'http_requests_total',
  help: 'Total de requisições HTTP',
  labelNames: ['method', 'route', 'status_code'],
});

export const httpRequestDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duração de requisições HTTP',
  labelNames: ['method', 'route'],
  buckets: [0.1, 0.5, 1, 2, 5],
});

export const httpRequestErrors = new Counter({
  name: 'http_request_errors_total',
  help: 'Total de erros HTTP',
  labelNames: ['method', 'route', 'error_type'],
});

// Métricas de negócio
export const ordersCreated = new Counter({
  name: 'orders_created_total',
  help: 'Total de pedidos criados',
  labelNames: ['status'],
});

export const activeUsers = new Gauge({
  name: 'active_users',
  help: 'Número de usuários ativos',
});

// Middleware para coletar métricas
export function metricsMiddleware(req, res, next) {
  const end = httpRequestDuration.startTimer({
    method: req.method,
    route: req.route?.path || req.path,
  });

  res.on('finish', () => {
    end();
    httpRequestTotal.inc({
      method: req.method,
      route: req.route?.path || req.path,
      status_code: res.statusCode,
    });

    if (res.statusCode >= 500) {
      httpRequestErrors.inc({
        method: req.method,
        route: req.route?.path || req.path,
        error_type: 'server_error',
      });
    }
  });

  next();
}

// Endpoint para expor métricas
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});
