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
    shutil.copyfile(PUBLISHED_LEDGER, dst)
    f2.set_ledger(dst)
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

    print("    -- y la barra efectiva por régimen que declara §3.2:")
    check(abs(f2.required_t_a(4875, 1669) - 4.788) < 0.001,
          f"diario: t exigido {f2.required_t_a(4875, 1669):.3f} (spec 4.788)")
    check(abs(f2.required_t_a(1004, 1669) - f2.DECISION_T) < 1e-9,
          "intradía: manda la línea de decisión (3.726), no la potencia")


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
    check(f2.budget_used("G6-terceros") == 20, "G6 agotó sus 20")
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

    print("    -- pero (4,2) daba PF 1.691 contra 1.507 de la publicada. Adoptarla:")
    raises(f2.SpecViolation,
           lambda: f2.preregister("G2-multidia", {"n_before": 4, "m_after": 2},
                                  "me gusta más esta"),
           "adoptar una celda de la vecindad sin declararlo")

    f2.preregister("G2-multidia", {"n_before": 4, "m_after": 2},
                   "adopción consciente de la mejor celda",
                   adopcion_de_vecindad=True)
    check(f2.budget_used("G2-multidia") == 1 + 9 + 1,
          f"la adopción cobró las 9 celdas + la nueva: {f2.budget_used('G2-multidia')} cartuchos")


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

    f2.preregister("G1-nocturna", cfg, "candidata de prueba")
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
    check(len(f2.read_ledger()) == 60, "60 líneas, como dice el README")
    check(f2.phase2_is_open() is False, "la Fase 2 todavía NO está abierta en el ledger real")

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
    print("    -- apertura de Fase 2 sin el margen: abre, pero G1 queda bloqueada")
    e = f2.open_phase2(margen_nocturno_mes=None, data_dir=os.path.join(REPO, "data"))
    check(f2.phase2_is_open() is True, "entrada APERTURA_FASE2 escrita")
    check(e["K_total"] == 257 and e["alpha"] == 0.05, "K_total y α quedan en el acta")
    check(f2.g1_enabled() is False, "G1 bloqueada: falta el margen nocturno (§7.3)")
    check("BLOQUEADA" in e["note"], "y el acta lo dice con todas las letras")
    check(isinstance(e["data_sha256"], dict) and len(e["data_sha256"]) == 3,
          "los SHA-256 de los tres archivos de datos quedan congelados")
    check(f2.verify_ledger() is True, "cadena válida después de la apertura")

    fresh_ledger(tmp)
    print("    -- con el margen declarado, G1 se habilita")
    f2.open_phase2(margen_nocturno_mes={"valor_usd": 1234.0, "fuente": "PRUEBA",
                                        "leido_el": "2026-08-23"},
                   data_dir=os.path.join(REPO, "data"))
    check(f2.g1_enabled() is True, "G1 habilitada solo con valor + fuente + fecha")


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
        for fn in (s2_prerregistro, s3_presupuesto, s4_vecindad, s5_ventanas,
                   s6_caja_fuerte, s7_barra_y_anios, s8_ledger_y_apertura):
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
