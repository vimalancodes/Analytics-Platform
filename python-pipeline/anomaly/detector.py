import pandas as pd
import numpy as np
from scipy import stats
import logging

logger = logging.getLogger(__name__)

def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    anomalies = []

    if df.empty or "total_amount" not in df.columns:
        return pd.DataFrame()

    # Reset index to avoid index mismatch issues
    df = df.reset_index(drop=True)

    amounts = pd.to_numeric(df["total_amount"], errors="coerce").dropna()

    if len(amounts) < 3:
        return pd.DataFrame()

    # Z-Score method
    z_scores = np.abs(stats.zscore(amounts))
    z_anomaly_idx = amounts.index[z_scores > 2.5].tolist()

    # IQR method
    Q1 = amounts.quantile(0.25)
    Q3 = amounts.quantile(0.75)
    IQR = Q3 - Q1
    upper = Q3 + 1.5 * IQR
    lower = Q1 - 1.5 * IQR
    iqr_anomaly_idx = amounts.index[
        (amounts < lower) | (amounts > upper)
    ].tolist()

    # Combine both
    all_anomaly_idx = list(set(z_anomaly_idx + iqr_anomaly_idx))

    # Build z_score lookup
    z_score_lookup = pd.Series(z_scores.values, index=amounts.index)

    for idx in all_anomaly_idx:
        row = df.loc[idx]
        amount = float(pd.to_numeric(row["total_amount"], errors="coerce"))
        z = float(z_score_lookup.loc[idx])

        method = []
        if idx in z_anomaly_idx:
            method.append("zscore")
        if idx in iqr_anomaly_idx:
            method.append("iqr")

        anomalies.append({
            "record_id": row.get("record_id", "UNKNOWN"),
            "customer_id": row.get("customer_id", "UNKNOWN"),
            "total_amount": amount,
            "anomaly_score": round(z, 4),
            "anomaly_type": "high_value" if amount > upper else "low_value",
            "detection_method": "+".join(method)
        })

    anomaly_df = pd.DataFrame(anomalies)
    logger.info(f"Anomalies detected: {len(anomaly_df)}")
    return anomaly_df