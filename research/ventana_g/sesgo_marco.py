"""
VENTANA G - DE DONDE SALE EL SESGO DEL MARCO NUEVO. El control A fallo y hay que localizarlo.

NO GASTA CARTUCHO. K = 261. Validacion de instrumento contra un caso de respuesta conocida.

EL PROBLEMA. Sobre bootstrap IID sin drift y con costo CERO, el marco de dolares por sesion
dio -$10,77 (5pt:20pt) y +$5,75 (20pt:10pt) en vez de cero. La condicion de falla estaba
declarada y se cumplio: el marco nuevo tiene sesgo propio.

LA HIPOTESIS. Es SOBREPASO DE BARRERA de contabilidad. Cuando el precio cruza una barrera la
CRUZA, no la toca: se pasa una cantidad o. Yo anoto exactamente +T o -S. Por paro opcional el
valor verdadero al cierre es p(T+a) - (1-p)(S+b) = 0, asi que lo que ANOTO vale

    anotado = p*T - (1-p)*S = -p*a + (1-p)*b  ~  o * (1 - 2p)   con a ~ b ~ o

Con p = S/(S+T): en 20pt:10pt p = 1/3 y el sesgo sale POSITIVO; en 5pt:20pt p = 0,8 y sale
NEGATIVO. Los dos signos observados coinciden. Y despejando o de cada uno:
   20pt:10pt  +0,665 $/op = +0,0133 pt  ->  o = 0,040 pt
    5pt:20pt  -1,029 $/op = -0,0206 pt  ->  o = 0,034 pt
Dos brackets independientes piden el MISMO sobrepaso. Eso ya es mas de lo que consiguio la
hipotesis de sobrepaso la vez pasada, donde los o despejados daban 1,3 / 2,2 / 9,2.

LA PREDICCION QUE LA PUEDE MATAR, escrita antes de correr. A ESPAN FIJO (las dos barreras
suman 25 puntos siempre, asi que el ritmo de operaciones y el ruido son comparables), el
sesgo por operacion tiene que ser LINEAL en (1 - 2p) y pasar por cero en el simetrico:

    bracket      p      1-2p    sesgo esperado
     5pt:20pt   0,80    -0,60   -0,60 o
    10pt:15pt   0,60    -0,20   -0,20 o
  12,5:12,5pt   0,50     0,00        0
    15pt:10pt   0,40    +0,20   +0,20 o
     20pt:5pt   0,20    +0,60   +0,60 o

   QUE LA FALSA: que el sesgo no siga esa recta, o que el o despejado de cada fila sea
   distinto. Ahi el culpable es otro y hay que seguir buscando.

   AVISO SOBRE EL PUNTO DEL MEDIO: en el bracket simetrico el sesgo es CERO FORZADO por
   simetria (p = 1/2 hace p*T - (1-p)*S = 0 sea cual sea el sobrepaso). Ese punto NO informa
   nada; lo que informa es la PENDIENTE y que las filas de los costados sean antisimetricas.

CONTROL SECUNDARIO: se mide la fraccion de barras AMBIGUAS, que se cuentan como perdida y
serian un sesgo negativo en todas las filas por igual.
   QUE LO HARIA FALLAR: ambiguedad apreciable. Explicaria un corrimiento parejo hacia abajo
   y no la antisimetria.
"""
import numpy as np

from dolares_por_tiempo import PUNTO_ES, SESION, cortes
from linea_base import cargar
from sintetico import armar, bootstrap, tripletes

K = 8
SEMILLA = 20260904
SPAN = 25.0
CELDAS = [(5.0, 20.0), (10.0, 15.0), (12.5, 12.5), (15.0, 10.0), (20.0, 5.0)]


def replay(cl, hi, lo, ini, fin, T, S, lado):
    """Igual que dolares_por_tiempo.secuencial pero devolviendo el detalle por operacion,
    que es lo que hace falta para localizar el sesgo. Costo cero, con marca a mercado."""
    sgn = 1.0 if lado == "largo" else -1.0
    tot = 0.0
    n_op = n_amb = 0
    for a, b in zip(ini, fin):
        pos = a
        while pos < b - 1:
            e = cl[pos]
            obj, stp = e + sgn * T, e - sgn * S
            h, l = hi[pos + 1:b], lo[pos + 1:b]
            if lado == "largo":
                to, ts = h >= obj, l <= stp
            else:
                to, ts = l <= obj, h >= stp
            algo = to | ts
            if not algo.any():
                n_op += 1
                tot += sgn * (cl[b - 1] - e)
                break
            j = int(np.argmax(algo))
            n_op += 1
            if to[j] and ts[j]:
                n_amb += 1
            tot += T if (to[j] and not ts[j]) else -S
            pos = pos + 1 + j + 1
    return tot, n_op, n_amb


def main():
    print("=" * 100)
    print("DE DONDE SALE EL SESGO DEL MARCO NUEVO - sobrepaso de barrera?")
    print("NO GASTA CARTUCHO. K = 261. Prediccion escrita antes de correr, ver docstring.")
    print("=" * 100)

    cl, hi, lo, con = cargar()
    n = len(cl)
    d, up, dn = tripletes(cl, hi, lo, con)
    mu = d.mean()
    dc, upc, dnc = d - mu, up - mu, dn - mu
    del cl, hi, lo, con
    ini, fin = cortes(n, SESION)
    print(f"\n   Bootstrap IID sin drift, {K} series de {n:,} barras, costo CERO,")
    print(f"   con marca a mercado. Espan fijo de {SPAN:.0f} puntos en las cinco celdas.\n")

    print(f"   {'bracket':>13}{'p':>7}{'1-2p':>8}{'sesgo pt/op':>14}{'error':>9}"
          f"{'en errores':>12}{'o despejado':>13}{'ambiguo':>10}{'op/serie':>10}")
    filas = []
    for T, S in CELDAS:
        p = S / (S + T)
        f = 1.0 - 2.0 * p
        por_serie, ambs, ops = [], 0, 0
        for k in range(K):
            rg = np.random.default_rng(SEMILLA + 7919 * k)
            c2, h2, l2 = armar(*bootstrap(dc, upc, dnc, n, rg))
            t2 = o2 = a2 = 0.0
            for lado in ("largo", "corto"):
                t, o, am = replay(c2, h2, l2, ini, fin, T, S, lado)
                t2 += t; o2 += o; a2 += am
            por_serie.append(t2 / o2)
            ambs += a2; ops += o2
            del c2, h2, l2
        v = np.array(por_serie)
        m, se = v.mean(), v.std(ddof=1) / np.sqrt(K)
        o_desp = m / f if abs(f) > 1e-9 else float("nan")
        filas.append((T, S, f, m, se, o_desp))
        print(f"   {f'{T:g}pt:{S:g}pt':>13}{p:>7.2f}{f:>8.2f}{m:>+14.4f}{se:>9.4f}"
              f"{m/se:>+12.1f}{o_desp:>13.4f}{ambs/ops*100:>9.3f}%{ops//(2*K):>10,}")

    print("\n" + "=" * 100)
    print("LA PRUEBA - el sesgo es lineal en (1-2p) y pasa por cero en el simetrico?")
    print("=" * 100)
    x = np.array([f[2] for f in filas])
    y = np.array([f[3] for f in filas])
    a, b = np.polyfit(x, y, 1)
    pred = a * x + b
    ss_res = ((y - pred) ** 2).sum()
    ss_tot = ((y - y.mean()) ** 2).sum()
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    os_ = np.array([f[5] for f in filas[:2] + filas[3:]])
    disp = np.nanmax(os_) - np.nanmin(os_)
    print(f"\n   recta ajustada:  sesgo = {a:+.4f} * (1-2p) {b:+.4f}")
    print(f"   pendiente = el sobrepaso o = {a:.4f} pt = {a/0.25:.2f} ticks = ${a*PUNTO_ES:.2f}")
    print(f"   ordenada al origen {b:+.4f} pt   (tiene que ser ~0: es el simetrico)")
    print(f"   R2 = {r2:.4f}")
    print(f"   o despejado por fila (sin el simetrico, que esta forzado a cero): "
          f"{', '.join(f'{o:.4f}' for o in os_)}")
    print(f"   dispersion de o: {disp:.4f} pt")
    ok = r2 >= 0.95 and abs(b) < 0.01 and disp < 0.5 * abs(a)
    print(f"\n   PREDICCION {'SOSTENIDA' if ok else 'FALSADA'}")
    if ok:
        print(f"\n   -> el sesgo del marco nuevo es sobrepaso de barrera de contabilidad,")
        print(f"      vale {a*PUNTO_ES:.2f} dolares por operacion por mini, tiene signo")
        print(f"      predecible por el bracket y SE PUEDE RESTAR porque su nula se calcula.")
    return filas


if __name__ == "__main__":
    main()
