from data_pipeline import get_data
from helpers import select_price, metrics
from strategies.ma import moving_average_crossover
from backtester import backtest

def run_demo(ticker="AAPL", start="2019-01-01", end="2024-12-31",
             short=20, long=50, fee_bps=10.0):
    info = get_data(ticker, start=start, end=end, interval="1d", auto_adjust=True)
    df = info["df"]
    price = select_price(df)

    signal = moving_average_crossover(price, short=short, long=long)
    res = backtest(price, signal, fee_bps=fee_bps)

    m_strat = metrics(res["strat_ret"])
    m_bh = metrics(res["asset_ret"])

    print(f"\n=== {ticker} {start}->{end} | MA ({short},{long}) | Fee={fee_bps} bps ===")
    print("Strategy:", {k: round(v, 4) for k, v in m_strat.items()})
    print("Buy&Hold:", {k: round(v, 4) for k, v in m_bh.items()})

if __name__ == "__main__":
    run_demo()