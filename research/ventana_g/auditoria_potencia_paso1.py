"""
TAREA 1, PASO 1 - EL ARCHIVO SOPORTA LA PREGUNTA DE POTENCIA?

NO GASTA CARTUCHO. K = 261. Dinero: $0. Es lectura del ledger, no medicion de mercado.

LA PREGUNTA QUE SE QUIERE CONTESTAR (Tarea 1): cuantas de las 261 tenian POTENCIA para detectar lo
que afirmaban? Si casi ninguna la tenia, 272 negativos no son un resultado sobre el mercado sino
sobre el instrumento.

LO QUE HACE FALTA POR FILA: algo que haga de MAGNITUD AFIRMADA y algo que haga de RESOLUCION del
test. Este script NO contesta la pregunta: contesta si se puede contestar, y con que.

NO SE RECONSTRUYE NINGUNA TAXONOMIA A OJO. Se listan las columnas que hay, con cuantas filas las
tienen y que contienen, y se dice derecho.
"""

import json
import os
import sys
from collections import Counter

AQUI = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(os.path.dirname(os.path.dirname(AQUI)), "factory", "experiments_ledger.jsonl")

CANDIDATAS_MAGNITUD = ["prediccion", "stat", "linea_decision_t", "linea_decision_p",
                       "linea_suerte_p", "alpha", "h", "estrato_h", "medibilidad_config",
                       "robustness_cells", "margen_nocturno_mes", "margen_vigente"]


def main():
    R = []
    A = R.append
    A("=" * 100)
    A("TAREA 1, PASO 1 - EL LEDGER SOPORTA LA AUDITORIA DE POTENCIA?")
    A("NO GASTA CARTUCHO. K = 261. Dinero: $0.")
    A("=" * 100)
    if not os.path.exists(LEDGER):
        A(f"   NO EXISTE {LEDGER}. La pregunta no se puede ni plantear.")
        print("\n".join(R))
        return 1
    filas = [json.loads(l) for l in open(LEDGER, encoding="utf-8") if l.strip()]
    A(f"\n   {LEDGER}")
    A(f"   {len(filas)} filas. K acumulado declarado en el ledger: "
      f"{max([f.get('K_acumulado') or f.get('K_total') or 0 for f in filas if isinstance(f.get('K_acumulado') or f.get('K_total'), (int, float))], default='?')}")

    A("")
    A("-" * 100)
    A("   LAS COLUMNAS QUE PODRIAN SERVIR, con cuantas filas las tienen y que contienen")
    A("-" * 100)
    A(f"   {'columna':>22}{'filas':>7}   ejemplos (hasta 3, truncados)")
    for c in CANDIDATAS_MAGNITUD:
        v = [f[c] for f in filas if c in f]
        if not v:
            A(f"   {c:>22}{0:>7}   -")
            continue
        ej = "  |  ".join(str(x)[:44] for x in v[:3])
        A(f"   {c:>22}{len(v):>7}   {ej}")

    A("")
    A("-" * 100)
    A("   LO QUE HAY EN result, que es lo unico presente en cantidad")
    A("-" * 100)
    con_r = [f for f in filas if isinstance(f.get("result"), dict) and "trades" in f["result"]]
    A(f"   {len(con_r)} filas con result completo (trades, net_pnl, profit_factor, win_rate,")
    A(f"   max_drawdown, per_year). NO hay desvio, ni error estandar, ni n de sesiones, ni t.")
    tr = [f["result"]["trades"] for f in con_r]
    A(f"   trades por fila: mediana {sorted(tr)[len(tr)//2]}, min {min(tr)}, max {max(tr)}")
    A(f"   filas con menos de 30 operaciones: {sum(1 for t in tr if t < 30)} de {len(con_r)}")

    A("")
    A("-" * 100)
    A("   LAS DOS COSAS QUE HARIAN FALTA, y si estan")
    A("-" * 100)
    n_pred = sum(1 for f in filas if "prediccion" in f)
    n_stat = sum(1 for f in filas if "stat" in f)
    n_lin = sum(1 for f in filas if "linea_decision_t" in f or "linea_decision_p" in f)
    A(f"   MAGNITUD AFIRMADA -cuanto decia el candidato que iba a dar-:")
    A(f"      'prediccion' en {n_pred} filas de {len(filas)}. En ninguna otra columna hay algo que")
    A(f"      diga que magnitud se esperaba. Los 'config' traen PARAMETROS (hold, target_r, k), no")
    A(f"      una magnitud esperada.")
    A(f"   RESOLUCION DEL TEST -el efecto mas chico que esa corrida podia ver-:")
    A(f"      'linea_decision_t' / 'linea_decision_p' en {n_lin} filas. 'stat' en {n_stat}.")
    A(f"      result NO trae desvio ni error estandar, asi que la resolucion no se puede leer;")
    A(f"      habria que RECALCULARLA.")

    A("")
    A("=" * 100)
    A("   LA RESPUESTA: NO SE PUEDE DIRECTO. SE PUEDE UNA VERSION MAS DEBIL, Y DICE MENOS.")
    A("=" * 100)
    A("   DIRECTO: NO. No existe, en ninguna cantidad utilizable, una columna de MAGNITUD AFIRMADA")
    A(f"   ({n_pred} filas de {len(filas)}) ni una de RESOLUCION. Sin las dos, 'tenia potencia para")
    A("   detectar lo que afirmaba' no se puede contestar fila por fila. Y las 114 filas no son las")
    A("   261 configuraciones: una fila puede cubrir muchas.")
    A("")
    A("   VERSION MAS DEBIL QUE SI SE PUEDE, con lo que hay:")
    A(f"      Para las {len(con_r)} filas con result, se conoce 'trades'. Con el desvio por operacion")
    A("      del ES ya medido en esta ventana se puede RECONSTRUIR la resolucion de cada corrida")
    A("      como MDE = z * sigma_op / raiz(trades), y compararla contra el tamano de efecto")
    A("      OBSERVADO (net_pnl / trades). Eso contesta:")
    A("         'que fraccion de las corridas tenia resolucion peor que su propio efecto observado'")
    A("      QUE NO CONTESTA, y es la pregunta original: que fraccion tenia potencia para detectar")
    A("      lo que AFIRMABA. Comparar contra el efecto OBSERVADO no es comparar contra el")
    A("      AFIRMADO: el observado ya incorpora el resultado, asi que una corrida que no encontro")
    A("      nada tiene efecto observado ~0 y saldria 'sin potencia' por construccion. Es")
    A("      circular en la direccion peligrosa.")
    A("")
    A("      Una segunda version, menos circular: comparar la resolucion reconstruida contra una")
    A("      magnitud de REFERENCIA FIJA -por ejemplo la ventaja de referencia del juez, $72,69 por")
    A("      sesion por mini-. Eso SI contesta algo limpio: 'cuantas corridas podian ver un efecto")
    A("      del tamano que esta casa considera relevante'. No es lo que se afirmaba en cada una,")
    A("      pero es una vara comun y no depende del resultado.")
    A("")
    A("   LO QUE NO VOY A HACER: inventar la magnitud afirmada leyendo las hipotesis a ojo. Es la")
    A("   misma disciplina de la Pieza 2 y el motivo es el mismo: una auditoria reconstruida de")
    A("   memoria no es una medicion, y esta seria peor que la de causas de muerte porque el numero")
    A("   resultante parece objetivo.")
    A("")
    A("   RECOMENDACION: correr la SEGUNDA version (vara comun, no circular) y reportarla con su")
    A("   nombre exacto, que no es 'cuantas tenian potencia para lo que afirmaban' sino 'cuantas")
    A("   tenian resolucion para ver la ventaja de referencia'. Es mas chica que la pregunta")
    A("   original y es honesta. La pregunta original muere con las columnas nombradas.")

    # ------------------------------------------------------------------ la version debil, corrida
    A("")
    A("=" * 100)
    A("   LA VERSION DEBIL, CORRIDA. Nombre exacto: 'cuantas corridas tenian resolucion para ver")
    A("   la ventaja de REFERENCIA de esta casa'. No es la pregunta original.")
    A("=" * 100)
    import math
    sys.path.insert(0, AQUI)
    import juez as J  # noqa: E402
    # sigma por OPERACION del ES, derivado de lo ya publicado: la nula de permutacion da sd_tot por
    # SESION con op_ses operaciones por sesion; sigma_op = sd_ses * raiz(op_ses) / op_ses.
    # Numeros publicados (salida_juez_controles.txt, C1): sd 28,11 por sesion con 4,96 op/sesion.
    SD_SES, OP_SES = 28.11, 4.96
    sigma_op = SD_SES / math.sqrt(OP_SES)
    ref_op = J.REF_EDGE_OP_MINI          # $ por operacion por mini, ventaja de referencia
    A(f"   sigma por operacion (derivado de C1: sd ${SD_SES}/sesion con {OP_SES} op/sesion): "
      f"${sigma_op:.2f}")
    A(f"   ventaja de REFERENCIA por operacion (juez.REF_EDGE_OP_MINI): ${ref_op:.2f}")
    A(f"   MARCA DE FRAGILIDAD: sigma_op sale de UNA celda (5pt:20pt) y de un flujo sintetico del ES.")
    A(f"   Las corridas del ledger son de otras familias, otros instrumentos y otras reglas de")
    A(f"   salida. Es una vara COMUN, no la vara de cada corrida. Estimacion mia, marcada.")
    A("")
    for z_nom, z in (("vara del juez 3,0", J.Z_BASE), ("vara del programa 3,55", 3.552)):
        ok = 0
        for f in con_r:
            n = f["result"]["trades"]
            if n < 2:
                continue
            mde = z * sigma_op / math.sqrt(n)
            if mde <= ref_op:
                ok += 1
        A(f"   Con {z_nom}: {ok} de {len(con_r)} corridas tenian MDE <= la ventaja de referencia "
          f"({ok/len(con_r):.0%})")
    nec = {}
    for z_nom, z in (("3,0", J.Z_BASE), ("3,552", 3.552)):
        nec[z_nom] = (z * sigma_op / ref_op) ** 2
    A("")
    A(f"   Operaciones necesarias para que la MDE baje a la ventaja de referencia: "
      + "   ".join(f"con z={k}: {v:.0f}" for k, v in nec.items()))
    A(f"   Mediana de operaciones en el ledger: {sorted(tr)[len(tr)//2]}")
    A("")
    A("")
    A("-" * 100)
    A("   Y LA VARA DE REFERENCIA ES ENORME, ASI QUE ESE 92% NO DISCRIMINA NADA")
    A("-" * 100)
    A(f"   ventaja de referencia / sigma por operacion = {ref_op/sigma_op:.2f} desvios POR OPERACION.")
    A("   Un efecto de 1,16 desvios por operacion no es una ventaja de mercado: es la ventaja que se")
    A("   INYECTO a proposito en permutacion.py para verificar que el instrumento la recuperaba. Con")
    A("   una vara asi, 7 operaciones alcanzan y cualquier corrida pasa. El 92% mide la vara, no las")
    A("   corridas.")
    A("")
    A("   LA VERSION QUE SI DISCRIMINA: barrer el tamano de efecto en vez de fijarlo. Para cada")
    A("   tamano plausible, cuantas corridas tenian n suficiente. No inventa nada por fila: cambia")
    A("   una pregunta imposible ('que afirmaba cada una') por una contestable ('para que tamanos")
    A("   habia n').")
    A("")
    A(f"   {'efecto (sd/op)':>16}{'n necesario':>14}{'corridas con n suficiente':>28}")
    for e in (1.0, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01):
        n_nec = (3.552 / e) ** 2
        k = sum(1 for f in con_r if f["result"]["trades"] >= n_nec)
        A(f"   {e:>16.2f}{n_nec:>14,.0f}{k:>18} de {len(con_r)}  ({k/len(con_r):>4.0%})")
    A("")
    A("   ESTO SI CONTESTA ALGO, y la lectura es dura: por debajo de 0,1 desvios por operacion -que")
    A("   es donde vive cualquier ventaja de mercado creible- NINGUNA corrida del ledger tenia n")
    A("   para verla. La mediana de 533 operaciones da resolucion para 0,15 desvios por operacion y")
    A("   nada mas fino.")
    A("   LO QUE SIGUE SIN CONTESTARSE: si las corridas AFIRMABAN efectos de ese tamano. Si")
    A("   afirmaban efectos grandes, estaban bien dimensionadas y sus negativos valen. Si afirmaban")
    A("   efectos chicos, sus negativos son sobre el instrumento. El ledger no lo dice y por eso la")
    A("   Tarea 1, como esta formulada, sigue muerta.")

    A("")
    A("   COMO LEER ESTO, y es lo que impide sacar la conclusion grande: da que la MAYORIA de las")
    A("   corridas con result SI tenian resolucion para la ventaja de referencia. Pero eso NO dice")
    A("   que tuvieran potencia para lo que afirmaban, porque no sabemos que afirmaban. Una corrida")
    A("   que buscaba un efecto diez veces mas chico que la referencia estaba ciega aunque aparezca")
    A("   en la columna de 'si'. La pregunta de la Tarea 1 sigue sin contestar, y esta version")
    A("   solo descarta la hipotesis mas extrema -que casi ninguna tuviera n suficiente-.")
    A("=" * 100)
    print("\n".join(R))
    return 0


if __name__ == "__main__":
    sys.exit(main())
