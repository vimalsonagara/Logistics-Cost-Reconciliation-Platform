import pandas as pd
from backend.utils.logger import logger

REQUIRED_COLUMNS = {"truck_id", "capacity", "assigned_load", "company"}

def read_excel(path: str) -> pd.DataFrame:
    logger.info(f"Reading excel: {path}")
    df = pd.read_excel(path, engine="openpyxl")
    df.columns = [c.lower() for c in df.columns]
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    df["capacity"] = pd.to_numeric(df["capacity"], errors="coerce")
    df["assigned_load"] = pd.to_numeric(df["assigned_load"], errors="coerce")
    df = df.dropna(subset=["truck_id"]).copy()
    bad = df[df["assigned_load"] > df["capacity"]]
    if not bad.empty:
        raise ValueError(f"Assigned_load exceeds capacity for rows: {bad.index.tolist()}")
    df["company"] = df["company"].astype(str)
    df["truck_id"] = df["truck_id"].astype(str)
    return df
