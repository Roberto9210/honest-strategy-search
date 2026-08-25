# -*- coding: utf-8 -*-
"""Medicion CIEGA de sigma y frecuencia, para el paquete multi-mercado.

POR QUE EXISTE
--------------
Para saber si un mercado sobrevive la friccion hace falta `sigma` por operacion.
Calcularla exige correr la regla sobre las barras de ese mercado, y quien corre la
regla puede ver si gano plata ahi. Si lo ve ANTES de pre-registrar, el fuera de
muestra deja de valer: la eleccion de mercados quedaria contaminada por el
resultado, que es exactamente el pecado que este proyecto persigue.

Es el mismo problema que la Fase 2 ya resolvio una vez, y con la misma respuesta:
contar FRECUENCIA no es contar RENTABILIDAD (`spec_fase2.md` §3.5). `sigma` es una
propiedad del MERCADO -- cuanto se mueve -- no de si la regla acierta. La media es
la propiedad que decide, y la media NO SALE DE ACA.

EL CONTRATO
-----------
`medir_ciego()` devuelve UNICAMENTE:
    n_operaciones   int    frecuencia (§3.5 ya la declaro legitima)
    sesiones        int    largo del calendario
    ocupacion       float  n*hold/sesiones
    sigma_puntos    float  dispersion por operacion, en puntos de precio
    sigma_ticks     float  la misma, en ticks
    primera / ultima str   los bordes de la serie

Nunca una media, nunca una suma, nunca un P&L, nunca un conteo de ganadoras,
nunca la serie de operaciones. La prueba de que es ciega no es esta docstring:
son los dos controles de `tests/multimercado/test_ciego.py`, que le dan vuelta el
signo a todas las operaciones y le suman una constante a cada una, y exigen que
la salida NO CAMBIE. Una funcion cuya salida no distingue una regla ganadora de
una perdedora no puede filtrar el resultado.
"""
from __future__ import annotations

CLAVES_PERMITIDAS = ("mercado", "n_operaciones", "sesiones", "ocupacion",
                     "sigma_puntos", "sigma_ticks", "primera", "ultima")

# Palabras que NO pueden aparecer en una clave de salida. Si alguien agrega un
# campo con cualquiera de estas, el test lo tumba.
PALABRAS_PROHIBIDAS = ("media", "mean", "suma", "sum", "pnl", "p_l", "neto",
                       "net", "ganancia", "profit", "retorno", "return",
                       "ganadoras", "wins", "sharpe", "equity", "total")


class FugaDeResultado(Exception):
    """Un camino de este modulo estuvo a punto de exponer rentabilidad."""


def _validar_salida(out: dict) -> dict:
    """Fail-closed: si aparece una clave no declarada, revienta. No se filtra
    en silencio, porque un filtrado silencioso esconde justamente el error."""
    for k in out:
        if k not in CLAVES_PERMITIDAS:
            raise FugaDeResultado(
                f"clave no declarada en la salida ciega: {k!r}. "
                f"Permitidas: {CLAVES_PERMITIDAS}")
        bajo = k.lower()
        for mala in PALABRAS_PROHIBIDAS:
            if mala in bajo:
                raise FugaDeResultado(
                    f"la clave {k!r} contiene {mala!r}: eso es rentabilidad, "
                    "no dispersion")
    for k, v in out.items():
        if not isinstance(v, (int, float, str)) or isinstance(v, bool):
            raise FugaDeResultado(
                f"{k!r} devuelve {type(v).__name__}: solo escalares y texto. "
                "Un vector puede llevar el P&L adentro")
    return out


def medir_ciego(strategy_fn, df, config: dict, tick_size: float,
                mercado: str = "?") -> dict:
    """sigma por operacion y frecuencia. Nada mas. Ver el contrato arriba."""
    import numpy as np

    trades = strategy_fn(df, config)
    n = int(len(trades))
    sesiones = int(len(df))
    if n < 2:
        return _validar_salida({
            "mercado": mercado, "n_operaciones": n, "sesiones": sesiones,
            "ocupacion": 0.0, "sigma_puntos": 0.0, "sigma_ticks": 0.0,
            "primera": str(df.index[0].date()) if sesiones else "",
            "ultima": str(df.index[-1].date()) if sesiones else "",
        })

    # Se calcula la dispersion y se DESCARTA todo lo demas en el acto. La media
    # existe en memoria el tiempo que tarda np.std en restarla, y no sale.
    puntos = (trades["points"] * trades["contracts"]).to_numpy(dtype=float)
    sigma_puntos = float(np.std(puntos, ddof=1))
    del puntos, trades

    hold = float(config.get("hold", 1))
    return _validar_salida({
        "mercado": mercado,
        "n_operaciones": n,
        "sesiones": sesiones,
        "ocupacion": n * hold / sesiones if sesiones else 0.0,
        "sigma_puntos": sigma_puntos,
        "sigma_ticks": sigma_puntos / float(tick_size),
        "primera": str(df.index[0].date()),
        "ultima": str(df.index[-1].date()),
    })


def friccion(costo_ticks: float, sigma_ticks: float) -> float:
    """f = costo por vuelta completa / sigma de la operacion, ambos en TICKS.

    En ticks y no en dolares a proposito: el valor de tick en dolares es una
    spec que no se pudo verificar contra CME desde esta sesion, mientras que el
    TAMANIO de tick es un numero de precio, mas robusto. Y f es adimensional, asi
    que la razon no cambia por medirla en una unidad o en otra."""
    if sigma_ticks <= 0:
        raise ValueError("sigma_ticks <= 0: no hay dispersion que dividir")
    return float(costo_ticks) / float(sigma_ticks)


def n_necesario(delta_neto: float) -> float:
    """Operaciones para 80% de potencia a alfa 0.05 bilateral (§3.2 de la Fase 2)."""
    if delta_neto <= 0:
        return float("inf")
    return 7.8489 / float(delta_neto) ** 2


def costo_ticks_maximo(sigma_ticks: float, delta_bruto: float = 0.107006,
                       f_objetivo: float | None = None) -> float:
    """Cuantos ticks de peaje aguanta un mercado.

    Con f_objetivo=None devuelve el peaje LETAL (el que deja delta neto en cero).
    Con f_objetivo=0.023301 devuelve el que lo deja empatado con el ancla ES/MES."""
    f = float(delta_bruto if f_objetivo is None else f_objetivo)
    return f * float(sigma_ticks)


def sesiones_ocupadas(strategy_fn, df, config: dict) -> set:
    """Fechas en las que la regla TIENE posicion abierta. Solo fechas.

    Timing, no rentabilidad: es la misma clase de dato que `count_trades_only`
    de la Fase 2. El test lo prueba dandole vuelta el signo a las operaciones y
    exigiendo el mismo conjunto de fechas."""
    trades = strategy_fn(df, config)
    hold = int(config.get("hold", 1))
    pos = {d: i for i, d in enumerate(df.index)}
    ocupadas = set()
    for fecha_salida in trades.index:
        p = pos.get(fecha_salida)
        if p is None:
            continue
        for q in range(max(0, p - hold), p):
            ocupadas.add(df.index[q].date())
    return ocupadas


def solapamiento(ocup_a: set, ocup_b: set, calendario_comun: set) -> dict:
    """Cuanto se pisan dos mercados, contra lo que darian si fueran independientes.

    Devuelve SOLO escalares. No mira un solo P&L: son fechas contra fechas."""
    cal = set(calendario_comun)
    a, b = ocup_a & cal, ocup_b & cal
    d = len(cal)
    if d == 0:
        raise ValueError("calendario comun vacio")
    obs = len(a & b) / d
    esp = (len(a) / d) * (len(b) / d)
    return _validar_salida_solape({
        "dias_comunes": d,
        "ocupa_a": len(a) / d,
        "ocupa_b": len(b) / d,
        "solape_observado": obs,
        "solape_esperado_si_independientes": esp,
        "lift": (obs / esp) if esp > 0 else float("inf"),
    })


CLAVES_SOLAPE = ("dias_comunes", "ocupa_a", "ocupa_b", "solape_observado",
                 "solape_esperado_si_independientes", "lift")


def _validar_salida_solape(out: dict) -> dict:
    for k, v in out.items():
        if k not in CLAVES_SOLAPE:
            raise FugaDeResultado(f"clave no declarada en el solape: {k!r}")
        if not isinstance(v, (int, float)) or isinstance(v, bool):
            raise FugaDeResultado(f"{k!r} no es escalar")
    return out
