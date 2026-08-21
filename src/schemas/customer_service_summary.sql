-- Customer Service Summary Table
-- Aggregated customer service issues by category

CREATE TABLE IF NOT EXISTS IDENTIFIER(:catalog || '.' || :schema || '.customer_service_summary') (
  issue_category STRING COMMENT 'Category of customer service issue',
  total_records BIGINT COMMENT 'Total number of records in this category'
)
USING delta
COMMENT 'Summary of customer service issues grouped by category'
TBLPROPERTIES (
  'delta.enableDeletionVectors' = 'true',
  'delta.parquet.compression.codec' = 'zstd'
);
