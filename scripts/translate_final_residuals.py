#!/usr/bin/env python3
"""
scripts/translate_final_residuals.py — Translates final remaining Portuguese snippets across skills
"""

from pathlib import Path

def run():
    # 1. testing-mastery
    tm = Path("skills/testing-mastery/SKILL.md")
    if tm.exists():
        content = tm.read_text(encoding="utf-8")
        content = content.replace("// Usar MSW para mockar API", "// Use MSW to mock API")
        tm.write_text(content, encoding="utf-8")
        
    # 2. git-workflow
    gw = Path("skills/git-workflow/SKILL.md")
    if gw.exists():
        content = gw.read_text(encoding="utf-8")
        gw_replacements = [
            ("G[Merge ou Rebase?]", "G[Merge or Rebase?]"),
            ('# Arquivos com "both modified" são conflitantes', '# Files marked "both modified" are in conflict'),
            ("código da branch que está mergeando", "code from the incoming branch"),
            ("3. Edite manualmente para resolver:", "3. Edit manually to resolve conflicts:"),
            ("1. Certifique-se que está em develop:", "1. Ensure you are on the develop branch:"),
            ("5. Commit das mudanças:", "5. Commit release preparation changes:"),
            ("6. Merge para main:", "6. Merge into main:"),
            ("8. Merge de volta para develop:", "8. Merge back into develop:"),
            ("10. **Checkpoint**: Push com tags:", "10. **Checkpoint**: Push commits with tags:"),
            ("3. No editor, escolha ação para cada commit:", "3. In the editor, choose the rebase action for each commit:"),
            ("- `squash` — unir com commit anterior", "- `squash` — combine with the previous commit"),
        ]
        for pt, en in gw_replacements:
            content = content.replace(pt, en)
        gw.write_text(content, encoding="utf-8")

    # 3. agent-planning-execution
    ape = Path("skills/agent-planning-execution/SKILL.md")
    if ape.exists():
        content = ape.read_text(encoding="utf-8")
        ape_replacements = [
            ("Quando você precisar varrer as ADRs do repositório para obter contexto, faça **PRIMEIRO** a leitura do `docs/adr/ADR-INDEX.md` ou um `grep` no frontmatter das ADRs.", "When scanning repository ADRs for context, **FIRST** read `docs/adr/ADR-INDEX.md` or grep the YAML frontmatter of ADRs."),
            ("Você está **PROIBIDO** de ler o conteúdo completo (via `view_file` ou `cat`) de qualquer arquivo que possua a tag `implementation_status: CONSOLIDADA` no seu frontmatter YAML. Aplique o 'SKIP' sumário a esses arquivos, pois o conteúdo é passado e estático. Só faça a leitura profunda caso o usuário solicite especificamente uma auditoria, ou se a tarefa atual exigir a modificação daquela exata arquitetura.", "You are **STRICTLY FORBIDDEN** from reading the full content (via `view_file` or `cat`) of any file with `implementation_status: CONSOLIDADA` in its YAML frontmatter. Apply a summary 'SKIP' to these files, as their content is historical and immutable. Only perform deep inspection if explicitly requested by the user for an audit, or if the active task specifically modifies that architecture."),
            ("**ATENÇÃO:** O planejamento deve idealmente ser derivado de uma ADR aprovada e refletido no Roadmap.", "**IMPORTANT:** Planning must ideally derive from an approved ADR and be reflected in the project Roadmap."),
            ("1. **Fallback**: Se a feature solicitada é complexa e não possui ADR, acione a skill `adr-generator` antes de prosseguir.", "1. **Fallback**: If the requested feature is complex and lacks an ADR, trigger the `adr-generator` skill before proceeding."),
            ("3. **Roadmap**: Exija o preenchimento ou atualização do Roadmap do projeto (via `roadmap-update` ou atualizando o arquivo de roadmap aplicável) para refletir o planejamento recém-criado.", "3. **Roadmap**: Require filling or updating the project Roadmap (via `roadmap-update` or by modifying the applicable roadmap file) to reflect newly created plans."),
            ("**ATENÇÃO:** Planos de implementação (PI) devem idealmente derivar de uma ADR aprovada.", "**IMPORTANT:** Implementation Plans (PI) must ideally derive from an approved ADR."),
            ("1. Se não houver ADR para a feature solicitada, acione o **Fallback**: peça para o usuário gerar a ADR (usando a skill `adr-generator`) antes de detalhar o plano, a menos que seja uma tarefa trivial.", "1. If no ADR exists for the requested feature, trigger the **Fallback**: prompt the user to generate an ADR (using the `adr-generator` skill) before detailing the plan, unless it is a trivial task."),
            ("3. Exija o uso e atualização do arquivo `docs/adr/ADR-XXX-TODO.md` para rastrear as tarefas criadas no PI. (Não use formatos antigos como `task-card`).", "3. Require using and updating `docs/adr/ADR-XXX-TODO.md` to track tasks created in the PI (do not use legacy formats like `task-card`)."),
            ("**É TERMINANTEMENTE PROIBIDO** criar múltiplos arquivos TODO para a mesma ADR (ex: `ADR-XXX-P2-TODO.md` ou `ADR-XXX-Fase2-TODO.md`). O formato da Quadra exige mapeamento 1:1 rigoroso.", "**IT IS STRICTLY FORBIDDEN** to create multiple TODO files for the same ADR (e.g. `ADR-XXX-P2-TODO.md`). The Decision Set format requires strict 1:1 mapping."),
            ("Se uma ADR tiver múltiplas fases, mapeie TODAS ELAS em um único arquivo `ADR-XXX-TODO.md` usando cabeçalhos markdown (`## Fase 1`, `## Fase 2`).", "If an ADR contains multiple phases, map ALL OF THEM within a single `ADR-XXX-TODO.md` file using markdown section headers (`## Phase 1`, `## Phase 2`)."),
            ("Se o escopo da ADR for gigantesco a ponto de inviabilizar um único TODO, oriente o usuário a desmembrar a própria ADR-mãe em sub-ADRs independentes (ex: `ADR-008-A`, `ADR-008-B`), cada qual com sua própria Quadra.", "If the scope of the ADR is too massive for a single TODO, guide the user to decompose the parent ADR into independent sub-ADRs (e.g. `ADR-008-A`, `ADR-008-B`), each with its own Decision Set."),
            ("Se o repositório for legado e não possuir governança de ADRs (Fallback silencioso), salve provisoriamente em: `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md` e ignore o `todo`.", "If the repository is legacy and lacks ADR governance (silent fallback), save provisionally to: `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md` and ignore the `todo` file."),
        ]
        for pt, en in ape_replacements:
            content = content.replace(pt, en)
        ape.write_text(content, encoding="utf-8")

    print("[✓] Residuals successfully translated to English.")

if __name__ == "__main__":
    run()
