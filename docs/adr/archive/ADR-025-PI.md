---
id: ADR-025-PI
type: pi
title: "Implementation Plan - Ingestão Hierárquica Multi-Asset de Skills (Skill Bundles)"
created: "2026-08-24"
updated: "2026-08-24"
adr_ref: ADR-025
---

# ADR-025-PI: Implementation Plan - Ingestão Hierárquica Multi-Asset de Skills (Skill Bundles)

> Referência: [ADR-025](./ADR-025-hierarchical-multi-asset-ingestion.md) | [ADR-025-TODO](./ADR-025-TODO.md)

---

## 1. Visão Geral (Overview)

Este plano estabelece os passos de engenharia de software para implementar a ingestão hierárquica tipada de ativos de skills (`references/`, `templates/`, `scripts/`) com parent linking (`parent_skill_id`), parsing especializado contra poluição vetorial, damping factor multiplicativo no reranking e payload XML enriquecido no servidor MCP e CLI.

---

## 2. Padrões de Aceitação e Qualidade (Quality Standards)

- **Zero Ruído Vetorial:** Scripts executáveis não devem ter seu código procedural indexado linha a linha. Apenas docstrings, cabeçalhos de comentários, constantes e flags de uso (`--help` / `USAGE`) são vetorizadas.
- **Isolamento e Invariante de Linhagem:** Todo chunk derivado de subpasta possui `parent_skill_id` preenchido obrigatoriamente apontando para a skill-mãe.
- **Retrocompatibilidade:** Bundles contendo apenas `SKILL.md` permanecem 100% funcionais com `asset_type = 'skill_root'` e damping `1.00`.
- **Test Coverage:** Suíte unitária dedicada cobrindo 100% dos novos métodos do parser e deserialização MCP.
- **Portabilidade:** Resolução dinâmica via `os.path` sem caminhos hardcoded.

---

## 3. Plano de Execução Granular (TDD & Step-by-Step)

### Fase A: Esquema de Dados & Parser Seletivo de Ativos

#### Passo A1.1: Atualização do Schema DDL do Banco SQLite
- **Arquivos Afetados:** [.github/scripts/skills_rag_indexer.py](file:///home/loupan/.gemini/config/skills/.github/scripts/skills_rag_indexer.py)
- **Alterações:**
  ```python
  # Na criação da tabela skill_chunks:
  cur.execute("""
  CREATE TABLE IF NOT EXISTS skill_chunks (
      chunk_id TEXT PRIMARY KEY,
      skill_id TEXT NOT NULL,
      parent_skill_id TEXT NOT NULL,
      asset_type TEXT NOT NULL DEFAULT 'skill_root',
      file_path TEXT NOT NULL DEFAULT 'SKILL.md',
      section_title TEXT NOT NULL,
      chunk_text TEXT NOT NULL,
      chunk_tokens INTEGER NOT NULL,
      vector_embedding TEXT NOT NULL,
      vector_embedding_2048 TEXT,
      FOREIGN KEY (skill_id) REFERENCES skills(id)
  );
  """)
  ```

#### Passo A1.2: Implementação da Classe `AssetParser`
- **Arquivos Afetados:** [.github/scripts/skills_rag_indexer.py](file:///home/loupan/.gemini/config/skills/.github/scripts/skills_rag_indexer.py)
- **Assinaturas:**
  ```python
  class AssetParser:
      @staticmethod
      def parse_markdown(file_path: str) -> List[Dict[str, str]]:
          """Extrai seções baseadas em headers ## e ###"""
          ...
          
      @staticmethod
      def parse_script(file_path: str) -> Dict[str, str]:
          """Extrai docstring, comentários de cabeçalho e flags USAGE/help"""
          ...
          
      @staticmethod
      def parse_template(file_path: str) -> Dict[str, str]:
          """Extrai cabeçalho descritivo e esqueleto do template"""
          ...
  ```

#### Passo A1.3: Varredura de Pastas de Sub-ativos no `SkillsRAGIndexer`
- **Arquivos Afetados:** [.github/scripts/skills_rag_indexer.py](file:///home/loupan/.gemini/config/skills/.github/scripts/skills_rag_indexer.py)
- **Lógica:**
  - Varre `references/*.md` $\rightarrow$ `asset_type: "reference"`.
  - Varre `templates/*` $\rightarrow$ `asset_type: "template"`.
  - Varre `scripts/*` $\rightarrow$ `asset_type: "script_doc"`.
  - Para cada ativo, gera `skill_id = f"{parent_id}:{asset_type}:{asset_name}"` e vincula `parent_skill_id = parent_id`.

---

### Fase B: Damping Factor Ponderado & Payload Tipado

#### Passo B1.1: Adaptação de Consultas e Damping no `SkillsDatabase`
- **Arquivos Afetados:** [.github/scripts/skills_mcp_server.py](file:///home/loupan/.gemini/config/skills/.github/scripts/skills_mcp_server.py), [.github/scripts/skills_router.py](file:///home/loupan/.gemini/config/skills/.github/scripts/skills_router.py)
- **Lógica de Damping:**
  ```python
  DAMPING_FACTORS = {
      "skill_root": 1.00,
      "reference": 0.85,
      "template": 0.80,
      "script_doc": 0.75
  }
  
  # Aplicação no score híbrido:
  damping = DAMPING_FACTORS.get(c.get("asset_type", "skill_root"), 1.00)
  c["confidence_percent"] = round(c["confidence_percent"] * damping, 1)
  ```

#### Passo B1.2: Serialização XML Enriquecida
- **Arquivos Afetados:** [.github/scripts/skills_mcp_server.py](file:///home/loupan/.gemini/config/skills/.github/scripts/skills_mcp_server.py)
- **Formato Emitido:**
  ```xml
  <active_skill id="{skill_id}" parent="{parent_skill_id}" type="{asset_type}" path="{file_path}" confidence="{conf}%">
    {chunk_content}
  </active_skill>
  ```

---

### Fase C: Suíte de Testes & Auditoria

#### Passo C1.1: Criação de `test_rag_hierarchical.py`
- **Arquivo de Teste:** [.github/scripts/tests/test_rag_hierarchical.py](file:///home/loupan/.gemini/config/skills/.github/scripts/tests/test_rag_hierarchical.py)
- **Casos de Teste Obrigatórios:**
  1. `test_asset_parser_python_script`: Extração de docstring sem código procedural.
  2. `test_asset_parser_template`: Extração de esqueleto SQL/JSON.
  3. `test_parent_linking_and_schema`: Invariante de `parent_skill_id` e colunas no SQLite.
  4. `test_damping_factor_scoring`: Priorização de `skill_root` vs promoção de `template` sob intenção explícita.
  5. `test_mcp_xml_typed_payload`: Validação dos atributos `type`, `parent` e `path` no XML de saída.

---

## 4. Validação Contínua (Continuous Validation)

Comandos a serem executados no encerramento:

```bash
# 1. Execução do pipeline de indexação multi-asset
python3 .github/scripts/skills_rag_indexer.py

# 2. Execução da suíte completa de testes (5 suítes)
python3 .github/scripts/tests/test_rag_quad_sota.py && \
python3 .github/scripts/tests/test_rag_federated.py && \
python3 .github/scripts/tests/test_mcp_bootstrap.py && \
python3 .github/scripts/tests/test_mcp_telemetry.py && \
python3 .github/scripts/tests/test_rag_hierarchical.py

# 3. Auditoria Forense
python3 .github/scripts/audit_engine.py
```

---

## 5. Handoff para Fechamento

Após a conclusão da implementação e aprovação de todos os testes, o Decision Set será finalizado com a emissão de [docs/adr/ADR-025-ER.md](file:///home/loupan/.gemini/config/skills/docs/adr/ADR-025-ER.md) e arquivado pelo Janitor (`adr-archive`).

---

*Documento gerado em 2026-08-24. Referência: ADR-025.*
