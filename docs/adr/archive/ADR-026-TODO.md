---
id: ADR-026-TODO
type: todo
title: "Execução - Catálogo Canônico Unificado em Inglês (EN-US) via NVIDIA NIM"
created: "2026-08-25"
updated: "2026-08-25"
adr_ref: ADR-026
---

# ADR-026-TODO: Execução - Catálogo Canônico Unificado em Inglês (EN-US) via NVIDIA NIM

> Referência: [ADR-026](./ADR-026.md) | Status: ✅ CONCLUÍDO

## Legenda

- ✅ Concluído
- ⬜ Pendente
- 🔄 Em Andamento
- ❌ Bloqueado
- ⏸️ Pausado

**Prioridade:** 🔴 Alta | 🟡 Média | 🟢 Baixa

---

## Fase A: Script de Tradução Autônomo

### A1: Pipeline de Tradução via NVIDIA NIM

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|:------:|:----------:|--------------|:----------:|
| A1.1 | Implementar `init_cache()` (SQLite, SHA256) | ✅ | 🔴 | — | 10m |
| A1.2 | Implementar `detect_language()` (stopword heuristic) | ✅ | 🔴 | — | 15m |
| A1.3 | Implementar `call_nvidia_nim()` com cascata de fallback | ✅ | 🔴 | A1.1 | 20m |
| A1.4 | Implementar `protect_syntax()`/`restore_syntax()` (regex) | ✅ | 🔴 | — | 25m |
| A1.5 | Implementar `extract_docstrings_and_comments()` para `.py/.sh/.js` | ✅ | 🟡 | A1.4 | 25m |
| A1.6 | Implementar validação AST (`ast.parse`) e `bash -n` | ✅ | 🔴 | — | 15m |
| A1.7 | Implementar `call_nim_code_judge()` (NIM Code Judge) | ✅ | 🔴 | A1.3 | 20m |
| A1.8 | Implementar `validate_translation()` (estágio unificado) | ✅ | 🔴 | A1.6, A1.7 | 15m |
| A1.9 | Implementar `process_file()` e `main()` | ✅ | 🔴 | A1.1-A1.8 | 20m |
| A1.10 | Implementar suíte de testes unitários offline `test_catalog_translation.py` | ✅ | 🔴 | A1.1-A1.9 | 15m |

**Checkpoint Fase A:**
- [x] `translate_catalog_nim.py` criado e executável (stdlib-only)
- [x] Cascata de modelos verificada e funcionando
- [x] `test_catalog_translation.py` passando 100% offline

---

## Fase B: Execução, Auditoria e Re-indexação

### B1: Pipeline Fim a Fim

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|:------:|:----------:|--------------|:----------:|
| B1.1 | Executar `python3 .github/scripts/translate_catalog_nim.py` | ✅ | 🔴 | Fase A | 30m |
| B1.2 | Executar `python3 .github/scripts/audit_engine.py` (100% conformidade) | ✅ | 🔴 | B1.1 | 15m |
| B1.3 | Corrigir cabeçalhos Markdown se danificados | ✅ | 🟡 | B1.2 | 15m |
| B1.4 | Executar `python3 .github/scripts/skills_rag_indexer.py --force` | ✅ | 🔴 | B1.2 | 15m |
| B1.5 | Executar 7 suítes completas de testes automatizados | ✅ | 🔴 | B1.4 | 20m |

**Checkpoint Fase B:**
- [x] Tradução executada, auditoria 100%, re-indexação completa
- [x] 7/7 suítes de testes passando

---

## Fase C: Governança e Fechamento

### C1: Evidence Record, Arquivamento e Release

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|:------:|:----------:|--------------|:----------:|
| C1.1 | Gerar `ADR-026-ER.md` com métricas de compressão BPE | ✅ | 🔴 | Fase B | 15m |
| C1.2 | Arquivar Decision Set em `docs/adr/archive/` | ✅ | 🔴 | C1.1 | 10m |
| C1.3 | Atualizar `ADR-INDEX.md` para `CONSOLIDADA \| ARCHIVED_OK` | ✅ | 🔴 | C1.2 | 10m |
| C1.4 | Reconciliar 6 pilares documentais | ✅ | 🟡 | C1.3 | 15m |
| C1.5 | Commit atômico + tag `v2.5.0` + push | ✅ | 🔴 | C1.4 | 10m |

**Checkpoint Fase C:**
- [x] ER gerado, Decision Set arquivado, index atualizado
- [x] Tag `v2.5.0` criada e reconciliação concluída

---

## Resumo Geral

| Fase | Tarefas | Horas Est. | Status |
|------|:-------:|:----------:|:------:|
| **Fase A: Script de Tradução** | 10 | ~3.0h | ✅ |
| **Fase B: Execução & Validação** | 5 | ~1.5h | ✅ |
| **Fase C: Governança & Release** | 5 | ~1.0h | ✅ |
| **Total** | **20** | **~5.5h** | ✅ CONCLUÍDO |

---

## Dependências entre Fases

```text
Fase A (Script de Tradução Autônomo)
  │
  └─── A1: Pipeline NIM + Validação Forense ──┐
                                              │
Fase B (Execução, Auditoria & Re-indexação) ◄─┘
  │
  └─── B1: Pipeline Fim a Fim ────────────────┐
                                              │
Fase C (Governança & Release) ◄───────────────┘
```

---

*Documento gerado em 2026-08-25. Referência: ADR-026.*