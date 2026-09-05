"""
VENTANA G - LOS CORTES REALES DE SESION, Y EL TRAMO SIN TENDENCIA.

NO GASTA CARTUCHO. K = 261. Medicion descriptiva sobre muestra ya recogida. La caja sellada
(2020-01-02 -> 2026-08-19) no se toca.

DOS COSAS, las dos ideas mias del reporte anterior.

(3) LOS CORTES REALES. En dolares_por_tiempo.py parti la serie en bloques FIJOS de 1.380
    barras: salieron 983 bloques donde las sesiones reales son 1.007, con mediana de 1.362
    barras. O sea que la marca a mercado quedaba desalineada del corte nocturno real. Se
    rehace con los cortes de verdad.
    CRITERIO, escrito antes: si el piso se mueve MENOS que su error de $6,69, la
    aproximacion era inocua y se dice. Si se mueve mas, la unidad de tiempo del marco estaba
    mal y hay que rehacer el piso.

(4) EL TRAMO SIN TENDENCIA. Con entradas al azar el lado largo empataba (-$2,36 por sesion,
    a 0,1 errores de cero) y el corto perdia feo (-$108,23). La sospecha es que eso es el
    tramo alcista 2016-2019 y nada mas. Se parte por ano calendario y se mira si el resultado
    del largo sigue al movimiento del ano.
    Si en un ano sin tendencia el largo tambien pierde feo, era el periodo y queda cerrado.
    Si el largo sigue empatando, es otra cosa y se dice SIN ponerle nombre.

    AVISO QUE VA CON ESTO, para que no se lea mal despues: aunque el largo empatara, EMPATAR
    NO ES VENTAJA. El piso sigue siendo el piso, no cero.

CONTROL, con condicion de falla declarada: las dos particiones -bloques fijos y sesiones
reales- tienen que cubrir el mismo numero de barras salvo los restos, y el total de dolares
tiene que ser del mismo orden.
   QUE LO HARIA FALLAR: que el total de operaciones cambie mas de un 10%. Significaria que
   una de las dos particiones esta perdiendo pedazos de la serie.
"""
import numpy as np

from aritmetica import C1_POR_MINI
from dolares_por_tiempo import MEDIA_EXCESO, PUNTO_ES, SESION, cortes, secuencial
from razon_escalas import cargar_con_sesion

CELDAS = [(5, 20), (20, 10)]
O_SOBREPASO = 0.0642      # medido en sesgo_marco.py
MIN_BARRAS = 60           # una "sesion" de menos de una hora no es una sesion


def piso(v, op_lado, T, S):
    """Piso = lo que hay que superar, ya restado el sesgo de sobrepaso del propio marco."""
    p = S / (S + T)
    sesgo = O_SOBREPASO * (1 - 2 * p) * PUNTO_ES * op_lado
    return -(v.mean() - sesgo), sesgo


def medir(cl, hi, lo, ini, fin, T, S):
    exc = MEDIA_EXCESO[S]
    vs, nops = {}, {}
    for lado in ("largo", "corto"):
        v, no, na = secuencial(cl, hi, lo, ini, fin, T, S, lado, exceso=exc, c1=C1_POR_MINI)
        vs[lado], nops[lado] = v, no
    comb = (vs["largo"] + vs["corto"]) / 2.0
    op_lado = (nops["largo"] + nops["corto"]) / 2.0 / len(ini)
    return vs, comb, op_lado, nops["largo"] + nops["corto"]


def main():
    print("=" * 100)
    print("LOS CORTES REALES DE SESION, Y EL TRAMO SIN TENDENCIA")
    print("NO GASTA CARTUCHO. K = 261. La caja sellada no se toca.")
    print("=" * 100)

    df = cargar_con_sesion()
    cl = df["close"].to_numpy(float)
    hi = df["high"].to_numpy(float)
    lo = df["low"].to_numpy(float)
    sess = df["sess"].to_numpy()
    anio = df["sess"].dt.year.to_numpy()
    corte = np.flatnonzero(sess[1:] != sess[:-1]) + 1
    ini_r = np.concatenate(([0], corte))
    fin_r = np.concatenate((corte, [len(cl)]))
    largo_ses = fin_r - ini_r
    chicas = int((largo_ses < MIN_BARRAS).sum())
    keep = largo_ses >= MIN_BARRAS
    ini_r, fin_r = ini_r[keep], fin_r[keep]
    anio_ses = anio[ini_r]

    ini_b, fin_b = cortes(len(cl), SESION)
    print(f"\n   barras: {len(cl):,}")
    print(f"   sesiones REALES: {len(largo_ses):,}  (mediana {int(np.median(largo_ses)):,} "
          f"barras, minimo {largo_ses.min()}, maximo {largo_ses.max()})")
    print(f"   se descartan {chicas} sesiones de menos de {MIN_BARRAS} barras")
    print(f"   -> quedan {len(ini_r):,} sesiones reales")
    print(f"   bloques FIJOS de {SESION}: {len(ini_b):,}")

    # -------------------------------------------------------------------------------------
    print("\n" + "=" * 100)
    print("(3) CORTES REALES CONTRA BLOQUES FIJOS")
    print("   CRITERIO: si el piso se mueve menos que su error ($6,69), la aproximacion era")
    print("   inocua. Si se mueve mas, la unidad de tiempo estaba mal.")
    print("=" * 100)
    print(f"\n   {'celda':>10}{'particion':>18}{'sesiones':>10}{'$/sesion':>11}{'error':>9}"
          f"{'op/sesion':>11}{'sesgo marco':>13}{'PISO':>10}{'total op':>11}")
    pisos = {}
    for T, S in CELDAS:
        for nom, (ii, ff) in (("bloques 1380", (ini_b, fin_b)),
                              ("sesiones reales", (ini_r, fin_r))):
            vs, comb, op_lado, tot_op = medir(cl, hi, lo, ii, ff, T, S)
            pi, sg = piso(comb, op_lado, T, S)
            pisos[(T, S, nom)] = (pi, comb.std(ddof=1) / np.sqrt(len(ii)), tot_op, vs)
            print(f"   {f'{T}pt:{S}pt':>10}{nom:>18}{len(ii):>10,}{comb.mean():>+11.2f}"
                  f"{comb.std(ddof=1)/np.sqrt(len(ii)):>9.2f}{op_lado:>11.2f}"
                  f"{sg:>+13.2f}{pi:>+10.2f}{tot_op:>11,}")
    print()
    ok_ctrl = True
    for T, S in CELDAS:
        pb, eb, ob, _ = pisos[(T, S, "bloques 1380")]
        pr, er, orr, _ = pisos[(T, S, "sesiones reales")]
        dif = pr - pb
        rel_op = abs(orr - ob) / ob * 100
        if rel_op > 10:
            ok_ctrl = False
        print(f"   {f'{T}pt:{S}pt':>10}  piso {pb:+.2f} -> {pr:+.2f}   mueve {dif:+.2f}   "
              f"error {eb:.2f}   {'INOCUA' if abs(dif) < eb else 'IMPORTA'}"
              f"   (operaciones {rel_op:+.1f}%)")
    print(f"\n   CONTROL (las dos particiones cubren la misma serie): "
          f"{'PASADO' if ok_ctrl else 'FALLADO'}")

    # -------------------------------------------------------------------------------------
    print("\n" + "=" * 100)
    print("(4) POR ANO CALENDARIO - el largo sigue al movimiento del ano?")
    print("   Si en un ano sin tendencia el largo tambien pierde feo, el empate era el tramo")
    print("   alcista. AVISO: empatar tampoco seria ventaja. El piso sigue siendo el piso.")
    print("=" * 100)
    for T, S in CELDAS:
        print(f"\n   celda {T}pt:{S}pt")
        print(f"   {'ano':>6}{'sesiones':>10}{'mov. del ano':>14}{'largo $/ses':>13}"
              f"{'error':>8}{'en err':>8}{'corto $/ses':>13}{'error':>8}{'en err':>8}"
              f"{'PISO':>9}")
        for a in sorted(set(anio_ses.tolist())):
            m = anio_ses == a
            ii, ff = ini_r[m], fin_r[m]
            mov = cl[ff[-1] - 1] - cl[ii[0]]
            vs, comb, op_lado, _ = medir(cl, hi, lo, ii, ff, T, S)
            pi, _ = piso(comb, op_lado, T, S)
            fila = []
            for lado in ("largo", "corto"):
                v = vs[lado]
                se = v.std(ddof=1) / np.sqrt(len(v))
                fila += [v.mean(), se, v.mean() / se]
            print(f"   {a:>6}{len(ii):>10,}{mov:>+13.1f}pt{fila[0]:>+13.2f}{fila[1]:>8.1f}"
                  f"{fila[2]:>+8.1f}{fila[3]:>+13.2f}{fila[4]:>8.1f}{fila[5]:>+8.1f}"
                  f"{pi:>+9.2f}")
    print("\n   'mov. del ano' = cierre del ultimo minuto menos cierre del primero, en puntos.")
    return pisos


if __name__ == "__main__":
    main()
