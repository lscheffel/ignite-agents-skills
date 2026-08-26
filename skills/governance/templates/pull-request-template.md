# Pull Request Template

## Description

{Clear and concise summary of the change}

## Change Type

- [ ] Bug fix (non-API-breaking correction)
- [ ] Feature (new functionality)
- [ ] Breaking change (API-breaking change)
- [ ] Documentation (change only in docs)
- [ ] Refactor (improvement without behavior change)

## Checklist

### Code Quality
- [ ] Code adheres to project standards
- [ ] No commented or debug code
- [ ] Variables and functions have clear names
- [ ] Cyclomatic complexity < 10

### Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added (if applicable)
- [ ] All tests pass (`npm test`)
- [ ] Coverage ≥ 80% (if applicable)

### Documentation
- [ ] README.md updated (if necessary)
- [ ] Code comments added
- [ ] CHANGELOG.md updated (if necessary)

### Security
- [ ] No credentials exposed
- [ ] Input validated
- [ ] Dependencies verified (`npm audit`)

## Screenshots (if applicable)

{Add screenshots of UI or visual changes}

## Related Issues

Fixes #{issue-number}
Closes #{issue-number}
Relates to #{issue-number}