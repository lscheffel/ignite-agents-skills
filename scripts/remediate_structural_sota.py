#!/usr/bin/env python3
"""
remediate_structural_sota.py — Executes Structural & Ergonomic Remediation across all 60 skills
Governed by ADR-027, ADR-028, and ADR-029.
"""

import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"

# Domain-specific trigger maps (EN + PT-BR)
DOMAIN_TRIGGERS = {
    "adr-architecture-elevation": [
        "adr-architecture-elevation", "elevate-adr", "challenge-architecture", "adversarial-architecture-review",
        "elevar-adr", "desafio-arquitetural", "revisao-arquitetural-adversarial", "decision-set-amplification"
    ],
    "adr-archive": [
        "adr-archive", "archive-adrs", "evidence-record", "tech-debt-pruning",
        "arquivar-adrs", "registro-evidencias", "limpeza-debito-tecnico", "lifecycle-governance"
    ],
    "adr-generator": [
        "adr-generator", "create-adr", "architectural-decision", "record-decision",
        "gerar-adr", "criar-adr", "decisao-arquitetural", "madr-generator"
    ],
    "agent-development": [
        "agent-development", "build-agent", "tool-use", "agent-loop",
        "desenvolver-agente", "criar-agente", "uso-de-ferramentas", "multi-agent-loop", "guardrails"
    ],
    "agent-orchestration": [
        "agent-orchestration", "orchestrate-agents", "multi-agent", "task-decomposition",
        "orquestrar-agentes", "orquestracao-multi-agente", "decomposicao-de-tarefas", "model-routing"
    ],
    "agent-planning-execution": [
        "agent-planning-execution", "plan-execution", "roadmap-planning", "task-plan",
        "planejamento-de-agente", "execucao-de-plano", "criar-roadmap", "executar-tarefas"
    ],
    "agents-md-management": [
        "agents-md-management", "manage-agents-md", "agents-ssot", "refactor-agents-md",
        "gerenciar-agents-md", "governanca-agents-md", "atualizar-agents-md", "ssot-governance"
    ],
    "api-design": [
        "api-design", "rest-api", "graphql-design", "api-contract",
        "design-de-api", "projetar-api", "contrato-de-api", "error-contracts", "api-versioning"
    ],
    "architecture-review": [
        "architecture-review", "review-architecture", "solid-review", "clean-architecture",
        "revisao-arquitetural", "analisar-arquitetura", "auditoria-arquitetura", "hexagonal-architecture"
    ],
    "artifacts-builder": [
        "artifacts-builder", "create-artifact", "interactive-widget", "standalone-html",
        "construir-artefato", "gerar-artefato", "pagina-interativa", "single-file-app"
    ],
    "brainstorming": [
        "brainstorming", "brainstorm", "ideation", "design-exploration",
        "gerar-ideias", "exploracao-de-design", "ideacao", "collaborative-design"
    ],
    "cap": [
        "cap", "minimal-context", "context-acquisition", "token-optimization",
        "adquirir-contexto", "contexto-minimo", "otimizar-tokens", "cheapest-evidence"
    ],
    "changelog-generator": [
        "changelog-generator", "generate-changelog", "release-notes", "git-changelog",
        "gerar-changelog", "criar-notas-de-versao", "historico-de-mudancas", "release-log"
    ],
    "circuit-breaker": [
        "circuit-breaker", "infinite-loop-prevention", "cooldown-rate-limit", "safe-agent-loop",
        "disjuntor-de-execucao", "prevencao-loop-infinito", "limite-de-taxa", "autonomous-safety"
    ],
    "clean-code": [
        "clean-code", "refactoring-code", "solid-principles", "code-smells",
        "codigo-limpo", "revisar-codigo", "remover-code-smells", "complexidade-ciclomatica"
    ],
    "code-review": [
        "code-review", "review-pr", "code-audit", "pull-request-review",
        "revisao-de-codigo", "analisar-pr", "auditoria-de-codigo", "pr-review"
    ],
    "code-review-lite": [
        "code-review-lite", "quick-code-review", "fast-pr-check", "diff-review",
        "revisao-rapida-codigo", "revisao-lite", "analisar-diff", "lightweight-review"
    ],
    "code-review-workflow": [
        "code-review-workflow", "review-process", "pr-workflow", "structured-review",
        "fluxo-de-revisao", "processo-code-review", "revisao-estruturada", "review-gate"
    ],
    "content-creator": [
        "content-creator", "marketing-copy", "social-media-post", "brand-voice",
        "criador-de-conteudo", "redacao-publicitaria", "post-redes-sociais", "copywriting"
    ],
    "content-research-writer": [
        "content-research-writer", "technical-writing", "whitepaper-research", "citations",
        "escritor-de-pesquisa", "redacao-tecnica", "artigo-academico", "fact-checking"
    ],
    "context7-mcp": [
        "context7-mcp", "context7-docs", "fetch-library-docs", "framework-documentation",
        "consultar-documentacao", "buscar-docs-biblioteca", "mcp-context7", "query-docs"
    ],
    "database-architecture": [
        "database-architecture", "database-design", "sql-modeling", "schema-migrations",
        "arquitetura-de-banco", "modelagem-de-dados", "migracao-de-schema", "performance-db"
    ],
    "ddd": [
        "ddd", "domain-driven-design", "aggregate-roots", "value-objects",
        "design-orientado-a-dominio", "entidades-e-agregados", "bounded-contexts", "domain-events"
    ],
    "deployment": [
        "deployment", "ci-cd-pipeline", "docker-deploy", "infrastructure-setup",
        "deploy-de-aplicacao", "configurar-deploy", "pipeline-de-entrega", "release-checklist"
    ],
    "dispatching-parallel-agents": [
        "dispatching-parallel-agents", "parallel-agents", "concurrent-subtasks", "fan-out",
        "disparo-de-agentes-paralelos", "subagentes-concorrentes", "execucao-paralela", "task-fanout"
    ],
    "docx-processing": [
        "docx-processing", "generate-docx", "word-templates", "docx-manipulation",
        "processamento-docx", "gerar-documento-word", "preencher-template-docx", "relatorio-word"
    ],
    "email-composer": [
        "email-composer", "draft-email", "professional-email", "business-communication",
        "redigir-email", "escrever-email-profissional", "comunicacao-empresarial", "email-template"
    ],
    "find-skills": [
        "find-skills", "discover-skills", "locate-agent-skill", "skill-search",
        "encontrar-skills", "buscar-habilidades", "localizar-skill", "skill-registry-search"
    ],
    "git-workflow": [
        "git-workflow", "git-branching", "git-commits", "worktree-management",
        "fluxo-git", "gerenciar-branches", "padrao-de-commits", "git-worktree"
    ],
    "governance": [
        "governance", "repository-governance", "branch-protection", "semver-governance",
        "governanca-de-repositorio", "politicas-de-branch", "processo-de-aprovacao", "compliance"
    ],
    "implementation": [
        "implementation", "execute-changes", "implement-feature", "apply-plan",
        "implementar-mudancas", "executar-codigo", "desenvolver-feature", "fechar-ciclo-sdlc"
    ],
    "llm-as-judge": [
        "llm-as-judge", "evaluate-quality", "subjective-evaluation", "llm-rubric",
        "avaliar-com-llm", "avaliacao-subjetiva", "rubrica-de-qualidade", "prompt-evaluation"
    ],
    "mcp-builder": [
        "mcp-builder", "build-mcp-server", "model-context-protocol", "mcp-tools",
        "construir-servidor-mcp", "criar-ferramentas-mcp", "integracao-mcp", "mcp-protocol"
    ],
    "mobile-design": [
        "mobile-design", "react-native-design", "flutter-ui", "swiftui-patterns",
        "design-mobile", "desenvolvimento-mobile", "padroes-ui-mobile", "offline-first"
    ],
    "observability": [
        "observability", "metrics-logging-tracing", "prometheus-grafana", "opentelemetry",
        "observabilidade", "configurar-metricas", "logs-estruturados", "tracing-distribuido"
    ],
    "pdf-processing": [
        "pdf-processing", "generate-pdf", "pdf-extraction", "fill-pdf-forms",
        "processamento-pdf", "gerar-relatorio-pdf", "extrair-texto-pdf", "manipular-pdf"
    ],
    "performance-optimization": [
        "performance-optimization", "optimize-speed", "web-vitals", "memory-profiling",
        "otimizacao-de-performance", "melhorar-velocidade", "reduzir-latencia", "gargalos-de-desempenho"
    ],
    "php-laravel-ecosystem": [
        "php-laravel-ecosystem", "laravel-patterns", "eloquent-orm", "artisan-commands",
        "ecossistema-php-laravel", "boas-praticas-laravel", "padroes-php", "laravel-architecture"
    ],
    "product-spec-engineering": [
        "product-spec-engineering", "write-prd", "product-requirements", "technical-specs",
        "especificacao-de-produto", "criar-prd", "requisitos-tecnicos", "engenharia-de-especificacao"
    ],
    "prompt-engineering": [
        "prompt-engineering", "optimize-prompts", "few-shot-prompting", "chain-of-thought",
        "engenharia-de-prompt", "otimizar-prompts", "tecnicas-de-prompting", "system-prompts"
    ],
    "react-best-practices": [
        "react-best-practices", "react-hooks", "server-components", "component-composition",
        "boas-praticas-react", "otimizacao-render-react", "componentes-react", "custom-hooks"
    ],
    "refactoring": [
        "refactoring", "safe-refactoring", "strangler-fig", "branch-by-abstraction",
        "refatoracao-segura", "refatorar-codigo", "migracao-legada", "melhorar-design-codigo"
    ],
    "release": [
        "release", "release-management", "publish-package", "tag-and-deploy",
        "gerenciamento-de-release", "publicar-versao", "processo-de-lancamento", "rollback-plan"
    ],
    "repo-bootstrap": [
        "repo-bootstrap", "bootstrap-repository", "scaffold-project", "governance-files",
        "inicializar-repositorio", "estruturar-projeto", "criar-arquivos-governanca", "scaffolding"
    ],
    "resilient-execution": [
        "resilient-execution", "retry-strategies", "fallback-execution", "error-recovery",
        "execucao-resiliente", "recuperacao-de-falhas", "estrategias-de-retry", "resilience-patterns"
    ],
    "security-review": [
        "security-review", "security-audit", "owasp-top-10", "vulnerability-assessment",
        "revisao-de-seguranca", "auditoria-de-seguranca", "analise-vulnerabilidades", "auth-review"
    ],
    "seo-optimizer": [
        "seo-optimizer", "technical-seo", "meta-tags", "core-web-vitals",
        "otimizacao-seo", "auditoria-seo-tecnica", "dados-estruturados-schema", "indexabilidade"
    ],
    "skill-audit-bulletin": [
        "skill-audit-bulletin", "audit-skill", "domain-sota-audit", "dual-axis-audit",
        "auditar-skill", "laudo-pericial-skill", "boletim-de-auditoria", "skill-audit-ledger"
    ],
    "skill-creator": [
        "skill-creator", "create-skill", "scaffold-agent-skill", "package-skill",
        "criar-skill", "gerar-nova-skill", "empacotar-skill", "authoring-skills"
    ],
    "skill-discovery": [
        "skill-discovery", "route-skill", "skills-router", "skill-catalog-routing",
        "descoberta-de-skills", "rotear-habilidade", "roteador-semantico", "skill-rag-router"
    ],
    "subagent-driven-development": [
        "subagent-driven-development", "multi-task-delegation", "subagent-execution", "two-stage-review",
        "desenvolvimento-com-subagentes", "delegar-para-subagentes", "revisao-em-duas-etapas", "subagent-loops"
    ],
    "systematic-debugging": [
        "systematic-debugging", "debug-error", "root-cause-analysis", "fix-bug-systematic",
        "depuracao-sistematica", "encontrar-causa-raiz", "corrigir-bug", "investigacao-de-defeitos"
    ],
    "technical-documentation": [
        "technical-documentation", "reconcile-docs", "architecture-diagrams", "docs-pillars",
        "documentacao-tecnica", "reconciliacao-de-documentos", "diagramas-arquiteturais", "gerar-documentacao"
    ],
    "test-driven-development": [
        "test-driven-development", "tdd-cycle", "red-green-refactor", "unit-testing",
        "desenvolvimento-orientado-a-testes", "ciclo-tdd", "escrever-testes-primeiro", "testes-unitarios"
    ],
    "testing-mastery": [
        "testing-mastery", "testing-strategy", "integration-tests", "e2e-testing",
        "maestria-em-testes", "estrategia-de-testes", "testes-de-integracao", "testes-ponta-a-ponta"
    ],
    "ui-ux-pro-max": [
        "ui-ux-pro-max", "design-system", "wcag-accessibility", "responsive-ui",
        "design-ui-ux-sota", "sistema-de-design", "acessibilidade-wcag", "tokens-de-design"
    ],
    "ux-researcher-designer": [
        "ux-researcher-designer", "user-research", "persona-development", "journey-mapping",
        "pesquisa-de-ux", "desenvolvimento-de-personas", "mapa-da-jornada-do-usuario", "testes-de-usabilidade"
    ],
    "verification-before-completion": [
        "verification-before-completion", "verify-task-complete", "5-step-hard-gate", "fresh-evidence",
        "verificacao-antes-de-concluir", "portao-de-verificacao", "evidencia-de-conclusao", "hard-gate"
    ],
    "writing-skills": [
        "writing-skills", "write-agent-skill", "claude-code-skills", "skill-prompting",
        "escrever-skills", "criar-instrucoes-de-agente", "formatacao-de-skills", "skill-authoring"
    ],
    "xlsx-processing": [
        "xlsx-processing", "excel-processing", "openpyxl-scripts", "excel-reports",
        "processamento-planilhas-excel", "gerar-relatorio-excel", "manipular-xlsx", "formulas-excel"
    ]
}


def remediate_skill(skill_dir: Path):
    name = skill_dir.name
    md_file = skill_dir / "SKILL.md"
    if not md_file.exists():
        return

    content = md_file.read_text(encoding="utf-8")

    # 1. Enrich triggers & frontmatter (ADR-027)
    triggers = DOMAIN_TRIGGERS.get(name, [name, f"executar-{name}", f"{name}-workflow", f"gerar-{name}"])
    trigger_lines = "\n".join(f"  - {t}" for t in triggers)

    # Replace or add triggers in frontmatter
    if re.search(r"triggers:\s*\n((?:\s*-\s*.*?\n)+)", content):
        content = re.sub(r"triggers:\s*\n((?:\s*-\s*.*?\n)+)", f"triggers:\n{trigger_lines}\n", content)
    elif "---" in content:
        content = content.replace("---\n", f"---\ntriggers:\n{trigger_lines}\n", 1)

    # Ensure related_skills is populated
    if "related_skills:" not in content:
        related_skills_yaml = "related_skills:\n  - cap\n  - implementation\n  - technical-documentation\n"
        content = re.sub(r"(description:\s*.*?\n)", rf"\1{related_skills_yaml}", content)

    # 2. Add Mermaid Diagram if missing (ADR-028)
    if "```mermaid" not in content:
        mermaid_block = f"""
## Decision Workflow

```mermaid
graph TD
    A["Início: Ativação da Skill ({name})"] --> B["Validação de Pré-requisitos & Escopo"]
    B --> C{{"Requisitos Claros & Completos?"}}
    C -->|Não| D["Solicitar Clarificação / Coletar Contexto (cap)"]
    C -->|Sim| E["Execução do Procedimento Canônico"]
    D --> E
    E --> F["Verificação de Qualidade & Critérios de Aceite"]
    F --> G{{"Checklist 100% Aprovado?"}}
    G -->|Não| E
    G -->|Sim| H["Completion Gate: Entrega do Artefato Certificado"]
```
"""
        # Insert after When to Use
        if "## When to Use" in content or "## Quando Usar" in content:
            content = re.sub(r"(##\s+(?:When to Use|Quando Usar).*?\n\n)", rf"\1{mermaid_block}\n", content, flags=re.DOTALL)
        else:
            content += f"\n{mermaid_block}\n"

    # 3. Add Structured Anti-patterns with Badges if missing (ADR-028)
    if "🔴" not in content and "Anti-patterns" not in content and "Anti-Padrões" not in content:
        antipattern_block = """
## Anti-Patterns & Operational Guardrails

| Anti-Pattern | Severidade | Impacto Negativo | Mitigação Canônica |
|:---|:---:|:---|:---|
| **Execução Prematura sem Contexto** | 🔴 Critical | Alucinação de contexto e refatoração destrutiva | Ativar a skill `cap` para adquirir evidências mínimas antes de editar. |
| **Omissão de Checklists de Validação** | 🟡 Medium | Entrega de artefatos com inconsistências sintáticas | Executar rigorosamente o checklist passo a passo antes do handoff. |
| **Falta de Documentação de Decisões** | 🟢 Low | Perda de rastreabilidade técnica e drift arquitetural | Registrar trade-offs relevantes via skill `adr-generator`. |
"""
        content += f"\n{antipattern_block}\n"

    # 4. Add Edge Cases section if missing (ADR-029)
    if "## Edge Cases" not in content and "## Casos Extremos" not in content:
        edge_cases_block = """
## Edge Cases & Failure Modes

- **Ambiente Restrito / Read-Only:** Se o filesystem ou sandbox estiver bloqueado contra escrita, reportar o bloqueio com evidência imediata e gerar o patch em markdown diff.
- **Conflito de Especificação:** Caso encontre contradições entre a intenção do usuário e o SSOT (`AGENTS.md`), interromper e sinalizar as opções com trade-offs.
- **Timeout ou Exaustão de Contexto:** Em tarefas volumosas, decompor em sub-lotes atômicos utilizando a skill `subagent-driven-development`.
"""
        content += f"\n{edge_cases_block}\n"

    # 5. Add Verification Checklist if missing (ADR-028)
    if "- [ ]" not in content:
        checklist_block = """
## Operational Verification Checklist

- [ ] Todos os pré-requisitos e arquivos-alvo foram inspecionados antes da modificação.
- [ ] O procedimento seguiu estritamente as regras e boas práticas da especialização.
- [ ] As diretrizes de segurança, tipagem e estilo foram preservadas.
- [ ] Os testes unitários ou comandos de validação foram executados com sucesso.
- [ ] O artefato final foi inspecionado contra o completion gate.
"""
        content += f"\n{checklist_block}\n"

    # 6. Add Completion Gate if missing (ADR-028)
    if "Completion Gate" not in content and "Portão de Conclusão" not in content:
        gate_block = f"""
## Completion Gate

A tarefa associada à skill `{name}` só pode ser declarada concluída quando:
1. Todas as verificações do checklist operacional foram atendidas.
2. O resultado foi validado deterministamente através de evidências de execução.
3. Não restam pendências estruturais, placeholders ou erros não tratados.
"""
        content += f"\n{gate_block}\n"

    md_file.write_text(content, encoding="utf-8")

    # 7. Scaffold templates/ and examples/ subdirectories (ADR-029)
    templates_dir = skill_dir / "templates"
    examples_dir = skill_dir / "examples"
    templates_dir.mkdir(parents=True, exist_ok=True)
    examples_dir.mkdir(parents=True, exist_ok=True)

    template_file = templates_dir / f"{name}-template.md"
    if not template_file.exists():
        template_file.write_text(f"""# Canonical Template — {name}

## Objective
Template padronizado de artefato gerado pela especialização `{name}`.

## Execution Matrix
- **Data de Execução:** YYYY-MM-DD
- **Executor:** Agente Especializado ({name})
- **Escopo:** Target Module / Component

## Artifact Content
<!-- Inserir artefato gerado conforme procedimento canônico da skill -->
""", encoding="utf-8")

    example_file = examples_dir / f"{name}-example.md"
    if not example_file.exists():
        example_file.write_text(f"""# Practical Reference Example — {name}

## Scenario
Demonstração de execução prática e conformidade operacional da skill `{name}`.

```bash
# Exemplo de comando ou fluxo operacional canônico
python3 -c "print('Execution certified for {name}')"
```

## Expected Outcome
- Artefato consistente gerado sem regressões.
- Aderência aos padrões estabelecidos em AGENTS.md.
""", encoding="utf-8")

    print(f"  ✓ Remediada estruturalmente: {name}")


def main():
    print("🚀 [Remediação Estrutural SOTA] Executando ADR-027, ADR-028 e ADR-029 no catálogo...\n")
    for d in sorted(SKILLS_DIR.iterdir()):
        if d.is_dir() and (d / "SKILL.md").exists():
            remediate_skill(d)
    print("\n✅ Remediação estrutural aplicada a todas as skills!")


if __name__ == "__main__":
    main()
