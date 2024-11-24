# 3rd Party.
import os
import json
from typing import List, Dict, TypedDict, Any
import pandas as pd
from enum import Enum

# Local.
from strategies.augmentation import augment_df

DATA_PATH_RAW = "data/raw"
DATA_PATH_POST = "data/pricing"
FUNDS_PATH = "data/portfolios.json"


class DataFormat(str, Enum):
    RAW = DATA_PATH_RAW
    POSTPROCESSED = DATA_PATH_POST


class PortfolioPricing(TypedDict):
    pricing: pd.DataFrame
    data: Dict
    name: str
    type: str
    id: str
    expense_ratio: float
    y1_return: float
    y5_return: float
    daily_return: float
    volatility: float
    average_return: float
    excess_return: float
    sharpe_ratio: float


def get_porfolio_pricing(
    id: str, data_format: DataFormat = DataFormat.RAW
) -> pd.DataFrame:
    df = pd.read_csv(
        os.path.join(data_format, f"{id}.csv"),
        index_col=1 if data_format == DataFormat.RAW else 0,
    ).sort_values(by="asOfDate", ascending=True)
    return df


def get_all_portfolio_pricing(portfolio_ids: List[str]) -> List[pd.DataFrame]:
    return [get_porfolio_pricing(id) for id in portfolio_ids]


def get_all_portfolios() -> List[Dict]:
    with open(FUNDS_PATH, "r") as f:
        return json.load(f)


def get_all_portfolios_as_dict(
    risk_free_rate: float,
    data_format: DataFormat = DataFormat.RAW,
) -> Dict[str, PortfolioPricing]:
    """Obtains all the porfolios as a dictionary where the keys are the IDs, and the value custom structures.

    Returns:
        Dict[str, PortfolioPricing]: with all the portfolios data.
    """

    def load_data(
        id: str, risk_free_rate: float, augment: bool = False
    ) -> Dict[str, Any]:
        d = get_porfolio_pricing(id, data_format=data_format)
        return {
            "pricing": d,
            **augment_df(
                d,
                price_column="price",
                has_weekends=data_format == DataFormat.POSTPROCESSED,
                risk_free_rate=risk_free_rate,
            )
            .iloc[-1]
            .to_dict(),
        }

    return {
        p["portId"]: {
            "data": p,
            "name": p["name"],
            "type": p["shareClass"],
            "id": p["portId"],
            "expense_ratio": p["ocfValue"],
            **load_data(p["portId"], risk_free_rate=risk_free_rate),
        }
        for p in get_all_portfolios()
    }
