# Exemplos: Antes e Depois

## Visão Geral

Este documento mostra exemplos de como a skill `agents-md-generator` transforma a documentação de projetos.

---

## Exemplo 1: Projeto CRM

### Antes (Sem AGENTS.md)

```
meu-crm/
├── src/
│   ├── models/
│   ├── routes/
│   └── controllers/
├── package.json
└── README.md
```

**Problemas:**
- Agentes de IA não sabem a estrutura do projeto
- Não há padrões documentados
- Comandos importantes não são conhecidos
- Governança não está definida

### Depois (Com AGENTS.md)

**AGENTS.md gerado:**

```markdown
# AGENTS.md - Sistema CRM

## Visão Geral
Sistema de Customer Relationship Management para gerenciamento de clientes, vendas e leads.

## Estrutura do Projeto
src/
├── models/        # Modelos de dados
├── routes/        # Rotas da API
└── controllers/   # Controllers

## Comandos Importantes
npm run dev        # Iniciar desenvolvimento
npm test           # Rodar testes
npm run build      # Build de produção

## Governança
- Branching: GitFlow
- PR: Pelo menos 1 aprovação
- CI: Testes automáticos

## Skills Recomendadas
- `ddd` — para modelagem de domínio
- `api-design` — para design de APIs
```

**Benefícios:**
- Agentes entendem a estrutura
- Padrões são claros
- Comandos são conhecidos
- Governança está definida

---

## Exemplo 2: Projeto de API

### Antes (Com AGENTS.md Genérico)

```markdown
# AGENTS.md

## Visão Geral
Este projeto usa Node.js com Express.

## Estrutura
src/
├── routes/
├── models/
└── utils/

## Comandos
npm run dev
npm test
```

**Problemas:**
- Muito genérico
- Não descreve endpoints
- Não documenta autenticação
- Não lista padrões específicos

### Depois (Com AGENTS.md Adaptativo)

```markdown
# AGENTS.md - API RESTful

## Visão Geral
API RESTful para sistema de e-commerce com autenticação JWT.

## Endpoints Principais
POST /auth/login          # Login
GET    /users             # Listar usuários
POST   /users             # Criar usuário
GET    /products          # Listar produtos
POST   /orders            # Criar pedido

## Autenticação
- JWT tokens com expiração de 15 minutos
- Refresh tokens válidos por 7 dias
- Roles: admin, user, readonly

## Padrões
- Versionamento: /api/v1/
- Paginação: ?page=1&limit=20
- Erros: { error: { code, message } }
```

**Benefícios:**
- Documentação específica da API
- Endpoints claros
- Autenticação documentada
- Padrões definidos

---

## Exemplo 3: Biblioteca

### Antes (Sem Documentação)

```
minha-lib/
├── src/
│   ├── index.ts
│   ├── utils.ts
│   └── types.ts
├── package.json
└── README.md
```

**Problemas:**
- Não há documentação de API pública
- Não há exemplos de uso
- Não há guia de contribuição

### Depois (Com AGENTS.md)

```markdown
# AGENTS.md - Biblioteca

## Visão Geral
Biblioteca TypeScript para formatação e validação de dados.

## API Pública

### Funções Exportadas
formatDate(date: Date, format: string): string
validateEmail(email: string): boolean
calculateTotal(items: Item[]): number

### Uso
import { formatDate, validateEmail } from 'minha-lib';

const formatted = formatDate(new Date(), 'DD/MM/YYYY');
const isValid = validateEmail('user@example.com');

## Desenvolvimento
npm run dev          # Watch mode
npm test             # Rodar testes
npm run build        # Build
npm publish          # Publicar
```

**Benefícios:**
- API pública documentada
- Exemplos de uso claros
- Comandos de desenvolvimento listados

---

## Exemplo 4: CLI

### Antes (Sem Help)

```bash
$ mycli create
Usage: mycli create [options] <name>

Opções:
  --template <template>  Template a usar
  --output-dir <dir>     Diretório de saída
```

**Problemas:**
- Help básico
- Sem exemplos de uso
- Sem documentação de configuração

### Depois (Com AGENTS.md)

```markdown
# AGENTS.md - CLI

## Visão Geral
CLI para geração de projetos e componentes.

## Comandos

### create
mycli create <project-name> --template react

Opções:
  --template <template>    Template: react, vue, angular
  --output-dir <dir>       Diretório de saída (default: ".")
  --dry-run                Simular sem criar

### generate
mycli generate component UserProfile

### validate
mycli validate --fix

## Configuração
Arquivo: ~/.myclirc
{
  "defaultTemplate": "react",
  "outputDir": "./projects"
}
```

**Benefícios:**
- Help completo
- Exemplos práticos
- Configuração documentada

---

## Comparação de Métricas

| Métrica | Antes | Depois | Melhoria |
|---------|-------|--------|----------|
| Linhas de documentação | 10-20 | 50-100 | 300-500% |
| Seções obrigatórias | 0-2 | 8-10 | 400-500% |
| Comandos documentados | 1-2 | 5-10 | 300-500% |
| Padrões definidos | 0 | 3-5 | ∞ |
| Skills recomendadas | 0 | 3-5 | ∞ |

---

## Conclusão

A skill `agents-md-generator` transforma documentação genérica em guias adaptativos e completos, melhorando significativamente a experiência de agentes de IA ao interagir com projetos.
