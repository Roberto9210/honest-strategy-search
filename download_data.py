"""Download ES=F (daily/1h/5m) and SPY (daily) from Yahoo Finance via yfinance.

Writes raw CSVs into ./data. No cleaning, no adjustment: what Yahoo serves is what lands on disk.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import yfinance as yf

DATA = Path(__file__).resolve().parent / "data"
DATA.mkdir(parents=True, exist_ok=True)

COLS = ["Open", "High", "Low", "Close", "Volume"]


def fetch(symbol: str, interval: str, period: str | None = None, start=None, end=None) -> pd.DataFrame:
    tk = yf.Ticker(symbol)
    kw = dict(interval=interval, auto_adjust=False, actions=False, prepost=False)
    if period:
        kw["period"] = period
    if start is not None:
        kw["start"] = start
    if end is not None:
        kw["end"] = end
    df = tk.history(**kw)
    if df is None or df.empty:
        raise RuntimeError(f"empty frame for {symbol} {interval} {period or (start, end)}")
    df = df[COLS].copy()
    df.columns = [c.lower() for c in df.columns]
    df.index.name = "date" if interval == "1d" else "datetime"
    return df


def write(df: pd.DataFrame, name: str) -> None:
    out = DATA / name
    df.to_csv(out, date_format="%Y-%m-%d" if df.index.name == "date" else "%Y-%m-%dT%H:%M:%S%z")
    tz = getattr(df.index, "tz", None)
    print(f"{name}: {len(df)} rows, {df.index.min()} -> {df.index.max()}, tz={tz}")


def main() -> int:
    jobs = [
        ("ES=F", "1d", "max", "es_daily.csv"),
        ("ES=F", "1h", "730d", "es_1h.csv"),
        ("ES=F", "5m", "60d", "es_5m.csv"),
        ("SPY", "1d", "max", "spy_daily.csv"),
    ]
    failures = []
    for symbol, interval, period, name in jobs:
        try:
            df = fetch(symbol, interval, period=period)
        except Exception as exc:  # noqa: BLE001
            print(f"FAILED {symbol} {interval} {period}: {exc!r}")
            # intraday: retry with an explicit date window slightly inside Yahoo's hard limit
            if interval in ("1h", "5m"):
                days = 729 if interval == "1h" else 59
                end = pd.Timestamp.now(tz="UTC").normalize()
                start = end - pd.Timedelta(days=days)
                try:
                    df = fetch(symbol, interval, start=start, end=end)
                    print(f"  retry with start={start.date()} end={end.date()} OK")
                except Exception as exc2:  # noqa: BLE001
                    print(f"  retry FAILED: {exc2!r}")
                    failures.append(name)
                    continue
            else:
                failures.append(name)
                continue
        write(df, name)
    if failures:
        print("FAILURES:", failures)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
