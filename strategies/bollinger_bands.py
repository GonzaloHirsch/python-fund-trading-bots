import pandas as pd
from strategies.general import init_signal_if_missing


def bollinger_bands_strategy(
    data: pd.DataFrame, window: int, num_std: float, price_col: str
):
    # Compute rolling mean and standard deviation
    data["rolling_mean"] = data[price_col].rolling(window=window).mean()
    data["rolling_std"] = data[price_col].rolling(window=window).std()

    # Compute upper and lower bands
    data["upper_band"] = data["rolling_mean"] + (data["rolling_std"] * num_std)
    data["lower_band"] = data["rolling_mean"] - (data["rolling_std"] * num_std)

    # Generate buy/sell signals
    init_signal_if_missing(data)
    data["signal"] = (
        data["signal"] + ((data[price_col] / data["lower_band"]) - 1) * 1000
    )

    return data
