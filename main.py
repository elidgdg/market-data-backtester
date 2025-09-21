from data_pipeline import get_data
from helpers import select_price, metrics, pretty_print_metrics
from strategies.ma import moving_average_crossover
from strategies.momentum import momentum_threshold
from backtester import backtest

def run_compare(
        ticker="AAPL",
        start="2019-01-01",
        end="2024-12-31",
        fee_bps=10.0,
        ma_short=20,
        ma_long=50,
        mom_lookback=60,
        mom_threshold=0.05,
):
    # load data
    info = get_data(ticker, start=start, end=end, interval="1d", auto_adjust=True)
    df = info['df']
    price = select_price(df)

    # MA strategy
    sig_ma = moving_average_crossover(price, short=ma_short, long=ma_long)
    res_ma = backtest(price, sig_ma, fee_bps=fee_bps)
    met_ma = metrics(res_ma['strat_ret'])

    # Buy and hold
    met_bh = metrics(res_ma['asset_ret'])

    # Momentum strategy
    sig_mo = momentum_threshold(price, lookback=mom_lookback, threshold=mom_threshold)
    res_mo = backtest(price, sig_mo, fee_bps=fee_bps)
    met_mo = metrics(res_mo['strat_ret'])

    print(f"\n=== {ticker} {start}->{end} | fee={fee_bps} bps ===")
    print(f"Buy&Hold : {pretty_print_metrics(met_bh)}")
    print(f"MA({ma_short},{ma_long}) : {pretty_print_metrics(met_ma)}")
    print(f"Momentum(LB={mom_lookback}, thr={mom_threshold:.2f}) : {pretty_print_metrics(met_mo)}")

if __name__ == "__main__":
    run_compare()