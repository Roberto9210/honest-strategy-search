"""
VENTANA G - la corrida DES-DRIFTADA, con el des-drift CALIBRADO.

NO GASTA CARTUCHO. K = 261. Medicion descriptiva sobre muestra ya recogida.

Primer intento: restar a cada contrato su tendencia lineal completa. SOBRE-CORRIGIO — la
separacion largo/corto no se cerro, se dio vuelta (+5,78 -> -6,17 en el bracket simetrico).
Restar la tendencia de cada contrato no es lo mismo que restar el drift del mercado, porque
cada contrato tiene su propia convergencia.

Solucion: des-driftar con un FACTOR y calibrarlo contra un observable. El observable natural
es la separacion largo/corto del bracket SIMETRICO 10pt:10pt, que por identidad de
construccion tiene pooled = 0 exacto y por lo tanto su separacion es drift puro.

Despues, en el factor calibrado, se mide el sesgo POOLED de los brackets asimetricos. Eso es
lo que contesta si el residuo era drift.
"""
import numpy as np
import pandas as pd

from linea_base import cargar, replica

SESION = 1380
HORIZONTE = 5 * SESION
NPATHS = 30_000
FACTORES = [0.0, 0.5, 1.0]
BRACKETS = [(10, 10), (20, 10), (5, 20)]


def desdriftar(cl, hi, lo, con, factor):
    if factor == 0.0:
        return cl, hi, lo
    cl2, hi2, lo2 = cl.copy(), hi.copy(), lo.copy()
    for c in pd.unique(con):
        k = np.flatnonzero(con == c)
        if len(k) < 2:
            continue
        mu = (cl[k[-1]] - cl[k[0]]) / (len(k) - 1)
        aj = factor * mu * np.arange(len(k))
        cl2[k] -= aj; hi2[k] -= aj; lo2[k] -= aj
    return cl2, hi2, lo2


def medir(cl, hi, lo, con, T, S):
    asum = S / (S + T)
    g = res = 0
    lados = {}
    for lado in ("largo", "corto"):
        r = replica(cl, hi, lo, con, T, S, lado, HORIZONTE, npaths=NPATHS)
        ri = r["gana"] + r["pierde"] + r["amb"]
        lados[lado] = (r["gana"] / ri - asum) * 100
        g += r["gana"]; res += ri
        sin_res = r["vivo"] / r["n"] * 100
    return dict(largo=lados["largo"], corto=lados["corto"],
                pool=(g / res - asum) * 100, sep=lados["largo"] - lados["corto"],
                sin_res=sin_res)


def main():
    cl, hi, lo, con = cargar()
    print("=" * 100)
    print("DES-DRIFT CALIBRADO - sobrevive el residuo?")
    print("NO GASTA CARTUCHO. K = 261.")
    print("=" * 100)
    print(f"\n   5 sesiones de horizonte, {NPATHS:,} rutas por lado.")
    print("   El factor se calibra contra la separacion largo/corto de 10pt:10pt, que por")
    print("   identidad tiene pooled = 0 y por lo tanto su separacion es drift puro.\n")

    res = {}
    print(f"   {'factor':>8}" + "".join(
        f"{f'{T}:{S} sep':>12}{f'{T}:{S} pool':>13}" for T, S in BRACKETS))
    for f in FACTORES:
        c2, h2, l2 = desdriftar(cl, hi, lo, con, f)
        fila = {}
        for T, S in BRACKETS:
            fila[(T, S)] = medir(c2, h2, l2, con, T, S)
        res[f] = fila
        print(f"   {f:>8.2f}" + "".join(
            f"{fila[(T,S)]['sep']:>+12.2f}{fila[(T,S)]['pool']:>+13.2f}"
            for T, S in BRACKETS))
        del c2, h2, l2

    # factor que anula la separacion del simetrico, por interpolacion lineal
    xs = FACTORES
    ys = [res[f][(10, 10)]["sep"] for f in FACTORES]
    f_cal = None
    for i in range(len(xs) - 1):
        if ys[i] * ys[i + 1] < 0:
            f_cal = xs[i] + (xs[i + 1] - xs[i]) * (0 - ys[i]) / (ys[i + 1] - ys[i])
    print(f"\n   Separacion de 10pt:10pt por factor: " +
          ", ".join(f"{f:.2f}->{y:+.2f}" for f, y in zip(xs, ys)))
    if f_cal is None:
        print("   No cruza cero en la grilla; no se puede calibrar.")
        return res
    print(f"   FACTOR CALIBRADO (separacion = 0): {f_cal:.3f}")

    c2, h2, l2 = desdriftar(cl, hi, lo, con, f_cal)
    print(f"\n   En el factor calibrado:")
    print(f"   {'bracket':>11}{'sep':>9}{'pooled':>9}{'sin res':>9}"
          f"{'censura predice':>18}{'RESIDUO':>10}")
    for T, S in BRACKETS:
        d = medir(c2, h2, l2, con, T, S)
        asim = (T - S) / (T + S)
        pred = -0.5 * asim * d["sin_res"]
        print(f"   {f'{T}pt:{S}pt':>11}{d['sep']:>+9.2f}{d['pool']:>+9.2f}"
              f"{d['sin_res']:>8.1f}%{pred:>+18.2f}{d['pool']-pred:>+10.2f}")
    print("\n   RESIDUO = pooled - lo que la censura explica, ya sin drift.")
    return res


if __name__ == "__main__":
    main()
