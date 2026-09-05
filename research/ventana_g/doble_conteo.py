"""
VENTANA G - SOBREPASO Y DESLIZAMIENTO DE ENTRADA: el mismo termino contado dos veces, o dos?

NO GASTA CARTUCHO. K = 261. Validacion de instrumento.

LA SOSPECHA, mia, del reporte anterior. El sobrepaso de contabilidad del marco nuevo dio
0,0642 pt = 0,26 TICKS. El limite de deslizamiento de entrada que medi antes era 0,28 TICKS.
Estan sospechosamente cerca. Si son el mismo termino, el piso de $44,64 esta inflado y el
numero que le pase a Roberto cambia.

COMO SE DISTINGUE, y es limpio porque los dos tienen FIRMA FUNCIONAL DISTINTA:

  - el SOBREPASO es geometrico: vale o*(1-2p) con p = S/(S+T), asi que depende del bracket y
    CAMBIA DE SIGNO al pasar de p<1/2 a p>1/2.
  - el DESLIZAMIENTO DE ENTRADA es un costo por operacion: vale -e SIEMPRE, no depende de la
    geometria y NUNCA cambia de signo.

Ajustando sesgo = a*(1-2p) + b sobre brackets de igual span, el sobrepaso vive en la
PENDIENTE a y el deslizamiento de entrada vive en la ORDENADA b. Son coordenadas distintas
del mismo ajuste: si son terminos distintos, inyectar deslizamiento tiene que mover SOLO b.

LA PRUEBA, escrita antes de correr. Se corre el mismo barrido con deslizamiento de entrada
inyectado e = 0,25 puntos (un tick entero) y se compara contra e = 0:

  PREDICCION: la pendiente a NO se mueve (queda en 0,064 dentro del ruido) y la ordenada b
  pasa de ~0 a -0,25 EXACTO. Eso significa dos terminos distintos y el piso esta bien.

  QUE LA FALSA: que la pendiente se mueva al inyectar deslizamiento. Ahi los dos terminos
  interactuan, se estan contando dos veces, y hay que corregir el piso.

Las dos salidas son posibles y las dos cambian lo que hay que decirle a Roberto.
"""
import numpy as np

from dolares_por_tiempo import PUNTO_ES, SESION, cortes
from linea_base import cargar
from sintetico import armar, bootstrap, tripletes

K = 6
SEMILLA = 20260904
CELDAS = [(5.0, 20.0), (10.0, 15.0), (12.5, 12.5), (15.0, 10.0), (20.0, 5.0)]
ENTRADAS = [0.0, 0.25]          # puntos de deslizamiento de ENTRADA inyectados
E_INYECTADA_TICKS = 1.0


def replay(cl, hi, lo, ini, fin, T, S, lado, entrada=0.0):
    """Replay secuencial, costo cero salvo el deslizamiento de ENTRADA inyectado, que se
    paga en TODA operacion apenas se abre, resuelva o no."""
    sgn = 1.0 if lado == "largo" else -1.0
    tot = 0.0
    n_op = 0
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
            n_op += 1
            tot -= entrada                      # el deslizamiento de entrada se paga siempre
            if not algo.any():
                tot += sgn * (cl[b - 1] - e)
                break
            j = int(np.argmax(algo))
            tot += T if (to[j] and not ts[j]) else -S
            pos = pos + 1 + j + 1
    return tot, n_op


def main():
    print("=" * 100)
    print("DOBLE CONTEO? - sobrepaso de barrera contra deslizamiento de entrada")
    print("NO GASTA CARTUCHO. K = 261. Prediccion escrita antes de correr, ver docstring.")
    print("=" * 100)

    cl, hi, lo, con = cargar()
    n = len(cl)
    d, up, dn = tripletes(cl, hi, lo, con)
    mu = d.mean()
    dc, upc, dnc = d - mu, up - mu, dn - mu
    del cl, hi, lo, con
    ini, fin = cortes(n, SESION)
    print(f"\n   Bootstrap IID sin drift, {K} series de {n:,} barras, brackets de span 25.")
    print(f"   Deslizamiento de entrada inyectado: {ENTRADAS} puntos "
          f"({E_INYECTADA_TICKS:.0f} tick entero en el segundo caso).\n")

    ajustes = {}
    for ent in ENTRADAS:
        print(f"   --- deslizamiento de entrada inyectado = {ent:.2f} pt ---")
        print(f"   {'bracket':>13}{'p':>7}{'1-2p':>8}{'sesgo pt/op':>14}{'error':>9}")
        xs, ys = [], []
        for T, S in CELDAS:
            p = S / (S + T)
            f = 1.0 - 2.0 * p
            porc = []
            for k in range(K):
                rg = np.random.default_rng(SEMILLA + 7919 * k)
                c2, h2, l2 = armar(*bootstrap(dc, upc, dnc, n, rg))
                t2 = o2 = 0.0
                for lado in ("largo", "corto"):
                    t, o = replay(c2, h2, l2, ini, fin, T, S, lado, entrada=ent)
                    t2 += t; o2 += o
                porc.append(t2 / o2)
                del c2, h2, l2
            v = np.array(porc)
            xs.append(f); ys.append(v.mean())
            print(f"   {f'{T:g}pt:{S:g}pt':>13}{p:>7.2f}{f:>8.2f}{v.mean():>+14.4f}"
                  f"{v.std(ddof=1)/np.sqrt(K):>9.4f}")
        a, b = np.polyfit(np.array(xs), np.array(ys), 1)
        pred = a * np.array(xs) + b
        ss_res = ((np.array(ys) - pred) ** 2).sum()
        ss_tot = ((np.array(ys) - np.mean(ys)) ** 2).sum()
        ajustes[ent] = (a, b, 1 - ss_res / ss_tot)
        print(f"   ajuste: pendiente a = {a:+.4f}   ordenada b = {b:+.4f}   "
              f"R2 = {1 - ss_res/ss_tot:.4f}\n")

    a0, b0, _ = ajustes[0.0]
    a1, b1, _ = ajustes[0.25]
    print("=" * 100)
    print("EL VEREDICTO")
    print("=" * 100)
    print(f"\n   {'':>28}{'e = 0,00':>12}{'e = 0,25':>12}{'movimiento':>13}{'esperado':>11}")
    print(f"   {'PENDIENTE (sobrepaso)':>28}{a0:>+12.4f}{a1:>+12.4f}{a1-a0:>+13.4f}"
          f"{0.0:>+11.4f}")
    print(f"   {'ORDENADA (desliz. entrada)':>28}{b0:>+12.4f}{b1:>+12.4f}{b1-b0:>+13.4f}"
          f"{-0.25:>+11.4f}")
    mov_a = abs(a1 - a0)
    mov_b = abs((b1 - b0) - (-0.25))
    distintos = mov_a < 0.25 * abs(a0) and mov_b < 0.02
    print(f"\n   La pendiente se movio {mov_a:.4f} ({mov_a/abs(a0)*100:.1f}% de su valor).")
    print(f"   La ordenada se movio {b1-b0:+.4f} contra los {-0.25:+.2f} inyectados "
          f"(error {mov_b:.4f}).")
    if distintos:
        print("\n   -> SON DOS TERMINOS DISTINTOS. El deslizamiento de entrada entra entero")
        print("      en la ordenada y no toca la pendiente. NO hay doble conteo y el piso")
        print("      publicado NO cambia.")
    else:
        print("\n   -> INTERACTUAN. Se estan contando dos veces y hay que corregir el piso.")
    print(f"\n   Nota sobre la coincidencia numerica: sobrepaso {a0:.4f} pt = "
          f"{a0/0.25:.2f} ticks contra 0,28 ticks del limite de deslizamiento de entrada.")
    print("   Que dos cantidades den parecido no las hace la misma: lo que decide es como")
    print("   escalan, y escalan distinto.")
    return ajustes


if __name__ == "__main__":
    main()
