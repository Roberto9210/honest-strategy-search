"""CLASIFICA los dias de 2026 posteriores a la caja sellada por el tercil EX-ANTE de volatilidad.
No compra nada: lee el archivo auxiliar ya descargado (ohlcv-1m, ES.n.0, 2026-08-19 22:00Z -> 2026-09-04).

VENTANA G. K = 261. No gasta cartucho.

Eje: volatilidad (rango medio de barra de 1 minuto) de la sesion ANTERIOR, en puntos basicos de
precio para poder usar los cortes de 2016-2019 (databento_seleccion_dias.py), porque ES cotiza ~3x
mas alto que entonces y un corte en puntos no viaja entre epocas.

Sesion = 17:00 CT del dia anterior -> 16:00 CT (T23), como en toda la ventana.

Regla de eleccion, escrita antes de mirar: 2026-09-02 esta aprobada y ocupa el tercil en que caiga.
Para los otros dos terciles se elige el dia normal (martes a jueves, sesion completa, ni feriado ni
vencimiento) cuyo valor ex-ante este mas cerca del CENTRO del tercil segun los cortes de 2016-2019;
si un tercil no tiene ningun dia posterior a la caja, se dice y se elige el mas cercano, marcado
como RELATIVO (no es de ese tercil).

Uso: python databento_clasificar_2026.py <b33> <b66>     (cortes en bps de 2016-2019)
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import databento as db

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "data" / "microestructura" / "ohlcv-1m_ESn0_auxiliar_2026.dbn.zst"
FIJO = pd.Timestamp("2026-09-02")
EXCLUIR = {pd.Timestamp("2026-08-21")}      # tercer viernes de agosto: vencimiento mensual de opciones


def main(argv):
    b33, b66 = float(argv[1]), float(argv[2])
    store = db.DBNStore.from_file(SRC)
    df = store.to_df(price_type="float", pretty_ts=True)
    ts = df.index.tz_convert("America/Chicago")
    m = ts.hour * 60 + ts.minute
    fecha = ts.normalize().tz_localize(None)
    sess = pd.to_datetime(np.where(m >= 17 * 60, fecha + pd.Timedelta(days=1), fecha))
    df = df.assign(sess=sess, rango=df["high"] - df["low"])
    g = df.groupby("sess").agg(barras=("close", "size"), vol_pt=("rango", "mean"), px=("close", "mean"))
    g["vol_bps"] = g["vol_pt"] / g["px"] * 1e4
    g["exante_bps"] = g["vol_bps"].shift(1)
    g["exante_pt"] = g["vol_pt"].shift(1)
    g["dia"] = g.index.strftime("%a")
    g["tercil"] = np.where(g["exante_bps"].isna(), "-",
                           np.where(g["exante_bps"] <= b33, "bajo", np.where(g["exante_bps"] <= b66, "medio", "alto")))
    normal = ((g.index.weekday >= 1) & (g.index.weekday <= 3) & (g["barras"] >= 1300)
              & g["exante_bps"].notna() & ~g.index.isin(EXCLUIR))
    g["normal"] = normal
    print(f"cortes 2016-2019 en bps: bajo <= {b33:.3f} < medio <= {b66:.3f} < alto")
    print(f"\n{'sesion':>12}{'dia':>5}{'barras':>8}{'px':>8}{'vol pt':>9}{'vol bps':>9}{'ex-ante bps':>13}{'tercil':>8}{'normal':>8}")
    for s, r in g.iterrows():
        ex = f"{r['exante_bps']:.3f}" if not np.isnan(r["exante_bps"]) else "  -"
        print(f"{str(s.date()):>12}{r['dia']:>5}{int(r['barras']):>8}{r['px']:>8.0f}{r['vol_pt']:>9.4f}{r['vol_bps']:>9.3f}"
              f"{ex:>13}{r['tercil']:>8}{('si' if r['normal'] else 'no'):>8}")
    centros = {"bajo": b33 / 2, "medio": (b33 + b66) / 2, "alto": b66 * 1.25}
    eleg = {}
    if FIJO in g.index:
        eleg[g.loc[FIJO, "tercil"]] = (FIJO.date(), float(g.loc[FIJO, "exante_bps"]), "aprobado")
    cand = g[normal & (g.index != FIJO)]
    for t in ("bajo", "medio", "alto"):
        if t in eleg:
            continue
        c = cand[cand["tercil"] == t]
        if len(c):
            i = (c["exante_bps"] - centros[t]).abs().idxmin()
            eleg[t] = (i.date(), float(c.loc[i, "exante_bps"]), "en tercil")
        elif len(cand):
            i = (cand["exante_bps"] - centros[t]).abs().idxmin()
            eleg[t] = (i.date(), float(cand.loc[i, "exante_bps"]), f"RELATIVO: ningun dia post-caja cae en '{t}'")
    print("\nELEGIDOS (A, 2026):")
    for t in ("bajo", "medio", "alto"):
        if t in eleg:
            d, bps, como = eleg[t]
            print(f"   {t:<6} {d}   ex-ante {bps:.3f} bps   ({como})")
        else:
            print(f"   {t:<6} SIN CANDIDATO")


if __name__ == "__main__":
    main(sys.argv)
