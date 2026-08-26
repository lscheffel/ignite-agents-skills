---
id: ADR-025-BP
type: bp
title: "Blueprint - Ingestão Hierárquica Multi-Asset de Skills (Skill Bundles)"
created: "2026-08-24"
updated: "2026-08-24"
adr_ref: ADR-025
---

# Blueprint — ADR-025: Ingestão Hierárquica Multi-Asset de Skills (Skill Bundles)

> Referência: [ADR-025](./ADR-025-hierarchical-multi-asset-ingestion.md)

---

## 1. Visão Geral

### Objetivo
Capacitar o pipeline RAG a indexar, vetorizar e recuperar artefatos complementares (`references/`, `templates/` e `scripts/`) associados a cada skill sem poluir o catálogo principal, aplicando tipagem semântica (`asset_type`), vínculo de linhagem (`parent_skill_id`) e damping ponderado no Cross-Encoder.

### Métricas de Sucesso

| Métrica | Antes (ADR-024) | Depois (ADR-025) | Status |
|---|:---:|:---:|:---:|
| **Tipos de Artefatos Ingeridos** | 2 (`root`, `references`) | 4 (`root`, `references`, `templates`, `scripts`) | ⬜ |
| **Precisão de Intenção em Templates** | Indireta (via busca genérica) | Direta (Damping ponderado + Reranker) | ⬜ |
| **Ruído Vetorial em Scripts/Código** | 100% (se indexado bruto) | 0% (Extração estrita de docstrings/help) | ⬜ |
| **Rastreabilidade de Linhagem** | Nula | 100% (`parent_skill_id` e `file_path`) | ⬜ |
| **Suíte de Testes Automatizados** | 17 testes | 21+ testes (+ `test_rag_hierarchical.py`) | ⬜ |

---

## 2. Estrutura de Artefatos Afetados

```text
.github/scripts/
├── skills_rag_indexer.py                  # Extrator multi-asset, parser seletivo e migração DDL
├── skills_mcp_server.py                   # Suporte a asset_type, parent linking e XML tipado
├── skills_router.py                       # CLI flags (--asset-type), damping factor e formatação
└── tests/
    └── test_rag_hierarchical.py           # Nova suíte de testes unitários para hierarquia multi-asset

docs/adr/
├── ADR-025-hierarchical-multi-asset-ingestion.md
├── ADR-025-BP.md
├── ADR-025-TODO.md
└── ADR-025-PI.md
```

---

## 3. Conceitos-Chave da Solução

### 3.1 Skill Bundle (Pacote Hierárquico Coeso)
Cada skill deixa de ser um documento markdown isolado e passa a ser tratada como um bundle coeso estruturado em 4 camadas funcionais:

```text
skills/database-architecture/
├── SKILL.md                              <- asset_type: "skill_root" (Peso: 1.00)
├── references/
│   └── patterns-and-migrations.md        <- asset_type: "reference"  (Peso: 0.85)
├── templates/
│   └── migration-template.sql            <- asset_type: "template"   (Peso: 0.80)
└── scripts/
    └── generate_erd.py                   <- asset_type: "script_doc" (Peso: 0.75)
```

### 3.2 Parser Seletivo de Scripts & Templates (Noise Reduction Engine)
Evita a vetorização de variáveis, loops e código procedural descartável:
- **Scripts Python (`.py`):** Extrai a docstring do módulo (`"""..."""`), comentários de cabeçalho (`#`), assinaturas de funções principais e blocos `argparse` / `USAGE`.
- **Scripts Shell (`.sh`, `.bash`):** Extrai blocos de comentários iniciais e seções de ajuda `--help`.
- **Templates de Código (`.sql`, `.json`, `.yaml`):** Extrai cabeçalhos de metadados e a estrutura esquelética das tabelas/chaves.

### 3.3 Damping Multiplicativo por Tipo de Ativo
Multiplicadores aplicados no cálculo do score preliminar antes do Cross-Encoder:
$$\text{Score}_{\text{final}} = \text{Score}_{\text{híbrido}} \times \text{Damping}(\text{asset\_type})$$

- `skill_root`: $1.00$
- `reference`: $0.85$
- `template`: $0.80$
- `script_doc`: $0.75$

---

## 4. Workflows de Implementação

### Workflow 1: Migração do Esquema SQLite & Indexador Multi-Asset
1. **Passo 1.1:** Atualizar DDL em `skills_rag_indexer.py` adicionando colunas `asset_type`, `parent_skill_id` e `file_path` em `skill_chunks`.
2. **Passo 1.2:** Implementar `AssetParser` com lógica especializada para Markdown, Python/Shell scripts e templates estruturados.
3. **Passo 1.3:** Implementar varredura recursiva de `references/`, `templates/` e `scripts/` durante a ingestão do Skill Bundle.
4. **Checkpoint:** `python3 .github/scripts/skills_rag_indexer.py` indexa com sucesso todas as 4 camadas sem erros.

### Workflow 2: Roteamento Ponderado & Servidor MCP
1. **Passo 2.1:** Atualizar `skills_mcp_server.py` e `skills_router.py` para consultar `asset_type`, `parent_skill_id` e `file_path`.
2. **Passo 2.2:** Aplicar o fator de Damping ponderado na ordenação pré-neural.
3. **Passo 2.3:** Atualizar serializador XML para renderizar tags com `type="..."`, `parent="..."` e `path="..."`.
4. **Checkpoint:** Chamadas a `search_skills` e `route_task` retornam payloads tipados corretamente.

---

## 5. Anti-patterns Específicos desta Decisão

### 🔴 Crítico
#### Indexação Cega de Código Executável (Raw Code Ingestion)
- **O que é:** Vetorizar o código fonte completo de scripts linha a linha.
- **Por que é ruim:** Polui os embeddings com palavras-chave de linguagem (`for`, `while`, `import`, `return`), degradando a similaridade semântica.
- **Como evitar:** Aplicar o `AssetParser` estrito que retém apenas docstrings e documentação de uso.

### 🟡 Médio
#### Proliferação de IDs sem Parent Link
- **O que é:** Indexar templates e referências sem salvar `parent_skill_id`.
- **Por que é ruim:** Impossibilita saber a qual skill um template pertence quando carregado isoladamente.
- **Como evitar:** Invariante estrita de `parent_skill_id = root_skill_id`.

---

## 6. Checklists

### Checklist de Pré-Deploy
- [ ] Colunas `asset_type`, `parent_skill_id` e `file_path` presentes em `skill_chunks`
- [ ] Parser seletivo de docstrings testado com `.py`, `.sh`, `.sql`, `.json`, `.yaml`
- [ ] Damping factor calibrado (1.00, 0.85, 0.80, 0.75)
- [ ] Nova suíte `test_rag_hierarchical.py` criada e passando 100%

### Checklist de Pós-Deploy
- [ ] Re-indexação completa executada (`skills_rag_indexer.py`)
- [ ] Todas as 5 suítes de testes executando e passando em < 1.0s
- [ ] Reconciliação dos 6 pilares canônicos de documentação

---

## 7. Edge Cases

### Script sem Docstring / Comentários
- **Situação:** Script `scripts/util.sh` sem comentários de cabeçalho.
- **Solução:** O `AssetParser` gera uma descrição sintetizada baseada no nome do arquivo e no `description` da skill-mãe.

### Template JSON com Sintaxe Inválida / Chaves Complexas
- **Situação:** Template JSON contendo tags Jinja2 (`{{ ... }}`).
- **Solução:** Parser em modo texto tolerante com extração de chaves principais via regex.

---

## 8. Skills Relacionadas

| Skill | Relação com este Blueprint |
|---|---|
| `adr-generator` | Governança da Quadra SOTA e decisões arquiteturais |
| `implementation` | Execução governada dos workflows e DAG de tarefas |
| `technical-documentation` | Reconciliação dos 6 pilares documentais |
| `testing-mastery` | Estratégia de testes unitários e validação contínua |

---

*Documento gerado em 2026-08-24. Referência: ADR-025.*
