"""Inspeccion de la fecha discordante 2016-11-16 y conteo de discordancias entre proveedores.

No mide terreno ni ventaja. Compara barra contra barra: la sesion 17:00->16:00 CT
reconstruida desde ES 1-min de Databento contra la barra diaria ES de NT8 (CSV del
guardian, 37a0144), sobre las mismas 828 fechas del control de terreno_tenencia.py.

    venv/Scripts/python.exe research/ventaja_futuros/discordancia_20161116.py > research/ventaja_futuros/discordancia_20161116.txt
"""

from __future__ import annotations

import glob
import os

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, "data", "es_1min_databento.csv")
GUARD_CSV = (r"C:\Users\home\AppData\Local\Temp\claude\C--Users-home-Desktop-ALAYA"
             r"\03cf4965-af02-4a1f-8eb0-bc27e9d414df\scratchpad\nt8-daily-csv")
START, END = pd.Timestamp("2016-01-04"), pd.Timestamp("2019-12-31")
DEGRADED_UTC = {"2017-11-13", "2018-10-21", "2019-01-15", "2019-02-22", "2019-03-13", "2019-03-26"}
TARGET = pd.Timestamp("2016-11-16")
BINS = [0.25, 1.0, 2.0, 5.0, 10.0]


def load_databento():
    df = pd.read_csv(SRC, usecols=["ts_event_utc", "contract", "open", "high", "low", "close", "volume"],
                     dtype={"contract": "category"})
    yr = df["ts_event_utc"].str.slice(0, 4)
    df = df[yr.isin(["2016", "2017", "2018", "2019", "2020"])].copy()
    ts = pd.to_datetime(df["ts_event_utc"], utc=True)
    df["utc_date"] = ts.dt.strftime("%Y-%m-%d")
    ct = ts.dt.tz_convert("America/Chicago")
    df["ct"] = ct.dt.tz_localize(None)
    df["m"] = ct.dt.hour * 60 + ct.dt.minute
    ct_date = ct.dt.normalize().dt.tz_localize(None)
    df["sess"] = pd.to_datetime(np.where(df["m"] >= 17 * 60, ct_date + pd.Timedelta(days=1), ct_date))
    df = df[(df["sess"] >= START) & (df["sess"] <= END)].sort_values("ts_event_utc").reset_index(drop=True)
    return df


def load_guardian_es_all():
    frames = []
    for fn in sorted(glob.glob(os.path.join(GUARD_CSV, "ES_*.csv"))):
        d = pd.read_csv(fn)
        d["contract"] = os.path.basename(fn)[:-4]
        frames.append(d)
    d = pd.concat(frames, ignore_index=True)
    d["date"] = pd.to_datetime(d["date"])
    return d


def guardian_selected(d):
    d = d.sort_values(["date", "volume"], ascending=[True, False])
    sel = d.groupby("date").head(1).sort_values("date").reset_index(drop=True)
    changed = sel["contract"] != sel["contract"].shift(1)
    changed.iloc[0] = False
    sel["discard_roll"] = changed
    return sel.set_index("date")


def main():
    df = load_databento()
    g_all = load_guardian_es_all()
    g_sel = guardian_selected(g_all)

    # ------------------------------------------------ sesiones Databento agregadas
    g = df.groupby("sess", sort=True)
    sess = pd.DataFrame({
        "open": g["open"].first(), "high": g["high"].max(), "low": g["low"].min(),
        "close": g["close"].last(), "volume": g["volume"].sum(), "bars": g.size(),
        "first_m": g["m"].first(), "n_contracts": g["contract"].nunique(),
        "contract": g["contract"].first().astype(str),
    })
    degraded_sess = set(df.loc[df["utc_date"].isin(DEGRADED_UTC), "sess"].unique())
    ok = (sess.index.weekday < 5) & (sess["n_contracts"] == 1) & (~sess.index.isin(list(degraded_sess))) & (sess["first_m"] == 17 * 60)
    kept = g_sel[~g_sel["discard_roll"]]
    common = sess.index[ok & sess.index.isin(kept.index)]
    print(f"Fechas comunes (mismo P-control que terreno_tenencia.py): {len(common)}")

    # ------------------------------------------------ 1. la fecha
    print()
    print("=" * 100)
    print("1. LA FECHA 2016-11-16, barra contra barra, con sus vecinas")
    print("=" * 100)
    lo, hi = TARGET - pd.Timedelta(days=3), TARGET + pd.Timedelta(days=3)
    print("  NT8 diario, TODAS las filas de ES_*.csv entre 11-13 y 11-19 (no solo el contrato elegido):")
    w = g_all[(g_all["date"] >= lo) & (g_all["date"] <= hi)].sort_values(["date", "contract"])
    for _, r in w.iterrows():
        tag = "<- elegido" if g_sel.loc[r["date"], "contract"] == r["contract"] else ""
        print(f"    {r['date'].date()}  {r['contract']:<9} O {r['open']:8.2f} H {r['high']:8.2f} L {r['low']:8.2f} C {r['close']:8.2f} V {int(r['volume']):>9}  {tag}")
    print("  Databento, sesion 17:00->16:00 CT reconstruida, mismas fechas:")
    ws = sess[(sess.index >= lo) & (sess.index <= hi)]
    for d, r in ws.iterrows():
        print(f"    {d.date()}  {r['contract']:<9} O {r['open']:8.2f} H {r['high']:8.2f} L {r['low']:8.2f} C {r['close']:8.2f} V {int(r['volume']):>9}  barras {int(r['bars'])}  primera {int(r['first_m'])//60:02d}:{int(r['first_m'])%60:02d} CT")

    s = df[df["sess"] == TARGET]
    print()
    print(f"  Databento, sesion {TARGET.date()}: primeras 6 barras (CT):")
    for _, r in s.head(6).iterrows():
        print(f"    {r['ct']}  {r['contract']}  O {r['open']:.2f} H {r['high']:.2f} L {r['low']:.2f} C {r['close']:.2f} V {int(r['volume'])}")
    imin = s["low"].idxmin()
    r = s.loc[imin]
    print(f"  barra del minimo: {r['ct']}  O {r['open']:.2f} H {r['high']:.2f} L {r['low']:.2f} C {r['close']:.2f} V {int(r['volume'])}")
    imax = s["high"].idxmax()
    r = s.loc[imax]
    print(f"  barra del maximo: {r['ct']}  O {r['open']:.2f} H {r['high']:.2f} L {r['low']:.2f} C {r['close']:.2f} V {int(r['volume'])}")
    rth = s[(s["m"] >= 8 * 60 + 30) & (s["m"] < 15 * 60)]
    print(f"  solo RTH 08:30->15:00: O {rth['open'].iloc[0]:.2f} H {rth['high'].max():.2f} L {rth['low'].min():.2f} C {rth['close'].iloc[-1]:.2f}")
    night = s[s["m"] >= 17 * 60]
    print(f"  solo la tarde-noche 17:00->23:59 del 11-15: O {night['open'].iloc[0]:.2f} H {night['high'].max():.2f} L {night['low'].min():.2f} C {night['close'].iloc[-1]:.2f}  barras {len(night)}")
    # cuantas barras de Databento quedan por debajo del low de NT8 ese dia
    nt8_low = g_sel.loc[TARGET, "low"]
    below = s[s["low"] < nt8_low]
    print(f"  barras de Databento con low < low de NT8 ({nt8_low:.2f}): {len(below)}; primera {below['ct'].iloc[0] if len(below) else '-'}; ultima {below['ct'].iloc[-1] if len(below) else '-'}")
    nt8_open = g_sel.loc[TARGET, "open"]
    at_open = s[(s["open"] == nt8_open) | (s["close"] == nt8_open)]
    print(f"  barras de Databento que tocan el open de NT8 ({nt8_open:.2f}) como open o close: {len(at_open)}; primera {at_open['ct'].iloc[0] if len(at_open) else '-'}")

    # ------------------------------------------------ 2. conteo de discordancias
    print()
    print("=" * 100)
    print("2. CONTEO DE DISCORDANCIAS sobre las fechas comunes, campo por campo y por excursion")
    print("=" * 100)
    a = sess.loc[common]
    b = kept.loc[common]
    cmp = pd.DataFrame(index=common)
    for f in ["open", "high", "low", "close"]:
        cmp[f] = (a[f] - b[f]).abs()
    cmp["largo"] = ((a["open"] - a["low"]) - (b["open"] - b["low"])).abs()
    cmp["corto"] = ((a["high"] - a["open"]) - (b["high"] - b["open"])).abs()
    cmp["vol_ratio"] = a["volume"] / b["volume"]

    # distancia a un cambio de contrato en cualquiera de las dos fuentes
    roll_dates = set(g_sel.index[g_sel["discard_roll"]])
    db_contract = sess["contract"]
    db_roll = set(db_contract.index[db_contract != db_contract.shift(1)][1:])
    all_roll = sorted(roll_dates | db_roll)
    idx_all = sess.index
    pos = {d: i for i, d in enumerate(idx_all)}
    roll_pos = [pos[d] for d in all_roll if d in pos]

    def dist_to_roll(d):
        p = pos[d]
        return min(abs(p - rp) for rp in roll_pos) if roll_pos else 999

    cmp["sesiones_a_roll"] = [dist_to_roll(d) for d in cmp.index]

    print(f"  {'campo':<8}" + "".join(f"{'<= ' + str(x):>10}" for x in BINS) + f"{'> ' + str(BINS[-1]):>10}   (fechas, acumulado por umbral)")
    for f in ["open", "high", "low", "close", "largo", "corto"]:
        x = cmp[f]
        print(f"  {f:<8}" + "".join(f"{int((x <= t).sum()):>10}" for t in BINS) + f"{int((x > BINS[-1]).sum()):>10}")
    print()
    print(f"  volumen: mediana Databento/NT8 = {cmp['vol_ratio'].median():.4f}, p10 {cmp['vol_ratio'].quantile(.1):.4f}, p90 {cmp['vol_ratio'].quantile(.9):.4f}")

    for thr in [2.0, 5.0, 9.0]:
        big = cmp[(cmp["largo"] > thr) | (cmp["corto"] > thr)]
        near = big[big["sesiones_a_roll"] <= 3]
        print(f"  excursion (largo o corto) discordante en mas de {thr:>4.1f} pts: {len(big):>3} fechas; de ellas a <= 3 sesiones de un cambio de contrato: {len(near)}; lejos de todo roll: {len(big) - len(near)}")

    # ---- el cierre: NT8 vs el ultimo precio de Databento a distintas horas.
    # HIPOTESIS a comprobar: el close diario de NT8 es la LIQUIDACION (settlement), que en ES se
    # fija sobre 15:14:30-15:15:00 CT, no el ultimo precio de las 15:59 CT.
    print()
    print("  EL CIERRE. Fechas comunes en las que el close de NT8 coincide (<= 0.25) con el close de la barra de Databento de:")
    for label, mm in [("15:59 CT (ultima barra de la sesion)", 15 * 60 + 59), ("15:14 CT (ultima barra antes del corte 15:15)", 15 * 60 + 14),
                      ("15:15 CT", 15 * 60 + 15), ("15:29 CT", 15 * 60 + 29), ("15:30 CT (primera tras el corte)", 15 * 60 + 30)]:
        bar = df[df["m"] == mm].groupby("sess")["close"].last().reindex(common)
        d = (bar - b["close"]).abs()
        print(f"    {label:<48} {int((d <= 0.25).sum()):>4} de {int(d.notna().sum())} con barra  ({100 * (d <= 0.25).sum() / max(1, d.notna().sum()):.1f} %)")
    bar1514 = df[df["m"] == 15 * 60 + 14].groupby("sess")["close"].last().reindex(common)
    d1514 = (bar1514 - b["close"]).abs()
    print(f"    mediana |close NT8 - close 15:14| = {d1514.median():.2f} pts;  mediana |close NT8 - close 15:59| = {cmp['close'].median():.2f} pts")

    print()
    print("  TODAS las fechas con discordancia > 2 pts en alguna excursion, con el campo que difiere:")
    big = cmp[(cmp["largo"] > 2.0) | (cmp["corto"] > 2.0)].sort_values("largo", ascending=False)
    for d, r in big.iterrows():
        fields = ", ".join(f"{f} {r[f]:.2f}" for f in ["open", "high", "low", "close"] if r[f] > 0.25)
        print(f"    {d.date()}  largo {r['largo']:6.2f}  corto {r['corto']:6.2f}  a {int(r['sesiones_a_roll'])} sesiones de un roll  | campos: {fields}  | vol db/nt8 {r['vol_ratio']:.3f}")


if __name__ == "__main__":
    main()
