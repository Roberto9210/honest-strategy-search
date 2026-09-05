"""
TAREA 1 - LA TABLA DE FRECUENCIA CON EL COSTO ADENTRO, y con el escalado del movimiento MEDIDO.

NO GASTA CARTUCHO. K = 261. Dinero: $0. ES 1-min 2016-2019. La caja sellada no se toca.

LO QUE CORRIGE. La tanda pasada concluí que "subir la frecuencia solo ayuda". Esa conclusion tenia
adentro un supuesto que no verifique: que sigma POR OPERACION no cambia al acortar el horizonte. Si
el movimiento escala con raiz del tiempo, sigma por operacion SI se achica al acortar, el costo por
operacion NO, y entonces la ventaja EXIGIDA por operacion crece. Es exactamente la pregunta que hay
que medir y no suponer.

QUE SE MIDE, sobre el ES 1-min 2016-2019: el desvio del retorno a horizonte H, para H de 1 a 390
minutos, en dolares por contrato. De ahi salen las dos curvas que deciden:
    ventaja EXIGIDA por operacion (para cubrir el costo)  =  costo_ida_y_vuelta / sigma(H)
    ventaja DETECTABLE por operacion (con los datos que hay) =  z / raiz(n operaciones)

COSTOS, de help.tradeify.co leidos 2026-09-05 (R5), ida y vuelta todo incluido por contrato:
    ES $5,76   MES $1,82.  Mas el medio-spread de entrada medido: 0,13 pt.
Y el aviso de la propia firma: 10 micros cuestan $18,20 contra $5,76 de un mini.

LO QUE LA MATARIA a la direccion de alta frecuencia: que la ventaja exigida por operacion crezca mas
rapido, al acortar, que la detectabilidad que se gana. Se calcula, no se asume.
"""

import math
import os
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import juez as J  # noqa: E402

HORIZONTES = [1, 2, 5, 10, 20, 30, 60, 120, 390]
FRECUENCIAS = [1, 5, 10, 20, 40]
N_OBJETIVO = {0.10: None, 0.05: None}          # se llenan con z/e al cuadrado
SESIONES_ANO = 252
ANOS = 4
# R5, help.tradeify.co 2026-09-05: ida y vuelta todo incluido por contrato
COMISION = {"ES": 5.76, "MES": 1.82}
PUNTO = {"ES": 50.0, "MES": 5.0}
TICK_PT = 0.25
MEDIO_SPREAD_PT = 0.13                          # microestructura_tbbo.py


def main():
    R = []
    A = R.append
    A("=" * 100)
    A("TAREA 1 - FRECUENCIA CON EL COSTO ADENTRO, y el escalado del movimiento MEDIDO")
    A("NO GASTA CARTUCHO. K = 261. Dinero: $0. La caja sellada no se toca.")
    A("=" * 100)
    m = J.cargar_mercado()
    ini, fin, cl = m["ini"], m["fin"], m["cl"]
    ses = np.flatnonzero(np.isin(m["anio_ses"], (2016, 2017, 2018, 2019)))
    A(f"\n   {len(ses):,} sesiones de ES 1-min. Costos R5: ES ${COMISION['ES']:.2f}, "
      f"MES ${COMISION['MES']:.2f} ida y vuelta; medio-spread {MEDIO_SPREAD_PT} pt.")

    # ---------------------------------------------------------------- el escalado, medido
    A("")
    A("-" * 100)
    A("   (0) COMO ESCALA EL MOVIMIENTO CON EL HORIZONTE. Es lo que decide todo lo demas.")
    A("-" * 100)
    sig_pt = {}
    for H in HORIZONTES:
        d = []
        for k in ses:
            a, b = int(ini[k]), int(fin[k])
            c = cl[a:b]
            if len(c) <= H:
                continue
            d.append(c[H:] - c[:-H])
        v = np.concatenate(d)
        sig_pt[H] = float(np.std(v, ddof=1))
    s1 = sig_pt[1]
    A(f"   {'H (min)':>9}{'sigma (pt)':>13}{'sigma ($ ES)':>14}{'sigma/sigma(1)':>17}"
      f"{'raiz(H)':>10}{'exponente':>11}")
    for H in HORIZONTES:
        r = sig_pt[H] / s1
        expo = math.log(r) / math.log(H) if H > 1 else float("nan")
        A(f"   {H:>9}{sig_pt[H]:>13.3f}{sig_pt[H]*PUNTO['ES']:>14.2f}{r:>17.2f}"
          f"{math.sqrt(H):>10.2f}{expo:>11.3f}")
    expos = [math.log(sig_pt[H] / s1) / math.log(H) for H in HORIZONTES if H > 1]
    expo_med = float(np.mean(expos))
    A("")
    A(f"   EXPONENTE MEDIO: {expo_med:.3f}   (raiz del tiempo puro seria 0,500)")
    if abs(expo_med - 0.5) < 0.04:
        A(f"   El movimiento escala practicamente con RAIZ DEL TIEMPO. Entonces sigma por operacion")
        A(f"   SI se achica al acortar el horizonte, y el costo por operacion NO. Mi conclusion de la")
        A(f"   tanda pasada -'subir la frecuencia solo ayuda'- tenia ese supuesto adentro y ERA FALSO.")
    else:
        A(f"   NO escala con raiz del tiempo: el exponente medio es {expo_med:.3f}.")

    # ---------------------------------------------------------------- la tabla que se pidio
    for inst in ("ES", "MES"):
        costo = COMISION[inst] + MEDIO_SPREAD_PT * PUNTO[inst]
        A("")
        A("-" * 100)
        A(f"   {inst}: costo ida y vuelta ${costo:.2f} (comision ${COMISION[inst]:.2f} + medio-spread "
          f"${MEDIO_SPREAD_PT*PUNTO[inst]:.2f})")
        A("-" * 100)
        A(f"   {'op/dia':>8}{'H (min)':>9}{'ses p/1262':>12}{'ses p/5047':>12}{'costo $/ses':>13}"
          f"{'vent exigida':>14}{'en ticks':>10}{'en sigmas':>11}{'detectable':>12}{'razon':>8}")
        base = None
        for f in FRECUENCIAS:
            # horizonte implicito: la sesion RTH de 390 min repartida en f operaciones
            H = max(1, int(round(390 / f)))
            Hs = min(HORIZONTES, key=lambda x: abs(x - H))
            sig_d = sig_pt[Hs] * PUNTO[inst]
            vent_d = costo                       # $ por operacion para empatar
            vent_tk = vent_d / (TICK_PT * PUNTO[inst])
            vent_sig = vent_d / sig_d
            n4 = f * SESIONES_ANO * ANOS
            det = J.Z_BASE / math.sqrt(n4)
            if base is None:
                base = (vent_d, vent_sig, det)
            A(f"   {f:>8}{Hs:>9}{1262/f:>12,.0f}{5047/f:>12,.0f}{f*costo:>13,.2f}"
              f"{vent_d:>14.2f}{vent_tk:>10.2f}{vent_sig:>11.3f}{det:>12.3f}"
              f"{vent_sig/det:>8.1f}")
        A("")
        A(f"   'vent exigida' = $ por operacion para empatar el costo. Es el MISMO numero a toda")
        A(f"   frecuencia (${costo:.2f}): el costo no depende de cuanto dura la operacion.")
        A(f"   'en sigmas' = ese costo dividido por el movimiento tipico del horizonte. ESE si crece")
        A(f"   al acortar, porque el movimiento se achica y el costo no.")
        A(f"   'razon' = exigida / detectable. Mayor que 1 significa que la ventaja que hace falta")
        A(f"   para ganar plata es MAS GRANDE que la mas chica que se puede ver: se puede medir, pero")
        A(f"   hay que tener una ventaja grande. Menor que 1 es lo contrario.")

    # ---------------------------------------------------------------- la respuesta
    A("")
    A("=" * 100)
    A("   LA RESPUESTA A LA PREGUNTA DE LA TABLA")
    A("=" * 100)
    costo_es = COMISION["ES"] + MEDIO_SPREAD_PT * PUNTO["ES"]
    for f in (1, 40):
        H = max(1, int(round(390 / f)))
        Hs = min(HORIZONTES, key=lambda x: abs(x - H))
        vs = costo_es / (sig_pt[Hs] * PUNTO["ES"])
        det = J.Z_BASE / math.sqrt(f * SESIONES_ANO * ANOS)
        A(f"   {f:>3} op/dia (H~{Hs:>3} min): exigida {vs:.3f} sigmas, detectable {det:.3f}, "
          f"razon {vs/det:.1f}")
    v1 = costo_es / (sig_pt[min(HORIZONTES, key=lambda x: abs(x - 390))] * PUNTO["ES"])
    v40 = costo_es / (sig_pt[min(HORIZONTES, key=lambda x: abs(x - 10))] * PUNTO["ES"])
    d1 = J.Z_BASE / math.sqrt(1 * SESIONES_ANO * ANOS)
    d40 = J.Z_BASE / math.sqrt(40 * SESIONES_ANO * ANOS)
    A("")
    A(f"   Al pasar de 1 a 40 operaciones por dia:")
    A(f"      la ventaja EXIGIDA por operacion sube  {v40/v1:.1f}x  ({v1:.3f} -> {v40:.3f} sigmas)")
    A(f"      la DETECTABILIDAD mejora               {d1/d40:.1f}x  ({d1:.3f} -> {d40:.3f} sigmas)")
    A(f"      la razon exigida/detectable            {(v40/d40)/(v1/d1):.1f}x")
    if (v40 / d40) > (v1 / d1):
        A("")
        A("   LA EXIGIDA SUBE MAS RAPIDO QUE LO QUE SE GANA EN DETECTABILIDAD. Subir la frecuencia")
        A("   NO es gratis: mejora la resolucion pero empeora la economia mas rapido. Mi conclusion")
        A("   de la tanda pasada estaba mal, y estaba mal por el supuesto que no habia verificado.")
    else:
        A("")
        A("   La exigida sube mas lento que la detectabilidad: subir la frecuencia sigue conviniendo.")
    A("")
    A("   POR QUE, en una linea: el costo por operacion es FIJO en dolares, y el movimiento del que")
    A("   hay que sacarlo se achica con raiz del tiempo. Acortar el horizonte a la mitad deja el")
    A("   costo igual y achica el movimiento 1,41 veces.")

    # ---------------------------------------------------------------- ES contra MES
    A("")
    A("-" * 100)
    A("   Y EL MICRO ES PEOR QUE EL MINI, con el numero de la propia firma")
    A("-" * 100)
    ce, cm = COMISION["ES"] + MEDIO_SPREAD_PT * 50, COMISION["MES"] + MEDIO_SPREAD_PT * 5
    A(f"   costo por contrato: ES ${ce:.2f}   MES ${cm:.2f}")
    A(f"   costo POR UNIDAD DE EXPOSICION (dividido por el valor del punto): "
      f"ES ${ce/50:.4f}/pt   MES ${cm/5:.4f}/pt")
    A(f"   El MES cuesta {(cm/5)/(ce/50):.2f}x mas por unidad de exposicion.")
    A(f"   Y NO coincide con el 3,2x del aviso de la propia Tradeify (10 micros $18,20 contra $5,76")
    A(f"   de un mini), asi que hay que decir por que: el 3,2x es SOLO comision. Al sumar el")
    A(f"   medio-spread -que SI escala con el valor del punto- el castigo se diluye de 3,16x a")
    A(f"   {(cm/5)/(ce/50):.2f}x. El aviso de la firma exagera el castigo porque mira su propia factura,")
    A(f"   no el costo total de operar.")
    A(f"   CONSECUENCIA: toda la tabla de arriba es PEOR en MES por ese factor. Operar chico para")
    A(f"   arriesgar menos cuesta ventaja exigida.")
    A("=" * 100)
    print("\n".join(R))
    return 0


if __name__ == "__main__":
    sys.exit(main())
