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