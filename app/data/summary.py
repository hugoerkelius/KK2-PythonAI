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
    parts.append(f"\nBilligaste kort:\n{df[['card_name', 'market_price']].sort_values('market_price').head(5).to_string()}")
    parts.append(f"\nKorttyper:\n{df['card_type'].value_counts().to_string()}")
    parts.append(f"\nRaritet:\n{df['rarity'].value_counts().head(5).to_string()}")
    parts.append(f"\nPrisstatistik:\n{df['market_price'].describe().to_string()}")
    parts.append(f"\nStarkaste kort:\n{df[['card_name', 'card_power', 'card_cost']].dropna().sort_values('card_power', ascending=False).head(5).to_string()}")
    parts.append(f"\nAttribut:\n{df['attribute'].value_counts().head(5).to_string()}")
    parts.append(f"\nStörsta prisskillnad:\n{df.assign(diff=df['inventory_price']-df['market_price'])[['card_name','diff']].sort_values('diff', ascending=False).head(3).to_string()}")
    parts.append(f"\nVanligaste sub-typer:\n{df['sub_types'].value_counts().head(5).to_string()}")
    parts.append(f"\nKort per set:\n{df['set_name'].value_counts().head(5).to_string()}")



    return "\n".join(parts)

if __name__ == "__main__":
    from app.data.data import load_from_api
    df = load_from_api()
    print(df.columns.tolist())
    print(df.head(3).to_string())