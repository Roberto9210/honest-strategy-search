# -*- coding: utf-8 -*-
"""La medicion ciega es ciega: pruebas conductuales con controles.

La afirmacion que hay que probar no es "la funcion parece prudente", es:
LA SALIDA NO PUEDE DISTINGUIR UNA REGLA GANADORA DE UNA PERDEDORA.
Se prueba dandole vuelta el signo a todas las operaciones y exigiendo que la
salida sea identica bit a bit. Si cambiara, la eleccion de mercados podria estar
contaminada por el resultado, que es lo que el fuera de muestra no perdona.
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "factory"))

import sigma_ciego as sc  # noqa: E402
from familia_g2 import reversion_k_dias  # noqa: E402

OK = 0
FAIL: list[str] = []


def check(cond: bool, label: str) -> None:
    global OK
    if cond:
        OK += 1
        print(f"    ok   {label}")
    else:
        FAIL.append(label)
        print(f"    FALLA {label}")


def serie_falsa(n: int = 3000, semilla: int = 7) -> pd.DataFrame:
    rng = np.random.default_rng(semilla)
    precio = 1000 + np.cumsum(rng.normal(0.05, 8.0, n))
    idx = pd.bdate_range("2005-01-03", periods=n)
    return pd.DataFrame({"open": precio, "high": precio + 3, "low": precio - 3,
                         "close": precio, "volume": 1000.0}, index=idx)


def con_signo_dado_vuelta(fn):
    def envuelta(df, config):
        t = fn(df, config).copy()
        t["points"] = -t["points"]
        return t
    return envuelta


def con_constante(fn, c):
    def envuelta(df, config):
        t = fn(df, config).copy()
        t["points"] = t["points"] + c
        return t
    return envuelta


def s1_contrato():
    print("\n[1] el contrato de salida: solo dispersion, frecuencia y bordes")
    df = serie_falsa()
    cfg = {"k": 3, "side": 1, "hold": 3}
    out = sc.medir_ciego(reversion_k_dias, df, cfg, tick_size=0.25, mercado="FALSO")
    check(set(out) <= set(sc.CLAVES_PERMITIDAS),
          f"claves devueltas: {sorted(out)}")
    check(all(isinstance(v, (int, float, str)) for v in out.values()),
          "todos los valores son escalares o texto (ningun vector)")
    check(out["n_operaciones"] > 0 and out["sigma_puntos"] > 0,
          f"midio algo: n={out['n_operaciones']}, sigma={out['sigma_puntos']:.4f}")

    print("    -- y una clave de rentabilidad no puede colarse")
    for mala in ("media_neta", "pnl_total", "ganadoras", "retorno_medio"):
        try:
            sc._validar_salida({mala: 1.0})
            check(False, f"{mala!r} deberia haber sido rechazada")
        except sc.FugaDeResultado:
            check(True, f"{mala!r} -> FugaDeResultado")
    try:
        sc._validar_salida({"sigma_puntos": np.array([1.0, 2.0])})
        check(False, "un vector deberia haber sido rechazado")
    except sc.FugaDeResultado:
        check(True, "un vector en la salida -> FugaDeResultado")


def s2_el_control_que_manda():
    print("\n[2] EL CONTROL: la salida no distingue ganar de perder")
    df = serie_falsa()
    cfg = {"k": 3, "side": 1, "hold": 3}
    normal = sc.medir_ciego(reversion_k_dias, df, cfg, 0.25, "FALSO")
    volteada = sc.medir_ciego(con_signo_dado_vuelta(reversion_k_dias), df, cfg,
                              0.25, "FALSO")
    check(normal == volteada,
          "invertir el signo de TODAS las operaciones no cambia ni un campo")

    print("    -- y sumarle una constante a cada operacion tampoco")
    for c in (5.0, -5.0, 100.0):
        corrida = sc.medir_ciego(con_constante(reversion_k_dias, c), df, cfg,
                                 0.25, "FALSO")
        check(corrida == normal,
              f"sumar {c:+.0f} a cada operacion (cambia la media, no sigma): "
              "salida identica")

    print("    -- CONTROL DEL CONTROL: la media SI cambiaba con esas mutaciones")
    base = reversion_k_dias(df, cfg)["points"].to_numpy(float)
    check(abs((-base).mean() - base.mean()) > 1e-9,
          f"la media pasa de {base.mean():+.5f} a {(-base).mean():+.5f}")
    check(abs((base + 5.0).mean() - base.mean() - 5.0) < 1e-9,
          "y con la constante se corre exactamente esa constante")
    check(abs(float(np.std(-base, ddof=1)) - float(np.std(base, ddof=1))) < 1e-12,
          "mientras que sigma no se mueve: por eso sigma se puede publicar y la media no")


def s3_escalado_y_friccion():
    print("\n[3] friccion en ticks, y el ancla ES/MES reproducida")
    df = serie_falsa()
    cfg = {"k": 3, "side": 1, "hold": 3}
    a = sc.medir_ciego(reversion_k_dias, df, cfg, tick_size=0.25)
    b = sc.medir_ciego(reversion_k_dias, df, cfg, tick_size=0.50)
    check(abs(a["sigma_ticks"] - 2 * b["sigma_ticks"]) < 1e-9,
          "sigma_ticks escala con el tamanio de tick, sigma_puntos no")
    check(a["sigma_puntos"] == b["sigma_puntos"], "sigma_puntos identica")

    print("    -- el ancla: MES sigma $167.37, peaje $3.90, tick $1.25")
    sigma_ticks_mes = 167.37 / 1.25
    costo_ticks_mes = 3.90 / 1.25
    f = sc.friccion(costo_ticks_mes, sigma_ticks_mes)
    check(abs(f - 0.023301) < 1e-5, f"f = {f:.6f} (publicado 0.023301)")
    check(abs(sc.n_necesario(0.107006 - f) - 1120) < 2,
          f"n necesario = {sc.n_necesario(0.107006 - f):.0f} (publicado 1120)")

    print("    -- cuantos ticks de peaje aguanta antes de morir")
    letal = sc.costo_ticks_maximo(sigma_ticks_mes)
    check(abs(letal - 0.107006 * sigma_ticks_mes) < 1e-9,
          f"peaje letal para MES = {letal:.2f} ticks (paga {costo_ticks_mes:.2f})")
    check(sc.n_necesario(-0.01) == float("inf"), "delta neto negativo -> n infinito")


def main() -> int:
    print("=" * 78)
    print("MULTI-MERCADO — la medicion ciega")
    print("=" * 78)
    for fn in (s1_contrato, s2_el_control_que_manda, s3_escalado_y_friccion):
        fn()
    print("\n" + "=" * 78)
    print(f"aserciones OK: {OK}   fallas: {len(FAIL)}")
    for f in FAIL:
        print("   FALLA:", f)
    print("=" * 78)
    return 0 if not FAIL else 1


if __name__ == "__main__":
    sys.exit(main())
