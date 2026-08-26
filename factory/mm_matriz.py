"""Multi-mercado, la medicion que decide: MATRIZ DE CORRELACION de los retornos de
vuelta de mes (F4 congelada: n_before=4, m_after=3) sobre 2000-2019.

Disciplina de salida ciega, la misma de sigma_ciego.py:
  - los retornos se DESMEDIAN por mercado antes de correlacionar; la media no sale nunca
  - la salida se valida contra una LISTA BLANCA de claves y falla cerrado ante cualquier otra
  - nunca una media, nunca una suma, nunca un P&L, nunca un profit factor

NO se toca 2020-2026 de NINGUN mercado: cada serie se corta en 2019-12-31 ANTES de
construir ventanas (el protocolo del ledger: la vuelta de dic-2019 muere sola porque
no tiene sesiones de enero). Los conteos 2020-2026 que usa la regla de decision vienen
de mm_muestra.json, que es CALENDARIO (fechas), no precios.

La regla de decision contra la que se contrasta esta escrita y commiteada ANTES
(spec_botc_multimercado.md §d, commit 7c0e4d0), igual que la prediccion (mm_prediccion.md).
"""
from __future__ import annotations

import json
import sys
from math import erfc, sqrt
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"

N_BEFORE, M_AFTER = 4, 3
A_END = "2019-12-31"
BANDA = 8
QM = (3, 6, 9, 12)
EXPIRY = {"ES": "3F", "NQ": "3F", "YM": "3F", "NKD": "2F_thu"}
FASE = ("NQ", "YM", "NKD")          # ES entra SOLO como fila de referencia (spec §D1)

# spec §c: efecto pre-registrado y maquinaria de potencia (harness_f2 §3.2)
DELTA = 25.30 / 166.95              # 0.151542, neto MES sobre ES parte A
DELTA_BRUTO = DELTA + 3.90 / 166.95
Z_A, Z_B = 1.959964, 0.841621
POWER_CONST = Z_A + Z_B             # 2.801585
Z90 = 1.281552

# spec §c.3 — friccion por mercado, contrato chico donde existe. NO verificadas contra
# CME salvo NKD (spec §b.8); el min() de la formula impide que un error las afloje.
FRICTION = {
    "NQ":  {"instrumento": "MNQ", "point_value": 2.0,  "tick": 0.25, "comision_rt": 1.40},
    "YM":  {"instrumento": "MYM", "point_value": 0.50, "tick": 1.00, "comision_rt": 1.40},
    "NKD": {"instrumento": "NKD", "point_value": 5.0,  "tick": 5.00, "comision_rt": 2.50},
}

WHITELIST_MERCADO = {"mercado", "n_parte_a", "sigma_puntos", "sigma_usd_instrumento",
                     "instrumento", "friccion_rt_usd", "f_i", "delta_i", "excluidas_por_roll_parte_a"}


def load(tag: str) -> pd.DataFrame:
    df = pd.read_csv(DATA / f"{tag.lower()}_daily.csv", index_col=0, parse_dates=True)
    df.index.name = "date"
    return df.loc[:A_END]           # el corte ANTES de construir nada


def nth_weekday(y: int, m: int, wd: int, n: int) -> pd.Timestamp:
    f = pd.Timestamp(y, m, 1)
    return f + pd.Timedelta(days=(wd - f.dayofweek) % 7 + 7 * (n - 1))


def windows_with_roll(tag: str, df: pd.DataFrame):
    """Ventanas de vuelta de mes post-exclusion de roll. Identica seleccion de indices
    que familias_4_5.turn_of_month; identica banda que mm_muestra.py."""
    idx = df.index
    month = idx.to_period("M")
    wins = []
    for per in month.unique():
        days = np.where(month == per)[0]
        if len(days) < N_BEFORE + 2:
            continue
        nxt = np.where(month == per + 1)[0]
        if len(nxt) < M_AFTER:
            continue
        wins.append((per, int(days[-N_BEFORE]), int(nxt[M_AFTER - 1])))
    band = set()
    for y in range(idx.min().year, idx.max().year + 1):
        for m in QM:
            e = nth_weekday(y, m, 4, 3) if EXPIRY[tag] == "3F" \
                else nth_weekday(y, m, 4, 2) - pd.Timedelta(days=1)
            if not (idx.min() <= e <= idx.max()):
                continue
            j = int(idx.searchsorted(e, side="right")) - 1
            if j >= 0:
                band.update(range(max(0, j - BANDA + 1), j + 1))
    keep = [(per, i, j) for per, i, j in wins
            if not any(k in band for k in range(i, j + 1))]
    dropped = len(wins) - len(keep)
    rets = pd.Series({per: df["open"].iloc[j] - df["open"].iloc[i] for per, i, j in keep},
                     name=tag).sort_index()
    return rets, dropped


def correlate(series: dict[str, pd.Series]):
    """Correlaciones por pares sobre periodos comunes, DESMEDIANDO por mercado.
    Devuelve (matriz, n_comunes). Jamas devuelve una media."""
    tags = list(series)
    R = pd.DataFrame(np.eye(len(tags)), index=tags, columns=tags)
    NC = pd.DataFrame(0, index=tags, columns=tags, dtype=int)
    for i, a in enumerate(tags):
        NC.loc[a, a] = len(series[a])
        for b in tags[i + 1:]:
            j = pd.concat([series[a], series[b]], axis=1).dropna()
            x = j.iloc[:, 0].to_numpy(float)
            y = j.iloc[:, 1].to_numpy(float)
            x = x - x.mean()        # desmediado interno; la media muere aca
            y = y - y.mean()
            r = float(np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y)))
            R.loc[a, b] = R.loc[b, a] = r
            NC.loc[a, b] = NC.loc[b, a] = len(j)
    return R, NC


def n_efectivo(R: pd.DataFrame, counts: dict[str, int], overlaps: dict[tuple, int]) -> float:
    """spec §c.2: n_ef = N^2 / sum_ij R_ij * |T_i ∩ T_j|. Solo mercados de la FASE."""
    tags = [t for t in R.index if t in counts]
    N = sum(counts[t] for t in tags)
    den = 0.0
    for a in tags:
        for b in tags:
            ov = counts[a] if a == b else overlaps[tuple(sorted((a, b)))]
            den += float(R.loc[a, b]) * ov
    return N * N / den, N


def upper90(R: pd.DataFrame, NC: pd.DataFrame) -> pd.DataFrame:
    """Compuerta 2: cota superior al 90% de cada correlacion, tope en 1."""
    U = R.copy()
    for a in R.index:
        for b in R.columns:
            if a == b:
                continue
            r, n = float(R.loc[a, b]), int(NC.loc[a, b])
            se = (1 - r * r) / sqrt(max(n - 3, 1))
            U.loc[a, b] = min(r + Z90 * se, 1.0)
    return U


def power(n_ef: float, delta: float) -> float:
    return 0.5 * erfc(-(delta * sqrt(n_ef) - Z_A) / sqrt(2))


def main() -> int:
    # --- retornos de vuelta de mes, parte A, post-roll --------------------------------
    series, per_market = {}, []
    for tag in ("ES",) + FASE:
        rets, dropped = windows_with_roll(tag, load(tag))
        series[tag] = rets
        row = {"mercado": tag, "n_parte_a": int(len(rets)),
               "sigma_puntos": round(float(rets.std(ddof=1)), 4),
               "excluidas_por_roll_parte_a": dropped}
        if tag in FRICTION:
            fr = FRICTION[tag]
            sigma_usd = float(rets.std(ddof=1)) * fr["point_value"]
            rt = fr["comision_rt"] + 2 * fr["tick"] * fr["point_value"]
            f_i = rt / sigma_usd
            row.update({"instrumento": fr["instrumento"],
                        "sigma_usd_instrumento": round(sigma_usd, 2),
                        "friccion_rt_usd": round(rt, 2),
                        "f_i": round(f_i, 6),
                        "delta_i": round(min(DELTA_BRUTO - f_i, DELTA), 6)})
        extra = set(row) - WHITELIST_MERCADO
        if extra:
            raise SystemExit(f"SALIDA FUERA DE LA LISTA BLANCA: {extra}")
        per_market.append(row)

    # control duro (spec A.3 corregida): la muestra congelada de ES en el bloque A es 230
    # -- las 231 del ledger (049b809f5e9def5c) menos la vuelta 2017-08, excluida por roll.
    assert len(series["ES"]) == 230, f"ES bloque A = {len(series['ES'])}, esperaba 230 (231 del ledger - 2017-08)"

    R, NC = correlate(series)

    # --- conteos de la muestra congelada (calendario, mm_muestra.json) ----------------
    mm = json.loads((HERE / "mm_muestra.json").read_text(encoding="utf-8"))
    full = {t: mm["mercados"][t]["vueltas_en_muestra"] for t in FASE}
    a_cnt = {t: mm["mercados"][t]["en_muestra_bloque_A"] for t in FASE}
    b_cnt = {t: full[t] - a_cnt[t] for t in FASE}
    ov_full, ov_a, ov_b = {}, {}, {}
    for k, v in mm["pares"].items():
        pair = tuple(sorted(k.split("-")))
        ov_full[pair] = v["comunes_historia_completa"]
        ov_a[pair] = v["comunes_bloque_A"]
        ov_b[pair] = v["comunes_historia_completa"] - v["comunes_bloque_A"]

    # --- la regla de decision, tal como quedo escrita ---------------------------------
    delta_is = [r["delta_i"] for r in per_market if "delta_i" in r]
    n_tot = sum(full.values())
    delta_barra = sum(d * full[t] for d, t in zip(delta_is, FASE)) / n_tot
    umbral = (POWER_CONST / delta_barra) ** 2

    nef1, N1 = n_efectivo(R, full, ov_full)
    U = upper90(R, NC)
    nef2, _ = n_efectivo(U, full, ov_full)
    nefA, NA = n_efectivo(R, a_cnt, ov_a)
    nefB, NB = n_efectivo(R, b_cnt, ov_b)

    out = {
        "regla": {"umbral_operaciones_efectivas": round(umbral, 2),
                  "delta_barra": round(delta_barra, 6),
                  "procedencia": "spec_botc_multimercado.md §c-§d, commit 7c0e4d0"},
        "por_mercado": per_market,
        "matriz_R": {a: {b: round(float(R.loc[a, b]), 4) for b in R.columns} for a in R.index},
        "n_comunes": {a: {b: int(NC.loc[a, b]) for b in NC.columns} for a in NC.index},
        "matriz_cota_sup_90": {a: {b: round(float(U.loc[a, b]), 4) for b in U.columns} for a in U.index},
        "compuerta_1": {"N_nominal": N1, "n_efectivo": round(nef1, 1),
                        "pasa": bool(nef1 >= umbral)},
        "compuerta_2": {"n_efectivo_cota_sup": round(nef2, 1),
                        "pasa": bool(nef2 >= umbral)},
        "bloques_D1": {"bloque_A_hasta_2019_11": {"N": NA, "n_efectivo": round(nefA, 1)},
                       "bloque_B_desde_2019_12": {"N": NB, "n_efectivo": round(nefB, 1)},
                       "nota": "R medida en 2000-2019 aplicada a ambos bloques; 2020-2026 de NQ/YM/NKD no es la caja fuerte (esa es ES)"},
        "potencia": {"con_n_efectivo": round(power(nef1, DELTA), 4),
                     "delta_minimo_detectable": round(POWER_CONST / sqrt(nef1), 6),
                     "delta_75pct": round(power(nef1, DELTA * 0.75), 4),
                     "delta_50pct": round(power(nef1, DELTA * 0.50), 4)},
        "VEREDICTO": "LA FASE SE ABRE" if (nef1 >= umbral and nef2 >= umbral)
                     else "LA FASE NO SE ABRE",
    }
    (HERE / "mm_matriz_resultado.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"umbral = {umbral:.2f} op. efectivas (delta_barra = {delta_barra:.6f})\n")
    print("matriz R (2000-2019, post-roll, desmediada):")
    print(R.round(4).to_string())
    print("\nperiodos comunes:")
    print(NC.to_string())
    print("\ncota superior 90%:")
    print(U.round(4).to_string())
    print(f"\nCOMPUERTA 1: N={N1}  n_efectivo={nef1:.1f}  ->  {'PASA' if out['compuerta_1']['pasa'] else 'NO PASA'}")
    print(f"COMPUERTA 2: n_efectivo(cota sup)={nef2:.1f}  ->  {'PASA' if out['compuerta_2']['pasa'] else 'NO PASA'}")
    print(f"bloques D1: A(<=2019-11) N={NA} n_ef={nefA:.1f}   B(2019-12->) N={NB} n_ef={nefB:.1f}")
    print(f"potencia con n_ef: {out['potencia']['con_n_efectivo']:.1%}  "
          f"(al 75% del delta: {out['potencia']['delta_75pct']:.1%}, al 50%: {out['potencia']['delta_50pct']:.1%})")
    print(f"delta minimo detectable al 80%: {out['potencia']['delta_minimo_detectable']:.6f}")
    print(f"\n=== {out['VEREDICTO']} ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
