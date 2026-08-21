"""BOT C — step 0: re-verify F4 (turn-of-month) on PART A only, and price the multiple-testing bill.

Deliberately does NOT call harness.run_on: that function appends to
factory/experiments_ledger.jsonl, which is published evidence with a hash chain. Re-checking a
number that is already in the record must not add a line to the record. So this calls the strategy
and evaluate_trades directly.

It NEVER touches part B (2020-2026). The only thing it computes about B is how many trades the
CALENDAR would produce there, which is a property of the dates, not of the prices.
"""
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import harness  # noqa: E402
from familias_4_5 import turn_of_month  # noqa: E402

A_START, A_END = "2000-01-01", "2019-12-31"
B_START, B_END = "2020-01-01", "2026-12-31"
BEST = {"n_before": 4, "m_after": 3}
N_CONFIGS_TRIED = 57  # spec ledger: 59 entries - 2 harness self-tests


def load(path, price_cols=("open", "high", "low", "close")):
    df = pd.read_csv(path)
    date_col = "date" if "date" in df.columns else df.columns[0]
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.set_index(date_col).sort_index()
    df.columns = [c.lower() for c in df.columns]
    return df


def report(name, res):
    per_year = res.per_year
    positive = sum(1 for v in per_year.values() if v > 0)
    print(f"  {name:<28} PF {res.profit_factor:>6.3f}  trades {res.trades:>4}  "
          f"net ${res.net_pnl:>9,.2f}  DD ${res.max_drawdown:>9,.2f}  "
          f"years+ {positive}/{len(per_year)}")
    return positive, len(per_year)


def net_per_trade(trades):
    gross = trades["points"] * harness.POINT_VALUE * trades["contracts"]
    return gross - harness.FRICTION_RT * trades["contracts"]


def main():
    es = load(os.path.join(REPO, "data", "es_daily.csv"))
    a = es.loc[A_START:A_END]
    print(f"ES daily part A: {a.index.min().date()} -> {a.index.max().date()}, {len(a):,} bars")
    print()

    # ---- 1. reproduce the published number -------------------------------------------------
    print("1. The published F4 result, recomputed (ledger line 16: PF 1.507, 231 trades, $5,845.35)")
    trades = turn_of_month(a, BEST)
    res = harness.evaluate_trades(trades)
    report(f"turn_of_month {BEST}", res)
    match = (abs(res.profit_factor - 1.507) < 0.001 and res.trades == 231
             and abs(res.net_pnl - 5845.35) < 0.01)
    print(f"  reproduces the ledger entry exactly: {match}")
    print()

    # ---- 2. the robustness neighbourhood ---------------------------------------------------
    print("2. Robustness: the integer neighbourhood of (4, 3). The spec asks +/-20% on parameters;")
    print("   on small integers that rounds to +/-1, so the whole 3x3 block is shown.")
    losers = 0
    for nb in (3, 4, 5):
        for ma in (2, 3, 4):
            cfg = {"n_before": nb, "m_after": ma}
            r = harness.evaluate_trades(turn_of_month(a, cfg))
            tag = "  <-- published" if cfg == BEST else ""
            report(f"n_before={nb} m_after={ma}{tag}", r)
            if r.profit_factor < 1.0:
                losers += 1
    print(f"  configurations in the neighbourhood that LOSE money: {losers}/9")
    print()

    # ---- 3. is it significant BEFORE the multiple-testing bill? ----------------------------
    print("3. Significance of the part-A result, and what 57 configurations cost it.")
    net = net_per_trade(trades)
    n = len(net)
    mean, sd = float(net.mean()), float(net.std(ddof=1))
    t = mean / (sd / np.sqrt(n))
    # two-sided p from the normal approximation (n=231 -> t and z agree to 3 decimals)
    from math import erfc, sqrt
    p_raw = erfc(abs(t) / sqrt(2))
    p_bonf = min(1.0, p_raw * N_CONFIGS_TRIED)
    print(f"  mean net per trade  ${mean:,.2f}   sd ${sd:,.2f}   n {n}")
    print(f"  t = {t:.3f}")
    print(f"  p (raw, two-sided)              {p_raw:.4f}")
    print(f"  p x {N_CONFIGS_TRIED} configs tried (Bonferroni)  {p_bonf:.4f}")
    print(f"  survives a 5% bar after the correction: {p_bonf < 0.05}")
    print()

    # ---- 4. how big would the final exam even be? ------------------------------------------
    print("4. Size of the untouched hold-out, from the CALENDAR ONLY (no prices read).")
    b_index = es.loc[B_START:B_END].index
    months = b_index.to_period("M").unique()
    print(f"  part B spans {b_index.min().date()} -> {b_index.max().date()}, "
          f"{len(months)} months => at most {len(months)} trades")
    print(f"  the spec's bar asks for >= {harness.PASS_BAR['min_trades_b']} trades in B.")
    print(f"  {len(months)} < {harness.PASS_BAR['min_trades_b']}: the ORIGINAL bar is unreachable here,")
    print("  and that is precisely why the Phase 1 verdict called F4 'out of scope' rather than 'dead'.")
    print()

    # ---- 5. the SPY cross-check, and why it is weaker than it looks -------------------------
    spy_path = os.path.join(REPO, "data", "spy_daily.csv")
    if os.path.exists(spy_path):
        print("5. The SPY confirmation the verdict mentions, recomputed on the same window.")
        spy = load(spy_path)
        spy_a = spy.loc[A_START:A_END]
        # SPY is an ETF at ~1/10 the index; point value is meaningless here, so this is reported as
        # a SIGN check on gross points, not as money. Saying otherwise would be inventing a contract.
        st = turn_of_month(spy_a, BEST)
        pts = st["points"]
        wins = int((pts > 0).sum())
        print(f"  SPY {spy_a.index.min().date()} -> {spy_a.index.max().date()}: {len(pts)} month-turns, "
              f"{wins} positive ({wins / len(pts):.1%}), mean {pts.mean():.3f} index points")
        print("  NOT an independent confirmation: the QC reports ES/SPY daily return correlation 0.976.")
        print("  It confirms the effect is in the index, not in one contract's quirks. Nothing more.")
    print()

    print("NOTHING IN PART B WAS EVALUATED. The safe is still closed.")


if __name__ == "__main__":
    main()
