# Database Architecture — Extended References, DDL Patterns & Migration Catalogs

> 💡 **Lazy Loading Reference:** This document contains the templates, DDL scripts, staged migration strategies, partitioning, and an exhaustive catalog of anti-patterns to support the skill [`database-architecture`](../SKILL.md).

---

## 1. DDL Templates & SQL Schemas

### 1.1 SQL Schema Template with Best Practices
```sql
-- Extension for generating UUID
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Users Table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    metadata JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE UNIQUE INDEX idx_users_email ON users(email);
COMMENT ON TABLE users IS 'Stores user credentials and registration data';
COMMENT ON COLUMN users.metadata IS 'User preferences and additional flags (JSONB)';

-- Orders Table
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    total_cents BIGINT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT chk_orders_status CHECK (status IN ('pending', 'processing', 'completed', 'cancelled'))
);
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- Order Items Table
CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id UUID NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price_cents BIGINT NOT NULL
);
CREATE INDEX idx_order_items_order ON order_items(order_id);
```

---

## 2. Safe Production Migration Strategies (Zero Downtime)

### 2.1 Expand / Contract Pattern for Adding NOT NULL Columns
```sql
-- Step 1: Add nullable column (Expand)
ALTER TABLE users ADD COLUMN full_name VARCHAR(200);

-- Step 2: Gradual backfill in background
UPDATE users SET full_name = name WHERE full_name IS NULL;

-- Step 3: Add NOT NULL constraint (Contract)
ALTER TABLE users ALTER COLUMN full_name SET NOT NULL;
```

### 2.2 Partitioning by Date Range
```sql
CREATE TABLE orders_partitioned (
    id UUID,
    user_id UUID NOT NULL,
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);

CREATE TABLE orders_2026_q1 PARTITION OF orders_partitioned
    FOR VALUES FROM ('2026-01-01') TO ('2026-04-01');

CREATE TABLE orders_2026_q2 PARTITION OF orders_partitioned
    FOR VALUES FROM ('2026-04-01') TO ('2026-07-01');
```

---

## 3. Exhaustive Anti-Pattern Catalog

| Severity | Anti-Pattern | Diagnosis | Recommended Solution |
|:---:|---|---|---|
| 🔴 **Critical** | **Migration without Rollback** | Migration with only UP section without DOWN script reversal. | Always version and test UP and DOWN in the CI environment. |
| 🔴 **Critical** | **Table without Primary Key** | Table without primary key violates 1NF and degrades replicas. | Define immutable primary key (preferably UUID v7 or BIGINT). |
| 🟡 **Medium** | **Index with Low Selectivity** | Create B-Tree index on boolean column or with <3 values. | Use partial indexes (`WHERE is_active = true AND status = 'pending'`). |
| 🟡 **Medium** | **Over-Normalization in Read Path** | More than 6 JOINs in high-frequency queries. | Use Materialized Views or denormalized tables. |
| 🟢 **Low** | **SELECT * in Production** | Unnecessary I/O and memory usage in large tables. | Explicitly project only the consumed columns by the contract. |