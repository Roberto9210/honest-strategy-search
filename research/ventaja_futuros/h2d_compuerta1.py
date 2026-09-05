"""COMPUERTA 1 de H2d sobre el mirado -- ejecuta hipotesis_congeladas.md Enmienda 3 (E3.4).

ES diario de NT8 (CSV del guardian), contrato de maximo volumen por fecha, pares consecutivos mismo
contrato, 2016-08-23 -> 2019-12-31 (851 pares esperados). NO toca la caja: ninguna fecha >= 2020-01-01
se lee para calcular nada. C0 primero y, si dispara, se para ahi. C1-C5 arriba del resultado.

    venv/Scripts/python.exe research/ventaja_futuros/h2d_compuerta1.py > research/ventaja_futuros/h2d_compuerta1.txt
"""

from __future__ import annotations

import glob
import os
import sys
from math import erfc, sqrt
from statistics import NormalDist

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from potencia_heredada import _binom_pmf  # noqa: E402

GUARD_CSV = (r"C:\Users\home\AppData\Local\Temp\claude\C--Users-home-Desktop-ALAYA"
             r"\03cf4965-af02-4a1f-8eb0-bc27e9d414df\scratchpad\nt8-daily-csv")
MIRADO = ("2016-08-23", "2019-12-31")
FRONTERA = "2020-01-01"
N_PARES_ESPERADOS = 851
N_CAJA = 1687                    # pares de la caja, contados de fechas en potencia_heredada.txt (calendario, no precios)
POINT_VALUE = 5.0                # USD por punto de MES
FRICTION_RT = 3.90               # USD ida y vuelta por contrato, factory/harness.py
TICK = 0.25
K_PROG = 261
ALPHA = 0.05 / (K_PROG + 1)      # K_D = 1
N = NormalDist()
Z_LINE = N.inv_cdf(1 - ALPHA / 2)
SEED = 20260903
N_PERM = 1000


def hr(t):
    print()
    print("=" * 118)
    print(t)
    print("=" * 118)


def load_root(root):
    frames = []
    for fn in sorted(glob.glob(os.path.join(GUARD_CSV, f"{root}_*.csv"))):
        d = pd.read_csv(fn)
        d["contract"] = os.path.basename(fn)[:-4]
        frames.append(d)
    if not frames:
        raise SystemExit(f"no hay {root}_*.csv en {GUARD_CSV}")
    d = pd.concat(frames, ignore_index=True)
    d["date"] = pd.to_datetime(d["date"])
    # LA CAJA NO SE LEE: se descarta toda fila >= FRONTERA antes de cualquier calculo
    d = d[d["date"] < FRONTERA]
    d = d.sort_values(["date", "volume"], ascending=[True, False])
    top2 = d.groupby("date").head(2)
    ties = top2.groupby("date")["volume"].agg(lambda s: len(s) == 2 and s.iloc[0] == s.iloc[1])
    if ties.any():
        raise SystemExit(f"EMPATE de volumen en {int(ties.sum())} fechas")
    sel = d.groupby("date").head(1).sort_values("date").reset_index(drop=True)
    sel["same"] = sel["contract"] == sel["contract"].shift(1)
    sel.loc[0, "same"] = False
    sel["close_prev"] = sel["close"].shift(1)
    sel["close_prev2"] = sel["close"].shift(2)
    sel["same2"] = sel["same"] & sel["same"].shift(1, fill_value=False)
    return sel


def rule(df, sig, contracts=1):
    """Aplica la regla de H2d con una senal de signo dada (serie alineada a df). Devuelve DataFrame de operaciones."""
    ops = df[(sig != 0)].copy()
    s = np.sign(sig[sig != 0]).to_numpy()
    ops["side"] = s
    ops["bruto_pts"] = s * (ops["close"] - ops["open"])
    ops["bruto_usd"] = ops["bruto_pts"] * POINT_VALUE * contracts
    ops["friccion"] = FRICTION_RT * contracts
    ops["neto"] = ops["bruto_usd"] - ops["friccion"]
    ops["acierto"] = ops["neto"] > 0
    return ops


def t_stat(x):
    x = np.asarray(x, dtype=float)
    n = len(x)
    if n < 2:
        return float("nan"), float("nan"), n
    sd = x.std(ddof=1)
    t = x.mean() / (sd / sqrt(n)) if sd > 0 else float("inf")
    p = erfc(abs(t) / sqrt(2))
    return t, p, n


def binom_two_sided(k, n):
    """p exacta a dos colas (suma de las probabilidades <= P(k)), H0 = 0.5."""
    pmf = _binom_pmf(n, 0.5)
    pk = pmf[k]
    return float(sum(v for v in pmf if v <= pk * (1 + 1e-12)))


def profit_factor(neto):
    g = neto[neto > 0].sum()
    l = -neto[neto < 0].sum()
    return float(g / l) if l > 0 else float("inf")


def report_ops(label, ops, decide=False):
    t, p, n = t_stat(ops["neto"])
    k = int(ops["acierto"].sum())
    hit = k / n
    pb = binom_two_sided(k, n)
    pf = profit_factor(ops["neto"].to_numpy())
    print(f"  {label}")
    print(f"    n = {n}   aciertos = {k}   acierto = {100 * hit:.2f} %   binomial dos colas p = {pb:.3e}")
    print(f"    media neta = {ops['neto'].mean():+.3f} USD   desvio = {ops['neto'].std(ddof=1):.3f}   t = {t:+.3f}   p_crudo = {p:.3e}   PF neto = {pf:.3f}")
    print(f"    media bruta = {ops['bruto_pts'].mean():+.3f} pts ES   friccion por op = {ops['friccion'].iloc[0]:.2f} USD")
    return {"n": n, "k": k, "hit": hit, "pb": pb, "t": t, "p": p, "pf": pf, "mean": float(ops["neto"].mean())}


def main():
    print("COMPUERTA 1 DE H2d SOBRE EL MIRADO -- Ventana D, 2026-09-03. ES diario NT8, contrato de max volumen, pares mismo contrato.")
    print(f"Ejecuta hipotesis_congeladas.md Enmienda 3 E3.4. alpha = 0.05/{K_PROG + 1} = {ALPHA:.4e}; |t| >= {Z_LINE:.3f}; linea de la suerte 1/(K+1) = {1 / (K_PROG + 2):.5f}")
    print("LA CAJA NO SE LEE: el cargador descarta toda fila >= 2020-01-01 antes de calcular nada.")

    es = load_root("ES")
    m = es[(es["date"] >= MIRADO[0]) & (es["date"] <= MIRADO[1])].copy()
    pares = m[m["same"]].copy()
    hr(f"0. POBLACION: fechas en el mirado {len(m)} ({m['date'].min().date()} -> {m['date'].max().date()}); pares mismo contrato {len(pares)}; esperados {N_PARES_ESPERADOS}")
    assert len(pares) == N_PARES_ESPERADOS, len(pares)
    pares["gap"] = pares["open"] - pares["close_prev"]
    pares["cc"] = pares["close"] - pares["close_prev"]

    # ---------------------------------------------------------------- C0
    hr("C0 - PRECONDICION -- si dispara, H2d muere aqui y el script termina")
    ident = float((pares["gap"] == 0).mean())
    var_gap, var_cc = float(pares["gap"].var(ddof=1)), float(pares["cc"].var(ddof=1))
    frac = var_gap / var_cc
    print(f"  fechas con open_t == close_(t-1) exacto: {int((pares['gap'] == 0).sum())} de {len(pares)} = {100 * ident:.2f} %   (criterio: > 10 % dispara)")
    print(f"  varianza(gap) = {var_gap:.3f}   varianza(close_t - close_(t-1)) = {var_cc:.3f}   fraccion = {100 * frac:.2f} %   (criterio: < 10 % dispara)")
    print(f"  |gap| p50 = {pares['gap'].abs().median():.2f} pts   |cc| p50 = {pares['cc'].abs().median():.2f} pts")
    c0_fires = ident > 0.10 or frac < 0.10
    print(f"  C0: {'DISPARA -- H2d NO es medible como hueco nocturno con estas columnas. H2d MUERE. Nada mas se calcula.' if c0_fires else 'NO dispara -- H2d es medible con estas columnas'}")
    if c0_fires:
        return

    real = rule(pares, pares["gap"])

    # ---------------------------------------------------------------- C1 placebo de signo
    hr(f"C1 - PLACEBO DE SIGNO -- {N_PERM} permutaciones de sign(gap), semilla {SEED}; banda 2.5-97.5 % del acierto y del t")
    rng = np.random.default_rng(SEED)
    base_sign = np.sign(real["side"].to_numpy())
    pts = (real["close"] - real["open"]).to_numpy()
    hits, ts = [], []
    for _ in range(N_PERM):
        s = rng.permutation(base_sign)
        neto = s * pts * POINT_VALUE - FRICTION_RT
        hits.append((neto > 0).mean())
        ts.append(neto.mean() / (neto.std(ddof=1) / sqrt(len(neto))))
    hits, ts = np.array(hits), np.array(ts)
    print(f"  acierto permutado: p2.5 = {100 * np.percentile(hits, 2.5):.2f} %   p50 = {100 * np.percentile(hits, 50):.2f} %   p97.5 = {100 * np.percentile(hits, 97.5):.2f} %")
    print(f"  t permutado:       p2.5 = {np.percentile(ts, 2.5):+.3f}   p50 = {np.percentile(ts, 50):+.3f}   p97.5 = {np.percentile(ts, 97.5):+.3f}")
    print("  (el real se imprime abajo; C1 pasa si el real cae fuera de las dos bandas)")

    # ---------------------------------------------------------------- C2 rival momentum
    hr("C2 - RIVAL: momentum diario sign(close_(t-1) - close_(t-2)), mismo contrato en t-2, t-1, t")
    p2 = pares[pares["same2"]].copy()
    mom = rule(p2, p2["close_prev"] - p2["close_prev2"])
    r2 = report_ops("momentum de un dia", mom)

    # ---------------------------------------------------------------- C3 otro libro
    hr("C3 - OTRO LIBRO: la misma regla sobre MES diario NT8, pares de 2019 (< 2020), y ES en las mismas fechas")
    mes = load_root("MES")
    mes_p = mes[mes["same"]].copy()
    mes_p["gap"] = mes_p["open"] - mes_p["close_prev"]
    mes_ops = rule(mes_p, mes_p["gap"])
    r3m = report_ops(f"MES {mes_p['date'].min().date()} -> {mes_p['date'].max().date()}", mes_ops)
    common = pares[pares["date"].isin(mes_p["date"])]
    es_ops_c = rule(common, common["gap"])
    r3e = report_ops("ES, mismas fechas", es_ops_c)
    same_sign = (np.sign(r3m["hit"] - 0.5) == np.sign(r3e["hit"] - 0.5)) and (np.sign(r3m["mean"]) == np.sign(r3e["mean"]))
    print(f"  C3: signos de (acierto - 0.5) y de la media neta {'COINCIDEN' if same_sign else 'NO COINCIDEN -- artefacto de contrato a declarar'}")

    # ---------------------------------------------------------------- C4 escala
    hr("C4 - ESCALA: 2 contratos")
    two = rule(pares, pares["gap"], contracts=2)
    ok4 = np.allclose(two["bruto_usd"], 2 * real["bruto_usd"]) and np.allclose(two["friccion"], 2 * real["friccion"])
    print(f"  bruto 2x exacto: {np.allclose(two['bruto_usd'], 2 * real['bruto_usd'])}   friccion 2x exacta: {np.allclose(two['friccion'], 2 * real['friccion'])}   C4: {'PASA' if ok4 else 'FALLA'}")

    # ---------------------------------------------------------------- C5 uniones
    hr("C5 - UNIONES: fechas del mirado descartadas por cambio de contrato")
    rolls = m[~m["same"]]
    rolls = rolls[rolls["date"] > m["date"].min()]
    print(f"  descartadas: {len(rolls)}   meses: {sorted(rolls['date'].dt.strftime('%Y-%m').tolist())}")

    # ---------------------------------------------------------------- RESULTADO
    hr("RESULTADO -- H2d, regla congelada, sobre los pares del mirado")
    r = report_ops("H2d real (|gap| >= 0.25, un contrato)", real)
    print(f"  huecos nulos que no operan: {len(pares) - r['n']} de {len(pares)}")
    print(f"  C1: acierto real {100 * r['hit']:.2f} % {'FUERA' if not (np.percentile(hits, 2.5) <= r['hit'] <= np.percentile(hits, 97.5)) else 'DENTRO'} de la banda; t real {r['t']:+.3f} {'FUERA' if not (np.percentile(ts, 2.5) <= r['t'] <= np.percentile(ts, 97.5)) else 'DENTRO'} de la banda")
    print(f"  C2: rival momentum acierto {100 * r2['hit']:.2f} % / t {r2['t']:+.3f}  contra real {100 * r['hit']:.2f} % / t {r['t']:+.3f}  -> {'el rival IGUALA O SUPERA: la atribucion al hueco cae' if r2['t'] >= r['t'] else 'el rival queda por debajo'}")

    # sin el mejor 1 %
    k_drop = int(np.ceil(0.01 * r["n"]))
    trimmed = np.sort(real["neto"].to_numpy())[:-k_drop]
    t_tr, p_tr, n_tr = t_stat(trimmed)
    print(f"  sin el mejor 1 % ({k_drop} operaciones): n = {n_tr}   t = {t_tr:+.3f}   p_crudo = {p_tr:.3e}   PF = {profit_factor(trimmed):.3f}")

    # vecindad: 2 ticks, impresa sin adoptar
    two_tick = rule(pares, pares["gap"].where(pares["gap"].abs() >= 2 * TICK, 0.0))
    rv = report_ops("vecindad |gap| >= 0.50 (impresa, NO adoptada)", two_tick)

    # por ano
    print("  por ano (neto USD, acierto):")
    for y, g in real.groupby(real["date"].dt.year):
        print(f"    {y}: n = {len(g):>3}   neto = {g['neto'].sum():+9.2f}   acierto = {100 * g['acierto'].mean():.1f} %")

    # ---------------------------------------------------------------- COMPUERTAS
    hr("COMPUERTA 1 -- cada criterio, fijado en E3.4")
    crit = [
        ("n_A >= 100", r["n"] >= 100),
        (f"|t_A| >= {Z_LINE:.3f} (p <= 0.05/262)", abs(r["t"]) >= Z_LINE),
        ("binomial dos colas p <= 0.05/262 con acierto > 0.5", r["pb"] <= ALPHA and r["hit"] > 0.5),
        ("PF neto >= 1.3", r["pf"] >= 1.3),
        (f"t_A sin el mejor 1 % >= {Z_LINE:.3f}", t_tr >= Z_LINE),
        ("vecindad (2 ticks) no pierde plata", rv["mean"] > 0),
        ("no solapamiento: una operacion por sesion", True),
    ]
    for lab, ok in crit:
        print(f"  [{'PASA' if ok else 'FALLA'}] {lab}")
    passed = all(ok for _, ok in crit)
    print(f"  media neta > 0: {'si' if r['mean'] > 0 else 'no'}   p_crudo {r['p']:.3e} contra la linea de la suerte {1 / (K_PROG + 2):.5f}: {'por debajo' if r['p'] < 1 / (K_PROG + 2) else 'POR ENCIMA (peor que el mejor del azar)'}")
    print(f"  COMPUERTA 1: {'PASA' if passed else 'NO PASA -- H2d MUERE sin haber gastado la caja'}")

    hr("COMPUERTA 2 -- potencia proyectada con n_B del CALENDARIO de la caja (ningun precio de B)")
    rate = r["n"] / len(pares)
    n_b = N_CAJA * rate
    bar = 2.8016 * sqrt(r["n"] / n_b)
    print(f"  tasa de operacion en A = {r['n']}/{len(pares)} = {rate:.4f}   n_B proyectado = {N_CAJA} x {rate:.4f} = {n_b:.0f}")
    print(f"  vara: |t_A| >= 2.8016 x sqrt({r['n']}/{n_b:.0f}) = {bar:.3f}   t_A = {r['t']:+.3f}   -> {'PASA' if abs(r['t']) >= bar else 'NO PASA'}")
    print(f"  barra efectiva en A = max({Z_LINE:.3f}, {bar:.3f}) = {max(Z_LINE, bar):.3f}")
    print()
    print("  LA CAJA SIGUE CERRADA. Este script no leyo ninguna fila >= 2020-01-01.")


if __name__ == "__main__":
    main()
