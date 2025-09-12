import yfinance as yf
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True) 

if __name__ == "__main__":
    print("data dir:", DATA_DIR)