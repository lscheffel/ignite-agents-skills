# AGENTS.md - Projeto de API

## Visão Geral

Este projeto é uma API RESTful/GraphQL para fornecer serviços backend. A API expõe endpoints para operações CRUD, autenticação, autorização e integrações com outros sistemas.

## Estrutura do Projeto

```
src/
├── routes/                    # Rotas da API
│   ├── v1/                   # Versão 1 da API
│   └── v2/                   # Versão 2 da API
├── controllers/               # Controllers
├── services/                  # Lógica de negócio
├── repositories/              # Acesso a dados
├── models/                    # Modelos de dados
├── middleware/                 # Middleware
├── utils/                     # Utilitários
├── config/                    # Configurações
└── types/                     # Tipos TypeScript
```

### Descrição dos Diretórios

- **routes/**: Definição de rotas da API
- **controllers/**: Handlers das requisições
- **services/**: Lógica de negócio
- **repositories/**: Acesso a banco de dados
- **models/**: Modelos de dados
- **middleware/**: Middleware (auth, validation, etc.)
- **utils/**: Funções utilitárias
- **config/**: Configurações da aplicação
- **types/**: Definições de tipos

## Padrões de Código

### Convenções

- Seguir padrões REST para endpoints
- Usar HTTP methods corretos (GET, POST, PUT, PATCH, DELETE)
- Retornar status codes apropriados
- Usar versionamento de API

### Formatação

- JSON para request/response
- CamelCase para propriedades
- snake_case para banco de dados
- UTF-8 para encoding

### Naming

- Endpoints em plural (/users, /orders)
- Nomes descritivos e auto-explicativos
- Verbos para ações especiais (/users/search)

## Comandos Importantes

### Desenvolvimento

```bash
# Instalar dependências
npm install

# Iniciar desenvolvimento
npm run dev

# Database migrations
npm run migrate

# Seed dados
npm run seed
```

### Build

```bash
# Build para produção
npm run build

# Build para desenvolvimento
npm run build:dev
```

### Testes

```bash
# Todos os testes
npm test

# Testes unitários
npm run test:unit

# Testes de integração
npm run test:integration

# Testes de contrato
npm run test:contract

# Coverage
npm run test:coverage
```

### Deploy

```bash
# Deploy para staging
npm run deploy:staging

# Deploy para produção
npm run deploy:production
```

## Governança

### Branching Strategy

- **main**: Código em produção
- **develop**: Branch de integração
- **feature/***: Novas funcionalidades
- **fix/***: Correções de bugs
- **release/***: Preparação de release

### Processo de PR

1. Criar branch a partir de `develop`
2. Fazer commits pequenos e focados
3. Abrir PR com descrição completa
4. Pelo menos 1 aprovação necessária
5. CI deve passar
6. Merge com squash

### Code Review

- Verificar contratos de API
- Testar endpoints
- Verificar segurança
- Revisar documentação
- Verificar performance

### CI/CD

- GitHub Actions para CI
- Testes em cada PR
- Deploy automático para staging
- Deploy manual para produção
- Health checks automáticos

## Endpoints

### Autenticação

```
POST /auth/login          # Login
POST /auth/register       # Registro
POST /auth/refresh        # Refresh token
POST /auth/logout         # Logout
```

### Usuários

```
GET    /users             # Listar usuários
GET    /users/:id         # Obter usuário
POST   /users             # Criar usuário
PUT    /users/:id         # Atualizar usuário
DELETE /users/:id         # Deletar usuário
```

### Pedidos

```
GET    /orders            # Listar pedidos
GET    /orders/:id        # Obter pedido
POST   /orders            # Criar pedido
PATCH  /orders/:id/status # Atualizar status
```

## Autenticação e Autorização

### JWT Tokens

- Access token: 15 minutos
- Refresh token: 7 dias
- Tokens são invalidados no logout

### Roles

- `admin`: Acesso total
- `user`: Acesso padrão
- `readonly`: Apenas leitura

### Permissões

```typescript
const permissions = {
  admin: ['*'],
  user: ['read', 'write', 'delete:own'],
  readonly: ['read']
};
```

## Skills Recomendadas

- `api-design` — para design de APIs
- `security-review` — para revisão de segurança
- `testing` — para testes
- `observability` — para monitoramento

## Anti-patterns

### 🔴 Crítico

#### Sem Validação de Input
**O que é:** Não validar dados de entrada.
**Por que é ruim:** Dados inválidos, vulnerabilidades.
**Como evitar:** Validar todos os inputs com schemas.

#### Sem Rate Limiting
**O que é:** Não limitar requisições por cliente.
**Por que é ruim:** Abuso, DDoS.
**Como evitar:** Implementar rate limiting.

### 🟡 Médio

#### Status Codes Errados
**O que é:** Retornar 200 para erros.
**Por que é ruim:** Clientes não conseguem tratar erros.
**Como evitar:** Usar status codes HTTP corretos.

#### Sem Paginação
**O que é:** Retornar todos os registros de uma vez.
**Por que é ruim:** Performance, memória.
**Como evitar:** Implementar paginação.

### 🟢 Baixo

#### Logs Excessivos
**O que é:** Logar dados sensíveis.
**Por que é ruim:** Segurança, performance.
**Como evitar:** Logar apenas o necessário.

## Edge Cases

### Timeout de Requisições
**Situação:** Requisição demora mais que o esperado.
**Solução:** Implementar timeout e retry.
**Exceção:** Para operações longas, usar jobs assíncronos.

### Concorrência
**Situação:** Múltiplas requisições alteram o mesmo recurso.
**Solução:** Usar optimistic locking.
**Exceção:** Para operações de leitura, não bloquear.

### Integração com APIs Externas
**Situação:** API externa está fora do ar.
**Solução:** Implementar circuit breaker.
**Exceção:** Se API é crítica, ter fallback.

## Referências

- [REST API Design](https://restfulapi.net/)
- [JSON Web Tokens](https://jwt.io/)
- [HTTP Status Codes](https://httpstatuses.com/)
- [API Design](./skills/api-design/SKILL.md)
- [Security Review](./skills/security-review/SKILL.md)

---

*Gerado automaticamente por `agents-md-generator` em {{generation_date}}*
*Última atualização: {{last_update}}*
