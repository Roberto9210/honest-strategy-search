"""INVARIANCIA DEL ORDEN -- ejecuta invariancia_orden_preregistro.md (commit 01f2489).

ES 1-min Databento, 2016-01-04 -> 2019-12-31. La caja no se toca: el cargador corta en 2019.
Controles K0-K5 arriba del resultado. Un solo par de horas (23:00 vs 08:30), un solo lado principal
(largo), una sola condicion (rango de ayer contra la mediana movil de 20).

    venv/Scripts/python.exe research/ventaja_futuros/invariancia_orden.py > research/ventaja_futuros/invariancia_orden.txt
"""

from __future__ import annotations

import os
import sys
from math import erfc, exp, sqrt
from statistics import NormalDist

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from terreno_tenencia import load_databento, window_stats, DEGRADED_UTC  # noqa: E402

N = NormalDist()
K_PROG = 262                      # tras el descarte de H2d
ALPHA = 0.05 / (K_PROG + 1)       # K_D = 1  -> 0.05/263
Z_LINE = N.inv_cdf(1 - ALPHA / 2)
Z_B = N.inv_cdf(0.80)
SEED = 20260903
N_PERM = 1000
LOOKBACK = 20
TICK = 0.25
POINT_VALUE = 5.0                 # USD por punto de MES
FRICTION_RT = 3.90                # USD ida y vuelta, factory/harness.py
X2_PTS = FRICTION_RT / POINT_VALUE  # 0.78 pts: umbral de indiferencia
HOUR_CHEAP, HOUR_OPEN = 23, 8
HOURS = list(range(17, 24)) + list(range(0, 16))
WINDOWS = {"T23": (None, None), "RTH": (8 * 60 + 30, 15 * 60),
           "H1": (8 * 60 + 30, 9 * 60 + 30), "M15": (8 * 60 + 30, 8 * 60 + 45)}


def hr(t):
    print()
    print("=" * 118)
    print(t)
    print("=" * 118)


def lg(x):
    return np.log(np.maximum(np.asarray(x, dtype=float), TICK))


def welch(a, b):
    """Diferencia de medias, error estandar de Welch, t y p bilateral."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    d = a.mean() - b.mean()
    se = sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
    t = d / se
    return d, se, t, erfc(abs(t) / sqrt(2))


def spearman(x, y):
    rx = pd.Series(x).rank().to_numpy()
    ry = pd.Series(y).rank().to_numpy()
    return float(np.corrcoef(rx, ry)[0, 1])


def main():
    print("INVARIANCIA DEL ORDEN -- Ventana D, 2026-09-03. ES 1-min Databento 2016-2019. NO es MES. La caja no se toca.")
    print(f"Ejecuta invariancia_orden_preregistro.md (01f2489). K = {K_PROG}, K_D = 1, alpha = {ALPHA:.4e} dos colas, |z| >= {Z_LINE:.3f}")
    print(f"X1 inversion: r cruza 1.00.  X2 indiferencia: exc(08:30) - exc(23:00) < {FRICTION_RT:.2f} USD MES = {X2_PTS:.2f} pts")

    df = load_databento()

    # ---- P-escalera, identica a terreno_tenencia.py
    sess = df.groupby("sess").agg(n_contracts=("contract", "nunique"))
    degraded = set(df.loc[df["utc_date"].isin(DEGRADED_UTC), "sess"].unique())
    t23 = window_stats(df, None, None)
    rth = window_stats(df, 8 * 60 + 30, 15 * 60)
    ok = ((sess.index.weekday < 5) & (sess["n_contracts"] == 1) & (~sess.index.isin(list(degraded)))
          & (t23["first_m"].reindex(sess.index) == 17 * 60)
          & (rth["first_m"].reindex(sess.index) == 8 * 60 + 30)
          & (rth["last_m"].reindex(sess.index) >= 15 * 60 - 1))
    esc = sess.index[ok.fillna(False)]
    assert len(esc) == 971, len(esc)

    # ---- condicion: rango de AYER contra la mediana movil de las 20 sesiones anteriores a ayer
    allsess = t23.sort_index()
    allsess["rango"] = allsess["high"] - allsess["low"]
    prev_rango = allsess["rango"].shift(1)
    med20 = allsess["rango"].shift(2).rolling(LOOKBACK).median()
    cond = pd.DataFrame({"prev_rango": prev_rango, "med20": med20})
    cond["alto"] = cond["prev_rango"] >= cond["med20"]
    cond["ok"] = cond["prev_rango"].notna() & cond["med20"].notna()

    idx = [d for d in esc if bool(cond["ok"].get(d, False))]
    idx = pd.DatetimeIndex(idx)
    perdidas = [d for d in esc if d not in set(idx)]
    hr(f"0. POBLACION: P-escalera 971 -> con 20 previas y sesion anterior: {len(idx)} ({idx.min().date()} -> {idx.max().date()})")
    print(f"  K5 - COBERTURA: sesiones perdidas {len(perdidas)}; meses: {sorted(set(pd.DatetimeIndex(perdidas).strftime('%Y-%m')))}")

    alto = cond["alto"].reindex(idx).to_numpy(dtype=bool)

    # ---- excursiones por hora y por ventana
    W = {name: window_stats(df, a, b).reindex(idx) for name, (a, b) in WINDOWS.items()}
    H = {h: window_stats(df, h * 60, (h + 1) * 60).reindex(idx) for h in HOURS}

    # ---------------------------------------------------------------- K0
    hr("K0 - LA CONDICION ES LA CONDICION")
    frac = float(alto.mean())
    exc_sess = W["T23"]["largo"].to_numpy(dtype=float)
    med_a, med_b = float(np.median(exc_sess[alto])), float(np.median(exc_sess[~alto]))
    print(f"  particion ALTO = {100 * frac:.1f} % ({int(alto.sum())} de {len(idx)})   criterio 40-60 %: {'PASA' if 0.40 <= frac <= 0.60 else 'FALLA'}")
    print(f"  excursion mediana de la sesion completa: ALTO {med_a:.2f} pts   BAJO {med_b:.2f} pts   factor {med_a / med_b:.2f}x   criterio ALTO > BAJO: {'PASA' if med_a > med_b else 'FALLA'}")
    if not (0.40 <= frac <= 0.60) or med_a <= med_b:
        print("  K0 FALLA -- la condicion no es lo que dice ser. El resultado no se interpreta.")
        return

    # ---------------------------------------------------------------- estadistico principal
    side = "largo"
    e_cheap = H[HOUR_CHEAP][side].to_numpy(dtype=float)
    e_open = H[HOUR_OPEN][side].to_numpy(dtype=float)
    d = lg(e_cheap) - lg(e_open)
    D, se, t, p = welch(d[alto], d[~alto])
    sd_d = float(np.std(d, ddof=1))
    corr = float(np.corrcoef(lg(e_cheap), lg(e_open))[0, 1])
    n1, n2 = int(alto.sum()), int((~alto).sum())
    mde = exp((Z_LINE + Z_B) * sd_d * sqrt(1 / n1 + 1 / n2))

    hr("POTENCIA EFECTIVA (la declarada usaba correlacion cero: sigma_d <= 1.42, minimo detectable 1.52x)")
    print(f"  correlacion medida log-log entre las dos horas: {corr:+.3f}   sigma_d medido = {sd_d:.3f}")
    print(f"  minimo detectable efectivo en r = {mde:.3f}x   criterio de archivo (> 2.0x): {'ARCHIVAR' if mde > 2.0 else 'decidible'}")

    # ---------------------------------------------------------------- K1
    hr(f"K1 - PLACEBO DE ETIQUETA: {N_PERM} permutaciones de ALTO/BAJO, semilla {SEED}")
    rng = np.random.default_rng(SEED)
    Ds = np.empty(N_PERM)
    for i in range(N_PERM):
        s = rng.permutation(alto)
        Ds[i] = d[s].mean() - d[~s].mean()
    lo, hi = np.percentile(Ds, 2.5), np.percentile(Ds, 97.5)
    print(f"  D permutado: p2.5 = {lo:+.4f}   p50 = {np.percentile(Ds, 50):+.4f}   p97.5 = {hi:+.4f}")
    print(f"  D real = {D:+.4f}   {'FUERA' if not (lo <= D <= hi) else 'DENTRO'} de la banda")

    # ---------------------------------------------------------------- K2
    hr("K2 - RIVAL SIN CONTENIDO: dia del mes par/impar en lugar de la condicion")
    par = (idx.day % 2 == 0)
    D2, _, t2, p2 = welch(d[par], d[~par])
    print(f"  D rival = {D2:+.4f}   t = {t2:+.3f}   p = {p2:.3e}   (contra el real D = {D:+.4f}, t = {t:+.3f})")

    # ---------------------------------------------------------------- K3
    hr("K3 - EL OTRO LADO: mismo contraste en corto")
    dc = lg(H[HOUR_CHEAP]["corto"].to_numpy(dtype=float)) - lg(H[HOUR_OPEN]["corto"].to_numpy(dtype=float))
    D3, _, t3, p3 = welch(dc[alto], dc[~alto])
    print(f"  D corto = {D3:+.4f}   t = {t3:+.3f}   p = {p3:.3e}   signos {'COINCIDEN' if np.sign(D3) == np.sign(D) else 'NO COINCIDEN'}")

    # ---------------------------------------------------------------- K4
    hr("K4 - ESCALA: la misma medicion en USD de MES")
    ok4 = np.allclose(e_cheap * POINT_VALUE, e_cheap * 5.0) and abs(X2_PTS * POINT_VALUE - FRICTION_RT) < 1e-12
    print(f"  puntos x 5 = USD MES exacto: {ok4}   X2 {X2_PTS:.2f} pts = {X2_PTS * POINT_VALUE:.2f} USD = friccion {FRICTION_RT:.2f}: {'PASA' if ok4 else 'FALLA'}")

    # ---------------------------------------------------------------- RESULTADO
    hr("RESULTADO -- contraste principal (lado largo, 23:00 contra 08:30)")
    print(f"  n ALTO = {n1}   n BAJO = {n2}")
    print(f"  D = media(log r | ALTO) - media(log r | BAJO) = {D:+.4f}   en factor: {exp(D):.3f}x")
    print(f"  error estandar = {se:.4f}   t = {t:+.3f}   p = {p:.3e}   linea de decision |t| >= {Z_LINE:.3f}: {'SIGNIFICATIVO' if abs(t) >= Z_LINE else 'no significativo'}")
    print()
    print("  cociente r = exc(23:00)/exc(08:30), por estado, sobre las excursiones agregadas:")
    for lab, mask in (("ALTO", alto), ("BAJO", ~alto)):
        for q in (50, 90, 95):
            a_, b_ = np.percentile(e_cheap[mask], q), np.percentile(e_open[mask], q)
            print(f"    {lab} p{q}: 23:00 = {a_:6.2f} pts ({a_ * POINT_VALUE:7.2f} USD)   08:30 = {b_:6.2f} pts ({b_ * POINT_VALUE:7.2f} USD)   r = {a_ / b_:.3f}   dif = {(b_ - a_) * POINT_VALUE:7.2f} USD")

    hr("UMBRALES X -- la decision")
    r_alto_50 = float(np.percentile(e_cheap[alto], 50) / np.percentile(e_open[alto], 50))
    r_bajo_50 = float(np.percentile(e_cheap[~alto], 50) / np.percentile(e_open[~alto], 50))
    dif_alto = float((np.percentile(e_open[alto], 50) - np.percentile(e_cheap[alto], 50)) * POINT_VALUE)
    x1 = (r_alto_50 >= 1.0) or (r_bajo_50 >= 1.0)
    x2 = dif_alto < FRICTION_RT
    sig = abs(t) >= Z_LINE
    print(f"  X1 inversion: r ALTO = {r_alto_50:.3f}, r BAJO = {r_bajo_50:.3f}; cruza 1.00: {'SI' if x1 else 'NO'}")
    print(f"  X2 indiferencia: dif p50 en ALTO = {dif_alto:.2f} USD contra friccion {FRICTION_RT:.2f}: {'CRUZA' if x2 else 'NO cruza'}")
    print(f"  contraste significativo a {ALPHA:.3e}: {'SI' if sig else 'NO'}")
    pos = "B" if (sig and (x1 or x2)) else "A"
    print(f"  POSICION ELEGIDA: {pos} -- {'hay que condicionar: dos tablas' if pos == 'B' else 'una sola tabla; la escalera incondicional se usa tal cual'}")

    # ---------------------------------------------------------------- secundarios
    hr("SECUNDARIOS (impresos, no deciden): ranking de las 23 horas y de las 4 ventanas, por estado")
    med_alto = {h: float(np.median(H[h][side].to_numpy(dtype=float)[alto])) for h in HOURS}
    med_bajo = {h: float(np.median(H[h][side].to_numpy(dtype=float)[~alto])) for h in HOURS}
    ra = sorted(HOURS, key=lambda h: med_alto[h])
    rb = sorted(HOURS, key=lambda h: med_bajo[h])
    print(f"  orden ALTO (mas barata primero): {[f'{h:02d}' for h in ra]}")
    print(f"  orden BAJO (mas barata primero): {[f'{h:02d}' for h in rb]}")
    print(f"  Spearman entre los dos ordenes: {spearman([med_alto[h] for h in HOURS], [med_bajo[h] for h in HOURS]):+.4f}")
    print(f"  hora mas barata: ALTO {ra[0]:02d}:00   BAJO {rb[0]:02d}:00   {'MISMA' if ra[0] == rb[0] else 'DISTINTA'}")
    print("  ventanas de tenencia, mediana de excursion largo (pts):")
    for name in WINDOWS:
        x = W[name][side].to_numpy(dtype=float)
        print(f"    {name:<5} ALTO {np.median(x[alto]):7.2f}   BAJO {np.median(x[~alto]):7.2f}   factor {np.median(x[alto]) / np.median(x[~alto]):.2f}x")
    print()
    print("  LA CAJA SIGUE CERRADA. Ninguna sesion posterior a 2019-12-31 entro en este calculo.")


if __name__ == "__main__":
    main()
