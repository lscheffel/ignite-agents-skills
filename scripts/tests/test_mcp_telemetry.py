#!/usr/bin/env python3
"""
Unit test suite for SOTA RAG MCP Telemetry Tool (ADR-024).
Tests:
1. Initial telemetry state (uptime, zero counts, valid structure).
2. Tracking queries after search_skills / route_task.
3. Cache hit ratio calculation.
4. JSON-RPC 2.0 dispatch of get_rag_telemetry.
"""

import os
import sys
import json
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from skills_mcp_server import SkillsDatabase, handle_rpc_request, RAGTelemetryTracker

class TestMCPTelemetry(unittest.TestCase):
    def setUp(self):
        self.db = SkillsDatabase()

    def test_tracker_unit_logic(self):
        tracker = RAGTelemetryTracker()
        self.assertEqual(tracker.total_queries, 0)
        self.assertEqual(tracker.cache_hits, 0)
        self.assertEqual(tracker.cache_misses, 0)

        tracker.record_query(latency_ms=50.0, cache_hit=True, neural_call=False, scope="global")
        tracker.record_query(latency_ms=150.0, cache_hit=False, neural_call=True, scope="workspace_local")

        metrics = tracker.get_telemetry()
        self.assertEqual(metrics["total_queries"], 2)
        self.assertEqual(metrics["cache_hits"], 1)
        self.assertEqual(metrics["cache_misses"], 1)
        self.assertEqual(metrics["cache_hit_ratio_percent"], 50.0)
        self.assertEqual(metrics["average_latency_ms"], 100.0)
        self.assertEqual(metrics["scope_distribution"]["global"], 1)
        self.assertEqual(metrics["scope_distribution"]["workspace_local"], 1)

    def test_db_get_rag_telemetry(self):
        telem = self.db.get_rag_telemetry()
        self.assertIn("uptime_seconds", telem)
        self.assertIn("total_queries", telem)
        self.assertIn("cache_hit_ratio_percent", telem)
        self.assertIn("average_latency_ms", telem)
        self.assertIn("scope_distribution", telem)

    def test_search_skills_updates_telemetry(self):
        initial_queries = self.db.telemetry.total_queries
        # Execute search
        res = self.db.search_skills("test-driven development", top_k=2, use_neural=False)
        self.assertTrue(len(res) > 0)
        self.assertEqual(self.db.telemetry.total_queries, initial_queries + 1)
        
        telem = self.db.get_rag_telemetry()
        self.assertGreaterEqual(telem["total_queries"], 1)

    def test_mcp_json_rpc_dispatch_get_rag_telemetry(self):
        req = {
            "jsonrpc": "2.0",
            "id": 99,
            "method": "tools/call",
            "params": {
                "name": "get_rag_telemetry",
                "arguments": {}
            }
        }
        res = handle_rpc_request(req, self.db)
        self.assertIsNotNone(res)
        self.assertEqual(res.get("id"), 99)
        self.assertIn("result", res)
        self.assertIn("content", res["result"])
        payload = json.loads(res["result"]["content"][0]["text"])
        self.assertIn("uptime_seconds", payload)
        self.assertIn("total_queries", payload)

if __name__ == "__main__":
    unittest.main()
