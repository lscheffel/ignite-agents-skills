# Estratégia de Índices

## Visão Geral

Documento de planejamento e estratégia de índices para o schema do banco de dados.

## Análise de Queries

### Queries Frequentes

| Query | Tabela | Colunas de Filtro | Frequência | Prioridade |
|-------|--------|-------------------|------------|------------|
| Login por email | users | email | 1000/dia | Alta |
| Pedidos do usuário | orders | user_id, status | 500/dia | Alta |
| Produtos por categoria | products | category_id | 300/dia | Média |
| Relatório mensal | orders | created_at | 10/dia | Baixa |

### Queries de Análise

```sql
-- Query 1: Login
SELECT id, name, email FROM users WHERE email = ? AND is_active = true;

-- Query 2: Pedidos do usuário
SELECT id, status, total, created_at
FROM orders
WHERE user_id = ? AND status IN ('pending', 'processing')
ORDER BY created_at DESC;

-- Query 3: Produtos por categoria
SELECT id, name, price, slug
FROM products
WHERE category_id = ? AND status = 'active'
ORDER BY name;
```

## Índices Planejados

### Índices Únicos

```sql
-- Email para login
CREATE UNIQUE INDEX idx_users_email ON users(email)
    WHERE is_deleted = FALSE;

-- Slug para URLs
CREATE UNIQUE INDEX idx_products_slug ON products(slug)
    WHERE is_deleted = FALSE;
```

### Índices Compostos

```sql
-- Pedidos do usuário por status
CREATE INDEX idx_orders_user_status ON orders(user_id, status)
    INCLUDE (total, created_at);

-- Produtos por categoria e status
CREATE INDEX idx_products_category_status ON products(category_id, status)
    INCLUDE (name, price);
```

### Índices Parciais

```sql
-- Apenas pedidos pendentes
CREATE INDEX idx_orders_pending ON orders(created_at)
    WHERE status = 'pending';

-- Apenas usuários ativos
CREATE INDEX idx_users_active ON users(email)
    WHERE is_active = TRUE AND is_deleted = FALSE;
```

### Índices para Full-Text Search

```sql
-- Busca por nome de produto
CREATE INDEX idx_products_name_gin ON products
    USING gin(name gin_trgm_ops);

-- Busca em descrição
CREATE INDEX idx_products_description_gin ON products
    USING gin(to_tsvector('portuguese', description));
```

## Selectividade

### Análise por Coluna

| Coluna | Selectividade | Recomendação |
|--------|---------------|--------------|
| users.email | 100% | Único |
| users.is_active | 2% | Índice parcial |
| orders.status | 4 valores | Índice composto |
| orders.user_id | 50% | Índice composto |
| products.category_id | 10% | Índice simples |

### Fórmula de Selectividade

```
Selectividade = (Valores Únicos / Total de Registros) × 100
```

- **> 30%**: Bom para índice simples
- **10-30%**: Índice composto pode ajudar
- **< 10%**: Índice parcial ou composto necessário
- **< 1%**: Índice provavelmente ineficiente

## Ordem de Índices Compostos

### Regra Geral

1. Colunas com igualdade (=) primeiro
2. Colunas com range (>, <, BETWEEN) depois
3. Colunas com ORDER BY por último

### Exemplo

```sql
-- Query: WHERE user_id = ? AND status = 'pending' AND created_at > ?
-- Índice correto:
CREATE INDEX idx_orders_composite ON orders(user_id, status, created_at);
--                       igualdade      range
```

## Monitoramento

### Queries Lentas

```sql
-- Encontrar queries lentas (PostgreSQL)
SELECT query, calls, mean_time, total_time
FROM pg_stat_statements
WHERE mean_time > 100  -- mais de 100ms
ORDER BY mean_time DESC;
```

### Índices Não Utilizados

```sql
-- Índices que nunca foram usados
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;
```

### Tamanho dos Índices

```sql
-- Tamanho dos índices por tabela
SELECT
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) as size
FROM pg_stat_user_indexes
ORDER BY pg_relation_size(indexrelid) DESC;
```

## Manutenção

### Tarefas Mensais

- [ ] Verificar queries lentas no monitoramento
- [ ] Reindexar tabelas com muitas atualizações
- [ ] Remover índices não utilizados
- [ ] Atualizar estatísticas (ANALYZE)

### Tarefas por Deploy

- [ ] Criar índices para novas queries
- [ ] Verificar performance antes e depois
- [ ] Documentar novos índices

## Custos e Benefícios

### Custo de Índices

- Espaço em disco (20-30% do tamanho da tabela)
- Tempo de INSERT/UPDATE/DELETE
- Manutenção em réplicas

### Benefício de Índices

- Queries de leitura 10-100x mais rápidas
- Redução de I/O
- Melhor uso de cache

## Decisões

| Decisão | Justificativa | Data |
|---------|---------------|------|
| Índice em users.email | Login frequente, 100% selectividade | YYYY-MM-DD |
| Índice parcial em orders | Apenas 10% são pendentes | YYYY-MM-DD |
| Índice GIN em products | Busca por nome é frequente | YYYY-MM-DD |

## Referências

- [PostgreSQL Indexing](https://www.postgresql.org/docs/current/indexes.html)
- [Use The Index, Luke](https://use-the-index-luke.com/)
- `data-modeling` — Schema e normalização
