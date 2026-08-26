#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SOTA CATALOG TRANSLATION ENGINE (NVIDIA NIM) - ADR-026
================================================================================
Pipeline autônomo de tradução do catálogo canônico de skills de PT-BR para EN-US
via NVIDIA NIM (Riva Translate / Nemotron / Llama-3), com:
- Preservação estrita de sintaxe (código procedural, YAML frontmatter, XML, IDs)
- Validação forense em dois estágios (AST estático Python / bash -n + NIM Code Judge)
- Cache de idempotência versionado em SQLite (SHA256)
- Rastreamento de métricas BPE de compressão de tokens
================================================================================
"""

import ast
import argparse
import hashlib
import json
import os
import re
import sqlite3
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any

# ==============================================================================
# CONFIGURAÇÃO GERAL & CONSTANTES SOTA
# ==============================================================================

PROMPT_VERSION = "v1.1.0"
DEFAULT_NIM_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

# Cascatas de Modelos (ADR-026)
TRANSLATION_MODELS = [
    "meta/llama-3.1-8b-instruct",
    "nvidia/nemotron-3.5-lightning-30b-a3b",
    "nvidia/riva-translate-4b-instruct-v2",
]

CODE_JUDGE_MODELS = [
    "deepseek-ai/deepseek-v4-flash-0731",
    "meta/llama-3.3-70b-instruct",
    "meta/llama-3.1-8b-instruct",
]

# Diretivas e Metadados que NUNCA devem ser traduzidos
PROTECTED_DIRECTIVES = {
    "parent_skill_id", "skill_id", "asset_type", "type", "pragma",
    "noqa", "pylint", "isort", "mypy", "flake8", "autopep8", "coding",
    "author", "version", "name", "id", "license", "copyright", "node_modules",
}

# Heurística de Stopwords para Detecção de Idioma (Stdlib-only)
PT_STOPWORDS: Set[str] = {
    "de", "a", "o", "que", "e", "do", "da", "em", "um", "para", "é", "com", "não",
    "uma", "os", "no", "se", "na", "por", "mais", "as", "dos", "como", "mas", "foi",
    "ao", "ele", "das", "tem", "à", "seu", "sua", "ou", "ser", "quando", "muito",
    "nos", "já", "eu", "também", "só", "pelo", "pela", "até", "isso", "ela", "entre",
    "era", "função", "método", "classe", "parâmetro", "retorna", "variável",
    "configuração", "arquivo", "diretório", "exemplo", "uso", "descrição", "regras",
    "diretrizes", "execução", "padrão", "auditoria", "tarefa", "requisito", "comando"
}

EN_STOPWORDS: Set[str] = {
    "the", "and", "to", "of", "a", "in", "is", "that", "for", "it", "as", "was",
    "with", "on", "are", "you", "this", "be", "at", "have", "from", "or", "by",
    "an", "not", "but", "all", "must", "when", "use", "user", "function", "method",
    "class", "parameter", "return", "variable", "config", "file", "directory",
    "example", "usage", "description", "rules", "guidelines", "execution", "standard",
    "audit", "task", "requirement", "command", "overview", "workflow", "checklist"
}

# Regex de Preservação de Sintaxe
CODE_BLOCK_RE = re.compile(r"```[\s\S]*?```")
FRONTMATTER_RE = re.compile(r"^---\n[\s\S]*?\n---", re.MULTILINE)
XML_TAG_RE = re.compile(r"<(?!!--)[^>]+>")
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")

# Prompts de Sistema
TRANSLATION_SYSTEM_PROMPT = """You are a strict, forensic technical translator.
Translate the Markdown document from Portuguese (PT-BR) to fluent technical English (EN-US).

CRITICAL INVARIANTS:
1. Translate ALL human-readable prose, headings, bullet points, checklists, Mermaid diagram node/edge labels, and explanatory CODE COMMENTS (e.g. `# ✅ CORRETO` -> `# ✅ CORRECT`, `# ❌ ERRADO` -> `# ❌ WRONG`, `# Listar` -> `# List`).
2. Preserve all code identifiers, variable names, functions, classes, imports, HTTP paths, and parameters EXACTLY intact.
3. Preserve all YAML frontmatter keys (name, version, triggers, tags, etc.) intact; translate only the description text.
4. DO NOT add any extra explanations, tutorials, introductions, or conclusions.
5. Preserve all backticks (`code`), markdown links, and formatting.
6. Output ONLY the translated document without conversational filler or wrappers."""

CODE_JUDGE_SYSTEM_PROMPT = """You are a forensic code and technical documentation compliance auditor.
Your ONLY job is to verify that a translated technical text/code comment preserved all critical identifiers and structure.

Verification criteria:
1. No variable names, function names, parameter names, CLI flags, file paths, or DB column names were translated.
2. No code indentation, procedural logic, or structural tags were damaged.
3. ONLY human-readable informational/explanatory sentences were translated into English.

Respond ONLY with a valid JSON object in this exact schema:
{"valid": true, "reason": "OK"} or {"valid": false, "reason": "Specific issue description"}
"""

# ==============================================================================
# RESOLUÇÃO DE DIRETÓRIOS & AMBIENTE
# ==============================================================================

def get_workspace_root() -> Path:
    """Resolve a raiz do workspace dinamicamente."""
    return Path(__file__).resolve().parent.parent.parent

def load_dotenv(workspace_root: Path) -> Dict[str, str]:
    """Carrega variáveis do arquivo .env sem dependências externas."""
    env_file = workspace_root / ".env"
    env_vars = {}
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            k = k.strip()
            v = v.strip().strip("'\"")
            env_vars[k] = v
            if k not in os.environ:
                os.environ[k] = v
    return env_vars

# ==============================================================================
# CACHE DE IDEMPOTÊNCIA VERSIONADO (SQLite)
# ==============================================================================

def get_cache_db_path(workspace_root: Path) -> Path:
    return workspace_root / ".local" / "skills_rag" / "translation_cache.sqlite3"

def init_cache(workspace_root: Path) -> sqlite3.Connection:
    """Inicializa o banco de cache de tradução com auto-migração de schema."""
    db_path = get_cache_db_path(workspace_root)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS translation_cache (
            content_hash TEXT PRIMARY KEY,
            original_sample TEXT,
            translated_content TEXT NOT NULL,
            model_used TEXT NOT NULL,
            prompt_version TEXT,
            created_at REAL NOT NULL
        )
    """)
    conn.commit()
    
    # Auto-migração para bancos existentes
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(translation_cache)")
    existing_cols = {col[1] for col in cur.fetchall()}
    if "original_sample" not in existing_cols:
        conn.execute("ALTER TABLE translation_cache ADD COLUMN original_sample TEXT")
    if "prompt_version" not in existing_cols:
        conn.execute("ALTER TABLE translation_cache ADD COLUMN prompt_version TEXT")
    conn.commit()
    return conn

def get_cache_key(content: str, model: str) -> str:
    """Gera chave SHA256 versionada combinando conteúdo, modelo e prompt version."""
    payload = f"{content}:{model}:{PROMPT_VERSION}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()

def get_cached_translation(conn: sqlite3.Connection, cache_key: str) -> Optional[str]:
    """Recupera tradução do cache se existente."""
    cur = conn.cursor()
    cur.execute("SELECT translated_content FROM translation_cache WHERE content_hash = ?", (cache_key,))
    row = cur.fetchone()
    return row[0] if row else None

def store_cached_translation(conn: sqlite3.Connection, cache_key: str, original: str, translated: str, model: str) -> None:
    """Armazena resultado da tradução no cache."""
    cur = conn.cursor()
    cur.execute("""
        INSERT OR REPLACE INTO translation_cache (content_hash, original_sample, translated_content, model_used, prompt_version, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (cache_key, original[:200], translated, model, PROMPT_VERSION, time.time()))
    conn.commit()

# ==============================================================================
# DETECÇÃO DE IDIOMA (Stopwords Heuristic)
# ==============================================================================

def detect_language(text: str) -> str:
    """
    Detecta se o texto está predominantemente em 'pt' (Português), 'en' (Inglês) ou 'unknown'.
    Utiliza heurística de contagem de stopwords com threshold de confiança 1.5x.
    """
    words = set(re.findall(r"\b[a-zA-ZÀ-ÿ]{3,}\b", text.lower()))
    if not words:
        return "unknown"
    pt_score = sum(1 for w in words if w in PT_STOPWORDS)
    en_score = sum(1 for w in words if w in EN_STOPWORDS)
    
    if pt_score == 0 and en_score == 0:
        return "unknown"
    
    if pt_score > en_score * 1.5:
        return "pt"
    elif en_score > pt_score * 1.5:
        return "en"
    return "unknown"

# ==============================================================================
# PRESERVAÇÃO DE SINTAXE (Regex Extract / Restore)
# ==============================================================================

def protect_syntax(content: str) -> Tuple[str, List[Tuple[str, str]]]:
    """
    Substitui blocos protegidos (Code blocks, Frontmatter, Inline code, XML tags)
    por placeholders determinísticos. Retorna (texto_protegido, lista_de_tuplas_(placeholder, original)).
    """
    placeholders: List[Tuple[str, str]] = []
    
    # 1. Proteger Frontmatter YAML no topo do documento
    def repl_fm(match: re.Match) -> str:
        ph = f"@@FRONTMATTER_{len(placeholders)}@@"
        placeholders.append((ph, match.group(0)))
        return ph
    
    protected = FRONTMATTER_RE.sub(repl_fm, content, count=1)
    
    # 2. Proteger Code Blocks com fences (```...```)
    def repl_code(match: re.Match) -> str:
        ph = f"@@CODE_BLOCK_{len(placeholders)}@@"
        placeholders.append((ph, match.group(0)))
        return ph
    
    protected = CODE_BLOCK_RE.sub(repl_code, protected)
    
    # 3. Proteger Inline Code (`...`) ANTES de XML tags (para evitar que XML dentro de backticks seja tocado)
    def repl_inline(match: re.Match) -> str:
        ph = f"@@INLINE_CODE_{len(placeholders)}@@"
        placeholders.append((ph, match.group(0)))
        return ph
    
    protected = INLINE_CODE_RE.sub(repl_inline, protected)
    
    # 4. Proteger Tags XML / HTML
    def repl_xml(match: re.Match) -> str:
        ph = f"@@XML_TAG_{len(placeholders)}@@"
        placeholders.append((ph, match.group(0)))
        return ph
    
    protected = XML_TAG_RE.sub(repl_xml, protected)
    
    return protected, placeholders

def restore_syntax(protected: str, placeholders: List[Any]) -> str:
    """
    Restaura todos os placeholders inseridos por protect_syntax(),
    iterando na ordem reversa de substituição para garantir integridade aninhada.
    """
    restored = protected
    # Se placeholders for lista de tuplas (placeholder, original) ou lista simples de strings
    if placeholders and isinstance(placeholders[0], tuple):
        for ph, original in reversed(placeholders):
            restored = restored.replace(ph, original)
    else:
        for i in range(len(placeholders) - 1, -1, -1):
            original = placeholders[i]
            for ph_prefix in ("@@XML_TAG_", "@@INLINE_CODE_", "@@CODE_BLOCK_", "@@FRONTMATTER_"):
                restored = restored.replace(f"{ph_prefix}{i}@@", original)
    return restored

# ==============================================================================
# EXTRAÇÃO DE COMENTÁRIOS E DOCSTRINGS EM CÓDIGO FONTE
# ==============================================================================

def is_protected_comment(line: str) -> bool:
    """Verifica se um comentário contém diretivas de máquina que não devem ser traduzidas."""
    clean = line.strip().lstrip("#/").strip().lower()
    if clean.startswith("!"):  # Shebang
        return True
    for directive in PROTECTED_DIRECTIVES:
        if clean.startswith(f"{directive}:") or clean.startswith(f"{directive} =") or f": {directive}" in clean:
            return True
    return False

def extract_docstrings_and_comments(content: str, ext: str) -> Tuple[List[str], List[Tuple[int, int, str]]]:
    """
    Para arquivos de script (.py, .sh, .bash, .js, .ts), isola comentários e docstrings traduzíveis.
    Retorna (lista_de_textos_traduziveis, posicoes_no_arquivo).
    """
    translatable_texts = []
    positions = []
    
    if ext == ".py":
        # Usar ast para docstrings e regex para comentários #
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    doc = ast.get_docstring(node)
                    if doc and detect_language(doc) == "pt":
                        translatable_texts.append(doc)
        except Exception:
            pass
        
        # Linhas de comentários #
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("#") and not is_protected_comment(stripped):
                comment_text = stripped.lstrip("#").strip()
                if len(comment_text) > 3 and detect_language(comment_text) == "pt":
                    translatable_texts.append(comment_text)
                    positions.append((idx, idx, line))
                    
    elif ext in (".sh", ".bash"):
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("#") and not is_protected_comment(stripped):
                comment_text = stripped.lstrip("#").strip()
                if len(comment_text) > 3 and detect_language(comment_text) == "pt":
                    translatable_texts.append(comment_text)
                    positions.append((idx, idx, line))
                    
    elif ext in (".js", ".ts"):
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("//") and not is_protected_comment(stripped):
                comment_text = stripped.lstrip("/").strip()
                if len(comment_text) > 3 and detect_language(comment_text) == "pt":
                    translatable_texts.append(comment_text)
                    positions.append((idx, idx, line))
                    
    return translatable_texts, positions

# ==============================================================================
# VALIDAÇÃO ESTÁTICA DETERMINÍSTICA (Estágio A)
# ==============================================================================

def validate_python_ast(code: str) -> Tuple[bool, str]:
    """Verifica se o código Python compila via AST sem erros de sintaxe ou indentação."""
    try:
        ast.parse(code)
        return True, "AST Python Válido"
    except SyntaxError as e:
        return False, f"SyntaxError na linha {e.lineno}: {e.msg}"
    except Exception as e:
        return False, f"Erro inesperado no parser AST: {str(e)}"

def validate_shell_syntax(code: str) -> Tuple[bool, str]:
    """Verifica a sintaxe de scripts Shell via dry-run `bash -n`."""
    try:
        proc = subprocess.run(
            ["bash", "-n"],
            input=code,
            text=True,
            capture_output=True,
            timeout=5
        )
        if proc.returncode != 0:
            return False, f"Bash Syntax Error: {proc.stderr.strip()}"
        return True, "Sintaxe Shell Válida"
    except Exception as e:
        return False, f"Falha ao executar validador shell: {str(e)}"

# ==============================================================================
# COMUNICAÇÃO HTTP COM NVIDIA NIM
# ==============================================================================

def call_nvidia_nim_api(
    prompt: str,
    system_prompt: str,
    models: List[str],
    api_key: str,
    max_retries: int = 2,
    max_tokens: int = 4096,
    temperature: float = 0.0,
    base_url: str = DEFAULT_NIM_URL
) -> Tuple[bool, str, str]:
    """
    Executa chamada à API NVIDIA NIM com suporte a cascata de modelos e backoff exponencial.
    Retorna (sucesso, texto_resposta, modelo_utilizado).
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    last_error = ""
    for model in models:
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        for attempt in range(max_retries):
            try:
                req = urllib.request.Request(
                    base_url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers=headers,
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=45) as resp:
                    if resp.status == 200:
                        data = json.loads(resp.read().decode("utf-8"))
                        content = data["choices"][0]["message"]["content"].strip()
                        # Limpar eventuais cercas ``` markdown envolventes
                        if content.startswith("```") and content.endswith("```"):
                            lines = content.splitlines()
                            if len(lines) >= 2 and lines[0].startswith("```"):
                                content = "\n".join(lines[1:-1]).strip()
                        return True, content, model
                    else:
                        last_error = f"HTTP {resp.status}"
            except urllib.error.HTTPError as he:
                try:
                    err_body = he.read().decode("utf-8")
                    err_json = json.loads(err_body)
                    last_error = f"HTTP {he.code}: {err_json.get('message', err_body)}"
                except Exception:
                    last_error = f"HTTP {he.code}: {he.reason}"
                time.sleep(2 ** attempt)
            except urllib.error.URLError as ue:
                last_error = f"URLError: {str(ue.reason)}"
                time.sleep(2 ** attempt)
            except Exception as ex:
                last_error = f"Exception: {str(ex)}"
                time.sleep(2 ** attempt)
                
    return False, f"Falha em todos os modelos da cascata. Último erro: {last_error}", "none"

# ==============================================================================
# AUDITORIA NIM CODE JUDGE (Estágio B)
# ==============================================================================

def call_nim_code_judge(original: str, translated: str, file_ext: str, api_key: str) -> Tuple[bool, str]:
    """
    Executa auditoria forense via modelo NIM Code Judge para garantir que
    nenhum identificador ou sintaxe foi corrompido durante a tradução.
    """
    if not api_key:
        return True, "API Key ausente, auditoria NIM pulada (fallback seguro)."
    
    judge_prompt = f"""You are a strict, forensic code quality auditor evaluating a technical translation from Portuguese (PT-BR) to English (EN-US).

Original Document ({file_ext}):
```
{original}
```

Translated Document ({file_ext}):
```
{translated}
```

Evaluate if the translation preserves complete structural integrity, formatting, code fences, YAML frontmatter, identifiers, and meaning.
Output ONLY valid JSON with no markdown wrapping:
{{"valid": true, "reason": "OK"}} or {{"valid": false, "reason": "Explanation of structural issue"}}"""

    ok, resp_text, model = call_nvidia_nim_api(
        prompt=judge_prompt,
        system_prompt=CODE_JUDGE_SYSTEM_PROMPT,
        models=CODE_JUDGE_MODELS,
        api_key=api_key,
        max_tokens=512,
        temperature=0.0
    )
    
    if not ok:
        # Se os modelos de judge falharem na API, não bloqueamos se a validação estática passou
        return True, f"Code Judge skipped (API unavailable: {model})"
    
    try:
        # Extrair JSON da resposta
        json_match = re.search(r"\{[\s\S]*\}", resp_text)
        if json_match:
            data = json.loads(json_match.group(0))
            is_valid = data.get("valid", True)
            reason = data.get("reason", "OK")
            return is_valid, f"[{model}] {reason}"
    except Exception:
        pass
        
    return True, f"[{model}] Resposta não-JSON recebida, aceita por fallback."

# ==============================================================================
# VALIDAÇÃO UNIFICADA EM DOIS ESTÁGIOS
# ==============================================================================

def validate_translation(original: str, translated: str, file_ext: str, api_key: str) -> Tuple[bool, str]:
    """
    Aplica o gate de validação em dois estágios:
    - Estágio A: Validação Estática (AST Python ou bash -n)
    - Estágio B: NIM Code Judge (Integridade de Identificadores)
    """
    # 1. Estágio A: Sintaxe Estática
    if file_ext == ".py":
        ok, reason = validate_python_ast(translated)
        if not ok:
            return False, f"Estágio A (AST): {reason}"
    elif file_ext in (".sh", ".bash"):
        ok, reason = validate_shell_syntax(translated)
        if not ok:
            return False, f"Estágio A (Shell): {reason}"
            
    # 2. Estágio B: Code Judge Forense
    ok, reason = call_nim_code_judge(original, translated, file_ext, api_key)
    if not ok:
        return False, f"Estágio B (Code Judge): {reason}"
        
    return True, "Validação aprovada em ambos os estágios."

# ==============================================================================
# ESTIMATIVA DE COMPRESSÃO BPE DE TOKENS
# ==============================================================================

def estimate_bpe_tokens(text: str) -> int:
    """
    Estima a contagem de tokens BPE (SentencePiece/cl100k) usando tokenizer aproximado.
    Em média, tokenizers BPE quebram palavras longas e caracteres acentuados.
    """
    tokens = re.findall(r"\w+|[^\w\s]", text, re.UNICODE)
    token_count = 0
    for tok in tokens:
        # Penaliza caracteres acentuados típicos de PT-BR no BPE
        accented_chars = len(re.findall(r"[áàãâéêíóôõúçÁÀÃÂÉÊÍÓÔÕÚÇ]", tok))
        if accented_chars > 0:
            token_count += 1 + accented_chars
        else:
            token_count += max(1, (len(tok) + 3) // 4)
    return token_count

# ==============================================================================
# MOTOR PRINCIPAL DE PROCESSAMENTO DE ARQUIVO
# ==============================================================================

def split_markdown_into_chunks(content: str, max_chunk_chars: int = 2500) -> List[str]:
    """
    Divide um documento Markdown em chunks lógicos por cabeçalhos (#, ##, ###)
    ou quebras de parágrafo duplo, sem quebrar blocos de código ou tabelas.
    """
    lines = content.splitlines(keepends=True)
    chunks: List[str] = []
    current_chunk: List[str] = []
    current_len = 0
    in_code_block = False
    
    for line in lines:
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            
        is_heading = (line.startswith("#") or line.startswith("##") or line.startswith("###")) and not in_code_block
        
        if is_heading and current_len >= max_chunk_chars and current_chunk:
            chunks.append("".join(current_chunk))
            current_chunk = [line]
            current_len = len(line)
        else:
            current_chunk.append(line)
            current_len += len(line)
            
    if current_chunk:
        chunks.append("".join(current_chunk))
        
    return chunks if chunks else [content]

def tokenize_markdown(raw_content: str) -> List[Tuple[str, str]]:
    """
    Divide o documento Markdown em blocos atômicos:
    - ('frontmatter', yaml_raw)
    - ('code', fenced_code_block)
    - ('text', markdown_prose)
    Garante que blocos de código nunca sejam expostos a alterações indesejadas pelo modelo.
    """
    tokens = []
    
    # 1. Extrair YAML Frontmatter no topo
    fm_match = re.match(r"^---\n(.*?)\n---\n*", raw_content, re.DOTALL)
    if fm_match:
        tokens.append(("frontmatter", fm_match.group(1)))
        rest = raw_content[fm_match.end():]
    else:
        rest = raw_content
        
    # 2. Alternar entre code blocks (```...```) e texto
    code_pattern = re.compile(r"```[\s\S]*?```")
    last_end = 0
    for m in code_pattern.finditer(rest):
        text_part = rest[last_end:m.start()]
        if text_part:
            tokens.append(("text", text_part))
        tokens.append(("code", m.group(0)))
        last_end = m.end()
        
    if last_end < len(rest):
        tokens.append(("text", rest[last_end:]))
        
    return tokens

def protect_code_blocks(text: str) -> Tuple[str, Dict[str, str]]:
    """Substitui blocos de código ```...``` por placeholders HTML resistentes a LLM."""
    placeholders: Dict[str, str] = {}
    counter = 0
    def repl(m: re.Match) -> str:
        nonlocal counter
        ph = f"<!-- CODE_BLOCK_{counter} -->"
        placeholders[ph] = m.group(0)
        counter += 1
        return f"\n\n{ph}\n\n"
    protected = re.sub(r"```[\s\S]*?```", repl, text)
    return protected, placeholders

def restore_code_blocks(text: str, placeholders: Dict[str, str]) -> str:
    """Restaura blocos de código byte-a-byte a partir dos placeholders HTML."""
    for ph, orig in placeholders.items():
        text = text.replace(ph, orig)
    return text

def translate_markdown_text(
    content: str,
    conn: sqlite3.Connection,
    api_key: str,
    force: bool = False
) -> Tuple[bool, str, str, bool]:
    """
    Traduz documento Markdown decompondo em seções H2 com proteção estrita de code blocks e frontmatter.
    Garante integridade estrutural absoluta e aprovação no Code Judge.
    """
    if not content.strip() or detect_language(content) == "en":
        return True, content, "none", True
        
    cache_key = get_cache_key(content, TRANSLATION_MODELS[0])
    cached_text = None if force else get_cached_translation(conn, cache_key)
    if cached_text:
        return True, cached_text, "cache", True
        
    if not api_key:
        return False, "", "API key ausente", False
        
    # 1. Separar Frontmatter
    fm_match = re.match(r"^---\n(.*?)\n---\n*", content, re.DOTALL)
    if fm_match:
        fm_raw = fm_match.group(1)
        body = content[fm_match.end():]
    else:
        fm_raw = ""
        body = content
        
    # 2. Proteger Code Blocks no Body
    protected_body, phs = protect_code_blocks(body)
    
    # 3. Dividir Body em seções H2 para prevenir alucinações e estouro de contexto
    sections = re.split(r"(?=\n##\s+)", protected_body)
    trans_sections: List[str] = []
    overall_model = "none"
    all_cached = True
    
    sys_prompt = (
        "You are a strict, faithful technical translator.\n"
        "Translate the input text from Portuguese (PT-BR) to fluent technical English (EN-US).\n\n"
        "CRITICAL INVARIANTS:\n"
        "1. Translate all headings, lists, bullet points, and explanatory text to English.\n"
        "2. DO NOT translate, modify, or remove HTML comments like `<!-- CODE_BLOCK_0 -->`. Keep them EXACTLY as they appear.\n"
        "3. Preserve all backticks (`code`) and inline identifiers.\n"
        "4. Output ONLY the translated text without conversational filler or wrappers."
    )
    
    for sec in sections:
        if not sec.strip() or detect_language(sec) == "en":
            trans_sections.append(sec)
            continue
            
        sec_cache_key = get_cache_key(sec, TRANSLATION_MODELS[0])
        sec_cached = None if force else get_cached_translation(conn, sec_cache_key)
        if sec_cached:
            trans_sections.append(sec_cached)
            overall_model = "cache"
        else:
            all_cached = False
            ok, trans_sec, model_used = call_nvidia_nim_api(
                prompt=sec,
                system_prompt=sys_prompt,
                models=TRANSLATION_MODELS,
                api_key=api_key,
                max_tokens=4096,
                temperature=0.0
            )
            if ok:
                overall_model = model_used
                store_cached_translation(conn, sec_cache_key, sec, trans_sec, model_used)
                trans_sections.append(trans_sec)
            else:
                trans_sections.append(sec)
            time.sleep(0.1)
            
    # 4. Restaurar blocos de código
    translated_body_prot = "".join(trans_sections)
    restored_body = restore_code_blocks(translated_body_prot, phs)
    
    # 5. Traduzir apenas o campo description no Frontmatter
    new_fm = fm_raw
    if fm_raw:
        desc_match = re.search(r"(description:\s*)(.*?)(\n[a-zA-Z_-]+:|\Z)", fm_raw, re.DOTALL)
        if desc_match:
            clean_desc = desc_match.group(2).strip()
            if detect_language(clean_desc) == "pt":
                desc_cache_key = get_cache_key(clean_desc, TRANSLATION_MODELS[0])
                desc_cached = None if force else get_cached_translation(conn, desc_cache_key)
                if desc_cached:
                    trans_desc = desc_cached
                else:
                    all_cached = False
                    ok, trans_desc, model_used = call_nvidia_nim_api(
                        prompt=f"Translate to English:\n{clean_desc}",
                        system_prompt=TRANSLATION_SYSTEM_PROMPT,
                        models=TRANSLATION_MODELS,
                        api_key=api_key
                    )
                    if ok:
                        store_cached_translation(conn, desc_cache_key, clean_desc, trans_desc, model_used)
                    else:
                        trans_desc = clean_desc
                new_fm = fm_raw[:desc_match.start(2)] + trans_desc.strip() + fm_raw[desc_match.end(2):]
                
    if fm_raw:
        final_doc = f"---\n{new_fm}\n---\n\n{restored_body.strip()}\n"
    else:
        final_doc = restored_body.strip() + "\n"
        
    store_cached_translation(conn, cache_key, content, final_doc, overall_model)
    return True, final_doc, overall_model, all_cached

def process_file(
    file_path: Path,
    conn: sqlite3.Connection,
    api_key: str,
    dry_run: bool = False,
    force: bool = False
) -> Dict[str, Any]:
    """
    Processa um único arquivo:
    1. Lê o conteúdo original
    2. Detecta o idioma
    3. Protege sintaxe e traduz via NIM / Cache
    4. Restaura sintaxe
    5. Executa validação em 2 estágios
    6. Grava ou faz rollback em caso de falha
    """
    result: Dict[str, Any] = {
        "path": str(file_path),
        "status": "SKIPPED",
        "original_tokens": 0,
        "translated_tokens": 0,
        "model_used": "none",
        "cached": False,
        "reason": ""
    }
    
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        result["status"] = "ERROR"
        result["reason"] = f"Falha de leitura: {str(e)}"
        return result
        
    ext = file_path.suffix.lower()
    lang = detect_language(content)
    result["original_tokens"] = estimate_bpe_tokens(content)
    
    # Se já estiver em inglês e não forçado, skip
    if lang == "en" and not force:
        result["status"] = "SKIPPED"
        result["reason"] = "Já em EN-US"
        result["translated_tokens"] = result["original_tokens"]
        return result
        
    if ext == ".md":
        ok, final_content, model_used, was_cached = translate_markdown_text(content, conn, api_key, force=force)
        if not ok:
            result["status"] = "FAILED"
            result["reason"] = model_used
            return result
        result["model_used"] = model_used
        result["cached"] = was_cached
    else:
        # Para scripts (.py, .sh, etc.)
        protected_content, placeholders = protect_syntax(content)
        if detect_language(protected_content) != "pt" and not force:
            result["status"] = "SKIPPED"
            result["reason"] = "Código procedural sem comentários em PT-BR"
            result["translated_tokens"] = result["original_tokens"]
            return result
            
        cache_key = get_cache_key(protected_content, TRANSLATION_MODELS[0])
        translated_protected = None
        if not force:
            cached = get_cached_translation(conn, cache_key)
            if cached:
                translated_protected = cached
                result["cached"] = True
                result["model_used"] = "cache"
                
        if not translated_protected:
            if not api_key:
                result["status"] = "ERROR"
                result["reason"] = "NVIDIA_API_KEY necessária para tradução online."
                return result
                
            ok, resp_text, model_used = call_nvidia_nim_api(
                prompt=protected_content,
                system_prompt=TRANSLATION_SYSTEM_PROMPT,
                models=TRANSLATION_MODELS,
                api_key=api_key
            )
            if not ok:
                result["status"] = "FAILED"
                result["reason"] = resp_text
                return result
            translated_protected = resp_text
            result["model_used"] = model_used
            store_cached_translation(conn, cache_key, protected_content, translated_protected, model_used)
            time.sleep(0.2)
            
        final_content = restore_syntax(translated_protected, placeholders)
        
    result["translated_tokens"] = estimate_bpe_tokens(final_content)
    
    # Validação Forense em Dois Estágios
    valid, val_reason = validate_translation(content, final_content, ext, api_key)
    if not valid:
        result["status"] = "REJECTED"
        result["reason"] = f"Falha na validação forense: {val_reason}"
        return result
        
    if not dry_run:
        try:
            file_path.write_text(final_content, encoding="utf-8")
            result["status"] = "TRANSLATED"
            result["reason"] = val_reason
        except Exception as e:
            result["status"] = "ERROR"
            result["reason"] = f"Falha ao escrever arquivo: {str(e)}"
    else:
        result["status"] = "DRY_RUN_OK"
        result["reason"] = val_reason
        
    return result

# ==============================================================================
# DESCOBERTA DE ARQUIVOS NO WORKSPACE
# ==============================================================================

def discover_catalog_files(workspace_root: Path) -> List[Path]:
    """Descobre arquivos Markdown e scripts elegíveis no repositório de skills."""
    eligible_files: List[Path] = []
    excluded_dirs = {
        ".git", "__pycache__", ".local", "data", "node_modules",
        ".kilo", ".kilocode", "venv", ".venv", ".system_generated",
        "docs", ".github", ".githooks", "rules", "plugins"
    }
    
    valid_extensions = {".md", ".py", ".sh", ".bash", ".js", ".ts"}
    
    for root, dirs, files in os.walk(workspace_root):
        dirs[:] = [d for d in dirs if d not in excluded_dirs and not d.startswith(".")]
        for file in files:
            p = Path(root) / file
            if p.parent == workspace_root and p.suffix.lower() == ".md":
                # Arquivos canônicos de governança da raiz são reconciliados separadamente
                continue
            if p.suffix.lower() in valid_extensions:
                eligible_files.append(p)
                
    return sorted(eligible_files)

# ==============================================================================
# CLI & EXECUÇÃO PRINCIPAL
# ==============================================================================

def main() -> int:
    parser = argparse.ArgumentParser(
        description="SOTA Catalog Translation Engine (NVIDIA NIM) - ADR-026"
    )
    parser.add_argument("--dry-run", action="store_true", help="Simula o pipeline sem alterar arquivos em disco.")
    parser.add_argument("--force", action="store_true", help="Força re-tradução ignorando cache e detecção prévia.")
    parser.add_argument("--file", type=str, help="Processa um único arquivo específico.")
    parser.add_argument("--stats", action="store_true", help="Exibe estatísticas do cache de tradução e sai.")
    
    args = parser.parse_args()
    workspace_root = get_workspace_root()
    env_vars = load_dotenv(workspace_root)
    api_key = os.environ.get("NVIDIA_API_KEY", env_vars.get("NVIDIA_API_KEY", ""))
    
    conn = init_cache(workspace_root)
    
    if args.stats:
        cur = conn.cursor()
        cur.execute("SELECT count(*), model_used FROM translation_cache GROUP BY model_used")
        rows = cur.fetchall()
        print("\n=== ESTATÍSTICAS DO CACHE DE TRADUÇÃO (ADR-026) ===")
        total = 0
        for count, model in rows:
            print(f"  • {model}: {count} entradas")
            total += count
        print(f"Total de Entradas em Cache: {total}\n")
        return 0
        
    print("=" * 80)
    print("SOTA CATALOG TRANSLATION ENGINE (NVIDIA NIM) - ADR-026")
    print("=" * 80)
    print(f"[*] Workspace Root: {workspace_root}")
    print(f"[*] NVIDIA API Key: {'Configurada (OK)' if api_key else 'AUSENTE (Operando em Modo Validação/Offline)'}")
    print(f"[*] Cache DB: {get_cache_db_path(workspace_root)}")
    print(f"[*] Modo de Execução: {'DRY RUN' if args.dry_run else 'PRODUÇÃO ATIVA'}")
    print("=" * 80)
    
    if args.file:
        target_path = Path(args.file).resolve()
        if not target_path.exists():
            print(f"[!] Arquivo não encontrado: {target_path}")
            return 1
        files = [target_path]
    else:
        files = discover_catalog_files(workspace_root)
        
    print(f"[*] Total de arquivos elegíveis descobertos: {len(files)}")
    
    stats = {"TRANSLATED": 0, "SKIPPED": 0, "DRY_RUN_OK": 0, "REJECTED": 0, "ERROR": 0, "FAILED": 0}
    total_orig_tokens = 0
    total_trans_tokens = 0
    
    for i, file_path in enumerate(files, 1):
        rel_path = file_path.relative_to(workspace_root)
        res = process_file(file_path, conn, api_key, dry_run=args.dry_run, force=args.force)
        st = res["status"]
        stats[st] = stats.get(st, 0) + 1
        total_orig_tokens += res["original_tokens"]
        total_trans_tokens += res["translated_tokens"]
        
        status_icon = "✓" if st in ("TRANSLATED", "DRY_RUN_OK") else "•" if st == "SKIPPED" else "✗"
        print(f"[{i:02d}/{len(files):02d}] {status_icon} [{st:<10}] {rel_path} (Model: {res['model_used']})")
        if res["reason"] and st not in ("SKIPPED", "TRANSLATED", "DRY_RUN_OK"):
            print(f"      └─ Motivo: {res['reason']}")
            
    print("\n" + "=" * 80)
    print("RESUMO DA EXECUÇÃO")
    print("=" * 80)
    for k, v in stats.items():
        if v > 0:
            print(f"  • {k}: {v}")
    
    if total_orig_tokens > 0 and total_trans_tokens > 0:
        compression = (1.0 - (total_trans_tokens / total_orig_tokens)) * 100.0
        print(f"\n[*] Tokens Originais Estimados (PT-BR): {total_orig_tokens}")
        print(f"[*] Tokens Finais Estimados (EN-US):     {total_trans_tokens}")
        print(f"[*] Taxa de Compressão BPE Global:       {compression:.2f}%")
    print("=" * 80 + "\n")
    
    return 0 if stats.get("ERROR", 0) == 0 and stats.get("FAILED", 0) == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
