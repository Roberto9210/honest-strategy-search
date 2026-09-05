"""POTENCIA DEL ESTADISTICO DE COLA -- Ventana D, 2026-09-03. NO gasta cartucho.

Pregunta de Roberto: el 1.52x declarado detectable se calculo para un contraste de MEDIAS en log.
La forma 3 de pregunta_cuanto_y_cuando.md mide COLA. Cual es el efecto minimo detectable para el
estadistico que esa forma usaria de verdad, con alpha heredado y las 951 sesiones?

Esto NO es la pregunta y no la pre-registra. Es la compuerta de potencia que la spec exige calcular
ANTES (seccion 3.2). Por eso, y esto es la linea que separa una cosa de la otra:

    NADA se mide partido por estado. Todas las cantidades de aca son INCONDICIONALES sobre las 951
    sesiones, o simuladas bajo H0 (las dos mitades vienen de la misma distribucion). La tasa de
    superacion por estado -- que es la respuesta de la forma 3 -- no se calcula ni se imprime.

Dos estadisticos, porque la forma 3 admite dos redacciones:
  A) contraste de p95 de la excursion adversa entre los dos grupos (cociente de p95).
  B) contraste de la TASA de superar un umbral L (la redaccion literal: "probabilidad de cruzar el
     limite diario"), para una grilla de L en USD de MES.

    venv/Scripts/python.exe research/ventaja_futuros/potencia_cola.py > research/ventaja_futuros/potencia_cola.txt
"""

from __future__ import annotations

import os
import sys
from math import sqrt
from statistics import NormalDist

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from terreno_tenencia import load_databento, window_stats, DEGRADED_UTC  # noqa: E402

N = NormalDist()
K_PROG = 263                      # tras el descarte de H2d y la invariancia del orden
ALPHA = 0.05 / (K_PROG + 1)       # K_D = 1 para la forma 3, si se pre-registrara
Z_A = N.inv_cdf(1 - ALPHA / 2)
Z_B = N.inv_cdf(0.80)
N1, N2 = 459, 492                 # la particion que la condicion produjo, ya publicada en K0
LOOKBACK = 20
POINT_VALUE = 5.0                 # USD por punto de MES
N_BOOT = 4000
SEED = 20260903
EFECTO_MEDIDO = 1.51              # p95 ALTO / p95 BAJO, del diagnostico ya publicado (06758f6)
LS_USD = [100, 200, 300, 400, 500, 750, 1000]


def hr(t):
    print()
    print("=" * 118)
    print(t)
    print("=" * 118)


def min_detectable_prop(p_base, n1, n2):
    """Menor factor r = p1/p2 con potencia >= 80 % a dos colas, manteniendo la tasa global en p_base.

    Se busca r por biseccion sobre la potencia normal con varianzas separadas."""
    def power(r):
        # p1 = r*p2, y la mezcla n1*p1 + n2*p2 = (n1+n2)*p_base  -> despeja p2
        p2 = p_base * (n1 + n2) / (n1 * r + n2)
        p1 = r * p2
        if p1 >= 1.0:
            return 0.0
        pbar = (n1 * p1 + n2 * p2) / (n1 + n2)
        se0 = sqrt(pbar * (1 - pbar) * (1 / n1 + 1 / n2))
        se1 = sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
        return float(N.cdf((abs(p1 - p2) - Z_A * se0) / se1))
    lo, hi = 1.0, 100.0
    if power(hi) < 0.80:
        return float("nan")
    for _ in range(200):
        mid = (lo + hi) / 2
        if power(mid) >= 0.80:
            hi = mid
        else:
            lo = mid
    return hi


def main():
    print("POTENCIA DEL ESTADISTICO DE COLA -- Ventana D, 2026-09-03. ES 1-min Databento 2016-2019. NO gasta cartucho.")
    print(f"alpha = 0.05/{K_PROG + 1} = {ALPHA:.4e} dos colas, z = {Z_A:.3f}; potencia 80 %, z_b = {Z_B:.3f}; particion {N1} / {N2}")
    print(f"Referencia a batir: el efecto medido en la cola ya publicado es p95 ALTO / p95 BAJO = {EFECTO_MEDIDO:.2f}x (commit 06758f6).")
    print("NADA se calcula partido por estado: todo es incondicional o simulado bajo H0.")

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
    okc = allsess["rango"].shift(1).notna() & allsess["rango"].shift(2).rolling(LOOKBACK).median().notna()
    idx = pd.DatetimeIndex([d for d in esc if bool(okc.get(d, False))])
    x = t23["largo"].reindex(idx).to_numpy(dtype=float)
    hr(f"0. POBLACION: {len(idx)} sesiones, la misma de la corrida anterior. Excursion adversa larga de la sesion completa, incondicional.")
    print(f"  p50 = {np.percentile(x, 50):.2f}   p90 = {np.percentile(x, 90):.2f}   p95 = {np.percentile(x, 95):.2f}   p99 = {np.percentile(x, 99):.2f} pts   max = {x.max():.2f}")
    assert len(x) == 951, len(x)

    # ---------------------------------------------------------------- A) contraste de p95
    hr("A) CONTRASTE DE p95 -- error estandar del cociente bajo H0, por remuestreo de la MISMA distribucion")
    rng = np.random.default_rng(SEED)
    d = np.empty(N_BOOT)
    for i in range(N_BOOT):
        s = rng.choice(x, size=N1 + N2, replace=True)
        d[i] = np.log(np.percentile(s[:N1], 95)) - np.log(np.percentile(s[N1:], 95))
    se95 = float(d.std(ddof=1))
    mde95 = float(np.exp((Z_A + Z_B) * se95))
    print(f"  {N_BOOT} remuestreos; las dos mitades salen de la misma distribucion, asi que esto es el ruido puro del cociente de p95")
    print(f"  desvio de log(p95_1/p95_2) bajo H0 = {se95:.4f}   -> un cociente de p95 de 1.00 tiene ruido de +-{100 * (np.exp(1.96 * se95) - 1):.1f} % al 95 %")
    print(f"  EFECTO MINIMO DETECTABLE al 80 % en el cociente de p95: {mde95:.3f}x")
    print(f"  para comparar, el mismo calculo con alpha 0.05 (sin la deuda): {float(np.exp((N.inv_cdf(0.975) + Z_B) * se95)):.3f}x")

    # ---------------------------------------------------------------- B) tasa de superacion
    hr("B) TASA DE SUPERAR UN UMBRAL L -- la redaccion literal de la forma 3. L en USD de MES, un contrato")
    print(f"  {'L (USD)':>9}{'L (pts)':>9}{'tasa base':>11}{'n dias':>8}{'factor min detectable':>24}{'tasa que habria que ver':>26}")
    for L in LS_USD:
        Lp = L / POINT_VALUE
        p = float((x >= Lp).mean())
        n_days = int((x >= Lp).sum())
        if n_days == 0:
            print(f"  {L:>9}{Lp:>9.1f}{'0.00 %':>11}{n_days:>8}{'imposible: 0 dias':>24}{'--':>26}")
            continue
        r = min_detectable_prop(p, N1, N2)
        if not np.isfinite(r):
            print(f"  {L:>9}{Lp:>9.1f}{100 * p:>10.2f}%{n_days:>8}{'no alcanzable':>24}{'--':>26}")
            continue
        p2 = p * (N1 + N2) / (N1 * r + N2)
        print(f"  {L:>9}{Lp:>9.1f}{100 * p:>10.2f}%{n_days:>8}{r:>23.2f}x{100 * r * p2:>19.2f}% vs {100 * p2:.2f}%")

    # ---------------------------------------------------------------- C) veredicto aritmetico
    hr("C) CONTRA EL EFECTO QUE EXISTE (1.51x en p95, ya publicado)")
    print(f"  estadistico de p95:  detectable desde {mde95:.2f}x   contra 1.51x medido   -> {'ALCANZA' if mde95 <= EFECTO_MEDIDO else 'NO ALCANZA'}")
    r400 = min_detectable_prop(float((x >= 400 / POINT_VALUE).mean()), N1, N2)
    r200 = min_detectable_prop(float((x >= 200 / POINT_VALUE).mean()), N1, N2)
    print(f"  tasa con L = 200 USD: detectable desde {r200:.2f}x   contra 1.51x medido en p95   -> {'ALCANZA' if r200 <= EFECTO_MEDIDO else 'NO ALCANZA'}")
    print(f"  tasa con L = 400 USD: detectable desde {(f'{r400:.2f}x' if np.isfinite(r400) else 'no alcanzable')}   contra 1.51x medido en p95   -> {'ALCANZA' if r400 <= EFECTO_MEDIDO else 'NO ALCANZA'}")
    print()
    print("  Cuidado con comparar peras con manzanas: 1.51x es el cociente de p95, no el cociente de TASAS,")
    print("  y la seccion B pide un cociente de tasas. La seccion D traduce uno en otro sin partir por estado.")

    # ---------------------------------------------------------------- D) traduccion, con modelo declarado
    hr("D) TRADUCCION: que cociente de TASAS implica un efecto de cola de 1.51x en p95")
    print("  Modelo declarado, y es una COTA OPTIMISTA a proposito: se supone que la cola de cada grupo es la")
    print("  incondicional escalada, con ALTO por s y BAJO por s/1.51, s = sqrt(1.51) = 1.229. Es optimista porque")
    print("  el efecto medido NO es un escalamiento puro: la mediana no se movio (1.00x), asi que el desplazamiento")
    print("  real de la cola es menor que el de un escalamiento que multiplique todo. Si ni con esta cota alcanza,")
    print("  no alcanza. Todo se evalua sobre la distribucion INCONDICIONAL: no se parte por estado.")
    s = sqrt(EFECTO_MEDIDO)
    print(f"  {'L (USD)':>9}{'L (pts)':>9}{'tasa base':>11}{'tasa ALTO':>11}{'tasa BAJO':>11}{'cociente implicado':>21}{'detectable':>12}{'':>4}")
    for L in LS_USD:
        Lp = L / POINT_VALUE
        p = float((x >= Lp).mean())
        if (x >= Lp).sum() == 0:
            continue
        p_hi = float((x >= Lp / s).mean())
        p_lo = float((x >= Lp * EFECTO_MEDIDO / s).mean())
        imp = p_hi / p_lo if p_lo > 0 else float("inf")
        r = min_detectable_prop(p, N1, N2)
        veredicto = "ALCANZA" if np.isfinite(r) and imp >= r else "no alcanza"
        rtxt = f"{r:.2f}x" if np.isfinite(r) else "n/a"
        print(f"  {L:>9}{Lp:>9.1f}{100 * p:>10.2f}%{100 * p_hi:>10.2f}%{100 * p_lo:>10.2f}%{imp:>20.2f}x{rtxt:>12}   {veredicto}")
    print()
    print("  LA CAJA SIGUE CERRADA.")


if __name__ == "__main__":
    main()
