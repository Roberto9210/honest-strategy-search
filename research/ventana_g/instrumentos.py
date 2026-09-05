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


def C(valor, origen, fuente, n=None, reparto=None, verif_resolucion=False):
    """n = sobre cuantas sesiones/dias descansa la medicion. reparto = 'repartido' (dias elegidos
    uno por regimen) o 'contiguo' (un tramo seguido). Los dos campos son parte del ORIGEN: una
    constante MEDIDA sin decir sobre cuanto no es una constante medida, es un numero.

    verif_resolucion = si el script que produjo la constante trae una VERIFICACION DE RESOLUCION,
    o sea si midio que el instrumento podia ver el efecto que reporta. Auditado en
    REGLA_resolucion_del_instrumento.md: HOY NINGUNA LA TIENE, y por eso el defecto es False. No es
    un descuido del campo, es el estado real, y ahora viaja en cada fila del registro del juez en
    vez de vivir solo en un documento aparte."""
    return dict(valor=valor, origen=origen, fuente=fuente, n=n, reparto=reparto,
                verif_resolucion=verif_resolucion)


# MUESTRA MINIMA por constante, medida y no inventada (cortes_tercil_muestra.py, bootstrap de los
# cortes del ES): con los cortes estimados sobre n sesiones sorteadas, el % de sesiones que cambian
# de etiqueta contra los cortes del periodo entero es 34% a n=3, 15% a n=25, 10% a n=50, 7% a n=100,
# 4,7% a n=250 y 3,3% a n=500. El veredicto por regimen exige que la ventaja aguante en LOS TRES
# terciles, asi que una etiqueta equivocada mueve sesiones de tercil: el corte se fija en 250, donde
# el error baja a ~5%. Los de microestructura piden pocos DIAS pero REPARTIDOS, porque ahi el
# problema no es varianza sino sesgo: en ventanas CONTIGUAS el error a n=250 sigue en 29%.
MUESTRA_MINIMA = {
    "cortes_tercil_bps": 250,
    "exceso_stop": 250,
    "o_sobrepaso": 250,
    "deslizamiento_entrada": 3,
    "markout_pasivo": 3,
    "llenado_pasivo": 3,
}
# Las que ademas exigen dias REPARTIDOS por regimen y no un tramo seguido.
EXIGEN_REPARTO = ("deslizamiento_entrada", "markout_pasivo", "llenado_pasivo")


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
                                "microestructura_tbbo.py, tbbo 2017-2019+2026, por tercil ex-ante",
                                n=6, reparto="repartido"),
        # RECALIBRADAS 2026-09-06 (decision D1 de Roberto). Los valores anteriores
        # -markout {0:+0.0392, 1:+0.0073, 2:+0.0697}, llenado {0:0.477, 1:0.514, 2:0.469}- salieron
        # del libro que solo veia cambios de PRECIO, donde el tamano de cola que decide el llenado
        # estaba congelado 669 ms en mediana. Con reconstruir(con_tamano=True) el markout CAMBIA DE
        # SIGNO -cinco de seis terciles negativos- y el llenado baja 10-20%. El piso pasivo honesto
        # pasa de $15,45 a $43,86 (5pt:20pt) y de $32,33 a $73,45 (20pt:10pt).
        markout_pasivo=C({0: -0.0014, 1: -0.0027, 2: -0.0063}, MEDIDO,
                         "mbo_entrada_pasiva.py con MBO_CON_TAMANO=1, mbo, latencia 250 ms, "
                         "muerte 1 tick, epoca B (2017-2019)",
                         n=3, reparto="repartido"),
        llenado_pasivo=C({0: 0.451, 1: 0.423, 2: 0.423}, MEDIDO,
                         "mbo_entrada_pasiva.py con MBO_CON_TAMANO=1, epoca B",
                         n=3, reparto="repartido"),
        exceso_stop=C({10: 0.722, 20: 0.982}, MEDIDO, "media_exceso.py, exceso medio en el stop",
                      n=1006, reparto="repartido"),
        o_sobrepaso=C(0.0642, MEDIDO, "sesgo_marco.py, +-7,6% entre corridas",
                      n=1006, reparto="repartido"),
        # EL SESGO DE CONTABILIDAD TIENE DOS TERMINOS, medido en sesgo_marco_spans_cortos.py:
        #     sesgo_op = o(span) * (1 - 2p)  -  tasa_ambigua(span) * span * 0,5
        # El primero es antisimetrico (sobrepaso de barrera); el segundo es un corrimiento parejo
        # hacia abajo por las barras AMBIGUAS -las dos barreras tocadas en la misma barra de un
        # minuto, que se cuentan como perdida-. Verificado: el intercepto medido coincide con el
        # predicho por la ambiguedad a 1,03-1,17x en los seis spans.
        # En span 20-35 el segundo termino es despreciable (0,006% de ambiguas) y por eso el modelo
        # de un termino alcanzaba. En span 3 es el que MANDA.
        o_por_span=C({3.0: 0.0310, 4.0: 0.0257, 5.0: 0.0237, 7.0: 0.0273, 10.0: 0.0242,
                      25.0: 0.0546}, MEDIDO,
                     "sesgo_marco_spans_cortos.py, bootstrap IID, 6 series, 3 celdas por span. "
                     "SIMPLIFICACION MIA, no medicion: en 3-10 la falta de monotonia "
                     "(0,0310/0,0257/0,0237/0,0273/0,0242) es probablemente ruido de 6 series, y "
                     "el juez interpola. Rango observado en 3-10: 0,0237 a 0,0310, media 0,0264",
                     n=6, reparto="repartido"),
        tasa_ambigua_por_span=C({3.0: 0.01522, 4.0: 0.00733, 5.0: 0.00373, 7.0: 0.00168,
                                 10.0: 0.00051, 25.0: 0.00006}, MEDIDO,
                                "sesgo_marco_spans_cortos.py, fraccion de barras donde se tocan las "
                                "dos barreras. Es artefacto de RESOLUCION de la barra de 1 min, no "
                                "del mercado: con tick se sabria cual se toco primero",
                                n=6, reparto="repartido"),
        cortes_tercil_bps=C("terciles de rango/precio de la sesion ANTERIOR", MEDIDO,
                            "juez_regimen_bps.py, sobre 2016-2019",
                            n=1006, reparto="repartido"),
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
                                "Declarado como herencia, no medido sobre MES",
                                n=6, reparto="repartido"),
        markout_pasivo=C({0: -0.0014, 1: -0.0027, 2: -0.0063}, MEDIDO,
                         "HEREDADO del ES, idem (recalibrado 2026-09-06)",
                         n=3, reparto="repartido"),
        llenado_pasivo=C({0: 0.451, 1: 0.423, 2: 0.423}, MEDIDO,
                         "HEREDADO del ES, idem (recalibrado 2026-09-06)",
                         n=3, reparto="repartido"),
        exceso_stop=C({10: 0.722, 20: 0.982}, MEDIDO, "HEREDADO del ES, idem",
                      n=1006, reparto="repartido"),
        o_sobrepaso=C(0.0642, MEDIDO, "HEREDADO del ES, idem", n=1006, reparto="repartido"),
        cortes_tercil_bps=C("terciles de rango/precio de la sesion ANTERIOR", MEDIDO,
                            "HEREDADO del ES: es la misma serie de precios",
                            n=1006, reparto="repartido"),
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
    # LA MUESTRA, no solo la etiqueta. Una constante MEDIDA sobre 3 dias pasaba la misma compuerta
    # que una medida sobre 1.006 sesiones, y no son lo mismo: medido en cortes_tercil_muestra.py.
    flacas = []
    for k in pide:
        if f[k]["origen"] != MEDIDO:
            continue
        n_min = MUESTRA_MINIMA.get(k)
        if n_min is not None and (f[k]["n"] is None or f[k]["n"] < n_min):
            flacas.append(f"     - {k:<24} n = {f[k]['n']}, hace falta >= {n_min}")
        elif k in EXIGEN_REPARTO and f[k]["reparto"] != "repartido":
            flacas.append(f"     - {k:<24} reparto = {f[k]['reparto']!r}; hacen falta dias "
                          f"REPARTIDOS por regimen, no un tramo seguido")
    if flacas:
        det = "\n".join(flacas)
        raise NoCalibrado(
            f"'{inst}' ({f['nombre']}) tiene todas las constantes pero {len(flacas)} descansan en "
            f"muestra insuficiente:\n{det}\n"
            f"  Medido (cortes_tercil_muestra.py): con los cortes de tercil estimados sobre n "
            f"sesiones, el % de sesiones que cambian de etiqueta contra el periodo entero es 34% a "
            f"n=3, 10% a n=50 y 4,7% a n=250. Con un tercio de las etiquetas mal, 'la ventaja "
            f"aguanta en los tres terciles' no significa nada.")
    return {k: f[k]["valor"] for k in f if isinstance(f[k], dict) and "valor" in f[k]}


# =========================================================================================
# LA PLOMERIA: NO IMPLEMENTADA, y esto es lo que la hace imposible de leer como funcionando
# =========================================================================================
# DECISION 2026-09-05: se eligio (b) -marcarla- y NO (a) -terminarla-. El motivo, en una linea: (a)
# exige que cargar_mercado() sepa cargar otro instrumento, y NO HAY datos de otro instrumento en el
# repo (el paquete de divisas esta COTIZADO, no comprado). Terminar la plomeria significaria escribir
# un camino de codigo que no se puede correr ni una vez, y los diez controles no lo tocarian. Codigo
# sin corrida encima es exactamente lo que este juez existe para no aceptar.
#
# LO QUE QUEDA CABLEADO AL ES dentro de juzgar_periodo, con nombre y sin eufemismo:
#   1. EXCESO_STOP          el exceso medio en el stop (media_exceso.py, ES)
#   2. O_SOBREPASO/O_ERROR_REL  la constante de sobrepaso del bracket (sesgo_marco.py, ES)
#   3. MARKOUT_PASIVO y LLENADO_PASIVO  el modo pasivo, via m["mk_ses_pt"] y m["fi_ses"]
#   4. m["slip_ses_pt"]     el deslizamiento de entrada, que cargar_mercado arma con el
#                           DESLIZAMIENTO_ENTRADA del ES y el eje de terciles del ES
# Y ademas el camino de datos entero: cargar_mercado() lee ES 1-min y nada mas, y tercil_exante es
# el eje del ES.
#
# Hoy nada de esto hace dano porque validar() no deja pasar otro instrumento. Pero eso lo garantiza
# la compuerta, no el calculo: si manana alguien completa la ficha de 6E, la compuerta se abre y el
# calculo le cobra el medio-spread del ES en silencio. Por eso la lista de abajo es una TERCERA
# cerradura, dentro del calculo, que no depende de que la ficha este completa.
CALIBRACION_CABLEADA = ("ES", "MES")


def exigir_plomeria(inst):
    """Se llama DENTRO del calculo. No confia en que la compuerta de la ficha haya cerrado."""
    if inst not in CALIBRACION_CABLEADA:
        raise NoCalibrado(
            f"'{inst}' tiene ficha completa pero el CALCULO todavia esta cableado al ES. Quedan "
            f"cuatro constantes leyendose de los globales del ES -exceso en el stop, constante de "
            f"sobrepaso, markout y llenado pasivos, y el deslizamiento de entrada- y "
            f"cargar_mercado() solo sabe leer ES 1-min.\n"
            f"  La plomeria por instrumento esta NO IMPLEMENTADA a proposito y marcada como tal "
            f"(instrumentos.py, seccion LA PLOMERIA). Completar la ficha NO alcanza: hay que "
            f"terminar el calculo y volver a correr los diez controles.")


def inventario():
    """Filas (instrumento, constante, origen, fuente) para el reporte."""
    for inst, f in INSTRUMENTOS.items():
        for k, v in f.items():
            if isinstance(v, dict) and "origen" in v:
                yield inst, k, v["origen"], v["fuente"]
