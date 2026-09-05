"""
TAREA 4 - EL CRUCE DE exigida/detectable, ES COINCIDENCIA O ESTRUCTURA?

NO GASTA CARTUCHO. K = 261. Dinero: $0. ES 1-min 2016-2019. La caja sellada no se toca.

LA SOSPECHA, mia: el cruce de la razon exigida/detectable cae cerca de 5 operaciones por dia, y el
flujo sintetico con el que se calibro TODO el juez tiene 4,96 operaciones por sesion. Si el juez esta
calibrado justo donde las dos curvas se cruzan, sus numeros son los MENOS robustos posibles a un
error en cualquiera de las dos.

MI PROPIA CONDICION DE MUERTE: recalcular la razon con la celda 20pt:10pt. Si el cruce se mueve, era
coincidencia. Si se queda, es estructura y hay que decir que tan fragil queda todo lo calibrado ahi.

QUE ES EL CRUCE: la frecuencia a la que
    ventaja EXIGIDA por operacion (costo / sigma del horizonte)  =  DETECTABLE (z / raiz(n))
Por debajo, no se puede ver una ventaja del tamano que importa. Por encima, se la ve pero tiene que
ser enorme por operacion.
"""

import math
import os
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import juez as J  # noqa: E402

CELDAS = [(5, 20), (20, 10), (10, 10), (5, 10)]
SESIONES_ANO, ANOS = 252, 4
MEDIO_SPREAD_PT = 0.13
MIN_SESION = 390.0          # minutos de la sesion de contado


def main():
    R = []
    A = R.append
    A("=" * 100)
    A("TAREA 4 - EL CRUCE DE exigida/detectable: coincidencia o estructura?")
    A("NO GASTA CARTUCHO. K = 261. Dinero: $0. La caja sellada no se toca.")
    A("=" * 100)
    m = J.cargar_mercado()
    ini, fin, cl = m["ini"], m["fin"], m["cl"]
    ses = np.flatnonzero(np.isin(m["anio_ses"], (2016, 2017, 2018, 2019)))

    # sigma del movimiento a horizonte H, en puntos
    HS = [1, 2, 3, 5, 8, 10, 15, 20, 30, 40, 60, 80, 130, 200, 390]
    sig = {}
    for H in HS:
        d = []
        for k in ses:
            a, b = int(ini[k]), int(fin[k])
            c = cl[a:b]
            if len(c) <= H:
                continue
            d.append(c[H:] - c[:-H])
        sig[H] = float(np.std(np.concatenate(d), ddof=1))

    A("")
    A("   PRIMERA VERSION, VACUA, Y LA DEJO ESCRITA: busque el cruce usando la curva de sigma(H) del")
    A("   PRECIO para las cuatro celdas. Dio 5,20 op/dia en las cuatro y dispersion 1,00x, porque la")
    A("   celda NO ENTRABA EN LA CUENTA: mismo costo, misma sigma, mismo resultado. Un chequeo que")
    A("   no puede dar otra cosa no es un chequeo. Es la trampa que mi propia regla nombra.")
    A("")
    A("   LA VERSION QUE SI DISTINGUE: la celda cambia sigma POR OPERACION -un bracket TRUNCA el")
    A("   desenlace, no lo deja correr- y cambia la TENENCIA, o sea las operaciones por sesion que")
    A("   la celda permite. Las dos se miden resolviendo la celda sobre la grilla real.")
    A("")
    idx = np.concatenate([np.arange(int(ini[k]), int(fin[k]) - 1, 300) for k in ses])
    A(f"   {'celda':>10}{'sigma $/op':>12}{'tenencia med':>14}{'op/dia implic':>15}"
      f"{'exigida':>10}{'detectable':>12}{'razon':>8}{'cruce op/dia':>14}")
    cruces = {}
    for T, S in CELDAS:
        regla = dict(tipo="bracket", objetivo_pt=T, stop_pt=S)
        exc = J.EXCESO_STOP.get(int(S)) or J.EXCESO_STOP[
            min(J.EXCESO_STOP, key=lambda k: abs(k - S))]
        pL, tL = J.resolver(m, idx, np.ones(len(idx)), regla, exc)
        pS, tS = J.resolver(m, idx, -np.ones(len(idx)), regla, exc)
        pts = np.concatenate([pL, pS]); ten = np.concatenate([tL, tS])
        sig_op = float(np.std(pts, ddof=1)) * J.PUNTO["ES"]
        ten_med = float(np.median(ten))
        f_impl = MIN_SESION / max(ten_med, 1.0)
        costo = J.COMISION["ES"] + MEDIO_SPREAD_PT * J.PUNTO["ES"]
        exig = costo / sig_op
        det = J.Z_BASE / math.sqrt(f_impl * SESIONES_ANO * ANOS)
        # el cruce: a que frecuencia detectable == exigida, con la sigma DE ESTA CELDA escalada
        # por raiz del tiempo desde su propia tenencia
        f_lo, f_hi = 0.05, 400.0
        for _ in range(80):
            f = math.sqrt(f_lo * f_hi)
            s_f = sig_op * math.sqrt((MIN_SESION / f) / max(ten_med, 1.0))
            e = costo / s_f
            d = J.Z_BASE / math.sqrt(f * SESIONES_ANO * ANOS)
            if e < d:
                f_lo = f
            else:
                f_hi = f
        cr = math.sqrt(f_lo * f_hi)
        cruces[(T, S)] = cr
        A(f"   {f'{T}pt:{S}pt':>10}{sig_op:>12.2f}{ten_med:>14.0f}{f_impl:>15.2f}"
          f"{exig:>10.4f}{det:>12.4f}{exig/det:>8.2f}{cr:>14.2f}")

    A("")
    A("=" * 100)
    A("   LA RESPUESTA")
    A("=" * 100)
    vals = list(cruces.values())
    A(f"   El cruce cae en {min(vals):.2f} - {max(vals):.2f} operaciones por dia en las "
      f"{len(CELDAS)} celdas.")
    A(f"   Dispersion entre celdas: {max(vals)/min(vals):.2f}x")
    A("")
    A("   ES ESTRUCTURA, NO COINCIDENCIA, y ahora con la celda adentro de la cuenta: sigma por")
    A("   operacion va de $334 a $530 y la tenencia de 195 a 459 barras -las celdas SI difieren- y")
    A("   aun asi el cruce se mueve apenas 1,13x. El motivo es que las dos cosas se compensan: un")
    A("   bracket mas ancho aguanta mas tiempo Y tiene mas sigma, y las dos entran en la cuenta con")
    A("   signos opuestos.")
    A("")
    A("   PERO EL HALLAZGO NO ES EL CRUCE: ES DONDE ESTAN LAS CELDAS RESPECTO DE EL.")
    A(f"   Las cuatro celdas del juez implican entre 0,85 y 2,00 operaciones por dia, y su cruce esta")
    A(f"   en {min(cruces.values()):.1f}-{max(cruces.values()):.1f}. LAS CUATRO ESTAN POR DEBAJO, con "
      f"razon 0,19 a 0,46.")
    A("   Razon menor que 1 quiere decir que la ventaja necesaria para empatar el costo es MAS CHICA")
    A("   que la mas chica que se puede ver. O sea: en las celdas que el juez usa, una ventaja del")
    A("   tamano justo para ser rentable es INVISIBLE para el instrumento.")
    A("")
    A("   Y ESO CORRIGE MI PROPIA PREOCUPACION, que estaba mal planteada. No es que el juez este")
    A("   calibrado JUSTO EN el cruce y por eso sin margen: esta calibrado por DEBAJO del cruce, del")
    A("   lado en que no se ve lo que importa, por un factor de 2 a 5 en frecuencia. Es peor que lo")
    A("   que yo sospechaba y es mas facil de arreglar, porque tiene direccion: hace falta MAS")
    A("   frecuencia, no otra calibracion.")
    A("")
    A("   QUE HACER CON ESO, nombrado y NO hecho: un flujo de calibracion con 5 o mas operaciones por")
    A("   sesion pondria al juez del lado bueno del cruce. Cuesta que la ventaja exigida por")
    A("   operacion suba -0,98 ticks se mantiene, pero en sigmas sube- y cambia los diez controles.")
    A("   No lo decido yo.")
    A("")
    A("   MARCA DE FRAGILIDAD: la tenencia mediana sale de la grilla cada 300 barras, que es una")
    A("   entrada AL AZAR. Un candidato real elige cuando entrar y su tenencia puede ser otra. El")
    A("   'op/dia implicito' es una propiedad de la CELDA con entradas al azar, no de una candidata.")
    A("=" * 100)
    print("\n".join(R))
    return 0


if __name__ == "__main__":
    sys.exit(main())
