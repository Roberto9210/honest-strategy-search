"""
VENTANA G - ES LA VOLATILIDAD EL EJE DEL REGIMEN? Verificacion previa a usar terciles en el juez.

NO GASTA CARTUCHO. K = 261. Medicion descriptiva sobre muestra ya recogida (ES 1-min 2016-2019).
No hay hipotesis de mercado, no se elige entre candidatas, no se declara regla de operacion. La
caja sellada (2020-01-02 -> 2026-08-19) no se toca.

EL PROBLEMA. El piso de un candidato sin ventaja va de $3,49 (2017) a $106,03 (2018) por sesion,
factor 30 (salida_cortes.txt). Un piso promedio mide el promedio de juegos distintos. El juez va a
exigir que la ventaja aguante por REGIMEN, y el eje propuesto es la volatilidad de la sesion en
terciles. Antes de usarlo hay que verificar que el piso lo mueva la volatilidad y no otra cosa.

DOS TESTS, del mas debil al mas fuerte:
  (1) Correlacion del piso ANUAL publicado contra el rango medio de barra del anio. Son CUATRO
      puntos: cuatro observaciones no deciden nada solas y se dice. Sirve para ver si al menos
      el orden coincide.
  (2) El test que decide: el piso calculado DIRECTAMENTE por tercil de volatilidad de sesion,
      con entradas al azar y la misma maquina de dolares por sesion (cortes_y_tramo.medir). Si
      el piso es monotono en los terciles y el tercil alto es varias veces el bajo, la
      volatilidad es un eje que explica el factor 30. Si los tres pisos salen parecidos, el eje
      es otro.

CONDICION DE FALLA, escrita antes: los terciles son el eje CORRECTO si (a) el piso crece con el
tercil sin cruzarse, y (b) el cociente alto/bajo es >= 3 (contra el factor 30 anual: si la
volatilidad explica el regimen, tiene que reproducir buena parte de ese factor). Si falla (a)
o (b), se dice que la volatilidad no es el eje y se propone otro con lo que se vea.
"""
import numpy as np

from cortes_y_tramo import MIN_BARRAS, medir, piso
from razon_escalas import cargar_con_sesion

CELDAS = [(5, 20), (20, 10)]
# pisos anuales publicados en salida_cortes.txt (sesiones reales, sesgo del marco restado)
PISO_ANUAL = {(5, 20): {2016: 13.56, 2017: 3.49, 2018: 106.03, 2019: 48.56},
              (20, 10): {2016: 59.39, 2017: 27.52, 2018: 119.97, 2019: 84.76}}


def main():
    print("=" * 96)
    print("ES LA VOLATILIDAD EL EJE DEL REGIMEN?  verificacion previa a los terciles del juez")
    print("NO GASTA CARTUCHO. K = 261. La caja sellada no se toca.")
    print("=" * 96)
    df = cargar_con_sesion()
    cl = df["close"].to_numpy(float); hi = df["high"].to_numpy(float); lo = df["low"].to_numpy(float)
    sess = df["sess"].to_numpy(); anio = df["sess"].dt.year.to_numpy()
    corte = np.flatnonzero(sess[1:] != sess[:-1]) + 1
    ini = np.concatenate(([0], corte)); fin = np.concatenate((corte, [len(cl)]))
    keep = (fin - ini) >= MIN_BARRAS
    ini, fin = ini[keep], fin[keep]
    nses = len(ini)
    anio_ses = anio[ini]
    rango = hi - lo
    vol_ses = np.array([rango[a:b].mean() for a, b in zip(ini, fin)])
    q33, q66 = np.quantile(vol_ses, [1 / 3, 2 / 3])
    tercil = np.where(vol_ses <= q33, 0, np.where(vol_ses <= q66, 1, 2))
    print(f"\n   {nses:,} sesiones reales. Volatilidad de sesion = rango medio de barra (pt).")
    print(f"   cortes de tercil: {q33:.4f} y {q66:.4f} pt   (bajo <= {q33:.3f} < medio <= {q66:.3f} < alto)")

    # ------------------------------------------------------------ (1) cuatro puntos
    print("\n(1) PISO ANUAL PUBLICADO contra RANGO MEDIO DE BARRA DEL ANIO. n = 4: NO decide solo.")
    print(f"   {'anio':>6}{'rango medio':>13}{'piso 5:20':>11}{'piso 20:10':>12}"
          f"{'% ses tercil alto':>19}")
    anios = sorted(set(anio_ses.tolist()))
    rm = []
    for a in anios:
        m = anio_ses == a
        rm.append(vol_ses[m].mean())
        print(f"   {a:>6}{rm[-1]:>13.4f}{PISO_ANUAL[(5, 20)][a]:>11.2f}{PISO_ANUAL[(20, 10)][a]:>12.2f}"
              f"{(tercil[m] == 2).mean() * 100:>18.0f}%")
    rm = np.array(rm)
    for T, S in CELDAS:
        p = np.array([PISO_ANUAL[(T, S)][a] for a in anios])
        r = np.corrcoef(rm, p)[0, 1]
        orden_ok = np.all(np.argsort(rm) == np.argsort(p))
        print(f"   celda {T}pt:{S}pt: r = {r:+.3f} sobre 4 puntos; el ORDEN de los anios "
              f"{'coincide' if orden_ok else 'NO coincide'} entre rango y piso.")
    print("   Lectura: cuatro puntos no establecen nada; el test que decide es el (2).")

    # ------------------------------------------------------------ (2) piso por tercil, directo
    print("\n(2) PISO POR TERCIL DE VOLATILIDAD, calculado directo con entradas al azar.")
    print("   CONDICION DE FALLA (escrita antes): eje correcto si el piso crece con el tercil sin")
    print("   cruzarse Y el cociente alto/bajo es >= 3. Si no, la volatilidad no es el eje.")
    ok_total = True
    for T, S in CELDAS:
        print(f"\n   celda {T}pt:{S}pt")
        print(f"   {'tercil':>8}{'sesiones':>10}{'$/sesion':>11}{'error':>8}{'op/ses':>8}{'PISO':>10}"
              f"{'2016':>7}{'2017':>7}{'2018':>7}{'2019':>7}")
        pisos = []
        for t, nom in ((0, "bajo"), (1, "medio"), (2, "alto")):
            m = tercil == t
            ii, ff = ini[m], fin[m]
            vs, comb, op_lado, _ = medir(cl, hi, lo, ii, ff, T, S)
            pi, _ = piso(comb, op_lado, T, S)
            pisos.append(pi)
            por_anio = [int((anio_ses[m] == a).sum()) for a in anios]
            print(f"   {nom:>8}{m.sum():>10,}{comb.mean():>+11.2f}{comb.std(ddof=1)/np.sqrt(m.sum()):>8.2f}"
                  f"{op_lado:>8.2f}{pi:>+10.2f}" + "".join(f"{x:>7}" for x in por_anio))
        mono = pisos[0] < pisos[1] < pisos[2]
        coc = pisos[2] / pisos[0] if pisos[0] > 0 else float("inf")
        ok = mono and coc >= 3.0
        ok_total &= ok
        print(f"   monotono: {'SI' if mono else 'NO'}   cociente alto/bajo: {coc:.1f}x   "
              f"-> {'EJE CORRECTO' if ok else 'EJE INCORRECTO'}")
    print("\n" + "=" * 96)
    if ok_total:
        print("VEREDICTO: la volatilidad de sesion en terciles ES el eje del regimen. El juez la usa.")
    else:
        print("VEREDICTO: la volatilidad de sesion NO explica el piso. Hay que proponer otro eje.")
    print("   Aviso de independencia: los terciles mezclan anios (ver columnas), asi que el")
    print("   contraste entre terciles NO es el contraste entre anios y no hereda su n = 4.")
    print("=" * 96)


if __name__ == "__main__":
    main()
