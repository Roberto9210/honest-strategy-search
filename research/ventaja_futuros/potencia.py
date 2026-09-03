"""Potencia por RESOLUCION -- Tarea 2 de Ventana D.

No lee ningun dato de precios. Es aritmetica sobre los N del inventario
(hipotesis_congeladas.md, seccion 0), y se corre DESPUES de que ese archivo
quedo commiteado solo.

Pregunta: con N sesiones y una hipotesis cuyo acierto real es p1, y una
prueba binomial contra H0 p0 = 0.5, hay 80 % de potencia?

Cuenta a la vista (aproximacion normal, la misma que usa cualquier tabla):

    n_req = ( (z_alpha * sqrt(p0 q0) + z_beta * sqrt(p1 q1)) / (p1 - p0) )^2

y al lado la potencia EXACTA binomial para el N disponible, que es la que
manda si las dos difieren.

Tres operaciones por sesion: se muestran las dos cotas. Si las tres son
independientes, n = 3N. Si estan totalmente correlacionadas dentro de la
sesion, n = N y las tres no agregan nada. La verdad esta entre las dos y
NO se sabe hasta medir la correlacion intra-sesion; por eso se imprimen
ambas y ninguna se elige.

    python research/ventaja_futuros/potencia.py > research/ventaja_futuros/potencia.txt
"""

from math import sqrt
from statistics import NormalDist

P0 = 0.5
EFFECTS = [0.52, 0.55, 0.58, 0.60, 0.65]
POWER = 0.80
ALPHAS = [("alpha 0.05 unilateral", 0.05), ("alpha 0.0125 (4 hipotesis)", 0.0125)]

# --- Poblaciones, POR RESOLUCION. Procedencia en hipotesis_congeladas.md seccion 0.
POBLACIONES = [
    ("DIARIO  MES NT8   (pares mismo contrato)         ", 1821, "guardian f75d126, resultado-pregunta1 M3"),
    ("MINUTOS MES NT8   (archivos en dia habil)        ", 12,   "guardian f75d126, datos-futuros seccion 2"),
    ("MINUTOS MES NT8   (LEGIBLES hoy)                 ", 0,    "guardian f75d126, datos-futuros seccion 3"),
    ("MINUTOS ES  Databento 2016-2026 (todo)           ", 2747, "data_quality_es_1min_databento.md, tabla por anio"),
    ("MINUTOS ES  Databento 2020-2026 (SELLADO busq. 1)", 1715, "ARTICLE.md hold-out; QC tabla por anio"),
    ("MINUTOS ES  Databento 2016-2019 (ya mirado)      ", 1032, "spec v1 seccion 4 parte A; QC tabla por anio"),
]

# Particion candidata para el diario: fraccion intocada. Se imprimen dos, la
# convencional 30 % y la 50 % que se propone en diseno.md para reglas SIN
# parametros libres.
FRACCIONES_INTOCADO = [0.30, 0.50]

N = NormalDist()


def n_requerido(p1, alpha, power=POWER, p0=P0):
    za = N.inv_cdf(1 - alpha)
    zb = N.inv_cdf(power)
    num = za * sqrt(p0 * (1 - p0)) + zb * sqrt(p1 * (1 - p1))
    return (num / (p1 - p0)) ** 2


def _binom_pmf_table(n, p):
    # pmf por recurrencia, estable para n hasta unos miles
    from math import lgamma, log, exp
    logp, logq = log(p), log(1 - p)
    out = []
    for k in range(n + 1):
        lc = lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1)
        out.append(exp(lc + k * logp + (n - k) * logq))
    return out


def potencia_exacta(n, p1, alpha, p0=P0):
    """Prueba binomial unilateral exacta: umbral k* = menor k con P(K>=k | p0) <= alpha."""
    if n <= 0:
        return 0.0, None
    pmf0 = _binom_pmf_table(n, p0)
    tail = 0.0
    kstar = n + 1
    for k in range(n, -1, -1):
        tail += pmf0[k]
        if tail > alpha:
            kstar = k + 1
            break
    if kstar > n:
        return 0.0, kstar
    pmf1 = _binom_pmf_table(n, p1)
    return sum(pmf1[kstar:]), kstar


def fila_requeridos():
    print("=" * 110)
    print("A. N REQUERIDO (una decision independiente por fila), potencia 80 %, H0 acierto = 0.50")
    print("   n_req = ((z_a*sqrt(.25) + z_b*sqrt(p1(1-p1))) / (p1-.5))^2 ; z_b(0.80) = %.4f" % N.inv_cdf(POWER))
    print("=" * 110)
    print(f"  {'acierto real':<14}" + "".join(f"{lab:>32}" for lab, _ in ALPHAS))
    for p1 in EFFECTS:
        cells = []
        for lab, a in ALPHAS:
            za = N.inv_cdf(1 - a)
            cells.append(f"{n_requerido(p1, a):>22.0f}  (z_a={za:.3f})")
        print(f"  {p1:<14.2f}" + "".join(f"{c:>32}" for c in cells))
    print()


def tabla_poblacion(nombre, n_ses, fuente):
    print("=" * 110)
    print(f"B. {nombre.strip()}   N sesiones = {n_ses}   [{fuente}]")
    print("=" * 110)
    for lab, a in ALPHAS:
        print(f"  --- {lab} ---")
        print(f"  {'acierto':>8} | {'1 op/sesion':^30} | {'3 ops/sesion, cota INDEPENDIENTE (n=3N)':^42} | {'3 ops, cota CORRELACIONADA (n=N)':^32}")
        print(f"  {'':>8} | {'n=%d   potencia   alcanza?' % n_ses:^30} | {'n=%d   potencia   alcanza?' % (3 * n_ses):^42} | {'igual que 1 op/sesion':^32}")
        for p1 in EFFECTS:
            pw1, _ = potencia_exacta(n_ses, p1, a)
            pw3, _ = potencia_exacta(3 * n_ses, p1, a)
            ok1 = "SI" if pw1 >= POWER else "NO"
            ok3 = "SI" if pw3 >= POWER else "NO"
            print(f"  {p1:>8.2f} | {'%6.3f      %s' % (pw1, ok1):^30} | {'%6.3f      %s' % (pw3, ok3):^42} | {'%6.3f      %s' % (pw1, ok1):^32}")
        print()


def tabla_particion(nombre, n_ses):
    print("=" * 110)
    print(f"C. {nombre.strip()}: potencia del PERIODO INTOCADO solo (1 op/sesion), que es donde se hace la unica corrida")
    print("=" * 110)
    for frac in FRACCIONES_INTOCADO:
        n_int = int(round(n_ses * frac))
        print(f"  intocado = {frac:.0%} de N -> n = {n_int}")
        for lab, a in ALPHAS:
            cells = []
            for p1 in EFFECTS:
                pw, _ = potencia_exacta(n_int, p1, a)
                cells.append(f"{p1:.2f}:{pw:.3f}{'*' if pw >= POWER else ' '}")
            print(f"     {lab:<28} " + "  ".join(cells))
    print("  (* = alcanza 80 %)")
    print()


if __name__ == "__main__":
    print("POTENCIA POR RESOLUCION -- Ventana D, 2026-09-03. Sin datos de precios; solo los N del inventario.")
    print()
    fila_requeridos()
    for nombre, n_ses, fuente in POBLACIONES:
        tabla_poblacion(nombre, n_ses, fuente)
    tabla_particion("DIARIO MES NT8 (1.821)", 1821)
    tabla_particion("MINUTOS ES Databento, intocado = lo sellado 2020-2026", 1715)
    print("Cota de sensibilidad, para leer la tabla: con N sesiones, el acierto minimo detectable al 80 % es")
    print("aprox. 0.5 + 2.4864/(2*sqrt(N)) con alpha 0.05, y 0.5 + 3.0824/(2*sqrt(N)) con alpha 0.0125:")
    for nombre, n_ses, _ in POBLACIONES:
        if n_ses > 0:
            d05 = (N.inv_cdf(0.95) + N.inv_cdf(POWER)) * 0.5 / sqrt(n_ses)
            d0125 = (N.inv_cdf(1 - 0.0125) + N.inv_cdf(POWER)) * 0.5 / sqrt(n_ses)
            print(f"  {nombre.strip():<52} N={n_ses:>5}  p_min(0.05)={0.5 + d05:.4f}  p_min(0.0125)={0.5 + d0125:.4f}")
        else:
            print(f"  {nombre.strip():<52} N={n_ses:>5}  no hay nada que detectar")
