"""Escalera por hora del dia -- ejecuta terreno_horas_preregistro.md.

Terreno, no ventaja. 23 tenencias de una hora en punto (17:00 CT -> 15:00 CT)
sobre la misma P-escalera de terreno_tenencia.py (ES 1-min Databento, 2016-2019).
Primero el control (suma de horas > tenencia continua); si falla, no hay escalera.

    venv/Scripts/python.exe research/ventaja_futuros/terreno_horas.py > research/ventaja_futuros/terreno_horas.txt
"""

from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from terreno_tenencia import load_databento, window_stats, DEGRADED_UTC, PCTS  # noqa: E402

HOURS = list(range(17, 24)) + list(range(0, 16))          # 17..23, 0..15  -> 23 ventanas
REF = (8 * 60 + 30, 9 * 60 + 30)                          # la hora de la apertura


def hr(t):
    print()
    print("=" * 118)
    print(t)
    print("=" * 118)


def pct(x):
    x = np.asarray(x, dtype=float)
    return {f"p{p}": float(np.percentile(x, p)) for p in PCTS} | {"n": int(len(x))}


def main():
    print("ESCALERA POR HORA DEL DIA -- Ventana D, 2026-09-03. ES 1-min Databento, 2016-01-04 -> 2019-12-31. NO es MES.")
    print("Ejecuta terreno_horas_preregistro.md. Primero el control; sin control no hay escalera.")
    df = load_databento()

    # ---- P-escalera, exactamente como en terreno_tenencia.py
    sess = df.groupby("sess").agg(n_contracts=("contract", "nunique"))
    degraded = set(df.loc[df["utc_date"].isin(DEGRADED_UTC), "sess"].unique())
    t23 = window_stats(df, None, None)
    rth = window_stats(df, 8 * 60 + 30, 15 * 60)
    ok = ((sess.index.weekday < 5) & (sess["n_contracts"] == 1) & (~sess.index.isin(list(degraded)))
          & (t23["first_m"].reindex(sess.index) == 17 * 60)
          & (rth["first_m"].reindex(sess.index) == 8 * 60 + 30)
          & (rth["last_m"].reindex(sess.index) >= 15 * 60 - 1))
    idx = sess.index[ok.fillna(False)]
    hr(f"0. POBLACION: P-escalera = {len(idx)} sesiones ({idx.min().date()} -> {idx.max().date()}); debe ser 971 como en terreno_tenencia.txt")
    assert len(idx) == 971, len(idx)

    # ---- ventanas
    win = {}
    cover = []
    for h in HOURS:
        w = window_stats(df, h * 60, (h + 1) * 60).reindex(idx)
        win[h] = w
        cover.append((h, int(w["open"].isna().sum()), int(((w["first_m"] != h * 60) & w["open"].notna()).sum()),
                      float(w["bars"].median()) if w["bars"].notna().any() else 0.0))
    ref = window_stats(df, *REF).reindex(idx)
    assert ref["open"].notna().all() and (ref["first_m"] == REF[0]).all()
    t23 = t23.reindex(idx)

    hr("0b. COBERTURA por ventana: sesiones sin barra alguna, sesiones sin barra exacta a h:00, mediana de barras")
    print(f"  {'hora':<14}{'sin barra':>10}{'sin h:00':>10}{'barras med':>12}")
    for h, none, inexact, med in cover:
        print(f"  {h:02d}:00->{(h + 1) % 24:02d}:00  {none:>10}{inexact:>10}{med:>12.0f}")

    # ---- CONTROL
    hr("1. CONTROL -- suma de las 23 excursiones horarias (S) contra la tenencia continua 17:00->16:00 (T), por sesion")
    full = idx[np.all([win[h]["open"].notna().reindex(idx).values for h in HOURS], axis=0)]
    print(f"  sesiones con las 23 ventanas cubiertas: {len(full)} de {len(idx)}  (el control se corre sobre estas)")
    verdict_ok = True
    for side in ["largo", "corto"]:
        S = sum(win[h][side].reindex(full) for h in HOURS)
        T = t23[side].reindex(full)
        below = full[(S < T).values]
        ratio = (S / T.replace(0, np.nan)).dropna()
        print(f"  --- {side.upper()} ---")
        print(f"    S media {S.mean():8.2f}  mediana {S.median():8.2f}   |   T media {T.mean():8.2f}  mediana {T.median():8.2f}")
        print(f"    S/T mediana {ratio.median():.3f}  (p10 {ratio.quantile(.1):.3f}, p90 {ratio.quantile(.9):.3f})")
        print(f"    sesiones con S >= T : {int((S >= T).sum())}   con S > T : {int((S > T).sum())}   con S < T : {len(below)}")
        for d in below[:10]:
            print(f"      S < T en {d.date()}: S {S[d]:.2f}  T {T[d]:.2f}  dif {S[d] - T[d]:+.2f}")
        if not (S.mean() > T.mean() and S.median() > T.median() and (S >= T).mean() > 0.99):
            verdict_ok = False
    print()
    print(f"  >>> CONTROL: {'PASA -- S es mayor que T' if verdict_ok else 'FALLA -- el calculo esta mal en algun lado; NO se publica la escalera'}")
    if not verdict_ok:
        sys.exit(1)

    # ---- ESCALERA
    for side in ["largo", "corto"]:
        hr(f"2.{side.upper()} -- excursion adversa {side} por hora de arranque, puntos de ES, y RAZON respecto de 08:30->09:30")
        r = pct(ref[side].values)
        print(f"  {'hora de arranque':<16}{'n':>5} | {'p50':>7}{'p90':>7}{'p95':>7}{'p99':>7} pts | {'p50/ref':>8}{'p90/ref':>8}{'p95/ref':>8}{'p99/ref':>8}")
        print(f"  {'REF 08:30->09:30':<16}{r['n']:>5} | " + "".join(f"{r[k]:>7.2f}" for k in ['p50', 'p90', 'p95', 'p99']) + " pts | " + "".join(f"{1.0:>8.2f}" for _ in range(4)))
        for h in HOURS:
            x = win[h][side].dropna().values
            s = pct(x)
            print(f"  {h:02d}:00->{(h + 1) % 24:02d}:00     {s['n']:>5} | " + "".join(f"{s[k]:>7.2f}" for k in ['p50', 'p90', 'p95', 'p99']) + " pts | "
                  + "".join(f"{s[k] / r[k]:>8.2f}" for k in ['p50', 'p90', 'p95', 'p99']))
        print()

    print("Limitaciones, al pie: ES y no MES (traslado supuesto). Tenencia de horario fijo no es estrategia. NIVELES de")
    print("2016-2019, la mitad de violento que 2016-2026: las razones pueden trasladarse, los niveles no, y que las razones")
    print("aguanten un regimen violento NO esta verificado. No se miro rentabilidad de ninguna hora.")


if __name__ == "__main__":
    main()
