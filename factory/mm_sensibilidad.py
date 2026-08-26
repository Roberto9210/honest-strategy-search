"""Agregados a la spec ANTES del pre-registro. Tres calculos, ninguno es un backtest:

1. SENSIBILIDAD A NKD: las dos compuertas recalculadas sin NKD, con la matriz ya
   publicada (mm_matriz_resultado.json) y los conteos de calendario. Solo lo que
   Roberto pidio: el eslabon NKD. NO es una invitacion a elegir subconjuntos --
   reportar el mejor subconjunto esta en la lista de §f que convierte K=1 en mentira.

2. LA CUENTA DEL FORWARD: a que ritmo crece n_efectivo por anio calendario con los
   tres mercados (R medida como supuesto declarado, conteos post-roll por anio), y
   cuantos anios tarda en llegar a 342, contra ES solo.

3. ALINEACION DE CALENDARIO DE NKD: cotiza en CME pero su subyacente es Tokio.
   Se verifica contra los datos que cada sesion de NKD lleva el MISMO dia calendario
   que ES/NQ/YM y que la ventana de vuelta de mes no queda corrida una sesion.
   Fechas e indices de sesion: cero precios, cero retornos.
"""
from __future__ import annotations

import json
from math import sqrt
from pathlib import Path

import numpy as np
import pandas as pd

import mm_matriz as mm

HERE = Path(__file__).resolve().parent
RES = json.loads((HERE / "mm_matriz_resultado.json").read_text(encoding="utf-8"))
MUE = json.loads((HERE / "mm_muestra.json").read_text(encoding="utf-8"))

R = {a: {b: v for b, v in row.items()} for a, row in RES["matriz_R"].items()}
U = {a: {b: v for b, v in row.items()} for a, row in RES["matriz_cota_sup_90"].items()}
FULL = {t: MUE["mercados"][t]["vueltas_en_muestra"] for t in ("NQ", "YM", "NKD")}
OV = {tuple(sorted(k.split("-"))): v["comunes_historia_completa"] for k, v in MUE["pares"].items()}
UMBRAL = RES["regla"]["umbral_operaciones_efectivas"]


def n_ef(matrix, tags):
    N = sum(FULL[t] for t in tags)
    den = 0.0
    for a in tags:
        for b in tags:
            ov = FULL[a] if a == b else OV[tuple(sorted((a, b)))]
            den += matrix[a][b] * ov
    return N * N / den, N


def main():
    print("=" * 72)
    print("1. SENSIBILIDAD: las dos compuertas si NKD se cae (queda NQ+YM)")
    print("=" * 72)
    for nombre, tags in [("los tres (control: reproduce el veredicto)", ["NQ", "YM", "NKD"]),
                         ("SIN NKD", ["NQ", "YM"])]:
        n1, N = n_ef(R, tags)
        n2, _ = n_ef(U, tags)
        print(f"  {nombre}: N={N}")
        print(f"    compuerta 1: n_ef = {n1:8.1f}  {'PASA' if n1 >= UMBRAL else 'NO PASA'} "
              f"(umbral {UMBRAL})")
        print(f"    compuerta 2: n_ef = {n2:8.1f}  {'PASA' if n2 >= UMBRAL else 'NO PASA'}"
              f"  [margen {100*(n2/UMBRAL-1):+.1f}%]")

    print()
    print("=" * 72)
    print("2. LA CUENTA DEL FORWARD (R medida como supuesto declarado)")
    print("=" * 72)
    # ritmo anual post-roll, medido sobre la muestra congelada completa
    anios = {}
    tasa = {}
    for t in ("NQ", "YM", "NKD"):
        m = MUE["mercados"][t]
        span = (pd.Period(m["hasta"][:7], "M") - pd.Period(m["desde"][:7], "M")).n / 12.0
        anios[t] = span
        tasa[t] = FULL[t] / span
        print(f"  {t}: {FULL[t]} vueltas post-roll en {span:.1f} anios  ->  {tasa[t]:.2f}/anio")
    # hacia adelante los tres estan presentes a la vez: solapamiento anual = tasa del
    # mercado con MENOS vueltas del par (las exclusiones de NKD son subconjunto de sus periodos)
    ov_y = {("NQ", "YM"): min(tasa["NQ"], tasa["YM"]),
            ("NKD", "NQ"): min(tasa["NQ"], tasa["NKD"]),
            ("NKD", "YM"): min(tasa["YM"], tasa["NKD"])}
    n_y = sum(tasa.values())
    den_y = n_y + 2 * sum(R[a][b] * ov_y[tuple(sorted((a, b)))]
                          for a, b in [("NQ", "YM"), ("NQ", "NKD"), ("YM", "NKD")])
    ritmo = n_y * n_y / den_y
    print(f"  nominales/anio = {n_y:.2f};  n_efectivo/anio = {ritmo:.2f}")
    print(f"  anios de forward para 342 efectivas, 3 mercados: {UMBRAL / ritmo:.1f}")
    print(f"  contra ES solo (12/anio, n_ef = n):              {UMBRAL / 12.0:.1f}")
    print(f"  [el encargo estimaba ~15.2/anio y ~22.5 anios]")

    print()
    print("=" * 72)
    print("3. ALINEACION DE CALENDARIO DE NKD (fechas e indices, cero precios)")
    print("=" * 72)
    idx = {t: mm.load(t).index for t in ("ES", "NQ", "YM", "NKD")}
    base = idx["NQ"]
    nkd = idx["NKD"]
    comun_rango = base[(base >= nkd.min()) & (base <= nkd.max())]
    solo_nkd = nkd.difference(comun_rango)
    solo_nq = comun_rango.difference(nkd)
    print(f"  rango comun {nkd.min().date()} -> {nkd.max().date()}")
    print(f"  sesiones NQ en el rango: {len(comun_rango)};  NKD: {len(nkd)}")
    print(f"  dias de NKD que NQ no tiene: {len(solo_nkd)}  {[str(d.date()) for d in solo_nkd[:8]]}")
    print(f"  dias de NQ que NKD no tiene: {len(solo_nq)}  {[str(d.date()) for d in solo_nq[:8]]}")
    wd = pd.Series(nkd.dayofweek).value_counts().sort_index()
    print(f"  dias de semana de NKD (0=lun..6=dom): {wd.to_dict()}")

    # la prueba que decide: para cada periodo comun, la ENTRADA y la SALIDA de la
    # ventana de NKD contra las de NQ, en dias de diferencia
    def windows(tag):
        rets, _ = mm.windows_with_roll(tag, mm.load(tag))
        df = mm.load(tag)
        idx_ = df.index
        month = idx_.to_period("M")
        out = {}
        for per in month.unique():
            days = np.where(month == per)[0]
            if len(days) < mm.N_BEFORE + 2:
                continue
            nxt = np.where(month == per + 1)[0]
            if len(nxt) < mm.M_AFTER:
                continue
            out[per] = (idx_[days[-mm.N_BEFORE]], idx_[nxt[mm.M_AFTER - 1]])
        return {p: v for p, v in out.items() if p in rets.index}

    w_nq, w_nkd = windows("NQ"), windows("NKD")
    comunes = sorted(set(w_nq) & set(w_nkd))
    d_ent = [abs((w_nkd[p][0] - w_nq[p][0]).days) for p in comunes]
    d_sal = [abs((w_nkd[p][1] - w_nq[p][1]).days) for p in comunes]
    ent_dist = pd.Series(d_ent).value_counts().sort_index().to_dict()
    sal_dist = pd.Series(d_sal).value_counts().sort_index().to_dict()
    print(f"  periodos comunes NQ-NKD comparados: {len(comunes)}")
    print(f"  |dif| en dias CALENDARIO de la ENTRADA: {ent_dist}")
    print(f"  |dif| en dias CALENDARIO de la SALIDA:  {sal_dist}")
    identicas = sum(1 for p in comunes if w_nkd[p][0] == w_nq[p][0] and w_nkd[p][1] == w_nq[p][1])
    print(f"  ventanas con entrada Y salida en el MISMO dia calendario: {identicas}/{len(comunes)}")


if __name__ == "__main__":
    main()
