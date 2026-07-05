# AGENTS.md - ignite-agents-skills

## Visão Geral

Registro centralizado de skills para agentes de IA compatíveis com o padrão [Agent Skills](https://agentskills.io). Hospedado como GitHub Pages, este repositório serve como registry remoto para múltiplos projetos que usam **Kilo**, **OpenCode** e outros agentes compatíveis.

Contém **22 skills** categorizadas em Architecture, Documentation, Governance, Planning, Implementation, Quality, Security, AI, Orchestration, Data, API, Operations, Code Quality, Tools e Audit.

## Estrutura do Projeto

```
.
├── LICENSE
├── README.md                           # Documentação principal
├── USAGE.md                            # Guia completo de uso das skills
├── CHANGELOG.md                        # Histórico de versões
├── AGENTS.md                           # Este arquivo (guia para agentes de IA)
├── skills/
│   ├── index.json                      # Registry centralizado (fonte única)
│   ├── adr-generator/
│   ├── agent-orchestration/
│   ├── agents-md-generator/
│   ├── api-design/
│   ├── architecture-review-kilo/
│   ├── data-modeling/
│   ├── ddd/
│   ├── documentation/
│   ├── git/
│   ├── governance/
│   ├── implementation/
│   ├── observability/
│   ├── planning/
│   ├── prompt-engineering/
│   ├── refactoring/
│   ├── release/
│   ├── repo-bootstrap/
│   ├── security-review/
│   ├── skill-audit-bulletin/
│   ├── testing/
│   ├── vibe-coding/
│   └── writing-plans/
├── scripts/
│   ├── archive-adrs.sh                 # Arquiva ADRs implementadas
│   ├── sync-index.sh                   # Auto-gera index.json
│   ├── validate-index.sh               # Valida index.json contra arquivos reais
│   └── validate-skill.sh               # Valida qualidade Ultra-High Quality Grade
├── templates/                          # Templates para novas skills
└── docs/
    ├── adr/
    │   ├── INDEX.md                    # Índice de ADRs (active + archived)
    │   └── archive/                    # Cold storage (ADRs implementadas)
    └── skill-maintenance.md            # Guia de manutenção de skills
```

### Descrição dos Diretórios

- **skills/**: Contém todas as 22 skills do repositório, cada uma com SKILL.md, templates/, examples/ e checklists/
- **scripts/**: Scripts de automação para validação, sincronização e arquivamento
- **docs/**: Documentação do projeto incluindo ADRs e guias de manutenção
- **templates/**: Templates para criação de novas skills

## Padrões de Código

### Convenções

- Seguir padrão **Ultra-High Quality Grade** (v2.0.0+) para todas as skills
- Cada skill deve conter: Decision Trees (Mermaid), Workflows com checkpoints, Anti-patterns com severidade, Checklists, Edge Cases
- Usar Markdown para documentação
- Incluir frontmatter válido em todas as skills (name, description, version, tags, related_skills)
- Manter consistência de formatação

### Formatação

- Usar 2 espaços para indentação
- Manter linhas com máx. 80 caracteres
- Usar code blocks com linguagem especificada
- Incluir linhas vazias entre seções
- Usar tabelas Markdown para dados estruturados

### Naming

- Nomes de skills em kebab-case (ex: `architecture-review-kilo`)
- Arquivos de templates em snake_case ou kebab-case
- Diretórios em kebab-case
- ADRs numerados sequencialmente (ADR-001, ADR-002, etc.)

## Comandos Importantes

### Desenvolvimento

```bash
# Criar nova skill
mkdir -p skills/{skill-name}/{templates,examples,checklists}
cp templates/skill-template.md skills/{skill-name}/SKILL.md

# Validar skill específica
bash scripts/validate-skill.sh skills/{skill-name}

# Sincronizar index.json
./scripts/sync-index.sh

# Validar index.json
./scripts/validate-index.sh
```

### Build

```bash
# Não há build necessário - projeto é documentação
# GitHub Pages serve os arquivos Markdown diretamente
```

### Testes

```bash
# Validar todas as skills
for skill in skills/*/; do
  if [ -f "$skill/SKILL.md" ]; then
    echo "Validating: $skill"
    bash scripts/validate-skill.sh "$skill"
  fi
done

# Validar index.json contra arquivos reais
./scripts/validate-index.sh
```

### Deploy

```bash
# Deploy automático via GitHub Pages
git push origin master

# Workflow sync-and-deploy.yml sincroniza index.json e faz deploy
```

## Governança

### Branching Strategy

- **master**: Código principal, sempre deployável
- **feature/***: Novas features (ex: `feature/add-new-skill`)
- **fix/***: Correções (ex: `fix/validate-index-error`)
- **docs/***: Atualizações de documentação (ex: `docs/update-readme`)

### Processo de PR

1. Criar branch a partir de `master`
2. Fazer commits pequenos e focados (Conventional Commits)
3. Abrir PR com descrição completa
4. Aguardar CI verde (validate-skills.yml)
5. Merge após aprovação (mínimo 1 aprovação para equipes solo)

### Code Review

- Pelo menos 1 aprovação necessária (condicional para equipes solo)
- Verificar qualidade da documentação
- Testar skill localmente com `validate-skill.sh`
- Verificar compatibilidade com o padrão Agent Skills
- Validar que `index.json` está sincronizado

### CI/CD

- **validate-skills.yml**: Roda em push/PR que tocam `skills/**` ou `scripts/**`
  - Valida `index.json` contra arquivos reais
  - Valida qualidade Ultra-High Quality Grade de cada skill
- **sync-and-deploy.yml**: Sincroniza `index.json` e faz deploy para GitHub Pages

### Ciclo de Vida de uma ADR

Uma ADR segue um ciclo completo de 4 etapas:

```
ADR criada → Implementação → Arquivamento → Deploy gh-pages
```

#### Etapa 1: Criação
- Sempre criar ADR + BP + TODO simultaneamente (via `adr-generator`)
- Status inicial: "Proposto"

#### Etapa 2: Implementação
- Seguir o BP e executar as tarefas do TODO
- Validar cada tarefa com o comando especificado
- Ao concluir todas as tarefas sem débitos, atualizar status para "Implementado"

#### Etapa 3: Arquivamento (obrigatório após implementação completa)
- **Regra:** Toda ADR com status "Implementado" e sem débitos pendentes **deve** ser arquivada
- Executar: `./scripts/archive-adrs.sh`
- O script move ADR + BP + TODO para `docs/adr/archive/`
- Atualizar `docs/adr/INDEX.md` movendo a entrada para a seção "Archived ADRs"
- **Checklist de arquivamento:**
  - [ ] Status da ADR é "Implementado"
  - [ ] TODO tem 0 tarefas pendentes (`[ ]`)
  - [ ] Todos os comandos de validação passam
  - [ ] `archive-adrs.sh` executado com sucesso
  - [ ] INDEX.md atualizado

#### Etapa 4: Deploy gh-pages (obrigatório após arquivamento)
- **Regra:** Sempre que uma ADR é arquivada (etapa 3 concluída), a branch `gh-pages` deve ser atualizada
- A branch `gh-pages` reflete as skills e fluxos atuais, disponibilizando o repo para consumidores via GitHub Pages
- Processo:
  ```bash
  # Após merge no master
  git checkout gh-pages
  git merge master
  git push origin gh-pages
  git checkout master
  ```
- **Checklist de deploy:**
  - [ ] ADR arquivada com sucesso
  - [ ] Branch `gh-pages` atualizada com `master`
  - [ ] GitHub Pages reflete o estado atual

## Skills Recomendadas

- `git` — para commits e branches (Conventional Commits)
- `testing` — para testes automatizados
- `documentation` — para padrões de documentação
- `governance` — para processos de governança
- `skill-audit-bulletin` — para auditoria de qualidade de skills
- `repo-bootstrap` — para estrutura inicial de repositório
- `implementation` — para execução governada de mudanças

## Anti-patterns

### 🔴 Crítico

#### Skill sem SKILL.md
**O que é:** Skill sem documentação principal.
**Por que é ruim:** Agentes não sabem como usar a skill.
**Como evitar:** Sempre criar SKILL.md com frontmatter válido e todas as seções obrigatórias.

#### Skill sem validação
**O que é:** Skill não passa no `validate-skill.sh`.
**Por que é ruim:** Pode conter erros estruturais que quebram agentes.
**Como evitar:** Sempre validar antes de commitar: `bash scripts/validate-skill.sh skills/{skill-name}`

#### Index.json desincronizado
**O que é:** `skills/index.json` não reflete os arquivos reais no diretório.
**Por que é ruim:** Agentes não conseguem carregar skills que existem mas não estão no index.
**Como evitar:** Rodar `./scripts/sync-index.sh` antes de commitar mudanças em skills.

### 🟡 Médio

#### Templates não reutilizáveis
**O que é:** Templates específicos demais para um caso de uso.
**Por que é ruim:** Dificulta reuso em outros projetos.
**Como evitar:** Criar templates genéricos com placeholders bem documentados.

#### Exemplos incompletos
**O que é:** Exemplos sem contexto ou explicação.
**Por que é ruim:** Dificulta entendimento da skill.
**Como evitar:** Incluir contexto, explicação e output esperado em cada exemplo.

#### Anti-patterns sem severidade
**O que é:** Anti-patterns listados sem indicador de severidade (🔴🟡🟢).
**Por que é ruim:** Dificulta priorização de correções.
**Como evitar:** Sempre classificar anti-patterns por severidade.

### 🟢 Baixo

#### Documentação desatualizada
**O que é:** SKILL.md não reflete funcionalidade atual da skill.
**Por que é ruim:** Confunde usuários e agentes.
**Como evitar:** Atualizar documentação a cada mudança significativa.

#### Frontmatter incompleto
**O que é:** SKILL.md sem todos os campos obrigatórios (name, description, version, tags, related_skills).
**Por que é ruim:** Dificulta descoberta e categorização de skills.
**Como evitar:** Usar template de frontmatter e validar com `validate-skill.sh`.

## Edge Cases

### Múltiplas versões da mesma skill
**Situação:** Precisa manter múltiplas versões de uma skill.
**Solução:** Usar versionamento semântico no frontmatter (ex: `version: 2.0.0`).
**Exceção:** Versões antigas devem ser movidas para archive ou removidas.

### Skill com dependências circulares
**Situação:** Skill A depende de Skill B que depende de Skill A.
**Solução:** Reestruturar skills para eliminar dependência circular.
**Exceção:** Se impossível, documentar limitação claramente no SKILL.md.

### Conflicts entre skills
**Situação:** Duas skills tentam modificar o mesmo arquivo.
**Solução:** Definir ordem de prioridade e documentar conflitos.
**Exceção:** Se conflito é crítico, reconsiderar design das skills.

### Novos tipos de projeto
**Situação:** Precisa criar skill para tipo de projeto não coberto.
**Solução:** Usar `AGENTS-base.md` como template e personalizar.
**Exceção:** Se o tipo é muito específico, considerar extensão de skill existente.

### Contexto incerto
**Situação:** Detecção de contexto tem confiança <80%.
**Solução:** Pedir confirmação do usuário antes de gerar ou atualizar AGENTS.md.
**Exceção:** Em contexto de prototipação, usar melhor estimativa disponível.

## Referências

- [Ultra-High Quality Grade](./docs/adr/archive/ADR-002.md) — Padrão de qualidade das skills
- [Skill Maintenance](./docs/skill-maintenance.md) — Guia de manutenção de skills
- [Governance](./skills/governance/SKILL.md) — Processos de governança
- [Documentation](./skills/documentation/SKILL.md) — Padrões de documentação
- [Agent Skills Standard](https://agentskills.io) — Padrão oficial de skills
- [ADR-007](./docs/adr/archive/ADR-007.md) — Decisão de criar skill agents-md-generator

---

*Gerado automaticamente por `agents-md-generator` em 2026-07-05*
*Última atualização: 2026-07-05*
