import numpy as np
import pandas as pd

TRADING_DAYS = 252 # Trading days in a year

def select_price(df: pd.DataFrame) -> pd.Series:
    # Use adjusted if available, otherwise close
    return df['Adj Close'] if 'Adj Close' in df.columns else df['Close']

def pct_returns(price: pd.Series) -> pd.Series:
    return price.pct_change().fillna(0)