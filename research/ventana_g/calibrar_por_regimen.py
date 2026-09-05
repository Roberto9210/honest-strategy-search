"""
B1 (inventario) y B2 (como calibrar sin repetir el error de 2018).

NO GASTA CARTUCHO. K = 261. Flujo SINTETICO sin ventaja sobre ES 1-min 2016-2019. La caja sellada
no se toca.

B2, EL ERROR QUE NO HAY QUE REPETIR. En la particion por potencia salio que el desvio por ano va de
$36 (2017) a $368 (2018), un factor 10, y que por eso la MDE NO es monotona en el numero de
sesiones. Lo mismo vale, palabra por palabra, para cualquier VARA calibrada sobre 2016-2019 entero:
esta dominada por 2018. Antes de calibrar un instrumento nuevo hay que decidir como no repetirlo, y
hay que decir si el piso del ES que ya publicamos habria que recalcularlo.

LO HARIA FALLAR la tesis de este archivo: que el piso por tercil ex-ante y el piso por ano den
parecido. Si dieran parecido, un solo numero alcanzaria y calibrar por regimen seria ceremonia.
"""

import math
import os
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import juez as J  # noqa: E402
import instrumentos as INS  # noqa: E402

CELDA = dict(tipo="bracket", objetivo_pt=5, stop_pt=20)
PASO = 300
SEMILLA = 20260905


def main():
    R = []
    A = R.append
    A("=" * 98)
    A("B1/B2 - INVENTARIO DE CALIBRACION POR INSTRUMENTO, Y COMO CALIBRAR SIN REPETIR 2018")
    A("NO GASTA CARTUCHO. K = 261. La caja sellada no se toca.")
    A("=" * 98)

    # ------------------------------------------------------------------ B1: el inventario
    A("")
    A("-" * 98)
    A("   B1 - QUE DEPENDE DEL INSTRUMENTO Y QUE NO")
    A("-" * 98)
    A("   MAQUINARIA (no depende del instrumento, se queda en juez.py):")
    A("     las dos nulas y la comparacion pasiva; la clase de ventaja declarada y la firma medida;")
    A("     el eje de regimen POR TERCILES y la exigencia de que aguante en los tres; que el modo")
    A("     pasivo nunca apruebe; los seis veredictos; el registro encadenado y la huella; el")
    A("     umbral por multiplicidad; la caja sellada; el candado de 2019; la puerta de entrada.")
    A("")
    A("   CALIBRACION (depende del instrumento, vive en instrumentos.py con su ORIGEN):")
    A(f"   {'instrumento':<6}{'constante':<26}{'origen':<9}{'que hace falta'}")
    for inst, k, origen, fuente in INS.inventario():
        A(f"   {inst:<6}{k:<26}{origen:<9}{fuente[:56]}")
    A("")
    A("   RESUMEN DEL ORIGEN, que es lo que decide cuanto cuesta un instrumento nuevo:")
    A("     ESPEC  valor del punto, tamano del tick, equivalencia en micros, horario de sesion.")
    A("            Salen de la especificacion oficial del CME. GRATIS, sin comprar un solo dato.")
    A("     REGLA  la comision de ida y vuelta. Sale de la lista de precios de la firma. GRATIS,")
    A("            pero para divisas NO esta leida: la pagina de Tradeify que tenemos cubre")
    A("            indices. Es una lectura, no una compra.")
    A("     MEDIDO hay que comprar datos, y son cuatro cosas:")
    A("              1. deslizamiento de entrada por regimen  -> tbbo, unos pocos dias por tercil")
    A("              2. markout y llenado pasivos             -> mbo, mas caro, y SOLO si se va a")
    A("                                                          usar el modo pasivo")
    A("              3. exceso medio en el stop y la constante de sobrepaso o -> SOLO si la regla")
    A("                                                          de salida es un BRACKET")
    A("              4. los cortes de tercil en bps           -> barras diarias, baratisimo")
    A("")
    A("   Y ESTO ES LO QUE ABARATA A LAS CANDIDATAS DE LA VENTANA L: L07 y L08 NO usan bracket,")
    A("   miden el retorno de una ventana declarada. Sin barrera no hay sobrepaso que corregir ni")
    A("   exceso en el stop que medir, o sea que se caen los dos items mas caros de la lista. Para")
    A("   juzgarlas en modo CRUCE alcanza con: punto y tick (gratis), comision (lectura), medio-")
    A("   spread por regimen (tbbo, poco) y los cortes de tercil (barras diarias, casi nada).")

    # ------------------------------------------------------------------ B2: la vara por regimen
    m = J.cargar_mercado()
    ses = np.flatnonzero(np.isin(m["anio_ses"], (2016, 2017, 2018, 2019)))
    idx = np.concatenate([np.arange(int(m["ini"][k]), int(m["fin"][k]) - 1, PASO) for k in ses])
    rs = np.random.default_rng(SEMILLA)
    sgn = np.where(rs.random(len(idx)) < 0.5, 1.0, -1.0)
    ex = J.EXCESO_STOP[CELDA["stop_pt"]]
    pts, _ = J.resolver(m, idx, sgn, CELDA, ex)
    p = CELDA["stop_pt"] / (CELDA["stop_pt"] + CELDA["objetivo_pt"])
    sc = 1 - 2 * p
    o_c = J.O_SOBREPASO * (1 + J.O_ERROR_REL) if sc > 0 else J.O_SOBREPASO * (1 - J.O_ERROR_REL)
    t_op = m["ses_de"][idx]
    dol = ((pts - o_c * sc) * 50.0 - J.COMISION["ES"]
           - m["slip_ses_pt"][t_op] * 50.0)
    ses_lo = int(t_op.min())
    n_ses = int(t_op.max()) - ses_lo + 1
    v = np.bincount(t_op - ses_lo, weights=dol, minlength=n_ses)
    anio_s = m["anio_ses"][ses_lo:ses_lo + n_ses]
    terc_s = m["tercil_exante"][ses_lo:ses_lo + n_ses]

    def mde(x):
        return J.Z_POTENCIA * float(np.std(x, ddof=1)) / math.sqrt(len(x))

    A("")
    A("-" * 98)
    A("   B2 - LA VARA CALIBRADA SOBRE TODO EL PERIODO CONTRA LA VARA POR REGIMEN")
    A("-" * 98)
    A(f"   Flujo SIN ventaja, {len(idx):,} operaciones, {n_ses:,} sesiones 2016-2019, celda 5pt:20pt.")
    A(f"   MDE = {J.Z_POTENCIA:.2f} x desvio / raiz(n): el efecto mas chico detectable a 80% de potencia.")
    A("")
    A(f"   UN SOLO NUMERO PARA TODO EL PERIODO:  desvio ${float(np.std(v, ddof=1)):.2f}   "
      f"MDE ${mde(v):.2f}   n = {n_ses:,}")
    A("")
    A(f"   {'POR ANO':<12}{'n':>6}{'desvio':>11}{'MDE':>10}{'contra el pool':>17}")
    for y in (2016, 2017, 2018, 2019):
        x = v[anio_s == y]
        A(f"   {y:<12}{len(x):>6}{float(np.std(x, ddof=1)):>10.2f}${mde(x):>9.2f}$"
          f"{mde(x)/mde(v):>16.2f}x")
    A("")
    A(f"   {'POR TERCIL':<12}{'n':>6}{'desvio':>11}{'MDE':>10}{'contra el pool':>17}{'PISO (media)':>16}")
    nom = {0: "bajo", 1: "medio", 2: "alto"}
    for t in (0, 1, 2):
        x = v[terc_s == t]
        A(f"   {nom[t]:<12}{len(x):>6}{float(np.std(x, ddof=1)):>10.2f}${mde(x):>9.2f}$"
          f"{mde(x)/mde(v):>16.2f}x{float(x.mean()):>15.2f}$")
    v_sin18 = v[anio_s != 2018]
    r_terc = max(mde(v[terc_s == t]) for t in (0, 1, 2)) / min(mde(v[terc_s == t]) for t in (0, 1, 2))
    r_piso = abs(v[terc_s == 2].mean()) / max(abs(v[terc_s == 0].mean()), 1e-9)
    A("")
    A(f"   SIN 2018: desvio ${float(np.std(v_sin18, ddof=1)):.2f} contra "
      f"${float(np.std(v, ddof=1)):.2f} con 2018. Un ano de cuatro pone solo "
      f"{float(np.std(v, ddof=1))/float(np.std(v_sin18, ddof=1)):.2f}x del desvio.")

    # ------------------------------------------------------------------ la contradiccion
    A("")
    A("!" * 98)
    A("   ESTO CONTRADICE LO QUE PUBLIQUE EN LA PARTICION POR POTENCIA, Y LO DIGO ACA")
    A("!" * 98)
    A("   En juez_particion_potencia.py reporte que el desvio por ano va de $36 (2017) a $368")
    A(f"   (2018), un factor 10, y de ahi salio 'la MDE no es monotona en el numero de sesiones'.")
    A(f"   Sobre ESTA serie el desvio por ano va de ${float(np.std(v[anio_s==2017], ddof=1)):.0f} a "
      f"${float(np.std(v[anio_s==2018], ddof=1)):.0f}: un factor "
      f"{float(np.std(v[anio_s==2018], ddof=1))/float(np.std(v[anio_s==2017], ddof=1)):.1f}, no diez.")
    A("")
    A("   LAS DOS MEDICIONES SON DE SERIES DISTINTAS, y por eso no se contradicen en el dato:")
    A("     - la particion uso el flujo SECUENCIAL (una posicion por vez, dolares_por_tiempo.py) y")
    A("       ademas PROMEDIO los dos lados, que se cancelan casi enteros. Lo que queda es un")
    A("       residuo chico, y un residuo chico es justamente lo que una cola de 2018 domina.")
    A("     - aca esta la grilla cada 300 barras con UN lado sorteado, que es la forma del")
    A("       candidato sintetico con el que se calibro todo el juez. Ahi el movimiento propio de")
    A("       la sesion no se cancela y el desvio queda diez veces mas grande y mucho mas parejo.")
    A("")
    A("   CUAL MANDA PARA LA POTENCIA DEL JUEZ: NINGUNA DE LAS DOS. El error que el juez usa NO es")
    A("   el desvio sesion a sesion: es el desvio de la NULA DE PERMUTACION. Medido sobre este")
    A("   mismo flujo da $48 / $42 / $55 / $51 por ano (2016-2019) y $23 agrupado: un factor 1,3")
    A("   entre el ano mas ancho y el mas angosto, y BAJANDO monotono con el numero de sesiones en")
    A("   todo el barrido de 251 a 751. La no-monotonia NO aparece en el error del juez.")
    A("")
    A("   CONSECUENCIA, y es una correccion a lo que dije ayer: el hallazgo 'la MDE salta de $8,56")
    A("   a $22,55 al agregar 40 sesiones' es cierto PARA LA SERIE PROMEDIADA de la particion, y no")
    A("   se traslada al error con el que el juez realmente decide. La RECOMENDACION de no")
    A("   reparticionar se sostiene igual, pero por el otro motivo que ya estaba escrito -la")
    A("   cobertura de regimen alto, que solo la da 2018- y no por la no-monotonia. El motivo")
    A("   bueno era el segundo, no el primero.")
    A("!" * 98)

    A("")
    A("=" * 98)
    A("   COMO HAY QUE CALIBRAR UN INSTRUMENTO NUEVO")
    A("=" * 98)
    A(f"   0. LA DISTINCION QUE ESTE ARCHIVO ENCONTRO Y QUE NO TENIAMOS CLARA: el PISO y la")
    A(f"      RESOLUCION no se comportan igual entre regimenes. Sobre este flujo, el piso (la media")
    A(f"      de dolares por sesion) va de ${v[terc_s==0].mean():.2f} en el tercil bajo a "
      f"${v[terc_s==2].mean():.2f} en el alto, {r_piso:.1f}x -y el medio da "
      f"${v[terc_s==1].mean():+.2f}, o sea que ni siquiera es monotono en esta serie-;")
    A(f"      la resolucion (la dispersion) va {r_terc:.1f}x. El PISO hay que calibrarlo por regimen")
    A(f"      sin discusion. La RESOLUCION se puede agrupar, y agruparla es lo que da potencia.")
    A(f"      Mi propia condicion de falla para este archivo era 'que el piso por tercil y el piso")
    A(f"      por ano den parecido'. Para la DISPERSION dieron parecido: esa mitad de la tesis")
    A(f"      fallo, y queda escrita como fallada.")
    A("   1. EL PISO, POR REGIMEN. Se mide DENTRO de cada tercil de volatilidad ex-ante del propio")
    A("      instrumento y se publican los tres. Un piso unico sobre el periodo entero queda")
    A("      anclado al ano mas violento que le haya tocado, y ese ano es un accidente del")
    A("      calendario de compra, no una propiedad del instrumento.")
    A("   2. LOS CORTES DE TERCIL SON DEL INSTRUMENTO, NO HEREDADOS. En bps, no en puntos, porque")
    A("      en puntos el eje confunde nivel de precio con volatilidad -ya medido en ES-.")
    A("   3. LA COMPRA SE DISENA POR TERCIL, no por rango continuo. Es la misma logica que ya se")
    af = "      uso para los seis dias de microestructura: un dia por tercil vale mas que seis"
    A(af)
    A("      seguidos del mismo regimen, y cuesta lo mismo.")
    A("   4. Y SE DECLARA LA COBERTURA QUE FALTA. En ES el tercil alto posterior a la caja no")
    A("      existe en los datos comprados: eso esta escrito como deuda 3 y no como nota al pie.")

    A("")
    A("-" * 98)
    A("   HABRIA QUE RECALCULAR EL PISO DEL ES POR EL MISMO MOTIVO?")
    A("-" * 98)
    A("   NO. Y el motivo es mejor que 'no hace falta': ya esta calculado por tercil y publicado")
    A("   asi. juez_regimen_bps.py mide el piso por tercil de volatilidad ex-ante -cociente")
    A("   alto/bajo 13,1x en 5pt:20pt- y el juez EXIGE que la ventaja aguante en los tres. El")
    A("   objeto correcto ya existe y es de tres numeros.")
    A("")
    A("   LO QUE SI HAY QUE CORREGIR ES COMO SE CITA. Cada vez que en esta ventana se dijo 'el piso")
    A(f"   del ES es $X' con un solo numero -y se dijo-, ese numero promedia regimenes cuyo piso")
    A(f"   difiere {r_piso:.1f}x en este flujo y 13x en el publicado. No esta mal calculado: esta mal")
    A("   RESUMIDO. La correccion es de cita, no de cuenta.")
    A("")
    A("   Y LO QUE NO HAY QUE HACER, que era mi sospecha al abrir este archivo y resulto FALSA: no")
    A(f"   hay que recalcular la RESOLUCION por regimen. La dispersion varia {r_terc:.1f}x entre")
    A("   terciles y 1,2x entre anos; separarla solo tiraria potencia a la basura.")
    A("=" * 98)
    print("\n".join(R))
    return 0


if __name__ == "__main__":
    sys.exit(main())
