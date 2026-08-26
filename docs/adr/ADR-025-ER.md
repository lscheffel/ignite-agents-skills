---
id: ADR-025-ER
type: er
title: "Evidence Record - ADR-025: Ingestão Hierárquica Multi-Asset de Skills (Skill Bundles: Root, References, Templates e Scripts com Parent Linking e Damping Ponderado)"
created: 2026-08-24
updated: 2026-08-24
adr_ref: ADR-025
implementation_status: CONSOLIDADA
tasks_completed: 17/17
completion_rate: 100%
verification_gate: PASSED
---

# Evidence Record — ADR-025: Ingestão Hierárquica Multi-Asset de Skills (Skill Bundles: Root, References, Templates e Scripts com Parent Linking e Damping Ponderado)

> **Documento de Evidência e Certificação Algorítmica de Conclusão**  
> Gerado automaticamente pelo Gatekeeper Janitor (`adr-archive / audit.py`).  
> Este artefato constitui a prova imutável e verificável de que o Decision Set da `ADR-025` foi 100% implementado e auditado.

---

## 1. Metadados de Execução e Certificação

| Campo | Valor |
|---|---|
| **ADR Referência** | [`ADR-025`](./ADR-025.md) |
| **Título da Decisão** | Ingestão Hierárquica Multi-Asset de Skills (Skill Bundles: Root, References, Templates e Scripts com Parent Linking e Damping Ponderado) |
| **Data de Início (Planejamento)** | 2026-08-24 |
| **Data de Conclusão (Auditoria)** | 2026-08-24 |
| **Taxa de Conclusão de Tarefas** | **100%** (17/17 tarefas concluídas) |
| **Branch Git** | `main` |
| **Commit SHA de Validação** | `38dacad` |
| **Gatekeeper Algorítmico** | `audit.py` (Janitor SOTA Engine) |
| **Status Final de Governança** | `CONSOLIDADA` ✅ |

---

## 2. Contexto Arquitetural & Decisão Implementada

### Diagnóstico e Motivação
Após a consolidação da [ADR-024](./archive/ADR-024-rice-optimizations-telemetry.md), que estabeleceu o isolamento de catálogos extensos em diretórios `references/` (Lazy Loading) e otimizou o consumo de tokens de System Prompt, o ecossistema canônico de skills evoluiu para uma arquitetura onde cada skill opera como um **pacote coeso (*Skill Bundle*)**.

Além do arquivo mestre `SKILL.md`, uma skill moderna pode conter múltiplos tipos de ativos complementares:
1. `references/`: Catálogos aprofundados, matrizes de decisão e documentações auxiliares.
2. `templates/`: Esqueletos estruturais (`*.sql`, `*.json`, `*.yaml`, `*.md`, etc.) para scaffolding instantâneo.
3. `scripts/`: Utilitários executáveis e scripts de automação (`*.py`, `*.sh`, `*.js`).

### Solução Arquitetural Efetivada
Implementar a **Arquitetura de Ingestão Hierárquica Multi-Asset de Skills (*Skill Bundles*)** no pipeline de indexação ([skills_rag_indexer.py](file:///home/loupan/.gemini/config/skills/.github/scripts/skills_rag_indexer.py)), no motor de roteamento ([skills_router.py](file:///home/loupan/.gemini/config/skills/.github/scripts/skills_router.py)) e no servidor MCP ([skills_mcp_server.py](file:///home/loupan/.gemini/config/skills/.github/scripts/skills_mcp_server.py)).

---

## 3. Matriz Completa de Tarefas Concluídas

Abaixo estão listadas todas as tarefas verificadas e atestadas no checklist de execução:

| ID | Descrição da Tarefa | Status de Execução | Validação |
|---|---|:---:|:---:|
| `A1.1` | Adicionar colunas `asset_type`, `parent_skill_id` e `file_path` na tabela `skill_chunks` em `skills_rag_indexer.py` | ✅ Concluído | Aprovado no Gate |
| `A1.2` | Implementar a classe `AssetParser` com métodos para Markdown, Python/Shell (`extract_script_docstring`) e Templates (`extract_template_skeleton`) | ✅ Concluído | Aprovado no Gate |
| `A1.3` | Atualizar o método de varredura `scan_skill_directory` para processar recursivamente as pastas `references/`, `templates/` e `scripts/` associadas ao bundle | ✅ Concluído | Aprovado no Gate |
| `A1.4` | Executar re-indexação de teste e validar persistência das 4 camadas no banco SQLite `data/skills_rag_db/skills_rag.sqlite3` | ✅ Concluído | Aprovado no Gate |
| `B1.1` | Atualizar consultas SQL em `skills_mcp_server.py` para selecionar `asset_type`, `parent_skill_id` e `file_path` | ✅ Concluído | Aprovado no Gate |
| `B1.2` | Implementar o Damping Factor multiplicativo no scoring inicial (`skill_root: 1.0`, `reference: 0.85`, `template: 0.80`, `script_doc: 0.75`) | ✅ Concluído | Aprovado no Gate |
| `B1.3` | Atualizar serializador XML de chunks para emitir tags tipadas `<active_skill id="..." parent="..." type="..." path="...">` | ✅ Concluído | Aprovado no Gate |
| `B1.4` | Adicionar flag `--asset-type` (opcional) em `skills_router.py` para filtragem direcionada via CLI | ✅ Concluído | Aprovado no Gate |
| `C1.1` | Criar a suíte [.github/scripts/tests/test_rag_hierarchical.py](file:///home/loupan/.gemini/config/skills/.github/scripts/tests/test_rag_hierarchical.py) testando parser, parent linking, damping factor e XML serialization | ✅ Concluído | Aprovado no Gate |
| `C1.2` | Executar todas as 5 suítes de testes automatizados (`test_rag_hierarchical`, `test_mcp_telemetry`, `test_mcp_bootstrap`, `test_rag_federated`, `test_rag_quad_sota`) | ✅ Concluído | Aprovado no Gate |
| `C1.3` | Executar o motor forense `python3 .github/scripts/audit_engine.py` e validar integridade de 100% dos ativos | ✅ Concluído | Aprovado no Gate |
| `T01` | Tabela `skill_chunks` armazena `asset_type`, `parent_skill_id` e `file_path` | ✅ Concluído | Aprovado no Gate |
| `T02` | Chunks de scripts e templates extraídos com zero ruído de código procedural | ✅ Concluído | Aprovado no Gate |
| `T03` | Servidor MCP retorna chunks com atributos XML tipados | ✅ Concluído | Aprovado no Gate |
| `T04` | Intenção explícita de template/script promove o chunk secundário no reranker | ✅ Concluído | Aprovado no Gate |
| `T05` | 5/5 suítes de testes passando com 100% de sucesso | ✅ Concluído | Aprovado no Gate |
| `T06` | 81/81 ativos auditados com nota média $\ge 91.0 / 100$ | ✅ Concluído | Aprovado no Gate |

---

## 4. Verificação de Integridade e Validações Realizadas

| Dimensão de Validação | Método de Verificação | Veredito |
|---|---|:---:|
| **Conformidade de Escopo (DAG)** | Inspeção estrita contra TODO / PI | **PASSOU** ✅ |
| **Isolamento de Escopo** | Scope Isolation / Offloading para Registry | **PASSOU** ✅ |
| **Sincronização Documental** | Atualização de referências e status | **PASSOU** ✅ |
| **Rastreabilidade de Artefatos** | Decision Set completo (ADR, BP, TODO, PI) | **PASSOU** ✅ |

---

## 5. Gestão de Débitos Técnicos (Tech Debt Registry)

### Débitos Mitigados por esta ADR

- Nenhum débito pré-existente foi explicitamente vinculado a esta ADR.

### Débitos Incidentais Descarregados Durante a Execução

- Zero débitos secundários registrados durante o ciclo desta ADR.

---

## 6. Rastreabilidade e Arquivamento de Artefatos

Com a geração deste Evidence Record, os artefatos de trabalho da `ADR-025` foram promovidos e arquivados:

* **ADR Primária:** [`docs/adr/archive/ADR-025.md`](./archive/ADR-025.md)
* **Blueprint:** [`docs/adr/archive/ADR-025-BP.md`](./archive/ADR-025-BP.md)
* **Checklist TODO:** [`docs/adr/archive/ADR-025-TODO.md`](./archive/ADR-025-TODO.md)
* **Implementation Plan:** [`docs/adr/archive/ADR-025-PI.md`](./archive/ADR-025-PI.md)

---

## 7. Certificado Algorítmico de Fechamento

```text
[CERTIFICADO DE IMPLEMENTAÇÃO E GOVERNANÇA]
ADR: ADR-025
DATA: 2026-08-24
HASH DE VALIDAÇÃO: 22B5FEB941E33000
GATEKEEPER: adr-archive / audit.py v2.1.0
VEREDITO: DECISION SET CONSOLIDADO COM SUCESSO
```
