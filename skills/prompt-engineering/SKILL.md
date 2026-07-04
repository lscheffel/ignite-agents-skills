---
name: prompt-engineering
description: Diretrizes para engenharia de prompts eficazes com agentes de IA. Cobre estrutura de prompts, few-shot, chain-of-thought, role prompting, constraints e técnicas avançadas. Use quando criar prompts complexos, otimizar interações com agentes, ou treinar equipes em IA.
---

# Prompt Engineering

Diretrizes para engenharia de prompts eficazes.

## Quando Usar

- Criação de prompts para agentes de IA
- Otimização de interações com LLMs
- Treinamento de equipes em IA
- Padronização de prompts entre projetos

## Estrutura de Prompt

### 1. Contexto
Quem é o agente, qual seu papel, qual o objetivo.

### 2. Tarefa
O que deve ser feito, de forma clara e específica.

### 3. Formato de Saída
Estrutura esperada da resposta.

### 4. Restrições
O que NÃO fazer, limites e regras.

## Técnicas

### Role Prompting
```
Você é um arquiteto de software sênior especializado em DDD...
```

### Few-Shot
```
Exemplo 1:
Input: ...
Output: ...

Exemplo 2:
Input: ...
Output: ...

Agora processe:
Input: ...
```

### Chain-of-Thought
```
Pense passo a passo:
1. Primeiro, ...
2. Depois, ...
3. Finalmente, ...
```

### Constrained Output
```
Responda APENAS com o código final.
Não inclua explicações.
```

## Anti-patterns

- Prompts vagos ("melhore o código")
- Múltiplas tarefas em um prompt
- Instruções contraditórias
- Falta de contexto necessário
