"""
VENTANA G - LOCALIZAR EL SESGO DEL SINTETICO: defecto del codigo o SOBREPASO DE BARRERA?

NO GASTA CARTUCHO. K = 261. Validacion de instrumento contra casos de respuesta conocida.

DE DONDE VIENE ESTO. El test sintetico FALLO contra mi prediccion sellada: sobre un paseo IID
sin drift, con horizonte de 20 sesiones y 0,0% sin resolver, el replicador dio sesgos de hasta
+1,00 y -1,09 puntos contra S/(S+T). Sell que en ese caso no se escribe nada hasta localizar
la causa. Esto es la localizacion.

LA HIPOTESIS. S/(S+T) sale de aplicar el teorema de paro opcional a un martingala CONTINUO,
donde la barrera se toca exactamente. Un paseo con saltos la CRUZA, no la toca: se pasa de
largo una cantidad o. Con eso el paro opcional da

    p(T + o) = (1 - p)(S + o)   ->   p = (S + o) / (S + T + 2o)

y a primer orden el sesgo vale   o x (T - S) / (S + T)^2   en puntos porcentuales.

Si esto es lo que pasa, el replicador NO tiene un defecto: lo que esta mal es la NULA. Y la
formula hace dos predicciones que se pueden falsar por separado.

LAS DOS PREDICCIONES, ESCRITAS ANTES DE CORRER:

  PREDICCION 1 - por TAMAÑO. A razon fija, el sesgo escala como 1/tamaño: al duplicar las dos
  barreras el sesgo se tiene que partir por la mitad. 20:10 -> 40:20 -> 80:40 debe dar una
  progresion cerca de 1 : 1/2 : 1/4, y lo mismo 5:20 -> 10:40 -> 20:80.
  QUE LA FALSA: que el sesgo se quede plano al agrandar el bracket. Eso seria un defecto del
  codigo, porque un error de conteo no sabe de escalas.

  PREDICCION 2 - por GRANULARIDAD. El sobrepaso vale o ~ sigma/raiz(m) con m sub-pasos por
  barra, asi que el sesgo tiene que caer como 1/raiz(m). De m=1 a m=100 debe caer ~10 veces y
  quedar practicamente en cero.
  QUE LA FALSA: que el sesgo sobreviva con m=100, donde el paseo ya es casi continuo y
  S/(S+T) es casi exacto. Ahi el culpable seria el codigo.

  CONTROL CRUZADO. El sobrepaso o despejado de cada celda tiene que dar parecido entre
  brackets de distinto tamaño con el mismo m. Si cada celda pide un o distinto, la formula
  no es la explicacion aunque las tendencias den.

Las tres cosas tienen que dar a la vez. Con dos de tres no alcanza.
"""
import numpy as np

from linea_base import cargar, replica
from sintetico import armar, gauss, tripletes

N = 600_000
NPATHS = 20_000
SEMILLA = 20260904
SESION = 1380
M_BASE = 3
ESCALAS = [[(20, 10), (40, 20), (80, 40)], [(5, 20), (10, 40), (20, 80)]]
MS = [1, 3, 10, 30, 100]
BRACKET_M = (20, 10)


def medir(cl, hi, lo, con, T, S, horizonte, npaths=NPATHS):
    asum = S / (S + T)
    g = res = viv = nn = am = 0
    for lado in ("largo", "corto"):
        r = replica(cl, hi, lo, con, T, S, lado, horizonte, npaths=npaths)
        ri = r["gana"] + r["pierde"] + r["amb"]
        g += r["gana"]; res += ri; viv += r["vivo"]; nn += r["n"]; am += r["amb"]
    p = g / res
    sin_res = viv / nn * 100
    sesgo = (p - asum) * 100
    pred_cens = -0.5 * (T - S) / (T + S) * sin_res
    return dict(sesgo=sesgo, resid=sesgo - pred_cens, sin_res=sin_res,
                amb=am / res * 100, se=np.sqrt(p * (1 - p) / res) * 100)


def o_implicito(sesgo_pt, T, S):
    """Despeja el sobrepaso o de p = (S+o)/(S+T+2o). Exacto, no a primer orden."""
    p = S / (S + T) + sesgo_pt / 100.0
    den = 1.0 - 2.0 * p
    if abs(den) < 1e-12:
        return float("nan")
    return (p * (S + T) - S) / den


def horizonte_para(T, S, sigma, veces=12):
    """El tiempo medio de salida de un intervalo de dos barreras vale S*T/sigma^2 pasos."""
    return int(veces * S * T / sigma ** 2)


def main():
    print("=" * 100)
    print("LOCALIZAR EL SESGO - sobrepaso de barrera, o defecto del replicador?")
    print("NO GASTA CARTUCHO. K = 261. Predicciones escritas antes de correr, ver docstring.")
    print("=" * 100)

    cl, hi, lo, con = cargar()
    d, _, _ = tripletes(cl, hi, lo, con)
    sigma = d.std()
    del cl, hi, lo, con
    print(f"\n   Paseo gaussiano IID, sigma = {sigma:.4f} pt por barra (la medida en ES),")
    print(f"   {N:,} barras, {NPATHS:,} rutas por lado. Sin drift por construccion.")

    con_s = np.zeros(N, dtype=np.int8)
    rng = np.random.default_rng(SEMILLA)
    base = armar(*gauss(N, sigma, M_BASE, rng, chunk=50_000))

    # -------------------------------------------------------------------------------------
    print("\n" + "=" * 100)
    print("PREDICCION 1 - POR TAMAÑO. A razon fija el sesgo debe caer como 1/tamaño.")
    print("   QUE LA FALSA: sesgo plano al agrandar el bracket (un error de conteo no sabe")
    print("   de escalas). Se exige ademas que el sobrepaso despejado sea parecido entre")
    print(f"   filas del mismo grupo, porque m esta fijo en {M_BASE}.")
    print("=" * 100)
    ok1 = True
    for grupo in ESCALAS:
        T0, S0 = grupo[0]
        print(f"\n   Grupo razon {T0}:{S0}   S/(S+T) = {S0/(S0+T0)*100:.1f}%")
        print(f"   {'bracket':>11}{'horizonte':>11}{'sesgo':>9}{'error est':>11}"
              f"{'sin resolv':>12}{'ambiguo':>10}{'resid cens':>12}"
              f"{'vs 1er':>9}{'esperado':>10}{'o desp.':>9}")
        prim = None
        os_ = []
        for T, S in grupo:
            h = min(horizonte_para(T, S, sigma), N // 3)
            r = medir(*base, con_s, T, S, h)
            o = o_implicito(r["resid"], T, S)
            os_.append(o)
            if prim is None:
                prim, esp_ref = r["resid"], (T - S) / (S + T) ** 2
                rel, esp = 1.0, 1.0
            else:
                rel = r["resid"] / prim
                esp = ((T - S) / (S + T) ** 2) / esp_ref
            print(f"   {f'{T}:{S}':>11}{h:>11,}{r['sesgo']:>+9.2f}{r['se']:>11.2f}"
                  f"{r['sin_res']:>11.1f}%{r['amb']:>9.3f}%{r['resid']:>+12.2f}"
                  f"{rel:>9.2f}{esp:>10.2f}{o:>9.3f}")
        disp = np.nanmax(os_) - np.nanmin(os_)
        coherente = disp < 0.5 * np.nanmean(os_)
        ok1 &= coherente
        print(f"      sobrepaso despejado: {', '.join(f'{o:.3f}' for o in os_)} pt   "
              f"dispersion {disp:.3f}   {'COHERENTE' if coherente else 'INCOHERENTE'}")
    print(f"\n   PREDICCION 1 {'SOSTENIDA' if ok1 else 'FALSADA'}")

    # -------------------------------------------------------------------------------------
    T, S = BRACKET_M
    h = min(horizonte_para(T, S, sigma, veces=25), N // 3)
    print("\n" + "=" * 100)
    print(f"PREDICCION 2 - POR GRANULARIDAD. Bracket fijo {T}:{S}, horizonte {h:,} barras.")
    print("   El sobrepaso vale o ~ sigma/raiz(m): el sesgo debe caer como 1/raiz(m) y")
    print("   quedar practicamente en cero con m = 100.")
    print("   QUE LA FALSA: sesgo que sobrevive con m = 100. Ahi el culpable es el codigo.")
    print("=" * 100)
    print(f"\n   {'m':>5}{'rango medio':>13}{'sesgo':>9}{'error est':>11}{'sin resolv':>12}"
          f"{'ambiguo':>10}{'resid cens':>12}{'vs m=1':>9}{'1/raiz(m)':>11}{'o desp.':>9}")
    ref = None
    for m in MS:
        rg = np.random.default_rng(SEMILLA + 1000 + m)
        c2, h2, l2 = armar(*gauss(N, sigma, m, rg, chunk=50_000))
        r = medir(c2, h2, l2, con_s, T, S, h)
        o = o_implicito(r["resid"], T, S)
        if ref is None:
            ref = r["resid"]
        print(f"   {m:>5}{(h2-l2).mean():>13.4f}{r['sesgo']:>+9.2f}{r['se']:>11.2f}"
              f"{r['sin_res']:>11.1f}%{r['amb']:>9.3f}%{r['resid']:>+12.2f}"
              f"{r['resid']/ref:>9.2f}{1/np.sqrt(m):>11.2f}{o:>9.3f}")
        del c2, h2, l2
    print("\n   Si la columna 'vs m=1' sigue a '1/raiz(m)', el sesgo es sobrepaso y nada mas.")
    return ok1


if __name__ == "__main__":
    main()
