from pandas import DataFrame


def init_signal_if_missing(data: DataFrame):
    if "signal" not in data.columns:
        data["signal"] = 0
