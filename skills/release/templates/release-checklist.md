# Production Release Governance Checklist

## Phase 1: Pre-Release Invariants & Quality Gates
- [ ] Ensure all feature branches are merged cleanly into `master` / release branch.
- [ ] Run full automated test suite (`python3 -m unittest discover`) with 100% passing tests.
- [ ] Execute linter, static analysis, and type checker with zero errors and zero warnings.
- [ ] Verify that all Architecture Decision Records (ADRs) have corresponding Evidence Records.
- [ ] Confirm no active high-severity technical debts remain in the registry.

---

## Phase 2: Documentation & Version Reconciliation
- [ ] Update version strings across all canonical pillars (`package.json`, `index.json`, `README.md`).
- [ ] Generate comprehensive entry in `CHANGELOG.md` following Keep a Changelog standards.
- [ ] Draft detailed `RELEASE-NOTES.md` highlighting key changes, metrics, and breaking changes.
- [ ] Rebuild static documentation portal (`python3 pages/build.py`) with latest metadata.

---

## Phase 3: Tagging, Deployment & Multi-Target Sync
- [ ] Create annotated and signed Git tag (`git tag -a vX.Y.Z -m "release: vX.Y.Z"`).
- [ ] Push branch and tags to remote repository (`git push origin master --tags`).
- [ ] Execute multi-target runtime synchronization engine (`python3 scripts/sync_runtime.py --deploy`).
- [ ] Verify GitHub Actions release workflow passes and deploys to production / GitHub Pages.

---

## Phase 4: Post-Release Verification & Monitoring
- [ ] Verify live production endpoints and asset CDN caches.
- [ ] Monitor telemetry, error logs, and performance metrics for regression anomalies.
- [ ] Announce release to stakeholders and update roadmap milestones.