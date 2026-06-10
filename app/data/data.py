import requests, io, os
import pandas as pd
from typing import Optional

df: Optional[pd.DataFrame] = None

def load_from_csv(contents: bytes, filename: str) -> pd.DataFrame:
    global df
    if not filename.endswith(".csv"):
        raise ValueError("Måste vara en CSV-fil.")

    df = pd.read_csv(io.BytesIO(contents))
    return df

def save_to_csv(path: str = "data/cards.csv") -> None:
    mapp = os.path.dirname(path)
    if mapp: 
        os.makedirs(mapp, exist_ok=True)
    get_df().to_csv(path, index=False)

def load_from_api() -> pd.DataFrame:
    global df
    response = requests.get("https://optcgapi.com/api/allSetCards/", timeout=10)
    response.raise_for_status()
    df = pd.DataFrame(response.json())
    return df

def get_df() -> pd.DataFrame:
    if df is None:
        raise ValueError("Inget dataset laddat.")
    return df

def get_stats() -> dict:
    return get_df().describe().to_dict()

def get_metadata() -> dict:
    df = get_df()
    return {
        "rows": len(df),
        "columns": df.columns.tolist(),
        "dtypes": df.dtypes.astype(str).to_dict()
    }