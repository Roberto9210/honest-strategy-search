"""DIAGNOSTICO de por que fallo K0 -- NO reabre la pregunta de invariancia_orden_preregistro.md.

La pregunta quedo cerrada por su propio control: K0 exigia que ALTO tuviera excursion mayor que BAJO
y las dos mitades dieron 8.75 pts. Esto no cambia ningun criterio, no vuelve a correr el contraste
principal y no formula ninguna hipotesis nueva. Solo separa tres causas posibles del empate:

  (1) bug de alineacion mio (la etiqueta no corresponde al dia que dice),
  (2) la mediana es un estadistico grueso y las distribuciones si difieren en media o en colas,
  (3) el rango de ayer, con esta particion, no separa la excursion adversa de hoy.

La prueba de alineacion es la clave: el rango de HOY tiene que separar la excursion de HOY casi
perfectamente, porque la excursion es parte del rango por construccion. Si el de hoy separa y el de
ayer no, no hay bug.

    venv/Scripts/python.exe research/ventaja_futuros/invariancia_orden_diagnostico.py > research/ventaja_futuros/invariancia_orden_diagnostico.txt
"""

from __future__ import annotations

import os
import sys
from math import erfc, sqrt

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from terreno_tenencia import load_databento, window_stats, DEGRADED_UTC  # noqa: E402

LOOKBACK = 20
QS = [10, 25, 50, 75, 90, 95, 99]


def hr(t):
    print()
    print("=" * 118)
    print(t)
    print("=" * 118)


def spearman(x, y):
    rx = pd.Series(np.asarray(x, float)).rank().to_numpy()
    ry = pd.Series(np.asarray(y, float)).rank().to_numpy()
    return float(np.corrcoef(rx, ry)[0, 1])


def compare(label, x, mask):
    a, b = x[mask], x[~mask]
    d = a.mean() - b.mean()
    se = sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
    t = d / se
    print(f"  {label}")
    print(f"    ALTO n={len(a):>4} media {a.mean():7.2f} | " + " ".join(f"p{q}={np.percentile(a, q):6.2f}" for q in QS))
    print(f"    BAJO n={len(b):>4} media {b.mean():7.2f} | " + " ".join(f"p{q}={np.percentile(b, q):6.2f}" for q in QS))
    print(f"    diferencia de medias {d:+.3f} pts   t = {t:+.3f}   p = {erfc(abs(t) / sqrt(2)):.3e}   factor de medias {a.mean() / b.mean():.3f}x")


def main():
    print("DIAGNOSTICO DE LA FALLA DE K0 -- Ventana D, 2026-09-03. No reabre la pregunta: no recalcula el contraste principal")
    print("ni los rankings, y no cambia ningun criterio. Separa bug de alineacion, grosor de la mediana y ausencia de senal.")

    df = load_databento()
    sess = df.groupby("sess").agg(n_contracts=("contract", "nunique"))
    degraded = set(df.loc[df["utc_date"].isin(DEGRADED_UTC), "sess"].unique())
    t23 = window_stats(df, None, None)
    rth = window_stats(df, 8 * 60 + 30, 15 * 60)
    ok = ((sess.index.weekday < 5) & (sess["n_contracts"] == 1) & (~sess.index.isin(list(degraded)))
          & (t23["first_m"].reindex(sess.index) == 17 * 60)
          & (rth["first_m"].reindex(sess.index) == 8 * 60 + 30)
          & (rth["last_m"].reindex(sess.index) >= 15 * 60 - 1))
    esc = sess.index[ok.fillna(False)]

    allsess = t23.sort_index()
    allsess["rango"] = allsess["high"] - allsess["low"]
    prev_rango = allsess["rango"].shift(1)
    med20 = allsess["rango"].shift(2).rolling(LOOKBACK).median()
    okc = prev_rango.notna() & med20.notna()
    idx = pd.DatetimeIndex([d for d in esc if bool(okc.get(d, False))])

    alto_ayer = (prev_rango.reindex(idx) >= med20.reindex(idx)).to_numpy(dtype=bool)
    rango_hoy = allsess["rango"].reindex(idx).to_numpy(dtype=float)
    med20_hoy = med20.reindex(idx).to_numpy(dtype=float)
    alto_hoy = rango_hoy >= med20_hoy
    exc = t23["largo"].reindex(idx).to_numpy(dtype=float)
    rango_ayer = prev_rango.reindex(idx).to_numpy(dtype=float)

    hr(f"0. POBLACION: {len(idx)} sesiones, la misma que uso el script de la pregunta")

    hr("1. PRUEBA DE ALINEACION -- el rango de HOY contra la excursion de HOY (tiene que separar; si no, hay bug)")
    compare("particion por rango de HOY (control positivo, NO es la condicion pre-registrada)", exc, alto_hoy)

    hr("2. LA CONDICION PRE-REGISTRADA -- rango de AYER contra su mediana movil")
    compare("particion por rango de AYER (la condicion que fallo K0)", exc, alto_ayer)

    hr("3. CORRELACIONES DE RANGO (Spearman), sobre las mismas sesiones")
    print(f"  rango de HOY  vs excursion adversa de HOY: {spearman(rango_hoy, exc):+.4f}   (por construccion, alto)")
    print(f"  rango de AYER vs excursion adversa de HOY: {spearman(rango_ayer, exc):+.4f}")
    print(f"  rango de AYER vs rango de HOY:             {spearman(rango_ayer, rango_hoy):+.4f}   (esto es el agrupamiento de volatilidad)")
    print(f"  rango de AYER vs rango de HOY, en log:     {float(np.corrcoef(np.log(rango_ayer), np.log(rango_hoy))[0, 1]):+.4f}")

    hr("4. LA MISMA CONDICION CONTRA EL RANGO DE HOY (no contra la excursion): separa el agrupamiento?")
    compare("rango de HOY partido por el estado de AYER", rango_hoy, alto_ayer)

    hr("5. GROSOR DE LA MEDIANA: cuantos valores distintos hay cerca del centro")
    v, c = np.unique(np.round(exc, 2), return_counts=True)
    med = float(np.median(exc))
    near = [(float(a), int(b)) for a, b in zip(v, c) if abs(a - med) <= 0.75]
    print(f"  mediana global de la excursion = {med:.2f} pts; valores a menos de 0.75 pts de ella y su frecuencia:")
    print(f"    {near}")
    print(f"  la excursion es multiplo de 0.25, asi que dos muestras parecidas comparten mediana exacta con facilidad.")
    print()
    print("  LA CAJA SIGUE CERRADA.")


if __name__ == "__main__":
    main()
