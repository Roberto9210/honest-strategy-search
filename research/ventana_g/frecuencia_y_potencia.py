"""
TAREA 2 - LA FRECUENCIA. Que FORMA tiene que tener una candidata para que valga la pena pensarla.

NO GASTA CARTUCHO. K = 261. Dinero: $0. Es aritmetica sobre numeros ya medidos.

DE DONDE SALE. El barrido de potencia dio que hacen falta 315 operaciones para ver un efecto de 0,20
desvios por operacion, 1.262 para 0,10 y 5.047 para 0,05. Eso NO es un requisito de anos: es de
OPERACIONES. Traducirlo a frecuencia dice que forma tiene que tener una candidata.

Y LA CONTRA, que hay que calcular en la misma tabla: el costo por operacion es FIJO, asi que operar
20 veces por dia multiplica el costo por 20. Si la ventaja por operacion necesaria para cubrir el
costo crece mas rapido que la detectabilidad, la salida se cierra sola.

LO QUE LA MATARIA: que a alta frecuencia el piso de costos suba tanto que la ventaja necesaria crezca
mas rapido que la potencia ganada.
"""

import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import juez as J  # noqa: E402

# SIGMA POR OPERACION. PRIMERA VERSION MAL, Y LA DEJO ESCRITA PORQUE ES EL MISMO ERROR DE SIEMPRE:
# use los $28,11 del control C1 como si fueran el desvio de UNA SESION. No lo son: son sd_tot, el
# desvio de la MEDIA por sesion del reparto de permutacion sobre 758 sesiones. Dividirlo por
# raiz(op/sesion) daba $12,62 y una "ventaja necesaria" de 0,97 desvios por operacion, que es
# absurda. Es otra vez no mirar donde se consume el numero.
# EL BUENO: el desvio del TOTAL de una sesion, medido en calibrar_por_regimen.py sobre el mismo
# flujo sintetico (grilla de 300 barras, un lado al azar, 5pt:20pt, 1 ES, 2016-2019): $972,47 por
# sesion con 4,96 operaciones por sesion.
SD_SESION_TOTAL, OP_SES_REF = 972.47, 4.96
SIGMA_OP = SD_SESION_TOTAL / math.sqrt(OP_SES_REF)        # $ por operacion
SESIONES_ANO = 252
FRECUENCIAS = [("1 por mes", 12 / 252), ("1 por semana", 1 / 5), ("1 por dia", 1.0),
               ("5 por dia", 5.0), ("20 por dia", 20.0)]
EFECTOS = [0.20, 0.10, 0.05]
# costo por operacion, ida y vuelta, a 1 mini: comision + medio-spread de entrada
COSTO_OP = J.COMISION["ES"] + 0.13 * J.PUNTO["ES"]
ANOS_QUE_TENEMOS = 4


def main():
    R = []
    A = R.append
    A("=" * 100)
    A("TAREA 2 - FRECUENCIA, POTENCIA Y COSTO: que forma tiene que tener una candidata")
    A("NO GASTA CARTUCHO. K = 261. Dinero: $0.")
    A("=" * 100)
    A(f"\n   sigma por operacion: ${SIGMA_OP:.2f}   (desvio del TOTAL de una sesion "
      f"${SD_SESION_TOTAL:.2f} con {OP_SES_REF} op/sesion, calibrar_por_regimen.py)")
    A(f"   vara del juez (nueva): z = {J.Z_BASE:.3f}   costo por operacion (1 mini, ida y vuelta "
      f"con medio-spread): ${COSTO_OP:.2f}")
    A(f"   MARCA DE FRAGILIDAD: sigma_op sale de UNA celda (5pt:20pt) del ES. Otras reglas de salida")
    A(f"   dan otro sigma. Es una vara comun, no la de cada candidata.")

    A("")
    A("-" * 100)
    A("   (1) OPERACIONES POR ANO Y ANOS NECESARIOS")
    A("-" * 100)
    n_nec = {e: (J.Z_BASE / e) ** 2 for e in EFECTOS}
    A(f"   operaciones necesarias: " + "   ".join(f"efecto {e:.2f} -> {n_nec[e]:,.0f}"
                                                  for e in EFECTOS))
    A("")
    A(f"   {'frecuencia':>14}{'op/ano':>10}" + "".join(f"{'anos p/' + f'{e:.2f}':>14}"
                                                       for e in EFECTOS))
    for nom, por_ses in FRECUENCIAS:
        opa = por_ses * SESIONES_ANO
        cel = "".join(f"{n_nec[e]/opa:>14,.1f}" for e in EFECTOS)
        A(f"   {nom:>14}{opa:>10,.0f}{cel}")

    A("")
    A("-" * 100)
    A(f"   (2) EL CRUCE: que es medible con los {ANOS_QUE_TENEMOS} anos que YA TENEMOS (2016-2019)")
    A("-" * 100)
    A(f"   {'frecuencia':>14}{'op en 4 anos':>14}" + "".join(f"{'efecto ' + f'{e:.2f}':>14}"
                                                             for e in EFECTOS))
    for nom, por_ses in FRECUENCIAS:
        op4 = por_ses * SESIONES_ANO * ANOS_QUE_TENEMOS
        cel = "".join(f"{'SI' if op4 >= n_nec[e] else 'no':>14}" for e in EFECTOS)
        A(f"   {nom:>14}{op4:>14,.0f}{cel}")
    # frecuencia minima para cada efecto con 4 anos
    A("")
    for e in EFECTOS:
        f_min = n_nec[e] / (SESIONES_ANO * ANOS_QUE_TENEMOS)
        A(f"   Para un efecto de {e:.2f} desvios/op hacen falta {f_min:.2f} operaciones por SESION "
          f"con los 4 anos que hay.")

    A("")
    A("-" * 100)
    A("   (3) LA CONTRA: el costo por operacion es FIJO, asi que la frecuencia lo multiplica")
    A("-" * 100)
    A("   'ventaja necesaria' = la que hace que el candidato quede en cero despues del costo, en")
    A("   desvios por operacion. Es costo_op / sigma_op y NO depende de la frecuencia.")
    ve_nec = COSTO_OP / SIGMA_OP
    A(f"   costo por operacion ${COSTO_OP:.2f} / sigma ${SIGMA_OP:.2f} = "
      f"{ve_nec:.3f} desvios por operacion, SIEMPRE.")
    A("")
    A(f"   {'frecuencia':>14}{'op/ano':>10}{'costo $/ano':>14}{'detectable en 4 anos':>22}"
      f"{'alcanza p/ el costo?':>22}")
    for nom, por_ses in FRECUENCIAS:
        opa = por_ses * SESIONES_ANO
        op4 = opa * ANOS_QUE_TENEMOS
        det = J.Z_BASE / math.sqrt(op4) if op4 > 0 else float("inf")
        A(f"   {nom:>14}{opa:>10,.0f}{opa*COSTO_OP:>14,.0f}{det:>22.3f}"
          f"{('SI' if det <= ve_nec else 'no'):>22}")

    A("")
    A("=" * 100)
    A("   LO QUE ESTO DECIDE")
    A("=" * 100)
    A(f"   LA CONTRA NO CIERRA LA SALIDA, y el motivo es que las dos cosas escalan distinto:")
    A(f"     - la ventaja NECESARIA para cubrir el costo es {ve_nec:.3f} desvios por operacion y NO")
    A(f"       depende de la frecuencia: el costo y la ventaja se multiplican por el mismo numero de")
    A(f"       operaciones. Operar 20 veces por dia multiplica el costo por 20 y tambien multiplica")
    A(f"       la ventaja bruta por 20.")
    A(f"     - la DETECTABILIDAD mejora con raiz(n), o sea que baja con la frecuencia.")
    A(f"   Entonces subir la frecuencia SOLO ayuda: acerca la detectabilidad a un umbral que se queda")
    A(f"   quieto. Mi propia condicion de muerte para esta tarea era que la ventaja necesaria")
    A(f"   creciera mas rapido que la potencia ganada, y NO crece: es plana.")
    A("")
    det20 = J.Z_BASE / math.sqrt(20 * SESIONES_ANO * ANOS_QUE_TENEMOS)
    A(f"   Y EL CRUCE ES EL NUMERO QUE MANDA: la ventaja necesaria para empatar el costo es")
    A(f"   {ve_nec:.3f} desvios por operacion, y la detectabilidad con 4 anos recien baja de ese")
    A(f"   umbral a 20 operaciones por dia ({det20:.3f}). A 5 por dia da 0,050: casi el DOBLE del")
    A(f"   umbral de costo, o sea que una ventaja del tamano justo para empatar el costo NO se puede")
    A(f"   distinguir de cero. La frecuencia minima para que el instrumento vea una ventaja del")
    A(f"   tamano que importa esta entre 5 y 20 operaciones por dia, con los 4 anos que hay.")
    A(f"   Esa es la respuesta con numero: una candidata tiene que operar del orden de VEINTE veces")
    A(f"   por dia para que valga la pena medirla, no una vez por dia y mucho menos una por mes.")
    A("")
    A(f"   LA FORMA DE UNA CANDIDATA QUE VALE LA PENA PENSAR, con los datos que hay:")
    A(f"     - al menos {n_nec[0.10]/(SESIONES_ANO*ANOS_QUE_TENEMOS):.1f} operaciones por sesion si")
    A(f"       se busca un efecto de 0,10 desvios; {n_nec[0.05]/(SESIONES_ANO*ANOS_QUE_TENEMOS):.1f}")
    A(f"       si se busca 0,05.")
    A(f"     - una candidata de 1 por MES esta descartada de entrada: 48 operaciones en 4 anos, y")
    A(f"       hacen falta {n_nec[0.20]:,.0f} para el efecto mas grande de la tabla.")
    A(f"     - y con cualquier frecuencia, tiene que ganar mas de {ve_nec:.2f} desvios por operacion")
    A(f"       o no cubre el costo. Ese numero no lo mejora la frecuencia ni el tamano de la muestra.")
    A("=" * 100)
    print("\n".join(R))
    return 0


if __name__ == "__main__":
    sys.exit(main())
