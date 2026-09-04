"""
VENTANA G - la vara convertida en criterio: PORCENTAJE DE ACIERTOS REQUERIDO.

NO GASTA CARTUCHO. K se queda en 261. Esto no pone ninguna hipotesis a prueba contra
datos: es aritmetica sobre parametros ya fijados (reglas de las firmas leidas el
2026-09-03, terreno ES 2016-2019 ya medido y commiteado). No hay poblacion nueva, no hay
estadistico de prueba, no hay decision contra un alfa. Nadie debe contarlo como un test.

QUE CALCULA
-----------
Dada una firma y un bracket (contratos N, objetivo T y stop S en puntos, costo por
operacion), despeja la tasa de acierto por operacion `p` mas baja con la que el intento
tiene esperanza POSITIVA:

    E(p) = P_pasar(p) * cobro - costo > 0        ->   P_pasar(p*) = costo / cobro

`P_pasar(p)` es la cadena entera (evaluacion x cuenta fondeada hasta el primer retiro)
simulada con la misma maquina de bracket.py: drawdown trailing del tipo que declara cada
firma, limite de perdida diario, dias minimos y dias calificados. La unica diferencia con
bracket.py es que ahi la tasa de acierto estaba clavada en S/(S+T) (sin ventaja) y aca es
la incognita.

Se usan numeros aleatorios comunes (misma semilla en cada llamada) para que P_pasar(p) sea
monotona y la biseccion no persiga ruido de Monte Carlo.

USO
---
    python vara_criterio.py --firma tradeify --contratos 10 --objetivo 20 --stop 10
    python vara_criterio.py --tabla
    python vara_criterio.py --control
    python vara_criterio.py --verificar
    python vara_criterio.py --sensibilidad
"""
import argparse
import sys

import numpy as np

from aritmetica import FIRMAS
from bracket import (C1, TICK, sim_bracket, trades_por_dia,
                     factible_escala, factible_dia, factible_horizonte)
from factibilidad import filtro_mercado, filtro_azar, veredicto_azar

SEMILLA = 20260904
NPATHS = 20_000
NPATHS_VERIF = 150_000
MAX_DAYS_FUND = 500

ALIAS = {
    "apex": "Apex (Intraday 50K)",
    "topstep": "Topstep (50K)",
    "lucid": "Lucid Pro (50K)",
    "fundednext": "FundedNext Flex (50K)",
    "blusky": "BluSky Launch (50K)",
    "tpt": "Take Profit Trader (50K)",
    "tradeify": "Tradeify Growth (50K)",
    "mffu": "MyFundedFutures Rapid (50K)",
}

# Columnas de la tabla: (objetivo pt, stop pt). El stop es lo que el terreno filtra, asi
# que hay dos anclas: 10pt (el unico punto donde el terreno casi cede) y 4pt (el regimen
# de stop apretado, que el deslizamiento medido descarta). Las dos columnas de R:R 2,0
# a distinto stop muestran por que un mismo R:R no significa lo mismo.
BRACKETS = [(5, 10), (10, 10), (20, 10), (8, 4)]
N_TABLA = 10


def p_pasar(firma, N, T_pt, S_pt, c1, p_win, npaths=NPATHS, semilla=SEMILLA):
    """Probabilidad de recorrer la cadena entera: evaluacion Y despues cuenta fondeada
    hasta el primer retiro."""
    f = FIRMAS[firma]
    T_ticks, S_ticks = T_pt * 4, S_pt * 4
    ev = dict(f["eval"])
    fu = dict(f["fund"])
    fu.setdefault("max_days", MAX_DAYS_FUND)
    p_ev, _, _ = sim_bracket(N=N, S_ticks=S_ticks, T_ticks=T_ticks, c1=c1, p_win=p_win,
                             npaths=npaths, rng=np.random.default_rng(semilla), **ev)
    p_fu, _, _ = sim_bracket(N=N, S_ticks=S_ticks, T_ticks=T_ticks, c1=c1, p_win=p_win,
                             npaths=npaths, rng=np.random.default_rng(semilla + 1), **fu)
    return p_ev * p_fu, p_ev, p_fu


def p_equilibrio(firma):
    f = FIRMAS[firma]
    return (f["precio"] + f["activacion"]) / (f["pago"] * f["split"])


def acierto_requerido(firma, N, T_pt, S_pt, c1, npaths=NPATHS, tol=2e-4):
    """Biseccion sobre la tasa de acierto por operacion. Devuelve p* en [0,1], o None si
    ni ganando siempre alcanza."""
    objetivo = p_equilibrio(firma)
    if p_pasar(firma, N, T_pt, S_pt, c1, 1.0, npaths)[0] < objetivo:
        return None
    lo, hi = 0.0, 1.0
    while hi - lo > tol:
        mid = (lo + hi) / 2
        if p_pasar(firma, N, T_pt, S_pt, c1, mid, npaths)[0] < objetivo:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def acierto_sin_ventaja(T_pt, S_pt):
    """La tasa que da el paseo sin drift: la referencia 'moneda'."""
    return S_pt / (S_pt + T_pt)


def factible(firma, N, T_pt, S_pt, c1):
    """Filtros SEPARADOS (ver factibilidad.py): el de mercado rechaza y no se negocia; el
    de azar esta calibrado sobre entradas sin ventaja, asi que frente a un candidato CON
    ventaja no rechaza, deja la celda SIN DECIDIR.
    Devuelve (estado, motivo) con estado en {'si', 'no', 'sin decidir'}."""
    f = FIRMAS[firma]
    T_ticks, S_ticks = T_pt * 4, S_pt * 4
    ev, fu = f["eval"], f["fund"]

    ok_m, ratio, _ = filtro_mercado(S_pt)
    if ok_m is None:
        return "no", "desliz. no medido"
    if ok_m is False:
        return "no", f"mercado {ratio*100:.0f}%"

    veredictos = {v: veredicto_azar(filtro_azar(T_pt, S_pt, v)) for v in ("T23", "RTH")}
    if "RECHAZA" in veredictos.values():
        return "no", "azar rechaza"
    azar_limpio = all(v == "pasa" for v in veredictos.values())

    tpd = trades_por_dia(round(S_ticks / 4))
    win = T_ticks * TICK * N - c1 * N
    if fu.get("qual_days", 0) and tpd * win < fu.get("qual_amt", 0.0):
        return "no", "no califica"
    if not factible_escala(N, S_ticks, T_ticks, ev["target"]):
        return "no", "1 op decide"
    if not (factible_dia(N, S_ticks, T_ticks, c1, ev["target"], ev["dd"])
            and factible_dia(N, S_ticks, T_ticks, c1, fu["target"], fu["dd"])):
        return "no", "1 dia decide"
    if not factible_horizonte(N, S_ticks, T_ticks, c1, ev["target"], ev["dd"],
                              ev.get("max_days", 250)):
        return "no", "horizonte"
    if azar_limpio:
        return "si", f"pasa ambos (mercado {ratio*100:.0f}%, al borde)"
    return "sin decidir", "azar indeterminado con ventaja"


def _fmt(p):
    return "  ---  " if p is None else f"{p * 100:5.1f}%"


def tabla(c1, titulo, npaths=NPATHS):
    print("=" * 104)
    print(titulo)
    print(f"N = {N_TABLA} micros MES   costo = ${c1:.2f} por micro por operacion   "
          f"{npaths:,} caminos por celda")
    print("=" * 104)
    cab = "".join(f"{f'{t}pt:{s}pt (R:R {t/s:.1f})':>22}" for t, s in BRACKETS)
    print(f"{'firma':<28}{cab}")
    print(f"{'':<28}" + "".join(f"{'sin ventaja: ' + f'{acierto_sin_ventaja(t, s)*100:.1f}%':>22}"
                                for t, s in BRACKETS))
    print("-" * 104)

    celdas = []
    for alias, nombre in ALIAS.items():
        fila = f"{nombre:<28}"
        for T_pt, S_pt in BRACKETS:
            ok, motivo = factible(nombre, N_TABLA, T_pt, S_pt, c1)
            p = acierto_requerido(nombre, N_TABLA, T_pt, S_pt, c1, npaths)
            marca = {"si": "", "sin decidir": " [?]"}.get(ok, " [x]")
            fila += f"{_fmt(p) + marca:>22}"
            if p is not None:
                celdas.append((p, nombre, T_pt, S_pt, ok))
        print(fila)

    print("-" * 104)
    if celdas:
        mejor = min(celdas, key=lambda x: x[0])
        peor = max(celdas, key=lambda x: x[0])
        print(f"MEJOR (menos acierto exigido): {mejor[1]}  {mejor[2]}pt:{mejor[3]}pt  "
              f"-> {mejor[0]*100:.1f}%   factible={mejor[4]}")
        print(f"PEOR  (mas acierto exigido):   {peor[1]}  {peor[2]}pt:{peor[3]}pt  "
              f"-> {peor[0]*100:.1f}%   factible={peor[4]}")
    return celdas


def control(npaths=NPATHS):
    print()
    celdas = tabla(0.0, "CONTROL - la misma tabla con COSTO POR OPERACION = 0", npaths)
    print()
    print("Criterio escrito a mano en el pedido: TODAS las celdas deben dar 50,0%.")
    fuera = [c for c in celdas if abs(c[0] - 0.5) > 0.005]
    if not fuera:
        print("CONTROL PASADO: todas las celdas dan 50,0%.")
        return True
    print(f"CONTROL FALLADO CONTRA EL CRITERIO ESCRITO A MANO: {len(fuera)} de "
          f"{len(celdas)} celdas no dan 50,0%.")
    print()
    print("Por que el criterio de 50,0% no puede valer, con aritmetica elemental:")
    print("  Con costo cero, un bracket que arriesga S y busca T da valor esperado nulo")
    print("  cuando p*T = (1-p)*S, es decir p = S/(S+T). Eso es 50,0% SOLO si T = S.")
    for T_pt, S_pt in BRACKETS:
        pf = acierto_sin_ventaja(T_pt, S_pt)
        ev50 = 0.5 * T_pt - 0.5 * S_pt
        print(f"    {T_pt}pt:{S_pt}pt -> equilibrio en {pf*100:.1f}%. "
              f"Con 50% de acierto el valor esperado por operacion es "
              f"{ev50:+.1f}pt, no cero.")
    print("  Exigir 50,0% en un bracket 20pt:10pt declararia 'apenas en equilibrio' a una")
    print("  estrategia que gana +5pt por operacion. El umbral esta mal, no la aritmetica.")
    print()
    print("  Es la misma clase de fallo que el '< 3 %' de terreno_stop: umbral escrito a")
    print("  mano en vez de derivado del dato. El control DERIVADO del dato es: con costo")
    print("  cero la tasa exigida por el bracket debe ser exactamente S/(S+T).")
    return False


def control_derivado(npaths=NPATHS):
    """El control que si se deriva del dato: con costo cero, el equilibrio POR OPERACION
    cae exactamente en S/(S+T). Se verifica sobre el valor esperado, que es donde vive la
    afirmacion, sin Monte Carlo de por medio."""
    print()
    print("=" * 104)
    print("CONTROL DERIVADO - con costo cero, el equilibrio por operacion = S/(S+T)")
    print("=" * 104)
    ok = True
    for T_pt, S_pt in BRACKETS:
        p = acierto_sin_ventaja(T_pt, S_pt)
        ev = p * T_pt - (1 - p) * S_pt
        bien = abs(ev) < 1e-12
        ok &= bien
        print(f"  {T_pt}pt:{S_pt}pt  p={p*100:5.1f}%  valor esperado por operacion="
              f"{ev:+.2e}pt  {'OK' if bien else 'MAL'}")
    print(f"CONTROL DERIVADO {'PASADO' if ok else 'FALLADO'}")
    return ok


def verificar():
    """Las dos comprobaciones exigidas antes de commitear."""
    print("=" * 104)
    print("VERIFICACION 1 - el script con costo cero")
    print("=" * 104)
    p = acierto_requerido("Tradeify Growth (50K)", 10, 20, 10, 0.0)
    print(f"  Tradeify 20pt:10pt, costo 0 -> acierto requerido = {p*100:.1f}%")
    print(f"  Esperado por el criterio escrito a mano: 50,0%  -> "
          f"{'COINCIDE' if abs(p - 0.5) <= 0.005 else 'NO COINCIDE'}")
    print(f"  Esperado por el criterio derivado S/(S+T) = "
          f"{acierto_sin_ventaja(20, 10)*100:.1f}% (equilibrio de la operacion, no del intento)")
    v1 = abs(p - 0.5) <= 0.005

    print()
    print("=" * 104)
    print("VERIFICACION 2 - reproducir una celda de BRACKET_RESULTADO.md")
    print("=" * 104)
    print("  Celda: Tradeify, N=10, stop 40 ticks (10pt), objetivo 80 ticks (20pt), sin ventaja")
    print("  Publicado: P(eval)=0,231  P(fondeada)=0,226  P(total)=0,0521  vara=1,181")
    tot, ev, fu = p_pasar("Tradeify Growth (50K)", 10, 20, 10, C1, None, NPATHS_VERIF)
    vara = p_equilibrio("Tradeify Growth (50K)") / tot
    print(f"  Recalculado: P(eval)={ev:.3f}  P(fondeada)={fu:.3f}  P(total)={tot:.4f}  "
          f"vara={vara:.3f}")
    d_ev, d_fu, d_v = abs(ev - 0.231), abs(fu - 0.226), abs(vara - 1.181)
    print(f"  Diferencias: eval {d_ev:.4f}  fondeada {d_fu:.4f}  vara {d_v:.4f}")
    print("  Tolerancia (ruido de Monte Carlo, semilla distinta): 0,010 en P, 0,060 en vara")
    v2 = d_ev <= 0.010 and d_fu <= 0.010 and d_v <= 0.060
    print(f"  -> {'COINCIDE' if v2 else 'NO COINCIDE'}")
    return v1, v2


def sensibilidad(npaths=60_000):
    """Cuanto tiene que bajar el costo para que la vara caiga por debajo de 1,0 en la
    mejor celda utilizable de Tradeify (N=10, stop 10pt, objetivo 20pt, vara 1,181)."""
    print("=" * 104)
    print("SENSIBILIDAD - de cuanto tiene que ser el costo para que la vara llegue a 1,0")
    print("=" * 104)
    firma, N, T_pt, S_pt = "Tradeify Growth (50K)", 10, 20, 10
    objetivo = p_equilibrio(firma)
    print(f"  Celda: {firma}, N={N} micros, {T_pt}pt:{S_pt}pt")
    print(f"  vara = 1,0 exige P(total, sin ventaja) = costo/cobro = {objetivo*100:.3f}%")
    # Escaneo en grilla, no biseccion: P(total) tiene ruido de Monte Carlo y escalones
    # (el tamano del paso cambia con el costo), asi que una biseccion se puede colgar de
    # un cruce espurio. La curva entera se imprime para que se vea la forma.
    import math
    T_ticks, S_ticks = T_pt * 4, S_pt * 4
    ev = FIRMAS[firma]["eval"]
    print(f"\n  {'costo $/op':>12}{'gana $':>10}{'pierde $':>10}"
          f"{'ganadas p/objetivo':>20}{'perdidas p/piso':>17}{'P(total)':>11}{'vara':>9}")
    grilla = [i * 0.125 for i in range(int(C1 / 0.125) + 1)]
    curva = []
    for c in grilla:
        win = T_ticks * TICK * N - c * N
        loss = S_ticks * TICK * N + c * N
        n_win = math.ceil(ev["target"] / win)
        n_loss = math.ceil(ev["dd"] / loss)
        p = p_pasar(firma, N, T_pt, S_pt, c, None, npaths)[0]
        v = objetivo / p if p > 0 else float("inf")
        curva.append((c, p, v))
        print(f"  {c:>12.3f}{win:>10.2f}{loss:>10.2f}{n_win:>20}{n_loss:>17}"
              f"{p*100:>10.3f}%{v:>9.3f}")

    if curva[0][2] > 1.0:
        print("\n  Ni con costo CERO la vara baja de 1,0 en esta celda.")
        return None

    # No se interpola a traves de un ESCALON. La cantidad entera de operaciones ganadoras
    # que hacen falta para llegar al objetivo cambia de golpe con el costo; un cruce de la
    # vara que coincide con ese cambio no es un umbral de costo, es un filo de
    # divisibilidad, y publicarlo como si fuera un precio alcanzable seria inventar.
    n_win_de = lambda c: math.ceil(ev["target"] / (T_ticks * TICK * N - c * N))
    c_star = None
    for (c0, _, v0), (c1_, _, v1) in zip(curva, curva[1:]):
        if v0 <= 1.0 < v1:
            if n_win_de(c0) != n_win_de(c1_):
                print(f"\n  La vara cruza 1,0 entre ${c0:.3f} y ${c1_:.3f}, pero en ese mismo")
                print(f"  tramo la cantidad de ganadas necesarias salta de {n_win_de(c0)} a "
                      f"{n_win_de(c1_)}.")
                print("  Es un ESCALON de divisibilidad, no un umbral de costo. No se interpola.")
                continue
            c_star = c0 + (c1_ - c0) * (1.0 - v0) / (v1 - v0)

    if c_star is None:
        peor_caso = min(v for _, _, v in curva[1:])
        print(f"\n  RESULTADO: ningun costo POSITIVO baja la vara de 1,0 en esta celda.")
        print(f"  Con costo tendiendo a cero por arriba la vara se estanca en {peor_caso:.3f}")
        print(f"  y no baja mas. Bajar el costo de ${C1:.2f} a $0,125 -un recorte del 95%-")
        print(f"  mueve la vara de {curva[-1][2]:.3f} a {peor_caso:.3f}: no cruza 1,0.")
        print("  El termino dominante en ESTA celda no es el costo, es cuantas operaciones")
        print("  ganadoras enteras hacen falta para cubrir el objetivo.")
        return None

    print(f"\n  COSTO UMBRAL = ${c_star:.2f} por micro por operacion (cruce interpolado)")
    print(f"  Hoy se supone ${C1:.2f}. Hay que bajar ${C1 - c_star:.2f}, "
          f"es decir un {(C1 - c_star)/C1*100:.0f}% del costo actual "
          f"(quedarse con el {c_star/C1*100:.0f}%).")
    return c_star


def main():
    ap = argparse.ArgumentParser(description="Acierto requerido por firma y bracket.")
    ap.add_argument("--firma", choices=sorted(ALIAS))
    ap.add_argument("--contratos", type=int, default=10, help="micros MES")
    ap.add_argument("--objetivo", type=float, help="puntos")
    ap.add_argument("--stop", type=float, help="puntos")
    ap.add_argument("--costo", type=float, default=C1, help="USD por micro por operacion")
    ap.add_argument("--tabla", action="store_true")
    ap.add_argument("--control", action="store_true")
    ap.add_argument("--verificar", action="store_true")
    ap.add_argument("--sensibilidad", action="store_true")
    a = ap.parse_args()

    if a.tabla:
        tabla(a.costo, "ENTREGABLE 1 - ACIERTO REQUERIDO POR OPERACION (esperanza positiva del intento)")
    elif a.control:
        paso = control()
        control_derivado()
        sys.exit(0 if paso else 1)
    elif a.verificar:
        v1, v2 = verificar()
        sys.exit(0 if (v1 and v2) else 1)
    elif a.sensibilidad:
        sensibilidad()
    elif a.firma and a.objetivo and a.stop:
        nombre = ALIAS[a.firma]
        estado, motivo = factible(nombre, a.contratos, a.objetivo, a.stop, a.costo)
        p = acierto_requerido(nombre, a.contratos, a.objetivo, a.stop, a.costo)
        print(f"{nombre}   N={a.contratos} micros   {a.objetivo:g}pt:{a.stop:g}pt "
              f"(R:R {a.objetivo/a.stop:.1f})   costo ${a.costo:.2f}/op")
        print(f"  acierto requerido : {_fmt(p).strip()}")
        print(f"  sin ventaja da    : {acierto_sin_ventaja(a.objetivo, a.stop)*100:.1f}%")
        print(f"  factible          : {estado.upper()} ({motivo})")
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
