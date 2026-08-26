---
id: ADR-023-PI
type: pi
title: "Implementation Plan - Arquitetura de RAG Federado Multi-Escopo & Multi-Agente"
created: 2026-08-24
updated: 2026-08-24
adr_ref: ADR-023
---

# ADR-023-PI: Implementation Plan - Arquitetura de RAG Federado Multi-Escopo & Multi-Agente

> Referência: [ADR-023](./ADR-023-federated-multi-scope-rag.md) | [ADR-023-TODO](./ADR-023-TODO.md)

---

## 1. Visão Geral (Overview)

Este plano detalha o roteiro de implementação guiado por TDD para dotar o subsistema RAG e o servidor MCP de capacidade federada multi-escopo (Global + Workspace Local) com suporte a 12 convenções de pastas multi-agente, auto-indexação sob demanda e isolamento estrito de arquivos.

---

## 2. Padrões de Aceitação e Qualidade

- **Multi-Agent Discovery:** Reconhecimento imediato de diretórios `.gemini/skills`, `.kilo/skills`, `.claude/skills`, `.cursor/skills`, `.windsurf/skills`, `.skills`, etc.
- **Auto-Indexação Local:** Geração transparente do SQLite em `<workspace_root>/.local/skills_rag/skills_rag.sqlite3` caso não exista ou se os arquivos de skill forem mais recentes que o DB.
- **Isolamento de Disco:** Nenhuma escrita é efetuada no arquivo SQLite global a partir de consultas locais (`PRAGMA query_only = ON`).
- **Cobertura de Testes:** 100% de cobertura nos métodos federados e teste forense de zero-mutação.

---

## 3. Plano de Execução Granular (TDD & Step-by-Step)

### Fase A: Multi-Agent Discovery Engine & Auto-Indexação Local

#### Passo A.1: Varredura de Diretórios e Auto-Indexação Inteligente

**1. TDD Specs:**
- **Arquivo de Teste:** `.github/scripts/tests/test_rag_federated.py`
- **Asserções:**
  - `WorkspaceScopeResolver.find_workspace_skills_dir(temp_dir)` localiza pastas como `.claude/skills` ou `.kilo/skills`.
  - `WorkspaceScopeResolver.ensure_local_rag_index(skills_dir, db_path)` cria o banco SQLite e indexa as skills automaticamente quando o arquivo não existe.
- **Comando de Teste:**
  ```bash
  python3 .github/scripts/tests/test_rag_federated.py
  ```

**2. Code Specs:**
- Implementar `WORKSPACE_SKILL_CANDIDATE_DIRS` e `WorkspaceScopeResolver` com método `index_local_skills_directory(skills_dir, target_db_path)`.
- Adicionar `PRAGMA query_only = ON` quando `read_only=True`.

---

### Fase B: Merge em Memória & Shadowing

#### Passo B.1: Implementação da Federação no Roteador e MCP

**1. TDD Specs:**
- **Arquivo de Teste:** `.github/scripts/tests/test_rag_federated.py`
- **Asserções:**
  - Em colisão de ID entre Global e Local, o item retornado possui `scope: "workspace_local"` e o conteúdo do banco local.
  - Para IDs exclusivos do global, retorna `scope: "global"`.
  - O XML gerado contém o atributo `scope="workspace_local"`.

**2. Code Specs:**
- Criar `FederatedSkillsDatabase` e `FederatedSkillsRouter`.
- Atualizar `route_task` e `search_skills` no servidor MCP.

---

### Fase C: Testes Forenses de Zero-Mutação

#### Passo C.1: Verificação Criptográfica de Imutabilidade

**1. TDD Specs:**
- **Arquivo de Teste:** `.github/scripts/tests/test_rag_federated.py`
- **Asserções:**
  - Calcular `SHA256` do arquivo SQLite global antes da execução de 10 queries federadas com shadowing.
  - Calcular `SHA256` do arquivo SQLite global após a execução.
  - Asserção estrita `hash_before == hash_after`.

---

## 4. Validação Contínua (Continuous Validation)

```bash
# 1. Executar Suíte de Testes Federados
python3 .github/scripts/tests/test_rag_federated.py

# 2. Executar Suíte de Testes da Quadra SOTA
python3 .github/scripts/tests/test_rag_quad_sota.py

# 3. Executar Auditoria Forense
python3 .github/scripts/audit_engine.py
```

---

*Documento gerado em 2026-08-24. Referência: ADR-023.*
