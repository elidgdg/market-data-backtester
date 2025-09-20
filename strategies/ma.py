import pandas as pd

def moving_average_crossover(price: pd.Series, short: int = 20, long: int = 50) -> pd.Series:
    """
    Long-only (0/1) signal.
    Signals are aligned to today, backtester will shift by 1 to avoid lookahead bias.
    """
    if short >= long:
        raise ValueError("Short window must be less than long window")
    
    ma_s = price.rolling(window=short, min_periods=short).mean()
    ma_l = price.rolling(window=long, min_periods=long).mean()

    sig = (ma_s > ma_l).astype(float)
    sig[(ma_s.isna()) | (ma_l.isna())] = 0.0 # no signal until both MAs are valid
    sig.name = "signal"
    return sig