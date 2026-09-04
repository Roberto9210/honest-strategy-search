"""
VENTANA G - EL ARRASTRE DEL DES-DRIFT: efecto o ruido?

NO GASTA CARTUCHO. K = 261. Medicion descriptiva sobre muestra ya recogida.

EL PROBLEMA, planteado por Roberto. En la corrida de des-drift el POOLED se movio ~0,5
puntos entre factor 0,00 y factor 1,00. Por mi propia conclusion de esa misma corrida -"el
drift vive casi enteramente en la separacion largo/corto y casi nada en el pooled"- ese
pooled no deberia moverse. O mi conclusion esta mal, o ese medio punto es ruido que le puse
nombre.

COMO SE DISTINGUE. Con tres puntos no se puede: por tres puntos pasa cualquier cosa. Se
agregan factores intermedios y se mira la FORMA:
  - si el pooled cae sobre una recta -> es un EFECTO real del des-drift, y mi conclusion de
    que el drift no toca el pooled era demasiado fuerte;
  - si salta sin orden alrededor de una recta -> es RUIDO, y el medio punto no significa nada.

EL DISCRIMINADOR. Las corridas comparten semilla, asi que usan LAS MISMAS entradas sobre
series que solo difieren en el ajuste: es Monte Carlo con numeros aleatorios comunes. Eso
hace que la DIFERENCIA entre factores tenga mucho menos ruido que cada nivel por separado,
y por lo tanto que la no-linealidad sea informativa. El residuo de la recta se compara
contra el error estandar de Monte Carlo de cada celda, derivado del n y no escrito a mano.
"""
import numpy as np

from desdrift import HORIZONTE, NPATHS, desdriftar
from linea_base import cargar, replica

FACTORES = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
BRACKETS = [(10, 10), (20, 10), (5, 20)]


def medir(cl, hi, lo, con, T, S):
    """Igual que desdrift.medir pero devolviendo tambien el error estandar de Monte Carlo."""
    asum = S / (S + T)
    g = res = 0
    lados = {}
    for lado in ("largo", "corto"):
        r = replica(cl, hi, lo, con, T, S, lado, HORIZONTE, npaths=NPATHS)
        ri = r["gana"] + r["pierde"] + r["amb"]
        lados[lado] = (r["gana"] / ri - asum) * 100
        g += r["gana"]; res += ri
    p = g / res
    return dict(pool=(p - asum) * 100, sep=lados["largo"] - lados["corto"],
                se=np.sqrt(p * (1 - p) / res) * 100)


def main():
    cl, hi, lo, con = cargar()
    print("=" * 100)
    print("EL ARRASTRE DEL DES-DRIFT SOBRE EL POOLED - efecto o ruido?")
    print("NO GASTA CARTUCHO. K = 261.")
    print("=" * 100)
    print(f"\n   {HORIZONTE//1380} sesiones de horizonte, {NPATHS:,} rutas por lado, "
          f"{len(FACTORES)} factores.")
    print("   Numeros aleatorios comunes: las mismas entradas en todos los factores.\n")

    print(f"   {'factor':>8}" + "".join(
        f"{f'{T}:{S} pool':>13}{f'{T}:{S} sep':>12}" for T, S in BRACKETS))
    datos = {b: [] for b in BRACKETS}
    ses = {}
    for f in FACTORES:
        c2, h2, l2 = desdriftar(cl, hi, lo, con, f)
        fila = {}
        for T, S in BRACKETS:
            d = medir(c2, h2, l2, con, T, S)
            fila[(T, S)] = d
            datos[(T, S)].append(d["pool"])
            ses[(T, S)] = d["se"]
        print(f"   {f:>8.2f}" + "".join(
            f"{fila[(T,S)]['pool']:>+13.3f}{fila[(T,S)]['sep']:>+12.2f}" for T, S in BRACKETS))
        del c2, h2, l2

    print("\n" + "=" * 100)
    print("LA FORMA - se ajusta una recta al pooled contra el factor")
    print("   QUE HARIA FALLAR LA LECTURA 'es un efecto': que el residuo de la recta sea del")
    print("   tamano del recorrido, o que el recorrido entero quepa dentro del error de")
    print("   Monte Carlo. Cualquiera de las dos cosas lo convierte en ruido con nombre.")
    print("=" * 100)
    x = np.array(FACTORES)
    print(f"\n   {'bracket':>11}{'recorrido':>12}{'pendiente':>12}{'R2':>9}"
          f"{'resid max':>12}{'error MC':>11}{'resid/err':>11}{'lectura':>12}")
    for T, S in BRACKETS:
        y = np.array(datos[(T, S)])
        rec = y[-1] - y[0]
        a, b = np.polyfit(x, y, 1)
        pred = a * x + b
        ss_res = ((y - pred) ** 2).sum()
        ss_tot = ((y - y.mean()) ** 2).sum()
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")
        rmax = np.abs(y - pred).max()
        se = ses[(T, S)]
        # el recorrido tiene que superar el ruido Y la recta tiene que explicar la forma
        if abs(rec) < 2 * se:
            lect = "RUIDO"
        elif r2 >= 0.90 and rmax < abs(rec) / 3:
            lect = "EFECTO"
        else:
            lect = "MIXTO"
        print(f"   {f'{T}pt:{S}pt':>11}{rec:>+12.3f}{a:>+12.3f}{r2:>9.3f}"
              f"{rmax:>12.3f}{se:>11.3f}{rmax/se:>11.2f}{lect:>12}")

    print("\n   'recorrido' = pooled(1,00) - pooled(0,00), en puntos porcentuales.")
    print("   'error MC' = error estandar binomial de una celda, derivado del n de esa celda.")
    print("   Con numeros aleatorios comunes el error de la DIFERENCIA es bastante menor que")
    print("   ese, asi que 'error MC' es una cota generosa: si algo no lo supera, es ruido.")
    return datos


if __name__ == "__main__":
    main()
