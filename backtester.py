from __future__ import annotations
import pandas as pd
import numpy as np

def backtest(
        price: pd.Series,
        signal: pd.Series,
        fee_bps: float = 10.0 # 1 bps = 0.01% (0.0001)
) -> dict:
    """
    price: price series (daily)
    signal: desired position today. Executed next day.
    """
    price = price.dropna()
    signal = signal.reindex(price.index).fillna(0.0)

    # Daily assets returns
    asset_ret = price.pct_change().fillna(0.0)

    # Position we hold today (based on yesterday's signal)
    pos = signal.shift(1).fillna(0.0)

    # Transaction costs: charge when position changes
    turnover = pos.diff().abs().fillna(pos.abs())
    fee_rate = fee_bps / 10000.0
    fees = turnover * fee_rate

    # Strategy returns
    strat_ret_gross = pos * asset_ret
    strat_ret = strat_ret_gross - fees

    # Equity curves
    eq_strat = (1 + strat_ret).cumprod()
    eq_bh = (1 + asset_ret).cumprod() # Buy and hold

    return {
        "asset_ret": asset_ret,
        "pos": pos,
        "turnover": turnover,
        "fees": fees,
        "strat_ret" : strat_ret,
        "eq_strat": eq_strat,
        "eq_bh": eq_bh
    }