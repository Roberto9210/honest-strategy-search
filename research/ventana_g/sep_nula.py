"""
VENTANA G - EL DESVIO DE LA NULA PARA LA SEPARACION LARGO/CORTO, POR HORIZONTE.

NO GASTA CARTUCHO. K = 261. Medicion del error de un instrumento.

PARA QUE. La correccion del 5x -mi idea (c3): toda barra de error que involucre una
diferencia largo/corto esta ~5 veces chica- hay que aplicarla al inventario, y para eso hace
falta el desvio de la nula A CADA HORIZONTE. El ensamble anterior solo lo midio a 5 sesiones
(2,08 - 2,35 - 1,35). Las bandas por lado de salida_linea_base.txt estan a UNA sesion, donde
las rutas se pisan menos y el desvio tiene que ser MENOR. Usar el de 5 sesiones ahi seria una
cota, no una medicion, y una cota exagera el error y borra cosas que quizas si estan.

Se mide, entonces, en vez de acotar.

CONTROL, con su condicion de falla. La separacion del bracket SIMETRICO no es una identidad
-la identidad es sobre el POOLED- asi que su desvio tiene que ser distinto de cero y del
mismo orden que el de los asimetricos.
   QUE LO HARIA FALLAR: un desvio cero en 10pt:10pt. Significaria que estoy midiendo la
   identidad otra vez y no la separacion.
"""
import numpy as np

from linea_base import cargar, replica
from sintetico import armar, bootstrap, tripletes

K = 20
NPATHS = 30_000
SESION = 1380
HORIZONTES = [("1 sesion", SESION), ("5 sesiones", 5 * SESION)]
BRACKETS = [(5, 10), (10, 10), (20, 10), (5, 20), (10, 20)]
SEMILLA = 20260904

# Separaciones MEDIDAS sobre ES real a UNA sesion (salida_linea_base.txt, columna "contra").
REAL_SEP_1S = {(5, 10): 70.1 - 66.4, (10, 10): 52.6 - 47.4, (20, 10): 28.6 - 26.0,
               (5, 20): 85.8 - 84.6, (10, 20): 74.0 - 71.4}


def sep(cl, hi, lo, con, T, S, horizonte):
    asum = S / (S + T)
    lad, se2 = {}, 0.0
    for lado in ("largo", "corto"):
        r = replica(cl, hi, lo, con, T, S, lado, horizonte, npaths=NPATHS)
        ri = r["gana"] + r["pierde"] + r["amb"]
        p = r["gana"] / ri
        lad[lado] = (p - asum) * 100
        se2 += p * (1 - p) / ri * 1e4
    return lad["largo"] - lad["corto"], np.sqrt(se2)


def main():
    print("=" * 100)
    print("DESVIO DE LA NULA PARA LA SEPARACION LARGO/CORTO, POR HORIZONTE")
    print("NO GASTA CARTUCHO. K = 261.")
    print("=" * 100)

    cl, hi, lo, con = cargar()
    n = len(cl)
    d, up, dn = tripletes(cl, hi, lo, con)
    mu = d.mean()
    dc, upc, dnc = d - mu, up - mu, dn - mu
    del cl, hi, lo, con
    con_s = np.zeros(n, dtype=np.int8)
    print(f"\n   Nula IID (remuestreo de barras reales, media cero), {K} series de "
          f"{n:,} barras,\n   {NPATHS:,} rutas por lado. Sin drift por construccion: la "
          f"separacion verdadera es CERO.\n")

    acum, binom = {}, {}
    for k in range(K):
        rng = np.random.default_rng(SEMILLA + 7919 * k)
        c2, h2, l2 = armar(*bootstrap(dc, upc, dnc, n, rng))
        for hn, h in HORIZONTES:
            for b in BRACKETS:
                s, sb = sep(c2, h2, l2, con_s, b[0], b[1], h)
                acum.setdefault((hn, b), []).append(s)
                binom[(hn, b)] = sb
        del c2, h2, l2

    ok = True
    for hn, _ in HORIZONTES:
        print("=" * 100)
        print(f"HORIZONTE {hn.upper()}")
        print("=" * 100)
        print(f"   {'bracket':>11}{'nula media':>12}{'nula desvio':>13}{'binomial':>11}"
              f"{'subestima':>11}{'sep REAL':>10}{'en desvios':>12}{'lectura':>22}")
        for b in BRACKETS:
            v = np.array(acum[(hn, b)])
            sd, sb = v.std(ddof=1), binom[(hn, b)]
            if sd < 1e-9:
                ok = False
            if hn == "1 sesion":
                real = REAL_SEP_1S[b]
                z = (real - v.mean()) / sd
                lect = "se distingue" if abs(z) >= 3 else (
                    "al borde" if abs(z) >= 2 else "NO se distingue de 0")
                print(f"   {f'{b[0]}pt:{b[1]}pt':>11}{v.mean():>+12.3f}{sd:>13.3f}{sb:>11.3f}"
                      f"{sd/sb:>10.1f}x{real:>+10.2f}{z:>+12.1f}{lect:>22}")
            else:
                print(f"   {f'{b[0]}pt:{b[1]}pt':>11}{v.mean():>+12.3f}{sd:>13.3f}{sb:>11.3f}"
                      f"{sd/sb:>10.1f}x{'-':>10}{'-':>12}{'-':>22}")
        print()
    print(f"   CONTROL (el desvio de 10pt:10pt no puede ser cero): "
          f"{'PASADO' if ok else 'FALLADO'}")
    print(f"   Desvio del desvio con K={K}: {1/np.sqrt(2*(K-1))*100:.1f}%")
    return acum


if __name__ == "__main__":
    main()
