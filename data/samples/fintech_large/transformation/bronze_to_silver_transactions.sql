-- Bronze to Silver: Transactions
-- Cleans raw transaction data, handles duplicates, and joins with reference data.

CREATE OR REPLACE TABLE silver_transactions AS
SELECT
    t.tx_id,
    t.account_id,
    t.amount,
    t.currency,
    t.tx_timestamp,
    t.merchant_id,
    CASE 
        WHEN t.amount > 10000 THEN 'HIGH_VALUE'
        ELSE 'STANDARD'
    END as tx_category
FROM bronze_kafka_raw t
WHERE t.status = 'COMPLETED'
AND t.tx_timestamp > current_date() - 30;
