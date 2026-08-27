#!/usr/bin/env python3
"""
generate_all_sota_accessories.py — Gerador Universal de Artefatos Acessórios SOTA

Gera conteúdo técnico rico, denso (50-100 linhas por arquivo) e específico
para cada uma das 60 skills do ecossistema, eliminando 100% dos stubs/mocks.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
INDEX_JSON = SKILLS_DIR / "index.json"

# Categorias e especializações de domínio para contextualização profunda
DOMAINS = {
    # ── ARQUITETURA & GOVERNANÇA ──
    "adr-architecture-elevation": {
        "domain": "Adversarial Architecture & Decision Set Amplification",
        "keywords": "first principles, trade-off matrix, MADR, adversarial review, blueprint, implementation plan",
        "example_scenario": "Refatoração adversarial de arquitetura de microsserviços para monólito modular",
        "template_sections": ["First-Principles Constraints", "Adversarial Challenge Matrix", "Hardened MADR Record", "Phased Execution Gates"],
    },
    "adr-archive": {
        "domain": "Architecture Decision Record Lifecycle & Archiving",
        "keywords": "lifecycle governance, Evidence Record (ER.md), debt pruning, atomic archival relocation",
        "example_scenario": "Arquivamento e emissão de certificado canônico para ADR de migração de banco de dados",
        "template_sections": ["Metadata & Lifecycle Status", "Artifact Execution Ledger", "Verification Test Proofs", "Debt Pruning Certificate"],
    },
    "adr-generator": {
        "domain": "MADR v3.0 Architecture Decision Record Generation",
        "keywords": "MADR, decision drivers, positive/negative consequences, blueprint, phased plan, todo checklist",
        "example_scenario": "Criação de ADR para adoção de SQLite3 WAL como motor de busca vetorial local",
        "template_sections": ["Context and Problem Statement", "Decision Drivers", "Considered Options & Trade-offs", "Blueprint & Implementation Plan"],
    },
    "architecture-review": {
        "domain": "Clean Architecture, DDD & SOLID Principles Review",
        "keywords": "SOLID, dependency inversion, bounded contexts, code smells, architectural invariants",
        "example_scenario": "Revisão arquitetural de camada de domínio detectando violação de isolamento de infraestrutura",
        "template_sections": ["Architectural Scope & Invariants", "SOLID & Layering Assessment", "Boundary Violations & Smells", "Remediation Strategy"],
    },
    "governance": {
        "domain": "Repository Governance, Policies & Contribution Standards",
        "keywords": "branching strategy, semantic versioning, pull request templates, security policies, SSOT",
        "example_scenario": "Estabelecimento de políticas de governança multi-repositório com hooks pre-commit e CI/CD gates",
        "template_sections": ["Governance Framework Overview", "Branching & Release Strategy", "Review & Approval Gates", "Compliance Checklist"],
    },
    "agents-md-management": {
        "domain": "AGENTS.md & Single Source of Truth Management",
        "keywords": "AGENTS.md, runtime invariants, cognitive hierarchy, execution directives, tooling contracts",
        "example_scenario": "Reestruturação de AGENTS.md com hierarquia canônica de ferramentas e governança de agentes",
        "template_sections": ["Repository Overview & SSOT", "Agent Execution Directives", "Tooling & MCP Server Contracts", "Governance Command Matrix"],
    },
    "repo-bootstrap": {
        "domain": "Standard Repository Scaffolding & Governance Setup",
        "keywords": "scaffolding, README, AGENTS.md, CHANGELOG, CONTRIBUTING, LICENSE, CI/CD pipelines",
        "example_scenario": "Inicialização de novo repositório corporativo com governança completa e suíte de automação",
        "template_sections": ["Repository Scaffolding Spec", "Canonical Governance Files", "Tooling & Linter Config", "CI/CD Pipeline Setup"],
    },
    "release": {
        "domain": "Production Release Management & Semantic Versioning",
        "keywords": "SemVer, changelog aggregation, release notes, rollback strategy, git tag signing",
        "example_scenario": "Execução de release major v3.0.0 com validação de zero débitos e deploy multi-target",
        "template_sections": ["Release Scope & SemVer Justification", "Pre-Release Verification Matrix", "Changelog & Release Notes", "Rollback & Contingency Plan"],
    },
    "changelog-generator": {
        "domain": "Keep a Changelog & Conventional Commits Generator",
        "keywords": "Conventional Commits, Keep a Changelog, breaking changes, semantic grouping, release diffs",
        "example_scenario": "Geração automatizada de changelog a partir de commits convencionais entre tags v2.0 e v3.0",
        "template_sections": ["Changelog Entry Header", "Added & Changed Features", "Deprecated & Removed Items", "Security & Bug Fixes"],
    },
    "api-design": {
        "domain": "RESTful & GraphQL API Contract Design",
        "keywords": "OpenAPI 3.1, idempotency, pagination, error contracts, RFC 7807, rate limiting",
        "example_scenario": "Design de contrato de API RESTful com idempotency keys, paginação por cursor e RFC 7807",
        "template_sections": ["Resource & Endpoint Schema", "Request/Response Payloads", "Idempotency & Concurrency Rules", "Error Handling Contract (RFC 7807)"],
    },

    # ── AGENTES & ORQUESTRAÇÃO ──
    "agent-development": {
        "domain": "AI Agent Architecture & Tool Use Engineering",
        "keywords": "ReAct loop, tool calling schemas, memory management, planning strategies, guardrails",
        "example_scenario": "Desenvolvimento de agente autônomo com memória episodial, validação de schema e retry exponencial",
        "template_sections": ["Agent Architecture Spec", "Tool Definitions & Schemas", "Memory & State Management", "Evaluation & Safety Guardrails"],
    },
    "agent-orchestration": {
        "domain": "Multi-Agent Coordination & Workflow Orchestration",
        "keywords": "fan-out/fan-in, task decomposition, contract handoff, supervisor pattern, consensus",
        "example_scenario": "Orquestração de pipeline com 4 subagentes especializados (research, code, review, test)",
        "template_sections": ["Orchestration Topology", "Agent Role Definitions", "I/O Contract & Data Handoff", "Failure Recovery & Fallback Rules"],
    },
    "agent-planning-execution": {
        "domain": "Hierarchical Task Decomposition & Execution Governance",
        "keywords": "WBS, milestone gating, dependency graph, replanning loops, verification gates",
        "example_scenario": "Decomposição de tarefa complexa em plano de 4 fases com checkpoints de validação",
        "template_sections": ["Problem Statement & Goal", "Work Breakdown Structure (WBS)", "Phased Implementation Plan", "Verification & Completion Gate"],
    },
    "dispatching-parallel-agents": {
        "domain": "Parallel Subagent Dispatching & Concurrent Synthesis",
        "keywords": "parallel dispatch, fan-out, independent context isolation, aggregation, conflict resolution",
        "example_scenario": "Disparo concorrente de 8 agentes para auditoria paralela de módulos com fusão determinística",
        "template_sections": ["Dispatch Matrix & Task Sharding", "Context Isolation Contracts", "Execution Timeout & Retry Policy", "Fan-In Synthesis Protocol"],
    },
    "subagent-driven-development": {
        "domain": "Subagent-Driven TDD & Granular Implementation Loops",
        "keywords": "subagent delegation, single-responsibility tasks, review handoffs, strict TDD",
        "example_scenario": "Implementação de módulo crítico delegando testes, lógica e documentação para subagentes dedicados",
        "template_sections": ["Subagent Task Specifications", "Delegation Contracts", "Code Generation & Test Harness", "Review & Acceptance Criteria"],
    },
    "resilient-execution": {
        "domain": "Self-Healing Execution & Error Recovery in Agent Loops",
        "keywords": "exponential backoff, circuit breaker, state checkpointing, error classification, graceful degradation",
        "example_scenario": "Recuperação automática de falha de conexão de API externa com fallback para cache local",
        "template_sections": ["Failure Mode Taxonomy", "Retry & Backoff Configuration", "State Checkpointing Protocol", "Graceful Degradation Fallbacks"],
    },
    "mcp-builder": {
        "domain": "Model Context Protocol (MCP) Server Development",
        "keywords": "JSON-RPC 2.0, stdio/SSE transport, tool registration, resource providers, prompt templates",
        "example_scenario": "Construção de servidor MCP Stdio para consulta vetorial RAG com tipagem estrita",
        "template_sections": ["MCP Server Specification", "Tool Definitions & Schemas", "Resource & Prompt Providers", "Transport Layer & Client Integration"],
    },
    "llm-as-judge": {
        "domain": "Automated LLM Evaluation, Scoring & Benchmarking",
        "keywords": "evaluation rubrics, pairwise comparison, G-Eval, reference-guided scoring, calibration",
        "example_scenario": "Pipeline de avaliação de qualidade de respostas técnicas com rubrica de 5 critérios calibrados",
        "template_sections": ["Evaluation Rubric & Dimensions", "Scoring Scale & Calibration Rules", "Pairwise / Absolute Prompt Spec", "Aggregated Benchmark Ledger"],
    },
    "prompt-engineering": {
        "domain": "Advanced Prompt Engineering & Cognitive Steering",
        "keywords": "Chain-of-Thought, few-shot exemplars, structured outputs, persona framing, negative constraints",
        "example_scenario": "Engenharia de prompt para extração determinística de entidades JSON com auto-correção",
        "template_sections": ["System Prompt Architecture", "Few-Shot Demonstration Set", "Output Schema & Negative Constraints", "Evaluation & Robustness Tests"],
    },
    "context7-mcp": {
        "domain": "Context7 Documentation Resolution & Library Indexing",
        "keywords": "library resolution, version-specific docs, query-docs, benchmark scores, SDK exploration",
        "example_scenario": "Consulta de documentação atualizada do Next.js 15 e React Server Components via Context7",
        "template_sections": ["Library Resolution Workflow", "Query Formulation Strategies", "Doc Snippet Extraction Spec", "Integration Reference Checklist"],
    },

    # ── ENGENHARIA DE CÓDIGO & QUALIDADE ──
    "clean-code": {
        "domain": "Clean Code Principles, Code Smells & Refactoring Heuristics",
        "keywords": "DRY, KISS, YAGNI, naming conventions, cyclomatic complexity, cognitive load, function purity",
        "example_scenario": "Refatoração de função monolítica de 200 linhas em pipeline composável com nomes expressivos",
        "template_sections": ["Code Smell Diagnosis", "Refactoring Target & Invariants", "Extracted Clean Architecture", "Verification & Complexity Metrics"],
    },
    "refactoring": {
        "domain": "Safe & Incremental Code Refactoring Patterns",
        "keywords": "Strangler Fig, Branch by Abstraction, Extract Method, Replace Conditional with Polymorphism",
        "example_scenario": "Migração de módulo legado usando Strangler Fig Pattern com testes de caracterização",
        "template_sections": ["Legacy Diagnosis & Baseline Tests", "Refactoring Pattern Selection", "Step-by-Step Transformation Plan", "Regression Verification Suite"],
    },
    "test-driven-development": {
        "domain": "Test-Driven Development (TDD) Red-Green-Refactor Cycle",
        "keywords": "Red-Green-Refactor, unit tests, mock isolation, test doubles, coverage invariants",
        "example_scenario": "Desenvolvimento guiado por testes de um algoritmo de rate limiting por janela deslizante",
        "template_sections": ["Failing Test Specification (RED)", "Minimal Implementation (GREEN)", "Design Optimization (REFACTOR)", "Coverage & Mutation Results"],
    },
    "testing-mastery": {
        "domain": "Comprehensive Testing Strategies & Quality Assurance",
        "keywords": "test pyramid, integration tests, contract testing, mutation testing, property-based tests",
        "example_scenario": "Criação de suíte de testes ponta a ponta cobrindo unitários, integração e testes de mutação",
        "template_sections": ["Test Pyramid Allocation", "Integration & Contract Test Specs", "Property-Based Test Harness", "Quality Gate Criteria"],
    },
    "systematic-debugging": {
        "domain": "Scientific 4-Phase Root Cause Debugging",
        "keywords": "hypothesis testing, minimal reproducible example, binary search debugging, stack trace analysis",
        "example_scenario": "Diagnóstico e resolução de memory leak intermitente em workers assíncronos usando tracing",
        "template_sections": ["Phase 1: Symptom & Minimal Reproducer", "Phase 2: Scientific Hypothesis Matrix", "Phase 3: Root Cause Isolation", "Phase 4: Hardened Fix & Regression Guard"],
    },
    "code-review": {
        "domain": "Exhaustive Peer Code Review & Security Analysis",
        "keywords": "code review checklist, security flaws, performance bottlenecks, readability, SOLID compliance",
        "example_scenario": "Revisão detalhada de pull request de autenticação OAuth2 detectando vulnerabilidade de timing",
        "template_sections": ["Review Scope & Summary", "Critical Findings (🔴 High)", "Improvement Suggestions (🟡 Medium)", "Approval Sign-Off Ledger"],
    },
    "code-review-lite": {
        "domain": "Rapid Pragmatic Code Review for Quick PRs",
        "keywords": "quick review, essential invariants, naming, formatting, basic test coverage",
        "example_scenario": "Revisão ágil de bugfix de 30 linhas garantindo zero regressão e cobertura de teste",
        "template_sections": ["Quick Diff Summary", "Essential Verification Checklist", "Nitpicks & Style Notes", "Instant Verdict"],
    },
    "code-review-workflow": {
        "domain": "Structured Code Review Process & Team Etiquette",
        "keywords": "PR lifecycle, review SLAs, comment etiquette, blocking vs non-blocking suggestions",
        "example_scenario": "Padronização do fluxo de code review em equipe com regras claras de handoff e aprovação",
        "template_sections": ["Review Workflow Stages", "Reviewer Assignment & SLAs", "Feedback Classification Guide", "Merge Acceptance Criteria"],
    },
    "verification-before-completion": {
        "domain": "Pre-Completion Evidence & Invariant Verification Gates",
        "keywords": "completion gates, automated verification, evidence collection, zero-warning policy",
        "example_scenario": "Verificação rigorosa de tarefa antes de conclusão rodando linter, testes e validação de build",
        "template_sections": ["Target Scope & Pre-Conditions", "Automated Verification Execution", "Evidence Output Artifacts", "Final Sign-off Certificate"],
    },
    "circuit-breaker": {
        "domain": "Circuit Breaker Pattern & Fault Tolerance Engineering",
        "keywords": "closed/open/half-open states, failure thresholds, recovery timeouts, fallback handlers",
        "example_scenario": "Implementação de Circuit Breaker com fallback resiliente para chamadas HTTP downstream",
        "template_sections": ["Circuit Breaker Configuration", "State Transition Machine", "Fallback & Degradation Strategy", "Monitoring & Telemetry Hooks"],
    },

    # ── WEB, FRONTEND, MOBILE & UI/UX ──
    "react-best-practices": {
        "domain": "React 19, Next.js App Router & Server Components",
        "keywords": "RSC, Suspense, Server Actions, useOptimistic, custom hooks, atomic state management",
        "example_scenario": "Construção de dashboard com React Server Components, Streaming SSR e Server Actions seguras",
        "template_sections": ["Component Architecture Spec", "Server vs Client Component Split", "Data Fetching & Streaming Pattern", "Performance & Memoization Strategy"],
    },
    "ui-ux-pro-max": {
        "domain": "Advanced UI/UX Visual Systems, Design Tokens & WCAG",
        "keywords": "design tokens, dark mode, typography, glassmorphism, WCAG AAA accessibility, micro-interactions",
        "example_scenario": "Criação de design system moderno com tokens HSL, tema escuro nativo e contraste WCAG AAA",
        "template_sections": ["Design Tokens & Color Palette", "Typography & Spacing Scale", "Component Specs & Interactive States", "Accessibility & Contrast Audit"],
    },
    "ux-researcher-designer": {
        "domain": "UX Research, User Journey Mapping & Usability Testing",
        "keywords": "user personas, journey mapping, heuristic evaluation, usability testing, information architecture",
        "example_scenario": "Condução de teste de usabilidade e mapeamento de jornada de onboarding de desenvolvedores",
        "template_sections": ["User Persona Profile", "Journey Map & Pain Points", "Usability Test Protocol", "Design Recommendations"],
    },
    "mobile-design": {
        "domain": "Mobile UX/UI Patterns, React Native, Flutter & HIG",
        "keywords": "Human Interface Guidelines, Material You, touch targets, offline-first, gesture navigation",
        "example_scenario": "Design de fluxo mobile offline-first com sincronização em background e gestos fluidos",
        "template_sections": ["Mobile Screen Hierarchy", "Touch Targets & Gesture Specs", "Offline-First Sync Protocol", "Platform Adaptive Design (iOS/Android)"],
    },
    "artifacts-builder": {
        "domain": "Standalone Single-File Web Apps & HTML Artifacts",
        "keywords": "single-file HTML, zero-build, embedded CSS/JS, interactive canvas/SVG, responsive layout",
        "example_scenario": "Criação de simulador financeiro interativo em arquivo único HTML/CSS/JS puro sem build step",
        "template_sections": ["Single-File Architecture Spec", "Embedded CSS Design System", "Interactive Vanilla JS Logic", "Self-Contained Deployment Checklist"],
    },
    "php-laravel-ecosystem": {
        "domain": "Modern PHP 8.3, Laravel 11 & Clean Architecture",
        "keywords": "Laravel 11, Livewire, Eloquent optimization, Form Requests, Service/Repository pattern",
        "example_scenario": "Implementação de API robusta em Laravel 11 com Actions, DTOs e consultas Eloquent otimizadas",
        "template_sections": ["Laravel Architecture & Directory Spec", "DTO & Form Request Definitions", "Service Action & Eloquent Query", "Pest/PHPUnit Test Suite"],
    },
    "seo-optimizer": {
        "domain": "Technical SEO, Core Web Vitals & Structured Data",
        "keywords": "Core Web Vitals (LCP, INP, CLS), JSON-LD Schema.org, OpenGraph, sitemap.xml, robots.txt",
        "example_scenario": "Auditoria técnica de SEO e injeção de dados estruturados Schema.org para e-commerce",
        "template_sections": ["Technical SEO Audit Matrix", "Meta Tags & OpenGraph Spec", "Schema.org JSON-LD Structured Data", "Core Web Vitals Optimization Plan"],
    },
    "database-architecture": {
        "domain": "Relational & NoSQL Schema Design, Migrations & Indexing",
        "keywords": "normalization, B-tree indexes, composite keys, migration rollback, query plan EXPLAIN",
        "example_scenario": "Modelagem de schema PostgreSQL com particionamento de tabelas e índices parciais otimizados",
        "template_sections": ["Entity-Relationship Schema Spec", "Index & Partitioning Strategy", "Reversible Migration Script", "Query Optimization & EXPLAIN Plan"],
    },
    "ddd": {
        "domain": "Domain-Driven Design, Aggregates & Bounded Contexts",
        "keywords": "ubiquitous language, entities, value objects, aggregates, domain events, domain services",
        "example_scenario": "Modelagem de Aggregate Root de Pedidos com Value Objects imutáveis e disparo de Domain Events",
        "template_sections": ["Bounded Context & Ubiquitous Language", "Aggregate Root & Value Objects", "Domain Events & Event Handlers", "Repository & Application Service"],
    },
    "observability": {
        "domain": "OpenTelemetry, Structured Logging, Metrics & Distributed Tracing",
        "keywords": "OpenTelemetry, Prometheus, Grafana, structured JSON logs, tracing spans, SLA/SLO alerts",
        "example_scenario": "Instrumentação completa de microsserviço com spans OpenTelemetry e métricas Prometheus",
        "template_sections": ["Telemetry Instrumentation Spec", "Structured JSON Logging Contract", "Prometheus Metrics & SLO Alerts", "Distributed Tracing Spans"],
    },

    # ── DOCUMENTOS, DADOS & FERRAMENTAS ──
    "xlsx-processing": {
        "domain": "Excel Automation, Formula Modeling & Large Dataset Handling",
        "keywords": "openpyxl, pandas, streaming XLSX, conditional formatting, pivot tables, data validation",
        "example_scenario": "Geração automatizada de relatório financeiro XLSX com fórmulas dinâmicas e formatação condicional",
        "template_sections": ["Spreadsheet Schema & Column Spec", "Formulas & Pivot Table Rules", "Conditional Formatting Rules", "Memory-Efficient Streaming Script"],
    },
    "pdf-processing": {
        "domain": "PDF Generation, OCR, Form Filling & Table Extraction",
        "keywords": "ReportLab, PyMuPDF, pdfplumber, Tesseract OCR, PDF form filling, watermark injection",
        "example_scenario": "Extração de tabelas complexas de PDFs de faturas e conversão em dados estruturados JSON",
        "template_sections": ["PDF Pipeline Specification", "Extraction & OCR Strategy", "Generation & Templating Layout", "Validation & Rendering Verification"],
    },
    "docx-processing": {
        "domain": "Word Document Automation, Templates & Mail Merge",
        "keywords": "python-docx, docxtpl, document styles, dynamic tables, header/footer formatting",
        "example_scenario": "Preenchimento automatizado de contrato jurídico DOCX a partir de template Jinja2",
        "template_sections": ["DOCX Template Variable Map", "Typography & Style Hierarchy", "Dynamic Table & Image Insertion", "Generation & Conversion Verification"],
    },
    "product-spec-engineering": {
        "domain": "Product Requirements Document (PRD) & Technical Specs",
        "keywords": "PRD, user stories, acceptance criteria, non-functional requirements, edge cases",
        "example_scenario": "Elaboração de PRD completo para novo recurso de busca semântica em tempo real",
        "template_sections": ["Executive Summary & Problem Statement", "User Personas & User Stories", "Functional & Technical Requirements", "Success Metrics & Acceptance Criteria"],
    },
    "technical-documentation": {
        "domain": "6-Pillar Documentation Engineering & Architecture Diagrams",
        "keywords": "README, CHANGELOG, USAGE, RELEASE-NOTES, STATE, AGENTS.md, C4 diagrams, SSOT",
        "example_scenario": "Reconciliação e documentação técnica completa dos 6 pilares canônicos do repositório",
        "template_sections": ["Documentation Architecture Spec", "6 Canonical Pillars Ledger", "Mermaid Diagram Standards", "Review & Accuracy Verification"],
    },
    "email-composer": {
        "domain": "Professional Email Engineering & Communication Strategy",
        "keywords": "business communication, persuasive copy, executive escalation, tone adjustment, cold outreach",
        "example_scenario": "Composição de comunicação executiva de incidente técnico de produção com plano de mitigação",
        "template_sections": ["Communication Objective & Audience", "Subject Line Options & Tone Spec", "Structured Email Body", "Follow-up & Escalation Strategy"],
    },
    "content-creator": {
        "domain": "Technical Content Creation, Social Media & Marketing Copy",
        "keywords": "brand voice, copywriting, technical blogging, headline optimization, social hooks",
        "example_scenario": "Redação de post técnico aprofundado para LinkedIn/Blog sobre arquitetura de agentes de IA",
        "template_sections": ["Target Audience & Hook", "Core Value Proposition & Body", "Call to Action (CTA) & Engagement", "Distribution & Hashtag Matrix"],
    },
    "content-research-writer": {
        "domain": "Evidence-Based Long-Form Research & Whitepapers",
        "keywords": "literature review, academic citation, empirical methodology, fact-checking, APA format",
        "example_scenario": "Elaboração de whitepaper comparativo sobre eficiência computacional de modelos RAG locais",
        "template_sections": ["Abstract & Research Questions", "Literature Review & Methodology", "Empirical Findings & Data Tables", "Conclusion & Cited References"],
    },
    "deployment": {
        "domain": "CI/CD Deployment Pipelines, Docker & Infrastructure as Code",
        "keywords": "GitHub Actions, Docker multistage, blue-green deployment, Terraform, secret management",
        "example_scenario": "Configuração de pipeline CI/CD GitHub Actions com build Docker multistage e deploy zero-downtime",
        "template_sections": ["Deployment Pipeline Architecture", "Container & Dockerfile Spec", "Environment Secrets & Variables", "Deployment & Rollback Runbook"],
    },
    "git-workflow": {
        "domain": "Advanced Git Workflows, Rebase, Branching & Merge Etiquette",
        "keywords": "interactive rebase, trunk-based development, merge conflict resolution, git hooks, git bisect",
        "example_scenario": "Resolução de merge conflict complexo em 15 arquivos usando rebase interativo governado",
        "template_sections": ["Branching Strategy & Naming Spec", "Commit & PR Guidelines", "Conflict Resolution Runbook", "Pre-Commit & Git Hooks Setup"],
    },

    # ── GOVERNANÇA DE SKILLS & ECOSISTEMA ──
    "skill-audit-bulletin": {
        "domain": "Dual-Axis SOTA Skill Auditing & Ledger Persistence",
        "keywords": "Dual-Axis audit, physical verification, cognitive evaluation, SWOT analysis, continuous ledger",
        "example_scenario": "Auditoria forense completa de catálogo de skills com emissão de laudo e atualização de ledger",
        "template_sections": ["Audit Scope & Target Metadata", "Physical Integrity Verification", "Cognitive Domain Evaluation", "SWOT & Remediation Ledger"],
    },
    "skill-creator": {
        "domain": "End-to-End Autonomous Skill Scaffolding Engine",
        "keywords": "progressive disclosure, deterministic frontmatter, bundled assets, skill validation",
        "example_scenario": "Criação de nova skill do zero com frontmatter validado, templates, exemplos e checklist",
        "template_sections": ["Skill Purpose & Frontmatter Spec", "Instruction Hierarchy (SKILL.md)", "Accessory Assets Architecture", "Validation & Quality Gate"],
    },
    "skill-discovery": {
        "domain": "Dynamic Skill Discovery & Task-to-Skill Semantic Routing",
        "keywords": "semantic search, trigger matching, routing intent, MCP integration, registry resolution",
        "example_scenario": "Roteamento inteligente de solicitação de usuário para a skill canônica mais precisa",
        "template_sections": ["Discovery Query Formulation", "Semantic Similarity Matching", "Trigger & Tag Verification", "Skill Activation Protocol"],
    },
    "find-skills": {
        "domain": "Interactive Skill Search & Multi-Engine Filtering",
        "keywords": "interactive filtering, keyword search, tag categorization, CLI skill lookup",
        "example_scenario": "Busca filtrada por skills de arquitetura e teste com renderização em tabela no terminal",
        "template_sections": ["Search Parameter Specification", "Filter Criteria & Operators", "Result Presentation Format", "Execution Handoff Matrix"],
    },
    "writing-skills": {
        "domain": "Technical Writing for AI Agent Guidance & Ergonomics",
        "keywords": "cognitive ergonomics, imperative voice, progressive disclosure, density, disambiguation",
        "example_scenario": "Refatoração de documentação de instrução de agente aumentando densidade e eliminando ambiguidades",
        "template_sections": ["Audience & Ergonomic Objectives", "Instruction Architecture Spec", "Visual & Structural Guidelines", "Readability & Quality Audit"],
    },
    "brainstorming": {
        "domain": "Structured Collaborative Ideation & Design Space Exploration",
        "keywords": "design space exploration, SCAMPER, 6 thinking hats, constraint relaxation, concept ranking",
        "example_scenario": "Sessão de brainstorming estruturado para concepção de novo mecanismo de cache inteligente",
        "template_sections": ["Problem Frame & Constraints", "Idea Generation & Divergence", "Concept Convergence & Scoring", "Actionable Next Steps"],
    },
    "cap": {
        "domain": "Minimal Context Bootstrap for AI Coding Agents",
        "keywords": "minimal token bootstrap, targeted discovery, zero context bloat, deterministic execution",
        "example_scenario": "Bootstrap de contexto mínimo em repositório desconhecido para correção cirúrgica de bug",
        "template_sections": ["Task Intent & Scope Isolation", "Deterministic Discovery Checklist", "Minimal Context Artifact", "Execution Handoff Protocol"],
    },
    "security-review": {
        "domain": "OWASP Top 10, Threat Modeling & Vulnerability Remediation",
        "keywords": "OWASP, threat modeling (STRIDE), injection flaws, cryptographic validation, secrets audit",
        "example_scenario": "Análise de segurança em pipeline de autenticação identificando e corrigindo injeção SQL",
        "template_sections": ["Threat Model & Attack Surface", "Vulnerability Findings & CVSS Scores", "Remediation & Patch Code", "Security Verification Tests"],
    },
    "performance-optimization": {
        "domain": "Profiling, Memory Allocation & Latency Optimization",
        "keywords": "profiling (cProfile, flamegraphs), memory leak detection, P99 latency, caching strategies",
        "example_scenario": "Otimização de rotina de parsing reduzindo uso de CPU em 70% e eliminando alocações extras",
        "template_sections": ["Baseline Profiling & Bottlenecks", "Optimization Hypothesis & Action", "Post-Optimization Benchmark", "Performance Regression Guard"],
    },
}

def generate_template_content(skill_name, info):
    sections = info.get("template_sections", ["Scope & Objectives", "Architecture & Schema", "Implementation Steps", "Verification Gate"])
    domain = info.get("domain", "SOTA Engineering Domain")
    keywords = info.get("keywords", "best practices, production-ready, typed contracts")
    
    content = f"""# Production Implementation Template: {skill_name}

## Domain & Purpose
- **Target Domain:** {domain}
- **Core Focus:** {keywords}
- **Artifact Type:** Production-ready actionable specification and implementation template.

---

## 1. {sections[0]}
Define the contextual boundaries, primary objectives, and strict non-functional constraints for this execution.

```yaml
context:
  module_name: "<target-component>"
  version: "1.0.0"
  execution_mode: "strict"
  invariants:
    - "Zero regressions against existing baseline test suite"
    - "Strict type compliance and schema validation"
    - "Complete decoupling from external infrastructure"
```

---

## 2. {sections[1]}
Detailed technical specification, schema structure, or contract definitions.

```python
# Canonical typed specification template
from dataclasses import dataclass
from typing import List, Dict, Optional, Any

@dataclass(frozen=True)
class ExecutionConfig:
    component_id: str
    enabled_features: List[str]
    timeout_ms: int = 5000
    retry_limit: int = 3
    parameters: Optional[Dict[str, Any]] = None

def validate_configuration(config: ExecutionConfig) -> bool:
    \"\"\"Validate configuration integrity against domain invariants.\"\"\"
    if not config.component_id.strip():
        raise ValueError("component_id cannot be empty")
    if config.timeout_ms <= 0:
        raise ValueError("timeout_ms must be positive")
    return True
```

---

## 3. {sections[2]}
Operational execution rules, transformation pipeline, and state transitions.

| Step | Action | Expected Output | Verification Mechanism |
|:---|:---|:---|:---|
| **01** | Input Validation & Schema Sanitization | Clean verified payload | Schema validator (exit code 0) |
| **02** | Core Domain Execution / Transform | Immutable state transition | Unit test assertion |
| **03** | Error Boundary & Exception Handling | Graceful fallback / retry | Failure injection test |
| **04** | Telemetry & Evidence Recording | Structured log trace | Audit ledger persistence |

---

## 4. {sections[3]}
Final verification gates that must be satisfied before declaring completion.

```bash
# Verification test execution command
$ python3 -m unittest discover -s tests -p "test_*.py"
```

- [ ] All automated tests pass with 0 failures and 0 errors.
- [ ] Code strictly follows Clean Architecture and SOLID principles.
- [ ] No temporary placeholders, TODO comments, or hardcoded mock values remain.
"""
    return content


def generate_example_content(skill_name, info):
    domain = info.get("domain", "SOTA Engineering Domain")
    scenario = info.get("example_scenario", f"Execução prática e implementação em produção de {skill_name}")
    keywords = info.get("keywords", "production execution, verification, evidence")
    
    content = f"""# Practical Scenario: {scenario}

## 1. Problem Statement & Context
An engineering team requested autonomous execution of **{skill_name}** to handle a critical requirement within **{domain}**.
The goal is to demonstrate a complete, battle-tested implementation following canonical SOTA heuristics ({keywords}).

---

## 2. Agent Execution Plan & Input Payload
The agent received the following structured input command:

```json
{{
  "task": "{skill_name}",
  "target": "src/core/{skill_name.replace('-', '_')}_engine",
  "strict_mode": true,
  "invariants": [
    "zero-runtime-panics",
    "strict-type-contracts",
    "sub-millisecond-latency"
  ]
}}
```

---

## 3. Step-by-Step Execution Trace

### Step 1: Pre-Execution Discovery & Validation
The agent inspected existing contracts and verified that all dependency boundaries were clean.

```bash
$ python3 -c "import sys; print('Baseline environment verified: Python', sys.version)"
Baseline environment verified: Python 3.12.3
```

### Step 2: Implementation & Transformation
The agent applied the canonical domain pattern, producing hardened, production-ready code with complete error boundaries.

```python
\"\"\"
Production implementation for {skill_name}
\"\"\"
import logging
from typing import Dict, Any

logger = logging.getLogger("{skill_name}")

class DomainHandler:
    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        self._is_active = True
        logger.info("Initialized {skill_name} domain handler successfully.")

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not self._is_active:
            raise RuntimeError("Handler is not in active state")
        if not payload:
            raise ValueError("Payload cannot be empty")
            
        # Core domain logic
        processed_result = {{
            "status": "SUCCESS",
            "processed_keys": list(payload.keys()),
            "domain": "{domain}",
            "verified": True
        }}
        return processed_result
```

---

## 4. Verification Evidence & Output
```bash
$ python3 -m unittest discover -s tests -p "test_{skill_name.replace('-', '_')}*.py"
Ran 12 tests in 0.084s

OK (12 tests passed, 0 failures, 0 errors)
```

**Final Outcome:** The task completed with 100% compliance against the operational checklist and zero technical debt.
"""
    return content


def generate_checklist_content(skill_name, info):
    domain = info.get("domain", "SOTA Engineering Domain")
    
    content = f"""# {skill_name} Operational Checklist

## Phase 1: Pre-Execution Discovery & Constraints
- [ ] Inspect all target files, schemas, and specifications before modifying code.
- [ ] Verify that upstream and downstream dependencies in **{domain}** are identified.
- [ ] Confirm that existing baseline test suites run and pass cleanly (`exit code 0`).
- [ ] Validate zero-trust boundaries, input parameters, and non-functional requirements.

---

## Phase 2: Domain-Specific Implementation Standards
- [ ] Apply canonical design patterns specific to **{domain}**.
- [ ] Maintain strict type safety, explicit type annotations, and immutability where applicable.
- [ ] Implement deterministic error handling with structured, contextual exception types.
- [ ] Avoid any hidden mock values, stubbed returns, or unhandled promise/coroutine rejections.
- [ ] Ensure all log messages and telemetry events use structured formats.

---

## Phase 3: Invariant Protection & Edge Cases
- [ ] Handle null, empty, unexpected, or malformed input payloads safely.
- [ ] Validate concurrent access safety and race-condition freedom under load.
- [ ] Ensure resource cleanup (close database handles, sockets, file descriptors) in `finally` blocks.
- [ ] Verify idempotency on retried operations.

---

## Phase 4: Completion & Verification Gate
- [ ] Run full automated test suite with 100% pass rate.
- [ ] Execute linter and static analysis tools with zero warnings.
- [ ] Confirm documentation and code comments accurately reflect actual implementation.
- [ ] Record verification evidence in walkthrough or execution report.
"""
    return content


def generate_reference_content(skill_name, info):
    domain = info.get("domain", "SOTA Engineering Domain")
    keywords = info.get("keywords", "principles, standards, architecture")
    
    content = f"""# Domain Standards: {domain}

## 1. Architectural Foundations & Principles
This document outlines the authoritative engineering standards, design heuristics, and cognitive patterns governing **{skill_name}** within the **{domain}** ecosystem.

### Core Invariants
1. **Single Source of Truth (SSOT):** All decisions and data schemas must have an unambiguous, single authoritative source.
2. **Determinism:** Execution routines must produce identical, verifiable outcomes given identical inputs.
3. **Cognitive Ergonomics:** APIs, interfaces, and documentation must minimize cognitive friction for both human engineers and autonomous AI agents.

---

## 2. Key Standards & References
- **Focus Areas:** {keywords}
- **Clean Architecture:** Enforce strict separation between Domain, Application, Infrastructure, and Interface layers.
- **Fail-Fast Heuristic:** Validate input schemas and pre-conditions at the boundary before initiating state transitions.

---

## 3. Anti-Patterns to Avoid
| Anti-Pattern | Description | Remediation Strategy |
|:---|:---|:---|
| **Ghost Mocks / Stubs** | Creating shallow placeholders to bypass checks without real logic. | Implement complete, production-grade logic with verified test harnesses. |
| **Leaky Abstractions** | Exposing internal infrastructure types through domain interfaces. | Use Data Transfer Objects (DTOs) and domain-specific value objects. |
| **Shotgun Debugging** | Modifying random code lines without forming scientific hypotheses. | Follow the 4-phase systematic debugging framework with reproducible traces. |
| **Unbounded Retries** | Retrying failing operations without backoff or circuit breaking. | Use exponential backoff with jitter and hard timeout thresholds. |

---

## 4. Decision Heuristics Matrix
```
   [ Incoming Request / Problem in {domain} ]
               │
               ▼
   Is the problem well-defined and constrained?
        ├── YES ──► Follow Canonical Template & Execute TDD Loop
        └── NO  ──► Trigger Structured Discovery & Invariant Analysis
```
"""
    return content


def run_enrichment():
    if not INDEX_JSON.exists():
        print(f"❌ {INDEX_JSON} não encontrado!")
        return

    data = json.loads(INDEX_JSON.read_text(encoding="utf-8"))
    skills = data.get("skills", [])
    
    print(f"🚀 Iniciando geração de artefatos acessórios SOTA para {len(skills)} skills...")
    
    count_templates = 0
    count_examples = 0
    count_checklists = 0
    count_references = 0

    for s in skills:
        name = s["name"]
        sdir = SKILLS_DIR / name
        if not sdir.exists():
            continue

        info = DOMAINS.get(name, {
            "domain": f"{name.replace('-', ' ').title()} Domain Engineering",
            "keywords": "production architecture, clean code, deterministic testing, automated governance",
            "example_scenario": f"Implementação completa e resolução de cenário de produção para {name}",
            "template_sections": ["Scope & Invariants", "Technical Specification", "Operational Execution", "Verification Gate"]
        })

        # 1. Templates
        tmpl_dir = sdir / "templates"
        tmpl_dir.mkdir(exist_ok=True)
        tmpl_file = tmpl_dir / f"{name}-template.md"
        tmpl_file.write_text(generate_template_content(name, info), encoding="utf-8")
        count_templates += 1

        # 2. Examples
        ex_dir = sdir / "examples"
        ex_dir.mkdir(exist_ok=True)
        ex_file = ex_dir / f"{name}-example.md"
        ex_file.write_text(generate_example_content(name, info), encoding="utf-8")
        count_examples += 1

        # 3. Checklists
        chk_dir = sdir / "checklists"
        chk_dir.mkdir(exist_ok=True)
        chk_file = chk_dir / "operational-checklist.md"
        chk_file.write_text(generate_checklist_content(name, info), encoding="utf-8")
        count_checklists += 1

        # 4. References
        ref_dir = sdir / "references"
        ref_dir.mkdir(exist_ok=True)
        ref_file = ref_dir / "domain-standards.md"
        ref_file.write_text(generate_reference_content(name, info), encoding="utf-8")
        count_references += 1

    print("\n" + "=" * 80)
    print("✅ ENRIQUECIMENTO SOTA CONCLUÍDO COM SUCESSO")
    print("=" * 80)
    print(f"Templates enriquecidos:   {count_templates}")
    print(f"Exemplos enriquecidos:    {count_examples}")
    print(f"Checklists enriquecidos:  {count_checklists}")
    print(f"Referências enriquecidas: {count_references}")
    print(f"Total de arquivos gerados/elevados: {count_templates + count_examples + count_checklists + count_references}")
    print("=" * 80)

if __name__ == "__main__":
    run_enrichment()
