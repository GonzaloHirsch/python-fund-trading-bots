import pandas as pd

COL_RETURN_1Y = "return_score_1y"
COL_RETURN_5Y = "return_score_5y"
COL_VOLATILITY = "volatility_score"
COL_SHARPE = "sharpe_score"
COL_EXPENSE = "expense_score"
COL_TOTAL = "total_score"


def rank_funds(
    df: pd.DataFrame,
    y1r_col: str = "y1_return",
    y5r_col: str = "y5_return",
    vol_col: str = "volatility",
    srp_col: str = "sharpe_ratio",
    exp_col: str = "expense_ratio",
) -> pd.DataFrame:
    """Assume we have a DataFrame with the following columns for all funds:
    ['Fund Name', '1Y Return', '5Y Return', 'Expense Ratio', 'Volatility', 'Sharpe Ratio']

    Args:
        df (pd.DataFrame): _description_

    Returns:
        pd.DataFrame: _description_
    """
    # Normalize each metric so that they can be compared (min-max normalization)
    df[COL_RETURN_1Y] = (df[y1r_col] - df[y1r_col].min()) / (
        df[y1r_col].max() - df[y1r_col].min()
    )
    df[COL_RETURN_5Y] = (df[y5r_col] - df[y5r_col].min()) / (
        df[y5r_col].max() - df[y5r_col].min()
    )
    df[COL_VOLATILITY] = (df[vol_col].max() - df[vol_col]) / (
        df[vol_col].max() - df[vol_col].min()
    )
    df[COL_SHARPE] = (df[srp_col] - df[srp_col].min()) / (
        df[srp_col].max() - df[srp_col].min()
    )
    df[COL_EXPENSE] = (df[exp_col].max() - df[exp_col]) / (
        df[exp_col].max() - df[exp_col].min()
    )

    # Combine the scores with custom weights
    weights = {
        COL_RETURN_1Y: 0.4,  # 30% weight for returns 1Y
        # COL_RETURN_5Y: 0.05,  # 10% weight for returns 5Y
        COL_VOLATILITY: 0.2,  # 20% weight for volatility (lower is better)
        COL_SHARPE: 0.35,  # 30% weight for Sharpe ratio
        COL_EXPENSE: 0.05,  # 10% weight for expense ratio (lower is better)
    }

    # Computing the total score.
    df[COL_TOTAL] = sum([df[key] * weights[key] for key in weights])

    # Sort by the highest total score
    return df.sort_values(by=COL_TOTAL, ascending=False)
