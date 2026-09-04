"""
VENTANA G - la cadena completa con el TERCER ESTADO: "abierta al corte".

NO GASTA CARTUCHO. K = 261.

sim_bracket suponia resolucion del 100%: cada operacion era win o -loss. Medido, entre el
7% y el 35% no resuelve en una sesion, y esas no valen cero: valen su marca a mercado, que
se midio en abiertas_al_corte.py.

CONTROL: con la fraccion abierta en cero el modelo nuevo tiene que devolver EXACTAMENTE lo
mismo que el viejo. Si no coincide, el estado nuevo metio algo mas que el efecto buscado.
"""
import os

import numpy as np

from aritmetica import C1_POR_MICRO_VIA_MINI, FIRMAS
from bracket import sim_bracket
from vara_criterio import MAX_DAYS_FUND, SEMILLA, acierto_sin_ventaja, p_equilibrio

AQUI = os.path.dirname(os.path.abspath(__file__))
FIRMA = "Tradeify Growth (50K)"
N = 10
C1 = C1_POR_MICRO_VIA_MINI
NPATHS = 60_000
MEDIA_EXCESO = {10: 0.722, 20: 0.982}
CELDAS = [(5, 10), (10, 10), (20, 10), (5, 20), (10, 20)]

# Medido en abiertas_al_corte.py, horizonte de una sesion, pooled sobre los dos lados.
P_ABIERTA = {(5, 10): 0.071, (10, 10): 0.189, (20, 10): 0.354,
             (5, 20): 0.174, (10, 20): 0.354}
# Tasa de acierto entre las RESUELTAS, tambien medida (linea_base.py, 1 sesion, pooled).
# Va junto con P_ABIERTA y no se puede mezclar con la asumida: ver control_consistencia().
P_RESUELTA = {(5, 10): 0.682, (10, 10): 0.500, (20, 10): 0.273,
              (5, 20): 0.852, (10, 20): 0.727}


def m2m(T, S):
    return np.load(os.path.join(AQUI, f"m2m_{T}_{S}.npy"))


def cadena(T, S, p_abierta=0.0, muestra=None, npaths=NPATHS, p_win=None):
    f = FIRMAS[FIRMA]
    ev = dict(f["eval"]); fu = dict(f["fund"]); fu.setdefault("max_days", MAX_DAYS_FUND)
    kw = dict(N=N, S_ticks=S * 4, T_ticks=T * 4, c1=C1,
              p_win=acierto_sin_ventaja(T, S) if p_win is None else p_win,
              exceso_pt=MEDIA_EXCESO[S],
              npaths=npaths, p_abierta=p_abierta, m2m_muestra=muestra)
    p_ev, _, _ = sim_bracket(rng=np.random.default_rng(SEMILLA), **kw, **ev)
    p_fu, _, _ = sim_bracket(rng=np.random.default_rng(SEMILLA + 1), **kw, **fu)
    return p_ev * p_fu, p_ev, p_fu


def control_consistencia():
    """Una entrada AL AZAR tiene que dar esperanza ~0 por operacion antes de costo. Si se
    mezcla la tasa de resueltas ASUMIDA con el M2M MEDIDO de las abiertas, los pedazos no
    cierran y aparece una ventaja fantasma. Este control lo caza."""
    print("=" * 100)
    print("CONTROL DE CONSISTENCIA - esperanza por operacion antes de costo, en puntos")
    print("Una entrada al azar tiene que dar ~0. Si no, la mezcla de piezas esta mal.")
    print("=" * 100)
    ok = True
    print(f"   {'bracket':>11}{'con tasa ASUMIDA':>20}{'con tasa MEDIDA':>19}")
    for T, S in CELDAS:
        pa, mm, med = P_ABIERTA[(T, S)], m2m(T, S).mean(), P_RESUELTA[(T, S)]
        asum = acierto_sin_ventaja(T, S)
        e_as = (1 - pa) * (asum * T - (1 - asum) * S) + pa * mm
        e_me = (1 - pa) * (med * T - (1 - med) * S) + pa * mm
        bien = abs(e_me) < 0.10
        ok &= bien
        print(f"   {f'{T}pt:{S}pt':>11}{e_as:>+19.3f}pt{e_me:>+18.3f}pt   "
              f"{'OK' if bien else 'MAL'}")
    print("\n   La columna ASUMIDA se desvia hasta 1,18pt: esa mezcla fabrica ventaja donde")
    print("   no hay. Por eso el tercer estado va SIEMPRE con la tasa de resueltas medida.")
    print(f"   CONTROL {'PASADO' if ok else 'FALLADO'}\n")
    return ok


def control():
    print("=" * 100)
    print("CONTROL - con fraccion abierta CERO el modelo nuevo debe reproducir el viejo")
    print("=" * 100)
    ok = True
    for T, S in CELDAS:
        viejo = cadena(T, S)[0]
        nuevo = cadena(T, S, p_abierta=0.0, muestra=m2m(T, S))[0]
        bien = viejo == nuevo
        ok &= bien
        print(f"   {f'{T}pt:{S}pt':>11}  viejo {viejo*100:8.4f}%   nuevo {nuevo*100:8.4f}%"
              f"   {'IDENTICO' if bien else 'DISTINTO'}")
    print(f"   CONTROL {'PASADO' if ok else 'FALLADO'}\n")
    return ok


def main():
    if not control_consistencia():
        raise SystemExit("Las piezas no cierran en esperanza cero. No se publica.")
    if not control():
        raise SystemExit("El estado nuevo cambia el resultado con p_abierta=0. No se publica.")

    print("=" * 100)
    print("LA CADENA CON EL TERCER ESTADO - P(pasar) vieja contra nueva")
    print("=" * 100)
    print("   'abierta' = fraccion medida que no resuelve en una sesion.")
    print("   'M2M medio' = valor a mercado medio de esas, en puntos de ES.\n")
    print(f"   {'bracket':>11}{'abierta':>10}{'M2M medio':>12}{'P vieja':>11}{'P nueva':>11}"
          f"{'dif rel':>10}{'direccion':>12}")
    filas = []
    for T, S in CELDAS:
        mu = m2m(T, S)
        viejo = cadena(T, S)[0]
        nuevo = cadena(T, S, p_abierta=P_ABIERTA[(T, S)], muestra=mu,
                       p_win=P_RESUELTA[(T, S)])[0]
        rel = (nuevo / viejo - 1) * 100 if viejo else float("nan")
        filas.append((T, S, viejo, nuevo, rel, mu.mean()))
        print(f"   {f'{T}pt:{S}pt':>11}{P_ABIERTA[(T,S)]*100:>9.1f}%{mu.mean():>12.3f}"
              f"{viejo*100:>10.3f}%{nuevo*100:>10.3f}%{rel:>+9.1f}%"
              f"{('BAJA' if rel < 0 else 'sube'):>12}")

    obj = p_equilibrio(FIRMA)
    print(f"\n   Equilibrio del intento: P >= {obj*100:.3f}%")
    print(f"   {'bracket':>11}{'P nueva':>11}{'supera equilibrio?':>22}")
    for T, S, viejo, nuevo, rel, mm in filas:
        print(f"   {f'{T}pt:{S}pt':>11}{nuevo*100:>10.3f}%"
              f"{('SI' if nuevo >= obj else 'no'):>22}")

    print("\n   LECTURA: el signo del M2M medio manda. Donde el objetivo esta mas cerca que")
    print("   el stop, las que quedan abiertas van hacia el stop lejano y su M2M es NEGATIVO:")
    print("   el modelo viejo las ignoraba y por eso sobreestimaba. Donde el objetivo esta")
    print("   mas lejos, pasa al reves.")
    return filas


if __name__ == "__main__":
    main()
