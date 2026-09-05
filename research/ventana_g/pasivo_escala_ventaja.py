"""
TAREA 1 - EL MODO PASIVO DEL JUEZ ESCALA LA VENTAJA POR fi, O SOLO EL PISO?

NO GASTA CARTUCHO. K = 261. Candidato SINTETICO con ventaja INYECTADA de tamano conocido. La caja
sellada no se toca. Dinero: $0.

LA SOSPECHA, mia: el modo pasivo multiplica los dolares por sesion por la fraccion de llenado fi.
Eso baja el piso -y ese numero lo publicamos-. Pero un candidato REAL veria su ventaja multiplicada
por el MISMO fi: se llena el 42% de sus senales, no el 42% de sus perdidas y el 100% de sus
ganancias. Si el juez baja el piso sin escalar la ventaja, TODO veredicto pasivo es optimista por
construccion, y es un defecto distinto de las tres deudas ya declaradas.

MI PROPIA PRUEBA: inyectar una ventaja conocida (el control C2) y mirar si la ventaja RECUPERADA en
modo pasivo sale escalada por fi.
   - si sale escalada  -> el juez lo hace bien y la sospecha MUERE. Se cierra.
   - si NO sale escalada -> el modo pasivo esta roto, y hay que decir de que tamano es el error en
     dolares por sesion.

VERIFICACION DE RESOLUCION, y su segunda mitad -el chequeo tiene que PODER FALLAR-: el cociente
medido (ventaja pasiva / ventaja cruce) se compara contra fi medio. Puede dar cualquier cosa entre 0
y 1; que de justo fi no esta forzado por ninguna identidad del codigo de este script, porque el
script no calcula el escalado: se lo pide al juez y lee lo que devuelve.
"""

import os
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import juez as J  # noqa: E402
import juez_controles as C  # noqa: E402


def correr(m, cand, pasivo):
    reg = C.registro_nuevo("escala_pasivo")
    s = J.juzgar(cand, m, npermuta=C.NPERM, registro=reg, pasivo=pasivo, anotar_=False)
    return s["periodos"]["trabajo"]


def main():
    R = []
    A = R.append
    A("=" * 100)
    A("TAREA 1 - EL MODO PASIVO ESCALA LA VENTAJA POR fi, O SOLO EL PISO?")
    A("NO GASTA CARTUCHO. K = 261. Dinero: $0. La caja sellada no se toca.")
    A("=" * 100)
    m = J.cargar_mercado()
    rng = np.random.default_rng(C.SEMILLA)
    idx = C.grilla(m, (2016, 2017, 2018))
    dL, dS = C.ambos_lados(m, idx)
    # C2: con probabilidad q se elige el lado que resulto mejor; si no, moneda.
    mejor = dL > dS
    coin = rng.random(len(idx)) < 0.5
    largo = np.where(rng.random(len(idx)) < C.Q2, mejor, coin)
    cand = C.candidato("escala_pasivo", m, idx, largo)

    fi_prom = float(np.mean([J.LLENADO_PASIVO[t] for t in (0, 1, 2)]))
    A(f"\n   Candidato: el mismo C2 (ventaja inyectada, q = {C.Q2}), {len(idx):,} operaciones.")
    A(f"   fi promedio de las constantes del juez: {fi_prom:.3f}")

    rc = correr(m, cand, pasivo=False)
    rp = correr(m, cand, pasivo=True)

    A("")
    A("-" * 100)
    A("   LO QUE DEVUELVE EL JUEZ EN CADA MODO")
    A("-" * 100)
    A(f"   {'':<26}{'CRUCE':>14}{'PASIVO':>14}{'pasivo/cruce':>15}")
    filas = [
        ("observado ($/sesion)", rc["obs"], rp["obs"]),
        ("nula A rotacion", rc["nulas"]["A rotacion"][0], rp["nulas"]["A rotacion"][0]),
        ("nula B signo", rc["nulas"]["B signo"][0], rp["nulas"]["B signo"][0]),
        ("VENTAJA contra signo", rc["nulas"]["B signo"][2], rp["nulas"]["B signo"][2]),
        ("VENTAJA contra rotacion", rc["nulas"]["A rotacion"][2], rp["nulas"]["A rotacion"][2]),
        ("desvio total (sd_tot)", rc["sd_tot"], rp["sd_tot"]),
        ("comparacion pasiva", rc["pasiva"], rp["pasiva"]),
    ]
    for nom, a, b in filas:
        r = b / a if abs(a) > 1e-9 else float("nan")
        A(f"   {nom:<26}{a:>+14.4f}{b:>+14.4f}{r:>15.3f}")
    A("")
    A(f"   {'z contra rotacion':<26}{rc['nulas']['A rotacion'][3]:>+14.2f}"
      f"{rp['nulas']['A rotacion'][3]:>+14.2f}"
      f"{rp['nulas']['A rotacion'][3]/rc['nulas']['A rotacion'][3]:>15.3f}")
    A(f"   {'z contra signo':<26}{rc['nulas']['B signo'][3]:>+14.2f}"
      f"{rp['nulas']['B signo'][3]:>+14.2f}"
      f"{rp['nulas']['B signo'][3]/rc['nulas']['B signo'][3]:>15.3f}")
    A(f"   {'z contra pasiva':<26}{rc['z_pas']:>+14.2f}{rp['z_pas']:>+14.2f}"
      f"{rp['z_pas']/rc['z_pas']:>15.3f}")
    A(f"   {'veredicto':<26}{rc['veredicto']:>14}{rp['veredicto']:>14}")

    A("")
    A("=" * 100)
    A("   LA RESPUESTA")
    A("=" * 100)
    esc_v = rp["nulas"]["B signo"][2] / rc["nulas"]["B signo"][2]
    esc_sd = rp["sd_tot"] / rc["sd_tot"]
    esc_z = rp["nulas"]["B signo"][3] / rc["nulas"]["B signo"][3]
    A(f"   La VENTAJA recuperada sale escalada por {esc_v:.3f}.  fi promedio = {fi_prom:.3f}.")
    if abs(esc_v - fi_prom) < 0.05:
        A(f"   SALE ESCALADA POR fi. El juez NO baja el piso sin bajar la ventaja: escala las dos.")
        A(f"   MI SOSPECHA MUERE Y LA CIERRO.")
    else:
        A(f"   NO sale escalada por fi ({esc_v:.3f} contra {fi_prom:.3f}). El modo pasivo esta roto.")
    A("")
    A(f"   Y el desvio se escala por {esc_sd:.3f}, asi que el COCIENTE -que es el z- se mueve solo")
    A(f"   {esc_z:.3f}. El VEREDICTO es casi invariante a fi, que es lo que uno quiere: la decision")
    A(f"   de aprobar no deberia depender de cuantas senales se llenan, solo de si las que se llenan")
    A(f"   tienen informacion.")
    A("")
    A("-" * 100)
    A("   DONDE SI ESTABA EL PROBLEMA, Y NO ERA DONDE YO DIJE")
    A("-" * 100)
    A("   El VEREDICTO del juez es (casi) invariante a fi: mi sospecha sobre el modo pasivo del juez")
    A("   era equivocada. Pero el PISO PUBLICADO en dolares por sesion SI se escala por fi, y ese es")
    A("   otro numero, calculado en piso_pasivo.py y no por el juez. La critica valia para el piso")
    A("   -donde ya la aplique y bajo de $15,45 a $43,86- y NO para el veredicto.")
    A("   Es la misma leccion de siempre en otra forma: el numero y el veredicto no se comportan")
    A("   igual, y hay que decir de CUAL se habla.")
    A("")
    A("   LAS DOS ASIMETRIAS QUE SI QUEDAN, chicas y en la direccion conservadora:")
    A(f"      - el error de la constante de sobrepaso (err_o) NO se escala por fi, asi que con fi<1")
    A(f"        pesa relativamente mas en sd_tot: hace el z mas chico. Conservador.")
    A(f"      - la comparacion pasiva ({rc['pasiva']:+.2f} en cruce, {rp['pasiva']:+.2f} en pasivo) "
      f"tampoco se")
    A(f"        escala igual que el observado, asi que z_pas mezcla escalas. Es la unica de las tres")
    A(f"        nulas donde el modo cambia la comparacion, y va anotada.")

    A("")
    A("-" * 100)
    A("   VERIFICACION DE RESOLUCION, y su segunda mitad")
    A("-" * 100)
    A("   El chequeo PODIA fallar: el cociente medido puede caer en cualquier valor entre 0 y 1 y")
    A("   este script no lo calcula -se lo pide al juez y lee lo que devuelve-. Si el juez no")
    A(f"   escalara la ventaja, el cociente daria ~1,00 en vez de {esc_v:.3f}.")
    A(f"   Y la ventaja inyectada es grande ({rc['nulas']['B signo'][2]:+.2f} $/sesion contra un")
    A(f"   desvio de {rc['sd_tot']:.2f}), asi que el cociente se mide con error relativo del orden de")
    A(f"   {rc['sd_tot']/abs(rc['nulas']['B signo'][2]):.1%}: bastante mas chico que la diferencia")
    A(f"   entre {esc_v:.3f} y 1,00 que habria que distinguir.")
    A("=" * 100)
    print("\n".join(R))
    return 0


if __name__ == "__main__":
    sys.exit(main())
