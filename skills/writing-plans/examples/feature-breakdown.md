# Exemplo: Breakdown de Feature — Sistema de Notificações Push

## Contexto

Aplicativo mobile precisa de notificações push para:
- Alertas de segurança (login suspeito, tentativa de acesso)
- Atualizações de status de pedido
- Promocões personalizadas

## Especificação

- Firebase Cloud Messaging (FCM) para Android/iOS
- Backend: Python + FastAPI
- Fila de mensagens: Redis
- ~50k usuários ativos

## Plano de Implementação

### Fase 1: Infraestrutura (2 dias)

| Tarefa | Arquivos | Critérios de Aceitação | Complexidade |
|--------|----------|----------------------|--------------|
| 1.1 Configurar Firebase Admin SDK | `config/firebase.py`, `requirements.txt` | SDK inicializa sem erro, credenciais validadas | S |
| 1.2 Criar modelo de dispositivo | `models/device.py`, `schemas/device.py` | Device tem: user_id, token, platform, active | S |
| 1.3 Criar tabela de dispositivos | `migrations/002_devices.sql`, `alembic.ini` | Tabela existe com índices em user_id e token | S |

**Dependências:** Nenhuma
**Estimativa:** 4h

### Fase 2: Core de Notificação (3 dias)

| Tarefa | Arquivos | Critérios de Aceitação | Complexidade |
|--------|----------|----------------------|--------------|
| 2.1 Criar serviço de envio | `services/notification_sender.py` | Envia FCM, trata rate limit, retentativa | M |
| 2.2 Criar fila de mensagens | `services/notification_queue.py` | Push para Redis, retry com backoff exponencial | M |
| 2.3 Criar template de mensagem | `templates/notification.py` | 3 templates: security, order, promotion | S |
| 2.4 Criar endpoint de registro | `routes/devices.py` | POST /devices registra token, PUT atualiza | S |

**Dependências:** Fase 1 completa
**Estimativa:** 12h

### Fase 3: Tipos de Notificação (3 dias)

| Tarefa | Arquivos | Critérios de Aceitação | Complexidade |
|--------|----------|----------------------|--------------|
| 3.1 Alertas de segurança | `services/security_notifier.py` | Login suspeito gera push em <30s | M |
| 3.2 Status de pedido | `services/order_notifier.py` | Mudança de status gera push com dados do pedido | M |
| 3.3 Promoções personalizadas | `services/promo_notifier.py` | Segmentação por preferências do usuário | M |

**Dependências:** Fase 2 completa
**Estimativa:** 12h

### Fase 4: Observabilidade (1 dia)

| Tarefa | Arquivos | Critérios de Aceitação | Complexidade |
|--------|----------|----------------------|--------------|
| 4.1 Métricas de envio | `metrics/notifications.py` | Taxa de entrega, latência, erros por tipo | S |
| 4.2 Logs estruturados | `logging/notification_logger.py` | Log com user_id, tipo, status, timestamp | S |
| 4.3 Dashboard básico | `grafana/notification-dashboard.json` | Painel com taxa de entrega e erros | S |

**Dependências:** Fase 3 completa
**Estimativa:** 4h

## DAG de Dependências

```
1.1 → 1.2 → 1.3 → 2.1 → 2.2 → 2.3 → 2.4 → 3.1 → 3.2 → 3.3 → 4.1 → 4.2 → 4.3
```

## Estimativa Total

| Fase | Horas | Dias |
|------|-------|------|
| Infraestrutura | 4h | 2 |
| Core | 12h | 3 |
| Tipos | 12h | 3 |
| Observabilidade | 4h | 1 |
| **Total** | **32h** | **~9 dias** |

## Critérios de Aceite Globais

- [ ] Push entregue em <30s para alertas de segurança
- [ ] Taxa de entrega >99% para todos os tipos
- [ ] Retry automático com backoff exponencial (máx 3 tentativas)
- [ ] Métricas disponíveis no Grafana
- [ ] Testes unitários com cobertura >80%
