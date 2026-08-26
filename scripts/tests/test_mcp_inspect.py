#!/usr/bin/env python3
"""
Unit test suite for SOTA RAG MCP Tool `inspect_rag_index`.
Tests:
1. test_inspect_rag_index_summary: Default summary metrics and distribution counts.
2. test_inspect_rag_index_filter_parent_skill: Isolated sub-assets for specific parent skill.
3. test_inspect_rag_index_filter_asset_type: Filtering by asset_type (e.g. 'template').
4. test_inspect_rag_index_detailed_mode: Detailed inventory list with file_path and section.
5. test_inspect_rag_index_json_rpc_call: Invocations via JSON-RPC 2.0 protocol.
6. test_inspect_rag_index_view_items: Ensures view="items" returns nominal lists grouped by type.
7. test_inspect_rag_index_save_report: Ensures creation of JSON and Markdown report files.
8. test_inspect_backward_compatibility: Ensures old calls with detailed=True still work.
"""

import os
import sys
import json
import unittest
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from skills_mcp_server import SkillsDatabase, handle_rpc_request


class TestMCPInspectRAGIndex(unittest.TestCase):
    def setUp(self):
        self.db = SkillsDatabase()

    def test_inspect_rag_index_summary(self):
        res = self.db.inspect_rag_index()
        self.assertEqual(res.get("status"), "success")
        self.assertGreater(res.get("total_chunks", 0), 0)
        self.assertIn("distribution_by_asset_type", res)
        dist = res["distribution_by_asset_type"]
        self.assertIn("skill_root", dist)
        self.assertGreater(dist["skill_root"]["chunks"], 0)
        self.assertGreater(dist["skill_root"]["unique_skills"], 0)
        self.assertGreater(res.get("unique_parent_skills_count", 0), 0)

    def test_inspect_rag_index_filter_parent_skill(self):
        res = self.db.inspect_rag_index(parent_skill="database-architecture")
        self.assertEqual(res.get("status"), "success")
        self.assertGreater(res.get("total_chunks", 0), 0)
        self.assertIn("parent_skill_details", res)
        details = res["parent_skill_details"]
        self.assertEqual(details["parent_skill_id"], "database-architecture")
        self.assertGreaterEqual(len(details["indexed_files"]), 1)
        self.assertEqual(res.get("unique_parent_skills_count"), 1)

    def test_inspect_rag_index_filter_asset_type(self):
        res = self.db.inspect_rag_index(asset_type="template")
        self.assertEqual(res.get("status"), "success")
        self.assertGreater(res.get("total_chunks", 0), 0)
        dist = res["distribution_by_asset_type"]
        self.assertIn("template", dist)
        self.assertEqual(len(dist), 1)
        self.assertNotIn("skill_root", dist)

    def test_inspect_rag_index_detailed_mode(self):
        res = self.db.inspect_rag_index(parent_skill="database-architecture", detailed=True)
        self.assertEqual(res.get("status"), "success")
        self.assertIn("artifacts_inventory", res)
        self.assertIn("detailed_inventory", res)
        inventory = res["artifacts_inventory"]
        self.assertGreater(len(inventory), 0)
        item = inventory[0]
        self.assertIn("file_path", item)
        self.assertIn("section", item)
        self.assertIn("section_title", item)
        self.assertIn("asset_type", item)
        self.assertEqual(item["parent_skill_id"], "database-architecture")

    def test_inspect_rag_index_view_items(self):
        """Ensures view="items" returns nominal lists grouped by asset_type."""
        res = self.db.inspect_rag_index(view="items")
        self.assertEqual(res.get("status"), "success")
        self.assertIn("assets_by_type", res)
        self.assertIn("view", res)
        self.assertEqual(res["view"], "items")
        # Should have assets grouped by type (skill_root, reference, template, script_doc)
        assets_by_type = res.get("assets_by_type", {})
        self.assertIn("skill_root", assets_by_type)
        # Each asset should have parent_skill_id, file_path, chunk_count, total_tokens
        for asset in assets_by_type["skill_root"]:
            self.assertIn("parent_skill_id", asset)
            self.assertIn("file_path", asset)
            self.assertIn("chunk_count", asset)
            self.assertIn("total_tokens", asset)

    def test_inspect_rag_index_save_report(self):
        """Ensures save_report=True creates JSON and Markdown files in .local/skills_rag/reports/."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a minimal .local/skills_rag structure
            report_dir = os.path.join(tmpdir, ".local", "skills_rag", "reports")
            os.makedirs(report_dir, exist_ok=True)

            # Temporarily override the workspace path
            import skills_mcp_server as sm
            orig_workspace = sm.WORKSPACE_DIR
            sm.WORKSPACE_DIR = tmpdir

            try:
                res = self.db.inspect_rag_index(save_report=True, workspace_path=tmpdir)
                self.assertEqual(res.get("status"), "success")
                self.assertIn("saved_reports", res)

                # Verify files were created
                json_path = os.path.join(report_dir, "latest_rag_inventory.json")
                md_path = os.path.join(report_dir, "latest_rag_inventory.md")

                self.assertTrue(os.path.isfile(json_path), f"JSON report not found at {json_path}")
                self.assertTrue(os.path.isfile(md_path), f"Markdown report not found at {md_path}")

                # Validate JSON content
                with open(json_path, "r", encoding="utf-8") as jf:
                    json_data = json.load(jf)
                self.assertIn("status", json_data)
                self.assertIn("distribution_by_asset_type", json_data)

# Validate Markdown content has tables
                with open(md_path, "r", encoding="utf-8") as mf:
                    md_content = mf.read()
                self.assertIn("### Skill Root", md_content)
            finally:
                sm.WORKSPACE_DIR = orig_workspace

    def test_inspect_backward_compatibility(self):
        """Ensures old calls with detailed=True still work (promoted to view='chunks')."""
        # detailed=True with default view="summary" should promote to view="chunks"
        res = self.db.inspect_rag_index(detailed=True)
        self.assertEqual(res.get("status"), "success")
        self.assertIn("view", res)
        self.assertEqual(res["view"], "chunks")
        self.assertIn("total_chunks", res)
        self.assertIn("distribution_by_asset_type", res)

        # detailed=True with view="chunks" explicitly
        res2 = self.db.inspect_rag_index(detailed=True, view="chunks")
        self.assertEqual(res2.get("status"), "success")
        self.assertIn("detailed_inventory", res2)
        self.assertGreater(len(res2["detailed_inventory"]), 0)
        item = res2["detailed_inventory"][0]
        self.assertIn("file_path", item)
        self.assertIn("section", item)
        self.assertIn("section_title", item)

    def test_inspect_rag_index_json_rpc_call(self):
        req = {
            "jsonrpc": "2.0",
            "id": 101,
            "method": "tools/call",
            "params": {
                "name": "inspect_rag_index",
                "arguments": {
                    "parent_skill": "database-architecture",
                    "detailed": False
                }
            }
        }
        res = handle_rpc_request(req, self.db)
        self.assertIsNotNone(res)
        self.assertEqual(res.get("id"), 101)
        self.assertIn("result", res)
        self.assertIn("content", res["result"])
        payload = json.loads(res["result"]["content"][0]["text"])
        self.assertEqual(payload.get("status"), "success")
        self.assertGreater(payload.get("total_chunks", 0), 0)
        self.assertIn("distribution_by_asset_type", payload)


if __name__ == "__main__":
    unittest.main()
