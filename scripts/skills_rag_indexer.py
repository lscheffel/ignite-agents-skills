#!/usr/bin/env python3
"""
SOTA DEDICATED SKILLS RAG INDEXER (WITH STOPWORDS FILTERING)
Ingere e vetoriza 100% dos 80 ativos acionáveis no banco semântico dedicado (data/skills_rag_db/skills_rag.sqlite3).
"""

import os
import re
import sys
import json
import math
import sqlite3
import hashlib
from datetime import datetime, timezone

WORKSPACE_DIR = os.environ.get("SKILLS_WORKSPACE_DIR", os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
GOVERNANCE_DIR = os.path.join(WORKSPACE_DIR, ".github/governance")
DB_DIR = os.path.join(WORKSPACE_DIR, "data/skills_rag_db")
DB_PATH = os.environ.get("SKILLS_DB_PATH", os.path.join(DB_DIR, "skills_rag.sqlite3"))

os.makedirs(DB_DIR, exist_ok=True)

def load_env_cascade():
    candidates = [
        os.path.join(os.getcwd(), ".env"),
        os.path.join(WORKSPACE_DIR, ".env"),
        os.path.expanduser("~/.gemini/.env"),
        os.path.expanduser("~/.config/antigravity/.env")
    ]
    for env_path in candidates:
        if os.path.isfile(env_path):
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#") or "=" not in line:
                            continue
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip("'\"")
                        if k and k not in os.environ:
                            os.environ[k] = v
            except Exception:
                pass

load_env_cascade()

STOPWORDS = {
    "de", "a", "o", "que", "e", "do", "da", "em", "um", "para", "é", "com", "não", "uma", "os", "no", "se", "na",
    "por", "mais", "as", "dos", "como", "mas", "foi", "ao", "ele", "das", "tem", "à", "seu", "sua", "ou", "ser",
    "quando", "muito", "nos", "já", "eu", "também", "só", "pelo", "pela", "até", "isso", "ela", "entre", "era",
    "the", "and", "to", "of", "a", "in", "is", "that", "for", "it", "as", "was", "with", "on", "are", "you",
    "this", "be", "at", "have", "from", "or", "by", "an", "not", "but", "all", "must", "when", "use", "user",
    "whenever", "asks", "needs", "using", "defines", "rules", "section", "tasks", "task"
}

VOCAB_SIZE = 512

def tokenize(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9_\-\s]', ' ', text)
    tokens = [t for t in text.split() if len(t) > 2 and t not in STOPWORDS]
    return tokens

def compute_embedding(text, dim=VOCAB_SIZE):
    tokens = tokenize(text)
    if not tokens:
        return [0.0] * dim
    
    vec = [0.0] * dim
    for token in tokens:
        h1 = int(hashlib.md5(token.encode('utf-8')).hexdigest(), 16) % dim
        h2 = int(hashlib.sha256(token.encode('utf-8')).hexdigest(), 16) % dim
        vec[h1] += 1.0
        vec[h2] += 0.5
        
        if len(token) >= 4:
            for j in range(len(token) - 2):
                gram = token[j:j+3]
                hg = int(hashlib.md5(gram.encode('utf-8')).hexdigest(), 16) % dim
                vec[hg] += 0.35

    norm = math.sqrt(sum(x * x for x in vec))
    if norm > 0:
        vec = [round(x / norm, 5) for x in vec]
    return vec

def cosine_similarity(v1, v2):
    dot = sum(a * b for a, b in zip(v1, v2))
    return max(0.0, min(1.0, dot))

def init_db(conn):
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS skills (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        version TEXT NOT NULL,
        description TEXT NOT NULL,
        triggers_json TEXT NOT NULL,
        tags_json TEXT NOT NULL,
        dim_scores_json TEXT NOT NULL,
        telemetry_json TEXT NOT NULL,
        primary_sha256 TEXT NOT NULL,
        total_tokens INTEGER NOT NULL,
        vector_embedding TEXT NOT NULL,
        vector_embedding_2048 TEXT,
        doc_summary TEXT NOT NULL,
        full_content TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS skill_chunks (
        chunk_id TEXT PRIMARY KEY,
        skill_id TEXT NOT NULL,
        parent_skill_id TEXT NOT NULL DEFAULT '',
        asset_type TEXT NOT NULL DEFAULT 'skill_root',
        file_path TEXT NOT NULL DEFAULT 'SKILL.md',
        section_title TEXT NOT NULL,
        chunk_text TEXT NOT NULL,
        chunk_tokens INTEGER NOT NULL,
        vector_embedding TEXT NOT NULL,
        vector_embedding_2048 TEXT,
        FOREIGN KEY (skill_id) REFERENCES skills(id)
    );
    """)

    cur.execute("PRAGMA table_info(skill_chunks);")
    cols = [r[1] for r in cur.fetchall()]
    if "parent_skill_id" not in cols:
        cur.execute("ALTER TABLE skill_chunks ADD COLUMN parent_skill_id TEXT NOT NULL DEFAULT '';")
    if "asset_type" not in cols:
        cur.execute("ALTER TABLE skill_chunks ADD COLUMN asset_type TEXT NOT NULL DEFAULT 'skill_root';")
    if "file_path" not in cols:
        cur.execute("ALTER TABLE skill_chunks ADD COLUMN file_path TEXT NOT NULL DEFAULT 'SKILL.md';")

    cur.execute("""
    CREATE VIRTUAL TABLE IF NOT EXISTS skills_fts USING fts5(
        skill_id,
        name,
        description,
        triggers,
        content
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS rerank_cache (
        query_hash TEXT PRIMARY KEY,
        query_text TEXT NOT NULL,
        rankings_json TEXT NOT NULL,
        engine_name TEXT NOT NULL,
        hit_count INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()

class AssetParser:
    @staticmethod
    def parse_markdown(content, rel_path, parent_id):
        """
        Divide documentos Markdown por seções de cabeçalho (#, ##, ###).
        Determina asset_type com base no path (references/ -> reference, templates/ -> template, caso contrário -> skill_root).
        """
        asset_type = "skill_root"
        if "references/" in rel_path:
            asset_type = "reference"
        elif "templates/" in rel_path:
            asset_type = "template"

        lines = content.split('\n')
        chunks = []
        current_title = "Overview"
        current_lines = []

        for line in lines:
            if line.startswith('#'):
                if current_lines:
                    text = '\n'.join(current_lines).strip()
                    if len(text) > 5:
                        chunks.append({
                            "section_title": current_title,
                            "chunk_text": text,
                            "asset_type": asset_type,
                            "file_path": rel_path,
                            "parent_skill_id": parent_id
                        })
                    current_lines = []
                current_title = line.lstrip('#').strip()
            else:
                current_lines.append(line)

        if current_lines:
            text = '\n'.join(current_lines).strip()
            if len(text) > 5:
                chunks.append({
                    "section_title": current_title,
                    "chunk_text": text,
                    "asset_type": asset_type,
                    "file_path": rel_path,
                    "parent_skill_id": parent_id
                })

        return chunks

    @staticmethod
    def parse_script(content, rel_path, parent_id):
        """
        Extrai seletivamente docstrings, comentários de cabeçalho e flags USAGE/help.
        Elimina loops, variáveis e código procedural de baixo nível para evitar ruído vetorial.
        """
        lines = content.split('\n')
        docstring_lines = []
        in_docstring = False
        doc_delimiter = None

        comment_header_lines = []
        signatures = []
        usage_lines = []

        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Module Docstring
            if not in_docstring and (stripped.startswith('"""') or stripped.startswith("'''")):
                in_docstring = True
                doc_delimiter = stripped[:3]
                rest = stripped[3:]
                if rest.endswith(doc_delimiter) and len(rest) > 3:
                    docstring_lines.append(rest[:-3])
                    in_docstring = False
                elif rest:
                    docstring_lines.append(rest)
                continue
            elif in_docstring:
                if stripped.endswith(doc_delimiter):
                    docstring_lines.append(stripped[:-3])
                    in_docstring = False
                else:
                    docstring_lines.append(line)
                continue

            # Header comments (early in file)
            if i < 25 and (stripped.startswith('#') or stripped.startswith('//')):
                comment_header_lines.append(stripped.lstrip('#/').strip())

            # Function / Class signatures
            if stripped.startswith('def ') or stripped.startswith('class ') or stripped.startswith('async def '):
                signatures.append(stripped.split(':')[0])

            # USAGE / --help indicators
            if any(term in stripped.lower() for term in ['usage:', 'arguments:', 'example:', '--help', 'options:']):
                usage_lines.append(stripped)

        parts = []
        if docstring_lines:
            parts.append("Module Documentation:\n" + '\n'.join(docstring_lines).strip())
        if comment_header_lines and not docstring_lines:
            parts.append("Header Notes:\n" + '\n'.join(comment_header_lines).strip())
        if usage_lines:
            parts.append("CLI / Usage:\n" + '\n'.join(usage_lines).strip())
        if signatures:
            parts.append("Declared Signatures:\n" + '\n'.join(signatures[:10]))

        if not parts:
            parts.append(f"Script Utility: {os.path.basename(rel_path)} for {parent_id}")

        text = '\n\n'.join(parts)
        return [{
            "section_title": f"Script ({os.path.basename(rel_path)})",
            "chunk_text": text,
            "asset_type": "script_doc",
            "file_path": rel_path,
            "parent_skill_id": parent_id
        }]

    @staticmethod
    def parse_template(content, rel_path, parent_id):
        """
        Extrai cabeçalhos de metadados, schema DDL, esqueleto JSON/YAML.
        """
        lines = content.split('\n')
        comments = []
        structural_lines = []

        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('--') or stripped.startswith('#') or stripped.startswith('//') or stripped.startswith('/*'):
                comments.append(stripped.lstrip('-#/*').strip())
            elif any(kw in stripped.upper() for kw in ['CREATE TABLE', 'ALTER TABLE', 'INTERFACE', 'TYPE', 'SCHEMA', 'MODEL']):
                structural_lines.append(line)
            elif (stripped.startswith('{') or stripped.startswith('}') or ':' in stripped) and len(structural_lines) < 40:
                structural_lines.append(line)

        parts = []
        if comments:
            parts.append("Template Metadata:\n" + '\n'.join(comments[:20]).strip())
        
        if len(content) <= 2500:
            parts.append("Template Body:\n" + content.strip())
        else:
            if structural_lines:
                parts.append("Structure Skeleton:\n" + '\n'.join(structural_lines[:40]))
            parts.append(f"Sample Excerpt:\n{content[:1500]}...")

        text = '\n\n'.join(parts)
        return [{
            "section_title": f"Template ({os.path.basename(rel_path)})",
            "chunk_text": text,
            "asset_type": "template",
            "file_path": rel_path,
            "parent_skill_id": parent_id
        }]

def chunk_markdown(content, max_chunk_tokens=350):
    return AssetParser.parse_markdown(content, "SKILL.md", "")

def build_skills_rag():
    print("="*80)
    print("🚀 SOTA DEDICATED SKILLS RAG - INDEXING & INGESTION PIPELINE (ADR-025)")
    print(f"Target Vector DB: {DB_PATH}")
    print("="*80)
    
    raw_manifest_path = os.path.join(GOVERNANCE_DIR, "raw_manifest.json")
    if not os.path.exists(raw_manifest_path):
        print("❌ Error: raw_manifest.json not found! Please run audit_engine.py first.")
        sys.exit(1)
        
    with open(raw_manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
        
    assets = manifest.get("assets", {})
    print(f"[*] Loaded {len(assets)} assets from forensic manifest.")
    
    conn = sqlite3.connect(DB_PATH)
    init_db(conn)
    cur = conn.cursor()
    
    cur.execute("DELETE FROM skills;")
    cur.execute("DELETE FROM skill_chunks;")
    cur.execute("DELETE FROM skills_fts;")
    cur.execute("DELETE FROM rerank_cache;")
    conn.commit()
    
    total_chunks_indexed = 0
    now_iso = datetime.now(timezone.utc).isoformat()
    
    for idx, (asset_id, asset_data) in enumerate(assets.items(), 1):
        name = asset_data.get("name", asset_id)
        cat = asset_data.get("category", "skill")
        sha = asset_data.get("primary_sha256", "")
        tot_tok = asset_data.get("total_tokens", 0)
        
        skill_doc_dir = os.path.join(GOVERNANCE_DIR, "individual", asset_id)
        audit_report_p = os.path.join(skill_doc_dir, "audit_report.md")
        telemetry_p = os.path.join(skill_doc_dir, "telemetry_spec.json")
        
        audit_content = ""
        if os.path.exists(audit_report_p):
            with open(audit_report_p, 'r', encoding='utf-8') as f:
                audit_content = f.read()
                
        telemetry_data = {}
        if os.path.exists(telemetry_p):
            with open(telemetry_p, 'r', encoding='utf-8') as f:
                telemetry_data = json.load(f)
                
        full_code = ""
        all_chunks = []
        
        for fi in asset_data.get("files", []):
            fp = fi.get("path", "")
            rel = fi.get("relpath", "")
            if rel in ["README.md", "CHANGELOG.md", "USAGE.md", "RELEASE-NOTES.md", "STATE.md", "AGENTS.md", "GEMINI.md", "CONTRIBUTING.md", "DOCUMENTATION_AUDIT_REPORT.md"]:
                continue
            if not os.path.exists(fp):
                continue
                
            try:
                with open(fp, 'r', encoding='utf-8', errors='ignore') as fh:
                    fcontent = fh.read()
                full_code += f"\n\n--- FILE: {rel} ---\n" + fcontent
            except Exception:
                continue

            if rel.endswith('.md'):
                parsed = AssetParser.parse_markdown(fcontent, rel, asset_id)
                all_chunks.extend(parsed)
            elif rel.endswith(('.py', '.sh', '.bash', '.js', '.ts')):
                if 'scripts/' in rel or fp.endswith(('.sh', '.py')):
                    parsed = AssetParser.parse_script(fcontent, rel, asset_id)
                    all_chunks.extend(parsed)
            elif rel.endswith(('.sql', '.json', '.yaml', '.yml', '.j2', '.graphql', '.proto')):
                if 'templates/' in rel or 'references/' in rel:
                    parsed = AssetParser.parse_template(fcontent, rel, asset_id)
                    all_chunks.extend(parsed)
                    
        desc_match = re.search(r'\* \*\*Descrição Funcional:\*\* (.*?)\n', audit_content)
        description = desc_match.group(1).strip() if desc_match else f"Módulo autônomo para {name}"
        
        ver_match = re.search(r'\*\*Versão:\*\* `(.*?)`', audit_content)
        version = ver_match.group(1).strip() if ver_match else "v1.0.0"
        
        triggers = [name, name.replace('-', ' '), name.replace('_', ' ')]
        if "triggers:" in full_code.lower():
            t_match = re.search(r'triggers:\s*\n((?:\s*-\s*[^\n]+\n)+)', full_code, re.I)
            if t_match:
                for line in t_match.group(1).split('\n'):
                    if line.strip().startswith('-'):
                        triggers.append(line.strip().lstrip('-').strip(' "\''))
                        
        triggers = sorted(list(set(triggers)))
        tags = [cat, name.split('-')[0], "sota-skill"]
        
        embedding_text = f"{name} {cat} {description} {' '.join(triggers)} {' '.join(tags)}"
        vec = compute_embedding(embedding_text)
        
        doc_summary = f"{name} ({version}) [{cat}]: {description}. Triggers: {', '.join(triggers[:4])}."
        
        cur.execute("""
        INSERT INTO skills (
            id, name, category, version, description,
            triggers_json, tags_json, dim_scores_json, telemetry_json,
            primary_sha256, total_tokens, vector_embedding,
            doc_summary, full_content, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            asset_id, name, cat, version, description,
            json.dumps(triggers), json.dumps(tags), json.dumps({"global_score": asset_data.get("global_score", 90.0)}),
            json.dumps(telemetry_data), sha, tot_tok, json.dumps(vec),
            doc_summary, full_code[:12000], now_iso
        ))
        
        cur.execute("""
        INSERT INTO skills_fts (skill_id, name, description, triggers, content)
        VALUES (?, ?, ?, ?, ?);
        """, (asset_id, name, description, ' '.join(triggers), full_code[:15000]))
        
        for c_idx, c_info in enumerate(all_chunks):
            sec_title = c_info["section_title"]
            chunk_txt = c_info["chunk_text"]
            a_type = c_info.get("asset_type", "skill_root")
            f_path = c_info.get("file_path", "SKILL.md")
            p_id = c_info.get("parent_skill_id", asset_id)

            c_id = f"{asset_id}__{a_type}_{c_idx}"
            c_tok = len(chunk_txt) // 4
            c_vec = compute_embedding(f"{asset_id} [{a_type}] {sec_title}: {chunk_txt}")
            cur.execute("""
            INSERT INTO skill_chunks (
                chunk_id, skill_id, parent_skill_id, asset_type, file_path,
                section_title, chunk_text, chunk_tokens, vector_embedding
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (c_id, asset_id, p_id, a_type, f_path, sec_title, chunk_txt, c_tok, json.dumps(c_vec)))
            total_chunks_indexed += 1
            
        print(f"  [{idx:02d}/{len(assets):02d}] Ingested: {asset_id} ({len(all_chunks)} hierarchical chunks, {len(triggers)} triggers)")

    conn.commit()
    conn.close()
    
    print("\n" + "="*80)
    print("✅ SOTA SKILLS RAG INGESTION COMPLETE (ADR-025)")
    print(f"Total Skills Ingested: {len(assets)}")
    print(f"Total Chunks Vectorized: {total_chunks_indexed}")
    print(f"Database File: {DB_PATH} ({os.path.getsize(DB_PATH):,} bytes)")
    print("="*80)

if __name__ == "__main__":
    build_skills_rag()
