import pandas as pd
from pydantic import BaseModel, ConfigDict

class QueryInput(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    question: str
    df: pd.DataFrame