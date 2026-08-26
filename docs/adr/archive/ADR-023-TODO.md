---
id: ADR-023-TODO
type: todo
title: "Execução - Arquitetura de RAG Federado Multi-Escopo & Multi-Agente"
created: 2026-08-24
updated: 2026-08-24
adr_ref: ADR-023
---

# ADR-023-TODO: Execução - Arquitetura de RAG Federado Multi-Escopo & Multi-Agente

> Referência: [ADR-023](./ADR-023-federated-multi-scope-rag.md) | [ADR-023-BP](./ADR-023-BP.md) | Status: ✅ CONCLUÍDO

## Legenda

- ✅ Concluído
- ⬜ Pendente
- 🔄 Em Andamento
- ❌ Bloqueado
- ⏸️ Pausado

**Prioridade:** 🔴 Alta | 🟡 Média | 🟢 Baixa

---

## Fase A: Multi-Agent Discovery Engine & Auto-Indexação Local

### A1: Módulo de Resolução Multi-Agente e Auto-Indexador

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|---|:---:|:---:|---|:---:|
| A1.1 | Criar lista `WORKSPACE_SKILL_CANDIDATE_DIRS` com as 12 convenções canônicas de agentes | ✅ | 🔴 | — | ~10 min |
| A1.2 | Implementar `WorkspaceScopeResolver` com varredura recursiva de diretórios de skills | ✅ | 🔴 | A1.1 | ~15 min |
| A1.3 | Implementar auto-indexador local sob demanda baseado em `mtime` de arquivos `.md` | ✅ | 🔴 | A1.2 | ~20 min |
| A1.4 | Implementar suporte a `read_only=True` com `PRAGMA query_only = ON` em `SkillsDatabase` | ✅ | 🔴 | — | ~10 min |

**Checkpoint A1:**
- [x] O roteador descobre automaticamente pastas como `.gemini/skills`, `.claude/skills`, `.kilo/skills` e cria/atualiza o `.sqlite3` local se necessário.

---

## Fase B: Merge em Memória, Shadowing & Payload Tagging

### B1: Lógica de Fusão e Formatação XML

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|---|:---:|:---:|---|:---:|
| B1.1 | Implementar algoritmo de merge in-memory com shadowing de `skill_id` e boost local | ✅ | 🔴 | A1.4 | ~20 min |
| B1.2 | Integrar pool federado ao Cross-Encoder Rerank (NVIDIA NIM e Fallback Local) | ✅ | 🔴 | B1.1 | ~15 min |
| B1.3 | Atualizar `generate_prompt_payload` para incluir atributo `scope="global"` ou `scope="workspace_local"` | ✅ | 🔴 | B1.2 | ~10 min |
| B1.4 | Atualizar ferramentas do MCP Server (`search_skills` e `route_task`) com suporte federado | ✅ | 🔴 | B1.3 | ~15 min |

**Checkpoint B1:**
- [x] Em colisão de `skill_id`, a versão local sobrescreve a global apenas na memória da sessão.
- [x] O XML gerado contém o atributo `scope="workspace_local"`.

---

## Fase C: Suíte de Testes Automatizados & Teste Forense

### C1: Validação Rigorosa e Verificação Invariante

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|---|:---:|:---:|---|:---:|
| C1.1 | Criar `test_rag_federated.py` com testes de resolução multi-agente e auto-indexação | ✅ | 🔴 | B1.4 | ~20 min |
| C1.2 | Implementar teste `test_in_memory_shadowing` validando precedência local | ✅ | 🔴 | C1.1 | ~15 min |
| C1.3 | Implementar teste forense `test_zero_mutation_global_db` (SHA-256 do arquivo global inalterado) | ✅ | 🔴 | C1.2 | ~15 min |
| C1.4 | Executar auditoria de governança `audit_engine.py` e validar 100% dos ativos | ✅ | 🔴 | C1.3 | ~10 min |

**Checkpoint C1:**
- [x] 5/5 testes da suíte federada passando com sucesso.
- [x] Invariante de zero-mutação comprovada matematicamente.

---

## Resumo Geral

| Fase | Tarefas | Horas Est. | Status |
|---|---|:---:|:---:|
| **Fase A: Multi-Agent Discovery & Auto-Indexação** | 4 | ~55 min | ✅ |
| **Fase B: Merge em Memória, Shadowing & Payload Tagging** | 4 | ~1h 00m | ✅ |
| **Fase C: Suíte de Testes Automatizados & Teste Forense** | 4 | ~1h 00m | ✅ |
| **Total** | **12** | **~2h 55m** | ✅ CONCLUÍDO |

---

*Documento gerado em 2026-08-24. Referência: ADR-023.*
