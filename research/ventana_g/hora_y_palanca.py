"""
VENTANA G - contaminacion horaria de la constante de costo, y la ultima palanca de parametros.

NO GASTA CARTUCHO. K = 261.

PRECISION QUE NO SE PASA POR ALTO: medir cuanto contamina una hora atipica a una constante
NO gasta cartucho. "Operar fuera de las 17:00 CT" seria una REGLA DE ESTRATEGIA y SI
gastaria cartucho. Aca no se declara ninguna regla de operacion: se reportan dos constantes
y nada mas. La decision de si eso se convierte en hipotesis se toma con presupuesto aparte.
"""
import os
import re

import numpy as np

from aritmetica import FIRMAS, C1_POR_MICRO_VIA_MINI
from vara_criterio import acierto_requerido, acierto_sin_ventaja

AQUI = os.path.dirname(os.path.abspath(__file__))
FIRMA = "Tradeify Growth (50K)"
N = 10
CELDAS = [(5, 10), (10, 10), (20, 10), (5, 20), (10, 20)]
D_COL = [4, 10, 20]


def tabla_horas():
    """Lee la tabla por hora ya medida y publicada en salida_media_exceso.txt."""
    txt = open(os.path.join(AQUI, "salida_media_exceso.txt"), encoding="utf-8").read()
    bloque = txt.split("2. MEDIA DEL EXCESO POR HORA")[1]
    filas = {}
    for m in re.finditer(r"^\s*(\d{1,2}):00((?:\s+(?:\d+ / [\d.]+|---)){3})\s*$",
                          bloque, re.M):
        hora = int(m.group(1))
        celdas = re.findall(r"(\d+) / ([\d.]+)|---", m.group(2))
        vals = []
        for a, b in celdas:
            vals.append((int(a), float(b)) if a else None)
        filas[hora] = vals
    return filas


def pooled(filas, col, excluir=()):
    """Media ponderada por n sobre las horas, con y sin las horas excluidas."""
    num = den = 0
    for h, vals in filas.items():
        if h in excluir or vals[col] is None:
            continue
        n, m = vals[col]
        num += n * m
        den += n
    return num / den, den


def seccion_hora():
    print("=" * 100)
    print("1. CONTAMINACION HORARIA DE LA CONSTANTE DE COSTO")
    print("=" * 100)
    print("   NO es una regla de operacion. Son dos constantes, medidas, presentadas al lado.")
    filas = tabla_horas()
    print(f"\n   {'D':>4}{'horas':>8}{'TODAS: media':>15}{'SIN 17:00: media':>19}"
          f"{'cambio':>10}{'peso de 17:00':>16}")
    consts = {}
    for i, D in enumerate(D_COL):
        todas, n_t = pooled(filas, i)
        sin17, n_s = pooled(filas, i, excluir=(17,))
        peso = (n_t - n_s) / n_t
        consts[D] = (todas, sin17)
        print(f"   {D:>3}pt{len(filas):>8}{todas:>14.4f}{sin17:>18.4f}"
              f"{(sin17/todas-1)*100:>9.1f}%{peso*100:>15.1f}%")
    print("\n   La reapertura pesa poco en n pero mueve la media: es un outlier, no un sesgo")
    print("   general. (Poblacion: ventanas de 1 hora, que es donde existe el desglose.)")

    print("\n" + "=" * 100)
    print("2. CUANTO MUEVE EL REQUERIDO - sensibilidad, sustituyendo una constante por la otra")
    print("=" * 100)
    print("   Aviso: la constante que usa el modelo sale de la ventana T23, no de ventanas de")
    print("   1 hora. En T23 el stop se puede tocar a cualquier hora y NO se registro la hora")
    print("   del toque, asi que la constante T23 no se puede desglosar con lo medido. Esto")
    print("   es una SENSIBILIDAD del mismo tamano que la contaminacion, no una remedicion.\n")
    print(f"   {'bracket':>11}{'moneda':>9}{'req TODAS':>12}{'req SIN 17:00':>16}{'cambio':>10}")
    for T, S in CELDAS:
        todas, sin17 = consts[S if S in consts else 10]
        mon = 100 * acierto_sin_ventaja(T, S)
        a = 100 * acierto_requerido(FIRMA, N, T, S, C1_POR_MICRO_VIA_MINI, extra_pt=todas)
        b = 100 * acierto_requerido(FIRMA, N, T, S, C1_POR_MICRO_VIA_MINI, extra_pt=sin17)
        print(f"   {f'{T}pt:{S}pt':>11}{mon:>8.1f}%{a:>11.1f}%{b:>15.1f}%{b-a:>+9.1f}")


def seccion_palanca():
    print("\n" + "=" * 100)
    print("3. LA ULTIMA PALANCA DE PARAMETROS: objetivo / drawdown, que la fija la firma")
    print("=" * 100)
    print("   Cuentas de 50K, etapa de evaluacion, de datos_crudos.md. Menor = mejor forma.\n")
    print(f"   {'firma':<30}{'objetivo':>10}{'drawdown':>10}{'obj/dd':>9}{'vs Tradeify':>13}")
    filas = [(k, v["eval"]["target"], v["eval"]["dd"],
              v["eval"]["target"] / v["eval"]["dd"]) for k, v in FIRMAS.items()]
    tra = [x for x in filas if x[0].startswith("Tradeify")][0][3]
    for nombre, o, d, r in sorted(filas, key=lambda x: x[3]):
        print(f"   {nombre:<30}{o:>10,}{d:>10,}{r:>9.3f}{r/tra:>12.2f}x")
    rs = [x[3] for x in filas]
    dds = sorted({x[2] for x in filas})
    print(f"\n   Rango de forma: {min(rs):.3f} a {max(rs):.3f}. El mejor es "
          f"{max(rs)/min(rs):.2f}x el peor y {min(rs)/tra:.2f}x el de Tradeify.")
    print(f"   Rango de ESCALA (drawdown absoluto, que es lo que manda la holgura): "
          f"${min(dds):,} a ${max(dds):,}.")
    print(f"   La compuerta 1 midio que harian falta $9.000 para bajar la ruina nocturna al")
    print(f"   3,7%. Falta un factor de {9000/max(dds):.1f} contra el mayor drawdown de 50K.")


if __name__ == "__main__":
    seccion_hora()
    seccion_palanca()
