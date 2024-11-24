import pandas as pd
from strategies.general import init_signal_if_missing


def moving_average_crossover_strategy(
    data: pd.DataFrame, short_window: int, long_window: int, price_col: str
):
    # Compute short-term moving average
    data["short_ma"] = data[price_col].rolling(window=short_window).mean()

    # Compute long-term moving average
    data["long_ma"] = data[price_col].rolling(window=long_window).mean()

    # Generate buy/sell signals
    init_signal_if_missing(data)
    data["signal"] = data["signal"] + ((data["short_ma"] / data["long_ma"]) - 1) * 1000

    return data
