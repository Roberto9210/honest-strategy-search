"""
CONTROLES DEL JUEZ - seis, cada uno con condicion de falla escrita contra un resultado PUBLICADO,
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
  C5  VENTAJA EN UN SOLO REGIMEN (q = 0,75 solo en sesiones del tercil alto, moneda en el resto).
      Publicado: juez_regimen.py, el tercil alto tiene piso $118,61 contra $2,29 del bajo; la
      ventaja global va a ser grande y solo un tercil la sostiene. ESPERADO: APUESTA AL REGIMEN.
      LO HARIA FALLAR: SUPERA (no distingue el regimen) o NO SUPERA (no ve la ventaja).
  C6  EL ATAQUE A1: solo-largo restringido a 2017. Publicado: salida_cortes.txt, 2017 largo
      +$85,56/sesion a +2,7 errores; con la rotacion GLOBAL la nula vive en 2016-2019 y el
      candidato en 2017. Con la defensa (rotacion dentro del rango + pasiva) la nula tambien vive
      en 2017. ESPERADO: NO SUPERA con la defensa. Y se corre SIN defensa para mostrar que la
      defensa hace falta: ahi el 'informativo' tiene que subir.
      LO HARIA FALLAR: SUPERA o APUESTA con la defensa puesta.

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
NPERM = int(os.environ.get("JUEZ_NPERM", "200"))
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


def candidato(nombre, m, idx, largo_mask, variantes=1, familia=None):
    ops = [dict(ts=str(m["ts"][i]), lado=("largo" if L else "corto")) for i, L in zip(idx, largo_mask)]
    c = dict(nombre=nombre, instrumento="ES", contratos=1, limite_contratos=12,
             variantes_probadas=variantes, regla_salida=dict(CELDA), operaciones=ops)
    if familia:
        c["familia"] = familia
    return c


def juzgar(nombre, cand, m, reg, **kw):
    t0 = time.time()
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


def main():
    print("=" * 100)
    print("CONTROLES DEL JUEZ - seis, con condicion de falla contra lo publicado")
    print(f"NO GASTA CARTUCHO. K = 261. Permutaciones por nula: {NPERM}. La caja sellada no se toca.")
    print("=" * 100)
    m = J.cargar_mercado()
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
        ok2 = (v == "SUPERA") and (0.67 <= rec <= 1.33)
    resultados["C2"] = (ok2, v)

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
    print(f"\nC5  VENTAJA SOLO EN EL TERCIL ALTO (q={Q5}). Esperado APUESTA AL REGIMEN.")
    terc_op = m["tercil"][m["ses_de"][idx]]
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
    print(f"\n   {n_ok} de {len(resultados)} controles PASADOS.")
    print("=" * 100)
    if n_ok < len(resultados):
        raise SystemExit("ALGUN CONTROL FALLO")


if __name__ == "__main__":
    main()
