-- Daily Sales Transformation
-- Source: Raw CSV uploads
-- Target: Silver Delta Table

CREATE OR REPLACE TABLE silver_sales AS
SELECT 
    transaction_id,
    product_id,
    store_id,
    cast(transaction_date as date) as sale_date,
    quantity * unit_price as total_amount
FROM bronze_sales_csv
WHERE transaction_date IS NOT NULL;
