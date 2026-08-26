#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
UNIT TESTS: CATALOG TRANSLATION & SYNTAX PRESERVATION (ADR-026)
================================================================================
Testes unitários offline para o pipeline de tradução do catálogo canônico:
- Detecção de idioma determinística (Stopwords)
- Preservação e restauração de sintaxe (Code blocks, Frontmatter, XML, Inline code)
- Isolamento de comentários protegidos vs traduzíveis
- Validação estática de AST Python e Shell syntax
- Cache SQLite de idempotência versionado
================================================================================
"""

import ast
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

# Adicionar diretório pai para importação
SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

import translate_catalog_nim as tc


class TestCatalogTranslationUnit(unittest.TestCase):
    """Testes unitários offline para funções puras do pipeline de tradução."""

    def test_01_language_detection_pt(self):
        """Valida que textos em português são detectados como 'pt'."""
        pt_text = (
            "Esta função executa a auditoria estrutural do repositório de skills, "
            "verificando se o arquivo de configuração e as diretrizes de governança "
            "estão em conformidade com o padrão estabelecido."
        )
        self.assertEqual(tc.detect_language(pt_text), "pt")

    def test_02_language_detection_en(self):
        """Valida que textos em inglês são detectados como 'en'."""
        en_text = (
            "This function executes the structural audit of the skills repository, "
            "verifying that the configuration file and governance guidelines "
            "are compliant with the standard requirements."
        )
        self.assertEqual(tc.detect_language(en_text), "en")

    def test_03_language_detection_unknown_or_empty(self):
        """Valida comportamento para strings vazias ou sem stopwords reconhecidas."""
        self.assertEqual(tc.detect_language(""), "unknown")
        self.assertEqual(tc.detect_language("12345 67890 + = ()"), "unknown")

    def test_04_protect_and_restore_code_blocks(self):
        """Valida que blocos de código com cercas (```...```) são protegidos e restaurados perfeitamente."""
        content = (
            "# Introdução\n\n"
            "Aqui está um exemplo de código:\n\n"
            "```python\n"
            "def calculate_metrics(data):\n"
            "    # Não traduzir variáveis\n"
            "    return {'score': 100}\n"
            "```\n\n"
            "Texto após o bloco de código.\n"
        )
        protected, placeholders = tc.protect_syntax(content)
        self.assertIn("@@CODE_BLOCK_0@@", protected)
        self.assertNotIn("def calculate_metrics", protected)

        # Simula tradução apenas do texto livre
        translated_sim = protected.replace("Aqui está um exemplo de código:", "Here is a code example:").replace(
            "Texto após o bloco de código.", "Text after code block."
        )
        restored = tc.restore_syntax(translated_sim, placeholders)

        self.assertIn("Here is a code example:", restored)
        self.assertIn("def calculate_metrics(data):", restored)
        self.assertIn("Text after code block.", restored)
        self.assertNotIn("@@CODE_BLOCK_0@@", restored)

    def test_05_protect_and_restore_frontmatter(self):
        """Valida que o frontmatter YAML é protegido e preservado intacto."""
        content = (
            "---\n"
            "name: my-sample-skill\n"
            "version: 1.0.0\n"
            "description: Descrição da skill\n"
            "---\n\n"
            "# Título Principal\n"
            "Corpo do documento em português.\n"
        )
        protected, placeholders = tc.protect_syntax(content)
        self.assertTrue(protected.startswith("@@FRONTMATTER_0@@"))
        self.assertNotIn("name: my-sample-skill", protected)

        restored = tc.restore_syntax(protected, placeholders)
        self.assertEqual(restored, content)

    def test_06_protect_and_restore_xml_tags_and_inline_code(self):
        """Valida proteção de tags XML (<tag>) e inline code (`code`)."""
        content = (
            "Use a tag <active_skill id=\"sample\"> para carregar a skill "
            "e execute `python3 .github/scripts/audit_engine.py` no terminal."
        )
        protected, placeholders = tc.protect_syntax(content)
        self.assertIn("@@XML_TAG_", protected)
        self.assertIn("@@INLINE_CODE_", protected)
        self.assertNotIn("<active_skill", protected)
        self.assertNotIn("`python3", protected)

        restored = tc.restore_syntax(protected, placeholders)
        self.assertEqual(restored, content)

    def test_07_roundtrip_idempotency(self):
        """Valida que protect -> restore sem alteração preserva 100% da integridade."""
        raw_doc = (
            "---\n"
            "id: SAMPLE-001\n"
            "type: doc\n"
            "---\n\n"
            "# Heading 1\n"
            "Parágrafo com `<tag id='1'>` e `inline_var`.\n\n"
            "```bash\n"
            "echo 'hello world'\n"
            "```\n"
        )
        protected, placeholders = tc.protect_syntax(raw_doc)
        restored = tc.restore_syntax(protected, placeholders)
        self.assertEqual(restored, raw_doc)

    def test_08_protected_comments_identification(self):
        """Valida identificação de diretivas de máquina em comentários."""
        self.assertTrue(tc.is_protected_comment("# parent_skill_id: test-skill"))
        self.assertTrue(tc.is_protected_comment("# type: ignore"))
        self.assertTrue(tc.is_protected_comment("# noqa: F401"))
        self.assertTrue(tc.is_protected_comment("# pragma: no cover"))
        self.assertTrue(tc.is_protected_comment("#!/usr/bin/env python3"))
        self.assertFalse(tc.is_protected_comment("# Esta é uma função utilitária para cálculo de métricas"))

    def test_09_static_validation_python_ast(self):
        """Valida o gate estático AST de Python."""
        valid_code = "def foo(x: int) -> int:\n    return x * 2\n"
        ok, msg = tc.validate_python_ast(valid_code)
        self.assertTrue(ok)

        invalid_code = "def foo(x:\n    return x *\n"
        ok, msg = tc.validate_python_ast(invalid_code)
        self.assertFalse(ok)
        self.assertIn("SyntaxError", msg)

    def test_10_static_validation_shell_syntax(self):
        """Valida o gate estático de sintaxe Shell."""
        valid_sh = "#!/bin/bash\nif [ \"$1\" == \"test\" ]; then\n    echo ok\nfi\n"
        ok, msg = tc.validate_shell_syntax(valid_sh)
        self.assertTrue(ok)

        invalid_sh = "#!/bin/bash\nif [ \"$1\" == \"test\" ]; then\n    echo ok\n"  # Faltando fi
        ok, msg = tc.validate_shell_syntax(invalid_sh)
        self.assertFalse(ok)

    def test_11_sqlite_cache_versioning_and_crud(self):
        """Valida inicialização, chaveamento versionado e operações de cache SQLite."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmproot = Path(tmpdir)
            conn = tc.init_cache(tmproot)

            key1 = tc.get_cache_key("Texto de teste em português", "nvidia/riva-translate-4b-instruct-v2")
            key2 = tc.get_cache_key("Texto de teste em português", "meta/llama-3.1-8b-instruct")
            
            # Modelos diferentes geram chaves diferentes
            self.assertNotEqual(key1, key2)

            # Miss inicial
            self.assertIsNone(tc.get_cached_translation(conn, key1))

            # Store e Hit
            tc.store_cached_translation(
                conn, key1, "Texto de teste em português", "Test text in English", "nvidia/riva-translate-4b-instruct-v2"
            )
            cached = tc.get_cached_translation(conn, key1)
            self.assertEqual(cached, "Test text in English")

    def test_12_token_bpe_estimation(self):
        """Valida cálculo determinístico da contagem aproximada de tokens BPE."""
        pt_sample = "Configuração e execução de padrões de arquitetura."
        en_sample = "Configuration and execution of architecture patterns."
        
        tokens_pt = tc.estimate_bpe_tokens(pt_sample)
        tokens_en = tc.estimate_bpe_tokens(en_sample)
        
        self.assertGreater(tokens_pt, 0)
        self.assertGreater(tokens_en, 0)


if __name__ == "__main__":
    unittest.main()
