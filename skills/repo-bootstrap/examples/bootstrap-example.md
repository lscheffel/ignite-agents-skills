# Exemplo: Repo Bootstrap

## Estrutura Criada
```
my-service/
├── README.md
├── AGENTS.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
├── LICENSE
├── .github/
│   └── workflows/
│       └── ci.yml
├── docs/
│   ├── architecture/
│   └── adr/
└── src/
    ├── domain/
    ├── application/
    └── infrastructure/
```

## Comandos
```bash
# Criar estrutura
mkdir -p docs/{adr,api,architecture}
mkdir -p .github/workflows

# Copiar templates
cp templates/*.md .
cp templates/ci.yml .github/workflows/
```

## Resultado
Repo pronto para desenvolvimento com todos os arquivos de governança.