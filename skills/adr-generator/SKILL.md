---
name: adr-generator
description: Cria Architecture Decision Records (ADRs) para documentar decisões arquiteturais importantes. Gera templates padronizados com contexto, decisão, consequências e status. Use quando o usuário mencionar ADR, decisão arquitetural, ou precisar documentar trade-offs técnicos.
version: 2.0.0
tags: [architecture, decisions, adr, documentation]
related_skills: [documentation, architecture-review]
---

# ADR Generator

Gera Architecture Decision Records (ADRs) seguindo o formato MADR ou similar.

## Quando Usar

### Use quando:
- Decisão arquitetural significativa precisa ser documentada
- Usuário solicita criação de ADR
- Registro de trade-offs técnicos
- Decisões que afetam múltiplos módulos ou equipes

### Não use quando:
- Decisão é óbvia (ex: usar tabs vs spaces)
- Decisão é reversível sem custo
- Protótipo rápido

### Skills relacionadas:
- `documentation` — para padrões de documentação
- `architecture-review` — para revisar decisões arquiteturais

## Decision Tree

```mermaid
graph TD
    A[Decisão importante?] -->|Arquitetura| B[ADR]
    A -->|Processo| C[RFC]
    A -->|Simples| D[Decision Doc]
    A -->|Urgente| E[ADR de Emergência]
    B -->|Impacto alto| F[ADR Completo]
    B -->|Impacto baixo| G[ADR Simplificado]
```

## Workflow

### Fase 1: Criar ADR Completo

1. Crie arquivo em `docs/adr/ADR-XXX.md`:
   ```bash
   cp templates/adr.md docs/adr/ADR-00X.md
   ```
2. Preencha contexto:
   - Problema
   - Motivação
   - Restrições
3. Liste alternativas:
   - Alternativa A: prós/contras
   - Alternativa B: prós/contras
4. Defina decisão
5. Documente consequências
6. **Checkpoint**: ADR aprovado e linkado em README

### Fase 2: Revisar ADR Existente

1. Leia ADR:
   ```bash
   cat docs/adr/ADR-00X.md
   ```
2. Verifique se ainda é válido:
   - Contexto mudou?
   - Alternativas mudaram?
3. Atualize status:
   - Aceito → Substituído (se aplicável)
4. **Checkpoint**: ADR revisado ou mantido

### Fase 3: Substituir ADR

1. Crie novo ADR:
   ```bash
   cp templates/adr.md docs/adr/ADR-NEW.md
   ```
2. No ADR antigo, atualize status:
   ```markdown
   ## Status
   Substituído por ADR-NEW
   ```
3. Link no novo ADR:
   ```markdown
   ## Referências
   - Substitui ADR-OLD
   ```
4. **Checkpoint**: Substituição documentada

## Conceitos Fundamentais

### Estrutura do ADR

```markdown
# ADR-XXX: [Título da Decisão]

## Status
Proposto | Aceito | Rejeitado | Suspenso | Substituído

## Contexto
Descreva o problema, motivação e restrições.

## Decisão
Descreva a solução escolhida.

## Alternativas Consideradas
- Alternativa A: descrição, prós e contras
- Alternativa B: descrição, prós e contras

## Consequências
### Positivas
- ...

### Negativas
- ...
```

### Status Values

- **Proposto**: Em discussão
- **Aceito**: Aprovado e implementado
- **Rejeitado**: Rejeitado, não implementado
- **Suspenso**: Em espera
- **Substituído**: Reemplazado por outro ADR

## Templates

### adr.md
Localização: `templates/adr.md`

Template para Architecture Decision Record.

**Uso:**
```bash
cp templates/adr.md docs/adr/ADR-00X.md
```

## Anti-patterns

### 🔴 Crítico

#### ADR Retrospectivo
**O que é:** Criar ADR após decisão já implementada.
**Por que é ruim:** Não registra trade-offs, parece justificação.
**Como evitar:** Crie ADR antes da implementação.
**Exemplo:**
```
# ❌ ERRADO
Decisão tomada em 2024-01-01
ADR criado em 2024-06-01

# ✅ CORRETO
ADR criado em 2024-01-01
Decisão implementada em 2024-01-15
```

#### ADR sem Alternativas
**O que é:** ADR que não lista alternativas consideradas.
**Por que é ruim:** Não mostra trade-offs, parece decisão aleatória.
**Como evitar:** Sempre liste pelo menos 2 alternativas.
**Exemplo:**
```
# ❌ ERRADO
Escolhemos React porque é bom

# ✅ CORRETO
Alternativas:
- React: comunidade grande, curva aprendizado média
- Vue: curva aprendizado baixa, comunidade menor
- Svelte: performance alta, comunidade pequena
Escolhemos React por comunidade e documentação
```

### 🟡 Médio

#### ADR Vago
**O que é:** ADR sem contexto ou decisão clara.
**Por que é ruim:** Futuro desenvolvedor não entende motivação.
**Como evitar:** Seja específico, inclua dados.
**Exemplo:**
```
# ❌ ERRADO
Usamos PostgreSQL

# ✅ CORRETO
Usamos PostgreSQL por:
- Suporte a JSONB para queries flexíveis
- Replicação síncrona para HA
- Equipe já tem experiência
```

### 🟢 Baixo

#### ADR sem Data
**O que é:** ADR sem data de criação.
**Por que é ruim:** Difícil rastrear histórico.
**Como evitar:** Sempre inclua data.
**Exemplo:**
```markdown
# ✅ CORRETO
# ADR-001: Database Choice
## Status
Aceito

## Date
2024-01-15
```

## Checklists

### Checklist de ADR
- [ ] Título claro e descritivo
- [ ] Contexto completo
- [ ] Alternativas listadas
- [ ] Decisão justificada
- [ ] Consequências documentadas
- [ ] Data incluída
- [ ] Stakeholders identificados

### Checklist de Review
- [ ] Contexto ainda relevante?
- [ ] Decisão ainda válida?
- [ ] Alternativas precisam atualização?
- [ ] Status atualizado

## Edge Cases

### ADR de Emergência
**Situação:** Decisão urgente precisa ser documentada.
**Solução:** Crie ADR simplificado, detalhe depois.
**Exceção:** Se emergência é crítica, documente imediatamente.

```markdown
## Status
Aceito (emergencial)
```

### ADR para Experimento
**Situação:** Decisão experimental precisa ser documentada.
**Solução:** Use status "Suspenso" ou "Experimental".
**Exceção:** Se experimento é pequeno, use Decision Doc.

```markdown
## Status
Suspenso (experimental)
```

## Referências

- [MADR](https://adr.github.io/madr/)
- `documentation` — para padrões
- `architecture-review` — para revisões