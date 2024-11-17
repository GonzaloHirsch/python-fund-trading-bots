import os
import json
from typing import List, Dict
import pandas as pd

DATA_PATH = "data/pricing"
FUNDS_PATH = "data/portfolios.json"


def get_porfolio_pricing(id: str) -> pd.DataFrame:
    df = pd.read_csv(os.path.join(DATA_PATH, f"{id}.csv"), index_col=1)
    df_reindexed = df.reindex(index=df.index[::-1])
    return df_reindexed


def get_all_portfolio_pricing(portfolio_ids: List[str]) -> List[pd.DataFrame]:
    return [get_porfolio_pricing(id) for id in portfolio_ids]


def get_all_portfolios() -> List[Dict]:
    with open(FUNDS_PATH, "r") as f:
        return json.load(f)
