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
        progress=False,
        threads=False
    )
    if df.empty:
        raise ValueError(f"No data for ticker {ticker} with start {start} and end {end}")
    
    return df.sort_index()
    

if __name__ == "__main__":
    df = fetch_ohlcv("AAPL", "2020-01-01", "2023-01-01")
    print(df.head())
    print("rows:", len(df))