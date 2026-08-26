"""LA PRUEBA UNICA — pre-registrada en el ledger (PRE_REGISTRO 8129df0c2170b9fe) ANTES
de que este script exista. Se corre UNA VEZ. El resultado, sea cual sea, es el resultado.

Primer y unico calculo de P&L multi-mercado del proyecto: historia completa post-roll de
NQ, YM y NKD (2000/2002/2004 -> 2026). La caja fuerte de ES (2020-2026 de ES) NO se lee:
ES no participa de esta prueba.

Este script escribe el resultado CRUDO a mm_prueba_resultado.json y NO lo interpreta:
el veredicto es un documento aparte, escrito despues de commitear el crudo (encargo
26-ago, pasos 4 y 5).
"""
from __future__ import annotations

import json
import sys
from math import erfc, sqrt
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mm_matriz as mm          # windows_with_roll: la misma banda y la misma seleccion

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"

# congelado en el PRE_REGISTRO 8129df0c2170b9fe
POINT_VALUE = {"NQ": 2.0, "YM": 0.50, "NKD": 5.0}       # MNQ / MYM / NKD
FRICTION_RT = {"NQ": 2.40, "YM": 2.40, "NKD": 52.50}
ESPERADO = {"NQ": 309, "YM": 289, "NKD": 180}           # muestra congelada (mm_muestra.json)
N_EF_PREREG = 361.3
Z_CRIT = 1.959964
A_LAST = pd.Period("2019-11", "M")


def load_full(tag: str) -> pd.DataFrame:
    df = pd.read_csv(DATA / f"{tag.lower()}_daily.csv", index_col=0, parse_dates=True)
    df.index.name = "date"
    return df                    # SIN corte: esta es la prueba


def cluster_stats(s: pd.DataFrame) -> dict:
    """s: filas = periodos, columnas = mercados, valores estandarizados (NaN si ausente).
    delta_hat = media sobre las N operaciones; SE agrupado por periodo."""
    vals = s.to_numpy(float)
    n = int(np.isfinite(vals).sum())
    if n == 0:
        return {"n": 0}
    delta = float(np.nansum(vals) / n)
    t_p = np.nansum(vals, axis=1)                       # suma por periodo
    k_p = np.isfinite(vals).sum(axis=1)                 # mercados activos por periodo
    resid = t_p - k_p * delta
    se = float(np.sqrt(np.sum(resid ** 2)) / n)
    z = delta / se if se > 0 else float("nan")
    return {"n": n, "delta_hat": round(delta, 6), "se_cluster": round(se, 6),
            "z": round(z, 4), "p_bilateral": round(erfc(abs(z) / sqrt(2)), 6),
            "periodos": int((k_p > 0).sum())}


def main() -> int:
    out_path = HERE / "mm_prueba_resultado.json"
    if out_path.exists():
        print("mm_prueba_resultado.json YA EXISTE. La prueba se corre UNA vez. Abortado.")
        return 1

    per_market, series = {}, {}
    for tag in ("NQ", "YM", "NKD"):
        rets_pts, dropped = mm.windows_with_roll(tag, load_full(tag))
        assert len(rets_pts) == ESPERADO[tag], \
            f"{tag}: {len(rets_pts)} vueltas contra {ESPERADO[tag]} de la muestra congelada"
        net = rets_pts * POINT_VALUE[tag] - FRICTION_RT[tag]
        sigma = float(net.std(ddof=1))
        series[tag] = net / sigma
        per_market[tag] = {"n": int(len(net)), "sigma_usd": round(sigma, 2),
                           "friccion_rt_usd": FRICTION_RT[tag],
                           "delta_hat_mercado": round(float(series[tag].mean()), 6),
                           "excluidas_por_roll": dropped}

    S = pd.concat(series, axis=1)                       # index = periodos
    res_total = cluster_stats(S)
    z_diseno = res_total["delta_hat"] * sqrt(N_EF_PREREG)

    bloque_a = cluster_stats(S.loc[[p for p in S.index if p <= A_LAST]])
    bloque_b = cluster_stats(S.loc[[p for p in S.index if p > A_LAST]])

    out = {
        "pre_registro": "8129df0c2170b9fe (ledger), spec commits 7c0e4d0/250d298/59fa917/9456128",
        "prueba_unica": {**res_total,
                         "confirma": bool(abs(res_total["z"]) >= Z_CRIT),
                         "z_critico": Z_CRIT},
        "z_diseno_diagnostico": round(z_diseno, 4),
        "por_mercado": per_market,
        "bloque_A_hasta_2019_11": bloque_a,
        "bloque_B_desde_2019_12": bloque_b,
        "nota": "resultado CRUDO, escrito antes de cualquier interpretacion; "
                "el veredicto es un documento aparte",
    }
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
