-- Bronze to Silver: Customers (SCD Type 2)
-- Maintains history of customer profile changes.

MERGE INTO silver_customers_scd2 target
USING (
    SELECT 
        customer_id,
        email,
        address,
        updated_at
    FROM bronze_kafka_raw
    WHERE event_type = 'CUSTOMER_UPDATE'
) source
ON target.customer_id = source.customer_id
WHEN MATCHED AND target.is_current = true THEN
    UPDATE SET target.is_current = false, target.end_date = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (customer_id, email, address, start_date, is_current)
    VALUES (source.customer_id, source.email, source.address, source.updated_at, true);
