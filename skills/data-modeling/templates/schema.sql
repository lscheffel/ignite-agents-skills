-- =====================================================
-- Template de Schema SQL
-- Use: cp templates/schema.sql migrations/YYYYMMDD_create_{table}.sql
-- =====================================================

-- =====================================================
-- UP: Migração para frente
-- =====================================================

-- Tabela principal
CREATE TABLE IF NOT EXISTS {table_name} (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    -- Colunas obrigatórias
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL UNIQUE,

    -- Colunas opcionais
    description TEXT,
    metadata JSONB DEFAULT '{}',

    -- Status e controle
    status VARCHAR(20) DEFAULT 'active'
        CHECK (status IN ('active', 'inactive', 'pending', 'archived')),
    is_deleted BOOLEAN DEFAULT FALSE,

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);

-- Comentários na tabela
COMMENT ON TABLE {table_name} IS '{Descrição da tabela}';
COMMENT ON COLUMN {table_name}.id IS 'Identificador único UUID';
COMMENT ON COLUMN {table_name}.slug IS 'Slug único para URLs amigáveis';
COMMENT ON COLUMN {table_name}.metadata IS 'Dados extras em JSON';
COMMENT ON COLUMN {table_name}.status IS 'Status do registro (active/inactive/pending/archived)';

-- Índices
CREATE UNIQUE INDEX IF NOT EXISTS idx_{table_name}_slug
    ON {table_name}(slug)
    WHERE is_deleted = FALSE;

CREATE INDEX IF NOT EXISTS idx_{table_name}_status
    ON {table_name}(status)
    WHERE is_deleted = FALSE;

CREATE INDEX IF NOT EXISTS idx_{table_name}_created_at
    ON {table_name}(created_at DESC);

-- Trigger para updated_at
CREATE OR REPLACE FUNCTION update_{table_name}_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_{table_name}_updated_at
    BEFORE UPDATE ON {table_name}
    FOR EACH ROW
    EXECUTE FUNCTION update_{table_name}_updated_at();

-- =====================================================
-- Tabela de relacionamento (1:N)
-- =====================================================

CREATE TABLE IF NOT EXISTS {related_table} (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    {parent_table}_id UUID NOT NULL
        REFERENCES {table_name}(id) ON DELETE CASCADE,

    -- Colunas específicas do relacionamento
    name VARCHAR(100) NOT NULL,
    position INTEGER DEFAULT 0,

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_{related_table}_{parent_table}_id
    ON {related_table}({parent_table}_id);

-- =====================================================
-- Tabela de associação (N:M)
-- =====================================================

CREATE TABLE IF NOT EXISTS {junction_table} (
    {table_a}_id UUID NOT NULL
        REFERENCES {table_a}(id) ON DELETE CASCADE,
    {table_b}_id UUID NOT NULL
        REFERENCES {table_b}(id) ON DELETE CASCADE,

    -- Atributos do relacionamento
    role VARCHAR(50) DEFAULT 'member',
    assigned_at TIMESTAMPTZ DEFAULT NOW(),

    PRIMARY KEY ({table_a}_id, {table_b}_id)
);

CREATE INDEX IF NOT EXISTS idx_{junction_table}_{table_b}_id
    ON {junction_table}({table_b}_id);

-- =====================================================
-- Tabela de log/audit
-- =====================================================

CREATE TABLE IF NOT EXISTS {table_name}_audit (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    {table_name}_id UUID NOT NULL,
    action VARCHAR(20) NOT NULL
        CHECK (action IN ('INSERT', 'UPDATE', 'DELETE')),
    old_data JSONB,
    new_data JSONB,
    performed_by UUID,
    performed_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_{table_name}_audit_id
    ON {table_name}_audit({table_name}_id);

CREATE INDEX IF NOT EXISTS idx_{table_name}_audit_performed_at
    ON {table_name}_audit(performed_at DESC);

-- =====================================================
-- DOWN: Rollback (testado!)
-- =====================================================

-- Ordem inversa de criação
DROP TABLE IF EXISTS {table_name}_audit;
DROP TABLE IF EXISTS {junction_table};
DROP TABLE IF EXISTS {related_table};
DROP TRIGGER IF EXISTS trigger_{table_name}_updated_at ON {table_name};
DROP FUNCTION IF EXISTS update_{table_name}_updated_at();
DROP TABLE IF EXISTS {table_name};
