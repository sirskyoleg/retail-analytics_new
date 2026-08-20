-- Product Revenue Table
-- Revenue aggregated by product

CREATE TABLE IF NOT EXISTS IDENTIFIER(:catalog || '.' || :schema || '.product_wise_revenue') (
  product_name STRING COMMENT 'Name of the product',
  revenue DOUBLE COMMENT 'Total revenue for this product'
)
USING delta
COMMENT 'Product-level revenue summary'
TBLPROPERTIES (
  'delta.enableDeletionVectors' = 'true',
  'delta.parquet.compression.codec' = 'zstd'
);
