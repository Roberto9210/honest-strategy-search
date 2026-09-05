"""
VENTANA G - EL EJE DEL REGIMEN, PERO CONOCIBLE AL ENTRAR. Corrige el defecto (b) de la tanda anterior.

NO GASTA CARTUCHO. K = 261. Medicion descriptiva sobre muestra ya recogida (ES 1-min 2016-2019). No
hay hipotesis de mercado, no se elige entre candidatas, no se declara regla de operacion. La caja
sellada no se toca.

EL DEFECTO. juez_regimen.py clasifico las sesiones por la volatilidad de la sesion ENTERA (rango
medio de barra de 17:00 CT a 16:00 CT), que incluye lo que paso DESPUES de cada entrada. Para
describir el piso vale; para EXIGIRLE a un candidato que aguante en cada regimen, le pregunta por
algo que no podia conocer al entrar. Aca se recalculan los pisos por tercil con ejes conocibles al
entrar y se decide si el veredicto por regimen se queda, cambia de eje, o se saca.

LOS EJES EX-ANTE:
  ANTERIOR  volatilidad (rango medio de barra) de la sesion ANTERIOR.
  HORA1     volatilidad de la PRIMERA HORA de la sesion en curso (17:00-18:00 CT, las primeras
            60 barras). Conocible para toda entrada posterior a las 18:00 CT.
  PREV4     mi tercero: media de la volatilidad de las CUATRO sesiones anteriores. Justificacion
            DEL DATO: el plazo de agrupamiento de volatilidad medido en bloques.py es L* = 5.520
            barras = 4,00 sesiones; promediar sobre ese plazo deberia predecir la sesion en curso
            con menos ruido que una sola sesion anterior.
  HINDSIGHT la sesion entera, como en juez_regimen.py, solo de referencia. No se juzga con el.

CONDICION ESCRITA ANTES DE CORRER, la misma vara que con el eje de hindsight: un eje ex-ante SIRVE
si el piso es monotono en sus terciles (bajo < medio < alto, sin cruces) Y el cociente alto/bajo
es >= 3. Si el factor 52 (5pt:20pt) colapsa a algo cercano a 1, el eje ex-ante no existe.

MI EXPECTATIVA, escrita antes de mirar (para que se vea si me sorprendio): el agrupamiento existe
(L* = 4 sesiones), asi que ANTERIOR deberia conservar la monotonia con un cociente mucho menor que
52, quiza entre 3 y 10. PREV4 deberia ser el mejor de los tres por promediar el ruido. HORA1 deberia
ser el peor: la hora 17:00-18:00 CT es la mas fina del dia. No se cual cae bajo 3.

LAS DOS SALIDAS SON VALIDAS. Si un eje ex-ante pasa, el juez cambia a ese eje y el veredicto por
regimen queda. Si ninguno pasa, el veredicto por regimen se SACA del juez -no se deja con una
advertencia- porque una funcion que no se puede accionar da falsa confianza. En los dos casos, el
eje de hindsight puede seguir sirviendo para DESCRIBIR el piso, con nombre distinto.
"""
import numpy as np

from cortes_y_tramo import MIN_BARRAS, medir, piso
from razon_escalas import cargar_con_sesion

CELDAS = [(5, 20), (20, 10)]
HORA1 = 60          # barras de la primera hora
PREV = 4            # sesiones anteriores promediadas (L* = 4,00 sesiones, bloques.py)
VARA = 3.0


def terciles(v):
    q33, q66 = np.quantile(v, [1 / 3, 2 / 3])
    return np.where(v <= q33, 0, np.where(v <= q66, 1, 2)), (float(q33), float(q66))


def main():
    print("=" * 96)
    print("EL EJE DEL REGIMEN CONOCIBLE AL ENTRAR - pisos por tercil con tres ejes ex-ante")
    print("NO GASTA CARTUCHO. K = 261. La caja sellada no se toca.")
    print("=" * 96)
    df = cargar_con_sesion()
    cl = df["close"].to_numpy(float); hi = df["high"].to_numpy(float); lo = df["low"].to_numpy(float)
    sess = df["sess"].to_numpy()
    corte = np.flatnonzero(sess[1:] != sess[:-1]) + 1
    ini = np.concatenate(([0], corte)); fin = np.concatenate((corte, [len(cl)]))
    keep = (fin - ini) >= MIN_BARRAS
    ini, fin = ini[keep], fin[keep]
    nses = len(ini)
    rango = hi - lo
    vol_full = np.array([rango[a:b].mean() for a, b in zip(ini, fin)])
    vol_h1 = np.array([rango[a:min(a + HORA1, b)].mean() for a, b in zip(ini, fin)])
    vol_prev = np.concatenate([[np.nan], vol_full[:-1]])
    vol_prev4 = np.array([vol_full[max(0, k - PREV):k].mean() if k >= 1 else np.nan for k in range(nses)])

    ejes = {"HINDSIGHT (sesion entera, referencia)": vol_full,
            "ANTERIOR (sesion anterior)": vol_prev,
            "HORA1 (primera hora, 17-18 CT)": vol_h1,
            f"PREV{PREV} (media de {PREV} sesiones anteriores)": vol_prev4}

    # ------------------------------------------------ 1. cuanto predice cada eje la sesion entera
    print(f"\n   {nses:,} sesiones reales. Volatilidad = rango medio de barra (pt).")
    print("\n(1) CUANTO PREDICE CADA EJE LA VOLATILIDAD DE LA SESION ENTERA (Spearman, y % de sesiones")
    print("    cuyo tercil ex-ante coincide con el tercil de hindsight).")
    def spearman(a, b):
        ra = np.argsort(np.argsort(a)).astype(float); rb = np.argsort(np.argsort(b)).astype(float)
        return float(np.corrcoef(ra, rb)[0, 1])
    t_full, _ = terciles(vol_full)
    for nom, v in ejes.items():
        ok = ~np.isnan(v)
        rho = spearman(v[ok], vol_full[ok])
        t_v, _ = terciles(v[ok])
        coinc = (t_v == t_full[ok]).mean() * 100
        print(f"   {nom:<44} rho = {rho:+.3f}   coincide {coinc:5.1f}%   (azar 33,3%)")

    # ------------------------------------------------ 2. el piso por tercil, cada eje
    print("\n(2) PISO POR TERCIL, entradas al azar, misma maquina (cortes_y_tramo.medir).")
    print(f"    CONDICION (escrita antes): sirve si es monotono y alto/bajo >= {VARA:.0f}x.")
    veredictos = {}
    for T, S in CELDAS:
        print(f"\n   celda {T}pt:{S}pt")
        print(f"   {'eje':<44}{'bajo':>9}{'medio':>9}{'alto':>9}{'alto/bajo':>11}{'monotono':>10}{'sirve':>8}")
        for nom, v in ejes.items():
            ok = ~np.isnan(v)
            t_v, _ = terciles(v[ok])
            idx_ok = np.flatnonzero(ok)
            pisos = []
            for t in (0, 1, 2):
                m = idx_ok[t_v == t]
                vs, comb, op_lado, _ = medir(cl, hi, lo, ini[m], fin[m], T, S)
                pi, _ = piso(comb, op_lado, T, S)
                pisos.append(pi)
            mono = pisos[0] < pisos[1] < pisos[2]
            coc = pisos[2] / pisos[0] if pisos[0] > 0 else float("inf")
            sirve = mono and coc >= VARA
            veredictos[(T, S, nom)] = (sirve, coc, mono, pisos)
            print(f"   {nom:<44}{pisos[0]:>+9.2f}{pisos[1]:>+9.2f}{pisos[2]:>+9.2f}{coc:>10.1f}x"
                  f"{('SI' if mono else 'NO'):>10}{('SI' if sirve else 'no'):>8}")

    # ------------------------------------------------ 3. veredicto
    print("\n" + "=" * 96)
    exante = [n for n in ejes if not n.startswith("HINDSIGHT")]
    pasa = {n: all(veredictos[(T, S, n)][0] for T, S in CELDAS) for n in exante}
    mejor = None
    if any(pasa.values()):
        mejor = max((n for n in exante if pasa[n]),
                    key=lambda n: min(veredictos[(T, S, n)][1] for T, S in CELDAS))
        print(f"VEREDICTO: el eje ex-ante EXISTE. El mejor es {mejor}: pasa la vara en las dos celdas")
        print("   con el mayor cociente minimo. El juez cambia a ese eje; el veredicto por regimen queda.")
    else:
        print("VEREDICTO: NINGUN eje ex-ante pasa la vara en las dos celdas. El veredicto por regimen")
        print("   describe algo que nadie puede accionar al entrar: se SACA del juez.")
    for n in exante:
        cs = "  ".join(f"{T}:{S} {veredictos[(T, S, n)][1]:.1f}x{'' if veredictos[(T, S, n)][2] else '(cruza)'}"
                       for T, S in CELDAS)
        print(f"   {n:<44} {'PASA' if pasa[n] else 'no pasa'}   {cs}")
    print("   El eje de HINDSIGHT sigue sirviendo para DESCRIBIR el piso (juez_regimen.py), no para juzgar.")
    print("=" * 96)


if __name__ == "__main__":
    main()
