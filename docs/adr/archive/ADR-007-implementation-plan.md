# Plano de Implementação: Skill agents-md-generator

## Visão Geral

Criar uma skill para geração e manutenção de `AGENTS.md` adaptativo que se adapta ao contexto do projeto sendo desenvolvido. A skill detecta automaticamente o tipo de projeto, tecnologias, padrões e governança, gerando um AGENTS.md personalizado que serve como "conciliador" entre o estado atual do projeto e as regras de governança para agentes de IA.

## Épicos

### Épico 1: Fundação da Skill
- [ ] Criar estrutura de diretórios da skill
- [ ] Definir frontmatter padrão
- [ ] Implementar detecção básica de contexto
- [ ] Criar template base do AGENTS.md

### Épico 2: Detecção de Contexto
- [ ] Implementar detecção de tipo de projeto (CRM, API, WebApp, etc.)
- [ ] Implementar detecção de tecnologias (linguagens, frameworks)
- [ ] Implementar detecção de padrões arquiteturais
- [ ] Implementar detecção de governança existente

### Épico 3: Geração de Templates
- [ ] Criar template para repositórios de skills
- [ ] Criar template para projetos CRM
- [ ] Criar template para projetos de API
- [ ] Criar template para webapps
- [ ] Criar template para bibliotecas
- [ ] Criar template para CLIs

### Épico 4: Geração do AGENTS.md
- [ ] Implementar lógica de seleção de template
- [ ] Implementar preenchimento automático de placeholders
- [ ] Implementar seção de visão geral adaptativa
- [ ] Implementar seção de estrutura do projeto
- [ ] Implementar seção de padrões de código
- [ ] Implementar seção de comandos importantes
- [ ] Implementar seção de governança
- [ ] Implementar seção de skills recomendadas
- [ ] Implementar seção de anti-patterns
- [ ] Implementar seção de edge cases

### Épico 5: Manutenção e Validação
- [ ] Implementar detecção de mudanças no projeto
- [ ] Implementar sugestões de atualização
- [ ] Implementar validação do AGENTS.md
- [ ] Criar checklists de validação
- [ ] Integrar com scripts existentes

### Épico 6: Documentação e Exemplos
- [ ] Criar documentação completa da skill
- [ ] Criar exemplos de antes e depois
- [ ] Criar exemplos de detecção de contexto
- [ ] Criar guia de uso

## Timeline

| Sprint | Épico | Features | Complexidade |
|--------|-------|----------|--------------|
| Sprint 1 | Épico 1 | Fundação da Skill | M |
| Sprint 2 | Épico 2 | Detecção de Contexto | L |
| Sprint 3 | Épico 3 | Geração de Templates | M |
| Sprint 4 | Épico 4 | Geração do AGENTS.md | L |
| Sprint 5 | Épico 5 | Manutenção e Validação | M |
| Sprint 6 | Épico 6 | Documentação e Exemplos | S |

## Tarefas Detalhadas

### Tarefa 1: Criar Estrutura de Diretórios

**Arquivos:** skills/agents-md-generator/{SKILL.md,templates/,examples/,checklists/}  
**Complexidade:** S  
**Dependências:** Nenhuma  
**Critérios de aceitação:**
- [ ] Diretório `skills/agents-md-generator/` criado
- [ ] Subdiretórios `templates/`, `examples/`, `checklists/` criados
- [ ] Arquivo `SKILL.md` criado com frontmatter válido

**Comandos de validação:**
```bash
ls -la skills/agents-md-generator/
bash scripts/validate-skill.sh skills/agents-md-generator
```

### Tarefa 2: Definir Frontmatter Padrão

**Arquivos:** skills/agents-md-generator/SKILL.md  
**Complexidade:** S  
**Dependências:** Tarefa 1  
**Critérios de aceitação:**
- [ ] Frontmatter inclui `name: agents-md-generator`
- [ ] Frontmatter inclui `description` adequada
- [ ] Frontmatter inclui `version: 1.0.0`
- [ ] Frontmatter inclui `tags` relevantes
- [ ] Frontmatter inclui `related_skills` apropriadas

**Comandos de validação:**
```bash
head -20 skills/agents-md-generator/SKILL.md
```

### Tarefa 3: Implementar Detecção Básica de Contexto

**Arquivos:** skills/agents-md-generator/SKILL.md  
**Complexidade:** M  
**Dependências:** Tarefa 2  
**Critérios de aceitação:**
- [ ] Documenta como detectar tipo de projeto
- [ ] Documenta como detectar tecnologias
- [ ] Documenta como detectar padrões arquiteturais
- [ ] Inclui exemplos de detecção

**Comandos de validação:**
```bash
grep -A 10 "Detecção" skills/agents-md-generator/SKILL.md
```

### Tarefa 4: Criar Template Base do AGENTS.md

**Arquivos:** skills/agents-md-generator/templates/AGENTS-base.md  
**Complexidade:** M  
**Dependências:** Tarefa 1  
**Critérios de aceitação:**
- [ ] Template inclui seção de visão geral
- [ ] Template inclui seção de estrutura
- [ ] Template inclui seção de padrões
- [ ] Template inclui seção de comandos
- [ ] Template inclui seção de governança
- [ ] Template usa placeholders `{{placeholder}}`

**Comandos de validação:**
```bash
cat skills/agents-md-generator/templates/AGENTS-base.md
```

### Tarefa 5: Criar Template para Repositórios de Skills

**Arquivos:** skills/agents-md-generator/templates/AGENTS-skills-repo.md  
**Complexidade:** M  
**Dependências:** Tarefa 4  
**Critérios de aceitação:**
- [ ] Template adaptado para repositórios de skills
- [ ] Inclui seção sobre padrões de skills
- [ ] Inclui seção sobre validação de skills
- [ ] Inclui seção sobre manutenção de skills

**Comandos de validação:**
```bash
cat skills/agents-md-generator/templates/AGENTS-skills-repo.md
```

### Tarefa 6: Criar Template para Projetos CRM

**Arquivos:** skills/agents-md-generator/templates/AGENTS-crm.md  
**Complexidade:** M  
**Dependências:** Tarefa 4  
**Critérios de aceitação:**
- [ ] Template adaptado para projetos CRM
- [ ] Inclui seção sobre modelagem de dados
- [ ] Inclui seção sobre processos de negócio
- [ ] Inclui seção sobre integrações

**Comandos de validação:**
```bash
cat skills/agents-md-generator/templates/AGENTS-crm.md
```

### Tarefa 7: Criar Template para Projetos de API

**Arquivos:** skills/agents-md-generator/templates/AGENTS-api.md  
**Complexidade:** M  
**Dependências:** Tarefa 4  
**Critérios de aceitação:**
- [ ] Template adaptado para projetos de API
- [ ] Inclui seção sobre endpoints
- [ ] Inclui seção sobre autenticação
- [ ] Inclui seção sobre versionamento

**Comandos de validação:**
```bash
cat skills/agents-md-generator/templates/AGENTS-api.md
```

### Tarefa 8: Criar Template para WebApps

**Arquivos:** skills/agents-md-generator/templates/AGENTS-webapp.md  
**Complexidade:** M  
**Dependências:** Tarefa 4  
**Critérios de aceitação:**
- [ ] Template adaptado para webapps
- [ ] Inclui seção sobre componentes
- [ ] Inclui seção sobre estado
- [ ] Inclui seção sobre rotas

**Comandos de validação:**
```bash
cat skills/agents-md-generator/templates/AGENTS-webapp.md
```

### Tarefa 9: Implementar Lógica de Seleção de Template

**Arquivos:** skills/agents-md-generator/SKILL.md  
**Complexidade:** L  
**Dependências:** Tarefas 5-8  
**Critérios de aceitação:**
- [ ] Documenta como selecionar template baseado no contexto
- [ ] Inclui fluxograma de decisão
- [ ] Inclui exemplos de seleção

**Comandos de validação:**
```bash
grep -A 20 "Seleção de Template" skills/agents-md-generator/SKILL.md
```

### Tarefa 10: Implementar Preenchimento Automático

**Arquivos:** skills/agents-md-generator/SKILL.md  
**Complexidade:** L  
**Dependências:** Tarefa 9  
**Critérios de aceitação:**
- [ ] Documenta como preencher placeholders automaticamente
- [ ] Inclui exemplos de preenchimento
- [ ] Documenta como override manual

**Comandos de validação:**
```bash
grep -A 20 "Preenchimento" skills/agents-md-generator/SKILL.md
```

### Tarefa 11: Implementar Seções do AGENTS.md

**Arquivos:** skills/agents-md-generator/SKILL.md  
**Complexidade:** L  
**Dependências:** Tarefa 10  
**Critérios de aceitação:**
- [ ] Documenta cada seção do AGENTS.md
- [ ] Inclui exemplos de cada seção
- [ ] Documenta como personalizar cada seção

**Comandos de validação:**
```bash
grep -A 5 "Seções" skills/agents-md-generator/SKILL.md
```

### Tarefa 12: Implementar Manutenção Automática

**Arquivos:** skills/agents-md-generator/SKILL.md  
**Complexidade:** M  
**Dependências:** Tarefa 11  
**Critérios de aceitação:**
- [ ] Documenta como detectar mudanças no projeto
- [ ] Documenta como sugerir atualizações
- [ ] Documenta como validar AGENTS.md

**Comandos de validação:**
```bash
grep -A 20 "Manutenção" skills/agents-md-generator/SKILL.md
```

### Tarefa 13: Criar Checklists de Validação

**Arquivos:** skills/agents-md-generator/checklists/validation.md  
**Complexidade:** S  
**Dependências:** Tarefa 12  
**Critérios de aceitação:**
- [ ] Checklist inclui validação de estrutura
- [ ] Checklist inclui validação de conteúdo
- [ ] Checklist inclui validação de format

**Comandos de validação:**
```bash
cat skills/agents-md-generator/checklists/validation.md
```

### Tarefa 14: Criar Exemplos de Antes e Depois

**Arquivos:** skills/agents-md-generator/examples/before-after.md  
**Complexidade:** S  
**Dependências:** Tarefa 13  
**Critérios de aceitação:**
- [ ] Exemplo mostra AGENTS.md antes da skill
- [ ] Exemplo mostra AGENTS.md depois da skill
- [ ] Exemplo inclui contexto de uso

**Comandos de validação:**
```bash
cat skills/agents-md-generator/examples/before-after.md
```

### Tarefa 15: Criar Exemplos de Detecção de Contexto

**Arquivos:** skills/agents-md-generator/examples/context-detection.md  
**Complexidade:** S  
**Dependências:** Tarefa 14  
**Critérios de aceitação:**
- [ ] Exemplo mostra detecção de tipo de projeto
- [ ] Exemplo mostra detecção de tecnologias
- [ ] Exemplo mostra detecção de padrões

**Comandos de validação:**
```bash
cat skills/agents-md-generator/examples/context-detection.md
```

### Tarefa 16: Criar Documentação Completa

**Arquivos:** skills/agents-md-generator/SKILL.md  
**Complexidade:** M  
**Dependências:** Tarefas 1-15  
**Critérios de aceitação:**
- [ ] SKILL.md tem ≥150 linhas
- [ ] SKILL.md inclui todas as seções obrigatórias
- [ ] SKILL.md é válido pelo `validate-skill.sh`

**Comandos de validação:**
```bash
wc -l skills/agents-md-generator/SKILL.md
bash scripts/validate-skill.sh skills/agents-md-generator
```

### Tarefa 17: Integrar com Scripts Existentes

**Arquivos:** scripts/sync-index.sh, scripts/validate-index.sh  
**Complexidade:** M  
**Dependências:** Tarefa 16  
**Critérios de aceitação:**
- [ ] Skill é detectada pelo `sync-index.sh`
- [ ] Skill é validada pelo `validate-index.sh`
- [ ] Skill aparece no `index.json`

**Comandos de validação:**
```bash
./scripts/sync-index.sh
./scripts/validate-index.sh
grep "agents-md-generator" skills/index.json
```

### Tarefa 18: Testar em Diferentes Contextos

**Arquivos:** N/A  
**Complexidade:** L  
**Dependências:** Tarefa 17  
**Critérios de aceitação:**
- [ ] Testado em repositório de skills
- [ ] Testado em projeto CRM
- [ ] Testado em projeto de API
- [ ] Testado em webapp
- [ ] Testado em biblioteca
- [ ] Testado em CLI

**Comandos de validação:**
```bash
# Testar em cada contexto
```

## Riscos

- **Detecção Incorreta**: O contexto pode ser mal interpretado
  - **Mitigação**: Permitir override manual do contexto detectado
- **Templates Desatualizados**: Templates podem ficar obsoletos
  - **Mitigação**: Processo de revisão e atualização periódica
- **Complexidade Excessiva**: A skill pode ficar complexa demais
  - **Mitigação**: Começar com templates básicos e evoluir
- **Integração com Scripts**: Pode haver problemas de integração
  - **Mitigação**: Testar integração cedo e frequentemente

## Critérios de Aceitação Gerais

- [ ] Skill passa na validação do `validate-skill.sh`
- [ ] Skill tem ≥150 linhas de conteúdo acionável
- [ ] Skill inclui ≥3 templates adaptativos
- [ ] Skill inclui ≥3 exemplos
- [ ] Skill inclui checklists de validação
- [ ] Skill é registrada no `index.json`
- [ ] Skill funciona em ≥3 tipos de projetos diferentes
- [ ] Skill documenta override manual do contexto
- [ ] Skill inclui fluxograma de decisão
- [ ] Skill inclui anti-patterns com severidade
