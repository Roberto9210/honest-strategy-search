"""Download ES.n.0 (front-month by open interest) OHLCV-1m from GLBX.MDP3, 2010-06-06 -> today.

Streams to data/es_1min_databento.dbn.zst (raw, billed once), then writes data/es_1min_databento.csv.
If the .dbn.zst already exists, it is re-used (no second charge).
"""
from __future__ import annotations

import os
import sys
import time
from datetime import date
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")
key = os.environ.get("DATABENTO_API_KEY")
if not key:
    print("DATABENTO_API_KEY missing")
    sys.exit(2)

import databento as db  # noqa: E402

DATASET, SCHEMA, SYMBOL = "GLBX.MDP3", "ohlcv-1m", "ES.n.0"
START, END = "2010-06-06", str(date.today())
DBN = ROOT / "data" / "es_1min_databento.dbn.zst"
CSV = ROOT / "data" / "es_1min_databento.csv"

client = db.Historical(key)

if DBN.exists() and DBN.stat().st_size > 0:
    print(f"re-using {DBN} ({DBN.stat().st_size/1e6:.1f} MB)")
    store = db.DBNStore.from_file(DBN)
else:
    t0 = time.time()
    print(f"requesting {SYMBOL} {SCHEMA} {START}->{END} ...")
    store = client.timeseries.get_range(
        dataset=DATASET,
        symbols=[SYMBOL],
        stype_in="continuous",
        schema=SCHEMA,
        start=START,
        end=END,
        path=str(DBN),
    )
    print(f"downloaded in {time.time()-t0:.0f}s -> {DBN} ({DBN.stat().st_size/1e6:.1f} MB)")

t0 = time.time()
df = store.to_df(price_type="float", pretty_ts=True, map_symbols=True)
print(f"to_df: {len(df):,} rows in {time.time()-t0:.0f}s; columns={list(df.columns)}")
print(df.head(3))
print(df.tail(3))

# `symbol` is the continuous alias (ES.n.0). Resolve the real contract per bar from instrument_id:
# the DBN symbology carries instrument_id intervals; map id -> raw ticker via the (free) symbology.resolve call.
mappings = store.symbology["mappings"][SYMBOL]
import re
pat = re.compile(r"^ES[HMUZ]\d$")
utc_date = df.index.tz_convert("UTC").normalize()
contract = pd.Series(pd.NA, index=df.index, dtype="object")
problems = []
for m in mappings:
    iid = int(m["symbol"])
    # CME re-uses instrument ids over time -> resolve each id ONLY inside its own interval
    for attempt in range(5):
        try:
            res = client.symbology.resolve(dataset=DATASET, symbols=[str(iid)], stype_in="instrument_id",
                                           stype_out="raw_symbol", start_date=str(max(m["start_date"], date(2010, 6, 6))), end_date=str(m["end_date"]))
            break
        except Exception as exc:  # noqa: BLE001
            print(f"  resolve {iid} attempt {attempt+1} failed: {exc!r}"); time.sleep(3 * (attempt + 1))
    else:
        raise RuntimeError(f"resolve failed for {iid}")
    raws = sorted({iv["s"] for iv in res["result"].get(str(iid), [])})
    es = [r for r in raws if pat.match(r)]
    if len(es) != 1:
        problems.append((iid, m["start_date"], m["end_date"], raws))
    raw = es[0] if len(es) == 1 else (raws[0] if raws else f"id:{iid}")
    lo = pd.Timestamp(m["start_date"], tz="UTC"); hi = pd.Timestamp(m["end_date"], tz="UTC")
    contract[(utc_date >= lo) & (utc_date < hi)] = raw
print("intervals:", len(mappings), "unresolved/ambiguous:", problems)
mismatch = int((contract.isna()).sum())
print("bars without contract from intervals:", mismatch)
out = df[["instrument_id", "open", "high", "low", "close", "volume"]].copy()
out.insert(0, "contract", contract.values)
out.index.name = "ts_event_utc"
out.to_csv(CSV, date_format="%Y-%m-%dT%H:%M:%SZ")
print(f"wrote {CSV} ({CSV.stat().st_size/1e6:.1f} MB), {len(out):,} rows, "
      f"{out.index.min()} -> {out.index.max()}")
print("contracts:", out["contract"].nunique(), "first/last:", out["contract"].iloc[0], out["contract"].iloc[-1])
# sanity: contract from interval vs instrument_id in the row
chk = out.groupby("contract")["instrument_id"].nunique()
print("contracts with >1 instrument_id:", chk[chk > 1].to_dict())
