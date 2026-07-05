# Change Plan

> Plano interno de execução construído a partir da análise de dependências do TODO.

---

## Identificação

| Campo | Valor |
|-------|-------|
| ADR | {{adr_path}} |
| Data de geração | {{date}} |
| Total de tarefas | {{total_tasks}} |
| Estimativa total | {{total_estimate}} |

---

## DAG de Execução

```mermaid
graph LR
{{#each dag_nodes}}
    {{id}}[{{label}}]{{#if edges}} --> {{target}}{{/if}}
{{/each}}
```

### Legenda

| Cor | Significado |
|-----|-------------|
| ⬜ | Pendente |
| 🔄 | Em andamento |
| ✅ | Concluído |
| ❌ | Bloqueado |

---

## Ordem de Execução

| Fase | Tarefas | Dependências | Tempo Est. |
|------|---------|--------------|------------|
{{#each phases}}
| {{number}} | {{tasks}} | {{dependencies}} | {{estimate}} |
{{/each}}

---

## Tarefas Detalhadas

| # | Tarefa | Estado | Dependências | Prioridade | Estimativa | Arquivos |
|---|--------|--------|--------------|------------|------------|----------|
{{#each tasks}}
| {{number}} | {{name}} | {{status}} | {{deps}} | {{priority}} | {{estimate}} | {{files}} |
{{/each}}

---

## Tarefas Paralelizáveis

| Fase | Tarefas que podem rodar em paralelo |
|------|--------------------------------------|
{{#each parallel_tasks}}
| {{phase}} | {{tasks}} |
{{/each}}

---

## Pontos de Verificação

| Após Tarefa | Verificar | Critério |
|-------------|-----------|----------|
{{#each checkpoints}}
| {{after_task}} | {{check}} | {{criterion}} |
{{/each}}

---

## Estimativa Detalhada

| Componente | Tempo Est. | Notas |
|------------|------------|-------|
| Tarefas de infraestrutura | {{infra_estimate}} | Criação de estrutura |
| Tarefas de implementação | {{impl_estimate}} | Código principal |
| Tarefas de validação | {{validation_estimate}} | Testes e verificação |
| Tarefas de documentação | {{docs_estimate}} | Atualização de docs |
| Buffer (20%) | {{buffer}} | Imprevistos |
| **Total** | **{{total}}** | |

---

## Riscos do Plano

| # | Risco | Impacto no Plano | Mitigação |
|---|-------|------------------|-----------|
{{#each plan_risks}}
| {{number}} | {{risk}} | {{impact}} | {{mitigation}} |
{{/each}}

---

## Validação do Plano

- [ ] DAG construído sem ciclos
- [ ] Todas as tarefas têm dependências definidas
- [ ] Estimativas somam ao total esperado
- [ ] Tarefas paralelizáveis são realmente independentes
- [ ] Pontos de verificação cobrem tarefas críticas
- [ ] Riscos do plano documentados
