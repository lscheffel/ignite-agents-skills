# Contributing Guidelines

Thank you for your interest in contributing to this project! To maintain the highest standards of code quality, security, and developer experience, please adhere to the following workflow:

---

## 1. Code of Conduct & Ground Rules
- Treat all contributors and users with respect and professional courtesy.
- Ensure all contributions follow the Single Source of Truth (SSOT) defined in `AGENTS.md`.
- No code changes may be merged without accompanying automated tests.

---

## 2. Development Workflow & Git Etiquette
1. **Fork or Branch:** Create a feature branch following the naming convention:
   - `feature/<feature-name>`
   - `fix/<bugfix-name>`
   - `docs/<doc-update>`
2. **Follow TDD:** Write failing unit tests demonstrating the requirement or bug before implementing production code.
3. **Commit Messages:** Follow Conventional Commits:
   - `feat(scope): add new feature`
   - `fix(scope): resolve bug`
   - `docs(scope): update documentation`

---

## 3. Pull Request & Quality Gates
- Run all automated linters and unit tests locally before submitting a PR.
- Ensure CI/CD checks pass with 100% success rate.
- Request reviews from repository maintainers and resolve all actionable comments.