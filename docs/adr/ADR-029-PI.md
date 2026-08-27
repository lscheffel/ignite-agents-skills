# Plano de Implementação: ADR-029 — Modular Multi-Asset Scaffolding & Edge Cases Baseline

## 1. Fases de Execução

### Fase 1: Criação de Estrutura de Diretórios
- Percorrer as 60 pastas em `skills/` e assegurar que as subpastas `templates/` e `examples/` existam.

### Fase 2: Geração de Templates & Exemplos Canônicos
- Gerar templates de artefato e referências de exemplo executáveis para cada skill.

### Fase 3: Injeção de Casos de Borda em SKILL.md
- Adicionar a seção `## Edge Cases & Failure Modes` em cada arquivo `SKILL.md`.

### Fase 4: Reindexação do RAG Hierárquico
- Executar `python3 scripts/skills_rag_indexer.py` para ingerir os novos bundles e atualizar o banco vetorial SQLite.

---

## 2. Critérios de Aceite
- [ ] 60/60 skills possuem subpastas `templates/` e `examples/`.
- [ ] 60/60 skills possuem seções de Edge Cases.
- [ ] Ingestão RAG indexa com sucesso todos os novos assets.
