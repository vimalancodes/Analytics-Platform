import os
import logging
import pandas as pd
import sqlalchemy.types
from sqlalchemy import text
from db import get_engine
from ingestion.ingestor import ingest_all
from validation.validator import validate_records
from anomaly.detector import detect_anomalies
from insights.ai_insights import generate_insights

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

DATA_DIR = os.getenv("DATA_DIR", "/app/data")

def run_pipeline():
    engine = get_engine()
    logger.info("Pipeline started")

    # 1. Ingest
    raw_df = ingest_all(DATA_DIR)

    # 2. Store raw records (convert all to string to avoid type errors)
    raw_store = raw_df.copy()
    raw_store["quantity"] = raw_store["quantity"].astype(str)
    raw_store["unit_price"] = raw_store["unit_price"].astype(str)
    raw_store["total_amount"] = raw_store["total_amount"].astype(str)
    raw_store.to_sql("raw_records", engine, if_exists="append", index=False, dtype={
        "quantity": sqlalchemy.types.TEXT,
        "unit_price": sqlalchemy.types.TEXT,
        "total_amount": sqlalchemy.types.TEXT,
    })
    logger.info(f"Stored {len(raw_store)} raw records")

    # 3. Validate
    valid_df, invalid_df = validate_records(raw_df)

    # 4. Store valid records
    if not valid_df.empty:
        cols = ["record_id","customer_id","product_id","quantity","unit_price","total_amount","transaction_date","region","category"]
        valid_store = valid_df[[c for c in cols if c in valid_df.columns]].copy()
        valid_store["quantity"] = pd.to_numeric(valid_store["quantity"], errors="coerce")
        valid_store["unit_price"] = pd.to_numeric(valid_store["unit_price"], errors="coerce")
        valid_store["total_amount"] = pd.to_numeric(valid_store["total_amount"], errors="coerce")
        valid_store.to_sql("valid_records", engine, if_exists="append", index=False)
        logger.info(f"Stored {len(valid_store)} valid records")

    ## 5. Store invalid records
    if not invalid_df.empty:
        import json
        import math
        def clean_for_json(obj):
            if isinstance(obj, dict):
                return {k: clean_for_json(v) for k, v in obj.items()}
            elif isinstance(obj, float) and math.isnan(obj):
                return None
            return obj

        with engine.connect() as conn:
            for _, row in invalid_df.iterrows():
                cleaned = clean_for_json(row["raw_data"])
                conn.execute(text("""
                    INSERT INTO invalid_records (record_id, raw_data, validation_errors, source_file)
                    VALUES (:record_id, :raw_data, :errors, :source_file)
                """), {
                    "record_id": row["record_id"],
                    "raw_data": json.dumps(cleaned),
                    "errors": row["validation_errors"],
                    "source_file": row["source_file"]
                })
            conn.commit()
        logger.info(f"Stored {len(invalid_df)} invalid records")

    # 6. Detect anomalies
    anomaly_df = detect_anomalies(valid_df)
    if not anomaly_df.empty:
        anomaly_df.to_sql("anomalies", engine, if_exists="append", index=False)
        logger.info(f"Stored {len(anomaly_df)} anomalies")

    # 7. Compute summary
    total = len(raw_df)
    valid_count = len(valid_df)
    invalid_count = len(invalid_df)
    anomaly_count = len(anomaly_df)
    total_revenue = float(pd.to_numeric(valid_df["total_amount"], errors="coerce").sum()) if not valid_df.empty else 0
    avg_order = round(total_revenue / valid_count, 2) if valid_count > 0 else 0
    top_region = valid_df["region"].value_counts().idxmax() if not valid_df.empty else "N/A"
    top_category = valid_df["category"].value_counts().idxmax() if not valid_df.empty else "N/A"

    summary = {
        "total_records": total,
        "valid_records": valid_count,
        "invalid_records": invalid_count,
        "anomaly_count": anomaly_count,
        "total_revenue": round(total_revenue, 2),
        "avg_order_value": avg_order,
        "top_region": top_region,
        "top_category": top_category
    }

    # 8. Store summary metrics
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO summary_metrics 
            (metric_date, total_records, valid_records, invalid_records, anomaly_count, total_revenue, avg_order_value, top_region, top_category)
            VALUES (CURRENT_DATE, :total, :valid, :invalid, :anomaly, :revenue, :avg, :region, :category)
        """), {
            "total": total, "valid": valid_count, "invalid": invalid_count,
            "anomaly": anomaly_count, "revenue": total_revenue,
            "avg": avg_order, "region": top_region, "category": top_category
        })
        conn.commit()

    # 9. Generate AI insights
    insight_text = generate_insights(summary)
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO ai_insights (insight_type, insight_text, model_used)
            VALUES (:type, :text, :model)
        """), {
            "type": "pipeline_summary",
            "text": insight_text,
            "model": "mock" if os.getenv("OPENAI_API_KEY", "mock") == "mock" else "gpt-3.5-turbo"
        })
        conn.commit()

    logger.info("Pipeline completed successfully!")
    logger.info(f"Summary: {summary}")
    return summary

if __name__ == "__main__":
    run_pipeline()