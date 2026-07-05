# Exemplo: Validação de Criptografia — AES-256-GCM

## Contexto

Aplicação armazena dados sensíveis (tokens, credenciais) criptografados com AES-256-GCM. Precisa validar que a implementação está correta e segura.

## Checklist de Validação

### 1. Geração de Chave

```python
# ✅ CORRETO: Usar PBKDF2/scrypt/Argon2 para derivar chave de senha
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,  # 16 bytes aleatórios
    iterations=600_000,  # mínimo OWASP 2023
)
key = kdf.derive(password.encode())

# ❌ ERRADO: Usar hash simples (MD5, SHA-256) como chave
key = hashlib.sha256(password.encode()).digest()  # NÃO FAÇA ISSO
```

**Validação:**
- [ ] KDF usa PBKDF2 (≥600k iterações), scrypt (N≥16384), ou Argon2id
- [ ] Salt é aleatório e único por registro (≥16 bytes)
- [ ] Salt é armazenado junto com o ciphertext (não secreto)

### 2. Nonce/IV

```python
# ✅ CORRETO: Nonce aleatório de 12 bytes (96 bits) para GCM
import os
nonce = os.urandom(12)  # 96 bits = padrão para GCM

# ❌ ERRADO: Reutilizar nonce com a mesma chave
nonce = b'\x00' * 12  # NUNCA fazer isso
nonce = bytes.fromhex('000000000000000000000000')  # NUNCA
```

**Validação:**
- [ ] Nonce tem 12 bytes (96 bits) para GCM
- [ ] Nonce é gerado aleatoriamente (`os.urandom(12)`)
- [ ] Nonce NÃO é derivado de counter sequencial (risco de colisão)
- [ ] Nunca reutilizar par (chave, nonce)

### 3. Autenticação (AAD)

```python
# ✅ CORRETO: Usar Additional Authenticated Data (AAD)
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

aesgcm = AESGCM(key)
# AAD autentica metadados sem criptografá-los
ciphertext = aesgcm.encrypt(nonce, plaintext, aad=user_id.encode())

# ❌ ERRADO: Não usar AAD (perde autenticação de contexto)
ciphertext = aesgcm.encrypt(nonce, plaintext, None)
```

**Validação:**
- [ ] AAD inclui identificador do registro (user_id, record_id)
- [ ] AAD é verificado na decriptação (se não bate, falha)
- [ ] AAD não contém dados sensíveis (é autenticado, não criptografado)

### 4. Armazenamento

```python
# ✅ CORRETO: Armazenar nonce + ciphertext + tag juntos
import base64

# Formato: base64(nonce || ciphertext || tag)
encrypted = base64.b64encode(nonce + ciphertext).decode()

# ✅ OU: Formato JSON estruturado
encrypted_data = {
    "ciphertext": base64.b64encode(ciphertext).decode(),
    "nonce": base64.b64encode(nonce).decode(),
    "aad": user_id,
    "algorithm": "AES-256-GCM",
    "version": 1
}

# ❌ ERRADO: Armazenar só o ciphertext
encrypted = base64.b64encode(ciphertext).decode()  # nonce perdido!
```

**Validação:**
- [ ] Nonce é armazenado (não recalculado)
- [ ] Formato inclui todos os campos necessários para decriptação
- [ ] Nonce não é considerado segredo (pode ser armazenado em plaintext)

### 5. Decriptação

```python
# ✅ CORRETO: Verificar autenticação antes de decriptar
def decrypt(encrypted_data: dict, key: bytes) -> bytes:
    nonce = base64.b64decode(encrypted_data["nonce"])
    ciphertext = base64.b64decode(encrypted_data["ciphertext"])
    aad = encrypted_data.get("aad", "").encode()

    aesgcm = AESGCM(key)
    try:
        plaintext = aesgcm.decrypt(nonce, ciphertext, aad)
        return plaintext
    except Exception:
        # NÃO expor detalhes do erro
        raise ValueError("Dados inválidos ou corrompidos")

# ❌ ERRADO: Expor detalhes do erro de criptografia
except InvalidTag as e:
    raise ValueError(f"Tag inválida: {e}")  # NUNCA fazer isso
```

**Validação:**
- [ ] Erros de decriptação são genéricos (não expõem causa)
- [ ] AAD é verificado na decriptação
- [ ] Dados corrompidos causam falha (não output parcial)

## Resumo da Auditoria

| Check | Status | Observação |
|-------|--------|------------|
| KDF correto | ✅ | PBKDF2 com 600k iterações |
| Nonce único | ✅ | os.urandom(12) |
| AAD utilizado | ✅ | user_id como AAD |
| Armazenamento correto | ✅ | nonce + ciphertext + tag |
| Decriptação segura | ✅ | Erros genéricos |

## Anti-patterns Encontrados

| Anti-pattern | Severidade | Encontrado? |
|-------------|------------|-------------|
| Reutilização de nonce | 🔴 Crítico | Não |
| Nonce fixo/predizível | 🔴 Crítico | Não |
| Sem AAD | 🟡 Médio | Não |
| Erros expõem detalhes | 🟡 Médio | Não |
| Nonce como counter | 🟡 Médio | Não |
