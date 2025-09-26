from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

REPORTS_DIR = Path(__file__).resolve().parent / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

def plot_equity_curves(eq_strat: pd.Series, eq_bh: pd.Series, title: str = "", save: bool = True):
    eq_strat = eq_strat.dropna()
    eq_bh = eq_bh.reindex(eq_strat.index).dropna()

    plt.figure(figsize=(10, 5))
    eq_bh.plot(label="Buy & Hold")
    eq_strat.plot(label="Strategy")
    plt.title(title or "Equity Curves")
    plt.ylabel("Growth of $1")
    plt.legend()
    plt.tight_layout()
    if save:
        out = REPORTS_DIR / f"equity_{eq_strat.index[0].date()}_{eq_strat.index[-1].date()}.png"
        plt.savefig(out, dpi=150)
        print("Saved:", out)
    plt.show()

def plot_mean_reversion_signals(price: pd.Series,
                                lookback: int,
                                z_enter: float,
                                z_exit: float,
                                signal: pd.Series,
                                title: str = "",
                                save: bool = True):
    """Plot price with SMA bands and entry/exit signals."""
    price = price.dropna()
    signal = signal.reindex(price.index).fillna(0)

    sma = price.rolling(lookback, min_periods=lookback).mean()
    std = price.rolling(lookback, min_periods=lookback).std(ddof=0)

    upper = sma + std
    lower = sma - std

    # entry/exit bands
    chg = signal.diff().fillna(signal)
    entries = chg[chg > 0].index
    exits = chg[chg < 0].index

    plt.figure(figsize=(12, 6))
    price.plot(label="Price")
    sma.plot(label=f"SMA({lookback})")
    upper.plot(label=f"Upper Band (+1 STD)", linestyle="--", linewidth=1)
    lower.plot(label=f"Lower Band (-1 STD)", linestyle="--", linewidth=1)

    # entry/exit markers
    if len(entries) > 0:
        plt.scatter(entries, price.loc[entries], marker="^", s=60, label="Enter (buy)")
    if len(exits) > 0:
        plt.scatter(exits, price.loc[exits], marker="v", s=60, label="Exit (flat)")

    plt.title(title or f"Mean Reversion Signals (LB={lookback}, enter={z_enter}, exit={z_exit}")
    plt.ylabel("Price")
    plt.legend()
    plt.tight_layout()
    if save:
        out = REPORTS_DIR / f"meanrev_{price.index[0].date()}_{price.index[-1].date()}.png"
        plt.savefig(out, dpi=150)
        print("Saved:", out)
    plt.show()