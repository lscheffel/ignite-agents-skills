# ADR-029: Modular Multi-Asset Scaffolding & Edge Cases Baseline across Skills

## Status
Aceita (Accepted)

## Contexto (Context)
Conforme estabelecido pela ADR-025, o repositório suporta ingestão hierárquica ponderada de múltiplos assets por skill bundle (`SKILL.md`, `templates/`, `examples/`, `references/`, `scripts/`). No entanto, cerca de 35 micro-skills possuíam apenas o arquivo `SKILL.md` isolado, sem templates reutilizáveis ou exemplos de código práticos, limitando sua utilidade em tempo de execução e reduzindo a pontuação no Eixo Estrutural.

## Decisão (Decision)
1. **Asset Scaffolding:** Criar subpastas modulares de apoio (`templates/` e `examples/`) para as micro-skills que não possuíam arquivos complementares.
2. **Edge Cases Section:** Adicionar seções explícitas de casos extremos e modos de falha (`## Edge Cases & Failure Modes`) para instruir os agentes sobre comportamento em cenários não ideais.
3. **Command & Code Snippet Verification:** Garantir que todas as skills contenham blocos de código concretos e comandos testáveis, sem placeholders (`TODO`, `TBD`, `<insert here>`).

## Consequências (Consequences)
- **Positivas:**
  - Enriquecimento dos Skill Bundles ingeridos pelo RAG.
  - Acesso direto a templates prontos para uso em geração de artefatos.
  - Mitigação de alucinação em casos de borda.

---

## Decision Set Reference
- **Backlog de Tarefas:** [ADR-029-TODO.md](./ADR-029-TODO.md)
