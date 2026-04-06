import pandas as pd
import numpy as np
from scipy import stats
import logging

logger = logging.getLogger(__name__)

def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    anomalies = []

    if df.empty or "total_amount" not in df.columns:
        return pd.DataFrame()

    amounts = pd.to_numeric(df["total_amount"], errors="coerce").dropna()

    # Z-Score method
    z_scores = np.abs(stats.zscore(amounts))
    z_anomaly_idx = amounts.index[z_scores > 2.5]

    # IQR method
    Q1 = amounts.quantile(0.25)
    Q3 = amounts.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    iqr_anomaly_idx = amounts.index[(amounts < lower) | (amounts > upper)]

    # Combine both
    all_anomaly_idx = set(z_anomaly_idx).union(set(iqr_anomaly_idx))

    for idx in all_anomaly_idx:
        row = df.loc[idx]
        amount = float(row["total_amount"])
        z = float(np.abs(stats.zscore(amounts))[amounts.index.get_loc(idx)])

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