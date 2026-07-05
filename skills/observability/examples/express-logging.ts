import express from 'express';
import pino from 'pino';

const app = express();
const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  formatters: {
    level: (label) => ({ level: label }),
  },
});

// Middleware de logging
app.use((req, res, next) => {
  const traceId = req.headers['x-trace-id'] || generateTraceId();
  const start = Date.now();

  res.on('finish', () => {
    const duration = Date.now() - start;
    logger.info({
      traceId,
      method: req.method,
      path: req.path,
      statusCode: res.statusCode,
      duration,
    });
  });

  req.traceId = traceId;
  next();
});

// Rota de exemplo
app.get('/api/users/:id', async (req, res) => {
  const { id } = req.params;
  
  logger.debug({ traceId: req.traceId, userId: id }, 'Fetching user');
  
  try {
    const user = await userService.findById(id);
    logger.info({ traceId: req.traceId, userId: id }, 'User fetched');
    res.json(user);
  } catch (error) {
    logger.error({ traceId: req.traceId, userId: id, error: error.message }, 'Failed to fetch user');
    res.status(500).json({ error: 'Internal server error' });
  }
});

function generateTraceId(): string {
  return Math.random().toString(36).substring(2, 15);
}

app.listen(3000, () => {
  logger.info('Server started on port 3000');
});
