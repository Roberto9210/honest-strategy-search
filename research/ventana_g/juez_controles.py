"""
CONTROLES DEL JUEZ - diez, cada uno con condicion de falla escrita contra un resultado PUBLICADO,
y todos tienen que poder salir de las dos formas.

NO GASTA CARTUCHO. K = 261. Construir la herramienta no es usarla: los candidatos de aca son
SINTETICOS, de propiedades conocidas, construidos sobre el mismo terreno (ES 1-min 2016-2018, el
periodo de trabajo). Ninguno es una hipotesis de mercado. La caja sellada no se toca.

LECCION DE AYER, aplicada: cada condicion de falla se escribe contra el numero ya publicado, no
contra lo que supongo. Un control calibrado contra una linea de base imaginada falla sin que nada
este mal (me paso con "A domina a TODO capital", que contradecia mi propia curva).

  C1  SIN VENTAJA. Entradas en grilla de 300 barras, lado por moneda. Publicado: permutacion.py C0
      dio +0,6 desvios contra las dos nulas. ESPERADO: NO SUPERA.
      LO HARIA FALLAR: SUPERA o APUESTA AL REGIMEN.
  C2  VENTAJA INYECTADA de tamano conocido (q = 0,62: con prob. q se elige el lado que resulto
      mejor). Publicado: permutacion.py recupero la inyectada al 100% y 101%, con resolucion
      +-33%. ESPERADO: SUPERA, y la ventaja contra la nula de signo dentro de +-33% de la
      inyectada REALIZADA (no la nominal: esa fue la trampa).
      LO HARIA FALLAR: no SUPERA, o recuperacion fuera de [0,67; 1,33].
  C3  POCAS OPERACIONES (80). Publicado: con 4.994 la resolucion es +-33%; con 80 el error
      supera a la ventaja de referencia. ESPERADO: NO MEDIBLE, no un numero.
      LO HARIA FALLAR: cualquier veredicto numerico.
  C4  ENTRADA CON RESULTADOS (campo 'pnl'). ESPERADO: RECHAZADA en la puerta.
      LO HARIA FALLAR: que se juzgue.
  C5  VENTAJA EN UN SOLO REGIMEN (q = 0,75 solo en sesiones del tercil alto EX-ANTE -volatilidad
      de la sesion anterior, que un candidato SI puede conocer-, moneda en el resto). Publicado:
      juez_regimen_exante.py, el tercil alto ex-ante tiene piso $105,34 contra $5,07 del bajo; la
      ventaja global va a ser grande y solo un tercil la sostiene. ESPERADO: APUESTA AL REGIMEN.
      LO HARIA FALLAR: SUPERA (no distingue el regimen) o NO SUPERA (no ve la ventaja).
  C6  EL ATAQUE A1: solo-largo restringido a 2017. Publicado: salida_cortes.txt, 2017 largo
      +$85,56/sesion a +2,7 errores; con la rotacion GLOBAL la nula vive en 2016-2019 y el
      candidato en 2017. Con la defensa (rotacion dentro del rango + pasiva) la nula tambien vive
      en 2017. ESPERADO: NO SUPERA con la defensa. Y se corre SIN defensa para mostrar que la
      defensa hace falta: ahi el 'informativo' tiene que subir.
      LO HARIA FALLAR: SUPERA o APUESTA con la defensa puesta.
  C7  VENTAJA SOLO EN TENDENCIAS BAJISTAS (q = 0,90 en sesiones cuyo movimiento neto de las 20
      anteriores fue negativo, moneda en el resto). Nace de mi propio (c1): al cerrar el eje de
      direccion medi que las sesiones bajistas caen mayormente en el tercil ALTO de volatilidad
      (172 de 261 en juez_regimen_direccion.py), asi que una ventaja puramente bajista tiene que
      aparecer como ventaja concentrada en el regimen alto, no repartida. Es la prueba de que
      cerrar el eje de direccion NO dejo un agujero. ESPERADO: APUESTA AL REGIMEN.
      LO HARIA FALLAR: SUPERA (el juez no ve que la ventaja es de un solo regimen).
      NOTA medida: a q=0,75 el deslizamiento de entrada -costo plano sobre todas las operaciones-
      tumbaba el obs global bajo 3sd y daba NO SUPERA (el costo mataba la ventaja concentrada antes
      de mirar el regimen). Se sube a 0,90 para aislar la maquinaria de regimen: rentable global, y
      el unico freno es que solo un tercil aguanta.
  C8  CANDIDATO EN EL BORDE entre modos (q=0,545, semilla dedicada 5): obs cae JUSTO entre el piso
      pasivo y el de cruce. Recalibrado con c8_semillas.py: a q=0,56 solo 42% de las semillas caian
      en el borde (5/12 quedaban POR ENCIMA, SUPERA en cruce); a q=0,545 las 12 dan NO SUPERA en
      cruce y 9/12 cruzan hacia arriba en pasivo.
      Es el unico control que prueba la frontera donde el desplazamiento de nivel entre modos podria
      hacer dano. ESPERADO: NO APRUEBA en ninguno de los dos modos (NO SUPERA / APUESTA / REQUIERE
      MEDICION), NUNCA SUPERA. La categoria exacta de no-aprobacion depende del sorteo (que aguanten
      los tres terciles en el borde) y no se fija; el invariante robusto es NO SUPERA. La conversion
      SUPERA->REQUIERE MEDICION la ejercita C2, que tiene ventaja grande y SUPERA firme en cruce.
      LO HARIA FALLAR: que devuelva SUPERA en cualquiera de los dos modos.

  C9  VENTAJA DE TIMING declarada BIEN (sabe CUANDO, lado al azar; el mejor tercio de ranuras DENTRO
      de cada tercil de volatilidad, para que el timing quede repartido por regimen y el control aisle
      una sola propiedad). Publicado en juez_formas_ventaja.py: una ventaja de timing pura la recupera
      la rotacion al 98% y la de signo al -1%. Como la nula de signo NO es un test valido para esa
      clase, si el candidato la DECLARA y la firma lo confirma, se la omite del minimo.
      ESPERADO: SUPERA (o REQUIERE MEDICION en pasivo).
      LO HARIA FALLAR: que siga dando NO SUPERA -el punto ciego no se arreglo-.
      MEDIDO de paso: con seleccion GLOBAL (no estratificada) el mismo candidato da APUESTA AL REGIMEN
      -el juez SI ve la ventaja, pero la ventaja vive en un regimen-.
  C10 LA PUERTA TRASERA: candidato SIN ventaja que declara 'timing'. ESPERADO: NO SUPERA igual, de
      plano. La declaracion no compra nada: la relajacion se gana con la FIRMA medida, no con decirlo.
      LO HARIA FALLAR: que declarar una clase falsa lo mueva de NO SUPERA.

REGLA DE MODO PASIVO: el juez NUNCA devuelve SUPERA en modo pasivo (la cota optimista solo rechaza).
Cuando superaria la cota devuelve REQUIERE MEDICION PASIVA POR CANDIDATO. Verificado en los ocho.

DEMOSTRACION (no es un control): el contador. C1 juzgado otra vez en el registro donde ya esta
C2 (misma huella de entradas) tiene que disparar el aviso de familia y subir el umbral.
"""
import json
import os
import sys
import tempfile
import time

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import juez as J  # noqa: E402

PASO = 300
CELDA = dict(tipo="bracket", objetivo_pt=5, stop_pt=20)
Q2, Q5 = 0.62, 0.75
# C7 inyecta ventaja SOLO en el 26% de las sesiones (bajistas). A q=0,75 el deslizamiento de entrada
# -costo plano sobre TODAS las operaciones- tumbaba el obs global por debajo de 3sd y daba NO SUPERA:
# el costo mataba la ventaja concentrada antes de que el juez llegara a mirar el regimen. Se sube a
# 0,90 para que el candidato SI sea rentable globalmente y el UNICO freno sea el regimen -> APUESTA.
# El hecho de que a q=0,75 el costo solo lo tumbe queda anotado en el reporte.
Q7 = 0.90
# C8 (candidato en el BORDE entre modos). RECALIBRADO con c8_semillas.py sobre 12 semillas x 3 q:
# q=0,56 quedaba mal centrado (solo 42% en el borde, y 5/12 semillas POR ENCIMA -SUPERA en cruce-).
# q=0,545 centra: 12/12 semillas dan NO SUPERA en cruce (ninguna por encima) y 9/12 cruzan a una
# categoria mas alta en pasivo. Se usa una semilla DEDICADA (5), que en el barrido dio el caso limpio
# NO SUPERA (cruce) -> REQUIERE MEDICION (pasivo), para que el suite principal muestre el borde
# siempre y no dependa del sorteo compartido.
Q8 = 0.545
SEMILLA_C8 = 5
NPERM = int(os.environ.get("JUEZ_NPERM", "200"))
MODO_PASIVO = False              # lo togglea correr(); el helper juzgar() lo inyecta en J.juzgar
SEMILLA = 20260904


def registro_nuevo(nombre):
    ruta = os.path.join(tempfile.gettempdir(), f"juez_ctrl_{nombre}.jsonl")
    if os.path.exists(ruta):
        os.remove(ruta)
    return ruta


def grilla(m, anios):
    ses = np.flatnonzero(np.isin(m["anio_ses"], anios))
    return np.concatenate([np.arange(m["ini"][k], m["fin"][k] - 1, PASO) for k in ses])


def ambos_lados(m, idx):
    ex = J.EXCESO_STOP[CELDA["stop_pt"]]
    pL, _ = J.resolver(m, idx, np.ones(len(idx)), CELDA, ex)
    pS, _ = J.resolver(m, idx, -np.ones(len(idx)), CELDA, ex)
    return pL, pS


def candidato(nombre, m, idx, largo_mask, variantes=1, familia=None, clase="direccional"):
    ops = [dict(ts=str(m["ts"][i]), lado=("largo" if L else "corto")) for i, L in zip(idx, largo_mask)]
    c = dict(nombre=nombre, instrumento="ES", contratos=1, limite_contratos=12,
             variantes_probadas=variantes, clase_ventaja=clase,
             regla_salida=dict(CELDA), operaciones=ops)
    if familia:
        c["familia"] = familia
    return c


def juzgar(nombre, cand, m, reg, **kw):
    t0 = time.time()
    kw.setdefault("pasivo", MODO_PASIVO)
    try:
        s = J.juzgar(cand, m, npermuta=NPERM, registro=reg, **kw)
        v = s["periodos"]["trabajo"]["veredicto"]
        print(f"   [{nombre}] {v}   ({time.time()-t0:.0f}s)")
        return v, s
    except J.NoMedible as e:
        print(f"   [{nombre}] NO MEDIBLE   ({time.time()-t0:.0f}s)\n      motivo: {str(e).splitlines()[0][:150]}")
        return "NO MEDIBLE", None
    except J.Rechazo as e:
        print(f"   [{nombre}] RECHAZADA   ({time.time()-t0:.0f}s)\n      motivo: {str(e).splitlines()[0][:150]}")
        return "RECHAZADA", None


def resumen(s):
    r = s["periodos"]["trabajo"]
    A, B = r["nulas"]["A rotacion"], r["nulas"]["B signo"]
    print(f"      obs {r['obs']:+.2f}  nulaA {A[0]:+.2f} (vent {A[2]:+.2f}, {A[3]:+.1f}sd)  "
          f"nulaB {B[0]:+.2f} (vent {B[2]:+.2f}, {B[3]:+.1f}sd)  pasiva {r['pasiva']:+.2f} "
          f"({r['z_pas']:+.1f}sd)  sd {r['sd_tot']:.2f}  z_req {r['z_req']:.2f}")
    print("      regimen: " + "  ".join(
        f"{t['nombre']}={'SIN DATOS' if not t['verificable'] else f'{t['ventaja']:+.1f}({t['z']:+.1f}sd){'SI' if t['aguanta'] else 'no'}'}"
        for t in r["regimen"]))
    c = r["cadena"]
    print(f"      cadena eval x fondeada ({c['N']} micros): P(pasa eval) {c['p_pasa']:.3f}  P(pago) {c['p_pago']:.3f}  "
          f"P(se acaba el rango) {c['p_tiempo']:.3f}  E sesiones {c['e_ses']:.0f}  E $/intento {c['E']:+.0f}")
    frena = [n for n, z in (("rotacion en rango", A[3]), ("signo", B[3]), ("pasiva", r["z_pas"]))
             if z < r["z_req"]]
    print(f"      informativo = min(rotacion, signo, pasiva) = {r['z_info']:+.1f}sd; "
          f"lo frena: {', '.join(frena) if frena else 'nada (bate las tres)'}")


def correr(pasivo, m):
    global MODO_PASIVO
    MODO_PASIVO = pasivo
    print("=" * 100)
    print(f"CONTROLES DEL JUEZ - diez, con condicion de falla contra lo publicado   "
          f"[MODO {'PASIVO' if pasivo else 'CRUCE'}]")
    print(f"NO GASTA CARTUCHO. K = 261. Permutaciones por nula: {NPERM}. La caja sellada no se toca.")
    print("=" * 100)
    rng = np.random.default_rng(SEMILLA)
    idx = grilla(m, [2016, 2017, 2018])
    pL, pS = ambos_lados(m, idx)
    punto, c1 = J.PUNTO["ES"], J.COMISION["ES"]
    dL, dS = pL * punto - c1, pS * punto - c1
    dif = np.abs(dL - dS)
    mejor_largo = dL >= dS
    print(f"\n   grilla 2016-2018: {len(idx):,} ranuras cada {PASO} barras, celda 5pt:20pt, 1 ES.")
    resultados = {}

    # ---------------------------------------------------------------- C1 sin ventaja
    print("\nC1  SIN VENTAJA. Esperado NO SUPERA. Falla si SUPERA o APUESTA.")
    moneda = rng.random(len(idx)) < 0.5
    c1c = candidato("C1_sin_ventaja", m, idx, moneda)
    v, s = juzgar("C1", c1c, m, registro_nuevo("c1"))
    if s: resumen(s)
    resultados["C1"] = (v == "NO SUPERA", v)

    # ---------------------------------------------------------------- C2 ventaja inyectada
    print(f"\nC2  VENTAJA INYECTADA q={Q2}. Esperado SUPERA y recuperacion dentro de +-33% de la realizada.")
    acierta = rng.random(len(idx)) < Q2
    lado2 = np.where(acierta, mejor_largo, ~mejor_largo)
    c2c = candidato("C2_ventaja_inyectada", m, idx, lado2)
    v, s = juzgar("C2", c2c, m, registro_nuevo("c2"))
    ok2 = False
    if s:
        resumen(s)
        r = s["periodos"]["trabajo"]
        realizada = float(((acierta - 0.5) * dif).sum() / r["n_ses"])
        ventB = r["nulas"]["B signo"][2]; ventA = r["nulas"]["A rotacion"][2]
        rec = ventB / realizada if realizada else float("nan")
        print(f"      inyectada REALIZADA {realizada:+.2f}/sesion   recuperada: signo {ventB:+.2f} "
              f"({rec:.0%})   rotacion {ventA:+.2f} ({ventA/realizada:.0%})")
        if MODO_PASIVO:
            # en pasivo el juez NUNCA devuelve SUPERA: la cota optimista solo sirve para rechazar, y
            # cuando la supera devuelve REQUIERE MEDICION. Ademas la recuperacion cae a ~fill*100% POR
            # CONSTRUCCION (dolares escalados por el llenado); la banda de magnitud es de modo CRUCE.
            ok2 = (v == J.REQUIERE_MEDICION)
            print(f"      (modo pasivo: no da SUPERA -> {J.REQUIERE_MEDICION}. Recuperacion ~{rec:.0%} "
                  f"= escalado por llenado ~{np.mean([J.LLENADO_PASIVO[k] for k in (0,1,2)]):.0%}, no un fallo)")
        else:
            ok2 = (v == "SUPERA") and (0.67 <= rec <= 1.33)
    resultados["C2"] = (ok2, v)

    # ---- barrido de TAMANO en la cadena (tu (b)): P(pasar) para el MISMO flujo de C2 a 1/4/10/40
    # micro-equivalentes. El juez ya usa el tamano DECLARADO; esto muestra cuanto pesa esa decision.
    if s:
        r2 = s["periodos"]["trabajo"]
        print("   BARRIDO DE TAMANO (mismo flujo de C2, cadena Tradeify 50K), P(pasar) por micro-equiv:")
        print(f"      {'micros':>8}{'P(pasa ev)':>12}{'P(pago)':>10}{'E ses':>8}{'E $/intento':>13}")
        for k in (1, 4, 10, 40):
            c = J.cadena_pasar(r2, m, n_micros=k)
            print(f"      {k:>8}{c['p_pasa']:>12.3f}{c['p_pago']:>10.3f}{c['e_ses']:>8.0f}{c['E']:>+13.0f}")
        print("      -> el tamano es una decision del candidato tan importante como su ventaja: el mismo")
        print("         flujo va de casi-nunca-cobra a cobrar seguido segun cuantos contratos ponga.")

    # ---------------------------------------------------------------- C3 pocas operaciones
    print("\nC3  POCAS OPERACIONES (80). Esperado NO MEDIBLE. Falla si da un numero.")
    sel = np.sort(rng.choice(len(idx), 80, replace=False))
    c3c = candidato("C3_pocas", m, idx[sel], moneda[sel])
    v, s = juzgar("C3", c3c, m, registro_nuevo("c3"))
    resultados["C3"] = (v == "NO MEDIBLE", v)

    # ---------------------------------------------------------------- C4 con resultados
    print("\nC4  ENTRADA CON RESULTADOS. Esperado RECHAZADA. Falla si se juzga.")
    c4c = json.loads(json.dumps(c1c)); c4c["nombre"] = "C4_con_resultados"
    for o in c4c["operaciones"][:50]:
        o["pnl"] = 12.5
    v, s = juzgar("C4", c4c, m, registro_nuevo("c4"))
    resultados["C4"] = (v == "RECHAZADA", v)

    # ---------------------------------------------------------------- C5 un solo regimen
    print(f"\nC5  VENTAJA SOLO EN EL TERCIL ALTO EX-ANTE (sesion anterior; q={Q5}). Esperado APUESTA AL REGIMEN.")
    terc_op = m["tercil_exante"][m["ses_de"][idx]]
    alto = terc_op == 2
    acierta5 = rng.random(len(idx)) < Q5
    lado5 = np.where(alto, np.where(acierta5, mejor_largo, ~mejor_largo), rng.random(len(idx)) < 0.5)
    c5c = candidato("C5_un_regimen", m, idx, lado5)
    v, s = juzgar("C5", c5c, m, registro_nuevo("c5"))
    if s: resumen(s)
    resultados["C5"] = (v == "APUESTA AL REGIMEN", v)

    # ---------------------------------------------------------------- C6 ataque A1
    print("\nC6  ATAQUE A1: solo-largo restringido a 2017. Esperado NO SUPERA con la defensa.")
    idx6 = grilla(m, [2017])
    c6c = candidato("C6_solo_largo_2017", m, idx6, np.ones(len(idx6), bool))
    v, s = juzgar("C6 con defensa", c6c, m, registro_nuevo("c6"))
    if s: resumen(s)
    resultados["C6"] = (v == "NO SUPERA", v)
    if s:
        B6 = s["periodos"]["trabajo"]["nulas"]["B signo"]
        print(f"      LECTURA: la nula de signo SOLA lo aprobaria a {B6[3]:+.1f}sd. Lo frenan la rotacion "
              f"DENTRO del rango y la pasiva: la defensa de A1 es lo que actua.")
    v2, s2 = juzgar("C6 SIN defensa (rotacion global, solo para ver que hace falta)", c6c, m,
                    registro_nuevo("c6b"), rotacion_global=True)
    if s2:
        resumen(s2)
    else:
        print("      LECTURA: sin la defensa, la rotacion GLOBAL de un candidato de UN anio reparte sus "
              "entradas por cuatro anios de regimenes distintos y su desvio se dispara: el juez ni "
              "siquiera puede decidir. La nula global es ruido para un candidato de periodo corto; "
              "la defensa no solo cierra el ataque, tambien devuelve la resolucion.")

    # ---------------------------------------------------------------- C7 ventaja solo bajista
    print(f"\nC7  VENTAJA SOLO EN TENDENCIAS BAJISTAS (mov. neto de las 20 sesiones anteriores < 0; "
          f"q={Q7}). Esperado APUESTA AL REGIMEN. Falla si SUPERA.")
    mov = np.array([m["cl"][b - 1] - m["cl"][a] for a, b in zip(m["ini"], m["fin"])])
    cum = np.concatenate([[0.0], np.cumsum(mov)])
    dir20 = np.array([np.sign(cum[k] - cum[k - 20]) if k >= 20 else 0.0 for k in range(m["nses"])])
    baja = dir20[m["ses_de"][idx]] < 0
    acierta7 = rng.random(len(idx)) < Q7
    lado7 = np.where(baja, np.where(acierta7, mejor_largo, ~mejor_largo), rng.random(len(idx)) < 0.5)
    c7c = candidato("C7_solo_bajista", m, idx, lado7)
    v, s = juzgar("C7", c7c, m, registro_nuevo("c7"))
    if s: resumen(s)
    print(f"      slots en sesion bajista: {int(baja.sum())} de {len(idx)} ({baja.mean()*100:.0f}%). "
          f"La ventaja concentrada ahi tiene que aparecer en el tercil ALTO de volatilidad, no repartida.")
    resultados["C7"] = (v == "APUESTA AL REGIMEN", v)

    # ---------------------------------------------------------------- C8 candidato en el borde
    print(f"\nC8  CANDIDATO EN EL BORDE (q={Q8}, entre el piso pasivo y el de cruce). Prueba la frontera")
    print(f"    entre modos, donde el desplazamiento de nivel podria hacer dano. Esperado: NO APRUEBA en")
    print(f"    ninguno de los dos modos (NO SUPERA / APUESTA / REQUIERE MEDICION), NUNCA SUPERA. Falla si SUPERA.")
    rng8 = np.random.default_rng(SEMILLA_C8)     # dedicada: el borde no puede depender del sorteo compartido
    acierta8 = rng8.random(len(idx)) < Q8
    lado8 = np.where(acierta8, mejor_largo, ~mejor_largo)
    c8c = candidato("C8_borde", m, idx, lado8)
    v, s = juzgar("C8", c8c, m, registro_nuevo("c8"))
    if s:
        resumen(s)
    # el invariante robusto es "no SUPERA en el borde"; la categoria exacta de no-aprobacion depende
    # del sorteo (que aguanten o no los tres terciles) y no se fija. La conversion SUPERA->REQUIERE
    # MEDICION la ejercita C2 de forma estable (ventaja grande, SUPERA firme en cruce).
    NO_APRUEBA = {"NO SUPERA", "APUESTA AL REGIMEN", J.REQUIERE_MEDICION}
    resultados["C8"] = (v in NO_APRUEBA, v)

    # ------------------------------------------------- C9/C10 la clase de ventaja y la puerta trasera
    prom = (dL + dS) / 2.0
    # el mejor tercio de ranuras DENTRO DE CADA TERCIL de volatilidad: asi la ventaja de timing queda
    # repartida por regimen y el control aisla el timing puro, sin mezclarlo con concentracion de
    # regimen. (Con seleccion GLOBAL el mismo candidato da APUESTA AL REGIMEN: la ventaja existe y el
    # juez la ve, pero vive en un regimen. Son dos propiedades distintas y este control mide una.)
    terc_op = m["tercil_exante"][m["ses_de"][idx]]
    sel = np.zeros(len(idx), bool)
    for t in (0, 1, 2):
        mk = terc_op == t
        if mk.any():
            sel |= mk & (prom >= np.quantile(prom[mk], 2 / 3))
    print(f"\nC9  VENTAJA DE TIMING declarada BIEN (lado al azar, mejor tercio DENTRO de cada tercil).")
    print(f"    Esperado: SUPERA / REQUIERE MEDICION. La nula de signo no puede verla y se omite si la firma confirma.")
    lado9 = rng.random(int(sel.sum())) < 0.5
    c9c = candidato("C9_timing_declarado", m, idx[sel], lado9, clase="timing")
    v, s = juzgar("C9", c9c, m, registro_nuevo("c9"))
    if s:
        resumen(s)
        r9 = s["periodos"]["trabajo"]
        print(f"      clase declarada {r9['clase_declarada']} / firma medida {r9['firma']}   "
              f"omite signo: {r9['aplica_timing']}   z_info {r9['z_info']:+.1f} (estricto seria {r9['z_estricto']:+.1f})")
    resultados["C9"] = (v in ("SUPERA", J.REQUIERE_MEDICION), v)

    print(f"\nC10 LA PUERTA TRASERA: candidato SIN ventaja que declara 'timing'. Esperado NO SUPERA igual.")
    print(f"    Falla si declarar una clase falsa lo hace pasar.")
    c10c = candidato("C10_nulo_declara_timing", m, idx, moneda, clase="timing")
    v, s = juzgar("C10", c10c, m, registro_nuevo("c10"))
    if s:
        resumen(s)
        r10 = s["periodos"]["trabajo"]
        print(f"      clase declarada {r10['clase_declarada']} / firma medida {r10['firma']}   "
              f"omite signo: {r10['aplica_timing']}   z_info {r10['z_info']:+.1f}")
    # estricto a proposito: un candidato NULO tiene que ser rechazado de plano, declare lo que declare.
    # Si declarar 'timing' lo moviera aunque sea a APUESTA, la declaracion estaria comprando algo.
    resultados["C10"] = (v == "NO SUPERA", v)

    # ---------------------------------------------------------------- demostracion: contador
    print("\nDEMOSTRACION (no es control): el contador de familia.")
    reg = registro_nuevo("contador")
    juzgar("C2 en registro limpio", c2c, m, reg)
    v, s = juzgar("C1 despues, misma huella", c1c, m, reg)
    if s:
        print(f"      hermanos detectados: {len(s['hermanos'])}   variantes totales: {s['variantes_total']}   "
              f"umbral exigido: {s['periodos']['trabajo']['z_req']:.2f} desvios (base {J.Z_BASE:.1f})")
        for f, j, como in s["hermanos"]:
            print(f"         {f.get('nombre')}  {f.get('veredicto')}  ({como})")
    filas, ok, rota = J.leer_registro(reg)
    with open(reg, "a", encoding="utf-8") as f:
        f.write('{"cuando":"editado","hash":"0000","prev_hash":"nada"}\n')
    _, ok2_, rota2 = J.leer_registro(reg)
    print(f"      cadena antes de alterar: {'OK' if ok else 'ROTA'}   despues de alterar: "
          f"{'OK' if ok2_ else f'ROTA en linea {rota2}'}")

    # ---------------------------------------------------------------- resumen
    print("\n" + "=" * 100)
    n_ok = sum(1 for ok, _ in resultados.values() if ok)
    for k, (ok, v) in resultados.items():
        print(f"   {k}: {'PASADO' if ok else 'FALLADO'}   (veredicto: {v})")
    print(f"\n   {n_ok} de {len(resultados)} controles PASADOS.  [MODO {'PASIVO' if pasivo else 'CRUCE'}]")
    print("=" * 100)
    return resultados


def main():
    m = J.cargar_mercado()
    res_cruce = correr(False, m)
    res_pas = correr(True, m)
    n = len(res_cruce)
    print("\n" + "#" * 100)
    print("COMPARACION DE MODOS. Regla: el modo PASIVO nunca aprueba (nunca SUPERA); una cota optimista")
    print("solo sirve para rechazar. Un SUPERA de cruce se vuelve REQUIERE MEDICION en pasivo, y un")
    print("candidato en el borde (C8) que cruce NO SUPERA puede volverse REQUIERE MEDICION -nunca SUPERA-.")
    print("LO HARIA FALLAR: que cualquier corrida en PASIVO devuelva SUPERA.")
    print("#" * 100)
    # ancho fijo >= el veredicto mas largo ("REQUIERE MEDICION PASIVA POR CANDIDATO", 38): con 28 las
    # dos columnas se pegaban y la tabla mentia sobre donde termina una y empieza la otra.
    W = max(len(v[1]) for v in list(res_cruce.values()) + list(res_pas.values())) + 2
    print(f"   {'control':>8}  {'CRUCE':<{W}}{'PASIVO':<{W}}")
    hay_supera_pasivo = False
    for k in res_cruce:
        vc = res_cruce[k][1]; vp = res_pas[k][1]
        if vp == "SUPERA":
            hay_supera_pasivo = True
        print(f"   {k:>8}  {vc:<{W}}{vp:<{W}}")
    nc = sum(1 for ok, _ in res_cruce.values() if ok)
    npa = sum(1 for ok, _ in res_pas.values() if ok)
    print(f"\n   controles pasados: CRUCE {nc}/{n}   PASIVO {npa}/{n}")
    print(f"   SUPERA en modo pasivo (tiene que ser NINGUNO): "
          f"{'HAY - FALLA' if hay_supera_pasivo else 'ninguno - OK'}")
    print("#" * 100)
    if nc < n or npa < n or hay_supera_pasivo:
        raise SystemExit("FALLO: algun control fallo, o el modo pasivo devolvio SUPERA")


if __name__ == "__main__":
    main()
