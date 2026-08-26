---
id: ADR-026-BP
type: bp
title: "Blueprint - Catálogo Canônico Unificado em Inglês (EN-US) via NVIDIA NIM"
created: "2026-08-25"
updated: "2026-08-25"
adr_ref: ADR-026
---

# Blueprint — ADR-026: Catálogo Canônico Unificado em Inglês (EN-US) via NVIDIA NIM

> Referência: [ADR-026](./ADR-026.md)

---

## 1. Visão Geral

### Objetivo
Padronizar o catálogo canônico de skills para EN-US via NVIDIA NIM (`nvidia/riva-translate-4b-instruct-v2`), com pipeline autônomo de tradução, preservação estrita de sintaxe (código, frontmatter, XML, `parent_skill_id`) e validação forense em dois estágios (AST estático + NIM Code Judge), maximizando compressão BPE e alinhamento semântico no Reranker Neural.

### Métricas de Sucesso

| Métrica | Antes (PT-BR) | Depois (EN-US) | Status |
|---|:---:|:---:|:---:|
| **Tokens por Documento (BPE Llama/cl100k)** | `X` | `< X` (compressão média estimada ~15-25%) | ⬜ |
| **Precisão do Reranker em Consultas EN-US** | Base | Melhorada (alinhamento Cross-Encoder) | ⬜ |
| **Uniformidade Linguística do Catálogo** | Mista (PT/EN) | 100% EN-US | ⬜ |
| **Sintaxe/Identificadores Intactos** | — | 100% (AST + Code Judge) | ⬜ |
| **Suíte de Testes Automatizados** | 6 suítes | 7 suítes (6 regressão + 1 nova suíte unitária offline) | ⬜ |

---

## 2. Estrutura de Artefatos Afetados

```text
.github/scripts/
├── translate_catalog_nim.py             # Pipeline autônomo de tradução EN-US via NIM
├── audit_engine.py                      # Auditoria estrutural de sub-ativos (pós-tradução)
├── skills_rag_indexer.py                # Re-ingestão da base vetorial após tradução
├── skills_mcp_server.py                 # Consultas RAG sobre o catálogo traduzido
└── tests/
    └── test_catalog_translation.py      # Testes unitários offline do módulo de tradução e sintaxe

.local/skills_rag/
└── translation_cache.sqlite3            # Cache de idempotência versionado (SHA256)

docs/adr/
├── ADR-026.md                           # Decisão arquitetural
├── ADR-026-BP.md                        # Blueprint (este documento)
├── ADR-026-TODO.md                      # Checklist operacional
├── ADR-026-PI.md                        # Plano de injeção e rollback
└── ADR-026-ER.md                        # Evidence Record (pós-execução)
```

---

## 3. Conceitos-Chave da Solução

### 3.1 Cascata de Modelos com Tolerância a Falhas
- **Tradução:** `nvidia/riva-translate-4b-instruct-v2` → `nvidia/nemotron-3.5-lightning-30b-a3b` → `meta/llama-3.1-8b-instruct`.
- **Code Judge:** `deepseek-ai/deepseek-v4-flash-0731` → `meta/llama-3.3-70b-instruct` → `meta/llama-3.1-8b-instruct`.
- `temperature=0.0` (determinística) + fallback automático.

### 3.2 Preservação Estrita de Sintaxe
- Extração de blocos de código (` ``` `), frontmatter e tags XML → placeholders → tradução → restauração.
- Isolamento de código procedural de scripts; tradução apenas de docstrings/comentários.
- Comentários diretivos e metadados protegidos (`# parent_skill_id:`, `# type:`, etc.) são mantidos inalterados.

### 3.3 Validação Forense em Dois Estágios
- **Estágio A (estático):** `ast.parse()` (Python) e `bash -n` (Shell).
- **Estágio B (NIM Code Judge):** Comparação original vs traduzido, saída JSON, verificação de identificadores/indentação.

### 3.4 Idempotência via Cache Versionado & Metodologia BPE
- `translation_cache.sqlite3` chaveado por `SHA256(content + ":" + model_name + ":" + prompt_version)` para prevenir re-tradução desnecessária e garantir invalidação em caso de atualização de modelo ou prompt.
- Medição BPE calculada comparando a contagem de tokens pré e pós-tradução via tokenizer padrão Llama-3 / cl100k_base.

---

## 4. Workflows de Implementação

### Workflow 1: Criação do Script de Tradução e Testes Unitários
1. **Passo 1.1:** Implementar `init_cache()`, `detect_language()`, `extract_translatable_segments()`.
2. **Passo 1.2:** Implementar `call_nvidia_nim()` com cascata de fallback.
3. **Passo 1.3:** Implementar `protect_syntax()`/`restore_syntax()` e `extract_docstrings_and_comments()`.
4. **Passo 1.4:** Implementar `validate_python_ast()`, `validate_shell_syntax()`, `call_nim_code_judge()`, `validate_translation()`.
5. **Passo 1.5:** Implementar `process_file()` e `main()`.
6. **Passo 1.6:** Implementar suíte de testes unitários offline `.github/scripts/tests/test_catalog_translation.py`.
7. **Checkpoint:** `python3 .github/scripts/tests/test_catalog_translation.py` executa e passa 100% dos testes offline.

### Workflow 2: Execução, Auditoria e Re-indexação
1. **Passo 2.1:** Executar tradução (`translate_catalog_nim.py`).
2. **Passo 2.2:** Executar `audit_engine.py` — validar 100% conformidade estrutural.
3. **Passo 2.3:** Executar `skills_rag_indexer.py --force` — re-ingestão vetorial.
4. **Passo 2.4:** Executar 7 suítes completas de testes automatizados.
5. **Checkpoint:** 100% dos testes passando e auditoria 100% conforme.

### Workflow 3: Governança e Fechamento
1. **Passo 3.1:** Gerar `ADR-026-ER.md` com métricas de compressão BPE.
2. **Passo 3.2:** Arquivar Decision Set em `docs/adr/archive/`.
3. **Passo 3.3:** Atualizar `ADR-INDEX.md` para `CONSOLIDADA | ARCHIVED_OK`.
4. **Passo 3.4:** Reconciliar 6 pilares documentais.
5. **Checkpoint:** Tag `v2.5.0` criada e commit atômico.

---

## 5. Anti-patterns Específicos desta Decisão

### 🔴 Crítico
#### Tradução de Identificadores e Código Procedural
- **O que é:** Traduzir nomes de variáveis, funções, `parent_skill_id`, chaves de frontmatter ou código procedural.
- **Por que é ruim:** Quebra compatibilidade com SQLite, MCP, AssetParser e o roteamento semântico.
- **Como evitar:** Regex extract/restore + validação forense (AST + NIM Code Judge) com auto-rollback.

### 🟡 Médio
#### Dependência de `langdetect` externo
- **O que é:** Usar biblioteca externa para detecção de idioma.
- **Por que é ruim:** Quebra ambientes sem pip/internet (stdlib-only).
- **Como evitar:** Heurística de stopwords PT/EN embutida.

---

## 6. Checklists

### Checklist de Pré-Deploy
- [ ] Cascata de modelos de tradução e judge configurada e verificada
- [ ] `protect_syntax`/`restore_syntax` testado com `.md`, `.py`, `.sh`
- [ ] Validação AST (`ast.parse`) e `bash -n` funcionando
- [ ] NIM Code Judge retornando JSON `{"valid": bool}`
- [ ] Testes unitários offline `test_catalog_translation.py` passando 100%

### Checklist de Pós-Deploy
- [ ] Tradução executada sem erros (cache populado)
- [ ] `audit_engine.py` 100% conformidade
- [ ] 7 suítes completas de testes passando (6 regressão + 1 unitária)
- [ ] `ADR-026-ER.md` gerado com métricas BPE
- [ ] `ADR-026-ER.md` gerado com métricas BPE

---

## 7. Edge Cases

### Arquivo Já em Inglês
- **Situação:** `.md` já em EN-US.
- **Solução:** `detect_language()` retorna `en` → skip (não gasta API call).

### Script sem Docstring
- **Situação:** `.py` sem docstring.
- **Solução:** Extração de comentários `#` de cabeçalho; se ausentes, skip sem tradução.

### Modelo NIM Indisponível
- **Situação:** Riva fora do ar.
- **Solução:** Cascata de fallback; se todos falharem, manter original (não corromper).

---

## 8. Skills Relacionadas

| Skill | Relação com este Blueprint |
|---|---|
| `adr-generator` | Governança da Quadra SOTA e decisões arquiteturais |
| `implementation` | Execução governada dos workflows e DAG de tarefas |
| `technical-documentation` | Reconciliação dos 6 pilares documentais |
| `testing-mastery` | Estratégia de testes unitários e validação contínua |

---

*Documento gerado em 2026-08-25. Referência: ADR-026.*