"""Multi-mercado, paso 1: BAJAR y CONTROLAR CALIDAD. No calcula ni un retorno de estrategia.

Lo unico que produce son propiedades del PROVEEDOR y del CALENDARIO:
filas, rango, huecos, OHLC absurdo, y cuantas vueltas de mes hay bajo (n_before=4, m_after=3).
Nunca una media, nunca un P&L, nunca un profit factor. La matriz de correlacion es otro script.

Fuente: Yahoo Finance via yfinance (Ticker.history, auto_adjust=False, sin pre/post).
Los CSV van a data/, que esta gitignored: no se redistribuyen.
"""
from __future__ import annotations

import json
import os
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
DATA = REPO / "data"
DATA.mkdir(exist_ok=True)

# Candidatos: ES entra SOLO como referencia (mercado de descubrimiento, excluido de la fase).
MARKETS = {
    "ES": "ES=F",
    "NQ": "NQ=F",
    "YM": "YM=F",
    "NKD": "NKD=F",
    "RTY": "RTY=F",
}
N_BEFORE, M_AFTER = 4, 3
COLS = ["Open", "High", "Low", "Close", "Volume"]


def download(tag: str, ticker: str) -> pd.DataFrame:
    import yfinance as yf
    path = DATA / f"{tag.lower()}_daily.csv"
    if path.exists():
        df = pd.read_csv(path, index_col=0, parse_dates=True)
        df.index.name = "date"
        return df
    df = yf.Ticker(ticker).history(period="max", interval="1d",
                                   auto_adjust=False, actions=False, prepost=False)
    if df is None or df.empty:
        raise RuntimeError(f"serie vacia para {ticker}")
    df = df[COLS].copy()
    df.columns = [c.lower() for c in df.columns]
    df.index = pd.to_datetime(df.index).tz_localize(None).normalize()
    df.index.name = "date"
    df.to_csv(path, date_format="%Y-%m-%d")
    return df


def qc(tag: str, df: pd.DataFrame) -> dict:
    idx = df.index
    bd = pd.bdate_range(idx.min(), idx.max())
    deltas = pd.Series(idx).diff().dt.days.dropna()
    # hueco = mas de 3 dias habiles faltantes entre filas consecutivas (mismo criterio que qc/)
    gaps = []
    for a, b in zip(idx[:-1], idx[1:]):
        missing = len(pd.bdate_range(a, b)) - 2
        if missing > 3:
            gaps.append((str(a.date()), str(b.date()), missing))
    close = df["close"].to_numpy(float)
    ret = np.diff(close) / close[:-1]
    incoh = int(((df["high"] < df["low"])
                 | (df["high"] < df[["open", "close"]].max(axis=1) - 1e-9)
                 | (df["low"] > df[["open", "close"]].min(axis=1) + 1e-9)).sum())
    return {
        "mercado": tag,
        "filas": int(len(df)),
        "desde": str(idx.min().date()),
        "hasta": str(idx.max().date()),
        "monotono": bool(idx.is_monotonic_increasing),
        "duplicados": int(idx.duplicated().sum()),
        "nan_ohlc": int(df[["open", "high", "low", "close"]].isna().sum().sum()),
        "volumen_cero": int((df["volume"] == 0).sum()),
        "ohlc_incoherente": incoh,
        "precio_no_positivo": int((df[["open", "high", "low", "close"]] <= 0).sum().sum()),
        "sesiones_habiles_del_rango": int(len(bd)),
        "cobertura_vs_habiles": round(len(df) / len(bd), 4),
        "huecos_gt_3_habiles": len(gaps),
        "huecos_detalle": gaps[:15],
        "max_salto_cierre_a_cierre": round(float(np.nanmax(np.abs(ret))) * 100, 2),
        "fecha_max_salto": str(idx[1:][int(np.nanargmax(np.abs(ret)))].date()),
    }


def month_turn_windows(idx: pd.DatetimeIndex, n_before: int, m_after: int) -> list[dict]:
    """Ventanas de vuelta de mes SOLO por calendario: posiciones de sesion, no precios.
    Replica exactamente la seleccion de indices de familias_4_5.turn_of_month."""
    month = idx.to_period("M")
    entry_pos = {}
    for per in month.unique():
        days = np.where(month == per)[0]
        if len(days) < n_before + 2:
            continue
        entry_pos[per] = int(days[-n_before])
    out = []
    for per, ei in entry_pos.items():
        nxt = np.where(month == per + 1)[0]
        if len(nxt) < m_after:
            continue
        xi = int(nxt[m_after - 1])
        out.append({"periodo": str(per), "entrada_i": ei, "salida_i": xi,
                    "entrada": str(idx[ei].date()), "salida": str(idx[xi].date())})
    return out


def nth_weekday(year: int, month: int, weekday: int, n: int) -> pd.Timestamp:
    """n-esimo <weekday> del mes (weekday: lunes=0 ... viernes=4)."""
    first = pd.Timestamp(year=year, month=month, day=1)
    shift = (weekday - first.dayofweek) % 7
    return first + pd.Timedelta(days=shift + 7 * (n - 1))


def main() -> int:
    report = {"n_before": N_BEFORE, "m_after": M_AFTER, "mercados": {}}
    for tag, ticker in MARKETS.items():
        try:
            df = download(tag, ticker)
        except Exception as exc:
            report["mercados"][tag] = {"mercado": tag, "ERROR": repr(exc)}
            print(f"{tag}: FALLO {exc!r}")
            continue
        r = qc(tag, df)
        idx = df.index
        wins_full = month_turn_windows(idx, N_BEFORE, M_AFTER)
        a = df.loc[:"2019-12-31"]
        wins_a = month_turn_windows(a.index, N_BEFORE, M_AFTER)
        r["ticker"] = ticker
        r["vueltas_de_mes_historia_completa"] = len(wins_full)
        r["vueltas_de_mes_2000_2019"] = len(wins_a)
        r["primera_vuelta"] = wins_full[0]["entrada"] if wins_full else None
        r["ultima_vuelta"] = wins_full[-1]["salida"] if wins_full else None
        # posicion de la sesion de salida dentro del mes (indice 0 = primera sesion del mes)
        pos_salida = []
        month = idx.to_period("M")
        for w in wins_full:
            days = np.where(month == month[w["salida_i"]])[0]
            pos_salida.append(int(np.where(days == w["salida_i"])[0][0]))
        r["indice_de_sesion_de_salida"] = {"min": min(pos_salida), "max": max(pos_salida)} if pos_salida else None
        report["mercados"][tag] = r
        print(f"{tag:4s} {ticker:6s} filas={r['filas']:5d}  {r['desde']} -> {r['hasta']}  "
              f"cobertura={r['cobertura_vs_habiles']:.3f}  huecos={r['huecos_gt_3_habiles']:2d}  "
              f"vueltas: completa={len(wins_full):3d}  2000-2019={len(wins_a):3d}")
    out = HERE / "mm_qc_cobertura.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nescrito: {out.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
