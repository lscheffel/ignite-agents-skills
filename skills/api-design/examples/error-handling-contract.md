# Exemplo: Contrato de Erros — API de Pagamentos

## Contexto

API de processamento de pagamentos com alta criticidade. Erros devem ser claros, acionáveis e seguros (sem vazar dados sensíveis).

## Definição de Categorias de Erro

### 1. Erros de Validação (4xx)

```json
{
  "type": "https://pay.example.com/errors/invalid-request",
  "title": "Requisição inválida",
  "status": 400,
  "detail": "O campo 'amount' deve ser um número positivo",
  "instance": "/payments",
  "request_id": "req_abc123",
  "timestamp": "2026-07-05T18:00:00Z",
  "errors": [
    {
      "field": "amount",
      "code": "INVALID_VALUE",
      "message": "deve ser um número positivo",
      "rejected_value": -100
    }
  ]
}
```

### 2. Erros de Autenticação (401/403)

```json
{
  "type": "https://pay.example.com/errors/unauthorized",
  "title": "Não autorizado",
  "status": 401,
  "detail": "Token de acesso expirado ou inválido",
  "instance": "/payments",
  "request_id": "req_def456",
  "timestamp": "2026-07-05T18:00:00Z"
}
```

**Regra de segurança:** Nunca incluir detalhes sobre por que a autenticação falhou (token inválido vs expirado vs inexistente).

### 3. Erros de Negócio (422)

```json
{
  "type": "https://pay.example.com/errors/insufficient-funds",
  "title": "Saldo insuficiente",
  "status": 422,
  "detail": "O saldo disponível (R$ 50.00) é menor que o valor solicitado (R$ 100.00)",
  "instance": "/payments",
  "request_id": "req_ghi789",
  "timestamp": "2026-07-05T18:00:00Z",
  "metadata": {
    "available_balance": 50.00,
    "requested_amount": 100.00,
    "currency": "BRL"
  }
}
```

### 4. Erros de Limite (429)

```json
{
  "type": "https://pay.example.com/errors/rate-limited",
  "title": "Limite de requisições atingido",
  "status": 429,
  "detail": "Limite de 100 requisições/minuto atingido. Tente novamente em 30 segundos.",
  "instance": "/payments",
  "request_id": "req_jkl012",
  "timestamp": "2026-07-05T18:00:00Z",
  "retry_after": 30
}
```

### 5. Erros de Servidor (5xx)

```json
{
  "type": "https://pay.example.com/errors/gateway-error",
  "title": "Erro no gateway de pagamento",
  "status": 502,
  "detail": "O gateway de pagamento retornou uma resposta inesperada",
  "instance": "/payments",
  "request_id": "req_mno345",
  "timestamp": "2026-07-05T18:00:00Z"
}
```

**Regra de segurança:** Nunca expor stack traces, IDs internos ou detalhes de infraestrutura em erros 5xx.

## Regras Gerais

1. **Consistência:** Todos os erros seguem RFC 7807
2. **Segurança:** Nunca vazar dados sensíveis (tokens, senhas, IDs internos)
3. **Accionabilidade:** O `detail` deve explicar o que fazer para corrigir
4. **Rastreabilidade:** `request_id` e `timestamp` são obrigatórios
5. **Idioma:** Mensagens em português (para APIs brasileiras) ou inglês (para APIs internacionais)
6. **Log:** Erros 4xx logam em WARN, 5xx em ERROR
7. **Alerta:** Erros 5xx disparam alerta se taxa > 1% em 5 minutos
