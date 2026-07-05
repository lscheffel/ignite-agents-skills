# Manutenção de Skills

> Guia para criar e manter skills no padrão Ultra-High Quality Grade

---

## Como Criar uma Nova Skill

### 1. Estrutura de Diretórios

```bash
mkdir -p skills/{skill-name}/{templates,examples,checklists}
```

### 2. Frontmatter Obrigatório

```yaml
---
name: {skill-name}
description: {descrição em 1 linha, máx. 200 caracteres}
version: 2.0.0
tags: [tag1, tag2, tag3]
related_skills: [skill1, skill2]
---
```

### 3. Usar o Template Base

Copie `templates/skill-template.md` e adapte para a nova skill:

```bash
cp templates/skill-template.md skills/{skill-name}/SKILL.md
```

### 4. Preencher Seções Obrigatórias

- [ ] Quando Usar (critérios claros de uso)
- [ ] Decision Tree (ou justificativa para ausência)
- [ ] Workflow (≥3 fases com checkpoints)
- [ ] Conceitos Fundamentais
- [ ] Templates (arquivos em `templates/`)
- [ ] Anti-patterns (com severidade 🔴🟡🟢)
- [ ] Checklists
- [ ] Edge Cases
- [ ] Referências

### 5. Validar

```bash
bash scripts/validate-skill.sh skills/{skill-name}
```

### 6. Registrar no index.json

Adicione a nova skill ao `skills/index.json` com:
- name
- version
- tags
- related_skills
- files (paths relativos)

---

## Como Modificar uma Skill Existente

### 1. Atualizar Frontmatter

Se houver mudanças significativas, incremente a versão:
- **PATCH** (2.0.x): Correções menores, typos
- **MINOR** (2.x.0): Novas seções, templates adicionais
- **MAJOR** (x.0.0): Mudanças estruturais, remoção de conteúdo

### 2. Manter Backward Compatibility

- Não remova templates existentes sem criar novos
- Mantenha cross-references atualizados
- Atualize checklists se mudar workflows

### 3. Validar Após Modificação

```bash
bash scripts/validate-skill.sh skills/{skill-name}
```

---

## Checklist de Qualidade

### SKILL.md

- [ ] ≥150 linhas de conteúdo acionável
- [ ] Frontmatter completo e válido
- [ ] Decision tree presente (ou justificativa)
- [ ] ≥3 workflows numerados
- [ ] Checkpoints em cada workflow
- [ ] ≥3 anti-patterns com severidade
- [ ] Checklist de validação
- [ ] ≥1 edge case documentado
- [ ] ≥1 template referenciado
- [ ] ≥1 cross-reference

### Templates

- [ ] Arquivo em `templates/` com nome descritivo
- [ ] Template é reutilizável (não específico de um caso)
- [ ] Instruções de uso no SKILL.md
- [ ] Template inclui placeholders `{{placeholder}}`

### Examples

- [ ] Exemplo mostra "antes" e "depois"
- [ ] Exemplo é mínimo e focado
- [ ] Exemplo inclui contexto de uso

---

## Padrões de Escrita

### Tom e Estilo

- **Direto e técnico**: Evite conversa, foque em ação
- **Imperativo**: "Execute", "Crie", "Valide"
- **Verificável**: Cada passo pode ser testado
- **Contexto primeiro**: Explique por que antes do quê

### Formatação

- Markdown puro
- Code blocks com linguagem especificada
- Tabelas para dados estruturados
- Links relativos quando possível

### Cross-references

Use formato consistente:
```markdown
- `skill-name` — {contexto de relacionamento}
```

---

## Processo de Review

### Auto-review

1. Execute `validate-skill.sh`
2. Verifique ≥150 linhas
3. Confirme todos os checklists marcados

### Peer Review

1. Abra PR com mudanças
2. Solicite review de 1 maintainer
3. Execute skill com agente real
4. Merge após aprovação

---

## Troubleshooting

### Skill não passa na validação

**Erro: "SKILL.md não tem ≥150 linhas"**
- Adicione mais detalhes em workflows
- Inclua mais anti-patterns
- Documente edge cases

**Erro: "Frontmatter inválido"**
- Verifique sintaxe YAML
- Certifique-se de que todos os campos estão presentes

**Erro: "Seção ausente"**
- Use o template base como referência
- Cada seção é obrigatória

### Templates não são encontrados

- Verifique se a pasta `templates/` existe
- Confirme que os arquivos estão listados em `index.json`
- Use paths relativos no SKILL.md

---

*Última atualização: 2026-07-05. Referência: ADR-002.*