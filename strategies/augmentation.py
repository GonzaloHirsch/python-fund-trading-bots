import pandas as pd
import numpy as np


def augment_df(
    df: pd.DataFrame,
    price_column: str,
    has_weekends: bool = False,
    risk_free_rate: float = 0.01,
) -> pd.DataFrame:
    """Augments a pricing dataframe with metrics.

    Args:
        df (pd.DataFrame): with pricing information.
        price_column (str): name of the column for pricing.
        has_weekends (bool, optional): whether the data is filled for weekends. Defaults to False.
        risk_free_rate (float, optional): current risk free rate. Defaults to 0.01.

    Returns:
        pd.DataFrame: with added columns for
        [
            "y1_return",
            "y5_return",
            "daily_return",
            "volatility",
            "average_return",
            "excess_return",
            "sharpe_ratio"
        ]
    """
    # Compute some constants based on the configuration.
    days_in_1_year = 252
    if has_weekends:
        days_in_1_year = 365
    days_in_5_years = days_in_1_year * 5

    # 1-Year and 5-Year Return
    price_1y_ago = df[price_column].shift(days_in_1_year)
    df["y1_return"] = (df[price_column] - price_1y_ago) / price_1y_ago

    price_5y_ago = df[price_column].shift(days_in_5_years)
    df["y5_return"] = (df[price_column] - price_5y_ago) / price_5y_ago

    # Volatility (annualized standard deviation of daily returns)
    df["daily_return"] = df[price_column].pct_change()
    df["volatility"] = df["daily_return"].rolling(
        window=days_in_1_year
    ).std() * np.sqrt(days_in_1_year)

    # Sharpe Ratio (risk-adjusted return)
    df["average_return"] = df["daily_return"].rolling(window=days_in_1_year).mean()
    df["excess_return"] = df["average_return"] - (risk_free_rate / days_in_1_year)
    df["sharpe_ratio"] = (df["excess_return"] * days_in_1_year) / df["volatility"]

    return df
