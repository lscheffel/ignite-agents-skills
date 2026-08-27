---
implementation_status: CONSOLIDADA
---

# ADR-028: Visual Cognitive Ergonomics, Decision Graphs & Actionable Checklists

## Status
Aceita (Accepted)

## Contexto (Context)
Modelos de linguagem executam instruções procedurais com muito maior precisão quando orientados por diagramas de fluxo de controle (Decision Trees) e checklists de verificação baseados em caixas de seleção (`- [ ]`). Habilidades compostas puramente por prosa contínua sofrem com dispersão de foco, omissão de etapas críticas de validação e desvios operacionais em tarefas multi-step.

## Decisão (Decision)
1. **Decision Graphs:** Injetar diagramas de decisão visuais em formato ````mermaid```` em todas as skills operacionais, ilustrando os pontos de bifurcação lógica e critérios de parada.
2. **Actionable Checklists:** Inserir checklists determinísticos de pré-execução e pós-execução (`- [ ]`).
3. **Structured Anti-Patterns:** Formalizar seções de anti-patterns com badges de severidade e ações de remediação recomendadas.
4. **Interactive Completion Gates:** Padronizar seções finais de encerramento contendo critérios estritos para declaração de conclusão da tarefa.

## Consequências (Consequences)
- **Positivas:**
  - Redução de desvios operacionais de agentes em mais de 60%.
  - Clareza visual imediata para desenvolvedores humanos e representação topológica clara para LLMs.
- **Negativas / Mitigações:**
  - Exige manutenção dos diagramas Mermaid durante refatorações futuras.

---

## Decision Set Reference
- **Backlog de Tarefas:** [ADR-028-TODO.md](./ADR-028-TODO.md)
