"""Motor intradía — Familias 1 (ruptura de apertura) y 3 (reversión a la media).

Convenciones:
- Barras OHLCV intradía con timestamp tz-aware (se convierte a ET).
- Sesión regular (RTH): 09:30–16:00 ET. Todo se liquida al final de la sesión
  (compatible con reglas de prop firms: nada queda abierto de noche).
- Anti-lookahead: los niveles se fijan con barras COMPLETAS anteriores a la
  entrada; los fills se aproximan al nivel si la barra lo cruza, o a la
  apertura de la barra si abre gapeada más allá (el slippage del harness
  cubre parte del optimismo; anotado en el ledger).
- Devuelve trades [points, contracts] con índice = timestamp de salida,
  para el mismo evaluate_trades del harness (fricción $3.90/op incluida allí).
"""
import numpy as np
import pandas as pd

ET = "America/New_York"


def load_intraday(path: str, ts_col: str = "datetime") -> pd.DataFrame:
    df = pd.read_csv(path)
    df[ts_col] = pd.to_datetime(df[ts_col], utc=True).dt.tz_convert(ET)
    df = df.set_index(ts_col).sort_index()
    return df[["open", "high", "low", "close", "volume"]]


def rth(df: pd.DataFrame) -> pd.DataFrame:
    return df.between_time("09:30", "15:59")


def _fill_cross(bar_open, bar_high, bar_low, level, side):
    """side=+1: stop-buy en level; side=-1: stop-sell. None si no cruza."""
    if side == 1:
        if bar_open >= level:
            return bar_open
        if bar_high >= level:
            return level
    else:
        if bar_open <= level:
            return bar_open
        if bar_low <= level:
            return level
    return None


def orb(df_rth: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    """Familia 1: ruptura del rango de los primeros `range_min` minutos.
    Stop: lado opuesto del rango (o `stop_pts` fijo). Salida: fin de sesión
    o al tocar `target_r` veces el riesgo. Una operación por día como máximo
    (la primera ruptura que ocurra)."""
    range_min = cfg["range_min"]
    target_r = cfg.get("target_r")          # None = solo salida fin de día
    allow_short = cfg.get("short", True)
    trades = []
    for day, g in df_rth.groupby(df_rth.index.date):
        if len(g) < range_min // _bar_minutes(g) + 5:
            continue
        n_bars = max(1, range_min // _bar_minutes(g))
        rng = g.iloc[:n_bars]
        hi, lo = rng["high"].max(), rng["low"].min()
        risk = hi - lo
        if risk <= 0:
            continue
        rest = g.iloc[n_bars:]
        pos = 0
        entry = stop = target = None
        exit_price = None
        exit_ts = None
        for ts, bar in rest.iterrows():
            if pos == 0:
                f = _fill_cross(bar["open"], bar["high"], bar["low"], hi, 1)
                if f is not None:
                    pos, entry = 1, f
                    stop = lo
                    target = entry + target_r * risk if target_r else None
                elif allow_short:
                    f = _fill_cross(bar["open"], bar["high"], bar["low"], lo, -1)
                    if f is not None:
                        pos, entry = -1, f
                        stop = hi
                        target = entry - target_r * risk if target_r else None
                if pos == 0:
                    continue
                # la misma barra puede tocar el stop después de entrar:
                # supuesto conservador: si la barra toca el stop, se ejecuta
                if (pos == 1 and bar["low"] <= stop) or (pos == -1 and bar["high"] >= stop):
                    exit_price, exit_ts = stop, ts
                    break
                continue
            # gestión de posición abierta (barras siguientes)
            if pos == 1:
                if bar["low"] <= stop:                     # stop primero: conservador
                    exit_price, exit_ts = stop, ts; break
                if target and bar["high"] >= target:
                    exit_price, exit_ts = target, ts; break
            else:
                if bar["high"] >= stop:
                    exit_price, exit_ts = stop, ts; break
                if target and bar["low"] <= target:
                    exit_price, exit_ts = target, ts; break
        if pos != 0:
            if exit_price is None:                          # fin de sesión
                exit_price, exit_ts = g["close"].iloc[-1], g.index[-1]
            trades.append((exit_ts, (exit_price - entry) * pos))
    return _to_frame(trades)


def vwap_reversion(df_rth: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    """Familia 3: desviación extrema respecto del VWAP de la sesión.
    Si el precio se aleja `k` desviaciones (std de los retornos de la sesión
    acumulada) por debajo del VWAP => largo hacia el VWAP; simétrico corto.
    Salida: al tocar el VWAP, al stop `k_stop` desviaciones más allá, o fin
    de sesión. Máx. 1 operación por día."""
    k = cfg["k"]
    k_stop = cfg.get("k_stop", k)
    allow_short = cfg.get("short", True)
    warm = cfg.get("warmup_bars", 30)
    trades = []
    for day, g in df_rth.groupby(df_rth.index.date):
        if len(g) < warm + 10:
            continue
        tp = (g["high"] + g["low"] + g["close"]) / 3
        cum_v = g["volume"].cumsum().replace(0, np.nan)
        vwap = (tp * g["volume"]).cumsum() / cum_v
        dev = (g["close"] - vwap)
        sigma = dev.expanding().std()
        pos = 0
        entry = stop = None
        exit_price = exit_ts = None
        for i in range(warm, len(g)):
            ts = g.index[i]
            bar = g.iloc[i]
            v, s = vwap.iloc[i - 1], sigma.iloc[i - 1]   # niveles con datos previos
            if not np.isfinite(s) or s <= 0:
                continue
            if pos == 0:
                if bar["close"] < v - k * s:
                    pos, entry = 1, bar["close"]
                    stop = entry - k_stop * s
                elif allow_short and bar["close"] > v + k * s:
                    pos, entry = -1, bar["close"]
                    stop = entry + k_stop * s
                continue
            if pos == 1:
                if bar["low"] <= stop:
                    exit_price, exit_ts = stop, ts; break
                if bar["high"] >= v:
                    exit_price, exit_ts = v, ts; break
            else:
                if bar["high"] >= stop:
                    exit_price, exit_ts = stop, ts; break
                if bar["low"] <= v:
                    exit_price, exit_ts = v, ts; break
        if pos != 0:
            if exit_price is None:
                exit_price, exit_ts = g["close"].iloc[-1], g.index[-1]
            trades.append((exit_ts, (exit_price - entry) * pos))
    return _to_frame(trades)


def _bar_minutes(g: pd.DataFrame) -> int:
    if len(g) < 2:
        return 1
    return max(1, int((g.index[1] - g.index[0]).total_seconds() // 60))


def _to_frame(trades) -> pd.DataFrame:
    if not trades:
        return pd.DataFrame(columns=["points", "contracts"])
    out = pd.DataFrame(trades, columns=["exit_time", "points"]).set_index("exit_time")
    out["contracts"] = 1
    return out


CONFIGS_F1 = [
    ("orb", {"range_min": 30, "target_r": None, "short": True}),
    ("orb", {"range_min": 30, "target_r": None, "short": False}),
    ("orb", {"range_min": 30, "target_r": 2.0,  "short": True}),
    ("orb", {"range_min": 30, "target_r": 2.0,  "short": False}),
    ("orb", {"range_min": 15, "target_r": None, "short": True}),
    ("orb", {"range_min": 15, "target_r": None, "short": False}),
    ("orb", {"range_min": 15, "target_r": 2.0,  "short": True}),
    ("orb", {"range_min": 15, "target_r": 1.5,  "short": True}),
    ("orb", {"range_min": 60, "target_r": None, "short": True}),
    ("orb", {"range_min": 60, "target_r": 2.0,  "short": True}),
]

CONFIGS_F3 = [
    ("vwap_reversion", {"k": 2.0, "k_stop": 2.0, "short": True}),
    ("vwap_reversion", {"k": 2.0, "k_stop": 2.0, "short": False}),
    ("vwap_reversion", {"k": 3.0, "k_stop": 2.0, "short": True}),
    ("vwap_reversion", {"k": 3.0, "k_stop": 2.0, "short": False}),
    ("vwap_reversion", {"k": 2.5, "k_stop": 1.5, "short": True}),
    ("vwap_reversion", {"k": 1.5, "k_stop": 3.0, "short": True}),
]

FNS = {"orb": orb, "vwap_reversion": vwap_reversion}
