#!/usr/bin/env python3
"""
scripts/translate_catalog_portuguese_cleaner.py — Comprehensive PT-BR to EN-US Normalization

Translates all remaining Portuguese prose, table rows, checklists, and edge cases in `skills/`
into clean, idiomatic technical English (EN-US), while strictly preserving:
1. Bilingual `triggers` and `tags` in YAML frontmatter (for discovery/routing).
2. Code identifiers, backtick markdown tokens, and URLs.
"""

import re
from pathlib import Path

REPLACEMENTS = [
    # Tables & Anti-patterns (flexible regex)
    (
        r"\|\s*\*\*Execução Prematura sem Contexto\*\*\s*\|\s*🔴\s*Critical\s*\|\s*Alucinação de contexto e refatoração destrutiva\s*\|\s*Ativar a skill `cap` para adquirir evidências mínimas antes de editar\.\s*\|",
        r"| **Premature Execution Without Context** | 🔴 Critical | Context hallucination and destructive refactoring | Activate `cap` to acquire minimal evidence before editing. |"
    ),
    (
        r"\|\s*\*\*Omissão de Checklists de Validação\*\*\s*\|\s*🟡\s*Medium\s*\|\s*Entrega de artefatos com inconsistências sintáticas\s*\|\s*Executar rigorosamente o checklist passo a passo antes do handoff\.\s*\|",
        r"| **Omission of Validation Checklists** | 🟡 Medium | Delivering artifacts with syntax inconsistencies | Rigorously execute the checklist step-by-step before handoff. |"
    ),

    # Specific prose in agent-planning-execution
    (
        r"> Quando você precisar varrer as ADRs do repositório para obter contexto, faça \*\*PRIMEIRO\*\* a leitura do `docs/adr/ADR-INDEX\.md` ou um `grep` no frontmatter das ADRs\.",
        r"> When scanning repository ADRs for context, **FIRST** read `docs/adr/ADR-INDEX.md` or grep the frontmatter of ADRs."
    ),
    (
        r"> Você está \*\*PROIBIDO\*\* de ler o conteúdo completo \(via `view_file` ou `cat`\) de qualquer arquivo que possua a tag `implementation_status: CONSOLIDADA` no seu frontmatter YAML\. Aplique o 'SKIP' sumário a esses arquivos, pois o conteúdo é passado e estático\. Só faça a leitura profunda caso o usuário solicite especificamente uma auditoria, ou se a tarefa atual exigir a modificação daquela exata arquitetura\.",
        r"> You are **STRICTLY FORBIDDEN** from reading the full content (via `view_file` or `cat`) of any file with `implementation_status: CONSOLIDADA` in its YAML frontmatter. Apply a summary 'SKIP' to these files, as their content is historical and immutable. Only perform deep inspection if explicitly requested by the user for an audit, or if the active task specifically modifies that architecture."
    ),
    (
        r"> \*\*ATENÇÃO:\*\* O planejamento deve idealmente ser derivado de uma ADR aprovada e refletido no Roadmap\.",
        r"> **IMPORTANT:** Planning must ideally derive from an approved ADR and be reflected in the Roadmap."
    ),
    (
        r"> 1\. \*\*Fallback\*\*: Se a feature solicitada é complexa e não possui ADR, acione a skill `adr-generator` antes de prosseguir\.",
        r"> 1. **Fallback**: If the requested feature is complex and lacks an ADR, trigger the `adr-generator` skill before proceeding."
    ),
    (
        r"> 3\. \*\*Roadmap\*\*: Exija o preenchimento ou atualização do Roadmap do projeto \(via `roadmap-update` ou atualizando o arquivo de roadmap aplicável\) para refletir o planejamento recém-criado\.",
        r"> 3. **Roadmap**: Require filling or updating the project Roadmap (via `roadmap-update` or by modifying the applicable roadmap file) to reflect newly created plans."
    ),
    (
        r"> \*\*ATENÇÃO:\*\* Planos de implementação \(PI\) devem idealmente derivar de uma ADR aprovada\.",
        r"> **IMPORTANT:** Implementation Plans (PI) must ideally derive from an approved ADR."
    ),
    (
        r"> 1\. Se não houver ADR para a feature solicitada, acione o \*\*Fallback\*\*: peça para o usuário gerar a ADR \(usando a skill `adr-generator`\) antes de detalhar o plano, a menos que seja uma tarefa trivial\.",
        r"> 1. If no ADR exists for the requested feature, trigger the **Fallback**: prompt the user to generate an ADR (using the `adr-generator` skill) before detailing the plan, unless it is a trivial task."
    ),
    (
        r"> 3\. Exija o uso e atualização do arquivo `docs/adr/ADR-XXX-TODO\.md` para rastrear as tarefas criadas no PI\. \(Não use formatos antigos como `task-card`\)\.",
        r"> 3. Require the use and update of `docs/adr/ADR-XXX-TODO.md` to track tasks created in the PI (do not use legacy formats like `task-card`)."
    ),
    (
        r"> \*\*É TERMINANTEMENTE PROIBIDO\*\* criar múltiplos arquivos TODO para a mesma ADR \(ex: `ADR-XXX-P2-TODO\.md` ou `ADR-XXX-Fase2-TODO\.md`\)\. O formato da Quadra exige mapeamento 1:1 rigoroso\.",
        r"> **IT IS STRICTLY FORBIDDEN** to create multiple TODO files for the same ADR (e.g. `ADR-XXX-P2-TODO.md`). The Decision Set format requires strict 1:1 mapping."
    ),
    (
        r"> Se uma ADR tiver múltiplas fases, mapeie TODAS ELAS em um único arquivo `ADR-XXX-TODO\.md` usando cabeçalhos markdown \(`## Fase 1`, `## Fase 2`\)\.",
        r"> If an ADR contains multiple phases, map ALL OF THEM within a single `ADR-XXX-TODO.md` file using markdown section headers (`## Phase 1`, `## Phase 2`)."
    ),
    (
        r"> Se o escopo da ADR for gigantesco a ponto de inviabilizar um único TODO, oriente o usuário a desmembrar a própria ADR-mãe em sub-ADRs independentes \(ex: `ADR-008-A`, `ADR-008-B`\), cada qual com sua própria Quadra\.",
        r"> If the scope of the ADR is too massive for a single TODO, guide the user to decompose the parent ADR into independent sub-ADRs (e.g. `ADR-008-A`, `ADR-008-B`), each with its own Decision Set."
    ),
    (
        r"> Se o repositório for legado e não possuir governança de ADRs \(Fallback silencioso\), salve provisoriamente em: `docs/superpowers/plans/YYYY-MM-DD-<feature-name>\.md` e ignore o `todo`\.",
        r"> If the repository is legacy and lacks ADR governance (silent fallback), save provisionally to: `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md` and ignore the `todo` file."
    ),
]

def translate_file(file_path: Path):
    content = file_path.read_text(encoding="utf-8")
    
    # Split frontmatter to preserve triggers and tags untouched
    fm_match = re.match(r"^---\n(.*?)\n---\n(.*)$", content, re.DOTALL)
    if fm_match:
        frontmatter = fm_match.group(1)
        body = fm_match.group(2)
    else:
        frontmatter = ""
        body = content
        
    original_body = body
    for pattern, replacement in REPLACEMENTS:
        body = re.sub(pattern, replacement, body)
        
    if body != original_body:
        if frontmatter:
            new_content = f"---\n{frontmatter}\n---\n{body}"
        else:
            new_content = body
        file_path.write_text(new_content, encoding="utf-8")
        print(f"[✓] Translated PT-BR -> EN-US: {file_path.relative_to(file_path.parents[2])}")

def main():
    root = Path(__file__).resolve().parent.parent
    skills_dir = root / "skills"
    
    for md_file in sorted(skills_dir.glob("**/*.md")):
        translate_file(md_file)

if __name__ == "__main__":
    main()
