"""RONDA DE FALSACION — las cuatro pruebas pre-registradas (ledger 87f11292a6eee7a9,
f64878c04e90cdaf, 3e5e015f4eef8a6a, 81b6d915f9bf6ed6; K 258-261), UNA corrida cada una.

Escribe el resultado CRUDO a mm_falsacion_resultado.json y NO lo interpreta. Se niega a
correr dos veces. ES no participa; su caja fuerte no se lee.
"""
from __future__ import annotations

import json
import sys
from math import sqrt
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mm_matriz as mm

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"

POINT_VALUE = {"NQ": 2.0, "YM": 0.50, "NKD": 5.0}
FRICTION_RT = {"NQ": 2.40, "YM": 2.40, "NKD": 52.50}
FASE = ("NQ", "YM", "NKD")
A_LAST = pd.Period("2019-11", "M")
DELTA_TOM = 0.101767
CASH = {"NQ": "NDX", "YM": "DJI", "NKD": "N225"}
CASH_START = {"NQ": "2000-09-18", "YM": "2002-04-05", "NKD": "2004-02-17"}


def load_full(tag: str) -> pd.DataFrame:
    df = pd.read_csv(DATA / f"{tag.lower()}_daily.csv", index_col=0, parse_dates=True)
    df.index.name = "date"
    return df.dropna(subset=["open", "close"])


def roll_band(tag: str, idx: pd.DatetimeIndex) -> set:
    band = set()
    for y in range(idx.min().year, idx.max().year + 1):
        for m in mm.QM:
            e = mm.nth_weekday(y, m, 4, 3) if mm.EXPIRY[tag] == "3F" \
                else mm.nth_weekday(y, m, 4, 2) - pd.Timedelta(days=1)
            if not (idx.min() <= e <= idx.max()):
                continue
            j = int(idx.searchsorted(e, side="right")) - 1
            if j >= 0:
                band.update(range(max(0, j - mm.BANDA + 1), j + 1))
    return band


def cluster(vals: pd.DataFrame) -> dict:
    v = vals.to_numpy(float)
    n = int(np.isfinite(v).sum())
    if n == 0:
        return {"n": 0}
    d = float(np.nansum(v) / n)
    t_p = np.nansum(v, axis=1)
    k_p = np.isfinite(v).sum(axis=1)
    se = float(np.sqrt(np.sum((t_p - k_p * d) ** 2)) / n)
    return {"n": n, "delta_hat": round(d, 6), "se_cluster": round(se, 6),
            "z": round(d / se, 4) if se > 0 else None}


# ---------------- PRUEBA 1: placebo sesiones 8 -> 14 --------------------------------
def prueba1() -> tuple[dict, pd.DataFrame]:
    series = {}
    detalle = {}
    for tag in FASE:
        df = load_full(tag)
        idx = df.index
        month = idx.to_period("M")
        band = roll_band(tag, idx)
        rets, dropped = {}, 0
        for per in month.unique():
            days = np.where(month == per)[0]
            if len(days) < 14:
                continue
            i, j = int(days[7]), int(days[13])          # sesiones 8 y 14 (1-indexadas)
            if any(k in band for k in range(i, j + 1)):
                dropped += 1
                continue
            rets[per] = df["open"].iloc[j] - df["open"].iloc[i]
        net = pd.Series(rets).sort_index() * POINT_VALUE[tag] - FRICTION_RT[tag]
        sigma = float(net.std(ddof=1))
        series[tag] = net / sigma
        detalle[tag] = {"n": len(net), "excluidas_por_roll": dropped,
                        "sigma_usd": round(sigma, 2),
                        "delta_hat_mercado": round(float(series[tag].mean()), 6)}
    S = pd.concat(series, axis=1)
    res = cluster(S)
    res.update({"por_mercado": detalle,
                "criterio": "pasa sii delta_hat < 0.0509",
                "PASA": bool(res["delta_hat"] < 0.0509)})
    return res, S


# ---------------- PRUEBA 2: el contado, bruto contra bruto --------------------------
def prueba2() -> dict:
    out = {}
    for tag in FASE:
        cash = pd.read_csv(DATA / f"{CASH[tag].lower()}_daily.csv",
                           index_col=0, parse_dates=True).dropna(subset=["open"])
        cash = cash.loc[CASH_START[tag]:]
        rets_pts, _ = mm.windows_with_roll.__wrapped__(cash) if False else (None, None)
        # ventana -4/+3 sobre el calendario propio, SIN roll (el contado no rulea)
        idx = cash.index
        month = idx.to_period("M")
        rows = {}
        for per in month.unique():
            days = np.where(month == per)[0]
            if len(days) < mm.N_BEFORE + 2:
                continue
            nxt = np.where(month == per + 1)[0]
            if len(nxt) < mm.M_AFTER:
                continue
            i, j = int(days[-mm.N_BEFORE]), int(nxt[mm.M_AFTER - 1])
            rows[per] = cash["open"].iloc[j] - cash["open"].iloc[i]
        g = pd.Series(rows).sort_index()
        sigma = float(g.std(ddof=1))
        d_cash = float((g / sigma).mean())
        # el futuro, en BRUTO: neto publicado + f_i
        fut_net = {"NQ": 0.094809, "YM": 0.127191, "NKD": 0.072892}[tag]
        f_i = FRICTION_RT[tag] / {"NQ": 560.74, "YM": 229.01, "NKD": 3526.93}[tag]
        out[tag] = {"indice": f"^{CASH[tag]}", "n_ventanas": len(g),
                    "delta_bruto_contado": round(d_cash, 6),
                    "delta_bruto_futuro": round(fut_net + f_i, 6),
                    "diferencia": round(d_cash - (fut_net + f_i), 6)}
    pasa = all(v["delta_bruto_contado"] > 0 for v in out.values())
    return {"por_indice": out, "criterio": "pasa sii delta bruto > 0 en los tres",
            "PASA": bool(pasa)}


# ---------------- PRUEBA 3: concentracion en la frontera ----------------------------
def prueba3() -> dict:
    pasos_tot = np.zeros(6)
    n_tot = 0
    por_mercado = {}
    for tag in FASE:
        df = load_full(tag)
        idx = df.index
        month = idx.to_period("M")
        band = roll_band(tag, idx)
        filas = []
        for per in month.unique():
            days = np.where(month == per)[0]
            if len(days) < mm.N_BEFORE + 2:
                continue
            nxt = np.where(month == per + 1)[0]
            if len(nxt) < mm.M_AFTER:
                continue
            i, j = int(days[-mm.N_BEFORE]), int(nxt[mm.M_AFTER - 1])
            if any(k in band for k in range(i, j + 1)):
                continue
            sesiones = [i, i + 1, i + 2, i + 3] if False else None
            camino = [int(days[-4]), int(days[-3]), int(days[-2]), int(days[-1]),
                      int(nxt[0]), int(nxt[1]), int(nxt[2])]
            opens = df["open"].iloc[camino].to_numpy(float)
            filas.append(np.diff(opens))                # 6 pasos en puntos
        arr = np.array(filas) * POINT_VALUE[tag]        # USD brutos
        sigma_full = float(arr.sum(axis=1).std(ddof=1)) # sigma del retorno completo
        std = arr / sigma_full
        por_mercado[tag] = {"n": len(arr),
                            "pasos": [round(float(x), 6) for x in std.mean(axis=0)]}
        pasos_tot += std.sum(axis=0)
        n_tot += len(arr)
    pasos_med = pasos_tot / n_tot
    total = float(pasos_med.sum())
    frontera = float(pasos_med[2] + pasos_med[3] + pasos_med[4])   # -2->-1, -1->+1, +1->+2
    share = frontera / total
    return {"n": n_tot,
            "pasos_agrupados": [round(float(x), 6) for x in pasos_med],
            "etiquetas": ["-4->-3", "-3->-2", "-2->-1", "-1->+1", "+1->+2", "+2->+3"],
            "total_bruto": round(total, 6), "frontera": round(frontera, 6),
            "participacion_frontera": round(share, 4),
            "por_mercado": por_mercado,
            "criterio": "pasa sii participacion >= 0.60",
            "PASA": bool(share >= 0.60)}


# ---------------- PRUEBA 4: el signo del rebalanceo ---------------------------------
def prueba4() -> dict:
    series_sign, series_std = {}, {}
    excl = {}
    for tag in FASE:
        df = load_full(tag)
        idx = df.index
        month = idx.to_period("M")
        band = roll_band(tag, idx)
        rets, signo, fuera = {}, {}, 0
        for per in month.unique():
            days = np.where(month == per)[0]
            if len(days) < mm.N_BEFORE + 2:
                continue
            nxt = np.where(month == per + 1)[0]
            if len(nxt) < mm.M_AFTER:
                continue
            i, j = int(days[-mm.N_BEFORE]), int(nxt[mm.M_AFTER - 1])
            if any(k in band for k in range(i, j + 1)):
                continue
            prev = np.where(month == per - 1)[0]
            if len(days) < 5 or len(prev) == 0:         # falta sesion -5 o cierre previo
                fuera += 1
                continue
            c_m5 = df["close"].iloc[int(days[-5])]
            c_prev = df["close"].iloc[int(prev[-1])]
            rets[per] = df["open"].iloc[j] - df["open"].iloc[i]
            signo[per] = 1 if (c_m5 / c_prev - 1) > 0 else -1
        net = pd.Series(rets).sort_index() * POINT_VALUE[tag] - FRICTION_RT[tag]
        sigma = float(net.std(ddof=1))
        series_std[tag] = net / sigma
        series_sign[tag] = pd.Series(signo).sort_index()
        excl[tag] = fuera
    S = pd.concat(series_std, axis=1)
    G = pd.concat(series_sign, axis=1)
    res = {}
    for etiqueta, s in [("tras_mes_en_baja", -1), ("tras_mes_en_alza", 1)]:
        mask = G == s
        res[etiqueta] = cluster(S.where(mask))
    brecha = res["tras_mes_en_baja"]["delta_hat"] - res["tras_mes_en_alza"]["delta_hat"]
    res.update({"brecha": round(brecha, 6), "fuera_por_condicionante": excl,
                "criterio": "pasa sii brecha >= 0.02",
                "PASA": bool(brecha >= 0.02)})
    return res


def main() -> int:
    out_path = HERE / "mm_falsacion_resultado.json"
    if out_path.exists():
        print("mm_falsacion_resultado.json YA EXISTE. Una corrida por prueba. Abortado.")
        return 1
    p1, S1 = prueba1()
    bloq = {"bloque_A": cluster(S1.loc[[p for p in S1.index if p <= A_LAST]]),
            "bloque_B": cluster(S1.loc[[p for p in S1.index if p > A_LAST]])}
    p1["bloques"] = bloq
    out = {"pre_registros": ["87f11292a6eee7a9", "f64878c04e90cdaf",
                             "3e5e015f4eef8a6a", "81b6d915f9bf6ed6"],
           "P1_placebo_calendario": p1,
           "P2_contado_testigo": prueba2(),
           "P3_concentracion_frontera": prueba3(),
           "P4_signo_rebalanceo": prueba4(),
           "nota": "resultado CRUDO; el veredicto es un documento aparte"}
    out["PASAN"] = {k: out[k]["PASA"] for k in
                    ("P1_placebo_calendario", "P2_contado_testigo",
                     "P3_concentracion_frontera", "P4_signo_rebalanceo")}
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
