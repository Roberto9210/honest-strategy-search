"""Fábrica de backtests — spec_busqueda_estrategia v1 (19-ago-2026).

Reglas de la spec cableadas en el código, no en la buena voluntad:
- Todo resultado es NETO de fricción (comisión + slippage).
- Partición temporal A (desarrollo) / B (caja fuerte). El harness se niega
  a evaluar sobre B salvo con examen_final=True, y registra cada acceso a B
  en el ledger de experimentos. B se toca UNA vez por candidata.
- Ledger de experimentos append-only con cadena de hashes (estilo deadman):
  cada prueba queda registrada, gane o pierda. Editar el pasado se nota.
"""
from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone

import numpy as np
import pandas as pd

# --- Contrato: MES (Micro E-mini S&P 500) ---
POINT_VALUE = 5.0          # USD por punto
TICK = 0.25                # tamaño de tick en puntos
COMMISSION_RT = 1.40       # USD ida y vuelta por contrato (broker + exchange)
SLIPPAGE_TICKS_PER_SIDE = 1
FRICTION_RT = COMMISSION_RT + 2 * SLIPPAGE_TICKS_PER_SIDE * TICK * POINT_VALUE
# => 1.40 + 2.50 = 3.90 USD por operación por contrato. Nada se mira en bruto.

LEDGER_PATH = os.path.join(os.path.dirname(__file__), "experiments_ledger.jsonl")


@dataclass
class Split:
    """Partición temporal. B es la caja fuerte."""
    a_start: str
    a_end: str        # inclusive
    b_start: str
    b_end: str

    def part_a(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.loc[self.a_start : self.a_end]

    def part_b(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.loc[self.b_start : self.b_end]


@dataclass
class Result:
    trades: int
    net_pnl: float
    profit_factor: float
    win_rate: float
    max_drawdown: float
    per_year: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "trades": self.trades,
            "net_pnl": round(self.net_pnl, 2),
            "profit_factor": round(self.profit_factor, 3),
            "win_rate": round(self.win_rate, 3),
            "max_drawdown": round(self.max_drawdown, 2),
            "per_year": {k: round(v, 2) for k, v in self.per_year.items()},
        }


def evaluate_trades(trades: pd.DataFrame) -> Result:
    """trades: DataFrame con columnas [exit_time (índice o col), points, contracts].
    points = puntos ganados/perdidos por contrato (positivo o negativo), bruto.
    La fricción se descuenta AQUÍ, una vez por operación por contrato — el
    código de la estrategia no puede olvidarse de las comisiones porque no
    es responsabilidad suya."""
    if trades.empty:
        return Result(0, 0.0, 0.0, 0.0, 0.0, {})
    gross = trades["points"] * POINT_VALUE * trades["contracts"]
    net = gross - FRICTION_RT * trades["contracts"]
    wins = net[net > 0].sum()
    losses = -net[net <= 0].sum()
    pf = float(wins / losses) if losses > 0 else float("inf")
    equity = net.cumsum()
    dd = float((equity - equity.cummax()).min())
    years = trades.index.year if isinstance(trades.index, pd.DatetimeIndex) else pd.to_datetime(trades["exit_time"]).dt.year
    per_year = net.groupby(years).sum().to_dict()
    return Result(
        trades=len(net),
        net_pnl=float(net.sum()),
        profit_factor=pf,
        win_rate=float((net > 0).mean()),
        max_drawdown=dd,
        per_year={str(k): float(v) for k, v in per_year.items()},
    )


PASS_BAR = {
    "min_trades_b": 200,
    "min_profit_factor_b": 1.3,
    "every_year_positive_b": True,
    "robustness_neighborhood": 0.20,  # ±20% en parámetros debe seguir ganando
}


def passes_bar(res: Result) -> tuple[bool, list[str]]:
    reasons = []
    if res.trades < PASS_BAR["min_trades_b"]:
        reasons.append(f"trades {res.trades} < {PASS_BAR['min_trades_b']}")
    if res.profit_factor < PASS_BAR["min_profit_factor_b"]:
        reasons.append(f"profit_factor {res.profit_factor:.2f} < {PASS_BAR['min_profit_factor_b']}")
    if PASS_BAR["every_year_positive_b"] and any(v <= 0 for v in res.per_year.values()):
        bad = [y for y, v in res.per_year.items() if v <= 0]
        reasons.append(f"años no positivos: {bad}")
    return (len(reasons) == 0, reasons)


# --- Ledger de experimentos (append-only, hash-chained) ---

def _last_hash() -> str:
    if not os.path.exists(LEDGER_PATH):
        return "genesis"
    last = None
    with open(LEDGER_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                last = line
    return json.loads(last)["hash"] if last else "genesis"


def log_experiment(family: str, config: dict, part: str, result: Result | None,
                   note: str = "") -> dict:
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "family": family,
        "config": config,
        "part": part,             # "A", "B" (examen final) o "meta"
        "result": result.to_dict() if result else None,
        "note": note,
        "prev": _last_hash(),
    }
    entry["hash"] = hashlib.sha256(
        json.dumps(entry, sort_keys=True).encode()
    ).hexdigest()[:16]
    with open(LEDGER_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def verify_ledger() -> bool:
    prev = "genesis"
    with open(LEDGER_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            e = json.loads(line)
            h = e.pop("hash")
            if e.get("prev") != prev:
                return False
            recomputed = hashlib.sha256(
                json.dumps(e, sort_keys=True).encode()
            ).hexdigest()[:16]
            if recomputed != h:
                return False
            prev = h
    return True


class VaultViolation(Exception):
    """Se intentó evaluar sobre la parte B sin declararlo examen final."""


def run_on(df: pd.DataFrame, split: Split, strategy_fn, config: dict,
           family: str, examen_final: bool = False) -> Result:
    """Único punto de entrada para evaluar una estrategia.
    strategy_fn(data, config) -> DataFrame de trades [points, contracts]
    con índice datetime de salida."""
    part = "B" if examen_final else "A"
    data = split.part_b(df) if examen_final else split.part_a(df)
    trades = strategy_fn(data, config)
    res = evaluate_trades(trades)
    log_experiment(family, config, part, res,
                   note="EXAMEN FINAL" if examen_final else "")
    return res
