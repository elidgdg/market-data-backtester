from data_pipeline import get_data
from helpers import select_price, metrics, pretty_print_metrics
from strategies.ma import moving_average_crossover
from strategies.momentum import momentum_threshold
from strategies.mean_reversion import mean_reversion
from backtester import backtest
from plots import plot_equity_curves

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

    # Mean Reversion strategy
    sig_mr = mean_reversion(price, lookback=20, z_enter=-1.0, z_exit=0.0)
    res_mr = backtest(price, sig_mr, fee_bps=fee_bps)
    met_mr = metrics(res_mr['strat_ret'])

    print(f"\n=== {ticker} {start}->{end} | fee={fee_bps} bps ===")
    print(f"Buy&Hold : {pretty_print_metrics(met_bh)}")
    print(f"MA({ma_short},{ma_long}) : {pretty_print_metrics(met_ma)}")
    print(f"Momentum(LB={mom_lookback}, thr={mom_threshold:.2f}) : {pretty_print_metrics(met_mo)}")
    print(f"MeanRev(LB=20, z_enter=-1.0, z_exit=0.0) : {pretty_print_metrics(met_mr)}")

    # Plot equity curves
    plot_equity_curves(res_ma['eq_strat'], res_ma['eq_bh'], title=f"{ticker} Equity Curves (fee={fee_bps} bps)")

if __name__ == "__main__":
    run_compare()