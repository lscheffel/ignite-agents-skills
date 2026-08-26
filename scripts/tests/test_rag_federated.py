#!/usr/bin/env python3
"""
Unit, Integration and Forensic Tests for ADR-023:
Federated Multi-Scope RAG Architecture (Global + Multi-Agent Workspace Local)
1. Multi-Agent Workspace Discovery (Gemini, Kilo, Claude, Cursor, Windsurf)
2. On-Demand Dynamic Local Auto-Indexing (mtime-based)
3. In-Memory Shadowing & Conflict Resolution (Precedence of local over global)
4. Scope Tagging in XML Injection Payload (scope="workspace_local" vs scope="global")
5. Forensic Invariant: ZERO-MUTATION on Global SQLite Database (SHA-256 integrity check)
"""

import os
import sys
import json
import shutil
import unittest
import sqlite3
import tempfile
import hashlib

SCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, SCRIPTS_DIR)

from skills_router import (
    SkillsRouter,
    WorkspaceScopeResolver,
    WORKSPACE_SKILL_CANDIDATE_DIRS,
    compute_embedding
)

class TestRAGFederated(unittest.TestCase):
    def setUp(self):
        # 1. Create a mock Global DB
        self.global_dir = tempfile.mkdtemp(prefix="mock_global_")
        self.global_db_path = os.path.join(self.global_dir, "skills_rag.sqlite3")
        self._init_mock_db(self.global_db_path, [
            {
                "id": "test-driven-development",
                "name": "test-driven-development",
                "category": "config_skill",
                "version": "1.0.0",
                "description": "Global standard for Test-Driven Development (RED-GREEN-REFACTOR).",
                "triggers": ["tdd", "test-driven-development"],
                "content": "# TDD Global Standard\n\n## Core Rules\nWrite failing test first.",
                "summary": "Global TDD guidelines"
            },
            {
                "id": "git-workflow",
                "name": "git-workflow",
                "category": "config_skill",
                "version": "1.0.0",
                "description": "Global Git operations and branch management.",
                "triggers": ["git", "git-workflow", "commit"],
                "content": "# Git Workflow Standard\n\n## Branching\nFollow Conventional Commits.",
                "summary": "Global Git operations"
            }
        ])

        # 2. Create a mock Workspace Root
        self.workspace_dir = tempfile.mkdtemp(prefix="mock_workspace_")

    def tearDown(self):
        shutil.rmtree(self.global_dir, ignore_errors=True)
        shutil.rmtree(self.workspace_dir, ignore_errors=True)

    def _init_mock_db(self, db_path, skills):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        conn = sqlite3.connect(db_path)
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
            skill_id, name, description, triggers, content
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS rerank_cache (
            query_hash TEXT PRIMARY KEY, query_text TEXT NOT NULL,
            rankings_json TEXT NOT NULL, engine_name TEXT NOT NULL,
            hit_count INTEGER DEFAULT 1, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        for s in skills:
            vec = compute_embedding(f"{s['name']} {s['description']} {' '.join(s['triggers'])}")
            sha = hashlib.sha256(s['content'].encode('utf-8')).hexdigest()
            cur.execute("""
            INSERT INTO skills VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                s["id"], s["name"], s["category"], s["version"], s["description"],
                json.dumps(s["triggers"]), json.dumps(["test"]), json.dumps({"global_score": 95.0}),
                json.dumps({"telemetry_metrics": {"schema_tokens": 200, "estimated_latency_ms": 100, "side_effects": "Read-Only"}}),
                sha, 500, json.dumps(vec), None, s["summary"], s["content"], "2026-08-24"
            ))
            cur.execute("""
            INSERT INTO skill_chunks VALUES (?, ?, ?, ?, ?, ?, ?);
            """, (f"{s['id']}_c1", s["id"], "Overview", s["content"], 100, json.dumps(vec), None))
            cur.execute("""
            INSERT INTO skills_fts VALUES (?, ?, ?, ?, ?);
            """, (s["id"], s["name"], s["description"], " ".join(s["triggers"]), s["content"]))
        conn.commit()
        conn.close()

    def test_global_only_resolution(self):
        """When workspace has no local skills, router operates in single-scope Global-Only mode"""
        router = SkillsRouter(global_db_path=self.global_db_path, cwd=self.workspace_dir)
        self.assertIsNone(router.local_db)
        results = router.query("como fazer commits no git", top_k=1, use_neural=False)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["skill_id"], "git-workflow")
        self.assertEqual(results[0]["scope"], "global")

    def test_multi_agent_workspace_discovery_and_auto_indexing(self):
        """Test discovering skills in multi-agent dirs (.kilo/skills, .claude/skills, .gemini/skills) and auto-indexing"""
        for candidate_dir in [".kilo/skills", ".claude/skills", ".cursor/skills"]:
            ws = tempfile.mkdtemp()
            target_skills_dir = os.path.join(ws, candidate_dir)
            os.makedirs(os.path.join(target_skills_dir, "custom-deploy"), exist_ok=True)
            
            with open(os.path.join(target_skills_dir, "custom-deploy", "SKILL.md"), "w", encoding="utf-8") as f:
                f.write("""---
name: custom-deploy
version: 1.0.0
description: Deploy local para ambiente de staging interno da empresa.
triggers:
  - deploy-staging
  - custom-deploy
---
# Custom Deploy
Instruções para deploy no Kubernetes interno.""")

            found_dir = WorkspaceScopeResolver.find_workspace_skills_dir(ws)
            self.assertIsNotNone(found_dir)
            self.assertTrue(found_dir.endswith(candidate_dir))
            
            # Ensure Auto-Indexing runs and generates SQLite DB in .local/skills_rag/
            local_db = WorkspaceScopeResolver.resolve_and_ensure_local_db(ws)
            self.assertIsNotNone(local_db)
            self.assertTrue(os.path.isfile(local_db))
            self.assertTrue(local_db.endswith(os.path.join(".local", "skills_rag", "skills_rag.sqlite3")))
            
            shutil.rmtree(ws, ignore_errors=True)

    def test_in_memory_shadowing(self):
        """Local skill with same ID as global must shadow (override) global skill in session memory"""
        # Create a custom local skill with same ID 'test-driven-development' in workspace .gemini/skills
        local_skills_dir = os.path.join(self.workspace_dir, ".gemini", "skills", "test-driven-development")
        os.makedirs(local_skills_dir, exist_ok=True)
        with open(os.path.join(local_skills_dir, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write("""---
name: test-driven-development
version: 2.0.0-custom-company
description: TDD Customizado com mocks proprietários da empresa.
triggers:
  - tdd
  - test-driven-development
---
# TDD Customizado
Usar sempre pytest com fixtures internas.""")

        router = SkillsRouter(global_db_path=self.global_db_path, cwd=self.workspace_dir)
        self.assertIsNotNone(router.local_db, "Local DB should be auto-indexed and connected")
        
        results = router.query("como aplicar tdd no projeto", top_k=2, use_neural=False)
        self.assertGreaterEqual(len(results), 1)
        
        # Verify shadowing
        best = results[0]
        self.assertEqual(best["skill_id"], "test-driven-development")
        self.assertEqual(best["scope"], "workspace_local")
        self.assertEqual(best["version"], "2.0.0-custom-company")
        self.assertIn("proprietários da empresa", best["description"])

    def test_payload_scope_tagging(self):
        """XML Prompt injection payload must include scope='workspace_local' or scope='global'"""
        local_skills_dir = os.path.join(self.workspace_dir, ".skills", "seed-db")
        os.makedirs(local_skills_dir, exist_ok=True)
        with open(os.path.join(local_skills_dir, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write("""---
name: seed-db
version: 1.0.0
description: Executa seeds do banco local para testes.
triggers:
  - seed-db
---
# Seed DB
php artisan db:seed""")

        router = SkillsRouter(global_db_path=self.global_db_path, cwd=self.workspace_dir)
        results = router.query("seed de banco de dados", top_k=1, use_neural=False)
        self.assertEqual(len(results), 1)
        
        xml_payload = router.generate_prompt_payload(results[0])
        self.assertIn('scope="workspace_local"', xml_payload)
        self.assertIn('name="seed-db"', xml_payload)

    def test_zero_mutation_global_db(self):
        """Forensic Test: SHA-256 hash of the Global DB file must remain 100% UNCHANGED after local queries & shadowing"""
        def get_file_sha256(path):
            h = hashlib.sha256()
            with open(path, "rb") as f:
                while chunk := f.read(8192):
                    h.update(chunk)
            return h.hexdigest()

        initial_global_sha = get_file_sha256(self.global_db_path)

        # Setup local skill that conflicts with global
        local_skills_dir = os.path.join(self.workspace_dir, ".gemini", "skills", "git-workflow")
        os.makedirs(local_skills_dir, exist_ok=True)
        with open(os.path.join(local_skills_dir, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write("""---
name: git-workflow
version: 9.9.9-local
description: Git workflow local com regras de trunk based.
triggers:
  - git
  - commit
---
# Trunk based development""")

        router = SkillsRouter(global_db_path=self.global_db_path, cwd=self.workspace_dir)
        
        # Execute multiple queries
        for _ in range(5):
            router.query("como commitar no git", top_k=2, use_neural=False)
            router.query("regras de tdd", top_k=2, use_neural=False)

        post_query_global_sha = get_file_sha256(self.global_db_path)
        
        self.assertEqual(
            initial_global_sha,
            post_query_global_sha,
            "CRITICAL INVARIANT VIOLATION: Global SQLite database was mutated during federated query!"
        )

if __name__ == "__main__":
    unittest.main()
