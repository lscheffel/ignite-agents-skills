---
id: ADR-XXX-PI
type: pi
title: Implementation Plan - [Título da Decisão]
created: YYYY-MM-DD
updated: YYYY-MM-DD
adr_ref: ADR-XXX
---

# ADR-XXX-PI: Implementation Plan - [Título da Decisão]

> Referência: [ADR-XXX](./ADR-XXX.md) | [ADR-XXX-TODO](./ADR-XXX-TODO.md)

## 1. Visão Geral (Overview)

Breve sumário do objetivo técnico deste plano. O que o agente autônomo está prestes a codificar e por quê?

## 2. Padrões de Aceitação e Qualidade (Quality Standards)

- **Test Coverage:** Exigência de cobertura (ex: > 90% para a nova feature).
- **Linter/Typing:** Padrão a ser respeitado (ex: Strict mypy, ruff).
- **Design Patterns:** Padrões a serem aplicados (ex: Repository Pattern, Strategy).

## 3. Plano de Execução Granular (TDD & Step-by-Step)

A implementação deve ser dividida em passos lógicos, auto-contidos e validados por testes ANTES da implementação do código-fonte (TDD).

### Fase [A/B/C]: [Nome da Fase]

#### Passo [X.Y]: [Título do Passo - Ex: Criar Abstração de Repositório]

**1. TDD Specs (O que testar primeiro):**
- **Arquivo de Teste:** `tests/caminho/para/test_arquivo.py`
- **Mocks Necessários:** Ex: Mock do banco de dados, Fixtures.
- **Asserções Esperadas:** O que caracteriza o sucesso deste teste? (Ex: Deve levantar exceção X quando Y ocorrer).
- **Comando de Teste:** `pytest tests/caminho/para/test_arquivo.py -v`

**2. Code Specs (Implementação da regra de negócio):**
- **Arquivos Afetados:** `src/caminho/para/arquivo.py`
- **Assinaturas/Interfaces:**
  ```python
  class INomeDaInterface(Protocol):
      async def metodo_x(self, param: str) -> bool: ...
  ```
- **Lógica e Constantes:** Instruções precisas sobre como preencher a lógica.

**3. Integração e Comandos de Terminal:**
- Bibliotecas a instalar: `pip install lib-X`
- Geração de types/migrations: `alembic revision --autogenerate -m "..."`

**4. Edge Cases e Rollback (Prevenção de Falhas):**
- O que o agente deve fazer se a biblioteca X não estiver na versão correta?
- O que fazer se o teste falhar por falta de dependência circular? (Plano de Rollback / Fix).

---
*(Repetir a estrutura de "Passo X.Y" para cada micro-tarefa da fase correspondente no arquivo TODO).*

## 4. Validação Contínua (Continuous Validation)

Comandos exatos que o agente deve rodar no terminal para validar que o contrato de execução inteiro (build, lint, test) não foi quebrado após a conclusão de todos os passos:

```bash
# 1. Typecheck
mypy src/

# 2. Linting
ruff check src/

# 3. Test Suite da Feature
pytest tests/caminho/da/feature/
```
