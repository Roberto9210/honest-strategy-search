"""
TAREA 1 - ACOTAR EL 15%: converge el span 25 al 0,0642 publicado, o se queda en 0,0546?

NO GASTA CARTUCHO. K = 261. Dinero: $0. Bootstrap IID sobre ES, costo CERO. La caja sellada no se
toca.

EL PROBLEMA. Mi control de span 25 dio o = 0,0546 contra el 0,0642 publicado (0,85x), y todos los o
de la tabla de spans cortos arrastran ese 15%.

Y EL SOSPECHOSO ES EL SPAN 25, NO LOS CORTOS, por la columna que mire sin que me la pidieran: el span
25 tiene ~1.200 operaciones por serie contra decenas de miles en span 3. Es la medicion MENOS
precisa de la tabla, no la mas.

QUE SE HACE: correr SOLO span 25, con muchas mas series, y ver si converge.

LA PREDICCION NULA, POR COMPONENTE -la regla nueva, y esta vez desglosada y no en bloque-:
  (i)   si el 0,0546 era ruido de muestreo, al subir K el valor se mueve hacia 0,0642 y el error
        baja como raiz(K);
  (ii)  si el 0,0546 es el valor real de ESTA implementacion, se queda en 0,0546 con error chico y
        entonces hay algo distinto entre mi corrida y la original -semilla, celdas, o el codigo-;
  (iii) el error de muestreo tiene que bajar como raiz(K) en cualquiera de los dos casos; si no baja
        asi, el estimador no es lo que creo que es.
Las tres se pueden observar por separado y por eso van escritas por separado.
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

K = int(os.environ.get("K_SERIES", "40"))
SEMILLA = 20260907          # LA MISMA que uso sesgo_marco_spans_cortos.py, para que sea comparable
CELDAS = [(5.0, 20.0), (12.5, 12.5), (20.0, 5.0)]
O_PUBLICADO = 0.0642
O_MIO_K6 = 0.0546


def main():
    R = []
    A = R.append
    A("=" * 100)
    A("TAREA 1 - CONVERGENCIA DEL SPAN 25: el 15% es ruido o es otra cosa?")
    A("NO GASTA CARTUCHO. K = 261. Dinero: $0. La caja sellada no se toca.")
    A("=" * 100)
    A("")
    A("   PREDICCION NULA, POR COMPONENTE (escrita antes de correr):")
    A(f"   (i)   si era ruido: al subir K el valor se mueve hacia {O_PUBLICADO:.4f}")
    A(f"   (ii)  si es real: se queda en {O_MIO_K6:.4f} con error chico, y hay algo distinto")
    A("   (iii) el error tiene que bajar como raiz(K) en los dos casos")
    cl, hi, lo, con = cargar()
    n = len(cl)
    d, up, dn = tripletes(cl, hi, lo, con)
    mu = d.mean()
    dc, upc, dnc = d - mu, up - mu, dn - mu
    del cl, hi, lo, con
    ini, fin = cortes(n, SESION)
    A(f"\n   Span 25, {len(CELDAS)} celdas, {K} series de bootstrap (contra 6 de la tabla anterior).")

    por_celda = {}
    for T, S in CELDAS:
        f = 1.0 - 2.0 * (S / (S + T))
        serie = []
        for k in range(K):
            rg = np.random.default_rng(SEMILLA + 7919 * k)
            c2, h2, l2 = armar(*bootstrap(dc, upc, dnc, n, rg))
            t2 = o2 = 0.0
            for lado in ("largo", "corto"):
                t, o, am = replay(c2, h2, l2, ini, fin, T, S, lado)
                t2 += t; o2 += o
            serie.append(t2 / o2)
            del c2, h2, l2
        por_celda[(T, S)] = (f, np.array(serie))
        print(f"   {T}:{S} listo", file=sys.stderr, flush=True)

    A("")
    A(f"   {'bracket':>13}{'1-2p':>8}{'sesgo pt/op':>14}{'error':>10}{'o despejado':>14}"
      f"{'o con K=6':>12}")
    o_acum = []
    for (T, S), (f, v) in por_celda.items():
        m, se = v.mean(), v.std(ddof=1) / np.sqrt(len(v))
        o_d = m / f if abs(f) > 1e-9 else float("nan")
        if abs(f) > 1e-9:
            o_acum.append(o_d)
        A(f"   {f'{T:g}:{S:g}':>13}{f:>8.2f}{m:>+14.4f}{se:>10.5f}{o_d:>14.4f}"
          f"{'-' if abs(f) < 1e-9 else '':>12}")
    o_new = float(np.mean(o_acum))

    # la convergencia, por subconjuntos crecientes de series
    A("")
    A("-" * 100)
    A("   (iii) EL ERROR BAJA COMO RAIZ(K)?  o despejado usando las primeras k series")
    A("-" * 100)
    A(f"   {'k series':>10}{'o despejado':>14}{'error de o':>13}{'error x raiz(k)':>18}")
    for k in (3, 6, 10, 20, K):
        if k > K:
            continue
        os_k, ses_k = [], []
        for (T, S), (f, v) in por_celda.items():
            if abs(f) < 1e-9:
                continue
            m = v[:k].mean(); se = v[:k].std(ddof=1) / np.sqrt(k)
            os_k.append(m / f); ses_k.append(se / abs(f))
        A(f"   {k:>10}{np.mean(os_k):>14.4f}{np.mean(ses_k):>13.5f}"
          f"{np.mean(ses_k)*np.sqrt(k):>18.5f}")

    A("")
    A("=" * 100)
    A("   LA RESPUESTA")
    A("=" * 100)
    se_fin = np.mean([por_celda[c][1].std(ddof=1) / np.sqrt(K) / abs(por_celda[c][0])
                      for c in CELDAS if abs(por_celda[c][0]) > 1e-9])
    A(f"   o con K={K}: {o_new:.4f} +- {se_fin:.4f}   (con K=6 daba {O_MIO_K6:.4f})")
    A(f"   publicado en sesgo_marco.py: {O_PUBLICADO:.4f}")
    A(f"   distancia al publicado: {(o_new - O_PUBLICADO)/se_fin:+.1f} errores")
    A("")
    if abs(o_new - O_PUBLICADO) < 2 * se_fin:
        A("   (i) CONVERGE. El 0,0546 era ruido de muestreo: con mas series el valor es compatible")
        A(f"   con el {O_PUBLICADO:.4f} publicado dentro de dos errores. El 15% desaparece y la")
        A("   cadena de spans cortos queda limpia.")
    elif abs(o_new - O_MIO_K6) < 2 * se_fin:
        A("   (ii) NO CONVERGE: se queda donde estaba, con error chico. Hay algo distinto entre esta")
        A("   corrida y la original y NO es ruido. Candidatos, sin elegir uno: la semilla (uso")
        A(f"   {SEMILLA} contra 20260904), las celdas (tres contra cinco) o el numero de series.")
    else:
        A("   NI UNA NI OTRA: el valor se movio a un tercer lugar. Hay que mirarlo.")
    A("")
    A(f"   Y LO QUE ESTO LE HACE A LOS SPANS CORTOS: si el span 25 sube a {O_PUBLICADO:.4f}, el")
    A(f"   cociente o_corto/o_25 pasa de ~0,48 a ~{0.0264/O_PUBLICADO:.2f}. La conclusion NO cambia")
    A("   -o sigue siendo la mitad o menos en brackets estrechos- pero el factor exacto si.")
    A("=" * 100)
    print("\n".join(R))
    return 0


if __name__ == "__main__":
    sys.exit(main())
