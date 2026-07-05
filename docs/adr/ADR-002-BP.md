# Blueprint: Refatoração de Skills para Ultra-High Quality Grade

> ADR-002 | Versão 1.0 | 2026-07-05

---

## 1. Visão Geral

### Objetivo
Elevar todas as 14 skills do repositório `ignite-agents-skills` de "documentação conceitativa" para "instruções acionáveis ultra-high quality grade" — instruções que um agente de IA possa consumir deterministicamente e produzir resultados verificáveis.

### Métricas de Sucesso

| Métrica | Antes | Depois |
|---------|-------|--------|
| Média de linhas por skill | 67 | ≥200 |
| Skills com templates externos | 1/14 | 14/14 |
| Skills com decision trees | 0/14 | 12/14* |
| Skills com workflows numerados | 0/14 | 14/14 |
| Skills com anti-patterns detalhados | 0/14 | 14/14 |
| Skills com checklists | 1/14 | 14/14 |
| Skills com cross-references | 0/14 | 14/14 |
| Skills com edge cases | 0/14 | 14/14 |
| Estrutura de diretório padronizada | 1/14 | 14/14 |

*Skills conceituais (vibe-coding) usam decision tree simplificada.

### Timeline Estimada

| Fase | Duração | Entregável |
|------|---------|------------|
| Fase 0: Infraestrutura | 2h | Template base, scripts de validação |
| Fase 1: Skills Core (6) | 12-18h | git, testing, governance, release, documentation, writing-plans |
| Fase 2: Skills de Domínio (4) | 10-14h | ddd, architecture-review, adr-generator, repo-bootstrap |
| Fase 3: Skills Conceituais (3) | 6-9h | vibe-coding, prompt-engineering, planning |
| Fase 4: Validação & Polish | 4-6h | Testes com agentes, ajustes finais |
| **Total** | **34-49h** | **14 skills refatoradas** |

---

## 2. Fase 0: Infraestrutura Base

### 2.1 Criar Template Base da Skill

**Arquivo:** `templates/skill-template.md`

O template unifica a estrutura de todas as skills, servindo como point of departure.

### 2.2 Criar Script de Validação

**Arquivo:** `scripts/validate-skill.sh`

Script que verifica:
- [ ] SKILL.md existe e tem ≥150 linhas
- [ ] Frontmatter válido (name, description, version, tags, related_skills)
- [ ] Seções obrigatórias presentes (Quando Usar, Workflow, Anti-patterns, Checklists, Edge Cases)
- [ ] Templates/ e examples/ existem
- [ ] Nenhum link quebrado

### 2.3 Atualizar index.json

Adicionar campos `version`, `tags`, `related_skills` ao registry.

### Tarefas

| # | Tarefa | Arquivos | Complexidade | Dependências |
|---|--------|----------|-------------|--------------|
| 0.1 | Criar `templates/skill-template.md` | templates/skill-template.md | M | — |
| 0.2 | Criar `scripts/validate-skill.sh` | scripts/validate-skill.sh | M | — |
| 0.3 | Atualizar schema do `index.json` | skills/index.json | S | — |
| 0.4 | Documentar processo de manutenção | docs/skill-maintenance.md | S | 0.1 |

---

## 3. Fase 1: Skills Core (6 skills)

Skills que definem workflows operacionais padrão para qualquer projeto.

### 3.1 git

**Arquivo:** `skills/git/SKILL.md`  
**Estado atual:** 68 linhas, 0 templates, 0 workflows  
**Alvo:** ~250 linhas, 3 templates, 4 workflows, decision tree

**Estrutura proposta:**
- Decision tree: merge vs rebase vs cherry-pick vs squash
- Workflow 1: Criar commit convencional (passo-a-passo com comandos)
- Workflow 2: Resolver conflito de merge
- Workflow 3: Fazer release via git flow
- Workflow 4: Limpar histórico (rebase interativo, squash, amend)
- Templates: `commit-message.md`, `branch-naming.md`, `pr-description.md`
- Anti-patterns: force push em shared branch, commit com segredos, mensagem vaga
- Edge cases: submodule, rebase com conflito em arquivo binário, detach HEAD
- Checklists: pre-commit, pre-merge, pre-release

### 3.2 testing

**Arquivo:** `skills/testing/SKILL.md`  
**Estado atual:** 65 linhas, 0 templates, 0 workflows  
**Alvo:** ~280 linhas, 4 templates, 5 workflows, decision tree

**Estrutura proposta:**
- Decision tree: qual tipo de teste para cada cenário
- Workflow 1: Escrever teste unitário (AAA com exemplos por linguagem)
- Workflow 2: Escrever teste de integração
- Workflow 3: Escrever teste E2E
- Workflow 4: Analisar cobertura e decidir próximos passos
- Workflow 5: Refatorar com testes como safety net
- Templates: `unit-test.ts`, `integration-test.ts`, `e2e-test.ts`, `test-plan.md`
- Anti-patterns: test leaky, mock excessivo, test sem assertion, test frágil
- Edge cases: teste dependente de ordem, flaky test, teste com I/O externo
- Checklists: review de teste, cobertura mínima, CI gate

### 3.3 governance

**Arquivo:** `skills/governance/SKILL.md`  
**Estado atual:** 65 linhas, 0 templates, 0 workflows  
**Alvo:** ~250 linhas, 3 templates, 4 workflows, decision tree

**Estrutura proposta:**
- Decision tree: GitFlow vs Trunk-Based vs GitHub Flow
- Workflow 1: Configurar branch protection
- Workflow 2: Configurar CODEOWNERS
- Workflow 3: Processo de PR (criação → review → merge)
- Workflow 4: Release management
- Templates: `pull-request-template.md`, `issue-template.md`, `codeowners`
- Anti-patterns: approve sem review, merge com CI vermelho, branch sem PR
- Edge cases: hotfix em produção, revert de release, contributor externo
- Checklists: PR checklist, release checklist, onboarding checklist

### 3.4 release

**Arquivo:** `skills/release/SKILL.md`  
**Estado atual:** 76 linhas, 0 templates, 0 workflows  
**Alvo:** ~240 linhas, 3 templates, 4 workflows, decision tree

**Estrutura proposta:**
- Decision tree: npm vs docker vs github release vs custom
- Workflow 1: Preparar release (version bump, changelog)
- Workflow 2: Validar release (testes, lint, build)
- Workflow 3: Publicar release
- Workflow 4: Rollback
- Templates: `changelog-entry.md`, `release-checklist.md`, `rollback-plan.md`
- Anti-patterns: release sem changelog, version skip, release sem testes
- Edge cases: release com breaking change não documentado, hotfix durante release
- Checklists: pre-release, post-release, rollback

### 3.5 documentation

**Arquivo:** `skills/documentation/SKILL.md`  
**Estado atual:** 60 linhas, 0 templates, 0 workflows  
**Alvo:** ~220 linhas, 4 templates, 4 workflows, decision tree

**Estrutura proposta:**
- Decision tree: README vs ADR vs API docs vs Architecture docs
- Workflow 1: Criar documentação de projeto
- Workflow 2: Escrever ADR
- Workflow 3: Documentar API
- Workflow 4: Revisar documentação existente
- Templates: `readme.md`, `adr.md`, `api-doc.md`, `architecture-doc.md`
- Anti-patterns: doc desatualizada, doc sem exemplos, doc duplicada
- Edge cases: doc para projeto legado, doc para microserviço vs monolito
- Checklists: review de doc, link checker, freshness check

### 3.6 writing-plans

**Arquivo:** `skills/writing-plans/SKILL.md`  
**Estado atual:** 68 linhas, 0 templates, 0 workflows  
**Alvo:** ~220 linhas, 2 templates, 3 workflows, decision tree

**Estrutura proposta:**
- Decision tree: plano de feature vs plano de refatoração vs plano de incidente
- Workflow 1: Criar plano de implementação (specs → tasks)
- Workflow 2: Estimar e priorizar (MoSCoW, RICE)
- Workflow 3: Acompanhar execução (burndown, blockers)
- Templates: `implementation-plan.md`, `task-card.md`
- Anti-patterns: plano sem critérios de aceitação, tarefa > 4h, dependência circular
- Edge cases: plano para spike/exploração, replanificação durante execução
- Checklists: quality gate do plano, review de estimativas

---

## 4. Fase 2: Skills de Domínio (4 skills)

Skills que cobrem tópicos técnicos profundos.

### 4.1 ddd

**Arquivo:** `skills/ddd/SKILL.md`  
**Estado atual:** 88 linhas, 0 templates, 0 workflows  
**Alvo:** ~350 linhas, 6 templates, 6 workflows, decision tree completa

**Estrutura proposta:**
- Decision tree: Entidade vs Value Object vs Aggregate vs Domain Event
- Workflow 1: Modelar domínio (event storming → Bounded Contexts → Aggregates)
- Workflow 2: Implementar Aggregate Root (com validação de invariants)
- Workflow 3: Implementar Domain Event (criação, publicação, handler)
- Workflow 4: Implementar Repository (interface + infraestrutura)
- Workflow 5: Definir Bounded Context e mapear integrações
- Workflow 6: Refatorar entidade anêmica para rica
- Templates: `entity.ts`, `value-object.ts`, `aggregate-root.ts`, `domain-event.ts`, `repository.ts`, `domain-service.ts`
- Anti-patterns: entidade anêmica, aggregate grosso, repository genérico, event como command
- Edge cases: aggregate com muitas entidades, evento que precisa de rollback, shared kernel
- Checklists: DDD modeling review, aggregate consistency, event schema validation

### 4.2 architecture-review

**Arquivo:** `skills/architecture-review/SKILL.md`  
**Estado atual:** 58 linhas, 0 templates, 0 workflows  
**Alvo:** ~300 linhas, 2 templates, 5 workflows, decision tree

**Estrutura proposta:**
- Decision tree: quando revisar arquitetura (PR, adoc, tech debt, scaling)
- Workflow 1: Revisão de PR com impacto arquitetural
- Workflow 2: Análise de estrutura de projeto
- Workflow 3: Detecção de code smells estruturais
- Workflow 4: Avaliação de aderência a padrões
- Workflow 5: Criar relatório de revisão
- Templates: `architecture-review-report.md`, `tech-debt-item.md`
- Anti-patterns: revisão superficial, focar em estilo而非estrutura, ignorar dependências circulares
- Edge cases: projeto legado sem testes, microserviço mal delimitado, monolito que precisa escalar
- Checklists: SOLID, Clean Architecture, DDD, performance, security

### 4.3 adr-generator

**Arquivo:** `skills/adr-generator/SKILL.md`  
**Estado atual:** 58 linhas (1 template externo)  
**Alvo:** ~200 linhas, template aprimorado, 3 workflows, decision tree

**Estrutura proposta:**
- Decision tree: quando criar ADR vs RFC vs Decision Doc
- Workflow 1: Criar ADR (contexto → alternativas → decisão → consequências)
- Workflow 2: Revisar ADR existente
- Workflow 3: Substituir ADR (status: Superseded)
- Template aprimorado: `templates/adr.md` (com campos extras: stakeholders, deadline, review date)
- Anti-patterns: ADR retrospectivo, ADR sem alternativas, ADR vago
- Edge cases: ADR de emergência, ADR para experimento temporário
- Checklists: ADR quality gate, review checklist

### 4.4 repo-bootstrap

**Arquivo:** `skills/repo-bootstrap/SKILL.md`  
**Estado atual:** 79 linhas, 0 templates, 0 workflows  
**Alvo:** ~240 linhas, 5 templates, 3 workflows, decision tree

**Estrutura proposta:**
- Decision tree: monorepo vs multi-repo,开源 vs interno, Node vs Python vs Go
- Workflow 1: Criar repositório do zero
- Workflow 2: Adicionar governança a repositório existente
- Workflow 3: Configurar CI/CD
- Templates: `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `.github/workflows/ci.yml`, `AGENTS.md`
- Anti-patterns: repositório sem LICENSE, sem .gitignore, sem CI
- Edge cases: fork de projeto externo, monorepo com múltiplas linguagens
- Checklists: repo completeness, CI pipeline, security basics

---

## 5. Fase 3: Skills Conceituais (3 skills)

Skills que orientam comportamento e mentalidade.

### 5.1 vibe-coding

**Arquivo:** `skills/vibe-coding/SKILL.md`  
**Estado atual:** 61 linhas, 0 templates, 0 workflows  
**Alvo:** ~200 linhas, 1 template, 3 workflows, decision tree

**Estrutura proposta:**
- Decision tree: vibe-coding vs pair programming vs code review
- Workflow 1: Briefing → Refinamento → Validação → Ajuste (ciclo iterativo)
- Workflow 2: Gerar scaffolding com IA
- Workflow 3: Refatorar com IA como copiloto
- Template: `vibe-session.md` (template de sessão de vibe coding)
- Anti-patterns: confiar 100% na IA, não revisar código gerado, prompts vagos
- Edge cases: código gerado com vulnerabilidades, performance degradada, dependências obsoletas
- Checklists: post-session review, security scan, test coverage

### 5.2 prompt-engineering

**Arquivo:** `skills/prompt-engineering/SKILL.md`  
**Estado atual:** 71 linhas, 0 templates, 0 workflows  
**Alvo:** ~250 linhas, 3 templates, 4 workflows, decision tree

**Estrutura proposta:**
- Decision tree: qual técnica de prompt para cada cenário
- Workflow 1: Criar prompt para tarefa simples
- Workflow 2: Criar prompt para tarefa complexa (com role, context, constraints)
- Workflow 3: Otimizar prompt (few-shot, chain-of-thought, structured output)
- Workflow 4: Avaliar qualidade de prompt
- Templates: `prompt-simple.md`, `prompt-complex.md`, `prompt-evaluation.md`
- Anti-patterns: prompt vago, múltiplas tarefas, instruções contraditórias
- Edge cases: prompt para código legado, prompt para documentação em língua estrangeira
- Checklists: prompt quality, output format, constraint completeness

### 5.3 planning

**Arquivo:** `skills/planning/SKILL.md`  
**Estado atual:** 55 linhas, 0 templates, 0 workflows  
**Alvo:** ~220 linhas, 3 templates, 4 workflows, decision tree

**Estrutura proposta:**
- Decision tree: qual framework de priorização (MoSCoW, RICE, WSJF, Kano)
- Workflow 1: Decompor iniciativa em épico/features/tasks
- Workflow 2: Estimar esforço (T-shirt, Planning Poker, Story Points)
- Workflow 3: Priorizar backlog
- Workflow 4: Criar roadmap visual
- Templates: `epic-card.md`, `feature-card.md`, `task-card.md`
- Anti-patterns: task sem critério de aceitação, estimativa sem base, dependência circular
- Edge cases: projeto sem histórico, estimativa para tecnologia nova, scope creep
- Checklists: decomposition quality, estimation confidence, dependency validation

---

## 6. Fase 4: Validação & Polish

### 6.1 Validação com Agentes

Testar cada skill refatorada com um agente (Kilo Code ou similar) para verificar:
- O agente consegue seguir o workflow?
- O resultado esperado é produzido?
- As seções de edge case são acionadas quando apropriado?

### 6.2 Validação Automatizada

Executar `scripts/validate-skill.sh` em todas as skills:
```bash
for skill in skills/*/; do
  bash scripts/validate-skill.sh "$skill"
done
```

### 6.3 Atualização do index.json

Garantir que todas as 14 skills estão registradas com os novos campos.

### 6.4 Documentação de Manutenção

Atualizar `docs/skill-maintenance.md` com:
- Como criar uma nova skill seguindo o padrão
- Como modificar uma skill existente
- Processo de review

### Tarefas

| # | Tarefa | Arquivos | Complexidade | Dependências |
|---|--------|----------|-------------|--------------|
| 4.1 | Testar cada skill com agente | — | L | Fase 1-3 |
| 4.2 | Executar validação automatizada | — | S | 0.2 |
| 4.3 | Atualizar index.json final | skills/index.json | S | Fase 1-3 |
| 4.4 | Documentar manutenção | docs/skill-maintenance.md | M | 0.4 |
| 4.5 | Ajustes finais | various | M | 4.1 |

---

## 7. Priorização & Sequenciamento

### Ordem de Execução Recomendada

```
Fase 0 (Infraestrutura)
  │
  ├─── 0.1 Template base ────────────────────┐
  ├─── 0.2 Script de validação ──────────────┤
  ├─── 0.3 Schema do index.json ─────────────┤
  └─── 0.4 Doc de manutenção ────────────────┘
                                              │
Fase 1 (Core) ◄──────────────────────────────┘
  │
  ├─── 1.1 git (referência para todas)
  ├─── 1.2 testing (referência para todas)
  ├─── 1.3 governance (depois de git)
  ├─── 1.4 release (depois de governance)
  ├─── 1.5 documentation (independente)
  └─── 1.6 writing-plans (independente)
  │
Fase 2 (Domínio)
  │
  ├─── 2.1 ddd (complexa, fazer primeiro)
  ├─── 2.2 architecture-review (depois de ddd)
  ├─── 2.3 adr-generator (independente)
  └─── 2.4 repo-bootstrap (independente)
  │
Fase 3 (Conceitual)
  │
  ├─── 3.1 prompt-engineering (independente)
  ├─── 3.2 planning (independente)
  └─── 3.3 vibe-coding (última, mais simples)
  │
Fase 4 (Validação)
  │
  ├─── 4.1 Testar com agentes
  ├─── 4.2 Validação automatizada
  ├─── 4.3 Atualizar index.json
  ├─── 4.4 Doc de manutenção
  └─── 4.5 Ajustes finais
```

### Dependências Críticas

1. **Template base (0.1)** deve ser aprovado antes de iniciar qualquer skill
2. **git (1.1)** deve ser aprovado como referência de qualidade antes de paralelizar
3. **ddd (2.1)** deve ser concluído antes de architecture-review (2.2)
4. **Todas as skills** devem ser concluídas antes da Fase 4

### Critérios de Aprovação por Skill

Para cada skill ser considerada "aprovada":

- [ ] SKILL.md ≥ 150 linhas com conteúdo acionável
- [ ] Frontmatter completo (name, description, version, tags, related_skills)
- [ ] Decision tree presente (ou justificativa para ausência)
- [ ] ≥ 3 workflows numerados com checkpoints
- [ ] ≥ 3 anti-patterns com severidade e exemplos antes/depois
- [ ] Checklist de validação
- [ ] ≥ 1 edge case documentado
- [ ] ≥ 1 template em arquivo separado
- [ ] ≥ 1 cross-reference para skill relacionada
- [ ] Script validate-skill.sh passa

---

## 8. Riscos e Mitigações

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Skills ficam complexas demais para agentes | Alto | Média | Progressive Disclosure: seção concisa + detalhes opcionais |
| Manutenção futura muito custosa | Médio | Alta | Template padronizado + script de validação + doc de manutenção |
| Algumas skills não se beneficiam de templates | Baixo | Alta | Adaptar estrutura: skills conceituais focam em exemplos e decision trees |
| Inconsistência entre skills refatoradas | Médio | Baixa | Template único + validação automatizada |
| Aprovação do template base atrasa tudo | Alto | Baixa | Template v1 simples, refinar depois |

---

## 9. Anexo: Estimativas Detalhadas por Skill

| Skill | Linhas Atual | Linhas Alvo | Templates | Workflows | Anti-patterns | Horas Est. |
|-------|-------------|-------------|-----------|-----------|---------------|------------|
| git | 68 | ~250 | 3 | 4 | 5+ | 2-3h |
| testing | 65 | ~280 | 4 | 5 | 5+ | 2-3h |
| governance | 65 | ~250 | 3 | 4 | 4+ | 2-3h |
| release | 76 | ~240 | 3 | 4 | 4+ | 2-3h |
| documentation | 60 | ~220 | 4 | 4 | 4+ | 2-3h |
| writing-plans | 68 | ~220 | 2 | 3 | 3+ | 2-3h |
| ddd | 88 | ~350 | 6 | 6 | 6+ | 4-5h |
| architecture-review | 58 | ~300 | 2 | 5 | 5+ | 3-4h |
| adr-generator | 58 | ~200 | 1 (update) | 3 | 3+ | 2-3h |
| repo-bootstrap | 79 | ~240 | 5 | 3 | 3+ | 2-3h |
| vibe-coding | 61 | ~200 | 1 | 3 | 4+ | 2h |
| prompt-engineering | 71 | ~250 | 3 | 4 | 4+ | 2-3h |
| planning | 55 | ~220 | 3 | 4 | 3+ | 2-3h |
| **Total** | **872** | **~3,220** | **40** | **52** | **55+** | **29-41h** |

---

*Documento gerado em 2026-07-05. Referência: ADR-002.*
