# Plano de Implementação: ADR-028 — Visual Cognitive Ergonomics & Decision Graphs

## 1. Fases de Execução

### Fase 1: Identificação de Skills sem Diagrama Mermaid
- Escanear o repositório identificando skills com ausência de blocos ````mermaid````.

### Fase 2: Injeção de Topologias Visuais & Checklists
- Injetar grafos de decisão Mermaid após a seção `When to Use`.
- Injetar tabela de `Anti-Patterns` com badges `🔴 Critical`, `🟡 Medium`, `🟢 Low`.
- Injetar seção de `Operational Verification Checklist` e `Completion Gate`.

### Fase 3: Validação de Renderização
- Compilar as páginas HTML via `python3 pages/build.py` para certificar que os blocos Mermaid renderizam com precisão.

---

## 2. Critérios de Aceite
- [ ] 60/60 skills possuem diagramas Mermaid válidos.
- [ ] 60/60 skills possuem checkboxes `- [ ]` e Completion Gates explícitos.
