"""
VENTANA G - el criterio recalculado con la MEDIA medida, y que significa exactamente el 34,1%.

NO GASTA CARTUCHO. K = 261. Aritmetica sobre parametros fijados mas un descriptivo ya
calculado (media_exceso.py).

    LA MEDIA GOBIERNA LA ESPERANZA.       -> seccion 1 y 2
    LA COLA GOBIERNA TOCAR EL LIMITE.     -> seccion 3
Son dos preguntas. Hasta ayer estaban mezcladas en un solo filtro que usaba el p95 para
las dos cosas, y el p95 es la respuesta correcta a la segunda y la equivocada a la primera.
"""
import numpy as np

from bracket import C1, TICK
from vara_criterio import (FIRMAS, acierto_requerido, acierto_sin_ventaja, p_equilibrio,
                            p_pasar)

# Medido por media_exceso.py sobre ES 1-min Databento 2016-2019, P-escalera 971 (control
# de poblacion reproducido exacto). Ventana T23, lado largo, exceso dentro de la barra que
# toca, en PUNTOS. La columna media/p95 sale ~0,26-0,29 en toda la tabla.
EXCESO = {   # D_pt: (media, p50, p95, p99, maximo, n)
    4:  (0.596, 0.25, 2.10, 5.43, 31.25, 733),
    10: (0.722, 0.25, 2.50, 7.02, 25.25, 449),
    20: (0.982, 0.50, 3.82, 9.47, 15.50, 208),
}
# El costo del modelo (C1 = $2,50/micro) ya incluye 1 tick = 0,25pt de deslizamiento.
YA_MODELADO_PT = 0.25
PUNTO = 5.0   # USD por punto por micro (MES)

FIRMA = "Tradeify Growth (50K)"
N = 10
CELDAS = [(5, 10), (10, 10), (20, 10), (5, 20), (10, 20)]


def exceso_extra(S_pt):
    """Lo que el modelo NO capturaba: de la mediana ya contada hasta la media medida."""
    return EXCESO[S_pt][0] - YA_MODELADO_PT


def equilibrio_operacion(T_pt, S_pt, c1=C1, extra_pt=0.0):
    """Punto de equilibrio POR OPERACION, en la misma contabilidad que usa el modelo:
    el costo se cobra en las dos ramas, el exceso de deslizamiento solo en la perdedora."""
    win = T_pt * PUNTO * N - c1 * N
    loss = S_pt * PUNTO * N + c1 * N + extra_pt * PUNTO * N
    return loss / (win + loss)


def seccion1():
    print("=" * 104)
    print("1. LA MEDIA MEDIDA, Y QUE TAN LEJOS ESTABA EL SUPUESTO")
    print("=" * 104)
    print(f"   el modelo asumia {YA_MODELADO_PT}pt (1 tick) de deslizamiento por operacion\n")
    print(f"   {'stop':>7}{'n':>7}{'MEDIA':>9}{'p50':>7}{'p95':>7}{'media/p95':>11}"
          f"{'no modelado':>13}")
    for S in sorted(EXCESO):
        m, p50, p95, _, _, n = EXCESO[S]
        print(f"   {S:>5.0f}pt{n:>7}{m:>9.3f}{p50:>7.2f}{p95:>7.2f}{m/p95:>11.2f}"
              f"{exceso_extra(S):>+13.3f}pt")
    print("\n   La media es el 26-29% del p95 en toda la tabla. Usar el p95 para juzgar la")
    print("   ESPERANZA sobreestimaba el dano por un factor de 3 a 4.")


def seccion2():
    print("\n" + "=" * 104)
    print("2. EL CRITERIO RECALCULADO CON LA MEDIA (la pregunta de la esperanza)")
    print("=" * 104)
    print(f"   {FIRMA}, N={N} micros. 'requerido' = acierto para esperanza POSITIVA del intento.\n")
    print(f"   {'bracket':>12}{'moneda':>9}{'req (modelo)':>14}{'req (media med.)':>18}"
          f"{'ventaja pedida':>16}{'margen':>10}")
    filas = []
    for T, S in CELDAS:
        moneda = 100 * acierto_sin_ventaja(T, S)
        req_mod = 100 * acierto_requerido(FIRMA, N, T, S, C1)
        req_med = 100 * acierto_requerido(FIRMA, N, T, S, C1, extra_pt=exceso_extra(S))
        ventaja = req_med - moneda
        # margen = cuanto sobra entre lo que el criterio pide y lo que ya se sabe que
        # el deslizamiento medio se come; si es negativo, el numero no se sostiene
        margen = (req_mod - moneda) - (req_med - req_mod)
        filas.append((T, S, moneda, req_mod, req_med, ventaja, margen))
        print(f"   {f'{T}pt:{S}pt':>12}{moneda:>8.1f}%{req_mod:>13.1f}%{req_med:>17.1f}%"
              f"{ventaja:>+15.1f}{margen:>+10.1f}")
    print("\n   'ventaja pedida' = cuanto por encima de la moneda hay que acertar, ya con la")
    print("   media medida adentro. 'margen' = lo que sobra despues de descontar el error de")
    print("   deslizamiento que el modelo tenia. Negativo = el numero no se sostiene.")
    return filas


def seccion3():
    print("\n" + "=" * 104)
    print("3. LA COLA (la otra pregunta: puede UNA operacion tocar el limite de perdida)")
    print("=" * 104)
    dd = FIRMAS[FIRMA]["eval"]["dd"]
    print(f"   drawdown de la evaluacion = ${dd:,}. Perdida de UNA operacion con N={N} micros:\n")
    print(f"   {'stop':>7}{'nominal':>11}{'con p95':>11}{'con p99':>11}{'con max':>11}"
          f"{'max / dd':>11}")
    for S in sorted(EXCESO):
        _, _, p95, p99, mx, _ = EXCESO[S]
        base = S * PUNTO * N
        f = lambda e: (S + e) * PUNTO * N
        print(f"   {S:>5.0f}pt{base:>11,.0f}{f(p95):>11,.0f}{f(p99):>11,.0f}{f(mx):>11,.0f}"
              f"{f(mx)/dd:>10.0%}")
    print("\n   El peor llenado observado en 2016-2019 se come el 88-89% del drawdown ENTERO")
    print("   en una sola operacion. No lo rompe por si solo, pero el drawdown es TRAILING:")
    print("   despues de cualquier ganancia el piso sube y ese margen ya no existe.")
    print("   Esta es la pregunta de supervivencia, y NO se responde con la media.")


def seccion4():
    print("\n" + "=" * 104)
    print("4. QUE SIGNIFICA EL 34,1% - y su reconciliacion con la vara de 1,181x")
    print("=" * 104)
    T, S = 20, 10
    moneda = 100 * acierto_sin_ventaja(T, S)
    equil = 100 * equilibrio_operacion(T, S)
    req = 100 * acierto_requerido(FIRMA, N, T, S, C1)
    print(f"   bracket {T}pt:{S}pt, N={N} micros, costo ${C1:.2f}/micro\n")
    print(f"   (i)  equilibrio POR OPERACION despues de costos : {equil:.1f}%")
    print(f"   (ii) umbral para esperanza positiva de PASAR    : {req:.1f}%   <- ESTE es el 34,1%")
    print(f"        moneda sin ventaja                          : {moneda:.1f}%")
    print(f"\n   El 34,1% es (ii), NO (i). Y notar que (ii) < (i): {req:.1f}% < {equil:.1f}%.")
    win = T * PUNTO * N - C1 * N
    loss = S * PUNTO * N + C1 * N
    ev = (req / 100) * win - (1 - req / 100) * loss
    print(f"   A {req:.1f}% de acierto la operacion PIERDE ${-ev:.0f} por vez "
          f"(gana ${win:.0f} / pierde ${loss:.0f}).")
    print("   El intento igual conviene porque es una entrada barata a un premio grande:")
    print(f"   cuota ${FIRMAS[FIRMA]['precio'] + FIRMAS[FIRMA]['activacion']:.0f} contra un "
          f"pago de ${FIRMAS[FIRMA]['pago'] * FIRMAS[FIRMA]['split']:,.0f}.")
    print("   NO es 'el nivel para ser rentable operando'. Es 'el nivel para que el billete valga'.")

    print("\n   RECONCILIACION CON LA VARA (las dos en las mismas unidades):")
    obj = p_equilibrio(FIRMA)
    p0 = acierto_sin_ventaja(T, S)
    P0 = p_pasar(FIRMA, N, T, S, C1, p0)[0]
    P1 = p_pasar(FIRMA, N, T, S, C1, req / 100)[0]
    print(f"     acierto por operacion : {p0*100:.1f}%  ->  {req:.1f}%   cociente "
          f"{(req/100)/p0:.3f}")
    print(f"     P(pasar la cadena)    : {P0*100:.3f}%  ->  {P1*100:.3f}%   cociente "
          f"{P1/P0:.3f}")
    print(f"     vara publicada = equilibrio / P(sin ventaja) = {obj*100:.3f}% / "
          f"{P0*100:.3f}% = {obj/P0:.3f}")
    elast = ((P1 / P0) - 1) / ((req / 100) / p0 - 1)
    print(f"\n   No cierran porque NO estan en las mismas unidades: 1,024 es un cociente de")
    print(f"   TASAS DE ACIERTO POR OPERACION y 1,181 es un cociente de PROBABILIDADES DE")
    print(f"   PASAR LA CADENA. La conversion entre las dos es la elasticidad de la barrera:")
    print(f"   un +1% relativo de acierto por operacion produce un +{elast:.1f}% relativo de")
    print(f"   probabilidad de pasar. Con esa elasticidad, {(req/100)/p0:.3f} en acierto se")
    print(f"   convierte en {P1/P0:.3f} en pasar, que es la vara. Cierra.")


def seccion5():
    """Medido el deslizamiento, el unico termino del costo que sigue SIN MEDIR es la
    comision. Si su incertidumbre mueve el requerido tanto como el margen que quedo, no hay
    criterio; si lo mueve menos, si lo hay."""
    print("\n" + "=" * 104)
    print("5. LO QUE QUEDA SIN MEDIR: LA COMISION. Cuanto mueve el requerido?")
    print("=" * 104)
    print("   c1 del modelo = comision + 0,25pt de deslizamiento ($1,25). La comision NUNCA")
    print("   se leyo de fuente oficial: es la deuda declarada en aritmetica.py.\n")
    T, S = 5, 10
    moneda = 100 * acierto_sin_ventaja(T, S)
    extra = exceso_extra(S)
    print(f"   celda {T}pt:{S}pt (la de mayor margen), con la media medida adentro")
    print(f"   {'comision $/micro':>18}{'c1':>8}{'requerido':>12}{'sobre la moneda':>18}")
    reqs = []
    for com in (0.00, 1.25, 2.50, 3.75):
        c1 = com + 1.25
        r = 100 * acierto_requerido(FIRMA, N, T, S, c1, extra_pt=extra)
        reqs.append(r)
        marca = "  <- supuesto del modelo" if abs(com - 1.25) < 1e-9 else ""
        print(f"   {com:>18.2f}{c1:>8.2f}{r:>11.1f}%{r - moneda:>+17.1f}{marca}")
    spread = max(reqs) - min(reqs)
    print(f"\n   El requerido se mueve {spread:.1f} puntos entre comision 0 y $3,75/micro.")
    return spread


if __name__ == "__main__":
    seccion1()
    filas = seccion2()
    seccion3()
    seccion4()
    spread = seccion5()

    print("\n" + "=" * 104)
    print("VEREDICTO")
    print("=" * 104)
    mejor = max(filas, key=lambda f: f[6])
    T, S, moneda, req_mod, req_med, ventaja, margen = mejor
    print(f"   Mejor celda por margen: {T}pt:{S}pt -> requerido {req_med:.1f}% "
          f"(moneda {moneda:.1f}%), margen {margen:+.1f} puntos.")
    print(f"   Incertidumbre por la comision no medida: {spread:.1f} puntos.")
    if spread <= abs(margen):
        print("   El margen sobrevive a la incertidumbre restante: HAY criterio.")
    else:
        print("   La incertidumbre de la comision es MAS GRANDE que el margen entero.")
        print("   SIGUE SIN HABER criterio publicable. Lo que lo cierra es UN numero:")
        print("   la comision real por micro, leida de una fuente oficial.")
