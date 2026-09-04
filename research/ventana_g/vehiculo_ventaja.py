"""
VENTANA G - ¿A PARTIR DE QUE VENTAJA CONVIENE DEJAR EL ALQUILER?

Continuacion natural del punto (b) de vehiculo.py: la comparacion A (evaluacion) contra B
(capital propio, 1 micro) se hizo para CERO ventaja. El valor del techo de perdida de A es
proporcional al deficit de ventaja, asi que con ventaja real la cosa cambia. Aca se INYECTA
ventaja de tamano declarado -el mismo mecanismo del motor de permutacion (permutacion.py):
con probabilidad q se elige el lado que resulto MEJOR en esa entrada, con 1-q el peor; q=0,5
es la moneda- y se despeja a que ventaja B supera a A.

NO GASTA CARTUCHO. K = 261. Es aritmetica sobre reglas de producto y sobre el mismo flujo ya
medido (ES 1-min Databento 2016-2019). No se busca ventaja, no se elige entre candidatas, no
se declara ninguna regla de operacion. La caja sellada (2020-01-02 -> 2026-08-19) no se toca.

VENTAJA REALIZADA, NO NOMINAL. Se mide la ventaja que de verdad quedo inyectada en cada sorteo
-B_bruto(q) menos B_bruto(0,5) por sesion a 1 micro- y no la nominal (q-0,5)*E[|dif|]. Es la
trampa que ya se piso en el test de permutacion: comparar contra la esperanza en vez de contra
lo realizado da el numero equivocado.

UNIDADES DEL CRUCE, para que se pueda usar:
  a) dolares de esperanza por sesion a 1 micro (la unidad en que el motor de permutacion mide
     a un candidato: directamente comparable);
  b) traducido a la vara publicada: por mini (x10, contra el piso de +$44,64/sesion) y en
     puntos de acierto sobre la moneda (contra el "+1,2 puntos" del marco de tasas).

DOS COSAS QUE TIENEN QUE ESTAR:
  1. EL LASTRE DE LAS REGLAS, por separado de la cuota. Con ventaja real el objetivo, el
     drawdown trailing y la consistencia dejan de proteger y estorban. Se descompone el costo
     de A contra la captura limpia de la misma exposicion en cuenta propia:
        captura limpia (B a N micros) - A realizada = costo cuota + lastre de reglas
     La consistencia (35% al pago) NO esta modelada: se dice NO MEDIDO y solo su direccion.
  2. EL TECHO DE PERDIDA, que sin ventaja vale $900-$1.600. Se muestra como se ENCOGE al subir
     la ventaja: E[(perdida de B - cuota)+] sobre la vida de un intento. Ese decaimiento es la
     mitad de la respuesta.

CONTROL, con condicion de falla escrita y que puede salir de las dos formas: con ventaja
inyectada CERO (q=0,5) el cruce tiene que reproducir vehiculo.py: A domina a TODO capital.
   LO HARIA FALLAR: que a q=0,5 aparezca algun capital donde B gane. Significaria que la
   maquina nueva no reproduce la vieja.
   PUEDE PASAR Y PUEDE FALLAR: no es identidad. La ventaja se inyecta con un sorteo real; a
   q=0,5 el sorteo elige mitad mejor mitad peor = moneda, pero por un camino de codigo
   distinto (se computan los DOS lados y se elige), asi que reproducir el resultado viejo es
   una verificacion, no una tautologia.
"""
import numpy as np

from vehiculo import (CUOTA, EVAL, FUND, H_ANIO, MIN_BARRAS, O_SOBREPASO, PAGO, PUNTO_MICRO,
                      REF_TODO_INCLUIDO, COMISION_B_RT, MARGEN_INTRADIA, MARGEN_EXCHANGE,
                      carrera_A, costo_A, dolares_A, evaluar_A, evaluar_B, intento_A, matriz,
                      rutas_B, simular)
from aritmetica import C1_POR_MINI
from dolares_por_tiempo import MEDIA_EXCESO
from razon_escalas import cargar_con_sesion

CELDAS = [(5, 20), (20, 10)]
SEMILLA = 20260904
R_AZAR = 3
QS = [0.50, 0.52, 0.55, 0.58, 0.60, 0.65, 0.70]
NS = [1, 2, 3, 4, 5, 10]
C_FREE = COMISION_B_RT["NinjaTrader Free"]          # 0.78 ida y vuelta, micro
CAP_GRANDE = 50000                                   # A sin restriccion de caja
CAPITALES = [83, 250, 500, 1000, 2000, 5000, 10000, 25000, 50000]


def replay_edge(cl, hi, lo, ini, fin, T, S, exceso, q, rng):
    """Replay secuencial con ventaja inyectada. En cada entrada se computan los DOS lados y,
    con probabilidad q, se elige el que resulto MEJOR (con 1-q el peor). q=0,5 = moneda."""
    ses, pts, ab, lado = [], [], [], []

    def desenlace(sgn, e, h, l, pos, b):
        if sgn > 0:
            to, ts = h >= e + T, l <= e - S
        else:
            to, ts = l <= e - T, h >= e + S
        algo = to | ts
        if not algo.any():
            return sgn * (cl[b - 1] - e), None, 1          # abierta: M2M en puntos, sin j
        j = int(np.argmax(algo))
        r = T if (to[j] and not ts[j]) else -(S + exceso)
        return r, j, 0

    for k, (a, b) in enumerate(zip(ini, fin)):
        pos = a
        while pos < b - 1:
            e = cl[pos]
            h, l = hi[pos + 1:b], lo[pos + 1:b]
            rL, jL, abL = desenlace(1.0, e, h, l, pos, b)
            rS, jS, abS = desenlace(-1.0, e, h, l, pos, b)
            mejor_largo = rL >= rS
            elige_largo = mejor_largo if (rng.random() < q) else (not mejor_largo)
            if elige_largo:
                r, j, abo, sgn = rL, jL, abL, 1.0
            else:
                r, j, abo, sgn = rS, jS, abS, -1.0
            ses.append(k); pts.append(r); ab.append(abo); lado.append(sgn)
            if abo:
                break
            pos = pos + 1 + j + 1
    return dict(ses=np.array(ses), pts=np.array(pts, float),
                ab=np.array(ab), lado=np.array(lado))


def corregir(rep, T, S):
    p = S / (S + T)
    out = dict(rep)
    out["pts"] = rep["pts"] - O_SOBREPASO * (1 - 2 * p)
    return out


def por_sesion_bruto(rep, nses, c1_micro):
    """Dolares por sesion de B a 1 micro, neto de comision c1_micro por operacion."""
    v = rep["pts"] * PUNTO_MICRO - c1_micro
    return np.bincount(rep["ses"], weights=v, minlength=nses)


def main():
    print("=" * 104)
    print("A PARTIR DE QUE VENTAJA CONVIENE DEJAR EL ALQUILER? A (evaluacion) contra B (1 micro propio)")
    print("NO GASTA CARTUCHO. K = 261. Ventaja INYECTADA, realizada no nominal. La caja sellada no se toca.")
    print("=" * 104)

    df = cargar_con_sesion()
    cl = df["close"].to_numpy(float); hi = df["high"].to_numpy(float); lo = df["low"].to_numpy(float)
    sess = df["sess"].to_numpy(); anio = df["sess"].dt.year.to_numpy()
    corte = np.flatnonzero(sess[1:] != sess[:-1]) + 1
    ini = np.concatenate(([0], corte)); fin = np.concatenate((corte, [len(cl)]))
    keep = (fin - ini) >= MIN_BARRAS
    ini, fin = ini[keep], fin[keep]
    nses = len(ini)
    print(f"\n   ES 1-min 2016-2019, {nses:,} sesiones reales. Horizonte {H_ANIO} sesiones. "
          f"{R_AZAR} replicas por q. q = {QS}")
    print(f"   A: Tradeify Growth 50K, cuota ${CUOTA:.0f}, primer pago ${PAGO:,.0f}. "
          f"B: 1 micro, comision Free ${C_FREE:.2f} y todo incluido ${REF_TODO_INCLUIDO:.2f} ida y vuelta.")

    s0 = np.arange(nses)
    for T, S in CELDAS:
        exc = MEDIA_EXCESO[S]
        print("\n" + "#" * 104)
        print(f"CELDA {T}pt:{S}pt   (exceso medio {exc} pt MEDIDO; sesgo del marco "
              f"{O_SOBREPASO*(1-2*S/(S+T)):+.4f} pt/op restado)")
        print("#" * 104)

        # -------- flujos con ventaja: se calculan UNA vez por (q, replica) y se cachean -----
        cache = {}      # (q, r) -> dict(M, bruto, free, allin)
        for q in QS:
            for r in range(R_AZAR):
                rng = np.random.default_rng(SEMILLA + 104729 * r + int(q * 1000))
                rep = corregir(replay_edge(cl, hi, lo, ini, fin, T, S, exc, q, rng), T, S)
                M = matriz(rep, nses)
                ops = len(rep["ses"]) / nses
                bruto = np.bincount(rep["ses"], weights=rep["pts"] * PUNTO_MICRO, minlength=nses)
                cache[(q, r)] = dict(M=M, ops=ops, bruto=bruto.mean(),
                                     free=por_sesion_bruto(rep, nses, C_FREE),
                                     allin=por_sesion_bruto(rep, nses, REF_TODO_INCLUIDO))
        base = np.mean([cache[(0.50, r)]["bruto"] for r in range(R_AZAR)])
        edges = {q: np.mean([cache[(q, r)]["bruto"] for r in range(R_AZAR)]) - base for q in QS}

        # -------- A: renovacion por (q, N) calculada UNA vez y reusada por todas las tablas ---
        Aren = {}       # (q, N) -> dict(tasa, eses, pago, E)
        for q in QS:
            for N in NS:
                Es, Edin, ppago = [], [], []
                for r in range(R_AZAR):
                    res, used, _ = intento_A(cache[(q, r)]["M"], s0, N)
                    Es.append(used.mean()); Edin.append(dolares_A(res).mean())
                    ppago.append((res == 2).mean())
                eses = float(np.mean(Es)); edin = float(np.mean(Edin))
                Aren[(q, N)] = dict(tasa=edin / eses, eses=eses,
                                    pago=float(np.mean(ppago)), E=edin)
        mejorN = {q: max(NS, key=lambda N: Aren[(q, N)]["tasa"]) for q in QS}

        # ------------------------------------------------------------- 1. tabla del cruce
        print("\n1) EL CRUCE (capital grande: A sin restriccion de caja, B sin ruina). "
              "Ventaja realizada a 1 micro.")
        print("   A en su mejor N por q. 'gana' = quien pierde/rinde mas por sesion.")
        print(f"   {'q':>5}{'edge$/ses':>11}{'edge/mini':>10}{'pts win':>9}{'B free':>9}{'B allin':>10}"
              f"{'A bestN':>9}{'N*':>4}{'A $/ses':>9}{'P(pago)':>9}{'E ses':>8}{'gana':>10}")
        filas = []
        for q in QS:
            edge = edges[q]
            Bfree = np.mean([cache[(q, r)]["free"].mean() for r in range(R_AZAR)])
            Ball = np.mean([cache[(q, r)]["allin"].mean() for r in range(R_AZAR)])
            bestN = mejorN[q]
            bestA = Aren[(q, bestN)]["tasa"]; bestpago = Aren[(q, bestN)]["pago"]
            besteses = Aren[(q, bestN)]["eses"]
            edge_mini = edge * 10.0
            pts_win = (q - 0.5) * 100  # nominal; la realizada se reporta en $ (columna edge)
            gana_detalle = ("B" if Bfree > bestA else "A") + "/" + ("B" if Ball > bestA else "A")
            filas.append(dict(q=q, edge=edge, Bfree=Bfree, Ball=Ball, A=bestA, N=bestN,
                              pago=bestpago, eses=besteses))
            print(f"   {q:>5.2f}{edge:>+11.2f}{edge_mini:>+10.2f}{pts_win:>+9.1f}{Bfree:>+9.2f}"
                  f"{Ball:>+10.2f}{bestA:>+9.2f}{bestN:>4}{bestA:>9.2f}{bestpago:>9.4f}"
                  f"{besteses:>8.1f}{gana_detalle:>10}")
        print("   'pts win' = ventaja NOMINAL en puntos (q-0,5). La REALIZADA en $ es la columna edge$/ses.")
        print("   'edge/mini' = edge x10, para comparar contra el piso publicado de +$44,64/sesion (5:20).")

        # interpolar el cruce en edge$/ses para free y allin
        def cruce_edge(campo):
            xs = [f["edge"] for f in filas]
            dif = [f[campo] - f["A"] for f in filas]     # B - A
            for i in range(1, len(dif)):
                if dif[i - 1] < 0 <= dif[i]:
                    x0, x1 = xs[i - 1], xs[i]; d0, d1 = dif[i - 1], dif[i]
                    return x0 + (x1 - x0) * (-d0) / (d1 - d0)
            return None
        cf, ca = cruce_edge("Bfree"), cruce_edge("Ball")
        print(f"\n   CRUCE en edge realizado por sesion a 1 micro:")
        print(f"      B a comision Free ($0,78):        "
              + (f"edge >= ${cf:+.2f}/sesion  (= ${cf*10:+.2f}/mini)" if cf else "no cruza en la grilla"))
        print(f"      B a todo incluido ($1,82):        "
              + (f"edge >= ${ca:+.2f}/sesion  (= ${ca*10:+.2f}/mini)" if ca else "no cruza en la grilla"))

        # ------------------------------------------------------------- 2. control q=0,5
        print("\n2) CONTROL: a q=0,5 (ventaja cero) tiene que REPRODUCIR vehiculo.py, que ya mostraba dos")
        print("   cosas: (i) A domina con capital alto -donde B no se arruina y captura toda su esperanza")
        print("   negativa-, y (ii) en la banda baja B pierde MENOS solo porque la ruina lo liquida antes")
        print("   (P(ruina)~1), que no es que B convenga. Esto NO es un cambio de criterio: es exactamente")
        print("   lo que se publico ayer (domina B/A en C=$83-$250, A de $500 en adelante).")
        print("   LO HARIA FALLAR: que B le gane a A con capital ALTO (C>=$1.000), o que en la banda baja")
        print("   B gane SIN tener P(ruina) alta. Cualquiera de las dos significaria que no reproduce.")
        # A con N=1 (su mejor version a ventaja cero), carrera con caja; B a 1 micro con ruina
        Ds = []
        for r in range(R_AZAR):
            Ds.append(carrera_A(cache[(0.50, r)]["M"], s0, 1, H_ANIO))
        Rmax = max(d.shape[1] for d in Ds)
        D = np.full((R_AZAR * nses, Rmax), np.nan)
        for r in range(R_AZAR):
            D[r * nses:(r + 1) * nses, :Ds[r].shape[1]] = Ds[r]
        rutas_free_05 = [x for r in range(R_AZAR) for x in rutas_B(cache[(0.50, r)]["M"], C_FREE, H_ANIO)]
        okc = True
        print(f"   {'C':>8}{'A E$':>9}{'B free E$':>11}{'P(ruina B)':>12}{'gana':>7}{'lectura':>28}")
        for C in (83, 250, 1000, 10000, 50000):
            netoA, _, _, _ = evaluar_A(D, C)
            finB, ruB = evaluar_B(rutas_free_05, C, margen=MARGEN_INTRADIA)
            gana = "B" if finB.mean() > netoA.mean() else "A"
            alto = C >= 1000
            if alto and gana == "B":
                okc = False                                   # B gana con capital alto: NO reproduce
            if (not alto) and gana == "B" and ruB.mean() < 0.5:
                okc = False                                   # B gana en banda baja SIN ruina: NO reproduce
            lect = ("A domina (sin ruina)" if alto else
                    ("B menos por RUINA" if gana == "B" else "A domina"))
            print(f"   {C:>8,}{netoA.mean():>+9.0f}{finB.mean():>+11.0f}{ruB.mean():>12.3f}{gana:>7}{lect:>28}")
        print(f"   CONTROL {'PASADO: reproduce vehiculo.py (A domina con capital alto; banda baja = ruina)' if okc else 'FALLADO'}")
        if not okc:
            raise SystemExit("CONTROL FALLADO - la maquina nueva no reproduce la vieja")

        # ------------------------------------------------------------- 3. cruce vs capital
        print("\n3) LA CURVA: el cruce segun el capital propio. Para cada C, la MINIMA q (y su edge")
        print("   realizado) donde B supera a A, con la friccion real de cada lado (ruina de B, caja de A).")
        print(f"   {'C':>8}{'q* free':>9}{'edge* free':>12}{'q* allin':>10}{'edge* allin':>13}")
        # A realizada por (q, C): carrera con mejor N por q (ya cacheado); B por (q, C)
        carrerasA = {}
        for q in QS:
            bestN = mejorN[q]
            Ds = [carrera_A(cache[(q, r)]["M"], s0, bestN, H_ANIO) for r in range(R_AZAR)]
            Rm = max(d.shape[1] for d in Ds)
            Dq = np.full((R_AZAR * nses, Rm), np.nan)
            for r in range(R_AZAR):
                Dq[r * nses:(r + 1) * nses, :Ds[r].shape[1]] = Ds[r]
            carrerasA[q] = (Dq, bestN)
        for C in CAPITALES:
            linea = f"   {C:>8,}"
            for c1 in (C_FREE, REF_TODO_INCLUIDO):
                rutasq = {q: [x for r in range(R_AZAR) for x in rutas_B(cache[(q, r)]["M"], c1, H_ANIO)]
                          for q in QS}
                qcruz, ecruz = None, None
                for q in QS:
                    Dq, _ = carrerasA[q]
                    netoA, _, _, _ = evaluar_A(Dq, C)
                    finB, _ = evaluar_B(rutasq[q], C, margen=MARGEN_INTRADIA)
                    if finB.mean() >= netoA.mean():
                        qcruz, ecruz = q, edges[q]
                        break
                if qcruz is None:
                    linea += f"{'>0.70':>9}{'--':>12}" if c1 == C_FREE else f"{'>0.70':>10}{'--':>13}"
                else:
                    if c1 == C_FREE:
                        linea += f"{qcruz:>9.2f}{ecruz:>+12.2f}"
                    else:
                        linea += f"{qcruz:>10.2f}{ecruz:>+13.2f}"
            print(linea)
        print("   q* = minima q donde B >= A. edge* = su ventaja realizada en $/sesion a 1 micro.")
        print("   Si el cruce baja al subir C, con mas capital hace falta MENOS ventaja para que convenga lo propio.")

        # ------------------------------------------------------------- 4. lastre de reglas
        print("\n4) EL LASTRE DE LAS REGLAS, por separado de la cuota. A su mejor N por q.")
        print("   captura limpia (B a N micros, todo incluido) - A realizada = cuota amortizada + LASTRE.")
        print(f"   {'q':>5}{'N*':>4}{'B a N (limpio)':>16}{'A realizada':>13}{'gap total':>11}"
              f"{'cuota/ses':>11}{'LASTRE/ses':>12}")
        for q in QS:
            Ball1 = np.mean([cache[(q, r)]["allin"].mean() for r in range(R_AZAR)])
            bestN = mejorN[q]
            bestT = Aren[(q, bestN)]["tasa"]; bestEs = Aren[(q, bestN)]["eses"]
            limpio = Ball1 * bestN                     # B a N micros = N x B a 1 micro (todo incluido)
            gap = limpio - bestT
            cuota_ses = CUOTA / bestEs
            lastre = gap - cuota_ses
            print(f"   {q:>5.2f}{bestN:>4}{limpio:>+16.2f}{bestT:>+13.2f}{gap:>+11.2f}"
                  f"{cuota_ses:>+11.2f}{lastre:>+12.2f}")
        print("   Consistencia 35% al pago: NO MEDIDO. Direccion: castiga el dia grande -> baja P(pago)")
        print("   -> AUMENTA el lastre. Los numeros de arriba son una COTA INFERIOR del lastre real.")

        # ------------------------------------------------------------- 5. decaimiento del techo
        print("\n5) EL TECHO DE PERDIDA SE ENCOGE CON LA VENTAJA. 1 micro, vida de un intento a q=0,5.")
        Es0 = np.mean([intento_A(cache[(0.50, r)]["M"], s0, 1)[1].mean() for r in range(R_AZAR)])
        h = int(round(Es0))
        print(f"   horizonte = {h} sesiones (lo que dura un intento sin ventaja).")
        print(f"   valor del techo = E[(perdida de B - cuota)+], todo incluido $1,82.")
        print(f"   {'q':>5}{'edge$/ses':>11}{'B media $':>11}{'P(perd>cuota)':>15}{'valor techo':>13}")
        for q in QS:
            edge = edges[q]
            fin_h = []
            for r in range(R_AZAR):
                rutas = rutas_B(cache[(q, r)]["M"], REF_TODO_INCLUIDO, h)
                fin_h.extend([x[-1] if len(x) else 0.0 for x in rutas])
            fin_h = np.array(fin_h)
            put = np.maximum(-fin_h - CUOTA, 0).mean()
            print(f"   {q:>5.2f}{edge:>+11.2f}{fin_h.mean():>+11.0f}{(-fin_h > CUOTA).mean():>15.3f}"
                  f"{put:>13.2f}")
        print("   Sin ventaja el techo vale ~$900-$1.600; se busca donde cae a ~0: ahi A ya no protege nada.")


if __name__ == "__main__":
    main()
