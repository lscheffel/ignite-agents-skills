---
name: release
description: Guia para gestão de releases e versionamento. Define processo de release, changelog, tag, deploy e rollback. Use quando preparar releases, publicar pacotes, ou gerenciar versionamento semântico.
---

# Release

Guia para gestão de releases e versionamento.

## Quando Usar

- Preparação de releases
- Publicação de pacotes
- Gestão de versionamento semântico
- Processo de deploy e rollback

## Versionamento Semântico

`MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]`

### Níveis
- **MAJOR**: mudanças incompatíveis (breaking changes)
- **MINOR**: funcionalidades novas, retrocompatível
- **PATCH**: correções de bug, retrocompatível
- **PRERELEASE**: alpha, beta, rc
- **BUILD**: metadados de build

## Processo de Release

### 1. Preparação
- Atualizar CHANGELOG.md
- Bump versão em arquivos de configuração
- Criar branch de release (se GitFlow)

### 2. Validação
- Executar testes completos
- Executar lint
- Validar build

### 3. Publicação
- Merge de release branch para main
- Tag: `git tag v1.2.3`
- Push: `git push --tags`
- Publicar pacote (npm, docker, etc.)

### 4. Pós-release
- Merge de main para develop
- Incrementar versão para próximo dev
- Atualizar CHANGELOG para próxima versão

## Changelog

Siga o formato [Keep a Changelog](https://keepachangelog.com/):

```markdown
# Changelog

## [Unreleased]
### Added
- Nova funcionalidade X

## [1.2.0] - 2024-01-15
### Added
- Feature X
### Fixed
- Bug Y

[Unreleased]: https://github.com/.../compare/v1.2.0...HEAD
[1.2.0]: https://github.com/.../compare/v1.1.0...v1.2.0
```

## Rollback

- Tag de rollback: `v1.2.3-rollback-20240115`
- Documentar motivo do rollback
- Priorizar fix do problema root cause
