-- Create schema if it doesn't exist
-- This ensures the schema exists before creating tables

CREATE SCHEMA IF NOT EXISTS IDENTIFIER(:catalog || '.' || :schema)
COMMENT 'Gold layer schema for retail analytics';
