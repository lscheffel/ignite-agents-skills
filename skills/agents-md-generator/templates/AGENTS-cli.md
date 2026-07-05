# AGENTS.md - CLI

## Visão Geral

Este projeto é uma ferramenta de linha de comando (CLI) que fornece utilitários para automatizar tarefas, gerenciar configurações e interagir com sistemas. A CLI pode ser usada por desenvolvedores e operadores para executar comandos específicos.

## Estrutura do Projeto

```
src/
├── commands/                  # Comandos da CLI
│   ├── command1.ts           # Comando 1
│   ├── command2.ts           # Comando 2
│   └── index.ts              # Registro de comandos
├── utils/                     # Utilitários
│   ├── logger.ts             # Logging
│   ├── config.ts             # Configurações
│   └── helpers.ts            # Funções auxiliares
├── types/                     # Tipos
└── index.ts                   # Entry point
```

### Descrição dos Diretórios

- **commands/**: Implementação dos comandos
- **utils/**: Utilitários compartilhados
- **types/**: Definições de tipos
- **index.ts**: Entry point da CLI

## Padrões de Código

### Convenções

- Usar Commander.js ou Yargs para parsing de argumentos
- Implementar help para cada comando
- Usar exit codes apropriados
- Logar erros adequadamente

### Formatação

- TypeScript para type safety
- ESLint + Prettier para formatação
- Chalk para cores no terminal
- Inquirer.js para input interativo

### Naming

- Comandos: kebab-case (create-user)
- Opções: kebab-case (--output-dir)
- Flags: camelCase (--dryRun)

## Comandos Importantes

### Desenvolvimento

```bash
# Instalar dependências
npm install

# Iniciar desenvolvimento
npm run dev

# Link local
npm link
```

### Build

```bash
# Build para produção
npm run build

# Build binário
npm run build:bin
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
```

### Distribuição

```bash
# Publicar no npm
npm publish

# Build para múltiplas plataformas
npm run build:all
```

## Comandos da CLI

### Comando: create

```bash
mycli create <project-name> [options]

Opções:
  --template <template>    Template a usar (default: "default")
  --output-dir <dir>       Diretório de saída (default: ".")
  --dry-run                Simular sem criar arquivos

Exemplo:
  mycli create my-project --template react
```

### Comando: generate

```bash
mycli generate <type> <name> [options]

Opções:
  --template <template>    Template específico
  --output-dir <dir>       Diretório de saída

Exemplo:
  mycli generate component UserProfile
```

### Comando: validate

```bash
mycli validate [options]

Opções:
  --fix                    Corrigir problemas automaticamente
  --report <format>        Formato do relatório (json, text)

Exemplo:
  mycli validate --fix
```

### Comando: config

```bash
mycli config <action> [options]

Ações:
  get <key>                Obter configuração
  set <key> <value>        Definir configuração
  list                     Listar todas as configurações
  reset                    Resetar configurações

Exemplo:
  mycli config set apiUrl https://api.example.com
```

## Governança

### Branching Strategy

- **main**: Código estável
- **develop**: Branch de integração
- **feature/***: Novos comandos
- **fix/***: Correções

### Processo de PR

1. Criar branch a partir de `develop`
2. Fazer commits pequenos e focados
3. Abrir PR com descrição completa
4. Pelo menos 1 aprovação necessária
5. CI deve passar
6. Merge com squash

### Code Review

- Verificar usabilidade da CLI
- Testar comandos
- Verificar help e documentação
- Revisar error handling

### CI/CD

- GitHub Actions para CI
- Testes em cada PR
- Build automático
- Publicação manual

## Configuração

### Arquivo de Configuração

```json
{
  "apiUrl": "https://api.example.com",
  "outputDir": "./output",
  "verbose": false,
  "template": "default"
}
```

### Variáveis de Ambiente

```bash
MYCLI_API_URL=https://api.example.com
MYCLI_OUTPUT_DIR=./output
MYCLI_VERBOSE=true
```

## Skills Recomendadas

- `testing` — para testes
- `documentation` — para documentação
- `release` — para versionamento

## Anti-patterns

### 🔴 Crítico

#### Sem Help
**O que é:** Comandos sem documentação de uso.
**Por que é ruim:** Usuários não sabem como usar.
**Como evitar:** Sempre implementar --help para cada comando.

#### Sem Error Handling
**O que é:** Erros não tratados adequadamente.
**Por que é ruim:** CLI crashes sem mensagem clara.
**Como evitar:** Tratar erros e mostrar mensagens úteis.

### 🟡 Médio

#### Sem Exit Codes
**O que é:** Sempre retornar 0.
**Por que é ruim:** Scripts não conseguem detectar falhas.
**Como evitar:** Usar exit codes apropriados.

#### Sem Validação
**O que é:** Não validar argumentos.
**Por que é ruim:** Erros confusos.
**Como evitar:** Validar argumentos antes de executar.

### 🟢 Baixo

#### Sem Colorno
**O que é:** Saída apenas em texto simples.
**Por que é ruim:** Difícil de ler.
**Como evitar:** Usar cores para diferentes níveis.

## Edge Cases

### Permissões
**Situação:** CLI precisa de permissões elevadas.
**Solução:** Documentar requisitos, usar sudo quando necessário.
**Exceção:** Se possível, evitar permissões elevadas.

### Plataformas
**Situação:** CLI deve rodar em múltiplas plataformas.
**Solução:** Testar em Linux, macOS, Windows.
**Exceção:** Se app é específico, documentar plataforma suportada.

### Argparse
**Situação:** Argumentos conflitantes.
**Solução:** Definir prioridade, documentar comportamento.
**Exceção:** Se conflito é crítico, rejeitar.

## Referências

- [Commander.js](https://github.com/tj/commander.js/)
- [Yargs](https://yargs.js.org/)
- [Chalk](https://github.com/chalk/chalk)
- [Inquirer.js](https://github.com/SBoudrias/Inquirer.js/)

---

*Gerado automaticamente por `agents-md-generator` em {{generation_date}}*
*Última atualização: {{last_update}}*
