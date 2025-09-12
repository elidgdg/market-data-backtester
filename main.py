from data_pipeline import get_data

def demo():
    aapl = get_data("AAPL", start="2019-01-01", end="2024-12-31", interval="1d", auto_adjust=True)
    print("AAPL:", len(aapl["df"]), "rows |", aapl["source"])

    btc = get_data("BTC-USD", start="2020-01-01", end="2024-12-31", interval="1d", auto_adjust=False)
    print("BTC-USD:", len(btc["df"]), "rows |", btc["source"])

if __name__ == "__main__":
    demo()