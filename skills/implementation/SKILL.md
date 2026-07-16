---
name: implementation
description: Executa mudanças previamente planejadas de forma governada e incremental. Consome ADRs, Blueprints e TODOs, valida Execution Contract, constrói DAG de execução, implementa com validação contínua e gera Execution Report. Use quando implementar uma ADR já aprovada.
version: 2.0.0
tags:
- implementation
- execution
- artifact-driven
- sdlc
- governance
related_skills:
- adr-archive
- adr-generator
- writing-plans
- planning
- testing
- git
- documentation
- governance
- release
- architecture-review-kilo
- ddd
---

# Implementation

Executa mudanças previamente planejadas de forma governada e incremental, fechando o ciclo do SDLC baseado em Agent Skills.

## ⚠️ Token Optimization (Skip Consolidated ADRs)
Quando você precisar varrer as ADRs do repositório para obter contexto, faça **PRIMEIRO** a leitura do `docs/adr/ADR-INDEX.md` ou um `grep` no frontmatter das ADRs. 
Você está **PROIBIDO** de ler o conteúdo completo (via `view_file` ou `cat`) de qualquer arquivo que possua a tag `implementation_status: CONSOLIDADA` no seu frontmatter YAML. Aplique o 'SKIP' sumário a esses arquivos, pois o conteúdo é passado e estático. Só faça a leitura profunda caso o usuário solicite especificamente uma auditoria, ou se a tarefa atual exigir a modificação daquela exata arquitetura.

## Quando Usar

### Use quando:
- Existe uma ADR aprovada (status "Aceito") que precisa ser implementada
- Existe um Blueprint e TODO associados à ADR
- Precisa de execução padronizada e reproduzível entre diferentes agentes
- Precisa de rastreabilidade completa durante a implementação
- Precisa de Execution Report ao término

### Não use quando:
- Ainda não existe ADR (use `adr-generator` primeiro)
- Precisa de planejamento (use `writing-plans` ou `planning`)
- A mudança é trivial (< 1 arquivo, < 30min) e não justifica governança
- Precisa de apenas um commit sem validação intermediária

### Skills relacionadas:
- `adr-generator` — gera as ADRs que esta skill consome
- `writing-plans` — gera Blueprints e TODOs que esta skill consome
- `testing` — executa testes durante validação contínua
- `git` — cria commits seguindo Conventional Commits
- `documentation` — atualiza documentação durante implementação
- `governance` — respeita processos de revisão e aprovação

## Decision Tree

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

## Conceitos Fundamentais

### Execution Contract

Contrato obrigatório que valida se todos os artefatos necessários estão presentes e coerentes antes de qualquer alteração.

**Campos do contrato:**
- ADR: path, status, decisão
- Blueprint: path, tarefas listadas
- TODO: path, tarefas com estados
- PI (Implementation Plan): path, passos granulares (TDD) **[Opcional / Recomendado]**
- Branch: nome, estado limpo
- Workspace: sem alterações não commitadas
- Arquivos impactados: lista extraída do PI
- Critérios de aceite: extraídos do TODO e do PI
- Critérios de rollback: definidos no Blueprint

**Regra de Auto-Repair:** Se a Tríade (ADR, BP, TODO) ou o PI estiverem ausentes, malformados ou divergirem dos templates padrão, a skill não deve abortar. O agente deve acionar a skill `adr-generator` (ou `writing-plans`) em modo **Retroactive Governance** para gerar ou refatorar os artefatos faltantes antes de iniciar a execução.

### Artifact Resolution

Processo de descoberta e correlação automática dos documentos envolvidos na mudança.

**Algoritmo:**
1. Buscar `ADR-XXX.md` no diretório `docs/adr/`
2. Derivar paths: `ADR-XXX-BP.md`, `ADR-XXX-TODO.md` e `ADR-XXX-PI.md`
3. Verificar existência de cada artefato (PI é opcional, mas gera execução legacy se ausente)
4. Extrair `related_skills` do frontmatter
5. Mapear arquivos impactados a partir do PI
6. Retornar mapa consolidado

### Execution Loop

Modelo incremental de execução. O loop tenta consumir o PI (Implementation Plan) em passos granulares (TDD). Se o PI não existir, o loop opera em modo **Legacy**, consumindo diretamente as tarefas macro do TODO:

1. **Ler** o plano detalhado no `ADR-XXX-PI.md` (ou o `ADR-XXX-TODO.md` no modo Legacy)
2. **Selecionar** tarefa (via DAG, respeitando dependências)
3. **Executar** alteração no código seguindo os passos prescritos (micro-tarefas no PI ou macro-escopo no TODO)
4. **Validar** (build, lint, typecheck, testes)
5. **Atualizar** documentação afetada
6. **Marcar** tarefa como concluída no PI e refletir o progresso no TODO
7. **Reavaliar** dependências (próximas tarefas podem iniciar)

**Regras:**
- Máximo 1 tarefa "Em andamento" por vez
- Tarefa só inicia se todas as dependências estão "Concluído"
- Se validação falhar, tarefa vai para "Bloqueado" até correção
- Big Bang é estritamente proibido

### Change Lifecycle

Modelo formal do ciclo de vida de uma mudança:

```
ADR → Blueprint → TODO → PI → Execution Contract → Artifact Resolution
  → Implementation → Validation → Documentation Update → Execution Report
```

## Workflow

### Workflow 1: Artifact Resolution

**Objetivo:** Descobrir e correlacionar todos os artefatos envolvidos.

1. Identificar a ADR de referência (por nome ou contexto)
2. Derivar paths: `ADR-XXX-BP.md`, `ADR-XXX-TODO.md`, `ADR-XXX-PI.md`
3. Verificar existência de cada artefato
4. Ler frontmatter da ADR para extrair status e decisão
5. Ler Blueprint para extrair fases macro
6. Ler TODO para extrair estados macro
7. Ler PI para extrair tarefas granulares e código
8. Mapear `related_skills` do frontmatter
9. Extrair arquivos impactados do PI
9. Retornar **Artifact Map** consolidado
10. **Checkpoint**: Todos os artefatos existem e estão coerentes

### Workflow 2: Execution Contract

**Objetivo:** Validar que a implementação pode iniciar com segurança.

1. Carregar Artifact Map (Workflow 1)
2. Validar se a ADR, BP e TODO existem e são coerentes.
3. Se faltar artefatos ou os templates estiverem desatualizados, **pause a validação e inicie o Auto-Repair**:
   - Acione a skill `adr-generator` para aplicar a governança retroativa (Retroactive Governance).
4. Verificar se o PI existe (Opcional, mas altera o workflow para Zen-Mode ou Legacy).
5. Validar que o PI (se existir) contém passos TDD ou que o TODO (se Legacy) contém tarefas.
6. Validar branch atual (não main/master sem PR)
7. Validar workspace limpo (sem uncommitted changes)
8. Validar que arquivos impactados existem
9. Extrair critérios de aceite do TODO e PI
10. Extrair critérios de rollback do Blueprint
11. Gerar `execution-contract.md` preenchido
11. **Checkpoint**: Contrato assinado (todos os campos válidos)

### Workflow 3: Dependency Analysis & Execution Plan

**Objetivo:** Construir DAG e plano de execução.

1. Ler PI e extrair todas as micro-tarefas
2. Ler dependências de cada tarefa no PI
3. Construir grafo dirigido acíclico (DAG)
4. Detectar ciclos (se existir, reportar erro e interromper)
5. Topological sort para ordem de execução
6. Identificar tarefas paralelizáveis (sem dependência entre si)
7. Gerar `change-plan.md` com DAG e ordem
8. Estimar tempo total a partir das estimativas do TODO
9. **Checkpoint**: DAG válido, sem ciclos, ordem definida

### Workflow 4: Incremental Execution

**Objetivo:** Executar tarefas uma a uma com validação.

Para cada tarefa na ordem do DAG (derivada do PI ou do TODO, se Legacy):

1. Verificar que todas as dependências estão "Concluído"
2. Marcar tarefa como "Em andamento" (no PI e no TODO simultaneamente se Zen-Mode, ou apenas no TODO se Legacy)
3. Gerar `task-progress.md` para a tarefa
4. Ler passos exatos (TDD no PI) ou inferir implementação (TODO no Legacy)
5. Executar as alterações no código exatamente como prescritas ou inferidas
6. Executar validação contínua (Workflow 5)
7. Se validação passar:
   - Atualizar documentação afetada
   - Marcar tarefa como "Concluído" no PI e atualizar TODO
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
5. Verificar se README precisa de atualização
6. Se sim, atualizar README
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

### Workflow 8: Final Audit & Handoff (GATEKEEPER RESTRITO)

**Objetivo:** Invocar a auditoria para fechamento de ciclo e geração indireta do Execution Report.

<HARD-GATE>
**PROIBIÇÃO ABSOLUTA DE GERAR ARQUIVOS `ER.md` DIRETAMENTE.**
Você (agente) está ESTRITAMENTE PROIBIDO de criar, editar ou mockar qualquer arquivo que termine em `*-ER.md`. A geração do Execution Report agora é de competência EXCLUSIVA do gatekeeper algorítmico (`audit.py` / `adr-archive`).
</HARD-GATE>

**Passo Final (Obrigatório):**
1. Você deve **tocar fisicamente** o arquivo `TODO.md` (ou `*-PI.md`) e marcar os checkboxes das tarefas concluídas com `- [x]`.
2. Após finalizar todas as marcações, **NÃO** gere o ER. Em vez disso, você **DEVE OBRIGATORIAMENTE** rodar o motor de auditoria executando o comando no terminal:
   `python3 ~/.gemini/config/skills/adr-archive/scripts/audit.py .`
3. Após o comando rodar, leia a saída do terminal e o relatório gerado na pasta `docs/reports`. Apresente um resumo claro e direto para o usuário informando o veredito do Janitor (ex: se o sistema aprovou o arquivamento e gerou o ER, ou se ainda há débitos a corrigir).

## Templates

### execution-contract.md
Localização: `templates/execution-contract.md`

Contrato obrigatório que deve ser preenchido e validado antes de qualquer alteração. Contém artefatos, ambiente, critérios de aceite e rollback.

### execution-report.md
Localização: `templates/execution-report.md`

Relatório final gerado ao término da implementação. Documenta tarefas concluídas, validações, riscos e recomendações.

### change-plan.md
Localização: `templates/change-plan.md`

Plano interno de execução com DAG de dependências, ordem de execução e estimativas.

### rollback-report.md
Localização: `templates/rollback-report.md`

Relatório produzido quando uma implementação requer reversão. Documenta motivo, tarefas revertidas e ações corretivas.

### task-progress.md
Localização: `templates/task-progress.md`

Progresso individual de cada tarefa durante a execução. Rastreia estado, alterações, validações e bloqueadores.

## Anti-patterns

### 🔴 Crítico

#### Executar sem Execution Contract
**O que é:** Iniciar alterações sem validar que ADR, Blueprint e TODO existem e estão coerentes.
**Por que é ruim:** Pode levar a implementação inconsistente com a decisão arquitetural.
**Como evitar:** Sempre rodar Artifact Resolution e Contract. Se faltarem arquivos, inicie o processo de **Auto-Repair** com `adr-generator`.
**Exemplo:**
```
# ❌ ERRADO
"Vou implementar a ADR-005 agora" (sem verificar se Blueprint existe)

# ✅ CORRETO
1. Gerar Artifact Map
2. Faltou BP? → Auto-Repair via adr-generator
3. Validar Execution Contract
4. Iniciar execução
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

## Checklists

### Checklist de Pré-Execução
Localização: `checklists/pre-execution.md`

Executar antes de iniciar qualquer implementação. Valida artefatos, coerência, ambiente, arquivos impactados, critérios e dependências.

### Checklist de Pós-Execução
Localização: `checklists/post-execution.md`

Executar após concluir toda a implementação. Valida tarefas, build, qualidade, testes, documentação, registry, git, riscos e relatório.

## Edge Cases

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

## Referências

- [ADR-005: Introdução da Skill implementation](../../docs/adr/archive/ADR-005.md)
- [ADR-005-BP: Blueprint detalhado](../../docs/adr/archive/ADR-005-BP.md)
- [ADR-002: Ultra-High Quality Grade](../../docs/adr/archive/ADR-002.md)
- [Skill adr-generator](../adr-generator/SKILL.md)
- [Skill writing-plans](../writing-plans/SKILL.md)
- [Skill testing](../testing/SKILL.md)
- [Skill governance](../governance/SKILL.md)
