---
id: ADR-001-PI
type: pi
title: Implementation Plan - Implementação do JWT
created: 2026-01-01
updated: 2026-01-01
adr_ref: ADR-001
---

# ADR-001-PI: Implementation Plan - Implementação do JWT

> Referência: [ADR-001](./ADR-001.md) | [ADR-001-TODO](./ADR-001-TODO.md)

## 1. Visão Geral (Overview)
Este plano descreve como o agente autônomo irá implementar, testar e plugar o serviço JWT e o Middleware na aplicação, garantindo segurança ECDSA.

## 2. Padrões de Aceitação e Qualidade (Quality Standards)
- **Test Coverage:** Exigência de 100% de cobertura no módulo `auth/`.
- **Linter/Typing:** `mypy --strict` e `ruff check`.
- **Bibliotecas:** Uso obrigatório de `PyJWT[crypto]`.

## 3. Plano de Execução Granular (TDD & Step-by-Step)

### Fase A: Core Authentication

#### Passo A1.1: Criar JWT Adapter com PyJWT

**1. TDD Specs (O que testar primeiro):**
- **Arquivo de Teste:** `tests/auth/test_jwt_service.py`
- **Mocks Necessários:** Injetar chaves ECDSA fake para o teste.
- **Asserções Esperadas:** 
  - `test_generate_token_success()`: Verifica se o payload contém `exp` e `sub`.
  - `test_decode_token_expired()`: Lança exceção customizada `TokenExpiredError` quando `exp` está no passado.
- **Comando de Teste:** `pytest tests/auth/test_jwt_service.py -v`

**2. Code Specs (Implementação da regra de negócio):**
- **Arquivos Afetados:** `src/auth/jwt_service.py` e `src/auth/exceptions.py`
- **Assinaturas/Interfaces:**
  ```python
  import jwt
  
  class JWTService:
      def __init__(self, private_key: str, public_key: str): ...
      def create_access_token(self, user_id: str) -> str: ...
      def decode_token(self, token: str) -> dict[str, Any]: ...
  ```
- **Lógica e Constantes:**
  - `ALGORITHM = "ES256"`
  - Tempo de expiração do access token cravado em 15 minutos (use `datetime.utcnow()`).

**3. Integração e Comandos de Terminal:**
- `pip install "PyJWT[crypto]"`
- `pip freeze > requirements.txt`

**4. Edge Cases e Rollback (Prevenção de Falhas):**
- **Se PyJWT falhar por falta de dependências C (cryptography):** Adicione instruções para rodar `apt-get install build-essential libssl-dev libffi-dev` ou use fallback para `HS256` provisório comunicando o usuário.
- **Rollback:** Em caso de quebra persistente, desfaça os imports e reverta o commit.

#### Passo A1.2: Implementar Auth Middleware

**1. TDD Specs (O que testar primeiro):**
- **Arquivo de Teste:** `tests/auth/test_middleware.py`
- **Mocks:** Mockar a classe `JWTService` retornando payloads fixos. Usar `httpx.AsyncClient` para simular requests ao app ASGI.
- **Asserções Esperadas:**
  - Request sem header `Authorization` retorna HTTP 401.
  - Request com token expirado retorna HTTP 401 e JSON `{"detail": "Token expired"}`.
- **Comando de Teste:** `pytest tests/auth/test_middleware.py -v`

**2. Code Specs:**
- **Arquivos Afetados:** `src/auth/middleware.py` e `src/main.py`
- **Lógica:**
  - Extrair o token do cabeçalho HTTP: `header.split("Bearer ")[1]`.
  - Capturar `TokenExpiredError` da `jwt_service.py` e mapear para Exception da Web Framework.

**3. Integração:**
- Registrar o middleware na instância do FastAPI em `src/main.py`.

**4. Edge Cases e Rollback:**
- Certifique-se de que endpoints de Login não passam pelo Middleware (Whitelist ou rota não protegida).

## 4. Validação Contínua (Continuous Validation)
```bash
# Validar Tipagem
mypy src/auth/

# Validar Linting
ruff check src/auth/

# Garantir Cobertura Final do Módulo
pytest tests/auth/ --cov=src/auth --cov-fail-under=100
```
