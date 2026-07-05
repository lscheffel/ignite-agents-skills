# Especificação de Logging

## Visão Geral
Documento de referência para logging estruturado no projeto.

## Formato
Todos os logs devem ser emitidos em formato JSON.

## Campos Obrigatórios

| Campo | Tipo | Descrição | Exemplo |
|-------|------|-----------|---------|
| `timestamp` | ISO 8601 | Momento do evento | `2025-01-15T10:30:00Z` |
| `level` | string | Nível do log | `info`, `error`, `warn`, `debug` |
| `message` | string | Mensagem descritiva | `User created successfully` |
| `service` | string | Nome do serviço | `user-service` |

## Campos de Contexto

| Campo | Tipo | Descrição | Exemplo |
|-------|------|-----------|---------|
| `traceId` | string | ID do trace distribuído | `abc123def456` |
| `userId` | string | ID do usuário (quando aplicável) | `user_123` |
| `environment` | string | Ambiente de execução | `production`, `staging` |
| `requestId` | string | ID da requisição | `req_789` |

## Níveis de Log

### ERROR
- **Uso:** Falhas que precisam de ação imediata
- **Exemplos:** Falha de conexão, timeout, erro de validação crítica
- **Ação:** Investigar imediatamente

### WARN
- **Uso:** Anormalidades sem falha
- **Exemplos:** Retry, fallback, depreciação
- **Ação:** Monitorar, pode precisar de ação futura

### INFO
- **Uso:** Eventos significativos do negócio
- **Exemplos:** Criação de usuário, pagamento processado
- **Ação:** Auditoria e rastreabilidade

### DEBUG
- **Uso:** Detalhes para desenvolvimento
- **Exemplos:** Query SQL, payloads, variáveis
- **Ação:** Apenas em ambiente de dev/staging

## Sanitização de Dados

### Dados que NUNCA devem ser logados:
- Senhas ou tokens de autenticação
- Dados pessoais (CPF, RG, email completo)
- Números de cartão de crédito
- Chaves de API

### Regras de Sanitização:
```typescript
function sanitize(data: Record<string, any>): Record<string, any> {
  const sensitiveFields = ['password', 'token', 'secret', 'cpf', 'creditCard'];
  const sanitized = { ...data };
  
  for (const field of sensitiveFields) {
    if (sanitized[field]) {
      sanitized[field] = '***';
    }
  }
  
  return sanitized;
}
```

## Exemplos

### Log de Request
```json
{
  "timestamp": "2025-01-15T10:30:00Z",
  "level": "info",
  "message": "Request processed",
  "service": "api-gateway",
  "traceId": "abc123def456",
  "method": "POST",
  "path": "/api/users",
  "statusCode": 201,
  "duration": 45
}
```

### Log de Erro
```json
{
  "timestamp": "2025-01-15T10:30:00Z",
  "level": "error",
  "message": "Database connection failed",
  "service": "user-service",
  "traceId": "abc123def456",
  "error": "ECONNREFUSED",
  "host": "postgres-primary",
  "retryCount": 3
}
```

## Configuração por Ambiente

| Ambiente | Nível | Retenção | Destino |
|----------|-------|----------|---------|
| Development | debug | 7 dias | Console |
| Staging | info | 30 dias | ELK Stack |
| Production | info | 90 dias | ELK + S3 |

## Checklist de Implementação
- [ ] Logger centralizado configurado
- [ ] Formato JSON definido
- [ ] Campos obrigatórios implementados
- [ ] Sanitização de dados sensíveis
- [ ] Níveis de log configurados por ambiente
- [ ] Retenção de logs documentada
