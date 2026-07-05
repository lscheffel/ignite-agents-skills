# Exemplo: Auditoria de Dependências — Projeto Node.js

## Contexto

Aplicação Express.js com 47 dependências diretas. Precisa de auditoria de segurança antes de deploy.

## Ferramentas Utilizadas

- `npm audit` (nativo)
- `snyk test` (complementar)
- Revisão manual de dependências criticas

## Execução

### Passo 1: npm audit

```bash
$ npm audit --json | jq '.metadata.vulnerabilities'
{
  "info": 0,
  "low": 3,
  "medium": 2,
  "high": 1,
  "critical": 0,
  "total": 6
}
```

### Passo 2: Detalhar Vulnerabilidades

| Pacote | Severidade | Vulnerabilidade | Versão Afetada | Fix |
|--------|------------|-----------------|----------------|-----|
| `lodash` | 🟡 Medium | Prototype Pollution | <4.17.21 | Atualizar para 4.17.21 |
| `minimist` | 🟡 Medium | Prototype Pollution | <1.2.6 | Atualizar para 1.2.6 |
| `node-fetch` | 🔴 High | Information Exposure | <2.6.7 | Atualizar para 2.6.7 |
| `express` | 🟢 Low | Open Redirect | <4.18.2 | Atualizar para 4.18.2 |
| `qs` | 🟢 Low | Prototype Pollution | <6.11.0 | Atualizar para 6.11.0 |
| `cookie` | 🟢 Low | Insufficient Validation | <0.5.0 | Atualizar para 0.5.0 |

### Passo 3: Análise de Impacto

**`node-fetch` (High):**
- Vulnerabilidade: expõe headers de autorização em redirects cross-origin
- Impacto: tokens de acesso podem ser vazados se houver redirect malicioso
- Mitigação: verificar se a aplicação segue redirects (raro em APIs)
- Ação: ATUALIZAR URGENTE

**`lodash` e `minimist` (Medium):**
- Vulnerabilidade: prototype pollution permite injeção de propriedades
- Impacto: depende de como a aplicação processa input do usuário
- Mitigação: verificar se há input não sanitizado passado para essas libs
- Ação: ATUALIZAR

### Passo 4: Correção

```bash
# Atualizar dependências vulneráveis
npm install lodash@4.17.21 minimist@1.2.6 node-fetch@2.6.7 express@4.18.2 qs@6.11.0 cookie@0.5.0

# Verificar correção
npm audit
# expected: 0 vulnerabilities
```

### Passo 5: Validação

```bash
# Rodar testes para garantir que atualizações não quebraram nada
npm test

# Verificar que nenhum lockfile mudou inesperadamente
git diff package-lock.json | grep -E "^\+.*version" | head -10
```

## Resultado

| Métrica | Antes | Depois |
|---------|-------|--------|
| Vulnerabilidades | 6 | 0 |
| High | 1 | 0 |
| Medium | 2 | 0 |
| Low | 3 | 0 |
| Dependências atualizadas | — | 6 |

## Recomendações

1. **Automatizar:** Adicionar `npm audit --audit-level=high` ao CI
2. **Dependabot:** Habilitar dependabot para PRs automáticos
3. **Revisão trimestral:** Auditoria completa a cada trimestre
4. **Lockfile:** Commitar `package-lock.json` sempre
