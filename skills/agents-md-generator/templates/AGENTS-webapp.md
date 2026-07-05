# AGENTS.md - WebApp

## Visão Geral

Este projeto é uma aplicação web front-end construída com React/Vue/Angular. A aplicação fornece interface de usuário para interação com APIs backend, gerenciamento de estado, e experiência de usuário rica.

## Estrutura do Projeto

```
src/
├── components/                # Componentes reutilizáveis
│   ├── atoms/                # Componentes atômicos
│   ├── molecules/            # Componentes compostos
│   ├── organisms/            # Componentes complexos
│   └── templates/            # Templates de página
├── pages/                     # Páginas/Rotas
├── hooks/                     # Custom hooks
├── services/                  # Serviços (API calls)
├── store/                     # Gerenciamento de estado
├── utils/                     # Utilitários
├── types/                     # Tipos TypeScript
├── styles/                    # Estilos globais
└── assets/                    # Assets estáticos
```

### Descrição dos Diretórios

- **components/**: Componentes React organizados por atomic design
- **pages/**: Componentes de página (rotas)
- **hooks/**: Custom hooks para lógica reativa
- **services/**: Chamadas à API e lógica de negócio
- **store/**: Estado global da aplicação
- **utils/**: Funções utilitárias
- **types/**: Definições de tipos
- **styles/**: Estilos globais e variáveis
- **assets/**: Imagens, fontes, etc.

## Padrões de Código

### Convenções

- Usar Atomic Design para componentes
- Separar presentação de lógica
- Usar hooks para lógica reativa
- Manter componentes pequenos e focados

### Formatação

- TypeScript para type safety
- ESLint + Prettier para formatação
- CSS Modules ou Styled Components
- CamelCase para variáveis, PascalCase para componentes

### Naming

- Componentes: PascalCase (UserProfile)
- Hooks: camelCase com prefixo use (useAuth)
- Services: camelCase (apiService)
- Utils: camelCase (formatDate)

## Comandos Importantes

### Desenvolvimento

```bash
# Instalar dependências
npm install

# Iniciar desenvolvimento
npm run dev

# Acessar em
http://localhost:3000
```

### Build

```bash
# Build de produção
npm run build

# Build de análise
npm run build:analyze
```

### Testes

```bash
# Todos os testes
npm test

# Testes unitários
npm run test:unit

# Testes de componente
npm run test:component

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

### Processo de PR

1. Criar branch a partir de `develop`
2. Fazer commits pequenos e focados
3. Abrir PR com descrição completa
4. Pelo menos 1 aprovação necessária
5. CI deve passar (lint, testes, build)
6. Merge com squash

### Code Review

- Verificar acessibilidade
- Testar em diferentes telas
- Verificar performance
- Revisar UX
- Documentar mudanças

### CI/CD

- GitHub Actions para CI
- Lint automático
- Testes em cada PR
- Deploy automático para staging
- Deploy manual para produção

## Componentes

### Atomic Design

#### Atoms
- Button, Input, Label, Icon
- Componentes básicos, sem dependências

#### Molecules
- SearchBar (Input + Button)
- FormField (Label + Input + Error)
- Componentes compostos de atoms

#### Organisms
- Header (Logo + Nav + UserMenu)
- ProductCard (Image + Title + Price + Button)
- Componentes complexos

#### Templates
- PageLayout (Header + Content + Footer)
- DashboardLayout (Sidebar + Content)
- Templates de página

### State Management

```typescript
// Redux/Zustand store
interface AppState {
  user: UserState;
  cart: CartState;
  ui: UIState;
}

// Actions
type AppAction =
  | { type: 'SET_USER'; payload: User }
  | { type: 'ADD_TO_CART'; payload: Product }
  | { type: 'TOGGLE_SIDEBAR' };
```

### Rotas

```typescript
const routes = [
  { path: '/', component: HomePage },
  { path: '/login', component: LoginPage },
  { path: '/dashboard', component: DashboardPage, protected: true },
  { path: '/products', component: ProductsPage },
  { path: '/products/:id', component: ProductDetailPage },
];
```

## Skills Recomendadas

- `testing` — para testes
- `documentation` — para documentação
- `refactoring` — para refatoração

## Anti-patterns

### 🔴 Crítico

#### Componentes Gigantes
**O que é:** Componentes com muita responsabilidade.
**Por que é ruim:** Dificulta manutenção e teste.
**Como evitar:** Separar em componentes menores.

#### Estado Global Excessivo
**O que é:** Tudo no estado global.
**Por que é ruim:** Performance, complexidade.
**Como evitar:** Usar estado local quando possível.

### 🟡 Médio

#### Props Drilling
**O que é:** Passar props através de muitos componentes.
**Por que é ruim:** Acoplamento,难 de refactor.
**Como evitar:** Usar Context ou state management.

#### Não Usar Memoização
**O que é:** Não memoizar componentes custosos.
**Por que é ruim:** Performance ruim.
**Como evitar:** Usar React.memo, useMemo, useCallback.

### 🟢 Baixo

#### CSS Globals
**O que é:** Estilos globais conflitantes.
**Por que é ruim:** Conflitos de estilos.
**Como evitar:** Usar CSS Modules ou Scoped Styles.

## Edge Cases

### Responsividade
**Situação:** Layout quebra em telas pequenas.
**Solução:** Usar mobile-first design.
**Exceção:** Se app é desktop-only, documentar.

### Acessibilidade
**Situação:** Componentes não acessíveis.
**Solução:** Seguir WCAG 2.1.
**Exceção:** Se app é interno, pode ter requisitos menores.

### Performance
**Situação:** App lenta com muitos dados.
**Solução:** Virtualização, lazy loading.
**Exceção:** Se dados são sempre pequenos.

## Referências

- [React Documentation](https://reactjs.org/)
- [Atomic Design](https://atomicdesign.bradfrost.com/)
- [Testing Library](https://testing-library.com/)
- [Web Accessibility](https://www.w3.org/WAI/)

---

*Gerado automaticamente por `agents-md-generator` em {{generation_date}}*
*Última atualização: {{last_update}}*
