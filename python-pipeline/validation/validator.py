import pandas as pd
import logging

logger = logging.getLogger(__name__)

REQUIRED_FIELDS = ["record_id", "customer_id", "product_id", "quantity", "unit_price", "total_amount", "transaction_date", "region", "category"]

def validate_records(df: pd.DataFrame):
    valid_rows = []
    invalid_rows = []

    for _, row in df.iterrows():
        errors = []

        # Check required fields
        for field in REQUIRED_FIELDS:
            if field not in row or pd.isnull(row[field]) or str(row[field]).strip() == "":
                errors.append(f"Missing or null field: {field}")

        # Check numeric fields
        try:
            qty = float(row["quantity"])
            if qty <= 0:
                errors.append("quantity must be positive")
        except (ValueError, TypeError):
            errors.append("quantity must be a number")

        try:
            price = float(row["unit_price"])
            if price <= 0:
                errors.append("unit_price must be positive")
        except (ValueError, TypeError):
            errors.append("unit_price must be a number")

        try:
            amount = float(row["total_amount"])
            if amount <= 0:
                errors.append("total_amount must be positive")
        except (ValueError, TypeError):
            errors.append("total_amount must be a number")

        if errors:
            invalid_rows.append({
                "record_id": row.get("record_id", "UNKNOWN"),
                "raw_data": row.to_dict(),
                "validation_errors": errors,
                "source_file": row.get("source_file", "")
            })
        else:
            valid_rows.append(row)

    valid_df = pd.DataFrame(valid_rows)
    invalid_df = pd.DataFrame(invalid_rows)

    logger.info(f"Valid records: {len(valid_df)}, Invalid records: {len(invalid_df)}")
    return valid_df, invalid_df