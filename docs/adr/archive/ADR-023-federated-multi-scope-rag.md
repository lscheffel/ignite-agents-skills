---
id: ADR-023
type: adr
title: "Arquitetura de RAG Federado Multi-Escopo: Multi-Agent Workspace Discovery, Auto-Indexação e Shadowing em Memória"
created: 2026-08-24
updated: 2026-08-24
implementation_status: CONSOLIDADA
depends_on:
  - ADR-021
  - ADR-022
---

# ADR-023: Arquitetura de RAG Federado Multi-Escopo: Multi-Agent Workspace Discovery, Auto-Indexação e Shadowing em Memória

## Status
**Proposto**

## Contexto

### Diagnóstico

Com a consolidação do ecossistema RAG híbrido de alto desempenho ([ADR-021](./ADR-021-dual-engine-neural-rerank.md) e [ADR-022](./ADR-022-rag-sota-quad-optimizations.md)), o servidor MCP e o roteador CLI operam com excelência sobre o catálogo canônico global (`~/.gemini/config/skills/`). 

Entretanto, em ambientes de desenvolvimento modernos, múltiplos agentes e IDEs (Gemini CLI, Kilocode, Claude Code, Cursor, Windsurf, Antigravity) utilizam diferentes convenções de pastas para armazenar skills e comandos específicos de projeto:
- Gemini / Antigravity: `.gemini/skills`, `.gemini/config/skills`, `.agents/skills`, `.agent/skills`
- Kilo / Kilocode: `.kilo/skills`, `.kilocode/skills`
- Claude Code: `.claude/skills`, `.claude/commands`
- Cursor / Windsurf: `.cursor/skills`, `.windsurf/skills`
- Padrões Genéricos: `.skills`, `skills`, `.github/skills`

| Capacidade | Status Atual | Evidência / Impacto |
|---|---|---|
| **Escopo Global** | ✅ SOTA (81 skills canônicas) | Catálogo universal disponível em `~/.gemini/config/skills/`. |
| **Multi-Agent Discovery** | ❌ Inexistente | O roteador só conhecia o caminho fixo global, ignorando convenções de outras ferramentas de IA. |
| **Auto-Indexação Local** | ❌ Manual | Exigia criar e indexar manualmente um SQLite em cada projeto antes de usá-lo. |
| **Isolamento de Estado** | Parcial | Risco de misturar regras locais com o catálogo global se copiado diretamente. |
| **Precedência (Shadowing)** | Inexistente | Impossível substituir uma skill global por uma versão customizada no repositório atual. |

---

## Decisão

Adotamos a **Arquitetura de RAG Federado Multi-Escopo Multi-Agente (ADR-023)** com Descoberta Automática de Workspace, Auto-Indexação sob Demanda e Fusão em Memória:

```
                  ┌────────────────────────────────────────────────────────┐
                  │                 Query do Desenvolvedor                 │
                  └───────────────────────────┬────────────────────────────┘
                                              │
                 ┌────────────────────────────┴────────────────────────────┐
                 │                                                         │
                 ▼                                                         ▼
    ┌─────────────────────────┐                               ┌─────────────────────────┐
    │     DB Global (~/)      │                               │   Multi-Agent Discovery │
    │   ~/.gemini/.../skills  │                               │   Varre pastas locais:  │
    │   81 Skills Canônicas   │                               │   .gemini, .kilo,       │
    │   (Modo READ-ONLY)      │                               │   .claude, .cursor, etc │
    └────────────┬────────────┘                               └────────────┬────────────┘
                 │                                                         │
                 │                                                         ▼
                 │                                            ┌─────────────────────────┐
                 │                                            │  Auto-Indexação Local   │
                 │                                            │  (Gera SQLite se novo   │
                 │                                            │  ou arquivos mudaram)   │
                 │                                            └────────────┬────────────┘
                 │                                                         │
                 │                                                         ▼
                 │                                            ┌─────────────────────────┐
                 │                                            │    DB Local (./data)    │
                 │                                            │  Skills do Workspace    │
                 │                                            └────────────┬────────────┘
                 │                                                         │
                 └────────────────────────────┬────────────────────────────┘
                                              │
                                              ▼
                               ┌─────────────────────────────┐
                               │     Merge & Shadowing       │
                               │   (Local tem precedência    │
                               │   sobre Global em colisão)  │
                               └──────────────┬──────────────┘
                                              │
                                              ▼
                               ┌─────────────────────────────┐
                               │   NVIDIA Cross-Encoder      │
                               │   nv-rerank-qa-mistral-4b:1 │
                               └──────────────┬──────────────┘
                                              │
                                              ▼
                               ┌─────────────────────────────┐
                               │  Injeção XML com Atributo   │
                               │  scope="workspace_local"    │
                               └─────────────────────────────┘
```

### Invariantes e Regras Arquiteturais

1. **Multi-Agent Workspace Discovery:** O resolvedor inspeciona recursivamente a raiz do projeto procurando por qualquer uma das convenções de pastas suportadas (`.gemini/skills`, `.kilo/skills`, `.claude/skills`, `.cursor/skills`, etc.).
2. **Auto-Indexação Determinística:** Se o diretório contiver arquivos de skill e o arquivo `.local/skills_rag/skills_rag.sqlite3` local não existir ou estiver desatualizado em relação ao `mtime` dos arquivos de skill, o indexador local é executado automaticamente em background.
3. **Zero Poluição Global:** O banco SQLite global opera com `PRAGMA query_only = ON`. Jamais recebe registros, vetores ou índices derivados de repositórios locais.
4. **Isolamento de Disco do Workspace:** O banco local reside exclusivamente no diretório do projeto ativo (`<workspace_root>/.local/skills_rag/skills_rag.sqlite3`).
5. **Shadowing em Tempo de Execução:** Se houver colisão de `skill_id` entre o escopo Local e o Global, a skill Local substitui a Global em memória apenas para aquela consulta, sem alterar nenhum arquivo global no disco.
6. **Rastreabilidade no Payload XML:** O XML gerado inclui a tag de escopo explícita (`scope="global"` ou `scope="workspace_local"`).

---

## Alternativas Consideradas

### Alternativa A: Indexar tudo no mesmo banco global adicionando coluna `project_path`
- **Prós**: Consulta simplificada em uma única tabela SQLite.
- **Contras**: Violação do isolamento de estado, risco de poluição cruzada entre clientes e necessidade de reindexação do banco global a cada projeto aberto.

### Alternativa B: RAG isolado por projeto sem acesso ao catálogo global
- **Prós**: Isolamento total de arquivos.
- **Contras**: Perda de todo o ecossistema de 81 skills canônicas (TDD, ADR, Git Workflow, Security Review, Clean Code) em novos projetos.

### Alternativa C: Federação Multi-Agente com Auto-Indexação e Shadowing em Memória (Escolhida)
- **Prós**: Compatibilidade universal com múltiplos ecossistemas de agentes (Gemini, Kilo, Claude, Cursor), auto-indexação transparente e isolamento 100% estrito.
- **Contras**: Requer instanciação e verificação de timestamps de arquivos locais.

---

## Consequências

### Positivas
- **Interoperabilidade Total:** Suporta skills de Gemini, Kilo, Claude Code, Cursor e Windsurf no mesmo RAG sem intervenção manual.
- **Auto-Configuração:** Projetos novos com pasta de skills tornam-se imediatamente consultáveis sem necessidade de scripts manuais.
- **Segurança e Privacidade:** Dados confidenciais de regras de negócio locais não trafegam nem são persistidos no catálogo global.
- **Zero Overhead quando Inativo:** Se não houver skills locais, o sistema opera exatamente no tempo padrão do pipeline global.

### Riscos e Mitigações
- **Risco**: Custo de auto-indexação em cada consulta.
  - **Mitigação**: Comparação rápida de `mtime` (timestamp de modificação) dos arquivos contra a data do SQLite; se inalterado, não reindexa.

---

## Referências
- [ADR-021: Dual-Engine Neural Cross-Encoder Reranking](./ADR-021-dual-engine-neural-rerank.md)
- [ADR-022: Pipeline RAG Quádruplo SOTA](./ADR-022-rag-sota-quad-optimizations.md)
- Evidence Record: (pendente)
