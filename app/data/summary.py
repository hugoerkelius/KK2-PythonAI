import pandas as pd
from pydantic import BaseModel, ConfigDict

class QueryInput(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    question: str
    df: pd.DataFrame

def summarize(df: pd.DataFrame) -> str:
    parts = []
    parts.append(f"Antal kort: {df.shape[0]}")
    parts.append(f"\nVanligaste färger:\n{df['card_color'].value_counts().head(3).to_string()}")
    parts.append(f"\nDyraste kort:\n{df[['card_name', 'market_price']].sort_values('market_price', ascending=False).head(5).to_string()}")
    return "\n".join(parts)