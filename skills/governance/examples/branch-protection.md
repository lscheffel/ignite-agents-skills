# Exemplo: Configuração de Branch Protection

## Antes
- Push direto para main
- Nenhum review obrigatório
- CI opcional

## Depois
```yaml
# .github/branch-protection.yml
branches:
  - name: main
    protection:
      required_pull_request_reviews:
        required_approving_review_count: 1
      required_status_checks:
        strict: true
      restrictions: null
```

## Resultado
- 0 pushes diretos para main
- 100% dos PRs revisados
- CI obrigatório