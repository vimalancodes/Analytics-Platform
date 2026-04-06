-- =============================================
-- ANALYTICS PLATFORM - SCHEMA CREATION
-- =============================================

-- 1. RAW RECORDS (all ingested data)
CREATE TABLE IF NOT EXISTS raw_records (
    id SERIAL PRIMARY KEY,
    record_id VARCHAR(50),
    customer_id VARCHAR(50),
    product_id VARCHAR(50),
    quantity INTEGER,
    unit_price NUMERIC(10,2),
    total_amount NUMERIC(10,2),
    transaction_date DATE,
    region VARCHAR(50),
    category VARCHAR(50),
    source_file VARCHAR(100),
    ingested_at TIMESTAMP DEFAULT NOW()
);

-- 2. VALID RECORDS (passed validation)
CREATE TABLE IF NOT EXISTS valid_records (
    id SERIAL PRIMARY KEY,
    record_id VARCHAR(50),
    customer_id VARCHAR(50),
    product_id VARCHAR(50),
    quantity INTEGER,
    unit_price NUMERIC(10,2),
    total_amount NUMERIC(10,2),
    transaction_date DATE,
    region VARCHAR(50),
    category VARCHAR(50),
    processed_at TIMESTAMP DEFAULT NOW()
);

-- 3. INVALID RECORDS (failed validation)
CREATE TABLE IF NOT EXISTS invalid_records (
    id SERIAL PRIMARY KEY,
    record_id VARCHAR(50),
    raw_data JSONB,
    validation_errors TEXT[],
    source_file VARCHAR(100),
    flagged_at TIMESTAMP DEFAULT NOW()
);

-- 4. ANOMALIES (flagged by anomaly detection)
CREATE TABLE IF NOT EXISTS anomalies (
    id SERIAL PRIMARY KEY,
    record_id VARCHAR(50),
    customer_id VARCHAR(50),
    total_amount NUMERIC(10,2),
    anomaly_score NUMERIC(10,4),
    anomaly_type VARCHAR(50),
    detection_method VARCHAR(50),
    detected_at TIMESTAMP DEFAULT NOW()
);

-- 5. AI INSIGHTS
CREATE TABLE IF NOT EXISTS ai_insights (
    id SERIAL PRIMARY KEY,
    insight_type VARCHAR(100),
    insight_text TEXT,
    model_used VARCHAR(100),
    generated_at TIMESTAMP DEFAULT NOW()
);

-- 6. SUMMARY METRICS (pre-aggregated)
CREATE TABLE IF NOT EXISTS summary_metrics (
    id SERIAL PRIMARY KEY,
    metric_date DATE,
    total_records INTEGER,
    valid_records INTEGER,
    invalid_records INTEGER,
    anomaly_count INTEGER,
    total_revenue NUMERIC(12,2),
    avg_order_value NUMERIC(10,2),
    top_region VARCHAR(50),
    top_category VARCHAR(50),
    computed_at TIMESTAMP DEFAULT NOW()
);