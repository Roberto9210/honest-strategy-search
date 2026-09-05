"""
B1 - LA CALIBRACION POR INSTRUMENTO, SEPARADA DE LA MAQUINARIA.

NO GASTA CARTUCHO. K = 261. Este archivo no mide nada: junta en un solo lugar lo que ya estaba
medido y disperso, y declara con nombre y procedencia lo que FALTA para cada instrumento nuevo.

POR QUE EXISTE. La VENTANA L trajo once candidatas y las mas fuertes son de DIVISAS o necesitan
flujo de ordenes. El juez solo acepta ES y MES, asi que las mejores son justo las que no puede
juzgar. Fue un error de ORDEN nuestro: se construyo la herramienta antes de saber que habia que
medir. Lo que se puede arreglar sin rehacerla es hacer explicito donde termina la maquinaria y
empieza la calibracion, para que agregar un instrumento sea llenar una ficha y no tocar el juez.

LO QUE **NO** DEPENDE DEL INSTRUMENTO (maquinaria, se queda en juez.py y no se toca):
  - las dos nulas de permutacion (rotacion en rango, signo) y la comparacion pasiva
  - la clase de ventaja declarada, la firma medida y que nula se omite
  - el eje de regimen POR TERCILES y la exigencia de que la ventaja aguante en los tres
  - la asimetria del modo pasivo (nunca aprueba), los seis veredictos, el registro encadenado,
    la huella de familia, el umbral por multiplicidad, la caja sellada, el candado de 2019
  - la puerta de entrada (nada de resultados) y el limite de exposicion

LO QUE **SI** DEPENDE DEL INSTRUMENTO (calibracion, vive aca):
  cada constante lleva su ORIGEN, y el origen decide si hace falta comprar datos:
    ESPEC   se deriva de la especificacion oficial del contrato. Gratis, sin datos.
    REGLA   sale de la letra del producto o de la lista de precios. Gratis, sin datos.
    MEDIDO  hay que medirlo sobre datos del instrumento. Cuesta.
    FALTA   no esta, y el juez tiene que NEGARSE en vez de sustituir.

LA REGLA DURA: sustituir la calibracion de un instrumento por la de otro esta PROHIBIDO. El ES y el
6E no comparten ni el valor del punto ni el tamano del tick ni la sesion ni el spread. Un juez que
acepta '6E' usando el medio-spread del ES devuelve un numero con cara de veredicto. Por eso
`calibracion()` levanta NoCalibrado y lista exactamente que falta.
"""

ESPEC, REGLA, MEDIDO, FALTA = "ESPEC", "REGLA", "MEDIDO", "FALTA"


def C(valor, origen, fuente):
    return dict(valor=valor, origen=origen, fuente=fuente)


# =========================================================================================
# Las fichas. ES y MES son las dos que estan completas; las demas estan a medio llenar A
# PROPOSITO, para que se vea de un vistazo que falta y cuanto de eso es gratis.
# =========================================================================================
INSTRUMENTOS = {
    "ES": dict(
        nombre="E-mini S&P 500",
        punto=C(50.0, ESPEC, "CME: $50 por punto de indice"),
        tick=C(0.25, ESPEC, "CME: 0,25 puntos = $12,50"),
        micros_equiv=C(10, ESPEC, "1 ES = 10 MES"),
        sesion=C("ETH 17:00-16:00 CT", ESPEC, "CME globex; verificado contra NT8 en 828 barras"),
        comision=C(5.76, REGLA, "help.tradeify.co 2026-09-03, ida y vuelta todo incluido"),
        # los tres de abajo son los caros
        deslizamiento_entrada=C({0: 0.1267, 1: 0.1334, 2: 0.1330}, MEDIDO,
                                "microestructura_tbbo.py, tbbo 2017-2019+2026, por tercil ex-ante"),
        markout_pasivo=C({0: 0.0392, 1: 0.0073, 2: 0.0697}, MEDIDO,
                         "mbo_entrada_pasiva.py, mbo, latencia 250 ms, muerte 1 tick"),
        llenado_pasivo=C({0: 0.477, 1: 0.514, 2: 0.469}, MEDIDO, "mbo_entrada_pasiva.py"),
        exceso_stop=C({10: 0.722, 20: 0.982}, MEDIDO, "media_exceso.py, exceso medio en el stop"),
        o_sobrepaso=C(0.0642, MEDIDO, "sesgo_marco.py, +-7,6% entre corridas"),
        cortes_tercil_bps=C("terciles de rango/precio de la sesion ANTERIOR", MEDIDO,
                            "juez_regimen_bps.py, sobre 2016-2019"),
    ),
    "MES": dict(
        nombre="Micro E-mini S&P 500",
        punto=C(5.0, ESPEC, "CME: $5 por punto de indice"),
        tick=C(0.25, ESPEC, "CME"),
        micros_equiv=C(1, ESPEC, "es la unidad"),
        sesion=C("ETH 17:00-16:00 CT", ESPEC, "CME globex"),
        comision=C(1.82, REGLA, "help.tradeify.co 2026-09-03"),
        # el MES hereda del ES A PROPOSITO y con motivo escrito: mismo subyacente, mismo libro
        # de referencia, mismo horario, y el tick en PUNTOS es identico. Es la unica herencia
        # permitida en todo el archivo, y esta declarada como herencia, no como medicion.
        deslizamiento_entrada=C({0: 0.1267, 1: 0.1334, 2: 0.1330}, MEDIDO,
                                "HEREDADO del ES: mismo subyacente y mismo tick en puntos. "
                                "Declarado como herencia, no medido sobre MES"),
        markout_pasivo=C({0: 0.0392, 1: 0.0073, 2: 0.0697}, MEDIDO, "HEREDADO del ES, idem"),
        llenado_pasivo=C({0: 0.477, 1: 0.514, 2: 0.469}, MEDIDO, "HEREDADO del ES, idem"),
        exceso_stop=C({10: 0.722, 20: 0.982}, MEDIDO, "HEREDADO del ES, idem"),
        o_sobrepaso=C(0.0642, MEDIDO, "HEREDADO del ES, idem"),
        cortes_tercil_bps=C("terciles de rango/precio de la sesion ANTERIOR", MEDIDO,
                            "HEREDADO del ES: es la misma serie de precios"),
    ),
    # ---------------------------------------------------------------- las de la VENTANA L
    "6E": dict(
        nombre="Euro FX (L08, panel de divisas)",
        punto=C(125000.0, ESPEC, "CME: contrato de EUR 125.000; $1 por 0,00001 => $12,50 por pip"),
        tick=C(0.00005, ESPEC, "CME: 0,00005 USD/EUR = $6,25"),
        micros_equiv=C(10, ESPEC, "1 6E = 10 M6E"),
        sesion=C("ETH 17:00-16:00 CT", ESPEC, "CME globex, mismo calendario que el ES"),
        comision=C(None, FALTA, "la lista de Tradeify leida cubre indices (ES/NQ/YM/RTY y micros); "
                                "no se leyo la tarifa de divisas. GRATIS de cerrar: es leer la pagina"),
        deslizamiento_entrada=C(None, FALTA, "hay que medirlo: tbbo de 6E"),
        markout_pasivo=C(None, FALTA, "hay que medirlo: mbo de 6E"),
        llenado_pasivo=C(None, FALTA, "hay que medirlo: mbo de 6E"),
        exceso_stop=C(None, FALTA, "solo hace falta si la regla de salida es bracket. L08 no usa "
                                   "bracket: mide el retorno de una ventana declarada"),
        o_sobrepaso=C(None, FALTA, "idem: es una correccion de contabilidad DE BRACKET"),
        cortes_tercil_bps=C(None, FALTA, "hay que medirlo: rango/precio de la sesion anterior en 6E"),
    ),
    "6J": dict(
        nombre="Japanese Yen (L07, gotobi)",
        punto=C(12500000.0, ESPEC, "CME: contrato de JPY 12.500.000"),
        tick=C(0.0000005, ESPEC, "CME: $6,25 por tick"),
        micros_equiv=C(10, ESPEC, "1 6J = 10 M6J"),
        sesion=C("ETH 17:00-16:00 CT", ESPEC, "CME globex"),
        comision=C(None, FALTA, "misma pagina sin leer que 6E"),
        deslizamiento_entrada=C(None, FALTA, "hay que medirlo: tbbo de 6J en la ventana de Tokio"),
        markout_pasivo=C(None, FALTA, "hay que medirlo"),
        llenado_pasivo=C(None, FALTA, "hay que medirlo"),
        exceso_stop=C(None, FALTA, "no hace falta si no hay bracket"),
        o_sobrepaso=C(None, FALTA, "idem"),
        cortes_tercil_bps=C(None, FALTA, "hay que medirlo"),
    ),
}

# Las que el juez puede juzgar HOY. No se toca esta lista sin llenar la ficha entera.
COMPLETOS = ("ES", "MES")

# Que hace falta segun la regla de salida declarada. Un candidato de VENTANA (retorno en una
# ventana, sin barreras) no necesita la correccion de sobrepaso ni el exceso en el stop: no hay
# barrera que sobrepasar. Es la diferencia entre lo caro y lo carisimo.
NECESARIO = {
    "bracket": ("punto", "comision", "deslizamiento_entrada", "exceso_stop", "o_sobrepaso",
                "cortes_tercil_bps"),
    "tiempo": ("punto", "comision", "deslizamiento_entrada", "cortes_tercil_bps"),
    "ventana": ("punto", "comision", "deslizamiento_entrada", "cortes_tercil_bps"),
}
NECESARIO_PASIVO = ("markout_pasivo", "llenado_pasivo")


class NoCalibrado(Exception):
    pass


def calibracion(inst, tipo_regla="bracket", pasivo=False):
    """Devuelve los valores del instrumento, o levanta NoCalibrado con la lista de lo que falta.
    NUNCA sustituye por otro instrumento: eso devolveria un numero con cara de veredicto."""
    if inst not in INSTRUMENTOS:
        raise NoCalibrado(
            f"El juez no tiene ficha de calibracion para '{inst}'. Instrumentos con ficha: "
            f"{', '.join(sorted(INSTRUMENTOS))} (completos: {', '.join(COMPLETOS)}).\n"
            f"  QUE HACER: agregar la ficha en instrumentos.py. Lo que sale de la especificacion "
            f"oficial es gratis; lo demas hay que medirlo sobre datos del instrumento.")
    f = INSTRUMENTOS[inst]
    pide = list(NECESARIO.get(tipo_regla, NECESARIO["bracket"]))
    if pasivo:
        pide += list(NECESARIO_PASIVO)
    faltan = [k for k in pide if f[k]["origen"] == FALTA or f[k]["valor"] is None]
    if faltan:
        det = "\n".join(f"     - {k:<24} {f[k]['fuente']}" for k in faltan)
        raise NoCalibrado(
            f"'{inst}' ({f['nombre']}) tiene ficha pero le faltan {len(faltan)} constantes para una "
            f"regla de tipo '{tipo_regla}'{' en modo pasivo' if pasivo else ''}:\n{det}\n"
            f"  El juez NO sustituye por la calibracion de otro instrumento. Un medio-spread de ES "
            f"aplicado a 6E devuelve un numero que parece un veredicto y no lo es.")
    return {k: f[k]["valor"] for k in f if isinstance(f[k], dict) and "valor" in f[k]}


def inventario():
    """Filas (instrumento, constante, origen, fuente) para el reporte."""
    for inst, f in INSTRUMENTOS.items():
        for k, v in f.items():
            if isinstance(v, dict) and "origen" in v:
                yield inst, k, v["origen"], v["fuente"]
