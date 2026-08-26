---
id: ADR-025-TODO
type: todo
title: "Execução - Ingestão Hierárquica Multi-Asset de Skills (Skill Bundles)"
created: "2026-08-24"
updated: "2026-08-24"
adr_ref: ADR-025
---

# ADR-025-TODO: Execução - Ingestão Hierárquica Multi-Asset de Skills (Skill Bundles)

> Referência: [ADR-025](./ADR-025-hierarchical-multi-asset-ingestion.md) | Status: ✅ CONCLUIDO

## Legenda

- ✅ Concluído
- ⬜ Pendente
- 🔄 Em Andamento
- ❌ Bloqueado
- ⏸️ Pausado

**Prioridade:** 🔴 Alta | 🟡 Média | 🟢 Baixa

---

## Fase A: Esquema de Dados & Parser Seletivo de Ativos (Indexador)

### A1: DDL Migration & AssetParser em `skills_rag_indexer.py`

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|:------:|:----------:|--------------|:----------:|
| A1.1 | Adicionar colunas `asset_type`, `parent_skill_id` e `file_path` na tabela `skill_chunks` em `skills_rag_indexer.py` | ✅ | 🔴 | — | 15m |
| A1.2 | Implementar a classe `AssetParser` com métodos para Markdown, Python/Shell (`extract_script_docstring`) e Templates (`extract_template_skeleton`) | ✅ | 🔴 | A1.1 | 30m |
| A1.3 | Atualizar o método de varredura `scan_skill_directory` para processar recursivamente as pastas `references/`, `templates/` e `scripts/` associadas ao bundle | ✅ | 🔴 | A1.2 | 25m |
| A1.4 | Executar re-indexação de teste e validar persistência das 4 camadas no banco SQLite `data/skills_rag_db/skills_rag.sqlite3` | ✅ | 🔴 | A1.3 | 15m |

**Checkpoint Fase A:**
- [x] Tabela `skill_chunks` armazena `asset_type`, `parent_skill_id` e `file_path`
- [x] Chunks de scripts e templates extraídos com zero ruído de código procedural

---

## Fase B: Damping Factor Ponderado & Payload Tipado (Roteador e MCP)

### B1: Integração no Servidor MCP (`skills_mcp_server.py`) e CLI (`skills_router.py`)

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|:------:|:----------:|--------------|:----------:|
| B1.1 | Atualizar consultas SQL em `skills_mcp_server.py` para selecionar `asset_type`, `parent_skill_id` e `file_path` | ✅ | 🔴 | Fase A | 20m |
| B1.2 | Implementar o Damping Factor multiplicativo no scoring inicial (`skill_root: 1.0`, `reference: 0.85`, `template: 0.80`, `script_doc: 0.75`) | ✅ | 🔴 | B1.1 | 20m |
| B1.3 | Atualizar serializador XML de chunks para emitir tags tipadas `<active_skill id="..." parent="..." type="..." path="...">` | ✅ | 🔴 | B1.2 | 15m |
| B1.4 | Adicionar flag `--asset-type` (opcional) em `skills_router.py` para filtragem direcionada via CLI | ✅ | 🟡 | B1.3 | 15m |

**Checkpoint Fase B:**
- [x] Servidor MCP retorna chunks com atributos XML tipados
- [x] Intenção explícita de template/script promove o chunk secundário no reranker

---

## Fase C: Suíte de Testes Automatizados & Validação SOTA

### C1: Criação e Execução de Testes Unitários e Forenses

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|:------:|:----------:|--------------|:----------:|
| C1.1 | Criar a suíte [.github/scripts/tests/test_rag_hierarchical.py](file:///home/loupan/.gemini/config/skills/.github/scripts/tests/test_rag_hierarchical.py) testando parser, parent linking, damping factor e XML serialization | ✅ | 🔴 | Fase B | 30m |
| C1.2 | Executar todas as 5 suítes de testes automatizados (`test_rag_hierarchical`, `test_mcp_telemetry`, `test_mcp_bootstrap`, `test_rag_federated`, `test_rag_quad_sota`) | ✅ | 🔴 | C1.1 | 15m |
| C1.3 | Executar o motor forense `python3 .github/scripts/audit_engine.py` e validar integridade de 100% dos ativos | ✅ | 🔴 | C1.2 | 15m |

**Checkpoint Fase C:**
- [x] 5/5 suítes de testes passando com 100% de sucesso
- [x] 81/81 ativos auditados com nota média $\ge 91.0 / 100$

---

## Resumo Geral

| Fase | Tarefas | Horas Est. | Status |
|------|:-------:|:----------:|:------:|
| **Fase A: Esquema & Parser de Ativos** | 4 | ~1.4h | ✅ |
| **Fase B: Damping Factor & MCP Tipado** | 4 | ~1.2h | ✅ |
| **Fase C: Suíte de Testes & Auditoria** | 3 | ~1.0h | ✅ |
| **Total** | **11** | **~3.6h** | **✅ CONCLUIDO** |

---

## Dependências entre Fases

```text
Fase A (Esquema & Parser de Ativos)
  │
  └─── A1: Indexador Multi-Asset & DDL ─────┐
                                            │
Fase B (Damping Factor & MCP Tipado) ◄──────┘
  │
  └─── B1: Resolução Tipada & Scoring ──────┐
                                            │
Fase C (Testes Automatizados & Auditoria) ◄─┘
```

---

*Documento gerado em 2026-08-24. Referência: ADR-025.*
