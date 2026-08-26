#!/usr/bin/env python3
"""
Unit and Integration Tests for MCP Tool: bootstrap_agent_instructions
Verifies:
1. Creation of AGENTS.md and GEMINI.md from scratch in isolated workspace.
2. Idempotent append behavior in AGENTS.md (no duplication of protocol block).
3. Correct lightweight stub content in GEMINI.md.
4. Full MCP JSON-RPC 2.0 tool execution via handle_rpc_request.
"""

import os
import sys
import json
import shutil
import unittest
import tempfile

SCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, SCRIPTS_DIR)

from skills_mcp_server import SkillsDatabase, handle_rpc_request, MCP_TOOLS

class TestMCPBootstrap(unittest.TestCase):
    def setUp(self):
        self.workspace_dir = tempfile.mkdtemp(prefix="test_bootstrap_ws_")
        self.db = SkillsDatabase()

    def tearDown(self):
        shutil.rmtree(self.workspace_dir, ignore_errors=True)

    def test_bootstrap_creates_new_files(self):
        """Test creating AGENTS.md and GEMINI.md from scratch in an empty directory"""
        agents_path = os.path.join(self.workspace_dir, "AGENTS.md")
        gemini_path = os.path.join(self.workspace_dir, "GEMINI.md")
        
        self.assertFalse(os.path.exists(agents_path))
        self.assertFalse(os.path.exists(gemini_path))

        res = self.db.bootstrap_agent_instructions(workspace_path=self.workspace_dir)
        
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["agents_md"]["action"], "created")
        self.assertEqual(res["gemini_md"]["action"], "synced_stub")
        self.assertTrue(os.path.isfile(agents_path))
        self.assertTrue(os.path.isfile(gemini_path))

        with open(agents_path, "r", encoding="utf-8") as f:
            agents_content = f.read()
        self.assertIn("PROTOCOLO DE ORQUESTRAÇÃO DE SKILLS (MCP DYNAMIC RAG)", agents_content)
        self.assertIn("route_task(task_description=\"<intenção exata>\")", agents_content)

    def test_bootstrap_idempotent_append(self):
        """Test executing bootstrap twice and verify idempotency (no duplication)"""
        agents_path = os.path.join(self.workspace_dir, "AGENTS.md")
        
        # Pre-populate existing AGENTS.md with some custom text
        with open(agents_path, "w", encoding="utf-8") as f:
            f.write("# Custom Project Guidelines\n\nSome custom instructions here.\n")

        # Run 1: Should append the protocol block
        res1 = self.db.bootstrap_agent_instructions(workspace_path=self.workspace_dir)
        self.assertEqual(res1["agents_md"]["action"], "updated_append")

        with open(agents_path, "r", encoding="utf-8") as f:
            content1 = f.read()
        self.assertIn("Custom Project Guidelines", content1)
        self.assertIn("PROTOCOLO DE ORQUESTRAÇÃO DE SKILLS (MCP DYNAMIC RAG)", content1)
        self.assertEqual(content1.count("PROTOCOLO DE ORQUESTRAÇÃO DE SKILLS"), 1)

        # Run 2: Should be unchanged
        res2 = self.db.bootstrap_agent_instructions(workspace_path=self.workspace_dir)
        self.assertEqual(res2["agents_md"]["action"], "unchanged")

        with open(agents_path, "r", encoding="utf-8") as f:
            content2 = f.read()
        self.assertEqual(content2, content1)
        self.assertEqual(content2.count("PROTOCOLO DE ORQUESTRAÇÃO DE SKILLS"), 1)

    def test_gemini_stub_content(self):
        """Validate that GEMINI.md is configured strictly as a lightweight stub pointing to AGENTS.md"""
        gemini_path = os.path.join(self.workspace_dir, "GEMINI.md")

        self.db.bootstrap_agent_instructions(workspace_path=self.workspace_dir)
        self.assertTrue(os.path.isfile(gemini_path))

        with open(gemini_path, "r", encoding="utf-8") as f:
            gemini_content = f.read()

        self.assertIn("GEMINI SYSTEM INSTRUCTIONS (SOTA RUNTIME)", gemini_content)
        self.assertIn("Single Source of Truth (SSOT)", gemini_content)
        self.assertIn("[AGENTS.md](./AGENTS.md)", gemini_content)
        self.assertIn("Orquestração MCP Obrigatória", gemini_content)
        # Should NOT be bloated with full duplicate skill tables
        self.assertLess(len(gemini_content.splitlines()), 25)

    def test_mcp_json_rpc_call(self):
        """Test full JSON-RPC 2.0 tools/call execution for bootstrap_agent_instructions"""
        rpc_req = {
            "jsonrpc": "2.0",
            "id": "test-req-123",
            "method": "tools/call",
            "params": {
                "name": "bootstrap_agent_instructions",
                "arguments": {
                    "workspace_path": self.workspace_dir
                }
            }
        }
        resp = handle_rpc_request(rpc_req, self.db)
        self.assertEqual(resp["jsonrpc"], "2.0")
        self.assertEqual(resp["id"], "test-req-123")
        self.assertIn("result", resp)
        self.assertIn("content", resp["result"])
        
        parsed_result = json.loads(resp["result"]["content"][0]["text"])
        self.assertEqual(parsed_result["status"], "success")
        self.assertTrue(os.path.isfile(os.path.join(self.workspace_dir, "AGENTS.md")))
        self.assertTrue(os.path.isfile(os.path.join(self.workspace_dir, "GEMINI.md")))

if __name__ == "__main__":
    unittest.main()
