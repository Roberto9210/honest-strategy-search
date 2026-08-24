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
        f2.log_measurability_screen(fam, 5000, "fixture de prueba")
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
    f2.preregister("G1-nocturna", cfg, "prima nocturna: prueba de humo")
    check(f2.budget_used() == n0 + 1, "el pre-registro gasta cartucho al escribirse, no al correr")
    res = f2.run_on(df, "G1-nocturna", cfg, strat_record)
    check(res.trades > 0, f"con pre-registro corre ({res.trades} operaciones)")

    print("    -- y el pre-registro se consume: no habilita una segunda corrida")
    raises(f2.PreregistrationMissing,
           lambda: f2.run_on(df, "G1-nocturna", cfg, strat_record),
           "segunda corrida con el mismo pre-registro")

    print("    -- hipótesis obligatoria")
    raises(f2.SpecViolation,
           lambda: f2.preregister("G1-nocturna", {"x": 1}, "   "),
           "pre-registro sin hipótesis")
    raises(f2.SpecViolation,
           lambda: f2.preregister("INVENTADA", {"x": 1}, "h"),
           "familia no declarada en la spec")

    print("    -- lo que el código no puede impedir, se registra y cobra igual")
    n1 = f2.budget_used()
    f2.log_spec_violation("G2-multidia", {"y": 2}, None, "corrida por fuera de run_on")
    check(f2.budget_used() == n1 + 1, "una violación de spec consume presupuesto igual")


def s3_presupuesto(tmp):
    print("\n[3] §2 — el presupuesto es un tope, y no se transfiere entre familias")
    fresh_ledger(tmp)
    for i in range(f2.FAMILY_BUDGET["G6-terceros"]):
        f2.preregister("G6-terceros", {"i": i}, "regla de un tercero")
        f2.abandon("G6-terceros", {"i": i}, "prueba de presupuesto: no se corre")
    check(f2.budget_used("G6-terceros") == 20, "G6 agotó sus 20")
    check(len(f2.open_preregistrations()) == 0, "ninguno quedó colgando")
    check(f2.budget_used("G6-terceros") == 20,
          "abandonar NO devuelve el cartucho (§7.2: los errores también cuestan)")
    raises(f2.BudgetExhausted,
           lambda: f2.preregister("G6-terceros", {"i": 999}, "una más"),
           "configuración 21 de G6")
    check(f2.budget_used() == 20 and f2.budget_used("G1-nocturna") == 0,
          "el sobrante de otras familias no rescata a G6 (ni al revés)")
    rep = f2.budget_report()
    check(rep["restante"] == 180, f"restante global {rep['restante']} de {f2.K2}")


def s4_vecindad(tmp):
    print("\n[4] §7.2 — la trampa del bloque 3x3: adoptar una celda cuesta las 9")
    fresh_ledger(tmp)
    best = {"n_before": 4, "m_after": 3}
    cells = [{"n_before": nb, "m_after": ma} for nb in (3, 4, 5) for ma in (2, 3, 4)]
    f2.preregister("G2-multidia", best, "publicada; vecindad declarada como robustez",
                   robustness_cells=cells)
    check(f2.budget_used("G2-multidia") == 1,
          "la vecindad declarada NO gasta: 1 cartucho, no 10")
    f2.abandon("G2-multidia", best, "cerrada para probar la adopción")

    print("    -- pero (4,2) daba PF 1.691 contra 1.507 de la publicada. Adoptarla:")
    raises_msg(f2.SpecViolation,
               lambda: f2.preregister("G2-multidia", {"n_before": 4, "m_after": 2},
                                      "me gusta más esta"),
               "adoptar una celda de la vecindad sin declararlo",
               must_contain=("celda de robustez", "SELECCIÓN"))

    f2.preregister("G2-multidia", {"n_before": 4, "m_after": 2},
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
    f2.preregister("G1-nocturna", cfg, "prueba de ventana")
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
    f2.preregister("G4-bordes", {"z": 1}, "borde de sesión")
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
    f2.preregister("G1-nocturna", cfg, "candidata de prueba")
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
    f2.preregister("G2-multidia", cfg2, "otra candidata")
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
    f2.preregister("G3-regimen", {"q": 1}, "estado de volatilidad")
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

    e = f2.preregister("G1-nocturna", cfg_a, "primera hipótesis")
    check(len(f2.open_preregistrations()) == 1, "queda 1 pre-registro abierto")

    print("    -- CONTROL DE MUTACIÓN: lo dejo colgando y pido el siguiente")
    msg = raises_msg(f2.SpecViolation,
                     lambda: f2.preregister("G1-nocturna", cfg_b, "segunda hipótesis"),
                     "preregister() con uno sin resolver",
                     must_contain=("sin resolver", "G1-nocturna", e["hash"]))
    check('"step": 5' in msg, "el mensaje nombra la config exacta que quedó abierta")
    check("abandon(" in msg, "y dice cómo cerrarla")
    check(f2.budget_used() == 1, "el bloqueado no gastó cartucho")

    print("    -- salida 1 de 3: el resultado lo resuelve")
    f2.run_on(df, "G1-nocturna", cfg_a, strat_record)
    check(len(f2.open_preregistrations()) == 0, "resuelto por RESULTADO")
    f2.preregister("G1-nocturna", cfg_b, "segunda hipótesis")
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
    f2.preregister("G2-multidia", cfg_c, "tercera hipótesis")
    used = f2.budget_used()
    v = f2.log_spec_violation("G2-multidia", cfg_c, None, "corrida por fuera de run_on")
    check(v.get("prereg") is not None, "la violación enlaza al pre-registro que resuelve")
    check(len(f2.open_preregistrations()) == 0, "resuelto por VIOLACION")
    check(f2.budget_used() == used, "no cobra dos veces: el cartucho ya se había pagado")

    print("    -- y una corrida que revienta NO deja el pre-registro resuelto")
    f2.preregister("G4-bordes", {"z": 2}, "borde de sesión")
    try:
        f2.run_on(df, "G4-bordes", {"z": 2}, strat_record)
    except f2.WindowViolation:
        pass
    check(len(f2.open_preregistrations()) == 1,
          "la corrida falló y el pre-registro sigue abierto: hay que cerrarlo a mano")
    raises(f2.SpecViolation,
           lambda: f2.preregister("G1-nocturna", {"step": 11}, "otra"),
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
    f2.preregister("G2-multidia", {"a": 1}, "prueba de sellado")
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
    f2.preregister("G2-multidia", cfg, "el margen no cambia ningún número del backtest")
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
                   lambda: f2.preregister("G2-multidia", {"b": 1}, "hipótesis"),
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
    f2.preregister("G6-terceros", {"c": 1}, "una regla de un amigo")
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
               lambda: f2.preregister("G6-terceros", {"c": 2}, "otra"),
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
               lambda: f2.preregister("G1-nocturna", {"z": 1}, "hipótesis"),
               "pre-registrar sin criba de medibilidad",
               must_contain=("criba de medibilidad", "no gasta presupuesto"))

    print("    -- una familia NO VALIDABLE no puede gastar sus cartuchos")
    used = f2.budget_used()
    e = f2.log_measurability_screen(
        "G1-nocturna", 100,
        "techo estructural de prueba: 100 operaciones en B")
    check(e["screen"]["validable"] is False, "100 < 342: NO VALIDABLE")
    check(f2.budget_used() == used, "y la criba NO consumió presupuesto")
    check(abs(e["screen"]["delta_min_detectable"] - 2.8016 / 10) < 1e-3,
          f"efecto mínimo detectable {e['screen']['delta_min_detectable']:.4f} "
          "= 2.8016/sqrt(100)")
    raises_msg(f2.SpecViolation,
               lambda: f2.preregister("G1-nocturna", {"z": 1}, "hipótesis"),
               "pre-registrar en una familia NO VALIDABLE",
               must_contain=("NO VALIDABLE", "342"))

    print("    -- y sacarla de alcance pierde los cartuchos, sin mover el listón")
    oos = f2.declare_not_validable(
        "G1-nocturna", "techo de 100 operaciones contra 342 necesarias")
    check(oos["cartuchos_perdidos"] == 40, "los 40 de G1 se pierden")
    check(oos["K_total_sigue_en"] == 257, "K_total sigue en 257")
    rep_ = f2.budget_report()
    check(rep_["perdidos_fuera_de_alcance"] == 40 and rep_["K_total"] == 257,
          "perdidos, no devueltos y no reasignados (§1.4 + §2)")
    check(f2.verify_ledger() is True, "cadena válida")


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
                   s12_bloqueantes, s13_criba_medibilidad):
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
    print("=" * 78)
    return 0 if not FAIL and published_ok else 1


if __name__ == "__main__":
    sys.exit(main())
