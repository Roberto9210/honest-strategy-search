"""
VENTANA G - EL TEST SINTETICO. Es el replicador el que esta roto, o es el mercado?

NO GASTA CARTUCHO. K = 261. No hay hipotesis de mercado, no hay estadistico contra un alfa,
no se elige entre candidatas, no se declara ninguna regla de operacion. Es la validacion de
un instrumento de medicion contra un caso de respuesta conocida.

EL PROBLEMA. Sobre ES 2016-2019 el bracket con entradas al azar da una tasa corrida ~1,3
puntos de S/(S+T). Ya se descarto que sea ambiguedad de la barra (0%), censura por horizonte
(se resta y sobrevive) y drift (des-drift calibrado, sobrevive). Quedan dos culpables y hay
que separarlos: o el replicador tiene un defecto, o el precio real de ES no es un paseo sin
drift con barreras.

COMO SE SEPARAN. Se le da al MISMO replicador una serie donde la respuesta se conoce: un
paseo IID sin drift, donde S/(S+T) es exacto salvo sobrepaso de barrera. Si lo recupera, el
instrumento esta bien y el residuo es del mercado. Si no lo recupera, el defecto es mio.

  SINTETICO A - gaussiano. Paseo IID con la volatilidad por barra medida en ES, generado con
  sub-pasos dentro de cada barra para que el rango intrabarra no sea degenerado. Colas finas,
  sobrepaso de barrera minimo.

  SINTETICO B - bootstrap. Se remuestrean IID los tripletes reales de cada barra
  (delta de cierre, extension hacia arriba, extension hacia abajo), centrados a media cero.
  Conserva EXACTAMENTE la forma marginal de la barra de ES -colas, saltos, rango- y destruye
  SOLO la estructura serial. Es el test decisivo.

La comparacion A vs B aisla el efecto de las colas gordas sobre el sobrepaso. La comparacion
B vs real aisla la estructura serial.

LA PREDICCION ESTA SELLADA ANTES DE CORRER, en PREDICCION_SELLADA_sintetico.md.

UMBRALES. No se escriben a mano. Cada control se juzga contra su propio error estandar de
Monte Carlo, calculado desde el n de esa celda, y se reporta en unidades de ese error.

DATOS: ES 1-min Databento 2016-2019, fuera de la caja sellada (2020-01-02 -> 2026-08-19).
La caja no se toca.
"""
import numpy as np

from linea_base import cargar, replica

SESION = 1380
H_CORTO = SESION            # una sesion: el horizonte con el que se midio el residuo
H_LARGO = 20 * SESION       # "horizonte infinito" practico
NPATHS = 30_000
BRACKETS = [(10, 10), (20, 10), (5, 20)]
SEMILLA_GEN = 20260904
P0 = 3000.0                 # precio inicial; es un paseo aditivo, el nivel no cambia nada
M_CANDIDATOS = [1, 2, 3, 5, 8, 12, 20, 30]
NCAL = 200_000              # barras para calibrar el numero de sub-pasos


# ----------------------------------------------------------------------------------------
# tripletes reales y generadores
# ----------------------------------------------------------------------------------------
def tripletes(cl, hi, lo, con):
    """delta de cierre, extension arriba y extension abajo, todas medidas contra el cierre
    ANTERIOR. Se excluyen los saltos de contrato: un roll no es un movimiento de precio."""
    mismo = con[1:] == con[:-1]
    prev = cl[:-1][mismo]
    d = cl[1:][mismo] - prev
    up = hi[1:][mismo] - prev
    dn = lo[1:][mismo] - prev
    return d, up, dn


def armar(d, up, dn, p0=P0):
    """De incrementos a series OHLC acumuladas. up/dn ya vienen medidos contra el cierre
    anterior, asi que el desplazamiento es uniforme y la barra queda internamente coherente."""
    prev = p0 + np.concatenate(([0.0], np.cumsum(d)[:-1]))
    return prev + d, prev + up, prev + dn


def gauss(n, sigma, m, rng, chunk=200_000):
    """Paseo gaussiano IID con m sub-pasos por barra. La barra arranca en el cierre anterior,
    asi que el maximo y el minimo incluyen ese punto de partida."""
    ds, ups, dns = [], [], []
    s = sigma / np.sqrt(m)
    hecho = 0
    while hecho < n:
        b = min(chunk, n - hecho)
        cs = np.cumsum(rng.normal(0.0, s, (b, m)), axis=1)
        ds.append(cs[:, -1])
        ups.append(np.maximum(cs.max(axis=1), 0.0))
        dns.append(np.minimum(cs.min(axis=1), 0.0))
        hecho += b
    return np.concatenate(ds), np.concatenate(ups), np.concatenate(dns)


def bootstrap(d, up, dn, n, rng):
    k = rng.integers(0, len(d), n)
    return d[k], up[k], dn[k]


# ----------------------------------------------------------------------------------------
# medicion
# ----------------------------------------------------------------------------------------
def medir(cl, hi, lo, con, T, S, horizonte, npaths=NPATHS):
    """Sesgo de la tasa observada contra S/(S+T), por lado y pooled, con el error estandar
    de Monte Carlo de cada uno. El error estandar NO se escribe a mano: sale del n."""
    asum = S / (S + T)
    g = res = viv = nn = am = 0
    lados, se_l = {}, {}
    for lado in ("largo", "corto"):
        r = replica(cl, hi, lo, con, T, S, lado, horizonte, npaths=npaths)
        ri = r["gana"] + r["pierde"] + r["amb"]
        p = r["gana"] / ri
        lados[lado] = (p - asum) * 100
        se_l[lado] = np.sqrt(p * (1 - p) / ri) * 100
        g += r["gana"]; res += ri; viv += r["vivo"]; nn += r["n"]; am += r["amb"]
    pp = g / res
    return dict(largo=lados["largo"], corto=lados["corto"], pool=(pp - asum) * 100,
                sep=lados["largo"] - lados["corto"],
                se_pool=np.sqrt(pp * (1 - pp) / res) * 100,
                se_sep=np.sqrt(se_l["largo"] ** 2 + se_l["corto"] ** 2),
                sin_res=viv / nn * 100, amb=am / res * 100, n=res)


def veredicto(valor, se, k=3.0):
    """Compatible con cero a k errores estandar. El umbral se deriva del n, no se elige."""
    return abs(valor) <= k * se


def main():
    print("=" * 100)
    print("TEST SINTETICO - el replicador contra un caso de respuesta conocida")
    print("NO GASTA CARTUCHO. K = 261. Prediccion sellada en PREDICCION_SELLADA_sintetico.md")
    print("=" * 100)

    cl, hi, lo, con = cargar()
    n = len(cl)
    d, up, dn = tripletes(cl, hi, lo, con)
    mu_d, sd_d = d.mean(), d.std()
    rango_real = (hi - lo).mean()
    print(f"\nES 1-min 2016-2019: {n:,} barras, {len(d):,} incrementos utiles "
          f"(se excluyen {n-1-len(d)} saltos de contrato).")
    print(f"   media del incremento  {mu_d:+.6f} pt   (el drift medido)")
    print(f"   desvio del incremento  {sd_d:.4f} pt")
    print(f"   rango medio de la barra {rango_real:.4f} pt")
    print(f"   barras con maximo por debajo del cierre anterior: "
          f"{(up < 0).mean()*100:.2f}%")

    # los sinteticos se centran a media cero EXACTA: el drift es lo que se quiere sacar
    dc, upc, dnc = d - mu_d, up - mu_d, dn - mu_d

    print("\n" + "=" * 100)
    print("CONTROL 0 - el generador. Los sinteticos tienen que igualar volatilidad y rango")
    print("   QUE LO HARIA FALLAR: media del incremento distinta de cero, o desvio / rango")
    print("   que no reproduzcan los de ES. Ahi el sintetico no seria comparable con el real.")
    print("=" * 100)

    rng = np.random.default_rng(SEMILLA_GEN)
    print(f"\n   Calibracion del numero de sub-pasos contra el rango medio real "
          f"({rango_real:.4f} pt):")
    mejor, mejor_err = None, np.inf
    for m in M_CANDIDATOS:
        gd, gu, gl = gauss(NCAL, sd_d, m, np.random.default_rng(SEMILLA_GEN + m))
        rg = (gu - gl).mean()
        err = abs(rg - rango_real)
        marca = ""
        if err < mejor_err:
            mejor, mejor_err, marca = m, err, ""
        print(f"      m = {m:>3}   rango medio {rg:.4f} pt   dif {rg-rango_real:+.4f}{marca}")
    print(f"   -> se toma m = {mejor} sub-pasos por barra (el mas cercano al rango real).")
    if mejor == M_CANDIDATOS[-1]:
        print("      AVISO: el optimo esta en el borde de la grilla; un gaussiano no puede")
        print("      superar ~1,60 desvios de rango medio y ES podria estar por encima.")

    series = {}
    gd, gu, gl = gauss(n, sd_d, mejor, rng)
    series["A gaussiano"] = armar(gd, gu, gl)
    bd, bu, bl = bootstrap(dc, upc, dnc, n, rng)
    series["B bootstrap"] = armar(bd, bu, bl)
    con_syn = np.zeros(n, dtype=np.int8)

    print(f"\n   {'serie':<14}{'media inc':>12}{'desvio inc':>12}{'rango medio':>13}"
          f"{'vs real':>10}")
    print(f"   {'ES real':<14}{mu_d:>+12.6f}{sd_d:>12.4f}{rango_real:>13.4f}{'-':>10}")
    ok0 = True
    for nom, (c2, h2, l2) in series.items():
        di = np.diff(c2)
        rg = (h2 - l2).mean()
        print(f"   {nom:<14}{di.mean():>+12.6f}{di.std():>12.4f}{rg:>13.4f}"
              f"{(rg/rango_real-1)*100:>+9.1f}%")
        # media cero: contra el error estandar de la propia media, derivado del n
        se_mu = di.std() / np.sqrt(len(di))
        if abs(di.mean()) > 3 * se_mu:
            ok0 = False
    print(f"\n   media cero a 3 errores estandar: {'OK' if ok0 else 'MAL'}")
    print(f"   B reproduce el rango real por construccion (remuestrea barras enteras).")
    print(f"   CONTROL 0 {'PASADO' if ok0 else 'FALLADO'}")

    # ------------------------------------------------------------------------------------
    print("\n" + "=" * 100)
    print(f"CONTROL 1 - HORIZONTE LARGO ({H_LARGO//SESION} sesiones). Casi todo resuelve, y")
    print("   sin censura un paseo IID sin drift TIENE que dar S/(S+T).")
    print("   QUE LO HARIA FALLAR: sesgo por encima de 3 errores estandar con sin-resolver")
    print("   cerca de cero. Eso seria el replicador roto, y nada mas de esta ventana valdria.")
    print("=" * 100)
    print(f"\n   {'serie':<14}{'bracket':>11}{'S/(S+T)':>10}{'sesgo pool':>12}{'error est':>11}"
          f"{'en errores':>12}{'sin resolv':>12}{'ambiguo':>10}{'veredicto':>11}")
    ok1 = True
    largo = {}
    for nom, (c2, h2, l2) in series.items():
        for T, S in BRACKETS:
            r = medir(c2, h2, l2, con_syn, T, S, H_LARGO)
            largo[(nom, T, S)] = r
            bien = veredicto(r["pool"], r["se_pool"])
            ok1 &= bien
            print(f"   {nom:<14}{f'{T}pt:{S}pt':>11}{S/(S+T)*100:>9.1f}%{r['pool']:>+12.2f}"
                  f"{r['se_pool']:>11.2f}{r['pool']/r['se_pool']:>+12.1f}"
                  f"{r['sin_res']:>11.1f}%{r['amb']:>9.3f}%{('OK' if bien else 'MAL'):>11}")
    print(f"\n   CONTROL 1 {'PASADO' if ok1 else 'FALLADO'}")

    # ------------------------------------------------------------------------------------
    print("\n" + "=" * 100)
    print("CONTROL 2 - SEPARACION LARGO/CORTO. Los sinteticos no tienen drift por")
    print("   construccion, asi que los dos lados tienen que dar lo mismo.")
    print("   QUE LO HARIA FALLAR: separacion por encima de 3 errores estandar. Eso seria")
    print("   drift residual en el generador, o un replicador que trata distinto a los lados.")
    print("   NO es vacio: sobre ES real esta misma medicion da +5,67 puntos.")
    print("=" * 100)
    print(f"\n   {'serie':<14}{'bracket':>11}{'largo':>9}{'corto':>9}{'separacion':>12}"
          f"{'error est':>11}{'en errores':>12}{'veredicto':>11}")
    ok2 = True
    for nom in series:
        for T, S in BRACKETS:
            r = largo[(nom, T, S)]
            bien = veredicto(r["sep"], r["se_sep"])
            ok2 &= bien
            print(f"   {nom:<14}{f'{T}pt:{S}pt':>11}{r['largo']:>+9.2f}{r['corto']:>+9.2f}"
                  f"{r['sep']:>+12.2f}{r['se_sep']:>11.2f}"
                  f"{r['sep']/r['se_sep']:>+12.1f}{('OK' if bien else 'MAL'):>11}")
    print(f"\n   CONTROL 2 {'PASADO' if ok2 else 'FALLADO'}")

    # ------------------------------------------------------------------------------------
    print("\n" + "=" * 100)
    print("LA PREGUNTA - a UNA SESION, el sintetico reproduce el residuo de ~1,3 puntos?")
    print("   El sesgo por censura se predice con -0,5 x asimetria x %sin_resolver.")
    print("   RESIDUO = sesgo pooled - lo que la censura explica.")
    print("   QUE HARIA FALLAR LA LECTURA 'el replicador esta bien': un residuo sintetico")
    print("   del mismo tamano que el real. Ahi el culpable seria el codigo, no el mercado.")
    print("=" * 100)
    print(f"\n   {'serie':<14}{'bracket':>11}{'sesgo pool':>12}{'sin resolv':>12}"
          f"{'ambiguo':>10}{'censura':>10}{'RESIDUO':>10}{'error est':>11}{'en errores':>12}")
    resid = {}
    for nom, (c2, h2, l2) in list(series.items()):
        for T, S in BRACKETS:
            r = medir(c2, h2, l2, con_syn, T, S, H_CORTO)
            asim = (T - S) / (T + S)
            pred = -0.5 * asim * r["sin_res"]
            rr = r["pool"] - pred
            resid[(nom, T, S)] = (rr, r["se_pool"])
            print(f"   {nom:<14}{f'{T}pt:{S}pt':>11}{r['pool']:>+12.2f}{r['sin_res']:>11.1f}%"
                  f"{r['amb']:>9.3f}%{pred:>+10.2f}{rr:>+10.2f}{r['se_pool']:>11.2f}"
                  f"{rr/r['se_pool']:>+12.1f}")

    print("\n   Para comparar, lo MEDIDO sobre ES real (des-driftado, 5 sesiones):")
    print("      10pt:10pt  residuo +0,00   (identidad de construccion, no informa)")
    print("      20pt:10pt  residuo -1,32")
    print("      5pt:20pt   residuo +0,78")

    peor = max(abs(v[0]) for k, v in resid.items() if k[1] != k[2])
    print(f"\n   Peor residuo sintetico en un bracket asimetrico: {peor:.2f} puntos.")
    return dict(ok0=ok0, ok1=ok1, ok2=ok2, resid=resid, peor=peor, m=mejor)


if __name__ == "__main__":
    main()
