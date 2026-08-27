#!/usr/bin/env python3
"""
SOTA DEDICATED SKILLS ROUTER & DYNAMIC DISCOVERY ENGINE (HIGH-PRECISION SOTA)
Busca semântica híbrida com balanceamento global + chunk, BM25 normalizado e boosting determinístico de triggers.
"""

import os
import re
import sys
import json
import math
import sqlite3
import hashlib
import argparse
import copy

WORKSPACE_DIR = os.environ.get("SKILLS_WORKSPACE_DIR", os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
DB_PATH = os.environ.get("SKILLS_DB_PATH", os.path.join(WORKSPACE_DIR, "data/skills_rag_db/skills_rag.sqlite3"))

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

def fetch_nemotron_query_embedding(query, api_key):
    """Obtém embedding de 2048 dimensões via NVIDIA NIM (nvidia/nemotron-3-embed-1b)"""
    if not api_key:
        return None
    try:
        import requests
        url = "https://integrate.api.nvidia.com/v1/embeddings"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        payload = {
            "input": [query],
            "model": "nvidia/nemotron-3-embed-1b",
            "input_type": "query",
            "encoding_format": "float"
        }
        r = requests.post(url, json=payload, headers=headers, timeout=3.0)
        if r.status_code == 200:
            data = r.json()
            return data["data"][0]["embedding"]
    except Exception:
        pass
    return None

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
    - Stage 3: Logit Cutoff (logit >= -16.0) + Sigmoid Calibration + Anti-Redundancy Diversity
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
            c["confidence"] = min(99.9, max(15.0, round(prob * 100, 1)))
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
        
        # Salvar em Cache se disponível
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
        # Não considerar o próprio diretório global canônico ou o próprio repo de skills como workspace local
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
        
        # Verificar mtimes para auto-indexação sob demanda
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

        # Auto-Indexação Local
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

            # Parse frontmatter
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

                # Ingest chunks
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
            
        # Check direct sqlite existing in project (.local or legacy fallback)
        direct_db = os.path.join(base_dir, ".local", "skills_rag", "skills_rag.sqlite3")
        if os.path.isfile(direct_db):
            return direct_db
            
        direct_legacy = os.path.join(base_dir, ".gemini", "skills_rag.sqlite3")
        if os.path.isfile(direct_legacy):
            return direct_legacy
            
        return None

DAMPING_FACTORS = {
    "skill_root": 1.00,
    "reference": 0.85,
    "template": 0.80,
    "script_doc": 0.75
}

class SkillsRouter:
    def __init__(self, global_db_path=DB_PATH, local_db_path=None, db_path=None, cwd=None):
        target_global = db_path or global_db_path
        self.global_db_path = target_global
        self.global_conn = None
        self.global_cur = None
        
        if os.path.exists(target_global):
            # Conexão estrita somente-leitura com o banco global (Zero-Mutation guarantee)
            self.global_conn = sqlite3.connect(target_global)
            self.global_cur = self.global_conn.cursor()
            try:
                self.global_cur.execute("PRAGMA query_only = ON;")
            except Exception:
                pass
            self._ensure_cache_table(self.global_conn, self.global_cur)

        # Resolução e conexão com banco local do Workspace
        self.local_db_path = local_db_path or WorkspaceScopeResolver.resolve_and_ensure_local_db(cwd)
        self.local_conn = None
        self.local_cur = None
        if self.local_db_path and os.path.exists(self.local_db_path) and os.path.abspath(self.local_db_path) != os.path.abspath(target_global):
            self.local_conn = sqlite3.connect(self.local_db_path)
            self.local_cur = self.local_conn.cursor()
            self._ensure_cache_table(self.local_conn, self.local_cur)

        # Alias de retrocompatibilidade
        self.conn = self.global_conn
        self.cur = self.global_cur
        self.local_db = self.local_conn

    def _ensure_cache_table(self, conn, cur):
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
            conn.commit()
        except Exception:
            pass

    def get_best_matching_chunk(self, skill_id, query_vec, query_text="", cur=None):
        """Retorna o chunk de maior relevância semântica para injeção focalizada (Token Economy - ADR-025)"""
        curs = [cur] if cur else [self.local_cur, self.global_cur]
        for c in curs:
            if not c:
                continue
            try:
                try:
                    c.execute("""
                    SELECT section_title, chunk_text, vector_embedding, parent_skill_id, asset_type, file_path 
                    FROM skill_chunks WHERE skill_id = ? OR parent_skill_id = ?;
                    """, (skill_id, skill_id))
                    rows = c.fetchall()
                except Exception:
                    c.execute("""
                    SELECT section_title, chunk_text, vector_embedding, '', 'skill_root', 'SKILL.md'
                    FROM skill_chunks WHERE skill_id = ?;
                    """, (skill_id,))
                    rows = c.fetchall()

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

    def _search_scope_db(self, conn, cur, text_query, expanded_query, query_vec, q_tokens, q_lower, scope_name, category_filter=None):
        if not cur:
            return []
            
        cur.execute("""
        SELECT id, name, category, version, description, triggers_json, telemetry_json,
               primary_sha256, vector_embedding, doc_summary FROM skills;
        """)
        rows = cur.fetchall()
        
        fts_matches = {}
        if q_tokens:
            literal_tokens = tokenize(text_query)
            fts_query_parts = []
            for t in literal_tokens:
                if len(t) > 2:
                    fts_query_parts.append(f'"{t}"*')
            for t in q_tokens:
                if len(t) > 2 and t not in literal_tokens:
                    fts_query_parts.append(f'"{t}"*')
            if fts_query_parts:
                fts_q = ' OR '.join(fts_query_parts)
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
            if category_filter and cat != category_filter:
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
            
            # Boost local context (+5%)
            if scope_name == "workspace_local":
                confidence = min(99.9, round(confidence * 1.05, 1))
                
            telem_metrics = telem.get("telemetry_metrics", {})
            schema_tok = telem_metrics.get("schema_tokens", 250)
            latency_ms = telem_metrics.get("estimated_latency_ms", 120)
            side_eff = telem_metrics.get("side_effects", "Read-Only")
            
            candidates.append({
                "skill_id": sid,
                "name": name,
                "category": cat,
                "version": ver,
                "scope": scope_name,
                "primary_sha256": sha256,
                "confidence": confidence,
                "description": desc,
                "matched_trigger": matched_trigger or (triggers[0] if triggers else name),
                "side_effects": side_eff,
                "schema_tokens": schema_tok,
                "latency_ms": latency_ms,
                "doc_summary": summary,
                "engine": "Stage-1-Hybrid-Local (SQLite3/FTS5)"
            })

        return candidates

    def query(self, text_query, top_k=3, category_filter=None, use_neural=True):
        api_key = os.environ.get("NVIDIA_API_KEY")
        expanded_query = expand_acronyms(text_query)
        query_vec = compute_embedding(text_query)
        q_tokens = tokenize(expanded_query)
        q_lower = text_query.lower()
        
        # 1. Coleta do escopo Global
        global_candidates = self._search_scope_db(
            self.global_conn, self.global_cur, text_query, expanded_query,
            query_vec, q_tokens, q_lower, "global", category_filter
        )

        # 2. Coleta do escopo Local do Workspace (se ativo)
        local_candidates = self._search_scope_db(
            self.local_conn, self.local_cur, text_query, expanded_query,
            query_vec, q_tokens, q_lower, "workspace_local", category_filter
        )

        # 3. Fusão com Shadowing em Memória (Local tem precedência sobre Global em caso de colisão de ID)
        candidates_map = {}
        for c in global_candidates:
            candidates_map[c["skill_id"]] = c
            
        for c in local_candidates:
            candidates_map[c["skill_id"]] = c # Shadowing garantido

        merged_candidates = list(candidates_map.values())
        merged_candidates.sort(key=lambda x: x["confidence"], reverse=True)
        
        # 4. Reranking Neural Unificado com Cache
        if use_neural:
            candidate_pool = merged_candidates[:max(top_k * 5, 15)]
            active_cur = self.local_cur or self.global_cur
            active_conn = self.local_conn or self.global_conn
            final_results = neural_cross_encoder_rerank(
                text_query, candidate_pool, top_k=top_k,
                api_key=api_key, conn=active_conn, cur=active_cur
            )
            return final_results
        
        return merged_candidates[:top_k]

    def generate_prompt_payload(self, skill_item, query=""):
        """Gera payload XML com injeção focalizada por chunks e rastreabilidade de escopo (ADR-023)"""
        q_vec = compute_embedding(query if query else skill_item.get("matched_trigger", ""))
        best_chunk = self.get_best_matching_chunk(skill_item["skill_id"], q_vec, query)
        
        focused_xml = ""
        if best_chunk and best_chunk.get("section_title"):
            focused_xml = f"""
  <focused_chunk section="{best_chunk['section_title']}">
{best_chunk['chunk_text']}
  </focused_chunk>"""

        scope_val = skill_item.get("scope", "global")
        parent_val = best_chunk.get("parent_skill_id", skill_item["skill_id"]) if best_chunk else skill_item["skill_id"]
        type_val = best_chunk.get("asset_type", "skill_root") if best_chunk else "skill_root"
        path_val = best_chunk.get("file_path", "SKILL.md") if best_chunk else "SKILL.md"

        return f"""<!-- DYNAMIC SKILL INJECTION (ADR-025 HIERARCHICAL): {skill_item['name']} ({skill_item['version']}) -->
<skill id="{skill_item['skill_id']}" parent="{parent_val}" type="{type_val}" path="{path_val}" name="{skill_item['name']}" category="{skill_item['category']}" scope="{scope_val}">
  <summary>{skill_item['doc_summary']}</summary>
  <description>{skill_item['description']}</description>
  <side_effects>{skill_item['side_effects']}</side_effects>
  <matched_trigger>{skill_item['matched_trigger']}</matched_trigger>{focused_xml}
</skill>"""

def main():
    parser = argparse.ArgumentParser(description="SOTA Dedicated Skills Router & Dynamic Discovery Engine (ADR-025 Hierarchical)")
    parser.add_argument("query", nargs="?", help="Texto da tarefa ou consulta em linguagem natural")
    parser.add_argument("--top-k", type=int, default=3, help="Quantidade de skills recomendadas (default: 3)")
    parser.add_argument("--category", choices=["config_skill", "plugin_skill", "builtin_skill", "mcp_server"], help="Filtrar por categoria")
    parser.add_argument("--asset-type", choices=["skill_root", "reference", "template", "script_doc"], help="Filtrar por tipo de ativo")
    parser.add_argument("--local", action="store_true", help="Força execução em modo local (desativa reranking neural)")
    parser.add_argument("--json", action="store_true", help="Saída em formato JSON para integração de agentes")
    parser.add_argument("--prompt-snippet", action="store_true", help="Gera snippet XML para injeção no prompt")
    parser.add_argument("--interactive", action="store_true", help="Inicia REPL interativo")
    
    args = parser.parse_args()
    router = SkillsRouter()
    use_neural = not args.local
    
    if args.interactive:
        print("="*80)
        print("🧠 SOTA DEDICATED SKILLS ROUTER - REPL INTERATIVO (ADR-022 QUAD-SOTA)")
        print(f"Modo de Execução: {'⚡ Neural Cross-Encoder & Cache' if use_neural else '🖥️ Local Hashing (Zero-Dep)'}")
        print("Digite sua consulta (ou 'exit' para sair):")
        print("="*80)
        while True:
            try:
                q = input("\n🔍 Query > ").strip()
                if not q or q.lower() in ['exit', 'quit', 'q']:
                    break
                results = router.query(q, top_k=args.top_k, category_filter=args.category, use_neural=use_neural)
                print(f"\nTop {len(results)} Skills Recomendadas:")
                for idx, item in enumerate(results, 1):
                    logit_info = f" | Logit: {item.get('rerank_logit', 'N/A')}" if 'rerank_logit' in item else ""
                    print(f"  [{idx}] {item['name']} ({item['category']}) - Confiança: {item['confidence']}%{logit_info}")
                    print(f"      Engine: {item.get('engine', 'Local')} | Trigger: '{item['matched_trigger']}' | Latência: ~{item['latency_ms']}ms")
                    print(f"      Resumo: {item['doc_summary'][:140]}...")
            except (KeyboardInterrupt, EOFError):
                break
        return

    if not args.query:
        parser.print_help()
        sys.exit(1)
        
    results = router.query(args.query, top_k=args.top_k, category_filter=args.category, use_neural=use_neural)
    
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return
        
    if args.prompt_snippet:
        print("\n".join(router.generate_prompt_payload(item, query=args.query) for item in results))
        return

    print("="*80)
    print(f"🧠 SOTA SKILLS ROUTER - RESULTADOS PARA: '{args.query}'")
    engine_name = results[0].get('engine', 'Local') if results else 'Local'
    print(f"Engine Ativo: {engine_name}")
    print("="*80)
    for idx, item in enumerate(results, 1):
        logit_info = f" | Rerank Logit: {item.get('rerank_logit')}" if 'rerank_logit' in item else ""
        print(f"\n[{idx}] 🎯 {item['name']} (ID: {item['skill_id']})")
        print(f"    • Categoria: {item['category']} | Versão: {item['version']} | Confiança: {item['confidence']}%{logit_info}")
        print(f"    • Gatilho Ativado: '{item['matched_trigger']}'")
        print(f"    • Telemetria: ~{item['schema_tokens']} tokens de schema | ~{item['latency_ms']}ms latência | Efeitos: {item['side_effects']}")
        print(f"    • Descrição: {item['description']}")
    print("\n" + "="*80)

if __name__ == "__main__":
    main()
