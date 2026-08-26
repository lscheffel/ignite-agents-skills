# Example: Dependency Audit — Node.js Project

## Context

Express.js application with 47 direct dependencies. Requires security audit before deployment.

## Tools Used

- `npm audit` (native)
- `snyk test` (complementary)
- Manual review of critical dependencies

## Execution

### Step 1: npm audit

```bash
$ npm audit --json | jq '.metadata.vulnerabilities'
{
  "info": 0,
  "low": 3,
  "medium": 2,
  "high": 1,
  "critical": 0,
  "total": 6
}
```

### Step 2: Detailing Vulnerabilities

| Package | Severity | Vulnerability | Affected Version | Fix |
|--------|------------|-----------------|----------------|-----|
| `lodash` | 🟡 Medium | Prototype Pollution | <4.17.21 | Update to 4.17.21 |
| `minimist` | 🟡 Medium | Prototype Pollution | <1.2.6 | Update to 1.2.6 |
| `node-fetch` | 🔴 High | Information Exposure | <2.6.7 | Update to 2.6.7 |
| `express` | 🟢 Low | Open Redirect | <4.18.2 | Update to 4.18.2 |
| `qs` | 🟢 Low | Prototype Pollution | <6.11.0 | Update to 6.11.0 |
| `cookie` | 🟢 Low | Insufficient Validation | <0.5.0 | Update to 0.5.0 |

### Step 3: Impact Analysis

**`node-fetch` (High):**
- Vulnerability: exposes authorization headers in cross-origin redirects
- Impact: access tokens may be leaked if malicious redirect occurs
- Mitigation: verify if the application follows redirects (rare in APIs)
- Action: URGENTLY UPDATE

**`lodash` and `minimist` (Medium):**
- Vulnerability: prototype pollution allows property injection
- Impact: depends on how the application processes user input
- Mitigation: verify if unsanitized user input is passed to these libs
- Action: UPDATE

### Step 4: Correction

```bash
# Update vulnerable dependencies
npm install lodash@4.17.21 minimist@1.2.6 node-fetch@2.6.7 express@4.18.2 qs@6.11.0 cookie@0.5.0

# Verify correction
npm audit
# expected: 0 vulnerabilities
```

### Step 5: Validation

```bash
# Run tests to ensure updates did not break anything
npm test

# Verify no unexpected lockfile changes
git diff package-lock.json | grep -E "^\+.*version" | head -10
```

## Result

| Metric | Before | After |
|---------|-------|--------|
| Vulnerabilities | 6 | 0 |
| High | 1 | 0 |
| Medium | 2 | 0 |
| Low | 3 | 0 |
| Updated Dependencies | — | 6 |

## Recommendations

1. **Automate:** Add `npm audit --audit-level=high` to CI
2. **Dependabot:** Enable dependabot for automatic PRs
3. **Quarterly Review:** Perform complete audit every quarter
4. **Lockfile:** Commit `package-lock.json` always