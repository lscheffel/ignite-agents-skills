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

WORKSPACE_DIR = "/home/loupan/.gemini/config/skills"
DOCS_DIR = os.path.join(WORKSPACE_DIR, "data/docs")
DB_DIR = os.path.join(WORKSPACE_DIR, "data/skills_rag_db")
DB_PATH = os.path.join(DB_DIR, "skills_rag.sqlite3")

os.makedirs(DB_DIR, exist_ok=True)

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
        doc_summary TEXT NOT NULL,
        full_content TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS skill_chunks (
        chunk_id TEXT PRIMARY KEY,
        skill_id TEXT NOT NULL,
        section_title TEXT NOT NULL,
        chunk_text TEXT NOT NULL,
        chunk_tokens INTEGER NOT NULL,
        vector_embedding TEXT NOT NULL,
        FOREIGN KEY (skill_id) REFERENCES skills(id)
    );
    """)

    cur.execute("""
    CREATE VIRTUAL TABLE IF NOT EXISTS skills_fts USING fts5(
        skill_id,
        name,
        description,
        triggers,
        content
    );
    """)
    conn.commit()

def chunk_markdown(content, max_chunk_tokens=350):
    lines = content.split('\n')
    chunks = []
    current_title = "Overview"
    current_lines = []
    
    for line in lines:
        if line.startswith('#'):
            if current_lines:
                text = '\n'.join(current_lines).strip()
                if len(text) > 30:
                    chunks.append((current_title, text))
                current_lines = []
            current_title = line.lstrip('#').strip()
        else:
            current_lines.append(line)
            
    if current_lines:
        text = '\n'.join(current_lines).strip()
        if len(text) > 30:
            chunks.append((current_title, text))
            
    return chunks

def build_skills_rag():
    print("="*80)
    print("🚀 SOTA DEDICATED SKILLS RAG - INDEXING & INGESTION PIPELINE")
    print(f"Target Vector DB: {DB_PATH}")
    print("="*80)
    
    raw_manifest_path = os.path.join(DOCS_DIR, "00_INVENTORY/raw_manifest.json")
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
    conn.commit()
    
    total_chunks_indexed = 0
    now_iso = datetime.now(timezone.utc).isoformat()
    
    for idx, (asset_id, asset_data) in enumerate(assets.items(), 1):
        name = asset_data.get("name", asset_id)
        cat = asset_data.get("category", "skill")
        sha = asset_data.get("primary_sha256", "")
        tot_tok = asset_data.get("total_tokens", 0)
        
        skill_doc_dir = os.path.join(DOCS_DIR, "01_SKILLS_INDIVIDUAL", asset_id)
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
        for fi in asset_data.get("files", []):
            fp = fi.get("path", "")
            if os.path.exists(fp) and (fp.endswith(('.md', '.json', '.py', '.sh', '.js', '.ts'))):
                try:
                    with open(fp, 'r', encoding='utf-8', errors='ignore') as fh:
                        full_code += f"\n\n--- FILE: {fi.get('relpath')} ---\n" + fh.read()
                except:
                    pass
                    
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
        
        chunks = chunk_markdown(full_code)
        for c_idx, (sec_title, chunk_txt) in enumerate(chunks):
            c_id = f"{asset_id}__chunk_{c_idx}"
            c_tok = len(chunk_txt) // 4
            c_vec = compute_embedding(f"{name} {sec_title}: {chunk_txt}")
            cur.execute("""
            INSERT INTO skill_chunks (chunk_id, skill_id, section_title, chunk_text, chunk_tokens, vector_embedding)
            VALUES (?, ?, ?, ?, ?, ?);
            """, (c_id, asset_id, sec_title, chunk_txt, c_tok, json.dumps(c_vec)))
            total_chunks_indexed += 1
            
        print(f"  [{idx:02d}/{len(assets):02d}] Ingested: {asset_id} ({len(chunks)} chunks, {len(triggers)} triggers)")

    conn.commit()
    conn.close()
    
    print("\n" + "="*80)
    print("✅ SOTA SKILLS RAG INGESTION COMPLETE")
    print(f"Total Skills Ingested: {len(assets)}")
    print(f"Total Chunks Vectorized: {total_chunks_indexed}")
    print(f"Database File: {DB_PATH} ({os.path.getsize(DB_PATH):,} bytes)")
    print("="*80)

if __name__ == "__main__":
    build_skills_rag()
