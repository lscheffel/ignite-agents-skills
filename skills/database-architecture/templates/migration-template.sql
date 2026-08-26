-- SOTA ZERO-DOWNTIME POSTGRESQL MIGRATION TEMPLATE
-- Asset Type: template
-- Parent Skill: database-architecture
-- Description: Standard forward and rollback migration template with transaction safety, index concurrently, and backfill batches.

BEGIN;

-- UP MIGRATION
-- 1. Create table / columns with safe nullable defaults
CREATE TABLE IF NOT EXISTS idempotency_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    key TEXT NOT NULL UNIQUE,
    response_payload JSONB NOT NULL,
    status_code INT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- 2. Concurrently add index outside main transaction lock if needed
-- COMMIT;
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_idempotency_keys_expires_at ON idempotency_keys(expires_at);
-- BEGIN;

COMMIT;

-- DOWN MIGRATION (ROLLBACK):
-- BEGIN;
-- DROP TABLE IF EXISTS idempotency_keys CASCADE;
-- COMMIT;
