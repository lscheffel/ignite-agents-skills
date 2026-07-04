---
name: repo-bootstrap
description: Gera estrutura inicial de repositório com arquivos de governança: README.md, AGENTS.md, CHANGELOG.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md, LICENSE, estrutura de docs/ e exemplos de CI/CD. Use quando iniciar um novo repositório ou padronizar estrutura de projeto.
---

# Repo Bootstrap

Gera estrutura inicial padronizada para repositórios.

## Quando Usar

- Inicialização de novo repositório
- Padronização de estrutura existente
- Onboarding de novos projetos
- Criação de templates de repositório

## Estrutura Gerada

```
repo/
├── README.md
├── AGENTS.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── LICENSE
├── .github/
│   └── workflows/
│       └── ci.yml
├── docs/
│   ├── architecture/
│   ├── adr/
│   └── decisions/
└── src/
```

## Arquivos Gerados

### README.md
- Descrição do projeto
- Pré-requisitos
- Instalação
- Uso básico
- Como contribuir (link para CONTRIBUTING.md)
- Licença

### AGENTS.md
- Instruções para agentes de IA trabalharem no projeto
- Padrões de código
- Estrutura do projeto
- Comandos importantes
- Restrições e regras

### CHANGELOG.md
- Formato Keep a Changelog
- Seções: Added, Changed, Deprecated, Removed, Fixed, Security

### CONTRIBUTING.md
- Processo de contribuição
- Padrões de commit
- Fluxo de PR
- Checklist de revisão

### CODE_OF_CONDUCT.md
- Baseado no Contributor Covenant
- Comportamento esperado
- Processo de reporte

### SECURITY.md
- Política de segurança
- Como reportar vulnerabilidades
- Versões suportadas

### .github/workflows/ci.yml
- Lint
- Testes
- Build
- Publicação (se aplicável)
