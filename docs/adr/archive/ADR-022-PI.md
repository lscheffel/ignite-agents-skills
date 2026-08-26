---
id: ADR-022-PI
type: pi
title: "Implementation Plan - Pipeline RAG Quádruplo SOTA"
created: 2026-08-24
updated: 2026-08-24
adr_ref: ADR-022
---

# ADR-022-PI: Implementation Plan - Pipeline RAG Quádruplo SOTA

> Referência: [ADR-022](./ADR-022-rag-sota-quad-optimizations.md) | [ADR-022-TODO](./ADR-022-TODO.md)

---

## 1. Visão Geral (Overview)

Este plano de implementação estabelece o roteiro microscópico com abordagem TDD para introduzir os 4 módulos SOTA no subsistema RAG:
1. **Cache de Rerank SQLite3**
2. **Dense Embeddings Nemotron-3 (2048-dim)**
3. **Chunk-Level Focused Injection**
4. **Acronym & Synonym Expansion**

---

## 2. Padrões de Aceitação e Qualidade

- **Test Coverage:** 100% de testes unitários e de integração para novas funções de cache e expansão de siglas.
- **Latência:** Cache hits devem retornar em `< 2ms` no SQLite local.
- **Compatibilidade:** Fallback 100% preservado para ambientes offline sem dependências de rede.
- **Padrão de Código:** Python 3.10+, zero bibliotecas externas obrigatórias (usar `urllib` / `requests` nativo e `sqlite3`).

---

## 3. Plano de Execução Granular (TDD & Step-by-Step)

### Fase A: Cache Persistente & Expansão de Siglas

#### Passo A.1: TDD para Expansão de Siglas e Cache Local

**1. TDD Specs:**
- **Arquivo de Teste:** `.github/scripts/tests/test_rag_enhancements.py`
- **Asserções Esperadas:**
  - `expand_query("Como implementar RBAC?")` deve conter `"role based access control"`.
  - `set_rerank_cache(hash, data)` seguido de `get_rerank_cache(hash)` deve retornar o JSON idêntico.
- **Comando de Teste:**
  ```bash
  python3 -m unittest .github/scripts/tests/test_rag_enhancements.py
  ```

**2. Code Specs:**
- Criar módulo `ACRONYM_EXPANSION_DICT` em `skills_router.py` e `skills_mcp_server.py`.
- Adicionar métodos de cache:
  ```python
  def get_cached_ranking(cur, query_hash: str) -> dict | None: ...
  def save_cached_ranking(cur, conn, query_hash: str, query_text: str, rankings: list, engine: str) -> None: ...
  ```

---

### Fase B: Embeddings Densos Nemotron-3 (2048-dim)

#### Passo B.1: Ingestão e Cálculo de Vetores de 2048 Dimensões

**1. TDD Specs:**
- **Arquivo de Teste:** `.github/scripts/tests/test_nemotron_embeddings.py`
- **Asserções Esperadas:**
  - Vetor retornado pela API da NVIDIA deve possuir dimensão exata de `2048` elementos float.
  - Em caso de falha de conexão / timeout, deve retornar vetor de 512 dimensões sem quebrar o fluxo.

**2. Code Specs:**
- Implementar em `skills_rag_indexer.py`:
  ```python
  def fetch_nemotron_embedding(text: str, api_key: str) -> list[float] | None: ...
  ```
- Atualizar o schema SQLite para armazenar `vector_embedding_2048 TEXT`.

---

### Fase C: Injeção Dinâmica por Chunks (Token Economy)

#### Passo C.1: Extração e Formatação do Chunk Mais Relevante

**1. TDD Specs:**
- **Arquivo de Teste:** `.github/scripts/tests/test_focused_injection.py`
- **Asserções Esperadas:**
  - Para a query `"como fazer refatoracao strangler fig"`, o chunk retornado deve ser a seção correspondente de `refactoring`.
  - O XML retornado deve conter a tag `<focused_chunk section="...">`.

**2. Code Specs:**
- No `skills_router.py`:
  ```python
  def get_focused_chunk_for_skill(cur, skill_id: str, query_vec: list[float]) -> dict: ...
  ```

---

## 4. Validação Contínua (Continuous Validation)

Comandos para validar a integridade completa da suíte após implementação:

```bash
# 1. Testes Automatizados das Otimizações
python3 -m unittest discover -s .github/scripts/tests/ -p "test_*.py"

# 2. Auditoria Forense dos 8 Vetores SOTA
python3 .github/scripts/audit_engine.py

# 3. Teste End-to-End do Roteador com Cache
python3 .github/scripts/skills_router.py "auditoria de seguranca rbac"
python3 .github/scripts/skills_router.py "auditoria de seguranca rbac"  # deve dar Cache Hit (0ms)
```

---

## 5. Handoff para Fechamento

Ao concluir os testes e validações contínuas, este plano servirá de insumo para a geração do Evidence Record (`docs/governance/ER-022.md`), fechando o ciclo de governança do Decision Set.

---

*Documento gerado em 2026-08-24. Referência: ADR-022.*
