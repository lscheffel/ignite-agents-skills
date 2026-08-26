#!/usr/bin/env python3
"""
Unit and Integration Tests for ADR-022 RAG SOTA Quad Enhancements:
1. Acronym and Technical Jargon Expansion
2. Rerank Cache with SHA-256 integrity keys
3. Focused Chunk-Level Dynamic XML Injection
4. 100% Offline / Local Fallback Compatibility
"""

import os
import sys
import json
import unittest
import sqlite3
import tempfile
import hashlib

SCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, SCRIPTS_DIR)

from skills_router import (
    SkillsRouter,
    expand_acronyms,
    generate_cache_key,
    compute_jaccard_similarity,
    compute_embedding
)

class TestRAGQuadSOTA(unittest.TestCase):
    def setUp(self):
        self.temp_db_fd, self.temp_db_path = tempfile.mkstemp(suffix=".sqlite3")
        self.conn = sqlite3.connect(self.temp_db_path)
        self.cur = self.conn.cursor()
        
        # Setup schema
        self.cur.execute("""
        CREATE TABLE skills (
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
        self.cur.execute("""
        CREATE TABLE skill_chunks (
            chunk_id TEXT PRIMARY KEY,
            skill_id TEXT NOT NULL,
            section_title TEXT NOT NULL,
            chunk_text TEXT NOT NULL,
            chunk_tokens INTEGER NOT NULL,
            vector_embedding TEXT NOT NULL,
            vector_embedding_2048 TEXT
        );
        """)
        self.cur.execute("""
        CREATE VIRTUAL TABLE skills_fts USING fts5(
            skill_id,
            name,
            description,
            triggers,
            content
        );
        """)
        self.cur.execute("""
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
        
        # Insert sample test skill
        skill_vec = compute_embedding("security review rbac access control")
        self.cur.execute("""
        INSERT INTO skills (
            id, name, category, version, description, triggers_json, tags_json,
            dim_scores_json, telemetry_json, primary_sha256, total_tokens,
            vector_embedding, doc_summary, full_content, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            "security-review",
            "security-review",
            "config_skill",
            "1.0.0",
            "Reviews code for security vulnerabilities, authentication, authorization, and RBAC.",
            json.dumps(["security-review", "rbac", "auth", "vulnerability"]),
            json.dumps(["security", "auth", "rbac"]),
            json.dumps({"global_score": 95.0}),
            json.dumps({"telemetry_metrics": {"schema_tokens": 280, "estimated_latency_ms": 110, "side_effects": "Read-Only"}}),
            "sha256_mock_hash_123",
            1200,
            json.dumps(skill_vec),
            "Security review and vulnerability scanner guide.",
            "# Security Review\n\n## Section 1: RBAC\nRBAC rules and checks.\n\n## Section 2: Input Sanitization\nSanitizing user input.",
            "2026-08-24"
        ))
        
        # Insert sample chunks
        chunk1_vec = compute_embedding("RBAC rules access control and authorization matrices")
        self.cur.execute("""
        INSERT INTO skill_chunks (chunk_id, skill_id, section_title, chunk_text, chunk_tokens, vector_embedding)
        VALUES (?, ?, ?, ?, ?, ?);
        """, (
            "sec_chunk_1",
            "security-review",
            "Section 1: RBAC",
            "RBAC rules access control, permissions verification and authorization matrices.",
            150,
            json.dumps(chunk1_vec)
        ))
        
        self.cur.execute("""
        INSERT INTO skills_fts (skill_id, name, description, triggers, content)
        VALUES (?, ?, ?, ?, ?);
        """, (
            "security-review",
            "security-review",
            "Reviews code for security vulnerabilities, authentication, authorization, and RBAC.",
            "security-review rbac auth vulnerability",
            "RBAC rules access control and input sanitization"
        ))
        
        self.conn.commit()

    def tearDown(self):
        self.conn.close()
        try:
            os.close(self.temp_db_fd)
            os.unlink(self.temp_db_path)
        except OSError:
            pass

    def test_acronym_expansion(self):
        """Test acronym expansion returns expanded terms with weighted structure"""
        query = "como configurar rbac e tdd no projeto"
        expanded = expand_acronyms(query)
        self.assertIn("role based access control", expanded.lower())
        self.assertIn("test driven development", expanded.lower())
        self.assertTrue(expanded.startswith(query))

    def test_cache_key_generation_and_integrity(self):
        """Test cache key changes when skill SHA256 changes (auto-invalidation)"""
        candidates_v1 = [
            {"skill_id": "security-review", "primary_sha256": "hash_aaa"}
        ]
        candidates_v2 = [
            {"skill_id": "security-review", "primary_sha256": "hash_bbb"}
        ]
        
        k1 = generate_cache_key("auditoria rbac", candidates_v1)
        k2 = generate_cache_key("auditoria rbac", candidates_v1)
        k3 = generate_cache_key("auditoria rbac", candidates_v2)
        
        self.assertEqual(k1, k2, "Same query and skill hashes must produce identical cache key")
        self.assertNotEqual(k1, k3, "Modified skill SHA256 must invalidate cache key")

    def test_focused_chunk_xml_injection(self):
        """Test XML generation with focused chunk match preserving canonical metadata"""
        router = SkillsRouter(db_path=self.temp_db_path)
        results = router.query("como verificar permissoes de rbac", top_k=1, use_neural=False)
        self.assertEqual(len(results), 1)
        skill_item = results[0]
        xml_payload = router.generate_prompt_payload(skill_item, query="rbac")
        self.assertIn('name="security-review"', xml_payload)
        self.assertIn('<skill', xml_payload)
        self.assertIn('<description>', xml_payload)
        self.assertIn('<side_effects>Read-Only</side_effects>', xml_payload)
        self.assertIn('<focused_chunk section="Section 1: RBAC">', xml_payload)

    def test_offline_fallback_execution(self):
        """Test local fallback executes seamlessly without NVIDIA_API_KEY"""
        router = SkillsRouter(db_path=self.temp_db_path)
        results = router.query("auditoria de seguranca rbac", top_k=1, use_neural=False)
        self.assertGreaterEqual(len(results), 1)
        self.assertEqual(results[0]["skill_id"], "security-review")
        self.assertIn("Hybrid-Local", results[0]["engine"])

if __name__ == "__main__":
    unittest.main()
