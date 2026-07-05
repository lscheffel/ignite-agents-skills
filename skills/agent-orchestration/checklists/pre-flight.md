# Pre-Flight Checklist

Checklist antes de iniciar orquestração multi-agente.

## Decomposição
- [ ] Tarefa decomposta em subtarefas claras
- [ ] Dependências entre subtarefas mapeadas
- [ ] Subtarefas independentes identificadas para paralelismo

## Papéis
- [ ] Papel definido para cada agente
- [ ] Card de papel preenchido para cada agente
- [ ] Responsabilidades não se sobrepõem

## Contratos
- [ ] Contrato I/O definido para cada handoff
- [ ] Schemas consistentes entre agentes
- [ ] Validação implementada para cada contrato
- [ ] Fallback definido para cada contrato

## Roteamento
- [ ] Modelo selecionado para cada papel
- [ ] Custo estimado documentado
- [ ] Fallback de modelo definido
- [ ] Throughput adequado

## Execução
- [ ] Fan-out configurado para subtarefas independentes
- [ ] Fan-in configurado para agregação
- [ ] Gate de sincronização definido
- [ ] Janela de contexto configurada
- [ ] Logging configurado
