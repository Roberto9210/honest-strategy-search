"""Potencia con el alfa HEREDADO (Enmienda 1 de hipotesis_congeladas.md).

alfa = 0.05 / (261 + K_D), dos colas para H2d (asi esta congelada). Se imprime K_D = 1 (solo H2d),
2 (H2d + una replica pagada) y 4 (las cuatro hipotesis), y al lado el 0.05 viejo para ver la distancia.

Poblaciones: pares consecutivos MISMO CONTRATO contados desde las FECHAS y CONTRATOS de los CSV del
guardian (37a0144): regla de maximo volumen por fecha, fecha descartada si el contrato cambio. No se
lee ningun precio para nada mas que elegir el contrato por volumen. Tramos: mirado 2016-08-23 ->
2019-12-31 e intocado 2020-01-02 -> 2026-08-21 (la caja del programa), para ES y MES.

    venv/Scripts/python.exe research/ventaja_futuros/potencia_heredada.py > research/ventaja_futuros/potencia_heredada.txt
"""

from __future__ import annotations

import glob
import os
from math import sqrt
from statistics import NormalDist

import pandas as pd

GUARD_CSV = (r"C:\Users\home\AppData\Local\Temp\claude\C--Users-home-Desktop-ALAYA"
             r"\03cf4965-af02-4a1f-8eb0-bc27e9d414df\scratchpad\nt8-daily-csv")
K_BASE = 261
EFFECTS = [0.52, 0.55, 0.56, 0.57, 0.58, 0.60, 0.65]
POWER = 0.80
FRONTERA = pd.Timestamp("2020-01-01")
N = NormalDist()


def pairs_by_tramo(root):
    frames = []
    for fn in sorted(glob.glob(os.path.join(GUARD_CSV, f"{root}_*.csv"))):
        d = pd.read_csv(fn, usecols=["date", "volume"])
        d["contract"] = os.path.basename(fn)[:-4]
        frames.append(d)
    d = pd.concat(frames, ignore_index=True)
    d["date"] = pd.to_datetime(d["date"])
    d = d.sort_values(["date", "volume"], ascending=[True, False])
    sel = d.groupby("date").head(1).sort_values("date").reset_index(drop=True)
    same = sel["contract"] == sel["contract"].shift(1)
    same.iloc[0] = False
    pairs = sel[same]
    n_mir = int((pairs["date"] < FRONTERA).sum())
    n_int = int((pairs["date"] >= FRONTERA).sum())
    return len(sel), int(same.sum()), n_mir, n_int, sel["date"].min().date(), sel["date"].max().date()


def _binom_pmf(n, p):
    from math import lgamma, log, exp
    lp, lq = log(p), log(1 - p)
    return [exp(lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1) + k * lp + (n - k) * lq) for k in range(n + 1)]


def power_two_sided(n, p1, alpha, p0=0.5):
    """Binomial exacta, dos colas simetricas (alpha/2 por cola), potencia contra p1 > p0."""
    if n <= 0:
        return 0.0
    pmf0 = _binom_pmf(n, p0)
    tail, kstar = 0.0, n + 1
    for k in range(n, -1, -1):
        tail += pmf0[k]
        if tail > alpha / 2:
            kstar = k + 1
            break
    if kstar > n:
        return 0.0
    pmf1 = _binom_pmf(n, p1)
    return sum(pmf1[kstar:])


def p_min(n, alpha):
    """Acierto minimo detectable al 80 %, aproximacion normal, dos colas."""
    za, zb = N.inv_cdf(1 - alpha / 2), N.inv_cdf(POWER)
    return 0.5 + (za + zb) * 0.5 / sqrt(n)


def main():
    print("POTENCIA CON ALFA HEREDADO -- Ventana D, 2026-09-03. K = 261 + K_D. H2d a dos colas.")
    alphas = [("K_D=1  a=0.05/262", 0.05 / 262), ("K_D=2  a=0.05/263", 0.05 / 263), ("K_D=4  a=0.05/265", 0.05 / 265), ("viejo  a=0.05", 0.05)]
    for lab, a in alphas:
        print(f"  {lab:<20} alpha = {a:.4e}   z(2 colas) = {N.inv_cdf(1 - a / 2):.3f}")

    print()
    print("=" * 110)
    print("POBLACIONES -- pares consecutivos mismo contrato, contados desde fechas y contratos (sin precios)")
    print("=" * 110)
    pops = {}
    for root in ["ES", "MES", "NQ", "MNQ"]:
        n_dates, n_pairs, n_mir, n_int, d0, d1 = pairs_by_tramo(root)
        pops[root] = (n_pairs, n_mir, n_int)
        print(f"  {root:<4} fechas {n_dates:>5}  pares {n_pairs:>5}  | MIRADO <2020: {n_mir:>5} | INTOCADO >=2020 (caja del programa): {n_int:>5} | {d0} -> {d1}")

    rows = [
        ("ES  intocado (caja) ", pops["ES"][2]),
        ("ES  completo        ", pops["ES"][0]),
        ("ES  mirado <2020    ", pops["ES"][1]),
        ("MES intocado (caja) ", pops["MES"][2]),
        ("MES completo        ", pops["MES"][0]),
        ("MES mirado <2020    ", pops["MES"][1]),
        ("ES+NQ intocado (NO admisible: mismos dias, correlacionados; se imprime para verlo)", pops["ES"][2] + pops["NQ"][2]),
    ]
    for lab, a in alphas:
        print()
        print("=" * 110)
        print(f"POTENCIA, {lab}  (binomial exacta, dos colas)   acierto real ->")
        print("=" * 110)
        print(f"  {'poblacion':<22}{'n':>6} | " + "".join(f"{p:>8.2f}" for p in EFFECTS) + f" | {'p_min 80%':>10}")
        for name, n in rows:
            short = name if len(name) <= 22 else name[:22]
            print(f"  {short:<22}{n:>6} | " + "".join(f"{power_two_sided(n, p, a):>8.3f}" for p in EFFECTS) + f" | {p_min(n, a):>10.4f}")
    print()
    print("  Lectura: '*' no se marca; 0.800 o mas alcanza. La fila ES+NQ es la suma de sesiones de dos libros")
    print("  sobre los mismos dias: NO es N independiente y no se usa. Esta para que se vea lo que inflaria.")
    print("  Descuento no aplicado: los dias con hueco nulo no operan; traslado_signo.txt dice cuantos son.")


if __name__ == "__main__":
    main()
