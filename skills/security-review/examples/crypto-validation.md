# Example: Cryptography Validation — AES-256-GCM

## Context

Application stores sensitive data (tokens, credentials) encrypted with AES-256-GCM. Needs to validate that the implementation is correct and secure.

## Validation Checklist

### 1. Key Generation

```python
# ✅ CORRECT: Use PBKDF2/scrypt/Argon2 to derive key from password
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,  # 16 bytes random
    iterations=600_000,  # minimum OWASP 2023
)
key = kdf.derive(password.encode())

# ❌ WRONG: Use simple hash (MD5, SHA-256) as key
key = hashlib.sha256(password.encode()).digest()  # DO NOT DO THIS
```

**Validation:**
- [ ] KDF uses PBKDF2 (≥600k iterations), scrypt (N≥16384), or Argon2id
- [ ] Salt is random and unique per record (≥16 bytes)
- [ ] Salt is stored along with the ciphertext (not secret)

### 2. Nonce/IV

```python
# ✅ CORRECT: Random 12-byte nonce (96 bits) for GCM
import os
nonce = os.urandom(12)  # 96 bits = standard for GCM

# ❌ WRONG: Reuse nonce with the same key
nonce = b'\x00' * 12  # NEVER do this
nonce = bytes.fromhex('000000000000000000000000')  # NEVER
```

**Validation:**
- [ ] Nonce has 12 bytes (96 bits) for GCM
- [ ] Nonce is generated randomly (`os.urandom(12)`)
- [ ] Nonce is not derived from sequential counter (risk of collision)
- [ ] Never reuse key-nonce pair

### 3. Authentication (AAD)

```python
# ✅ CORRECT: Use Additional Authenticated Data (AAD)
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

aesgcm = AESGCM(key)
# AAD authenticates metadata without encrypting it
ciphertext = aesgcm.encrypt(nonce, plaintext, aad=user_id.encode())

# ❌ WRONG: Do not use AAD (lose authentication context)
ciphertext = aesgcm.encrypt(nonce, plaintext, None)
```

**Validation:**
- [ ] AAD includes record identifier (user_id, record_id)
- [ ] AAD is verified during decryption (if mismatch, fail)
- [ ] AAD does not contain sensitive data (is authenticated, not encrypted)

### 4. Storage

```python
# ✅ CORRECT: Store nonce + ciphertext + tag together
import base64

# Format: base64(nonce || ciphertext || tag)
encrypted = base64.b64encode(nonce + ciphertext).decode()

# ✅ OR: Structured JSON format
encrypted_data = {
    "ciphertext": base64.b64encode(ciphertext).decode(),
    "nonce": base64.b64encode(nonce).decode(),
    "aad": user_id,
    "algorithm": "AES-256-GCM",
    "version": 1
}

# ❌ WRONG: Store only ciphertext
encrypted = base64.b64encode(ciphertext).decode()  # nonce lost!
```

**Validation:**
- [ ] Nonce is stored (not recalculated)
- [ ] Format includes all necessary fields for decryption
- [ ] Nonce is not considered secret (can be stored in plaintext)

### 5. Decryption

```python
# ✅ CORRECT: Verify authentication before decrypting
def decrypt(encrypted_data: dict, key: bytes) -> bytes:
    nonce = base64.b64decode(encrypted_data["nonce"])
    ciphertext = base64.b64decode(encrypted_data["ciphertext"])
    aad = encrypted_data.get("aad", "").encode()

    aesgcm = AESGCM(key)
    try:
        plaintext = aesgcm.decrypt(nonce, ciphertext, aad)
        return plaintext
    except Exception:
        # DO NOT expose decryption error details
        raise ValueError("Invalid or corrupted data")

# ❌ WRONG: Expose decryption error details
except InvalidTag as e:
    raise ValueError(f"Invalid tag: {e}")  # NEVER do this
```

**Validation:**
- [ ] Decryption errors are generic (do not expose cause)
- [ ] AAD is verified during decryption
- [ ] Corrupted data causes failure (do not output partial data)

## Audit Summary

| Check | Status | Observation |
|-------|--------|-------------|
| Correct KDF | ✅ | PBKDF2 with 600k iterations |
| Unique nonce | ✅ | os.urandom(12) |
| AAD used | ✅ | user_id as AAD |
| Correct storage | ✅ | nonce + ciphertext + tag |
| Secure decryption | ✅ | Generic errors |

## Anti-patterns Found

| Anti-pattern | Severity | Found? |
|-------------|------------|-------------|
| Reusing nonce | 🔴 Critical | No |
| Predictable nonce | 🔴 Critical | No |
| No AAD | 🟡 Medium | No |
| Exposing error details | 🟡 Medium | No |
| Nonce as counter | 🟡 Medium | No |
