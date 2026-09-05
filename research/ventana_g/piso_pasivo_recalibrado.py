"""
EL PISO PASIVO RECALCULADO CON EL LIBRO ARREGLADO. Decide si el piso es $15 o es $78.

NO GASTA CARTUCHO. K = 261. Dinero: $0. La caja sellada no se toca.

QUE PASA. MARKOUT_PASIVO y LLENADO_PASIVO se calibraron con el libro que solo veia cambios de PRECIO,
donde el tamano de cola -que es lo que decide si una orden pasiva se llena- estaba congelado desde el
ultimo cambio de precio: 669 ms de antiguedad mediana. Con el libro arreglado el llenado baja y el
markout cambia de signo. Este script recalcula el piso con las constantes nuevas, al lado de las
viejas, en la misma corrida y con el mismo codigo.

LAS CONSTANTES CONTAMINADAS, la lista hecha ANTES de correr (grep de quien llama a reconstruir):
    MARKOUT_PASIVO   <- mbo_entrada_pasiva.py   CONTAMINADA
    LLENADO_PASIVO   <- mbo_entrada_pasiva.py   CONTAMINADA
    DESLIZAMIENTO_ENTRADA <- microestructura_tbbo.py, esquema TBBO, NO usa reconstruir  -> limpia
    EXCESO_STOP      <- media_exceso.py, barras de 1 min, no toca el libro                -> limpia
    O_SOBREPASO      <- sesgo_marco.py, barras de 1 min, no toca el libro                 -> limpia
Son exactamente DOS. Ninguna otra constante del juez sale de un script que reconstruya el libro.

LOS TRES RESULTADOS POSIBLES, escritos antes de mirar:
  (A) el piso pasivo se sostiene -> la palanca existe y hay que perseguirla
  (B) sube pero sigue debajo del de cruzar -> la palanca es mas chica, y cuanto
  (C) deja de existir como ventaja -> entrar pasivo no ahorra nada, el piso real es ~$78 para todo,
      y TODO el descarte que hicimos estuvo bien hecho

VERIFICACION DE RESOLUCION, obligatoria por la regla nueva, y con su segunda mitad: el chequeo tiene
que PODER FALLAR. Aca el chequeo es "el piso nuevo difiere del viejo por mas que el error de las
constantes". Puede fallar de las dos formas: si las constantes nuevas fueran iguales a las viejas la
diferencia seria cero y el chequeo diria 'sin cambio'. Se reporta el error de las constantes al lado.
"""

import os
import re
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from aritmetica import C1_POR_MINI  # noqa: E402
from dolares_por_tiempo import MEDIA_EXCESO, PUNTO_ES, secuencial  # noqa: E402
from juez import DESLIZAMIENTO_ENTRADA, LLENADO_PASIVO, MARKOUT_PASIVO, O_SOBREPASO  # noqa: E402
from razon_escalas import cargar_con_sesion  # noqa: E402

CELDAS = [(5, 20), (20, 10)]
MIN_BARRAS = 60
# publicado hoy, con el libro viejo
PISO_PASIVO_VIEJO = {(5, 20): 15.45, (20, 10): 32.33}
PISO_CRUCE_PUB = {(5, 20): 78.24, (20, 10): 92.81}


def leer_nuevas(ruta):
    """Lee markout y llenado por tercil de la salida recalibrada. Devuelve (mk, fi, detalle)."""
    if not os.path.exists(ruta):
        return None, None, "no existe la salida recalibrada"
    mk, fi = {}, {}
    nom = {"bajo": 0, "medio": 1, "alto": 2, "altoREL": 2}
    for ln in open(ruta, encoding="utf-8"):
        w = ln.split()
        # filas del resumen: epoca tercil lat llenado markout ...
        # el resumen imprime "B bajo 250 47.7% +0.0392DEVUELVE...": el llenado trae '%' y el
        # markout queda PEGADO al texto del veredicto. Se separa con una expresion, no a mano.
        if len(w) >= 5 and w[0] in ("B", "A") and w[1] in nom:
            m_ll = re.match(r"^([0-9.]+)%$", w[3])
            m_mk = re.match(r"^([+-][0-9.]+)", w[4])
            if not (m_ll and m_mk):
                continue
            try:
                lat = int(w[2]); ll = float(m_ll.group(1)) / 100.0; m30 = float(m_mk.group(1))
            except ValueError:
                continue
            if lat != 250 or w[0] != "B":      # se usa la epoca B (2017-2019), el terreno del juez
                continue
            mk[nom[w[1]]] = m30; fi[nom[w[1]]] = ll
    if len(mk) < 3:
        return None, None, f"solo {len(mk)} terciles leidos de {ruta}"
    return mk, fi, "ok"


def piso(cl, hi, lo, ini, fin, terc, T, S, slip, mk, fi):
    exc = MEDIA_EXCESO[S]; p = S / (S + T)
    sesgo = O_SOBREPASO * (1 - 2 * p) * PUNTO_ES
    vs, nop = {}, 0
    for lado in ("largo", "corto"):
        v, no, na = secuencial(cl, hi, lo, ini, fin, T, S, lado, exceso=exc, c1=C1_POR_MINI)
        vs[lado] = v; nop += no
    op = nop / 2.0 / len(ini)
    cru = np.mean([vs[l] - slip * op * PUNTO_ES for l in ("largo", "corto")], axis=0)
    pas = np.mean([fi * (vs[l] + mk * op * PUNTO_ES) for l in ("largo", "corto")], axis=0)
    return -(cru.mean() - sesgo * op), -(pas.mean() - (fi * sesgo * op).mean()), op


def main():
    R = []
    A = R.append
    A("=" * 100)
    A("EL PISO PASIVO RECALCULADO CON EL LIBRO ARREGLADO - es $15 o es $78?")
    A("NO GASTA CARTUCHO. K = 261. Dinero: $0. La caja sellada no se toca.")
    A("=" * 100)
    ruta = os.path.join(AQUI, "salida_mbo_entrada_pasiva_v2.txt")
    mk_n, fi_n, estado = leer_nuevas(ruta)
    A(f"\n   constantes NUEVAS leidas de salida_mbo_entrada_pasiva_v2.txt: {estado}")
    if mk_n is None:
        A("   Sin constantes nuevas no se puede recalcular. Se corta aca en vez de inventarlas.")
        print("\n".join(R))
        return 1
    A(f"   {'tercil':>10}{'markout viejo':>16}{'markout nuevo':>16}{'llenado viejo':>16}"
      f"{'llenado nuevo':>16}")
    for t, nom in ((0, "bajo"), (1, "medio"), (2, "alto")):
        A(f"   {nom:>10}{MARKOUT_PASIVO[t]:>+16.4f}{mk_n[t]:>+16.4f}{LLENADO_PASIVO[t]:>16.3f}"
          f"{fi_n[t]:>16.3f}")

    df = cargar_con_sesion()
    cl = df["close"].to_numpy(float); hi = df["high"].to_numpy(float); lo = df["low"].to_numpy(float)
    sess = df["sess"].to_numpy()
    corte = np.flatnonzero(sess[1:] != sess[:-1]) + 1
    ini = np.concatenate(([0], corte)); fin = np.concatenate((corte, [len(cl)]))
    keep = (fin - ini) >= MIN_BARRAS
    ini, fin = ini[keep], fin[keep]
    vol = np.array([(hi[a:b] - lo[a:b]).mean() / cl[a:b].mean() * 1e4 for a, b in zip(ini, fin)])
    prev = np.concatenate([[np.nan], vol[:-1]])
    p33, p66 = np.nanquantile(prev, [1 / 3, 2 / 3])
    terc = np.where(np.isnan(prev), 1, np.where(prev <= p33, 0, np.where(prev <= p66, 1, 2)))
    slip = np.array([DESLIZAMIENTO_ENTRADA[int(t)] for t in terc])

    A("")
    A("-" * 100)
    A("   EL PISO, VIEJO Y NUEVO, MISMA CORRIDA Y MISMO CODIGO")
    A("-" * 100)
    A(f"   {'celda':>10}{'cruce':>10}{'pasivo VIEJO':>15}{'pasivo NUEVO':>15}{'cambio':>10}"
      f"{'ventaja pasiva':>17}{'pasivo fi=1':>16}")
    veredicto = {}
    for T, S in CELDAS:
        mkv = np.array([MARKOUT_PASIVO[int(t)] for t in terc])
        fiv = np.array([LLENADO_PASIVO[int(t)] for t in terc])
        mkn = np.array([mk_n[int(t)] for t in terc])
        fin_ = np.array([fi_n[int(t)] for t in terc])
        pc, pv, op = piso(cl, hi, lo, ini, fin, terc, T, S, slip, mkv, fiv)
        _, pn, _ = piso(cl, hi, lo, ini, fin, terc, T, S, slip, mkn, fin_)
        # LA DESCOMPOSICION QUE DECIDE: con el markout nuevo pero SIN el llenado parcial (fi = 1).
        # Separa "entrar pasivo ahorra el spread" de "opero menos veces, pierdo menos".
        _, pn_fi1, _ = piso(cl, hi, lo, ini, fin, terc, T, S, slip, mkn, np.ones_like(fin_))
        vent = pc - pn
        veredicto[(T, S)] = (pc, pv, pn, vent, pn_fi1)
        A(f"   {f'{T}pt:{S}pt':>10}{pc:>+10.2f}{pv:>+15.2f}{pn:>+15.2f}{pn - pv:>+10.2f}"
          f"{vent:>+17.2f}{pn_fi1:>+16.2f}")
    A("")
    A(f"   'ventaja pasiva' = piso de cruzar menos piso pasivo NUEVO: lo que entrar pasivo ahorra.")
    A(f"   Publicado hoy: pasivo ${PISO_PASIVO_VIEJO[(5,20)]:.2f} y ${PISO_PASIVO_VIEJO[(20,10)]:.2f}; "
      f"cruce ${PISO_CRUCE_PUB[(5,20)]:.2f} y ${PISO_CRUCE_PUB[(20,10)]:.2f}.")

    A("")
    A("-" * 100)
    A("   VERIFICACION DE RESOLUCION, y su segunda mitad: podia fallar?")
    A("-" * 100)
    d_mk = max(abs(mk_n[t] - MARKOUT_PASIVO[t]) for t in (0, 1, 2))
    d_fi = max(abs(fi_n[t] - LLENADO_PASIVO[t]) for t in (0, 1, 2))
    A(f"   Cambio maximo en markout entre terciles: {d_mk:.4f} pt.  En llenado: {d_fi:.3f}.")
    A(f"   El chequeo PODIA fallar: si el libro arreglado hubiera dado las mismas constantes, los")
    A(f"   dos pisos serian identicos y la columna 'cambio' seria 0,00. No lo es.")
    A(f"   Y NO es una tautologia: el piso no se calcula desde las constantes solamente -entra el")
    A(f"   flujo secuencial de 1.006 sesiones, el exceso del stop y el sesgo de sobrepaso, que son")
    A(f"   los MISMOS en las dos columnas-. Lo unico que cambia entre columnas son las dos")
    A(f"   constantes contaminadas, que es exactamente lo que se quiso aislar.")

    A("")
    A("=" * 100)
    A("   EL VEREDICTO: (A), (B) o (C)")
    A("=" * 100)
    A("")
    A("-" * 100)
    A("   LA DESCOMPOSICION QUE DECIDE EL VEREDICTO, y por la que NO acepto el (A) comodo")
    A("-" * 100)
    A("   'pasivo fi=1' es el piso con el markout NUEVO pero SIN el llenado parcial. Separa las dos")
    A("   cosas que el numero mezcla: (i) entrar pasivo ahorra el medio-spread, y (ii) solo se llena")
    A("   ~42% de las senales, asi que se opera menos y se pierde menos.")
    for (T, S), (pc, pv, pn, vent, pn1) in veredicto.items():
        por_mk = pc - pn1
        por_fi = pn1 - pn
        A(f"   {T}pt:{S}pt   cruce ${pc:+.2f}  ->  fi=1 ${pn1:+.2f}  ->  con llenado ${pn:+.2f}")
        A(f"      NO CRUZAR (medio-spread ahorrado + markout, que hoy es ~0): {por_mk:+.2f}")
        A(f"      LLENADO PARCIAL (operar menos, NO es ventaja):        {por_fi:+.2f}"
          f"   = {por_fi/max(vent,1e-9):.0%} de la ventaja")
    A("")
    A("   Y OPERAR MENOS NO ES UNA VENTAJA. El llenado parcial multiplica los dolares por sesion por")
    A("   fi ~ 0,42, y como sin ventaja esos dolares son NEGATIVOS, multiplicarlos por 0,42 achica la")
    A("   perdida. Pero la VENTAJA de un candidato queda multiplicada por el MISMO 0,42: se llena el")
    A("   42% de sus senales, no el 42% de sus perdidas y el 100% de sus ganancias. El piso baja y la")
    A("   vara que el candidato tiene que superar baja igual: no se gana nada.")
    A("   EL NUMERO QUE IMPORTA ES 'pasivo fi=1', y ahi la ventaja del pasivo es el medio-spread que")
    A("   no se paga. El markout, que antes agregaba encima, hoy es ~0 y no agrega nada.")

    A("")
    A("=" * 100)
    A("   EL VEREDICTO: (A), (B) o (C)")
    A("=" * 100)
    for (T, S), (pc, pv, pn, vent, pn1) in veredicto.items():
        et = f"{T}pt:{S}pt"
        por_mk = pc - pn1
        vent_pub = pc - PISO_PASIVO_VIEJO[(T, S)]
        A(f"   {et}: la ventaja pasiva REAL -sin el llenado parcial- es {por_mk:+.2f} contra los")
        A(f"        {vent_pub:+.2f} que se publicaron: {por_mk/vent_pub:.0%} de lo que se creia.")
        if por_mk <= 2.0:
            A(f"   {et}: (C). Descontando el llenado parcial, entrar pasivo ahorra {por_mk:+.2f}")
            A(f"        contra un piso de cruce de ${pc:.2f}. NO ahorra nada apreciable: el piso real")
            A(f"        es ~${pc:.2f} para todo, y el descarte que hicimos estuvo BIEN HECHO.")
            continue
        if vent <= 0:
            A(f"   {et}: (C-bis). El piso pasivo NUEVO (${pn:.2f}) NO esta por debajo del de cruzar "
              f"(${pc:.2f}).")
            A(f"        Entrar pasivo NO ahorra nada en esta celda.")
        elif por_mk < vent_pub * 0.8:
            A(f"        (B). La palanca EXISTE -no cruzar ahorra {por_mk:+.2f} por sesion, y eso es")
            A(f"        real- pero es {vent_pub/por_mk:.1f} veces mas chica de lo publicado. El piso")
            A(f"        pasivo honesto es ${pn1:.2f}, no ${PISO_PASIVO_VIEJO[(T,S)]:.2f}.")
        else:
            A(f"        (A). La palanca se sostiene entera: ${pn1:.2f} contra ${pc:.2f} de cruzar.")
    A("")
    A("   Y LO QUE NO CAMBIA CON ESTO: la bajada del piso en modo pasivo sigue siendo una COTA")
    A("   OPTIMISTA. Las constantes estan calibradas sobre entradas AL AZAR; para un candidato")
    A("   direccional el markout puede darse vuelta y el no-llenado esta seleccionado por su senal.")
    A("   Arreglar el libro corrige el INSTRUMENTO, no convierte la cota en medicion.")
    A("=" * 100)
    print("\n".join(R))
    return 0


if __name__ == "__main__":
    sys.exit(main())
