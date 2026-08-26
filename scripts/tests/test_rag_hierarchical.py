#!/usr/bin/env python3
"""
Unit test suite for SOTA Hierarchical Multi-Asset RAG Pipeline (ADR-025).
Tests:
1. AssetParser for Markdown, Scripts (Docstrings only) and Templates.
2. SQLite Schema with asset_type, parent_skill_id, and file_path columns.
3. Parent Linking & Namespace resolution for secondary assets.
4. Damping Factor multipliers per asset_type.
5. Typed XML Serialization (<active_skill id="..." parent="..." type="..." path="...">).
"""

import os
import sys
import json
import sqlite3
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from skills_rag_indexer import AssetParser, init_db, compute_embedding
from skills_mcp_server import SkillsDatabase, DAMPING_FACTORS

class TestRAGHierarchical(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_hierarchical.sqlite3")
        self.conn = sqlite3.connect(self.db_path)
        init_db(self.conn)

    def tearDown(self):
        self.conn.close()
        self.temp_dir.cleanup()

    def test_asset_parser_markdown(self):
        md_content = """# Main Header
Introductory text.

## Section 1: Features
Feature detailed description.

### Subsection 1.1: Deep Dive
Detailed deep dive text.
"""
        chunks = AssetParser.parse_markdown(md_content, "references/deep-dive.md", "database-architecture")
        self.assertEqual(len(chunks), 3)
        self.assertEqual(chunks[0]["asset_type"], "reference")
        self.assertEqual(chunks[0]["file_path"], "references/deep-dive.md")
        self.assertEqual(chunks[0]["parent_skill_id"], "database-architecture")
        self.assertIn("Main Header", chunks[0]["section_title"])

    def test_asset_parser_script_noise_reduction(self):
        py_content = '''#!/usr/bin/env python3
"""
Generate ERD Diagram from SQLite Schema.
Usage: python3 generate_erd.py --input <db_file> --output <erd.png>
"""

import os
import sys

def main():
    for i in range(100):
        x = i * 2
        print(x)

if __name__ == "__main__":
    main()
'''
        chunks = AssetParser.parse_script(py_content, "scripts/generate_erd.py", "database-architecture")
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0]["asset_type"], "script_doc")
        self.assertEqual(chunks[0]["file_path"], "scripts/generate_erd.py")
        self.assertEqual(chunks[0]["parent_skill_id"], "database-architecture")
        # Ensure procedural loop was not included
        self.assertNotIn("for i in range(100)", chunks[0]["chunk_text"])
        self.assertIn("Generate ERD Diagram", chunks[0]["chunk_text"])
        self.assertIn("Usage:", chunks[0]["chunk_text"])

    def test_asset_parser_template_structure(self):
        sql_content = """-- PostgreSQL Migration Template with Rollback
-- Description: Standard zero-downtime schema migration template

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Down Migration:
-- DROP TABLE users;
"""
        chunks = AssetParser.parse_template(sql_content, "templates/migration.sql", "database-architecture")
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0]["asset_type"], "template")
        self.assertEqual(chunks[0]["file_path"], "templates/migration.sql")
        self.assertIn("PostgreSQL Migration Template", chunks[0]["chunk_text"])
        self.assertIn("CREATE TABLE users", chunks[0]["chunk_text"])

    def test_schema_has_hierarchical_columns(self):
        cur = self.conn.cursor()
        cur.execute("PRAGMA table_info(skill_chunks);")
        columns = [row[1] for row in cur.fetchall()]
        self.assertIn("asset_type", columns)
        self.assertIn("parent_skill_id", columns)
        self.assertIn("file_path", columns)

    def test_damping_factors_and_xml_payload(self):
        self.assertEqual(DAMPING_FACTORS.get("skill_root"), 1.00)
        self.assertEqual(DAMPING_FACTORS.get("reference"), 0.85)
        self.assertEqual(DAMPING_FACTORS.get("template"), 0.80)
        self.assertEqual(DAMPING_FACTORS.get("script_doc"), 0.75)

        # Test XML format helper
        db = SkillsDatabase(global_db_path=self.db_path)
        xml = db.format_chunk_xml(
            skill_id="database-architecture:template:migration",
            parent_skill_id="database-architecture",
            asset_type="template",
            file_path="templates/migration.sql",
            confidence=92.5,
            section_title="PostgreSQL Migration",
            content="CREATE TABLE example (id INT);"
        )
        self.assertIn('<active_skill id="database-architecture:template:migration"', xml)
        self.assertIn('parent="database-architecture"', xml)
        self.assertIn('type="template"', xml)
        self.assertIn('path="templates/migration.sql"', xml)
        self.assertIn('confidence="92.5%"', xml)

if __name__ == "__main__":
    unittest.main()
