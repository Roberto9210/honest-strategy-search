"""Cuantas barras diarias TRUNCADAS como la del 2016-11-16 hay en los CSV de ES del guardian.

Solo lee los CSV diarios de ES (37a0144). No toca Databento ni 2020+ de minutos: el diario del
guardian ya fue leido entero por Ventana A. Criterio: barra del contrato ELEGIDO (maximo volumen
por fecha) cuyo volumen es menor que el 5 % de la mediana de las 10 barras elegidas anteriores y
las 10 siguientes. Un dia feriado con sesion corta puede caer aca y se lista igual: la lista es
para mirar, no un veredicto.

    venv/Scripts/python.exe research/ventaja_futuros/nt8_barras_truncadas.py > research/ventaja_futuros/nt8_barras_truncadas.txt
"""

from __future__ import annotations

import glob
import os

import pandas as pd

GUARD_CSV = (r"C:\Users\home\AppData\Local\Temp\claude\C--Users-home-Desktop-ALAYA"
             r"\03cf4965-af02-4a1f-8eb0-bc27e9d414df\scratchpad\nt8-daily-csv")
ROOTS = ["ES", "MES", "NQ", "MNQ"]
FRAC = 0.05
HALF = 10


def selected(root):
    frames = []
    for fn in sorted(glob.glob(os.path.join(GUARD_CSV, f"{root}_*.csv"))):
        d = pd.read_csv(fn)
        d["contract"] = os.path.basename(fn)[:-4]
        frames.append(d)
    d = pd.concat(frames, ignore_index=True)
    d["date"] = pd.to_datetime(d["date"])
    d = d.sort_values(["date", "volume"], ascending=[True, False])
    return d.groupby("date").head(1).sort_values("date").reset_index(drop=True)


def main():
    print("BARRAS DIARIAS TRUNCADAS en los CSV del guardian (37a0144), contrato elegido por maximo volumen")
    print(f"criterio: volumen < {FRAC:.0%} de la mediana de las {HALF} barras anteriores y {HALF} siguientes (centrada, sin la propia)")
    for root in ROOTS:
        s = selected(root)
        med = s["volume"].rolling(2 * HALF + 1, center=True, min_periods=HALF).median()
        # sacar la propia barra de la mediana no cambia el resultado con 21 puntos; se deja centrada
        flag = s["volume"] < FRAC * med
        s["ratio"] = s["volume"] / med
        print()
        print(f"--- {root}: {len(s)} fechas, {int(flag.sum())} barras con volumen < {FRAC:.0%} de la mediana local ---")
        for _, r in s[flag].iterrows():
            rango = r["high"] - r["low"]
            print(f"  {r['date'].date()} {r['date'].strftime('%a')}  {r['contract']:<10} V {int(r['volume']):>9}  ({r['ratio']:.4f} de la mediana)"
                  f"  O {r['open']:.2f} H {r['high']:.2f} L {r['low']:.2f} C {r['close']:.2f}  rango {rango:.2f}")
        pre = s[(s["date"] < "2020-01-01") & flag]
        post = s[(s["date"] >= "2020-01-01") & flag]
        print(f"  antes de 2020: {len(pre)}   desde 2020: {len(post)}")


if __name__ == "__main__":
    main()
