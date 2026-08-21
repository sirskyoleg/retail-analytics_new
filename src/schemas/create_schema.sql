-- Create schema if it doesn't exist
-- This ensures the schema exists before creating tables
CREATE CATALOG IF NOT EXISTS IDENTIFIER(:catalog)
COMMENT 'Gold layer caralogfor retail analytics';
CREATE SCHEMA IF NOT EXISTS IDENTIFIER(:catalog || '.' || :schema)
COMMENT 'Gold layer schema for retail analytics';

-- Grant permissions to test group
GRANT USAGE ON CATALOG IDENTIFIER(:catalog) TO `test`;
GRANT USAGE ON SCHEMA IDENTIFIER(:catalog || '.' || :schema) TO `test`;
GRANT SELECT ON SCHEMA IDENTIFIER(:catalog || '.' || :schema) TO `test`;