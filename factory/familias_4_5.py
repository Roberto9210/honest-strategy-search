"""Familia 4 — Patrones de calendario. Familia 5 — Compresión de volatilidad.
Barras diarias. Mismo modelo anti-lookahead que Familia 2:
señal al cierre de t => ejecución en la apertura de t+1.

Familia 5 usa una aproximación documentada: la entrada "al romper el nivel"
se aproxima con datos diarios asumiendo fill en el nivel si el high/low del
día lo cruza (si abre gapeado más allá, fill en la apertura). El slippage
del harness cubre parte del optimismo de esta aproximación; queda anotado.
"""
import numpy as np
import pandas as pd


def _fixed_exit_trades(df, entries, hold_days, side=1):
    """entries: lista de (día_entrada_idx, precio_entrada). Sale en la
    apertura tras hold_days días de mercado."""
    opens = df["open"]
    trades = []
    n = len(df)
    for i, price in entries:
        j = min(i + hold_days, n - 1)
        pts = (opens.iloc[j] - price) * side
        trades.append((df.index[j], pts))
    if not trades:
        return pd.DataFrame(columns=["points", "contracts"])
    out = pd.DataFrame(trades, columns=["exit_time", "points"]).set_index("exit_time")
    out["contracts"] = 1
    return out


# ---------- Familia 4: calendario ----------

def turn_of_month(df, cfg):
    """Largo desde la apertura del día -N (antes de fin de mes) hasta la
    apertura del día +M del mes siguiente."""
    n_before, m_after = cfg["n_before"], cfg["m_after"]
    month = df.index.to_period("M")
    entries = []
    idx_positions = {}
    for per in month.unique():
        days = np.where(month == per)[0]
        if len(days) < n_before + 2:
            continue
        entry_i = days[-n_before]
        entries.append((entry_i, df["open"].iloc[entry_i]))
        idx_positions[per] = entry_i
    trades = []
    for per, entry_i in idx_positions.items():
        nxt = np.where(month == per + 1)[0]
        if len(nxt) < m_after:
            continue
        exit_i = nxt[m_after - 1]
        pts = df["open"].iloc[exit_i] - df["open"].iloc[entry_i]
        trades.append((df.index[exit_i], pts))
    if not trades:
        return pd.DataFrame(columns=["points", "contracts"])
    out = pd.DataFrame(trades, columns=["exit_time", "points"]).set_index("exit_time")
    out["contracts"] = 1
    return out


def day_of_week(df, cfg):
    """Largo (o corto) en la sesión del día de semana indicado:
    entra en la apertura, sale en la apertura del día siguiente."""
    dow, side = cfg["dow"], cfg.get("side", 1)
    entries = [(i, df["open"].iloc[i]) for i in range(len(df) - 1)
               if df.index[i].dayofweek == dow]
    return _fixed_exit_trades(df, entries, 1, side)


# ---------- Familia 5: compresión de volatilidad ----------

def nr_breakout(df, cfg):
    """Día t con el rango más estrecho de los últimos N (NR-N):
    al día siguiente, stop-buy en high(t) / stop-sell en low(t) (el primero
    que cruce; aproximación diaria). Salida en la apertura tras hold días."""
    n, hold = cfg["n"], cfg["hold"]
    rng = df["high"] - df["low"]
    is_nr = rng == rng.rolling(n).min()
    trades = []
    idx = df.index
    for i in range(n, len(df) - hold - 1):
        if not is_nr.iloc[i]:
            continue
        hi, lo = df["high"].iloc[i], df["low"].iloc[i]
        nxt = i + 1
        o, h, l = df["open"].iloc[nxt], df["high"].iloc[nxt], df["low"].iloc[nxt]
        if o >= hi:
            entry, side = o, 1
        elif o <= lo:
            entry, side = o, -1
        elif h >= hi:
            entry, side = hi, 1
        elif l <= lo:
            entry, side = lo, -1
        else:
            continue
        j = min(nxt + hold, len(df) - 1)
        pts = (df["open"].iloc[j] - entry) * side
        trades.append((idx[j], pts))
    if not trades:
        return pd.DataFrame(columns=["points", "contracts"])
    out = pd.DataFrame(trades, columns=["exit_time", "points"]).set_index("exit_time")
    out["contracts"] = 1
    return out


CONFIGS_F4 = [
    ("turn_of_month", {"n_before": 4, "m_after": 3}),
    ("turn_of_month", {"n_before": 2, "m_after": 2}),
    ("turn_of_month", {"n_before": 5, "m_after": 5}),
    ("day_of_week", {"dow": 0, "side": 1}),   # lunes largo
    ("day_of_week", {"dow": 0, "side": -1}),  # lunes corto
    ("day_of_week", {"dow": 1, "side": 1}),
    ("day_of_week", {"dow": 2, "side": 1}),
    ("day_of_week", {"dow": 3, "side": 1}),
    ("day_of_week", {"dow": 4, "side": 1}),
    ("day_of_week", {"dow": 4, "side": -1}),  # viernes corto
]

CONFIGS_F5 = [
    ("nr_breakout", {"n": 7, "hold": 1}),
    ("nr_breakout", {"n": 7, "hold": 3}),
    ("nr_breakout", {"n": 7, "hold": 5}),
    ("nr_breakout", {"n": 4, "hold": 1}),
    ("nr_breakout", {"n": 4, "hold": 3}),
    ("nr_breakout", {"n": 14, "hold": 3}),
    ("nr_breakout", {"n": 14, "hold": 5}),
]

FNS = {"turn_of_month": turn_of_month, "day_of_week": day_of_week,
       "nr_breakout": nr_breakout}
