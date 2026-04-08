import pandas as pd
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def ingest_csv(filepath: str) -> pd.DataFrame:
    logger.info(f"Ingesting CSV file: {filepath}")
    df = pd.read_csv(filepath)
    df["source_file"] = filepath
    logger.info(f"Loaded {len(df)} records from CSV")
    return df

def ingest_json(filepath: str) -> pd.DataFrame:
    logger.info(f"Ingesting JSON file: {filepath}")
    with open(filepath, "r") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df["source_file"] = filepath
    logger.info(f"Loaded {len(df)} records from JSON")
    return df

def ingest_all(data_dir: str) -> pd.DataFrame:
    import os
    frames = []
    for file in os.listdir(data_dir):
        filepath = os.path.join(data_dir, file)
        if file.endswith(".csv") and not file.startswith("sample"):
            frames.append(ingest_csv(filepath))
        elif file.endswith(".json") and not file.startswith("sample") and not file.startswith("chart"):
            frames.append(ingest_json(filepath))
    combined = pd.concat(frames, ignore_index=True)
    logger.info(f"Total records ingested: {len(combined)}")
    return combined