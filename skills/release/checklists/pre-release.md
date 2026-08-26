# Pre-Release Checklist

Execute antes de iniciar qualquer release.

## Versioning
- [ ] Major, minor, and patch versions incremented correctly (MAJOR.MINOR.PATCH)
- [ ] `index.json` reflects the new version
- [ ] `version` in the frontmatter of all skills updated (if applicable)

## CHANGELOG
- [ ] `[Unreleased]` entry moved to the new version
- [ ] Release date updated
- [ ] All changes documented (Added, Changed, Fixed, Removed)
- [ ] Keep a Changelog format maintained

## Quality
- [ ] `validate-index.sh` passes: 0 errors
- [ ] `validate-skill.sh` passes for all skills: 0 errors
- [ ] No `related_skills` pointing to non-existent skills
- [ ] `README.md` updated with new skill count

## Git
- [ ] Branch clean (no uncommitted changes)
- [ ] All commits follow Conventional Commits
- [ ] Merge into master via PR (if applicable)
- [ ] Tag created: `v{MAJOR}.{MINOR}.{PATCH}`

## Deploy
- [ ] GitHub Pages build triggered
- [ ] Site updated with new skills

---

*Pre-release checklist for ignite-agents-skills.*