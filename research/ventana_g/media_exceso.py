"""
VENTANA G - la MEDIA del exceso de deslizamiento sobre el stop.

NO GASTA CARTUCHO. K = 261. Es un estadistico DESCRIPTIVO sobre una muestra ya recogida
(ES 1-min Databento 2016-2019, P-escalera de 971 sesiones, fuera de la caja sellada
2020-2026). No hay hipotesis, ni estadistico de prueba, ni decision contra un alfa.

Por que hace falta: terreno_stop_resultado.md seccion 4 publico p50, p95, p99 y maximo del
exceso, pero NO la media -su funcion dist() solo calcula percentiles-. Y la media es lo que
gobierna la esperanza. Sin ella, la VENTANA G quedo comparando una cola (p95) contra un
margen de esperanza, que son dos preguntas distintas.

    LA MEDIA GOBIERNA LA ESPERANZA.
    LA COLA GOBIERNA LA PROBABILIDAD DE TOCAR EL LIMITE DE PERDIDA.

Se reusa la misma funcion touches() del script original, sin reimplementar nada: exc_same
es exactamente la variable cuyos percentiles se publicaron.

    python research/ventana_g/media_exceso.py > research/ventana_g/salida_media_exceso.txt
"""
import os
import sys

import numpy as np
import pandas as pd

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(RAIZ, "research", "ventaja_futuros"))

from terreno_tenencia import load_databento, window_stats, DEGRADED_UTC  # noqa: E402
from terreno_stop import window_frame, touches, DS, FOUR, HOURS          # noqa: E402

D_HORA = [4, 10, 20]     # las tres distancias con exceso ya publicado en la seccion 4


def resumen(x):
    x = np.asarray(pd.Series(x).dropna(), dtype=float)
    if len(x) == 0:
        return None
    return dict(n=len(x), media=float(x.mean()), p50=float(np.percentile(x, 50)),
                p95=float(np.percentile(x, 95)), p99=float(np.percentile(x, 99)),
                mx=float(x.max()))


def main():
    print("MEDIA DEL EXCESO SOBRE EL STOP - VENTANA G, 2026-09-04")
    print("ES 1-min Databento 2016-2019. NO GASTA CARTUCHO: descriptivo sobre muestra ya recogida.")
    print("Reusa touches() de terreno_stop.py sin reimplementar. exc_same = exceso dentro de la")
    print("barra que toca, en PUNTOS de ES.\n")

    df = load_databento()
    sess = df.groupby("sess").agg(n_contracts=("contract", "nunique"))
    degraded = set(df.loc[df["utc_date"].isin(DEGRADED_UTC), "sess"].unique())
    t23 = window_stats(df, None, None)
    rth = window_stats(df, 8 * 60 + 30, 15 * 60)
    ok = ((sess.index.weekday < 5) & (sess["n_contracts"] == 1) & (~sess.index.isin(list(degraded)))
          & (t23["first_m"].reindex(sess.index) == 17 * 60)
          & (rth["first_m"].reindex(sess.index) == 8 * 60 + 30)
          & (rth["last_m"].reindex(sess.index) >= 15 * 60 - 1))
    idx = sess.index[ok.fillna(False)]

    # CONTROL DE POBLACION: si no reproduce las 971 sesiones, el dato se movio y no se sigue.
    print(f"CONTROL de poblacion: {len(idx)} sesiones (esperado 971) -> "
          f"{'OK' if len(idx) == 971 else 'FALLADO'}")
    if len(idx) != 971:
        raise SystemExit("La poblacion no reproduce. No se publica nada.")
    print(f"  {idx.min().date()} -> {idx.max().date()}\n")

    print("=" * 96)
    print("1. MEDIA DEL EXCESO POR VENTANA, LADO Y DISTANCIA DEL STOP")
    print("=" * 96)
    print(f"  {'ventana':<7}{'lado':<7}{'D':>4}{'n':>7}{'MEDIA':>9}{'p50':>8}{'p95':>8}"
          f"{'p99':>8}{'max':>9}{'media/p95':>11}")
    filas = {}
    for name, a, b in FOUR:
        fr = window_frame(df, idx, a, b)
        for side in ("largo", "corto"):
            for D in DS:
                r = resumen(touches(fr, side, D)["exc_same"])
                if r is None:
                    continue
                filas[(name, side, D)] = r
                print(f"  {name:<7}{side:<7}{D:>4}{r['n']:>7}{r['media']:>9.3f}{r['p50']:>8.2f}"
                      f"{r['p95']:>8.2f}{r['p99']:>8.2f}{r['mx']:>9.2f}"
                      f"{r['media']/r['p95']:>11.2f}")
        del fr

    # Volcado de la MUESTRA cruda del exceso, no solo sus resumenes. Hace falta para la
    # pregunta de la cola: con que probabilidad UN llenado malo mata la cuenta. Eso no se
    # contesta con la media ni con un percentil; hay que remuestrear la distribucion.
    fr23 = window_frame(df, idx, None, None)
    for D in D_HORA:
        m = pd.Series(touches(fr23, "largo", D)["exc_same"]).dropna()
        m.to_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              f"exceso_muestra_T23_largo_D{D}.csv"), index=False,
                 header=["exc_same_pt"])
        print(f"  volcada muestra T23/largo D={D}: n={len(m)}")
    del fr23

    print("\n" + "=" * 96)
    print("2. MEDIA DEL EXCESO POR HORA DE ENTRADA (tenencia de 1 hora, lado largo)")
    print("   La seccion 3 del terreno mostro que la frecuencia de toque cambia 20x con la hora.")
    print("   Si la MEDIA del exceso tambien cambia, el p95 mezclado promedia dos regimenes.")
    print("=" * 96)
    print(f"  {'hora CT':>8}" + "".join(f"{f'D={d}: n / media':>22}" for d in D_HORA))
    for h in HOURS:
        fr = window_frame(df, idx, h * 60, h * 60 + 60)
        celdas = ""
        for D in D_HORA:
            r = resumen(touches(fr, "largo", D)["exc_same"])
            if r is None:
                celdas += f"{'---':>22}"
            else:
                celda = f"{r['n']} / {r['media']:.3f}"
                celdas += f"{celda:>22}"
        print(f"  {h:>6}:00{celdas}")
        del fr

    print("\nLECTURA. La media gobierna la ESPERANZA (cuanto cuesta en promedio cada stop).")
    print("La cola gobierna la PROBABILIDAD DE TOCAR EL LIMITE (cuanto puede costar una vez).")
    print("Son dos preguntas y hasta hoy estaban mezcladas en un solo filtro.")


if __name__ == "__main__":
    main()
