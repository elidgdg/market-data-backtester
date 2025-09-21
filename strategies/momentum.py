import pandas as pd

def momentum_threshold(price: pd.Series, lookback: int = 60, threshold: float = 0.05) -> pd.Series:
    """
    Long-only (0/1) signal based on momentum threshold.
    Signals are aligned to today, backtester will shift by 1 to avoid lookahead bias.
    """
    # past return over lookback period
    past_ret = price.pct_change(periods=lookback)

    sig = (past_ret >= threshold).astype(float)
    sig[past_ret.isna()] = 0.0 # no signal until enough data
    sig.name = "signal"
    return sig