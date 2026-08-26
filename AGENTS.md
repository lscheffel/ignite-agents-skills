# AGENTS.md — ignite-agents-skills (SSOT)

## 1. Visão Geral

Registro centralizado de **60 skills SOTA** para agentes de IA compatíveis com o padrão [Agent Skills](https://agentskills.io). Hospedado como GitHub Pages, este repositório serve como registry remoto para múltiplos projetos que usam **Kilo Code**, **OpenCode**, **Gemini CLI**, **Antigravity** e outros agentes compatíveis.

Além do registry remoto (`skills/index.json`), o repositório integra nativamente um **Servidor MCP Stdio (`skills-rag-mcp`)**, **Motor RAG Vetorial Semântico (SQLite3 + FTS5 + BM25 + Embeddings)**, **CLI Router**, **Motor de Auditoria Forense em 8 Dimensões SOTA** e **Gerador de Páginas Estáticas HTML** para deploy no GitHub Pages.

---

## 2. Estrutura do Projeto

```
.
├── LICENSE
├── README.md                           # Documentação principal
├── USAGE.md                            # Guia completo de uso das skills
├── CHANGELOG.md                        # Histórico de versões
├── AGENTS.md                           # Este arquivo (SSOT de governança para agentes)
├── skills/
│   ├── index.json                      # Registry centralizado (fonte única para Kilo/OpenCode)
│   ├── adr-architecture-elevation/     # Desafio adversarial e ampliação de ADRs
│   ├── adr-archive/
│   ├── adr-generator/
│   ├── ... (60 skills SOTA)
│   └── xlsx-processing/
├── scripts/                            # Toolbox e Motores Unificados
│   ├── sync-index.sh                   # Auto-gera skills/index.json
│   ├── validate-index.sh               # Valida index.json contra arquivos reais
│   ├── validate-skill.sh               # Valida qualidade Ultra-High Quality Grade
│   ├── archive-adrs.sh                 # Janitor de ciclo de vida de ADRs
│   ├── skills_mcp_server.py            # Servidor MCP Stdio (skills-rag-mcp)
│   ├── skills_rag_indexer.py           # Motor de Indexação Vetorial / FTS5
│   ├── skills_router.py                # CLI Router para busca semântica
│   ├── audit_engine.py                 # Motor de Auditoria Forense SOTA (8 Dimensões)
│   ├── translate_catalog_nim.py        # Tradutor de catálogo
│   └── tests/                          # Suíte de testes automatizados (42 testes)
├── pages/                              # Motor de Documentação Web
│   ├── build.py                        # Gerador de HTML estático
│   └── ...                             # Templates e artefatos renderizados
├── docs/                               # Governança e Arquitetura
│   ├── adr/                            # ADR-001 a ADR-026 (ativas + archive)
│   └── audit/                          # Ledgers de auditoria
└── data/                               # Banco SQLite vetorial e especificações
```

---

## 3. Diretrizes de Execução para Agentes de IA

### 3.1 Protocolo de Busca e Roteamento de Skills
Antes de responder ou executar qualquer tarefa técnica (planejamento, codificação, refatoração, documentação, testes):
1. Utilize o roteador semântico: `python3 scripts/skills_router.py "<intenção da tarefa>"` ou ferramentas do servidor MCP `skills-rag-mcp` (`route_task` / `search_skills`).
2. Adote estritamente os padrões, regras, fluxos de decisão e checklists contidos na skill ativada.
3. Declare no início da resposta a skill ativada quando aplicável.

### 3.2 Padrão de Qualidade Ultra-High Quality Grade (SOTA)
- Todas as skills seguem arquitetura modular com YAML Frontmatter (`name`, `description`, `version`, `tags`, `related_skills`).
- Documentação clara com seções de ativação, fluxos/processos, identificação de riscos/anti-patterns com severidade (`🔴 crítico`, `🟡 alerta`, `🟢 suave`), checklists de verificação e edge cases.

---

## 4. Matriz de Comandos de Governança

| Operação | Comando Oficial |
|:---|:---|
| **Sincronizar `skills/index.json`** | `./scripts/sync-index.sh` |
| **Validar `skills/index.json`** | `./scripts/validate-index.sh` |
| **Validar Qualidade de Skills** | `bash scripts/validate-skill.sh skills/{skill-name}` |
| **Auditoria Forense SOTA (8 Dimensões)** | `python3 scripts/audit_engine.py` |
| **Ingestão & Vetorização RAG** | `python3 scripts/skills_rag_indexer.py` |
| **Roteamento Semântico CLI** | `python3 scripts/skills_router.py "<consulta>"` |
| **Servidor MCP Stdio** | `python3 scripts/skills_mcp_server.py` |
| **Suíte de Testes Automatizados** | `python3 -m unittest discover -s scripts/tests -p "test_*.py"` |
| **Compilar Páginas HTML do Site** | `python3 pages/build.py` |
| **Janitor de Arquivamento de ADRs** | `./scripts/archive-adrs.sh` |

---

## 5. Governança e Branching Strategy

- **master**: Branch de produção e deploy contínuo.
- **feature/***: Novas features e especializações (ex: `feature/sync-gemini-skills`).
- **fix/***: Correções de bugs e integridade.
- **docs/***: Atualizações exclusivas de documentação.
- **adr-XXX/***: Implementação de ADR específica.

### Ciclo de Vida de Mudanças:
1. Criar branch de trabalho (`feature/...`, `fix/...`, `adr-XXX/...`).
2. Implementar mudanças em `skills/`, `scripts/` ou documentação.
3. Executar `./scripts/sync-index.sh` e `./scripts/validate-index.sh`.
4. Executar `python3 scripts/audit_engine.py` e `python3 -m unittest discover -s scripts/tests -p "test_*.py"`.
5. Executar `python3 pages/build.py`.
6. Merge para `master` e deploy sincronizado para `gh-pages`.
