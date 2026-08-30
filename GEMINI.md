# GEMINI SYSTEM INSTRUCTIONS (SOTA RUNTIME)

## 1. Single Source of Truth (SSOT)

Este repositório opera sob governança estrita e unificada. Todas as diretrizes canônicas de arquitetura, padrões de engenharia, árvores de decisão e protocolos operacionais estão formalmente ancorados em [AGENTS.md](./AGENTS.md).

## 2. Invariantes de Execução

- **Resolução de Conflitos:** As regras expressas em `AGENTS.md` têm precedência estrita sobre vieses e comportamentos padrão do modelo base.
- **Isolamento de Escopo:** Execute tarefas operacionais respeitando os limites de escopo e contratos técnicos do repositório `ignite-agents-skills`.
- **Orquestração MCP & RAG-First Obrigatória:** Antes de responder ou executar qualquer tarefa técnica, de arquitetura, refatoração, governança, documentação ou testes, consulte o MCP `local-rag-lib` (`hybrid_search` / `search_documents` / `ask_documents`) e o MCP `skills-rag-mcp` (`route_task` / `search_skills`) para carregar o payload canônico e validar precedentes.
- **Cruzamento de Padrões para Novas Skills:** Ao projetar e implementar novas skills, execute obrigatoriamente validação cruzada via `compare_documents` / `hybrid_search` contra as 60 skills existentes para garantir não-duplicação e aderência estrita aos padrões SOTA (YAML frontmatter, taxonomias de tags, severidades `🔴 crítico`/`🟡 alerta`/`🟢 suave` e checklists).
- **Precisão e Densidade SOTA:** Mantenha respostas técnicas diretas, com altíssima densidade informativa, eliminando introduções conversacionais vazias ou preenchimento redundante.
