# AGENTS.md - Biblioteca

## Visão Geral

Este projeto é uma biblioteca reutilizável que pode ser consumida por outros projetos. A biblioteca fornece funcionalidades específicas que podem ser importadas e usadas em diferentes contextos.

## Estrutura do Projeto

```
src/
├── index.ts                   # Entry point principal
├── module1/                   # Módulo 1
│   ├── index.ts              # Export do módulo
│   ├── types.ts              # Tipos
│   └── utils.ts              # Utilitários
├── module2/                   # Módulo 2
│   ├── index.ts
│   ├── types.ts
│   └── utils.ts
└── shared/                    # Código compartilhado
    ├── types.ts              # Tipos globais
    └── utils.ts              # Utilitários globais
```

### Descrição dos Diretórios

- **src/**: Código fonte da biblioteca
- **module1/**, **module2/**: Módulos funcionais
- **shared/**: Código compartilhado entre módulos

## Padrões de Código

### Convenções

- Usar TypeScript para type safety
- Exportar apenas o necessário (barrel exports)
- Manter API pública estável
- Documentar todas as exports públicas

### Formatação

- ESLint + Prettier para formatação
- TypeDoc para documentação
- Semantic Versioning para releases

### Naming

- Funções: camelCase (formatDate)
- Classes: PascalCase (UserService)
- Types: PascalCase (UserProfile)
- Constants: UPPER_SNAKE_CASE (API_URL)

## Comandos Importantes

### Desenvolvimento

```bash
# Instalar dependências
npm install

# Iniciar desenvolvimento
npm run dev

# Watch mode
npm run watch
```

### Build

```bash
# Build para produção
npm run build

# Build para desenvolvimento
npm run build:dev

# Build de documentação
npm run build:docs
```

### Testes

```bash
# Todos os testes
npm test

# Testes unitários
npm run test:unit

# Testes de integração
npm run test:integration

# Coverage
npm run test:coverage
```

### Publicação

```bash
# Publicar no npm
npm publish

# Publicar pré-release
npm publish --tag next
```

## Governança

### Branching Strategy

- **main**: Código estável
- **develop**: Branch de integração
- **feature/***: Novas funcionalidades
- **fix/***: Correções de bugs

### Processo de PR

1. Criar branch a partir de `develop`
2. Fazer commits pequenos e focados
3. Abrir PR com descrição completa
4. Pelo menos 1 aprovação necessária
5. CI deve passar
6. Merge com squash

### Code Review

- Verificar API pública
- Testar backward compatibility
- Verificar documentação
- Revisar performance

### CI/CD

- GitHub Actions para CI
- Testes em cada PR
- Build automático
- Publicação manual

## API Pública

### Exports

```typescript
// Funções
export function formatDate(date: Date): string;
export function calculateTotal(items: Item[]): number;

// Classes
export class UserService {
  constructor(config: Config);
  getUser(id: string): Promise<User>;
}

// Types
export interface User {
  id: string;
  name: string;
  email: string;
}

export type Config = {
  apiUrl: string;
  timeout: number;
};
```

### Uso

```typescript
// Importação named
import { formatDate, calculateTotal } from 'minha-biblioteca';

// Importação de classe
import { UserService } from 'minha-biblioteca';

// Importação de tipo
import type { User, Config } from 'minha-biblioteca';
```

## Versionamento

### Semantic Versioning

- **MAJOR**: Mudanças incompatíveis
- **MINOR**: Novas funcionalidades (backward compatible)
- **PATCH**: Correções (backward compatible)

### Changelog

- Manter CHANGELOG.md atualizado
- Documentar mudanças breaking changes
- Usar formato Keep a Changelog

## Skills Recomendadas

- `testing` — para testes
- `documentation` — para documentação
- `release` — para versionamento
- `refactoring` — para refatoração

## Anti-patterns

### 🔴 Crítico

#### API Pública Instável
**O que é:** Mudanças frequentes na API pública.
**Por que é ruim:** Quebra consumers da biblioteca.
**Como evitar:** Usar versionamento semântico, deprecation notices.

#### Dependências Excessivas
**O que é:** Muitas dependências externas.
**Por que é ruim:** Bundle size, vulnerabilidades.
**Como evitar:** Minimizar dependências, usar tree shaking.

### 🟡 Médio

#### Não Usar TypeScript
**O que é:** Biblioteca sem tipos.
**Por que é ruim:** Dificulta uso em projetos TypeScript.
**Como evitar:** Sempre usar TypeScript.

#### Bundle Grande
**O que é:** Bundle com código não utilizado.
**Por que é ruim:** Performance, tamanho.
**Como evitar:** Code splitting, tree shaking.

### 🟢 Baixo

#### Documentação Desatualizada
**O que é:** README não reflete API atual.
**Por que é ruim:** Dificulta adoção.
**Como evitar:** Atualizar docs a cada mudança.

## Edge Cases

### Breaking Changes
**Situação:** Precisa fazer mudança que quebra API.
**Solução:** Versionar como MAJOR, documentar migração.
**Exceção:** Se mudança é pequena, usar deprecation.

### Dependências Conflitantes
**Situação:** Consumer tem versão diferente de dependência.
**Solução:** Usar peer dependencies.
**Exceção:** Se dependência é opcional.

### Tree Shaking
**Situação:** Consumer não consegue fazer tree shaking.
**Solução:** Usar exports separados por módulo.
**Exceção:** Se biblioteca é pequena.

## Referências

- [Semantic Versioning](https://semver.org/)
- [TypeScript](https://www.typescriptlang.org/)
- [npm publish](https://docs.npmjs.com/cli/v8/commands/npm-publish)
- [Tree Shaking](https://developer.mozilla.org/en-US/docs/Glossary/Tree_shaking)

---

*Gerado automaticamente por `agents-md-generator` em {{generation_date}}*
*Última atualização: {{last_update}}*
