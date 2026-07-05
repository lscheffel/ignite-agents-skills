# TODO: {{title}}

> ADR-{{id}} | Início: {{date}} | Status: ⬜ PENDENTE

---

## Legenda

- ✅ Concluído
- ⬜ Pendente
- 🔄 Em Andamento
- ❌ Bloqueado
- ⏸️ Pausado

**Prioridade:** 🔴 Alta | 🟡 Média | 🟢 Baixa

---

## Fase A: {{phase_a_title}}

### A1: {{phase_a_subtitle}}

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| A1.1 | {{task_a1_1}} | ⬜ | 🔴 | — | {{time_a1_1}} |
| A1.2 | {{task_a1_2}} | ⬜ | 🔴 | A1.1 | {{time_a1_2}} |
| A1.3 | {{task_a1_3}} | ⬜ | 🔴 | A1.1 | {{time_a1_3}} |

**Checkpoint A1:**
- [ ] {{checkpoint_a1_1}}
- [ ] {{checkpoint_a1_2}}

---

### A2: {{phase_a2_subtitle}}

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| A2.1 | {{task_a2_1}} | ⬜ | 🔴 | A1 | {{time_a2_1}} |
| A2.2 | {{task_a2_2}} | ⬜ | 🟡 | A1 | {{time_a2_2}} |
| A2.3 | {{task_a2_3}} | ⬜ | 🔴 | A2.2 | {{time_a2_3}} |

**Checkpoint A2:**
- [ ] {{checkpoint_a2_1}}
- [ ] {{checkpoint_a2_2}}

---

### A3: {{phase_a3_subtitle}}

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| A3.1 | {{task_a3_1}} | ⬜ | 🔴 | A2 | {{time_a3_1}} |
| A3.2 | {{task_a3_2}} | ⬜ | 🔴 | A3.1 | {{time_a3_2}} |
| A3.3 | {{task_a3_3}} | ⬜ | 🔴 | A3.2 | {{time_a3_3}} |

**Checkpoint A3:**
- [ ] {{checkpoint_a3_1}}
- [ ] {{checkpoint_a3_2}}

---

**Checkpoint Geral Fase A:**
- [ ] {{checkpoint_a_general_1}}
- [ ] {{checkpoint_a_general_2}}

---

## Fase B: {{phase_b_title}}

### B1: {{phase_b_subtitle}}

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| B1.1 | {{task_b1_1}} | ⬜ | 🔴 | A | {{time_b1_1}} |
| B1.2 | {{task_b1_2}} | ⬜ | 🔴 | B1.1 | {{time_b1_2}} |
| B1.3 | {{task_b1_3}} | ⬜ | 🔴 | B1.2 | {{time_b1_3}} |
| B1.4 | {{task_b1_4}} | ⬜ | 🟡 | B1.3 | {{time_b1_4}} |

**Checkpoint B1:**
- [ ] {{checkpoint_b1_1}}
- [ ] {{checkpoint_b1_2}}

---

### B2: {{phase_b2_subtitle}}

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| B2.1 | {{task_b2_1}} | ⬜ | 🔴 | B1 | {{time_b2_1}} |
| B2.2 | {{task_b2_2}} | ⬜ | 🔴 | B2.1 | {{time_b2_2}} |
| B2.3 | {{task_b2_3}} | ⬜ | 🟡 | B2.2 | {{time_b2_3}} |
| B2.4 | {{task_b2_4}} | ⬜ | 🔴 | B2.3 | {{time_b2_4}} |
| B2.5 | {{task_b2_5}} | ⬜ | 🔴 | B2.4 | {{time_b2_5}} |
| B2.6 | {{task_b2_6}} | ⬜ | 🔴 | B2.5 | {{time_b2_6}} |
| B2.7 | {{task_b2_7}} | ⬜ | 🔴 | B2.6 | {{time_b2_7}} |
| B2.8 | {{task_b2_8}} | ⬜ | 🔴 | B2.7 | {{time_b2_8}} |
| B2.9 | {{task_b2_9}} | ⬜ | 🟡 | B2.8 | {{time_b2_9}} |

**Checkpoint B2:**
- [ ] {{checkpoint_b2_1}}
- [ ] {{checkpoint_b2_2}}
- [ ] {{checkpoint_b2_3}}

---

**Checkpoint Geral Fase B:**
- [ ] {{checkpoint_b_general_1}}
- [ ] {{checkpoint_b_general_2}}

---

## Fase C: {{phase_c_title}}

### C1: {{phase_c_subtitle}}

| # | Tarefa | Status | Prioridade | Dependências | Estimativa |
|---|--------|--------|------------|--------------|------------|
| C1.1 | {{task_c1_1}} | ⬜ | 🟡 | B | {{time_c1_1}} |
| C1.2 | {{task_c1_2}} | ⬜ | 🟡 | C1.1 | {{time_c1_2}} |
| C1.3 | {{task_c1_3}} | ⬜ | 🟢 | B | {{time_c1_3}} |

**Checkpoint C1:**
- [ ] {{checkpoint_c1_1}}
- [ ] {{checkpoint_c1_2}}

---

**Checkpoint Geral Fase C:**
- [ ] {{checkpoint_c_general_1}}
- [ ] {{checkpoint_c_general_2}}

---

## Resumo Geral

| Fase | Tarefas | Horas Est. | Status |
|------|---------|------------|--------|
| Fase A: {{phase_a_title}} | {{count_a}} | ~{{hours_a}} | ⬜ |
| Fase B: {{phase_b_title}} | {{count_b}} | ~{{hours_b}} | ⬜ |
| Fase C: {{phase_c_title}} | {{count_c}} | ~{{hours_c}} | ⬜ |
| **Total** | **{{total}}** | **~{{total_hours}}** | |

---

## Dependências entre Fases

```
Fase A ({{phase_a_title_short}})
  │
  ├─── A1: {{a1_short}} ─────┐
  ├─── A2: {{a2_short}} ─────┤
  ├─── A3: {{a3_short}} ─────┤
  └─── A4: {{a4_short}} ─────┘
                                │
Fase B ({{phase_b_title_short}}) ◄──────────────────┘
  │
  ├─── B1: {{b1_short}} ───────┐
  └─── B2: {{b2_short}} ────────┘
                                │
Fase C ({{phase_c_title_short}}) ◄──────────────────┘
  │
  └─── C1: {{c1_short}} ────────┘
```

---

*Documento gerado em {{date}}. Referência: ADR-{{id}}.*