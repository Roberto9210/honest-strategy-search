"""
VENTANA G - EL EJE DEL REGIMEN EN PUNTOS BASICOS: era volatilidad o era EPOCA disfrazada?

NO GASTA CARTUCHO. K = 261. Medicion descriptiva sobre muestra ya recogida (ES 1-min 2016-2019). No
hay hipotesis de mercado, no se elige entre candidatas, no se declara regla de operacion. La caja
sellada no se toca.

EL AGUJERO (mi propio (b) de la tanda anterior). El eje de regimen del juez esta en PUNTOS. Dentro de
2016-2019 el indice fue de ~1.800 a ~3.200, asi que el rango de barra en puntos crece con el PRECIO
aunque el mercado no sea mas volatil en terminos relativos. El "tercil alto" en puntos puede ser en
parte "2018-2019, cuando el indice valia mas". El cociente 20,8x podria llevar adentro un efecto de
epoca. Va ANTES de medir el costo de los datos comprados, porque ese costo se mide POR REGIMEN: si el
eje esta mal definido, esa medicion sale mal.

QUE SE MIDE. Se recalcula el eje ex-ante en PUNTOS BASICOS -rango medio de barra / precio medio de la
sesion * 1e4-, la unidad que ya use para clasificar 2026 y que viaja entre epocas. Y se contesta:
  a) el cociente alto/bajo del piso se sostiene o se cae?
  b) cuantas sesiones cambian de etiqueta de tercil al pasar de puntos a bps?
  c) las etiquetas en puntos se concentran por anio? Si el tercil alto en puntos es mayormente
     2018-2019 y el de bps se reparte parejo, esa es la evidencia directa de epoca disfrazada.

CONDICION ESCRITA ANTES DE CORRER. "SE SOSTIENE" = el piso por tercil bps es monotono (bajo < medio
< alto, sin cruces) Y el cociente alto/bajo es >= 3x en las DOS celdas, la misma vara de siempre.
Umbral de cambio de etiquetas: si cambian <= 33% de las sesiones, los dos ejes miden casi lo mismo y
la unidad no cambio el objeto; si cambian mas de 33%, son objetos materialmente distintos y (c)
decide cual mide regimen y cual mide epoca.

MI EXPECTATIVA, escrita antes de mirar (para que se vea si me sorprendio). Como el rango en puntos =
precio * (rango en bps), el eje en puntos conflaciona nivel de precio con volatilidad relativa.
Espero: (b) MAS del 33% de las sesiones cambian de etiqueta; (c) el tercil alto en puntos concentrado
en 2018-2019 y el de bps repartido mas parejo. Y (a) -la que no se- creo que el factor bps SE
SOSTIENE por encima de 3x pero MENOR que 20,8x (entre 5x y 15x), porque bps sigue capturando el
agrupamiento real de volatilidad, sin la inflacion por nivel de precio. Si el factor bps se cae cerca
de 1x, la mayor parte del 20,8x era nivel de precio: seria un hallazgo fuerte e incomodo y lo digo.

TENSION QUE HAY QUE TENER PRESENTE, y la escribo antes: el bracket del juez es fijo en PUNTOS
(5pt:20pt). Para un candidato ENTERO dentro de 2016-2019, el piso -que es en dolares, o sea en
puntos- lo gobierna el rango en PUNTOS, no en bps. O sea que el eje en puntos podria ser el
economicamente correcto DENTRO de una epoca, y el de bps el correcto para COMPARAR epocas (un
bracket de 20pt es 1,1% del precio en 2016 y 0,26% en 2026: no es el mismo instrumento). Los dos
pueden tener razon para preguntas distintas. La medicion decide cuanto de cada cosa hay.
"""
import numpy as np

from cortes_y_tramo import MIN_BARRAS, medir, piso
from razon_escalas import cargar_con_sesion

CELDAS = [(5, 20), (20, 10)]
VARA = 3.0
UMBRAL_CAMBIO = 0.33


def terciles(v):
    ok = ~np.isnan(v)
    q33, q66 = np.nanquantile(v, [1 / 3, 2 / 3])
    t = np.where(~ok, -1, np.where(v <= q33, 0, np.where(v <= q66, 1, 2)))
    return t, (float(q33), float(q66))


def pisos_por_tercil(cl, hi, lo, ini, fin, tercil, T, S):
    out = []
    for t in (0, 1, 2):
        m = tercil == t
        vs, comb, op_lado, _ = medir(cl, hi, lo, ini[m], fin[m], T, S)
        pi, _ = piso(comb, op_lado, T, S)
        out.append(pi)
    return out


def main():
    print("=" * 98)
    print("EL EJE DEL REGIMEN EN PUNTOS BASICOS: era volatilidad o epoca disfrazada?")
    print("NO GASTA CARTUCHO. K = 261. La caja sellada no se toca.")
    print("=" * 98)
    df = cargar_con_sesion()
    cl = df["close"].to_numpy(float); hi = df["high"].to_numpy(float); lo = df["low"].to_numpy(float)
    sess = df["sess"].to_numpy(); anio = df["sess"].dt.year.to_numpy()
    corte = np.flatnonzero(sess[1:] != sess[:-1]) + 1
    ini = np.concatenate(([0], corte)); fin = np.concatenate((corte, [len(cl)]))
    keep = (fin - ini) >= MIN_BARRAS
    ini, fin = ini[keep], fin[keep]
    nses = len(ini); anio_ses = anio[ini]
    rango = hi - lo
    vol_pt = np.array([rango[a:b].mean() for a, b in zip(ini, fin)])
    px = np.array([cl[a:b].mean() for a, b in zip(ini, fin)])
    vol_bps = vol_pt / px * 1e4
    prev_pt = np.concatenate([[np.nan], vol_pt[:-1]])
    prev_bps = np.concatenate([[np.nan], vol_bps[:-1]])
    t_pt, cortes_pt = terciles(prev_pt)
    t_bps, cortes_bps = terciles(prev_bps)
    print(f"\n   {nses:,} sesiones. Eje ex-ante = volatilidad de la sesion ANTERIOR.")
    print(f"   cortes en puntos:  bajo <= {cortes_pt[0]:.4f} < medio <= {cortes_pt[1]:.4f} < alto")
    print(f"   cortes en bps:     bajo <= {cortes_bps[0]:.3f} < medio <= {cortes_bps[1]:.3f} < alto")

    # ------------------------------------------------------------------ (a) el factor
    print("\n(a) PISO POR TERCIL, entradas al azar, misma maquina (cortes_y_tramo.medir).")
    print(f"    'se sostiene' = monotono Y alto/bajo >= {VARA:.0f}x en las dos celdas.")
    ok = ~np.isnan(prev_bps)
    factores = {}
    for T, S in CELDAS:
        print(f"\n   celda {T}pt:{S}pt")
        print(f"   {'eje':<18}{'bajo':>9}{'medio':>9}{'alto':>9}{'alto/bajo':>11}{'monotono':>10}{'sostiene':>10}")
        for nom, t in (("PUNTOS (viejo)", t_pt), ("BPS (nuevo)", t_bps)):
            pis = pisos_por_tercil(cl, hi, lo, ini, fin, t, T, S)
            mono = pis[0] < pis[1] < pis[2]
            coc = pis[2] / pis[0] if pis[0] > 0 else float("inf")
            sost = mono and coc >= VARA
            factores[(T, S, nom)] = (coc, mono, sost, pis)
            print(f"   {nom:<18}{pis[0]:>+9.2f}{pis[1]:>+9.2f}{pis[2]:>+9.2f}{coc:>10.1f}x"
                  f"{('SI' if mono else 'NO'):>10}{('SI' if sost else 'no'):>10}")

    # ------------------------------------------------------------------ (b) cambio de etiquetas
    cambia = (t_pt != t_bps) & ok
    frac = cambia.sum() / ok.sum()
    print(f"\n(b) CAMBIO DE ETIQUETA puntos -> bps: {int(cambia.sum())} de {int(ok.sum())} sesiones "
          f"({frac:.0%}). Umbral {UMBRAL_CAMBIO:.0%}.")
    print(f"    {'de\\a bps':>10}{'bajo':>8}{'medio':>8}{'alto':>8}   (fila = tercil en puntos)")
    for tp, nomp in ((0, "bajo"), (1, "medio"), (2, "alto")):
        fila = [int(((t_pt == tp) & (t_bps == tb) & ok).sum()) for tb in (0, 1, 2)]
        print(f"    {nomp:>10}{fila[0]:>8}{fila[1]:>8}{fila[2]:>8}")
    print(f"    -> los dos ejes miden {'CASI LO MISMO' if frac <= UMBRAL_CAMBIO else 'OBJETOS DISTINTOS'}.")

    # ------------------------------------------------------------------ (c) concentracion por anio
    print("\n(c) CONCENTRACION POR ANIO de cada tercil (% de las sesiones del tercil que caen en cada anio):")
    anios = sorted(set(anio_ses.tolist()))
    for nom, t in (("PUNTOS", t_pt), ("BPS", t_bps)):
        print(f"\n   eje {nom}:")
        print(f"   {'tercil':>8}" + "".join(f"{a:>8}" for a in anios) + f"{'dispersion':>12}")
        for tt, nomt in ((0, "bajo"), (1, "medio"), (2, "alto")):
            m = (t == tt) & ok
            fr = [((anio_ses == a) & m).sum() / max(1, m.sum()) for a in anios]
            # dispersion: 1 = repartido parejo entre 4 anios; 0 = todo en un anio (indice de uniformidad)
            disp = 1 - np.sqrt(((np.array(fr) - 0.25) ** 2).sum() / 0.75)
            print(f"   {nomt:>8}" + "".join(f"{x*100:>7.0f}%" for x in fr) + f"{disp:>12.2f}")
    print("   dispersion: 1 = repartido parejo entre los 4 anios; 0 = concentrado en uno solo.")

    # ------------------------------------------------------------------ veredicto
    print("\n" + "=" * 98)
    sost_bps = all(factores[(T, S, "BPS (nuevo)")][2] for T, S in CELDAS)
    cocs = [factores[(T, S, "BPS (nuevo)")][0] for T, S in CELDAS]
    alto_pt = [((t_pt == 2) & (anio_ses >= 2018) & ok).sum() / max(1, ((t_pt == 2) & ok).sum())]
    alto_bps = [((t_bps == 2) & (anio_ses >= 2018) & ok).sum() / max(1, ((t_bps == 2) & ok).sum())]
    if sost_bps:
        print(f"VEREDICTO: el factor SE SOSTIENE en bps ({cocs[0]:.1f}x y {cocs[1]:.1f}x, contra la vara "
              f">= 3x). El eje era volatilidad, no epoca.")
        print("   El juez pasa a bps IGUAL, porque es la unidad que viaja entre epocas y hace falta para")
        print("   comparar 2017 contra 2026.")
    else:
        print(f"VEREDICTO: el factor SE CAE en bps ({cocs[0]:.1f}x y {cocs[1]:.1f}x). Buena parte del 20,8x "
              f"era NIVEL DE PRECIO.")
        print("   El veredicto por regimen en puntos mide el anio y no el mercado. Hay que decirlo fuerte")
        print("   y decidir si se saca o se mueve a bps aun con factor menor.")
    print(f"   tercil alto en puntos que es 2018-2019: {alto_pt[0]*100:.0f}%   en bps: {alto_bps[0]*100:.0f}%")
    print("=" * 98)


if __name__ == "__main__":
    main()
