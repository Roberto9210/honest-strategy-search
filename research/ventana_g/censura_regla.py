"""
VENTANA G - la regla general de la censura por horizonte, y la pre-factibilidad del Camino 3.

NO GASTA CARTUCHO. K = 261. Medicion de una constante del modelo mas aritmetica sobre pisos
ya calculados.

PARTE 1. El sesgo de censura de los CINCO brackets (los tres que se reportaron en el chat mas
5pt:10pt y 20pt:10pt, que estaban en el archivo pero no en el resumen), a varios horizontes,
para contestar: el sesgo depende de la asimetria del bracket? Hay una banda donde es
despreciable, o solo el simetrico exacto sirve?

PARTE 2. Camino 3: que tendria que aparecer en datos de flujo de ordenes para que valga la
pena comprarlos. Solo la parte aritmetica; no se buscan precios ni se inventan hallazgos.
"""
import numpy as np

from linea_base import cargar, replica, CELDAS
from entrada_y_potencia import piezas, equilibrio, moneda, n_exacto
from piso_ventaja import mde_exacto, ritmo

SESION = 1380
HORIZONTES = [("1 sesion", SESION), ("2 sesiones", 2 * SESION), ("5 sesiones", 5 * SESION)]
NPATHS = 20_000
DIAS_MES = 21.0
PRESUPUESTOS = [1_000, 3_000]
TOLERANCIA = 0.5    # puntos de sesgo que se consideran despreciables frente al criterio de 1,2


def medir(cl, hi, lo, con):
    """Sesgo y fraccion sin resolver por bracket y horizonte, pooled sobre los dos lados."""
    out = {}
    for T, S in CELDAS:
        asum = S / (S + T)
        for et, h in HORIZONTES:
            g = res = viv = nn = 0
            for lado in ("largo", "corto"):
                r = replica(cl, hi, lo, con, T, S, lado, h, npaths=NPATHS)
                g += r["gana"]; res += r["gana"] + r["pierde"] + r["amb"]
                viv += r["vivo"]; nn += r["n"]
            out[(T, S, et)] = dict(obs=g / res, sesgo=(g / res - asum) * 100,
                                    sin_res=viv / nn * 100, asum=asum)
    return out


def parte1(m):
    print("=" * 100)
    print("1. EL SESGO DE CENSURA, LOS CINCO BRACKETS Y TRES HORIZONTES")
    print("=" * 100)
    print(f"   {'bracket':>11}{'asim':>8}{'asumido':>10}" +
          "".join(f"{et + ' sesgo':>17}{'sin res':>9}" for et, _ in HORIZONTES))
    filas = []
    for T, S in CELDAS:
        asim = (T - S) / (T + S)
        linea = f"   {f'{T}pt:{S}pt':>11}{asim:>+8.3f}{m[(T,S,HORIZONTES[0][0])]['asum']*100:>9.1f}%"
        for et, _ in HORIZONTES:
            d = m[(T, S, et)]
            linea += f"{d['sesgo']:>+16.2f}{d['sin_res']:>9.1f}%"
            filas.append((T, S, asim, et, d["sesgo"], d["sin_res"]))
        print(linea)

    print("\n" + "=" * 100)
    print("2. LA REGLA: el sesgo NO depende solo de la asimetria")
    print("=" * 100)
    print("   5pt:10pt y 10pt:20pt tienen la MISMA asimetria (-0,333) y sesgos muy distintos.")
    print("   Lo que los separa es cuanto queda sin resolver. La forma que ajusta es:\n")
    print("       sesgo (puntos)  ~  -0,5  x  asimetria  x  % sin resolver\n")
    print(f"   {'bracket':>11}{'horizonte':>12}{'asim':>8}{'sin res':>9}"
          f"{'predicho':>10}{'medido':>9}{'error':>8}")
    err = []
    for T, S, asim, et, sesgo, sin_res in filas:
        pred = -0.5 * asim * sin_res
        err.append(abs(pred - sesgo))
        print(f"   {f'{T}pt:{S}pt':>11}{et:>12}{asim:>+8.3f}{sin_res:>8.1f}%"
              f"{pred:>+10.2f}{sesgo:>+9.2f}{pred-sesgo:>+8.2f}")
    print(f"\n   Error medio de la regla: {np.mean(err):.2f} puntos. Es aproximada y alcanza")
    print("   para decidir, no para corregir un numero publicado.")

    print("\n" + "=" * 100)
    print(f"3. HORIZONTE MINIMO para que el sesgo baje de {TOLERANCIA} puntos - MEDIDO")
    print("=" * 100)
    print("   'usa brackets simetricos' NO es la regla. El sesgo se anula por DOS caminos")
    print("   independientes: asimetria cero, o sin-resolver cero. El segundo se compra con")
    print("   horizonte; el primero limita que brackets se pueden usar.\n")
    print(f"   {'bracket':>11}{'asim':>8}" +
          "".join(f"{et:>14}" for et, _ in HORIZONTES) + f"{'alcanza?':>26}")
    for T, S in CELDAS:
        asim = (T - S) / (T + S)
        linea = f"   {f'{T}pt:{S}pt':>11}{asim:>+8.3f}"
        ok_en = None
        for et, _ in HORIZONTES:
            s = m[(T, S, et)]["sesgo"]
            linea += f"{s:>+13.2f}"
            if ok_en is None and abs(s) <= TOLERANCIA:
                ok_en = et
        linea += f"{(ok_en or 'ni a 5 sesiones'):>26}"
        print(linea)
    print(f"\n   Umbral de asimetria util: para que |sesgo| <= {TOLERANCIA} hace falta")
    print(f"   |asimetria| x (% sin resolver) <= {TOLERANCIA/0.5:.0f}.")
    for sr in (5, 10, 20, 35):
        print(f"     con {sr:>2}% sin resolver -> |asimetria| <= {TOLERANCIA/0.5/sr:.3f}"
              f"  (o sea T/S entre {(1-TOLERANCIA/0.5/sr)/(1+TOLERANCIA/0.5/sr):.2f} y "
              f"{(1+TOLERANCIA/0.5/sr)/(1-TOLERANCIA/0.5/sr):.2f})")


def parte2():
    print("\n" + "=" * 100)
    print("4. CAMINO 3 - que tendria que aparecer en datos de flujo para que valga la pena")
    print("=" * 100)
    print("   Con los pisos ya calculados y los n CORREGIDOS (n_exacto por ultimo cruce).\n")
    print(f"   {'bracket':>11}{'equilibrio $/op':>18}" +
          "".join(f"{f'piso n={n:,}':>16}" for n in PRESUPUESTOS) +
          f"{'op/dia':>9}" + "".join(f"{f'meses n={n:,}':>15}" for n in PRESUPUESTOS) +
          f"{'meses criterio':>16}")
    for T, S in CELDAS:
        p0 = moneda(T, S)
        win, loss = piezas(T, S)
        suma = win + loss
        be = (equilibrio(T, S) - p0) * suma
        rit, _ = ritmo(T, S)
        pisos = [mde_exacto(n, p0) * suma for n in PRESUPUESTOS]
        meses = [n / rit / DIAS_MES for n in PRESUPUESTOS]
        m_cri = n_exacto(p0, equilibrio(T, S)) / rit / DIAS_MES
        print(f"   {f'{T}pt:{S}pt':>11}{be:>18.2f}" +
              "".join(f"{p:>16.2f}" for p in pisos) + f"{rit:>9.1f}" +
              "".join(f"{x:>14.0f}m" for x in meses) + f"{m_cri:>15.0f}m")
    print("\n   'meses criterio' = datos necesarios para demostrar el criterio mismo, no un")
    print("   hallazgo mayor. El backtest no va mas rapido que la estrategia: si toma una")
    print("   posicion por vez, un mes de datos rinde un mes de operaciones. Comprar datos")
    print("   no compra VELOCIDAD, compra el PASADO.")


if __name__ == "__main__":
    cl, hi, lo, con = cargar()
    m = medir(cl, hi, lo, con)
    parte1(m)
    parte2()
