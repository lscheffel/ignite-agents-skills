#!/usr/bin/env python3
"""
scripts/translate_git_workflow.py — Translates git-workflow/SKILL.md and agent-planning-execution/SKILL.md to EN-US
"""

import re
from pathlib import Path

def translate_git_workflow():
    p = Path("skills/git-workflow/SKILL.md")
    content = p.read_text(encoding="utf-8")
    
    replacements = [
        ("Padrões e workflows para versionamento com Git.", "Standards and workflows for version control with Git."),
        ("## Quando Usar", "## When to Use"),
        ("### Use quando:", "### Use when:"),
        ("- Precisa criar commits com mensagens padronizadas", "- Need to create commits with standardized messages (Conventional Commits)"),
        ("- Precisa decidir entre merge, rebase ou cherry-pick", "- Need to decide between merge, rebase, or cherry-pick"),
        ("- Precisa resolver conflitos de merge", "- Need to resolve merge conflicts deterministically"),
        ("- Precisa configurar branching strategy para equipe", "- Need to configure branching strategy for a team"),
        ("- Precisa fazer release via Git Flow", "- Need to manage releases via Git Flow or Trunk-Based workflows"),
        ("### Não use quando:", "### Do not use when:"),
        ("- Trabalhando em repositório somente leitura", "- Working in a read-only repository"),
        ("- Precisa de versionamento sem Git (ex: SVN)", "- Using non-Git version control systems (e.g., SVN, Mercurial)"),
        ("- Trabalhando com monorepo que usa outro sistema", "- Working in a repository managed by non-Git source control"),
        ("### Skills relacionadas:", "### Related Skills:"),
        ("- `governance` — para processos de branch protection e CODEOWNERS", "- `governance` — for branch protection rules and CODEOWNERS"),
        ("- `release` — para versionamento semântico e tags", "- `release` — for semantic versioning and release tags"),
        ("- `repo-bootstrap` — para configurar .gitignore e gitignore.io", "- `repo-bootstrap` — for configuring .gitignore and gitignore.io templates"),
        ("A[Preciso de Git?]", "A[Need Git Operation?]"),
        ("Criar commit", "Create commit"),
        ("Criar branch", "Create branch"),
        ("Qual tipo?", "What type?"),
        ("Nova feature", "New feature"),
        ("Hotfix produção", "Production hotfix"),
        ("Integrar branch", "Integrate branch"),
        ("Precisa preservar histórico", "Need full history"),
        ("Precisa histórico limpo", "Need clean linear history"),
        ("Branch compartilhado", "Shared remote branch"),
        ("Merge - NUNCA rebase", "Merge - NEVER rebase"),
        ("Branch local", "Local private branch"),
        ("Resolver conflito", "Resolve conflict"),
        ("Conflito de Merge", "Merge Conflict"),
        ("Arquivo binário", "Binary file conflict"),
        ("Arquivo texto", "Text file conflict"),
        ("Editar manualmente", "Edit markers manually"),
        ("### Fase 1: Criar Commit Convencional", "### Phase 1: Create Conventional Commit"),
        ("Stageie os arquivos relevantes:", "Stage the relevant files:"),
        ("Verifique o status:", "Verify working tree status:"),
        ("Crie o commit:", "Create the commit:"),
        ("Verifique o commit no log:", "Verify the commit in git log:"),
        ("Deve mostrar:", "Should display:"),
        ("### Fase 2: Resolver Conflito de Merge", "### Phase 2: Resolve Merge Conflict"),
        ("Identifique os arquivos em conflito:", "Identify conflicted files:"),
        ("Abra o arquivo e localize os marcadores:", "Open the file and locate conflict markers:"),
        ("Edite para manter o código correto:", "Edit to preserve correct code logic:"),
        ("Marque o conflito como resolvido:", "Mark the conflict as resolved:"),
        ("Conclua o merge:", "Complete the merge commit:"),
        ("Aborte o merge se necessário:", "Abort the merge if necessary:"),
        ("### Fase 3: Branching Strategy", "### Phase 3: Branching Strategy"),
        ("Escolha o modelo adequado:", "Select the appropriate branching model:"),
        ("Git Flow (recomendado para releases agendadas)", "Git Flow (recommended for scheduled milestone releases)"),
        ("Trunk-Based (recomendado para CI/CD contínuo)", "Trunk-Based (recommended for continuous integration and delivery)"),
        ("### Fase 4: Rebase Interativo para Limpar Histórico", "### Phase 4: Interactive Rebase for Clean History"),
        ("Inicie o rebase nos últimos N commits:", "Start interactive rebase on the last N commits:"),
        ("No editor, altere os comandos conforme necessário:", "In the editor, modify commands as necessary:"),
        ("Se houver conflitos durante o rebase:", "If conflicts occur during rebase:"),
        ("Salve e feche o editor. O Git aplicará as mudanças.", "Save and close the editor. Git will apply the rebased commits."),
        ("Seguro para shared", "Safe for shared branch"),
        ("Histórico linear", "Linear history"),
        ("Preserva contexto exato", "Preserves exact context"),
        ("Fácil de desfazer", "Easy rollback"),
        ("Template para mensagens de commit padronizadas.", "Template for standardized commit messages."),
        ("Convenção de nomes para branches.", "Naming conventions for branches."),
        ("Template para descrição de Pull Request.", "Template for Pull Request descriptions."),
        ("# Copie para usar como base", "# Copy to use as a baseline"),
        ("## Anti-Patterns", "## Anti-Patterns"),
        ("### Force push em branch compartilhado", "### Force push to shared branch"),
        ("**O que é:** Usar `git push --force` em branch que outros desenvolvedores estão usando.", "**What it is:** Using `git push --force` on branches shared with other developers."),
        ("**Por que é ruim:** Destrói histórico que outros desenvolvedores dependem, causando perda de trabalho.", "**Why it is bad:** Overwrites upstream commit history, causing unrecoverable data loss for collaborators."),
        ("**Como evitar:** Use `git push --force-with-lease` ou nunca force push em branches compartilhados.", "**How to avoid:** Use `git push --force-with-lease` and enforce branch protection on shared branches."),
        ("### Commit com segredos/credenciais", "### Committing secrets or credentials"),
        ("**O que é:** Commitar arquivos contendo senhas, tokens ou credenciais.", "**What it is:** Committing files containing passwords, API tokens, or credentials."),
        ("**Por que é ruim:** Exposição de credenciais no histórico do Git, impossível remover completamente.", "**Why it is bad:** Leaks credentials into permanent git history, necessitating credential revocation."),
        ("**Como evitar:** Use `.gitignore`, `git-secrets`, `trufflehog` e variáveis de ambiente.", "**How to avoid:** Use `.gitignore`, pre-commit scanners (`gitleaks`, `trufflehog`), and environment variables."),
        ("### Commit \"WIP\" ou mensagens genéricas", "### Generic 'WIP' commit messages"),
        ("**O que é:** Mensagens genéricas como \"fix bug\" ou \"update code\".", "**What it is:** Using generic messages such as 'fix bug', 'wip', or 'update code'."),
        ("**Por que é ruim:** Dificulta busca no histórico e gera documentação ruim.", "**Why it is bad:** Degrades git log traceability, bisect debugging, and changelog generation."),
        ("**Como evitar:** Use Conventional Commits com escopo e descrição clara.", "**How to avoid:** Follow Conventional Commits with concise scope and descriptive summaries."),
        ("### Trabalhar direto na branch main", "### Direct commits to main/production"),
        ("**O que é:** Trabalhar diretamente em main sem Pull Request.", "**What it is:** Pushing direct commits to main without peer review or automated CI verification."),
        ("**Por que é ruim:** Nenhuma revisão de código, histórico de decisões perdido.", "**Why it is bad:** Bypasses review gates and increases deployment breakage risks."),
        ("**Como evitar:** Sempre crie PR, mesmo para mudanças pequenas.", "**How to avoid:** Always open a Pull Request and require automated CI status checks."),
        ("### Commit grande com múltiplas mudanças", "### Giant commits with multi-topic changes"),
        ("**O que é:** Commitar vários arquivos com mudanças não relacionadas.", "**What it is:** Bundling unrelated refactorings, feature changes, and formatting in one commit."),
        ("**Por que é ruim:** Dificulta rollback seletivo e revisão de código.", "**Why it is bad:** Impairs atomic rollbacks and makes PR review cognitive load unmanageable."),
        ("**Como evitar:** Faça commits atômicos — uma mudança lógica por commit.", "**How to avoid:** Keep commits atomic — one cohesive logical change per commit."),
        ("- [ ] Arquivo .env não está no stage", "- [ ] .env and secret files excluded from staging"),
        ("- [ ] Branch está atualizada com main", "- [ ] Branch rebased and updated against main"),
        ("- [ ] Todos os testes passam", "- [ ] All unit and integration tests pass"),
        ("- [ ] Pelo menos 1 aprovação", "- [ ] At least 1 approving peer review received"),
        ("- [ ] Todos os testes E2E passam", "- [ ] All CI/CD and E2E checks pass"),
        ("- [ ] Tag criada com semantic versioning", "- [ ] Tag created using semantic versioning"),
        ("### Submodule com conflito", "### Submodule conflict"),
        ("**Situação:** Conflito em repositório que usa submodules.", "**Situation:** Conflict in repository utilizing git submodules."),
        ("### Rebase com arquivo binário conflito", "### Rebase with binary file conflict"),
        ("**Solução:** Use merge strategy para binários.", "**Solution:** Use checkout merge strategy for binary assets (`git checkout --ours/--theirs`)."),
        ("**Solução:** Crie branch para trabalhar ou retorne ao branch anterior.", "**Solution:** Create a tracking branch or return to previous branch state."),
        ("**Exceção:** Se for só para inspecionar, não há problema.", "**Exception:** If inspecting read-only state, detached HEAD is acceptable."),
        ("# ou criar branch", "# or create new branch"),
        ("- `governance` — para branch protection e CODEOWNERS", "- `governance` — for branch protection and CODEOWNERS"),
        ("- `release` — para versionamento semântico", "- `release` — for semantic versioning"),
        ("## Sub-Domain / Component: `git`", "## Domain Architecture: Git Operations"),
    ]
    
    for pt, en in replacements:
        content = content.replace(pt, en)
        
    p.write_text(content, encoding="utf-8")
    print("[✓] Fully translated skills/git-workflow/SKILL.md to EN-US")

def translate_agent_planning_execution():
    p = Path("skills/agent-planning-execution/SKILL.md")
    content = p.read_text(encoding="utf-8")
    
    # Replace all leftover PT occurrences
    content = re.sub(r"> Quando você precisar varrer as ADRs.*?\n", r"> When scanning repository ADRs for context, **FIRST** read `docs/adr/ADR-INDEX.md` or inspect ADR frontmatters via grep.\n", content)
    content = re.sub(r"> Você está \*\*PROIBIDO\*\* de ler o conteúdo completo.*?\n", r"> You are **STRICTLY FORBIDDEN** from reading the full content (via `view_file` or `cat`) of any file with `implementation_status: CONSOLIDADA` in its YAML frontmatter. Apply a summary 'SKIP' to these files, as their content is historical and immutable. Only perform deep inspection if explicitly requested by the user for an audit, or if the active task specifically modifies that architecture.\n", content)
    content = re.sub(r"> \*\*ATENÇÃO:\*\* O planejamento deve idealmente.*?\n", r"> **IMPORTANT:** Planning must ideally derive from an approved ADR and be reflected in the Roadmap.\n", content)
    content = re.sub(r"> 1\. \*\*Fallback\*\*: Se a feature solicitada é complexa.*?\n", r"> 1. **Fallback**: If the requested feature is complex and lacks an ADR, trigger the `adr-generator` skill before proceeding.\n", content)
    content = re.sub(r"> 3\. \*\*Roadmap\*\*: Exija o preenchimento ou atualização.*?\n", r"> 3. **Roadmap**: Require filling or updating the project Roadmap (via `roadmap-update` or by modifying the applicable roadmap file) to reflect newly created plans.\n", content)
    content = re.sub(r"> \*\*ATENÇÃO:\*\* Planos de implementação \(PI\) devem.*?\n", r"> **IMPORTANT:** Implementation Plans (PI) must ideally derive from an approved ADR.\n", content)
    content = re.sub(r"> 1\. Se não houver ADR para a feature solicitada.*?\n", r"> 1. If no ADR exists for the requested feature, trigger the **Fallback**: prompt the user to generate an ADR (using the `adr-generator` skill) before detailing the plan, unless it is a trivial task.\n", content)
    content = re.sub(r"> 3\. Exija o uso e atualização do arquivo `docs/adr/ADR-XXX-TODO\.md`.*?\n", r"> 3. Require the use and update of `docs/adr/ADR-XXX-TODO.md` to track tasks created in the PI (do not use legacy formats like `task-card`).\n", content)
    content = re.sub(r"> \*\*É TERMINANTEMENTE PROIBIDO\*\* criar múltiplos arquivos TODO.*?\n", r"> **IT IS STRICTLY FORBIDDEN** to create multiple TODO files for the same ADR (e.g. `ADR-XXX-P2-TODO.md`). The Decision Set format requires strict 1:1 mapping.\n", content)
    content = re.sub(r"> Se uma ADR tiver múltiplas fases.*?\n", r"> If an ADR contains multiple phases, map ALL OF THEM within a single `ADR-XXX-TODO.md` file using markdown section headers (`## Phase 1`, `## Phase 2`).\n", content)
    content = re.sub(r"> Se o escopo da ADR for gigantesco.*?\n", r"> If the scope of the ADR is too massive for a single TODO, guide the user to decompose the parent ADR into independent sub-ADRs (e.g. `ADR-008-A`, `ADR-008-B`), each with its own Decision Set.\n", content)
    content = re.sub(r"> Se o repositório for legado e não possuir governança de ADRs.*?\n", r"> If the repository is legacy and lacks ADR governance (silent fallback), save provisionally to: `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md` and ignore the `todo` file.\n", content)

    p.write_text(content, encoding="utf-8")
    print("[✓] Fully translated skills/agent-planning-execution/SKILL.md to EN-US")

if __name__ == "__main__":
    translate_git_workflow()
    translate_agent_planning_execution()
