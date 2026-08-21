-- Top Customers Table
-- Top spending customers

CREATE TABLE IF NOT EXISTS IDENTIFIER(:catalog || '.' || :schema || '.top_customers') (
  customer_id STRING COMMENT 'Unique customer identifier',
  name STRING COMMENT 'Customer name',
  total_spent DOUBLE COMMENT 'Total amount spent by customer'
)
USING delta
COMMENT 'Top customers ranked by total spending'
TBLPROPERTIES (
  'delta.enableDeletionVectors' = 'true',
  'delta.parquet.compression.codec' = 'zstd'
);
