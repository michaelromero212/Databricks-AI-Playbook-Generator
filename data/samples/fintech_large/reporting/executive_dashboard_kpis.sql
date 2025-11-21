-- Executive Dashboard KPIs
-- Aggregates risk scores and transaction volumes for reporting.

CREATE OR REPLACE VIEW gold_executive_dashboard AS
SELECT
    date_trunc('day', t.tx_timestamp) as report_date,
    count(t.tx_id) as total_transactions,
    sum(t.amount) as total_volume,
    avg(r.risk_score) as avg_risk_score,
    count(case when r.risk_score > 0.8 then 1 end) as high_risk_alerts
FROM silver_transactions t
JOIN gold_risk_scores r ON t.account_id = r.account_id
GROUP BY 1
ORDER BY 1 DESC;
