import yfinance as yf
from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True) 

# Download Open High Low Close Volume (OHLCV) data from Yahoo Finance
def fetch_ohlcv(ticker: str, start: str, end: str | None = None,
                interval: str = "1d", auto_adjust: bool = True) -> pd.DataFrame:
    
    df = yf.download(
        tickers=ticker,
        start=start,
        end=end,
        interval=interval,
        auto_adjust=auto_adjust,
        group_by="column",
        progress=False,
        threads=False
    )

    if df.empty:
        raise ValueError(f"No data for ticker {ticker} with start {start} and end {end}")
    
    # Flatten MultiIndex columns if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    
    df = df.sort_index()

    # Ensure data has expected columns
    expected_cols = {"Open", "High", "Low", "Close", "Volume"}
    missing = expected_cols.difference(df.columns)
    if missing:
        raise ValueError(f"Missing columns {missing} for ticker {ticker}")
    
    # Drop duplicate timestamps
    if df.index.duplicated().any():
        df = df[~df.index.duplicated(keep='first')]
    
    # Sanity check for negative prices
    if (df[["Open", "High", "Low", "Close"]] <= 0).any().any():
        raise ValueError(f"Negative or zero prices found for ticker {ticker}")
    
    # volume NaN to 0
    if df["Volume"].isna().any():
        df["Volume"] = df["Volume"].fillna(0)
    
    # Bounds check
    bad = (
        (df["High"] < df["Low"]) |
        (df["Open"] < df["Low"]) |
        (df["Open"] > df["High"]) |
        (df["Close"] < df["Low"]) |
        (df["Close"] > df["High"])
    )
    if bad.any():
        df = df[~bad]
    
    return df

if __name__ == "__main__":
    df = fetch_ohlcv("AAPL", "2020-01-01", "2023-01-01")
    print(df.head())
    print("rows:", len(df))