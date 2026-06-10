import pandas as pd
from pydantic import BaseModel, ConfigDict

class QueryInput(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    question: str
    df: pd.DataFrame
    
def summarize(df: pd.DataFrame) -> str:
    def has(*cols: str) -> bool:
        return set(cols) <= set(df.columns)

    parts = [f"Antal kort: {df.shape[0]}"]

    if has("card_color"):
        parts.append(f"\nVanligaste färger:\n{df['card_color'].value_counts().head(3).to_string()}")

    if has("card_name", "market_price"):
        parts.append(f"\nDyraste kort:\n{df[['card_name', 'market_price']].sort_values('market_price', ascending=False).head(5).to_string()}")
        parts.append(f"\nBilligaste kort:\n{df[['card_name', 'market_price']].sort_values('market_price').head(5).to_string()}")

    if has("card_type"):
        parts.append(f"\nKorttyper:\n{df['card_type'].value_counts().to_string()}")

    if has("rarity"):
        parts.append(f"\nRaritet:\n{df['rarity'].value_counts().head(5).to_string()}")

    if has("market_price"):
        parts.append(f"\nPrisstatistik:\n{df['market_price'].describe().to_string()}")

    if has("card_name", "card_power", "card_cost"):
        parts.append(f"\nStarkaste kort:\n{df[['card_name', 'card_power', 'card_cost']].assign(card_power=pd.to_numeric(df['card_power'], errors='coerce')).dropna(subset=['card_power']).sort_values('card_power', ascending=False).head(5).to_string()}")

    if has("attribute"):
        parts.append(f"\nAttribut:\n{df['attribute'].value_counts().head(5).to_string()}")

    if has("sub_types"):
        parts.append(f"\nVanligaste sub-typer:\n{df['sub_types'].value_counts().head(5).to_string()}")

    if has("set_name", "set_id"):
        parts.append(f"\nKort per set:\n{df[['set_name', 'set_id']].value_counts().head(5).to_string()}")

    return "\n".join(parts)

if __name__ == "__main__":
    from app.data.data import load_from_api
    df = load_from_api()
    print(summarize(df))