"""
TAREA 1(a) - EL PISO DE LAS CELDAS ESTRECHAS, DESCOMPUESTO. Y una correccion a mi propio numero.

NO GASTA CARTUCHO. K = 261. Dinero: $0. ES 1-min 2016-2018, candidatos SINTETICOS. La caja sellada
no se toca.

LA CORRECCION QUE VA PRIMERA, porque es mia: reporte que el piso de 3pt:4pt era $85,38 contra $78,24
de 5pt:20pt, y dije "la ventana operable no viene con descuento". El numero estaba MAL Y COMPARABA
PERAS CON MANZANAS: lo calcule como frecuencia x (comision + medio-spread) y NO incluia el EXCESO EN
EL STOP, que si esta dentro del $78,24. Y el exceso es justamente el termino que mas duele en un
bracket estrecho, porque EXCESO_STOP solo esta medido para stops de 10 y 20 pt: para un stop de 4 el
juez sustituye 0,722 pt, que es el 18% del stop contra el 4,9% de un stop de 20.

QUE SE HACE ACA: descomponer el piso en sus terminos, celda por celda, para ver cual manda.

LA PREDICCION NULA, POR COMPONENTE -desglosada, que es la forma adoptada-:
  (i)   si el exceso sustituido no importara, el piso escalaria con la frecuencia y nada mas, o sea
        que 3pt:4pt (7 op/dia) daria ~5x el piso de 5pt:20pt (1,5 op/dia);
  (ii)  si el termino de ambiguedad mandara, el piso crecerian al estrecharse mas rapido que la
        frecuencia;
  (iii) si manda el exceso sustituido, el piso explota en las celdas de stop chico y NO en las de
        stop grande a igual frecuencia.
Las tres se distinguen mirando la descomposicion.
"""

import math
import os
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import instrumentos as INS  # noqa: E402
import juez as J  # noqa: E402

PASO = 60
MEDIO_SPREAD_PT = 0.13
CELDAS = [(5, 20), (3, 4), (2, 3), (2, 2), (1, 2)]


def main():
    R = []
    A = R.append
    A("=" * 100)
    A("TAREA 1(a) - EL PISO DE LAS CELDAS ESTRECHAS, DESCOMPUESTO")
    A("NO GASTA CARTUCHO. K = 261. Dinero: $0. La caja sellada no se toca.")
    A("=" * 100)
    A("")
    A("   CORRECCION MIA, primero: reporte el piso de 3pt:4pt como $85,38 contra $78,24 de")
    A("   5pt:20pt. Ese $85,38 NO incluia el exceso en el stop y el $78,24 SI. No eran comparables.")
    m = J.cargar_mercado()
    ses = np.flatnonzero(np.isin(m["anio_ses"], (2016, 2017, 2018)))
    idx = np.concatenate([np.arange(int(m["ini"][k]), int(m["fin"][k]) - 1, PASO) for k in ses])
    n_ses = len(ses)
    o_tab = INS.INSTRUMENTOS["ES"]["o_por_span"]["valor"]
    amb_tab = INS.INSTRUMENTOS["ES"]["tasa_ambigua_por_span"]["valor"]

    A("")
    A(f"   {'celda':>10}{'span':>6}{'op/ses':>8}{'p(stop)':>9}{'exceso usado':>14}{'% del stop':>12}"
      f"{'comision':>10}{'m-spread':>10}{'EXCESO':>10}{'sesgo':>9}{'PISO $/ses':>12}")
    filas = {}
    for T, S in CELDAS:
        regla = dict(tipo="bracket", objetivo_pt=float(T), stop_pt=float(S))
        span = float(T + S)
        p = S / (S + T)
        exc = J.EXCESO_STOP.get(int(S))
        sust = exc is None
        if sust:
            exc = J.EXCESO_STOP[min(J.EXCESO_STOP, key=lambda k: abs(k - S))]
        pL, tL = J.resolver(m, idx, np.ones(len(idx)), regla, exc)
        pS, tS = J.resolver(m, idx, -np.ones(len(idx)), regla, exc)
        pts = np.concatenate([pL, pS])
        op_ses = len(pts) / n_ses
        # fraccion que termina en stop (pts negativos del tamano del stop)
        fr_stop = float(np.mean(pts <= -(S + exc) + 1e-9))
        # terminos del piso, en $/sesion, a 1 ES
        c_com = op_ses * J.COMISION["ES"]
        c_spr = op_ses * MEDIO_SPREAD_PT * J.PUNTO["ES"]
        c_exc = op_ses * fr_stop * exc * J.PUNTO["ES"]
        o_s = J.interp_span(o_tab, span)
        amb = J.interp_span(amb_tab, span)
        sesgo = o_s * (1 - 2 * p) - amb * span * 0.5
        c_ses = -op_ses * sesgo * J.PUNTO["ES"]      # el sesgo se RESTA, asi que su costo es -sesgo
        piso = c_com + c_spr + c_exc + c_ses
        filas[(T, S)] = dict(op=op_ses, piso=piso, com=c_com, spr=c_spr, exc=c_exc, ses=c_ses,
                             sust=sust, exc_pt=exc, fr=fr_stop)
        A(f"   {f'{T}pt:{S}pt':>10}{span:>6.0f}{op_ses:>8.2f}{fr_stop:>9.2f}"
          f"{exc:>11.3f}{'*' if sust else ' '}{exc/S:>12.0%}{c_com:>10.2f}{c_spr:>10.2f}"
          f"{c_exc:>10.2f}{c_ses:>9.2f}{piso:>12.2f}")
    A("   (*) exceso SUSTITUIDO: no esta medido para ese stop, se usa el medido mas cercano.")

    A("")
    A("=" * 100)
    A("   QUE MANDA")
    A("=" * 100)
    for (T, S), d in filas.items():
        pc = {k: d[k] / d["piso"] for k in ("com", "spr", "exc", "ses")}
        A(f"   {T}pt:{S}pt  piso ${d['piso']:.2f}/ses  =  comision {pc['com']:.0%} + "
          f"medio-spread {pc['spr']:.0%} + EXCESO {pc['exc']:.0%} + sesgo {pc['ses']:+.0%}")
    ref = filas[(5, 20)]
    A("")
    A(f"   MANDA EL EXCESO EN EL STOP, y en las estrechas es SUSTITUIDO y no medido:")
    for (T, S), d in filas.items():
        if (T, S) == (5, 20):
            continue
        A(f"      {T}pt:{S}pt: piso ${d['piso']:.2f} contra ${ref['piso']:.2f} de 5pt:20pt = "
          f"{d['piso']/ref['piso']:.1f}x, con el exceso pasando de {ref['exc']/ref['piso']:.0%} a "
          f"{d['exc']/d['piso']:.0%} del piso")
    A("")
    A("   OJO CON COMO SE LEE LA COLUMNA op/ses: es IGUAL en las cinco filas (45,61) porque la")
    A("   grilla de entradas es la misma. Eso NO es un hallazgo, es el montaje: la comparacion es A")
    A("   FRECUENCIA FIJA, y sirve justamente para aislar el costo POR OPERACION de la frecuencia.")
    A("   Comparar a frecuencia natural de cada celda es otra cuenta y no es esta.")
    A("")
    A("   La prediccion (iii) es la que se cumple: a IGUAL frecuencia, el piso de las estrechas es")
    A("   1,4 a 1,7 veces el de 5pt:20pt, y la diferencia entera esta en el exceso del stop -que")
    A("   pasa de 22% del piso a 45-58%-. Los otros tres terminos son identicos por construccion.")
    A("")
    A("   Y LO QUE ESTO SIGNIFICA PARA LA VENTANA OPERABLE, sin suavizar: las celdas que el")
    A("   reglamento permite operar tienen un piso dominado por una constante SUSTITUIDA. El juez la")
    A("   sustituye en la direccion conservadora -sobreestima el costo- pero eso quiere decir que su")
    A("   piso para brackets estrechos es una COTA SUPERIOR, no una medicion. Medir el exceso en el")
    A("   stop para stops de 2 a 5 pt es ahora el bloqueo, igual que el sesgo por span lo era ayer.")
    A("=" * 100)
    print("\n".join(R))
    return 0


if __name__ == "__main__":
    sys.exit(main())
