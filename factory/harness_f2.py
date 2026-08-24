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
    if entry.get("phase") == 2 and "rules_digest" not in entry:
        try:
            entry["rules_digest"] = rules_digest()
        except Exception:      # noqa: BLE001
            entry["rules_digest"] = None
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

# Entradas que gastan cartucho.
#   PREREGISTRO — una configuración anunciada antes de correrla.
#   CARTUCHO    — celda de vecindad cobrada por adopción (§7.2). No espera
#                 corrida: ya se pagó, no queda "abierta".
#   VIOLACION   — corrida por fuera de run_on. Gasta SOLO si no venía de un
#                 pre-registro que ya había pagado.
BUDGET_KINDS = ("PREREGISTRO", "CARTUCHO", "VIOLACION")


def budget_used(family: str | None = None) -> int:
    """Cartuchos gastados. Un pre-registro gasta en el momento de escribirse
    (no cuando se corre): reservar barato sería una forma de no contar. Las
    violaciones de spec gastan igual (§7.2)."""
    n = 0
    for e in read_ledger():
        if e.get("phase") != 2:
            continue
        if e.get("kind") not in BUDGET_KINDS:
            continue
        if e.get("kind") == "VIOLACION" and e.get("prereg"):
            continue          # ya lo pagó su pre-registro
        if family is not None and e.get("family") != family:
            continue
        n += 1
    return n


def budget_report() -> dict:
    fuera = out_of_scope_families()
    perdidos = sum(e.get("cartuchos_perdidos", 0) for e in fuera.values())
    return {
        "K1": K1, "K2": K2, "K_total": K_TOTAL,
        "usado": budget_used(),
        "perdidos_fuera_de_alcance": perdidos,
        "fuera_de_alcance": sorted(fuera),
        "restante": K2 - budget_used() - perdidos,
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


def required_t_a(n_a_trades: int, n_b_trades: int) -> float:
    """§3.2: la barra efectiva en A = max(línea de decisión, lo que hace falta
    para que el examen final pueda responder).

    LOS DOS ARGUMENTOS SON **OPERACIONES**, NO DÍAS NI SESIONES.

    Esto NO es un tamiz distinto de `power_check`: es la MISMA condición
    reescrita. Con t_A = δ̂·√n_A,

        t_A ≥ 2.8016·√(n_A/n_B)  ⟺  δ̂·√n_A ≥ 2.8016·√n_A/√n_B
                                  ⟺  δ̂·√n_B ≥ 2.8016      (= power_check)

    o sea que no pueden aprobar cosas distintas mientras se las llame con los
    mismos conteos. `passes_bar_a` las evalúa a las dos y `_assert_gates_agree`
    revienta si alguna vez difieren: dos compuertas que miden lo mismo y se
    llaman parecido son un accidente esperando, así que acá se cruzan solas.

    Pasar SESIONES en lugar de operaciones es un uso de PLANIFICACIÓN — el que
    hace la tabla de §3.2 — y sólo vale si la tasa de operaciones por sesión es
    la misma en A y en B. Para una estrategia de calendario (F4: ~12 operaciones
    al año) la tasa no sigue a las sesiones y el proxy miente. La DECISIÓN se
    toma siempre con operaciones reales de A y operaciones proyectadas en B.
    """
    if n_b_trades <= 0:
        return float("inf")
    return max(DECISION_T, POWER_CONST * sqrt(n_a_trades / n_b_trades))


def _assert_gates_agree(t_a: float, n_a_trades: int, n_b_trades: int,
                        delta_hat: float, power_ok: bool) -> None:
    """Guardia: la compuerta expresada en t y la expresada en potencia tienen
    que dar el mismo veredicto. Si no, alguien las llamó con unidades distintas
    (el error clásico: sesiones de un lado, operaciones del otro)."""
    t_ok = t_a >= POWER_CONST * sqrt(n_a_trades / max(n_b_trades, 1))
    if t_ok != power_ok:
        raise SpecViolation(
            "las dos formas de la compuerta de potencia discrepan "
            f"(t_A={t_a:.4f}, n_A={n_a_trades}, n_B={n_b_trades}, "
            f"delta={delta_hat:.6f}): revisá que ambas reciban OPERACIONES, "
            "no sesiones (§3.2)."
        )


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
    _assert_gates_agree(st["t"], st["n"], n_b_proyectado, st["delta"], pc["aprueba"])
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
    assert_frozen_constants()
    if family not in FAMILY_BUDGET:
        raise SpecViolation(f"familia no declarada en la spec: {family!r}")
    if not hypothesis or not hypothesis.strip():
        raise SpecViolation("pre-registro sin hipótesis: prohibido (§7.2)")

    if family in out_of_scope_families():
        e = out_of_scope_families()[family]
        raise SpecViolation(
            f"{family} está FUERA DE ALCANCE de la Fase 2 desde {e['ts'][:10]} "
            f"({e['motivo']}). Sus cartuchos se perdieron y no vuelven (§7.6)."
        )

    # Un plazo vencido y sin resolver detiene TODA la búsqueda, no solo lo que
    # bloquea: es una decisión que hay que tomar, no un trámite que espera.
    vencidos = overdue_blockers()
    if vencidos:
        detalle = "; ".join(
            f"{b['bloqueante']} venció el {b['vence_el']} y bloquea "
            f"{b['todavia_bloquea']} — resolver con {b['resuelve_con']}, o "
            f"declare_out_of_scope(...): {b['al_vencer']}" for b in vencidos)
        raise SpecViolation(
            f"hay {len(vencidos)} bloqueante(s) VENCIDO(s) sin resolver: {detalle} "
            "(§7.6: no puede haber un tercer estado)."
        )

    # Un pre-registro sin resolver BLOQUEA el siguiente. Desde afuera del repo,
    # "pre-registrado y nunca corrido" es indistinguible de "corrido, salió feo
    # y no escribí el resultado". Para el operador honesto da igual; para quien
    # audita es el hueco entero. Así que no se puede abrir otro hasta cerrarlo:
    # con un resultado, o con un abandono con motivo escrito.
    abiertos = open_preregistrations()
    if abiertos:
        detalle = "; ".join(
            f"{e['family']} {json.dumps(e['config'], sort_keys=True)} "
            f"(hash {e['hash']}, {e['ts'][:19]})" for e in abiertos)
        raise SpecViolation(
            f"hay {len(abiertos)} pre-registro(s) sin resolver y bloquean el "
            f"siguiente: {detalle}. Cerralo con run_on(...) o con "
            "abandon(family, config, motivo) antes de pre-registrar otra cosa "
            "(§7.2)."
        )

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
            # kind=CARTUCHO, no PREREGISTRO: se cobra pero no queda esperando
            # una corrida, así que no cuelga ni bloquea al siguiente.
            entries.append(_append({
                "phase": 2, "kind": "CARTUCHO", "family": family,
                "config": cell, "part": "A", "result": None,
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


# Un pre-registro se RESUELVE con exactamente una de tres entradas. Cualquier
# otra cosa lo deja colgando, y un pre-registro colgando es indistinguible desde
# afuera de "lo corrí, salió feo y no escribí el resultado" — que es justo lo
# que este ledger existe para impedir.
RESOLVING_KINDS = ("RESULTADO", "ABANDONO", "VIOLACION")


def open_preregistrations() -> list:
    """Todos los pre-registros sin resolver, en orden. Debería haber 0 o 1."""
    resolved = {e["prereg"] for e in read_ledger()
                if e.get("kind") in RESOLVING_KINDS and e.get("prereg")}
    return [e for e in read_ledger()
            if e.get("phase") == 2 and e.get("kind") == "PREREGISTRO"
            and e["hash"] not in resolved]


def open_preregistration(family: str, config: dict) -> dict | None:
    """El pre-registro sin resolver de esta configuración, si lo hay."""
    key = _cfg_key(family, config)
    for e in open_preregistrations():
        if _cfg_key(e["family"], e["config"]) == key:
            return e
    return None


def abandon(family: str, config: dict, motivo: str) -> dict:
    """Cierra un pre-registro que no se va a correr. El motivo es OBLIGATORIO:
    'datos faltantes', 'error de diseño', lo que sea — pero escrito. El cartucho
    ya se gastó y no se devuelve (§7.2: los errores de diseño también cuestan)."""
    if not motivo or not motivo.strip():
        raise SpecViolation("abandono sin motivo escrito: prohibido (§7.2)")
    prereg = open_preregistration(family, config)
    if prereg is None:
        raise SpecViolation(
            f"no hay pre-registro abierto para {family} {config} que abandonar")
    return _append({
        "phase": 2, "kind": "ABANDONO", "family": family, "config": config,
        "part": "A", "result": None, "prereg": prereg["hash"],
        "motivo": motivo.strip(),
        "note": "ABANDONADA sin correr. El cartucho ya se gastó y no se devuelve.",
    })


def log_spec_violation(family: str, config: dict, result: Result | None,
                       motivo: str) -> dict:
    """Para lo que el código no puede impedir: alguien corrió una estrategia sin
    pasar por `run_on`. Se registra CON su resultado y gasta cartucho igual.

    Si existía un pre-registro abierto para esa configuración, esta entrada lo
    RESUELVE (es la tercera de las tres salidas posibles) y no vuelve a cobrar:
    el cartucho ya se pagó al pre-registrar."""
    prereg = open_preregistration(family, config)
    body = {
        "phase": 2, "kind": "VIOLACION", "family": family, "config": config,
        "part": "A", "result": result.to_dict() if result else None,
        "spec_violation": motivo,
        "note": "VIOLACION DE SPEC: consume presupuesto igual (§7.2)",
    }
    if prereg is not None:
        body["prereg"] = prereg["hash"]
        body["note"] = ("VIOLACION DE SPEC sobre una config ya pre-registrada: "
                        "resuelve el pre-registro, no cobra dos veces (§7.2)")
    return _append(body)


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
    assert_frozen_constants()
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
        ok, why = can_declare_operable(family)
        if not ok:
            raise OperabilityUnknown(
                f"examen final de {family} bloqueado: {why}. El margen es una "
                "restricción de despliegue, no de investigación — no impide medir, "
                "pero sí gastar el único uso de la caja fuerte en algo que no se "
                "podría operar (§7.3)."
            )
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
        "margen_vigente": (overnight_margin() or {}).get("_hash"),
        "operable": can_declare_operable(family)[0],
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

# Congelar los datos y no las REGLAS deja el acta viéndose intacta mientras el
# significado de cada número cambia debajo. Un tercero reproduciría los números
# leyendo reglas distintas de las que regían.
#
# EL CORTE, y por qué cae donde cae. Se congela lo que NO puede cambiar durante
# la fase sin cambiar el significado de todo lo ya medido:
#
#   spec_fase2.md   las reglas escritas. Sus §1–§4 están congeladas por
#                   declaración; el hash lo hace comprobable en vez de prometido.
#   harness_f2.py   las reglas COMO SE APLICAN. La spec dice qué se exige; este
#                   archivo es lo que efectivamente se niega a correr. Si sólo se
#                   congelara la spec, la enforcement podría aflojarse sin rastro.
#   harness.py      la fricción ($3.90 adentro de cada número), evaluate_trades y
#                   la cadena del ledger. Además prometimos dejarlo byte a byte
#                   idéntico: el hash convierte esa promesa en algo verificable.
#
# NO se congelan los módulos de estrategia (familias_4_5.py, intradia.py,
# familia2_tendencia.py, familia_g2.py…). No son las reglas de la búsqueda: son
# las HIPÓTESIS, y se escriben a medida que a cada familia le llega el turno.
# Congelar al abrir algo que todavía no existe sería teatro. Lo que los protege
# es otra cosa y ya está: cada configuración queda en el ledger con su resultado,
# y el código que lo produjo, en el commit de git de ese momento — por eso el
# acta también guarda el commit del repo.
RULES_FILES = (
    os.path.join("factory", "spec_fase2.md"),
    os.path.join("factory", "harness_f2.py"),
    os.path.join("factory", "harness.py"),
)


def rules_hashes() -> dict:
    out = {}
    for rel in RULES_FILES:
        p = os.path.join(REPO, rel)
        key = rel.replace("\\", "/")
        out[key] = ({"sha256": sha256_file(p), "bytes": os.path.getsize(p)}
                    if os.path.exists(p)
                    else {"sha256": None, "bytes": None, "nota": "AUSENTE"})
    return out


def rules_digest(hashes: dict | None = None) -> str:
    """Huella corta de las tres reglas juntas. Va en CADA entrada de Fase 2, así
    cualquier deriva queda fechada y atribuida en vez de invisible."""
    h = hashes or rules_hashes()
    joined = "|".join(f"{k}:{v.get('sha256')}" for k, v in sorted(h.items()))
    return hashlib.sha256(joined.encode()).hexdigest()[:16]


def git_commit() -> str | None:
    """Commit del repo al abrir: cubre TODO lo versionado, incluido lo que
    todavía no se escribió. Complementa los hashes explícitos, no los reemplaza."""
    import subprocess
    try:
        out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO,
                             capture_output=True, text=True, timeout=15)
        return out.stdout.strip() or None
    except Exception:      # noqa: BLE001
        return None


# Constantes que el acta congela. Cambiar cualquiera de ellas después de firmar
# es cambiar la vara, así que el harness se niega a seguir corriendo.
FROZEN_KEYS = ("K1", "K2", "K_total", "alpha", "presupuesto_por_familia", "ventanas")


def _acta() -> dict | None:
    for e in read_ledger():
        if e.get("kind") == "APERTURA_FASE2":
            return e
    return None


def _live_frozen() -> dict:
    return {
        "K1": K1, "K2": K2, "K_total": K_TOTAL, "alpha": ALPHA,
        "presupuesto_por_familia": FAMILY_BUDGET,
        "ventanas": {k: {"a": [v.a_start, v.a_end], "b": [v.b_start, v.b_end],
                         "serie": v.series, "excluidas": len(v.excluded)}
                     for k, v in WINDOWS.items()},
    }


def assert_frozen_constants() -> None:
    """Fail-closed: si una constante congelada por el acta cambió, no se corre."""
    acta = _acta()
    if acta is None:
        return
    live = _live_frozen()
    difieren = [k for k in FROZEN_KEYS if acta.get(k) != live[k]]
    if difieren:
        raise SpecViolation(
            f"constantes congeladas por el acta que cambiaron: {difieren}. "
            "Los números de §1–§4 no se tocan hasta el veredicto; corregí el "
            "código o abrí una fase nueva."
        )


def rules_drift() -> dict:
    """Diferencia entre las reglas de HOY y las que congeló el acta. No bloquea
    —el harness y la spec pueden crecer legítimamente— pero queda a la vista, y
    el veredicto tiene que publicarla."""
    acta = _acta()
    if acta is None:
        return {"acta": None}
    antes = acta.get("rules_sha256") or {}
    ahora = rules_hashes()
    cambiados = {k: {"acta": antes.get(k, {}).get("sha256"),
                     "ahora": ahora.get(k, {}).get("sha256")}
                 for k in set(antes) | set(ahora)
                 if antes.get(k, {}).get("sha256") != ahora.get(k, {}).get("sha256")}
    return {"digest_acta": acta.get("rules_digest"),
            "digest_ahora": rules_digest(ahora), "cambiados": cambiados}


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


# ---------------------------------------------------------------------------
# §7.6 — CAMPOS BLOQUEANTES CON FECHA DE VENCIMIENTO
#
# Un campo bloqueante sin fecha de resolución es un pendiente eterno, y un
# pendiente eterno es una decisión no tomada disfrazada de trámite. Tiene la
# misma forma que el pre-registro sin desenlace (§7.2), un nivel más arriba:
# parece que se va a resolver, no se resuelve, y lo que bloquea vive en un limbo
# que se ve prolijo.
#
# NO PUEDE HABER UN TERCER ESTADO. O el dato llega con su fecha, o lo que
# bloquea sale de alcance con el motivo escrito y publicado.
#
# Los cartuchos de una familia que sale de alcance se PIERDEN: no se retiran del
# denominador (§1.4 — retirarlos aflojaría el listón: con 217 en vez de 257 el
# |t| exigido baja de 3.726 a 3.683) y tampoco se reasignan a otra familia (§2 —
# el presupuesto no usado no se transfiere). Se pierden, el denominador queda en
# 257, y el listón no se mueve ni un punto. Es la única salida que no exige
# enmendar una regla ya firmada.
# Familias que mantienen posicion fuera del horario de day-trading: son las
# unicas cuya OPERABILIDAD depende del margen nocturno (G4 es intradia).
OVERNIGHT_FAMILIES = ("G1-nocturna", "G2-multidia", "G3-regimen", "G5-cruzado")

BLOQUEANTE_PLAZO_DIAS = 14

BLOQUEANTES = {
    "margen_nocturno_mes": {
        "bloquea": OVERNIGHT_FAMILIES,
        "resuelve_con": "register_overnight_margin(valor_usd, fuente, leido_el)",
        "clock": "apertura",          # el reloj arranca al abrir la fase
        "plazo_dias": BLOQUEANTE_PLAZO_DIAS,
        "bloquea_que": "la declaración de operabilidad y el examen final de las "
                       "familias overnight — NO la búsqueda (§7.3 reclasificado)",
        "al_vencer": ("Se declara con acta publicada que la Fase 2 NO puede "
                      "pronunciarse sobre la operabilidad de ninguna candidata "
                      "overnight, y toda candidata se publica con esa limitación "
                      "escrita. El presupuesto NO se toca: la búsqueda nunca "
                      "dependió del margen, así que sacrificar cartuchos sería "
                      "pagar por un bloqueo que no existe."),
    },
    "mapeo_dia_cme": {
        "bloquea": ("G4-bordes",),
        "resuelve_con": "INTRADAY_TRADING_DAY_MAPPING_READY = True, con su prueba",
        "clock": "cierre de G3-regimen",   # no bloquea hasta que sea su turno
        "plazo_dias": BLOQUEANTE_PLAZO_DIAS,
        "al_vencer": ("G4-bordes sale FUERA DE ALCANCE con motivo escrito. Sus 40 "
                      "cartuchos se PIERDEN, mismo criterio."),
    },
}

# El margen nocturno es una entrada de COSTO, no una regla: no forma parte de lo
# que el acta congela, y su ausencia no impide abrir la fase. Se registra AUSENTE
# EXPLÍCITO — nunca en cero, nunca con un valor "mientras tanto", porque un número
# provisorio en un campo de riesgo es indistinguible de un número real.
MARGEN_AUSENTE = {
    "estado": "AUSENTE",
    "valor_usd": None,
    "fuente": None,
    "leido_el": None,
    "nota": ("No se conoce el requisito de margen nocturno del bróker. NO se usa "
             "cero ni un valor provisorio ni la cifra de CME (que es el piso, no "
             "lo exigido). Entra despues como entrada COSTO_MARGEN propia y "
             "fechada; hasta entonces G1 no corre (§7.3)."),
}


def _today() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def _plus_days(iso_date: str, days: int) -> str:
    from datetime import date, timedelta
    y, m, d = (int(x) for x in iso_date.split("-"))
    return (date(y, m, d) + timedelta(days=days)).isoformat()


# El margen es una restricción de DESPLIEGUE, no de investigación: que exista una
# ventaja no depende del capital que inmovilice; poder operarla sí. Por eso NO
# bloquea la búsqueda — bloquea la declaración de operabilidad y el examen final
# de toda familia que cruce la noche.
#
# SALVAGUARDA (§7.3). Mover el bloqueo abre una puerta chica: si aparece una
# candidata, nace la presión de conseguir un margen que le convenga. Es el peeking
# transplantado — en vez de elegir la ventana después de ver el resultado, elegís
# el bróker. Por eso la entrada COSTO_MARGEN se registra UNA vez y es inmutable:
#   · no se revisa porque una candidata necesite un número más chico;
#   · una revisión A LA BAJA se RECHAZA si ya existe cualquier resultado de Fase 2;
#   · una revisión legítima (el bróker subió el requisito) entra como entrada
#     NUEVA y fechada que NO reemplaza a la anterior;
#   · cada resultado queda sellado con el margen vigente al correrlo, así "esta
#     candidata se evaluó bajo el margen viejo" es un hecho del ledger y no un
#     recuerdo.


class OperabilityUnknown(SpecViolation):
    """Se quiso declarar operable algo cuyo capital requerido no se conoce."""


def register_overnight_margin(valor_usd: float, fuente: str, leido_el: str,
                              nota: str = "", revision_motivo: str = "") -> dict:
    """El margen nocturno de MES: entrada propia, fechada e INMUTABLE.

    `valor_usd`: el requisito del BRÓKER, no el de CME (§7.3).
    `fuente`: de dónde se leyó, textual (ej. "NinjaTrader Tools > Instruments > MES").
    `leido_el`: fecha de lectura, YYYY-MM-DD. Sin ella el dato no es citable.
    `revision_motivo`: obligatorio para registrar un segundo valor. La entrada
        nueva NO reemplaza a la anterior; ambas quedan.

    Fail-closed: falta uno de los tres ⇒ no se registra.
    """
    if not (valor_usd and float(valor_usd) > 0):
        raise SpecViolation("margen nocturno sin valor positivo: no se inventa (§7.3)")
    if not (fuente and fuente.strip()):
        raise SpecViolation("margen nocturno sin fuente escrita (§7.3)")
    if not (leido_el and leido_el.strip()):
        raise SpecViolation("margen nocturno sin fecha de lectura (§7.3)")

    previo = overnight_margin()
    if previo is not None:
        if not (revision_motivo and revision_motivo.strip()):
            raise SpecViolation(
                f"ya hay un margen registrado (${previo['valor_usd']:,.2f}, "
                f"{previo['fuente']}, {previo['leido_el']}) y es INMUTABLE. Una "
                "revisión exige `revision_motivo` escrito, y no reemplaza a la "
                "anterior (§7.3)."
            )
        hay_resultados = any(e.get("kind") == "RESULTADO" for e in read_ledger())
        if float(valor_usd) < float(previo["valor_usd"]) and hay_resultados:
            raise SpecViolation(
                "revisión A LA BAJA del margen con resultados de Fase 2 ya en el "
                f"ledger: RECHAZADA (${previo['valor_usd']:,.2f} → "
                f"${float(valor_usd):,.2f}). Bajar el capital exigido después de "
                "tener candidatas es elegir el bróker en vez de la ventana: el "
                "mismo peeking, transplantado (§7.3)."
            )
    return _append({
        "phase": 2, "kind": "COSTO_MARGEN", "family": "META",
        "config": {"evento": "MARGEN NOCTURNO MES"},
        "part": "meta", "result": None,
        "margen_nocturno_mes": {
            "estado": "DECLARADO",
            "valor_usd": float(valor_usd),
            "fuente": fuente.strip(),
            "leido_el": leido_el.strip(),
            "nota": nota.strip() or None,
        },
        "revisa_a": previo.get("_hash") if previo else None,
        "revision_motivo": revision_motivo.strip() or None,
        "note": ("Margen nocturno de MES declarado con fuente y fecha. Habilita la "
                 "declaración de operabilidad y el examen final de las familias "
                 "overnight (§7.3). Entrada INMUTABLE." if previo is None else
                 "REVISION del margen nocturno. NO reemplaza a la anterior: las "
                 "candidatas evaluadas bajo la vieja quedan evaluadas bajo la vieja."),
    })


def open_phase2(margen_nocturno_mes: dict | None = None,
                data_dir: str | None = None, dry_run: bool = False) -> dict:
    """Escribe la entrada meta que abre la Fase 2 (§9.5). Es la firma.

    `margen_nocturno_mes`: por defecto MARGEN_AUSENTE. El margen es un costo, no
    una regla: la fase abre sin él y G1 queda bloqueada hasta que llegue como
    entrada `COSTO_MARGEN` propia (`register_overnight_margin`).

    `dry_run=True` devuelve el acta EXACTA que se escribiría, sin escribirla.
    Solo `ts` y `hash` se calculan al momento de escribir; todo lo demás es esto.
    """
    if margen_nocturno_mes is None:
        margen_nocturno_mes = dict(MARGEN_AUSENTE)
    hoy = _today()
    bloqueantes = {}
    for name, spec in BLOQUEANTES.items():
        vence = (_plus_days(hoy, spec["plazo_dias"])
                 if spec["clock"] == "apertura" else None)
        bloqueantes[name] = {
            "bloquea": list(spec["bloquea"]),
            "clock": spec["clock"],
            "plazo_dias": spec["plazo_dias"],
            "desde": hoy if vence else None,
            "vence_el": vence,
            "resuelve_con": spec["resuelve_con"],
            "al_vencer": spec["al_vencer"],
        }
    if margen_nocturno_mes.get("estado") == "AUSENTE":
        margen_nocturno_mes = dict(margen_nocturno_mes)
        margen_nocturno_mes["vence_el"] = bloqueantes["margen_nocturno_mes"]["vence_el"]
        margen_nocturno_mes["al_vencer"] = bloqueantes["margen_nocturno_mes"]["al_vencer"]
    hashes = freeze_data_hashes(data_dir)
    rh = rules_hashes()
    body = _acta_body(margen_nocturno_mes, hashes, bloqueantes)
    body["rules_sha256"] = rh
    body["rules_digest"] = rules_digest(rh)
    body["git_commit"] = git_commit()
    if dry_run:
        preview = dict(body)
        preview["prev"] = _last_hash()
        preview["_dry_run"] = ("ts y hash se calculan al escribir; el resto es "
                               "exactamente lo que se anexa")
        return preview
    return _append(body)


def _acta_body(margen_nocturno_mes: dict, hashes: dict,
               bloqueantes: dict | None = None) -> dict:
    return {
        "bloqueantes": bloqueantes or {},
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
                 ("G1 HABILITADA."
                  if margen_nocturno_mes.get("estado") == "DECLARADO"
                  else "G1 BLOQUEADA: margen nocturno de MES AUSENTE (§7.3). "
                       "El margen es un costo, no una regla: entra despues como "
                       "entrada propia y fechada.")),
    }


def out_of_scope_families() -> dict:
    """{familia: entrada} de las que salieron de alcance. Sus cartuchos están
    perdidos: no se pueden gastar, y siguen contando en el denominador."""
    out = {}
    for e in read_ledger():
        if e.get("kind") == "FUERA_DE_ALCANCE":
            out[e["family"]] = e
    return out


def declare_out_of_scope(family: str, motivo: str, bloqueante: str | None = None) -> dict:
    """Saca una familia de alcance de la Fase 2. El motivo es OBLIGATORIO y se
    publica. Los cartuchos se pierden: el denominador sigue en K_total (§1.4) y
    no se reasignan (§2)."""
    if family not in FAMILY_BUDGET:
        raise SpecViolation(f"familia no declarada: {family!r}")
    if not motivo or not motivo.strip():
        raise SpecViolation("salir de alcance sin motivo escrito: prohibido (§7.6)")
    if family in out_of_scope_families():
        raise SpecViolation(f"{family} ya está fuera de alcance")
    perdidos = FAMILY_BUDGET[family] - budget_used(family)
    return _append({
        "phase": 2, "kind": "FUERA_DE_ALCANCE", "family": family,
        "config": {"evento": "FUERA DE ALCANCE"}, "part": "meta", "result": None,
        "motivo": motivo.strip(),
        "bloqueante": bloqueante,
        "cartuchos_perdidos": perdidos,
        "K_total_sigue_en": K_TOTAL,
        "note": (f"{family} FUERA DE ALCANCE de la Fase 2. {perdidos} cartuchos "
                 f"PERDIDOS: no se retiran del denominador (sigue en {K_TOTAL}, "
                 "§1.4) ni se reasignan a otra familia (§2). El listón no se mueve."),
    })


def _blocker_resolved(name: str) -> bool:
    if name == "margen_nocturno_mes":
        return overnight_margin() is not None
    if name == "mapeo_dia_cme":
        return bool(INTRADAY_TRADING_DAY_MAPPING_READY)
    raise SpecViolation(f"bloqueante desconocido: {name!r}")


def blocking_status(today: str | None = None) -> list:
    """Estado de cada campo bloqueante: resuelto, vigente con plazo, vencido, o
    todavía sin reloj (su disparador no ocurrió). Nunca hay un cuarto estado."""
    today = today or _today()
    plazos = {}
    for e in read_ledger():
        if e.get("kind") in ("APERTURA_FASE2", "PLAZO_BLOQUEANTE"):
            for name, info in (e.get("bloqueantes") or {}).items():
                if info.get("vence_el"):
                    plazos[name] = info["vence_el"]
    fuera = out_of_scope_families()
    out = []
    for name, spec in BLOQUEANTES.items():
        resuelto = _blocker_resolved(name)
        vence = plazos.get(name)
        bloqueadas = [f for f in spec["bloquea"] if f not in fuera]
        if resuelto:
            estado = "RESUELTO"
        elif not bloqueadas:
            estado = "MOOT"          # ya salió de alcance lo que bloqueaba
        elif vence is None:
            estado = "SIN_RELOJ"     # su disparador todavía no ocurrió
        elif today > vence:
            estado = "VENCIDO"
        else:
            estado = "VIGENTE"
        out.append({
            "bloqueante": name, "estado": estado, "vence_el": vence,
            "bloquea": list(spec["bloquea"]), "todavia_bloquea": bloqueadas,
            "clock": spec["clock"], "resuelve_con": spec["resuelve_con"],
            "al_vencer": spec["al_vencer"],
        })
    return out


def overdue_blockers(today: str | None = None) -> list:
    return [b for b in blocking_status(today) if b["estado"] == "VENCIDO"]


def start_blocker_clock(name: str, desde: str | None = None) -> dict:
    """Arranca el reloj de un bloqueante cuyo disparador es un evento (p. ej. el
    mapeo de día CME, que no bloquea hasta que G4 sea su turno)."""
    if name not in BLOQUEANTES:
        raise SpecViolation(f"bloqueante desconocido: {name!r}")
    desde = desde or _today()
    vence = _plus_days(desde, BLOQUEANTES[name]["plazo_dias"])
    return _append({
        "phase": 2, "kind": "PLAZO_BLOQUEANTE", "family": "META",
        "config": {"evento": "ARRANCA PLAZO", "bloqueante": name},
        "part": "meta", "result": None,
        "bloqueantes": {name: {"desde": desde, "vence_el": vence,
                               "al_vencer": BLOQUEANTES[name]["al_vencer"]}},
        "note": (f"Reloj del bloqueante {name} arrancado el {desde}; vence el "
                 f"{vence}. {BLOQUEANTES[name]['al_vencer']}"),
    })


def phase2_is_open() -> bool:
    return any(e.get("kind") == "APERTURA_FASE2" for e in read_ledger())


def overnight_margin_history() -> list:
    """Todos los márgenes registrados, en orden. Ninguno reemplaza a otro."""
    out = []
    for e in read_ledger():
        if e.get("kind") in ("COSTO_MARGEN", "APERTURA_FASE2"):
            m = e.get("margen_nocturno_mes")
            if m and m.get("valor_usd") and m.get("fuente") and m.get("leido_el"):
                m = dict(m)
                m["_hash"] = e["hash"]
                m["_ts"] = e["ts"]
                out.append(m)
    return out


def overnight_margin() -> dict | None:
    """El margen vigente (el último registrado), o None. Fail-closed: ausente,
    cero o sin fecha ⇒ None."""
    h = overnight_margin_history()
    return h[-1] if h else None


def can_declare_operable(family: str) -> tuple:
    """¿Se puede afirmar que una candidata de esta familia es OPERABLE?

    La búsqueda no depende de esto (el margen no cambia ningún número del
    backtest: la fricción de $3.90 ya está adentro). La operabilidad sí."""
    if family not in OVERNIGHT_FAMILIES:
        return (True, "familia intradía: no inmoviliza margen nocturno")
    m = overnight_margin()
    if m is None:
        return (False, "margen nocturno de MES AUSENTE: no se puede afirmar con "
                       "qué tamaño de cuenta sería operable (§7.3)")
    return (True, f"margen ${m['valor_usd']:,.2f} ({m['fuente']}, {m['leido_el']})")


def g1_enabled() -> bool:
    """Retrocompatible: ¿hay margen declarado? Ojo — desde la reclasificación de
    §7.3 esto NO condiciona la búsqueda de G1, sólo su operabilidad."""
    return overnight_margin() is not None
