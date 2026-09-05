"""
TAREA 3 - R7, LA REGLA DE CONSISTENCIA: que le exige a la DISTRIBUCION de resultados?

NO GASTA CARTUCHO. K = 261. Dinero: $0. Flujo SINTETICO sobre ES 1-min. La caja sellada no se toca.

R7, de help.tradeify.co leido 2026-09-05: ningun dia puede ser una fraccion demasiado grande de la
ganancia total. 40% en evaluacion Select, 35% en Growth, 20% en Lightning fondeada. Las comisiones NO
cuentan dentro de la ganancia a este efecto.

NADIE HABIA MIRADO ESTO, y toca el diseno: penaliza a una estrategia con pocas ganancias grandes y
favorece a una con muchas ganancias chicas y parejas. Puede matar candidatas que superan el piso.

LA ARITMETICA, primero, porque da la cota dura:
    si el mejor dia no puede pesar mas que c de la ganancia total, hacen falta AL MENOS 1/c dias
    ganadores, y ademas repartidos. Con c = 0,20 -> minimo 5 dias ganadores. Con c = 0,35 -> 3.
    Es una cota INFERIOR: 5 dias de ganancia identica dan exactamente 20% cada uno y quedan JUSTO
    en el limite. Cualquier desparejo lo rompe.

LO QUE SE MIDE: sobre intentos simulados que ALCANZAN el objetivo de $3.000, la distribucion de
   mejor_dia / ganancia_total, y que fraccion de esos intentos quedaria BLOQUEADA por cada cap.

LO QUE LA MATARIA como preocupacion: que casi todos los intentos que llegan al objetivo lo hagan con
muchos dias parejos, o sea que el cap no ate. Se calcula.
"""

import math
import os
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import juez as J  # noqa: E402
from aritmetica import C1_POR_MINI  # noqa: E402
from dolares_por_tiempo import MEDIA_EXCESO, PUNTO_ES, secuencial  # noqa: E402
from razon_escalas import cargar_con_sesion  # noqa: E402

CELDA = (5, 20)
MIN_BARRAS = 60
OBJETIVO = 3000.0
DD = 2000.0
CAPS = [("Lightning fondeada", 0.20), ("Growth", 0.35), ("Select eval", 0.40)]
N_MICROS = 10                    # 10 micro-equivalentes = 1 mini, el tamano barato (R5/R6)


def main():
    R = []
    A = R.append
    A("=" * 100)
    A("TAREA 3 - R7, LA REGLA DE CONSISTENCIA: que le exige a la distribucion de resultados")
    A("NO GASTA CARTUCHO. K = 261. Dinero: $0. La caja sellada no se toca.")
    A("=" * 100)

    A("")
    A("-" * 100)
    A("   (1) LA COTA DURA, que sale de la aritmetica y no necesita datos")
    A("-" * 100)
    A(f"   {'cuenta':>22}{'cap':>7}{'dias ganadores minimos':>26}{'si son parejos, c/u':>22}")
    for nom, c in CAPS:
        A(f"   {nom:>22}{c:>7.0%}{math.ceil(1/c):>26}{1/math.ceil(1/c):>22.0%}")
    A("")
    A("   Es una cota INFERIOR y ademas apretada: con el minimo de dias, todos tienen que dar")
    A("   EXACTAMENTE lo mismo. Cualquier desparejo obliga a mas dias.")
    A("   Y la condicion no es sobre el numero de dias sino sobre la FORMA: max_dia / suma_ganancias")
    A("   <= c. Un dia que sea el doble del promedio ya obliga a 2/c dias.")

    # ------------------------------------------------------------------ el flujo
    df = cargar_con_sesion()
    cl = df["close"].to_numpy(float); hi = df["high"].to_numpy(float); lo = df["low"].to_numpy(float)
    sess = df["sess"].to_numpy()
    corte = np.flatnonzero(sess[1:] != sess[:-1]) + 1
    ini = np.concatenate(([0], corte)); fin = np.concatenate((corte, [len(cl)]))
    keep = (fin - ini) >= MIN_BARRAS
    ini, fin = ini[keep], fin[keep]
    T, S = CELDA
    exc = MEDIA_EXCESO[S]
    vs = {}
    for lado in ("largo", "corto"):
        v, no, na = secuencial(cl, hi, lo, ini, fin, T, S, lado, exceso=exc, c1=C1_POR_MINI)
        vs[lado] = v
    n = len(vs["largo"])
    # PRIMERA VERSION, DESCARTADA Y DICHA: con el flujo SIN ventaja, CERO de 1.006 intentos llegan
    # al objetivo. Y eso ya es una respuesta parcial -a quien nunca cobra la regla de consistencia
    # no lo ata- pero no permite medir la distribucion, que era la pregunta.
    # LA POBLACION CORRECTA es la que la pregunta nombra: candidatas que SI superan el piso. Se
    # inyecta una ventaja direccional (se elige el lado bueno con probabilidad q) y se opera al
    # limite de la cuenta de 50K, 4 minis (R6), que es como se llegaria al objetivo de verdad.
    Q = 0.60
    CONTRATOS = 4
    rng = np.random.default_rng(20260906)
    elige_bien = rng.random(n) < Q
    dia = np.where(elige_bien, np.maximum(vs["largo"], vs["corto"]),
                   np.minimum(vs["largo"], vs["corto"])) * CONTRATOS
    A("")
    A("-" * 100)
    A(f"   (2) MEDIDO sobre intentos que ALCANZAN el objetivo de ${OBJETIVO:,.0f}")
    A("-" * 100)
    A(f"   PRIMERO, con el flujo SIN VENTAJA: CERO de {n:,} intentos llegan al objetivo. A quien")
    A(f"   nunca cobra, la regla de consistencia no lo ata. Por eso la poblacion correcta es otra.")
    A(f"   Flujo CON ventaja inyectada (q = {Q}, se elige el lado bueno el {Q:.0%} de las veces),")
    A(f"   {CONTRATOS} minis -el limite de la cuenta de 50K (R6)-, {n:,} sesiones, celda {T}pt:{S}pt.")
    A(f"   Un intento arranca en cada sesion y acumula hasta el objetivo o el drawdown de "
      f"${DD:,.0f}.")
    razones, largos = [], []
    for s0 in range(n):
        saldo = 0.0; pico = 0.0; dias = []
        for k in range(s0, n):
            saldo += dia[k]; dias.append(dia[k])
            pico = max(pico, saldo)
            if saldo <= min(pico - DD, 0.0):
                break
            if saldo >= OBJETIVO:
                pos = [d for d in dias if d > 0]
                if sum(pos) > 0:
                    razones.append(max(pos) / sum(pos)); largos.append(len(dias))
                break
    razones = np.array(razones); largos = np.array(largos)
    A(f"   intentos que llegan al objetivo: {len(razones):,} de {n:,} ({len(razones)/n:.1%})")
    if len(razones) < 20:
        A("   Muy pocos para decir nada de la distribucion. Se corta aca.")
        print("\n".join(R))
        return 0
    A(f"   dias hasta llegar: mediana {int(np.median(largos))}, p10 {int(np.percentile(largos,10))}, "
      f"p90 {int(np.percentile(largos,90))}")
    A("")
    A(f"   mejor_dia / suma de dias ganadores:")
    A(f"      mediana {np.median(razones):.1%}   p10 {np.percentile(razones,10):.1%}   "
      f"p90 {np.percentile(razones,90):.1%}   max {razones.max():.1%}")
    A("")
    A(f"   {'cuenta':>22}{'cap':>7}{'intentos BLOQUEADOS':>22}")
    for nom, c in CAPS:
        A(f"   {nom:>22}{c:>7.0%}{(razones > c).mean():>22.1%}")

    A("")
    A("=" * 100)
    A("   LO QUE ESTO DECIDE")
    A("=" * 100)
    bloq20 = (razones > 0.20).mean()
    A(f"   Con el cap del 20% (Lightning fondeada), {bloq20:.0%} de los intentos que LLEGAN al")
    A(f"   objetivo quedarian bloqueados para cobrar. Con 35%, {(razones>0.35).mean():.0%}.")
    A("")
    A("   Y ESTO NO ES UNA PENALIDAD SOBRE LA MALA SUERTE, ES SOBRE LA FORMA. La regla premia")
    A("   muchas ganancias chicas y parejas y castiga pocas grandes. Un candidato con la MISMA")
    A("   esperanza pero mas concentrado cobra menos veces.")
    A("")
    A("   LA CONDICION QUE EL JUEZ PUEDE VERIFICAR, y es una linea sobre lo que ya calcula:")
    A("      max(dias con ganancia) / suma(dias con ganancia)  <=  c")
    A("   calculada sobre las sesiones del candidato en el periodo. No necesita dato nuevo: el juez")
    A("   ya tiene v_obs, los dolares por sesion. Se puede reportar como una cifra mas del veredicto")
    A("   -'concentracion del mejor dia'- y compararla contra el cap de la cuenta declarada.")
    A("   NO LA IMPLEMENTO EN ESTA TANDA: agregar una cerradura mas al juez cambia los diez")
    A("   controles y ya cambie dos cosas hoy. Queda nombrada y medida.")
    A("")
    A("   Y EL MECANISMO ES LA VELOCIDAD, no la suerte: la mediana de dias hasta el objetivo es DOS.")
    A("   Con dos dias, el mejor dia pesa por construccion mas de la mitad. Cuanto MEJOR es el")
    A("   candidato y mas grande opera, mas rapido llega y MAS concentrado queda. La regla de")
    A("   consistencia y el tamano de contrato tiran en direcciones opuestas.")
    A("")
    A("   LA SALIDA QUE LA REGLA EMPUJA, y conecta con la tabla de frecuencia: operar MAS CHICO para")
    A("   estirar la ganancia en mas dias. Pero operar mas chico multiplica el costo por unidad de")
    A("   exposicion -el MES cuesta 2,0x mas por punto que el ES- y alarga el intento, que es")
    A("   exactamente lo que la Tarea 1 mostro que cobra caro. La regla de consistencia le pone un")
    A("   PISO al numero de dias y el costo le pone un TECHO. Nadie habia mirado que se cruzan.")
    A("")
    A("   MARCAS DE FRAGILIDAD, dos: (1) la ventaja inyectada (q = 0,60) es enorme y arbitraria; con")
    A("   una ventaja mas chica los intentos tardan mas y se concentran menos, asi que estos")
    A("   porcentajes son una COTA SUPERIOR. (2) El flujo promedia los dos lados por sesion y no")
    A("   modela el orden intradiario, asi que 'dia' es una unidad gruesa. Lo que NO es fragil es la")
    A("   aritmetica de la cota dura: con cap del 20% hacen falta 5 dias ganadores parejos, y eso no")
    A("   depende de ningun supuesto.")
    A("=" * 100)
    print("\n".join(R))
    return 0


if __name__ == "__main__":
    sys.exit(main())
