# Exemplos: Personalização

## Visão Geral

Este documento mostra como personalizar o AGENTS.md gerado para atender necessidades específicas do projeto.

---

## Exemplo 1: Override Manual de Contexto

### Situação

A detecção automática identificou o projeto como "API", mas na verdade é um "CRM com API".

### Comando

```bash
# Override manual do contexto
agents-md-generator --context crm --project-name "Sistema CRM"
```

### Resultado

O template `AGENTS-crm.md` é selecionado em vez de `AGENTS-api.md`.

---

## Exemplo 2: Adicionar Seção Personalizada

### Situação

Precisa adicionar uma seção específica de "Integrações" ao AGENTS.md.

### Processo

1. **Gerar AGENTS.md básico:**
   ```bash
   agents-md-generator --project-name "Meu Projeto"
   ```

2. **Adicionar seção personalizada:**
   ```markdown
   ## Integrações

   ### Sistema de Pagamento
   - Gateway: Stripe
   - Webhooks: /webhooks/payments
   - Events: payment.success, payment.failed

   ### Sistema de Email
   - Provider: SendGrid
   - Templates: /templates/email
   - Events: email.sent, email.failed
   ```

3. **Validar:**
   ```bash
   agents-md-generator --validate
   ```

---

## Exemplo 3: Override de Placeholders

### Situação

O placeholder `{{project_description}}` foi preenchido automaticamente, mas precisa de uma descrição mais detalhada.

### Processo

1. **Verificar AGENTS.md gerado:**
   ```markdown
   ## Visão Geral
   {{project_description}}
   ```

2. **Override manual:**
   ```markdown
   ## Visão Geral
   Sistema CRM completo para gerenciamento de clientes, vendas, leads e pipeline de vendas.
   Inclui integração com Stripe para pagamentos e SendGrid para emails transacionais.
   ```

3. **Validar:**
   ```bash
   agents-md-generator --validate
   ```

---

## Exemplo 4: Template Personalizado

### Situação

Nenhum template existente atende ao projeto específico (ex: jogo 2D).

### Processo

1. **Criar template personalizado:**
   ```bash
   mkdir -p skills/agents-md-generator/templates
   cp skills/agents-md-generator/templates/AGENTS-base.md \
      skills/agents-md-generator/templates/AGENTS-game-2d.md
   ```

2. **Editar template:**
   ```markdown
   # AGENTS.md - Jogo 2D

   ## Visão Geral
   {{project_description}}

   ## Engine
   - Engine: {{game_engine}}
   - Linguagem: {{language}}

   ## Asset Pipeline
   - Sprites: /assets/sprites/
   - Audio: /assets/audio/
   - Levels: /assets/levels/

   ## Comandos
   npm run dev          # Iniciar desenvolvimento
   npm run build        # Build para produção
   npm run test         # Rodar testes
   ```

3. **Usar template:**
   ```bash
   agents-md-generator --template game-2d --project-name "Meu Jogo"
   ```

---

## Exemplo 5: Múltiplos Projetos

### Situação

Monorepo com múltiplos projetos (API + WebApp + Biblioteca).

### Processo

1. **Gerar AGENTS.md para cada projeto:**
   ```bash
   # Para API
   cd packages/api
   agents-md-generator --context api --project-name "API"

   # Para WebApp
   cd packages/webapp
   agents-md-generator --context webapp --project-name "WebApp"

   # Para Biblioteca
   cd packages/shared
   agents-md-generator --context library --project-name "Shared Lib"
   ```

2. **Criar AGENTS.md raiz:**
   ```markdown
   # AGENTS.md - Monorepo

   ## Visão Geral
   Monorepo com API, WebApp e Biblioteca compartilhada.

   ## Estrutura
   packages/
   ├── api/        # API RESTful
   ├── webapp/     # WebApp React
   └── shared/     # Biblioteca compartilhada

   ## Comandos
   npm run dev          # Iniciar todos os projetos
   npm run build        # Build de todos os projetos
   npm run test         # Testes de todos os projetos
   ```

---

## Exemplo 6: Validação de Personalização

### Situação

Após personalizar o AGENTS.md, precisa validar se está correto.

### Comando

```bash
agents-md-generator --validate
```

### Resultado

```
✅ Validação do AGENTS.md

Estrutura:
  ✅ Arquivo existe
  ✅ Tem 85 linhas (≥30)
  ✅ Encoding UTF-8

Seções obrigatórias:
  ✅ Visão Geral
  ✅ Estrutura do Projeto
  ✅ Padrões de Código
  ✅ Comandos Importantes
  ✅ Governança
  ✅ Skills Recomendadas
  ✅ Anti-patterns
  ✅ Edge Cases

Placeholders:
  ✅ Nenhum placeholder não preenchido

Conteúdo:
  ✅ Descrição coerente
  ✅ Comandos relevantes
  ✅ Padrões definidos

Status: ✅ APROVADO
```

---

## Exemplo 7: Atualização Automática

### Situação

O projeto mudou (nova feature, mudança de tecnologia), e o AGENTS.md precisa ser atualizado.

### Processo

1. **Detectar mudanças:**
   ```bash
   agents-md-generator --detect-changes
   ```

2. **Resultado:**
   ```
   🔍 Mudanças detectadas:

   - Novo diretório: src/integrations/
   - Nova dependência: stripe
   - Comando novo: npm run deploy:prod

   Deseja atualizar o AGENTS.md? (s/n)
   ```

3. **Confirmar atualização:**
   ```bash
   s
   ```

4. **AGENTS.md atualizado:**
   ```markdown
   ## Integrações

   ### Stripe
   - SDK: stripe
   - Webhooks: /webhooks/stripe
   - Events: payment.success, payment.failed

   ## Comandos

   ### Deploy
   npm run deploy:staging    # Deploy para staging
   npm run deploy:prod      # Deploy para produção
   ```

---

## Comandos de Personalização

### Override de Contexto

```bash
agents-md-generator --context <tipo>
# Tipos: api, webapp, crm, library, cli, skills-repo, base
```

### Override de Template

```bash
agents-md-generator --template <nome>
# Nome do template em templates/
```

### Override de Placeholders

```bash
agents-md-generator --set "project_description=Minha descrição personalizada"
```

### Validação

```bash
agents-md-generator --validate
```

### Detecção de Mudanças

```bash
agents-md-generator --detect-changes
```

### Atualização

```bash
agents-md-generator --update
```

---

## Melhores Práticas

### 1. Override com Cuidado

- Use override apenas quando a detecção automática falha
- Documente o motivo do override no AGENTS.md
- Valide após o override

### 2. Templates Personalizados

- Crie templates para contextos específicos do seu projeto
- Mantenha templates genéricos para uso geral
- Documente templates personalizados

### 3. Atualização Regular

- Atualize o AGENTS.md a cada mudança significativa
- Use detecção automática para identificar mudanças
- Valide após cada atualização

### 4. Validação Contínua

- Execute validação antes de commitar
- Use CI/CD para validar AGENTS.md
- Monitore qualidade da documentação

---

## Conclusão

A personalização permite adaptar o AGENTS.md a necessidades específicas, mantendo os benefícios da geração automática. Use override com sabedoria e valide sempre após personalizações.
