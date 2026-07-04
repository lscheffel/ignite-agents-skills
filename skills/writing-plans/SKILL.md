---
name: writing-plans
description: Cria planos de implementação detalhados, passo a passo, a partir de uma especificação técnica ou requisitos. Divide trabalho em tarefas executáveis com critérios de aceitação, dependências e sequenciamento. Use quando o usuário pedir um plano de implementação, roadmap técnico, ou quebra de tarefas.
---

# Writing Plans

Gera planos de implementação estruturados e executáveis a partir de especificações.

## Quando Usar

- Usuário pede um plano de implementação
- Necessário quebrar uma feature em tarefas
- Solicitação de roadmap técnico
- Análise de dependências e sequenciamento de trabalho

## Fluxo de Trabalho

1. **Leia a especificação**
   - Compreenda o objetivo final
   - Identifique restrições e requisitos não funcionais
   - Liste entidades e domínios envolvidos

2. **Divida em fases**
   - Fase 1: Fundação (estrutura, tipos, contratos)
   - Fase 2: Core (lógica principal, happy path)
   - Fase 3: Integração (conectores, APIs, eventos)
   - Fase 4: Observabilidade (logs, métricas, traces)

3. **Para cada tarefa, documente:**
   - Título claro e acionável
   - Arquivos a criar/modificar
   - Critérios de aceitação (comandos de teste se aplicável)
   - Dependências de outras tarefas
   - Estimativa de complexidade (S/M/L)

4. **Validação**
   - Revise se o plano cobre todos os requisitos
   - Verifique se não há tarefas duplicadas
   - Confira se a ordem de execução é lógica

## Formato de Saída

Use uma lista numerada com o seguinte formato:

```markdown
## Tarefa 1: [Título]

**Arquivos:** caminho/arquivo1.ext, caminho/arquivo2.ext  
**Complexidade:** S|M|L  
**Dependências:** Tarefa X (se houver)  
**Critérios de aceitação:**
- [ ] Critério 1
- [ ] Critério 2
- [ ] Critério 3

**Comandos de validação:**
\```bash
comando de teste ou verificação
\```
```

## Boas Práticas

- Tarefas pequenas (max 4h de trabalho)
- Uma responsabilidade por tarefa
- Sempre inclua critérios de aceitação verificáveis
- Priorize o caminho feliz antes de edge cases
