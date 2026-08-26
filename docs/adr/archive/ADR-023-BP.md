---
id: ADR-023-BP
type: bp
title: "Blueprint - Arquitetura de RAG Federado Multi-Escopo & Multi-Agente"
created: 2026-08-24
updated: 2026-08-24
adr_ref: ADR-023
---

# Blueprint — ADR-023: Arquitetura de RAG Federado Multi-Escopo & Multi-Agente

> Referência: [ADR-023](./ADR-023-federated-multi-scope-rag.md)

---

## 1. Visão Geral

### Objetivo
Habilitar descoberta multi-agente e recuperação unificada de skills em múltiplos escopos:
1. **Escopo Global:** Catálogo canônico (`~/.gemini/config/skills/data/skills_rag_db/skills_rag.sqlite3`).
2. **Escopo Workspace Local (Multi-Agent):** Descoberta automática de diretórios de skills de ferramentas como Gemini CLI, Kilocode, Claude Code, Cursor, Windsurf e auto-indexação em `<workspace>/.local/skills_rag/skills_rag.sqlite3`.

### Métricas de Sucesso

| Métrica | Antes | Depois | Status |
|---|---|---|:---:|
| **Suporte a Diretórios Multi-Agente** | Apenas `.gemini` | 12 convenções canônicas | ⬜ |
| **Auto-Indexação Local sob Demanda** | Manual | Automática (com base em mtime) | ⬜ |
| **Mutação no Banco Global em Consultas Locais** | 0 bytes | 0 bytes (Garantido por teste forense) | ⬜ |
| **Precedência de Shadowing Local** | N/A | 100% Determinístico em Memória | ⬜ |
| **Rastreabilidade de Escopo no Payload XML** | Inexistente | Tag explícita `scope="..."` | ⬜ |

---

## 2. Estrutura de Artefatos Afetados

```text
.github/scripts/
├── skills_router.py          # Atualização: WorkspaceScopeResolver (multi-agent) e FederatedSkillsRouter
├── skills_mcp_server.py      # Atualização: FederatedSkillsDatabase integrado com auto-indexação
└── tests/
    └── test_rag_federated.py # [NOVO] Suíte de testes da federação e teste forense de zero-mutação
```

---

## 3. Conceitos-Chave da Solução

### 3.1 Lista Canônica de Diretórios Multi-Agente (`WORKSPACE_SKILL_CANDIDATE_DIRS`)

```python
WORKSPACE_SKILL_CANDIDATE_DIRS = [
    ".gemini/skills",
    ".gemini/config/skills",
    ".kilo/skills",
    ".kilocode/skills",
    ".claude/skills",
    ".claude/commands",
    ".cursor/skills",
    ".windsurf/skills",
    ".github/skills",
    ".skills",
    "skills",
    ".agent/skills",
    ".agents/skills"
]
```

### 3.2 `WorkspaceScopeResolver` com Auto-Indexação Inteligente

```python
class WorkspaceScopeResolver:
    @staticmethod
    def find_workspace_skills_dir(cwd=None) -> str | None:
        base_dir = cwd or os.getcwd()
        for rel_dir in WORKSPACE_SKILL_CANDIDATE_DIRS:
            candidate = os.path.join(base_dir, rel_dir)
            if os.path.isdir(candidate):
                # Verifica se contém arquivos .md de skill
                for root, _, files in os.walk(candidate):
                    if any(f.endswith('.md') or f == 'SKILL.md' for f in files):
                        return os.path.abspath(candidate)
        return None

    @staticmethod
    def ensure_local_rag_index(skills_dir: str, target_db_path: str) -> str:
        # Se o banco SQLite não existir ou o mtime dos arquivos .md for mais recente que o DB:
        # Executa auto-indexação criando schema e populando FTS5 + vetores locais
        ...
```

### 3.3 Algoritmo de Shadowing & Merge em Memória

```python
# Coleta pool de ambos os bancos
candidates_map = {}

# 1. Coleta do Banco Global (Read-Only)
for skill in global_candidates:
    skill["scope"] = "global"
    candidates_map[skill["skill_id"]] = skill

# 2. Coleta do Banco Local (Sobrescreve se mesmo ID)
if local_candidates:
    for skill in local_candidates:
        skill["scope"] = "workspace_local"
        # Leve boost de prioridade para o contexto de projeto (+5%)
        skill["confidence"] = min(99.9, round(skill["confidence"] * 1.05, 1))
        candidates_map[skill["skill_id"]] = skill # Shadowing garantido
```

### 3.4 Estrutura do Payload XML Federado

```xml
<!-- DYNAMIC SKILL INJECTION (ADR-023 FEDERATED): custom-deploy (v1.0.0) -->
<skill name="custom-deploy" category="project_skill" scope="workspace_local">
  <summary>Instruções de deploy para ambiente de staging interno...</summary>
  <description>Automatiza o pipeline de deploy para a infraestrutura Kubernetes local.</description>
  <side_effects>External Execution / Local Only</side_effects>
  <matched_trigger>deploy-staging</matched_trigger>
  <focused_chunk section="Instruções de Execução">
    ./scripts/deploy-staging.sh --env=sandbox
  </focused_chunk>
</skill>
```

---

## 4. Workflows de Implementação

### Workflow 1: Multi-Agent Discovery & Auto-Indexing
- **Objetivo:** Descobrir diretórios de skills locais e auto-indexar em SQLite caso necessário.
- **Passos:**
  1. Varre `WORKSPACE_SKILL_CANDIDATE_DIRS` no diretório de trabalho.
  2. Se encontrado diretório com skills, compara `mtime` dos arquivos contra o DB.
  3. Se desatualizado/inexistente, constrói o banco local em `<workspace_root>/.local/skills_rag/skills_rag.sqlite3`.
- **Checkpoint:** Repositório novo com pasta `.claude/skills` ou `.kilo/skills` é auto-indexado em < 100ms.

### Workflow 2: Merge em Memória e Reranking Federado
- **Objetivo:** Fundir pools de candidatos preservando precedência local e alimentando o Cross-Encoder.
- **Passos:**
  1. Executar busca léxica + vetorial no banco global e local.
  2. Aplicar shadowing por `skill_id`.
  3. Enviar lista unificada para o Reranker neural com tag de escopo.
- **Checkpoint:** Query para skill customizada local com mesmo ID de skill global retorna a versão local.

### Workflow 3: Injeção de Prompt com Rastreabilidade
- **Objetivo:** Adicionar metadados de escopo no XML retornado.
- **Passos:**
  1. `generate_prompt_payload` inclui `scope="{skill_item['scope']}"`.
  2. Servidor MCP reflete `scope` na telemetria.
- **Checkpoint:** XML gerado documenta explicitamente se a skill é `global` ou `workspace_local`.

---

## 5. Checklists

### Checklist de Pré-Deploy
- [ ] Varredura das 12 convenções de pastas multi-agente testada.
- [ ] Conexão global protegida com `PRAGMA query_only = ON`.
- [ ] Auto-indexação local com verificação de `mtime` implementada.

### Checklist de Pós-Deploy
- [ ] Suíte `test_rag_federated.py` executando com 5/5 testes aprovados.
- [ ] Teste forense de integridade confirmando que o SHA-256 do arquivo global permanece imutável.
- [ ] Auditoria SOTA executando com 100% de conformidade.

---

*Documento gerado em 2026-08-24. Referência: ADR-023.*
