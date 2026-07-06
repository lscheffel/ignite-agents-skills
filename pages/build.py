#!/usr/bin/env python3
"""
Build script: generates HTML pages from skills/index.json and SKILL.md files.

Zero external dependencies — pure Python 3 markdown-to-HTML converter.

Usage:
    python3 pages/build.py

Output:
    pages/
    ├── index.html                  (skills listing)
    └── skills/
        └── {skill-name}/
            ├── index.html          (SKILL.md rendered)
            ├── templates/
            │   └── {file}.html     (template rendered)
            └── examples/
                └── {file}.html     (example rendered)
"""

import json
import os
import re
import html
import sys
from pathlib import Path
from datetime import datetime

# ─── Paths ──────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
INDEX_JSON = SKILLS_DIR / "index.json"
PAGES_DIR = ROOT / "pages"
DOCS_DIR = ROOT / "docs"
ADR_ARCHIVE_DIR = DOCS_DIR / "adr" / "archive"
THEME_VERSION = "2.3.0"


# ═══════════════════════════════════════════════════════════════════════════════
# MARKDOWN → HTML CONVERTER (pure Python, zero deps)
# ═══════════════════════════════════════════════════════════════════════════════

def md_escape(text):
    return html.escape(text)


def convert_inline_md(text, depth=1):
    """Convert inline markdown: bold, italic, code, links, images.
    
    Args:
        text: Markdown text to convert
        depth: Directory depth from pages/ root
               1 = pages/readme.html (use adr/, skills/)
               2 = pages/skills/name/index.html (use ../../adr/, ../../skills/)
               3 = pages/skills/name/category/file.html (use ../../../adr/)
    """
    # Calculate prefix for relative paths
    # depth=1 means page is at pages/XXX.html, so links are adr/, skills/ (no prefix)
    # depth=2 means page is at pages/skills/name/index.html, so links need ../../
    # depth=3 means page is at pages/skills/name/category/file.html, so links need ../../../
    prefix = "../" * (depth - 1) if depth > 1 else ""
    
    # Images ![alt](url)
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1" style="max-width:100%;border-radius:8px;">', text)
    # Links [text](url) - convert all .md links to .html
    def convert_link(match):
        link_text = match.group(1)
        link_url = match.group(2)
        # Skip external links (http, https, etc)
        if link_url.startswith(('http://', 'https://', 'mailto:', '#')):
            return f'<a href="{link_url}">{link_text}</a>'
        # Convert ADR INDEX.md link (./docs/adr/ or docs/adr/INDEX.md)
        if link_url.endswith('docs/adr/INDEX.md') or link_url == './docs/adr/' or link_url == 'docs/adr/':
            return f'<a href="{prefix}adr/index.html">{link_text}</a>'
        # Convert ADR archive links (docs/adr/archive/ADR-XXX.md)
        if 'docs/adr/archive/ADR-' in link_url and link_url.endswith('.md'):
            adr_name = link_url.split('/')[-1].replace('.md', '.html')
            return f'<a href="{prefix}adr/{adr_name}">{link_text}</a>'
        elif 'docs/adr/ADR-' in link_url and link_url.endswith('.md'):
            adr_name = link_url.split('/')[-1].replace('.md', '.html')
            return f'<a href="{prefix}adr/{adr_name}">{link_text}</a>'
        # Convert skill SKILL.md links (skills/name/SKILL.md)
        elif link_url.endswith('SKILL.md'):
            parts = link_url.split('/')
            skill_name = parts[-2] if len(parts) >= 2 else ''
            if skill_name:
                return f'<a href="{prefix}skills/{skill_name}/index.html">{link_text}</a>'
        # Convert skill template/example/checklist links (skills/name/category/file.md)
        elif '/skills/' in link_url and link_url.endswith('.md'):
            parts = link_url.split('/')
            skill_name = parts[-3] if len(parts) >= 3 else ''
            category = parts[-2] if len(parts) >= 2 else ''
            file_name = parts[-1].replace('.md', '.html')
            if skill_name and category:
                return f'<a href="{prefix}skills/{skill_name}/{category}/{file_name}">{link_text}</a>'
        # Convert root .md files (README.md, USAGE.md, etc)
        elif link_url.endswith('.md') and '/' not in link_url:
            return f'<a href="{link_url.replace(".md", ".html")}">{link_text}</a>'
        # Default: keep original link
        return f'<a href="{link_url}">{link_text}</a>'
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', convert_link, text)
    # Inline code `code`
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # Bold **text**
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    # Italic *text*
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    # Strikethrough ~~text~~
    text = re.sub(r'~~([^~]+)~~', r'<del>\1</del>', text)
    return text


def convert_md_to_html(md_text, depth=1):
    """Convert markdown text to HTML body content.
    
    Args:
        md_text: Markdown text to convert
        depth: Directory depth from pages/ root (1 for readme.html, 2 for skills/name/index.html)
    """
    lines = md_text.split('\n')
    html_parts = []
    i = 0
    in_list = False
    list_type = None  # 'ul' or 'ol'
    in_table = False
    table_rows = []
    in_blockquote = False
    blockquote_lines = []

    def close_list():
        nonlocal in_list, list_type
        if in_list:
            html_parts.append(f'</{list_type}>')
            in_list = False
            list_type = None

    def close_table():
        nonlocal in_table, table_rows
        if in_table:
            html_parts.append(render_table(table_rows))
            in_table = False
            table_rows = []

    def close_blockquote():
        nonlocal in_blockquote, blockquote_lines
        if in_blockquote:
            content = convert_inline_md('\n'.join(blockquote_lines), depth)
            html_parts.append(f'<blockquote>{content}</blockquote>')
            in_blockquote = False
            blockquote_lines = []

    while i < len(lines):
        line = lines[i]

        # Fenced code block
        if line.strip().startswith('```'):
            close_list()
            close_table()
            close_blockquote()
            lang = line.strip()[3:].strip()
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            i += 1  # skip closing ```
            code = md_escape('\n'.join(code_lines))
            lang_attr = f' data-lang="{lang}"' if lang else ''
            html_parts.append(f'<pre{lang_attr}><code>{code}</code></pre>')
            continue

        # Table row
        if '|' in line and line.strip().startswith('|'):
            close_list()
            close_blockquote()
            stripped = line.strip()
            # Check if separator row (|---|---|)
            if re.match(r'^\|[\s\-:|]+\|$', stripped):
                i += 1
                continue
            cells = [c.strip() for c in stripped.split('|')[1:-1]]
            if not in_table:
                in_table = True
                table_rows = []
            table_rows.append(cells)
            i += 1
            continue
        else:
            close_table()

        # Heading
        m = re.match(r'^(#{1,6})\s+(.*)', line)
        if m:
            close_list()
            close_blockquote()
            level = len(m.group(1))
            text = convert_inline_md(m.group(2), depth)
            anchor = re.sub(r'[^a-z0-9-]', '', m.group(2).lower().replace(' ', '-'))
            html_parts.append(f'<h{level} id="{anchor}">{text}</h{level}>')
            i += 1
            continue

        # Horizontal rule
        if re.match(r'^(\*{3,}|-{3,}|_{3,})\s*$', line.strip()):
            close_list()
            close_blockquote()
            html_parts.append('<hr>')
            i += 1
            continue

        # Blockquote
        if line.strip().startswith('>'):
            close_list()
            close_table()
            content = line.strip()[1:].strip()
            if not in_blockquote:
                in_blockquote = True
                blockquote_lines = []
            blockquote_lines.append(content)
            i += 1
            continue
        else:
            close_blockquote()

        # Unordered list
        m = re.match(r'^(\s*)[-*+]\s+(.*)', line)
        if m:
            close_table()
            close_blockquote()
            content = convert_inline_md(m.group(2), depth)
            if not in_list or list_type != 'ul':
                close_list()
                in_list = True
                list_type = 'ul'
                html_parts.append('<ul>')
            html_parts.append(f'<li>{content}</li>')
            i += 1
            continue

        # Ordered list
        m = re.match(r'^(\s*)\d+\.\s+(.*)', line)
        if m:
            close_table()
            close_blockquote()
            content = convert_inline_md(m.group(2), depth)
            if not in_list or list_type != 'ol':
                close_list()
                in_list = True
                list_type = 'ol'
                html_parts.append('<ol>')
            html_parts.append(f'<li>{content}</li>')
            i += 1
            continue

        # Empty line
        if not line.strip():
            close_list()
            close_blockquote()
            i += 1
            continue

        # Default: paragraph
        close_list()
        close_blockquote()
        para_lines = []
        while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith('#') and not lines[i].strip().startswith('```') and not lines[i].strip().startswith('|') and not lines[i].strip().startswith('>') and not re.match(r'^[-*+]\s', lines[i].strip()) and not re.match(r'^\d+\.\s', lines[i].strip()):
            para_lines.append(lines[i])
            i += 1
        if para_lines:
            text = convert_inline_md(' '.join(l.strip() for l in para_lines), depth)
            html_parts.append(f'<p>{text}</p>')
        continue

    close_list()
    close_table()
    close_blockquote()

    return '\n'.join(html_parts)


def render_table(rows):
    """Render a table from list of row cell lists."""
    if not rows:
        return ''
    html = '<div class="table-wrapper"><table>'
    for idx, row in enumerate(rows):
        tag = 'th' if idx == 0 else 'td'
        html += '<tr>'
        for cell in row:
            html += f'<{tag}>{convert_inline_md(cell)}</{tag}>'
        html += '</tr>'
    html += '</table></div>'
    return html


# ═══════════════════════════════════════════════════════════════════════════════
# HTML TEMPLATE
# ═══════════════════════════════════════════════════════════════════════════════

def get_css():
    return """
    :root {
      --bg-primary: #1a1a2e;
      --bg-secondary: #16213e;
      --bg-card: #1e2a3a;
      --bg-card-hover: #253447;
      --accent: #ff6b2b;
      --accent-glow: rgba(255, 107, 43, 0.25);
      --text-primary: #f0f0f0;
      --text-secondary: #a0aec0;
      --text-muted: #6b7a8d;
      --border: #2d3a4a;
      --tag-bg: rgba(255, 107, 43, 0.12);
      --tag-border: rgba(255, 107, 43, 0.3);
      --code-bg: #0d1117;
      --code-border: #21262d;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: var(--bg-primary);
      color: var(--text-primary);
      line-height: 1.7;
    }
    a { color: var(--accent); text-decoration: none; transition: color 0.2s; }
    a:hover { color: #ff8f5a; }

    /* ── Nav ── */
    .nav {
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(26, 26, 46, 0.92);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border);
      padding: 0.75rem 2rem;
      display: flex;
      align-items: center;
      gap: 1.5rem;
    }
    .nav-brand {
      font-weight: 800;
      font-size: 1rem;
      color: var(--text-primary);
      white-space: nowrap;
    }
    .nav-brand .accent { color: var(--accent); }
    .nav-links {
      display: flex;
      gap: 1rem;
      flex-wrap: wrap;
      font-size: 0.85rem;
    }
    .nav-links a {
      color: var(--text-secondary);
      padding: 4px 10px;
      border-radius: 6px;
      transition: all 0.2s;
    }
    .nav-links a:hover, .nav-links a.active {
      color: var(--accent);
      background: var(--tag-bg);
    }
    .nav-breadcrumb {
      margin-left: auto;
      font-size: 0.8rem;
      color: var(--text-muted);
    }
    .nav-breadcrumb a { color: var(--text-muted); }
    .nav-breadcrumb a:hover { color: var(--accent); }

    /* ── Content ── */
    .content {
      max-width: 900px;
      margin: 0 auto;
      padding: 2.5rem 2rem 4rem;
    }
    .content-full {
      max-width: 1200px;
    }

    /* ── Typography ── */
    h1 {
      font-size: 2.2rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      margin-bottom: 0.5rem;
      color: var(--text-primary);
    }
    h1 .accent { color: var(--accent); }
    .subtitle {
      color: var(--text-secondary);
      font-size: 1.1rem;
      margin-bottom: 2rem;
    }
    /* ── Fancy title ── */
    .fancy-title {
      font-size: 2.8rem;
      font-weight: 900;
      letter-spacing: -0.03em;
      margin-bottom: 0.25rem;
      background: linear-gradient(135deg, #ff6b2b 0%, #ff9b6a 40%, #ffffff 80%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      line-height: 1.2;
    }
    .fancy-title .ver {
      font-size: 0.45em;
      font-weight: 600;
      letter-spacing: 0;
      background: linear-gradient(135deg, #ff6b2b, #ff9b6a);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      vertical-align: middle;
      margin-left: 0.3em;
      border: 1px solid rgba(255,107,43,0.4);
      padding: 0.1em 0.5em;
      border-radius: 8px;
      position: relative;
      top: -0.1em;
    }
    .fancy-sub {
      font-size: 1.05rem;
      color: var(--text-secondary);
      margin-bottom: 2rem;
      line-height: 1.6;
    }
    .fancy-sub strong { color: var(--accent); }
    h2 {
      font-size: 1.5rem;
      font-weight: 700;
      margin: 2.5rem 0 1rem;
      padding-bottom: 0.5rem;
      border-bottom: 1px solid var(--border);
      color: var(--text-primary);
    }
    h3 {
      font-size: 1.2rem;
      font-weight: 600;
      margin: 2rem 0 0.75rem;
      color: var(--text-primary);
    }
    h4 { font-size: 1.05rem; font-weight: 600; margin: 1.5rem 0 0.5rem; color: var(--text-primary); }
    p { margin-bottom: 1rem; color: var(--text-secondary); }
    strong { color: var(--text-primary); }

    /* ── Tags ── */
    .tags { display: flex; flex-wrap: wrap; gap: 6px; margin: 1rem 0; }
    .tag {
      font-size: 0.75rem;
      padding: 3px 10px;
      border-radius: 6px;
      background: var(--tag-bg);
      border: 1px solid var(--tag-border);
      color: var(--accent);
      font-weight: 500;
    }
    .version-badge {
      display: inline-block;
      background: var(--accent);
      color: #fff;
      padding: 3px 12px;
      border-radius: 16px;
      font-size: 0.8rem;
      font-weight: 600;
      vertical-align: middle;
      margin-left: 8px;
    }

    /* ── Code ── */
    pre {
      background: var(--code-bg);
      border: 1px solid var(--code-border);
      border-radius: 8px;
      padding: 1.2rem;
      overflow-x: auto;
      margin: 1rem 0;
      position: relative;
    }
    pre code {
      font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
      font-size: 0.88rem;
      line-height: 1.6;
      color: #e6edf3;
      background: none;
      padding: 0;
      border: none;
      border-radius: 0;
    }
    pre::before {
      content: attr(data-lang);
      position: absolute;
      top: 8px;
      right: 12px;
      font-size: 0.7rem;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    code {
      font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
      font-size: 0.88em;
      background: var(--code-bg);
      border: 1px solid var(--code-border);
      padding: 2px 6px;
      border-radius: 4px;
      color: #ff9b6a;
    }

    /* ── Lists ── */
    ul, ol {
      margin: 0.75rem 0 1rem 1.5rem;
      color: var(--text-secondary);
    }
    li { margin-bottom: 0.4rem; }
    li::marker { color: var(--accent); }

    /* ── Tables ── */
    .table-wrapper { overflow-x: auto; margin: 1rem 0; }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.9rem;
    }
    th, td {
      padding: 10px 14px;
      text-align: left;
      border-bottom: 1px solid var(--border);
    }
    th {
      background: var(--bg-card);
      color: var(--text-primary);
      font-weight: 600;
      white-space: nowrap;
    }
    td { color: var(--text-secondary); }
    tr:hover td { background: rgba(255,255,255,0.02); }

    /* ── Blockquote ── */
    blockquote {
      border-left: 3px solid var(--accent);
      padding: 0.75rem 1.25rem;
      margin: 1rem 0;
      background: rgba(255, 107, 43, 0.05);
      border-radius: 0 8px 8px 0;
      color: var(--text-secondary);
    }
    blockquote p { margin-bottom: 0; }

    /* ── HR ── */
    hr {
      border: none;
      border-top: 1px solid var(--border);
      margin: 2rem 0;
    }

    /* ── Cards ── */
    .card-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 1rem;
      margin: 1.5rem 0;
    }
    .card {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 1.25rem;
      transition: all 0.25s;
    }
    .card::before {
      content: '';
      display: block;
      width: 3px;
      height: 0;
      background: var(--accent);
      border-radius: 2px;
      margin-bottom: 0;
      transition: all 0.25s;
    }
    .card:hover {
      border-color: var(--accent);
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    }
    .card:hover::before {
      height: 3px;
      margin-bottom: 12px;
    }
    .card-title {
      font-weight: 700;
      font-size: 1rem;
      margin-bottom: 0.5rem;
    }
    .card-title a { color: var(--text-primary); }
    .card-title a:hover { color: var(--accent); }
    .card-desc {
      font-size: 0.85rem;
      color: var(--text-secondary);
      margin-bottom: 0.75rem;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
    .card-meta {
      font-size: 0.75rem;
      color: var(--text-muted);
    }

    /* ── File list ── */
    .file-list {
      list-style: none;
      margin: 1rem 0;
      padding: 0;
    }
    .file-list li {
      margin: 0;
      padding: 10px 16px;
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      gap: 10px;
      transition: background 0.15s;
    }
    .file-list li:hover {
      background: rgba(255,255,255,0.03);
    }
    .file-list li:last-child { border-bottom: none; }
    .file-icon {
      width: 20px;
      text-align: center;
      flex-shrink: 0;
    }
    .file-list a { font-weight: 500; }
    .file-size {
      margin-left: auto;
      font-size: 0.75rem;
      color: var(--text-muted);
    }

    /* ── Footer ── */
    footer {
      border-top: 1px solid var(--border);
      padding: 2rem;
      text-align: center;
      color: var(--text-muted);
      font-size: 0.82rem;
    }
    footer a { color: var(--accent); }

    /* ── Search ── */
    .search-wrapper {
      position: relative;
      max-width: 500px;
      margin: 0 auto 2rem;
    }
    .search-wrapper input {
      width: 100%;
      padding: 12px 16px 12px 44px;
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 10px;
      color: var(--text-primary);
      font-size: 0.95rem;
      outline: none;
      transition: border-color 0.2s, box-shadow 0.2s;
    }
    .search-wrapper input::placeholder { color: var(--text-muted); }
    .search-wrapper input:focus {
      border-color: var(--accent);
      box-shadow: 0 0 0 3px var(--accent-glow);
    }
    .search-icon {
      position: absolute;
      left: 14px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
    }

    /* ── Responsive ── */
    @media (max-width: 768px) {
      .nav { padding: 0.75rem 1rem; gap: 0.75rem; }
      .content { padding: 1.5rem 1rem; }
      h1 { font-size: 1.6rem; }
      .card-grid { grid-template-columns: 1fr; }
    }
    """


def get_page_template(title, body_html, breadcrumb="", nav_active=""):
    css = get_css()
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{md_escape(title)} — ignite-agents-skills</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <style>{css}</style>
</head>
<body>
  <nav class="nav">
    <a href="../../index.html" class="nav-brand"><span class="accent">ignite</span>-agents-skills</a>
    <div class="nav-links">
      <a href="../../index.html"{ ' class="active"' if nav_active == "home" else ""}>Skills</a>
      <a href="../../readme.html"{ ' class="active"' if nav_active == "readme" else ""}>README</a>
      <a href="../../usage.html"{ ' class="active"' if nav_active == "usage" else ""}>USAGE</a>
    </div>
    <div class="nav-breadcrumb">{breadcrumb}</div>
  </nav>
  <div class="content">
    {body_html}
  </div>
<footer>
     <p><strong>ignite-agents-skills</strong> v{THEME_VERSION} &mdash; 23 skills &middot; 72 templates &middot; 18 examples &middot; 12 ADRs</p>
     <p style="margin-top:0.4rem"><a href="https://github.com/lscheffel/ignite-agents-skills">github.com/lscheffel/ignite-agents-skills</a></p>
   </footer>
</body>
</html>"""


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE GENERATORS
# ═══════════════════════════════════════════════════════════════════════════════

def generate_skill_page(skill, skill_dir):
    """Generate the main page for a skill (SKILL.md rendered)."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return

    md_content = skill_md.read_text(encoding="utf-8")
    # depth=3 because page is at pages/skills/name/index.html (3 levels from pages/ root)
    body_html = convert_md_to_html(md_content, depth=3)

    # Build file lists for templates and examples
    templates = sorted((skill_dir / "templates").glob("*")) if (skill_dir / "templates").exists() else []
    examples = sorted((skill_dir / "examples").glob("*")) if (skill_dir / "examples").exists() else []
    checklists = sorted((skill_dir / "checklists").glob("*")) if (skill_dir / "checklists").exists() else []

    files_section = ""

    if templates or examples or checklists:
        files_section += '<h2 id="files">Arquivos</h2>\n'

    if templates:
        files_section += '<h3>Templates</h3>\n<ul class="file-list">\n'
        for f in templates:
            if f.suffix == '.md':
                files_section += f'  <li><span class="file-icon">&#128196;</span><a href="templates/{f.stem}.html">{f.name}</a></li>\n'
        files_section += '</ul>\n'

    if examples:
        files_section += '<h3>Examples</h3>\n<ul class="file-list">\n'
        for f in examples:
            if f.suffix == '.md':
                files_section += f'  <li><span class="file-icon">&#128196;</span><a href="examples/{f.stem}.html">{f.name}</a></li>\n'
        files_section += '</ul>\n'

    if checklists:
        files_section += '<h3>Checklists</h3>\n<ul class="file-list">\n'
        for f in checklists:
            if f.suffix == '.md':
                files_section += f'  <li><span class="file-icon">&#9745;</span><a href="checklists/{f.stem}.html">{f.name}</a></li>\n'
        files_section += '</ul>\n'

    body_html += '\n' + files_section

    breadcrumb = f'<a href="../../index.html">Skills</a> &rsaquo; {skill["name"]}'
    page = get_page_template(skill["name"], body_html, breadcrumb=breadcrumb, nav_active="home")

    out = PAGES_DIR / "skills" / skill["name"] / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"  ✓ {skill['name']}/index.html")


def generate_file_page(skill_name, md_path, category, skill):
    """Generate an HTML page for a template/example/checklist .md file."""
    md_content = md_path.read_text(encoding="utf-8")
    # depth=4 because page is at pages/skills/name/category/file.html (4 levels from pages/ root)
    body_html = convert_md_to_html(md_content, depth=4)

    breadcrumb = (
        f'<a href="../../../index.html">Skills</a> &rsaquo; '
        f'<a href="../index.html">{skill_name}</a> &rsaquo; '
        f'{category} &rsaquo; {md_path.stem}'
    )

    title = f"{skill_name} / {category} / {md_path.stem}"
    page = get_page_template(title, body_html, breadcrumb=breadcrumb)

    out = PAGES_DIR / "skills" / skill_name / category / f"{md_path.stem}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"  ✓ {skill_name}/{category}/{md_path.stem}.html")


def generate_doc_page(md_path, title, nav_active):
    """Generate an HTML page for a root-level .md file (README, USAGE)."""
    if not md_path.exists():
        print(f"  ⚠ {md_path.name} not found, skipping")
        return
    md_content = md_path.read_text(encoding="utf-8")
    body_html = convert_md_to_html(md_content, depth=1)
    breadcrumb = title
    page = get_page_template(title, body_html, breadcrumb=breadcrumb, nav_active=nav_active)
    out_name = f"{md_path.stem.lower()}.html"
    out = PAGES_DIR / out_name
    out.write_text(page, encoding="utf-8")
    print(f"  ✓ {out_name}")


def generate_adr_page(md_path, adr_name):
    """Generate an HTML page for an ADR .md file."""
    if not md_path.exists():
        return
    md_content = md_path.read_text(encoding="utf-8")
    body_html = convert_md_to_html(md_content)
    breadcrumb = f'<a href="../index.html">Páginas</a> &rsaquo; <a href="index.html">ADRs</a> &rsaquo; {adr_name}'
    title = f"ADR — {adr_name}"
    page = get_page_template(title, body_html, breadcrumb=breadcrumb, nav_active="adr")
    out = PAGES_DIR / "adr" / f"{adr_name}"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"  ✓ adr/{adr_name}")


def generate_adr_index(adrs):
    """Generate the ADR index page."""
    cards_html = ""
    for adr in sorted(adrs, key=lambda x: x["name"]):
        cards_html += f"""
    <div class="card">
      <div class="card-title"><a href="{adr['name']}">{adr['name']}</a></div>
      <div class="card-desc">{md_escape(adr.get('title', ''))}</div>
    </div>"""

    body = f"""
    <h1 class="fancy-title">ADRs <span class="ver">Archive</span></h1>
    <p class="fancy-sub">Architecture Decision Records arquivadas (implementadas).</p>

    <h2 id="adrs">ADRs Disponíveis</h2>
    <div class="card-grid">
      {cards_html}
    </div>

    <footer style="margin-top:3rem">
      <p><strong>ignite-agents-skills</strong> &mdash; <a href="../index.html">Voltar para Skills</a></p>
    </footer>
  """

    css = get_css()
    page = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ADRs — ignite-agents-skills</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <style>{css}</style>
</head>
<body>
  <nav class="nav">
    <a href="../index.html" class="nav-brand"><span class="accent">ignite</span>-agents-skills</a>
    <div class="nav-links">
      <a href="../index.html">Skills</a>
      <a href="../readme.html">README</a>
      <a href="../usage.html">USAGE</a>
      <a href="index.html" class="active">ADRs</a>
    </div>
  </nav>
  <div class="content content-full">
    {body}
  </div>
</body>
</html>"""

    out = PAGES_DIR / "adr" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"  ✓ adr/index.html")


def generate_index(skills_data):
    """Generate the main pages/index.html listing all skills."""
    skills = skills_data["skills"]

    cards_html = ""
    for s in sorted(skills, key=lambda x: x["name"]):
        tags_html = " ".join(f'<span class="tag">{t}</span>' for t in s.get("tags", [])[:4])
        file_count = len(s.get("files", []))
        cards_html += f"""
    <div class="card">
      <div class="card-title"><a href="skills/{s['name']}/index.html">{s['name']}</a> <span class="version-badge">v{s.get('version', '?')}</span></div>
      <div class="card-desc">{md_escape(s.get('description', ''))}</div>
      <div class="tags">{tags_html}</div>
      <div class="card-meta">{file_count} files &middot; <a href="skills/{s['name']}/index.html">Ver SKILL.md &rarr;</a></div>
    </div>"""

    body = f"""
    <h1 class="fancy-title">ignite-agents-skills <span class="ver">v{THEME_VERSION}</span></h1>
    <p class="fancy-sub">Registro centralizado de <strong>23 skills</strong> ultra-high quality grade para agentes de IA compatíveis com o padrão <a href="https://agentskills.io">Agent Skills</a>.</p>

    <div class="search-wrapper">
      <span class="search-icon">&#128269;</span>
      <input type="text" id="search" placeholder="Buscar skill por nome, tag ou descrição..." autocomplete="off">
    </div>

    <h2 id="skills">Skills</h2>
    <div class="card-grid" id="skill-grid">
      {cards_html}
    </div>

<footer style="margin-top:3rem">
       <p><strong>ignite-agents-skills</strong> v{THEME_VERSION} &mdash; 23 skills &middot; 72 templates &middot; 18 examples &middot; 12 ADRs</p>
       <p style="margin-top:0.4rem"><a href="https://github.com/lscheffel/ignite-agents-skills">github.com/lscheffel/ignite-agents-skills</a></p>
     </footer>

    <script>
    const searchInput = document.getElementById('search');
    const grid = document.getElementById('skill-grid');
    const cards = Array.from(grid.querySelectorAll('.card'));
    searchInput.addEventListener('input', () => {{
      const q = searchInput.value.toLowerCase().trim();
      cards.forEach(card => {{
        const text = card.textContent.toLowerCase();
        card.style.display = !q || text.includes(q) ? '' : 'none';
      }});
    }});
    </script>
  </body>
</html>"""

    css = get_css()
    page = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ignite-agents-skills — Skill Registry</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <style>{css}</style>
</head>
<body>
  <nav class="nav">
    <a href="../index.html" class="nav-brand"><span class="accent">ignite</span>-agents-skills</a>
    <div class="nav-links">
      <a href="index.html" class="active">Skills</a>
      <a href="readme.html">README</a>
      <a href="usage.html">USAGE</a>
    </div>
  </nav>
  <div class="content content-full">
    {body}
  </div>
</body>
</html>"""

    out = PAGES_DIR / "index.html"
    out.write_text(page, encoding="utf-8")
    print(f"  ✓ pages/index.html")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    print("🔥 Building pages from skills/index.json ...")

    if not INDEX_JSON.exists():
        print(f"ERROR: {INDEX_JSON} not found", file=sys.stderr)
        sys.exit(1)

    data = json.loads(INDEX_JSON.read_text(encoding="utf-8"))
    skills = data.get("skills", [])
    print(f"   Found {len(skills)} skills\n")

    # Clean output
    if PAGES_DIR.exists():
        import shutil
        # Remove old generated pages but keep build.py
        for item in PAGES_DIR.iterdir():
            if item.name == "build.py":
                continue
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()

    # Generate index
    print("📄 Generating index...")
    generate_index(data)

    # Generate README and USAGE pages
    print("\n📖 Generating doc pages...")
    generate_doc_page(ROOT / "README.md", "README", "readme")
    generate_doc_page(ROOT / "USAGE.md", "USAGE", "usage")

    # Generate ADR pages
    print("\n📋 Generating ADR pages...")
    adr_files = sorted(ADR_ARCHIVE_DIR.glob("ADR-*.md")) if ADR_ARCHIVE_DIR.exists() else []
    adrs = []
    for adr_file in adr_files:
        adr_name = adr_file.stem + ".html"
        adrs.append({"name": adr_name, "title": adr_file.stem})
        generate_adr_page(adr_file, adr_name)
    if adrs:
        generate_adr_index(adrs)

    # Generate skill pages + sub-pages
    for s in sorted(skills, key=lambda x: x["name"]):
        skill_dir = SKILLS_DIR / s["name"]
        if not skill_dir.exists():
            print(f"  ⚠ {s['name']}: directory not found, skipping")
            continue

        print(f"\n🛠  {s['name']}...")
        generate_skill_page(s, skill_dir)

        # Templates
        for md_file in sorted((skill_dir / "templates").glob("*.md")) if (skill_dir / "templates").exists() else []:
            generate_file_page(s["name"], md_file, "templates", s)

        # Examples
        for md_file in sorted((skill_dir / "examples").glob("*.md")) if (skill_dir / "examples").exists() else []:
            generate_file_page(s["name"], md_file, "examples", s)

        # Checklists
        for md_file in sorted((skill_dir / "checklists").glob("*.md")) if (skill_dir / "checklists").exists() else []:
            generate_file_page(s["name"], md_file, "checklists", s)

    print(f"\n✅ Done! Generated pages in {PAGES_DIR}/")


if __name__ == "__main__":
    main()
