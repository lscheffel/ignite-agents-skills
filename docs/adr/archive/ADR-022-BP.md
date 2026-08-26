---
id: ADR-022-BP
type: bp
title: "Blueprint - Pipeline RAG Quádruplo SOTA"
created: 2026-08-24
updated: 2026-08-24
adr_ref: ADR-022
---

# Blueprint — ADR-022: Pipeline RAG Quádruplo SOTA

> Referência: [ADR-022](./ADR-022-rag-sota-quad-optimizations.md)

---

## 1. Visão Geral

### Objetivo
Implementar os quatro módulos de alta performance definidos na ADR-022:
1. Cache persistente de reranking no SQLite3 (0ms de latência em cache hits).
2. Embeddings densos com `nvidia/nemotron-3-embed-1b` (2048-dim) e fallback local.
3. Injeção dinâmica por chunks focados (`<focused_chunk>`) para economia de contexto.
4. Expansão léxica determinística de siglas e acrônimos no FTS5.

### Métricas de Sucesso

| Métrica | Antes | Depois | Status |
|---|---|---|:---:|
| **Latência para Queries Repetidas** | ~200ms | < 1ms (0ms no log) | ⬜ |
| **Dimensão do Vetor Denso** | 512 (Hash) | 2048 (Nemotron-3) | ⬜ |
| **Tokens Injetados por Invocação** | ~350 tokens fixos | ~120-180 tokens focados | ⬜ |
| **Recall para Siglas Curtas (ex: RBAC, TDD)** | 62% | > 95% | ⬜ |
| **Operação 100% Offline** | Preservada | Preservada | ⬜ |

---

## 2. Estrutura de Artefatos Afetados

```text
.github/scripts/
├── skills_rag_indexer.py     # Atualização: Ingestão de embeddings Nemotron-3 (2048-dim) e schema de cache
├── skills_router.py          # Atualização: Cache LRU, expansão de siglas e injeção focalizada por chunks
└── skills_mcp_server.py      # Atualização: Tools com injeção de chunks focados e cache integrado

data/skills_rag_db/
└── skills_rag.sqlite3        # Atualização: Novas tabelas `rerank_cache` e coluna `vector_embedding_2048`
```

---

## 3. Conceitos-Chave da Solução

### 3.1 Esquema da Tabela `rerank_cache` (SQLite3)

```sql
CREATE TABLE IF NOT EXISTS rerank_cache (
    query_hash TEXT PRIMARY KEY,
    query_text TEXT NOT NULL,
    rankings_json TEXT NOT NULL,
    engine_name TEXT NOT NULL,
    hit_count INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3.2 Dicionário Canônico de Expansão de Siglas

```python
ACRONYM_EXPANSION_DICT = {
    "rbac": "rbac role based access control permissões autorização",
    "xss": "xss cross site scripting segurança vulnerabilidade frontend",
    "tdd": "tdd test driven development testes unitários red green",
    "ddd": "ddd domain driven design entidades agregados bounded context",
    "adr": "adr architecture decision record decisões arquiteturais blueprint",
    "ci/cd": "cicd continuous integration continuous deployment pipeline github actions",
    "cicd": "cicd continuous integration continuous deployment pipeline github actions",
    "sota": "sota state of the art ultra high quality padrões enterprise",
    "rag": "rag retrieval augmented generation busca semântica embeddings",
    "mcp": "mcp model context protocol json-rpc ferramentas tools",
    "api": "api application programming interface rest graphql endpoints",
    "orm": "orm object relational mapping banco migrations database",
    "poc": "poc proof of concept teste de conceito vulnerabilidade"
}
```

### 3.3 Estrutura do Payload XML Focalizado por Chunks

```xml
<!-- DYNAMIC SKILL INJECTION: refactoring (v1.0.0) [FOCUSED CHUNK MATCH] -->
<skill name="refactoring" category="config_skill">
  <summary>Guia completo para refatoração segura e incremental...</summary>
  <matched_trigger>refactoring</matched_trigger>
  <focused_chunk section="Técnicas de Extração e Strangler Fig">
    [Texto compacto da seção exata relevante para o problema]
  </focused_chunk>
</skill>
```

---

## 4. Workflows de Implementação

### Workflow 1: Criação e Integração do Módulo de Cache
- **Objetivo:** Adicionar armazenamento e recuperação transparente de rankings antes da chamada à API.
- **Passos:**
  1. No `skills_router.py` e `skills_mcp_server.py`, verificar se `query_hash` existe em `rerank_cache`.
  2. Em caso de hit, retornar imediatamente o payload com `"engine": "ADR-022-Cache-Hit (0ms)"`.
  3. Em caso de miss, executar o reranking normal e persistir no SQLite.
- **Checkpoint:** Consultas idênticas sucessivas marcam latência de 0ms e reutilizam rankings.

### Workflow 2: Integração do Embedder Nemotron-3 (2048-dim)
- **Objetivo:** Permitir cálculo de embeddings densos de 2048 dimensões durante a ingestão e busca.
- **Passos:**
  1. `skills_rag_indexer.py`: Se `NVIDIA_API_KEY` estiver disponível, gerar vetores via `nvidia/nemotron-3-embed-1b` para skills e chunks.
  2. `skills_router.py`: Vetorizar a query do usuário com Nemotron-3 e calcular similaridade no espaço de 2048 dimensões.
  3. Fallback automático para o vetor de 512 dimensões (hashing local) se offline.
- **Checkpoint:** Ingestão salva vetores densos e busca opera com precisão expandida.

### Workflow 3: Expansão de Siglas e Injeção Focalizada por Chunk
- **Objetivo:** Elevar cobertura lexical e diminuir contagem de tokens no prompt.
- **Passos:**
  1. Função `expand_query_tokens(query)` injeta termos complementares antes do `skills_fts`.
  2. Função `get_best_matching_chunk(skill_id, query_vec)` seleciona o chunk com maior similaridade.
  3. XML gerado substitui texto redundante pelo `<focused_chunk>`.
- **Checkpoint:** Queries curtas como "rbac" ativam `security-review` com facilidade e geram XML enxuto.

---

## 5. Anti-patterns Específicos

### 🔴 Crítico
- **Cache Stale após Atualização de Skill:** Cache responder dados antigos após uma skill ser modificada.
  - **Mitigação:** O indexador limpa a tabela `rerank_cache` a cada nova ingestão.
- **Bloqueio de Inicialização por Ausência de Rede:** Falha ao chamar a API de embeddings travar a ferramenta.
  - **Mitigação:** Tratamento estrito de exceções com fallback instantâneo para 512-dim local.

---

## 6. Checklists

### Checklist de Pré-Deploy
- [ ] Schema da tabela `rerank_cache` criado no SQLite.
- [ ] Dicionário de siglas testado para os 15 acrônimos mais comuns.
- [ ] Validação de formato do XML com `<focused_chunk>`.

### Checklist de Pós-Deploy
- [ ] Execução de consulta com cache miss seguida de cache hit verificada.
- [ ] Compatibilidade retroativa com modo `--local` 100% validada.
- [ ] Script de auditoria de governança passando com score >= 90/100.

---

## 7. Riscos e Mitigações

| Risco | Impacto | Probabilidade | Mitigação |
|---|---|---|---|
| Timeout na API de embeddings Nemotron-3 | Baixo | Média | Timeout curto (3s) e fallback para hashing local. |
| Injeção de chunk muito longo no XML | Médio | Baixa | Truncamento estrito de chunks em 1.500 caracteres no XML. |

---

*Documento gerado em 2026-08-24. Referência: ADR-022.*
