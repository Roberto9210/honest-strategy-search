"""
VENTANA G - el TERCER RESULTADO: medir el valor a mercado de las operaciones que quedan
abiertas al corte, y perseguir la anomalia de las 5 sesiones.

NO GASTA CARTUCHO. K = 261. Medicion descriptiva sobre muestra ya recogida.

POR QUE. sim_bracket no tiene estado "abierta al corte": cada operacion es win o -loss,
binaria, o sea que supone resolucion del 100%. Medido, entre el 7% y el 35% no resuelve en
una sesion. Para agregar ese estado al modelo hace falta saber CUANTO valen esas
operaciones, y eso se mide, no se supone.

Se aprovecha la misma carga de datos para la anomalia que quedo sin perseguir: la regla
sesgo ~ -0,5 x asimetria x (% sin resolver) ajusta con error <=0,12 en nueve celdas y falla
con error 1,32 justo a 5 sesiones en 20pt:10pt y 10pt:20pt. Si sube a 100.000 rutas y
desaparece, era ruido. Si no desaparece, a horizonte largo hay algo ademas de la censura.
"""
import os

import numpy as np

from linea_base import cargar, CELDAS

SESION = 1380
NPATHS_M2M = 60_000
NPATHS_ANOM = 100_000
SEMILLA = 20260904
AQUI = os.path.dirname(os.path.abspath(__file__))


def replica_m2m(cl, hi, lo, con, T_pt, S_pt, lado, horizonte, npaths, semilla=SEMILLA):
    """Como linea_base.replica pero ademas devuelve el valor a mercado, en PUNTOS, de las
    que quedan abiertas al corte."""
    rng = np.random.default_rng(semilla)
    n = len(cl)
    ent = rng.integers(0, n - horizonte - 1, npaths)
    ent = ent[con[ent] == con[ent + horizonte]]
    entrada = cl[ent]
    if lado == "largo":
        objetivo, stop = entrada + T_pt, entrada - S_pt
    else:
        objetivo, stop = entrada - T_pt, entrada + S_pt

    vivo = np.ones(len(ent), dtype=bool)
    gana = np.zeros(len(ent), dtype=bool)
    pierde = np.zeros(len(ent), dtype=bool)
    amb = np.zeros(len(ent), dtype=bool)

    for k in range(1, horizonte + 1):
        if not vivo.any():
            break
        j = ent + k
        h, l = hi[j], lo[j]
        if lado == "largo":
            t_obj, t_stop = h >= objetivo, l <= stop
        else:
            t_obj, t_stop = l <= objetivo, h >= stop
        a = vivo & t_obj & t_stop
        g = vivo & t_obj & ~t_stop
        p = vivo & t_stop & ~t_obj
        amb |= a; gana |= g; pierde |= p
        vivo &= ~(a | g | p)

    salida = cl[ent + horizonte]
    m2m = (salida - entrada) if lado == "largo" else (entrada - salida)
    return dict(n=len(ent), gana=int(gana.sum()), pierde=int(pierde.sum()),
                amb=int(amb.sum()), vivo=int(vivo.sum()), m2m=m2m[vivo])


def parte_m2m(cl, hi, lo, con):
    print("=" * 100)
    print("1. VALOR A MERCADO DE LAS QUE QUEDAN ABIERTAS AL CORTE (horizonte 1 sesion)")
    print("=" * 100)
    print("   En PUNTOS de ES. Positivo = a favor. Es lo que cobra o paga un operador que")
    print("   aplana al cierre en vez de aguantar.\n")
    print(f"   {'bracket':>11}{'sin resolver':>14}{'n abiertas':>12}{'media':>9}{'p50':>8}"
          f"{'p10':>8}{'p90':>8}{'min':>9}{'max':>8}")
    guardado = {}
    for T, S in CELDAS:
        muestras = []
        viv = nn = 0
        for lado in ("largo", "corto"):
            r = replica_m2m(cl, hi, lo, con, T, S, lado, SESION, NPATHS_M2M)
            muestras.append(r["m2m"]); viv += r["vivo"]; nn += r["n"]
        m = np.concatenate(muestras)
        guardado[(T, S)] = m
        print(f"   {f'{T}pt:{S}pt':>11}{viv/nn*100:>13.1f}%{len(m):>12,}{m.mean():>9.3f}"
              f"{np.median(m):>8.2f}{np.percentile(m,10):>8.2f}{np.percentile(m,90):>8.2f}"
              f"{m.min():>9.2f}{m.max():>8.2f}")
        np.save(os.path.join(AQUI, f"m2m_{T}_{S}.npy"), m)
    print("\n   Guardadas las muestras en m2m_T_S.npy para que el modelo las remuestree.")
    print("   Notar el signo de la media: dice si aplanar al cierre cobra o paga.")
    return guardado


def parte_anomalia(cl, hi, lo, con):
    print("\n" + "=" * 100)
    print(f"2. LA ANOMALIA DE LAS 5 SESIONES, con {NPATHS_ANOM:,} rutas (antes 20.000)")
    print("=" * 100)
    print("   Si el error de la regla se achica, era ruido. Si no, hay algo mas.\n")
    print(f"   {'bracket':>11}{'asim':>8}{'sin res':>9}{'sesgo medido':>14}"
          f"{'regla predice':>15}{'error 20k':>11}{'error 100k':>12}")
    err_previo = {(5, 10): -0.22, (10, 10): 0.00, (20, 10): 1.32, (5, 20): -0.94,
                   (10, 20): -1.32}
    h = 5 * SESION
    for T, S in CELDAS:
        asum = S / (S + T)
        asim = (T - S) / (T + S)
        g = res = viv = nn = 0
        for lado in ("largo", "corto"):
            r = replica_m2m(cl, hi, lo, con, T, S, lado, h, NPATHS_ANOM)
            g += r["gana"]; res += r["gana"] + r["pierde"] + r["amb"]
            viv += r["vivo"]; nn += r["n"]
        sesgo = (g / res - asum) * 100
        sin_res = viv / nn * 100
        pred = -0.5 * asim * sin_res
        print(f"   {f'{T}pt:{S}pt':>11}{asim:>+8.3f}{sin_res:>8.1f}%{sesgo:>+14.2f}"
              f"{pred:>+15.2f}{err_previo[(T,S)]:>+11.2f}{pred-sesgo:>+12.2f}")
    print("\n   'error 20k' es el de la corrida anterior; 'error 100k' el de esta.")


if __name__ == "__main__":
    cl, hi, lo, con = cargar()
    parte_m2m(cl, hi, lo, con)
    parte_anomalia(cl, hi, lo, con)
