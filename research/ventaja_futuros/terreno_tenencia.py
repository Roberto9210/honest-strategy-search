"""Terreno por duracion de tenencia -- ejecuta terreno_tenencia_preregistro.md.

NO busca ventaja. NO mira rentabilidad. Excursion adversa desde la apertura
de una ventana horaria fija, sobre ES a 1 minuto de Databento, 2016-2019.

ORDEN OBLIGATORIO: primero el control (T23 reconstruida vs barras diarias
de NT8 del guardian, mismas fechas). Si el control no PASA, el script
termina con codigo 1 y la escalera NO se calcula ni se imprime.

    venv/Scripts/python.exe research/ventaja_futuros/terreno_tenencia.py > research/ventaja_futuros/terreno_tenencia.txt
"""

from __future__ import annotations

import glob
import os
import sys

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, "data", "es_1min_databento.csv")
GUARD_CSV = (r"C:\Users\home\AppData\Local\Temp\claude\C--Users-home-Desktop-ALAYA"
             r"\03cf4965-af02-4a1f-8eb0-bc27e9d414df\scratchpad\nt8-daily-csv")

START, END = pd.Timestamp("2016-01-04"), pd.Timestamp("2019-12-31")
# Dias 'degraded' de Databento dentro del periodo, tomados de
# data/data_quality_es_1min_databento.md seccion 1b. Fechas UTC.
DEGRADED_UTC = {"2017-11-13", "2018-10-21", "2019-01-15", "2019-02-22", "2019-03-13", "2019-03-26"}

MES_POINT_VALUE = 5.0     # dolares por punto, MES. SUPUESTO de traslado: los puntos son de ES.
ES_POINT_VALUE = 50.0
PCTS = [50, 90, 95, 99]

# Publicado por el guardian en f75d126, docs/resultado-pregunta1-terreno.md, M1 raiz ES,
# periodo 2016-08-23 -> 2026-08-21. ORIENTACION, no control: el periodo no es el mismo.
GUARD_PUBLISHED = {
    "largo": {"p50": 17.50, "p90": 73.00, "p95": 95.33, "p99": 155.03, "max": 355.75},
    "corto": {"p50": 18.50, "p90": 63.05, "p95": 82.50, "p99": 145.41, "max": 513.75},
}

# Ventanas en minutos CT desde medianoche. T23 es la sesion entera.
WINDOWS = [
    ("T23  17:00->16:00 (~23 h)", None, None),
    ("RTH  08:30->15:00 (6.5 h)", 8 * 60 + 30, 15 * 60),
    ("H1   08:30->09:30 (1 h)", 8 * 60 + 30, 9 * 60 + 30),
    ("M15  08:30->08:45 (15 min)", 8 * 60 + 30, 8 * 60 + 45),
]


def hr(title):
    print()
    print("=" * 110)
    print(title)
    print("=" * 110)


def pct_row(x):
    x = np.asarray(x, dtype=float)
    out = {f"p{p}": float(np.percentile(x, p)) for p in PCTS}
    out["max"] = float(x.max())
    out["n"] = int(len(x))
    return out


# ------------------------------------------------------------------ Databento
def load_databento():
    df = pd.read_csv(SRC, usecols=["ts_event_utc", "contract", "open", "high", "low", "close"],
                     dtype={"contract": "category"})
    # recorte grueso por prefijo antes de parsear fechas (4.9M filas)
    yr = df["ts_event_utc"].str.slice(0, 4)
    df = df[yr.isin(["2016", "2017", "2018", "2019", "2020"])].copy()
    ts = pd.to_datetime(df["ts_event_utc"], utc=True)
    df["utc_date"] = ts.dt.strftime("%Y-%m-%d")
    ct = ts.dt.tz_convert("America/Chicago")
    df["m"] = ct.dt.hour * 60 + ct.dt.minute
    ct_date = ct.dt.normalize().dt.tz_localize(None)
    df["sess"] = np.where(df["m"] >= 17 * 60, ct_date + pd.Timedelta(days=1), ct_date)
    df["sess"] = pd.to_datetime(df["sess"])
    df = df[(df["sess"] >= START) & (df["sess"] <= END)].copy()
    df = df.sort_values("ts_event_utc").reset_index(drop=True)
    return df


def window_stats(df, a, b):
    """Por sesion: open de la primera barra, min low, max high, minuto de la primera y ultima barra."""
    if a is None:
        sub = df
    else:
        sub = df[(df["m"] >= a) & (df["m"] < b)]
    g = sub.groupby("sess", sort=True)
    out = pd.DataFrame({
        "open": g["open"].first(),
        "low": g["low"].min(),
        "high": g["high"].max(),
        "first_m": g["m"].first(),
        "last_m": g["m"].last(),
        "bars": g.size(),
    })
    out["largo"] = out["open"] - out["low"]
    out["corto"] = out["high"] - out["open"]
    return out


# ------------------------------------------------------------------ guardian NT8 daily, raiz ES
def load_guardian_es():
    frames = []
    for fn in sorted(glob.glob(os.path.join(GUARD_CSV, "ES_*.csv"))):
        d = pd.read_csv(fn)
        d["contract"] = os.path.basename(fn)[:-4]
        frames.append(d)
    if not frames:
        raise SystemExit(f"no hay ES_*.csv en {GUARD_CSV}")
    d = pd.concat(frames, ignore_index=True)
    d["date"] = pd.to_datetime(d["date"])
    # regla de Ventana A: por fecha, el contrato de mayor volumen; abortar si hay empate
    d = d.sort_values(["date", "volume"], ascending=[True, False])
    top2 = d.groupby("date").head(2)
    ties = top2.groupby("date")["volume"].agg(lambda s: len(s) == 2 and s.iloc[0] == s.iloc[1])
    if ties.any():
        raise SystemExit(f"EMPATE de volumen en {int(ties.sum())} fechas; la regla no es total aca")
    sel = d.groupby("date").head(1).sort_values("date").reset_index(drop=True)
    changed = sel["contract"] != sel["contract"].shift(1)
    changed.iloc[0] = False
    sel["discard_roll"] = changed
    sel["largo"] = sel["open"] - sel["low"]
    sel["corto"] = sel["high"] - sel["open"]
    return sel


def main():
    print("TERRENO POR DURACION DE TENENCIA -- Ventana D, 2026-09-03")
    print("ES a 1 minuto (Databento), 2016-01-04 -> 2019-12-31. NO es MES. Excursion adversa, sin costos.")
    print("Ejecuta terreno_tenencia_preregistro.md. Primero el control; sin control no hay escalera.")

    # ============================================================ carga y poblacion base
    df = load_databento()
    hr("0. POBLACION -- sesiones del periodo y que excluye cada regla")
    sess_all = df.groupby("sess").agg(n_contracts=("contract", "nunique"), bars=("open", "size"))
    sess_all["weekday"] = sess_all.index.weekday
    degraded_sess = set(df.loc[df["utc_date"].isin(DEGRADED_UTC), "sess"].unique())
    t23 = window_stats(df, None, None)
    rth = window_stats(df, 8 * 60 + 30, 15 * 60)

    base = sess_all.copy()
    base["weekend"] = base["weekday"] >= 5
    base["multi_contract"] = base["n_contracts"] > 1
    base["degraded"] = base.index.isin(list(degraded_sess))
    base["open_1700_missing"] = ~(t23["first_m"].reindex(base.index) == 17 * 60)
    base["ok_base"] = ~(base["weekend"] | base["multi_contract"] | base["degraded"] | base["open_1700_missing"])

    print(f"  sesiones etiquetadas en el periodo            : {len(base)}")
    print(f"  excluidas por caer en sabado/domingo          : {int(base['weekend'].sum())}")
    print(f"  excluidas por mas de un contrato en la sesion : {int(base['multi_contract'].sum())}")
    print(f"  excluidas por dia 'degraded' de Databento     : {int(base['degraded'].sum())}")
    print(f"  excluidas por no tener barra a las 17:00 CT   : {int(base['open_1700_missing'].sum())}")
    print(f"  (las reglas se solapan; una sesion puede caer en varias)")
    print(f"  P-base (pasa todas)                           : {int(base['ok_base'].sum())}")

    # ============================================================ 1. CONTROL
    hr("1. CONTROL -- T23 reconstruida desde minutos vs barras diarias de NT8 (guardian 37a0144), MISMAS FECHAS")
    g = load_guardian_es()
    g_period = g[(g["date"] >= START) & (g["date"] <= END)]
    g_kept = g_period[~g_period["discard_roll"]].set_index("date")
    print(f"  NT8 diario ES en el periodo: {len(g_period)} fechas ({g_period['date'].min().date()} -> {g_period['date'].max().date()}),"
          f" {int(g_period['discard_roll'].sum())} descartadas por cambio de contrato, {len(g_kept)} conservadas")
    ok_idx = base.index[base["ok_base"]]
    common = t23.loc[t23.index.isin(ok_idx) & t23.index.isin(g_kept.index)]
    gc = g_kept.loc[common.index]
    print(f"  P-control (interseccion): {len(common)} fechas, {common.index.min().date()} -> {common.index.max().date()}")
    print(f"  Databento en P-base sin barra NT8 conservada ese dia: {int((~t23.index[t23.index.isin(ok_idx)].isin(g_kept.index)).sum())}")
    print(f"  NT8 conservadas sin sesion Databento en P-base      : {int((~g_kept.index.isin(ok_idx)).sum())}")

    verdicts = []
    for side in ["largo", "corto"]:
        a = pct_row(common[side])
        b = pct_row(gc[side])
        print()
        print(f"  --- lado {side.upper()} ---   {'':<10}{'p50':>9}{'p90':>9}{'p95':>9}{'p99':>9}{'max':>9}{'n':>7}")
        print(f"  Databento minutos->T23 {'':<3}" + "".join(f"{a[k]:>9.2f}" for k in ['p50', 'p90', 'p95', 'p99', 'max']) + f"{a['n']:>7}")
        print(f"  NT8 diario (mismas fechas)" + "".join(f"{b[k]:>9.2f}" for k in ['p50', 'p90', 'p95', 'p99', 'max']) + f"{b['n']:>7}")
        rel = {k: (a[k] - b[k]) / b[k] * 100 for k in ['p50', 'p90', 'p95', 'p99', 'max']}
        print(f"  diferencia relativa %     " + "".join(f"{rel[k]:>+9.2f}" for k in ['p50', 'p90', 'p95', 'p99', 'max']))
        gp = GUARD_PUBLISHED[side]
        print(f"  guardian PUBLICADO 2016-26" + "".join(f"{gp[k]:>9.2f}" for k in ['p50', 'p90', 'p95', 'p99', 'max']) + "   (orientacion, otro periodo)")
        worst = max(abs(rel[k]) for k in ["p50", "p90", "p95"])
        verdicts.append(worst)

    # acuerdo por fecha, lado largo
    both = pd.DataFrame({"db": common["largo"], "nt8": gc["largo"]})
    both = both[both["nt8"] > 0]
    ratio = both["db"] / both["nt8"]
    diff = (both["db"] - both["nt8"]).abs()
    corr = float(np.corrcoef(both["db"], both["nt8"])[0, 1])
    print()
    print(f"  ACUERDO POR FECHA, lado largo, sobre {len(both)} fechas con excursion NT8 > 0:")
    print(f"    mediana de la razon Databento/NT8 : {ratio.median():.4f}   (p10 {ratio.quantile(0.10):.4f}, p90 {ratio.quantile(0.90):.4f})")
    print(f"    fechas con |diferencia| <= 0.25 pt : {int((diff <= 0.25).sum())}  ({100 * (diff <= 0.25).mean():.1f} %)")
    print(f"    fechas con |diferencia| <= 2 pt    : {int((diff <= 2.0).sum())}  ({100 * (diff <= 2.0).mean():.1f} %)")
    print(f"    correlacion                        : {corr:.4f}")
    worst_diff = both.assign(diff=both["db"] - both["nt8"]).sort_values("diff", key=np.abs, ascending=False).head(8)
    print("    las 8 fechas con mayor diferencia (db - nt8):")
    for d, r in worst_diff.iterrows():
        print(f"      {d.date()}  db {r['db']:8.2f}  nt8 {r['nt8']:8.2f}  diff {r['diff']:+8.2f}")

    worst = max(verdicts)
    med = float(ratio.median())
    if worst < 5.0 and 0.97 <= med <= 1.03:
        verdict = "PASA"
    elif worst < 10.0 and 0.95 <= med <= 1.05:
        verdict = "INDETERMINADO"
    else:
        verdict = "FALLA"
    print()
    print(f"  >>> CONTROL: {verdict}   (peor diferencia en p50/p90/p95 = {worst:.2f} %, mediana de razon por fecha = {med:.4f})")
    print(f"      criterio pre-registrado: PASA < 5 % y razon en [0.97, 1.03]; 5-10 % INDETERMINADO; >= 10 % o razon fuera de [0.95, 1.05] FALLA")
    if verdict != "PASA":
        print()
        print("  >>> SE PARA. La escalera NO se calcula. Dos proveedores en desacuerdo son informacion, no un detalle.")
        sys.exit(1)

    # ============================================================ 2. ESCALERA
    hr("2. ESCALERA -- P-escalera: un contrato, no degraded, barra 17:00 CT, barra 08:30 CT, ultima barra RTH >= 15:59 CT")
    esc = base["ok_base"].copy()
    has_0830 = rth["first_m"].reindex(base.index) == 8 * 60 + 30
    full_rth = rth["last_m"].reindex(base.index) >= 15 * 60 - 1
    print(f"  P-base                                         : {int(esc.sum())}")
    print(f"  de ellas, sin barra exacta a las 08:30 CT       : {int((esc & ~has_0830.fillna(False)).sum())}")
    print(f"  de ellas, con cierre anticipado (sin barra 14:59): {int((esc & has_0830.fillna(False) & ~full_rth.fillna(False)).sum())}")
    esc = esc & has_0830.fillna(False) & full_rth.fillna(False)
    idx = base.index[esc]
    print(f"  P-ESCALERA                                      : {len(idx)}   ({idx.min().date()} -> {idx.max().date()})")

    results = {}
    for name, a, b in WINDOWS:
        w = window_stats(df, a, b).reindex(idx)
        assert w["open"].notna().all(), name
        if a is not None:
            assert (w["first_m"] == a).all(), name
        results[name] = w

    ref = results[WINDOWS[0][0]]
    for side in ["largo", "corto"]:
        hr(f"2.{side.upper()} -- excursion adversa {side} ({'open - min(low)' if side == 'largo' else 'max(high) - open'}), P-escalera n = {len(idx)}")
        print(f"  {'ventana':<28}{'n':>6} | {'p50':>8}{'p90':>8}{'p95':>8}{'p99':>8}{'max':>8} pts | "
              f"{'p50':>7}{'p90':>7}{'p95':>7}{'p99':>7} USD MES(x5) | {'>1000USD MES':>13}{'>1000USD ES':>13}")
        for name, _, _ in WINDOWS:
            x = results[name][side].values
            s = pct_row(x)
            over_mes = 100 * np.mean(x > 1000 / MES_POINT_VALUE)
            over_es = 100 * np.mean(x > 1000 / ES_POINT_VALUE)
            print(f"  {name:<28}{s['n']:>6} | " + "".join(f"{s[k]:>8.2f}" for k in ['p50', 'p90', 'p95', 'p99', 'max']) + " pts | "
                  + "".join(f"{s[k] * MES_POINT_VALUE:>7.0f}" for k in ['p50', 'p90', 'p95', 'p99']) + " USD MES(x5) | "
                  + f"{over_mes:>12.2f}%{over_es:>12.2f}%")

    # ============================================================ 3. LA TABLA
    hr("3. LA TABLA -- caida de cada percentil respecto de T23 (1 - percentil_ventana / percentil_T23), en %")
    for side in ["largo", "corto"]:
        print(f"  --- lado {side.upper()} ---")
        print(f"  {'ventana':<28}{'n':>6} | {'p50':>8}{'p90':>8}{'p95':>8}{'p99':>8} pts | {'caida p50':>10}{'caida p90':>10}{'caida p95':>10}{'caida p99':>10}")
        r = pct_row(ref[side].values)
        for name, _, _ in WINDOWS:
            s = pct_row(results[name][side].values)
            drops = {k: 100 * (1 - s[k] / r[k]) for k in ['p50', 'p90', 'p95', 'p99']}
            print(f"  {name:<28}{s['n']:>6} | " + "".join(f"{s[k]:>8.2f}" for k in ['p50', 'p90', 'p95', 'p99']) + " pts | "
                  + "".join(f"{drops[k]:>9.1f}%" for k in ['p50', 'p90', 'p95', 'p99']))
        print()

    print("Limitaciones, repetidas al pie: esto es ES y no MES (libros separados, OHLC distinto); los USD 'de MES' son")
    print("puntos de ES x 5 y su traslado es un SUPUESTO. Una tenencia de horario fijo no es una estrategia: es otra")
    print("tenencia pasiva, mas corta. No se miro rentabilidad de ninguna ventana.")


if __name__ == "__main__":
    main()
