# Template de Migração

## Metadados

- **Nome:** YYYYMMDD_descricao_curta.sql
- **Autor:** {nome}
- **Data:** {data}
- **Versão:** {versao}

## Descrição

{Descrever o que esta migração faz em 2-3 frases}

## Mudanças

### Tabela Alterada
- `{tabela}`: {descrição da mudança}

### Coluna Adicionada
- `{coluna}` ({tipo}): {descrição}

### Índice Criado
- `idx_{tabela}_{coluna}` em `{tabela}({coluna})`

### Dados Migrados
- {descrição dos dados migrados}

## Pré-requisitos

- [ ] Backup do banco realizado
- [ ] Migração anterior aplicada com sucesso
- [ ] Dependências instaladas (extensões, etc)

## Instruções

### 1. Aplicar Migração

```bash
# Desenvolvimento
psql -d dev_db -f migrations/YYYYMMDD_descricao.sql

# Produção
migrate -path ./migrations -database $PROD_DB up
```

### 2. Verificar Migração

```bash
# Verificar se tabela foi criada
psql -d dev_db -c "\d {tabela}"

# Verificar dados
psql -d dev_db -c "SELECT COUNT(*) FROM {tabela};"
```

### 3. Testar Rollback

```bash
# Rollback
psql -d dev_db -c "DROP TABLE IF EXISTS {tabela};"

# Verificar rollback
psql -d dev_db -c "\d {tabela}"
```

## SQL

```sql
-- UP
{código da migração}

-- DOWN
{código do rollback}
```

## Validação

### Antes de Commitar

- [ ] Migração roda sem erros
- [ ] Rollback funciona corretamente
- [ ] Dados existentes não são afetados
- [ ] Performance não degrada
- [ ] Comentários estão claros

### Após Deploy

- [ ] Migração aplicada em staging
- [ ] Testes E2E passam
- [ ] Queries continuam rápidas
- [ ] Monitoramento sem alertas

## Rollback

Se algo der errado:

```bash
# Rollback manual
psql -d prod_db -c "DROP TABLE IF EXISTS {tabela};"

# Ou usar migrate
migrate -path ./migrations -database $PROD_DB down 1
```

## Notas

- {Nota adicional 1}
- {Nota adicional 2}

## Referências

- Issue: #{numero}
- PR: #{numero}
- Docs: {link}
