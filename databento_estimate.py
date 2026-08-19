"""Cost estimate ONLY (no data is purchased/downloaded) for ES continuous OHLCV-1m on GLBX.MDP3.

Reads DATABENTO_API_KEY from the environment or from ./.env (never printed).
metadata.get_cost / get_billable_size / get_record_count are free metadata calls.
"""
from __future__ import annotations

import os
import sys
from datetime import date, timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")
key = os.environ.get("DATABENTO_API_KEY")
if not key:
    print("DATABENTO_API_KEY no está definida (env o .env). No se hace ninguna llamada.")
    sys.exit(2)

import databento as db  # noqa: E402

DATASET = "GLBX.MDP3"
SCHEMA = "ohlcv-1m"
START = "2010-06-06"
END = str(date.today())  # end is exclusive in the API; historical data lags ~24h anyway
SYMBOLS = {
    "ES.n.0": "front por open interest",
    "ES.v.0": "front por volumen",
    "ES.c.0": "front por calendario (vencimiento)",
}

client = db.Historical(key)

print(f"dataset={DATASET} schema={SCHEMA} start={START} end={END} (end exclusivo)")
avail = client.metadata.get_dataset_range(DATASET)
print(f"rango disponible del dataset: {avail}")
print()
total = 0.0
for sym, desc in SYMBOLS.items():
    kw = dict(dataset=DATASET, symbols=[sym], schema=SCHEMA, start=START, end=END, stype_in="continuous")
    cost = client.metadata.get_cost(**kw)
    size = client.metadata.get_billable_size(**kw)
    n = client.metadata.get_record_count(**kw)
    total += cost
    print(f"{sym:8s} ({desc}): USD {cost:,.2f} | {size/1e6:,.1f} MB facturables | {n:,} registros")
print()
print(f"Suma de los tres (si se bajaran los tres): USD {total:,.2f}")
print("Crédito gratis: USD 125.00 -> margen si se baja UNO:", f"USD {125 - cost:,.2f}" )
