"""El precio del traslado -- Enmienda 1, E1.4. Signo del hueco en ES contra MES, misma fecha.

gap_t = open_t - close_{t-1}, dentro del mismo contrato de cada raiz (maximo volumen por fecha, fecha
descartada si el contrato cambio). NADA de close - open se calcula ni se imprime: esto no mide H2d,
mide si dos libros ven el mismo signo de hueco.

Criterio pre-registrado (E1.4), sobre fechas con ambos huecos no nulos:
  PASA >= 95 % de acuerdo de signo | INDETERMINADO 90-95 % | FALLA < 90 %.

    venv/Scripts/python.exe research/ventaja_futuros/traslado_signo.py > research/ventaja_futuros/traslado_signo.txt
"""

from __future__ import annotations

import glob
import os

import numpy as np
import pandas as pd

GUARD_CSV = (r"C:\Users\home\AppData\Local\Temp\claude\C--Users-home-Desktop-ALAYA"
             r"\03cf4965-af02-4a1f-8eb0-bc27e9d414df\scratchpad\nt8-daily-csv")
TICK = 0.25


def gaps(root):
    frames = []
    for fn in sorted(glob.glob(os.path.join(GUARD_CSV, f"{root}_*.csv"))):
        d = pd.read_csv(fn, usecols=["date", "open", "close", "volume"])
        d["contract"] = os.path.basename(fn)[:-4]
        frames.append(d)
    d = pd.concat(frames, ignore_index=True)
    d["date"] = pd.to_datetime(d["date"])
    d = d.sort_values(["date", "volume"], ascending=[True, False])
    sel = d.groupby("date").head(1).sort_values("date").reset_index(drop=True)
    same = sel["contract"] == sel["contract"].shift(1)
    same.iloc[0] = False
    sel["gap"] = sel["open"] - sel["close"].shift(1)
    out = sel[same][["date", "gap"]].set_index("date")
    return out["gap"]


def report(a, b, la, lb):
    both = pd.concat([a.rename(la), b.rename(lb)], axis=1, join="inner")
    n = len(both)
    za, zb = both[la] == 0, both[lb] == 0
    nz = both[~za & ~zb]
    agree = (np.sign(nz[la]) == np.sign(nz[lb]))
    print(f"  fechas comunes (ambos en mismo contrato): {n}   {both.index.min().date()} -> {both.index.max().date()}")
    print(f"  hueco nulo (open == close_prev exacto): {la} {int(za.sum())} ({100 * za.mean():.1f} %), {lb} {int(zb.sum())} ({100 * zb.mean():.1f} %), alguno {int((za | zb).sum())} ({100 * (za | zb).mean():.1f} %)")
    print(f"  ambos no nulos: {len(nz)}   ACUERDO DE SIGNO: {int(agree.sum())} / {len(nz)} = {100 * agree.mean():.2f} %")
    big = nz[(nz[la].abs() >= TICK) & (nz[lb].abs() >= TICK)]
    ag2 = (np.sign(big[la]) == np.sign(big[lb]))
    print(f"  ambos |gap| >= {TICK}: {len(big)}   acuerdo: {100 * ag2.mean():.2f} %")
    for thr in [0.5, 1.0, 2.0]:
        sub = nz[(nz[la].abs() >= thr) | (nz[lb].abs() >= thr)]
        ags = (np.sign(sub[la]) == np.sign(sub[lb]))
        print(f"  alguno |gap| >= {thr:.2f}: {len(sub):>5}   acuerdo: {100 * ags.mean():.2f} %")
    dis = nz[~agree]
    print(f"  desacuerdos: {len(dis)}; mediana |gap_{la}| en ellos {dis[la].abs().median():.2f}, mediana |gap_{lb}| {dis[lb].abs().median():.2f}; max |gap| entre los dos {max(dis[la].abs().max(), dis[lb].abs().max()) if len(dis) else 0:.2f}")
    print(f"  diferencia gap_{la} - gap_{lb} en TODAS las comunes: mediana |dif| {(both[la] - both[lb]).abs().median():.2f}, p95 {(both[la] - both[lb]).abs().quantile(.95):.2f}, max {(both[la] - both[lb]).abs().max():.2f}")
    print("  por anio (fechas comunes / ambos no nulos / acuerdo %):")
    for y, g in nz.groupby(nz.index.year):
        ag = (np.sign(g[la]) == np.sign(g[lb])).mean()
        print(f"    {y}: {int((both.index.year == y).sum()):>4} / {len(g):>4} / {100 * ag:6.2f} %")
    return 100 * agree.mean(), 100 * (za | zb).mean()


def main():
    print("TRASLADO DEL SIGNO DEL HUECO -- Ventana D, 2026-09-03. CSV del guardian (37a0144). Sin close - open.")
    es, mes = gaps("ES"), gaps("MES")
    print()
    print("=== ES contra MES ===")
    acc, nul = report(es, mes, "ES", "MES")
    v = "PASA" if acc >= 95 else ("INDETERMINADO" if acc >= 90 else "FALLA")
    print()
    print(f"  >>> TRASLADO: {v}  (acuerdo {acc:.2f} % sobre fechas con ambos huecos no nulos; criterio E1.4: >= 95 PASA, 90-95 INDETERMINADO, < 90 FALLA)")
    print(f"  >>> precondicion C0 (rotulo, no veredicto): {nul:.1f} % de fechas con algun hueco nulo")
    print()
    print("=== NQ contra MNQ (mismo control en el otro par, orientacion) ===")
    report(gaps("NQ"), gaps("MNQ"), "NQ", "MNQ")
    print()
    print("=== ES contra NQ (dos indices distintos: para ver cuanto comparten signo, orientacion) ===")
    report(es, gaps("NQ"), "ES", "NQ")


if __name__ == "__main__":
    main()
