"""
VENTANA G - EL ERROR ESTANDAR DE VERDAD: rutas que se pisan entre si.

NO GASTA CARTUCHO. K = 261. Es la medicion del error de un instrumento, no una hipotesis de
mercado: no hay estadistico contra un alfa heredado, no se elige entre candidatas, no se
declara ninguna regla de operacion.

DE DONDE SALE ESTO, y es un error mio. Dos corridas del MISMO sesgo sobre el MISMO tipo de
serie -paseo gaussiano IID, bracket 20:10, todo resuelto- dieron +0,56 y +1,34 puntos. La
diferencia es 0,78, cuando el error estandar que yo venia reportando era 0,20-0,24. Una de
las dos cosas esta mal, y es el error estandar.

POR QUE ESTA MAL. Lo calculaba como binomial sobre el numero de rutas: raiz(p(1-p)/n). Eso
supone rutas INDEPENDIENTES. No lo son. Se sortean 30.000 entradas sobre una serie de 1,36
millones de barras y cada una escanea cientos o miles de barras: la misma barra participa de
decenas de rutas. Ademas hay una sola serie, y una serie tiene su propia realizacion. El
binomial mide el ruido del sorteo de entradas y no ve nada de lo otro.

QUE SE MIDE ACA. Se generan K series sinteticas INDEPENDIENTES, cada una del mismo largo que
ES 2016-2019, y se mide el sesgo en cada una con exactamente el mismo procedimiento con el
que se midio el real. El desvio del sesgo ENTRE series es el error estandar de verdad: es la
distribucion nula de "cuanto se corre de S/(S+T) una serie de este largo, sin estructura".

Con eso se contesta lo unico que importa: el residuo de ~1,3 puntos medido sobre ES real,
cabe adentro de esa nula o no?

CONTROL DE VACUIDAD INCORPORADO. El bracket simetrico 10:10 tiene pooled = 50% por identidad
de construccion, asi que su desvio entre series tiene que dar CERO EXACTO. Si diera algo
distinto de cero, la identidad que demostre estaria mal.
   QUE HARIA FALLAR ESE CONTROL: cualquier dispersion distinta de cero en la fila 10:10.
   Y al reves: que de cero NO informa nada sobre el mercado. Es la identidad, nada mas.
"""
import numpy as np

from linea_base import cargar, replica
from sintetico import armar, bootstrap, tripletes

K = 10
NPATHS = 30_000
SESION = 1380
HORIZONTES = [("1 sesion", SESION), ("5 sesiones", 5 * SESION)]
BRACKETS = [(10, 10), (20, 10), (5, 20)]
SEMILLA = 20260904

# Lo MEDIDO sobre ES real, para ponerlo contra la nula. Fuente: salida_desdrift.txt,
# factor de des-drift calibrado 0,425, horizonte de 5 sesiones.
REAL_DESDRIFT = {(10, 10): 0.00, (20, 10): -2.03, (5, 20): +1.19}
REAL_RESIDUO = {(10, 10): 0.00, (20, 10): -1.32, (5, 20): +0.78}
# Separacion largo/corto sobre ES real SIN des-driftar (factor 0,00), misma fuente.
REAL_SEP = {(10, 10): +5.67, (20, 10): +5.67, (5, 20): +3.68}


def sesgo(cl, hi, lo, con, T, S, horizonte, npaths=NPATHS):
    asum = S / (S + T)
    g = res = viv = nn = 0
    lad = {}
    for lado in ("largo", "corto"):
        r = replica(cl, hi, lo, con, T, S, lado, horizonte, npaths=npaths)
        ri = r["gana"] + r["pierde"] + r["amb"]
        lad[lado] = (r["gana"] / ri - asum) * 100
        g += r["gana"]; res += ri; viv += r["vivo"]; nn += r["n"]
    p = g / res
    sin_res = viv / nn * 100
    s = (p - asum) * 100
    return (s, s - (-0.5 * (T - S) / (T + S) * sin_res), sin_res,
            np.sqrt(p * (1 - p) / res) * 100, lad['largo'] - lad['corto'])


def main():
    print("=" * 100)
    print("EL ERROR ESTANDAR DE VERDAD - K series sinteticas independientes")
    print("NO GASTA CARTUCHO. K = 261. Medicion del error de un instrumento.")
    print("=" * 100)

    cl, hi, lo, con = cargar()
    n = len(cl)
    d, up, dn = tripletes(cl, hi, lo, con)
    mu = d.mean()
    dc, upc, dnc = d - mu, up - mu, dn - mu
    del cl, hi, lo, con
    print(f"\n   {K} series de {n:,} barras, remuestreo IID de las barras reales de ES")
    print(f"   (conserva la forma marginal exacta, destruye la estructura serial),")
    print(f"   centradas a media cero. {NPATHS:,} rutas por lado, igual que en el real.\n")

    con_s = np.zeros(n, dtype=np.int8)
    acum = {(nom, b): [] for nom, _ in HORIZONTES for b in BRACKETS}
    binom = {}
    for k in range(K):
        rng = np.random.default_rng(SEMILLA + 7919 * k)
        c2, h2, l2 = armar(*bootstrap(dc, upc, dnc, n, rng))
        for nom, h in HORIZONTES:
            for T, S in BRACKETS:
                s, resid, sr, se, sep = sesgo(c2, h2, l2, con_s, T, S, h)
                acum[(nom, (T, S))].append((s, resid, sr, sep))
                binom[(nom, (T, S))] = se
        del c2, h2, l2
        print(f"   serie {k+1}/{K} lista")

    for nom, _ in HORIZONTES:
        print("\n" + "=" * 100)
        print(f"HORIZONTE {nom.upper()} - dispersion del sesgo ENTRE series independientes")
        print("=" * 100)
        print(f"   {'bracket':>11}{'sesgo medio':>13}{'desvio REAL':>13}{'binomial':>11}"
              f"{'subestima':>11}{'min':>8}{'max':>8}{'recorrido':>11}")
        for T, S in BRACKETS:
            v = np.array([a[0] for a in acum[(nom, (T, S))]])
            sd, sb = v.std(ddof=1), binom[(nom, (T, S))]
            print(f"   {f'{T}pt:{S}pt':>11}{v.mean():>+13.3f}{sd:>13.3f}{sb:>11.3f}"
                  f"{(sd/sb if sb else float('nan')):>10.1f}x{v.min():>+8.2f}{v.max():>+8.2f}"
                  f"{v.max()-v.min():>11.2f}")

    print("\n" + "=" * 100)
    print("LA PREGUNTA - el residuo medido sobre ES real cabe adentro de esta nula?")
    print("   La nula es: series SIN estructura serial y SIN drift, del mismo largo que ES,")
    print("   medidas con el mismo procedimiento. Si el real cae adentro, el residuo NO esta")
    print("   establecido: es lo que hace una serie cualquiera de este largo.")
    print("   QUE HARIA FALLAR LA LECTURA 'no esta establecido': que el real quede afuera del")
    print("   recorrido completo de las K series, o a mas de 3 desvios de la media nula.")
    print("=" * 100)
    print(f"\n   {'bracket':>11}{'residuo REAL':>14}{'nula media':>12}{'nula desvio':>13}"
          f"{'en desvios':>12}{'nula min':>10}{'nula max':>10}{'cae adentro?':>14}")
    for T, S in BRACKETS:
        v = np.array([a[1] for a in acum[("5 sesiones", (T, S))]])
        r = REAL_RESIDUO[(T, S)]
        sd = v.std(ddof=1)
        z = (r - v.mean()) / sd if sd > 0 else float("nan")
        dentro = v.min() <= r <= v.max()
        print(f"   {f'{T}pt:{S}pt':>11}{r:>+14.2f}{v.mean():>+12.3f}{sd:>13.3f}"
              f"{z:>+12.1f}{v.min():>+10.2f}{v.max():>+10.2f}"
              f"{('SI' if dentro else 'NO'):>14}")

    print("\n" + "=" * 100)
    print("Y LA SEPARACION LARGO/CORTO - el drift medido sobrevive a la misma nula?")
    print("   Sobre ES real la separacion de 10pt:10pt dio +5,67 puntos, y con eso se")
    print("   calibro el factor de des-drift. Si la nula SIN drift ya produce")
    print("   separaciones de ese tamano, la calibracion no tiene de donde agarrarse.")
    print("   QUE HARIA FALLAR LA LECTURA 'el drift es real': que el valor real caiga")
    print("   adentro del recorrido de las K series, que no tienen drift por construccion.")
    print("=" * 100)
    print(f"\n   {'bracket':>11}{'sep REAL':>11}{'nula media':>12}{'nula desvio':>13}"
          f"{'en desvios':>12}{'nula min':>10}{'nula max':>10}{'cae adentro?':>14}")
    for T, S in BRACKETS:
        v = np.array([a[3] for a in acum[("5 sesiones", (T, S))]])
        r = REAL_SEP[(T, S)]
        sd = v.std(ddof=1)
        z = (r - v.mean()) / sd if sd > 0 else float("nan")
        dentro = v.min() <= r <= v.max()
        print(f"   {f'{T}pt:{S}pt':>11}{r:>+11.2f}{v.mean():>+12.3f}{sd:>13.3f}"
              f"{z:>+12.1f}{v.min():>+10.2f}{v.max():>+10.2f}"
              f"{('SI' if dentro else 'NO'):>14}")

    print("\n   Recordatorio: la fila 10pt:10pt es la IDENTIDAD de construccion. Su desvio")
    print("   tiene que ser cero exacto y no informa nada sobre el mercado.")
    return acum


if __name__ == "__main__":
    main()
