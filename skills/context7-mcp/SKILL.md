---
name: context7-mcp
version: 1.0.0
description: This skill should be used when the user asks about libraries, frameworks,
related_skills:
  - cap
  - implementation
  - technical-documentation
  API references, or needs code examples. Activates for setup questions, code generation
  involving libraries, or mentions of specific frameworks like React, Vue, Next.js,
  Prisma, Supabase, etc.
domain: domain-stack
triggers:
  - context7-mcp
  - context7-docs
  - fetch-library-docs
  - framework-documentation
  - consultar-documentacao
  - buscar-docs-biblioteca
  - mcp-context7
  - query-docs
tags:
- context7-mcp
- domain-stack
metadata:
  author: Context7 Community
  provenance: third-party
  source_repo: https://github.com/context7
  license: MIT
  last_audited: '2026-08-05'
---

# Context7 Mcp

When the user asks about libraries, frameworks, or needs code examples, use Context7 to fetch current documentation instead of relying on training data.

## When to Use This Skill


## Decision Workflow

```mermaid
graph TD
    A["Início: Ativação da Skill (context7-mcp)"] --> B["Validação de Pré-requisitos & Escopo"]
    B --> C{"Requisitos Claros & Completos?"}
    C -->|Não| D["Solicitar Clarificação / Coletar Contexto (cap)"]
    C -->|Sim| E["Execução do Procedimento Canônico"]
    D --> E
    E --> F["Verificação de Qualidade & Critérios de Aceite"]
    F --> G{"Checklist 100% Aprovado?"}
    G -->|Não| E
    G -->|Sim| H["Completion Gate: Entrega do Artefato Certificado"]
```

Activate this skill when the user:

- Asks setup or configuration questions ("How do I configure Next.js middleware?")
- Requests code involving libraries ("Write a Prisma query for...")
- Needs API references ("What are the Supabase auth methods?")
- Mentions specific frameworks (React, Vue, Svelte, Express, Tailwind, etc.)

## How to Fetch Documentation

### Step 1: Resolve the Library ID

Call `resolve-library-id` with:

- `libraryName`: The library name extracted from the user's question
- `query`: The user's full question (improves relevance ranking)

### Step 2: Select the Best Match

From the resolution results, choose based on:

- Exact or closest name match to what the user asked for
- Higher benchmark scores indicate better documentation quality
- If the user mentioned a version (e.g., "React 19"), prefer version-specific IDs

### Step 3: Fetch the Documentation

Call `query-docs` with:

- `libraryId`: The selected Context7 library ID (e.g., `/vercel/next.js`)
- `query`: The user's specific question

### Step 4: Use the Documentation

Incorporate the fetched documentation into your response:

- Answer the user's question using current, accurate information
- Include relevant code examples from the docs
- Cite the library version when relevant

## Guidelines

- **Be specific**: Pass the user's full question as the query for better results
- **Version awareness**: When users mention versions ("Next.js 15", "React 19"), use version-specific library IDs if available from the resolution step
- **Prefer official sources**: When multiple matches exist, prefer official/primary packages over community forks


## Anti-Patterns & Operational Guardrails

| Anti-Pattern | Severidade | Impacto Negativo | Mitigação Canônica |
|:---|:---:|:---|:---|
| **Execução Prematura sem Contexto** | 🔴 Critical | Alucinação de contexto e refatoração destrutiva | Ativar a skill `cap` para adquirir evidências mínimas antes de editar. |
| **Omissão de Checklists de Validação** | 🟡 Medium | Entrega de artefatos com inconsistências sintáticas | Executar rigorosamente o checklist passo a passo antes do handoff. |
| **Falta de Documentação de Decisões** | 🟢 Low | Perda de rastreabilidade técnica e drift arquitetural | Registrar trade-offs relevantes via skill `adr-generator`. |



## Edge Cases & Failure Modes

- **Ambiente Restrito / Read-Only:** Se o filesystem ou sandbox estiver bloqueado contra escrita, reportar o bloqueio com evidência imediata e gerar o patch em markdown diff.
- **Conflito de Especificação:** Caso encontre contradições entre a intenção do usuário e o SSOT (`AGENTS.md`), interromper e sinalizar as opções com trade-offs.
- **Timeout ou Exaustão de Contexto:** Em tarefas volumosas, decompor em sub-lotes atômicos utilizando a skill `subagent-driven-development`.



## Domain SOTA & Industry Engineering Standards

- **Live Documentation Retrieval:** Real-time API resolution, version pinning, and authoritative documentation indexing.
- **Model Context Protocol Integration:** Fast MCP lazy-loading, caching, and token-optimized query dispatch.
- **Semantic Routing:** Two-phase retrieval (1. `resolve-library-id` $\to$ 2. `query-docs`).
- **Knowledge Freshness:** Strict prioritization of Context7 over model training weights for libraries and SDKs.

### Context7 Operating Protocol:
1. **Phase 1 (Resolve ID):** Call `resolve-library-id` using official library name and question context. Select match matching `/org/project`.
2. **Phase 2 (Query Docs):** Call `query-docs` passing full natural language technical question.
3. **Phase 3 (Doc Ingestion):** Answer strictly based on fetched documentation payload.

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Never Guess Modern APIs):** For popular evolving frameworks (Next.js, React 19, Tailwind, Prisma), Context7 lookup is MANDATORY before writing code.
2. **Rule of Thumb 2 (Full Question Rule):** Always pass the complete user technical question to `query-docs`, never isolated single keywords.
3. **Rule of Thumb 3 (Version Specificity):** When a specific version is mentioned by the user (e.g. "Vite 6"), select the version-tagged library ID.
4. **Rule of Thumb 4 (Fallback to Web Search):** If Context7 returns empty results after 2 attempts, fall back to official web search with domain whitelisting.

## Operational Verification Checklist

- [ ] Todos os pré-requisitos e arquivos-alvo foram inspecionados antes da modificação.
- [ ] O procedimento seguiu estritamente as regras e boas práticas da especialização.
- [ ] As diretrizes de segurança, tipagem e estilo foram preservadas.
- [ ] Os testes unitários ou comandos de validação foram executados com sucesso.
- [ ] O artefato final foi inspecionado contra o completion gate.



## Completion Gate & Verification
Before concluding Context7 query:
- [ ] Best matching library ID resolved via `resolve-library-id`
- [ ] Query executed passing complete technical question context
- [ ] Final answer strictly grounded in fetched documentation payload