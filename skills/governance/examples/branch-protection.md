# Branch Protection & CI/CD Governance Rules

## 1. Overview & Policy Enforcement
To ensure zero regressions and maintain the integrity of production branches, the following branch protection rules are enforced via GitHub API and CI/CD policies.

---

## 2. Production (`master` / `main`) Protection Rules
- **Require Pull Request Reviews:** Minimum of 1 approving review from Code Owners before merge.
- **Require Status Checks to Pass:**
  - `lint-and-format`: Static analysis with zero warnings.
  - `unit-tests`: 100% test pass rate across supported matrix.
  - `sota-audit-engine`: 8-Dimension forensic audit pass.
- **Require Linear History:** Enforce squash merge or rebase merge (no merge commits in trunk).
- **Include Administrators:** Enforce protection rules strictly on repository administrators.
- **Do Not Allow Force Pushes:** Force pushing directly to production branches is permanently blocked.

---

## 3. Automation Setup Script (GitHub CLI)
```bash
#!/usr/bin/env bash
set -euo pipefail

gh api --method PUT /repos/:owner/:repo/branches/master/protection \
  --input - <<EOF
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["unit-tests", "sota-audit-engine"]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "required_approving_review_count": 1,
    "dismiss_stale_reviews": true
  },
  "restrictions": null
}
EOF
```