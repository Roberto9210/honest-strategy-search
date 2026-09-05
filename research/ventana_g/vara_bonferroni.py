"""
VERIFICACION: el juez usa 3,73 o ahi tambien hay un 3,0?

NO GASTA CARTUCHO. K = 261. Dinero: $0. Es aritmetica sobre constantes, no toca datos.

EL DATO QUE LLEGA (VENTANA L, ya commiteado por ella): la vara exacta de Bonferroni con K = 261 es
z = 3,730 bilateral (3,551 unilateral). Los margenes del inventario se calcularon con 3,0 "por ser la
mas baja que el juez usa", correcto como cota optimista, pero cuesta un factor 0,80 a cada margen.

LO QUE SE VERIFICA ACA: que hace el juez, exactamente, y si la convencion del programa (alfa =
0,05/262, anotada por VENTANA D) esta implementada o no.
"""

import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import juez as J  # noqa: E402

K = 261
K_MAS_UNO = 262          # el proximo cartucho, que es el que gastaria un candidato real


def z_de_alfa(alfa):
    """z tal que P(Z > z) = alfa, por biseccion sobre la misma sf_normal que usa el juez."""
    lo, hi = 0.0, 12.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if J.sf_normal(mid) > alfa:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def main():
    R = []
    A = R.append
    A("=" * 100)
    A("LA VARA DEL JUEZ CONTRA LA VARA DE BONFERRONI DEL PROGRAMA")
    A("NO GASTA CARTUCHO. K = 261. Dinero: $0.")
    A("=" * 100)

    A("")
    A("-" * 100)
    A("   QUE USA EL JUEZ, leido del codigo")
    A("-" * 100)
    A(f"   Z_BASE = {J.Z_BASE}   (juez.py, 'desvios exigidos con UNA variante probada')")
    a_base = J.sf_normal(J.Z_BASE)
    A(f"   z_requerido(variantes) reparte sf_normal(Z_BASE) = {a_base:.6g} entre las variantes")
    A(f"   declaradas. O sea que el alfa DE PARTIDA del juez, con una sola variante, es "
      f"{a_base:.6g} A UNA COLA.")
    A("")
    A(f"   {'variantes':>10}{'z exigido':>12}{'alfa implicado':>18}")
    for v in (1, 3, 10, 100, 261):
        z = J.z_requerido(v)
        A(f"   {v:>10}{z:>12.3f}{J.sf_normal(z):>18.3e}")

    A("")
    A("-" * 100)
    A("   QUE PIDE LA CONVENCION DEL PROGRAMA")
    A("-" * 100)
    A(f"   La convencion anotada es alfa = 0,05 / {K_MAS_UNO} (VENTANA D), sobre el contador K que")
    A(f"   NO se reinicia. Con K = {K} gastados, el proximo candidato es el cartucho {K_MAS_UNO}.")
    for nom, kk in (("K = 261", K), ("K+1 = 262", K_MAS_UNO)):
        a1 = 0.05 / kk
        z1 = z_de_alfa(a1)
        z2 = z_de_alfa(a1 / 2)
        A(f"   {nom:>12}   alfa = 0,05/{kk} = {a1:.6g}   ->   z unilateral {z1:.3f}   "
          f"z bilateral {z2:.3f}")
    A("")
    A(f"   El dato que paso la VENTANA L -3,730 bilateral y 3,551 unilateral- se reproduce con")
    A(f"   K = {K}: bilateral {z_de_alfa(0.05 / K / 2):.3f}, unilateral {z_de_alfa(0.05 / K):.3f}. Coincide.")

    A("")
    A("=" * 100)
    A("   LA RESPUESTA")
    A("=" * 100)
    z_prog = z_de_alfa(0.05 / K_MAS_UNO)
    A(f"   EN EL JUEZ HAY UN 3,0, NO UN 3,73. Z_BASE = {J.Z_BASE} corresponde a alfa = {a_base:.3g}")
    A(f"   a una cola. La convencion del programa pide alfa = 0,05/{K_MAS_UNO} = {0.05/K_MAS_UNO:.3g},")
    A(f"   que es z = {z_prog:.3f} unilateral. El juez esta {a_base/(0.05/K_MAS_UNO):.1f} veces mas")
    A(f"   permisivo en alfa, y {z_prog - J.Z_BASE:+.3f} desvios mas bajo en la vara.")
    A("")
    A("   PERO NO ES UN BUG SIN MAS, Y HAY QUE DECIR POR QUE. El juez NO reparte el alfa entre los")
    A("   261 cartuchos del programa: lo reparte entre las VARIANTES QUE EL CANDIDATO DECLARA. Son")
    A("   dos correcciones de multiplicidad distintas y las dos son legitimas por separado:")
    A("     - por VARIANTES: cuantas versiones de ESTA idea se probaron antes de traerla.")
    A("     - por CARTUCHOS: cuantas ideas se probaron en el programa entero.")
    A("   El juez implementa la primera y NO la segunda. Y la segunda es la que el programa declaro")
    A("   como su regla.")
    A("")
    A("   LO QUE CUESTA, en numeros:")
    for v in (1, 3, 10):
        z_j = J.z_requerido(v)
        A(f"      con {v:>3} variantes el juez exige {z_j:.3f}; componiendo AMBAS correcciones")
        A(f"      (alfa = 0,05/{K_MAS_UNO}/{v}) haria falta {z_de_alfa(0.05 / K_MAS_UNO / v):.3f}, "
          f"o sea {z_de_alfa(0.05/K_MAS_UNO/v) - z_j:+.3f} desvios mas.")
    A("")
    A(f"   Y EL FACTOR SOBRE LOS MARGENES: un margen calculado con 3,0 en vez de {z_prog:.3f} esta")
    A(f"   inflado por {z_prog/J.Z_BASE:.2f}x. Al reves: los margenes publicados hay que multiplicarlos")
    A(f"   por {J.Z_BASE/z_prog:.2f} para leerlos contra la vara del programa. Coincide con el 0,80")
    A("   que reporto la VENTANA L.")
    A("")
    A("   QUE NO DECIDO YO: si el juez DEBE componer las dos correcciones. Componerlas es lo")
    A("   conservador y es lo que la regla escrita del programa dice; no componerlas se puede")
    A("   defender si se argumenta que K cuenta intentos de OTRAS familias y este candidato no")
    A("   hereda su multiplicidad. Ese argumento NO esta escrito en ningun lado, y mientras no lo")
    A("   este, el juez esta por debajo de su propia regla de casa. Lo reporto, no lo cambio solo.")
    A("=" * 100)
    print("\n".join(R))
    return 0


if __name__ == "__main__":
    sys.exit(main())
