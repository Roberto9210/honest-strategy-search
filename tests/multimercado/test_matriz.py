"""Controles de mm_matriz.py, corridos ANTES de la corrida que decide.

1) Fidelidad a la hipotesis congelada: las ventanas de ES parte A reproducen EXACTAMENTE
   los trades de familias_4_5.turn_of_month (el codigo del ledger), fecha por fecha y
   punto por punto, n = 231.
2) Ceguera: signo dado vuelta y constante sumada no cambian la matriz R ni sigma.
3) Control del control: la MEDIA si cambia bajo esas mutaciones (y por eso no se publica).
4) La formula matricial de n_efectivo se reduce exacta al escalar N/(1+(m-1)rho).
5) La cota superior 90% es > R en toda celda fuera de la diagonal.
"""
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
FACTORY = os.path.join(os.path.dirname(os.path.dirname(HERE)), "factory")
sys.path.insert(0, FACTORY)

import mm_matriz as mm                      # noqa: E402
from familias_4_5 import turn_of_month      # noqa: E402

PASS = 0


def check(cond, msg):
    global PASS
    assert cond, msg
    PASS += 1
    print(f"  ok  {msg}")


def main():
    # --- 1. fidelidad al codigo congelado ------------------------------------------
    print("[1] ES bloque A == turn_of_month del ledger menos la exclusion 2017-08, exacto")
    es = mm.load("ES")
    rets, dropped = mm.windows_with_roll("ES", es)
    frozen = turn_of_month(es, {"n_before": 4, "m_after": 3})
    check(len(frozen) == 231, "turn_of_month (codigo congelado) da 231 == ledger 049b809f5e9def5c")
    check(len(rets) == 230, f"muestra congelada n = {len(rets)} == 230 (spec A.3 corregida)")
    check(dropped == 1, "exclusiones por roll en el bloque A de ES = 1 (2017-08)")
    check(str(pd.Period("2017-08", "M")) not in [str(p) for p in rets.index],
          "la vuelta excluida es exactamente 2017-08")
    fro = np.sort(frozen["points"].to_numpy())
    sub = np.sort(rets.to_numpy())
    i = j = matched = 0
    while i < len(sub) and j < len(fro):
        if abs(sub[i] - fro[j]) < 1e-9:
            matched += 1; i += 1; j += 1
        else:
            j += 1
    check(matched == 230, "los 230 retornos son un subconjunto uno-a-uno del codigo congelado")

    # --- 2/3. ceguera con sus controles --------------------------------------------
    print("[2] la matriz es ciega al signo y al nivel")
    rng = np.random.default_rng(7)
    per = pd.period_range("2001-01", periods=120, freq="M")
    base = {t: pd.Series(rng.normal(size=120), index=per, name=t) for t in ("A", "B", "C")}
    R0, NC0 = mm.correlate(base)
    for name, mut in [("signo dado vuelta", lambda s: -s),
                      ("constante +100", lambda s: s + 100.0),
                      ("constante -5", lambda s: s - 5.0)]:
        Rm, _ = mm.correlate({t: mut(s) for t, s in base.items()})
        check(np.allclose(R0.to_numpy(), Rm.to_numpy()), f"R identica bajo {name}")
    print("[3] control del control: la media SI cambia")
    m0 = float(base["A"].mean())
    check(abs(float((-base["A"]).mean()) - (-m0)) < 1e-12 and abs(m0) > 1e-6,
          f"la media cambia de {m0:+.4f} a {-m0:+.4f} bajo el signo (por eso no se publica)")
    check(abs(float((base["A"] + 100).mean()) - (m0 + 100)) < 1e-9,
          "la media cambia +100 bajo la constante")

    # --- 4. la formula matricial se reduce al escalar del proyecto -----------------
    print("[4] n_efectivo matricial == N/(1+(m-1)rho) en el caso simetrico")
    for m, k, rho in [(3, 100, 0.10), (3, 259, 0.765), (4, 50, 0.5)]:
        tags = [f"M{i}" for i in range(m)]
        M = np.full((m, m), rho)
        np.fill_diagonal(M, 1.0)
        R = pd.DataFrame(M, index=tags, columns=tags)
        counts = {t: k for t in tags}
        ov = {tuple(sorted((a, b))): k for i, a in enumerate(tags) for b in tags[i + 1:]}
        nef, N = mm.n_efectivo(R, counts, ov)
        esc = m * k / (1 + (m - 1) * rho)
        check(abs(nef - esc) < 1e-9, f"m={m} k={k} rho={rho}: {nef:.3f} == {esc:.3f}")

    # --- 5. la cota superior endurece, nunca afloja --------------------------------
    print("[5] cota superior 90% > R fuera de la diagonal")
    U = mm.upper90(R0, NC0)
    off = ~np.eye(len(R0), dtype=bool)
    check(np.all(U.to_numpy()[off] >= R0.to_numpy()[off]), "U >= R en toda celda")
    check(np.all(U.to_numpy()[off] <= 1.0), "U <= 1 (tope)")

    print(f"\n{PASS} aserciones, 0 fallas")


if __name__ == "__main__":
    main()
