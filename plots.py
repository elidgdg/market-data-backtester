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
