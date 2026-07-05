# Plano de Migração de Legado

## Visão Geral

| Campo | Valor |
|-------|-------|
| Sistema Legado | {legacy-system-name} |
| Responsável | {your-name} |
| Data de Início | {start-date} |
| Data Prevista de Conclusão | {target-date} |
| Status | Planejada/Em andamento/Concluída |

## Contexto

### Por que migrar?
- {reason 1: manutenção difícil}
- {reason 2: dependências desatualizadas}
- {reason 3: performance inadequada}

### Dependências do Sistema
- {service 1}: {description}
- {service 2}: {description}
- {database}: {type and version}

## Estratégia de Migração

### Abordagem: Strangler Fig

```
Fase 1: Criar abstração
┌─────────────────────────┐
│  API Gateway / Facade   │
├─────────────┬───────────┤
│   Legado    │  Novo     │
│  (100%)     │  (0%)     │
└─────────────┴───────────┘

Fase 2: Migrar módulo a módulo
┌─────────────────────────┐
│  API Gateway / Facade   │
├─────────────┬───────────┤
│   Legado    │  Novo     │
│  (70%)      │  (30%)    │
└─────────────┴───────────┘

Fase 3: Completar migração
┌─────────────────────────┐
│  API Gateway / Facade   │
├─────────────┬───────────┤
│   Legado    │  Novo     │
│  (0%)       │  (100%)   │
└─────────────┴───────────┘
```

## Fases de Migração

### Fase 1: Preparação

**Duração estimada:** {weeks}

- [ ] Mapear todas as rotas/endpoints do legado
- [ ] Identificar dependências externas
- [ ] Criar testes de caracterização
- [ ] Configurar ambiente de desenvolvimento para novo sistema
- [ ] Definir interface de migração

### Fase 2: Módulo {module-1}

**Duração estimada:** {weeks}

- [ ] Extrair interface do módulo
- [ ] Implementar novo módulo
- [ ] Criar testes para novo módulo
- [ ] Configurar feature flag
- [ ] Redirecionar 10% do tráfego
- [ ] Monitorar por {days} dias
- [ ] Redirecionar 100% do tráfego
- [ ] Remover código legado do módulo

### Fase 3: Módulo {module-2}

**Duração estimada:** {weeks}

- [ ] Extrair interface do módulo
- [ ] Implementar novo módulo
- [ ] Criar testes para novo módulo
- [ ] Configurar feature flag
- [ ] Redirecionar 10% do tráfego
- [ ] Monitorar por {days} dias
- [ ] Redirecionar 100% do tráfego
- [ ] Remover código legado do módulo

### Fase 4: Limpeza

**Duração estimada:** {weeks}

- [ ] Remover código legado restante
- [ ] Remover dependências legadas
- [ ] Atualizar documentação
- [ ] Remover feature flags
- [ ] Fechar issues de migração

## Riscos e Mitigações

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Dados inconsistentes | Alto | Média | Sincronização durante migração |
| Performance degradation | Médio | Baixa | Benchmark antes/depois |
| Perda de funcionalidade | Alto | Baixa | Testes de caracterização completos |
| Resistência da equipe | Médio | Média | Treinamento e documentação |

## Critérios de Sucesso

- [ ] Todos os módulos migrados
- [ ] Testes automatizados cobrindo novo sistema
- [ ] Performance igual ou melhor que legado
- [ ] Zero regressões em produção
- [ ] Documentação atualizada
- [ ] Time treinado no novo sistema

## Rollback Plan

1. Desativar feature flag para novo módulo
2. Redirecionar tráfego todo para legado
3. Investigar causa da falha
4. Corrigir e tentar novamente

## Referências

- [Strangler Fig Pattern](https://martinfowler.com/bliki/StranglerFigApplication.html)
- [Branch by Abstraction](https://martinfowler.com/bliki/branchByAbstraction.html)
- `refactoring` - para técnicas de refatoração incremental
