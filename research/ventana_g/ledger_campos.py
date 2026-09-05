"""
TAREA 1 - EL LEDGER EXTENDIDO. Los campos que hacen auditable un veredicto HACIA ADELANTE.

NO GASTA CARTUCHO. K = 261. Dinero: $0. No mide nada: define y calcula los campos.

POR QUE EXISTE, y es la unica tarea con reloj. La auditoria de potencia de las 261 murio con las
columnas nombradas: el ledger tiene 114 filas, 'prediccion' en 4 y ninguna columna de resolucion, asi
que no se puede contestar cuantas tenian potencia para lo que afirmaban. Cada dia sin estos campos es
otro dia de registros que tampoco se van a poder auditar. Ya perdimos 261 por exactamente esto.

DONDE SE ESCRIBE, y por que no en el otro: se extiende REGISTRO_JUEZ.jsonl, que es el registro del
juez y territorio de esta ventana. NO se toca factory/experiments_ledger.jsonl: es el ledger del
programa entero y cambiarle el esquema por mi cuenta seria hacer con el ledger lo que no hago con los
documentos de otras ventanas. El esquema queda escrito aca para que el ledger del programa lo adopte
si Roberto quiere.

LOS NUEVE CAMPOS, y de donde sale cada uno:
    veredicto                ya estaba
    causa                    NUEVO - que lo freno, en palabras: la nula, la cerradura o el regimen
    largo_ventana_barras     NUEVO - tenencia mediana en barras (la ventana de la operacion)
    n_op                     ya estaba - LA VARIABLE QUE DECIDE LA POTENCIA
    tenencia_mediana_seg     NUEVO - la misma en segundos, para la regla R2 de los 10 s
    magnitud_afirmada        NUEVO - declarada por el candidato, en $/sesion. Inverificable, por eso
                             se declara; si falta, queda None y el veredicto lo dice
    resolucion_mde           NUEVO - el efecto mas chico que ESA corrida podia ver, en $/sesion
    numero_que_lo_mato       NUEVO - el z que quedo por debajo del umbral, con su nombre y su valor
    constantes_verificadas   NUEVO - si las constantes que uso vienen de un script CON verificacion
                             de resolucion. Hoy da False para todas y eso es el hallazgo, no un bug
"""

CAMPOS_NUEVOS = ("causa", "largo_ventana_barras", "tenencia_mediana_seg", "magnitud_afirmada",
                 "resolucion_mde", "numero_que_lo_mato", "constantes_verificadas")


def causa_y_numero(r, z_req, veredicto):
    """Devuelve (causa, numero_que_lo_mato). El 'numero que lo mato' es el z mas chico de los que
    se le exigieron y su nombre, o None si nada lo freno."""
    if veredicto == "SUPERA":
        return "nada: bate todo y aguanta en los tres terciles", None
    cands = [("rentabilidad", r["z_rent"]), ("rotacion en rango", r["nulas"]["A rotacion"][3]),
             ("pasiva", r["z_pas"])]
    if not r.get("aplica_timing"):
        cands.append(("signo", r["nulas"]["B signo"][3]))
    peor = min(cands, key=lambda x: x[1])
    if peor[1] < z_req:
        return f"lo freno {peor[0]}", dict(nombre=peor[0], z=round(peor[1], 3),
                                           z_exigido=round(z_req, 3))
    # paso todo lo global: entonces lo freno el regimen o una cerradura
    reg = r.get("regimen") or []
    flojos = [t["nombre"] for t in reg if t.get("verificable") and not t.get("aguanta")]
    sin_datos = [t["nombre"] for t in reg if not t.get("verificable")]
    if flojos or sin_datos:
        det = (f"terciles que no aguantan: {', '.join(flojos)}" if flojos else "") + \
              (f"; sin datos: {', '.join(sin_datos)}" if sin_datos else "")
        peor_t = min((t for t in reg if t.get("verificable")), key=lambda t: t["z"], default=None)
        num = dict(nombre="tercil mas flojo", z=round(peor_t["z"], 3) if peor_t else None,
                   z_exigido=None) if peor_t else None
        return f"lo freno el REGIMEN ({det.strip('; ')})", num
    return "lo freno una cerradura externa (ver avisos)", None


def constantes_verificadas(inst_ficha, pide):
    """True solo si TODAS las constantes MEDIDAS que la corrida usa vienen de un script con
    verificacion de resolucion. Hoy ninguna la tiene -REGLA_resolucion_del_instrumento.md-, asi que
    esto da False y ESE es el punto: queda anotado en cada fila en vez de en un documento aparte."""
    faltan = []
    for k in pide:
        c = inst_ficha.get(k)
        if isinstance(c, dict) and c.get("origen") == "MEDIDO" and not c.get("verif_resolucion"):
            faltan.append(k)
    return (len(faltan) == 0), faltan


def fila_extendida(r, cand, z_req, veredicto, inst_ficha, pide):
    causa, num = causa_y_numero(r, z_req, veredicto)
    ok, faltan = constantes_verificadas(inst_ficha, pide)
    import numpy as np
    ten_bar = float(np.median(r["ten"])) if len(r["ten"]) else 0.0
    return dict(
        causa=causa,
        largo_ventana_barras=round(ten_bar, 2),
        tenencia_mediana_seg=round(ten_bar * 60.0, 1),
        magnitud_afirmada=cand.get("magnitud_afirmada"),
        resolucion_mde=round(r["mde"], 3),
        numero_que_lo_mato=num,
        constantes_verificadas=dict(todas_verificadas=ok, sin_verificacion=faltan),
    )
