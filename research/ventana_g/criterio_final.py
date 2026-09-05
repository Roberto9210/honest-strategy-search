"""
VENTANA G - el criterio con el costo MEDIDO, micros contra mini, y la cola cuantificada.

NO GASTA CARTUCHO. K = 261.

Cambios respecto de criterio_media.py:
  1. El costo ya no es hipotesis. https://help.tradeify.co/en/articles/10468315-trading-commission-fees
     (leida 2026-09-04): $1,82 ida y vuelta por micro, $5,76 por mini, y la pagina declara
     que ya incluye exchange, NFA, clearing y comision.
  2. Se separa limpio: el COSTO DE EJECUCION va en las dos ramas; el DESLIZAMIENTO medido
     va solo en la rama perdedora. Antes estaban mezclados en un c1 unico.
  3. Se agrega el caso "1 mini", que es la misma exposicion que 10 micros a 68% menos de
     costo, por recomendacion textual de la propia pagina.
  4. La cola deja de ser una nota al pie: el exceso se sortea de la muestra empirica.
"""
import os

import numpy as np
import pandas as pd

from aritmetica import C1_POR_MICRO, C1_POR_MICRO_VIA_MINI, FIRMAS
from vara_criterio import (acierto_requerido, acierto_sin_ventaja, p_equilibrio, p_pasar,
                            MAX_DAYS_FUND, SEMILLA)
from bracket import sim_bracket

AQUI = os.path.dirname(os.path.abspath(__file__))
FIRMA = "Tradeify Growth (50K)"
N = 10                      # micros, o micro-equivalentes si se opera 1 mini
PUNTO = 5.0                 # USD por punto por micro

# media_exceso.py, T23 lado largo, exceso dentro de la barra que toca, en puntos.
MEDIA_EXCESO = {4: 0.596, 10: 0.722, 20: 0.982}
CELDAS = [(5, 10), (10, 10), (20, 10), (5, 20), (10, 20)]

EJECUCION = {"10 micros": C1_POR_MICRO, "1 mini": C1_POR_MICRO_VIA_MINI}


def muestra(D_pt):
    f = os.path.join(AQUI, f"exceso_muestra_T23_largo_D{D_pt}.csv")
    return pd.read_csv(f)["exc_same_pt"].to_numpy(dtype=float)


def seccion_a():
    print("=" * 100)
    print("A. EL COSTO, AHORA MEDIDO - y por que 1 mini no es lo mismo que 10 micros")
    print("=" * 100)
    print("   https://help.tradeify.co/en/articles/10468315-trading-commission-fees (2026-09-04)")
    print("   Ida y vuelta por contrato, ya incluye exchange + NFA + clearing + comision.\n")
    print(f"   {'via':>12}{'$/operacion':>14}{'$/micro-equiv':>16}{'contra el limite 4 minis/40 micros':>38}")
    print(f"   {'10 micros':>12}{C1_POR_MICRO * N:>14.2f}{C1_POR_MICRO:>16.3f}"
          f"{'usa 10 de los 40 micros':>38}")
    print(f"   {'1 mini':>12}{C1_POR_MICRO_VIA_MINI * N:>14.2f}{C1_POR_MICRO_VIA_MINI:>16.3f}"
          f"{'usa 1 de los 4 minis':>38}")
    ahorro = (C1_POR_MICRO - C1_POR_MICRO_VIA_MINI) * N
    print(f"\n   Diferencia: ${ahorro:.2f} por operacion, "
          f"{100*ahorro/(C1_POR_MICRO*N):.0f}% menos, MISMA exposicion.")
    print("   VERIFICADO en fuente del proyecto: el limite del 50K Growth es '4 minis/40 micros'")
    print("   (datos_crudos.md, leido de la pagina oficial 2026-09-03). O sea: los minis estan")
    print("   permitidos y 1 mini cuenta como 10 micros. NO es supuesto.")
    print("   Cita de la pagina de fees: \"If you're trading micro contracts in multiples of 10,")
    print("   you should trade the corresponding mini contract instead to save on fees.\"")


def seccion_b():
    print("\n" + "=" * 100)
    print("B. EL CRITERIO CON EL COSTO MEDIDO - 10 micros contra 1 mini")
    print("=" * 100)
    print("   'ventaja pedida' = requerido - moneda. Es lo que el candidato tiene que aportar")
    print("   por encima de lo que ya da un paseo sin ventaja. Nada mas que eso.")
    print("   Deslizamiento medio medido cargado solo a la rama perdedora.\n")
    print(f"   {'bracket':>11}{'moneda':>9}" +
          "".join(f"{v + ' req':>13}{'ventaja':>10}" for v in EJECUCION))
    filas = []
    for T, S in CELDAS:
        moneda = 100 * acierto_sin_ventaja(T, S)
        linea = f"   {f'{T}pt:{S}pt':>11}{moneda:>8.1f}%"
        fila = {"T": T, "S": S, "moneda": moneda}
        for via, c1 in EJECUCION.items():
            req = 100 * acierto_requerido(FIRMA, N, T, S, c1, extra_pt=MEDIA_EXCESO[S])
            fila[via] = req
            linea += f"{req:>12.1f}%{req - moneda:>+10.1f}"
        filas.append(fila)
        print(linea)
    print("\n   El mini baja el requerido en todas las celdas. La ventaja pedida es lo que")
    print("   habria que demostrar; cuanto mas chica, mas alcanzable el criterio.")
    return filas


def seccion_c(filas):
    print("\n" + "=" * 100)
    print("C. LA BANDA QUE AYER BLOQUEABA - antes 4,9 puntos de incertidumbre")
    print("=" * 100)
    print("   Ayer el costo era hipotesis y su rango plausible movia el requerido 4,9 puntos,")
    print("   contra un margen de 1,7. Hoy el costo esta medido y no tiene rango: es un numero.")
    print("   Lo que queda de incertidumbre en el costo es la diferencia entre las dos vias,")
    print("   y esa es una ELECCION del operador, no una incognita.\n")
    mejor = min(filas, key=lambda f: f["1 mini"] - f["moneda"])
    for f in filas:
        d = f["10 micros"] - f["1 mini"]
        print(f"   {f['T']}pt:{f['S']}pt: 10 micros {f['10 micros']:.1f}% -> "
              f"1 mini {f['1 mini']:.1f}%   (elegir mini ahorra {d:.1f} puntos)")
    print(f"\n   Menor ventaja pedida via mini: {mejor['T']}pt:{mejor['S']}pt -> "
          f"{mejor['1 mini'] - mejor['moneda']:+.1f} puntos sobre la moneda.")
    return mejor


def seccion_d(mejor):
    print("\n" + "=" * 100)
    print("D. LA COLA - probabilidad de morir por UN llenado malo antes de terminar la cadena")
    print("=" * 100)
    T, S = mejor["T"], mejor["S"]
    c1 = C1_POR_MICRO_VIA_MINI
    p_win = acierto_sin_ventaja(T, S)
    m = muestra(S)
    print(f"   celda {T}pt:{S}pt via 1 mini, sin ventaja (p={p_win*100:.1f}%), "
          f"muestra empirica n={len(m)}")
    print(f"   exceso: media {m.mean():.3f}pt  p95 {np.percentile(m,95):.2f}pt  "
          f"max {m.max():.2f}pt\n")

    f = FIRMAS[FIRMA]
    ev = dict(f["eval"])
    fu = dict(f["fund"]); fu.setdefault("max_days", MAX_DAYS_FUND)
    T_ticks, S_ticks = T * 4, S * 4
    res = {}
    for etiqueta, kw in (("media (deterministico)", dict(exceso_pt=MEDIA_EXCESO[S])),
                          ("muestra (estocastico)", dict(exceso_muestra=m))):
        diag = {}
        p_ev, _, _ = sim_bracket(N=N, S_ticks=S_ticks, T_ticks=T_ticks, c1=c1, p_win=p_win,
                                 npaths=60_000, rng=np.random.default_rng(SEMILLA),
                                 diag=diag, **kw, **ev)
        p_fu, _, _ = sim_bracket(N=N, S_ticks=S_ticks, T_ticks=T_ticks, c1=c1, p_win=p_win,
                                 npaths=60_000, rng=np.random.default_rng(SEMILLA + 1),
                                 diag=diag, **kw, **fu)
        res[etiqueta] = (p_ev * p_fu, diag)
        print(f"   {etiqueta:<24} P(pasar la cadena) = {p_ev*p_fu*100:.3f}%")

    p_det = res["media (deterministico)"][0]
    p_est, diag = res["muestra (estocastico)"]
    caida = 100 * (1 - p_est / p_det) if p_det else float("nan")
    print(f"\n   Modelar la cola en vez de la media baja P(pasar) un {caida:.1f}% relativo.")
    if diag.get("muertes"):
        frac = diag["por_llenado"] / diag["muertes"]
        print(f"   Muertes atribuibles a UN llenado malo: {diag['por_llenado']:,} de "
              f"{diag['muertes']:,} = {frac*100:.1f}%")
        print("   (definicion: rompio el piso con el exceso sorteado, pero con el exceso MEDIO")
        print("    se habria mantenido arriba. Es la muerte que la media no ve.)")
    print("\n   El equilibrio se recalcula contra la P estocastica, no la deterministica:")
    obj = p_equilibrio(FIRMA)
    print(f"   equilibrio exige P >= {obj*100:.3f}%. Con la cola adentro P(sin ventaja) = "
          f"{p_est*100:.3f}%.")
    req_cola = 100 * acierto_requerido(FIRMA, N, T, S, c1, extra_pt=MEDIA_EXCESO[S])
    print(f"   requerido con la media: {req_cola:.1f}%  (moneda {100*p_win:.1f}%)")
    return p_det, p_est, diag


def equilibrio_operacion(T_pt, S_pt, c1):
    """(i) El criterio del OPERADOR: acierto que hace que la operacion en si no pierda
    plata. Costo en las dos ramas, deslizamiento medio solo en la perdedora."""
    win = T_pt * PUNTO * N - c1 * N
    loss = S_pt * PUNTO * N + c1 * N + MEDIA_EXCESO[S_pt] * PUNTO * N
    return 100 * loss / (win + loss)


def seccion_e():
    print("\n" + "=" * 100)
    print("E. LOS DOS CRITERIOS, QUE NO SON EL MISMO - via 1 mini, costo medido")
    print("=" * 100)
    print("   (i)  equilibrio POR OPERACION: el acierto con el que operar deja de perder plata.")
    print("   (ii) umbral del INTENTO: el acierto con el que la cuota de $83 vale la pena.")
    print("   (ii) incluye la cola remuestreada de la muestra empirica, no la media.\n")
    print(f"   {'bracket':>11}{'moneda':>9}{'(ii) intento':>15}{'(i) operacion':>16}"
          f"{'ventaja p/ (i)':>17}")
    filas = []
    for T, S in CELDAS:
        moneda = 100 * acierto_sin_ventaja(T, S)
        ii = 100 * acierto_requerido(FIRMA, N, T, S, C1_POR_MICRO_VIA_MINI,
                                      muestra=muestra(S))
        i = equilibrio_operacion(T, S, C1_POR_MICRO_VIA_MINI)
        filas.append((T, S, moneda, ii, i))
        print(f"   {f'{T}pt:{S}pt':>11}{moneda:>8.1f}%{ii:>14.1f}%{i:>15.1f}%"
              f"{i - moneda:>+16.1f}")
    print("\n   (ii) < (i) en todas: el intento conviene antes de que operar sea rentable.")
    print("   Un candidato que solo cumpla (ii) esta perdiendo plata por operacion y")
    print("   viviendo del valor de opcion de la cuota. Para una cuenta fondeada sostenible")
    print("   el numero que hay que exigir es (i).")
    mejor_i = min(filas, key=lambda f: f[4] - f[2])
    print(f"\n   Menor ventaja pedida contra (i): {mejor_i[0]}pt:{mejor_i[1]}pt -> "
          f"{mejor_i[4]:.1f}% contra moneda {mejor_i[2]:.1f}% = {mejor_i[4]-mejor_i[2]:+.1f} puntos.")
    return filas


if __name__ == "__main__":
    seccion_a()
    filas = seccion_b()
    mejor = seccion_c(filas)
    seccion_d(mejor)
    seccion_e()
