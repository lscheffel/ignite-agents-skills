# Exemplo: Release Process

## Pré-Release
```bash
# Atualizar CHANGELOG
## [1.2.0] - 2024-01-15
### Added
- Social login com Google

# Bump versão
npm version minor
```

## Release
```bash
git add .
git commit -m "chore(release): prepare v1.2.0"
git tag v1.2.0
git push origin main --tags
npm publish
gh release create v1.2.0
```

## Resultado
- Release publicada
- CHANGELOG atualizado
- Usuários notificados