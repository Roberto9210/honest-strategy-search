"""
VENTANA G - apretar el positivo de +$10 hasta que se rompa o aguante.

NO GASTA CARTUCHO. K = 261.

Dos celdas cruzaron el equilibrio con el tercer estado. Antes de que ese numero exista en
ningun documento como algo mas que una curiosidad, se lo somete a tres presiones y se
audita de donde salen sus dos insumos.
"""
import numpy as np

from aritmetica import C1_POR_MICRO_VIA_MINI, FIRMAS
from tercer_estado import cadena, m2m, P_ABIERTA, P_RESUELTA, FIRMA, N

T, S = 5, 20
C1 = C1_POR_MICRO_VIA_MINI
PUNTO_MINI = 50.0            # USD por punto, 1 E-mini = 10 micro-equivalentes
COBRO = 1500.0 * 0.90        # primer retiro maximo x split, los dos MEDIDOS
PRECIO_CUPON = 83.0
PRECIO_LISTA = 165.0


def P(c1=C1, p_win=None):
    return cadena(T, S, p_abierta=P_ABIERTA[(T, S)], muestra=m2m(T, S),
                  p_win=P_RESUELTA[(T, S)] if p_win is None else p_win,
                  npaths=60_000, c1=c1)[0]


def cruce(f, lo, hi, objetivo, tol=1e-4):
    """Bisecta f (decreciente) hasta el valor donde cruza objetivo."""
    for _ in range(18):
        mid = (lo + hi) / 2
        if f(mid) >= objetivo:
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    return (lo + hi) / 2


def main():
    base = P()
    eq_cupon = PRECIO_CUPON / COBRO
    print("=" * 100)
    print("APRETAR EL POSITIVO - celda 5pt:20pt via 1 mini, tercer estado adentro")
    print("=" * 100)
    print(f"   P(pasar) sin ventaja = {base*100:.3f}%")
    print(f"   Equilibrio con cuota ${PRECIO_CUPON:.0f}: {eq_cupon*100:.3f}%")
    print(f"   E = {base*100:.3f}% x ${COBRO:,.0f} - ${PRECIO_CUPON:.0f} = "
          f"${base*COBRO - PRECIO_CUPON:+.2f}")

    print("\n" + "-" * 100)
    print("(a) CUANTO DESLIZAMIENTO DE ENTRADA lo anula")
    print("-" * 100)
    print("   La entrada se paga en las TRES ramas (ganada, perdida y abierta al corte),")
    print("   asi que entra como costo por operacion: e puntos = 5e USD por micro-equiv.\n")
    print(f"   {'entrada':>12}{'c1 $/micro':>13}{'P(pasar)':>11}{'E $':>10}")
    for ticks in (0, 0.25, 0.5, 0.75, 1.0):
        e = ticks * 0.25
        p = P(c1=C1 + 5.0 * e)
        print(f"   {ticks:>7.2f} tk{C1 + 5.0*e:>13.3f}{p*100:>10.3f}%"
              f"{p*COBRO - PRECIO_CUPON:>+10.2f}")
    e_star = cruce(lambda e: P(c1=C1 + 5.0 * e), 0.0, 0.30, eq_cupon)
    print(f"\n   ANULA EN: {e_star:.4f} puntos = {e_star/0.25:.2f} ticks = "
          f"${e_star*PUNTO_MINI:.2f} por operacion por mini.")
    ticks_star = e_star / 0.25
    print(f"   Contra lo que dije la vez pasada -'un tick al filo, dos lo matan'-:")
    print(f"   el numero exacto es {ticks_star:.2f} ticks.")

    print("\n" + "-" * 100)
    print("(b) CUANTA CAIDA DE LA TASA DE ACIERTO lo anula")
    print("-" * 100)
    p0 = P_RESUELTA[(T, S)]
    print(f"   Tasa medida entre resueltas: {p0*100:.1f}%. Si el drift residual la inflo,")
    print(f"   cuanto habria que bajarla para volver al equilibrio?\n")
    print(f"   {'tasa':>10}{'P(pasar)':>11}{'E $':>10}")
    for d in (0.0, 0.005, 0.010, 0.015):
        p = P(p_win=p0 - d)
        print(f"   {(p0-d)*100:>9.1f}%{p*100:>10.3f}%{p*COBRO - PRECIO_CUPON:>+10.2f}")
    d_star = cruce(lambda d: P(p_win=p0 - d), 0.0, 0.03, eq_cupon)
    # cruce() bisecta suponiendo f decreciente en su argumento; aca d sube -> P baja, ok
    print(f"\n   ANULA EN: una caida de {d_star*100:.2f} puntos de tasa de acierto,")
    print(f"   de {p0*100:.1f}% a {(p0-d_star)*100:.2f}%.")
    print(f"   Para dimensionar: el residuo sin explicar, ya des-driftado, es 0,78 puntos")
    print(f"   en esta celda. Es {0.78/(d_star*100):.1f} veces lo que hace falta para anularlo.")

    print("\n" + "-" * 100)
    print("(c) DE DONDE SALEN LOS DOS INSUMOS")
    print("-" * 100)
    print(f"   COBRO ${COBRO:,.0f} = $1.500 x 90%. Los DOS MEDIDOS de fuente oficial:")
    print("     'Primer retiro maximo: $1.500 (50K)' y 'Traders receive 90% of the payout")
    print("     amount requested', help.tradeify.co, leidos 2026-09-03. Solido.")
    print(f"\n   CUOTA ${PRECIO_CUPON:.0f}: es el PRECIO PROMOCIONAL con codigo SEP.")
    print(f"   El precio de LISTA es ${PRECIO_LISTA:.0f} (datos_crudos.md, mismo widget oficial).")
    print(f"   Los dos estan medidos, pero NO son la misma clase de numero: el cupon caduca.\n")
    print(f"   {'cuota':>10}{'equilibrio':>12}{'E $':>10}{'signo':>10}")
    for pr in (PRECIO_CUPON, PRECIO_LISTA):
        e = base * COBRO - pr
        print(f"   {pr:>9.0f}{pr/COBRO*100:>11.3f}%{e:>+10.2f}{('POSITIVO' if e>0 else 'negativo'):>10}")
    print(f"\n   EL POSITIVO EXISTE SOLO AL PRECIO DE CUPON. A precio de lista es "
          f"${base*COBRO - PRECIO_LISTA:+.0f}.")


if __name__ == "__main__":
    main()
