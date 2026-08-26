---
id: ADR-025
type: adr
title: "Ingestão Hierárquica Multi-Asset de Skills (Skill Bundles: Root, References, Templates e Scripts com Parent Linking e Damping Ponderado)"
created: "2026-08-24"
updated: "2026-08-24"
implementation_status: CONSOLIDADA
depends_on:
  - ADR-021
  - ADR-022
  - ADR-023
  - ADR-024
---

# ADR-025: Ingestão Hierárquica Multi-Asset de Skills (Skill Bundles: Root, References, Templates e Scripts com Parent Linking e Damping Ponderado)

## Status
Proposto (Aprovado para Implementação - Tier 2 Quadra SOTA)

---

## Contexto

Após a consolidação da [ADR-024](./archive/ADR-024-rice-optimizations-telemetry.md), que estabeleceu o isolamento de catálogos extensos em diretórios `references/` (Lazy Loading) e otimizou o consumo de tokens de System Prompt, o ecossistema canônico de skills evoluiu para uma arquitetura onde cada skill opera como um **pacote coeso (*Skill Bundle*)**.

Além do arquivo mestre `SKILL.md`, uma skill moderna pode conter múltiplos tipos de ativos complementares:
1. `references/`: Catálogos aprofundados, matrizes de decisão e documentações auxiliares.
2. `templates/`: Esqueletos estruturais (`*.sql`, `*.json`, `*.yaml`, `*.md`, etc.) para scaffolding instantâneo.
3. `scripts/`: Utilitários executáveis e scripts de automação (`*.py`, `*.sh`, `*.js`).

### Diagnóstico de Limitações Atuais

| Capacidade | Status Atual | Evidência / Lacuna |
|---|:---:|---|
| **Ingestão de Artefatos Secundários** | `PARCIAL` | O indexador atual indexa `references/`, mas ignora `templates/` e `scripts/`, ou exigiria indexação plana sem diferenciação semântica. |
| **Diferenciação por Natureza de Ativo (`asset_type`)** | `AUSENTE` | Não há metadado explícito diferenciando um `SKILL.md` (root), uma referência descritiva, um template de código ou um script utilitário. |
| **Linhagem e Parent Linking** | `AUSENTE` | Artefatos dentro de subpastas não possuem vínculo explícito com a skill-mãe (`parent_skill_id`), dificultando a agregação hierárquica. |
| **Filtragem de Ruído em Código Bruto** | `RISCO` | A indexação cega de scripts e templates linha a linha introduz ruído vetorial (variáveis, loops, boilerplate), degradando a precisão do Cross-Encoder. |
| **Calibração de Relevância por Intenção (Damping Factor)** | `AUSENTE` | Sem pesos calibrados, uma busca ampla por uma skill poderia ranquear um template específico acima do manual mestre `SKILL.md`. |

### Consequências da Lacuna
- Agentes autônomos não conseguem descobrir templates estruturados e scripts operacionais via busca semântica RAG sem poluir o catálogo principal.
- Degradação de precisão semântica quando arquivos de código bruto são vetorizados integralmente.
- Inexistência de um payload XML tipado no MCP que declare se o chunk injetado é uma instrução raiz, uma referência, um template ou um script de automação.

---

## Decisão

Implementar a **Arquitetura de Ingestão Hierárquica Multi-Asset de Skills (*Skill Bundles*)** no pipeline de indexação ([skills_rag_indexer.py](file:///home/loupan/.gemini/config/skills/.github/scripts/skills_rag_indexer.py)), no motor de roteamento ([skills_router.py](file:///home/loupan/.gemini/config/skills/.github/scripts/skills_router.py)) e no servidor MCP ([skills_mcp_server.py](file:///home/loupan/.gemini/config/skills/.github/scripts/skills_mcp_server.py)).

### Estrutura Canônica do Skill Bundle
Cada diretório de skill passa a ser processado como um pacote hierárquico tipado:

```text
skills/<skill-name>/
├── SKILL.md                              <- asset_type: "skill_root" (Peso: 1.00)
├── references/
│   └── *.md                              <- asset_type: "reference"  (Peso: 0.85)
├── templates/
│   └── *.{sql,json,yaml,md,j2}           <- asset_type: "template"   (Peso: 0.80)
└── scripts/
    └── *.{py,sh,js,ts}                   <- asset_type: "script_doc" (Peso: 0.75)
```

---

## 4 Invariantes Arquiteturais de Indexação & Execução

### 1. Namespace & Parent Skill ID (`parent_linking`)
Todo artefato secundário indexado herda o identificador canônico da skill-mãe:
- `skill_id`: `<parent-skill-id>:<asset-type>:<asset-name>` (ex: `database-architecture:template:migration-template`).
- `parent_skill_id`: `<parent-skill-id>` (ex: `database-architecture`).
- `asset_type`: `skill_root` | `reference` | `template` | `script_doc`.
- `file_path`: Caminho relativo dentro do bundle (ex: `templates/migration-template.sql`).

### 2. Extração Semântica Inteligente por Tipo de Arquivo
- **Documentação & Referências (`SKILL.md`, `references/*.md`, `templates/*.md`):** Chunking semântico estruturado respeitando cabeçalhos Markdown (`##`, `###`).
- **Scripts de Automação (`scripts/*.py`, `*.sh`):** Extração estrita de docstrings iniciais, blocos de comentários de cabeçalho, constantes de configuração e seções `--help` / `USAGE`. O corpo de código procedural (loops, condicionais, variáveis) é descartado na vetorização para evitar ruído vetorial.
- **Templates de Código (`templates/*.json`, `*.sql`, `*.yaml`, `*.j2`):** Extração de cabeçalhos comentados e do esqueleto estrutural (schemas DDL, chaves de contrato JSON/YAML).

### 3. Ponderação no Reranker (Damping Factor Ponderado)
Aplica multiplicadores multiplicativos calibrados sobre a pontuação de similaridade inicial:
- `skill_root`: Multiplicador `1.00` (prioridade máxima para intenções conceituais amplas).
- `reference`: Multiplicador `0.85` (promovido quando a consulta exige detalhamento ou catálogo).
- `template`: Multiplicador `0.80` (promovido quando a consulta expressa intenção explícita de template/código).
- `script_doc`: Multiplicador `0.75` (promovido quando a consulta busca automação ou execução de script).

### 4. Resolução Tipada no Servidor MCP (`skills-rag-mcp`)
Ao invocar `route_task`, `search_skills` ou `get_skill_details`, o payload XML emitido passa a carregar os atributos tipados:

```xml
<active_skill id="database-architecture" parent="database-architecture" type="template" path="templates/migration-template.sql" confidence="92.5%">
  <!-- Conteúdo semântico do Template ou Chunk -->
</active_skill>
```

---

## Esquema do Banco SQLite (`skills_chunks` e `skills`)

Colunas adicionadas à tabela `skill_chunks`:
- `asset_type TEXT DEFAULT 'skill_root'` (`skill_root` | `reference` | `template` | `script_doc`)
- `parent_skill_id TEXT` (chave para linhagem e agregação multi-asset)
- `file_path TEXT` (caminho relativo do arquivo no bundle da skill)

---

## Alternativas Consideradas

### Alternativa A: Indexação Plana de Todos os Arquivos como Skills Independentes
- **Prós**: Implementação trivial sem alteração de schema.
- **Contras**: Poluição severa do catálogo mestre de skills; um template SQL competiria de igual para igual com o `SKILL.md`, degradando a precisão semântica do Reranker Neural.

### Alternativa B: RAG Isolado em Segundo Banco de Dados para Templates e Scripts
- **Prós**: Isolamento total do catálogo de skills.
- **Contras**: Complexidade operacional excessiva com múltiplos bancos SQLite, impossibilidade de fusão ponderada em consulta única e alto consumo de memória.

### Alternativa C: Hierarquia Tipada Multi-Asset com Parent Linking e Damping Factor (Escolhida)
- **Prós**: Mantém Single Source of Truth no mesmo banco SQLite; preserva 100% da acurácia de `SKILL.md` para buscas gerais; permite recuperação cirúrgica de templates e scripts sob demanda; token economy rigorosa.
- **Contras**: Exige enriquecimento do parser no indexador e recalibração dos scorers no roteador/MCP.

---

## Consequências

### Positivas
- **Acesso Direto a Modelos Operacionais:** Agentes podem requisitar e receber esqueletos de código e scripts utilitários em 0ms.
- **Zero Poluição Vetorial:** Extração semântica limpa ignora ruídos de sintaxe procedural de scripts.
- **Transparência de Linhagem:** Rastreamento total entre qualquer asset secundário e sua respectiva skill-mãe.
- **Compatibilidade Retroativa:** Skills que possuem apenas `SKILL.md` continuam operando com `asset_type = 'skill_root'` e peso `1.00`.

### Negativas / Riscos
- **Risco**: Indexação de scripts em linguagens não mapeadas.
  - **Mitigação**: Fallback parser com extração de comentários padrão (`#`, `//`, `/* */`, `--`).

---

## Referências
- [ADR-021: Arquitetura Tri-Stage com Neural Cross-Encoder Reranking](./archive/ADR-021-dual-engine-neural-rerank.md)
- [ADR-022: Pipeline RAG Quádruplo SOTA](./archive/ADR-022-sota-quad-optimizations.md)
- [ADR-023: Arquitetura de RAG Federado Multi-Escopo](./archive/ADR-023-federated-multi-agent-rag.md)
- [ADR-024: Otimização de Context Budget via Lazy Loading](./archive/ADR-024-rice-optimizations-telemetry.md)
- Evidence Record: (pendente — a ser gerado após validação de testes)
