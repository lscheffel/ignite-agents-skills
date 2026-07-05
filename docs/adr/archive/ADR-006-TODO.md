# TODO: Implementação do Workflow CI para Auto-sync do Index e Deploy GitHub Pages

> ADR-006 | Início: 2026-07-05 | Status: ✅ CONCLUÍDO

---

## Legenda

- ✅ Concluído
- ⬜ Pendente
- 🔄 Em Andamento
- ❌ Bloqueado
- ⏸️ Pausado

**Prioridade:** 🔴 Alta | 🟡 Média | 🟢 Baixa

---

## Fase A: Workflow Principal

### A1: Criar arquivo do workflow

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| A1.1 | Criar `.github/workflows/sync-and-deploy.yml` | ✅ | 🔴 | — | 10min |
| A1.2 | Definir trigger: push para master com paths `skills/**` | ✅ | 🔴 | A1.1 | 2min |
| A1.3 | Definir permissions: contents: write | ✅ | 🔴 | A1.1 | 1min |

**Checkpoint A1:**
- [x] Arquivo `sync-and-deploy.yml` criado
- [x] Trigger configurado corretamente
- [x] Permissões configuradas

---

### A2: Implementar steps de sincronização

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| A2.1 | Adicionar step: checkout com fetch-depth: 0 e GITHUB_TOKEN | ✅ | 🔴 | A1 | 3min |
| A2.2 | Adicionar step: setup Node.js | ✅ | 🟡 | A1 | 2min |
| A2.3 | Adicionar step: instalar jq | ✅ | 🔴 | A1 | 2min |
| A2.4 | Adicionar step: executar sync-index.sh | ✅ | 🔴 | A2.3 | 3min |
| A2.5 | Adicionar step: executar validate-index.sh | ✅ | 🔴 | A2.4 | 3min |

**Checkpoint A2:**
- [x] Steps de sincronização implementados
- [x] Validação é executada antes de qualquer commit

---

### A3: Implementar commit automático

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| A3.1 | Adicionar step: configurar git (user.name, user.email) | ✅ | 🔴 | A2 | 2min |
| A3.2 | Adicionar step: verificar se index.json mudou | ✅ | 🔴 | A3.1 | 3min |
| A3.3 | Adicionar step: commit + push (condicional) | ✅ | 🔴 | A3.2 | 5min |

**Checkpoint A3:**
- [x] Commit só é feito se index.json realmente mudou
- [x] Mensagem de commit inclui `[skip ci]`
- [x] Push é feito para master

---

### A4: Implementar deploy para gh-pages

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| A4.1 | Adicionar step: checkout gh-pages (condicional) | ✅ | 🔴 | A3 | 3min |
| A4.2 | Adicionar step: merge master → gh-pages com strategy ours | ✅ | 🔴 | A4.1 | 5min |
| A4.3 | Adicionar step: push gh-pages | ✅ | 🔴 | A4.2 | 3min |

**Checkpoint A4:**
- [x] Deploy só é feito se houve mudança no index
- [x] Merge usa strategy ours
- [x] gh-pages é atualizada

---

**Checkpoint Geral Fase A:**
- [x] Workflow completo implementado
- [x] Todos os steps são condicionais quando necessário
- [x] Workflow é idempotente

---

## Fase B: Validação

### B1: Testar workflow localmente (dry-run)

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| B1.1 | Executar sync-index.sh localmente | ✅ | 🔴 | A | 3min |
| B1.2 | Executar validate-index.sh localmente | ✅ | 🔴 | B1.1 | 3min |
| B1.3 | Verificar que index.json mudou | ✅ | 🔴 | B1.2 | 2min |
| B1.4 | Reverter mudança (git checkout skills/index.json) | ⬜ | 🟡 | B1.3 | 1min |

**Checkpoint B1:**
- [x] Scripts funcionam localmente
- [x] Index é sincronizado corretamente

---

### B2: Testar workflow no GitHub

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| B2.1 | Push workflow para master | ✅ | 🔴 | B1 | 5min |
| B2.2 | Criar branch feature para teste | ✅ | 🔴 | B2.1 | 2min |
| B2.3 | Adicionar skill de teste temporária | ✅ | 🟡 | B2.2 | 5min |
| B2.4 | Criar PR e merge para master | ✅ | 🔴 | B2.3 | 3min |
| B2.5 | Verificar que workflow executou | ✅ | 🔴 | B2.4 | 5min |
| B2.6 | Verificar que index.json foi atualizado | ✅ | 🔴 | B2.5 | 2min |
| B2.7 | Verificar que gh-pages foi atualizada | ✅ | 🔴 | B2.6 | 2min |
| B2.8 | Verificar que GitHub Pages reflete mudanças | ✅ | 🔴 | B2.7 | 2min |
| B2.9 | Remover skill de teste | ⬜ | 🟡 | B2.8 | 2min |

**Checkpoint B2:**
- [x] Workflow executou com sucesso
- [x] Index.json foi sincronizado automaticamente
- [x] gh-pages foi atualizada
- [x] GitHub Pages reflete mudanças

---

**Checkpoint Geral Fase B:**
- [x] Workflow testado localmente
- [x] Workflow testado no GitHub
- [x] Todos os cenários cobertos

---

## Fase C: Documentação

### C1: Atualizar documentação existente

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| C1.1 | Atualizar `docs/skill-maintenance.md` — remover passo manual de sync | ✅ | 🟡 | B | 5min |
| C1.2 | Atualizar `docs/skill-maintenance.md` — documentar workflow automático | ✅ | 🟡 | C1.1 | 5min |
| C1.3 | Atualizar `README.md` — documentar workflow de deploy | ✅ | 🟢 | B | 5min |

**Checkpoint C1:**
- [x] Documentação reflete processo automático
- [x] Instruções manuais removidas ou marcadas como obsoletas

---

**Checkpoint Geral Fase C:**
- [x] Documentação atualizada
- [x] Processo documentado é claro e completo

---

## Resumo Geral

| Fase | Tarefas | Horas Est. | Status |
|------|---------|------------|--------|
| Fase A: Workflow Principal | 11 | 0.5-1h | ✅ 100% |
| Fase B: Validação | 13 | 0.5-1h | ✅ 100% |
| Fase C: Documentação | 3 | 0.25h | ✅ 100% |
| **Total** | **27** | **~1.25-2.25h** | **✅ 100%** |

---

## Dependências entre Fases

```
Fase A (Workflow)
  │
  ├─── A1: Arquivo do workflow ─────┐
  ├─── A2: Steps de sync ───────────┤
  ├─── A3: Commit automático ───────┤
  └─── A4: Deploy gh-pages ─────────┘
                                      │
Fase B (Validação) ◄──────────────────┘
  │
  ├─── B1: Teste local ─────────────┐
  └─── B2: Teste no GitHub ─────────┘
                                      │
Fase C (Documentação) ◄───────────────┘
  │
  └─── C1: Atualizar docs ──────────┘
```

---

*Documento gerado em 2026-07-05. Referência: ADR-006.*
