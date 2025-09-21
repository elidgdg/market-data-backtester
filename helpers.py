import numpy as np
import pandas as pd

TRADING_DAYS = 252 # Trading days in a year

def select_price(df: pd.DataFrame) -> pd.Series:
    # Use adjusted if available, otherwise close
    return df['Adj Close'] if 'Adj Close' in df.columns else df['Close']

def pct_returns(price: pd.Series) -> pd.Series:
    return price.pct_change().fillna(0.0)

def max_drawdown(equity):
    # Calculate max drawdown given an equity curve
    roll_max = equity.cummax()
    drawdown = equity / roll_max - 1.0
    return float(drawdown.min())

def metrics(returns: pd.Series) -> dict:
    # Cumulative return, annualized vol, sharpe, max drawdown
    mean = returns.mean()
    std = returns.std() # daily return std dev
    ann_ret = mean * TRADING_DAYS
    ann_vol = std * np.sqrt(TRADING_DAYS)
    sharpe = (ann_ret / ann_vol) if ann_vol > 0 else np.nan

    cum_ret = (1 + returns).prod() - 1
    eq = (1 + returns).cumprod()
    mdd = max_drawdown(eq)

    return {
        "cum_ret" : float(cum_ret),
        "ann_vol" : float(ann_vol),
        "sharpe"  : float(sharpe),
        "max_dd"  : float(mdd)
    }

def pretty_print_metrics(m: dict) -> dict:
    # print returns/vol/dd as percentages, sharpe as is
    out = {}
    for k,v in m.items():
        if k in ("cum_ret", "ann_vol", "max_dd"):
            out[k] = round(v * 100, 2)
        else:
            out[k] = round(v, 3)
    return out