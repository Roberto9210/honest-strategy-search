"""
VENTANA G - COMPUERTA 1: sobrevive la cuenta a una posicion de un cierre al siguiente?

NO GASTA CARTUCHO. K = 261. Es una compuerta de FACTIBILIDAD sobre datos ya medidos, no una
hipotesis sobre el mercado: no se busca ninguna ventaja, no hay estadistico de prueba contra
un alfa, no se elige entre candidatas. Se mide si una mecanica de ejecucion cabe dentro de
un limite de perdida que ya esta publicado. Que nadie la cuente como test.

POR QUE VA PRIMERO. TMAC/BTIC/TACO fijan el precio por formula (VWAP de los ultimos 30
segundos antes de las 16:00 ET, cierre del indice, apertura especial) y no por el libro.
Ejecutar asi significa entrar en un cierre y salir en otro: NO HAY objetivo ni stop
intradiario, la posicion queda expuesta toda la noche sin freno. Si el salto nocturno solo
ya mata la cuenta, la rama se cierra y no hay nada que optimizar despues.

PROCEDENCIA DE LOS PARAMETROS
  Drawdown: "Trailing Max Drawdown (EOD) $2.000" para la 50K Growth, widget oficial de
    tradeify.co leido 2026-09-03 (datos_crudos.md). Es TRAILING: sube con las ganancias y
    no baja. Se usa esa mecanica, no un piso fijo.
  Valor del punto de ES: $50, tabla oficial de instrumentos de apextraderfunding.com leida
    2026-09-03 ("E-mini S&P 500 | ES | CME | 0.25 | $50"). Consistente con MES $5 x 10 y con
    el limite de Tradeify "4 minis/40 micros". La pagina de CME dio timeout hoy al
    reverificar; se deja anotado.
  Elegibilidad: solo E-mini completos. Los Micro E-mini NO son elegibles para TMAC, asi que
    la unidad minima de esta rama es UN ES = $50/punto. No se puede bajar el tamano.

DATOS: ES 1-min Databento, 2016-01-04 -> 2019-12-31. FUERA de la caja sellada
(2020-01-02 -> 2026-08-19). La caja no se toca.
"""
import os
import sys

import numpy as np
import pandas as pd

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(RAIZ, "research", "ventaja_futuros"))
from terreno_tenencia import load_databento, DEGRADED_UTC  # noqa: E402

PUNTO_ES = 50.0        # USD por punto, UN E-mini completo
DRAWDOWN = 2000.0      # USD, trailing EOD
CIERRE_M = 15 * 60     # 15:00 CT = 16:00 ET
NOCHES = [5, 10, 20]
NCAM = 200_000
RNG = np.random.default_rng(20260904)


def serie_cierres():
    """Cierre de RTH por sesion mas la excursion adversa entre cierres consecutivos.
    Solo pares de sesiones con el MISMO contrato: un roll no es una perdida."""
    df = load_databento()
    degraded = set(df.loc[df["utc_date"].isin(DEGRADED_UTC), "sess"].unique())
    # Mismo filtro que los scripts de terreno: una sesion con dos contratos es un roll y no
    # se puede leer como una serie de precios continua.
    ncon = df.groupby("sess")["contract"].nunique()
    limpias = set(ncon[ncon == 1].index) - degraded
    df = df[df["sess"].isin(limpias)]

    cierres = df[df["m"] == CIERRE_M].groupby("sess").agg(
        close=("close", "last"), contract=("contract", "last"))
    cierres = cierres[cierres.index.weekday < 5].sort_index()

    # Excursion entre dos cierres consecutivos: sobre las barras posteriores al cierre de
    # t-1 y hasta el cierre de t inclusive. Es la exposicion real de la posicion nocturna.
    df = df.sort_values("ts_event_utc").reset_index(drop=True)
    marca = (df["m"] == CIERRE_M)
    df["bloque"] = marca.shift(1, fill_value=False).cumsum()
    ext = df.groupby("bloque").agg(lo=("low", "min"), hi=("high", "max"),
                                    sess_fin=("sess", "last"))
    # Un bloque que no termina en un cierre (feriado, cierre anticipado) puede compartir
    # sesion final con otro: se colapsan al peor caso, que es el conservador.
    ext = ext.groupby("sess_fin").agg(lo=("lo", "min"), hi=("hi", "max"))

    out = pd.DataFrame(index=cierres.index)
    out["close"] = cierres["close"]
    out["contract"] = cierres["contract"]
    out["prev"] = cierres["close"].shift(1)
    out["prev_contract"] = cierres["contract"].shift(1)
    out["lo"] = ext["lo"].reindex(out.index)
    out["hi"] = ext["hi"].reindex(out.index)
    out = out[(out["contract"] == out["prev_contract"]) & out["prev"].notna()
              & out["lo"].notna()]
    out["mov"] = out["close"] - out["prev"]              # puntos, cierre a cierre
    out["adv_largo"] = out["prev"] - out["lo"]           # excursion adversa de un largo
    out["adv_corto"] = out["hi"] - out["prev"]           # excursion adversa de un corto
    return out


def simular(mov, adv_l, adv_c, n_noches, contratos, intradia, historico,
            npaths=NCAM, rng=None, drawdown=DRAWDOWN):
    """Trailing EOD sobre n_noches consecutivas. Lado al azar cada noche (sin ventaja).
    historico=True usa bloques consecutivos reales (conserva el agrupamiento);
    historico=False remuestrea IID. Devuelve la fraccion que rompe el piso."""
    rng = rng or np.random.default_rng(20260904)
    v = contratos * PUNTO_ES
    m = len(mov)
    if historico:
        if m - n_noches <= 0:
            return float("nan")
        arranques = rng.integers(0, m - n_noches, npaths)
        idx = arranques[:, None] + np.arange(n_noches)[None, :]
    else:
        idx = rng.integers(0, m, (npaths, n_noches))
    largo = rng.random((npaths, n_noches)) < 0.5

    bal = np.zeros(npaths)
    alto = np.zeros(npaths)
    vivo = np.ones(npaths, dtype=bool)
    for j in range(n_noches):
        k = idx[:, j]
        piso = np.minimum(alto - drawdown, 0.0)
        if intradia:
            adv = np.where(largo[:, j], adv_l[k], adv_c[k]) * v
            rompe = vivo & ((bal - adv) <= piso)
        else:
            rompe = np.zeros(npaths, dtype=bool)
        paso = np.where(largo[:, j], mov[k], -mov[k]) * v
        nuevo = bal + paso
        rompe |= vivo & (nuevo <= piso)
        vivo &= ~rompe
        bal = np.where(vivo, nuevo, bal)
        alto = np.maximum(alto, bal)
    return 1.0 - vivo.mean()


def main():
    print("=" * 100)
    print("COMPUERTA 1 - sobrevive la cuenta a una posicion de un cierre al siguiente?")
    print("NO GASTA CARTUCHO. K = 261. Compuerta de factibilidad, no hipotesis de mercado.")
    print("=" * 100)
    d = serie_cierres()
    mov = d["mov"].to_numpy(float)
    adv_l = np.clip(d["adv_largo"].to_numpy(float), 0, None)
    adv_c = np.clip(d["adv_corto"].to_numpy(float), 0, None)
    print(f"\n(a) Drawdown 50K Growth: ${DRAWDOWN:,.0f} TRAILING EOD (tradeify.co, 2026-09-03).")
    print(f"    Un E-mini = ${PUNTO_ES:.0f}/punto -> el drawdown entero son "
          f"{DRAWDOWN/PUNTO_ES:.0f} PUNTOS de ES.")
    print(f"    Micro E-mini NO elegible para TMAC: no se puede bajar de 1 contrato.")
    print(f"\n(b) Movimientos cierre a cierre, ES 1-min Databento, "
          f"{d.index.min().date()} -> {d.index.max().date()}")
    print(f"    (fuera de la caja sellada 2020-2026). n = {len(d):,} noches, "
          f"solo pares con el mismo contrato.")
    print(f"    {'':>14}{'puntos':>10}{'USD (1 ES)':>13}")
    for et, q in (("mediana |mov|", np.median(np.abs(mov))),
                   ("p90 |mov|", np.percentile(np.abs(mov), 90)),
                   ("p99 |mov|", np.percentile(np.abs(mov), 99)),
                   ("maximo |mov|", np.abs(mov).max())):
        print(f"    {et:>14}{q:>10.2f}{q*PUNTO_ES:>13,.0f}")

    print(f"\n(c) Fraccion de noches SUELTAS que exceden el drawdown de "
          f"{DRAWDOWN/PUNTO_ES:.0f} puntos:")
    for et, x in (("cierre a cierre, en contra", np.abs(mov)),
                   ("excursion adversa, largo", adv_l),
                   ("excursion adversa, corto", adv_c)):
        f = (x >= DRAWDOWN / PUNTO_ES).mean()
        una = f"1 de cada {1/f:,.0f}" if f > 0 else "ninguna"
        print(f"    {et:<28}{f*100:>7.2f}%   {una} noches")

    print(f"\n(d) Probabilidad de MORIR antes de completar N noches (trailing, lado al azar):")
    print(f"    {'N':>4}{'cierre IID':>13}{'cierre hist':>14}{'intradia IID':>15}"
          f"{'intradia hist':>16}")
    for n in NOCHES:
        a = simular(mov, adv_l, adv_c, n, 1, False, False, rng=np.random.default_rng(1))
        b = simular(mov, adv_l, adv_c, n, 1, False, True, rng=np.random.default_rng(2))
        c = simular(mov, adv_l, adv_c, n, 1, True, False, rng=np.random.default_rng(3))
        e = simular(mov, adv_l, adv_c, n, 1, True, True, rng=np.random.default_rng(4))
        print(f"    {n:>4}{a*100:>12.1f}%{b*100:>13.1f}%{c*100:>14.1f}%{e*100:>15.1f}%")

    print(f"\nCONTROL - con tamano de posicion CERO las cuatro medidas deben dar 0,00%")
    ok = True
    for n in NOCHES:
        vals = [simular(mov, adv_l, adv_c, n, 0, itd, hist,
                        rng=np.random.default_rng(9))
                for itd in (False, True) for hist in (False, True)]
        malo = [v for v in vals if v > 1e-12]
        ok &= not malo
        print(f"    N={n:>2}: " + "  ".join(f"{v*100:.2f}%" for v in vals) +
              f"   {'OK' if not malo else 'MAL'}")
    print(f"CONTROL {'PASADO' if ok else 'FALLADO'}")
    if not ok:
        raise SystemExit("Control fallado: el modelo esta mal, no se publica nada.")

    # Cierre constructivo: no se puede bajar el tamano (el micro no es elegible), asi que
    # la unica palanca es un drawdown mas grande, o sea una cuenta mas grande.
    print("\nQUE DRAWDOWN HARIA FALTA (la unica palanca: no se puede achicar el contrato)")
    print(f"    {'drawdown':>10}{'puntos':>9}{'muerte en 10 noches, intradia hist':>36}")
    for dd in (2000, 3000, 4500, 9000, 20000, 40000):
        p = simular(mov, adv_l, adv_c, 10, 1, True, True,
                    rng=np.random.default_rng(4), drawdown=float(dd))
        print(f"    ${dd:>9,}{dd/PUNTO_ES:>9.0f}{p*100:>35.1f}%")
    print("    Referencia: el drawdown mas grande de las ocho firmas medidas es $4.500")
    print("    (Topstep 150K). Ninguna cuenta del mercado medido llega a lo que haria falta.")
    return d


if __name__ == "__main__":
    main()
