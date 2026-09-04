"""SELECCION DE DIAS para la compra de microestructura. No compra nada, no llama a Databento.

VENTANA G. K = 261. No gasta cartucho.

Elige, con datos LOCALES (ES 1-min 2016-2019), un dia NORMAL por cada tercil EX-ANTE de volatilidad
-el eje validado en juez_regimen_exante.py: volatilidad (rango medio de barra de 1 minuto) de la
sesion ANTERIOR- y publica los cortes de tercil en PUNTOS BASICOS de precio, para poder clasificar
dias de 2026 (ES cotiza ~3x mas alto que en 2016-2019: el corte en puntos no sirve entre epocas).

DIA NORMAL: martes a jueves; sesion completa (>= 1.300 barras de 1 minuto); contrato unico; no
degradado; fuera de la semana de vencimiento trimestral (el tercer viernes de mar/jun/sep/dic y los
8 dias previos, que es cuando se rola). Y para mbo, desde 2017-06: GLBX.MDP3 no tiene mbo antes del
2017-05-21 (metadata.get_dataset_range, leido 2026-09-04).

Dentro de cada tercil se elige la sesion cuya volatilidad ex-ante esta mas cerca de la MEDIANA del
tercil: representativa, no extrema. Regla determinista, escrita antes de mirar.
"""
from __future__ import annotations

import os
import sys
from datetime import date, timedelta

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "research", "ventana_g"))
from razon_escalas import cargar_con_sesion  # noqa: E402

MIN_BARRAS_NORMAL = 1300
DESDE_MBO = pd.Timestamp("2017-06-01")


def tercer_viernes(y, m):
    d = date(y, m, 15)
    while d.weekday() != 4:
        d += timedelta(days=1)
    return d


def semana_vencimiento(fecha):
    """True si la fecha cae en los 8 dias previos al tercer viernes trimestral o ese mismo dia."""
    if fecha.month in (3, 6, 9, 12):
        tv = tercer_viernes(fecha.year, fecha.month)
        return tv - timedelta(days=8) <= fecha.date() <= tv
    return False


def main():
    df = cargar_con_sesion()
    cl = df["close"].to_numpy(float); hi = df["high"].to_numpy(float); lo = df["low"].to_numpy(float)
    sess = df["sess"].to_numpy()
    corte = np.flatnonzero(sess[1:] != sess[:-1]) + 1
    ini = np.concatenate(([0], corte)); fin = np.concatenate((corte, [len(cl)]))
    fechas = pd.to_datetime(sess[ini])
    nb = fin - ini
    rango = hi - lo
    vol_pt = np.array([rango[a:b].mean() for a, b in zip(ini, fin)])
    px = np.array([cl[a:b].mean() for a, b in zip(ini, fin)])
    vol_bps = vol_pt / px * 1e4
    prev_pt = np.concatenate([[np.nan], vol_pt[:-1]])
    prev_bps = np.concatenate([[np.nan], vol_bps[:-1]])
    ok = ~np.isnan(prev_pt)
    p33, p66 = np.nanquantile(prev_pt, [1 / 3, 2 / 3])
    b33, b66 = np.nanquantile(prev_bps, [1 / 3, 2 / 3])
    tercil = np.where(~ok, -1, np.where(prev_pt <= p33, 0, np.where(prev_pt <= p66, 1, 2)))

    print("CORTES DE TERCIL EX-ANTE (volatilidad de la sesion anterior), 2016-2019, 1.006 sesiones")
    print(f"   en puntos:          bajo <= {p33:.4f} < medio <= {p66:.4f} < alto")
    print(f"   en puntos basicos:  bajo <= {b33:.3f} < medio <= {b66:.3f} < alto   (para clasificar 2026)")
    print(f"   precio medio ES 2016-2019: {px.mean():.0f}; los cortes en bps son los que viajan entre epocas.")

    normal = (ok & (nb >= MIN_BARRAS_NORMAL) & (fechas.weekday >= 1) & (fechas.weekday <= 3)
              & (fechas >= DESDE_MBO) & ~np.array([semana_vencimiento(f) for f in fechas]))
    print(f"\n   sesiones candidatas (normales, desde 2017-06): {int(normal.sum())} de {len(fechas)}")
    print(f"\n   {'tercil':>8}{'fecha':>12}{'dia':>5}{'barras':>8}{'vol ex-ante pt':>16}{'ex-ante bps':>13}"
          f"{'vol propia pt':>15}{'mediana tercil':>16}")
    elegidos = []
    for t, nom in ((0, "bajo"), (1, "medio"), (2, "alto")):
        m = normal & (tercil == t)
        med = float(np.median(prev_pt[m]))
        i = int(np.flatnonzero(m)[np.argmin(np.abs(prev_pt[m] - med))])
        f = fechas[i]
        elegidos.append((nom, f.date(), float(prev_bps[i])))
        print(f"   {nom:>8}{str(f.date()):>12}{f.strftime('%a'):>5}{nb[i]:>8}{prev_pt[i]:>16.4f}"
              f"{prev_bps[i]:>13.3f}{vol_pt[i]:>15.4f}{med:>16.4f}")
    print("\n   ELEGIDOS (B, 2017-2019):")
    for nom, f, bps in elegidos:
        print(f"      {nom:<6} {f}   (ex-ante {bps:.2f} bps)")
    print("\n   Sesion = 17:00 CT del dia anterior -> 16:00 CT (T23). En UTC: [dia-1 22:00, dia 21:00)"
          " en horario de verano; [dia-1 23:00, dia 22:00) en invierno.")


if __name__ == "__main__":
    main()
