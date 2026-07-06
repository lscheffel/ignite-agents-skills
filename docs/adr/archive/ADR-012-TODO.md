# TODO: Dynamic HTML Pages — Rendering de Skills em GitHub Pages

> ADR-012 | Início: 2026-07-05 | Status: ✅ CONCLUÍDO

---

## Legenda

- ✅ Concluído
- ⬜ Pendente
- 🔄 Em Andamento
- ❌ Bloqueado
- ⏸️ Pausado

**Prioridade:** 🔴 Alta | 🟡 Média | 🟢 Baixa

---

## Fase A: Infraestrutura do Build Script

### A1: Conversor Markdown→HTML

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| A1.1 | Implementar `md_escape()` para HTML escaping | ✅ | 🔴 | — | 5min |
| A1.2 | Implementar `convert_inline_md()` (bold, italic, code, links, images) | ✅ | 🔴 | A1.1 | 15min |
| A1.3 | Implementar `convert_md_to_html()` com state machine (headers, lists, tables, blockquotes, code blocks) | ✅ | 🔴 | A1.2 | 45min |
| A1.4 | Implementar `render_table()` para tabelas Markdown | ✅ | 🔴 | A1.3 | 10min |

**Checkpoint A1:**
- [x] Conversor MD→HTML funciona com SKILL.md reais
- [x] Suporta code blocks, tables, lists, blockquotes

---

### A2: Template HTML e CSS

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| A2.1 | Definir variáveis CSS (tema escuro charcoal/laranja/branco) | ✅ | 🔴 | — | 10min |
| A2.2 | Implementar CSS para nav sticky, breadcrumbs, content, typography | ✅ | 🔴 | A2.1 | 30min |
| A2.3 | Implementar CSS para cards, file-lists, search, tables, code blocks | ✅ | 🔴 | A2.2 | 20min |
| A2.4 | Implementar CSS responsivo (mobile-first) | ✅ | 🟡 | A2.3 | 10min |
| A2.5 | Criar `get_page_template()` com nav, breadcrumb, footer | ✅ | 🔴 | A2.2 | 15min |

**Checkpoint A2:**
- [x] Tema escuro consistente em todas as páginas
- [x] Nav sticky funcional com links para Skills, README, USAGE
- [x] Breadcrumbs de navegação

---

## Fase B: Geradores de Página

### B1: Página Index

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| B1.1 | Implementar `generate_index()` com cards de skills | ✅ | 🔴 | A2.5 | 20min |
| B1.2 | Adicionar busca em tempo real (JavaScript) | ✅ | 🟡 | B1.1 | 10min |
| B1.3 | Estilo fancy title com gradiente | ✅ | 🟡 | B1.1 | 10min |

**Checkpoint B1:**
- [x] 23 skills listadas com cards
- [x] Busca filtra por nome, tag ou descrição

---

### B2: Páginas de Skill

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| B2.1 | Implementar `generate_skill_page()` para SKILL.md | ✅ | 🔴 | A1.4, A2.5 | 15min |
| B2.2 | Gerar lista de templates com links | ✅ | 🔴 | B2.1 | 10min |
| B2.3 | Gerar lista de examples com links | ✅ | 🔴 | B2.1 | 10min |
| B2.4 | Gerar lista de checklists com links | ✅ | 🟡 | B2.1 | 10min |

**Checkpoint B2:**
- [x] Cada skill tem página dedicada com SKILL.md formatado
- [x] Links para templates, examples e checklists

---

### B3: Páginas de Arquivos

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| B3.1 | Implementar `generate_file_page()` para templates | ✅ | 🔴 | A1.4, A2.5 | 10min |
| B3.2 | Gerar páginas para examples | ✅ | 🔴 | B3.1 | 5min |
| B3.3 | Gerar páginas para checklists | ✅ | 🟡 | B3.1 | 5min |

**Checkpoint B3:**
- [x] 72 templates renderizados como HTML
- [x] 18 examples renderizados como HTML
- [x] Checklists renderizados como HTML

---

### B4: Páginas de Documentação

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| B4.1 | Implementar `generate_doc_page()` para README.md | ✅ | 🔴 | A1.4, A2.5 | 10min |
| B4.2 | Gerar página USAGE.html | ✅ | 🟡 | B4.1 | 5min |
| B4.3 | Atualizar nav links para apontar para .html (não .md) | ✅ | 🔴 | B4.1 | 5min |

**Checkpoint B4:**
- [x] README.html renderizado e acessível
- [x] USAGE.html renderizado e acessível
- [x] Nav links apontam para versões HTML

---

## Fase C: CI/CD e Deploy

### C1: Workflow CI

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| C1.1 | Atualizar sync-and-deploy.yml com step de build de páginas | ✅ | 🔴 | B4.3 | 10min |
| C1.2 | Adicionar Setup Python 3.12 no workflow | ✅ | 🔴 | C1.1 | 5min |
| C1.3 | Adicionar detecção de mudanças em pages/ | ✅ | 🟡 | C1.1 | 5min |

**Checkpoint C1:**
- [x] Workflow roda build.py automaticamente
- [x] Commit com `[skip ci]` para evitar loops

---

### C2: Deploy

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| C2.1 | Manter .nojekyll em gh-pages | ✅ | 🔴 | — | 2min |
| C2.2 | Root index.html redireciona para pages/index.html | ✅ | 🔴 | — | 5min |
| C2.3 | Verificar que todas as páginas retornam 200 | ✅ | 🔴 | C1.3 | 5min |

**Checkpoint C2:**
- [x] pages/index.html → 200
- [x] pages/readme.html → 200
- [x] pages/usage.html → 200
- [x] pages/skills/*/index.html → 200
- [x] Root / → 200 (redirect)

---

**Checkpoint Geral Fase C:**
- [x] CI workflow funcional
- [x] Deploy automático para gh-pages
- [x] Todas as páginas acessíveis

---

## Resumo Geral

| Fase | Tarefas | Horas Est. | Status |
|------|---------|------------|--------|
| Fase A: Infraestrutura do Build Script | 8 | ~1.5h | ✅ |
| Fase B: Geradores de Página | 11 | ~1.5h | ✅ |
| Fase C: CI/CD e Deploy | 6 | ~0.5h | ✅ |
| **Total** | **25** | **~3.5h** | ✅ |

---

## Dependências entre Fases

```
Fase A (Infraestrutura)
  │
  ├─── A1: Conversor MD → HTML ──┐
  └─── A2: Template HTML/CSS ────┤
                                  │
Fase B (Geradores de Página) ◄────┘
  │
  ├─── B1: Index ────────────────┐
  ├─── B2: Páginas de Skill ─────┤
  ├─── B3: Páginas de Arquivo ───┤
  └─── B4: Páginas de Doc ───────┘
                                  │
Fase C (CI/CD e Deploy) ◄─────────┘
  │
  ├─── C1: Workflow CI ──────────┐
  └─── C2: Deploy ───────────────┘
```

---

*Documento gerado em 2026-07-05. Referência: ADR-012.*
