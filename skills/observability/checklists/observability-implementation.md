# Checklist de Implementação de Observabilidade

## Pré-requisitos
- [ ] Definir formato de log (JSON recomendado)
- [ ] Escolher stack de observabilidade (ELK/Datadog/Grafana)
- [ ] Definir SLAs/SLOs do sistema
- [ ] Mapear serviços críticos

## Logging
- [ ] Logger centralizado configurado
- [ ] Formato JSON definido
- [ ] Campos obrigatórios implementados
- [ ] Sanitização de dados sensíveis
- [ ] Níveis de log configurados por ambiente
- [ ] Retenção de logs documentada
- [ ] Logs centralizados (ELK/Datadog)

## Métricas
- [ ] Métricas RED implementadas (Rate, Errors, Duration)
- [ ] Métricas de negócio definidas
- [ ] Dashboards configurados
- [ ] Alertas baseados em métricas
- [ ] Retenção de métricas definida

## Tracing
- [ ] OpenTelemetry configurado
- [ ] Trace propagation entre serviços
- [ ] Spans instrumentados nos pontos principais
- [ ] Exportador configurado (Jaeger/Zipkin)
- [ ] Sampling rate definido

## Alertas
- [ ] Alertas definidos com severidade
- [ ] Runbooks anexados a cada alerta
- [ ] Escalonamento configurado
- [ ] Notificações testadas
- [ ] Alertas review quarterly

## Testes
- [ ] Testes de instrumentação
- [ ] Mocks de métricas configurados
- [ ] Testes de alertas
- [ ] Testes de tracing

## Documentação
- [ ] Especificação de logging documentada
- [ ] Métricas e SLAs documentados
- [ ] Regras de alerta documentadas
- [ ] Runbooks documentados
- [ ] Playbook de incidentes
