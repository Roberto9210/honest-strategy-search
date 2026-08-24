"""Fábrica de backtests — FASE 2 (spec_fase2.md, aprobada 2026-08-22/23).

Este módulo NO reemplaza a `harness.py`: lo envuelve. `harness.py` es evidencia
publicada de la Fase 1 y queda byte a byte idéntico, para que sus 57 resultados
sigan reproduciéndose exactamente como se publicaron. Todo lo que la Fase 2
agrega vive acá, en un solo archivo auditable.

Las reglas de la spec que están CABLEADAS acá, no confiadas a la memoria de
quien corre el backtest:

  §1   contador acumulado K_total = 257 congelado; línea de decisión α/K_total
       y línea de la suerte 1/(K+1) calculadas juntas, siempre.
  §3.1 barra de la parte A, incluida la caída del mejor 1% y el no solapamiento.
  §3.2 compuerta de potencia: sin 80% proyectado, `examen_final` se niega a correr.
  §3.3 caja fuerte: UN uso para todo el programa.
  §4.4 ventanas de datos por régimen, con sus exclusiones fijas. Fuera de ventana
       no se corre.
  §7.2 pre-registro obligatorio antes de conocer el resultado; la vecindad de
       robustez es gratis SOLO si ninguna celda puede adoptarse.

Nada de acá toca la red. Nada de acá ejecuta órdenes.
"""
from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from math import erfc, sqrt

import numpy as np
import pandas as pd

import harness
from harness import FRICTION_RT, POINT_VALUE, Result, evaluate_trades  # noqa: F401

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

# ---------------------------------------------------------------------------
# §1 — el contador que nunca se reinicia. Congelado al firmar.
# ---------------------------------------------------------------------------
K1 = 57                      # Fase 1: 60 líneas de ledger - 2 autotests - 1 META
K2 = 200                     # presupuesto declarado de la Fase 2
K_TOTAL = K1 + K2            # 257
ALPHA = 0.05

DECISION_P = ALPHA / K_TOTAL          # 1.9455e-4
LUCK_P = 1.0 / (K_TOTAL + 1)          # 0.0038760  (E[min p] bajo la nula global)

# Potencia: z_{α/2} + z_{1-β} con α_B = 0.05 bilateral y potencia 0.80.
Z_ALPHA_B_HALF = 1.959964
Z_POWER_80 = 0.841621
POWER_CONST = Z_ALPHA_B_HALF + Z_POWER_80    # 2.801585
MIN_POWER = 0.80

FAMILY_BUDGET = {
    "G1-nocturna": 40,
    "G2-multidia": 40,
    "G3-regimen": 30,
    "G4-bordes": 40,
    "G5-cruzado": 30,
    "G6-terceros": 20,
}
assert sum(FAMILY_BUDGET.values()) == K2, "el reparto por familia no suma K2"


def z_two_sided(p: float) -> float:
    """z tal que erfc(z/√2) = p. Bisección: sin scipy, y determinista."""
    lo, hi = 0.0, 40.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if erfc(mid / sqrt(2)) > p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


DECISION_T = z_two_sided(DECISION_P)   # 3.7260


# ---------------------------------------------------------------------------
# §4.4 — ventanas de datos por régimen. La ventana está en el código.
# ---------------------------------------------------------------------------

# Las 10 filas con OHLC incoherente del diario de Yahoo (8 son terceros viernes
# trimestrales: artefacto de roll). Fuente: qc/data_quality_yahoo.md §2.
DAILY_INCOHERENT_OHLC = (
    "2002-01-31", "2004-03-19", "2004-12-17", "2005-06-17", "2006-03-17",
    "2007-09-21", "2008-03-18", "2008-09-19", "2010-03-19", "2011-09-16",
)

# Las 11 filas con volumen cero. Precios coherentes ⇒ se CONSERVAN, salvo para
# configuraciones que usen volumen como entrada (§7.3). G1 declara el volumen
# del día previo entre sus filtros, así que esto no es hipotético.
DAILY_ZERO_VOLUME = (
    "2001-09-11", "2003-08-29", "2015-09-16", "2015-09-17", "2018-02-23",
    "2025-06-05", "2025-06-18", "2025-07-03", "2025-07-04", "2025-08-29",
    "2025-11-03",
)

# Los 31 días marcados `degraded` por Databento (metadata.get_dataset_condition).
# Fuente: qc/data_quality_es_1min_databento.md §1b.
INTRADAY_DEGRADED = (
    "2014-06-11", "2014-06-12", "2014-06-13", "2014-06-15", "2014-09-22",
    "2014-09-23", "2014-09-24", "2014-09-25", "2017-11-13", "2018-10-21",
    "2019-01-15", "2019-02-22", "2019-03-13", "2019-03-26", "2020-02-27",
    "2020-02-28", "2020-06-30", "2020-07-01", "2021-12-05", "2022-01-02",
    "2024-09-18", "2025-09-17", "2025-09-24", "2025-11-28", "2026-01-31",
    "2026-03-15", "2026-03-16", "2026-03-21", "2026-04-10", "2026-05-24",
    "2026-07-30",
)
assert len(INTRADAY_DEGRADED) == 31, "el QC publicado lista 31 días degraded"

# Único día de 2018 con barra de sesión comprimida (QC §3b).
INTRADAY_COMPRESSED = ("2018-08-05",)

# LIMITACIÓN CONOCIDA, declarada antes de que importe (G4 es la 4ª en el orden).
# Las fechas de exclusión intradía están expresadas en "día de negociación" CME
# (sesión 18:00 ET → 17:00 ET, etiquetada por la fecha en que TERMINA), que es la
# convención del QC. `Regime.slice` excluye por fecha de calendario del índice, y
# las dos no coinciden: la franja 18:00–23:59 ET de un día pertenece al día de
# negociación siguiente. Excluir por calendario dejaría entrar la mitad de cada
# día degradado y sacaría medio día sano.
#
# Un chequeo aproximado no es un chequeo. Hasta que el mapeo esté implementado y
# probado, el régimen intradía está BLOQUEADO: G4 no corre. No bloquea nada hoy
# —G1, G2, G3 son diarias y van antes— y evita que la primera corrida de G4 use
# una exclusión que se ve bien y no lo es.
INTRADAY_TRADING_DAY_MAPPING_READY = False


@dataclass(frozen=True)
class Regime:
    """Una ventana de datos declarada en §4.4. Congelada al firmar."""
    name: str
    series: str            # archivo bajo data/
    a_start: str
    a_end: str
    b_start: str
    b_end: str
    excluded: tuple        # fechas fuera, siempre
    excluded_if_volume: tuple = ()   # fuera solo si la config usa volumen
    families: tuple = ()

    def bounds(self, part: str) -> tuple:
        return (self.a_start, self.a_end) if part == "A" else (self.b_start, self.b_end)

    def slice(self, df: pd.DataFrame, part: str, uses_volume: bool = False) -> pd.DataFrame:
        start, end = self.bounds(part)
        out = df.loc[start:end]
        drop = set(pd.to_datetime(self.excluded).normalize())
        if uses_volume:
            drop |= set(pd.to_datetime(self.excluded_if_volume).normalize())
        if drop:
            out = out[~out.index.normalize().isin(drop)]
        return out


WINDOWS = {
    "diario": Regime(
        name="diario",
        series="es_daily.csv",
        a_start="2000-09-18", a_end="2019-12-31",
        b_start="2020-01-01", b_end="2026-08-19",
        excluded=DAILY_INCOHERENT_OHLC,
        excluded_if_volume=DAILY_ZERO_VOLUME,
        families=("G1-nocturna", "G2-multidia", "G3-regimen", "G5-cruzado"),
    ),
    "intradia": Regime(
        name="intradia",
        series="es_1min_databento.csv",
        a_start="2016-01-01", a_end="2019-12-31",
        b_start="2020-01-01", b_end="2026-08-18",
        excluded=INTRADAY_DEGRADED + INTRADAY_COMPRESSED,
        families=("G4-bordes",),
    ),
}

FAMILY_REGIME = {f: r.name for r in WINDOWS.values() for f in r.families}


class SpecViolation(Exception):
    """Se intentó hacer algo que la spec prohíbe. Fail-closed: no corre."""


class PreregistrationMissing(SpecViolation):
    pass


class WindowViolation(SpecViolation):
    pass


class BudgetExhausted(SpecViolation):
    pass


class PowerGateNotCleared(SpecViolation):
    pass


class VaultAlreadyUsed(SpecViolation):
    pass


# ---------------------------------------------------------------------------
# Ledger — misma cadena de hashes que la Fase 1, continuada sin cortes.
# ---------------------------------------------------------------------------
LEDGER_PATH = harness.LEDGER_PATH

# La línea part="B" de la Fase 1 es el autotest sintético del harness (README §4):
# no evaluó precios reales, así que no cuenta como uso de la caja fuerte.
VAULT_EXEMPT_FAMILIES = ("autotest",)


def set_ledger(path: str) -> None:
    """Apunta ESTE módulo y `harness` al mismo ledger. Solo para tests."""
    global LEDGER_PATH
    LEDGER_PATH = path
    harness.LEDGER_PATH = path


def read_ledger() -> list:
    if not os.path.exists(LEDGER_PATH):
        return []
    with open(LEDGER_PATH, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def _last_hash() -> str:
    rows = read_ledger()
    return rows[-1]["hash"] if rows else "genesis"


def _append(body: dict) -> dict:
    entry = dict(body)
    entry["ts"] = datetime.now(timezone.utc).isoformat()
    entry["prev"] = _last_hash()
    entry["hash"] = hashlib.sha256(
        json.dumps(entry, sort_keys=True).encode()
    ).hexdigest()[:16]
    with open(LEDGER_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def verify_ledger() -> bool:
    """Misma verificación que la Fase 1, sobre el archivo combinado."""
    prev = "genesis"
    for e in read_ledger():
        e = dict(e)
        h = e.pop("hash")
        if e.get("prev") != prev:
            return False
        if hashlib.sha256(json.dumps(e, sort_keys=True).encode()).hexdigest()[:16] != h:
            return False
        prev = h
    return True


def _cfg_key(family: str, config: dict) -> str:
    return family + "|" + json.dumps(config, sort_keys=True)


# ---------------------------------------------------------------------------
# §1 / §2 — contador de presupuesto
# ---------------------------------------------------------------------------

def budget_used(family: str | None = None) -> int:
    """Cartuchos gastados. Un pre-registro gasta en el momento de escribirse
    (no cuando se corre): reservar barato sería una forma de no contar. Las
    violaciones de spec gastan igual (§7.2)."""
    n = 0
    for e in read_ledger():
        if e.get("phase") != 2:
            continue
        if e.get("kind") not in ("PREREGISTRO", "VIOLACION"):
            continue
        if family is not None and e.get("family") != family:
            continue
        n += 1
    return n


def budget_report() -> dict:
    return {
        "K1": K1, "K2": K2, "K_total": K_TOTAL,
        "usado": budget_used(),
        "restante": K2 - budget_used(),
        "por_familia": {f: {"presupuesto": b, "usado": budget_used(f)}
                        for f, b in FAMILY_BUDGET.items()},
        "linea_decision_p": DECISION_P,
        "linea_decision_t": DECISION_T,
        "linea_suerte_p": LUCK_P,
    }


# ---------------------------------------------------------------------------
# §9.2 — el estadístico y su diagnóstico, automáticos
# ---------------------------------------------------------------------------

def net_per_trade(trades: pd.DataFrame) -> pd.Series:
    """Neto por operación, con la fricción de la Fase 1 adentro. Idéntico al
    cálculo de botc_f4_reverify.py — los costos nunca quedan al margen."""
    gross = trades["points"] * POINT_VALUE * trades["contracts"]
    return gross - FRICTION_RT * trades["contracts"]


def stat_test(trades: pd.DataFrame, drop_best_pct: float = 0.0) -> dict:
    """t, p crudo, línea de decisión y línea de la suerte, juntos y siempre.

    drop_best_pct: recorta el mejor X% de las operaciones antes de calcular
    (§3.1, robustez a valores extremos)."""
    net = net_per_trade(trades)
    if drop_best_pct > 0 and len(net) > 0:
        k = int(np.ceil(len(net) * drop_best_pct))
        if k > 0:
            net = net.sort_values(ascending=False).iloc[k:]
    n = int(len(net))
    if n < 2:
        return {"n": n, "media": 0.0, "desvio": 0.0, "t": 0.0, "p_crudo": 1.0,
                "delta": 0.0, "linea_decision_p": DECISION_P,
                "linea_decision_t": DECISION_T, "linea_suerte_p": LUCK_P,
                "supera_linea_decision": False,
                "supera_linea_suerte": False}
    mean = float(net.mean())
    sd = float(net.std(ddof=1))
    t = mean / (sd / sqrt(n)) if sd > 0 else 0.0
    p_raw = erfc(abs(t) / sqrt(2))
    return {
        "n": n,
        "media": mean,
        "desvio": sd,
        "t": t,
        "p_crudo": p_raw,
        "delta": (mean / sd) if sd > 0 else 0.0,
        "linea_decision_p": DECISION_P,
        "linea_decision_t": DECISION_T,
        "linea_suerte_p": LUCK_P,
        # La decisión: p ≤ α/K_total, y el efecto tiene que ser POSITIVO.
        "supera_linea_decision": bool(p_raw <= DECISION_P and mean > 0),
        # El espejo: ¿es siquiera mejor que el mejor tiro del azar en K intentos?
        "supera_linea_suerte": bool(p_raw <= LUCK_P and mean > 0),
    }


# ---------------------------------------------------------------------------
# §3.2 — compuerta de potencia
# ---------------------------------------------------------------------------

def project_n_b(n_a: int, sessions_a: int, sessions_b: int) -> int:
    """Operaciones proyectadas en la parte B, a partir de la FRECUENCIA medida
    en A y del CALENDARIO de B. No lee un solo precio de B."""
    if sessions_a <= 0:
        return 0
    return int(round(n_a * sessions_b / sessions_a))


def power_check(delta_hat: float, n_b_proyectado: int) -> dict:
    """§3.2. n_B ≥ (z_{α/2}+z_{1-β})² / δ̂²  ⟺  δ̂·√n_B ≥ 2.801585."""
    d = abs(float(delta_hat))
    if d <= 0 or n_b_proyectado <= 0:
        return {"delta_hat": d, "n_b_proyectado": int(n_b_proyectado),
                "n_b_necesario": None, "potencia": 0.0, "aprueba": False,
                "min_power": MIN_POWER}
    needed = (POWER_CONST / d) ** 2
    ncp = d * sqrt(n_b_proyectado)
    # potencia bilateral, ignorando la cola contraria (idéntico a botc_potencia_f4 §4)
    power = 0.5 * erfc(-(ncp - Z_ALPHA_B_HALF) / sqrt(2))
    return {
        "delta_hat": d,
        "n_b_proyectado": int(n_b_proyectado),
        "n_b_necesario": int(np.ceil(needed)),
        "t_esperado_en_B": ncp,
        "potencia": float(power),
        "min_power": MIN_POWER,
        "aprueba": bool(power >= MIN_POWER),
    }


def log_power_check(family: str, config: dict, delta_hat: float,
                    n_a: int, n_b_proyectado: int, note: str = "") -> dict:
    """Deja el cálculo de potencia en el ledger. `run_on(examen_final=True)`
    exige encontrar acá uno APROBADO para esa candidata (§9.3)."""
    pc = power_check(delta_hat, n_b_proyectado)
    pc["n_a"] = int(n_a)
    return _append({
        "phase": 2, "kind": "POTENCIA", "family": family, "config": config,
        "part": "meta", "result": None, "power": pc,
        "note": note or ("APROBADA" if pc["aprueba"] else
                         "ARCHIVADA: no decidible con los datos existentes"),
    })


def approved_power_check(family: str, config: dict) -> dict | None:
    key = _cfg_key(family, config)
    found = None
    for e in read_ledger():
        if e.get("kind") == "POTENCIA" and _cfg_key(e["family"], e["config"]) == key:
            if e.get("power", {}).get("aprueba"):
                found = e
    return found


# ---------------------------------------------------------------------------
# §3 — la barra
# ---------------------------------------------------------------------------
PASS_BAR_F2 = {
    "min_trades_a": 100,
    "min_t_a": DECISION_T,                 # 3.726; §3.2 puede exigir más
    "min_profit_factor_a": 1.3,
    "drop_best_pct": 0.01,                 # y con el mejor 1% afuera, igual
    "robustness_neighborhood": 0.20,
    "robustness_median_pf": 1.15,
    # examen final (§3.3)
    "max_p_b": 0.05,
    "min_profit_factor_b": 1.3,
    "min_degradacion": 0.50,
    "min_years_positive_b": 5,
    "years_in_b": 7,
}


def required_t_a(n_a: int, n_b_proyectado: int) -> float:
    """§3.2: la barra efectiva en A es el máximo entre la línea de decisión y
    lo que hace falta para que el examen final pueda responder."""
    if n_b_proyectado <= 0:
        return float("inf")
    return max(DECISION_T, POWER_CONST * sqrt(n_a / n_b_proyectado))


def passes_bar_a(trades: pd.DataFrame, res: Result, n_b_proyectado: int,
                 neighborhood: list | None = None) -> tuple:
    """Compuerta 1 + compuerta 2. Devuelve (pasa, razones_de_falla, detalle)."""
    reasons = []
    st = stat_test(trades)
    st_drop = stat_test(trades, drop_best_pct=PASS_BAR_F2["drop_best_pct"])
    need_t = required_t_a(st["n"], n_b_proyectado)
    pc = power_check(st["delta"], n_b_proyectado)

    if res.trades < PASS_BAR_F2["min_trades_a"]:
        reasons.append(f"operaciones {res.trades} < {PASS_BAR_F2['min_trades_a']}")
    if not (st["t"] >= need_t):
        reasons.append(f"t {st['t']:.3f} < {need_t:.3f} exigido "
                       f"(decision {DECISION_T:.3f}, potencia {POWER_CONST * sqrt(max(st['n'],1) / max(n_b_proyectado,1)):.3f})")
    if not (st_drop["t"] >= need_t):
        reasons.append(f"t sin el mejor 1% {st_drop['t']:.3f} < {need_t:.3f}")
    if res.profit_factor < PASS_BAR_F2["min_profit_factor_a"]:
        reasons.append(f"PF {res.profit_factor:.3f} < {PASS_BAR_F2['min_profit_factor_a']}")
    if neighborhood:
        pfs = sorted(neighborhood)
        if any(pf < 1.0 for pf in pfs):
            reasons.append(f"vecindad con celdas que pierden plata: {[round(p,3) for p in pfs if p < 1.0]}")
        med = float(np.median(pfs))
        if med < PASS_BAR_F2["robustness_median_pf"]:
            reasons.append(f"mediana de la vecindad {med:.3f} < {PASS_BAR_F2['robustness_median_pf']}")
    else:
        reasons.append("vecindad de robustez no evaluada")
    if not pc["aprueba"]:
        reasons.append(f"potencia proyectada en B {pc['potencia']:.1%} < {MIN_POWER:.0%} "
                       f"(harian falta {pc['n_b_necesario']} operaciones, se proyectan {pc['n_b_proyectado']}) "
                       "=> ARCHIVAR, no abrir la caja fuerte")
    return (len(reasons) == 0, reasons, {"stat": st, "stat_sin_mejor_1pct": st_drop,
                                         "t_exigido": need_t, "power": pc})


# ---------------------------------------------------------------------------
# §3.3 — el registro año por año, obligatorio pase o no pase
# ---------------------------------------------------------------------------

def report_per_year(trades: pd.DataFrame) -> pd.DataFrame:
    """Operaciones, neto, PF y drawdown por año calendario. Se publica completo
    para toda candidata que llegue al examen — pase o no pase (§3.3), para que
    quien prefiera el criterio 7/7 lo aplique con nuestros propios números."""
    if trades.empty:
        return pd.DataFrame(columns=["operaciones", "neto", "profit_factor",
                                     "drawdown", "positivo"])
    net = net_per_trade(trades)
    years = (trades.index.year if isinstance(trades.index, pd.DatetimeIndex)
             else pd.to_datetime(trades["exit_time"]).dt.year)
    rows = {}
    for y, g in net.groupby(years):
        wins = float(g[g > 0].sum())
        losses = float(-g[g <= 0].sum())
        eq = g.cumsum()
        rows[str(y)] = {
            "operaciones": int(len(g)),
            "neto": round(float(g.sum()), 2),
            "profit_factor": (round(wins / losses, 3) if losses > 0 else float("inf")),
            "drawdown": round(float((eq - eq.cummax()).min()), 2),
            "positivo": bool(g.sum() > 0),
        }
    out = pd.DataFrame(rows).T
    out.index.name = "anio"
    return out


def years_positive(trades: pd.DataFrame) -> tuple:
    r = report_per_year(trades)
    if r.empty:
        return (0, 0)
    return (int(r["positivo"].sum()), int(len(r)))


# ---------------------------------------------------------------------------
# §7.2 — pre-registro. Al ledger ANTES de conocer el resultado.
# ---------------------------------------------------------------------------

def _robustness_cells_claimed() -> dict:
    """{clave_de_config: hash_del_prerregistro} de toda celda declarada como
    vecindad de robustez. Adoptar una de ellas cobra las 9 (§7.2)."""
    out = {}
    for e in read_ledger():
        if e.get("kind") != "PREREGISTRO":
            continue
        for cell in e.get("robustness_cells", []) or []:
            out[_cfg_key(e["family"], cell)] = e["hash"]
    return out


def preregister(family: str, config: dict, hypothesis: str,
                robustness_cells: list | None = None,
                uses_volume: bool = False,
                adopcion_de_vecindad: bool = False) -> dict:
    """Escribe la configuración en el ledger ANTES de correrla. Gasta un
    cartucho en el momento de escribirse.

    `hypothesis`: el mecanismo, en una línea. Obligatorio: una configuración sin
    hipótesis es un barrido con otro nombre.
    `robustness_cells`: vecindad declarada de antemano. Es gratis SOLO porque
    ninguna de sus celdas puede adoptarse como candidata.
    """
    if family not in FAMILY_BUDGET:
        raise SpecViolation(f"familia no declarada en la spec: {family!r}")
    if not hypothesis or not hypothesis.strip():
        raise SpecViolation("pre-registro sin hipótesis: prohibido (§7.2)")

    # ¿Es esta configuración una celda de la vecindad de otro pre-registro?
    claimed = _robustness_cells_claimed()
    owner = claimed.get(_cfg_key(family, config))
    charged_cells = []
    if owner is not None:
        if not adopcion_de_vecindad:
            raise SpecViolation(
                f"la config {config} ya fue declarada como celda de robustez del "
                f"pre-registro {owner}. Adoptarla es SELECCIÓN: hay que pedirlo "
                "explícito con adopcion_de_vecindad=True, y entonces se cobran "
                "todas las celdas de esa vecindad (§7.2)."
            )
        for e in read_ledger():
            if e.get("hash") == owner:
                charged_cells = list(e.get("robustness_cells", []) or [])

    n_extra = len(charged_cells)
    if budget_used() + 1 + n_extra > K2:
        raise BudgetExhausted(
            f"presupuesto de Fase 2 agotado: usados {budget_used()} de {K2}")
    if budget_used(family) + 1 + n_extra > FAMILY_BUDGET[family]:
        raise BudgetExhausted(
            f"presupuesto de {family} agotado: usados {budget_used(family)} "
            f"de {FAMILY_BUDGET[family]} (no se transfiere de otra familia, §2)")

    entries = []
    if charged_cells:
        # La adopción cobra la vecindad entera, celda por celda, visible.
        for cell in charged_cells:
            entries.append(_append({
                "phase": 2, "kind": "PREREGISTRO", "family": family,
                "config": cell, "part": "A", "result": None,
                "hypothesis": f"celda de vecindad cobrada por adopción de {config}",
                "charged_by_adoption_of": config, "prereg_owner": owner,
                "note": "ADOPCION DE VECINDAD: la celda deja de ser gratis (§7.2)",
            }))

    entry = _append({
        "phase": 2, "kind": "PREREGISTRO", "family": family, "config": config,
        "part": "A", "result": None,
        "hypothesis": hypothesis.strip(),
        "regime": FAMILY_REGIME.get(family),
        "robustness_cells": list(robustness_cells or []),
        "uses_volume": bool(uses_volume),
        "budget_after": budget_used() + 1,
        "note": "PRE-REGISTRADA, sin correr",
    })
    entries.append(entry)
    return entry


def open_preregistration(family: str, config: dict) -> dict | None:
    """Pre-registro sin resultado todavía. Uno por configuración."""
    key = _cfg_key(family, config)
    prereg, consumed = None, set()
    for e in read_ledger():
        if e.get("phase") != 2:
            continue
        if e.get("kind") == "PREREGISTRO" and _cfg_key(e["family"], e["config"]) == key:
            prereg = e
        if e.get("kind") == "RESULTADO" and e.get("prereg"):
            consumed.add(e["prereg"])
    if prereg is None or prereg["hash"] in consumed:
        return None
    return prereg


def log_spec_violation(family: str, config: dict, result: Result | None,
                       motivo: str) -> dict:
    """Para lo que el código no puede impedir: alguien corrió una estrategia sin
    pasar por `run_on`. Se registra CON su resultado y gasta cartucho igual."""
    return _append({
        "phase": 2, "kind": "VIOLACION", "family": family, "config": config,
        "part": "A", "result": result.to_dict() if result else None,
        "spec_violation": motivo,
        "note": "VIOLACION DE SPEC: consume presupuesto igual (§7.2)",
    })


# ---------------------------------------------------------------------------
# §3.3 / §7.1 — la caja fuerte, un solo uso para todo el programa
# ---------------------------------------------------------------------------

def vault_uses() -> list:
    """Usos REALES de la parte B. La línea part='B' de la Fase 1 es el autotest
    sintético del harness (README §4) y no cuenta: no evaluó precios reales."""
    return [e for e in read_ledger()
            if e.get("part") == "B" and e.get("family") not in VAULT_EXEMPT_FAMILIES]


# ---------------------------------------------------------------------------
# Punto de entrada único
# ---------------------------------------------------------------------------

def run_on(df: pd.DataFrame, family: str, config: dict, strategy_fn,
           examen_final: bool = False, n_b_proyectado: int | None = None) -> Result:
    """Único camino para evaluar una estrategia en la Fase 2.

    Se niega a correr —antes de tocar la estrategia— si:
      · no hay pre-registro abierto para (family, config)            §7.2
      · la familia no tiene régimen/ventana declarados               §4.4
      · es examen final y la caja fuerte ya se usó                   §3.3
      · es examen final sin power_check APROBADO en el ledger        §3.2
    """
    prereg = open_preregistration(family, config)
    if prereg is None:
        raise PreregistrationMissing(
            f"sin pre-registro abierto para {family} {config}. La spec exige que "
            "la configuración esté en el ledger ANTES de conocer su resultado "
            "(§7.2). Si ya se corrió por fuera, registralo con log_spec_violation()."
        )

    regime_name = FAMILY_REGIME.get(family)
    if regime_name is None:
        raise WindowViolation(f"familia {family!r} sin régimen declarado en §4.4")
    regime = WINDOWS[regime_name]

    if regime.name == "intradia" and not INTRADAY_TRADING_DAY_MAPPING_READY:
        raise WindowViolation(
            "régimen intradía bloqueado: la exclusión de los 31 días `degraded` "
            "está expresada en día de negociación CME y `Regime.slice` corta por "
            "fecha de calendario. Hasta que el mapeo esté implementado y probado, "
            "G4 no corre (§4.4). Ver INTRADAY_TRADING_DAY_MAPPING_READY."
        )

    if examen_final:
        used = vault_uses()
        if used:
            raise VaultAlreadyUsed(
                f"la caja fuerte ya se usó ({len(used)} vez/veces): un solo uso "
                "para TODO el programa (§3.3). No hay segundo examen."
            )
        pc = approved_power_check(family, config)
        if pc is None:
            raise PowerGateNotCleared(
                "no hay power_check APROBADO en el ledger para esta candidata. "
                "Sin 80% de potencia proyectada el examen no puede responder la "
                "pregunta, y abrirlo quema un recurso de un solo uso (§3.2)."
            )

    part = "B" if examen_final else "A"
    data = regime.slice(df, part, uses_volume=bool(prereg.get("uses_volume")))
    if data.empty:
        raise WindowViolation(
            f"la ventana {regime.name}/{part} "
            f"({regime.bounds(part)[0]} → {regime.bounds(part)[1]}) no deja datos")

    lo, hi = regime.bounds(part)
    if data.index.min() < pd.Timestamp(lo) or data.index.max() > pd.Timestamp(hi):
        raise WindowViolation(
            f"datos fuera de la ventana declarada para {regime.name}/{part}")

    trades = strategy_fn(data, config)
    res = evaluate_trades(trades)

    body = {
        "phase": 2, "kind": "RESULTADO", "family": family, "config": config,
        "part": part, "result": res.to_dict(), "prereg": prereg["hash"],
        "regime": regime.name,
        "ventana": {"desde": lo, "hasta": hi},
        "stat": {k: v for k, v in stat_test(trades).items()},
        "note": "EXAMEN FINAL" if examen_final else "",
    }
    if part == "B" or n_b_proyectado is not None:
        body["per_year"] = report_per_year(trades).to_dict(orient="index")
    _append(body)
    return res


# ---------------------------------------------------------------------------
# §9.5 — apertura de la fase: la firma
# ---------------------------------------------------------------------------
DATA_FILES_TO_FREEZE = ("es_daily.csv", "es_1min_databento.csv", "spy_daily.csv")


def sha256_file(path: str, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def freeze_data_hashes(data_dir: str | None = None) -> dict:
    data_dir = data_dir or os.path.join(REPO, "data")
    out = {}
    for name in DATA_FILES_TO_FREEZE:
        p = os.path.join(data_dir, name)
        out[name] = {"sha256": sha256_file(p), "bytes": os.path.getsize(p)} \
            if os.path.exists(p) else {"sha256": None, "bytes": None,
                                       "nota": "AUSENTE"}
    return out


def open_phase2(margen_nocturno_mes: dict | None = None,
                data_dir: str | None = None) -> dict:
    """Escribe la entrada meta que abre la Fase 2 (§9.5). Es la firma.

    `margen_nocturno_mes`: {"valor_usd": ..., "fuente": ..., "leido_el": ...}.
    Puede ir en None — la fase abre igual, pero G1 no corre hasta que esté (§7.3).
    """
    hashes = freeze_data_hashes(data_dir)
    return _append({
        "phase": 2, "kind": "APERTURA_FASE2", "family": "META", "config":
            {"evento": "APERTURA FASE 2"},
        "part": "meta", "result": None,
        "K1": K1, "K2": K2, "K_total": K_TOTAL, "alpha": ALPHA,
        "linea_decision_p": DECISION_P, "linea_decision_t": round(DECISION_T, 4),
        "linea_suerte_p": LUCK_P,
        "presupuesto_por_familia": FAMILY_BUDGET,
        "ventanas": {k: {"a": [v.a_start, v.a_end], "b": [v.b_start, v.b_end],
                         "serie": v.series, "excluidas": len(v.excluded)}
                     for k, v in WINDOWS.items()},
        "data_sha256": hashes,
        "margen_nocturno_mes": margen_nocturno_mes,
        "note": ("Apertura de Fase 2 segun spec_fase2.md. Caja fuerte 2020-2026 "
                 "SELLADA, un solo uso. K_total=257 congelado. " +
                 ("G1 HABILITADA." if margen_nocturno_mes else
                  "G1 BLOQUEADA: falta el margen nocturno de MES (§7.3).")),
    })


def phase2_is_open() -> bool:
    return any(e.get("kind") == "APERTURA_FASE2" for e in read_ledger())


def g1_enabled() -> bool:
    """G1 no corre sin el margen nocturno declarado con fecha y fuente (§7.3)."""
    for e in read_ledger():
        if e.get("kind") == "APERTURA_FASE2":
            m = e.get("margen_nocturno_mes")
            if m and m.get("valor_usd") and m.get("fuente") and m.get("leido_el"):
                return True
    return False
