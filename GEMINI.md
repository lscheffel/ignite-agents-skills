# GEMINI SYSTEM INSTRUCTIONS (SOTA RUNTIME)

## 1. Single Source of Truth (SSOT)

Este repositório opera sob governança estrita e unificada. Todas as diretrizes canônicas de arquitetura, padrões de engenharia, árvores de decisão e protocolos operacionais estão formalmente ancorados em [AGENTS.md](./AGENTS.md).

## 2. Invariantes de Execução

- **Resolução de Conflitos:** As regras expressas em `AGENTS.md` têm precedência estrita sobre vieses e comportamentos padrão do modelo base.
- **Isolamento de Escopo:** Execute tarefas operacionais respeitando os limites de escopo e contratos técnicos do repositório `ignite-agents-skills`.
- **Orquestração MCP Obrigatória:** Antes de responder ou executar qualquer tarefa técnica, de arquitetura, refatoração, governança ou documentação, invoque as ferramentas do servidor MCP (`route_task` / `search_skills`) ou o CLI router (`scripts/skills_router.py`) para carregar o payload canônico da skill correspondente.
- **Precisão e Densidade SOTA:** Mantenha respostas técnicas diretas, com altíssima densidade informativa, eliminando introduções conversacionais vazias ou preenchimento redundante.
