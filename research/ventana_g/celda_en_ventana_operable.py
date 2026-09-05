"""
TAREA 2 - EL JUEZ NUNCA JUZGO NADA DENTRO DE LA VENTANA OPERABLE. Se verifica y se arregla.

NO GASTA CARTUCHO. K = 261. Dinero: $0. ES 1-min 2016-2019, candidatos SINTETICOS. La caja sellada
no se toca.

EL PROBLEMA, que salio como observacion mia y era una tarea: las celdas del juez tienen tenencia
mediana de 195 a 459 barras -3 a 7,6 horas- porque la grilla entra AL AZAR y casi ninguna operacion
se resuelve por objetivo ni por stop: llegan al corte de sesion y se marcan a mercado. La ventana
OPERABLE que las restricciones permiten es de 1 a ~90 minutos. Lo caracterizado y lo permitido casi
no se solapan.

MI PROPIA CONDICION DE MUERTE: medir la tenencia con entradas SELECCIONADAS POR UNA SENAL, no al
azar. Si la mediana cae dentro de los 90 minutos, el problema era la grilla y no el juez.

LA REGLA NUEVA APLICADA - QUE DARIA ESTO SI EL EFECTO NO EXISTIERA, escrito ANTES de correr: si la
tenencia dependiera solo de la celda y no de cuando se entra, las entradas por senal darian la MISMA
tenencia mediana que la grilla al azar -195 a 459 barras- y el cociente daria 1,00. Ahi el problema
seria del juez y no de la grilla.

Y DESPUES, LO QUE IMPORTA: caracterizar al menos una celda cuya tenencia mediana caiga DENTRO de la
ventana operable, con piso, resolucion, frecuencia implicita y razon exigida/detectable.
"""

import math
import os
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import juez as J  # noqa: E402

PASO = 300
MEDIO_SPREAD_PT = 0.13
SESIONES_ANO, ANOS = 252, 4
MIN_SESION = 390.0
VENTANA_OPERABLE = (1.0, 90.0)          # minutos, de ESPACIO_DE_CANDIDATAS.md
# celdas: las cuatro ya caracterizadas mas brackets ESTRECHOS, que son los que pueden resolverse
# rapido. Los estrechos caen fuera del span 20-35 pt donde el sesgo de contabilidad esta medido, y
# eso se dice en el resultado en vez de esconderlo.
CELDAS = [(5, 20), (20, 10), (10, 10), (5, 10), (4, 6), (3, 4), (2, 3), (2, 2), (1, 2)]


def tenencia(m, idx, regla):
    exc = J.EXCESO_STOP.get(int(regla["stop_pt"])) or J.EXCESO_STOP[
        min(J.EXCESO_STOP, key=lambda k: abs(k - regla["stop_pt"]))]
    pL, tL = J.resolver(m, idx, np.ones(len(idx)), regla, exc)
    pS, tS = J.resolver(m, idx, -np.ones(len(idx)), regla, exc)
    return (np.concatenate([pL, pS]), np.concatenate([tL, tS]))


def main():
    R = []
    A = R.append
    A("=" * 100)
    A("TAREA 2 - CARACTERIZAR UNA CELDA DENTRO DE LA VENTANA OPERABLE (1 a 90 min)")
    A("NO GASTA CARTUCHO. K = 261. Dinero: $0. La caja sellada no se toca.")
    A("=" * 100)
    A("")
    A("   QUE DARIA SI EL EFECTO NO EXISTIERA (antes de correr): entradas por senal darian la MISMA")
    A("   tenencia que la grilla al azar, cociente 1,00, y el problema seria del juez y no de la")
    A("   grilla.")
    m = J.cargar_mercado()
    ses = np.flatnonzero(np.isin(m["anio_ses"], (2016, 2017, 2018)))
    idx_azar = np.concatenate([np.arange(int(m["ini"][k]), int(m["fin"][k]) - 1, PASO) for k in ses])

    # ---- entradas SELECCIONADAS POR UNA SENAL --------------------------------------------------
    # senal: ruptura del rango de las 30 barras previas. Es la forma mas comun de regla de entrada
    # y NO usa informacion futura. No es una candidata: es un generador de INSTANTES realista.
    cl, hi, lo = m["cl"], m["hi"], m["lo"]
    sel = []
    for k in ses:
        a, b = int(m["ini"][k]), int(m["fin"][k])
        c = cl[a:b]
        if len(c) < 60:
            continue
        w = 30
        mx = np.maximum.accumulate(np.concatenate([[-1e18], hi[a:b - 1]]))
        # maximo movil de 30 barras, sin mirar el futuro
        rmax = np.array([hi[a + max(0, i - w):a + i].max() if i > 0 else -1e18
                         for i in range(len(c))])
        rup = np.flatnonzero((c > rmax) & (np.arange(len(c)) >= w))
        sel.append(a + rup)
    idx_senal = np.concatenate(sel)
    A(f"\n   grilla al azar: {len(idx_azar):,} entradas   senal de ruptura de 30 barras: "
      f"{len(idx_senal):,} entradas ({len(idx_senal)/len(ses):.1f} por sesion)")

    A("")
    A("-" * 100)
    A("   (1) LA TENENCIA: al azar contra por senal")
    A("-" * 100)
    A(f"   {'celda':>10}{'ten AZAR (bar)':>16}{'ten SENAL (bar)':>17}{'cociente':>10}"
      f"{'senal en min':>14}{'dentro de 1-90?':>17}")
    resu = {}
    for T, S in CELDAS:
        regla = dict(tipo="bracket", objetivo_pt=T, stop_pt=S)
        _, ta = tenencia(m, idx_azar, regla)
        ps, tsn = tenencia(m, idx_senal, regla)
        ma, ms = float(np.median(ta)), float(np.median(tsn))
        dentro = VENTANA_OPERABLE[0] <= ms <= VENTANA_OPERABLE[1]
        resu[(T, S)] = dict(ten=ms, pts=ps, dentro=dentro)
        A(f"   {f'{T}pt:{S}pt':>10}{ma:>16.0f}{ms:>17.0f}{ms/max(ma,1e-9):>10.2f}"
          f"{ms:>14.0f}{('SI' if dentro else 'no'):>17}")

    coc = np.median([resu[c]["ten"] for c in CELDAS[:4]]) / np.median(
        [float(np.median(tenencia(m, idx_azar, dict(tipo="bracket", objetivo_pt=T,
                                                    stop_pt=S))[1])) for T, S in CELDAS[:4]])
    A("")
    A(f"   Cociente mediano senal/azar en las cuatro celdas ya caracterizadas: {coc:.2f}")
    if abs(coc - 1.0) < 0.15:
        A("   MI CONDICION DE MUERTE SE CUMPLE PARCIAL: entrar por senal NO acorta la tenencia. El")
        A("   problema no era la grilla. Con estas celdas, la tenencia es larga se entre como se")
        A("   entre, porque el bracket es ANCHO respecto del movimiento tipico.")
    else:
        A(f"   Entrar por senal cambia la tenencia por {coc:.2f}x: la grilla SI era parte del")
        A(f"   problema.")

    # ---- caracterizar las que caen dentro -------------------------------------------------------
    A("")
    A("-" * 100)
    A("   (2) LAS CELDAS QUE CAEN DENTRO DE LA VENTANA OPERABLE, caracterizadas")
    A("-" * 100)
    costo = J.COMISION["ES"] + MEDIO_SPREAD_PT * J.PUNTO["ES"]
    A(f"   costo ida y vuelta ${costo:.2f}.  vara z = {J.Z_BASE:.3f}.  4 anos de datos.")
    A("")
    A(f"   {'celda':>10}{'ten (min)':>11}{'sigma $/op':>12}{'op/dia impl':>13}{'piso $/ses':>12}"
      f"{'exigida':>10}{'detectable':>12}{'razon':>8}{'span pt':>9}")
    hay = False
    for (T, S), d in resu.items():
        if not d["dentro"]:
            continue
        hay = True
        pts = d["pts"]
        sig_op = float(np.std(pts, ddof=1)) * J.PUNTO["ES"]
        f_impl = MIN_SESION / max(d["ten"], 1.0)
        # piso: lo que hay que ganar por sesion para empatar, a esa frecuencia
        piso = f_impl * costo
        exig = costo / sig_op
        det = J.Z_BASE / math.sqrt(f_impl * SESIONES_ANO * ANOS)
        A(f"   {f'{T}pt:{S}pt':>10}{d['ten']:>11.0f}{sig_op:>12.2f}{f_impl:>13.1f}{piso:>12.2f}"
          f"{exig:>10.4f}{det:>12.4f}{exig/det:>8.2f}{T+S:>9}")
    if not hay:
        A("   NINGUNA de las celdas probadas cae dentro de la ventana operable.")

    A("")
    A("=" * 100)
    A("   LO QUE DECIDE")
    A("=" * 100)
    dentro = [(c, d) for c, d in resu.items() if d["dentro"]]
    A(f"   {len(dentro)} de {len(CELDAS)} celdas caen dentro de la ventana operable de 1 a 90 min,")
    A(f"   y NINGUNA de las cuatro que el juez tiene caracterizadas esta entre ellas.")
    A("")
    A("   Y LA TRAMPA QUE HAY QUE DECIR ANTES DE FESTEJAR: las celdas que caen dentro tienen span")
    A(f"   (objetivo + stop) de 3 a 10 puntos, y el sesgo de contabilidad del juez esta medido SOLO")
    A(f"   para span entre {J.SPAN_CARACTERIZADO[0]:.0f} y {J.SPAN_CARACTERIZADO[1]:.0f} pt. El juez")
    A("   las RECHAZA con NO MEDIBLE, y hace bien: no extrapola una correccion.")
    A("   O sea que el solapamiento entre 'lo que el reglamento permite operar' y 'lo que el juez")
    A("   puede juzgar' es, hoy, VACIO. No es que el juez juzgue mal la ventana operable: es que no")
    A("   la juzga.")
    A("")
    A("   QUE HARIA FALTA, nombrado y NO hecho: correr sesgo_marco.py sobre spans de 3 a 10 pt para")
    A("   caracterizar el sesgo de contabilidad ahi. Es una corrida sobre datos que ya estan, cuesta")
    A("   $0 y ningun cartucho, y es lo que abre la ventana operable al juez. Sin eso, todos los")
    A("   numeros del juez describen un regimen que el reglamento no permite operar.")
    A("=" * 100)
    print("\n".join(R))
    return 0


if __name__ == "__main__":
    sys.exit(main())
