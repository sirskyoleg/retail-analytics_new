-- Create schema if it doesn't exist
-- This ensures the schema exists before creating tables
CREATE CATALOG IF NOT EXISTS IDENTIFIER(:catalog)
COMMENT 'Gold layer catalog for retail analytics';
CREATE SCHEMA IF NOT EXISTS IDENTIFIER(:catalog || '.' || :schema)
COMMENT 'Gold layer schema for retail analytics';

-- Grant permissions to test group (compatible with UC privilege version 1.0)
-- Note: GRANT statements don't support IDENTIFIER() or parameter concatenation
-- These will need to be run separately with actual values, or use catalog-level grants


GRANT USE CATALOG ON CATALOG IDENTIFIER(CONCAT(:catalog)) TO `test`;
GRANT SELECT ON SCHEMA IDENTIFIER(CONCAT(:catalog, '.', :schema)) TO `test`;
GRANT USE SCHEMA ON SCHEMA IDENTIFIER(CONCAT(:catalog, '.', :schema)) TO `test`;