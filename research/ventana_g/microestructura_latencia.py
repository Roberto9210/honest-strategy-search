"""
VENTANA G - ESCALAS DE TIEMPO DEL LIBRO, para anclar la latencia realista de la prueba pasiva.

NO GASTA CARTUCHO. K = 261. Medicion descriptiva sobre tbbo ya comprado (dos dias, calmo y agitado),
para justificar CON UN NUMERO MEDIDO el retardo realista del diseno mbo, en vez de suponerlo. NO es
el estudio mbo: no reconstruye la cola ni simula ordenes. La caja sellada no se toca.

QUE MIDE, en RTH (08:30-15:15 CT = 13:30-20:15 UTC, CDT):
  - operaciones por segundo y gap mediano entre operaciones
  - cambios del mejor precio (bid o ask) por segundo y su gap mediano ('dwell': cuanto vive una
    cotizacion antes de cambiar)
  - cuantos cambios de cotizacion y cuantas operaciones ocurren en 250 ms

POR QUE 250 ms. Es el orden de un ida y vuelta de internet residencial a Aurora (el datacenter de CME):
decenas a bajos cientos de ms. El NUMERO en si es de ingenieria, no del dato; lo que el DATO aporta es
cuanto se mueve el libro en esos 250 ms. Si la cotizacion cambia muchas veces en 250 ms, una orden
pasiva que llega 250 ms tarde aterriza sobre un libro que ya se dio vuelta varias veces: ese es el
argumento medido de que la latencia importa.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

import databento as db

DIR = Path(__file__).resolve().parents[2] / "data" / "microestructura"
ARCHIVOS = [("bajo 2017", "tbbo_ESn0_B_bajo_2017-06-07.dbn.zst"),
            ("alto 2018", "tbbo_ESn0_B_alto_2018-04-25.dbn.zst")]
RETARDO_MS = 250.0


def main():
    print("=" * 92)
    print("ESCALAS DE TIEMPO DEL LIBRO (tbbo, RTH) - para anclar la latencia realista")
    print("NO GASTA CARTUCHO. K = 261. No es el estudio mbo. La caja sellada no se toca.")
    print("=" * 92)
    print(f"\n   {'dia':>11}{'op RTH':>10}{'op/seg':>9}{'gap op ms':>11}{'cambios/seg':>13}"
          f"{'dwell ms':>10}{'camb/250ms':>12}{'op/250ms':>10}")
    for nom, fn in ARCHIVOS:
        p = DIR / fn
        if not p.exists():
            print(f"   {nom:>11}   FALTA {fn}")
            continue
        df = db.DBNStore.from_file(str(p)).to_df(price_type="float", pretty_ts=True)
        ts = df.index.tz_convert("UTC")
        m = ((ts.hour * 60 + ts.minute) >= 13 * 60 + 30) & ((ts.hour * 60 + ts.minute) < 20 * 60 + 15)
        d = df[m]
        t = d.index.tz_convert("UTC").view("int64") / 1e9      # segundos
        segs = t[-1] - t[0]
        gap_op = np.diff(t)
        bid = d["bid_px_00"].to_numpy(); ask = d["ask_px_00"].to_numpy()
        cambia = np.concatenate([[True], (bid[1:] != bid[:-1]) | (ask[1:] != ask[:-1])])
        t_cambio = t[cambia]
        gap_q = np.diff(t_cambio)
        op_seg = len(d) / segs
        camb_seg = cambia.sum() / segs
        print(f"   {nom:>11}{len(d):>10,}{op_seg:>9.1f}{np.median(gap_op) * 1e3:>11.1f}"
              f"{camb_seg:>13.1f}{np.median(gap_q) * 1e3:>10.1f}"
              f"{camb_seg * RETARDO_MS / 1e3:>12.1f}{op_seg * RETARDO_MS / 1e3:>10.1f}")
    print(f"\n   'dwell ms' = mediana del tiempo que vive el mejor precio antes de cambiar.")
    print(f"   'camb/250ms' = cambios de cotizacion en {RETARDO_MS:.0f} ms = cuantas veces se da vuelta")
    print(f"   el tope del libro mientras una orden pasiva viaja con latencia residencial.")


if __name__ == "__main__":
    main()
