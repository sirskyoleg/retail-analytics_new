-- Create schema if it doesn't exist
-- This ensures the schema exists before creating tables
CREATE CATALOG IF NOT EXISTS IDENTIFIER(:catalog)
COMMENT 'Gold layer catalog for retail analytics';
CREATE SCHEMA IF NOT EXISTS IDENTIFIER(:catalog || '.' || :schema)
COMMENT 'Gold layer schema for retail analytics';

-- Grant permissions to test group (compatible with UC privilege version 1.0)
GRANT USE CATALOG ON CATALOG IDENTIFIER(:catalog) TO `test`;
GRANT USE SCHEMA ON SCHEMA IDENTIFIER(:catalog || '.' || :schema) TO `test`;
GRANT SELECT ON SCHEMA IDENTIFIER(:catalog || '.' || :schema) TO `test`;