---
name: architecture-review
description: Realiza revisões arquiteturais de código, detectando violações de princípios SOLID, padrões arquiteturais (Clean Architecture, Hexagonal, DDD) e code smells estruturais. Use quando o usuário pedir revisão de arquitetura, análise de estrutura, ou avaliação de design.
---

# Architecture Review

Realiza revisões arquiteturais sistemáticas de código e estruturas de projeto.

## Quando Usar

- Revisão de PR com impacto arquitetural
- Análise de estrutura de projeto
- Detecção de violações de princípios SOLID
- Avaliação de aderência a padrões (Clean Architecture, Hexagonal, DDD)

## Checklist de Revisão

### SOLID
- [ ] SRP: Cada classe/módulo tem uma única responsabilidade?
- [ ] OCP: Extensível sem modificar código existente?
- [ ] LSP: Subtipos substituem seus tipos base?
- [ ] ISP: Interfaces específicas, não genéricas?
- [ ] DIP: Depende de abstrações, não concretos?

### Clean Architecture / Hexagonal
- [ ] Regras de negócio não dependem de frameworks
- [ ] Casos de uso orquestram entidades
- [ ] Adaptadores (gateways, controllers) isolam infraestrutura
- [ ] Inversão de dependência respeitada

### DDD
- [ ] Entidades com identidade própria
- [ ] Value Objects imutáveis
- [ ] Agregados com边界 bem definidos
- [ ] Repositórios como abstração de coleção
- [ ] Domain Events para comunicação entre contextos

### Code Smells Estruturais
- [ ] God Class / God Module
- [ ] Feature Envy
- [ ] Data Clumps
- [ ] Shotgun Surgery
- [ ] Circular Dependencies

## Formato de Saída

Para cada issue encontrada:

```markdown
### [Severidade] Título do Problema

**Arquivo:** caminho/arquivo.ext:linha  
**Princípio violado:** SOLID/Outro  
**Descrição:** Explicação clara do problema  
**Sugestão:** Como corrigir  
**Referência:** Link ou padrão aplicável
```
