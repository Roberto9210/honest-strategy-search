"""Familia G2 — Momento y reversión multi-día (spec_fase2.md §4.2).

Barras diarias. Mismo modelo anti-lookahead que las familias de la Fase 1:
**señal al cierre de t ⇒ ejecución en la apertura de t+1**. Nada mira un precio
que no existía todavía cuando la regla decidió.

Posiciones **NO solapadas** (§3.1): mientras haya una posición abierta no se
evalúan señales nuevas. No es burocracia — operaciones solapadas están
correlacionadas entre sí, el desvío se subestima y el `t` se infla.

La fricción NO se descuenta acá: la aplica `harness.evaluate_trades`, una vez
por operación por contrato, para que ninguna estrategia pueda olvidarse.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def reversion_k_dias(df: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    """Tras `k` cierres consecutivos en contra, tomar el otro lado.

    cfg:
      k     : cierres consecutivos que disparan la señal (cierre < cierre previo
              para `side` = 1; cierre > cierre previo para `side` = -1).
      hold  : sesiones de tenencia. Entra en la apertura de t+1 y sale en la
              apertura de t+1+hold.
      side  : 1 = largo tras caídas (reversión), -1 = corto tras subidas.

    Devuelve [points, contracts] con índice datetime de SALIDA, que es lo que
    `harness.evaluate_trades` espera.
    """
    k = int(cfg["k"])
    hold = int(cfg["hold"])
    side = int(cfg.get("side", 1))
    if k < 1 or hold < 1 or side not in (1, -1):
        raise ValueError(f"config inválida para reversion_k_dias: {cfg}")

    closes = df["close"].to_numpy(dtype=float)
    opens = df["open"].to_numpy(dtype=float)
    n = len(df)

    # contra[t] = el cierre de t se movió en contra del lado que vamos a tomar
    contra = np.zeros(n, dtype=bool)
    if n > 1:
        contra[1:] = ((closes[1:] < closes[:-1]) if side == 1
                      else (closes[1:] > closes[:-1]))

    trades = []
    i = k                      # primer t con k barras previas disponibles
    while i < n - 1:
        if contra[i - k + 1:i + 1].all():
            entry_i = i + 1                 # apertura de t+1
            exit_i = entry_i + hold
            if exit_i >= n:
                break                       # sin barra de salida: no se opera
            pts = (opens[exit_i] - opens[entry_i]) * side
            trades.append((df.index[exit_i], pts))
            i = exit_i                      # no solapamiento: recién ahí se vuelve a mirar
        else:
            i += 1

    if not trades:
        return pd.DataFrame(columns=["points", "contracts"])
    out = pd.DataFrame(trades, columns=["exit_time", "points"]).set_index("exit_time")
    out["contracts"] = 1
    return out
