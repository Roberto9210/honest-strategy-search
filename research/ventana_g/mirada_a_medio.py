"""
TAREA 5 - UN VISTAZO, NO UNA INVESTIGACION: el A/medio da markout -0,0682, 25x peor que los otros.

NO GASTA CARTUCHO. K = 261. Dinero: $0. La caja sellada no se toca (2026-09-02 es posterior al
2026-08-19). Diez minutos, no una tarde.

LA PREGUNTA: es un artefacto de ESE dia -un evento, un cierre raro, un tramo roto- o se repite en el
otro dia A? Si se repite, la seleccion adversa de 2026 es otra cosa que la de 2017-2019 y eso ataca
la comparabilidad por un camino que no esta en la lista de tres mediciones.

LO QUE SE MIRA, y nada mas: el markout por TRAMO de la sesion en los tres dias A y los tres B. Si el
-0,0682 del A/medio viene de un tramo y el resto del dia es normal, es artefacto. Si esta repartido,
no lo es.
"""

import os
import sys
import time
from pathlib import Path

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import mbo_lib as M  # noqa: E402
import mbo_entrada_pasiva as P  # noqa: E402

DIR = Path(AQUI).resolve().parents[1] / "data" / "microestructura"
N_ENTRADAS = 3000
LAT_MS = 250
MUERTE = 1
H = 30
N_TRAMOS = 6
SEMILLA = 20260904


def main():
    R = []
    A = R.append
    A("=" * 100)
    A("TAREA 5 - EL MARKOUT DEL A/medio POR TRAMOS: artefacto de un dia o cosa de la epoca?")
    A("NO GASTA CARTUCHO. K = 261. Dinero: $0. La caja sellada no se toca.")
    A("=" * 100)
    A(f"\n   Markout a H={H}s, latencia {LAT_MS} ms, muerte {MUERTE} tick, libro CON tamano.")
    A(f"   La sesion RTH se parte en {N_TRAMOS} tramos iguales.")
    A("")
    A(f"   {'dia':>16}{'total':>10}" + "".join(f"{'T' + str(i + 1):>10}" for i in range(N_TRAMOS))
      + f"{'n llenos':>10}")
    for i_d, (epoca, tercil, arch) in enumerate(P.ARCHIVOS):
        p = DIR / arch
        if not p.exists():
            continue
        t0 = time.time()
        rec = M.reconstruir(str(p), con_tamano=True)
        print(f"   {arch} en {time.time()-t0:.0f}s", file=sys.stderr, flush=True)
        tc = rec["tc"]
        rs = np.random.default_rng(SEMILLA + 101 * i_d)
        ent = np.sort(rs.integers(tc[0], tc[-1] - 400 * 1_000_000_000, N_ENTRADAS))
        lado = np.where(rs.random(N_ENTRADAS) < 0.5, 1.0, -1.0)
        filled, t_fill, lim, _ = P.simular(rec, ent, lado, LAT_MS * 1_000_000, MUERTE)
        tf = t_fill[filled]; lf = lim[filled]; sf = lado[filled]
        if len(tf) < 30:
            A(f"   {epoca + '/' + tercil:>16}   (pocos llenados)")
            del rec
            continue
        mk = (M.mid_en(rec, tf + H * 1_000_000_000) - lf) * sf
        bordes = np.linspace(tc[0], tc[-1], N_TRAMOS + 1)
        cel = []
        for k in range(N_TRAMOS):
            s = (tf >= bordes[k]) & (tf < bordes[k + 1])
            cel.append(f"{mk[s].mean():+.4f}" if s.sum() >= 10 else "-")
        A(f"   {epoca + '/' + tercil:>16}{mk.mean():>+10.4f}" + "".join(f"{c:>10}" for c in cel)
          + f"{len(mk):>10}")
        del rec
    A("")
    A("-" * 100)
    A("   COMO LEERLO")
    A("-" * 100)
    A("   Si el markout malo del A/medio esta concentrado en UN tramo, es un evento de ese dia y no")
    A("   dice nada de la epoca. Si esta repartido en los seis, es una propiedad del dia -y hay que")
    A("   mirar si el otro dia A la comparte-.")
    A("   ESTO ES UN VISTAZO: seis tramos de un dia son ~230 llenados por celda. No alcanza para")
    A("   afirmar nada sobre la epoca; alcanza para decidir si vale la pena mirarlo en serio.")
    A("=" * 100)
    print("\n".join(R))
    return 0


if __name__ == "__main__":
    sys.exit(main())
