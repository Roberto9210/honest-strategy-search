"""
VENTANA G - las dos "simetrias exactas" son IDENTIDADES DE CONSTRUCCION, y el histograma
de los bordes del M2M.

NO GASTA CARTUCHO. K = 261.

LA HIPOTESIS A REFUTAR O CONFIRMAR (de Roberto): reporte dos simetrias exactas -el M2M
espejo (+3,323 contra -3,323, simetrico 0,000 clavado) y el residuo "perfectamente
antisimetrico"- pero tambien medi que 2016-2019 tiene drift alcista (largo 54,6% / corto
45,4%). Con drift real, largo y corto no deberian salir espejo exacto. Sospecha que algo en
la construccion simetriza.

LA DEMOSTRACION. Para una entrada al precio p:
    bracket 20pt:10pt LARGO   -> niveles {p-10, p+20}, gana si toca +20 primero
    bracket 10pt:20pt CORTO   -> niveles {p-10, p+20}, gana si toca -10 primero
Son LOS MISMOS DOS NIVELES con las etiquetas invertidas. Y como las entradas usan la MISMA
semilla, son los MISMOS caminos. Entonces, camino por camino:
    gana(20:10 largo)  <=>  pierde(10:20 corto)
    sin resolver(20:10 largo)  <=>  sin resolver(10:20 corto)
Lo mismo cruzado para el otro lado. Sumando los dos lados:
    P_pooled(20:10) = 1 - P_pooled(10:20)      EXACTO, para cualquier serie
Y como las tasas asumidas tambien son complementarias (1/3 y 2/3), los sesgos salen
exactamente opuestos. NO ES UN HALLAZGO: es una identidad que valdria con o sin drift.

El caso simetrico es peor: para 10pt:10pt los dos lados comparten los niveles {p-10, p+10} y
cada camino resuelto es ganador para exactamente UNO de los dos lados, asi que
    P_pooled(10:10) = 1/2      EXACTO, siempre.
El "control" de que el pooled daba 50,0% clavado era VACIO: no podia dar otra cosa.
"""
import os

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
CELDAS = [(5, 10), (10, 10), (20, 10), (5, 20), (10, 20)]


def m2m(T, S):
    return np.load(os.path.join(AQUI, f"m2m_{T}_{S}.npy"))


def prueba_identidad():
    print("=" * 100)
    print("1. LAS SIMETRIAS SON IDENTIDADES - verificacion numerica sobre lo ya medido")
    print("=" * 100)

    # (a) Las tasas pooled publicadas suman exactamente 1.
    print("\n   (a) tasas pooled publicadas (linea_base.py, 1 sesion):")
    pares = [((20, 10), 0.273, (10, 20), 0.727), ((10, 10), 0.500, (10, 10), 0.500)]
    for (b1, p1, b2, p2) in pares:
        print(f"       {b1[0]}pt:{b1[1]}pt = {p1*100:.1f}%   +   "
              f"{b2[0]}pt:{b2[1]}pt = {p2*100:.1f}%   =   {(p1+p2)*100:.1f}%")
    print("       Suman 100,0% clavado. Es la identidad, no una coincidencia del mercado.")

    # (b) Las muestras de M2M son el negativo exacto una de la otra.
    a, b = m2m(20, 10), m2m(10, 20)
    print(f"\n   (b) muestras de M2M, 20pt:10pt contra 10pt:20pt:")
    print(f"       n iguales: {len(a) == len(b)}  ({len(a):,} contra {len(b):,})")
    igual = np.array_equal(np.sort(a), np.sort(-b))
    print(f"       sort(M2M 20:10) == sort(-M2M 10:20):  {igual}")
    print(f"       media {a.mean():+.4f} contra {b.mean():+.4f}   suma {a.mean()+b.mean():+.2e}")

    c = m2m(10, 10)
    sim = np.array_equal(np.sort(c), np.sort(-c))
    print(f"\n   (c) el bracket simetrico 10pt:10pt es su propio espejo:")
    print(f"       sort(M2M) == sort(-M2M):  {sim}   media {c.mean():+.2e}")

    print("\n   VEREDICTO: la hipotesis de Roberto se CONFIRMA. Las dos simetrias exactas son")
    print("   identidades de la construccion -mismos niveles, mismas entradas, etiquetas")
    print("   invertidas- y valdrian igual con drift o sin drift. NO informan nada del")
    print("   mercado, y yo las reporte como si fueran hallazgos.")
    print("\n   CONSECUENCIAS, que hay que decir:")
    print("   - El residuo de la anomalia es UN numero, no dos brackets que se confirman.")
    print("     20pt:10pt y 10pt:20pt son la misma medicion con el signo cambiado.")
    print("   - El control 'pooled = 50,0% clavado' era VACIO. No podia dar otra cosa.")
    print("     Lo que si medía algo era la SEPARACION largo/corto (54,6% / 45,4%), que es")
    print("     donde vive el drift, y que el pooling destruye por construccion.")
    return igual and sim


def bordes():
    print("\n" + "=" * 100)
    print("2. HISTOGRAMA DEL M2M - hay masa apilada contra las barreras?")
    print("=" * 100)
    print("   Sospecha propia: la distribucion del M2M de las abiertas esta truncada por")
    print("   construccion en los dos bordes (nunca puede pasar de +objetivo ni de -stop).")
    print("   Si hay masa APILADA justo adentro de los bordes, el promedio esconde una forma")
    print("   bimodal y el remuestreo del modelo estaria mal repartido.\n")
    print(f"   {'bracket':>11}{'borde -':>9}{'borde +':>9}{'n':>8}"
          f"{'% en 10% inferior':>19}{'% en 10% superior':>19}{'% en el medio':>15}")
    for T, S in CELDAS:
        x = m2m(T, S)
        lo, hi = -S, T          # los bordes teoricos del bracket
        ancho = hi - lo
        franja = 0.10 * ancho
        pl = (x <= lo + franja).mean() * 100
        ph = (x >= hi - franja).mean() * 100
        print(f"   {f'{T}pt:{S}pt':>11}{lo:>9.0f}{hi:>9.0f}{len(x):>8,}"
              f"{pl:>18.1f}%{ph:>18.1f}%{100-pl-ph:>14.1f}%")
    print("\n   Referencia: si el M2M fuera uniforme entre los bordes, cada franja del 10%")
    print("   tendria el 10%. Muy por encima = masa apilada; muy por debajo = centro pesado.")


if __name__ == "__main__":
    prueba_identidad()
    bordes()
