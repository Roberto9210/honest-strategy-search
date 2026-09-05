"""INVENTARIO 2010-2015 y potencia que traerian -- Ventana D, 2026-09-03. NO gasta cartucho.

Pregunta de Roberto: los minutos de ES de Databento llegan a 2010. Esas sesiones estan fuera de la
caja (que empieza en 2020) y fuera de lo que barrio la fase 1 (2016-2019). Son N nuevo?

Esto NO evalua ninguna estrategia y no mira ningun retorno: cuenta barras por sesion y verifica los
filtros de la P-escalera, que es inventario, y calcula cuanto bajaria el efecto minimo detectable del
cociente de p95 si esas sesiones se sumaran. Ninguna excursion de 2010-2015 se usa para decidir nada.

    venv/Scripts/python.exe research/ventaja_futuros/inventario_2010_2015.py > research/ventaja_futuros/inventario_2010_2015.txt
"""

from __future__ import annotations

import os
import sys
from math import sqrt
from statistics import NormalDist

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from terreno_tenencia import SRC, window_stats, DEGRADED_UTC  # noqa: E402

N = NormalDist()
K_PROG = 263
ALPHA = 0.05 / (K_PROG + 1)
Z_A = N.inv_cdf(1 - ALPHA / 2)
Z_B = N.inv_cdf(0.80)
N_BOOT = 4000
SEED = 20260903
SE_951 = 0.1514        # desvio de log(p95_1/p95_2) medido con 459/492 en potencia_cola.txt


def hr(t):
    print()
    print("=" * 118)
    print(t)
    print("=" * 118)


def load_all():
    """Igual que load_databento pero SIN recortar a 2016+. Solo columnas de tiempo y OHLC."""
    df = pd.read_csv(SRC, usecols=["ts_event_utc", "contract", "open", "high", "low", "close"])
    ts = pd.to_datetime(df["ts_event_utc"], utc=True)
    ct = ts.dt.tz_convert("America/Chicago")
    df["utc_date"] = ts.dt.strftime("%Y-%m-%d")
    df["m"] = ct.dt.hour * 60 + ct.dt.minute
    d = ct.dt.normalize()
    df["sess"] = d.where(df["m"] < 17 * 60, d + pd.Timedelta(days=1)).dt.tz_localize(None)
    return df


def main():
    print("INVENTARIO 2010-2015 -- Ventana D, 2026-09-03. Cuenta barras y sesiones. No evalua ninguna estrategia.")

    df = load_all()
    sess = df.groupby("sess").agg(n_contracts=("contract", "nunique"), bars=("m", "size"))
    t23 = window_stats(df, None, None)
    rth = window_stats(df, 8 * 60 + 30, 15 * 60)
    degraded = set(df.loc[df["utc_date"].isin(DEGRADED_UTC), "sess"].unique())

    filtros = ((sess.index.weekday < 5) & (sess["n_contracts"] == 1) & (~sess.index.isin(list(degraded)))
               & (t23["first_m"].reindex(sess.index) == 17 * 60)
               & (rth["first_m"].reindex(sess.index) == 8 * 60 + 30)
               & (rth["last_m"].reindex(sess.index) >= 15 * 60 - 1)).fillna(False)

    hr("1. SESIONES POR ANO: cuantas hay, cuantas pasan los filtros de la P-escalera, y barras por dia")
    print(f"  {'ano':>6}{'sesiones':>10}{'pasan filtros':>15}{'barras/dia medianas':>22}{'% dias con < 1300 barras':>27}")
    tot_viejo = 0
    for y in range(2010, 2020):
        m = sess.index.year == y
        if not m.any():
            continue
        n = int(m.sum())
        ok = int(filtros[m].sum())
        med_bars = float(sess.loc[m, "bars"].median())
        pobre = float((sess.loc[m, "bars"] < 1300).mean())
        print(f"  {y:>6}{n:>10}{ok:>15}{med_bars:>22.0f}{100 * pobre:>26.1f}%")
        if y <= 2015:
            tot_viejo += ok
    print(f"  2010-2015 que pasan los filtros de la P-escalera: {tot_viejo}")

    hr("2. EL CRITERIO DE CALIDAD DE LA SPEC, aplicado a esos anos con la maquinaria de este repo")
    print("  La spec (seccion 4.4) exige los tres: sesiones comprimidas < 1 %, barras/dia >= 1.300 en promedio,")
    print("  y correlacion anual >= 0.90 contra la referencia diaria. Aca se miden los dos primeros; el tercero")
    print("  exige la serie de Yahoo y ya esta publicado en el QC.")
    print(f"  {'ano':>6}{'barras/dia promedio':>22}{'% dias comprimidos (una barra > 30 % del volumen: no medible sin volumen)':>20}")
    for y in range(2010, 2020):
        m = sess.index.year == y
        if not m.any():
            continue
        print(f"  {y:>6}{float(sess.loc[m, 'bars'].mean()):>22.0f}   (el QC publicado dice: 2010 92.0 %, 2011 86.5 %, 2012 71.2 %, 2013 24.4 %, 2014 26.0 %, 2015 17.0 %, 2016+ 0.0 %)" if y <= 2016 else f"  {y:>6}{float(sess.loc[m, 'bars'].mean()):>22.0f}")

    hr("3. CUANTO BAJARIA EL EFECTO MINIMO DETECTABLE DEL COCIENTE DE p95")
    print("  El desvio del cociente de p95 escala como 1/sqrt(n). Base medida: 0.1514 con 951 sesiones (459/492).")
    print(f"  {'n total':>10}{'desvio implicado':>20}{'MDE del cociente de p95':>28}")
    for n_tot in [951, 951 + 500, 951 + 1000, 951 + 1500, 951 + 3000, 5000, 10000]:
        se = SE_951 * sqrt(951 / n_tot)
        print(f"  {n_tot:>10}{se:>20.4f}{np.exp((Z_A + Z_B) * se):>27.3f}x")
    print()
    print("  Referencia: el efecto que existe es 1.51x. n necesario para que el MDE baje a 1.51x:")
    target = np.log(1.51) / (Z_A + Z_B)
    n_need = 951 * (SE_951 / target) ** 2
    print(f"    desvio requerido = {target:.4f}   ->  n = {n_need:.0f} sesiones, es decir {n_need - 951:.0f} sesiones NUEVAS ({(n_need - 951) / 252:.1f} anos de negociacion)")
    print()
    print("  Con las sesiones de 2010-2015 que pasan los filtros:")
    for lab, extra in [("2013-2015 solamente", 606), ("2010-2015 completo", tot_viejo)]:
        n_tot = 951 + extra
        se = SE_951 * sqrt(951 / n_tot)
        print(f"    {lab:<22} n = {n_tot:>5}   desvio {se:.4f}   MDE {np.exp((Z_A + Z_B) * se):.3f}x   contra 1.51x: {'alcanza' if np.exp((Z_A + Z_B) * se) <= 1.51 else 'NO alcanza'}")

    # ---------------------------------------------------------------- 4. la otra serie
    hr("4. LA OTRA SERIE QUE EXISTE EN ESTE REPO: data/es_daily.csv (Yahoo, ES=F diario)")
    dd = pd.read_csv(os.path.join(os.path.dirname(SRC), "es_daily.csv"), parse_dates=["date"])
    a = dd[(dd["date"] >= "2000-09-18") & (dd["date"] <= "2019-12-31")]
    b = dd[dd["date"] >= "2020-01-01"]
    print(f"  filas totales {len(dd)} ({dd['date'].min().date()} -> {dd['date'].max().date()})")
    print(f"  parte A (desarrollo, 2000-09-18 -> 2019-12-31): {len(a)} sesiones   parte B (la caja): {len(b)}")
    print("  Tiene open, high y low, asi que la excursion adversa diaria (open - low) es medible sin minutos.")
    print("  ADVERTENCIA que hay que leer: NO es la misma ventana que la excursion de la sesion ETH de 17:00 a 16:00")
    print("  que midio toda la escalera. Es el dia de Yahoo sobre un continuo front-month sin ajustar por roll.")
    print("  Es una poblacion distinta, no mas sesiones de la misma.")
    for lab, n_tot in [("parte A sola", len(a)), ("parte A + las 951", len(a) + 951)]:
        se = SE_951 * sqrt(951 / n_tot)
        print(f"    {lab:<20} n = {n_tot:>5}   desvio {se:.4f}   MDE del cociente de p95 {np.exp((Z_A + Z_B) * se):.3f}x   contra 1.51x: {'ALCANZA' if np.exp((Z_A + Z_B) * se) <= 1.51 else 'no alcanza'}")
    print()
    print("  LA CAJA SIGUE CERRADA.")


if __name__ == "__main__":
    main()
