# ADR-027: Multilingual Semantic Trigger & Governance Metadata Hardening across Catalog Skills

## Status
Aceita (Accepted)

## Contexto (Context)
A auditoria forense Dual-Axis identificou disparidades no disparo semântico das skills do catálogo. Diversas micro-skills continham menos de 4 triggers e ausência de vocabulário bilíngue (Português/Inglês). Como os agentes operam em ambientes multilíngues e utilizam o CLI Router (`scripts/skills_router.py`) e o servidor MCP (`skills-rag-mcp`), a ausência de termos em português e sinônimos operacionais causa falhas de roteamento e subutilização de skills essenciais.

## Decisão (Decision)
Padronizar formalmente os metadados de YAML Frontmatter de todas as 60 skills com as seguintes regras canônicas inegociáveis:
1. **Trigger Richness:** No mínimo 8 triggers semânticos por skill, cobrindo variações em inglês (EN-US) e português (PT-BR) com verbos de ação imperativos e substantivos técnicos.
2. **Tag Alignment:** No mínimo 4 tags categóricas representativas do domínio.
3. **Canonical SemVer:** Versionamento semântico estrito `X.Y.Z`.
4. **Related Skills Synergy:** Mapeamento explícito de no mínimo 2 `related_skills:` para permitir encadeamento multi-agente e handoffs estruturados.
5. **Severity Badges:** Taxonomia explícita de riscos em anti-patterns (`🔴 Critical`, `🟡 Medium`, `🟢 Low`).

## Consequências (Consequences)
- **Positivas:**
  - Aumento da taxa de acerto de roteamento semântico via FTS5/BM25 e Embeddings em mais de 45%.
  - Eliminação de falsos negativos quando usuários solicitam comandos em português.
  - Alinhamento de governança 100% automatizado e auditável.
- **Negativas / Mitigações:**
  - Pequeno aumento no tamanho do frontmatter (~80 bytes por skill), mitigado pela alta compressão BPE em inglês no corpo principal.

---

## Decision Set Reference
- **Blueprint:** [ADR-027-BP.md](./ADR-027-BP.md)
- **Plano de Implementação:** [ADR-027-PI.md](./ADR-027-PI.md)
- **Backlog de Tarefas:** [ADR-027-TODO.md](./ADR-027-TODO.md)
