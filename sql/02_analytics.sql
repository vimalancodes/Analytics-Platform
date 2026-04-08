-- =============================================
-- ANALYTICS PLATFORM - ANALYTICAL QUERIES
-- =============================================

-- 1. Revenue by Region
SELECT 
    region,
    COUNT(*) AS total_orders,
    SUM(total_amount) AS total_revenue,
    ROUND(AVG(total_amount), 2) AS avg_order_value
FROM valid_records
GROUP BY region
ORDER BY total_revenue DESC;

-- 2. Revenue by Category
SELECT 
    category,
    COUNT(*) AS total_orders,
    SUM(total_amount) AS total_revenue,
    ROUND(AVG(unit_price), 2) AS avg_unit_price
FROM valid_records
GROUP BY category
ORDER BY total_revenue DESC;

-- 3. Daily Revenue Trend
SELECT 
    transaction_date,
    COUNT(*) AS orders,
    SUM(total_amount) AS daily_revenue,
    ROUND(AVG(total_amount), 2) AS avg_order_value
FROM valid_records
GROUP BY transaction_date
ORDER BY transaction_date;

-- 4. Top 10 Customers by Revenue
SELECT 
    customer_id,
    COUNT(*) AS total_orders,
    SUM(total_amount) AS total_spent,
    ROUND(AVG(total_amount), 2) AS avg_order_value
FROM valid_records
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 10;

-- 5. Validation Summary
SELECT
    COUNT(*) AS total_ingested,
    SUM(CASE WHEN source = 'valid' THEN 1 ELSE 0 END) AS valid_count,
    SUM(CASE WHEN source = 'invalid' THEN 1 ELSE 0 END) AS invalid_count,
    ROUND(
        100.0 * SUM(CASE WHEN source = 'valid' THEN 1 ELSE 0 END) / COUNT(*), 
        2
    ) AS valid_pct
FROM (
    SELECT record_id, 'valid' AS source FROM valid_records
    UNION ALL
    SELECT record_id, 'invalid' AS source FROM invalid_records
) combined;

-- 6. Anomaly Distribution by Type
SELECT 
    anomaly_type,
    detection_method,
    COUNT(*) AS count,
    ROUND(AVG(anomaly_score), 4) AS avg_score,
    MAX(total_amount) AS max_amount
FROM anomalies
GROUP BY anomaly_type, detection_method
ORDER BY count DESC;

-- 7. Monthly Revenue with Running Total (Window Function)
SELECT
    DATE_TRUNC('month', transaction_date) AS month,
    SUM(total_amount) AS monthly_revenue,
    SUM(SUM(total_amount)) OVER (
        ORDER BY DATE_TRUNC('month', transaction_date)
    ) AS running_total
FROM valid_records
GROUP BY DATE_TRUNC('month', transaction_date)
ORDER BY month;