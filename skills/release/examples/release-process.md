# Example: Release Process

## Pre-Release
```bash
# Update CHANGELOG
## [1.2.0] - 2024-01-15
### Added
- Google social login

# Bump version
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

## Result
- Release published
- CHANGELOG updated
- Users notified