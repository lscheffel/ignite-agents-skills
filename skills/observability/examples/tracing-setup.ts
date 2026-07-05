import { NodeTracerProvider } from '@opentelemetry/sdk-trace-node';
import { JaegerExporter } from '@opentelemetry/exporter-jaeger';
import { Resource } from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions';
import { BatchSpanProcessor } from '@opentelemetry/sdk-trace-base';
import { trace, SpanStatusCode, SpanKind } from '@opentelemetry/api';

// Configurar provider
const provider = new NodeTracerProvider({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: 'user-service',
    [SemanticResourceAttributes.SERVICE_VERSION]: '1.0.0',
  }),
});

// Configurar exportador Jaeger
const exporter = new JaegerExporter({
  serviceName: 'user-service',
  host: 'jaeger-collector',
  port: 6832,
});

provider.addSpanProcessor(new BatchSpanProcessor(exporter));
provider.register();

// Obter tracer
const tracer = trace.getTracer('user-service');

// Exemplo de uso
async function createUser(userData) {
  const span = tracer.startSpan('create-user', {
    kind: SpanKind.SERVER,
    attributes: {
      'user.email': userData.email,
    },
  });

  try {
    // Validar dados
    span.addEvent('validating-user-data');
    validateUserData(userData);

    // Salvar no banco
    span.addEvent('saving-to-database');
    const user = await database.save(userData);

    // Enviar email de boas-vindas
    span.addEvent('sending-welcome-email');
    await emailService.sendWelcome(user.email);

    span.setStatus({ code: SpanStatusCode.OK });
    return user;
  } catch (error) {
    span.setStatus({
      code: SpanStatusCode.ERROR,
      message: error.message,
    });
    span.recordException(error);
    throw error;
  } finally {
    span.end();
  }
}

// Middleware para propagar trace context
export function tracingMiddleware(req, res, next) {
  const traceId = req.headers['x-trace-id'];
  const spanId = req.headers['x-span-id'];

  if (traceId) {
    req.traceContext = { traceId, spanId };
  }

  next();
}
