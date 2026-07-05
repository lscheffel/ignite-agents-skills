# AGENTS.md - Projeto CRM

## Visão Geral

Este projeto é um sistema de Customer Relationship Management (CRM) para gerenciamento de clientes, vendas, leads e interações. O sistema permite rastrear todo o ciclo de vida do cliente, desde a prospecção até o pós-venda.

## Estrutura do Projeto

```
src/
├── domain/                    # Regras de negócio
│   ├── entities/             # Entidades de domínio
│   ├── value-objects/        # Objetos de valor
│   └── services/             # Serviços de domínio
├── application/              # Casos de uso
│   ├── commands/             # Comandos CQRS
│   ├── queries/              # Queries CQRS
│   └── handlers/             # Handlers
├── infrastructure/           # Adaptadores externos
│   ├── persistence/          # Repositórios
│   ├── messaging/            # Filas e eventos
│   └── external/             # APIs externas
├── interfaces/               # Controllers e APIs
│   ├── rest/                 # REST API
│   ├── graphql/              # GraphQL
│   └── web/                  # Web UI
└── shared/                   # Código compartilhado
    ├── types/                # Tipos
    └── utils/                # Utilitários
```

### Descrição dos Diretórios

- **domain/**: Contém regras de negócio puras, sem dependências externas
- **application/**: Contém casos de uso que orquestram o domínio
- **infrastructure/**: Contém implementações técnicas
- **interfaces/**: Contém pontos de entrada da aplicação
- **shared/**: Código compartilhado entre módulos

## Padrões de Código

### Convenções

- Seguir Clean Architecture / Hexagonal Architecture
- Usar DDD (Domain-Driven Design) para modelagem
- Implementar CQRS para operações de leitura/escrita
- Usar Event Sourcing para auditoria

### Formatação

- TypeScript/JavaScript: ESLint + Prettier
- Python: Black + Flake8
- Java: Checkstyle + SpotBugs

### Naming

- Entidades: substantivos no singular (Cliente, Venda)
- Value Objects: substantivos no singular (Email, Telefone)
- Services: verbos no infinitivo (CriarCliente, ProcessarVenda)
- Repositories: substantivos no plural (ClientesRepository)

## Comandos Importantes

### Desenvolvimento

```bash
# Instalar dependências
npm install

# Iniciar desenvolvimento
npm run dev

# Rodar migrações
npm run migrate

# Seed banco de dados
npm run seed
```

### Build

```bash
# Build de produção
npm run build

# Build de desenvolvimento
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

# Testes E2E
npm run test:e2e

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
- **hotfix/***: Correções urgentes

### Processo de PR

1. Criar branch `feature/nome-da-feature` a partir de `develop`
2. Fazer commits pequenos e focados
3. Abrir PR com descrição completa
4. Pelo menos 2 aprovações necessárias
5. CI deve passar (lint, testes, build)
6. Merge com squash ou rebase

### Code Review

- Verificar arquitetura e padrões
- Testar cenários principais
- Verificar segurança (injeção, XSS, etc.)
- Revisar performance
- Documentar mudanças

### CI/CD

- GitHub Actions para CI
- Testes automatizados em cada PR
- Deploy automático para staging
- Deploy manual para produção
- Monitoramento pós-deploy

## Models de Dados

### Cliente

```typescript
interface Cliente {
  id: string;
  nome: string;
  email: string;
  telefone: string;
  empresa?: string;
  cargo?: string;
  tags: string[];
  criadoEm: Date;
  atualizadoEm: Date;
}
```

### Venda

```typescript
interface Venda {
  id: string;
  clienteId: string;
  valor: number;
  status: 'pendente' | 'aprovada' | 'cancelada';
  dataVenda: Date;
  itens: ItemVenda[];
  criadoEm: Date;
}
```

### Lead

```typescript
interface Lead {
  id: string;
  nome: string;
  email: string;
  empresa: string;
  fonte: string;
  status: 'novo' | 'contatado' | 'qualificado' | 'convertido' | 'perdido';
  criadoEm: Date;
}
```

## Skills Recomendadas

- `ddd` — para modelagem de domínio
- `data-modeling` — para modelagem de dados
- `api-design` — para design de APIs
- `security-review` — para revisão de segurança
- `testing` — para testes

## Anti-patterns

### 🔴 Crítico

#### Lógica de negócio em Controllers
**O que é:** Colocar regras de negócio em controllers ou handlers.
**Por que é ruim:** Dificulta teste e reuso.
**Como evitar:** Manter lógica em services de domínio.

#### Anêmico Domain Model
**O que é:** Entidades sem comportamento, apenas dados.
**Por que é ruim:** Não aproveita OO, lógica espalhada.
**Como evitar:** Colocar comportamento nas entidades.

### 🟡 Médio

#### N+1 Queries
**O que é:** Múltiplas queries para carregar dados relacionados.
**Por que é ruim:** Performance ruim.
**Como evitar:** Usar eager loading ou batch loading.

#### Falta de Validação
**O que é:** Não validar dados de entrada.
**Por que é ruim:** Dados inválidos no banco.
**Como evitar:** Validar em todas as camadas.

### 🟢 Baixo

#### Logs Excessivos
**O que é:** Logar tudo, incluindo dados sensíveis.
**Por que é ruim:** Performance e segurança.
**Como evitar:** Logar apenas o necessário, mascarar dados sensíveis.

## Edge Cases

### Concorrência
**Situação:** Dois usuários editam o mesmo registro.
**Solução:** Usar optimistic locking ou pessimistic locking.
**Exceção:** Para operações de leitura, não bloquear.

### Migração de Dados
**Situação:** Precisa migrar dados de schema antigo para novo.
**Solução:** Criar scripts de migração testados.
**Exceção:** Se migração é muito complexa, fazer em etapas.

### Integração com Sistemas Legados
**Situação:** Precisa integrar com sistema legado.
**Solução:** Usar anti-corruption layer.
**Exceção:** Se sistema legado é muito instável, usar fallback.

## Referências

- [Clean Architecture](https://blog.cleancoder.com/clean-architecture-book.html)
- [Domain-Driven Design](https://www.domainlanguage.com/ddd/)
- [CQRS](http://cqrs.files.wordpress.com/2010/11/cqrs_documents.pdf)
- [API Design](./skills/api-design/SKILL.md)
- [Data Modeling](./skills/data-modeling/SKILL.md)

---

*Gerado automaticamente por `agents-md-generator` em {{generation_date}}*
*Última atualização: {{last_update}}*
