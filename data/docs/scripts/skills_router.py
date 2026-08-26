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

WORKSPACE_DIR = "/home/loupan/.gemini/config/skills"
DB_PATH = os.path.join(WORKSPACE_DIR, "data/skills_rag_db/skills_rag.sqlite3")

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

class SkillsRouter:
    def __init__(self, db_path=DB_PATH):
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Dedicated Skills RAG DB not found at: {db_path}. Run skills_rag_indexer.py first.")
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()

    def query(self, text_query, top_k=3, category_filter=None):
        query_vec = compute_embedding(text_query)
        q_tokens = tokenize(text_query)
        q_lower = text_query.lower()
        
        # 1. Fetch all skills
        self.cur.execute("SELECT id, name, category, version, description, triggers_json, telemetry_json, vector_embedding, doc_summary FROM skills;")
        rows = self.cur.fetchall()
        
        # 2. FTS5 Lexical Search (BM25 normalized)
        fts_matches = {}
        if q_tokens:
            fts_query_parts = []
            for t in q_tokens:
                if len(t) > 2:
                    fts_query_parts.append(f'"{t}"*')
            if fts_query_parts:
                fts_q = ' OR '.join(fts_query_parts)
                try:
                    self.cur.execute("SELECT skill_id, rank FROM skills_fts WHERE skills_fts MATCH ? ORDER BY rank LIMIT 40;", (fts_q,))
                    for sid, r in self.cur.fetchall():
                        # More negative rank = stronger BM25 score
                        fts_matches[sid] = min(1.0, max(0.1, abs(r) / 5.0))
                except:
                    pass

        # 3. Chunk-level Vector Max-Pooling
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
            if category_filter and cat != category_filter:
                continue
                
            skill_vec = json.loads(vec_json)
            triggers = json.loads(trig_json)
            telem = json.loads(telem_json) if telem_json else {}
            
            # 1. Dense Semantic Similarity
            global_dense_sim = cosine_similarity(query_vec, skill_vec)
            chunk_sim = chunk_dense_max.get(sid, 0.0)
            dense_score = (0.70 * global_dense_sim) + (0.30 * chunk_sim)
            
            # 2. Sparse Lexical BM25 Score
            sparse_score = fts_matches.get(sid, 0.0)
            
            # 3. Exact Trigger & Name Matching
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

            # Weighted Hybrid Score
            if trigger_score > 0.8:
                final_score = (0.40 * trigger_score) + (0.35 * sparse_score) + (0.25 * dense_score)
            elif sparse_score > 0.5:
                final_score = (0.45 * sparse_score) + (0.35 * dense_score) + (0.20 * trigger_score)
            else:
                final_score = (0.55 * dense_score) + (0.35 * sparse_score) + (0.10 * trigger_score)
                
            confidence = min(99.9, round(final_score * 100, 1))
            
            telem_metrics = telem.get("telemetry_metrics", {})
            schema_tok = telem_metrics.get("schema_tokens", 250)
            latency_ms = telem_metrics.get("estimated_latency_ms", 120)
            side_eff = telem_metrics.get("side_effects", "Read-Only")
            
            results.append({
                "skill_id": sid,
                "name": name,
                "category": cat,
                "version": ver,
                "confidence": confidence,
                "description": desc,
                "matched_trigger": matched_trigger or (triggers[0] if triggers else name),
                "side_effects": side_eff,
                "schema_tokens": schema_tok,
                "latency_ms": latency_ms,
                "doc_summary": summary
            })

        results.sort(key=lambda x: x["confidence"], reverse=True)
        return results[:top_k]

    def generate_prompt_payload(self, skill_item):
        return f"""<!-- DYNAMIC SKILL INJECTION: {skill_item['name']} ({skill_item['version']}) -->
<skill name="{skill_item['name']}" category="{skill_item['category']}">
<description>{skill_item['description']}</description>
<side_effects>{skill_item['side_effects']}</side_effects>
<matched_trigger>{skill_item['matched_trigger']}</matched_trigger>
</skill>"""

def main():
    parser = argparse.ArgumentParser(description="SOTA Dedicated Skills Router & Dynamic Discovery Engine")
    parser.add_argument("query", nargs="?", help="Texto da tarefa ou consulta em linguagem natural")
    parser.add_argument("--top-k", type=int, default=3, help="Quantidade de skills recomendadas (default: 3)")
    parser.add_argument("--category", choices=["config_skill", "plugin_skill", "builtin_skill", "mcp_server"], help="Filtrar por categoria")
    parser.add_argument("--json", action="store_true", help="Saída em formato JSON para integração de agentes")
    parser.add_argument("--prompt-snippet", action="store_true", help="Gera snippet XML para injeção no prompt")
    parser.add_argument("--interactive", action="store_true", help="Inicia REPL interativo")
    
    args = parser.parse_args()
    router = SkillsRouter()
    
    if args.interactive:
        print("="*80)
        print("🧠 SOTA DEDICATED SKILLS ROUTER - REPL INTERATIVO")
        print("Digite sua consulta (ou 'exit' para sair):")
        print("="*80)
        while True:
            try:
                q = input("\n🔍 Query > ").strip()
                if not q or q.lower() in ['exit', 'quit', 'q']:
                    break
                results = router.query(q, top_k=args.top_k, category_filter=args.category)
                print(f"\nTop {len(results)} Skills Recomendadas:")
                for idx, item in enumerate(results, 1):
                    print(f"  [{idx}] {item['name']} ({item['category']}) - Confiança: {item['confidence']}%")
                    print(f"      Trigger: '{item['matched_trigger']}' | Latência: ~{item['latency_ms']}ms | Overhead: ~{item['schema_tokens']} tokens")
                    print(f"      Resumo: {item['doc_summary'][:140]}...")
            except (KeyboardInterrupt, EOFError):
                break
        return

    if not args.query:
        parser.print_help()
        sys.exit(1)
        
    results = router.query(args.query, top_k=args.top_k, category_filter=args.category)
    
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return
        
    if args.prompt_snippet:
        print("\n".join(router.generate_prompt_payload(item) for item in results))
        return

    print("="*80)
    print(f"🧠 SOTA SKILLS ROUTER - RESULTADOS PARA: '{args.query}'")
    print("="*80)
    for idx, item in enumerate(results, 1):
        print(f"\n[{idx}] 🎯 {item['name']} (ID: {item['skill_id']})")
        print(f"    • Categoria: {item['category']} | Versão: {item['version']} | Confiança: {item['confidence']}%")
        print(f"    • Gatilho Ativado: '{item['matched_trigger']}'")
        print(f"    • Telemetria: ~{item['schema_tokens']} tokens de schema | ~{item['latency_ms']}ms latência | Efeitos: {item['side_effects']}")
        print(f"    • Descrição: {item['description']}")
    print("\n" + "="*80)

if __name__ == "__main__":
    main()
