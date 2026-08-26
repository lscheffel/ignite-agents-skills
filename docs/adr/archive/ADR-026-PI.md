---
id: ADR-026-PI
type: pi
title: "Implementation Plan - Catálogo Canônico Unificado em Inglês (EN-US) via NVIDIA NIM"
created: "2026-08-25"
updated: "2026-08-25"
adr_ref: ADR-026
---

# ADR-026-PI: Implementation Plan - Catálogo Canônico Unificado em Inglês (EN-US) via NVIDIA NIM

> Referência: [ADR-026](./ADR-026.md) | [ADR-026-TODO](./ADR-026-TODO.md)

---

## 1. Visão Geral (Overview)

Este plano estabelece os passos de engenharia para implementar a padronização do catálogo canônico de skills em EN-US via NVIDIA NIM, com pipeline autônomo de tradução, preservação estrita de sintaxe (código, frontmatter, XML, `parent_skill_id`), validação forense em dois estágios (AST estático + NIM Code Judge) e cache de idempotência.

---

## 2. Padrões de Aceitação e Qualidade (Quality Standards)

- **Zero Corrupção de Sintaxe:** Código procedural, `parent_skill_id`, nomes de variáveis e chaves de frontmatter permanecem intocados.
- **Determinismo:** `temperature=0.0` em todas as chamadas de modelo.
- **Tolerância a Falhas:** Cascata de fallback (tradução + judge); se todos falharem, o arquivo original é mantido.
- **Idempotência:** Cache SQLite por `SHA256(content)` permite retomada segura.
- **Stdlib-only:** Nenhuma dependência externa (`langdetect` proibido; heurística de stopwords).
- **Retrocompatibilidade:** Catálogo continua auditável e indexável após tradução.

---

## 3. Plano de Execução Granular (TDD & Step-by-Step)

### Fase A: Script de Tradução Autônomo

#### Passo A1.1: Implementação de `init_cache()`
- **Arquivos Afetados:** [.github/scripts/translate_catalog_nim.py](file:///home/loupan/.gemini/config/skills/.github/scripts/translate_catalog_nim.py)
- **Lógica:** Chave de cache `content_hash = hashlib.sha256(f"{content}:{model}:{PROMPT_VERSION}".encode()).hexdigest()`.
- **Alterações:**
  ```python
  PROMPT_VERSION = "v1.0.0"

  def get_cache_key(content: str, model: str) -> str:
      payload = f"{content}:{model}:{PROMPT_VERSION}".encode("utf-8")
      return hashlib.sha256(payload).hexdigest()

  def init_cache() -> sqlite3.Connection:
      CACHE_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
      conn = sqlite3.connect(str(CACHE_DB_PATH))
      conn.execute("""
          CREATE TABLE IF NOT EXISTS translation_cache (
              content_hash TEXT PRIMARY KEY,
              translated_content TEXT NOT NULL,
              model_used TEXT NOT NULL,
              prompt_version TEXT NOT NULL,
              created_at REAL NOT NULL
          )
      """)
      conn.commit()
      return conn
  ```

#### Passo A1.2: Implementação de `detect_language()` (stopword heuristic)
- **Arquivos Afetados:** [translate_catalog_nim.py](file:///home/loupan/.gemini/config/skills/.github/scripts/translate_catalog_nim.py)
- **Lógica:** Contagem de stopwords PT vs EN com fator de confiança `1.5`.

#### Passo A1.3: Implementação de `call_nvidia_nim()` com cascata
- **Cascata de Tradução:** `nvidia/riva-translate-4b-instruct-v2` → `nvidia/nemotron-3.5-lightning-30b-a3b` → `meta/llama-3.1-8b-instruct`.
- **HTTP:** `urllib.request` com `Authorization: Bearer {NVIDIA_API_KEY}`.

#### Passo A1.4: `protect_syntax()`/`restore_syntax()`
- Extrai blocos de código, frontmatter e tags XML; substitui por placeholders; restaura após tradução.

#### Passo A1.5: `extract_docstrings_and_comments()`
- **Para `.py`:** docstrings de módulos, classes e funções + comentários `#` informativos.
- **Para `.sh/.bash`:** comentários de cabeçalho explicativos + mensagens `--help`.
- **Para `.js/.ts`:** blocos JSDoc `/** ... */` + comentários `//` informativos.
- **Invariante de Proteção Semântica:** Comentários com diretivas de máquina (`# parent_skill_id:`, `# type:`, `# pragma:`, `# noqa:`, `# pylint:`, `# isort:`) e flags CLI são marcados como protegidos e NUNCA traduzidos.

#### Passo A1.6: Validação estática
- `validate_python_ast()` via `ast.parse`.
- `validate_shell_syntax()` via `bash -n`.

#### Passo A1.7: `call_nim_code_judge()`
- **Cascata de Judge:** `deepseek-ai/deepseek-v4-flash-0731` → `meta/llama-3.3-70b-instruct` → `meta/llama-3.1-8b-instruct`.
- Saída JSON `{"valid": bool, "reason": str}`.

#### Passo A1.8: `validate_translation()` (estágio unificado)
- Estágio A (AST/bash) + Estágio B (NIM Judge).

#### Passo A1.9: `process_file()` e `main()`
- Descobre arquivos `.md`, `.py`, `.sh`, `.bash`, `.js`, `.ts` em `SKILLS_DIR`.

#### Passo A1.10: Suíte de testes unitários offline
- **Arquivos Afetados:** [.github/scripts/tests/test_catalog_translation.py](file:///home/loupan/.gemini/config/skills/.github/scripts/tests/test_catalog_translation.py)
- **Cobertura:**
  - `detect_language()` com stopwords em PT e EN.
  - `protect_syntax()` e `restore_syntax()` para code blocks, frontmatter e tags XML.
  - `validate_python_ast()` para validação de AST sem quebra de indentação/sintaxe.
  - `validate_shell_syntax()` com `bash -n`.
  - `init_cache()` e operações CRUD do SQLite `translation_cache.sqlite3`.

---

### Fase B: Execução, Auditoria e Re-indexação

#### Passo B1.1: Executar tradução
```bash
python3 .github/scripts/translate_catalog_nim.py
```

#### Passo B1.2: Auditoria estrutural
```bash
python3 .github/scripts/audit_engine.py
```

#### Passo B1.3: Re-ingestão RAG
```bash
python3 .github/scripts/skills_rag_indexer.py --force
```

#### Passo B1.4: Suíte completa de testes (7 arquivos)
```bash
python3 .github/scripts/tests/test_catalog_translation.py && \
python3 .github/scripts/tests/test_mcp_inspect.py && \
python3 .github/scripts/tests/test_rag_hierarchical.py && \
python3 .github/scripts/tests/test_mcp_telemetry.py && \
python3 .github/scripts/tests/test_mcp_bootstrap.py && \
python3 .github/scripts/tests/test_rag_federated.py && \
python3 .github/scripts/tests/test_rag_quad_sota.py
```

---

### Fase C: Governança e Fechamento

#### Passo C1.1: Gerar `ADR-026-ER.md`
- Consolidar métricas de compressão BPE (comparativo de contagem de tokens pré vs pós tradução utilizando o tokenizer de referência downstream Llama-3 / tiktoken cl100k_base).
- Consolidar taxa de tradução, cache hit rate e relatório de integridade forense do Code Judge.

#### Passo C1.2: Arquivar Decision Set
```bash
mv docs/adr/ADR-026.md docs/adr/ADR-026-BP.md docs/adr/ADR-026-TODO.md docs/adr/ADR-026-PI.md docs/adr/archive/
```

#### Passo C1.3: Atualizar `ADR-INDEX.md`
- Marcar `CONSOLIDADA | ARCHIVED_OK`.

#### Passo C1.4: Reconciliar 6 pilares documentais
- `README.md`, `CHANGELOG.md`, `USAGE.md`, `RELEASE-NOTES.md`, `STATE.md`, `AGENTS.md`.

#### Passo C1.5: Commit atômico + tag `v2.5.0`
```bash
git add .
git commit -m "feat(catalog): unificação em EN-US via NIM e consolidação da ADR-026"
git tag -a v2.5.0 -m "Release v2.5.0 - Catálogo Canônico Unificado em Inglês (EN-US)"
git push origin main --tags
```

---

## 4. Validação Contínua (Continuous Validation)

```bash
# 1. Tradução
python3 .github/scripts/translate_catalog_nim.py

# 2. Auditoria estrutural
python3 .github/scripts/audit_engine.py

# 3. Re-ingestão RAG
python3 .github/scripts/skills_rag_indexer.py --force

# 4. Suíte completa de testes (7 arquivos)
python3 .github/scripts/tests/test_catalog_translation.py && \
python3 .github/scripts/tests/test_mcp_inspect.py && \
python3 .github/scripts/tests/test_rag_hierarchical.py && \
python3 .github/scripts/tests/test_mcp_telemetry.py && \
python3 .github/scripts/tests/test_mcp_bootstrap.py && \
python3 .github/scripts/tests/test_rag_federated.py && \
python3 .github/scripts/tests/test_rag_quad_sota.py
```

---

## 5. Handoff para Fechamento

Após a conclusão da implementação e aprovação de todos os testes, o Decision Set será finalizado com a emissão de [docs/adr/ADR-026-ER.md](file:///home/loupan/.gemini/config/skills/docs/adr/ADR-026-ER.md) e arquivado pelo Janitor (`adr-archive`).

---

*Documento gerado em 2026-08-25. Referência: ADR-026.*