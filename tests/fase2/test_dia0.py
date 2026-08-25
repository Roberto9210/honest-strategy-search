"""Pruebas conductuales del trabajo de día 0 de la Fase 2 (spec_fase2.md §9).

Método: cada regla de la spec probada por su CONDUCTA, con su control.
  · Estado TEMPORAL siempre: el ledger de trabajo es una copia del publicado en
    un tempdir. El ledger real NUNCA se toca.
  · Sin red, sin órdenes, sin datos de la parte B evaluados.
  · Los controles muestran qué hacía el harness de la Fase 1 en el mismo caso,
    para que "esto lo arregla" no sea una afirmación sin contraparte.

Uso:  venv\\Scripts\\python.exe tests\\fase2\\test_dia0.py
"""
from __future__ import annotations

import io
import json
import os
import re
import shutil
import sys
import tempfile
import traceback
from math import isclose

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
FACTORY = os.path.join(REPO, "factory")
sys.path.insert(0, FACTORY)

import harness            # noqa: E402
import harness_f2 as f2   # noqa: E402

PUBLISHED_LEDGER = os.path.join(FACTORY, "experiments_ledger.jsonl")

OK = 0
FAIL = []


def check(cond, label):
    global OK
    if cond:
        OK += 1
        print(f"    ok   {label}")
    else:
        FAIL.append(label)
        print(f"    FALLA {label}")


def raises_msg(exc, fn, label, must_contain=()):
    """Como raises(), pero además exige que el mensaje nombre lo que corresponde:
    una excepción que salta por el motivo equivocado es un test que miente."""
    try:
        fn()
    except exc as e:
        msg = str(e)
        missing = [m for m in must_contain if m not in msg]
        if missing:
            check(False, f"{label} -> mensaje no menciona {missing}: {msg[:160]}")
        else:
            check(True, f"{label} -> {type(e).__name__}, y el mensaje lo nombra")
        return str(e)
    except Exception as e:  # noqa: BLE001
        check(False, f"{label} -> {type(e).__name__} en vez de {exc.__name__}: {e}")
        return ""
    check(False, f"{label} -> NO levantó {exc.__name__}")
    return ""


def raises(exc, fn, label):
    try:
        fn()
    except exc as e:
        check(True, f"{label} -> {type(e).__name__}")
        return
    except Exception as e:  # noqa: BLE001
        check(False, f"{label} -> levantó {type(e).__name__} en vez de {exc.__name__}: {e}")
        return
    check(False, f"{label} -> NO levantó {exc.__name__}")


# --------------------------------------------------------------------------
# Fixtures sintéticos: nada depende de tener los datos reales bajados.
# --------------------------------------------------------------------------

def synthetic_daily(start="1995-01-02", end="2030-12-31", seed=7):
    """Barras diarias sintéticas, días hábiles. Deterministas."""
    idx = pd.bdate_range(start, end)
    rng = np.random.default_rng(seed)
    close = 1000 + np.cumsum(rng.normal(0.2, 10, len(idx)))
    df = pd.DataFrame({
        "open": close - rng.normal(0, 1, len(idx)),
        "high": close + np.abs(rng.normal(5, 2, len(idx))),
        "low": close - np.abs(rng.normal(5, 2, len(idx))),
        "close": close,
        "volume": rng.integers(1000, 5000, len(idx)),
    }, index=idx)
    return df


SEEN = {}


def strat_record(data, cfg):
    """Estrategia de juguete: anota qué datos recibió y devuelve operaciones
    con un neto por operación controlado por cfg['edge_points']."""
    SEEN["index"] = data.index
    step = cfg.get("step", 5)
    pts = cfg.get("edge_points", 1.0)
    noise = cfg.get("noise", 0.0)
    rng = np.random.default_rng(cfg.get("seed", 3))
    rows = data.index[::step]
    p = np.full(len(rows), pts, dtype=float)
    if noise:
        p = p + rng.normal(0, noise, len(rows))
    out = pd.DataFrame({"points": p, "contracts": 1.0}, index=rows)
    out.index.name = "exit_time"
    return out


def pre(family, config, hypothesis, **kw):
    """preregister() con la criba de configuración satisfecha por defecto.
    Las pruebas que son SOBRE la criba llaman a pre() directo."""
    kw.setdefault("n_b_proyectado", 5000)
    kw.setdefault("n_b_fuente", "fixture de prueba")
    kw.setdefault("mecanismo", "mecanismo-" + str(config))
    kw.setdefault("h", 1.0)
    if family in f2.FILTER_FAMILIES:      # §3.7: los filtros declaran tres numeros
        kw.setdefault("phi", 0.5)
        kw.setdefault("psi", 0.9)         # concentracion 1.8x, muy por encima de la vara
        kw.setdefault("h_residuo", kw["h"])
    return f2.preregister(family, config, hypothesis, **kw)


def fresh_ledger(tmp):
    """Copia el ledger PUBLICADO al tempdir y apunta ahí. Así también se prueba
    que la cadena de la Fase 2 engancha con la real, no con una inventada."""
    dst = os.path.join(tmp, "ledger.jsonl")
    # Se copia el ledger publicado TRUNCADO al cierre de la Fase 1: así se prueba
    # que la cadena de Fase 2 engancha con datos reales, y a la vez las pruebas no
    # dependen de cuánto haya crecido la Fase 2 desde que se escribieron.
    with io.open(PUBLISHED_LEDGER, encoding="utf-8") as src,             io.open(dst, "w", encoding="utf-8") as out:
        for linea in src:
            if not linea.strip():
                continue
            if json.loads(linea).get("phase") == 2:
                break
            out.write(linea)
    f2.set_ledger(dst)
    # §3.5: sin criba de medibilidad no se puede gastar un cartucho. Las pruebas
    # que no son sobre la criba arrancan con todas las familias cribadas.
    for fam in f2.FAMILY_BUDGET:
        f2.log_measurability_screen(fam, 5000, "fixture de prueba",
                                    sigma_por_operacion=200.0)
    return dst


# ==========================================================================
def s0_constantes():
    print("\n[0] §1/§2 — las constantes congeladas al firmar")
    check(f2.K1 == 57 and f2.K2 == 200 and f2.K_TOTAL == 257, "K1=57, K2=200, K_total=257")
    check(isclose(f2.DECISION_P, 0.05 / 257), "línea de decisión = α/K_total")
    check(abs(f2.DECISION_P - 1.9455e-4) < 1e-8, f"α/K = {f2.DECISION_P:.4e}")
    check(abs(f2.DECISION_T - 3.726) < 5e-4, f"|t| exigido = {f2.DECISION_T:.4f} (spec: 3.726)")
    check(isclose(f2.LUCK_P, 1 / 258), f"línea de la suerte = 1/(K+1) = {f2.LUCK_P:.5f}")
    check(abs(f2.LUCK_P - 0.00388) < 1e-5, "línea de la suerte 0.00388 como dice la spec")
    check(sum(f2.FAMILY_BUDGET.values()) == 200, "el reparto por familia suma 200")
    check(abs(f2.POWER_CONST - 2.8016) < 1e-3, f"z_α/2+z_β = {f2.POWER_CONST:.4f}")
    # la relación que la spec afirma: la decisión está ~20x por debajo de la suerte
    check(abs(f2.DECISION_P / f2.LUCK_P - 0.05) < 1e-3,
          "decisión / suerte ≈ α = 0.05 (20 veces por debajo)")


def s1_reproduce_f4():
    print("\n[1] CONTROL — el estadístico nuevo reproduce los números PUBLICADOS de F4")
    data_path = os.path.join(REPO, "data", "es_daily.csv")
    if not os.path.exists(data_path):
        print("    (salteado: data/es_daily.csv no está — data/ es gitignored)")
        return
    from familias_4_5 import turn_of_month
    df = pd.read_csv(data_path)
    c = df.columns[0]
    df[c] = pd.to_datetime(df[c])
    df = df.set_index(c).sort_index()
    df.columns = [x.lower() for x in df.columns]
    a = df.loc["2000-01-01":"2019-12-31"]
    trades = turn_of_month(a, {"n_before": 4, "m_after": 3})

    st = f2.stat_test(trades)
    check(st["n"] == 231, f"n = {st['n']} (publicado 231)")
    check(abs(st["media"] - 25.30) < 0.01, f"media ${st['media']:.2f} (publicado $25.30)")
    check(abs(st["desvio"] - 166.95) < 0.01, f"desvío ${st['desvio']:.2f} (publicado $166.95)")
    check(abs(st["t"] - 2.304) < 0.001, f"t = {st['t']:.3f} (publicado 2.304)")
    check(abs(st["p_crudo"] - 0.0212) < 0.0001, f"p = {st['p_crudo']:.4f} (publicado 0.0212)")

    print("    -- y la conclusión de la spec, ahora automática:")
    check(st["supera_linea_decision"] is False, "F4 NO supera la línea de decisión")
    check(st["supera_linea_suerte"] is False,
          f"F4 NO supera ni la línea de la suerte (p {st['p_crudo']:.4f} > {f2.LUCK_P:.5f})")

    pc = f2.power_check(st["delta"], 80)
    check(abs(pc["potencia"] - 0.273) < 0.002, f"potencia en B = {pc['potencia']:.1%} (publicado 27.3%)")
    check(pc["n_b_necesario"] == 342, f"operaciones para 80% = {pc['n_b_necesario']} (publicado 342)")
    check(pc["aprueba"] is False, "F4 NO pasa la compuerta de potencia -> se archiva")

    print("    -- required_t_a con las OPERACIONES reales de F4, no con sesiones:")
    check(abs(f2.required_t_a(231, 80) - 4.761) < 0.001,
          f"t exigido con n_A=231, n_B=80: {f2.required_t_a(231, 80):.3f}")
    check(st["t"] < f2.required_t_a(231, 80),
          f"F4 t={st['t']:.3f} por debajo de 4.761 -> mismo veredicto que power_check")

    print("    -- planificación con SESIONES: parecido, y NO es lo mismo")
    check(abs(f2.required_t_a(4875, 1669) - 4.788) < 0.001,
          f"sesiones diarias 4875/1669 -> {f2.required_t_a(4875, 1669):.3f} (tabla de §3.2)")
    check(abs(f2.required_t_a(4875, 1669) - f2.required_t_a(231, 80)) > 0.02,
          "4.788 (sesiones) != 4.761 (operaciones): el proxy es para planificar, no para decidir")
    check(abs(f2.required_t_a(1004, 1669) - f2.DECISION_T) < 1e-9,
          "intradía: manda la línea de decisión (3.726), no la potencia")


def s1b_compuertas_identicas():
    print("\n[1b] §3.2 — required_t_a y power_check son la MISMA condición")
    print("    t_A >= 2.8016*sqrt(n_A/n_B)  <=>  delta*sqrt(n_B) >= 2.8016")
    disagreements = []
    for n_a in (100, 231, 500, 1000, 4875):
        for n_b in (40, 80, 300, 1669, 5000):
            for delta in (0.02, 0.05, 0.0686, 0.1515, 0.3, 0.6):
                t_a = delta * np.sqrt(n_a)
                via_t = t_a >= f2.POWER_CONST * np.sqrt(n_a / n_b)
                via_power = f2.power_check(delta, n_b)["aprueba"]
                if via_t != via_power:
                    disagreements.append((n_a, n_b, delta, via_t, via_power))
    check(not disagreements,
          f"150 combinaciones (n_A, n_B, delta): 0 discrepancias "
          f"({len(disagreements)} encontradas)")

    print("    -- y la guardia revienta si alguien las llama con unidades distintas")
    raises(f2.SpecViolation,
           lambda: f2._assert_gates_agree(t_a=3.0, n_a_trades=4875,
                                          n_b_trades=1669, delta_hat=0.043,
                                          power_ok=True),
           "veredictos incompatibles (sesiones de un lado, operaciones del otro)")


def s2_prerregistro(tmp):
    print("\n[2] §7.2 — pre-registro obligatorio antes de conocer el resultado")
    fresh_ledger(tmp)
    df = synthetic_daily()
    cfg = {"step": 5, "edge_points": 1.0}

    print("    -- CONTROL: el harness de la Fase 1 corre sin pre-registro ninguno")
    ctrl_before = len(f2.read_ledger())
    split = harness.Split("2000-09-18", "2019-12-31", "2020-01-01", "2026-08-19")
    harness.run_on(df, split, strat_record, cfg, "CONTROL-fase1")
    check(len(f2.read_ledger()) == ctrl_before + 1,
          "Fase 1: corrió y registró DESPUÉS, sin exigir nada antes (ése era el hueco)")

    print("    -- FIX: la Fase 2 se niega")
    raises(f2.PreregistrationMissing,
           lambda: f2.run_on(df, "G1-nocturna", cfg, strat_record),
           "run_on sin pre-registro")

    n0 = f2.budget_used()
    pre("G1-nocturna", cfg, "prima nocturna: prueba de humo")
    check(f2.budget_used() == n0 + 1, "el pre-registro gasta cartucho al escribirse, no al correr")
    res = f2.run_on(df, "G1-nocturna", cfg, strat_record)
    check(res.trades > 0, f"con pre-registro corre ({res.trades} operaciones)")

    print("    -- y el pre-registro se consume: no habilita una segunda corrida")
    raises(f2.PreregistrationMissing,
           lambda: f2.run_on(df, "G1-nocturna", cfg, strat_record),
           "segunda corrida con el mismo pre-registro")

    print("    -- hipótesis obligatoria")
    raises(f2.SpecViolation,
           lambda: pre("G1-nocturna", {"x": 1}, "   "),
           "pre-registro sin hipótesis")
    raises(f2.SpecViolation,
           lambda: pre("INVENTADA", {"x": 1}, "h"),
           "familia no declarada en la spec")

    print("    -- lo que el código no puede impedir, se registra y cobra igual")
    n1 = f2.budget_used()
    f2.log_spec_violation("G2-multidia", {"y": 2}, None, "corrida por fuera de run_on")
    check(f2.budget_used() == n1 + 1, "una violación de spec consume presupuesto igual")


def s3_presupuesto(tmp):
    print("\n[3] §2 — el presupuesto es un tope, y no se transfiere entre familias")
    fresh_ledger(tmp)
    # Esta sección prueba el PRESUPUESTO POR FAMILIA, no la política de §2b:
    # se suspenden el tope de concentración y la cobertura de tenencias, que
    # tienen su propia sección.
    max_c, cob = f2.MAX_CONCENTRACION, f2.COBERTURA_ANTES_DE
    f2.MAX_CONCENTRACION, f2.COBERTURA_ANTES_DE = 1.0, 10 ** 9
    for i in range(f2.FAMILY_BUDGET["G6-terceros"]):
        pre("G6-terceros", {"i": i}, "regla de un tercero")
        f2.abandon("G6-terceros", {"i": i}, "prueba de presupuesto: no se corre")
    check(f2.budget_used("G6-terceros") == 20, "G6 agotó sus 20")
    check(len(f2.open_preregistrations()) == 0, "ninguno quedó colgando")
    check(f2.budget_used("G6-terceros") == 20,
          "abandonar NO devuelve el cartucho (§7.2: los errores también cuestan)")
    raises(f2.BudgetExhausted,
           lambda: pre("G6-terceros", {"i": 999}, "una más"),
           "configuración 21 de G6")
    check(f2.budget_used() == 20 and f2.budget_used("G1-nocturna") == 0,
          "el sobrante de otras familias no rescata a G6 (ni al revés)")
    rep = f2.budget_report()
    check(rep["restante"] == 180, f"restante global {rep['restante']} de {f2.K2}")
    f2.MAX_CONCENTRACION, f2.COBERTURA_ANTES_DE = max_c, cob


def s4_vecindad(tmp):
    print("\n[4] §7.2 — la trampa del bloque 3x3: adoptar una celda cuesta las 9")
    fresh_ledger(tmp)
    best = {"n_before": 4, "m_after": 3}
    cells = [{"n_before": nb, "m_after": ma} for nb in (3, 4, 5) for ma in (2, 3, 4)]
    pre("G2-multidia", best, "publicada; vecindad declarada como robustez",
                   robustness_cells=cells)
    check(f2.budget_used("G2-multidia") == 1,
          "la vecindad declarada NO gasta: 1 cartucho, no 10")
    f2.abandon("G2-multidia", best, "cerrada para probar la adopción")

    print("    -- pero (4,2) daba PF 1.691 contra 1.507 de la publicada. Adoptarla:")
    raises_msg(f2.SpecViolation,
               lambda: pre("G2-multidia", {"n_before": 4, "m_after": 2},
                                      "me gusta más esta"),
               "adoptar una celda de la vecindad sin declararlo",
               must_contain=("celda de robustez", "SELECCIÓN"))

    pre("G2-multidia", {"n_before": 4, "m_after": 2},
                   "adopción consciente de la mejor celda",
                   adopcion_de_vecindad=True)
    check(f2.budget_used("G2-multidia") == 1 + 9 + 1,
          f"la adopción cobró las 9 celdas + la nueva: {f2.budget_used('G2-multidia')} cartuchos")
    check(len(f2.open_preregistrations()) == 1,
          "las 9 celdas cobradas son CARTUCHO, no cuelgan: solo queda abierta la adoptada")


def s5_ventanas(tmp):
    print("\n[5] §4.4 — la ventana está en el código, no en la memoria")
    fresh_ledger(tmp)
    df = synthetic_daily("1995-01-02", "2030-12-31")
    cfg = {"step": 3, "edge_points": 1.0}
    pre("G1-nocturna", cfg, "prueba de ventana")
    f2.run_on(df, "G1-nocturna", cfg, strat_record)
    seen = SEEN["index"]
    check(str(seen.min().date()) >= "2000-09-18",
          f"el dato más viejo que vio la estrategia: {seen.min().date()} (ventana abre 2000-09-18)")
    check(str(seen.max().date()) <= "2019-12-31",
          f"el más nuevo: {seen.max().date()} (parte A cierra 2019-12-31)")
    check(len(df) > len(seen), "el df traía 1995-2030 y la ventana lo recortó sola")

    print("    -- exclusiones fijas: las 10 filas de OHLC incoherente")
    reg = f2.WINDOWS["diario"]
    sliced = reg.slice(df, "A")
    dropped = [d for d in f2.DAILY_INCOHERENT_OHLC
               if pd.Timestamp(d) in df.index and pd.Timestamp(d) not in sliced.index]
    present = [d for d in f2.DAILY_INCOHERENT_OHLC if pd.Timestamp(d) in df.index]
    check(len(dropped) == len(present) and len(present) > 0,
          f"{len(dropped)}/{len(present)} filas incoherentes excluidas siempre")

    print("    -- las 11 de volumen cero: SOLO si la config usa volumen")
    zv = [pd.Timestamp(d) for d in f2.DAILY_ZERO_VOLUME if pd.Timestamp(d) in df.index]
    zv_a = [d for d in zv if pd.Timestamp("2000-09-18") <= d <= pd.Timestamp("2019-12-31")]
    keep = reg.slice(df, "A", uses_volume=False)
    drop = reg.slice(df, "A", uses_volume=True)
    check(all(d in keep.index for d in zv_a) and len(zv_a) > 0,
          f"sin volumen: las {len(zv_a)} filas de volumen cero quedan")
    check(all(d not in drop.index for d in zv_a),
          "con volumen: se excluyen (G1 las declara entre sus filtros)")

    print("    -- régimen intradía bloqueado hasta tener el mapeo de día CME")
    check(f2.INTRADAY_TRADING_DAY_MAPPING_READY is False, "bandera en False, declarada")
    pre("G4-bordes", {"z": 1}, "borde de sesión")
    raises(f2.WindowViolation,
           lambda: f2.run_on(df, "G4-bordes", {"z": 1}, strat_record),
           "G4 con el mapeo pendiente")
    f2.abandon("G4-bordes", {"z": 1}, "régimen intradía bloqueado: mapeo de día CME pendiente")
    check(len(f2.open_preregistrations()) == 0,
          "y el intento bloqueado se cierra con motivo, no queda colgando")


def s6_caja_fuerte(tmp):
    print("\n[6] §3.2/§3.3 — la compuerta de potencia y el uso único de la caja fuerte")
    fresh_ledger(tmp)
    df = synthetic_daily()
    cfg = {"step": 4, "edge_points": 2.0, "noise": 3.0}

    print("    -- CONTROL: en la Fase 1 el examen final se abría con solo pedirlo")
    split = harness.Split("2000-09-18", "2019-12-31", "2020-01-01", "2026-08-19")
    n_b_ctrl = len(f2.vault_uses())
    harness.run_on(df, split, strat_record, cfg, "CONTROL-fase1", examen_final=True)
    check(len(f2.vault_uses()) == n_b_ctrl + 1,
          "Fase 1: examen_final=True y listo, sin compuerta de potencia")

    fresh_ledger(tmp)
    check(len(f2.vault_uses()) == 0,
          "la línea part='B' de la Fase 1 es el autotest sintético y NO cuenta como uso")

    print("    -- sin margen, el examen final de una familia overnight ni arranca")
    pre("G1-nocturna", cfg, "candidata de prueba")
    raises(f2.OperabilityUnknown,
           lambda: f2.run_on(df, "G1-nocturna", cfg, strat_record, examen_final=True),
           "examen final overnight sin margen declarado")
    f2.register_overnight_margin(1234.0, "PRUEBA Tools > Instruments > MES", "2026-08-24")
    check(f2.can_declare_operable("G1-nocturna")[0] is True, "con margen, operable")
    raises(f2.PowerGateNotCleared,
           lambda: f2.run_on(df, "G1-nocturna", cfg, strat_record, examen_final=True),
           "examen final sin power_check aprobado")

    print("    -- un power_check que NO aprueba tampoco abre nada")
    f2.log_power_check("G1-nocturna", cfg, delta_hat=0.1515, n_a=231, n_b_proyectado=80)
    check(f2.approved_power_check("G1-nocturna", cfg) is None,
          "power_check archivado (27.3%) no habilita el examen")
    raises(f2.PowerGateNotCleared,
           lambda: f2.run_on(df, "G1-nocturna", cfg, strat_record, examen_final=True),
           "examen final con potencia insuficiente")

    print("    -- con potencia suficiente, abre UNA vez")
    f2.log_power_check("G1-nocturna", cfg, delta_hat=0.1515, n_a=231, n_b_proyectado=400)
    check(f2.approved_power_check("G1-nocturna", cfg) is not None, "power_check aprobado (n_B=400)")
    res = f2.run_on(df, "G1-nocturna", cfg, strat_record, examen_final=True)
    check(res.trades > 0, f"examen final corrido ({res.trades} operaciones)")
    check(len(f2.vault_uses()) == 1, "un uso registrado")

    print("    -- y no hay segundo examen, para nadie")
    cfg2 = {"step": 6, "edge_points": 1.0}
    pre("G2-multidia", cfg2, "otra candidata")
    f2.log_power_check("G2-multidia", cfg2, delta_hat=0.2, n_a=300, n_b_proyectado=400)
    raises(f2.VaultAlreadyUsed,
           lambda: f2.run_on(df, "G2-multidia", cfg2, strat_record, examen_final=True),
           "segunda candidata pidiendo la caja fuerte")


def s7_barra_y_anios(tmp):
    print("\n[7] §3.1/§3.3 — la barra de la parte A y el registro año por año")
    fresh_ledger(tmp)
    df = synthetic_daily("2000-09-18", "2019-12-31")

    print("    -- una ventaja de puro ruido no pasa")
    t_noise = strat_record(df, {"step": 3, "edge_points": 0.05, "noise": 8.0, "seed": 11})
    r_noise = harness.evaluate_trades(t_noise)
    ok, why, det = f2.passes_bar_a(t_noise, r_noise, n_b_proyectado=600,
                                   neighborhood=[1.02, 0.98, 1.05])
    check(ok is False, f"rechazada, t={det['stat']['t']:.3f}")
    check(any("t " in w for w in why), "la razón nombra el t")
    check(any("pierden plata" in w for w in why), "y la celda de vecindad que pierde")

    print("    -- el caso 'PF 23.7 con 9 operaciones': el mejor 1% afuera lo desarma")
    idx = pd.bdate_range("2010-01-04", periods=200)
    pts = np.full(200, -0.1)
    pts[0] = 400.0                      # una sola operación monstruosa
    t_out = pd.DataFrame({"points": pts, "contracts": 1.0}, index=idx)
    st_all = f2.stat_test(t_out)
    st_drop = f2.stat_test(t_out, drop_best_pct=0.01)
    check(st_all["media"] > 0 and st_drop["media"] < 0,
          f"media ${st_all['media']:.2f} -> ${st_drop['media']:.2f} sacando el mejor 1%")

    print("    -- registro año por año, completo")
    per = f2.report_per_year(t_noise)
    check(len(per) == 20, f"{len(per)} años reportados, uno por año de la parte A")
    check(list(per.columns) == ["operaciones", "neto", "profit_factor", "drawdown", "positivo"],
          "columnas: operaciones, neto, PF, drawdown, positivo")
    pos, tot = f2.years_positive(t_noise)
    check(0 <= pos <= tot and tot == 20,
          f"{pos}/{tot} años positivos — el dato que permite aplicar el 7/7 externo")


def s8_ledger_y_apertura(tmp):
    print("\n[8] §7.5/§9.5 — la cadena sigue entera y la apertura es la firma")
    print("    -- el ledger PUBLICADO verifica con el verificador nuevo")
    f2.set_ledger(PUBLISHED_LEDGER)
    check(f2.verify_ledger() is True, "verify_ledger() sobre el archivo publicado: True")
    filas = f2.read_ledger()
    fase1 = [e for e in filas if e.get("phase") != 2]
    check(len(fase1) == 60, f"las 60 líneas de la Fase 1 intactas (total hoy: {len(filas)})")
    check(sum(1 for e in filas if e.get("kind") == "APERTURA_FASE2") == 1,
          "exactamente un acta de apertura, nunca dos")
    check(f2.phase2_is_open() is True, "la Fase 2 está abierta en el ledger real")

    fresh_ledger(tmp)
    pre("G3-regimen", {"q": 1}, "estado de volatilidad")
    f2.log_spec_violation("G3-regimen", {"q": 2}, None, "prueba")
    check(f2.verify_ledger() is True, "la cadena sigue válida tras anexar entradas de Fase 2")

    print("    -- editar una línea vieja rompe la cadena (control)")
    path = f2.LEDGER_PATH
    rows = [json.loads(x) for x in open(path, encoding="utf-8") if x.strip()]
    rows[30]["result"] = {"trades": 999}
    with open(path, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    check(f2.verify_ledger() is False, "manosear el pasado se nota")

    fresh_ledger(tmp)
    print("    -- dry_run muestra el acta sin escribir nada")
    n_antes = len(f2.read_ledger())
    prev = f2.open_phase2(data_dir=os.path.join(REPO, "data"), dry_run=True)
    check(len(f2.read_ledger()) == n_antes, "dry_run no anexó ninguna línea")
    check(f2.phase2_is_open() is False, "y la fase sigue cerrada en el ledger temporal")
    check(prev["prev"] == f2.read_ledger()[-1]["hash"],
          "el acta previsualizada engancha al último hash real del ledger")

    print("    -- apertura sin el margen: abre, y G1 queda bloqueada")
    e = f2.open_phase2(data_dir=os.path.join(REPO, "data"))
    check(f2.phase2_is_open() is True, "entrada APERTURA_FASE2 escrita")
    check(e["K_total"] == 257 and e["alpha"] == 0.05, "K_total y α quedan en el acta")
    check(e["margen_nocturno_mes"]["estado"] == "AUSENTE",
          "el margen queda AUSENTE explícito")
    check(e["margen_nocturno_mes"]["valor_usd"] is None,
          "nunca en cero ni con un valor provisorio")
    check(f2.g1_enabled() is False, "G1 bloqueada (§7.3)")
    check("BLOQUEADA" in e["note"], "y el acta lo dice con todas las letras")
    check(isinstance(e["data_sha256"], dict) and len(e["data_sha256"]) == 3,
          "los SHA-256 de los tres archivos de datos quedan congelados")
    check(f2.verify_ledger() is True, "cadena válida después de la apertura")
    check({k: v for k, v in prev.items() if k not in ("prev", "_dry_run")} ==
          {k: v for k, v in e.items() if k not in ("ts", "prev", "hash")},
          "lo que mostró dry_run es exactamente lo que se escribió")

    print("    -- el margen llega después, como entrada propia y fechada")
    raises(f2.SpecViolation,
           lambda: f2.register_overnight_margin(0, "NinjaTrader", "2026-08-23"),
           "margen en cero")
    raises(f2.SpecViolation,
           lambda: f2.register_overnight_margin(1234.0, "", "2026-08-23"),
           "margen sin fuente")
    raises(f2.SpecViolation,
           lambda: f2.register_overnight_margin(1234.0, "NinjaTrader", ""),
           "margen sin fecha de lectura")
    check(f2.g1_enabled() is False, "ninguno de los intentos fallidos habilitó G1")

    m = f2.register_overnight_margin(1234.0, "PRUEBA Tools > Instruments > MES",
                                     "2026-08-23")
    check(m["kind"] == "COSTO_MARGEN", "entra como entrada de COSTO, no como regla")
    check(f2.g1_enabled() is True, "y ahí sí G1 se habilita")
    check(f2.overnight_margin()["valor_usd"] == 1234.0, "el valor queda consultable")
    check(f2.verify_ledger() is True, "cadena válida con el margen adentro")


def s9_colgados(tmp):
    print("\n[9] §7.2 — un pre-registro sin resolver bloquea el siguiente")
    print("    Desde afuera del repo, 'pre-registrado y nunca corrido' es")
    print("    indistinguible de 'corrido, salió feo y no escribí el resultado'.")
    fresh_ledger(tmp)
    df = synthetic_daily()
    cfg_a = {"step": 5, "edge_points": 1.0}
    cfg_b = {"step": 7, "edge_points": 1.0}

    e = pre("G1-nocturna", cfg_a, "primera hipótesis")
    check(len(f2.open_preregistrations()) == 1, "queda 1 pre-registro abierto")

    print("    -- CONTROL DE MUTACIÓN: lo dejo colgando y pido el siguiente")
    msg = raises_msg(f2.SpecViolation,
                     lambda: pre("G1-nocturna", cfg_b, "segunda hipótesis"),
                     "preregister() con uno sin resolver",
                     must_contain=("sin resolver", "G1-nocturna", e["hash"]))
    check('"step": 5' in msg, "el mensaje nombra la config exacta que quedó abierta")
    check("abandon(" in msg, "y dice cómo cerrarla")
    check(f2.budget_used() == 1, "el bloqueado no gastó cartucho")

    print("    -- salida 1 de 3: el resultado lo resuelve")
    f2.run_on(df, "G1-nocturna", cfg_a, strat_record)
    check(len(f2.open_preregistrations()) == 0, "resuelto por RESULTADO")
    pre("G1-nocturna", cfg_b, "segunda hipótesis")
    check(len(f2.open_preregistrations()) == 1, "ahora sí deja abrir el siguiente")

    print("    -- salida 2 de 3: el abandono, con motivo obligatorio")
    raises(f2.SpecViolation,
           lambda: f2.abandon("G1-nocturna", cfg_b, "  "),
           "abandonar sin motivo escrito")
    used = f2.budget_used()
    ab = f2.abandon("G1-nocturna", cfg_b, "error de diseño: el filtro deja 0 operaciones")
    check(len(f2.open_preregistrations()) == 0, "resuelto por ABANDONO")
    check(ab["motivo"].startswith("error de diseño"), "el motivo queda escrito en el ledger")
    check(f2.budget_used() == used, "y el cartucho no se devuelve")
    raises(f2.SpecViolation,
           lambda: f2.abandon("G1-nocturna", cfg_b, "otra vez"),
           "abandonar algo que ya está resuelto")

    print("    -- salida 3 de 3: la violación de spec también lo cierra, sin cobrar dos veces")
    cfg_c = {"step": 9, "edge_points": 1.0}
    pre("G2-multidia", cfg_c, "tercera hipótesis")
    used = f2.budget_used()
    v = f2.log_spec_violation("G2-multidia", cfg_c, None, "corrida por fuera de run_on")
    check(v.get("prereg") is not None, "la violación enlaza al pre-registro que resuelve")
    check(len(f2.open_preregistrations()) == 0, "resuelto por VIOLACION")
    check(f2.budget_used() == used, "no cobra dos veces: el cartucho ya se había pagado")

    print("    -- y una corrida que revienta NO deja el pre-registro resuelto")
    pre("G4-bordes", {"z": 2}, "borde de sesión")
    try:
        f2.run_on(df, "G4-bordes", {"z": 2}, strat_record)
    except f2.WindowViolation:
        pass
    check(len(f2.open_preregistrations()) == 1,
          "la corrida falló y el pre-registro sigue abierto: hay que cerrarlo a mano")
    raises(f2.SpecViolation,
           lambda: pre("G1-nocturna", {"step": 11}, "otra"),
           "y mientras tanto bloquea todo lo demás")
    check(f2.verify_ledger() is True, "cadena válida con las tres salidas dentro")


def s10_reglas_congeladas(tmp):
    print("\n[10] §9.5 — las REGLAS se congelan igual que los datos")
    fresh_ledger(tmp)
    e = f2.open_phase2(data_dir=os.path.join(REPO, "data"))
    rh = e["rules_sha256"]
    check(len(rh) == 3, f"el acta congela {len(rh)} archivos de reglas")
    check(all("spec_fase2.md" in k or "harness" in k for k in rh),
          f"y son los que definen las reglas: {sorted(k.split('/')[-1] for k in rh)}")
    check(all(v["sha256"] for v in rh.values()), "los tres con SHA-256 real")
    check(len(e["rules_digest"]) == 16, f"huella corta de las reglas: {e['rules_digest']}")
    check(e.get("git_commit") is not None,
          "y el commit del repo, que cubre lo que todavía no se escribió")

    print("    -- cada entrada de Fase 2 queda sellada con esa huella")
    pre("G2-multidia", {"a": 1}, "prueba de sellado")
    ult = f2.read_ledger()[-1]
    check(ult["rules_digest"] == e["rules_digest"],
          "el pre-registro lleva la misma huella que el acta")

    print("    -- si una constante congelada cambia, el harness se planta")
    orig = f2.K2
    try:
        f2.K2 = 240
        raises_msg(f2.SpecViolation,
                   lambda: f2.run_on(synthetic_daily(), "G2-multidia", {"a": 1},
                                     strat_record),
                   "correr con K2 cambiado después de firmar",
                   must_contain=("congeladas", "K2"))
    finally:
        f2.K2 = orig
    check(f2.K2 == 200, "K2 restaurado para el resto de las pruebas")

    print("    -- y una deriva de reglas queda a la vista (no bloquea, se publica)")
    d = f2.rules_drift()
    check(d["cambiados"] == {}, "sin deriva ahora mismo")
    check(d["digest_acta"] == d["digest_ahora"], "huella del acta == huella de hoy")


def s11_margen_despliegue(tmp):
    print("\n[11] §7.3 — el margen es restricción de DESPLIEGUE, no de investigación")
    fresh_ledger(tmp)
    f2.open_phase2(data_dir=os.path.join(REPO, "data"))
    df = synthetic_daily()
    cfg = {"step": 5, "edge_points": 1.0}

    print("    -- sin margen, la BÚSQUEDA de una familia overnight corre igual")
    check(f2.overnight_margin() is None, "no hay margen registrado")
    pre("G2-multidia", cfg, "el margen no cambia ningún número del backtest")
    res = f2.run_on(df, "G2-multidia", cfg, strat_record)
    check(res.trades > 0, f"G2 corrió sin margen ({res.trades} operaciones)")
    ult = f2.read_ledger()[-1]
    check(ult["operable"] is False,
          "y el resultado queda sellado como NO operable-verificable")

    print("    -- pero el examen final no: gastar el único uso en algo inoperable, no")
    check(f2.can_declare_operable("G2-multidia")[0] is False, "G2 no declarable operable")
    check(f2.can_declare_operable("G4-bordes")[0] is True, "G4 es intradía: no aplica")

    print("    -- SALVAGUARDA: el margen se registra UNA vez y es inmutable")
    f2.register_overnight_margin(2000.0, "PRUEBA > Instruments > MES", "2026-08-24")
    check(f2.can_declare_operable("G2-multidia")[0] is True, "ahora sí es declarable")
    raises_msg(f2.SpecViolation,
               lambda: f2.register_overnight_margin(1500.0, "otro bróker", "2026-08-25"),
               "segundo margen sin motivo de revisión",
               must_contain=("INMUTABLE",))

    print("    -- una revisión A LA BAJA con resultados en el ledger: RECHAZADA")
    msg = raises_msg(f2.SpecViolation,
                     lambda: f2.register_overnight_margin(
                         1500.0, "bróker con menos margen", "2026-08-25",
                         revision_motivo="conseguí uno más barato"),
                     "bajar el margen después de tener resultados",
                     must_contain=("A LA BAJA", "peeking"))
    check("elegir el bróker en vez de la ventana" in msg,
          "y el mensaje nombra exactamente qué trampa es")

    print("    -- una revisión legítima al alza entra, y NO reemplaza a la anterior")
    f2.register_overnight_margin(2600.0, "PRUEBA > Instruments > MES", "2026-09-01",
                                 revision_motivo="el bróker subió el requisito")
    hist = f2.overnight_margin_history()
    check(len(hist) == 2, f"quedan las dos entradas: {[h['valor_usd'] for h in hist]}")
    check(f2.overnight_margin()["valor_usd"] == 2600.0, "vigente = la última")
    check(hist[0]["valor_usd"] == 2000.0, "la vieja sigue en el ledger, no se borró")
    viejo = hist[0]["_hash"]
    sellados = [e for e in f2.read_ledger() if e.get("margen_vigente") == viejo]
    check(len(sellados) == 0,
          "el resultado de G2 se corrió SIN margen, y así quedó sellado")
    check(f2.verify_ledger() is True, "cadena válida")


def s12_bloqueantes(tmp):
    print("\n[12] §7.6 — un campo bloqueante sin fecha es un pendiente eterno")
    fresh_ledger(tmp)
    e = f2.open_phase2(data_dir=os.path.join(REPO, "data"))
    bl = e["bloqueantes"]
    check(set(bl) == {"margen_nocturno_mes", "mapeo_dia_cme"},
          f"el acta declara los dos bloqueantes: {sorted(bl)}")
    check(bl["margen_nocturno_mes"]["vence_el"] is not None,
          f"el margen tiene fecha de vencimiento: {bl['margen_nocturno_mes']['vence_el']}")
    check(bl["margen_nocturno_mes"]["plazo_dias"] == 14, "14 días")
    check(bl["mapeo_dia_cme"]["vence_el"] is None
          and bl["mapeo_dia_cme"]["clock"] == "cierre de G3-regimen",
          "el mapeo CME no tiene reloj todavía: su turno no llegó")
    check("al_vencer" in bl["margen_nocturno_mes"], "y cada uno dice qué pasa al vencer")

    st = {b["bloqueante"]: b for b in f2.blocking_status()}
    check(st["margen_nocturno_mes"]["estado"] == "VIGENTE", "margen: VIGENTE")
    check(st["mapeo_dia_cme"]["estado"] == "SIN_RELOJ", "mapeo: SIN_RELOJ")
    check(len(f2.overdue_blockers()) == 0, "nada vencido hoy")

    print("    -- pasado el plazo sin resolver, se detiene TODA la búsqueda")
    vence = bl["margen_nocturno_mes"]["vence_el"]
    tarde = f2._plus_days(vence, 1)
    check(len(f2.overdue_blockers(today=tarde)) == 1, f"al {tarde} hay 1 vencido")
    real_today = f2._today
    try:
        f2._today = lambda: tarde
        raises_msg(f2.SpecViolation,
                   lambda: pre("G2-multidia", {"b": 1}, "hipótesis"),
                   "pre-registrar con un bloqueante vencido",
                   must_contain=("VENCIDO", "margen_nocturno_mes"))
    finally:
        f2._today = real_today

    print("    -- resolverlo lo cierra")
    f2.register_overnight_margin(2000.0, "PRUEBA", "2026-08-24")
    st = {b["bloqueante"]: b for b in f2.blocking_status(today=tarde)}
    check(st["margen_nocturno_mes"]["estado"] == "RESUELTO", "margen: RESUELTO")
    check(len(f2.overdue_blockers(today=tarde)) == 0, "y ya no detiene nada")

    print("    -- la otra salida: fuera de alcance, con los cartuchos PERDIDOS")
    fresh_ledger(tmp)
    f2.open_phase2(data_dir=os.path.join(REPO, "data"))
    pre("G6-terceros", {"c": 1}, "una regla de un amigo")
    f2.abandon("G6-terceros", {"c": 1}, "el amigo nunca mandó la regla")
    oos = f2.declare_out_of_scope("G6-terceros",
                                  "nadie respondió el cuestionario en el plazo")
    check(oos["cartuchos_perdidos"] == 19, f"{oos['cartuchos_perdidos']} cartuchos perdidos")
    check(oos["K_total_sigue_en"] == 257, "y K_total sigue en 257: el listón no se mueve")
    rep_ = f2.budget_report()
    check(rep_["K_total"] == 257 and rep_["perdidos_fuera_de_alcance"] == 19,
          "el reporte los muestra como perdidos, no como devueltos")
    check(rep_["restante"] == 200 - 1 - 19, f"restante {rep_['restante']}")
    raises_msg(f2.SpecViolation,
               lambda: pre("G6-terceros", {"c": 2}, "otra"),
               "pre-registrar en una familia fuera de alcance",
               must_contain=("FUERA DE ALCANCE",))
    raises(f2.SpecViolation,
           lambda: f2.declare_out_of_scope("G6-terceros", "  "),
           "salir de alcance sin motivo escrito")
    check(f2.verify_ledger() is True, "cadena válida")


def s13_criba_medibilidad(tmp):
    print("\n[13] §3.5 — cribar por MEDIBILIDAD es legítimo; por RENDIMIENTO no")
    fresh_ledger(tmp)
    check(f2.n_b_needed(f2.DELTA_REF_BEST) == 342,
          f"a delta {f2.DELTA_REF_BEST} hacen falta {f2.n_b_needed(f2.DELTA_REF_BEST)} "
          "operaciones — el mismo 342 que BOT C publicó para F4")
    check(abs(f2.DELTA_REF_BEST_GROSS - (25.30 + 3.90) / 166.95) < 1e-4,
          f"referencia BRUTA {f2.DELTA_REF_BEST_GROSS} = (25.30+3.90)/166.95 — "
          "la criba compara bruto contra bruto")
    check(f2.n_b_needed(f2.DELTA_REF_TYPICAL) == 1121,
          f"a delta {f2.DELTA_REF_TYPICAL} hacen falta {f2.n_b_needed(f2.DELTA_REF_TYPICAL)}")

    print("    -- el contador de frecuencia devuelve un int: el P&L no sale de ahí")
    df = synthetic_daily("2000-09-18", "2019-12-31")
    n = f2.count_trades_only(strat_record, df, {"step": 5, "edge_points": 99.0})
    check(isinstance(n, int) and n > 0, f"count_trades_only -> {n} (int)")
    n2 = f2.count_trades_only(strat_record, df, {"step": 5, "edge_points": -99.0})
    check(n == n2,
          "la frecuencia NO cambia al invertir el signo del P&L: es una propiedad "
          "del mercado, no de si la regla gana")

    print("    -- sin criba, la familia no puede gastar un cartucho")
    fresh_ledger(tmp)
    ledger = f2.LEDGER_PATH
    filas = [l for l in io.open(ledger, encoding="utf-8") if l.strip()
             and json.loads(l).get("kind") != "MEDIBILIDAD"]
    with io.open(ledger, "w", encoding="utf-8") as fh:
        fh.writelines(filas)
    raises_msg(f2.SpecViolation,
               lambda: pre("G1-nocturna", {"z": 1}, "hipótesis"),
               "pre-registrar sin criba de medibilidad de la FAMILIA",
               must_contain=("criba de medibilidad", "no gasta presupuesto"))

    print("    -- una familia NO VALIDABLE no puede gastar sus cartuchos")
    used = f2.budget_used()
    e = f2.log_measurability_screen(
        "G1-nocturna", 100,
        "techo estructural de prueba: 100 operaciones en B",
        sigma_por_operacion=200.0)
    check(e["screen"]["validable"] is False,
          "exige mas que la referencia bruta: NO VALIDABLE")
    check(f2.budget_used() == used, "y la criba NO consumió presupuesto")
    check(abs(e["screen"]["exigido_bruto_sigma"] - (2.8016 / 10 + 3.90 / 200)) < 1e-3,
          f"exigido bruto {e['screen']['exigido_bruto_sigma']:.4f} = potencia + fricción")

    print("    -- y una criba SIN sigma se niega: ignorar la fricción era el bug")
    raises_msg(f2.SpecViolation,
               lambda: f2.log_measurability_screen("G1-nocturna", 100, "sin sigma"),
               "criba sin sigma por operación",
               must_contain=("ignora la fricción",))
    raises_msg(f2.SpecViolation,
               lambda: pre("G1-nocturna", {"z": 1}, "hipótesis"),
               "pre-registrar en una familia NO VALIDABLE",
               must_contain=("NO VALIDABLE", "fricción"))

    print("    -- y sacarla de alcance pierde los cartuchos, sin mover el listón")
    oos = f2.declare_not_validable(
        "G1-nocturna", "techo de 100 operaciones contra 342 necesarias")
    check(oos["cartuchos_perdidos"] == 40, "los 40 de G1 se pierden")
    check(oos["K_total_sigue_en"] == 257, "K_total sigue en 257")
    rep_ = f2.budget_report()
    check(rep_["perdidos_fuera_de_alcance"] == 40 and rep_["K_total"] == 257,
          "perdidos, no devueltos y no reasignados (§1.4 + §2)")
    check(f2.verify_ledger() is True, "cadena válida")


def s14_criba_por_config(tmp):
    print("\n[14] \u00a73.5b \u2014 la criba corre por FAMILIA, el cartucho se gasta por CONFIGURACI\u00d3N")
    fresh_ledger(tmp)
    df = synthetic_daily()          # abarca A y B: la proyeccion necesita las dos

    print("    -- una config demasiado infrecuente se RECHAZA, y no cobra")
    used = f2.budget_used()
    msg = raises_msg(
        f2.SpecViolation,
        lambda: f2.preregister("G2-multidia", {"step": 60}, "dispara poqu\u00edsimo",
                               mecanismo="reversion-lenta", h=1.0,
                               strategy_fn=strat_record, df=df),
        "config con n_B por debajo de la potencia",
        must_contain=("RECHAZADA por medibilidad", "NO se cobr\u00f3 el cartucho"))
    check(f2.budget_used() == used, "el rechazo NO gast\u00f3 cartucho")
    check("Fuente del conteo" in msg, "y el mensaje dice de d\u00f3nde sali\u00f3 el conteo")

    print("    -- una config frecuente pasa, y su criba queda guardada")
    e = f2.preregister("G2-multidia", {"step": 2}, "dispara seguido",
                       mecanismo="reversion-rapida", h=1.0,
                       strategy_fn=strat_record, df=df)
    cm = e["medibilidad_config"]
    check(cm["medible"] is True, f"medible: n_B {cm['n_b_proyectado']} >= {cm['n_b_necesario']}")
    check(cm["n_a_contado"] > 0, f"n_A contado: {cm['n_a_contado']}")
    check("contado sobre la parte A" in cm["fuente"], "con su fuente escrita")
    check(f2.budget_used() == used + 1, "y reci\u00e9n ah\u00ed cobra")

    print("    -- sin conteo ni techo declarado: fail-closed")
    f2.abandon("G2-multidia", {"step": 2}, "cierre de prueba")
    raises_msg(f2.SpecViolation,
               lambda: f2.preregister("G2-multidia", {"step": 3}, "sin criba",
                                      mecanismo="reversion-x", h=1.0),
               "pre-registrar sin criba de configuraci\u00f3n",
               must_contain=("sin criba de medibilidad de la configuraci\u00f3n",))

    print("    -- el contrafactual del cartucho 1 (n_B 84 contra 342)")
    cm1 = f2.config_measurability(84)
    check(cm1["medible"] is False,
          f"n_B 84 < {cm1['n_b_necesario']}: bajo esta regla el cartucho 1 se rechazaba")
    check(abs(cm1["delta_min_detectable"] - 0.3057) < 0.001,
          f"s\u00f3lo pod\u00eda validar efectos de \u03b4 >= {cm1['delta_min_detectable']:.4f}, "
          "el doble del mejor que el proyecto midi\u00f3 jam\u00e1s")


def s15_direccion_de_los_cambios(tmp):
    print("\n[15] \u00a79.5c \u2014 la deriva puede ENDURECER pero no aflojar sin que se note")
    fresh_ledger(tmp)
    e = f2.log_rules_change("ENDURECE", "criba de medibilidad", "agrega una compuerta",
                            seccion="\u00a73.5")
    check(e["direccion"] == "ENDURECE", "un cambio que endurece se registra y basta")
    check(e["aprobado_por"] is None, "no necesita aprobaci\u00f3n explícita")

    print("    -- uno que AFLOJA sin aprobaci\u00f3n explícita: rechazado")
    raises_msg(f2.SpecViolation,
               lambda: f2.log_rules_change("AFLOJA", "bajar el PF exigido",
                                           "queda m\u00e1s lindo"),
               "aflojar sin aprobaci\u00f3n",
               must_contain=("aprobaci\u00f3n expl\u00edcita", "veredicto"))
    raises(f2.SpecViolation,
           lambda: f2.log_rules_change("MEJORA", "x", "y"),
           "direcci\u00f3n inventada")
    raises(f2.SpecViolation,
           lambda: f2.log_rules_change("ENDURECE", "x", "  "),
           "cambio sin argumento escrito")

    a = f2.log_rules_change("AFLOJA", "ejemplo", "para probar el rastro",
                            aprobado_por="Roberto")
    check(a["aprobado_por"] == "Roberto", "con aprobaci\u00f3n, entra")
    check(len(f2.loosening_changes()) == 1,
          "y queda listado aparte: el veredicto lo publica s\u00ed o s\u00ed")
    check(len(f2.rules_changes()) == 2, "dos cambios clasificados en total")

    print("    -- el pasado no se edita: se le anexa")
    pr = pre("G1-nocturna", {"q": 9}, "hip\u00f3tesis")
    antes = [dict(x) for x in f2.read_ledger()]
    n = f2.log_retro_note(pr["hash"], "esta config no habr\u00eda pasado la criba nueva",
                          motivo="regla agregada despu\u00e9s")
    check(n["sobre"] == pr["hash"], "la nota referencia la entrada original")
    ahora = f2.read_ledger()
    check(ahora[:len(antes)] == antes, "y NINGUNA l\u00ednea previa cambi\u00f3")
    raises(f2.SpecViolation,
           lambda: f2.log_retro_note("no-existe", "nota"),
           "anotar una entrada inexistente")
    check(f2.verify_ledger() is True, "cadena v\u00e1lida")


def s16_politica_asignacion(tmp):
    print("\n[16] \u00a72b \u2014 buscar concentra, medir dispersa")
    fresh_ledger(tmp)
    df = synthetic_daily()

    print("    -- mecanismo y tenencia son obligatorios en el pre-registro")
    raises_msg(f2.SpecViolation,
               lambda: f2.preregister("G1-nocturna", {"a": 1}, "hip",
                                      n_b_proyectado=5000, n_b_fuente="fx"),
               "pre-registro sin mecanismo",
               must_contain=("sin `mecanismo`", "un voto por MECANISMO"))
    raises_msg(f2.SpecViolation,
               lambda: f2.preregister("G1-nocturna", {"a": 1}, "hip",
                                      mecanismo="m", n_b_proyectado=5000,
                                      n_b_fuente="fx"),
               "pre-registro sin tenencia h",
               must_contain=("sin `h`", "estratificar"))

    print("    -- estratos de tenencia")
    for h, esperado in ((0.08, "intradia"), (1, "corto"), (3, "medio"), (10, "largo")):
        check(f2.estrato_de(h) == esperado, f"h={h} -> {f2.estrato_de(h)}")

    print("    -- tope de concentracion por MECANISMO")
    for i in range(4):
        pre("G1-nocturna", {"i": i}, "hip", mecanismo=f"mec-{i}", h=1.0)
        f2.abandon("G1-nocturna", {"i": i}, "cierre")
    check(f2.budget_used() == 4, "4 cartuchos, cuatro mecanismos distintos")
    for i in range(4, 6):
        pre("G2-multidia", {"i": i}, "hip", mecanismo="mec-repetido", h=3.0)
        f2.abandon("G2-multidia", {"i": i}, "cierre")
    msg = raises_msg(f2.SpecViolation,
                     lambda: pre("G2-multidia", {"i": 99}, "hip",
                                 mecanismo="mec-repetido", h=3.0),
                     "un mecanismo pasandose del 40%",
                     must_contain=("tope de concentraci\u00f3n", "mec-repetido"))
    check("40%" in msg, "y el mensaje dice cual es el tope")

    print("    -- el agujero cerrado: inventar un mecanismo por config no evade el tope")
    msg = raises_msg(f2.SpecViolation,
                     lambda: pre("G2-multidia", {"i": 100}, "hip",
                                 mecanismo="mecanismo-nuevo-inventado", h=3.0),
                     "misma familia con mecanismo nuevo cada vez",
                     must_contain=("tope de concentraci\u00f3n", "familia"))
    check("G2-multidia" in msg, "el tope por FAMILIA lo atrapa igual")

    print("    -- cobertura de tenencias antes del cartucho 20")
    fresh_ledger(tmp)
    f2.MAX_CONCENTRACION = 1.0
    try:
        for i in range(f2.COBERTURA_ANTES_DE - 1):
            pre("G1-nocturna", {"i": i}, "hip", mecanismo=f"m{i}", h=1.0)
            f2.abandon("G1-nocturna", {"i": i}, "cierre")
        cub = f2.estratos_cubiertos()
        check(set(cub) == {"corto"}, f"solo el estrato corto cubierto: {sorted(cub)}")
        raises_msg(f2.SpecViolation,
                   lambda: pre("G1-nocturna", {"i": 999}, "hip",
                               mecanismo="m999", h=1.0),
                   "cartucho 20 sin cubrir los estratos",
                   must_contain=("cobertura de tenencias", "medio", "largo"))
        check(True, "y solo se admiten los que COMPLETAN cobertura, no se traba sola")
        print("    -- y cubriendolos, deja pasar")
        pre("G1-nocturna", {"i": 900}, "hip", mecanismo="m900", h=3.0)
        f2.abandon("G1-nocturna", {"i": 900}, "cierre")
        pre("G1-nocturna", {"i": 901}, "hip", mecanismo="m901", h=8.0)
        f2.abandon("G1-nocturna", {"i": 901}, "cierre")
        cub = f2.estratos_cubiertos()
        check({"corto", "medio", "largo"} <= set(cub),
              f"tres estratos cubiertos: {sorted(cub)}")
        e = pre("G1-nocturna", {"i": 902}, "hip", mecanismo="m902", h=1.0)
        check(e["estrato_h"] == "corto", "y el cartucho 22 pasa, con su estrato anotado")
    finally:
        f2.MAX_CONCENTRACION = 0.40
    check(f2.verify_ledger() is True, "cadena v\u00e1lida")


def s17_solo_medicion(tmp):
    print("\n[17] \u00a73.6 \u2014 fuera de alcance para BUSCAR no es inutil para MEDIR")
    fresh_ledger(tmp)
    df = synthetic_daily()

    print("    -- una familia NO VALIDABLE no puede gastar cartuchos...")
    f2.log_measurability_screen("G4-bordes", 3338,
                                "2 tramos de 30 min por sesion",
                                sigma_por_operacion=22.08)
    check(f2.screened_families()["G4-bordes"]["screen"]["validable"] is False,
          "G4 sigue NO VALIDABLE con la friccion adentro")
    raises(f2.SpecViolation,
           lambda: pre("G4-bordes", {"x": 1}, "hip", mecanismo="bordes", h=0.08),
           "pre-registrar en G4 antes de reclasificarla")

    print("    -- ...hasta que se la reclasifica, y eso EXIGE aprobacion (AFLOJA)")
    raises_msg(f2.SpecViolation,
               lambda: f2.declare_measurement_only("G4-bordes", "cubrir el estrato corto", ""),
               "SOLO_MEDICION sin aprobacion explicita",
               must_contain=("aprobacion explicita", "AFLOJA"))
    e = f2.declare_measurement_only(
        "G4-bordes", "unico estrato de tenencia sin ningun dato", "Roberto")
    check(e["kind"] == "SOLO_MEDICION", "estado propio, distinto de FUERA_DE_ALCANCE")
    check("G4-bordes" not in f2.out_of_scope_families(),
          "y NO es fuera de alcance: sus cartuchos no se perdieron")

    print("    -- condicion 2: consume cartucho igual (revela rentabilidad)")
    antes = f2.budget_used()
    p = pre("G4-bordes", {"x": 1}, "borde de sesion", mecanismo="bordes", h=0.08)
    check(f2.budget_used() == antes + 1, "gasto un cartucho, como cualquier otro")
    check(p["solo_medicion"] is True and p["nunca_candidata"] is True,
          "el pre-registro queda marcado nunca_candidata")
    check(p["estrato_h"] == "intradia",
          "y en el estrato intradia, el unico sin ningun dato")

    print("    -- condicion 1: no puede abrir la caja fuerte, nunca")
    f2.log_power_check("G4-bordes", {"x": 1}, delta_hat=0.5, n_a=1000, n_b_proyectado=3338)
    raises_msg(f2.SpecViolation,
               lambda: f2.run_on(df, "G4-bordes", {"x": 1}, strat_record,
                                 examen_final=True),
               "G4 pidiendo el examen final",
               must_contain=("SOLO_MEDICION", "NUNCA"))

    print("    -- condicion 3: la config corrida queda vedada PARA SIEMPRE")
    f2.abandon("G4-bordes", {"x": 1}, "cierre de prueba")
    check(_cfg_en_vedadas(p), "la config figura entre las vedadas")
    raises_msg(f2.SpecViolation,
               lambda: pre("G4-bordes", {"x": 1}, "otra vez", mecanismo="bordes",
                           h=0.08),
               "re-registrar una config ya medida",
               must_contain=("VEDADA PARA SIEMPRE", "despues de ver su resultado"))
    check(f2.verify_ledger() is True, "cadena v\u00e1lida")


def _cfg_en_vedadas(prereg):
    import json as _j
    clave = prereg["family"] + "|" + _j.dumps(prereg["config"], sort_keys=True)
    return clave in f2.measurement_only_configs()


def s18_vara_de_filtros(tmp):
    print("\n[18] \u00a73.7 \u2014 la vara de un filtro es una FUNCION de (phi, h_residuo)")
    fresh_ledger(tmp)

    print("    -- la vara varia a lo largo de la cuenca: la tabla en h=1 dejaba pasar")
    b037 = f2.filter_bar(0.5, 0.3737)
    b100 = f2.filter_bar(0.5, 1.0)
    b131 = f2.filter_bar(0.5, 1.3171)
    check(abs(b037["concentracion_min"] - 1.1440) < 1e-3,
          f"h=0.3737 -> {b037['concentracion_min']:.4f}x")
    check(abs(b100["concentracion_min"] - 1.2434) < 1e-3,
          f"h=1.0000 -> {b100['concentracion_min']:.4f}x  (la tabla publicada)")
    check(abs(b131["concentracion_min"] - 1.2703) < 1e-3,
          f"h=1.3171 -> {b131['concentracion_min']:.4f}x")
    check(b131["concentracion_min"] > b100["concentracion_min"],
          "un residuo mas largo exige MAS concentracion: la tabla en h=1 subestimaba")

    print("    -- un filtro que pasaba con la tabla vieja y NO paga con la funcion")
    raises_msg(f2.SpecViolation,
               lambda: pre("G3-regimen", {"q": 1}, "estado de mediana",
                           mecanismo="regimen-vol", h=1.3171,
                           phi=0.5, psi=0.63, h_residuo=1.3171),
               "psi=0.63 (concentracion 1.26x) con h_residuo=1.3171",
               must_contain=("no paga su costo de frecuencia", "h_residuo"))
    check(0.63 / 0.5 > b100["concentracion_min"],
          "1.26x superaba la vara vieja de h=1 (1.2434x) — por eso importa")
    check(0.63 / 0.5 < b131["concentracion_min"],
          f"y no llega a la vara real de h=1.3171 ({b131['concentracion_min']:.4f}x)")

    print("    -- los tres numeros son obligatorios; sin h_residuo no hay hipotesis")
    raises_msg(f2.SpecViolation,
               lambda: f2.preregister("G3-regimen", {"q": 2}, "hip",
                                      mecanismo="m", h=1.0, phi=0.5, psi=0.9,
                                      n_b_proyectado=834, n_b_fuente="fx"),
               "filtro sin h_residuo",
               must_contain=("familia de FILTRO", "h_residuo"))
    raises(f2.SpecViolation,
           lambda: f2.filter_bar(0.5, 0),
           "h_residuo no positivo")
    raises(f2.SpecViolation,
           lambda: f2.filter_bar(1.5, 1.0),
           "phi fuera de (0,1]")

    print("    -- un filtro que SI paga entra, y su vara queda guardada")
    e = pre("G3-regimen", {"q": 3}, "estado de mediana que concentra 1.8x",
            mecanismo="regimen-vol", h=1.0, phi=0.5, psi=0.9, h_residuo=1.0)
    check(e["filtro"]["concentracion_declarada"] > e["filtro"]["concentracion_min"],
          f"declarada {e['filtro']['concentracion_declarada']:.2f}x > vara "
          f"{e['filtro']['concentracion_min']:.4f}x")
    check(e["filtro"]["h_residuo"] == 1.0, "y h_residuo queda en el ledger")
    f2.abandon("G3-regimen", {"q": 3}, "cierre de prueba")

    print("    -- las familias que NO son filtro no tienen que declarar nada de esto")
    e2 = pre("G2-multidia", {"q": 4}, "no es filtro", mecanismo="reversion", h=1.0)
    check(e2["filtro"] is None, "G2 no lleva vara de filtro")
    check(f2.verify_ledger() is True, "cadena v\u00e1lida")


def s19_estimador_y_formula(tmp):
    print("\n[19] \u00a73.8 \u2014 el estimador de c y la formula publicada")

    print("    -- la distribucion t, contra su forma cerrada en df=1 (Cauchy)")
    import math
    for t0 in (0.5, 1.6422, 3.0):
        cerrada = 1 - (2 / math.pi) * math.atan(t0)
        check(abs(f2.t_p_two_sided(t0, 1) - cerrada) < 1e-6,
              f"t={t0}: integracion {f2.t_p_two_sided(t0,1):.6f} = cerrada {cerrada:.6f}")
    check(abs(f2.t_crit(1, 0.05) - 12.7062) < 1e-2,
          f"t critico df=1 al 95% = {f2.t_crit(1,0.05):.4f} (tabla: 12.706)")
    check(abs(f2.t_crit(5, 0.05) - 2.5706) < 1e-3,
          f"t critico df=5 al 95% = {f2.t_crit(5,0.05):.4f} (tabla: 2.571)")

    print("    -- el estimador: punto y tau del MISMO estimador (DL ponderado)")
    r = f2.c_estimate({"liquidez": (0.04981, 0.02112),
                       "difusion": (-0.00490, 0.02413)})
    check(abs(r["c"] - 0.023700) < 1e-5, f"c ponderado = {r['c']:.6f} (no el simple 0.022455)")
    check(abs(r["tau"] - 0.031344) < 1e-5, f"tau DL = {r['tau']:.6f}")
    check(abs(r["t"] + 1.642234) < 1e-5, f"t = {r['t']:.6f}")
    check(r["df"] == 1, "df = m - 1 = 1")
    check(abs(r["p"] - 0.348204) < 1e-5,
          f"p bajo t(df=1) = {r['p']:.6f}  (bajo normal seria {r['p_normal_solo_referencia']:.4f})")
    check(r["p"] > 3 * r["p_normal_solo_referencia"],
          f"la distribucion cambia el p por un factor {r['p']/r['p_normal_solo_referencia']:.2f}")

    print("    -- con m=1 el modelo NO es computable, y no se cae a efectos fijos")
    r1 = f2.c_estimate({"uno": (0.05, 0.02)})
    check(r1["computable"] is False and r1["c"] is None, "no devuelve numero")
    check("NUNCA se cae de vuelta" in r1["motivo"], "y dice por que")

    print("    -- LA FORMULA PUBLICADA, ejecutada tal como esta escrita en el documento")
    doc = io.open(os.path.join(REPO, "factory", "frontera_factibilidad.md"),
                  encoding="utf-8").read()
    check("z(0.05/(2*257))" in doc or "z(0.05/(2\u00b7257))" in doc,
          "el documento escribe el cuantil con el factor 2 explicito")
    # ejecutar la formula como la leeria un tercero: cuantil de UNA cola
    z1 = f2.z_two_sided(2 * (0.05 / (2 * 257)))
    z2 = f2.z_two_sided(2 * (0.05 / (2 * 177)))
    costo = 100 * (z1 / z2 - 1)
    check(abs(z1 - 3.725987) < 1e-5, f"z(0.05/(2*257)) = {z1:.6f}")
    check(abs(z2 - 3.630853) < 1e-5, f"z(0.05/(2*177)) = {z2:.6f}")
    check(abs(costo - 2.6201) < 1e-4,
          f"la formula escrita produce {costo:.4f}% = el numero publicado 2.6201%")
    check(f"{costo:.4f}"[:6] in doc or "2,6201" in doc or "2.6201" in doc,
          "y ese numero esta en el documento")


def s20_procedencia_y_n_efectivo(tmp):
    print("\n[20] \u00a72c/\u00a73.10 \u2014 procedencia de la etiqueta y n efectivo")
    fresh_ledger(tmp)

    print("    -- \u00a72c: migrar exige CITA TEXTUAL del pre-registro")
    p = pre("G2-multidia", {"z": 1},
            "quien compra provee liquidez a vendedores forzados y cobra el flujo",
            mecanismo="", h=1.0) if False else None
    # un pre-registro SIN mecanismo no se puede crear hoy; se simula el caso viejo
    e = f2.preregister("G2-multidia", {"z": 1},
                       "quien compra provee liquidez a vendedores forzados",
                       mecanismo="temporal", h=1.0,
                       n_b_proyectado=5000, n_b_fuente="fx")
    raises_msg(f2.SpecViolation,
               lambda: f2.log_mechanism_migration(e["hash"], "otro", "provee liquidez"),
               "migrar un pre-registro que YA declaro mecanismo",
               must_contain=("ya declaro mecanismo",))
    f2.abandon("G2-multidia", {"z": 1}, "cierre")

    # ahora uno sin el campo, escrito a mano como los cartuchos 1 y 2
    viejo = f2._append({
        "phase": 2, "kind": "PREREGISTRO", "family": "G2-multidia",
        "config": {"z": 2}, "part": "A", "result": None,
        "hypothesis": "quien compra provee liquidez a vendedores forzados",
        "note": "simula un pre-registro anterior a 2b"})
    raises_msg(f2.SpecViolation,
               lambda: f2.log_mechanism_migration(viejo["hash"], "liquidez",
                                                  "texto que no esta"),
               "migrar con una cita que no aparece literal",
               must_contain=("no aparece LITERAL", "post-hoc"))
    m = f2.log_mechanism_migration(viejo["hash"], "liquidez",
                                   "provee liquidez a vendedores forzados")
    check(m["kind"] == "MIGRACION_ETIQUETA", "la migracion entra como entrada propia")
    check(f2.cartuchos_por_mecanismo().get("liquidez") == 1,
          "y el CONTADOR la honra: el codigo deja de discrepar con el analisis")
    check(f2.read_ledger()[-2]["hash"] == viejo["hash"],
          "la entrada original quedo intacta, la migracion se ANEXO")

    print("    -- \u00a73.10: una operacion se cuenta una sola vez")
    import datetime as _dt
    d = [_dt.date(2020, 1, i) for i in range(1, 11)]
    conf = [("a", 1, [(d[0], 10.0), (d[1], 20.0), (d[2], 30.0)]),
            ("b", 1, [(d[1], 20.0), (d[2], 30.0), (d[3], 40.0)]),
            ("c", 3, [(d[1], 99.0)])]
    r = f2.n_efectivo(conf)
    check(r[0][3] == 3, f"a aporta {r[0][3]} nuevas de {r[0][2]}")
    check(r[1][3] == 1, f"b aporta {r[1][3]} nueva de {r[1][2]} (2 ya estaban)")
    check(r[2][3] == 1,
          "c comparte fecha con a/b pero OTRA tenencia: es otra operacion")
    check(sum(x[3] for x in r) == 5, "5 operaciones distintas en total, no 7")

    print("    -- \u00a73.5: el contador de frecuencia NO puede ver el P&L")
    df = synthetic_daily()
    llamadas = {"n": 0}

    def strat_pnl_variable(data, cfg):
        """Mismas fechas siempre, P&L distinto en CADA llamada."""
        llamadas["n"] += 1
        rows = data.index[::4]
        rng = np.random.default_rng(llamadas["n"] * 977)
        return pd.DataFrame({"points": rng.normal(llamadas["n"] * 100, 50, len(rows)),
                             "contracts": 1.0}, index=rows)

    conteos = [f2.count_trades_only(strat_pnl_variable, df, {}) for _ in range(5)]
    check(len(set(conteos)) == 1,
          f"5 llamadas con P&L completamente distinto: mismo conteo {conteos[0]}")
    check(llamadas["n"] == 5, "y la estrategia se llamo 5 veces, no se cacheo")
    check(all(isinstance(c, int) for c in conteos), "devuelve int, no un objeto con P&L")
    cm = f2.config_measurability(conteos[0])
    prohibidos = [k for k in cm
                  if any(t in k.lower() for t in ("pnl", "neto", "media", "profit",
                                                  "ganancia", "retorno"))]
    check(not prohibidos, f"la criba no expone ningun campo de P&L: {prohibidos or 'ninguno'}")
    check(f2.verify_ledger() is True, "cadena v\u00e1lida")


def s21_matriz_y_tope(tmp):
    print("\n[21] \u00a73.10 corregido y \u00a72b: el punto ciego, la contabilidad y el off-by-one")
    import datetime as _dt
    d = [_dt.date(2020, 1, i) for i in range(1, 8)]

    print("    -- el PUNTO CIEGO: identidad (fecha, tenencia) no ve configs de otra tenencia")
    conf = [("largo", 3, [(d[0], 1.0), (d[1], 2.0)]),
            ("corto", 1, [(d[0], 3.0), (d[1], 4.0), (d[2], 5.0)])]
    r = f2.n_efectivo(conf)
    check(r[1][3] == 3,
          "por §3.10 la config corta aporta 3 'nuevas' aunque comparta 2 fechas")
    w = f2.peso_mecanismo(conf)
    check(w["W_nominal"] == 9 and w["W_identidad_310"] == 9,
          f"nominal {w['W_nominal']} = identidad {w['W_identidad_310']}: §3.10 no vio nada")
    check(w["W_entradas"] == 3,
          f"pero fechas de entrada distintas son {w['W_entradas']}, no 5")
    check(w["W_conservador"] == 3 and w["manda"] == "entradas",
          "manda la medida mas conservadora")
    check(w["se_conservador"] > w["se_identidad_310"],
          f"y el SE conservador {w['se_conservador']:.4f} > "
          f"{w['se_identidad_310']:.4f}: la correccion ENDURECE")

    print("    -- \u00a72b: el tope se evalua AL ACEPTAR EL PRE-REGISTRO, no despues")
    fresh_ledger(tmp)
    corridas = {"n": 0}

    def strat_marcador(data, cfg):
        corridas["n"] += 1
        return strat_record(data, cfg)

    for i in range(4):
        pre("G2-multidia", {"i": i}, "hip", mecanismo="repetido", h=1.0)
        f2.abandon("G2-multidia", {"i": i}, "cierre")
    check(f2.budget_used() == 4, "4 cartuchos, todos del mismo mecanismo")
    check(corridas["n"] == 0, "y ninguna estrategia se corrio todavia")
    msg = raises_msg(f2.SpecViolation,
                     lambda: f2.preregister("G2-multidia", {"i": 99}, "hip",
                                            mecanismo="repetido", h=1.0,
                                            strategy_fn=strat_marcador,
                                            df=synthetic_daily()),
                     "el 5o cartucho del mismo mecanismo",
                     must_contain=("tope de concentraci\u00f3n",))
    check(corridas["n"] == 0,
          "el rechazo ocurrio SIN correr la estrategia: es un control previo, no posterior")
    check("40%" in msg, "y nombra el tope")

    print("    -- OFF-BY-ONE: el tope empieza en el 5o cartucho, como declara la spec")
    check(f2.CONCENTRACION_DESDE == 5, "CONCENTRACION_DESDE = 5")
    check(f2.budget_used() + 1 == 5,
          "el rechazo de arriba fue en el cartucho 5, no en el 6")
    check("nominal" in f2.CONCENTRACION_CONTABILIDAD,
          "y la contabilidad declarada es NOMINAL, evaluable antes de correr")
    check(f2.verify_ledger() is True, "cadena v\u00e1lida")


def s22_meta_y_rotulos(tmp):
    print("\n[22] \u00a73.8 \u2014 la meta se deriva del estimador, y los rotulos van por efecto")

    COTAS = {"c1 aporta informacion propia": (0.04190, 0.02044),
             "c1 totalmente dependiente de c2": (0.03315, 0.02453)}
    DIF = ("difusion", (-0.00489, 0.02413))

    print("    -- la meta publicada tiene que salir del estimador vigente")
    metas = {}
    for nom, liq in COTAS.items():
        r = f2.mechanism_target({"liquidez": liq, DIF[0]: DIF[1]})
        metas[nom] = r
        check(r["meta"] is not None, f"{nom[:30]}: meta = {r['meta']}")
        check(r["t_meta"] > r["t_crit"],
              f"  t {r['t_meta']:.4f} > t_crit(df={r['meta']-1}) {r['t_crit']:.4f}")
        se_chk = ((r["tau2"] + r["vbar"]) / r["meta"]) ** 0.5
        check(abs(se_chk - r["se_meta"]) < 1e-12, "  SE(meta) reproduce su formula")
        # y con un mecanismo menos NO alcanza
        if r["meta"] > 2:
            se_prev = ((r["tau2"] + r["vbar"]) / (r["meta"] - 1)) ** 0.5
            check(r["brecha"] / se_prev <= f2.t_crit(r["meta"] - 2, 0.05),
                  f"  con {r['meta']-1} mecanismos todavia NO alcanza: la meta es minima")

    print("    -- LA META PUBLICADA EN EL DOCUMENTO coincide con la derivada")
    doc = io.open(os.path.join(REPO, "factory", "frontera_factibilidad.md"),
                  encoding="utf-8").read()
    m_cons = metas["c1 aporta informacion propia"]["meta"]
    m_gen = metas["c1 totalmente dependiente de c2"]["meta"]
    check(f"meta {m_cons}" in doc or f"**{m_cons}** mecanismos" in doc
          or f"= {m_cons}" in doc,
          f"la meta conservadora ({m_cons}) figura en el documento")
    check(f"**{m_gen}**" in doc or f"= {m_gen}" in doc,
          f"la meta generosa ({m_gen}) figura en el documento")
    check("6 mecanismos" not in doc.split("Adenda 9")[-1],
          "y la meta vieja de 6 no sobrevive en la adenda vigente")

    print("    -- los rotulos van por EFECTO sobre el veredicto, no por supuesto")
    p_a = metas["c1 aporta informacion propia"]["estimador"]["p"]
    p_b = metas["c1 totalmente dependiente de c2"]["estimador"]["p"]
    check(p_a > p_b,
          f"'c1 aporta info propia' da p={p_a:.4f} > p={p_b:.4f}: es la que MAS "
          "cuesta rechazar")
    check(m_cons > m_gen,
          f"y exige mas mecanismos ({m_cons} vs {m_gen}): por eso es la CONSERVADORA")
    check("CONSERVADORA" in doc and "GENEROSA" in doc,
          "el documento usa los rotulos por efecto")

    print("    -- el supuesto de independencia, medido sobre CALENDARIO COMUN")
    check(hasattr(f2, "ESTIMADOR_C_INDEPENDENCIA"), "hay constante declarada")
    check("despreciable" in f2.ESTIMADOR_C_INDEPENDENCIA,
          f"y dice su magnitud real: {f2.ESTIMADOR_C_INDEPENDENCIA}")
    check("0.00095" in f2.ESTIMADOR_C_INDEPENDENCIA,
          "con el numero de calendario comun, no el de la submuestra")
    rho_cal, n_liq, n_dif, nov = 0.0262, 1797, 1718, 64
    rho_est = rho_cal * nov / (n_liq * n_dif) ** 0.5
    check(abs(rho_est - 0.00095) < 1e-5,
          f"Corr entre estimadores = {rho_est:+.5f}")
    rho_sub = 0.7036 * 64 / (244 * 1718) ** 0.5
    check(rho_sub / rho_est > 50,
          f"la medicion vieja sobre salidas compartidas daba {rho_sub:+.4f}: "
          f"{rho_sub/rho_est:.0f} veces mayor. Sobreestimaba la violacion.")


def s23_filo_del_tope(tmp):
    print("\n[23] \u00a72b \u2014 el tope es '>' y la igualdad exacta PASA")
    import inspect
    src = inspect.getsource(f2.preregister)
    linea = [l.strip() for l in src.split("\n")
             if "MAX_CONCENTRACION * (gastado" in l][0]
    check(" > " in linea and " >= " not in linea,
          f"el codigo usa '>': {linea}")
    doc = io.open(os.path.join(REPO, "factory", "spec_fase2.md"),
                  encoding="utf-8").read()
    check("supera el 40" in doc, "y la spec dice 'supera', que es estrictamente mayor")

    print("    -- el caso de IGUALDAD EXACTA: 2 de 5 = 40.0%")
    check(not (2 > f2.MAX_CONCENTRACION * 5), "2 > 0.40*5 es falso: PASA")
    check(3 > f2.MAX_CONCENTRACION * 5, "3 de 5 = 60% si bloquea")

    print("    -- y probado de punta a punta sobre un ledger")
    fresh_ledger(tmp)
    f2.CONCENTRACION_DESDE = 4      # tope activo justo cuando se registra el 5o
    FAMS = ["G2-multidia", "G3-regimen", "G5-cruzado", "G6-terceros"]
    try:
        for i, fam in enumerate(FAMS):   # una familia y un mecanismo por cartucho
            pre(fam, {"e": i}, "hip", mecanismo=f"m{i}", h=1.0)
            f2.abandon(fam, {"e": i}, "cierre")
        check(f2.budget_used() == 4 and len(f2.cartuchos_por_mecanismo()) == 4,
              "4 cartuchos, 4 mecanismos y 4 familias distintas")
        pre("G2-multidia", {"e": 4}, "hip", mecanismo="m0", h=1.0)
        f2.abandon("G2-multidia", {"e": 4}, "cierre")
        check(f2.cartuchos_por_mecanismo()["m0"] == 2 and f2.budget_used() == 5,
              "m0 y G2 llegan a 2 de 5 = 40.0% EXACTO y paso con el tope ACTIVO")
        raises_msg(f2.SpecViolation,
                   lambda: pre("G2-multidia", {"e": 5}, "hip", mecanismo="m0", h=1.0),
                   "el siguiente de m0 (3 de 6 = 50%)",
                   must_contain=("tope de concentraci\u00f3n",))
    finally:
        f2.CONCENTRACION_DESDE = 5
    check(f2.verify_ledger() is True, "cadena v\u00e1lida")


def s24_ambos_topes(tmp):
    print("\n[24] \u00a72b \u2014 los DOS topes se evaluan, y uno solo no alcanza")
    fresh_ledger(tmp)
    max0, desde0 = f2.MAX_CONCENTRACION, f2.CONCENTRACION_DESDE
    try:
        # Montaje con el tope suspendido, para aislar el chequeo que se prueba.
        f2.MAX_CONCENTRACION = 1.0
        for i, mec in enumerate(["liq", "liq", "dif", "liq"]):
            pre("G2-multidia", {"z": i}, "hip", mecanismo=mec, h=1.0)
            f2.abandon("G2-multidia", {"z": i}, "cierre")
        f2.MAX_CONCENTRACION, f2.CONCENTRACION_DESDE = max0, 4
        check(f2.budget_used() == 4 and f2.budget_used("G2-multidia") == 4,
              "4 cartuchos, los 4 en G2 (como el ledger real)")
        mec = f2.cartuchos_por_mecanismo()
        check(mec["liq"] == 3 and mec["dif"] == 1, "liq 3, dif 1")

        print("    -- el tope de MECANISMO deja pasar a 'dif' (2 de 5 = 40.0% exacto)")
        tope = f2.MAX_CONCENTRACION * 5
        check(not (mec["dif"] + 1 > tope), f"dif: 2 > {tope} es falso -> pasaria")

        print("    -- pero el de FAMILIA bloquea G2 (5 de 5 = 100%)")
        check(f2.budget_used("G2-multidia") + 1 > tope, f"G2: 5 > {tope} -> bloquea")

        print("    -- y preregister() se niega igual: hay que pasar los DOS")
        msg = raises_msg(
            f2.SpecViolation,
            lambda: pre("G2-multidia", {"z": 9}, "hip", mecanismo="dif", h=1.0),
            "cartucho 5 a 'dif' dentro de G2",
            must_contain=("tope de concentraci\u00f3n", "familia"))
        check("G2-multidia" in msg,
              "el rechazo lo produjo el tope de FAMILIA, no el de mecanismo")
        check("mecanismo" not in msg.split("familia")[0],
              "y el de mecanismo habia pasado: uno solo no alcanza")

        print("    -- el mismo mecanismo en una familia NUEVA si entra")
        e = pre("G3-regimen", {"z": 10}, "estado sobre la regla base de difusion",
                mecanismo="dif", h=1.0)
        check(f2.cartuchos_por_mecanismo()["dif"] == 2 and f2.budget_used() == 5,
              "dif llega a 2 de 5 = 40.0% exacto, en familia G3: PASA")
        f2.abandon("G3-regimen", {"z": 10}, "cierre")
    finally:
        f2.MAX_CONCENTRACION, f2.CONCENTRACION_DESDE = max0, desde0
    check(f2.verify_ledger() is True, "cadena v\u00e1lida")


# §8.5 — "no detectado" NO es "no existe". Formulaciones prohibidas en el
# documento publicado, salvo dentro de una cita tachada (~~...~~).
# §75 — theta es el umbral de 80% de POTENCIA, no un piso de detectabilidad.
# Estos terminos solo se admiten con una cifra de potencia al lado (400 caracteres).
POTENCIA_OBLIGATORIA = ("no detectable", "indetectable", "piso de deteccion",
                        "piso de detecci\u00f3n")

AUSENCIA_PROHIBIDA = (
    "no existe ventaja", "no hay ventaja", "no existe borde", "no hay borde",
    "no existe se\u00f1al", "no hay se\u00f1al", "las reglas no funcionan",
    "sin ventaja explotable", "no tienen ventaja", "no tiene ventaja",
    "queda demostrado que no", "probamos que no hay",
)


def _sin_tachados(texto):
    """Quita los tramos ~~tachados~~: ahi una cita vieja puede decir lo que sea."""
    return re.sub(r"~~.*?~~", " ", texto, flags=re.S)


def s25_lenguaje_de_ausencia(tmp):
    print("\n[25] \u00a78.5 \u2014 'no detectado' no es 'no existe'")
    docs = ["factory/frontera_factibilidad.md", "factory/spec_fase2.md"]
    for rel in docs:
        texto = io.open(os.path.join(REPO, rel), encoding="utf-8").read()
        limpio = _sin_tachados(texto).lower()
        hallados = [p for p in AUSENCIA_PROHIBIDA if p.lower() in limpio]
        check(not hallados,
              f"{rel}: sin formulaciones de ausencia de efecto "
              f"({hallados if hallados else 'ninguna'})")

    print("    -- y el test detecta de verdad: se le inyecta una y falla")
    inyectado = "El resultado prueba que no hay ventaja en estas familias."
    check(any(p.lower() in inyectado.lower() for p in AUSENCIA_PROHIBIDA),
          "una frase de ausencia inyectada SI se detecta")

    print("    -- pero dentro de una cita tachada esta permitida")
    tachado = "~~El resultado prueba que no hay ventaja en estas familias.~~ Corregido."
    limpio = _sin_tachados(tachado).lower()
    check(not any(p.lower() in limpio for p in AUSENCIA_PROHIBIDA),
          "la misma frase, tachada, NO dispara: las citas viejas se conservan")

    print("    -- y el tachado no es una puerta trasera: tiene presupuesto")
    for rel in docs:
        texto = io.open(os.path.join(REPO, rel), encoding="utf-8").read()
        tramos = re.findall(r"~~.*?~~", texto, flags=re.S)
        tachado = sum(len(x) for x in tramos)
        frac = tachado / max(1, len(texto))
        mayor = max([len(x) for x in tramos] or [0])
        check(frac < 0.02,
              f"{rel}: texto tachado {frac*100:.2f}% del documento (< 2%)")
        check(mayor <= 400,
              f"{rel}: el tramo tachado mas largo mide {mayor} caracteres (<= 400)")

    print("    -- CONTROL: tachar el documento entero NO es una salida")
    bloque = "~~" + ("El resultado prueba que no hay ventaja. " * 40) + "~~"
    check(max(len(x) for x in re.findall(r"~~.*?~~", bloque, flags=re.S)) > 400,
          "un documento tachado en bloque violaria el tope de 400 caracteres")

    print("    -- \u00a775: 'no detectable' sin su potencia al lado tampoco se admite")
    for rel in docs:
        texto = _sin_tachados(io.open(os.path.join(REPO, rel), encoding="utf-8").read())
        bajo = texto.lower()
        huerfanas = []
        for termino in POTENCIA_OBLIGATORIA:
            desde = 0
            while True:
                i = bajo.find(termino, desde)
                if i < 0:
                    break
                desde = i + 1
                ventana = bajo[max(0, i - 400):i + 400]
                if not ("potencia" in ventana and "%" in ventana):
                    huerfanas.append((termino, texto[max(0, i - 60):i + 60]))
        check(not huerfanas,
              f"{rel}: {len(huerfanas)} usos de 'no detectable/indetectable/piso de "
              f"deteccion' sin cifra de potencia al lado")

    print("    -- y este test tambien se prueba a si mismo")
    suelta = "El efecto quedo por debajo del piso de deteccion y ahi murio."
    acompanada = ("El efecto quedo por debajo del piso de deteccion, o sea que el examen "
                  "habria tenido 71% de potencia y no el 80% exigido.")
    def _huerfana(txt):
        b = txt.lower()
        return any((b.find(x) >= 0 and not ("potencia" in b and "%" in b))
                   for x in POTENCIA_OBLIGATORIA)
    check(_huerfana(suelta), "la frase SIN potencia se detecta")
    check(not _huerfana(acompanada), "la misma frase CON su potencia pasa (control)")

    print("    -- el numero que sostiene la regla")
    theta = f2.POWER_CONST / (1669 ** 0.5)
    medidos = [0.0618, 0.04190, 0.03315, 0.020262, 0.013874]
    check(all(c < theta for c in medidos),
          f"los cinco c medidos ({min(medidos):.4f}..{max(medidos):.4f}) estan por "
          f"debajo del piso {theta:.6f}")
    check(abs(theta - 0.068577) < 1e-6, f"piso de deteccion = {theta:.6f}")


def s26_de_que_sigma_sale_c(tmp):
    print("\n[26] \u00a73.8 \u2014 c sale del sigma OBSERVADO de cada configuracion")
    from math import sqrt as _sq

    print("    -- la identidad t = c*sqrt(n*h), con fixture sintetico (sin datos)")
    rng = np.random.default_rng(20260824)
    for h in (1, 3, 7):
        x = rng.normal(4.0, 90.0, 800)
        n = len(x)
        media, sd = float(x.mean()), float(x.std(ddof=1))
        t_real = media / (sd / _sq(n))
        c_obs = (media / sd) / _sq(h)
        c_esc = (media / (81.06 * _sq(h))) / _sq(h)
        check(abs(c_obs * _sq(n * h) - t_real) < 1e-9,
              f"h={h}: c con sigma OBSERVADO reproduce t exacto ({t_real:+.4f})")
        check(abs(c_esc * _sq(n * h) - t_real) > 1e-3,
              f"h={h}: c con sigma ESCALADO NO reproduce t (control)")

    data_path = os.path.join(REPO, "data", "es_daily.csv")
    if not os.path.exists(data_path):
        print("    (resto salteado: data/es_daily.csv no esta)")
        return
    from familia_g2 import reversion_k_dias
    df = pd.read_csv(data_path)
    c0 = df.columns[0]
    df[c0] = pd.to_datetime(df[c0])
    df = df.set_index(c0).sort_index()
    df.columns = [x.lower() for x in df.columns]
    a = f2.WINDOWS["diario"].slice(df, "A")

    print("    -- el c PUBLICADO del cartucho 1 sale del observado, no del escalado")
    tr = reversion_k_dias(a, {"k": 3, "side": 1, "hold": 3})
    bruto = (tr["points"] * harness.POINT_VALUE * tr["contracts"]).to_numpy(dtype=float)
    media, sd_obs = float(bruto.mean()), float(bruto.std(ddof=1))
    c_obs = (media / sd_obs) / _sq(3)
    c_esc = (media / (81.06 * _sq(3))) / _sq(3)
    check(abs(c_obs - 0.0618) < 5e-5,
          f"c con sigma observado = {c_obs:.6f} = el publicado 0.0618")
    check(abs(c_esc - 0.0618) > 5e-3,
          f"c con sigma escalado = {c_esc:.6f} NO es el publicado (control)")
    theta = f2.POWER_CONST / _sq(1669)
    check(c_obs < theta < c_esc,
          f"y la direccion: el escalado ({c_esc:.5f}) cruzaria theta ({theta:.6f}) "
          f"y el observado ({c_obs:.5f}) no. La eleccion es la CONSERVADORA")

    print("    -- sigma_1 = 81.06 es apertura-a-apertura en la parte A, y la tabla \u00a71")
    for k, doc in ((1, 81.06), (2, 112.07), (3, 134.01), (5, 170.43),
                   (7, 196.87), (10, 231.01), (20, 317.85)):
        s = (a["open"].diff(k) * harness.POINT_VALUE).dropna()
        check(abs(float(s.std(ddof=1)) - doc) < 0.005,
              f"sigma a {k}d = ${float(s.std(ddof=1)):.2f} = ${doc:.2f} del documento")

    print("    -- la tabla de horizontes se reproduce de (POWER_CONST/c)^2")
    for c, sb_doc in ((0.06180, 2055), (0.04190, 4471), (0.03315, 7142),
                      (0.020262, 19118), (0.013874, 40776)):
        check(abs(round((f2.POWER_CONST / c) ** 2) - sb_doc) <= 1,
              f"c={c:+.6f} -> S_B necesario {round((f2.POWER_CONST/c)**2):,} "
              f"(publicado {sb_doc:,})")


def s27_la_caja_fuerte_es_el_futuro(tmp):
    print("\n[27] \u00a74.4/\u00a77.1 \u2014 la caja fuerte es el FUTURO, y A jamas entra en B")

    print("    -- las ventanas declaradas, tal como estan en la spec")
    d = f2.WINDOWS["diario"]
    check((d.a_start, d.a_end) == ("2000-09-18", "2019-12-31"),
          f"parte A diaria = {d.a_start} -> {d.a_end} (donde se BUSCO)")
    check((d.b_start, d.b_end) == ("2020-01-01", "2026-08-19"),
          f"parte B diaria = {d.b_start} -> {d.b_end} (la caja fuerte)")

    print("    -- A y B no se tocan, en los dos regimenes")
    for nombre, r in sorted(f2.WINDOWS.items()):
        check(r.a_end < r.b_start,
              f"{nombre}: A cierra {r.a_end} ANTES de que B abra {r.b_start}")
        check(r.a_start < r.a_end and r.b_start < r.b_end,
              f"{nombre}: las dos ventanas son intervalos bien formados")

    print("    -- CONTROL: correr B hacia atras se comeria sesiones YA BUSCADAS")
    for propuesta in ("2018-01-01", "2008-01-01", "2001-01-01"):
        check(d.a_start <= propuesta <= d.a_end,
              f"arrancar B en {propuesta} cae DENTRO de la parte A: no es fuera de muestra")
    check("1998-01-01" < d.a_start,
          "1998-01-01 es ANTERIOR a la parte A: no esta buscado, pero tampoco esta "
          "en esta fuente (la ventana arranca en 2000-09-18)")
    check("1997-09-09" < d.a_start,
          "lo unico jamas visto es anterior a 2000-09-18, y exige fuente nueva (#4.5)")

    print("    -- la caja fuerte sigue sin abrirse: ni una entrada de Fase 2 con part='B'")
    ent = [e for e in f2.read_ledger() if e.get("phase") == 2]
    partes = sorted({e.get("part") for e in ent if e.get("part")})
    check(partes == ["A", "meta"], f"partes usadas por la Fase 2: {partes}")
    check(not [e for e in ent if e.get("part") == "B"],
          f"0 entradas de Fase 2 sobre la parte B (de {len(ent)} entradas)")

    print("    -- la aritmetica de lo que compraria el backfill completo del ES")
    from math import sqrt as _sq
    theta_hoy = f2.POWER_CONST / _sq(1669)
    theta_bf = f2.POWER_CONST / _sq(1669 + 760)
    check(abs(theta_hoy - 0.068577) < 1e-6, f"theta hoy = {theta_hoy:.6f}")
    check(abs(theta_bf - 0.056845) < 1e-6,
          f"theta con 760 sesiones nunca vistas = {theta_bf:.6f}")
    check(0.0618 > theta_bf > 0.04190,
          "solo cruzaria el maximo sesgado (0.0618); liquidez (0.0419) seguiria debajo")


def s28_piso_del_dataset(tmp):
    print("\n[28] \u00a78.6 \u2014 el piso del dataset y el reparto A/B")
    from math import sqrt as _sq
    z, N = f2.POWER_CONST, 6544

    print("    -- el piso: hallar exige (z/c)^2 y validar otras tantas")
    piso = z * _sq(2.0 / N)
    check(abs(piso - 0.048978) < 1e-6,
          f"c >= z*sqrt(2/N) = {piso:.6f} con N={N} sesiones")
    check(abs(2 * (z / piso) ** 2 - N) < 1.0,
          "y en el piso las dos mitades suman exactamente el dataset")
    check(abs(z * _sq(2.0 / (N + 760)) - 0.046359) < 1e-6,
          "con el backfill completo del ES el piso solo baja a 0.046359")

    print("    -- aplicado a los c disponibles")
    for c, tot, entra in ((0.06180, 4110, True), (0.04190, 8941, False),
                          (0.03315, 14285, False), (0.020262, 38236, False)):
        need = 2 * (z / c) ** 2
        check(abs(round(need) - tot) <= 1,
              f"c={c:+.6f} exige {round(need):,} sesiones totales (publicado {tot:,})")
        check((need <= N) is entra,
              f"c={c:+.6f} {'entra' if entra else 'NO entra'} en las {N:,} disponibles")

    print("    -- la causa raiz: el prior del dia cero SUPERA el piso del dataset")
    prior = 0.174903 / _sq(7)
    check(abs(prior - 0.066107) < 1e-6, f"c(F4) = {prior:.6f}")
    check(prior > piso,
          f"prior {prior:.6f} > piso {piso:.6f}: la fase ERA viable con este dataset")
    check(prior < z / _sq(1669),
          f"pero prior {prior:.6f} < theta_B {z/_sq(1669):.6f}: el reparto la mataba")

    print("    -- el que ata es max(theta_A, theta_B), y se minimiza en 50/50")
    def ata(sa):
        return max(z / _sq(sa), z / _sq(N - sa))
    for sa, sb, ta, tb in ((4875, 1669, 0.040125, 0.068577),
                           (3926, 2618, 0.044712, 0.054754),
                           (3272, 3272, 0.048978, 0.048978),
                           (2618, 3926, 0.054754, 0.044712)):
        check(abs(z / _sq(sa) - ta) < 1e-6 and abs(z / _sq(sb) - tb) < 1e-6,
              f"reparto {sa:,}/{sb:,}: theta_A {ta:.6f}, theta_B {tb:.6f}")
    mejor = min(range(int(N * 0.30), int(N * 0.70)), key=ata)
    check(abs(mejor / N - 0.50) < 0.01,
          f"el minimo de max(theta_A,theta_B) cae en A = {100*mejor/N:.1f}%")
    check(abs(ata(mejor) - piso) < 1e-4,
          f"y vale {ata(mejor):.6f} = el piso analitico {piso:.6f}")
    check(ata(4875) > prior > ata(3272),
          "el reparto real deja el prior AFUERA y el 50/50 lo deja adentro")

    print("    -- CONTROL: NINGUN reparto baja del piso (es un minimo, no un promedio)")
    peor = 0.0
    for sa in range(200, N - 200, 37):
        check_silent = ata(sa) >= piso - 1e-12
        if not check_silent:
            peor = max(peor, piso - ata(sa))
    check(peor == 0.0,
          f"{len(range(200, N-200, 37)):,} repartos probados: ninguno baja de {piso:.6f}")
    check(ata(3272) - piso < 1e-9 < ata(4875) - piso,
          "el 50/50 toca el piso; el reparto real queda estrictamente por encima")


RESULTADO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "ultimo_resultado.json")


def escribir_resultado(ok, fallas, ledger_ok, codigo):
    """El veredicto en un archivo. Sobrevive a `| tail`, a `| head` y a cualquier
    tuberia que se coma el estado de salida."""
    import datetime
    payload = {
        "ts_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(
            timespec="seconds"),
        "aserciones_ok": ok,
        "fallas": len(fallas),
        "detalle_fallas": list(fallas),
        "ledger_publicado_ok": bool(ledger_ok),
        "veredicto": "OK" if codigo == 0 else "FALLA",
        "exit": codigo,
    }
    with io.open(RESULTADO_PATH, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    return payload


def s29_el_estado_de_salida_no_se_pierde(tmp):
    print("\n[29] el bug del tail: el veredicto tiene que sobrevivir a la tuberia")
    import subprocess
    import shutil as _sh

    falla = os.path.join(tmp, "suite_que_falla.py")
    pasa = os.path.join(tmp, "suite_que_pasa.py")
    io.open(falla, "w", encoding="utf-8").write(
        "import sys\nprint('aserciones OK: 3   fallas: 1')\nsys.exit(1)\n")
    io.open(pasa, "w", encoding="utf-8").write(
        "import sys\nprint('aserciones OK: 4   fallas: 0')\nsys.exit(0)\n")
    py = sys.executable

    print("    -- sin tuberia el estado de salida ya era correcto")
    check(subprocess.run([py, falla], capture_output=True).returncode != 0,
          "una suite que falla, sin entubar, devuelve estado != 0")
    check(subprocess.run([py, pasa], capture_output=True).returncode == 0,
          "y una que pasa devuelve 0 (control)")

    bash = _sh.which("bash")
    if bash:
        print("    -- CONTROL: el bug, reproducido. Entubada SIN pipefail da 0")
        cmd = f'"{py}" "{falla}" | tail -1'
        r = subprocess.run([bash, "-c", cmd], capture_output=True)
        check(r.returncode == 0,
              f"suite que FALLA entubada a tail sin pipefail -> estado {r.returncode}: "
              "el fallo queda invisible (esto es el bug)")

        print("    -- EL ARREGLO: con pipefail el estado es el de la suite")
        r = subprocess.run([bash, "-c", "set -o pipefail; " + cmd],
                           capture_output=True)
        check(r.returncode != 0,
              f"la misma tuberia con pipefail -> estado {r.returncode} != 0")
        r = subprocess.run([bash, "-c", f'set -o pipefail; "{py}" "{pasa}" | tail -1'],
                           capture_output=True)
        check(r.returncode == 0,
              "y pipefail NO rompe el caso que pasa: sigue dando 0 (control)")
    else:
        check(False, "bash no esta disponible: el control del pipe no pudo correr")

    print("    -- el runner del repo lleva el arreglo adentro")
    runner = os.path.join(REPO, "tests", "fase2", "correr.sh")
    check(os.path.exists(runner), "existe tests/fase2/correr.sh")
    texto = io.open(runner, encoding="utf-8").read()
    check("pipefail" in texto, "y declara pipefail")

    print("    -- y el veredicto en archivo, que ninguna tuberia puede tapar")
    global RESULTADO_PATH
    real_path, RESULTADO_PATH = RESULTADO_PATH, os.path.join(tmp, "veredicto.json")
    try:
        p = escribir_resultado(3, ["una falla inventada"], True, 1)
        leido = json.loads(io.open(RESULTADO_PATH, encoding="utf-8").read())
        check(leido == p, "escribir_resultado deja en disco exactamente lo que devuelve")
        for campo in ("aserciones_ok", "fallas", "veredicto", "exit", "ts_utc",
                      "ledger_publicado_ok", "detalle_fallas"):
            check(campo in leido, f"el archivo trae '{campo}'")
        check(leido["veredicto"] == "FALLA" and leido["exit"] == 1,
              "una corrida con fallas queda escrita como FALLA, sin depender del "
              "estado de salida")
        check(leido["detalle_fallas"] == ["una falla inventada"],
              "y con el detalle de que fallo")

        print("    -- CONTROL: una corrida limpia queda escrita como OK")
        p2 = escribir_resultado(391, [], True, 0)
        check(p2["veredicto"] == "OK" and p2["exit"] == 0,
              "sin fallas y con el ledger intacto -> OK")
        check(escribir_resultado(391, [], False, 1)["veredicto"] == "FALLA",
              "y un ledger publicado roto tambien es FALLA, aunque no haya fallas")
    finally:
        RESULTADO_PATH = real_path

    print("    -- y main() lo escribe de verdad, no es un helper huerfano")
    fuente = io.open(os.path.abspath(__file__), encoding="utf-8").read()
    cuerpo = fuente[fuente.index("def main():"):]
    check("escribir_resultado(" in cuerpo,
          "main() llama a escribir_resultado antes de devolver su codigo")


def main():
    print("=" * 78)
    print("FASE 2 — pruebas del trabajo de día 0 (spec_fase2.md §9)")
    print("Ledger real INTACTO: todo corre sobre una copia en tempdir.")
    print("=" * 78)
    real = harness.LEDGER_PATH
    tmp = tempfile.mkdtemp(prefix="f2_dia0_")
    try:
        for fn in (s0_constantes, s1_reproduce_f4):
            fn()
        s1b_compuertas_identicas()
        for fn in (s2_prerregistro, s3_presupuesto, s4_vecindad, s5_ventanas,
                   s6_caja_fuerte, s7_barra_y_anios, s8_ledger_y_apertura,
                   s9_colgados, s10_reglas_congeladas, s11_margen_despliegue,
                   s12_bloqueantes, s13_criba_medibilidad,
                   s14_criba_por_config, s15_direccion_de_los_cambios,
                   s16_politica_asignacion, s17_solo_medicion,
                   s18_vara_de_filtros, s19_estimador_y_formula,
                   s20_procedencia_y_n_efectivo, s21_matriz_y_tope,
                   s22_meta_y_rotulos, s23_filo_del_tope, s24_ambos_topes,
                   s25_lenguaje_de_ausencia, s26_de_que_sigma_sale_c,
                   s27_la_caja_fuerte_es_el_futuro, s28_piso_del_dataset,
                   s29_el_estado_de_salida_no_se_pierde):
            fn(tmp)
    except Exception:  # noqa: BLE001
        traceback.print_exc()
        FAIL.append("EXCEPCIÓN no controlada")
    finally:
        harness.LEDGER_PATH = real
        f2.LEDGER_PATH = real
        shutil.rmtree(tmp, ignore_errors=True)

    print("\n" + "=" * 78)
    print(f"aserciones OK: {OK}   fallas: {len(FAIL)}")
    for f in FAIL:
        print("   FALLA:", f)
    # cinturón: el ledger publicado quedó como estaba
    published_ok = harness.verify_ledger()
    print(f"ledger publicado intacto y verificado: {published_ok}")
    codigo = 0 if not FAIL and published_ok else 1
    # El VEREDICTO va a un archivo, no solo al estado de salida: entubar la suite
    # (`| tail`) hace que la shell lea el estado de tail y no el nuestro, y un
    # conteo falso paso desapercibido asi una vez. Un archivo no se entuba.
    escribir_resultado(OK, FAIL, published_ok, codigo)
    print(f"veredicto escrito en {os.path.relpath(RESULTADO_PATH, REPO)}")
    print("=" * 78)
    return codigo


if __name__ == "__main__":
    sys.exit(main())
