"""
EL TAMANO DE MUESTRA EN LAS CONSTANTES: son sensibles los cortes de tercil?

NO GASTA CARTUCHO. K = 261. ES 1-min 2016-2019, ya mirado. La caja sellada no se toca.

EL PROBLEMA, mio: instrumentos.py marca `cortes_tercil_bps` como MEDIDO sin decir SOBRE CUANTAS
SESIONES. Una calibracion de 6E hecha con 3 dias pasa la misma compuerta que la del ES hecha con
1.006. El origen deberia llevar tamano de muestra, no solo etiqueta.

Y MI PROPIA FORMA DE MATARLO, escrita antes: bootstrapear los cortes del ES a n = 50 / 100 / 250. Si
los cortes NO son sensibles al tamano, la anotacion es COSMETICA y hay que decirlo.

QUE SE MIDE, y son dos cosas distintas que no hay que confundir:
  1. la DISPERSION del corte en si (p33 y p66 en bps) al remuestrear n sesiones;
  2. cuantas sesiones CAMBIAN DE ETIQUETA cuando se clasifica el periodo entero con los cortes
     estimados en una muestra chica. Esto ultimo es lo que le importa al juez: el veredicto por
     regimen depende de la etiqueta, no del corte.

LO HARIA FALLAR la tesis de que hace falta anotar el tamano: que a n = 50 el error de etiqueta sea
comparable al de n = 1.006, o sea que remuestrear no mueva nada.

Y HAY UNA TERCERA COSA, que es la que de verdad decide y no es dispersion: un instrumento nuevo
calibrado con 3 dias no tiene UN CORTE RUIDOSO, tiene UN CORTE DE OTRA COSA -tres dias no contienen
regimen alto ni bajo, contienen los tres dias que se compraron-. Eso es SESGO, no varianza, y el
bootstrap no lo puede medir. Se mide aparte, con ventanas CONTIGUAS en vez de al azar.
"""

import os
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import juez as J  # noqa: E402

TAMANOS = (3, 10, 25, 50, 100, 250, 500)
NBOOT = 2000
SEMILLA = 20260906


def main():
    R = []
    A = R.append
    A("=" * 100)
    A("SON SENSIBLES LOS CORTES DE TERCIL AL TAMANO DE MUESTRA?")
    A("NO GASTA CARTUCHO. K = 261. La caja sellada no se toca.")
    A("=" * 100)
    m = J.cargar_mercado()
    ok = (m["anio_ses"] >= 2016) & (m["anio_ses"] <= 2019)
    # la volatilidad ex-ante de cada sesion, en bps: es lo que se corta en terciles
    t = m["tercil_exante"]
    p33, p66 = m["cortes_exante_bps"]
    # La serie de vol ex-ante, con LA MISMA definicion que cargar_mercado: rango MEDIO DE BARRA de
    # la sesion sobre el precio MEDIO de la sesion, en bps. (Primero la reconstrui como rango entero
    # de la sesion sobre el cierre y dio 67,7/112,3 contra los 1,814/2,622 del juez: el renglon de
    # verificacion de abajo lo agarro. No es "rango de la sesion": es el rango medio de las barras
    # de un minuto, que es una medida de agitacion y no de recorrido.)
    hi, lo, cl = m["hi"], m["lo"], m["cl"]
    ini, fin = m["ini"], m["fin"]
    rango = hi - lo
    vol_pt = np.array([rango[a:b].mean() for a, b in zip(ini, fin)])
    px_ses = np.array([cl[a:b].mean() for a, b in zip(ini, fin)])
    vol_bps = vol_pt / px_ses * 1e4
    prev = np.concatenate([[np.nan], vol_bps[:-1]])
    val = ok & ~np.isnan(prev)
    x = prev[val]
    n_all = len(x)
    A(f"\n   {n_all:,} sesiones 2016-2019 con volatilidad ex-ante en bps.")
    A(f"   Cortes del juez, calculados sobre todo el periodo: p33 = {p33:.3f} bps, "
      f"p66 = {p66:.3f} bps")
    A(f"   (verificacion: recalculados aca dan {np.quantile(x,1/3):.3f} y "
      f"{np.quantile(x,2/3):.3f}; tienen que coincidir)")

    rs = np.random.default_rng(SEMILLA)
    etiq_ref = np.where(x <= p33, 0, np.where(x <= p66, 1, 2))

    A("")
    A("-" * 100)
    A("   (1) BOOTSTRAP AL AZAR - solo varianza. Remuestreo n sesiones del periodo entero.")
    A("-" * 100)
    A(f"   {'n':>6}{'p33 medio':>12}{'sd p33':>9}{'p66 medio':>12}{'sd p66':>9}"
      f"{'% etiquetas mal':>18}{'p95 de ese %':>14}")
    filas = []
    for n in TAMANOS:
        c33 = np.empty(NBOOT); c66 = np.empty(NBOOT); mal = np.empty(NBOOT)
        for b in range(NBOOT):
            s = rs.choice(x, size=n, replace=True)
            a33, a66 = np.quantile(s, [1 / 3, 2 / 3])
            c33[b], c66[b] = a33, a66
            e = np.where(x <= a33, 0, np.where(x <= a66, 1, 2))
            mal[b] = (e != etiq_ref).mean()
        filas.append((n, c33.mean(), c33.std(ddof=1), c66.mean(), c66.std(ddof=1),
                      mal.mean(), np.percentile(mal, 95)))
        A(f"   {n:>6}{c33.mean():>12.3f}{c33.std(ddof=1):>9.3f}{c66.mean():>12.3f}"
          f"{c66.std(ddof=1):>9.3f}{mal.mean():>17.1%}{np.percentile(mal,95):>14.1%}")

    A("")
    A("-" * 100)
    A("   (2) VENTANAS CONTIGUAS - varianza MAS sesgo. Es lo que pasa de verdad al comprar n dias")
    A("       seguidos: no se sortean del periodo, se compra un tramo.")
    A("-" * 100)
    A(f"   {'n'  :>6}{'p33 medio':>12}{'sd p33':>9}{'p66 medio':>12}{'sd p66':>9}"
      f"{'% etiquetas mal':>18}{'peor tramo':>12}")
    for n in TAMANOS:
        starts = np.arange(0, n_all - n + 1)
        if len(starts) > 400:
            starts = starts[:: max(1, len(starts) // 400)]
        c33 = np.empty(len(starts)); c66 = np.empty(len(starts)); mal = np.empty(len(starts))
        for i, s0 in enumerate(starts):
            s = x[s0:s0 + n]
            a33, a66 = np.quantile(s, [1 / 3, 2 / 3])
            c33[i], c66[i] = a33, a66
            e = np.where(x <= a33, 0, np.where(x <= a66, 1, 2))
            mal[i] = (e != etiq_ref).mean()
        A(f"   {n:>6}{c33.mean():>12.3f}{c33.std(ddof=1):>9.3f}{c66.mean():>12.3f}"
          f"{c66.std(ddof=1):>9.3f}{mal.mean():>17.1%}{mal.max():>12.1%}")

    A("")
    A("=" * 100)
    A("   LO QUE DECIDE")
    A("=" * 100)
    f50 = [f for f in filas if f[0] == 50][0]
    f250 = [f for f in filas if f[0] == 250][0]
    f500 = [f for f in filas if f[0] == 500][0]
    f3 = [f for f in filas if f[0] == 3][0]
    A(f"   Error de etiqueta al azar:  n=3 {f3[5]:.0%}   n=50 {f50[5]:.1%}   n=250 {f250[5]:.1%}   "
      f"n=500 {f500[5]:.1%}")
    A(f"   O sea que la etiqueta de regimen a n=50 se equivoca en {f50[5]:.0%} de las sesiones, a")
    A(f"   n=250 en {f250[5]:.0%} y a n=3 en {f3[5]:.0%}: un tercio del periodo mal clasificado.")
    A("")
    A(f"   SI SON SENSIBLES, Y LA ANOTACION NO ES COSMETICA. El error de etiqueta cae {f3[5]/f500[5]:.0f}x")
    A(f"   entre n=3 y n=500. El veredicto por regimen exige que la ventaja aguante en LOS TRES")
    A(f"   terciles, y una etiqueta equivocada mueve sesiones de un tercil a otro: con {f3[5]:.0%} de")
    A(f"   etiquetas mal, 'aguanta en los tres' deja de significar lo que dice.")
    A(f"   Donde ponerlo: a n=250 el error es {f250[5]:.0%} y a n=500 {f500[5]:.0%}; el salto grande esta")
    A(f"   abajo de 100 ({[f for f in filas if f[0]==100][0][5]:.0%}) y se dispara abajo de 25 "
      f"({[f for f in filas if f[0]==25][0][5]:.0%}).")
    A("")
    A("   Y LA PARTE QUE EL BOOTSTRAP NO VE, que es la que importa mas: las ventanas CONTIGUAS dan")
    A("   peor que el sorteo al mismo n. El sorteo toma sesiones de los cuatro anos; comprar n dias")
    A("   seguidos toma el regimen que habia esa semana. Ese error es SESGO y no baja remuestreando:")
    A("   baja comprando dias REPARTIDOS por regimen, que es exactamente lo que ya se hizo con los")
    A("   seis dias de microestructura del ES y hay que repetir en cualquier instrumento nuevo.")
    A("=" * 100)
    print("\n".join(R))
    return 0


if __name__ == "__main__":
    sys.exit(main())
