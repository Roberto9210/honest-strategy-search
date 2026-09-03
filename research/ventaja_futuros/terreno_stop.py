"""Terreno del stop -- ejecuta terreno_stop_preregistro.md.

Terreno, no ventaja. Misma P-escalera (971) de terreno_tenencia.py, ES 1-min Databento 2016-2019.
Primero el control (D = 60 converge a sin stop); si falla, no se imprime lo demas.

    venv/Scripts/python.exe research/ventaja_futuros/terreno_stop.py > research/ventaja_futuros/terreno_stop.txt
"""

from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from terreno_tenencia import load_databento, window_stats, DEGRADED_UTC  # noqa: E402

DS = [2, 4, 6, 8, 10, 15, 20, 30]
D_CTRL = 60
MES = 5.0
ROLL = 20
FOUR = [("T23", None, None), ("RTH", 8 * 60 + 30, 15 * 60), ("H1", 8 * 60 + 30, 9 * 60 + 30), ("M15", 8 * 60 + 30, 8 * 60 + 45)]
HOURS = list(range(17, 24)) + list(range(0, 16))
REF_H = "08:30"


def hr(t):
    print()
    print("=" * 120)
    print(t)
    print("=" * 120)


def dist(x, keys=(50, 90, 95, 99)):
    x = np.asarray(x, dtype=float)
    if len(x) == 0:
        return {f"p{k}": float("nan") for k in keys} | {"max": float("nan"), "n": 0}
    return {f"p{k}": float(np.percentile(x, k)) for k in keys} | {"max": float(x.max()), "n": int(len(x))}


def window_frame(df, idx, a, b):
    """Barras de la ventana, con O (open de la primera barra de la ventana en su sesion) y posicion."""
    sub = df if a is None else df[(df["m"] >= a) & (df["m"] < b)]
    sub = sub[sub["sess"].isin(idx)].copy()
    sub["O"] = sub.groupby("sess")["open"].transform("first")
    sub["pos"] = sub.groupby("sess").cumcount()
    sub["nbars"] = sub.groupby("sess")["open"].transform("size")
    sub["end_close"] = sub.groupby("sess")["close"].transform("last")
    return sub.reset_index(drop=True)


def touches(sub, side, D):
    """Por sesion: si toco, exceso misma barra, salto apertura, exceso siguiente. Indexado por sesion (todas)."""
    if side == "largo":
        adv = sub["O"] - sub["low"]           # excursion adversa acumulada hasta esa barra (no acumulada: por barra)
        stop_vs_open = (sub["O"] - sub["open"]) - D
        nxt_low = sub.groupby("sess")["low"].shift(-1)
        adv_next = (sub["O"] - nxt_low) - D
    else:
        adv = sub["high"] - sub["O"]
        stop_vs_open = (sub["open"] - sub["O"]) - D
        nxt_high = sub.groupby("sess")["high"].shift(-1)
        adv_next = (nxt_high - sub["O"]) - D
    hit = sub[adv >= D]
    first = hit.groupby("sess").head(1)
    out = pd.DataFrame(index=sub["sess"].unique())
    out.index.name = "sess"
    out["touched"] = False
    out.loc[first["sess"].values, "touched"] = True
    out["exc_same"] = np.nan
    out["exc_open"] = np.nan
    out["exc_next"] = np.nan
    out.loc[first["sess"].values, "exc_same"] = (adv.loc[first.index] - D).values
    out.loc[first["sess"].values, "exc_open"] = np.clip(stop_vs_open.loc[first.index].values, 0, None)
    nx = np.clip(adv_next.loc[first.index].values, 0, None)   # NaN si no hay barra siguiente en la ventana
    out.loc[first["sess"].values, "exc_next"] = nx
    # perdida al final de la ventana (sin ganancia)
    end = sub.groupby("sess")[["O", "end_close"]].first()
    loss_end = (end["O"] - end["end_close"]) if side == "largo" else (end["end_close"] - end["O"])
    out["loss_nostop"] = np.clip(loss_end.reindex(out.index).values, 0, None)
    out["loss_stop"] = np.where(out["touched"], D + out["exc_open"].fillna(0), out["loss_nostop"])
    out["stop_only"] = np.where(out["touched"], D + out["exc_open"].fillna(0), 0.0)
    out["signed_end"] = (end["end_close"] - end["O"]) if side == "largo" else (end["O"] - end["end_close"])
    return out.sort_index()


def rolling_sums(t):
    s = t["loss_stop"].rolling(ROLL).sum().dropna()
    so = t["stop_only"].rolling(ROLL).sum().dropna()
    ns = t["loss_nostop"].rolling(ROLL).sum().dropna()
    cnt = t["touched"].astype(int).rolling(ROLL).sum().dropna()
    return s, so, ns, cnt


def max_dd_rolling(signed):
    """M4 del guardian: drawdown maximo dentro de ventanas moviles de 20 sobre la secuencia close-open."""
    x = signed.values
    out = []
    for i in range(ROLL - 1, len(x)):
        c = np.cumsum(x[i - ROLL + 1:i + 1])
        peak = np.maximum.accumulate(np.concatenate([[0.0], c]))[1:]
        out.append(float((peak - c).max()))
    return np.array(out)


def main():
    print("TERRENO DEL STOP -- Ventana D, 2026-09-03. ES 1-min Databento, 2016-2019, P-escalera 971. NO es MES.")
    print("Ejecuta terreno_stop_preregistro.md. Primero el control; sin control no se imprime lo demas.")
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
    assert len(idx) == 971, len(idx)
    print(f"P-escalera: {len(idx)} sesiones, {idx.min().date()} -> {idx.max().date()}")

    frames = {name: window_frame(df, idx, a, b) for name, a, b in FOUR}
    T = {(name, side, D): touches(frames[name], side, D) for name in frames for side in ["largo", "corto"] for D in DS + [D_CTRL]}

    # ------------------------------------------------------------ CONTROL
    hr(f"1. CONTROL (Enmienda 1) -- D = {D_CTRL}: toque == fraccion con excursion >= 60 por otro camino (exacto), T23 en 1-5 %, "
       f"y suma de 20 sesiones con stop ~ sin stop (mediana y p95 dentro del 10 %)")
    ok_ctrl = True
    print(f"  {'ventana':<6}{'lado':<7}{'toque%':>8}{'exc>=60%':>9} | {'CON stop 60: p50':>17}{'p95':>9} | {'SIN stop: p50':>15}{'p95':>9} | {'dif p50%':>9}{'dif p95%':>9} | {'M4 dd20 p50':>12}{'p95':>9}")
    for name, a_, b_ in FOUR:
        w = window_stats(df, a_, b_).reindex(idx)
        for side in ["largo", "corto"]:
            t = T[(name, side, D_CTRL)]
            s, so, ns, cnt = rolling_sums(t)
            a, b = dist(s), dist(ns)
            dd = dist(max_dd_rolling(t["signed_end"]))
            d50 = 100 * (a["p50"] - b["p50"]) / b["p50"] if b["p50"] else 0.0
            d95 = 100 * (a["p95"] - b["p95"]) / b["p95"] if b["p95"] else 0.0
            freq = 100 * t["touched"].mean()
            frac = 100 * (w[side] >= D_CTRL).mean()
            p95, p99 = np.percentile(w[side], 95), np.percentile(w[side], 99)
            # Enmienda 2: la banda la implican los percentiles de ESTA ventana y lado, no un numero a mano
            if D_CTRL > p99:
                band, band_ok = "< 1%", freq < 1.0
            elif D_CTRL < p95:
                band, band_ok = "> 5%", freq > 5.0
            else:
                band, band_ok = "1-5%", 1.0 <= freq <= 5.0
            print(f"  {name:<6}{side:<7}{freq:>7.2f}%{frac:>8.2f}% | {a['p50']:>17.2f}{a['p95']:>9.2f} | {b['p50']:>15.2f}{b['p95']:>9.2f} | {d50:>+8.1f}%{d95:>+8.1f}% | {dd['p50']:>12.2f}{dd['p95']:>9.2f}"
                  f" | p95 {p95:6.2f} p99 {p99:6.2f} -> banda {band:<5} {'ok' if band_ok else 'NO'}")
            if abs(d50) > 10 or abs(d95) > 10 or abs(freq - frac) > 1e-9 or not band_ok:
                ok_ctrl = False
    print()
    print(f"  >>> CONTROL: {'PASA' if ok_ctrl else 'FALLA -- el calculo esta mal en algun lado; NO se publica lo demas'}")
    if not ok_ctrl:
        sys.exit(1)

    # ------------------------------------------------------------ 1. FRECUENCIA DE TOQUE
    hr("2. FRECUENCIA DE TOQUE (% de sesiones que tocan el stop antes del fin de la ventana), cuatro ventanas")
    print(f"  {'ventana':<6}{'lado':<7}" + "".join(f"{'D=' + str(D):>8}" for D in DS + [D_CTRL]))
    for name, _, _ in FOUR:
        for side in ["largo", "corto"]:
            print(f"  {name:<6}{side:<7}" + "".join(f"{100 * T[(name, side, D)]['touched'].mean():>7.1f}%" for D in DS + [D_CTRL]))

    # ------------------------------------------------------------ 2. POR HORA
    hr("3. POR HORA -- tenencia de una hora, % de sesiones que tocan, por hora de arranque; y la razon p50 de excursion vs 08:30 (terreno_horas)")
    hframes = {h: window_frame(df, idx, h * 60, (h + 1) * 60) for h in HOURS}
    ref = window_frame(df, idx, 8 * 60 + 30, 9 * 60 + 30)
    HT = {}
    for side in ["largo", "corto"]:
        print(f"  --- lado {side.upper()} ---")
        ref_med = np.median((ref["O"] - ref.groupby("sess")["low"].transform("min")).groupby(ref["sess"]).first()) if side == "largo" \
            else np.median((ref.groupby("sess")["high"].transform("max") - ref["O"]).groupby(ref["sess"]).first())
        print(f"  {'hora':<14}{'n':>5}" + "".join(f"{'D=' + str(D):>8}" for D in DS) + f" | {'exc p50/ref':>12}")
        rt = {D: touches(ref, side, D) for D in DS}
        print(f"  {'REF 08:30':<14}{len(ref['sess'].unique()):>5}" + "".join(f"{100 * rt[D]['touched'].mean():>7.1f}%" for D in DS) + f" | {1.0:>12.2f}")
        for h in HOURS:
            f = hframes[h]
            n = f["sess"].nunique()
            exc = (f["O"] - f.groupby("sess")["low"].transform("min")) if side == "largo" else (f.groupby("sess")["high"].transform("max") - f["O"])
            med = np.median(exc.groupby(f["sess"]).first())
            row = []
            for D in DS:
                t = touches(f, side, D)
                HT[(h, side, D)] = t
                row.append(100 * t["touched"].mean())
            print(f"  {h:02d}:00->{(h + 1) % 24:02d}:00  {n:>5}" + "".join(f"{v:>7.1f}%" for v in row) + f" | {med / ref_med:>12.2f}")
        print()

    # ------------------------------------------------------------ 3. EXCESO
    hr("4. LO QUE EL STOP DEJA PASAR -- exceso sobre el stop, en puntos, sobre las sesiones que tocaron")
    print("  misma = (stop - low) de la barra que toca; apertura = max(0, stop - open de esa barra); siguiente = max(0, stop - low de la barra siguiente)")
    for name, _, _ in FOUR:
        print(f"  --- {name} ---")
        print(f"  {'lado':<7}{'D':>4}{'n toc':>7} | {'misma p50':>10}{'p95':>7}{'p99':>7}{'max':>7} | {'apert p50':>10}{'p95':>7}{'p99':>7}{'max':>7} | {'sig p50':>8}{'p95':>7}{'p99':>7}{'max':>7}{'n':>6}")
        for side in ["largo", "corto"]:
            for D in DS:
                t = T[(name, side, D)]
                tt = t[t["touched"]]
                a, b, c = dist(tt["exc_same"]), dist(tt["exc_open"]), dist(tt["exc_next"].dropna())
                print(f"  {side:<7}{D:>4}{len(tt):>7} | {a['p50']:>10.2f}{a['p95']:>7.2f}{a['p99']:>7.2f}{a['max']:>7.2f} | "
                      f"{b['p50']:>10.2f}{b['p95']:>7.2f}{b['p99']:>7.2f}{b['max']:>7.2f} | {c['p50']:>8.2f}{c['p95']:>7.2f}{c['p99']:>7.2f}{c['max']:>7.2f}{c['n']:>6}")
    print("  --- las 23 horas juntas (toques de todas las tenencias de una hora, por D) ---")
    print(f"  {'lado':<7}{'D':>4}{'n toc':>7} | {'misma p50':>10}{'p95':>7}{'p99':>7}{'max':>7} | {'apert p50':>10}{'p95':>7}{'p99':>7}{'max':>7} | {'sig p50':>8}{'p95':>7}{'p99':>7}{'max':>7}{'n':>6}")
    for side in ["largo", "corto"]:
        for D in DS:
            tt = pd.concat([HT[(h, side, D)] for h in HOURS])
            tt = tt[tt["touched"]]
            a, b, c = dist(tt["exc_same"]), dist(tt["exc_open"]), dist(tt["exc_next"].dropna())
            print(f"  {side:<7}{D:>4}{len(tt):>7} | {a['p50']:>10.2f}{a['p95']:>7.2f}{a['p99']:>7.2f}{a['max']:>7.2f} | "
                  f"{b['p50']:>10.2f}{b['p95']:>7.2f}{b['p99']:>7.2f}{b['max']:>7.2f} | {c['p50']:>8.2f}{c['p95']:>7.2f}{c['p99']:>7.2f}{c['max']:>7.2f}{c['n']:>6}")

    # ------------------------------------------------------------ 4. LA CUENTA
    hr(f"5. LA CUENTA DE {ROLL} SESIONES -- entra siempre, mismo lado, stop a D. Sin ninguna ganancia. Puntos de ES y USD de MES (x5)")
    print("  'stops' = suma de (D + salto apertura) en las sesiones que tocaron; 'con stop' = stops + perdida al cierre de las que no tocaron")
    for name, _, _ in FOUR:
        print(f"  --- {name} ---")
        print(f"  {'lado':<7}{'D':>4} | {'toques/20: p50':>15}{'p90':>5}{'p95':>5}{'max':>5} | {'stops pts: p50':>15}{'p90':>8}{'p95':>8}{'p99':>8}{'max':>8} | {'con stop pts: p50':>18}{'p95':>8}{'p99':>8} | {'stops USD MES p50':>18}{'p95':>8}{'p99':>8}{'max':>8}")
        for side in ["largo", "corto"]:
            for D in DS:
                s, so, ns, cnt = rolling_sums(T[(name, side, D)])
                a, b, c = dist(so), dist(s), dist(cnt)
                print(f"  {side:<7}{D:>4} | {c['p50']:>15.0f}{c['p90']:>5.0f}{c['p95']:>5.0f}{c['max']:>5.0f} | "
                      f"{a['p50']:>15.2f}{a['p90']:>8.2f}{a['p95']:>8.2f}{a['p99']:>8.2f}{a['max']:>8.2f} | "
                      f"{b['p50']:>18.2f}{b['p95']:>8.2f}{b['p99']:>8.2f} | "
                      f"{a['p50'] * MES:>18.0f}{a['p95'] * MES:>8.0f}{a['p99'] * MES:>8.0f}{a['max'] * MES:>8.0f}")
        print()

    print("Limitaciones, al pie: ES y no MES. El exceso es la cota del deslizamiento por movimiento del mercado, no por")
    print("profundidad del libro; un stop real se llena en algun lugar de la barra. Entrar siempre del mismo lado no es una")
    print("estrategia y esta cuenta no cuenta ganancias: es un piso de terreno. Niveles de 2016-2019.")


if __name__ == "__main__":
    main()
