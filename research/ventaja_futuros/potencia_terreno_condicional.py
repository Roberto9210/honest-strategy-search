"""Potencia de una pregunta de TERRENO CONDICIONAL con el alfa heredado -- Ventana D, 2026-09-03.

Pregunta de Roberto: la deuda de multiplicidad (alfa = 0.05/262) muerde igual de fuerte a una
pregunta cuyo efecto es un FACTOR (la excursion adversa es X veces mas grande bajo una condicion)
que a una ventaja direccional (acierto 55.6 %)?

Esto NO corre ninguna hipotesis condicional. No se define ninguna condicion. Solo mide, sobre la
P-escalera ya barrida (ES 1-min Databento 2016-2019, 971 sesiones), la DISPERSION incondicional
de la excursion adversa por ventana y por hora, y con ella calcula el factor minimo detectable al
80 % de potencia para una particion de la poblacion en dos grupos (f / 1-f) que todavia no existe.
Numero de planificacion, como potencia_heredada.py.

Tambien imprime, para contraste, la lectura del protocolo de spec_fase2 §3.3 (multiplicidad en A,
caja a 0.05) aplicada al N de H2d, sin correr nada.

    venv/Scripts/python.exe research/ventaja_futuros/potencia_terreno_condicional.py > research/ventaja_futuros/potencia_terreno_condicional.txt
"""

from __future__ import annotations

import os
import sys
from math import exp, log, sqrt
from statistics import NormalDist

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from terreno_tenencia import load_databento, window_stats, DEGRADED_UTC  # noqa: E402
from potencia_heredada import power_two_sided  # noqa: E402

N = NormalDist()
POWER = 0.80
K_PROG = 261
ALPHA_HER = 0.05 / (K_PROG + 1)        # K_D = 1
ALPHA_LIBRE = 0.05
Z_B = N.inv_cdf(POWER)
SPLITS = [0.50, 0.33, 0.20, 0.10]      # fraccion de sesiones que caeria en el grupo "condicionado"
DS = [2, 4, 6, 8, 10, 15, 20, 30]
TICK = 0.25
N_SESS = 971
WINDOWS = {"T23": (None, None), "RTH": (8 * 60 + 30, 15 * 60), "H1": (8 * 60 + 30, 9 * 60 + 30), "M15": (8 * 60 + 30, 8 * 60 + 45)}
HOURS = list(range(17, 24)) + list(range(0, 16))


def hr(t):
    print()
    print("=" * 118)
    print(t)
    print("=" * 118)


def z_alpha(alpha):
    return N.inv_cdf(1 - alpha / 2)


def min_ratio(sigma_log, n1, n2, alpha):
    """Factor minimo detectable (media geometrica grupo 1 / grupo 2) al 80 %, dos colas, t sobre log."""
    return exp((z_alpha(alpha) + Z_B) * sigma_log * sqrt(1 / n1 + 1 / n2))


def n_per_group(sigma_log, ratio, alpha):
    """Sesiones por grupo (50/50) para detectar un factor dado."""
    return 2 * ((z_alpha(alpha) + Z_B) * sigma_log / log(ratio)) ** 2


def min_prop_diff(p, n1, n2, alpha):
    """Diferencia minima detectable de una proporcion (aprox normal, misma varianza p(1-p))."""
    return (z_alpha(alpha) + Z_B) * sqrt(p * (1 - p) * (1 / n1 + 1 / n2))


def p_min_exact(n, alpha, p0=0.5):
    """Acierto minimo con potencia >= 80 % (binomial exacta, dos colas), busqueda por 0.001."""
    p = 0.500
    while p < 0.99:
        if power_two_sided(n, p, alpha, p0) >= POWER:
            return p
        p = round(p + 0.001, 3)
    return float("nan")


def main():
    print("POTENCIA DE TERRENO CONDICIONAL -- Ventana D, 2026-09-03. ES 1-min Databento 2016-2019. NO es MES. No corre ninguna condicion.")
    print(f"alfa heredado = 0.05/{K_PROG + 1} = {ALPHA_HER:.3e} (z dos colas {z_alpha(ALPHA_HER):.3f}); alfa libre 0.05 (z {z_alpha(ALPHA_LIBRE):.3f}); z_beta {Z_B:.3f}")
    print(f"La deuda multiplica el efecto minimo en log por (z_her+z_b)/(z_libre+z_b) = {(z_alpha(ALPHA_HER) + Z_B) / (z_alpha(ALPHA_LIBRE) + Z_B):.3f}")

    df = load_databento()
    sess = df.groupby("sess").agg(n_contracts=("contract", "nunique"))
    degraded = set(df.loc[df["utc_date"].isin(DEGRADED_UTC), "sess"].unique())
    t23 = window_stats(df, None, None)
    rth = window_stats(df, 8 * 60 + 30, 15 * 60)
    ok = ((sess.index.weekday < 5) & (sess["n_contracts"] == 1) & (~sess.index.isin(list(degraded)))
          & (t23["first_m"].reindex(sess.index) == 17 * 60)
          & (rth["first_m"].reindex(sess.index) == 8 * 60 + 30)
          & (rth["last_m"].reindex(sess.index) >= 15 * 60 - 1))
    idx = sess.index[ok.fillna(False)]
    hr(f"0. POBLACION: P-escalera = {len(idx)} sesiones ({idx.min().date()} -> {idx.max().date()}); debe ser {N_SESS}")
    assert len(idx) == N_SESS, len(idx)

    # ---------------------------------------------------------------- 1. dispersion incondicional
    hr("1. DISPERSION INCONDICIONAL DE LA EXCURSION ADVERSA (pts ES). sigma_log = desvio de log(max(exc, 0.25)); ceros = exc == 0")
    rows = []
    frames = {name: window_stats(df, a, b).reindex(idx) for name, (a, b) in WINDOWS.items()}
    for h in HOURS:
        frames[f"h{h:02d}"] = window_stats(df, h * 60, (h + 1) * 60).reindex(idx)
    print(f"  {'ventana':<8}{'lado':<7}{'n':>5}{'ceros%':>8}{'p50':>8}{'p90':>8}{'sigma_log':>11}{'sigma_log>0':>13}")
    for name, w in frames.items():
        for side in ["largo", "corto"]:
            x = w[side].dropna().to_numpy(dtype=float)
            x = x[np.isfinite(x)]
            lx = np.log(np.maximum(x, TICK))
            pos = x[x > 0]
            s_all, s_pos = float(lx.std(ddof=1)), float(np.log(pos).std(ddof=1))
            rows.append({"ventana": name, "lado": side, "n": len(x), "ceros": 100 * (x == 0).mean(), "p50": np.median(x),
                         "p90": np.percentile(x, 90), "sigma_log": s_all, "sigma_log_pos": s_pos, "x": x})
            print(f"  {name:<8}{side:<7}{len(x):>5}{100 * (x == 0).mean():>7.1f}%{np.median(x):>8.2f}{np.percentile(x, 90):>8.2f}{s_all:>11.3f}{s_pos:>13.3f}")

    # ---------------------------------------------------------------- 2. factor minimo detectable
    hr("2. FACTOR MINIMO DETECTABLE (media geometrica condicionado / resto) al 80 %, dos colas. f = fraccion de sesiones condicionadas")
    print("   Alfa heredado 0.05/262 y, al lado, alfa libre 0.05 para ver cuanto cuesta la deuda. Ventanas de la escalera + tres horas de referencia.")
    show = ["T23", "RTH", "H1", "M15", "h23", "h08", "h12"]
    print(f"  {'ventana':<8}{'lado':<7}{'sigma':>7}" + "".join(f"{'f=' + str(f):>9}" for f in SPLITS) + "  |" + "".join(f"{'f=' + str(f) + ' libre':>15}" for f in SPLITS))
    for r in rows:
        if r["ventana"] not in show:
            continue
        s = r["sigma_log"]
        her = [min_ratio(s, int(f * N_SESS), N_SESS - int(f * N_SESS), ALPHA_HER) for f in SPLITS]
        lib = [min_ratio(s, int(f * N_SESS), N_SESS - int(f * N_SESS), ALPHA_LIBRE) for f in SPLITS]
        print(f"  {r['ventana']:<8}{r['lado']:<7}{s:>7.3f}" + "".join(f"{v:>8.2f}x" for v in her) + "  |" + "".join(f"{v:>14.2f}x" for v in lib))

    hr("3. SESIONES POR GRUPO (50/50) PARA DETECTAR UN FACTOR DADO, alfa heredado. Para leer contra las 971 de la P-escalera")
    print(f"  {'ventana':<8}{'lado':<7}{'sigma':>7}" + "".join(f"{'x' + str(rt):>9}" for rt in [1.25, 1.5, 2.0, 3.0, 4.0]))
    for r in rows:
        if r["ventana"] not in show:
            continue
        s = r["sigma_log"]
        print(f"  {r['ventana']:<8}{r['lado']:<7}{s:>7.3f}" + "".join(f"{n_per_group(s, rt, ALPHA_HER):>9.0f}" for rt in [1.25, 1.5, 2.0, 3.0, 4.0]))

    # ---------------------------------------------------------------- 4. version binaria: toque del stop
    hr("4. VERSION BINARIA: frecuencia de toque del stop, diferencia minima detectable entre condicionado y resto (alfa heredado)")
    print("   toque(D) = fraccion de sesiones con excursion >= D (misma definicion que terreno_stop). Se muestra tasa base y la tasa minima")
    print("   detectable en el grupo condicionado, para f = 0.5 y f = 0.2. Entre parentesis, el cociente tasa detectable / tasa base.")
    for name in ["T23", "RTH", "H1", "M15"]:
        for side in ["largo", "corto"]:
            x = next(r["x"] for r in rows if r["ventana"] == name and r["lado"] == side)
            line = f"  {name:<5}{side:<7}"
            for D in DS:
                p = float((x >= D).mean())
                if p <= 0.02 or p >= 0.98:
                    line += f"  D={D:<2} {100 * p:5.1f}% ---- "
                    continue
                d50 = min_prop_diff(p, int(0.5 * N_SESS), N_SESS - int(0.5 * N_SESS), ALPHA_HER)
                d20 = min_prop_diff(p, int(0.2 * N_SESS), N_SESS - int(0.2 * N_SESS), ALPHA_HER)
                line += f"  D={D:<2} {100 * p:5.1f}%->{100 * min(1, p + d50):5.1f}%({(p + d50) / p:4.2f})/{100 * min(1, p + d20):5.1f}%({(p + d20) / p:4.2f})"
            print(line)

    # ---------------------------------------------------------------- 5. la misma deuda en la pregunta direccional
    hr("5. LA MISMA DEUDA EN UNA PREGUNTA DIRECCIONAL, para comparar unidades")
    for n in [971, 851, 1687]:
        pm = p_min_exact(n, ALPHA_HER)
        print(f"  n={n:>5}: acierto minimo detectable {100 * pm:.1f}%  = odds {pm / (1 - pm):.2f}x  (alfa libre 0.05: {100 * p_min_exact(n, ALPHA_LIBRE):.1f}%)")

    # ---------------------------------------------------------------- 6. lectura del protocolo de la spec sobre H2d
    hr("6. PROTOCOLO DE spec_fase2 secciones 3.1 a 3.3 LEIDO SOBRE H2d (multiplicidad en A, caja a 0.05) -- SIN CORRER NADA, solo N y alfa")
    n_a, n_b = 851, 1687
    print(f"  Compuerta 1 en A (n={n_a}), alfa {ALPHA_HER:.3e} dos colas: acierto minimo con potencia 80 % = {100 * p_min_exact(n_a, ALPHA_HER):.1f}%")
    print(f"     acierto que ya cruza la linea de decision en A (t >= {z_alpha(ALPHA_HER):.3f}), sin hablar de potencia: {100 * (0.5 + z_alpha(ALPHA_HER) * 0.5 / sqrt(n_a)):.1f}%")
    print(f"  Compuerta 2: t_A >= max(3.726, 2.8016*sqrt(n_A/n_B)) = max(3.726, {2.8016 * sqrt(n_a / n_b):.3f}) -> manda la compuerta 1 (n_B > n_A, caso 'intradia' de la tabla)")
    print(f"  Compuerta 3 en B (n={n_b}), alfa 0.05 dos colas: acierto minimo con potencia 80 % = {100 * p_min_exact(n_b, ALPHA_LIBRE):.1f}%")
    print(f"  Lo pre-registrado en Enmienda 2 (B a alfa heredado): acierto minimo {100 * p_min_exact(n_b, ALPHA_HER):.1f}%")
    print("  Son dos protocolos distintos. Cual rige para H2d lo decide Roberto; este archivo solo muestra los numeros de cada uno.")


if __name__ == "__main__":
    main()
