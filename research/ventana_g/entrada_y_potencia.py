"""
VENTANA G - deslizamiento de ENTRADA (acotado, no medido) y cuantas operaciones hacen
falta para verificar a un candidato.

NO GASTA CARTUCHO. K = 261. Aritmetica y calculo de potencia sobre parametros ya fijados.

1. ENTRADA. Todo lo medido es la SALIDA: terreno_stop midio el exceso por encima del stop,
   dentro de la barra que lo toca. La entrada no esta medida y NO SE PUEDE medir con los
   datos del proyecto: es_1min_databento.csv es schema ohlcv-1m (asi lo declara
   data/data_quality_es_1min_databento.md), o sea barras OHLCV sin bid/ask ni libro.
   Lo que haria falta: Databento GLBX.MDP3 schema mbp-1 (tope de libro) o mbo, mismo
   simbolo y periodo. Con eso se mide el spread y el llenado contra el medio en la entrada.
   Mientras tanto se acota: cuanto deslizamiento de entrada anula la ventaja.

2. POTENCIA. Distinguir 81,2% de 80,0% es una prueba de UNA muestra contra un valor
   CONOCIDO -la moneda no se estima, sale de S/(S+T)=20/25 exacto-, no de dos muestras.
   Eso cambia el n por un factor de ~2,5.
"""
import numpy as np
from scipy import stats

from aritmetica import C1_POR_MICRO_VIA_MINI
from bracket import trades_por_dia

N = 10           # micro-equivalentes = 1 mini
PUNTO = 5.0      # USD por punto por micro
VALOR_PT = PUNTO * N          # USD por punto de la posicion entera = $50 (1 ES)
TICK_PT = 0.25
MEDIA_EXCESO = {10: 0.722, 20: 0.982}
C1 = C1_POR_MICRO_VIA_MINI

# (objetivo, stop) y el equilibrio por operacion ya calculado en criterio_final.py
CELDAS = [(5, 10), (10, 10), (20, 10), (5, 20), (10, 20)]


def piezas(T_pt, S_pt, e_entrada=0.0):
    """Ganancia y perdida en dolares. El deslizamiento de ENTRADA pega en las DOS ramas
    (se paga al entrar, se gane o se pierda); el de SALIDA solo en la perdedora."""
    win = T_pt * VALOR_PT - C1 * N - e_entrada * VALOR_PT
    loss = S_pt * VALOR_PT + C1 * N + MEDIA_EXCESO[S_pt] * VALOR_PT + e_entrada * VALOR_PT
    return win, loss


def equilibrio(T_pt, S_pt, e_entrada=0.0):
    win, loss = piezas(T_pt, S_pt, e_entrada)
    return loss / (win + loss)


def moneda(T_pt, S_pt):
    return S_pt / (S_pt + T_pt)


def seccion1():
    print("=" * 100)
    print("1. DESLIZAMIENTO DE ENTRADA - no medible con estos datos, pero acotable")
    print("=" * 100)
    print("   Se puede medir? NO. es_1min_databento.csv es ohlcv-1m: barras sin bid/ask ni")
    print("   libro. Haria falta Databento GLBX.MDP3 schema mbp-1 o mbo, mismo periodo.\n")
    T, S = 5, 20
    base = 100 * equilibrio(T, S)
    mon = 100 * moneda(T, S)
    win, loss = piezas(T, S)
    print(f"   celda {T}pt:{S}pt via 1 mini. gana ${win:.2f} / pierde ${loss:.2f}")
    print(f"   equilibrio hoy {base:.2f}%, moneda {mon:.1f}%, ventaja pedida "
          f"{base - mon:+.2f} puntos\n")
    # La suma gana+pierde no depende del deslizamiento de entrada: sale de una rama y entra
    # en la otra. Por eso el equilibrio se mueve lineal y el coeficiente es exacto.
    por_punto = 100 * VALOR_PT / (win + loss)
    print(f"   Cada punto de deslizamiento de entrada sube el equilibrio "
          f"{por_punto:.3f} puntos de acierto.")
    print(f"   Un TICK ({TICK_PT}pt) lo sube {por_punto * TICK_PT:.2f} puntos, que es el "
          f"{100 * por_punto * TICK_PT / (base - mon):.0f}% de la ventaja entera.\n")
    print(f"   {'entrada':>12}{'equilibrio':>13}{'ventaja pedida':>17}")
    for ticks in (0, 0.5, 1, 1.25, 2):
        e = ticks * TICK_PT
        q = 100 * equilibrio(T, S, e)
        print(f"   {ticks:>8.2f} tk{q:>12.2f}%{q - mon:>+16.2f}")
    anula = (base - mon) / 100 * (win + loss) / VALOR_PT
    print(f"\n   ANULACION: {anula:.3f} puntos = {anula / TICK_PT:.2f} ticks de entrada")
    print(f"   agregan otros {base - mon:.1f} puntos al requerido, o sea DUPLICAN la ventaja")
    print("   que el candidato tiene que aportar. Un solo tick ya se lleva el 80%.")
    return anula


def n_necesario(p0, p1, alfa=0.05, potencia=0.80):
    """Una muestra, una cola. p0 es CONOCIDO (la moneda es S/(S+T) exacto), no estimado."""
    za, zb = stats.norm.ppf(1 - alfa), stats.norm.ppf(potencia)
    num = za * np.sqrt(p0 * (1 - p0)) + zb * np.sqrt(p1 * (1 - p1))
    return (num / (p1 - p0)) ** 2


def n_exacto(p0, p1, alfa=0.05, potencia=0.80, tope=200_000):
    """Binomial exacta: menor n cuyo test de una cola alcanza la potencia pedida."""
    n = 100
    while n < tope:
        k = stats.binom.ppf(1 - alfa, n, p0)          # valor critico
        if stats.binom.sf(k, n, p1) >= potencia:      # P(rechazar | p1)
            return int(n)
        n = int(n * 1.05) + 1
    return None


def seccion2():
    print("\n" + "=" * 100)
    print("2. CUANTAS OPERACIONES PARA VERIFICAR A UN CANDIDATO")
    print("=" * 100)
    print("   alfa 0,05 una cola, potencia 80%. UNA muestra contra un valor conocido:")
    print("   la moneda no se estima, es S/(S+T) exacto. Por eso NO es el n de dos muestras.\n")
    print(f"   {'bracket':>11}{'moneda':>9}{'equilibrio':>12}{'delta':>8}"
          f"{'n normal':>11}{'n exacto':>11}{'op/dia':>8}{'anios':>9}")
    filas = []
    for T, S in CELDAS:
        p0, p1 = moneda(T, S), equilibrio(T, S)
        nn, ne = n_necesario(p0, p1), n_exacto(p0, p1)
        tpd = trades_por_dia(S)
        anios = ne / tpd / 252
        filas.append((T, S, p0, p1, nn, ne, tpd, anios))
        print(f"   {f'{T}pt:{S}pt':>11}{p0*100:>8.1f}%{p1*100:>11.1f}%"
              f"{(p1-p0)*100:>7.1f}{nn:>11,.0f}{ne:>11,}{tpd:>8}{anios:>9.1f}")

    ele = [f for f in filas if (f[0], f[1]) == (5, 20)][0]
    print(f"\n   La celda elegida (5pt:20pt) necesita {ele[5]:,} operaciones: es la PEOR de")
    print(f"   la tabla para verificar. La mejor es 5pt:10pt con "
          f"{[f for f in filas if (f[0],f[1])==(5,10)][0][5]:,}.")
    print(f"   A {ele[6]} operacion por dia -el ritmo que el terreno da para un stop de "
          f"{ele[1]}pt- son {ele[7]:.0f} anios.")
    print("\n   HIPOTESIS DEL PEDIDO: '~17.000 operaciones'. REFUTADA EN MAGNITUD, CONFIRMADA")
    print("   EN SUSTANCIA. 17.000 es el n de DOS muestras (2 x (za+zb)^2 p(1-p)/delta^2 =")
    print(f"   {2*(stats.norm.ppf(0.975)+stats.norm.ppf(0.8))**2*0.16/0.012**2:,.0f}). Como la moneda es conocida y no")
    print(f"   estimada, el test es de una muestra y el n es {ele[5]:,}. Sigue siendo")
    print("   inverificable en plazo humano: el orden de magnitud del problema no cambia.")
    return filas


def seccion3(filas):
    print("\n" + "=" * 100)
    print("3. SE PUEDE DECIDIR SIN ESAS OPERACIONES?")
    print("=" * 100)
    T, S = 5, 20
    p0, p1 = moneda(T, S), equilibrio(T, S)
    win, loss = piezas(T, S)
    mu0 = p0 * win - (1 - p0) * loss
    mu1 = p1 * win - (1 - p1) * loss
    sd = np.sqrt(p0 * (1 - p0)) * (win + loss)
    za, zb = stats.norm.ppf(0.95), stats.norm.ppf(0.80)
    n_pnl = ((za + zb) * sd / (mu1 - mu0)) ** 2
    print("   (a) Medir el P&L en vez de la tasa de acierto: NO ayuda.")
    print(f"       El P&L es funcion deterministica del resultado binario, asi que lleva la")
    print(f"       misma informacion. n por P&L = {n_pnl:,.0f} contra "
          f"{[f for f in filas if (f[0],f[1])==(5,20)][0][5]:,} por tasa: el mismo numero.")
    print("\n   (b) Cambiar de bracket: SI ayuda, y mucho.")
    for T2, S2 in ((5, 10), (10, 10)):
        f = [x for x in filas if (x[0], x[1]) == (T2, S2)][0]
        print(f"       {T2}pt:{S2}pt necesita {f[5]:,} operaciones a {f[6]} op/dia = "
              f"{f[7]:.1f} anios.")
    print("       Pero esas celdas no sobreviven el terreno con margen. El costo de la")
    print("       factibilidad es la verificabilidad, y hay que elegir.")
    print("\n   (c) Medir el estadistico intermedio en vez del final: EN PRINCIPIO SI, con")
    print("       una advertencia. Si el candidato expone una senal CONTINUA, contrastar la")
    print("       correlacion de esa senal con el retorno futuro usa mucha mas informacion")
    print("       por observacion que un resultado binario 80/20. Pero prueba OTRA hipotesis")
    print("       -que la senal predice- y no esta: para pasar de habilidad de senal a")
    print("       esperanza del bracket hay que volver a la misma aritmetica de barreras.")
    print("       No es gratis, y exige que el candidato exponga la senal, no solo los trades.")
    print("\n   CONCLUSION: con la tasa de acierto final del bracket elegido, no hay atajo.")


if __name__ == "__main__":
    anula = seccion1()
    filas = seccion2()
    seccion3(filas)
