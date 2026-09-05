"""
VENTANA G - LA PARTICION TRABAJO / VERIFICACION, POR POTENCIA Y NO POR CALENDARIO.

NO GASTA CARTUCHO. K = 261. Calculo descriptivo sobre la muestra ya recogida. La caja sellada
(2020-2026) no se toca: esto reparte 2016-2019.

EL PROBLEMA. Partimos 2016-2018 (trabajo) contra 2019 (verificacion) por CALENDARIO. Medido despues:
la verificacion tiene resolucion +-72% de la ventaja de referencia contra +-33% del trabajo, o sea que
2019 solo NO PUEDE confirmar un efecto del tamano que el juez exige. Un periodo reservado que no
puede confirmar nada es un periodo reservado de adorno.

EL CALCULO AL REVES. La diferencia minima detectable de un periodo es MDE = z * sd / raiz(n), con sd
el desvio de los dolares por sesion DE ESE PERIODO. Igualar resolucion NO es igualar sesiones si los
desvios difieren: n_verif / n_trabajo = (sd_verif / sd_trabajo)^2. Como el tramo tardio (2018-2019) es
mas volatil, la verificacion necesita MAS de la mitad. Se busca el corte cronologico donde las dos
MDE se cruzan.

EL INTERCAMBIO, que hay que ver antes de fijar nada: con menos sesiones de trabajo, la MDE del periodo
de trabajo SUBE. Se reportan las dos puntas.
"""
import numpy as np

from aritmetica import C1_POR_MINI
from dolares_por_tiempo import MEDIA_EXCESO, PUNTO_ES, secuencial
from juez import DESLIZAMIENTO_ENTRADA, Z_POTENCIA
from razon_escalas import cargar_con_sesion

CELDA = (5, 20)
MIN_BARRAS = 60
O_SOBREPASO = 0.0642


def main():
    print("=" * 98)
    print("LA PARTICION TRABAJO / VERIFICACION POR POTENCIA - cuanto hay que reservar de verdad")
    print("NO GASTA CARTUCHO. K = 261. La caja sellada no se toca.")
    print("=" * 98)
    df = cargar_con_sesion()
    cl = df["close"].to_numpy(float); hi = df["high"].to_numpy(float); lo = df["low"].to_numpy(float)
    sess = df["sess"].to_numpy(); anio = df["sess"].dt.year.to_numpy()
    corte = np.flatnonzero(sess[1:] != sess[:-1]) + 1
    ini = np.concatenate(([0], corte)); fin = np.concatenate((corte, [len(cl)]))
    keep = (fin - ini) >= MIN_BARRAS
    ini, fin = ini[keep], fin[keep]
    fechas = df["sess"].to_numpy()[ini]
    anio_ses = anio[ini]
    n = len(ini)

    T, S = CELDA
    exc = MEDIA_EXCESO[S]
    # dolares por sesion de entradas al azar (combinado los dos lados), con costos: es la serie cuya
    # dispersion gobierna la potencia de cualquier periodo
    vs = {}
    nop = 0
    for lado in ("largo", "corto"):
        v, no, na = secuencial(cl, hi, lo, ini, fin, T, S, lado, exceso=exc, c1=C1_POR_MINI)
        vs[lado] = v; nop += no
    op_lado = nop / 2.0 / n
    slip = np.mean([DESLIZAMIENTO_ENTRADA[k] for k in (0, 1, 2)])
    comb = (vs["largo"] + vs["corto"]) / 2.0 - slip * op_lado * PUNTO_ES
    print(f"\n   {n:,} sesiones 2016-2019, celda {T}pt:{S}pt, {op_lado:.2f} op/sesion por lado.")
    print(f"   desvio de los dolares por sesion, por anio:")
    for a in sorted(set(anio_ses.tolist())):
        m = anio_ses == a
        print(f"      {a}: {int(m.sum()):>4} sesiones, desvio ${comb[m].std(ddof=1):>7.2f}")

    def mde(x):
        return Z_POTENCIA * x.std(ddof=1) / np.sqrt(len(x)) if len(x) > 2 else float("inf")

    # ------------------------------------------------------------------ el corte actual
    i_actual = int((anio_ses <= 2018).sum())
    print(f"\n   PARTICION ACTUAL (calendario): trabajo 2016-2018 = {i_actual} sesiones, "
          f"verificacion 2019 = {n - i_actual} sesiones")
    print(f"      MDE trabajo      ${mde(comb[:i_actual]):>7.2f}")
    print(f"      MDE verificacion ${mde(comb[i_actual:]):>7.2f}   "
          f"-> la verificacion es {mde(comb[i_actual:]) / mde(comb[:i_actual]):.2f}x mas gruesa")

    # ------------------------------------------------------------------ buscar el cruce
    print(f"\n   BARRIDO DEL CORTE CRONOLOGICO (trabajo = primeras i sesiones):")
    print(f"      {'i':>5}{'fecha del corte':>18}{'n trab':>8}{'n verif':>9}{'MDE trab':>10}{'MDE verif':>11}{'razon':>8}")
    mejor_i, mejor_gap = None, 1e9
    for i in range(int(0.25 * n), int(0.85 * n), 10):
        mt, mv = mde(comb[:i]), mde(comb[i:])
        gap = abs(np.log(mv / mt))
        if gap < mejor_gap:
            mejor_gap, mejor_i = gap, i
        if i % 50 < 10:
            print(f"      {i:>5}{str(fechas[i])[:10]:>18}{i:>8}{n-i:>9}{mt:>10.2f}{mv:>11.2f}{mv/mt:>8.2f}")
    mt, mv = mde(comb[:mejor_i]), mde(comb[mejor_i:])
    frac = mejor_i / n
    print(f"\n   CORTE DE IGUAL POTENCIA: i = {mejor_i} ({frac:.0%} trabajo / {1-frac:.0%} verificacion)")
    print(f"      fecha del corte: {str(fechas[mejor_i])[:10]}")
    print(f"      MDE trabajo ${mt:.2f}   MDE verificacion ${mv:.2f}   razon {mv/mt:.2f}")
    print(f"      La verificacion se lleva {1-frac:.0%}, MAS de la mitad, porque el tramo tardio es mas")
    print(f"      volatil: igualar resolucion no es igualar sesiones.")

    # ------------------------------------------------------------------ que se pierde
    mt_actual = mde(comb[:i_actual])
    print(f"\n   EL INTERCAMBIO, las dos puntas:")
    print(f"      trabajo AHORA  ({i_actual} ses): MDE ${mt_actual:.2f}")
    print(f"      trabajo NUEVO  ({mejor_i} ses): MDE ${mt:.2f}   -> el piso de deteccion del trabajo "
          f"SUBE {(mt/mt_actual - 1)*100:+.0f}%")
    print(f"      verificacion AHORA ({n-i_actual} ses): MDE ${mde(comb[i_actual:]):.2f}")
    print(f"      verificacion NUEVA ({n-mejor_i} ses): MDE ${mv:.2f}   -> BAJA "
          f"{(mv/mde(comb[i_actual:]) - 1)*100:+.0f}%")
    # ------------------------------------------------------------------ el hallazgo que decide
    i_pre = 501
    print("\n" + "=" * 98)
    print("PERO EL CALCULO NO SE SOSTIENE, Y ESTE ES EL HALLAZGO")
    print("=" * 98)
    print(f"   La MDE NO es monotona en el numero de sesiones. En el barrido salta de "
          f"${mde(comb[:i_pre]):.2f} con {i_pre} sesiones a ${mde(comb[:mejor_i]):.2f} con {mejor_i}: "
          f"{mde(comb[:mejor_i])/mde(comb[:i_pre]):.1f}x PEOR")
    print(f"   por agregar {mejor_i - i_pre} sesiones. El desvio por anio lo explica: "
          f"2017 $36, 2018 $368 -un factor 10-.")
    print(f"   Agregar datos EMPEORA el piso de deteccion cuando los datos que se agregan son la cola.")
    print(f"\n   Consecuencia: el corte de 'igual potencia' ({str(fechas[mejor_i])[:10]}) cae JUSTO sobre el")
    print(f"   pico de volatilidad de febrero 2018. Es el peor lugar posible para cortar: el punto de")
    print(f"   maxima sensibilidad a un punado de sesiones extremas. Reparticionar ahi seria ajustar la")
    print(f"   particion a la cola de 2018, que es exactamente la clase de cosa que esta busqueda rechaza.")
    print(f"\n   Y el intercambio NO es el que suponiamos: acortar el trabajo lo MEJORA "
          f"(${mt_actual:.2f} -> ${mde(comb[:i_pre]):.2f} con {i_pre} sesiones), porque saca 2018.")
    print(f"   Lo que se pierde no es potencia: es COBERTURA DE REGIMEN. Un trabajo de 2016-2017 no")
    print(f"   contiene regimen alto, y la maquinaria de tres terciles del juez se quedaria sin el")
    print(f"   tercil que mas importa.")
    print(f"\n   RECOMENDACION: NO reparticionar por potencia. La restriccion que manda es la cobertura")
    print(f"   de regimen, no el conteo de sesiones. La particion por calendario (2016-2018 / 2019) deja")
    print(f"   la verificacion gruesa, y ahora se sabe POR QUE: no le falta cantidad, le falta cola.")
    print(f"   Queda para que Roberto decida, con los dos numeros a la vista.")
    print("=" * 98)
    return str(fechas[mejor_i])[:10]


if __name__ == "__main__":
    main()
