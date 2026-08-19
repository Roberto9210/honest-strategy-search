"""Familia 2 — Seguimiento de tendencia en barras diarias.

Modelo de ejecución (anti-lookahead):
- La señal se calcula con el CIERRE del día t usando solo datos <= t.
- La entrada se ejecuta en la APERTURA del día t+1.
- La salida se ejecuta en la APERTURA del día siguiente a la señal de salida.
- points = precio_salida - precio_entrada (cortos: invertido). contracts = 1.
La fricción la descuenta el harness ($3.90/operación); aquí todo es bruto.
"""
import numpy as np
import pandas as pd


def _trades_from_position(df: pd.DataFrame, pos: pd.Series) -> pd.DataFrame:
    """pos: serie {-1,0,+1} decidida al cierre del día t.
    Se traduce a operaciones ejecutadas en la apertura de t+1."""
    pos = pos.shift(1).fillna(0)          # la posición del día t se decidió en t-1
    opens = df["open"]
    trades = []
    cur = 0
    entry_price = None
    entry_day = None
    for day, p in pos.items():
        p = int(p)
        if p != cur:
            if cur != 0:                   # cerrar posición vigente en la apertura de hoy
                pts = (opens.loc[day] - entry_price) * cur
                trades.append((day, pts))
            if p != 0:                     # abrir nueva en la apertura de hoy
                entry_price = opens.loc[day]
                entry_day = day
            cur = p
    if cur != 0:                           # posición abierta al final: cerrar al último open
        last = df.index[-1]
        if entry_day != last:
            trades.append((last, (opens.loc[last] - entry_price) * cur))
    if not trades:
        return pd.DataFrame(columns=["points", "contracts"])
    out = pd.DataFrame(trades, columns=["exit_time", "points"]).set_index("exit_time")
    out["contracts"] = 1
    return out


def donchian(df: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    n, m = cfg["entry_n"], cfg["exit_n"]
    hi = df["close"].rolling(n).max().shift(1)   # extremos hasta AYER
    lo = df["close"].rolling(n).min().shift(1)
    exit_hi = df["close"].rolling(m).max().shift(1)
    exit_lo = df["close"].rolling(m).min().shift(1)
    pos = pd.Series(0, index=df.index)
    cur = 0
    for i, day in enumerate(df.index):
        c = df["close"].iloc[i]
        if cur == 0:
            if c > hi.iloc[i]:
                cur = 1
            elif c < lo.iloc[i] and cfg.get("short", True):
                cur = -1
        elif cur == 1 and c < exit_lo.iloc[i]:
            cur = 0
        elif cur == -1 and c > exit_hi.iloc[i]:
            cur = 0
        pos.iloc[i] = cur
    return _trades_from_position(df, pos)


def ma_cross(df: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    f = df["close"].rolling(cfg["fast"]).mean()
    s = df["close"].rolling(cfg["slow"]).mean()
    raw = np.where(f > s, 1, -1 if cfg.get("short", True) else 0)
    pos = pd.Series(raw, index=df.index).where(s.notna(), 0)
    return _trades_from_position(df, pos)


CONFIGS = [
    ("donchian", {"entry_n": 20, "exit_n": 10, "short": True}),
    ("donchian", {"entry_n": 20, "exit_n": 10, "short": False}),
    ("donchian", {"entry_n": 55, "exit_n": 20, "short": True}),
    ("donchian", {"entry_n": 55, "exit_n": 20, "short": False}),
    ("donchian", {"entry_n": 10, "exit_n": 5,  "short": True}),
    ("donchian", {"entry_n": 10, "exit_n": 5,  "short": False}),
    ("donchian", {"entry_n": 40, "exit_n": 15, "short": True}),
    ("donchian", {"entry_n": 40, "exit_n": 15, "short": False}),
    ("ma_cross", {"fast": 10, "slow": 50,  "short": True}),
    ("ma_cross", {"fast": 10, "slow": 50,  "short": False}),
    ("ma_cross", {"fast": 20, "slow": 100, "short": True}),
    ("ma_cross", {"fast": 20, "slow": 100, "short": False}),
    ("ma_cross", {"fast": 50, "slow": 200, "short": True}),
    ("ma_cross", {"fast": 50, "slow": 200, "short": False}),
]

FNS = {"donchian": donchian, "ma_cross": ma_cross}
