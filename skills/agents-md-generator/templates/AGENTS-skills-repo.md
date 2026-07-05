# AGENTS.md - Repositório de Skills

## Visão Geral

Este repositório contém skills para agentes de IA seguindo o padrão Ultra-High Quality Grade. Cada skill é um módulo independente que pode ser carregado por agentes de IA para executar tarefas específicas.

## Estrutura do Projeto

```
skills/
├── skill-name/
│   ├── SKILL.md                    # Documentação principal
│   ├── templates/                  # Templates reutilizáveis
│   ├── examples/                   # Exemplos de uso
│   └── checklists/                 # Checklists de validação
├── index.json                      # Índice de todas as skills
└── README.md                       # Documentação principal
```

### Descrição dos Diretórios

- **skills/**: Contém todas as skills do repositório
- **docs/**: Documentação do projeto
- **scripts/**: Scripts de automação
- **templates/**: Templates para novas skills

## Padrões de Código

### Convenções

- Seguir padrão Ultra-High Quality Grade para todas as skills
- Usar Markdown para documentação
- Incluir frontmatter válido em todas as skills
- Manter consistência de formatação

### Formatação

- Usar 2 espaços para indentação
- Manter linhas com máx. 80 caracteres
- Usar code blocks com linguagem especificada
- Incluir linhas vazias entre seções

### Naming

- Nomes de skills em kebab-case
- Arquivos em snake_case ou kebab-case
- Diretórios em kebab-case

## Comandos Importantes

### Desenvolvimento

```bash
# Criar nova skill
mkdir -p skills/{skill-name}/{templates,examples,checklists}
cp templates/skill-template.md skills/{skill-name}/SKILL.md

# Validar skill
bash scripts/validate-skill.sh skills/{skill-name}

# Sincronizar index
./scripts/sync-index.sh

# Validar index
./scripts/validate-index.sh
```

### Build

```bash
# Não há build necessário - projeto é documentação
```

### Testes

```bash
# Validar todas as skills
for skill in skills/*/; do
  bash scripts/validate-skill.sh "$skill"
done
```

### Deploy

```bash
# Deploy automático via GitHub Pages
git push origin master
```

## Governança

### Branching Strategy

- **master**: Código principal, sempre deployável
- **feature/***: Novas features
- **fix/***: Correções
- **docs/***: Atualizações de documentação

### Processo de PR

1. Criar branch a partir de `master`
2. Fazer commits pequenos e focados
3. Abrir PR com descrição completa
4. Aguardar CI verde
5. Merge após aprovação

### Code Review

- Pelo menos 1 aprovação necessária
- Verificar qualidade da documentação
- Testar skill localmente
- Verificar compatibilidade

### CI/CD

- GitHub Actions para validação
- Deploy automático para GitHub Pages
- Validação de skills em cada PR

## Skills Recomendadas

- `git` — para commits e branches
- `testing` — para testes
- `documentation` — para padrões de docs
- `governance` — para processos
- `skill-audit-bulletin` — para auditoria de skills

## Anti-patterns

### 🔴 Crítico

#### Skill sem SKILL.md
**O que é:** Skill sem documentação principal.
**Por que é ruim:** Agentes não sabem como usar a skill.
**Como evitar:** Sempre criar SKILL.md com frontmatter válido.

#### Skill sem validação
**O que é:** Skill não passa no validate-skill.sh.
**Por que é ruim:** Pode conter erros estruturais.
**Como evitar:** Sempre validar antes de commitar.

### 🟡 Médio

#### Templates não reutilizáveis
**O que é:** Templates específicos demais para um caso.
**Por que é ruim:** Dificulta reuso em outros projetos.
**Como evitar:** Criar templates genéricos com placeholders.

#### Exemplos incompletos
**O que é:** Exemplos sem contexto ou explicação.
**Por que é ruim:** Dificulta entendimento da skill.
**Como evitar:** Incluir contexto e explicação em cada exemplo.

### 🟢 Baixo

#### Documentação desatualizada
**O que é:** SKILL.md não reflete funcionalidade atual.
**Por que é ruim:** Confunde usuários.
**Como evitar:** Atualizar documentação a cada mudança.

## Edge Cases

### Múltiplas versões da mesma skill
**Situação:** Precisa manter múltiplas versões de uma skill.
**Solução:** Usar versionamento semântico no frontmatter.
**Exceção:** Versões antigas devem ser movidas para archive.

### Skill com dependências circulares
**Situação:** Skill A depende de Skill B que depende de Skill A.
**Solução:** Reestruturar skills para eliminar dependência circular.
**Exceção:** Se impossível, documentar limitação claramente.

### Conflicts entre skills
**Situação:** Duas skills tentam modificar o mesmo arquivo.
**Solução:** Definir ordem de prioridade e documentar conflitos.
**Exceção:** Se conflito é crítico, reconsiderar design.

## Referências

- [Ultra-High Quality Grade](./docs/adr/ADR-002.md)
- [Skill Maintenance](./docs/skill-maintenance.md)
- [Governance](./skills/governance/SKILL.md)
- [Documentation](./skills/documentation/SKILL.md)

---

*Gerado automaticamente por `agents-md-generator` em {{generation_date}}*
*Última atualização: {{last_update}}*
