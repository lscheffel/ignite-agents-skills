# Blueprint: Skill `implementation` — Execução Governada de Mudanças

> ADR-005 | Versão 1.0 | 2026-07-05 | **Status: PENDENTE**

---

## 1. Visão Geral

### Objetivo
Criar a skill `implementation` — a ponte formal entre planejamento e execução no SDLC baseado em Agent Skills. A skill consome ADRs, Blueprints e TODOs e coordera sua implementação incremental com validação contínua.

### Métricas de Sucesso

| Métrica | Antes | Depois | Status |
|---------|-------|--------|--------|
| Skills no registry | 14 (+ 6 ADR-004) | 21 | ⬜ |
| SDLC coberto por skills | ~70% | ~95% | ⬜ |
| Capacidade de execução governada | Não | Sim | ⬜ |
| Artifact-Driven SDLC | Não | Sim | ⬜ |
| SKILL.md linhas | — | ≥250 | ⬜ |
| Templates criados | — | 5 | ⬜ |
| Examples criados | — | 2 | ⬜ |
| `validate-skill.sh` | — | 0 erros | ⬜ |

---

## 2. Estrutura de Artefatos

```
skills/implementation/
├── SKILL.md                          # Skill principal (~280 linhas)
├── templates/
│   ├── execution-contract.md         # Contrato de execução pré-implementation
│   ├── execution-report.md           # Relatório final da implementação
│   ├── change-plan.md                # Plano interno de execução (DAG)
│   ├── rollback-report.md            # Relatório de rollback
│   └── task-progress.md              # Progresso individual de tarefa
├── examples/
│   ├── simple-change.md              # Exemplo: mudança pontual (1-2 tarefas)
│   └── complex-change.md             # Exemplo: mudança multi-ADR (10+ tarefas)
└── checklists/
    ├── pre-execution.md              # Checklist antes de iniciar
    └── post-execution.md             # Checklist após conclusão
```

---

## 3. Decision Tree

```mermaid
graph TD
    A[Mudança solicitada] -->|Existe ADR?| B{ADR encontrada}
    B -->|Não| C[Usar adr-generator primeiro]
    B -->|Sim| D{Existe Blueprint?}
    D -->|Não| E[Usar writing-plans primeiro]
    D -->|Sim| F{Existe TODO?}
    F -->|Não| G[Usar writing-plans para gerar TODO]
    F -->|Sim| H{Execution Contract passa?}
    H -->|Não| I[Corrigir artefatos antes de continuar]
    H -->|Sim| J[Iniciar Execution Loop]
    J --> K[Selecionar tarefa via DAG]
    K --> L[Executar alteração]
    L --> M[Validar: build + lint + test]
    M -->|Falhou| N[Corrigir e re-validar]
    M -->|Passou| O[Atualizar documentação]
    O --> P[Atualizar TODO]
    P --> Q{Mais tarefas?}
    Q -->|Sim| K
    Q -->|Não| R[Gerar Execution Report]
```

---

## 4. Conceitos Fundamentais

### 4.1 Execution Contract

Contrato obrigatório que valida se todos os artefatos necessários estão presentes e coerentes antes de qualquer alteração.

**Campos do contrato:**
- ADR: path, status, decisão
- Blueprint: path, tarefas listadas
- TODO: path, tarefas com estados
- Branch: nome, estado limpo
- Workspace: sem alterações não commitadas
- Arquivos impactados: lista extraída do Blueprint
- Critérios de aceite: extraídos do TODO
- Critérios de rollback: definidos no Blueprint

**Regra:** Se qualquer campo obrigatório falhar, a implementação é interrompida.

### 4.2 Artifact Resolution

Processo de descoberta e correlação automática dos documentos envolvidos na mudança.

**Entrada:** Nome da ADR ou diretório de trabalho
**Saída:** Mapa de artefatos correlacionados

**Algoritmo:**
1. Buscar `ADR-XXX.md` no diretório `docs/adr/`
2. Derivar paths do Blueprint (`ADR-XXX-BP.md`) e TODO (`ADR-XXX-TODO.md`)
3. Verificar existência de cada artefato
4. Extrair `related_skills` do frontmatter
5. Mapear arquivos impactados a partir do Blueprint
6. Retornar mapa consolidado

### 4.3 Execution Loop

Modelo incremental de execução. Cada iteração do loop processa uma tarefa do TODO.

```
┌─────────────────────────────────────────┐
│           EXECUTION LOOP                │
│                                         │
│  1. Selecionar tarefa (via DAG)         │
│  2. Marcar como "Em andamento"          │
│  3. Executar alteração                  │
│  4. Validar (build/lint/test/typecheck) │
│  5. Atualizar documentação              │
│  6. Marcar como "Concluído"             │
│  7. Reavaliar dependências              │
│  8. Repetir até fim do DAG              │
└─────────────────────────────────────────┘
```

**Regras:**
- Máximo 1 tarefa "Em andamento" por vez
- Tarefa só inicia se todas as dependências estão "Concluído"
- Se validação falhar, tarefa vai para "Bloqueado" até correção
- Big Bang é estritamente proibido

### 4.4 Change Lifecycle

Modelo formal do ciclo de vida de uma mudança:

```
ADR → Blueprint → TODO → Execution Contract → Artifact Resolution
  → Implementation → Validation → Documentation Update → Execution Report
```

Cada transição é validada. A mudança só avança se a fase anterior foi concluída com sucesso.

---

## 5. Workflow

### Workflow 1: Artifact Resolution

**Objetivo:** Descobrir e correlacionar todos os artefatos envolvidos.

1. Identificar a ADR de referência (por nome ou contexto)
2. Derivar paths: `ADR-XXX-BP.md`, `ADR-XXX-TODO.md`
3. Verificar existência de cada artefato
4. Ler frontmatter da ADR para extrair status e decisão
5. Ler Blueprint para extrair tarefas e dependências
6. Ler TODO para extrair estados atuais
7. Mapear `related_skills` do frontmatter
8. Extrair arquivos impactados do Blueprint
9. Retornar **Artifact Map** consolidado
10. **Checkpoint**: Todos os artefatos existem e estão coerentes

### Workflow 2: Execution Contract

**Objetivo:** Validar que a implementação pode iniciar com segurança.

1. Carregar Artifact Map (Workflow 1)
2. Validar que ADR existe e está "Aceito" ou "Proposto"
3. Validar que Blueprint existe e contém tarefas
4. Validar que TODO existe e contém tarefas com estados
5. Validar branch atual (não main/master sem PR)
6. Validar workspace limpo (sem uncommitted changes)
7. Validar que arquivos impactados existem
8. Extrair critérios de aceite do TODO
9. Extrair critérios de rollback do Blueprint
10. Gerar `execution-contract.md` preenchido
11. **Checkpoint**: Contrato assinado (todos os campos válidos)

### Workflow 3: Dependency Analysis & Execution Plan

**Objetivo:** Construir DAG e plano de execução.

1. Ler TODO e extrair todas as tarefas
2. Ler dependências de cada tarefa
3. Construir grafo dirigido acíclico (DAG)
4. Detectar ciclos (se existir, reportar erro e interromper)
5. Topological sort para ordem de execução
6. Identificar tarefas paralelizáveis (sem dependência entre si)
7. Gerar `change-plan.md` com DAG e ordem
8. Estimar tempo total a partir das estimativas do TODO
9. **Checkpoint**: DAG válido, sem ciclos, ordem definida

### Workflow 4: Incremental Execution

**Objetivo:** Executar tarefas uma a uma com validação.

Para cada tarefa na ordem do DAG:

1. Verificar que todas as dependências estão "Concluído"
2. Marcar tarefa como "Em andamento" no TODO
3. Gerar `task-progress.md` para a tarefa
4. Ler descrição e critérios de aceite da tarefa
5. Executar as alterações no código
6. Executar validação contínua (Workflow 5)
7. Se validação passar:
   - Atualizar documentação afetada
   - Marcar tarefa como "Concluído" no TODO
   - Atualizar `task-progress.md`
8. Se validação falhar:
   - Analisar causa raiz
   - Corrigir
   - Re-executar validação
   - Se não corrigir em 3 tentativas: marcar "Bloqueado"
9. Reavaliar dependências (tarefas dependentes podem iniciar)
10. **Checkpoint**: Tarefa concluída, TODO atualizado

### Workflow 5: Continuous Validation

**Objetivo:** Validar estado do projeto após cada alteração.

**Sequência de validação (quando aplicável):**

1. **Build**: `npm run build` / `cargo build` / equivalente
2. **Lint**: `npm run lint` / `cargo clippy` / equivalente
3. **Typecheck**: `npm run typecheck` / `cargo check` / equivalente
4. **Testes unitários**: `npm run test` / `cargo test` / equivalente
5. **Testes de integração**: se existirem
6. **Validação arquitetural**: verificar consistência com ADR
7. **Validação documental**: verificar que docs estão atualizados

**Regra:** Se qualquer passo falhar, a tarefa não pode ser marcada como "Concluído".

### Workflow 6: Documentation Synchronization

**Objetivo:** Garantir que documentação está sincronizada com código.

Após cada tarefa concluída:

1. Verificar se a alteração impacta ADRs existentes
2. Se sim, atualizar a ADR com novas informações
3. Verificar se o Blueprint precisa de ajustes
4. Se sim, atualizar o Blueprint
5. Verificar se README, CHANGELOG, USAGE, STATE, AGENTS precisa de atualização
6. Se sim, atualizar README, CHANGELOG, USAGE, STATE, AGENTS
7. Verificar se `related_skills` de outras skills precisam de ajuste
8. **Checkpoint**: Nenhuma documentação divergente do código

### Workflow 7: Progress Tracking

**Objetivo:** Manter TODO sincronizado durante toda a implementação.

**Estados permitidos:**

| Estado | Descrição | Transições |
|--------|-----------|------------|
| ⬜ Pendente | Tarefa não iniciada | → Em andamento |
| 🔄 Em andamento | Tarefa em execução | → Concluído, Bloqueado |
| ✅ Concluído | Tarefa finalizada com sucesso | — |
| ❌ Bloqueado | Tarefa impedida | → Em andamento, Pendente |
| ⏸️ Pausado | Tarefa adiada voluntariamente | → Pendente |

**Regras:**
- Máximo 1 tarefa "Em andamento" por vez
- "Concluído" só após validação bem-sucedida
- "Bloqueado" requer justificativa
- Estado deve ser atualizado no TODO imediatamente

### Workflow 8: Execution Report

**Objetivo:** Gerar relatório final da implementação.

**Campos do relatório:**
- Resumo da implementação
- ADR referência
- Data de início e término
- Tarefas concluídas (lista)
- Tarefas adiadas (lista com justificativa)
- Tarefas bloqueadas (lista com bloqueador)
- Validações executadas (build, lint, test)
- Testes realizados (cobertura, resultados)
- Riscos remanescentes
- Dívida técnica criada
- Recomendações futuras

---

## 6. Templates

### 6.1 execution-contract.md

```markdown
# Execution Contract

## Artefatos

| Artefato | Path | Status | Coerente |
|----------|------|--------|----------|
| ADR | docs/adr/ADR-XXX.md | {status} | ✅/❌ |
| Blueprint | docs/adr/ADR-XXX-BP.md | {existente} | ✅/❌ |
| TODO | docs/adr/ADR-XXX-TODO.md | {existente} | ✅/❌ |

## Ambiente

| Campo | Valor |
|-------|-------|
| Branch | {nome} |
| Workspace limpo | {sim/não} |
| Arquivos impactados | {lista} |

## Critérios de Aceite

- [ ] {critério 1}
- [ ] {critério 2}

## Critérios de Rollback

- [ ] {critério 1}
- [ ] {critério 2}

## Assinatura

- [ ] Contrato validado
- [ ] Implementação autorizada
```

### 6.2 execution-report.md

```markdown
# Execution Report

## Resumo

| Campo | Valor |
|-------|-------|
| ADR | {referência} |
| Data início | {data} |
| Data término | {data} |
| Duração total | {tempo} |
| Tarefas totais | {número} |
| Tarefas concluídas | {número} |
| Tarefas adiadas | {número} |
| Tarefas bloqueadas | {número} |

## Tarefas Concluídas

| # | Tarefa | Duração | Validações |
|---|--------|---------|------------|
| 1 | {tarefa} | {tempo} | ✅ |

## Tarefas Adiadas

| # | Tarefa | Justificativa |
|---|--------|---------------|
| 1 | {tarefa} | {razão} |

## Validações Executadas

| Validação | Resultado |
|-----------|-----------|
| Build | ✅/❌ |
| Lint | ✅/❌ |
| Typecheck | ✅/❌ |
| Testes unitários | ✅/❌ |
| Testes integração | ✅/❌ |

## Riscos Remanescentes

- {risco 1}
- {risco 2}

## Dívida Técnica Criada

- {débito 1}
- {débito 2}

## Recomendações Futuras

- {recomendação 1}
- {recomendação 2}
```

### 6.3 change-plan.md

```markdown
# Change Plan

## DAG de Execução

```mermaid
graph LR
    T1[Tarefa 1] --> T3[Tarefa 3]
    T2[Tarefa 2] --> T3
    T3 --> T4[Tarefa 4]
    T3 --> T5[Tarefa 5]
```

## Ordem de Execução

| Fase | Tarefas Paralelas | Tarefas Sequenciais |
|------|-------------------|---------------------|
| 1 | T1, T2 | — |
| 2 | — | T3 |
| 3 | T4, T5 | — |

## Estimativa Total

| Fase | Tempo Est. |
|------|------------|
| 1 | {tempo} |
| 2 | {tempo} |
| 3 | {tempo} |
| **Total** | **{tempo}** |
```

### 6.4 rollback-report.md

```markdown
# Rollback Report

## Motivo

{descrição do motivo do rollback}

## Tarefas Revertidas

| # | Tarefa | Commits Revertidos |
|---|--------|-------------------|
| 1 | {tarefa} | {hashes} |

## Estado Final

| Campo | Valor |
|-------|-------|
| Branch | {nome} |
| Commit final | {hash} |
| Testes | ✅/❌ |
| Build | ✅/❌ |

## Ações Corretivas

- {ação 1}
- {ação 2}
```

### 6.5 task-progress.md

```markdown
# Task Progress: {Nome da Tarefa}

## Estado

| Campo | Valor |
|-------|-------|
| Estado atual | {🔄 Em andamento / ✅ Concluído / ❌ Bloqueado} |
| Data início | {data} |
| Data término | {data} |
| Tentativas | {número} |

## Alterações Realizadas

| Arquivo | Tipo | Descrição |
|---------|------|-----------|
| {path} | {modificado/criado/removido} | {descrição} |

## Validações

| Validação | Resultado | Tentativa |
|-----------|-----------|-----------|
| Build | ✅/❌ | {n} |
| Lint | ✅/❌ | {n} |
| Test | ✅/❌ | {n} |

## Bloqueadores (se aplicável)

- {bloqueador 1}

## Observações

- {observação 1}
```

---

## 7. Anti-patterns

### 🔴 Crítico

#### Executar sem Execution Contract
**O que é:** Iniciar alterações sem validar que ADR, Blueprint e TODO existem e estão coerentes.
**Por que é ruim:** Pode levar a implementação inconsistente com a decisão arquitetural.
**Como evitar:** Sempre gerar e validar o Execution Contract antes de qualquer alteração.
**Exemplo:**
```
# ❌ ERRADO
"Vou implementar a ADR-005 agora" (sem verificar se Blueprint existe)

# ✅ CORRETO
1. Gerar Artifact Map
2. Validar Execution Contract
3. Só então iniciar execução
```

#### Big Bang Implementation
**O que é:** Implementar todas as tarefas de uma vez sem validação intermediária.
**Por que é ruim:** Se algo falhar, não há ponto de retorno claro; dificulta rollback.
**Como evitar:** Seguir o Execution Loop estritamente — uma tarefa por vez.
**Exemplo:**
```
# ❌ ERRADO
Modificar 15 arquivos de uma vez, commitar tudo junto

# ✅ CORRETO
Tarefa 1 → validar → commit
Tarefa 2 → validar → commit
Tarefa 3 → validar → commit
```

#### Ignorar Falha de Validação
**O que é:** Prosseguir com tarefa seguinte quando build/test/lint falhou na tarefa atual.
**Por que é ruim:** Acumula erros; cada tarefa depende do estado anterior.
**Como evitar:** Se validação falhar, corrigir antes de avançar. Sem exceções.
**Exemplo:**
```
# ❌ ERRADO
"O teste falhou, mas vou continuar e corrigir depois"

# ✅ CORRETO
"O teste falhou → analisar causa → corrigir → re-testar → só então avançar"
```

### 🟡 Médio

#### Atualizar código sem atualizar documentação
**O que é:** Implementar alteração mas esquecer de sincronizar ADR, Blueprint ou README.
**Por que é ruim:** Documentação fica desatualizada; perde rastreabilidade.
**Como evitar:** Workflow 6 (Documentation Synchronization) deve rodar após cada tarefa.

#### Executar tarefas fora da ordem do DAG
**O que é:** Pular dependências e executar tarefa que depende de outra não concluída.
**Por que é ruim:** Pode causar erros de compilação, lógica inconsistente.
**Como evitar:** Respeitar topological sort do DAG; verificar dependências antes de cada tarefa.

#### Marcar tarefa como "Concluído" sem validação
**O que é:** Declarar tarefa pronta sem rodar build/test/lint.
**Por que é ruim:** Tarefa pode conter erros silenciosos.
**Como evitar:** Workflow 5 (Continuous Validation) é obrigatório antes de marcar "Concluído".

### 🟢 Baixo

#### Não gerar Execution Report
**O que é:** Finalizar implementação sem produzir relatório.
**Por que é ruim:** Perde-se oportunidade de documentar lições e riscos.
**Como evitar:** Sempre gerar relatório ao término, mesmo para mudanças simples.

#### Estimativas muito otimistas no change-plan
**O que é:** Subestimar tempo de tarefas no DAG.
**Por que é ruim:** Cria expectativa irreal; pode levar a pressão desnecessária.
**Como evitar:** Usar estimativas do TODO como base; adicionar buffer de 20%.

---

## 8. Checklists

### Checklist de Pré-Execução

- [ ] ADR existe e está com status "Aceito" ou "Proposto"
- [ ] Blueprint existe e contém tarefas documentadas
- [ ] TODO existe e contém tarefas com estados
- [ ] Branch atual não é main/master (ou há PR aberto)
- [ ] Workspace está limpo (sem uncommitted changes)
- [ ] Todos os arquivos impactados existem
- [ ] Critérios de aceite estão definidos
- [ ] Critérios de rollback estão definidos
- [ ] Execution Contract gerado e validado
- [ ] DAG construído e validado (sem ciclos)

### Checklist de Pós-Execução

- [ ] Todas as tarefas do TODO marcadas como "Concluído"
- [ ] Build passa sem erros
- [ ] Lint passa sem erros
- [ ] Typecheck passa sem erros
- [ ] Testes unitários passam
- [ ] Testes de integração passam (se aplicável)
- [ ] ADRs relacionadas estão atualizadas
- [ ] Blueprint está sincronizado com código
- [ ] README está atualizado (se aplicável)
- [ ] Execution Report gerado
- [ ] Nenhum risco remanescente não documentado

---

## 9. Edge Cases

### ADR com status "Proposto" (não "Aceito")
**Situação:** O usuário quer implementar uma ADR que ainda não foi formalmente aceita.
**Solução:** Alertar que a ADR não está aceita; pedir confirmação explícita antes de prosseguir.
**Exceção:** Em contexto de prototipação, "Proposto" pode ser suficiente.

### Blueprint incompleto (tarefas sem dependências)
**Situação:** O Blueprint existe mas não documenta dependências entre tarefas.
**Solução:** Assumir que tarefas sem dependência explícita são independentes; construir DAG com base no que está disponível.
**Exceção:** Se mais de 50% das tarefas não têm dependências, alertar sobre possível incompletude.

### TODO com tarefas desatualizadas
**Situação:** O TODO não reflete o estado atual do código (tarefas já executadas manualmente).
**Solução:** Antes de iniciar, verificar estado real do código contra o TODO; atualizar estados antes de construir DAG.
**Exceção:** Nenhuma — TODO deve sempre estar sincronizado antes de execução.

### Implementação com múltiplas ADRs
**Situação:** A mudança envolve mais de uma ADR (ex: ADR-004 + ADR-005).
**Solução:** Criar um Execution Contract para cada ADR; executar sequencialmente (uma ADR por vez); ou criar um "meta-contracto" se as ADRs são acopladas.
**Exceção:** Se as ADRs são totalmente independentes, podem ser executadas em paralelo (worktrees separados).

### Rollback durante execução
**Situação:** Tarefa executada causou problema que requer rollback.
**Solução:** Gerar `rollback-report.md`, reverter commits da tarefa, marcar tarefa como "Bloqueado", analisar causa raiz.
**Exceção:** Se o rollback corrompe o estado, interromper toda a implementação.

### Agente sem acesso a comandos de build/test
**Situação:** O agente não consegue rodar `npm test`, `cargo build`, etc.
**Solução:** Pular validação automatizada; marcar tarefa como "Concluído com ressalva"; documentar no Execution Report que validação manual é necessária.
**Exceção:** Nenhuma — neste caso, o Execution Report deve indicar claramente a ausência de validação.

---

## 10. Integração com Skills Existentes

### Referências Diretas (related_skills)

| Skill | Relação com `implementation` |
|-------|------------------------------|
| `adr-generator` | Consome ADRs geradas por esta skill |
| `writing-plans` | Consome Blueprints e TODOs gerados por esta skill |
| `planning` | Consome roadmap e estimativas |
| `documentation` | Delega atualização de documentação |
| `governance` | Respeita processos de revisão e aprovação |
| `testing` | Executa testes definidos nesta skill |
| `git` | Cria commits e branches seguindo padrões |
| `release` | Alimenta changelog e versionamento |
| `architecture-review-kilo` | Valida consistência arquitetural |
| `ddd` | Respeita modelos de domínio |
| `repo-bootstrap` | Compatível com estrutura de repositório |

### Referências Futuras (compatibilidade)

| Skill | Interação esperada |
|-------|-------------------|
| `security-review` | Validação de segurança durante execução |
| `refactoring` | Padrões de refatoração segura |
| `api-design` | Contratos de API durante implementação |
| `observability` | Instrumentação durante execução |
| `data-modeling` | Schema durante implementação |
| `agent-orchestration` | Coordenção multi-agente |

---

## 11. Estimativas

| Componente | Linhas Est. | Templates | Examples |
|------------|-------------|-----------|----------|
| SKILL.md | ~280 | — | — |
| execution-contract.md | ~60 | ✅ | — |
| execution-report.md | ~70 | ✅ | — |
| change-plan.md | ~50 | ✅ | — |
| rollback-report.md | ~40 | ✅ | — |
| task-progress.md | ~45 | ✅ | — |
| simple-change.md | ~80 | — | ✅ |
| complex-change.md | ~120 | — | ✅ |
| pre-execution.md | ~25 | ✅ | — |
| post-execution.md | ~25 | ✅ | — |
| **Total** | **~795** | **7** | **2** |

---

## 12. Riscos e Mitigações

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Skill muito complexa para agentes seguirem | Alto | Média | Progressive Disclosure + decision tree clara |
| Acoplamento forte com muitas skills | Médio | Alta | Contratos de I/O bem definidos |
| Agentes podem ignorar Execution Contract | Alto | Média | Tornar contract obrigatório no workflow |
| Dificuldade de debug durante execução | Médio | Média | task-progress.md detalhado |
| Manutenção de 7 templates | Baixo | Média | Templates simples e autoexplicativos |

---

*Documento gerado em 2026-07-05. Referência: ADR-005.*
