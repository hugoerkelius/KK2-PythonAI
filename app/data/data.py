import requests, io, os
import pandas as pd
import chardet
from typing import Optional

df: Optional[pd.DataFrame] = None

def load_from_csv(contents: bytes, filename: str) -> pd.DataFrame:
    global df
    if not filename.endswith(".csv"):
        raise ValueError("Måste vara en CSV-fil.")
    if len(contents) == 0:
        raise ValueError("Filen är tom.")
    encoding = chardet.detect(contents)["encoding"] or "utf-8"
    try:
        df = pd.read_csv(io.BytesIO(contents), encoding=encoding)
    except Exception as e:
        raise ValueError(f"Kunde inte läsa filen: {e}")
    if df.empty:
        raise ValueError("Csv filen saknar data")

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

if __name__ == "__main__":
    load_from_api()
    save_to_csv("data/cards.csv")
    print("Sparad!")