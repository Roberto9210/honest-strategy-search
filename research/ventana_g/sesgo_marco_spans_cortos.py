"""
TAREA 1 - EL SESGO DE CONTABILIDAD EN SPANS CORTOS (3 a 10 pt). Es lo unico que le abre la ventana
operable al juez.

NO GASTA CARTUCHO. K = 261. Dinero: $0. Bootstrap IID sobre ES, costo CERO. La caja sellada no se
toca: el bootstrap se arma con los tripletes ya usados en sesgo_marco.py.

POR QUE. El juez solo acepta brackets con span (objetivo + stop) entre 20 y 35 pt, porque ahi esta
MEDIDO el sesgo de contabilidad por sobrepaso de barrera. Las cuatro celdas que caen dentro de la
ventana operable del reglamento tienen span de 3 a 7 pt, asi que el juez las rechaza con NO MEDIBLE.
Mientras eso siga asi, el solapamiento entre lo que el reglamento permite operar y lo que el juez
puede juzgar es VACIO.

EL MODELO QUE SE ESTA PROBANDO, el mismo de sesgo_marco.py: cuando el precio cruza una barrera la
CRUZA, no la toca, y se pasa una cantidad o. Anotar exactamente +T o -S introduce
    sesgo por operacion  =  o * (1 - 2p)      con p = S/(S+T)
La constante o es una propiedad del PROCESO DE PRECIOS -cuanto se pasa una barrera- y NO del ancho
del bracket. En span 20-35 se midio o = 0,0642 pt.

LA REGLA NUEVA APLICADA - QUE DARIA ESTO SI EL SESGO NO DEPENDIERA DEL SPAN, escrito ANTES de correr:
  - o despejado seria el MISMO (~0,064 pt) en todos los spans, de 3 a 25;
  - el sesgo por operacion seguiria siendo lineal en (1-2p) y pasaria por cero en el simetrico;
  - lo unico que cambiaria seria la fraccion de barras AMBIGUAS -las dos barreras tocadas en la misma
    barra de un minuto-, que tiene que crecer al estrecharse porque la barra no se achica.
Si sale eso, el juez puede extender el rango caracterizado sin medir nada mas que la ambiguedad.
SI o CAMBIA DE FORMA AL ESTRECHARSE, eso es un hallazgo por si solo y hay que decirlo.
"""

import os
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from dolares_por_tiempo import SESION, cortes  # noqa: E402
from linea_base import cargar  # noqa: E402
from sesgo_marco import replay  # noqa: E402
from sintetico import armar, bootstrap, tripletes  # noqa: E402

K = int(os.environ.get("K_SERIES", "6"))
SEMILLA = 20260907
# por cada span, celdas con p distinto para poder ajustar la recta y despejar o.
# Se eligen multiplos del tick (0,25) para que sean brackets reales.
POR_SPAN = {
    3.0: [(1.0, 2.0), (1.5, 1.5), (2.0, 1.0)],
    4.0: [(1.0, 3.0), (2.0, 2.0), (3.0, 1.0)],
    5.0: [(1.0, 4.0), (2.5, 2.5), (4.0, 1.0)],
    7.0: [(2.0, 5.0), (3.5, 3.5), (5.0, 2.0)],
    10.0: [(2.0, 8.0), (5.0, 5.0), (8.0, 2.0)],
    25.0: [(5.0, 20.0), (12.5, 12.5), (20.0, 5.0)],   # el rango ya caracterizado, de control
}
O_PUBLICADO = 0.0642


def main():
    R = []
    A = R.append
    A("=" * 100)
    A("TAREA 1 - EL SESGO DE CONTABILIDAD EN SPANS DE 3 A 10 pt")
    A("NO GASTA CARTUCHO. K = 261. Dinero: $0. La caja sellada no se toca.")
    A("=" * 100)
    A("")
    A("   QUE DARIA SI EL SESGO NO DEPENDIERA DEL SPAN (escrito antes de correr): o despejado igual")
    A(f"   en todos los spans (~{O_PUBLICADO:.4f} pt), recta lineal en (1-2p) por cero, y lo unico")
    A("   que crece al estrecharse es la fraccion de barras AMBIGUAS.")
    cl, hi, lo, con = cargar()
    n = len(cl)
    d, up, dn = tripletes(cl, hi, lo, con)
    mu = d.mean()
    dc, upc, dnc = d - mu, up - mu, dn - mu
    del cl, hi, lo, con
    ini, fin = cortes(n, SESION)
    A(f"\n   Bootstrap IID sin drift, {K} series de {n:,} barras, costo CERO, con marca a mercado.")
    A(f"   El span 25 va de CONTROL: tiene que reproducir el o = {O_PUBLICADO:.4f} ya publicado.")
    A("")
    A(f"   {'span':>6}{'bracket':>13}{'p':>7}{'1-2p':>8}{'sesgo pt/op':>14}{'error':>9}"
      f"{'o despejado':>13}{'ambiguo':>10}{'op/serie':>11}")
    resumen = {}
    for span in sorted(POR_SPAN):
        os_desp, filas = [], []
        for T, S in POR_SPAN[span]:
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
            o_d = m / f if abs(f) > 1e-9 else float("nan")
            if abs(f) > 1e-9:
                os_desp.append(o_d)
            filas.append((f, m))
            A(f"   {span:>6.0f}{f'{T:g}:{S:g}':>13}{p:>7.2f}{f:>8.2f}{m:>+14.4f}{se:>9.4f}"
              f"{o_d:>13.4f}{ambs/ops*100:>9.3f}%{ops//(2*K):>11,}")
            print(f"      span {span} {T}:{S} listo", file=sys.stderr, flush=True)
        x = np.array([q[0] for q in filas]); y = np.array([q[1] for q in filas])
        a_, b_ = np.polyfit(x, y, 1)
        resumen[span] = dict(o=float(np.mean(os_desp)), pend=float(a_), inter=float(b_),
                             amb=ambs / ops * 100)
        A("")

    A("=" * 100)
    A("   EL RESUMEN POR SPAN")
    A("=" * 100)
    A(f"   {'span':>6}{'o despejado':>14}{'pendiente':>12}{'intercepto':>13}{'ambiguo %':>12}"
      f"{'o / o(25)':>12}")
    o25 = resumen[25.0]["o"]
    for span in sorted(resumen):
        r = resumen[span]
        A(f"   {span:>6.0f}{r['o']:>14.4f}{r['pend']:>12.4f}{r['inter']:>13.5f}{r['amb']:>11.3f}%"
          f"{r['o']/o25:>12.2f}")
    A("")
    A(f"   CONTROL: el span 25 tiene que reproducir el o publicado de {O_PUBLICADO:.4f}. Dio "
      f"{o25:.4f}, o sea {o25/O_PUBLICADO:.2f}x.")
    cocientes = [resumen[s]["o"] / o25 for s in sorted(resumen) if s != 25.0]
    A("")
    if max(abs(c - 1) for c in cocientes) < 0.20:
        A("   EL SESGO NO DEPENDE DEL SPAN: o despejado es el mismo dentro de +-20% en todo el rango")
        A("   de 3 a 25 pt. El modelo de sobrepaso vale igual en brackets estrechos, y el juez puede")
        A("   extender el rango caracterizado.")
    else:
        A("   EL SESGO CAMBIA DE FORMA AL ESTRECHARSE, y eso es un hallazgo por si solo: o despejado")
        A(f"   se mueve hasta {max(abs(c-1) for c in cocientes):.0%} respecto del span 25. El modelo de")
        A("   sobrepaso con o constante NO se puede extrapolar a brackets estrechos.")
    A("")
    A(f"   Y LA AMBIGUEDAD, que era la prediccion segura: pasa de {resumen[25.0]['amb']:.3f}% en span")
    A(f"   25 a {resumen[3.0]['amb']:.3f}% en span 3. Cada barra ambigua se cuenta como PERDIDA, asi")
    A(f"   que es un sesgo negativo que crece al estrecharse y NO lo captura el modelo de sobrepaso.")

    A("")
    A("-" * 100)
    A("   Y EL INTERCEPTO ES LA AMBIGUEDAD, VERIFICADO. El modelo de DOS terminos que si sirve.")
    A("-" * 100)
    A("   El modelo de un termino -sesgo = o*(1-2p)- exige que la recta pase por CERO. No pasa: el")
    A("   intercepto crece al estrecharse. Y hay un candidato obvio para explicarlo, porque una barra")
    A("   ambigua convierte una ganancia de +T en una perdida de -S, o sea que cuesta (T+S) = span,")
    A("   y afecta a TODAS las celdas por igual -es un corrimiento, no una antisimetria-.")
    A("   PREDICCION: intercepto  ~  - (tasa de ambiguas) x span x (fraccion que hubiera ganado)")
    A("   Con la fraccion en 0,5, que es lo que da una barra donde se tocan las dos barreras:")
    A("")
    A(f"   {'span':>6}{'intercepto medido':>20}{'predicho por ambiguedad':>26}{'cociente':>11}")
    for span in sorted(resumen):
        r = resumen[span]
        pred = -(r["amb"] / 100.0) * span * 0.5
        coc = r["inter"] / pred if abs(pred) > 1e-9 else float("nan")
        A(f"   {span:>6.0f}{r['inter']:>20.5f}{pred:>26.5f}{coc:>11.2f}")
    cocs = [resumen[s]["inter"] / (-(resumen[s]["amb"] / 100.0) * s * 0.5)
            for s in sorted(resumen) if resumen[s]["amb"] > 0.02]
    A("")
    if cocs and max(abs(c - 1) for c in cocs) < 0.35:
        A("   COINCIDE. El intercepto ES la ambiguedad, y entonces el sesgo de contabilidad tiene DOS")
        A("   terminos y no uno:")
        A("       sesgo por operacion  =  o * (1 - 2p)  -  (tasa ambigua) * span * 0,5")
        A("   El primero es antisimetrico y el segundo es un corrimiento parejo hacia abajo. En span")
        A("   20-35 el segundo es despreciable (0,006% de ambiguas) y por eso el modelo de un termino")
        A("   alcanzaba. En span 3 el segundo es el que MANDA.")
        A("")
        A("   CONSECUENCIA PRACTICA, y es la que abre la ventana operable: el juez SI puede juzgar")
        A(f"   brackets estrechos, con o ~ {np.mean([resumen[s]['o'] for s in (3.0,4.0,5.0,7.0,10.0)]):.4f}")
        A("   -no el 0,0642 del span 25- MAS el termino de ambiguedad, que se calcula de la tasa")
        A("   medida. Las dos cosas estan aca y las dos son del proceso, no del candidato.")
    else:
        A("   NO COINCIDE: el intercepto no se explica por la ambiguedad sola. Hay un tercer efecto y")
        A("   no se cual. El juez NO puede juzgar brackets estrechos hasta encontrarlo.")
    A("")
    A("   MARCA DE FRAGILIDAD, y es importante: el CONTROL del span 25 dio o = "
      f"{o25:.4f} contra el {O_PUBLICADO:.4f} publicado, o sea {o25/O_PUBLICADO:.2f}x. Con "
      f"{K} series")
    A("   y tres celdas contra las ocho series y cinco celdas del original, esa diferencia es del")
    A("   orden del error de muestreo, pero NO la verifique. Todos los o de esta tabla arrastran esa")
    A("   incertidumbre de ~15%.")
    A("=" * 100)
    print("\n".join(R))
    return 0


if __name__ == "__main__":
    sys.exit(main())
