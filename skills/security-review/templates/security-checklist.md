# Security Checklist

Use this checklist during code reviews to ensure secure practices.

## Secrets & Credentials

- [ ] No hardcoded secrets in code
- [ ] `.env` is in `.gitignore`
- [ ] `.env.example` documents all variables
- [ ] Tests use mock/placeholder values
- [ ] Logs do not expose sensitive data (PII, tokens)

## Dependencies

- [ ] `npm audit` / `yarn audit` without critical vulnerabilities
- [ ] Discontinued dependencies replaced
- [ ] Licenses compatible with the project
- [ ] Lock file committed

## Encryption

- [ ] Suitable algorithms (not MD5/SHA1 for passwords)
- [ ] AES-GCM: unique 12-byte nonce per operation
- [ ] scrypt: N≥16384, r≥8, p≥1
- [ ] Keys not hardcoded
- [ ] Comparisons use `crypto.timingSafeEqual()`

## Authentication & Authorization

- [ ] Authenticated endpoints verified
- [ ] Rate limiting implemented
- [ ] Sessions expire properly
- [ ] Tokens have limited lifetimes

## Input Validation

- [ ] Inputs sanitized against XSS
- [ ] Parameterized queries (not concatenation)
- [ ] File uploads validated (type, size)
- [ ] Security headers present (CSP, HSTS)

## References

- [OWASP Top 10](https://owasp.org/Top10/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)

---

*Security checklist for ignite-agents-skills.*