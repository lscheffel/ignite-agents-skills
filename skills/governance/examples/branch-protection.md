# Example: Branch Protection Configuration

## Before
- Direct push to main
- No mandatory review
- CI optional

## After
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

## Result
- 0 direct pushes to main
- 100% of PRs reviewed
- CI mandatory