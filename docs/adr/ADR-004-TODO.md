# TODO: Implementação das Recomendações da Ultra-Auditoria v2.0.2

> ADR-004 | Início: 2026-07-05 | Status: PENDENTE

---

## Legenda

- ⬜ Pendente
- 🔄 Em Andamento
- ✅ Concluído
- ❌ Bloqueado
- ⏸️ Pausado

**Prioridade:** 🔴 Alta | 🟡 Média | 🟢 Baixa

---

## Fase A: Correção de Débitos Técnicos

### A1: Adicionar `validate-skill.sh` ao pipeline CI

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| A1.1 | Modificar `.github/workflows/validate-skills.yml` para adicionar step de quality validation | ⬜ | 🔴 | — | 15min |
| A1.2 | Adicionar loop que executa `validate-skill.sh` em todas as skills | ⬜ | 🔴 | A1.1 | 10min |
| A1.3 | Tratar erros: exit 1 se qualquer skill falhar, warnings apenas reportados | ⬜ | 🔴 | A1.2 | 5min |
| A1.4 | Testar workflow localmente (simular CI) | ⬜ | 🟡 | A1.3 | 5min |

**Checkpoint A1:**
- [ ] `validate-skill.sh` é executado em todas as skills no pipeline
- [ ] Pipeline falha se qualquer skill tiver erro

---

### A2: Escrever CHANGELOG para v2.0.0→v2.0.2

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| A2.1 | Criar entrada `[2.0.2]` com data atual | ⬜ | 🔴 | — | 5min |
| A2.2 | Documentar adição de `skill-audit-bulletin` | ⬜ | 🔴 | A2.1 | 5min |
| A2.3 | Documentar refatoração das 13 skills para Ultra-High Quality Grade | ⬜ | 🔴 | A2.1 | 5min |
| A2.4 | Mover conteúdo de `[Unreleased]` para entrada `[2.0.1]` | ⬜ | 🔴 | — | 5min |
| A2.5 | Deixar seção `[Unreleased]` vazia | ⬜ | 🟢 | A2.4 | 1min |

**Checkpoint A2:**
- [ ] CHANGELOG tem entradas para 2.0.2 e 2.0.1
- [ ] Formato Keep a Changelog mantido
- [ ] `[Unreleased]` está vazia

---

### A3: Resolver colisão `architecture-review`

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| A3.1 | Renomear pasta `skills/architecture-review/` → `skills/architecture-review-kilo/` | ⬜ | 🔴 | — | 2min |
| A3.2 | Atualizar frontmatter em `SKILL.md`: `name: architecture-review-kilo` | ⬜ | 🔴 | A3.1 | 2min |
| A3.3 | Atualizar `index.json`: chave `name` e `files` | ⬜ | 🔴 | A3.1 | 3min |
| A3.4 | Buscar todas as referências em outros SKILL.md | ⬜ | 🔴 | — | 5min |
| A3.5 | Atualizar `adr-generator/SKILL.md` → `related_skills: [documentation, architecture-review-kilo]` | ⬜ | 🔴 | A3.4 | 2min |
| A3.6 | Atualizar `ddd/SKILL.md` → `related_skills: [architecture-review-kilo, testing]` | ⬜ | 🔴 | A3.4 | 2min |
| A3.7 | Atualizar `skill-audit-bulletin/SKILL.md` → `related_skills: [architecture-review-kilo, documentation]` | ⬜ | 🔴 | A3.4 | 2min |
| A3.8 | Verificar que nenhum `related_skills` aponta para nome inexistente | ⬜ | 🔴 | A3.5-A3.7 | 3min |

**Checkpoint A3:**
- [ ] Pasta renomeada
- [ ] Frontmatter e index.json atualizados
- [ ] Todos os `related_skills` apontam para nomes válidos

---

### A4: Resolver sobreposição `planning` vs `writing-plans`

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| A4.1 | Reescrever "Não use quando" em `planning/SKILL.md` mencionando `writing-plans` | ⬜ | 🔴 | — | 5min |
| A4.2 | Reescrever "Não use quando" em `writing-plans/SKILL.md` mencionando `planning` | ⬜ | 🔴 | — | 5min |
| A4.3 | Atualizar decision trees de ambas se necessário | ⬜ | 🟡 | A4.1, A4.2 | 5min |
| A4.4 | Verificar que `related_skills` mantêm referência cruzada | ⬜ | 🟢 | A4.1, A4.2 | 2min |

**Checkpoint A4:**
- [ ] Ambas as skills mencionam a outra na seção "Não use quando"
- [ ] Decision trees incluem desambiguação

---

### A5: Adicionar `skill-audit-bulletin` ao grafo de `related_skills`

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| A5.1 | Adicionar `skill-audit-bulletin` nos `related_skills` de `governance/SKILL.md` | ⬜ | 🟡 | — | 2min |
| A5.2 | Adicionar `skill-audit-bulletin` nos `related_skills` de `repo-bootstrap/SKILL.md` | ⬜ | 🟡 | — | 2min |
| A5.3 | Atualizar `index.json` com novos `related_skills` | ⬜ | 🟡 | A5.1, A5.2 | 2min |

**Checkpoint A5:**
- [ ] `governance` e `repo-bootstrap` referenciam `skill-audit-bulletin`
- [ ] `index.json` reflete mudanças

---

### A6: Resolver pasta `checklists/` fantasma

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| A6.1 | Criar `skills/release/checklists/pre-release.md` | ⬜ | 🟡 | — | 5min |
| A6.2 | Criar `skills/release/checklists/post-release.md` | ⬜ | 🟡 | A6.1 | 5min |
| A6.3 | Verificar que `templates/skill-template.md` não lista `checklists/` como obrigatório | ⬜ | 🟢 | — | 2min |

**Checkpoint A6:**
- [ ] `skills/release/checklists/` existe com ≥1 arquivo real
- [ ] `checklists/` não é listado como obrigatório no template

---

### A7: Marcar processo de Peer Review como condicional

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| A7.1 | Adicionar nota "para equipes com >1 mantenedor" na seção Peer Review | ⬜ | 🟢 | — | 3min |
| A7.2 | Reforçar seção Auto-review como processo atual para solo | ⬜ | 🟢 | A7.1 | 2min |

**Checkpoint A7:**
- [ ] Peer Review marcado como condicional
- [ ] Auto-review apresentado como processo atual

---

**Checkpoint Geral Fase A:**
- [ ] Todas as 7 tarefas (A1-A7) concluídas
- [ ] `validate-index.sh` ainda passa após mudanças
- [ ] Nenhum `related_skills` quebrado

---

## Fase B: Skills Novas

### B1: Criar skill `security-review` 🥇

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| B1.1 | Criar pasta `skills/security-review/` | ⬜ | 🔴 | A1 | 1min |
| B1.2 | Criar `SKILL.md` com frontmatter completo | ⬜ | 🔴 | B1.1 | 5min |
| B1.3 | Criar decision tree (secret scanning, injeção, criptografia, dependências, ameaça) | ⬜ | 🔴 | B1.2 | 15min |
| B1.4 | Criar Workflow 1: Secret scanning | ⬜ | 🔴 | B1.3 | 15min |
| B1.5 | Criar Workflow 2: Revisão de dependências | ⬜ | 🔴 | B1.3 | 15min |
| B1.6 | Criar Workflow 3: Validação de criptografia | ⬜ | 🔴 | B1.3 | 20min |
| B1.7 | Criar Workflow 4: Modelagem de ameaça leve | ⬜ | 🔴 | B1.3 | 15min |
| B1.8 | Criar Workflow 5: Relatório de vulnerabilidade | ⬜ | 🟡 | B1.3 | 10min |
| B1.9 | Criar templates (security-checklist.md, threat-model.md, vulnerability-report.md) | ⬜ | 🔴 | — | 30min |
| B1.10 | Criar anti-patterns com severidade 🔴🟡🟢 | ⬜ | 🔴 | — | 20min |
| B1.11 | Criar Checklists | ⬜ | 🔴 | — | 10min |
| B1.12 | Criar Edge Cases | ⬜ | 🟡 | — | 10min |
| B1.13 | Adicionar cross-references (`governance`, `architecture-review-kilo`, `testing`) | ⬜ | 🟡 | A3 | 5min |
| B1.14 | Atualizar `index.json` | ⬜ | 🔴 | B1.2-B1.13 | 3min |
| B1.15 | Validar com `validate-skill.sh` | ⬜ | 🔴 | B1.14 | 5min |

**Checkpoint B1:**
- [ ] `validate-skill.sh` passa com 0 erros
- [ ] SKILL.md ≥150 linhas
- [ ] 3 templates funcionais

---

### B2: Criar skill `agent-orchestration` 🥈

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| B2.1 | Criar pasta `skills/agent-orchestration/` | ⬜ | 🔴 | A1 | 1min |
| B2.2 | Criar `SKILL.md` com frontmatter completo | ⬜ | 🔴 | B2.1 | 5min |
| B2.3 | Criar decision tree (decomposição, handoff, roteamento, pipeline) | ⬜ | 🔴 | B2.2 | 15min |
| B2.4 | Criar Workflow 1: Decompor tarefa em papéis | ⬜ | 🔴 | B2.3 | 15min |
| B2.5 | Criar Workflow 2: Definir protocolo de handoff | ⬜ | 🔴 | B2.3 | 15min |
| B2.6 | Criar Workflow 3: Roteamento de modelo | ⬜ | 🔴 | B2.3 | 15min |
| B2.7 | Criar Workflow 4: Orquestração paralela | ⬜ | 🔴 | B2.3 | 15min |
| B2.8 | Criar Workflow 5: Validação de contrato | ⬜ | 🟡 | B2.3 | 10min |
| B2.9 | Criar templates (agent-role-card.md, handoff-protocol.md, routing-decision.md) | ⬜ | 🔴 | — | 30min |
| B2.10 | Criar anti-patterns com severidade 🔴🟡🟢 | ⬜ | 🔴 | — | 20min |
| B2.11 | Criar Checklists | ⬜ | 🔴 | — | 10min |
| B2.12 | Criar Edge Cases | ⬜ | 🟡 | — | 10min |
| B2.13 | Adicionar cross-references (`prompt-engineering`, `vibe-coding`, `governance`) | ⬜ | 🟡 | — | 5min |
| B2.14 | Atualizar `index.json` | ⬜ | 🔴 | B2.2-B2.13 | 3min |
| B2.15 | Validar com `validate-skill.sh` | ⬜ | 🔴 | B2.14 | 5min |

**Checkpoint B2:**
- [ ] `validate-skill.sh` passa com 0 erros
- [ ] SKILL.md ≥150 linhas
- [ ] 3 templates funcionais

---

### B3: Criar skill `data-modeling` 🥉

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| B3.1 | Criar pasta `skills/data-modeling/` | ⬜ | 🔴 | A1 | 1min |
| B3.2 | Criar `SKILL.md` com frontmatter completo | ⬜ | 🔴 | B3.1 | 5min |
| B3.3 | Criar decision tree (relacional, NoSQL, document, normalização, índices) | ⬜ | 🔴 | B3.2 | 15min |
| B3.4 | Criar Workflow 1: Analisar requisitos de dados | ⬜ | 🔴 | B3.3 | 15min |
| B3.5 | Criar Workflow 2: Definir schema relacional | ⬜ | 🔴 | B3.3 | 15min |
| B3.6 | Criar Workflow 3: Estratégia de índice | ⬜ | 🔴 | B3.3 | 15min |
| B3.7 | Criar Workflow 4: Migrations versionadas | ⬜ | 🔴 | B3.3 | 15min |
| B3.8 | Criar Workflow 5: Validação de schema | ⬜ | 🟡 | B3.3 | 10min |
| B3.9 | Criar templates (schema.sql, migration.md, index-strategy.md) | ⬜ | 🔴 | — | 30min |
| B3.10 | Criar anti-patterns com severidade 🔴🟡🟢 | ⬜ | 🔴 | — | 20min |
| B3.11 | Criar Checklists | ⬜ | 🔴 | — | 10min |
| B3.12 | Criar Edge Cases | ⬜ | 🟡 | — | 10min |
| B3.13 | Adicionar cross-references (`ddd`, `testing`, `architecture-review-kilo`) | ⬜ | 🟡 | A3 | 5min |
| B3.14 | Atualizar `index.json` | ⬜ | 🔴 | B3.2-B3.13 | 3min |
| B3.15 | Validar com `validate-skill.sh` | ⬜ | 🔴 | B3.14 | 5min |

**Checkpoint B3:**
- [ ] `validate-skill.sh` passa com 0 erros
- [ ] SKILL.md ≥150 linhas
- [ ] 3 templates funcionais

---

### B4: Criar skill `api-design`

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| B4.1 | Criar pasta `skills/api-design/` | ⬜ | 🔴 | A1 | 1min |
| B4.2 | Criar `SKILL.md` com frontmatter completo | ⬜ | 🔴 | B4.1 | 5min |
| B4.3 | Criar decision tree (REST, GraphQL, WebSocket, versionamento) | ⬜ | 🔴 | B4.2 | 15min |
| B4.4 | Criar Workflow 1: Definir contrato REST | ⬜ | 🔴 | B4.3 | 15min |
| B4.5 | Criar Workflow 2: Versionamento de API | ⬜ | 🔴 | B4.3 | 10min |
| B4.6 | Criar Workflow 3: Formato de erro consistente | ⬜ | 🔴 | B4.3 | 10min |
| B4.7 | Criar Workflow 4: Paginação | ⬜ | 🔴 | B4.3 | 10min |
| B4.8 | Criar Workflow 5: Idempotência | ⬜ | 🟡 | B4.3 | 10min |
| B4.9 | Criar templates (endpoint-spec.md, error-contract.md, api-versioning.md) | ⬜ | 🔴 | — | 25min |
| B4.10 | Criar anti-patterns com severidade 🔴🟡🟢 | ⬜ | 🔴 | — | 15min |
| B4.11 | Criar Checklists | ⬜ | 🔴 | — | 10min |
| B4.12 | Criar Edge Cases | ⬜ | 🟡 | — | 10min |
| B4.13 | Adicionar cross-references (`documentation`, `testing`, `governance`) | ⬜ | 🟡 | — | 5min |
| B4.14 | Atualizar `index.json` | ⬜ | 🔴 | B4.2-B4.13 | 3min |
| B4.15 | Validar com `validate-skill.sh` | ⬜ | 🔴 | B4.14 | 5min |

**Checkpoint B4:**
- [ ] `validate-skill.sh` passa com 0 erros
- [ ] SKILL.md ≥150 linhas
- [ ] 3 templates funcionais

---

### B5: Criar skill `observability`

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| B5.1 | Criar pasta `skills/observability/` | ⬜ | 🔴 | A1 | 1min |
| B5.2 | Criar `SKILL.md` com frontmatter completo | ⬜ | 🔴 | B5.1 | 5min |
| B5.3 | Criar decision tree (logging, métricas, tracing, alertas, SLAs) | ⬜ | 🔴 | B5.2 | 15min |
| B5.4 | Criar Workflow 1: Logging estruturado | ⬜ | 🔴 | B5.3 | 15min |
| B5.5 | Criar Workflow 2: Métricas RED | ⬜ | 🔴 | B5.3 | 15min |
| B5.6 | Criar Workflow 3: Alertas e limiares | ⬜ | 🔴 | B5.3 | 10min |
| B5.7 | Criar Workflow 4: Distributed tracing | ⬜ | 🔴 | B5.3 | 15min |
| B5.8 | Criar Workflow 5: SLAs/SLOs | ⬜ | 🟡 | B5.3 | 10min |
| B5.9 | Criar templates (logging-spec.md, metrics-sla.md, alert-rules.md) | ⬜ | 🔴 | — | 25min |
| B5.10 | Criar anti-patterns com severidade 🔴🟡🟢 | ⬜ | 🔴 | — | 15min |
| B5.11 | Criar Checklists | ⬜ | 🔴 | — | 10min |
| B5.12 | Criar Edge Cases | ⬜ | 🟡 | — | 10min |
| B5.13 | Adicionar cross-references (`testing`, `release`, `governance`) | ⬜ | 🟡 | — | 5min |
| B5.14 | Atualizar `index.json` | ⬜ | 🔴 | B5.2-B5.13 | 3min |
| B5.15 | Validar com `validate-skill.sh` | ⬜ | 🔴 | B5.14 | 5min |

**Checkpoint B5:**
- [ ] `validate-skill.sh` passa com 0 erros
- [ ] SKILL.md ≥150 linhas
- [ ] 3 templates funcionais

---

### B6: Criar skill `refactoring`

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| B6.1 | Criar pasta `skills/refactoring/` | ⬜ | 🔴 | A1 | 1min |
| B6.2 | Criar `SKILL.md` com frontmatter completo | ⬜ | 🔴 | B6.1 | 5min |
| B6.3 | Criar decision tree (testes existentes, strangler fig, branch by abstraction) | ⬜ | 🔴 | B6.2 | 15min |
| B6.4 | Criar Workflow 1: Avaliar risco | ⬜ | 🔴 | B6.3 | 10min |
| B6.5 | Criar Workflow 2: Adicionar testes de caracterização | ⬜ | 🔴 | B6.3 | 15min |
| B6.6 | Criar Workflow 3: Aplicar refatoração segura | ⬜ | 🔴 | B6.3 | 15min |
| B6.7 | Criar Workflow 4: Validar com testes e revisão | ⬜ | 🔴 | B6.3 | 10min |
| B6.8 | Criar Workflow 5: Documentar decisão | ⬜ | 🟡 | B6.3 | 10min |
| B6.9 | Criar templates (refactoring-catalog.md, legacy-migration.md, test-before-refactor.md) | ⬜ | 🔴 | — | 25min |
| B6.10 | Criar anti-patterns com severidade 🔴🟡🟢 | ⬜ | 🔴 | — | 15min |
| B6.11 | Criar Checklists | ⬜ | 🔴 | — | 10min |
| B6.12 | Criar Edge Cases | ⬜ | 🟡 | — | 10min |
| B6.13 | Adicionar cross-references (`architecture-review-kilo`, `ddd`, `testing`) | ⬜ | 🟡 | A3 | 5min |
| B6.14 | Atualizar `index.json` | ⬜ | 🔴 | B6.2-B6.13 | 3min |
| B6.15 | Validar com `validate-skill.sh` | ⬜ | 🔴 | B6.14 | 5min |

**Checkpoint B6:**
- [ ] `validate-skill.sh` passa com 0 erros
- [ ] SKILL.md ≥150 linhas
- [ ] 3 templates funcionais

---

**Checkpoint Geral Fase B:**
- [ ] 6 novas skills criadas e validadas
- [ ] `index.json` tem 20 entradas
- [ ] Todas as 20 skills passam em `validate-skill.sh`

---

## Fase C: Validação Final

### C1: Validação cruzada completa

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| C1.1 | Executar `validate-index.sh` — deve passar com 20/20 skills | ⬜ | 🔴 | A1-A7, B1-B6 | 5min |
| C1.2 | Executar `validate-skill.sh` em todas as 20 skills | ⬜ | 🔴 | C1.1 | 10min |
| C1.3 | Verificar que `index.json` tem 20 entradas e `version` = "2.0.2" | ⬜ | 🔴 | C1.2 | 3min |
| C1.4 | Verificar que nenhum `related_skills` aponta para skill inexistente | ⬜ | 🔴 | C1.3 | 5min |
| C1.5 | Verificar que todas as skills têm ≥150 linhas | ⬜ | 🔴 | C1.2 | 3min |
| C1.6 | Verificar que grafo de `related_skills` é conexo | ⬜ | 🟡 | C1.4 | 5min |
| C1.7 | Atualizar `CHANGELOG.md` com seção `[Unreleased]` se houver pendências | ⬜ | 🟢 | C1.6 | 5min |

**Checkpoint C1:**
- [ ] `validate-index.sh` passa: 20/20 skills, 0 erros
- [ ] `validate-skill.sh` passa para todas as 20 skills: 0 erros
- [ ] `index.json` consistente
- [ ] Grafo de `related_skills` conexo

---

## Resumo Geral

| Fase | Tarefas | Horas Est. | Status |
|------|---------|------------|--------|
| Fase A: Débitos Técnicos | 27 | 1.5-2h | ⬜ |
| Fase B: Skills Novas | 90 | 14-18h | ⬜ |
| Fase C: Validação | 7 | 0.5h | ⬜ |
| **Total** | **124** | **~16-20.5h** | **⬜ 0%** |

---

*Documento gerado em 2026-07-05. Referência: ADR-004.*
