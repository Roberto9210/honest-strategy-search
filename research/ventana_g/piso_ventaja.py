"""
VENTANA G - el calculo inverso: dado un presupuesto de operaciones, que ventaja minima se
puede distinguir. Es la especificacion para la busqueda.

NO GASTA CARTUCHO. K = 261.

La pregunta directa era "cuantas operaciones para verificar 81,2% contra 80,0%" y dio 6.988.
La inversa es "dado n, cual es la diferencia minima detectable", y es la que sirve para
descartar una idea ANTES de gastarle tiempo: si promete menos que el piso, no se puede
demostrar en el presupuesto disponible. No es que sea falsa: es que no es medible.

DOS UNIDADES, porque no significan lo mismo:
  - puntos de tasa de acierto: la unidad del test.
  - dolares de esperanza por operacion: la unidad de quien evalua una idea.
La conversion es exacta y no depende de nada mas:
      Delta E = delta * (gana + pierde)
porque E(p) = p*gana - (1-p)*pierde es lineal en p con pendiente (gana+pierde).
"""
import numpy as np
from scipy import stats

from entrada_y_potencia import (CELDAS, MEDIA_EXCESO, VALOR_PT, C1, N, piezas,
                                 equilibrio, moneda, n_exacto)
from factibilidad import filtro_azar

PRESUPUESTOS = [250, 1_000, 3_000]
DIAS_ANIO = 252
VENTANA_MIN = {"RTH": 390, "T23": 1380}
SESION_MIN = 1380.0


def mde_exacto(n, p0, alfa=0.05, potencia=0.80):
    """Inversa exacta de n_exacto: menor delta detectable con n operaciones.
    Mismo test de una cola y misma definicion de potencia que el calculo directo."""
    k = stats.binom.ppf(1 - alfa, n, p0)
    lo, hi = p0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if stats.binom.sf(k, n, mid) < potencia:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2 - p0


def ritmo(T_pt, S_pt):
    """Operaciones por dia segun el terreno, con LAS DOS barreras (correccion ya adoptada):
    la ventana mas chica donde P(resolver) >= 50%. Devuelve (op/dia, ventana)."""
    for nombre in ("RTH", "T23"):
        r = filtro_azar(T_pt, S_pt, nombre)
        if r is not None and r["inf"] >= 50.0:
            return max(1.0, SESION_MIN / VENTANA_MIN[nombre]), nombre
    return 1.0, "no resuelve"


def verificacion():
    print("=" * 104)
    print("VERIFICACION - la inversa tiene que reproducir la directa")
    print("=" * 104)
    n_dir = n_exacto(0.800, 0.812)
    print(f"   directa:  n_exacto(80,0% -> 81,2%) = {n_dir:,}   esperado 6.875   "
          f"{'OK' if n_dir == 6875 else 'FALLADO'}")
    print(f"   (era 6.988 con la version de pasos geometricos; corregida 2026-09-04)")
    d_inv = mde_exacto(n_dir, 0.800)
    print(f"   inversa:  mde_exacto(n={n_dir:,}) = {d_inv*100:.3f} puntos   "
          f"esperado ~1,200")
    # n_exacto avanza en pasos geometricos, asi que devuelve un n >= al minimo real; por eso
    # la inversa da un delta algo MENOR que 1,200. Se exige que cierre dentro de 0,05 puntos.
    ok = (n_dir == 6875) and abs(d_inv * 100 - 1.200) <= 0.05
    print(f"   cierre dentro de 0,05 puntos: {'OK' if ok else 'FALLADO'}")
    print(f"   INVERSION {'VERIFICADA' if ok else 'MAL - no se sigue'}\n")
    return ok


def tabla_mde():
    print("=" * 104)
    print("1. DIFERENCIA MINIMA DETECTABLE POR PRESUPUESTO (alfa 0,05 una cola, potencia 80%)")
    print("=" * 104)
    print("   'puntos' = puntos de tasa de acierto. '$/op' = dolares de esperanza por")
    print("   operacion por encima de la moneda. Delta E = delta * (gana + pierde).\n")
    filas = []
    for T, S in CELDAS:
        p0 = moneda(T, S)
        win, loss = piezas(T, S)
        suma = win + loss
        rit, vent = ritmo(T, S)
        fila = {"T": T, "S": S, "p0": p0, "suma": suma, "ritmo": rit, "ventana": vent}
        for n in PRESUPUESTOS:
            d = mde_exacto(n, p0)
            fila[n] = (d, d * suma, n / rit / DIAS_ANIO)
        filas.append(fila)

    for n in PRESUPUESTOS:
        print(f"   --- presupuesto {n:,} operaciones ---")
        print(f"   {'bracket':>11}{'moneda':>9}{'MDE puntos':>13}{'MDE $/op':>11}"
              f"{'op/dia':>9}{'anios':>8}")
        for f in filas:
            d, de, anios = f[n]
            etiqueta = f"{f['T']}pt:{f['S']}pt"
            print(f"   {etiqueta:>11}{f['p0']*100:>8.1f}%"
                  f"{d*100:>12.2f}{de:>11.2f}{f['ritmo']:>9.1f}{anios:>8.1f}")
        print()
    return filas


def tabla_piso(filas):
    print("=" * 104)
    print("2. EL PISO: que tiene que prometer una idea para que valga la pena MEDIRLA")
    print("=" * 104)
    print("   Hay DOS pisos y manda el mas alto:")
    print("     rentabilidad  = ventaja que hace que operar deje de perder plata (fija por bracket)")
    print("     detectabilidad = ventaja minima que el presupuesto puede distinguir de la moneda")
    print("   Si detectabilidad > rentabilidad, una idea apenas rentable es INDEMOSTRABLE ahi.\n")
    print(f"   {'bracket':>11}{'piso rentab.':>14}{'$/op':>9}" +
          "".join(f"{f'piso n={n:,}':>14}{'$/op':>9}" for n in PRESUPUESTOS))
    for f in filas:
        T, S = f["T"], f["S"]
        d_be = equilibrio(T, S) - f["p0"]
        linea = (f"   {f'{T}pt:{S}pt':>11}{d_be*100:>13.2f}{d_be*f['suma']:>9.2f}")
        for n in PRESUPUESTOS:
            d, de, _ = f[n]
            marca = "" if d <= d_be else "*"
            linea += f"{d*100:>13.2f}{marca}{de:>9.2f}"
        print(linea)
    print("\n   * = el presupuesto NO alcanza para distinguir ni siquiera el punto de")
    print("       equilibrio de ese bracket. Una idea exactamente rentable seria invisible.")

    print("\n   LECTURA POR PRESUPUESTO:")
    for n in PRESUPUESTOS:
        alcanzan = [f for f in filas if f[n][0] <= (equilibrio(f["T"], f["S"]) - f["p0"])]
        peor = max(filas, key=lambda f: f[n][1])
        mejor = min(filas, key=lambda f: f[n][1])
        print(f"     n={n:,}: piso en dolares entre ${mejor[n][1]:.0f}/op "
              f"({mejor['T']}pt:{mejor['S']}pt) y ${peor[n][1]:.0f}/op "
              f"({peor['T']}pt:{peor['S']}pt).")
        if alcanzan:
            nom = ", ".join(f"{f['T']}pt:{f['S']}pt" for f in alcanzan)
            print(f"             alcanza para el equilibrio de: {nom}")
        else:
            print(f"             NO alcanza para el equilibrio de NINGUN bracket.")


def cierre(filas):
    print("\n" + "=" * 104)
    print("3. LA ESPECIFICACION PARA LA BUSQUEDA")
    print("=" * 104)
    ele = [f for f in filas if (f["T"], f["S"]) == (5, 20)][0]
    d1000, e1000, a1000 = ele[1000]
    d_be = equilibrio(5, 20) - ele["p0"]
    print(f"   Celda del criterio (5pt:20pt): equilibrio a +{d_be*100:.2f} puntos = "
          f"${d_be*ele['suma']:.2f}/op.")
    print(f"   Con 1.000 operaciones solo se distingue +{d1000*100:.2f} puntos = "
          f"${e1000:.2f}/op,")
    print(f"   que es {e1000/(d_be*ele['suma']):.1f} veces el equilibrio. Una idea que prometa")
    print(f"   apenas rentabilidad en esta celda NO es demostrable con 1.000 operaciones.")
    print(f"\n   El piso no es un numero: depende del bracket, y va de "
          f"${min(f[1000][1] for f in filas):.0f} a ${max(f[1000][1] for f in filas):.0f}")
    print("   por operacion con el mismo presupuesto de 1.000. Por eso la tabla, y no una cifra.")


if __name__ == "__main__":
    if not verificacion():
        raise SystemExit("La inversion no reproduce la directa. No se publica nada.")
    filas = tabla_mde()
    tabla_piso(filas)
    cierre(filas)
