"""
DIAGNOSTICO DEL INSTRUMENTO ANTES DE ACEPTAR EL NEGATIVO DE LA PIEZA 3b.

NO GASTA CARTUCHO. K = 261. Dinero: $0. La caja sellada no se toca.

POR QUE EXISTE. La Pieza 3b dio rho ~ 0 (entre -0,07 y +0,05) entre el desbalance previo y el
markout del llenado, o sea "el libro NO avisa". Antes de publicar un negativo hay que descartar que
el negativo sea del INSTRUMENTO y no del mercado, y aca hay un motivo concreto para sospechar:

mbo_lib.reconstruir SOLO anota una fila de BBO cuando cambia el PRECIO del mejor bid o ask:
    if (not bid_l or best_bid != bid_l[-1] or best_ask != ask_l[-1]): anotar
Los cambios de TAMANO en el mismo mejor precio NO se anotan. Entonces bsz/asz -de donde sale el
desbalance- estan CONGELADOS desde el ultimo cambio de precio. Si entre cambios de precio pasan
cientos de milisegundos, el desbalance que mido no es el de "justo antes del llenado": es el de la
ultima vez que se movio el mejor precio, que puede ser mucho antes.

LO QUE SE MIDE ACA:
  1. el dwell entre cambios de MEJOR PRECIO (mediana y media, por dia);
  2. la ANTIGUEDAD del estado del libro en el instante del llenado: cuanto hace que se congelo;
  3. que fraccion de los llenados tiene un estado mas viejo que los adelantos d que use (100, 500,
     1000 ms). Si la mayoria lo tiene, entonces variar d no varia NADA y toda la fila de adelantos
     de la Pieza 3c estaba mirando el mismo numero.

LO QUE DECIDE: si la antiguedad mediana es del orden o mayor que los adelantos, el negativo de 3b
NO esta establecido -esta sin medir- y hay que decirlo asi.
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
ADELANTOS_MS = [100, 500, 1000]
LAT_MS = 250
MUERTE_TICKS = 1
N_ENTRADAS = 3000
SEMILLA = 20260906


def main():
    R = []
    A = R.append
    A("=" * 100)
    A("DIAGNOSTICO: el negativo de la Pieza 3b es del MERCADO o de mi INSTRUMENTO?")
    A("NO GASTA CARTUCHO. K = 261. Dinero: $0. La caja sellada no se toca.")
    A("=" * 100)
    A("")
    A("   mbo_lib.reconstruir anota BBO solo cuando cambia el PRECIO del mejor bid/ask. Los cambios")
    A("   de TAMANO en el mismo precio no se anotan, asi que bsz/asz -y con ellos el desbalance-")
    A("   quedan congelados desde el ultimo cambio de precio.")
    A("")
    A(f"   {'dia':>16}{'n cambios':>11}{'dwell med':>11}{'dwell prom':>12}"
      f"{'antig. med':>12}{'antig. p90':>12}" + "".join(f"{'> ' + str(d) + 'ms':>10}"
                                                        for d in ADELANTOS_MS))
    filas = []
    for i_d, (epoca, tercil, arch) in enumerate(P.ARCHIVOS):
        p = DIR / arch
        if not p.exists():
            continue
        t0 = time.time()
        rec = M.reconstruir(str(p))
        print(f"   {arch} en {time.time()-t0:.0f}s", file=sys.stderr, flush=True)
        tc = rec["tc"]
        if len(tc) < 1000:
            continue
        dw = np.diff(tc) / 1e6                       # ms entre cambios de mejor precio
        # llenados simulados, igual que en 3b
        rs = np.random.default_rng(SEMILLA + 7 + 101 * i_d)
        t0n, t1n = tc[0], tc[-1] - 400 * 1_000_000_000
        ent = np.sort(rs.integers(t0n, t1n, N_ENTRADAS))
        lado = np.where(rs.random(N_ENTRADAS) < 0.5, 1.0, -1.0)
        filled, t_fill, _, _ = P.simular(rec, ent, lado, LAT_MS * 1_000_000, MUERTE_TICKS)
        tf = t_fill[filled]
        j = np.clip(np.searchsorted(tc, tf, side="right") - 1, 0, len(tc) - 1)
        antig = (tf - tc[j]) / 1e6                   # ms de antiguedad del estado en el llenado
        frac = [float((antig > d).mean()) for d in ADELANTOS_MS]
        filas.append((f"{epoca}/{tercil}", len(tc), np.median(dw), dw.mean(),
                      np.median(antig), np.percentile(antig, 90), frac))
        A(f"   {epoca + '/' + tercil:>16}{len(tc):>11,}{np.median(dw):>11.1f}{dw.mean():>12.1f}"
          f"{np.median(antig):>12.1f}{np.percentile(antig, 90):>12.1f}"
          + "".join(f"{f:>10.1%}" for f in frac))

    A("")
    A("-" * 100)
    A("   LO QUE DECIDE")
    A("-" * 100)
    if not filas:
        A("   Sin dias legibles.")
        print("\n".join(R))
        return 1
    med = np.median([f[4] for f in filas])
    fr = {d: np.mean([f[6][i] for f in filas]) for i, d in enumerate(ADELANTOS_MS)}
    A(f"   Antiguedad MEDIANA del estado del libro en el instante del llenado: {med:.1f} ms.")
    for d in ADELANTOS_MS:
        A(f"   Fraccion de llenados cuyo estado ya era mas viejo que {d} ms: {fr[d]:.1%}")
    A("")
    peor = fr[ADELANTOS_MS[0]]
    if peor > 0.5:
        A(f"   EL INSTRUMENTO NO SIRVE PARA ESTA PREGUNTA. En {peor:.0%} de los llenados el estado")
        A(f"   del libro ya tenia mas de {ADELANTOS_MS[0]} ms cuando el llenado ocurrio, asi que")
        A(f"   'mirar el libro 100 ms antes' y 'mirarlo en el instante' devuelven EL MISMO estado.")
        A("   La fila de adelantos de la Pieza 3c estaba comparando el mismo numero con si mismo.")
        A("   EL NEGATIVO DE 3b NO ESTA ESTABLECIDO: esta SIN MEDIR.")
    elif med > 50:
        A(f"   EL INSTRUMENTO ESTA AL LIMITE. La mediana de antiguedad ({med:.0f} ms) es del orden")
        A(f"   del adelanto mas corto que use. El negativo de 3b es sospechoso y hay que rehacerlo")
        A("   con una reconstruccion que anote los cambios de TAMANO, no solo los de precio.")
    else:
        A(f"   EL INSTRUMENTO AGUANTA. La mediana de antiguedad ({med:.1f} ms) es chica contra los")
        A(f"   adelantos usados, asi que el desbalance medido es efectivamente 'el de justo antes'.")
        A("   El negativo de 3b es del MERCADO y se puede publicar como tal.")
    A("")
    A("   QUE HARIA FALTA PARA ARREGLARLO, si hace falta: anotar en reconstruir() una fila tambien")
    A("   cuando cambia el TAMANO en el mejor precio. Es un cambio de una linea en la condicion, y")
    A("   multiplica el largo de la serie por el cociente entre cambios de tamano y de precio -o sea")
    A("   que cuesta memoria y tiempo de corrida, no dinero-. No lo hago aca: primero el diagnostico.")
    A("=" * 100)
    print("\n".join(R))
    return 0


if __name__ == "__main__":
    sys.exit(main())
