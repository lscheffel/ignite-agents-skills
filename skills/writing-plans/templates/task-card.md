# Task Card Template

> Card individual de task para o Implementation Plan

---

## Task {{TASK_ID}}: {{TASK_NAME}}

**Fase:** {{FASE}}
**Dependências:** {{DEPENDENCIES}}
**Estimativa:** {{ESTIMATE}}

### Descrição
{{DESCRIPTION}}

### Arquivos

**Criar:**
- `{{NEW_FILE_1}}`
- `{{NEW_FILE_2}}`

**Modificar:**
- `{{MOD_FILE_1}}:{{LINE_RANGE}}`
- `{{MOD_FILE_2}}:{{LINE_RANGE}}`

**Testes:**
- `{{TEST_FILE}}`

### Interfaces

**Consome (de tasks anteriores):**
- `{{INTERFACE_1}}` — `{{TYPE_1}}`
- `{{INTERFACE_2}}` — `{{TYPE_2}}`

**Produz (para tasks seguintes):**
- `{{OUTPUT_1}}` — `{{TYPE_3}}`
- `{{OUTPUT_2}}` — `{{TYPE_4}}`

### Steps (TDD)

- [ ] **Step 1: Write Failing Test**

```{{LANG}}
// {{TEST_FILE}}
describe('{{FEATURE}}', () => {
  it('should {{BEHAVIOR}}', () => {
    const result = {{FUNCTION}}({{INPUT}});
    expect(result).to{{MATCHER}}({{EXPECTED}});
  });
});
```

**Run:** `{{TEST_CMD}}`
**Expected:** FAIL — `{{FAIL_REASON}}`

- [ ] **Step 2: Run Test to Verify Fail**

```bash
{{TEST_CMD}}
```

- [ ] **Step 3: Minimal Implementation**

```{{LANG}}
// {{MOD_FILE_1}}
export function {{FUNCTION}}({{PARAMS}}): {{RETURN_TYPE}} {
  return {{MINIMAL_IMPL}};
}
```

- [ ] **Step 4: Run Test to Verify Pass**

```bash
{{TEST_CMD}}
```

**Expected:** PASS

- [ ] **Step 5: Commit**

```bash
git add {{TEST_FILE}} {{MOD_FILE_1}}
git commit -m "{{CONVENTIONAL_COMMIT_MSG}}"
```

### Validação Pós-Commit

```bash
{{VALIDATION_CMD}}
```

**Critérios de Sucesso:**
- [ ] Tests pass
- [ ] Lint clean
- [ ] TypeCheck clean
- [ ] No regressions

---

*Template: `skills/writing-plans/templates/task-card.md`*