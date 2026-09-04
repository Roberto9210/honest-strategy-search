"""
VENTANA G - EL SEGUNDO EJE DEL REGIMEN: la DIRECCION, ex-ante. Separa los pisos tanto como la volatilidad?

NO GASTA CARTUCHO. K = 261. Medicion descriptiva sobre muestra ya recogida (ES 1-min 2016-2019). No
hay hipotesis de mercado, no se elige entre candidatas, no se declara regla de operacion. La caja
sellada no se toca.

EL AGUJERO. El juez mide el regimen en una sola dimension, la volatilidad. Pero la direccion tambien
es regimen: en 2018 (el unico anio a la baja) el largo perdio MAS que el corto y el orden se invirtio
(salida_cortes.txt). Un candidato puede aguantar los tres terciles de volatilidad y seguir siendo una
apuesta a la tendencia; 2016-2019 es mayormente alcista, asi que el sesgo esta vivo.

EL EJE, ex-ante (conocible al entrar): el SIGNO del movimiento neto de la sesion ANTERIOR
(cierre de la ultima barra menos cierre de la primera). Y una variante tambien ex-ante, porque la
inversion de 2018 fue de meses y no de un dia: el signo del movimiento neto de las 20 sesiones
anteriores. Se prueban las dos.

QUE SE MIDE. Con entradas al azar y la misma maquina de dolares (cortes_y_tramo.medir), el piso del
LARGO, del CORTO y el combinado, por celda de direccion (anterior al alza / a la baja), y al lado el
mismo desglose por tercil ex-ante de volatilidad, para comparar en la misma unidad.

CONDICION ESCRITA ANTES DE CORRER. La volatilidad separa el piso combinado 20,8x (5pt:20pt) y 5,1x
(20pt:10pt) entre terciles extremos. Considero que la direccion separa de forma COMPARABLE si, en
alguna de sus dos variantes y en alguna celda (5:20 o 20:10), el piso de UN MISMO LADO (largo o corto)
o el combinado difiere entre 'anterior al alza' y 'anterior a la baja' por un factor >= 3x, la misma
vara que se le pidio a la volatilidad, Y esa diferencia supera 3 errores estandar. Si el factor queda
por debajo de 3x, la direccion NO separa: la pasiva ya cubre la tendencia y el eje no hace falta.

MI EXPECTATIVA, escrita antes de mirar: el signo de UNA sesion casi no predice la siguiente (la
autocorrelacion diaria de ES es ~0), asi que espero factores cerca de 1x para la variante de una
sesion. La variante de 20 sesiones podria separar algo por lado (largo mas barato tras 20 sesiones al
alza), pero dudo que llegue a 3x. Espero "no separa" en las dos. Si separa, me sorprendio y lo digo.
"""
import numpy as np

from cortes_y_tramo import MIN_BARRAS, medir, piso
from razon_escalas import cargar_con_sesion

CELDAS = [(5, 20), (20, 10)]
VARA = 3.0
N_LARGO = 20


def pisos_por_lado(cl, hi, lo, ini, fin, T, S):
    vs, comb, op_lado, _ = medir(cl, hi, lo, ini, fin, T, S)
    out = {}
    for nom, v in (("largo", vs["largo"]), ("corto", vs["corto"]), ("comb", comb)):
        pi, _ = piso(v, op_lado, T, S)
        out[nom] = (pi, float(v.std(ddof=1) / np.sqrt(len(v))))
    return out, op_lado


def main():
    print("=" * 100)
    print("EL SEGUNDO EJE DEL REGIMEN: DIRECCION EX-ANTE. Separa los pisos como la volatilidad?")
    print("NO GASTA CARTUCHO. K = 261. La caja sellada no se toca.")
    print("=" * 100)
    df = cargar_con_sesion()
    cl = df["close"].to_numpy(float); hi = df["high"].to_numpy(float); lo = df["low"].to_numpy(float)
    sess = df["sess"].to_numpy()
    corte = np.flatnonzero(sess[1:] != sess[:-1]) + 1
    ini = np.concatenate(([0], corte)); fin = np.concatenate((corte, [len(cl)]))
    keep = (fin - ini) >= MIN_BARRAS
    ini, fin = ini[keep], fin[keep]
    nses = len(ini)
    mov = np.array([cl[b - 1] - cl[a] for a, b in zip(ini, fin)])
    rango = hi - lo
    vol = np.array([rango[a:b].mean() for a, b in zip(ini, fin)])
    prev_vol = np.concatenate([[np.nan], vol[:-1]])
    p33, p66 = np.nanquantile(prev_vol, [1 / 3, 2 / 3])
    terc = np.where(np.isnan(prev_vol), -1, np.where(prev_vol <= p33, 0, np.where(prev_vol <= p66, 1, 2)))
    dir1 = np.concatenate([[0.0], np.sign(mov[:-1])])
    cum = np.concatenate([[0.0], np.cumsum(mov)])
    dir20 = np.array([np.sign(cum[k] - cum[k - N_LARGO]) if k >= N_LARGO else 0.0 for k in range(nses)])
    print(f"\n   {nses:,} sesiones. Direccion ex-ante: signo del movimiento neto de la sesion anterior (dir1)"
          f" y de las {N_LARGO} anteriores (dir{N_LARGO}).")
    print(f"   dir1: {int((dir1 > 0).sum())} al alza / {int((dir1 < 0).sum())} a la baja.  "
          f"dir{N_LARGO}: {int((dir20 > 0).sum())} al alza / {int((dir20 < 0).sum())} a la baja.")
    print(f"   CONDICION (escrita antes): separa si algun piso (largo, corto o comb) difiere >= {VARA:.0f}x "
          f"entre alza y baja, con diferencia > 3 errores.")

    ejes = {"volatilidad ex-ante (referencia)": [("bajo", terc == 0), ("alto", terc == 2)],
            "dir1: sesion anterior": [("al alza", dir1 > 0), ("a la baja", dir1 < 0)],
            f"dir{N_LARGO}: {N_LARGO} sesiones anteriores": [("al alza", dir20 > 0), ("a la baja", dir20 < 0)]}
    separa_alguna = False
    for T, S in CELDAS:
        print(f"\n   celda {T}pt:{S}pt")
        print(f"   {'eje':<36}{'celda':<11}{'ses':>5}{'piso largo':>12}{'err':>6}{'piso corto':>12}{'err':>6}"
              f"{'piso comb':>11}{'err':>6}{'op/ses':>8}")
        for nom_eje, celdas in ejes.items():
            res = {}
            for nom_c, m in celdas:
                out, op = pisos_por_lado(cl, hi, lo, ini[m], fin[m], T, S)
                res[nom_c] = out
                print(f"   {nom_eje:<36}{nom_c:<11}{int(m.sum()):>5}{out['largo'][0]:>+12.2f}{out['largo'][1]:>6.1f}"
                      f"{out['corto'][0]:>+12.2f}{out['corto'][1]:>6.1f}{out['comb'][0]:>+11.2f}{out['comb'][1]:>6.1f}"
                      f"{op:>8.2f}")
            a, b = [res[c] for c, _ in celdas]
            linea = []
            for lado in ("largo", "corto", "comb"):
                x, ex = a[lado]; y, ey = b[lado]
                lo_, hi_ = sorted([x, y], key=abs)
                factor = abs(hi_) / abs(lo_) if lo_ != 0 else float("inf")
                cruza = (x > 0) != (y > 0)
                z = abs(x - y) / np.sqrt(ex ** 2 + ey ** 2) if (ex or ey) else 0.0
                sep = (factor >= VARA or cruza) and z > 3.0
                if "referencia" not in nom_eje:
                    separa_alguna |= sep
                linea.append(f"{lado} {factor:.1f}x{' (cambia signo)' if cruza else ''} {z:.1f}err{' SEPARA' if sep else ''}")
            print(f"   {'':<36}{'-> ':<11}" + " | ".join(linea))
    # ---------------------------------------------------------------------------------------
    # TEST AGREGADO DESPUES DE VER EL PRIMER RESULTADO, y se dice: el combinado separo por
    # direccion, pero con las operaciones por sesion subiendo 4,6 -> 6,5 y 3,6 -> 9,8 tras una
    # sesion a la baja, que es la firma de la VOLATILIDAD (una sesion a la baja anticipa una
    # volatil). Si la direccion es volatilidad disfrazada, dentro de cada tercil de volatilidad no
    # tiene que separar nada. MISMA REGLA de decision, aplicada dentro del estrato: >= 3x y > 3 err.
    # ---------------------------------------------------------------------------------------
    print("\n" + "=" * 100)
    print(f"DIRECCION DENTRO DE CADA TERCIL DE VOLATILIDAD (dir{N_LARGO}). Si separa aca, es direccion de verdad;")
    print("si no, era volatilidad disfrazada. Misma regla: >= 3x y > 3 errores, en comb o en un lado.")
    print("=" * 100)
    separa_estrato = False
    for T, S in CELDAS:
        print(f"\n   celda {T}pt:{S}pt")
        print(f"   {'tercil vol':<12}{'direccion':<11}{'ses':>5}{'piso largo':>12}{'err':>6}{'piso corto':>12}{'err':>6}"
              f"{'piso comb':>11}{'err':>6}{'op/ses':>8}")
        for t, nom_t in ((0, "bajo"), (1, "medio"), (2, "alto")):
            res = {}
            for nom_c, md in (("al alza", dir20 > 0), ("a la baja", dir20 < 0)):
                m = (terc == t) & md
                if m.sum() < 30:
                    print(f"   {nom_t:<12}{nom_c:<11}{int(m.sum()):>5}   (menos de 30 sesiones: sin datos)")
                    continue
                out, op = pisos_por_lado(cl, hi, lo, ini[m], fin[m], T, S)
                res[nom_c] = out
                print(f"   {nom_t:<12}{nom_c:<11}{int(m.sum()):>5}{out['largo'][0]:>+12.2f}{out['largo'][1]:>6.1f}"
                      f"{out['corto'][0]:>+12.2f}{out['corto'][1]:>6.1f}{out['comb'][0]:>+11.2f}{out['comb'][1]:>6.1f}{op:>8.2f}")
            if len(res) == 2:
                a, b = res["al alza"], res["a la baja"]
                linea = []
                for lado in ("largo", "corto", "comb"):
                    x, ex = a[lado]; y, ey = b[lado]
                    lo_, hi_ = sorted([x, y], key=abs)
                    factor = abs(hi_) / abs(lo_) if lo_ != 0 else float("inf")
                    cruza = (x > 0) != (y > 0)
                    z = abs(x - y) / np.sqrt(ex ** 2 + ey ** 2) if (ex or ey) else 0.0
                    sep = (factor >= VARA or cruza) and z > 3.0
                    separa_estrato |= sep
                    linea.append(f"{lado} {factor:.1f}x{' (signo)' if cruza else ''} {z:.1f}err{' SEPARA' if sep else ''}")
                print(f"   {'':<12}{'-> ':<11}" + " | ".join(linea))
    print("\n" + "=" * 100)
    if separa_alguna and separa_estrato:
        print("VEREDICTO: la DIRECCION ex-ante separa los pisos TAMBIEN dentro de los terciles de volatilidad.")
        print("   Es un regimen propio. El juez pasa a exigir que la ventaja aguante en las dos dimensiones.")
    elif separa_alguna:
        print("VEREDICTO: la direccion separo el piso COMBINADO en bruto, pero NO dentro de los terciles de")
        print("   volatilidad, y nunca separo un lado solo: era VOLATILIDAD DISFRAZADA (una sesion a la baja")
        print("   anticipa una volatil). El juez ya condiciona por volatilidad; la pasiva cubre la tendencia")
        print("   del rango. El segundo eje NO hace falta. Se cierra.")
    else:
        print("VEREDICTO: la direccion ex-ante NO separa los pisos con la vara de >= 3x y 3 errores.")
        print("   La pasiva ya cubre la tendencia del rango; el segundo eje no hace falta. Se cierra.")
    print("=" * 100)


if __name__ == "__main__":
    main()
