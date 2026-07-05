# Blueprint — ADR-{{id}}: {{title}}

> Referência: [ADR-{{id}}](./ADR-{{id}}.md)

---

## 1. Visão Geral

### Objetivo
{{objective}}

### Métricas de Sucesso

| Métrica | Antes | Depois | Status |
|---------|-------|--------|--------|
| {{metric_1}} | {{before_1}} | {{after_1}} | ⬜ |
| {{metric_2}} | {{before_2}} | {{after_2}} | ⬜ |

---

## 2. Estrutura de Artefatos

```
{{artifacts_structure}}
```

---

## 3. Decision Tree

```mermaid
graph TD
    {{decision_tree}}
```

---

## 4. Conceitos Fundamentais

### 4.1 {{concept_1_title}}

{{concept_1_description}}

**Configuração:**
```{{concept_1_config}}```

### 4.2 {{concept_2_title}}

{{concept_2_description}}

**Configuração:**
```{{concept_2_config}}```

---

## 5. Workflow

### Workflow 1: {{workflow_1_name}}

**Objetivo:** {{workflow_1_objective}}

**Triggers:**
- {{workflow_1_trigger}}

**Steps:**
{{workflow_1_steps}}

**Checkpoint:** {{workflow_1_checkpoint}}

---

## 6. Templates

### 6.1 {{template_1_name}}

```{{template_1_content}}```

---

## 7. Anti-patterns

### 🔴 Crítico

#### {{anti_pattern_1_title}}
**O que é:** {{anti_pattern_1_what}}
**Por que é ruim:** {{anti_pattern_1_why}}
**Como evitar:** {{anti_pattern_1_how}}
**Exemplo:**
```bash
# ❌ ERRADO
{{anti_pattern_1_wrong}}

# ✅ CORRETO
{{anti_pattern_1_right}}
```

### 🟡 Médio

#### {{anti_pattern_2_title}}
**O que é:** {{anti_pattern_2_what}}
**Por que é ruim:** {{anti_pattern_2_why}}
**Como evitar:** {{anti_pattern_2_how}}

### 🟢 Baixo

#### {{anti_pattern_3_title}}
**O que é:** {{anti_pattern_3_what}}
**Por que é ruim:** {{anti_pattern_3_why}}
**Como evitar:** {{anti_pattern_3_how}}

---

## 8. Checklists

### Checklist de Pré-Deploy

- [ ] {{checklist_pre_1}}
- [ ] {{checklist_pre_2}}

### Checklist de Pós-Deploy

- [ ] {{checklist_post_1}}
- [ ] {{checklist_post_2}}

---

## 9. Edge Cases

### {{edge_case_1_title}}
**Situação:** {{edge_case_1_situation}}
**Solução:** {{edge_case_1_solution}}
**Exceção:** {{edge_case_1_exception}}

### {{edge_case_2_title}}
**Situação:** {{edge_case_2_situation}}
**Solução:** {{edge_case_2_solution}}
**Exceção:** {{edge_case_2_exception}}

---

## 10. Integração com Skills Existentes

### Referências Diretas

| Skill | Relação com o workflow |
|-------|------------------------|
| `{{skill_1}}` | {{skill_1_relation}} |
| `{{skill_2}}` | {{skill_2_relation}} |

---

## 11. Estimativas

| Componente | Linhas Est. | Templates | Examples |
|------------|-------------|-----------|----------|
| {{component_1}} | {{lines_1}} | {{templates_1}} | {{examples_1}} |
| **Total** | **{{total_lines}}** | **{{total_templates}}** | **{{total_examples}}** |

---

## 12. Riscos e Mitigações

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| {{risk_1}} | {{impact_1}} | {{likelihood_1}} | {{mitigation_1}} |
| {{risk_2}} | {{impact_2}} | {{likelihood_2}} | {{mitigation_2}} |

---

*Documento gerado em {{date}}. Referência: ADR-{{id}}.*