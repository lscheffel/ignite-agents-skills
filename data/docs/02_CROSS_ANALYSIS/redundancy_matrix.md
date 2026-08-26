# Cross-Analysis: Matriz de Redundância e Sobreposição Funcional

Mapeamento de clusters funcionais para detecção de duplicidades, concorrência semântica e oportunidades de consolidação modular.

---

## 1. Clusters Funcionais Identificados

### Cluster A: Code Review & Quality Assurance
* **Ativos Concorrentes:** `code-review`, `code-review-lite`, `code-review-workflow`, `clean-code`.
* **Grau de Sobreposição:** 68%
* **Diagnóstico:** `code-review` e `code-review-lite` apresentam forte concorrência em triggers. Recomenda-se unificar em um único router com flag de intensidade (`mode: lite | full`).

### Cluster B: Documentação Técnica & Governança
* **Ativos Concorrentes:** `technical-documentation`, `repo-bootstrap`, `governance`, `agents-md-management`.
* **Grau de Sobreposição:** 45%
* **Diagnóstico:** Especializações complementares, mas com templates duplicados de `GEMINI.md` e `AGENTS.md`. Centralizar templates em diretório compartilhado.

### Cluster C: Processamento de Documentos de Escritório
* **Ativos Concorrentes:** `docx-processing`, `xlsx-processing`, `pdf-processing`.
* **Grau de Sobreposição:** 15% (Especializados por formato)
* **Diagnóstico:** Alta coerência modular; fronteiras bem delimitadas pelo formato do arquivo alvo.

### Cluster D: Planejamento & Arquitetura de Software
* **Ativos Concorrentes:** `adr-generator`, `adr-archive`, `agent-planning-execution`, `ddd`, `api-design`.
* **Grau de Sobreposição:** 35%
* **Diagnóstico:** Pipeline coeso: `adr-generator` cria, `implementation` executa e `adr-archive` finaliza.

---

## 2. Recomendações de Consolidação

| Ação Proposta | Ativos Impactados | Ganho Estimado de Tokens | Redução de Ambiguidade |
| :--- | :--- | :---: | :---: |
| **Unificação de Review Engine** | `code-review` + `code-review-lite` | ~1.400 tokens / prompt | Alta |
| **Template Hub Central** | `technical-documentation` + `repo-bootstrap` | ~900 tokens / prompt | Média |
| **Sinergia ADR-TechDebt** | `adr-generator` + `adr-archive` | ~600 tokens / prompt | Média |
