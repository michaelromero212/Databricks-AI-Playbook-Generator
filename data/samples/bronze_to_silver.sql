-- Bronze to Silver Transformation
-- Ingests raw clickstream data and cleans it

CREATE OR REPLACE TABLE silver_clickstream AS
SELECT 
  user_id,
  timestamp,
  cost,
  CASE WHEN cost > 100 THEN 'high' ELSE 'low' END as value_segment
FROM raw_clickstream
WHERE timestamp > current_date() - 1;
