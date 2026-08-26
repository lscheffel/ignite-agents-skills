#!/usr/bin/env python3
"""
SOTA SKILLS RAG - MODEL CONTEXT PROTOCOL (MCP) SERVER
Servidor MCP nativo em Python (JSON-RPC 2.0 Stdio) conectando o banco semântico dedicado de 80 skills.
"""

import os
import re
import sys
import json
import math
import sqlite3
import hashlib

WORKSPACE_DIR = "/home/loupan/.gemini/config/skills"
DEFAULT_DB_PATH = os.path.join(WORKSPACE_DIR, "data/skills_rag_db/skills_rag.sqlite3")
DB_PATH = os.environ.get("SKILLS_DB_PATH", DEFAULT_DB_PATH)

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

class SkillsDatabase:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cur = self.conn.cursor()

    def search_skills(self, query, top_k=3, category=None):
        query_vec = compute_embedding(query)
        q_tokens = tokenize(query)
        q_lower = query.lower()
        
        self.cur.execute("SELECT id, name, category, version, description, triggers_json, telemetry_json, vector_embedding, doc_summary FROM skills;")
        rows = self.cur.fetchall()
        
        fts_matches = {}
        if q_tokens:
            fts_parts = [f'"{t}"*' for t in q_tokens if len(t) > 2]
            if fts_parts:
                fts_q = ' OR '.join(fts_parts)
                try:
                    self.cur.execute("SELECT skill_id, rank FROM skills_fts WHERE skills_fts MATCH ? ORDER BY rank LIMIT 40;", (fts_q,))
                    for sid, r in self.cur.fetchall():
                        fts_matches[sid] = min(1.0, max(0.1, abs(r) / 5.0))
                except:
                    pass

        chunk_dense_max = {}
        self.cur.execute("SELECT skill_id, vector_embedding FROM skill_chunks;")
        for sid, cvec_json in self.cur.fetchall():
            cvec = json.loads(cvec_json)
            sim = cosine_similarity(query_vec, cvec)
            if sim > chunk_dense_max.get(sid, 0.0):
                chunk_dense_max[sid] = sim

        results = []
        for r in rows:
            sid, name, cat, ver, desc, trig_json, telem_json, vec_json, summary = r
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
            telem_metrics = telem.get("telemetry_metrics", {})
            
            results.append({
                "skill_id": sid,
                "name": name,
                "category": cat,
                "version": ver,
                "confidence_percent": confidence,
                "matched_trigger": matched_trigger or (triggers[0] if triggers else name),
                "description": desc,
                "telemetry": {
                    "schema_tokens": telem_metrics.get("schema_tokens", 250),
                    "latency_ms": telem_metrics.get("estimated_latency_ms", 120),
                    "side_effects": telem_metrics.get("side_effects", "Read-Only")
                },
                "doc_summary": summary
            })

        results.sort(key=lambda x: x["confidence_percent"], reverse=True)
        return results[:top_k]

    def get_skill_details(self, skill_id):
        self.cur.execute("""
        SELECT id, name, category, version, description, triggers_json, tags_json,
               dim_scores_json, telemetry_json, primary_sha256, total_tokens, doc_summary, full_content
        FROM skills WHERE id = ? OR name = ?;
        """, (skill_id, skill_id))
        row = self.cur.fetchone()
        if not row:
            return {"error": f"Skill '{skill_id}' not found in database."}
            
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

    def list_all_skills(self, category_filter=None):
        query = "SELECT id, name, category, version, description, dim_scores_json FROM skills"
        params = ()
        if category_filter:
            query += " WHERE category = ?"
            params = (category_filter,)
        query += " ORDER BY name ASC;"
        
        self.cur.execute(query, params)
        rows = self.cur.fetchall()
        skills = []
        for sid, name, cat, ver, desc, dim_json in rows:
            score_data = json.loads(dim_json) if dim_json else {}
            skills.append({
                "id": sid,
                "name": name,
                "category": cat,
                "version": ver,
                "global_score": score_data.get("global_score", 90.0),
                "description": desc
            })
        return {"total_count": len(skills), "skills": skills}

    def route_task(self, task_description, top_k=2):
        top_skills = self.search_skills(task_description, top_k=top_k)
        if not top_skills:
            return {"status": "no_match", "message": "No matching skills found."}
            
        best = top_skills[0]
        xml_prompt_injection = f"""<!-- DYNAMIC SKILL INJECTION VIA MCP ROUTER: {best['name']} ({best['version']}) -->
<active_skill id="{best['skill_id']}" category="{best['category']}">
<description>{best['description']}</description>
<side_effects>{best['telemetry']['side_effects']}</side_effects>
<trigger_reason>{best['matched_trigger']}</trigger_reason>
</active_skill>"""

        return {
            "primary_skill": best,
            "candidate_skills": top_skills,
            "prompt_injection_xml": xml_prompt_injection,
            "estimated_overhead_tokens": best["telemetry"]["schema_tokens"]
        }

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
                    "description": "Quantidade máxima de candidatos (default: 2)",
                    "default": 2
                }
            },
            "required": ["task_description"]
        }
    },
    {
        "name": "get_skill_details",
        "description": "Obtém as especificações completas, telemetria, regras operacionais e score forense de uma skill específica.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "skill_id": {
                    "type": "string",
                    "description": "ID ou nome da skill (ex: 'adr-generator', 'security-review', 'chrome-extensions')"
                }
            },
            "required": ["skill_id"]
        }
    },
    {
        "name": "list_skills_catalog",
        "description": "Lista todas as 80 skills ativas no ecossistema com metadados, categorias e notas de conformidade.",
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
