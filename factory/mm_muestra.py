"""Multi-mercado, paso 2: la MUESTRA CONGELADA. Calendario y nada mas.

Define, sin leer un solo retorno de estrategia:
  - las ventanas de vuelta de mes de cada mercado bajo (n_before=4, m_after=3)
  - la BANDA DE ROLL: las 8 sesiones que terminan en el ultimo dia de negociacion
    del contrato trimestral (mar/jun/sep/dic), inclusive
  - la exclusion: toda vuelta de mes cuya ventana [entrada..salida] toque la banda
  - los conteos por mercado y los solapamientos por par (periodos comunes)

Convenciones de vencimiento (CME, verificadas contra la ficha del producto salvo donde se dice):
  ES / NQ / YM : tercer viernes del mes de contrato
  NKD          : jueves anterior al segundo viernes (liquidacion = SOQ del segundo viernes)
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
N_BEFORE, M_AFTER = 4, 3
BANDA = 8                      # sesiones, terminando en el vencimiento inclusive
QM = (3, 6, 9, 12)
EXPIRY = {"ES": "3F", "NQ": "3F", "YM": "3F", "NKD": "2F_thu"}
MERCADOS_FASE = ("NQ", "YM", "NKD")     # ES entra solo como referencia


def load(tag: str) -> pd.DataFrame:
    df = pd.read_csv(DATA / f"{tag.lower()}_daily.csv", index_col=0, parse_dates=True)
    df.index.name = "date"
    return df


def nth_weekday(y: int, m: int, wd: int, n: int) -> pd.Timestamp:
    f = pd.Timestamp(y, m, 1)
    return f + pd.Timedelta(days=(wd - f.dayofweek) % 7 + 7 * (n - 1))


def expiries(tag: str, idx: pd.DatetimeIndex) -> list[pd.Timestamp]:
    out = []
    for y in range(idx.min().year, idx.max().year + 1):
        for m in QM:
            e = nth_weekday(y, m, 4, 3) if EXPIRY[tag] == "3F" \
                else nth_weekday(y, m, 4, 2) - pd.Timedelta(days=1)
            if idx.min() <= e <= idx.max():
                out.append(e)
    return out


def sample(tag: str) -> dict:
    df = load(tag)
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
        wins.append({"per": per, "i": int(days[-N_BEFORE]), "j": int(nxt[M_AFTER - 1])})
    band = set()
    for e in expiries(tag, idx):
        j = int(idx.searchsorted(e, side="right")) - 1
        if j >= 0:
            band.update(range(max(0, j - BANDA + 1), j + 1))
    keep, drop = [], []
    for w in wins:
        (drop if any(k in band for k in range(w["i"], w["j"] + 1)) else keep).append(w)
    return {"tag": tag, "df": df, "todas": wins, "keep": keep, "drop": drop}


def main() -> None:
    S = {t: sample(t) for t in ("ES",) + MERCADOS_FASE}
    rep = {"n_before": N_BEFORE, "m_after": M_AFTER, "banda_roll_sesiones": BANDA,
           "convencion_vencimiento": EXPIRY, "mercados": {}, "pares": {}}
    for t, s in S.items():
        rep["mercados"][t] = {
            "desde": str(s["df"].index.min().date()), "hasta": str(s["df"].index.max().date()),
            "vueltas_totales": len(s["todas"]),
            "excluidas_por_roll": len(s["drop"]),
            "vueltas_en_muestra": len(s["keep"]),
            "excluidas_2000_2019": sum(1 for w in s["drop"] if w["per"].year <= 2019),
            "en_muestra_2000_2019": sum(1 for w in s["keep"] if w["per"].year <= 2019),
            "ejemplos_excluidos": [str(w["per"]) for w in s["drop"][:4]],
        }
        print(f"{t:4s} totales={len(s['todas']):3d}  excluidas_por_roll={len(s['drop']):3d}  "
              f"en muestra={len(s['keep']):3d}  (parte A: {rep['mercados'][t]['en_muestra_2000_2019']:3d})")
    print()
    tags = list(MERCADOS_FASE)
    N = sum(rep["mercados"][t]["vueltas_en_muestra"] for t in tags)
    print(f"N nominal de la fase (NQ+YM+NKD, historia completa, post-roll) = {N}")
    for a in range(len(tags)):
        for b in range(a + 1, len(tags)):
            ta, tb = tags[a], tags[b]
            pa = {w["per"] for w in S[ta]["keep"]}
            pb = {w["per"] for w in S[tb]["keep"]}
            comun_full = len(pa & pb)
            paA = {w["per"] for w in S[ta]["keep"] if w["per"].year <= 2019}
            pbA = {w["per"] for w in S[tb]["keep"] if w["per"].year <= 2019}
            rep["pares"][f"{ta}-{tb}"] = {"comunes_historia_completa": comun_full,
                                          "comunes_2000_2019": len(paA & pbA)}
            print(f"  {ta}-{tb}: periodos comunes  completa={comun_full:3d}   2000-2019={len(paA & pbA):3d}")
    rep["N_nominal_fase"] = N
    (HERE / "mm_muestra.json").write_text(json.dumps(rep, indent=2, ensure_ascii=False), encoding="utf-8")
    print("\nescrito: factory/mm_muestra.json")


if __name__ == "__main__":
    main()
