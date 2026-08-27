#!/usr/bin/env python3
"""
SOTA SKILLS RAG - MODEL CONTEXT PROTOCOL (MCP) SERVER
Servidor MCP nativo em Python (JSON-RPC 2.0 Stdio) conectando o banco semântico dedicado de 80 skills.
"""

import os
import re
import sys
import json
import time
import math
import sqlite3
import hashlib
import copy
from typing import Optional, Dict, Any, List

WORKSPACE_DIR = os.environ.get("SKILLS_WORKSPACE_DIR", os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
DEFAULT_DB_PATH = os.path.join(WORKSPACE_DIR, "data/skills_rag_db/skills_rag.sqlite3")
DB_PATH = os.environ.get("SKILLS_DB_PATH", DEFAULT_DB_PATH)

def load_env_cascade():
    """
    Carrega variáveis de ambiente em cascata sem dependências externas:
    1. os.environ existente (processo / shell / mcp_config.json)
    2. CWD/.env (escopo do projeto cliente que executa o MCP/CLI)
    3. WORKSPACE_DIR/.env (/home/loupan/projetosVS/ignite-agents-skills/.env - escopo do repositório MCP)
    4. ~/.gemini/.env ou ~/.config/antigravity/.env (escopo global do usuário)
    """
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
    "whenever", "asks", "needs", "using", "defines", "rules", "section", "tasks", "task", "preciso", "como", "fazer"
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

ACRONYM_EXPANSION_DICT = {
    "rbac": "role based access control permissoes autorizacao permissions authorization matrix",
    "xss": "cross site scripting seguranca sanitizacao frontend vulnerabilities owasp",
    "sqli": "sql injection sanitize parameterized queries database security",
    "csrf": "cross site request forgery tokens session protection",
    "tdd": "test driven development testes unitarios red green refactor unit tests",
    "ddd": "domain driven design entidades agregados bounded context domain events",
    "adr": "architecture decision record decisoes arquiteturais blueprint todo plan",
    "ci/cd": "continuous integration continuous deployment pipeline github actions",
    "cicd": "continuous integration continuous deployment pipeline github actions",
    "sota": "state of the art ultra high quality padroes enterprise",
    "rag": "retrieval augmented generation busca semantica embeddings vetorial",
    "mcp": "model context protocol json-rpc ferramentas tools stdio",
    "api": "application programming interface rest graphql endpoints contracts",
    "orm": "object relational mapping banco migrations database schema",
    "poc": "proof of concept teste de conceito vulnerabilidade exploit verification",
    "ssrf": "server side request forgery network security egress filter",
    "jwt": "json web token authentication session stateless bearer"
}

def expand_acronyms(query):
    q_clean = query.strip()
    words = re.findall(r'[a-zA-Z0-9_\-\/]+', q_clean.lower())
    expansions = []
    for w in words:
        if w in ACRONYM_EXPANSION_DICT:
            expansions.append(ACRONYM_EXPANSION_DICT[w])
    if expansions:
        return f"{q_clean} {' '.join(expansions)}"
    return q_clean

def generate_cache_key(query, candidates):
    candidate_repr = sorted([(c.get('skill_id', c.get('name', '')), c.get('primary_sha256', '')) for c in candidates])
    raw = f"{query.strip().lower()}::{candidate_repr}"
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()

def compute_jaccard_similarity(tokens1, tokens2):
    s1 = set(tokens1)
    s2 = set(tokens2)
    if not s1 or not s2:
        return 0.0
    return len(s1.intersection(s2)) / len(s1.union(s2))

_IN_MEMORY_RERANK_CACHE = {}

def get_cached_rankings(cur, query_hash):
    if query_hash in _IN_MEMORY_RERANK_CACHE:
        entry = _IN_MEMORY_RERANK_CACHE[query_hash]
        entry["hit_count"] = entry.get("hit_count", 1) + 1
        return copy.deepcopy(entry["rankings"]), entry["engine_name"]
    try:
        cur.execute("""
        SELECT rankings_json, engine_name, hit_count FROM rerank_cache WHERE query_hash = ?;
        """, (query_hash,))
        row = cur.fetchone()
        if row:
            rankings_json, engine_name, hit_count = row
            try:
                cur.execute("""
                UPDATE rerank_cache SET hit_count = hit_count + 1, last_accessed = CURRENT_TIMESTAMP WHERE query_hash = ?;
                """, (query_hash,))
            except Exception:
                pass
            rankings = json.loads(rankings_json)
            _IN_MEMORY_RERANK_CACHE[query_hash] = {
                "rankings": rankings,
                "engine_name": engine_name,
                "hit_count": hit_count + 1
            }
            return rankings, engine_name
    except Exception:
        pass
    return None, None

def save_cached_rankings(cur, conn, query_hash, query_text, rankings, engine_name):
    _IN_MEMORY_RERANK_CACHE[query_hash] = {
        "rankings": copy.deepcopy(rankings),
        "engine_name": engine_name,
        "hit_count": 1
    }
    try:
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
        cur.execute("""
        INSERT OR REPLACE INTO rerank_cache (query_hash, query_text, rankings_json, engine_name, hit_count, last_accessed)
        VALUES (?, ?, ?, ?, 1, CURRENT_TIMESTAMP);
        """, (query_hash, query_text, json.dumps(rankings, ensure_ascii=False), engine_name))
        conn.commit()
    except Exception:
        pass

def neural_cross_encoder_rerank(query, candidates, top_k=3, api_key=None, conn=None, cur=None):
    """
    ADR-021/022 Tri-Stage SOTA Neural Reranking:
    - Stage 2: Cross-Encoder via Nvidia nv-rerank-qa-mistral-4b:1
    - Stage 3: Logit Cutoff (logit >= -10.0) + Sigmoid Calibration + Anti-Redundancy Diversity
    - Feature: Persistent SQLite Cache com Chave de Integridade SHA-256
    """
    if not candidates:
        return []
    
    # 1. Verificar Cache Persistente (0ms)
    cache_key = generate_cache_key(query, candidates)
    if cur:
        cached_res, cached_eng = get_cached_rankings(cur, cache_key)
        if cached_res:
            for item in cached_res:
                item["engine"] = f"ADR-022-Cache-Hit (0ms) [{cached_eng}]"
                item["cache_hit"] = True
            return cached_res[:top_k]
    
    key = api_key or os.environ.get("NVIDIA_API_KEY")
    if not key:
        return candidates[:top_k]
        
    try:
        import requests
        passages = []
        for c in candidates:
            txt = f"Skill: {c['name']} ({c['category']}). Description: {c['description']}. Matched Trigger: {c['matched_trigger']}. Summary: {c['doc_summary']}"
            passages.append({"text": txt})
            
        url = "https://ai.api.nvidia.com/v1/retrieval/nvidia/reranking"
        headers = {
            "Authorization": f"Bearer {key}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "nv-rerank-qa-mistral-4b:1",
            "query": {"text": query},
            "passages": passages,
            "truncate": "END"
        }
        
        resp = requests.post(url, json=payload, headers=headers, timeout=4.0)
        if resp.status_code != 200:
            return candidates[:top_k]
            
        data = resp.json()
        rankings = data.get("rankings", [])
        if not rankings:
            return candidates[:top_k]
            
        reranked = []
        for rank in rankings:
            idx = rank.get("index", 0)
            logit = rank.get("logit", -99.0)
            
            # Guardrail 1: Logit Cutoff Gate (Calibrado para cross-lingual)
            if logit < -16.0:
                continue
                
            c = dict(candidates[idx])
            prob = 1.0 / (1.0 + math.exp(-logit / 2.5))
            c["confidence_percent"] = min(99.9, max(15.0, round(prob * 100, 1)))
            c["rerank_logit"] = round(logit, 3)
            c["engine"] = "ADR-021-Neural-Rerank (nv-rerank-qa-mistral-4b:1)"
            c["cache_hit"] = False
            reranked.append(c)
            
        # Guardrail 2: Anti-Redundancy Diversity Filtering (Jaccard > 0.70)
        selected = []
        selected_token_sets = []
        for c in reranked:
            c_toks = set(tokenize(f"{c['name']} {c['description']}"))
            is_redundant = False
            for prev_toks in selected_token_sets:
                sim = compute_jaccard_similarity(c_toks, prev_toks)
                if sim > 0.70:
                    is_redundant = True
                    break
            if not is_redundant:
                selected.append(c)
                selected_token_sets.append(c_toks)
            if len(selected) >= top_k:
                break
                
        final_list = selected if selected else candidates[:top_k]
        
        if cur and conn and final_list:
            save_cached_rankings(cur, conn, cache_key, query, final_list, "nv-rerank-qa-mistral-4b:1")
            
        return final_list
    except Exception:
        return candidates[:top_k]

WORKSPACE_SKILL_CANDIDATE_DIRS = [
    ".gemini/skills",
    ".kilo/skills",
    ".kilocode/skills",
    ".claude/skills",
    ".claude/commands",
    ".cursor/skills",
    ".windsurf/skills",
    ".github/skills",
    ".skills",
    "skills",
    ".agent/skills",
    ".agents/skills"
]

class WorkspaceScopeResolver:
    @staticmethod
    def find_workspace_skills_dir(cwd=None):
        base_dir = os.path.abspath(cwd or os.getcwd())
        global_canonical = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        if base_dir == global_canonical or base_dir == repo_root:
            return None

        for rel_dir in WORKSPACE_SKILL_CANDIDATE_DIRS:
            candidate = os.path.join(base_dir, rel_dir)
            if os.path.isdir(candidate):
                has_skills = False
                for root, _, files in os.walk(candidate):
                    if any(f == 'SKILL.md' or (f.endswith('.md') and root == candidate) for f in files):
                        has_skills = True
                        break
                if has_skills:
                    return os.path.abspath(candidate)
        return None

    @staticmethod
    def ensure_local_rag_index(skills_dir, target_db_path):
        os.makedirs(os.path.dirname(target_db_path), exist_ok=True)
        max_mtime = 0.0
        skill_files = []
        for root, _, files in os.walk(skills_dir):
            for f in files:
                if f == 'SKILL.md' or (f.endswith('.md') and root == skills_dir):
                    fp = os.path.join(root, f)
                    try:
                        m = os.path.getmtime(fp)
                        if m > max_mtime:
                            max_mtime = m
                        skill_files.append(fp)
                    except OSError:
                        pass

        db_exists = os.path.isfile(target_db_path)
        db_mtime = os.path.getmtime(target_db_path) if db_exists else 0.0

        if db_exists and db_mtime >= max_mtime:
            return target_db_path

        conn = sqlite3.connect(target_db_path)
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
            section_title TEXT NOT NULL,
            chunk_text TEXT NOT NULL,
            chunk_tokens INTEGER NOT NULL,
            vector_embedding TEXT NOT NULL,
            vector_embedding_2048 TEXT
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
        
        cur.execute("DELETE FROM skills;")
        cur.execute("DELETE FROM skill_chunks;")
        cur.execute("DELETE FROM skills_fts;")
        cur.execute("DELETE FROM rerank_cache;")

        indexed_skills = {}
        for fp in skill_files:
            try:
                with open(fp, 'r', encoding='utf-8', errors='ignore') as fh:
                    content = fh.read()
            except Exception:
                continue

            name = os.path.basename(os.path.dirname(fp)) if os.path.basename(fp) == "SKILL.md" else os.path.splitext(os.path.basename(fp))[0]
            version = "1.0.0"
            description = f"Local workspace skill for {name}"
            triggers = [name, name.replace('-', ' '), name.replace('_', ' ')]

            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    fm = parts[1]
                    n_match = re.search(r'^name:\s*(.+)$', fm, re.M)
                    if n_match:
                        name = n_match.group(1).strip().strip('"\'')
                    v_match = re.search(r'^version:\s*(.+)$', fm, re.M)
                    if v_match:
                        version = v_match.group(1).strip().strip('"\'')
                    d_match = re.search(r'^description:\s*(.+)$', fm, re.M)
                    if d_match:
                        description = d_match.group(1).strip().strip('"\'')
                    t_match = re.search(r'triggers:\s*\n((?:\s*-\s*[^\n]+\n)+)', fm, re.I)
                    if t_match:
                        for line in t_match.group(1).split('\n'):
                            if line.strip().startswith('-'):
                                triggers.append(line.strip().lstrip('-').strip(' "\''))

            triggers = sorted(list(set(triggers)))
            sha = hashlib.sha256(content.encode('utf-8')).hexdigest()
            vec = compute_embedding(f"{name} {description} {' '.join(triggers)}")
            summary = f"{name} ({version}) [workspace_local]: {description}."

            if name not in indexed_skills:
                indexed_skills[name] = True
                cur.execute("""
                INSERT OR REPLACE INTO skills (
                    id, name, category, version, description, triggers_json, tags_json,
                    dim_scores_json, telemetry_json, primary_sha256, total_tokens,
                    vector_embedding, doc_summary, full_content, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """, (
                    name, name, "workspace_local", version, description,
                    json.dumps(triggers), json.dumps(["workspace_local"]),
                    json.dumps({"global_score": 90.0}),
                    json.dumps({"telemetry_metrics": {"schema_tokens": 200, "estimated_latency_ms": 50, "side_effects": "Workspace Local"}}),
                    sha, len(content) // 4, json.dumps(vec), summary, content[:12000], "2026-08-24"
                ))
                
                cur.execute("""
                INSERT INTO skills_fts (skill_id, name, description, triggers, content)
                VALUES (?, ?, ?, ?, ?);
                """, (name, name, description, ' '.join(triggers), content[:15000]))

                chunks = []
                lines = content.split('\n')
                curr_title = "Overview"
                curr_lines = []
                for line in lines:
                    if line.startswith('#'):
                        if curr_lines:
                            txt = '\n'.join(curr_lines).strip()
                            if len(txt) > 30:
                                chunks.append((curr_title, txt))
                            curr_lines = []
                        curr_title = line.lstrip('#').strip()
                    else:
                        curr_lines.append(line)
                if curr_lines:
                    txt = '\n'.join(curr_lines).strip()
                    if len(txt) > 30:
                        chunks.append((curr_title, txt))

                for c_idx, (sec_t, c_txt) in enumerate(chunks):
                    c_id = f"{name}__chunk_{c_idx}"
                    c_vec = compute_embedding(f"{name} {sec_t}: {c_txt}")
                    cur.execute("""
                    INSERT INTO skill_chunks (chunk_id, skill_id, section_title, chunk_text, chunk_tokens, vector_embedding)
                    VALUES (?, ?, ?, ?, ?, ?);
                    """, (c_id, name, sec_t, c_txt, len(c_txt) // 4, json.dumps(c_vec)))

        conn.commit()
        conn.close()
        return target_db_path

    @classmethod
    def resolve_and_ensure_local_db(cls, cwd=None):
        base_dir = os.path.abspath(cwd or os.getcwd())
        env_override = os.environ.get("SKILLS_LOCAL_DB_PATH") or os.environ.get("WORKSPACE_ROOT")
        if env_override:
            if os.path.isfile(env_override) and env_override.endswith(".sqlite3"):
                return env_override
            candidate_p = os.path.join(env_override, ".local/skills_rag/skills_rag.sqlite3")
            if os.path.isfile(candidate_p):
                return candidate_p
            candidate_legacy = os.path.join(env_override, ".gemini/skills_rag.sqlite3")
            if os.path.isfile(candidate_legacy):
                return candidate_legacy

        skills_dir = cls.find_workspace_skills_dir(base_dir)
        if skills_dir:
            target_db = os.path.join(base_dir, ".local", "skills_rag", "skills_rag.sqlite3")
            return cls.ensure_local_rag_index(skills_dir, target_db)
            
        direct_db = os.path.join(base_dir, ".local", "skills_rag", "skills_rag.sqlite3")
        if os.path.isfile(direct_db):
            return direct_db
            
        direct_legacy = os.path.join(base_dir, ".gemini", "skills_rag.sqlite3")
        if os.path.isfile(direct_legacy):
            return direct_legacy
            
        return None

class RAGTelemetryTracker:
    def __init__(self):
        self.start_time = time.time()
        self.total_queries = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.neural_calls = 0
        self.fallback_calls = 0
        self.latencies_ms = []
        self.scope_counts = {"global": 0, "workspace_local": 0}

    def record_query(self, latency_ms, cache_hit=False, neural_call=False, fallback_call=False, scope="global"):
        self.total_queries += 1
        if cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1
        if neural_call:
            self.neural_calls += 1
        if fallback_call:
            self.fallback_calls += 1
        if latency_ms is not None:
            self.latencies_ms.append(float(latency_ms))
            if len(self.latencies_ms) > 1000:
                self.latencies_ms = self.latencies_ms[-1000:]
        if scope in self.scope_counts:
            self.scope_counts[scope] += 1
        else:
            self.scope_counts[scope] = 1

    def get_telemetry(self):
        now = time.time()
        uptime = round(now - self.start_time, 2)
        avg_lat = round(sum(self.latencies_ms) / len(self.latencies_ms), 2) if self.latencies_ms else 0.0
        hit_ratio = round((self.cache_hits / self.total_queries) * 100, 1) if self.total_queries > 0 else 0.0
        return {
            "uptime_seconds": uptime,
            "total_queries": self.total_queries,
            "cache_hit_ratio_percent": hit_ratio,
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "neural_calls": self.neural_calls,
            "fallback_calls": self.fallback_calls,
            "average_latency_ms": avg_lat,
            "scope_distribution": dict(self.scope_counts),
            "nvidia_api_configured": bool(os.environ.get("NVIDIA_API_KEY"))
        }

DAMPING_FACTORS = {
    "skill_root": 1.00,
    "reference": 0.85,
    "template": 0.80,
    "script_doc": 0.75
}

class SkillsDatabase:
    def __init__(self, db_path=DB_PATH, global_db_path=None, local_db_path=None, cwd=None):
        self.telemetry = RAGTelemetryTracker()
        target_global = global_db_path or db_path
        self.global_db_path = target_global
        self.global_conn = None
        self.global_cur = None
        
        if os.path.exists(target_global):
            self.global_conn = sqlite3.connect(target_global, check_same_thread=False)
            self.global_cur = self.global_conn.cursor()
            try:
                self.global_cur.execute("PRAGMA query_only = ON;")
            except Exception:
                pass
            self._ensure_schema(self.global_conn, self.global_cur)

        # Local Workspace Database
        self.local_db_path = local_db_path or WorkspaceScopeResolver.resolve_and_ensure_local_db(cwd)
        self.local_conn = None
        self.local_cur = None
        if self.local_db_path and os.path.exists(self.local_db_path) and os.path.abspath(self.local_db_path) != os.path.abspath(target_global):
            self.local_conn = sqlite3.connect(self.local_db_path, check_same_thread=False)
            self.local_cur = self.local_conn.cursor()
            self._ensure_schema(self.local_conn, self.local_cur)

        self.conn = self.global_conn
        self.cur = self.global_cur

    def _ensure_schema(self, conn, cur):
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

    def format_chunk_xml(self, skill_id, parent_skill_id, asset_type, file_path, confidence, section_title, content):
        """Formata chunk XML enriquecido tipado (ADR-025)"""
        return f'<active_skill id="{skill_id}" parent="{parent_skill_id}" type="{asset_type}" path="{file_path}" confidence="{confidence}%">\n  <focused_chunk section="{section_title}">\n{content}\n  </focused_chunk>\n</active_skill>'

    def get_best_matching_chunk(self, skill_id, query_vec, query_text=""):
        curs = [self.local_cur, self.global_cur]
        for cur in curs:
            if not cur:
                continue
            try:
                try:
                    cur.execute("""
                    SELECT section_title, chunk_text, vector_embedding, parent_skill_id, asset_type, file_path 
                    FROM skill_chunks WHERE skill_id = ? OR parent_skill_id = ?;
                    """, (skill_id, skill_id))
                    rows = cur.fetchall()
                except Exception:
                    cur.execute("""
                    SELECT section_title, chunk_text, vector_embedding, '', 'skill_root', 'SKILL.md'
                    FROM skill_chunks WHERE skill_id = ?;
                    """, (skill_id,))
                    rows = cur.fetchall()

                if not rows:
                    continue
                    
                best_chunk = None
                max_sim = -1.0
                for sec_title, c_text, cvec_json, p_id, a_type, f_path in rows:
                    cvec = json.loads(cvec_json)
                    sim = cosine_similarity(query_vec, cvec)
                    damping = DAMPING_FACTORS.get(a_type, 1.0)
                    weighted_sim = sim * damping
                    if weighted_sim > max_sim:
                        max_sim = weighted_sim
                        best_chunk = {
                            "section_title": sec_title,
                            "chunk_text": c_text[:1200],
                            "similarity": round(sim, 3),
                            "weighted_similarity": round(weighted_sim, 3),
                            "parent_skill_id": p_id or skill_id,
                            "asset_type": a_type,
                            "file_path": f_path
                        }
                if best_chunk:
                    return best_chunk
            except Exception:
                pass
        return None

    def _search_single_db(self, conn, cur, query, expanded_query, query_vec, q_tokens, q_lower, scope_name, category=None):
        if not cur:
            return []
        cur.execute("""
        SELECT id, name, category, version, description, triggers_json, telemetry_json,
               primary_sha256, vector_embedding, doc_summary FROM skills;
        """)
        rows = cur.fetchall()
        
        fts_matches = {}
        if q_tokens:
            literal_tokens = tokenize(query)
            fts_parts = [f'"{t}"*' for t in literal_tokens if len(t) > 2]
            for t in q_tokens:
                if len(t) > 2 and t not in literal_tokens:
                    fts_parts.append(f'"{t}"*')
            if fts_parts:
                fts_q = ' OR '.join(fts_parts)
                try:
                    cur.execute("SELECT skill_id, rank FROM skills_fts WHERE skills_fts MATCH ? ORDER BY rank LIMIT 40;", (fts_q,))
                    for sid, r in cur.fetchall():
                        fts_matches[sid] = min(1.0, max(0.1, abs(r) / 5.0))
                except:
                    pass

        chunk_dense_max = {}
        try:
            cur.execute("SELECT skill_id, vector_embedding FROM skill_chunks;")
            for sid, cvec_json in cur.fetchall():
                cvec = json.loads(cvec_json)
                sim = cosine_similarity(query_vec, cvec)
                if sim > chunk_dense_max.get(sid, 0.0):
                    chunk_dense_max[sid] = sim
        except Exception:
            pass

        candidates = []
        for r in rows:
            sid, name, cat, ver, desc, trig_json, telem_json, sha256, vec_json, summary = r
            if category and cat != category:
                continue
                
            skill_vec = json.loads(vec_json)
            triggers = json.loads(trig_json)
            telem = json.loads(telem_json) if telem_json else {}
            
            global_dense_sim = cosine_similarity(query_vec, skill_vec)
            chunk_sim = chunk_dense_max.get(sid, 0.0)
            dense_score = (0.70 * global_dense_sim) + (0.30 * chunk_sim)
            sparse_score = fts_matches.get(sid, 0.0)
            
            trigger_score = 0.0
            matched_trigger = None
            clean_name = name.replace('-', ' ').replace('_', ' ')
            if clean_name in q_lower or name in q_lower:
                trigger_score = 1.0
                matched_trigger = name
            else:
                for t in triggers:
                    t_clean = t.lower().replace('-', ' ').replace('_', ' ')
                    if t_clean in q_lower or t.lower() in q_lower:
                        trigger_score = max(trigger_score, 0.95)
                        matched_trigger = t
                        break
                    elif any(tok == t_clean for tok in q_tokens if len(tok) > 3):
                        trigger_score = max(trigger_score, 0.70)
                        matched_trigger = t

            if trigger_score > 0.8:
                final_score = (0.40 * trigger_score) + (0.35 * sparse_score) + (0.25 * dense_score)
            elif sparse_score > 0.5:
                final_score = (0.45 * sparse_score) + (0.35 * dense_score) + (0.20 * trigger_score)
            else:
                final_score = (0.55 * dense_score) + (0.35 * sparse_score) + (0.10 * trigger_score)
                
            confidence = min(99.9, round(final_score * 100, 1))
            if scope_name == "workspace_local":
                confidence = min(99.9, round(confidence * 1.05, 1))

            telem_metrics = telem.get("telemetry_metrics", {})
            candidates.append({
                "skill_id": sid,
                "name": name,
                "category": cat,
                "version": ver,
                "scope": scope_name,
                "primary_sha256": sha256,
                "confidence_percent": confidence,
                "matched_trigger": matched_trigger or (triggers[0] if triggers else name),
                "description": desc,
                "telemetry": {
                    "schema_tokens": telem_metrics.get("schema_tokens", 250),
                    "latency_ms": telem_metrics.get("estimated_latency_ms", 120),
                    "side_effects": telem_metrics.get("side_effects", "Read-Only")
                },
                "doc_summary": summary,
                "engine": "Stage-1-Hybrid-Local (SQLite3/FTS5)"
            })
        return candidates

    def search_skills(self, query, top_k=3, category=None, use_neural=True):
        start_t = time.time()
        api_key = os.environ.get("NVIDIA_API_KEY")
        expanded_query = expand_acronyms(query)
        query_vec = compute_embedding(query)
        q_tokens = tokenize(expanded_query)
        q_lower = query.lower()
        
        global_candidates = self._search_single_db(
            self.global_conn, self.global_cur, query, expanded_query,
            query_vec, q_tokens, q_lower, "global", category
        )
        local_candidates = self._search_single_db(
            self.local_conn, self.local_cur, query, expanded_query,
            query_vec, q_tokens, q_lower, "workspace_local", category
        )

        candidates_map = {}
        for c in global_candidates:
            candidates_map[c["skill_id"]] = c
        for c in local_candidates:
            candidates_map[c["skill_id"]] = c # Shadowing

        merged_candidates = list(candidates_map.values())
        merged_candidates.sort(key=lambda x: x["confidence_percent"], reverse=True)
        
        is_neural = False
        is_fallback = False
        is_cache = False
        
        if use_neural:
            candidate_pool = merged_candidates[:max(top_k * 5, 15)]
            active_cur = self.local_cur or self.global_cur
            active_conn = self.local_conn or self.global_conn
            final_results = neural_cross_encoder_rerank(
                query, candidate_pool, top_k=top_k,
                api_key=api_key, conn=active_conn, cur=active_cur
            )
            if final_results and final_results[0].get("cache_hit"):
                is_cache = True
            elif final_results and any(t in final_results[0].get("engine", "") for t in ["Neural-Rerank", "Cross-Encoder", "nv-rerank"]):
                is_neural = True
            else:
                is_fallback = True
            res = final_results
        else:
            res = merged_candidates[:top_k]
            
        elapsed_ms = (time.time() - start_t) * 1000
        top_scope = res[0].get("scope", "global") if res else "global"
        self.telemetry.record_query(
            latency_ms=elapsed_ms,
            cache_hit=is_cache,
            neural_call=is_neural,
            fallback_call=is_fallback,
            scope=top_scope
        )
        return res

    def get_skill_details(self, skill_id):
        curs = [self.local_cur, self.global_cur]
        for cur in curs:
            if not cur:
                continue
            cur.execute("""
            SELECT id, name, category, version, description, triggers_json, tags_json,
                   dim_scores_json, telemetry_json, primary_sha256, total_tokens, doc_summary, full_content
            FROM skills WHERE id = ? OR name = ?;
            """, (skill_id, skill_id))
            row = cur.fetchone()
            if row:
                sid, name, cat, ver, desc, trig_json, tags_json, dim_json, telem_json, sha, tot_tok, summary, content = row
                return {
                    "id": sid,
                    "name": name,
                    "category": cat,
                    "version": ver,
                    "description": desc,
                    "triggers": json.loads(trig_json),
                    "tags": json.loads(tags_json),
                    "governance_score": json.loads(dim_json),
                    "telemetry": json.loads(telem_json) if telem_json else {},
                    "sha256": sha,
                    "total_tokens": tot_tok,
                    "doc_summary": summary,
                    "full_content_preview": content[:2500]
                }
        return {"error": f"Skill '{skill_id}' not found in database."}

    def list_all_skills(self, category_filter=None):
        skills_map = {}
        for cur in [self.global_cur, self.local_cur]:
            if not cur:
                continue
            query = "SELECT id, name, category, version, description, dim_scores_json FROM skills"
            params = ()
            if category_filter:
                query += " WHERE category = ?"
                params = (category_filter,)
            query += " ORDER BY name ASC;"
            
            cur.execute(query, params)
            rows = cur.fetchall()
            for sid, name, cat, ver, desc, dim_json in rows:
                score_data = json.loads(dim_json) if dim_json else {}
                skills_map[sid] = {
                    "id": sid,
                    "name": name,
                    "category": cat,
                    "version": ver,
                    "global_score": score_data.get("global_score", 90.0),
                    "description": desc
                }
        all_skills = list(skills_map.values())
        return {"total_count": len(all_skills), "skills": all_skills}

    def route_task(self, task_description, top_k=2):
        top_skills = self.search_skills(task_description, top_k=top_k)
        if not top_skills:
            return {"status": "no_match", "message": "No matching skills found."}
            
        best = top_skills[0]
        q_vec = compute_embedding(task_description)
        best_chunk = self.get_best_matching_chunk(best["skill_id"], q_vec, task_description)
        
        focused_xml = ""
        if best_chunk and best_chunk.get("section_title"):
            focused_xml = f"""
  <focused_chunk section="{best_chunk['section_title']}">
{best_chunk['chunk_text']}
  </focused_chunk>"""

        scope_val = best.get("scope", "global")
        parent_val = best_chunk.get("parent_skill_id", best["skill_id"]) if best_chunk else best["skill_id"]
        type_val = best_chunk.get("asset_type", "skill_root") if best_chunk else "skill_root"
        path_val = best_chunk.get("file_path", "SKILL.md") if best_chunk else "SKILL.md"

        xml_prompt_injection = f"""<!-- DYNAMIC SKILL INJECTION VIA MCP ROUTER (ADR-025 HIERARCHICAL): {best['name']} ({best['version']}) -->
<active_skill id="{best['skill_id']}" parent="{parent_val}" type="{type_val}" path="{path_val}" category="{best['category']}" scope="{scope_val}">
  <summary>{best['doc_summary']}</summary>
  <description>{best['description']}</description>
  <side_effects>{best['telemetry']['side_effects']}</side_effects>
  <trigger_reason>{best['matched_trigger']}</trigger_reason>{focused_xml}
</active_skill>"""

        tokens_saved = max(0, best['telemetry']['schema_tokens'] - 120)
        return {
            "primary_skill": best,
            "candidate_skills": top_skills,
            "prompt_injection_xml": xml_prompt_injection,
            "estimated_overhead_tokens": 140,
            "estimated_tokens_saved": tokens_saved,
            "cache_hit": best.get("cache_hit", False),
            "scope": scope_val
        }

    def bootstrap_agent_instructions(self, workspace_path=None):
        target_ws = os.path.abspath(workspace_path or os.getcwd())
        agents_path = os.path.join(target_ws, "AGENTS.md")
        gemini_path = os.path.join(target_ws, "GEMINI.md")

        orchestration_block = """## PROTOCOLO DE ORQUESTRAÇÃO DE SKILLS (MCP DYNAMIC RAG)

Você tem acesso às ferramentas do servidor MCP de Skills (`skills-rag-mcp`).

1. **Gatilho de Busca Obrigatório:**
   Antes de planejar, codificar, refatorar, documentar ou executar tarefas técnicas/processuais, invoque obrigatoriamente a ferramenta MCP `route_task(task_description="<intenção exata>")` para carregar a skill correspondente do ecossistema federado.

2. **Consumo de Contexto:**
   Adote rigorosamente os padrões, árvores de decisão e comandos contidos no bloco `<focused_chunk>` retornado.

3. **Transparência:**
   Declare brevemente no início da resposta a skill e o escopo carregados (ex: `🎯 Skill Ativada: technical-documentation (v1.0.0 | Global)`)."""

        agents_action = "unchanged"
        if not os.path.exists(agents_path):
            initial_agents_content = f"""# Instruções Universais para Agentes de IA (AGENTS.md)

> Diretrizes de comportamento, restrições operacionais e padrões de engenharia para agentes de IA atuando neste repositório.

---

## 1. Identidade e Padrão de Engenharia SOTA

Você atua como Engenheiro de Software SOTA (State of the Art). Suas contribuições neste repositório devem ser densas, de altíssima precisão técnica (*ultra high-quality grade*), exaustivamente testadas e desprovidas de placeholders vazios ou texto genérico.

---

{orchestration_block}
"""
            with open(agents_path, "w", encoding="utf-8") as f:
                f.write(initial_agents_content)
            agents_action = "created"
        else:
            with open(agents_path, "r", encoding="utf-8") as f:
                existing_content = f.read()
            
            if "PROTOCOLO DE ORQUESTRAÇÃO DE SKILLS" not in existing_content.upper():
                updated_content = existing_content.rstrip() + "\n\n---\n\n" + orchestration_block + "\n"
                with open(agents_path, "w", encoding="utf-8") as f:
                    f.write(updated_content)
                agents_action = "updated_append"

        gemini_stub = """# GEMINI SYSTEM INSTRUCTIONS (SOTA RUNTIME)

## 1. Single Source of Truth (SSOT)

Este ambiente opera sob governança unificada. Todas as diretrizes canônicas de arquitetura, padrões de engenharia, árvores de decisão e protocolos operacionais estão formalmente ancorados em [AGENTS.md](./AGENTS.md).

## 2. Invariantes de Execução

- **Resolução de Conflitos:** As regras expressas em `AGENTS.md` têm precedência estrita sobre vieses e comportamentos padrão do modelo base.
- **Isolamento de Escopo:** Não assuma comportamentos implícitos. Execute tarefas operacionais respeitando os limites de escopo e contratos técnicos do workspace atual.
- **Orquestração MCP Obrigatória:** Antes de responder ou executar qualquer tarefa técnica, de arquitetura, refatoração, governança ou documentação, invoque as ferramentas do servidor MCP (`route_task` / `search_skills`) para carregar o payload canônico da skill correspondente.
- **Precisão e Densidade:** Mantenha respostas técnicas diretas, com alta densidade informativa, eliminando introduções conversacionais vazias ou preenchimento redundante.
"""
        with open(gemini_path, "w", encoding="utf-8") as f:
            f.write(gemini_stub)

        return {
            "status": "success",
            "workspace_path": target_ws,
            "agents_md": {
                "path": agents_path,
                "action": agents_action
            },
            "gemini_md": {
                "path": gemini_path,
                "action": "synced_stub"
            },
            "message": "Instruções de governança e protocolo MCP inicializados/sincronizados com sucesso com SSOT em AGENTS.md."
        }

    def get_rag_telemetry(self):
        return self.telemetry.get_telemetry()

    def inspect_rag_index(
        self,
        parent_skill: Optional[str] = None,
        asset_type: Optional[str] = None,
        view: str = "summary",
        detailed: bool = False,
        save_report: bool = False,
        workspace_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Inspeciona o inventário completo da base de conhecimento RAG (chunks, sub-ativos e tipos de ativos: skill_root, reference, template, script_doc).

        Regras de negócio:
        - view="summary" (padrão): retorna métricas de distribuição (chunks totais, contagem por tipo).
        - view="items": retorna listas nominais agrupadas por asset_type com contagem de chunks e soma de tokens.
        - view="chunks": retorna inventário detalhado de todos os chunks (compatibilidade com detailed=True).
        - Se detailed=True e view="summary", é promovido automaticamente para view="chunks" (retrocompatibilidade).

        Args:
            parent_skill: Filtrar por ID específico de uma skill-mãe (ex: 'database-architecture').
            asset_type: Filtrar por tipo ('skill_root', 'reference', 'template', 'script_doc').
            view: Modo de visualização ("summary" | "items" | "chunks"). Padrão: "summary".
            detailed: Se True e view="chunks", retorna lista granular de seções e caminhos. Padrão: False.
                       Se True e view="summary", é promovido para view="chunks" automaticamente.
            save_report: Se True, persiste relatórios em .local/skills_rag/reports/. Padrão: False.
            workspace_path: Caminho raiz do workspace. Padrão: usa SKILLS_WORKSPACE_DIR ou diretório pai.
        """
        # Retrocompatibilidade: se detailed=True e view="summary", promove para view="chunks"
        if detailed and view == "summary":
            view = "chunks"

        sources = []
        if self.global_cur:
            sources.append((self.global_cur, "global"))
        if self.local_cur and self.local_cur != self.global_cur:
            sources.append((self.local_cur, "workspace_local"))

        # Determinar caminho do workspace para salvamento de relatórios
        if workspace_path is None:
            workspace_path = os.environ.get(
                "SKILLS_WORKSPACE_DIR",
                os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
            )
        report_dir = os.path.join(workspace_path, ".local", "skills_rag", "reports")

        # Dados brutos coletados de todas as fontes (global + local)
        all_rows = []
        for cur, scope in sources:
            try:
                cur.execute("""
                SELECT chunk_id, skill_id, parent_skill_id, asset_type, file_path, section_title, chunk_tokens
                FROM skill_chunks;
                """)
                rows = cur.fetchall()
                for row in rows:
                    all_rows.append(row)
            except Exception:
                pass

        # Aplicar filtros de parent_skill e asset_type
        filtered_rows = all_rows
        if parent_skill:
            filtered_rows = [r for r in filtered_rows if r[2] == parent_skill or r[1] == parent_skill]
        if asset_type:
            filtered_rows = [r for r in filtered_rows if r[3] == asset_type]

        if view == "items":
            # Modo itens: agrupar por asset_type, parent_skill_id, file_path
            # SQL: SELECT asset_type, parent_skill_id, COALESCE(file_path, 'SKILL.md') AS file_path,
            #       COUNT(*) AS chunk_count, SUM(chunk_tokens) AS total_tokens
            # FROM skill_chunks
            # WHERE (:parent_skill IS NULL OR parent_skill_id = :parent_skill)
            #   AND (:asset_type IS NULL OR asset_type = :asset_type)
            # GROUP BY asset_type, parent_skill_id, COALESCE(file_path, 'SKILL.md')
            # ORDER BY asset_type, parent_skill_id, file_path;

            asset_groups: Dict[str, List[Dict[str, Any]]] = {}
            for c_id, s_id, p_id, a_type, f_path, sec_title, c_tokens in filtered_rows:
                curr_type = a_type if a_type else "skill_root"
                curr_path = f_path if f_path else "SKILL.md"
                parent_id = p_id if p_id else s_id

                if curr_type not in asset_groups:
                    asset_groups[curr_type] = []
                asset_groups[curr_type].append({
                    "parent_skill_id": parent_id,
                    "file_path": curr_path,
                    "chunk_count": 1,
                    "total_tokens": c_tokens or 0,
                })

            # Agregar: somar chunks e tokens por (asset_type, parent_skill_id, file_path)
            aggregated: List[Dict[str, Any]] = []
            seen_keys: set = set()
            for curr_type in sorted(asset_groups.keys()):
                for entry in asset_groups[curr_type]:
                    key = (curr_type, entry["parent_skill_id"], entry["file_path"])
                    if key in seen_keys:
                        # Já existe este grupo, incrementar
                        for agg in aggregated:
                            if (agg["asset_type"], agg["parent_skill_id"], agg["file_path"]) == key:
                                agg["chunk_count"] += entry["chunk_count"]
                                agg["total_tokens"] += entry["total_tokens"]
                                break
                    else:
                        seen_keys.add(key)
                        aggregated.append({
                            "asset_type": curr_type,
                            "parent_skill_id": entry["parent_skill_id"],
                            "file_path": entry["file_path"],
                            "chunk_count": entry["chunk_count"],
                            "total_tokens": entry["total_tokens"],
                        })

            # Estruturar retorno agrupado por asset_type
            result_by_type: Dict[str, List[Dict[str, Any]]] = {}
            for atype in sorted(aggregated_key := [a["asset_type"] for a in aggregated] if aggregated else []):
                pass

            # Build structured by asset_type
            structured_by_type: Dict[str, List[Dict[str, Any]]] = {}
            for item in aggregated:
                atype = item["asset_type"]
                if atype not in structured_by_type:
                    structured_by_type[atype] = []
                structured_by_type[atype].append({
                    "parent_skill_id": item["parent_skill_id"],
                    "file_path": item["file_path"],
                    "chunk_count": item["chunk_count"],
                    "total_tokens": item["total_tokens"],
                })

            # Contadores totais
            total_chunks = sum(item["chunk_count"] for item in aggregated)
            unique_skills_count = len(set(r[1] for r in filtered_rows)) if filtered_rows else 0

            res = {
                "status": "success",
                "view": "items",
                "total_chunks": total_chunks,
                "unique_skills_count": unique_skills_count,
                "assets_by_type": structured_by_type,
                "filters_applied": {
                    "parent_skill": parent_skill,
                    "asset_type": asset_type,
                    "view": "items",
                }
            }

            # Adicionar detalhes de parent skill se filtrado
            if parent_skill:
                res["parent_skill_details"] = {
                    "parent_skill_id": parent_skill,
                    "total_chunks": total_chunks,
                    "assets": structured_by_type,
                }

            # Persistir relatório se solicitado
            if save_report:
                try:
                    os.makedirs(report_dir, exist_ok=True)

                    # JSON report
                    json_report = {
                        "status": "success",
                        "view": "items",
                        "total_chunks": total_chunks,
                        "unique_skills_count": unique_skills_count,
                        "assets_by_type": structured_by_type,
                        "filters_applied": {
                            "parent_skill": parent_skill,
                            "asset_type": asset_type,
                            "view": "items",
                        }
                    }
                    json_path = os.path.join(report_dir, "latest_rag_inventory.json")
                    with open(json_path, "w", encoding="utf-8") as jf:
                        json.dump(json_report, jf, indent=2, ensure_ascii=False)

                    # Markdown report
                    md_lines = [
                        "# 📊 Inventário RAG - Modo Itens (ADR-025)",
                        "",
                        f"**Total de chunks:** {total_chunks}",
                        f"**Únicas skills:** {unique_skills_count}",
                        "",
                        "## Ativos por Tipo",
                        "",
                    ]
                    for atype in sorted(structured_by_type.keys()):
                        md_lines.append(f"### {atype.replace('_', ' ').title()}")
                        md_lines.append("")
                        table_header = "| Pai | Arquivo | Chunks | Tokens Totais |"
                        table_sep = "|---|---|---|---|"
                        md_lines.append(table_header)
                        md_lines.append(table_sep)
                        for asset in structured_by_type[atype]:
                            md_lines.append(
                                f"| {asset['parent_skill_id'] or 'ROOT'} | "
                                f"{asset['file_path']} | "
                                f"{asset['chunk_count']} | "
                                f"{asset['total_tokens']} |"
                            )
                        md_lines.append("")

                    md_path = os.path.join(report_dir, "latest_rag_inventory.md")
                    with open(md_path, "w", encoding="utf-8") as mf:
                        mf.write("\n".join(md_lines))

                    res["saved_reports"] = {
                        "json": ".local/skills_rag/reports/latest_rag_inventory.json",
                        "markdown": ".local/skills_rag/reports/latest_rag_inventory.md",
                    }
                except Exception:
                    pass

            return res

        elif view == "chunks":
            # Modo chunks: inventário detalhado (compatibilidade com detailed=True)
            total_chunks = 0
            asset_type_counts = {}
            asset_type_unique_skills = {}
            matched_parent_skills = set()
            matched_files = set()
            detailed_inventory = []

            for c_id, s_id, p_id, a_type, f_path, sec_title, c_tokens in filtered_rows:
                parent_id = p_id if p_id else s_id
                curr_type = a_type if a_type else "skill_root"
                curr_path = f_path if f_path else "SKILL.md"

                if parent_skill and (parent_id != parent_skill and s_id != parent_skill):
                    continue
                if asset_type and curr_type != asset_type:
                    continue

                total_chunks += 1
                matched_parent_skills.add(parent_id)
                matched_files.add(curr_path)

                if curr_type not in asset_type_counts:
                    asset_type_counts[curr_type] = 0
                    asset_type_unique_skills[curr_type] = set()
                asset_type_counts[curr_type] += 1
                asset_type_unique_skills[curr_type].add(parent_id)

                if detailed:
                    detailed_inventory.append({
                        "chunk_id": c_id,
                        "parent_skill_id": parent_id,
                        "skill_id": s_id,
                        "asset_type": curr_type,
                        "file_path": curr_path,
                        "section_title": sec_title,
                        "section": sec_title,
                        "chunk_tokens": c_tokens,
                        "scope": "global"  # simplified
                    })

            distribution = {}
            for atype, count in sorted(asset_type_counts.items()):
                distribution[atype] = {
                    "chunks": count,
                    "unique_skills": len(asset_type_unique_skills.get(atype, set()))
                }

            res = {
                "status": "success",
                "view": "chunks",
                "total_chunks": total_chunks,
                "distribution_by_asset_type": distribution,
                "unique_parent_skills_count": len(matched_parent_skills),
                "filters_applied": {
                    "parent_skill": parent_skill,
                    "asset_type": asset_type,
                    "detailed": detailed,
                    "view": "chunks",
                }
            }

            if parent_skill:
                res["parent_skill_details"] = {
                    "parent_skill_id": parent_skill,
                    "total_chunks": total_chunks,
                    "asset_types_present": list(distribution.keys()),
                    "indexed_files": sorted(list(matched_files))
                }

            if detailed:
                res["artifacts_inventory"] = detailed_inventory
                res["detailed_inventory"] = detailed_inventory

            # Persistir relatório se solicitado
            if save_report:
                try:
                    os.makedirs(report_dir, exist_ok=True)

                    # JSON report
                    json_report = {
                        "status": "success",
                        "view": "chunks",
                        "total_chunks": total_chunks,
                        "distribution_by_asset_type": distribution,
                        "filters_applied": {
                            "parent_skill": parent_skill,
                            "asset_type": asset_type,
                            "detailed": detailed,
                            "view": "chunks",
                        }
                    }
                    json_path = os.path.join(report_dir, "latest_rag_inventory.json")
                    with open(json_path, "w", encoding="utf-8") as jf:
                        json.dump(json_report, jf, indent=2, ensure_ascii=False)

                    # Markdown report
                    md_lines = [
                        "# 📊 Inventário RAG - Modo Chunks (ADR-025)",
                        "",
                        f"**Total de chunks:** {total_chunks}",
                        "",
                        "## Distribuição por Tipo de Ativo",
                        "",
                    ]
                    for atype in sorted(distribution.keys()):
                        md_lines.append(f"### {atype.replace('_', ' ').title()}")
                        md_lines.append("")
                        table_header = "| Tipo | Chunks | Únicas Skills |"
                        table_sep = "|---|---|---|"
                        md_lines.append(table_header)
                        md_lines.append(table_sep)
                        md_lines.append(f"| {atype.replace('_', ' ').title()} | {distribution[atype]['chunks']} | {distribution[atype]['unique_skills']} |")
                        md_lines.append("")

                    md_path = os.path.join(report_dir, "latest_rag_inventory.md")
                    with open(md_path, "w", encoding="utf-8") as mf:
                        mf.write("\n".join(md_lines))

                    res["saved_reports"] = {
                        "json": ".local/skills_rag/reports/latest_rag_inventory.json",
                        "markdown": ".local/skills_rag/reports/latest_rag_inventory.md",
                    }
                except Exception:
                    pass

            return res

        else:  # view == "summary"
            # Modo summary: métricas de distribuição (padrão)
            total_chunks = 0
            asset_type_counts = {}
            asset_type_unique_skills = {}
            matched_parent_skills = set()
            matched_files = set()
            detailed_inventory = []

            for c_id, s_id, p_id, a_type, f_path, sec_title, c_tokens in filtered_rows:
                parent_id = p_id if p_id else s_id
                curr_type = a_type if a_type else "skill_root"
                curr_path = f_path if f_path else "SKILL.md"

                if parent_skill and (parent_id != parent_skill and s_id != parent_skill):
                    continue
                if asset_type and curr_type != asset_type:
                    continue

                total_chunks += 1
                matched_parent_skills.add(parent_id)
                matched_files.add(curr_path)

                if curr_type not in asset_type_counts:
                    asset_type_counts[curr_type] = 0
                    asset_type_unique_skills[curr_type] = set()
                asset_type_counts[curr_type] += 1
                asset_type_unique_skills[curr_type].add(parent_id)

            distribution = {}
            for atype, count in sorted(asset_type_counts.items()):
                distribution[atype] = {
                    "chunks": count,
                    "unique_skills": len(asset_type_unique_skills.get(atype, set()))
                }

            res = {
                "status": "success",
                "view": "summary",
                "total_chunks": total_chunks,
                "distribution_by_asset_type": distribution,
                "unique_parent_skills_count": len(matched_parent_skills),
                "filters_applied": {
                    "parent_skill": parent_skill,
                    "asset_type": asset_type,
                    "detailed": detailed,
                    "view": "summary",
                }
            }

            if parent_skill:
                res["parent_skill_details"] = {
                    "parent_skill_id": parent_skill,
                    "total_chunks": total_chunks,
                    "asset_types_present": list(distribution.keys()),
                    "indexed_files": sorted(list(matched_files))
                }

            if detailed:
                res["artifacts_inventory"] = detailed_inventory
                res["detailed_inventory"] = detailed_inventory

            # Persistir relatório se solicitado
            if save_report:
                try:
                    os.makedirs(report_dir, exist_ok=True)

                    # JSON report
                    json_report = {
                        "status": "success",
                        "view": "summary",
                        "total_chunks": total_chunks,
                        "distribution_by_asset_type": distribution,
                        "filters_applied": {
                            "parent_skill": parent_skill,
                            "asset_type": asset_type,
                            "detailed": detailed,
                            "view": "summary",
                        }
                    }
                    json_path = os.path.join(report_dir, "latest_rag_inventory.json")
                    with open(json_path, "w", encoding="utf-8") as jf:
                        json.dump(json_report, jf, indent=2, ensure_ascii=False)

                    # Markdown report
                    md_lines = [
                        "# 📊 Inventário RAG - Modo Summary (ADR-025)",
                        "",
                        f"**Total de chunks:** {total_chunks}",
                        "",
                        "## Distribuição por Tipo de Ativo",
                        "",
                    ]
                    for atype in sorted(distribution.keys()):
                        md_lines.append(f"### {atype.replace('_', ' ').title()}")
                        md_lines.append("")
                        table_header = "| Tipo | Chunks | Únicas Skills |"
                        table_sep = "|---|---|---|"
                        md_lines.append(table_header)
                        md_lines.append(table_sep)
                        md_lines.append(f"| {atype.replace('_', ' ').title()} | {distribution[atype]['chunks']} | {distribution[atype]['unique_skills']} |")
                        md_lines.append("")

                    md_path = os.path.join(report_dir, "latest_rag_inventory.md")
                    with open(md_path, "w", encoding="utf-8") as mf:
                        mf.write("\n".join(md_lines))

                    res["saved_reports"] = {
                        "json": ".local/skills_rag/reports/latest_rag_inventory.json",
                        "markdown": ".local/skills_rag/reports/latest_rag_inventory.md",
                    }
                except Exception:
                    pass

            return res

# ----------------------------------------------------------------------
# MCP Protocol Handlers (JSON-RPC 2.0)
# ----------------------------------------------------------------------

MCP_TOOLS = [
    {
        "name": "search_skills",
        "description": "Realiza busca semântica híbrida (vetorial + BM25) para encontrar as skills mais adequadas a uma tarefa.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Texto ou objetivo da tarefa (ex: 'criar testes para api laravel', 'auditoria de seguranca')"
                },
                "top_k": {
                    "type": "integer",
                    "description": "Número de skills a retornar (default: 3)",
                    "default": 3
                },
                "category": {
                    "type": "string",
                    "enum": ["config_skill", "plugin_skill", "builtin_skill", "mcp_server"],
                    "description": "Filtro opcional por categoria"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "route_task",
        "description": "Roteia automaticamente uma instrução de usuário para a melhor skill e gera o payload XML pronto para injeção no prompt.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "task_description": {
                    "type": "string",
                    "description": "Descrição completa da tarefa do usuário"
                },
                "top_k": {
                    "type": "integer",
                    "description": "Número de skills candidatas a considerar (default: 2)",
                    "default": 2
                }
            },
            "required": ["task_description"]
        }
    },
    {
        "name": "get_skill_details",
        "description": "Recupera os metadados completos, diretrizes de governança e preview do conteúdo de uma skill específica pelo seu ID.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "skill_id": {
                    "type": "string",
                    "description": "ID canônico da skill (ex: 'test-driven-development', 'security-review')"
                }
            },
            "required": ["skill_id"]
        }
    },
    {
        "name": "list_skills_catalog",
        "description": "Lista todas as skills indexadas no banco com seus IDs, nomes, versões, categorias e scores globais de governança.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "category_filter": {
                    "type": "string",
                    "enum": ["config_skill", "plugin_skill", "builtin_skill", "mcp_server"],
                    "description": "Filtro opcional por categoria"
                }
            }
        }
    },
    {
        "name": "bootstrap_agent_instructions",
        "description": "Inicializa ou sincroniza os arquivos AGENTS.md e GEMINI.md no workspace atual, configurando a matriz canônica de governança e o protocolo de orquestração MCP.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "workspace_path": {
                    "type": "string",
                    "description": "Caminho raiz do projeto (opcional; default: diretório de trabalho atual)"
                }
            }
        }
    },
    {
        "name": "get_rag_telemetry",
        "description": "Retorna métricas em tempo real de latência, taxa de cache hits, chamadas neurais e escopos ativos.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "inspect_rag_index",
        "description": "Inspeciona o inventário completo da base de conhecimento RAG (chunks, sub-ativos e tipos de ativos: skill_root, reference, template, script_doc). Suporta modos summary, items e chunks, além de persistência de relatórios.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "parent_skill": {
                    "type": "string",
                    "description": "Filtrar por ID específico de uma skill-mãe (ex: 'database-architecture')"
                },
                "asset_type": {
                    "type": "string",
                    "enum": ["skill_root", "reference", "template", "script_doc"],
                    "description": "Filtrar por tipo de ativo"
                },
                "view": {
                    "type": "string",
                    "enum": ["summary", "items", "chunks"],
                    "description": "Modo de visualização: 'summary' (padrão), 'items' (listas nominais agrupadas), 'chunks' (inventário detalhado). Padrão: 'summary'"
                },
                "detailed": {
                    "type": "boolean",
                    "description": "Se True e view='summary', promove automaticamente para view='chunks' (retrocompatibilidade). Se True e view='chunks', retorna lista granular de seções e caminhos. Padrão: False"
                },
                "save_report": {
                    "type": "boolean",
                    "description": "Se True, persiste relatórios JSON e Markdown em .local/skills_rag/reports/. Padrão: False"
                },
                "workspace_path": {
                    "type": "string",
                    "description": "Caminho raiz do workspace. Padrão: usa SKILLS_WORKSPACE_DIR ou diretório pai do servidor"
                }
            }
        }
    }
]

def send_response(response_dict):
    msg = json.dumps(response_dict)
    sys.stdout.write(msg + "\n")
    sys.stdout.flush()

def handle_rpc_request(req, db):
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "skills-rag-mcp",
                    "version": "1.0.0"
                }
            }
        }
    elif method == "notifications/initialized":
        return None
    elif method == "ping":
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": MCP_TOOLS
            }
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        
        try:
            if tool_name == "search_skills":
                res = db.search_skills(
                    query=args.get("query", ""),
                    top_k=args.get("top_k", 3),
                    category=args.get("category")
                )
            elif tool_name == "route_task":
                res = db.route_task(
                    task_description=args.get("task_description", ""),
                    top_k=args.get("top_k", 2)
                )
            elif tool_name == "get_skill_details":
                res = db.get_skill_details(skill_id=args.get("skill_id", ""))
            elif tool_name == "list_skills_catalog":
                res = db.list_all_skills(category_filter=args.get("category_filter"))
            elif tool_name == "bootstrap_agent_instructions":
                res = db.bootstrap_agent_instructions(workspace_path=args.get("workspace_path"))
            elif tool_name == "get_rag_telemetry":
                res = db.get_rag_telemetry()
            elif tool_name == "inspect_rag_index":
                res = db.inspect_rag_index(
                    parent_skill=args.get("parent_skill"),
                    asset_type=args.get("asset_type"),
                    view=args.get("view", "summary"),
                    detailed=args.get("detailed", False),
                    save_report=args.get("save_report", False),
                    workspace_path=args.get("workspace_path")
                )
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"}
                }
                
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(res, indent=2, ensure_ascii=False)
                        }
                    ]
                }
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "isError": True,
                    "content": [
                        {
                            "type": "text",
                            "text": f"Error executing tool '{tool_name}': {str(e)}"
                        }
                    ]
                }
            }
    else:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Method not found: {method}"}
        }

def run_mcp_server():
    db = SkillsDatabase()
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            res = handle_rpc_request(req, db)
            if res is not None:
                send_response(res)
        except Exception as e:
            err_res = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {str(e)}"}
            }
            send_response(err_res)

if __name__ == "__main__":
    run_mcp_server()
