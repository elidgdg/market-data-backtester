import pandas as pd
import numpy as np

def mean_reversion(price: pd.Series,
                   lookback: int = 20, # rolling window for SMA and std
                   z_enter: float = -1.0, # z-score to enter a position
                   z_exit: float = 0.0, # z-score to exit a position
) -> pd.Series:
    """
    Mean-reversion using rolling z-score of price vs SMA.
    Long-only (0/1) strategy.
    """
    sma = price.rolling(lookback).mean()
    vol = price.rolling(lookback, min_periods=lookback).std(ddof=0)
    z = (price - sma) / vol
    z.name = "z"

    # stay flat until enough data
    z_valid = ~(sma.isna() | vol.isna())

    sig = pd.Series(0.0, index=price.index, dtype=float)
    in_pos = False
    for t in range(len(price)):
        if not z_valid.iat[t]:
            sig.iat[t] = 0.0
            continue
        if not in_pos and z.iat[t] <= z_enter:
            in_pos = True # enter long
        elif in_pos and z.iat[t] >= z_exit:
            in_pos = False # exit long
        sig.iat[t] = 1.0 if in_pos else 0.0
    sig.name = "signal"
    return sig
    