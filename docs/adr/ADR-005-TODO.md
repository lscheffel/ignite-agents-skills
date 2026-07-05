# TODO: Implementação da Skill `implementation` — Execução Governada de Mudanças

> ADR-005 | Início: 2026-07-05 | Status: PENDENTE

---

## Legenda

- ⬜ Pendente
- 🔄 Em Andamento
- ✅ Concluído
- ❌ Bloqueado
- ⏸️ Pausado

**Prioridade:** 🔴 Alta | 🟡 Média | 🟢 Baixa

---

## Fase A: Estrutura Base

### A1: Criar diretório e estrutura de pastas

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| A1.1 | Criar diretório `skills/implementation/` | ⬜ | 🔴 | — | 1min |
| A1.2 | Criar subdiretório `skills/implementation/templates/` | ⬜ | 🔴 | A1.1 | 1min |
| A1.3 | Criar subdiretório `skills/implementation/examples/` | ⬜ | 🔴 | A1.1 | 1min |
| A1.4 | Criar subdiretório `skills/implementation/checklists/` | ⬜ | 🔴 | A1.1 | 1min |

**Checkpoint A1:**
- [ ] Estrutura de pastas criada conforme diagrama

---

### A2: Criar templates (5 arquivos)

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| A2.1 | Criar `templates/execution-contract.md` | ⬜ | 🔴 | A1.2 | 10min |
| A2.2 | Criar `templates/execution-report.md` | ⬜ | 🔴 | A1.2 | 10min |
| A2.3 | Criar `templates/change-plan.md` | ⬜ | 🔴 | A1.2 | 10min |
| A2.4 | Criar `templates/rollback-report.md` | ⬜ | 🟡 | A1.2 | 8min |
| A2.5 | Criar `templates/task-progress.md` | ⬜ | 🟡 | A1.2 | 8min |

**Checkpoint A2:**
- [ ] 5 templates criados com placeholders `{{placeholder}}`
- [ ] Cada template instrutivo e autocontido

---

### A3: Criar examples (2 arquivos)

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| A3.1 | Criar `examples/simple-change.md` — exemplo de mudança pontual (1-2 tarefas) | ⬜ | 🟡 | A2 | 15min |
| A3.2 | Criar `examples/complex-change.md` — exemplo de mudança multi-ADR (10+ tarefas) | ⬜ | 🟡 | A2 | 20min |

**Checkpoint A3:**
- [ ] Exemplo simples mostra fluxo completo: ADR → Contract → 1-2 tarefas → Report
- [ ] Exemplo complexo mostra DAG, paralelismo, rollback parcial

---

### A4: Criar checklists (2 arquivos)

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| A4.1 | Criar `checklists/pre-execution.md` | ⬜ | 🔴 | A1.4 | 8min |
| A4.2 | Criar `checklists/post-execution.md` | ⬜ | 🔴 | A1.4 | 8min |

**Checkpoint A4:**
- [ ] Pre-execution: ≥10 itens verificáveis
- [ ] Post-execution: ≥10 itens verificáveis

---

**Checkpoint Geral Fase A:**
- [ ] Estrutura de pastas completa
- [ ] 5 templates, 2 examples, 2 checklists criados
- [ ] Todos os artefatos são reutilizáveis e autoexplicativos

---

## Fase B: SKILL.md

### B1: Frontmatter e seções introdutórias

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| B1.1 | Criar frontmatter (name, description, version, tags, related_skills) | ⬜ | 🔴 | — | 3min |
| B1.2 | Criar parágrafo de contexto (o que é e por que existe) | ⬜ | 🔴 | B1.1 | 5min |
| B1.3 | Criar seção "Quando Usar" (Use quando / Não use quando / Skills relacionadas) | ⬜ | 🔴 | B1.2 | 5min |

**Checkpoint B1:**
- [ ] Frontmatter válido
- [ ] Descrição ≤200 caracteres
- [ ] `related_skills` inclui: `adr-generator`, `writing-plans`, `testing`, `git`, `documentation`

---

### B2: Decision Tree

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| B2.1 | Criar decision tree em Mermaid (fluxo completo: ADR → Blueprint → TODO → Contract → Execution) | ⬜ | 🔴 | B1 | 15min |
| B2.2 | Incluir ramos para "não existe ADR", "não existe Blueprint", "contract falha" | ⬜ | 🔴 | B2.1 | 5min |

**Checkpoint B2:**
- [ ] Decision tree cobre todos os caminhos
- [ ] Mermaid renderiza corretamente

---

### B3: Conceitos Fundamentais

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| B3.1 | Documentar conceito "Execution Contract" (definição, campos, regras) | ⬜ | 🔴 | B1 | 10min |
| B3.2 | Documentar conceito "Artifact Resolution" (algoritmo, entrada, saída) | ⬜ | 🔴 | B1 | 10min |
| B3.3 | Documentar conceito "Execution Loop" (ciclo, regras, diagrama) | ⬜ | 🔴 | B1 | 10min |
| B3.4 | Documentar conceito "Change Lifecycle" (transições, validações) | ⬜ | 🔴 | B1 | 10min |

**Checkpoint B3:**
- [ ] 4 conceitos documentados com definição precisa
- [ ] Cada conceito tem diagrama ou exemplo

---

### B4: Workflows (8 workflows)

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| B4.1 | Workflow 1: Artifact Resolution (10 passos + checkpoint) | ⬜ | 🔴 | B3 | 15min |
| B4.2 | Workflow 2: Execution Contract (11 passos + checkpoint) | ⬜ | 🔴 | B3 | 15min |
| B4.3 | Workflow 3: Dependency Analysis & Execution Plan (9 passos + checkpoint) | ⬜ | 🔴 | B3 | 15min |
| B4.4 | Workflow 4: Incremental Execution (10 passos + checkpoint) | ⬜ | 🔴 | B3 | 20min |
| B4.5 | Workflow 5: Continuous Validation (7 passos) | ⬜ | 🔴 | B3 | 10min |
| B4.6 | Workflow 6: Documentation Synchronization (8 passos + checkpoint) | ⬜ | 🔴 | B3 | 10min |
| B4.7 | Workflow 7: Progress Tracking (5 estados + regras) | ⬜ | 🔴 | B3 | 10min |
| B4.8 | Workflow 8: Execution Report (campos do relatório) | ⬜ | 🔴 | B3 | 10min |

**Checkpoint B4:**
- [ ] 8 workflows documentados
- [ ] Cada workflow tem passos numerados
- [ ] Cada workflow tem checkpoint explícito
- [ ] ≥5 workflows com ≥5 passos

---

### B5: Anti-patterns

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| B5.1 | Criar 3 anti-patterns 🔴 Crítico (sem contract, big bang, ignorar falha) | ⬜ | 🔴 | B1 | 15min |
| B5.2 | Criar 2 anti-patterns 🟡 Médio (código sem docs, ordem incorreta) | ⬜ | 🔴 | B1 | 10min |
| B5.3 | Criar 2 anti-patterns 🟢 Baixo (sem report, estimativas otimistas) | ⬜ | 🟡 | B1 | 8min |

**Checkpoint B5:**
- [ ] ≥3 anti-patterns 🔴
- [ ] ≥2 anti-patterns 🟡
- [ ] ≥2 anti-patterns 🟢
- [ ] Cada um com: o que é, por que é ruim, como evitar, exemplo antes/depois

---

### B6: Checklists e Edge Cases

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| B6.1 | Criar seção "Checklists" no SKILL.md (referência aos checklists externos) | ⬜ | 🔴 | A4 | 5min |
| B6.2 | Criar 5 edge cases (ADR proposta, Blueprint incompleto, TODO desatualizado, múltiplas ADRs, rollback) | ⬜ | 🔴 | B1 | 20min |
| B6.3 | Criar 1 edge case adicional (agente sem acesso a build/test) | ⬜ | 🟡 | B6.2 | 5min |

**Checkpoint B6:**
- [ ] ≥5 edge cases documentados
- [ ] Cada um com: situação, solução, exceção

---

### B7: Integração e Referências

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| B7.1 | Criar seção "Integração com Skills Existentes" (tabela de relações) | ⬜ | 🟡 | B1 | 10min |
| B7.2 | Criar seção "Referências" (links para ADRs e skills) | ⬜ | 🟢 | B1 | 5min |

**Checkpoint B7:**
- [ ] Tabela de integração com ≥10 skills
- [ ] Referências para ADR-001 a ADR-005

---

### B8: Validação do SKILL.md

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| B8.1 | Verificar SKILL.md ≥150 linhas | ⬜ | 🔴 | B1-B7 | 2min |
| B8.2 | Executar `validate-skill.sh skills/implementation` | ⬜ | 🔴 | B8.1 | 3min |
| B8.3 | Corrigir qualquer erro retornado pelo script | ⬜ | 🔴 | B8.2 | variável |
| B8.4 | Re-executar `validate-skill.sh` até 0 erros | ⬜ | 🔴 | B8.3 | 3min |

**Checkpoint B8:**
- [ ] SKILL.md ≥150 linhas
- [ ] `validate-skill.sh` retorna 0 erros

---

**Checkpoint Geral Fase B:**
- [ ] SKILL.md completo com todas as seções obrigatórias
- [ ] Decision tree funcional
- [ ] 8 workflows documentados
- [ ] 7+ anti-patterns com severidade
- [ ] 5+ edge cases
- [ ] Validação automática passa

---

## Fase C: Registro no Registry

### C1: Atualizar `skills/index.json`

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| C1.1 | Adicionar entrada `implementation` ao array `skills` | ⬜ | 🔴 | B8 | 5min |
| C1.2 | Definir `name: "implementation"` | ⬜ | 🔴 | C1.1 | 1min |
| C1.3 | Definir `version: "2.0.0"` | ⬜ | 🔴 | C1.1 | 1min |
| C1.4 | Definir `tags: ["implementation", "execution", "artifact-driven", "sdlc"]` | ⬜ | 🔴 | C1.1 | 1min |
| C1.5 | Definir `related_skills` | ⬜ | 🔴 | C1.1 | 2min |
| C1.6 | Definir `files` (SKILL.md + 5 templates) | ⬜ | 🔴 | C1.1 | 2min |
| C1.7 | Atualizar `description` global para "(21 skills)" | ⬜ | 🟡 | C1.1 | 1min |

**Checkpoint C1:**
- [ ] `index.json` tem 21 entradas (ou 15 se ADR-004 ainda não implementado)
- [ ] Todos os `files` são paths relativos corretos
- [ ] `validate-index.sh` passa

---

### C2: Atualizar `related_skills` das skills impactadas

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| C2.1 | `adr-generator/SKILL.md` — adicionar `implementation` em `related_skills` | ⬜ | 🔴 | C1 | 2min |
| C2.2 | `writing-plans/SKILL.md` — adicionar `implementation` em `related_skills` | ⬜ | 🔴 | C1 | 2min |
| C2.3 | `planning/SKILL.md` — adicionar `implementation` em `related_skills` | ⬜ | 🟡 | C1 | 2min |
| C2.4 | `testing/SKILL.md` — adicionar `implementation` em `related_skills` | ⬜ | 🟡 | C1 | 2min |
| C2.5 | `documentation/SKILL.md` — adicionar `implementation` em `related_skills` | ⬜ | 🟡 | C1 | 2min |
| C2.6 | `governance/SKILL.md` — adicionar `implementation` em `related_skills` | ⬜ | 🟡 | C1 | 2min |
| C2.7 | `git/SKILL.md` — adicionar `implementation` em `related_skills` | ⬜ | 🟡 | C1 | 2min |
| C2.8 | `release/SKILL.md` — adicionar `implementation` em `related_skills` | ⬜ | 🟡 | C1 | 2min |
| C2.9 | `architecture-review/SKILL.md` — adicionar `implementation` em `related_skills` | ⬜ | 🟡 | C1 | 2min |
| C2.10 | `ddd/SKILL.md` — adicionar `implementation` em `related_skills` | ⬜ | 🟢 | C1 | 2min |
| C2.11 | Atualizar `index.json` com novos `related_skills` | ⬜ | 🔴 | C2.1-C2.10 | 3min |

**Checkpoint C2:**
- [ ] ≥8 skills referenciam `implementation` em `related_skills`
- [ ] `index.json` reflete mudanças

---

### C3: Atualizar documentação do registry

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| C3.1 | Atualizar `README.md` — adicionar `implementation` na tabela de categorias | ⬜ | 🟡 | C1 | 5min |
| C3.2 | Atualizar `README.md` — adicionar na estrutura de diretórios | ⬜ | 🟡 | C1 | 3min |
| C3.3 | Atualizar `CHANGELOG.md` — adicionar entrada para `implementation` | ⬜ | 🟡 | C1 | 5min |

**Checkpoint C3:**
- [ ] README reflete 21 skills
- [ ] CHANGELOG tem entrada para nova skill

---

**Checkpoint Geral Fase C:**
- [ ] `index.json` atualizado e validado
- [ ] ≥8 skills com `implementation` em `related_skills`
- [ ] README e CHANGELOG atualizados

---

## Fase D: Validação Final

### D1: Validação completa

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| D1.1 | Executar `validate-index.sh` — deve passar | ⬜ | 🔴 | C1-C3 | 5min |
| D1.2 | Executar `validate-skill.sh skills/implementation` — deve passar | ⬜ | 🔴 | C1 | 3min |
| D1.3 | Executar `validate-skill.sh` em todas as skills — nenhuma deve quebrar | ⬜ | 🔴 | D1.2 | 10min |
| D1.4 | Verificar que SKILL.md ≥150 linhas | ⬜ | 🔴 | D1.2 | 2min |
| D1.5 | Verificar que nenhum `related_skills` aponta para skill inexistente | ⬜ | 🔴 | D1.3 | 5min |
| D1.6 | Verificar que todos os arquivos listados em `index.json` existem | ⬜ | 🔴 | D1.1 | 3min |

**Checkpoint D1:**
- [ ] `validate-index.sh`: 0 erros
- [ ] `validate-skill.sh` para `implementation`: 0 erros
- [ ] `validate-skill.sh` para todas as skills: 0 erros novos
- [ ] Todos os paths válidos

---

### D2: Revisão de consistência

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| D2.1 | Verificar que SKILL.md referencia todos os templates criados | ⬜ | 🔴 | D1 | 3min |
| D2.2 | Verificar que decision tree está coerente com workflows | ⬜ | 🟡 | D1 | 5min |
| D2.3 | Verificar que anti-patterns cobrem os principais riscos | ⬜ | 🟡 | D1 | 5min |
| D2.4 | Verificar que edge cases cobrem cenários reais | ⬜ | 🟡 | D1 | 5min |

**Checkpoint D2:**
- [ ] SKILL.md referencia todos os templates
- [ ] Decision tree coerente com workflows
- [ ] Anti-patterns e edge cases abrangentes

---

**Checkpoint Geral Fase D:**
- [ ] Validação automática passa para todas as skills
- [ ] Consistência interna verificada
- [ ] Skill pronta para uso

---

## Resumo Geral

| Fase | Tarefas | Horas Est. | Status |
|------|---------|------------|--------|
| Fase A: Estrutura Base | 13 | 1.5-2h | ⬜ |
| Fase B: SKILL.md | 30 | 3-4h | ⬜ |
| Fase C: Registro no Registry | 21 | 1-1.5h | ⬜ |
| Fase D: Validação Final | 10 | 0.5-1h | ⬜ |
| **Total** | **74** | **~6-8.5h** | **⬜ 0%** |

---

## Dependências entre Fases

```
Fase A (Estrutura)
  │
  ├─── A1: Diretórios ──────────┐
  ├─── A2: Templates ───────────┤
  ├─── A3: Examples ────────────┤
  └─── A4: Checklists ──────────┘
                                  │
Fase B (SKILL.md) ◄───────────────┘
  │
  ├─── B1: Frontmatter ─────────┐
  ├─── B2: Decision Tree ───────┤
  ├─── B3: Conceitos ───────────┤
  ├─── B4: Workflows ───────────┤
  ├─── B5: Anti-patterns ───────┤
  ├─── B6: Checklists/Edge ─────┤
  ├─── B7: Integração ──────────┤
  └─── B8: Validação ───────────┘
                                  │
Fase C (Registry) ◄───────────────┘
  │
  ├─── C1: index.json ──────────┐
  ├─── C2: related_skills ──────┤
  └─── C3: Docs do registry ────┘
                                  │
Fase D (Validação) ◄──────────────┘
  │
  ├─── D1: Validação completa ──┐
  └─── D2: Revisão de consistência┘
```

---

*Documento gerado em 2026-07-05. Referência: ADR-005.*
