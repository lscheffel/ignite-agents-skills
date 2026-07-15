import os
import sys
import glob
import re
import datetime
import shutil

def extract_frontmatter_info(filepath):
    info = {"title": "Unknown Title", "impl_status": "PENDENTE", "status": "unknown"}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
            # Extract title
            match = re.search(r"^title:\s*(.*?)$", content, re.MULTILINE)
            if match:
                info["title"] = match.group(1).strip()
            else:
                match = re.search(r"^#\s+(.*?)$", content, re.MULTILINE)
                if match:
                    info["title"] = match.group(1).strip()
                    
            # Extract implementation_status
            match = re.search(r"^implementation_status:\s*(.*?)$", content, re.MULTILINE)
            if match:
                info["impl_status"] = match.group(1).strip()
                
            # Extract ADR status (draft, proposed, accepted, etc.)
            match_status = re.search(r"^## Status\s+(.*?)(?=^##|\Z)", content, re.MULTILINE | re.DOTALL | re.IGNORECASE)
            if match_status:
                status_text = match_status.group(1).strip().lower()
                if status_text:
                    info["status"] = status_text.split('\n')[0].strip()
    except Exception:
        pass
    return info

def update_implementation_status(filepath, status_value):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
        if match:
            frontmatter = match.group(1)
            if "implementation_status:" in frontmatter:
                new_frontmatter = re.sub(r"implementation_status:.*", f"implementation_status: {status_value}", frontmatter)
            else:
                new_frontmatter = frontmatter + f"\nimplementation_status: {status_value}"
            new_content = content[:match.start(1)] + new_frontmatter + content[match.end(1):]
        else:
            new_content = f"---\nimplementation_status: {status_value}\n---\n\n" + content
            
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
    except Exception as e:
        print(f"Erro atualizando tag em {filepath}: {e}")

def parse_todo(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        tasks = []
        
        table_pattern = re.compile(r"^\s*\|\s*([A-Za-z0-9\.]+)\s*\|\s*(.*?)\s*\|\s*([✅⬜🔄❌⏸️])\s*\|", re.MULTILINE)
        for match in table_pattern.finditer(content):
            task_id = match.group(1).strip()
            desc = match.group(2).strip()
            status_icon = match.group(3).strip()
            
            is_done = status_icon == "✅"
            tasks.append({
                "desc": f"[{task_id}] {desc}",
                "done": is_done,
                "raw_status": status_icon
            })
            
        list_pattern = re.compile(r"^\s*-\s*\[([ xX])\]\s+(.*?)$", re.MULTILINE)
        for match in list_pattern.finditer(content):
            status_char = match.group(1).strip().lower()
            desc = match.group(2).strip()
            
            is_done = status_char == "x"
            tasks.append({
                "desc": desc,
                "done": is_done,
                "raw_status": status_char
            })
            
        return tasks
    except Exception as e:
        print(f"Erro lendo TODO {filepath}: {e}")
        return []

def main():
    if len(sys.argv) < 2:
        print("Usage: python audit.py <repo_path> [--archive <ADR_ID>]")
        sys.exit(1)
        
    repo_path = sys.argv[1]
    
    # Handle --archive flag
    if len(sys.argv) >= 4 and sys.argv[2] == "--archive":
        archive_id = sys.argv[3]
        adr_root = os.path.join(repo_path, "docs", "adr")
        
        todo_file = os.path.join(adr_root, f"{archive_id}-TODO.md")
        er_file = os.path.join(adr_root, f"{archive_id}-ER.md")
        
        # Validations before archiving
        if not os.path.exists(todo_file):
            print(f"Erro: Não é possível arquivar {archive_id} (Arquivo TODO não encontrado).")
            sys.exit(1)
            
        tasks = parse_todo(todo_file)
        if tasks and not all(t["done"] for t in tasks):
            print(f"Erro: Não é possível arquivar {archive_id} (Existem tarefas PENDENTES no TODO).")
            sys.exit(1)
            
        if not os.path.exists(er_file):
            print(f"Erro: Não é possível arquivar {archive_id} (Arquivo ER ausente na raiz).")
            sys.exit(1)
            
        archive_dir = os.path.join(repo_path, "docs", "adr", "archive")
        os.makedirs(archive_dir, exist_ok=True)
        pattern = os.path.join(adr_root, f"{archive_id}*.md")
        
        moved_count = 0
        for filepath in glob.glob(pattern):
            if filepath.endswith("-ER.md"):
                continue
            if os.path.dirname(filepath) == adr_root:
                filename = os.path.basename(filepath)
                shutil.move(filepath, os.path.join(archive_dir, filename))
                moved_count += 1
                print(f"Archived: {filename}")
        print(f"Archival of {archive_id} complete. ({moved_count} files moved)")
        sys.exit(0) # Stop execution here so we don't run a full audit without being explicitly asked, or we can just let it run. Let's let it run the full audit to update index.
        
    reports_dir = os.path.join(repo_path, "docs", "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    adr_files = glob.glob(os.path.join(repo_path, "**", "ADR-*.md"), recursive=True)
    
    results = []
    debts = []
    seen_debts = set()
    actions = []
    
    for filepath in adr_files:
        dirname = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        
        if not re.match(r"^ADR-\d+\.md$", filename):
            continue
            
        adr_id = filename.replace(".md", "")
        fm_info = extract_frontmatter_info(filepath)
        title = fm_info["title"]
        current_impl_status = fm_info["impl_status"]
        adr_status = fm_info.get("status", "unknown")
        is_draft_or_proposed = adr_status in ["draft", "proposed"]
        is_archived = os.path.basename(dirname) == "archive"
        root_adr_dir = os.path.dirname(dirname) if is_archived else dirname
            
        todo_file = os.path.join(dirname, f"{adr_id}-TODO.md")
        er_file = os.path.join(root_adr_dir, f"{adr_id}-ER.md")
        
        if not os.path.exists(todo_file):
            results.append({
                "id": adr_id,
                "title": title,
                "status": "NO_TODO",
                "archived": is_archived,
                "total_tasks": 0,
                "done_tasks": 0
            })
            continue
            
        tasks = parse_todo(todo_file)
        
        if not tasks:
            is_fully_implemented = os.path.exists(er_file)
        else:
            is_fully_implemented = all(t["done"] for t in tasks)
            
        for t in tasks:
            if not t["done"]:
                clean_desc = t["desc"].strip()
                normalized = clean_desc.lower()
                if normalized not in seen_debts:
                    seen_debts.add(normalized)
                    if not is_draft_or_proposed:
                        debts.append(f"- **{adr_id}**: {clean_desc}")
                    
        status_flag = ""
        action_flag = ""
        
        if is_archived:
            if is_fully_implemented:
                if not os.path.exists(er_file):
                    action_flag = f"ARCHIVED_NEEDS_ER: {adr_id} (Path: {dirname})"
                    status_flag = "ARCHIVED_NEEDS_ER"
                else:
                    status_flag = "ARCHIVED_OK"
            else:
                action_flag = f"ARCHIVED_MISTAKE_RETURN: {adr_id} (Path: {dirname})"
                status_flag = "ARCHIVED_MISTAKE"
        else:
            if is_fully_implemented:
                if os.path.exists(er_file):
                    action_flag = f"READY_TO_ARCHIVE: {adr_id} (Path: {dirname})"
                    status_flag = "READY_TO_ARCHIVE"
                else:
                    action_flag = f"NEEDS_ER: {adr_id} (Path: {dirname})"
                    status_flag = "NEEDS_ER"
            else:
                status_flag = "IN_PROGRESS"
                
        if action_flag:
            actions.append(action_flag)
            
        # --- AUTO TAGGING ---
        if status_flag in ["READY_TO_ARCHIVE", "ARCHIVED_OK"] and current_impl_status != "CONSOLIDADA":
            update_implementation_status(filepath, "CONSOLIDADA")
            current_impl_status = "CONSOLIDADA"
        elif status_flag not in ["READY_TO_ARCHIVE", "ARCHIVED_OK"] and current_impl_status == "CONSOLIDADA":
            # If it lost the requirement (e.g., someone unchecked a task)
            update_implementation_status(filepath, "PENDENTE")
            current_impl_status = "PENDENTE"
            
        results.append({
            "id": adr_id,
            "title": title,
            "status": status_flag,
            "impl_status": current_impl_status,
            "archived": is_archived,
            "total_tasks": len(tasks),
            "done_tasks": sum(1 for t in tasks if t["done"])
        })
        
    results.sort(key=lambda x: x["id"])
    
    index_path = os.path.join(repo_path, "docs", "adr", "ADR-INDEX.md")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("# ADR Index\n\n")
        f.write("> Índice gerado automaticamente pelo motor de auditoria da skill `adr-archive`.\n\n")
        f.write("| ADR | Título | Arquivada | Progresso (Tarefas) | Implementação | Janitor Status |\n")
        f.write("|-----|--------|-----------|---------------------|---------------|----------------|\n")
        for r in results:
            arch = "Sim" if r["archived"] else "Não"
            prog = f'{r["done_tasks"]}/{r["total_tasks"]}' if r["total_tasks"] > 0 else "N/A"
            f.write(f'| {r["id"]} | {r["title"]} | {arch} | {prog} | {r["impl_status"]} | {r["status"]} |\n')
            
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(reports_dir, f"adr-archive-report-{timestamp}.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# ADR Archive Janitor Report ({timestamp})\n\n")
        f.write("## 1. Ações Requeridas (Anomalias Detectadas)\n\n")
        if not actions:
            f.write("Nenhuma ação corretiva necessária. Repositório higienizado.\n\n")
        else:
            for act in actions:
                f.write(f"- {act}\n")
        f.write("\n## 2. Débitos Técnicos Consolidados\n\n")
        f.write("> Tarefas pendentes extraídas dos TODOs (desduplicadas por similaridade).\n\n")
        if not debts:
            f.write("Nenhum débito técnico encontrado! 🎉\n")
        else:
            for d in debts:
                f.write(f"{d}\n")
                
    print("--- AUDIT COMPLETED ---")
    print(f"Index updated: {index_path}")
    print(f"Report generated: {report_path}")
    print("--- ACTIONS REQUIRED ---")
    if not actions:
        print("NONE")
    for act in actions:
        print(act)

if __name__ == "__main__":
    main()
