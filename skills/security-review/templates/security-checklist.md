# Security Checklist

Use este checklist durante revisões de código para garantir práticas de segurança.

## Secrets & Credenciais

- [ ] Nenhum secret hardcoded no código
- [ ] `.env` está no `.gitignore`
- [ ] `.env.example` documenta todas as variáveis
- [ ] Testes usam valores mock/placeholder
- [ ] Logs não expõem dados sensíveis (PII, tokens)

## Dependências

- [ ] `npm audit` / `yarn audit` sem vulnerabilidades críticas
- [ ] Dependências descontinuadas substituídas
- [ ] Licenças compatíveis com o projeto
- [ ] Lock file commitado

## Criptografia

- [ ] Algoritmos adequados (não MD5/SHA1 para senhas)
- [ ] AES-GCM: nonce único de 12 bytes por operação
- [ ] scrypt: N≥16384, r≥8, p≥1
- [ ] Chaves não hardcoded
- [ ] Comparações usam `crypto.timingSafeEqual()`

## Autenticação & Autorização

- [ ] Endpoints autenticados verificados
- [ ] Rate limiting implementado
- [ ] Sessões expiram adequadamente
- [ ] Tokens têm tempo de vida limitado

## Validação de Entrada

- [ ] Inputs sanitizados contra XSS
- [ ] Queries parametrizadas (não concatenação)
- [ ] Upload de arquivos validado (tipo, tamanho)
- [ ] Headers de segurança presentes (CSP, HSTS)

## Referências

- [OWASP Top 10](https://owasp.org/Top10/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)

---

*Checklist de segurança para ignite-agents-skills.*
