# Implementation Plan: Workflow CI para Auto-sync do Index e Deploy GitHub Pages

## Visão Geral

Automatizar o sincronismo do `skills/index.json` e o deploy para GitHub Pages via workflow de CI/CD. Quando uma nova skill é adicionada ou modificada em `./skills`, o workflow automaticamente:
1. Sincroniza o `index.json` usando `sync-index.sh`
2. Valida o index usando `validate-index.sh`
3. Commita a mudança na branch `master`
4. Faz merge na branch `gh-pages`
5. Atualiza o GitHub Pages

**Referência:** ADR-006, ADR-006-BP, ADR-006-TODO

---

## Épicos

### Épico 1: Workflow Principal (sync-and-deploy.yml)

- [ ] Criar arquivo `.github/workflows/sync-and-deploy.yml`
- [ ] Configurar trigger: push para master com paths `skills/**`
- [ ] Configurar permissions: contents: write
- [ ] Implementar steps de checkout, setup, sync, validate
- [ ] Implementar commit automático condicional
- [ ] Implementar deploy para gh-pages via merge

### Épico 2: Validação

- [ ] Testar scripts localmente (sync-index.sh + validate-index.sh)
- [ ] Testar workflow no GitHub (push, merge, verificar deploy)
- [ ] Verificar que GitHub Pages reflete mudanças

### Épico 3: Documentação

- [ ] Atualizar `docs/skill-maintenance.md`
- [ ] Atualizar `README.md`

---

## Timeline

| Fase | Tarefas | Tempo Est. | Dependências |
|------|---------|------------|--------------|
| Fase 1: Workflow | 6 tarefas | 30-45min | — |
| Fase 2: Validação | 3 tarefas | 30-45min | Fase 1 |
| Fase 3: Documentação | 2 tarefas | 10-15min | Fase 2 |
| **Total** | **11 tarefas** | **~70-105min** | — |

---

## Tarefa 1: Criar workflow sync-and-deploy.yml

**Arquivos:** `.github/workflows/sync-and-deploy.yml`  
**Complexidade:** M  
**Dependências:** Nenhuma  
**Critérios de aceitação:**
- [ ] Arquivo criado com trigger correto
- [ ] Permissions configuradas
- [ ] Steps de sync e validate implementados
- [ ] Commit automático com [skip ci]
- [ ] Deploy para gh-pages com strategy ours

**Comandos de validação:**
```bash
# Verificar syntax YAML
cat .github/workflows/sync-and-deploy.yml | python3 -c "import sys, yaml; yaml.safe_load(sys.stdin)"
```

---

## Tarefa 2: Testar scripts localmente

**Arquivos:** Nenhum (uso de scripts existentes)  
**Complexidade:** S  
**Dependências:** Tarefa 1  
**Critérios de aceitação:**
- [ ] `sync-index.sh` executa sem erros
- [ ] `validate-index.sh` retorna 0 erros
- [ ] `index.json` é sincronizado corretamente

**Comandos de validação:**
```bash
chmod +x scripts/sync-index.sh scripts/validate-index.sh
./scripts/sync-index.sh
./scripts/validate-index.sh
echo $?  # Deve retornar 0
```

---

## Tarefa 3: Testar workflow no GitHub

**Arquivos:** Nenhum  
**Complexidade:** M  
**Dependências:** Tarefa 1, Tarefa 2  
**Critérios de aceitação:**
- [ ] Workflow aparece em Actions tab
- [ ] Workflow executa quando skills são modificadas
- [ ] Index.json é sincronizado automaticamente
- [ ] gh-pages é atualizada
- [ ] GitHub Pages reflete mudanças

**Comandos de validação:**
```bash
# Verificar workflow via GitHub CLI
gh workflow list
gh run list --workflow=sync-and-deploy.yml
```

---

## Tarefa 4: Atualizar documentação

**Arquivos:** `docs/skill-maintenance.md`, `README.md`  
**Complexidade:** S  
**Dependências:** Tarefa 3  
**Critérios de aceitação:**
- [ ] `skill-maintenance.md` documenta processo automático
- [ ] Instruções manuais marcadas como obsoletas
- [ ] `README.md` menciona workflow de deploy

**Comandos de validação:**
```bash
grep -i "automático\|workflow\|sync" docs/skill-maintenance.md
grep -i "deploy\|gh-pages\|workflow" README.md
```

---

## Riscos

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Loop infinito de workflows | Baixa | Alto | `[skip ci]` no commit |
| Conflitos de merge | Baixa | Médio | Strategy `ours` |
| Token sem permissão | Baixa | Alto | `permissions: contents: write` |
| Index quebrado deployado | Baixa | Alto | `validate-index.sh` antes de commitar |

---

## Notas

- O workflow é **idempotente**: pode ser re-executado sem efeitos colaterais
- O workflow é **condicional**: só commita e deploya se houver mudanças reais
- O workflow é **auditável**: todos os steps são logados no GitHub Actions
- A strategy `ours` garante que `master` é sempre a fonte de verdade
- `[skip ci]` previne loop infinito de workflows

---

*Plano gerado em 2026-07-05. Referência: ADR-006.*
