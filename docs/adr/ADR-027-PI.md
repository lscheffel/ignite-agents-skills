# Plano de Implementação: ADR-027 — Multilingual Semantic Trigger & Governance Metadata Hardening

## 1. Fases de Execução

### Fase 1: Análise e Mapeamento de Triggers
- Mapear a tabela canônica de vocabulário bilíngue para todas as 60 skills em `scripts/remediate_structural_sota.py`.

### Fase 2: Injeção Sistemática no Frontmatter
- Percorrer os 60 arquivos `skills/*/SKILL.md`.
- Substituir o bloco `triggers:` existente pelo conjunto bilíngue mínimo de 8 termos.
- Garantir presença de `tags:`, `related_skills:`, `version:` e metadados de governança.

### Fase 3: Validação Forense & Reindexação RAG
- Executar `scripts/validate-index.sh` e `python3 scripts/skills_rag_indexer.py`.
- Verificar cobertura de busca via `python3 scripts/skills_router.py "auditar vulnerabilidades"`.

---

## 2. Critérios de Aceite
- [ ] 60/60 skills possuem no mínimo 8 triggers (EN + PT-BR).
- [ ] 0 violações de validação em `validate-index.sh`.
- [ ] Reindexação do banco SQLite vetorial concluída sem erros.
