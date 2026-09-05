"""
VENTANA G - EL TEST DE PERMUTACION: el piso del CANDIDATO, no el de las entradas al azar.

NO GASTA CARTUCHO. K = 261. Construccion y validacion de un instrumento contra candidatos
sinteticos de propiedades conocidas. No hay hipotesis de mercado, no se elige entre
candidatas reales, no se declara ninguna regla de operacion. La caja sellada no se toca.

EL PROBLEMA. El piso de $44,64 por sesion es una propiedad de las ENTRADAS AL AZAR. Un
candidato real no entra al azar: entra condicionado, y eso le cambia cuantas veces opera,
cuanto aguanta, que fraccion le queda abierta y de que lado esta. Su piso es otro y no lo
sabemos.

LA SOLUCION. Calcular el piso sobre las entradas del PROPIO candidato, con su informacion
destruida por permutacion. Dos nulas, porque destruyen cosas distintas:

  NULA A - ROTACION. Se corre circularmente el vector (que ranuras toma, de que lado) sobre
  la grilla de ranuras. Conserva EXACTO cuantas opera, el espaciado y la secuencia de lados.
  Destruye CUANDO. Es la que pidio Roberto.

  NULA B - SIGNO. Se dan vuelta los lados al azar, dejando las ranuras intactas. Conserva
  EXACTO las ranuras, la tenencia, la fraccion abierta y el conteo. Destruye QUE LADO.

HONESTIDAD SOBRE LA NULA A, que hay que decir antes: para un candidato cuya senal depende del
precio es IMPOSIBLE conservar la tenencia bajo una permutacion temporal, porque la tenencia
la produce el precio. La rotacion conserva la SENAL; la tenencia se corre. Se mide cuanto se
corre y se reporta. Por eso van las dos nulas y no una.

LOS TRES CANDIDATOS SINTETICOS:
  C0      - toma todas las ranuras, lado al azar. Sin ventaja. Es la referencia.
  C_LENTO - toma solo las ranuras de volatilidad baja, lado al azar. SIN VENTAJA pero con
            patron de tenencia distinto: opera menos veces y aguanta mas.
  C_VENT  - todas las ranuras, y con probabilidad q = 0,55 elige el lado que resulto MEJOR
            en esa ranura. VENTAJA INYECTADA de magnitud declarable:

              ventaja por operacion = (q - 0,5) * E[ |P&L largo - P&L corto| ]

            que es exacta en esperanza, no aproximada. Con q = 0,55 son 0,05 * E[|dif|].

CONTROL, con condicion de falla escrita, y los dos lados pueden salir mal:
   sobre C0 y C_LENTO las dos nulas tienen que dar ventaja CERO dentro de su error;
   sobre C_VENT tienen que RECUPERAR la magnitud inyectada.
   LO HARIA FALLAR: que no recupere la inyectada, o que le encuentre ventaja a los que no
   tienen.
   Y UNA ADVERTENCIA SOBRE LA FUERZA DE CADA MITAD: que la nula B recupere la ventaja
   inyectada esta CASI FORZADO por construccion, porque la inyeccion se define justamente
   contra el promedio de los dos lados, que es lo que la nula B estima. La que NO esta
   forzada -y por lo tanto la que informa- es que la nula A tambien la recupere, y que las
   dos den cero en C0 y C_LENTO.
"""
import numpy as np

from aritmetica import C1_POR_MINI
from dolares_por_tiempo import MEDIA_EXCESO, PUNTO_ES
from razon_escalas import cargar_con_sesion

PASO = 300              # separacion entre ranuras, en barras
MIN_BARRAS = 60
CELDA = (5, 20)
Q = 0.55
NPERM = 1000
SEMILLA = 20260904


def ranuras(cl, hi, lo, ini, fin, T, S, exceso, c1):
    """Tabla de resultados por ranura y por lado. Se calcula UNA vez; despues todas las
    permutaciones son selecciones sobre esta tabla."""
    idx, ses, pnl_l, pnl_c, ten_l, ten_c, ab_l, ab_c = [], [], [], [], [], [], [], []
    for k, (a, b) in enumerate(zip(ini, fin)):
        for p0 in range(a, b - 1, PASO):
            e = cl[p0]
            fila = {}
            for lado, sgn in (("largo", 1.0), ("corto", -1.0)):
                obj, stp = e + sgn * T, e - sgn * S
                h, l = hi[p0 + 1:b], lo[p0 + 1:b]
                if lado == "largo":
                    to, ts = h >= obj, l <= stp
                else:
                    to, ts = l <= obj, h >= stp
                algo = to | ts
                if not algo.any():
                    fila[lado] = (sgn * (cl[b - 1] - e) * PUNTO_ES - c1, b - 1 - p0, 1)
                else:
                    j = int(np.argmax(algo))
                    r = T if (to[j] and not ts[j]) else -(S + exceso)
                    fila[lado] = (r * PUNTO_ES - c1, j + 1, 0)
            idx.append(p0); ses.append(k)
            pnl_l.append(fila["largo"][0]); ten_l.append(fila["largo"][1])
            ab_l.append(fila["largo"][2])
            pnl_c.append(fila["corto"][0]); ten_c.append(fila["corto"][1])
            ab_c.append(fila["corto"][2])
    return dict(ses=np.array(ses), pnl=np.stack([np.array(pnl_c), np.array(pnl_l)]),
                ten=np.stack([np.array(ten_c), np.array(ten_l)]),
                ab=np.stack([np.array(ab_c), np.array(ab_l)]), idx=np.array(idx))


def por_sesion(tab, masc, lado01, nses):
    """Dolares por sesion de un candidato. lado01: 0 = corto, 1 = largo."""
    v = tab["pnl"][lado01, np.arange(len(masc))] * masc
    return np.bincount(tab["ses"], weights=v, minlength=nses)


def tenencia(tab, masc, lado01):
    m = masc.astype(bool)
    if not m.any():
        return float("nan"), float("nan")
    t = tab["ten"][lado01[m], np.flatnonzero(m)]
    a = tab["ab"][lado01[m], np.flatnonzero(m)]
    return t.mean(), a.mean() * 100


def main():
    print("=" * 100)
    print("TEST DE PERMUTACION - el piso del CANDIDATO, no el de las entradas al azar")
    print("NO GASTA CARTUCHO. K = 261. La caja sellada no se toca.")
    print("=" * 100)

    T, S = CELDA
    df = cargar_con_sesion()
    cl = df["close"].to_numpy(float)
    hi = df["high"].to_numpy(float)
    lo = df["low"].to_numpy(float)
    sess = df["sess"].to_numpy()
    corte = np.flatnonzero(sess[1:] != sess[:-1]) + 1
    ini = np.concatenate(([0], corte)); fin = np.concatenate((corte, [len(cl)]))
    keep = (fin - ini) >= MIN_BARRAS
    ini, fin = ini[keep], fin[keep]
    nses = len(ini)

    tab = ranuras(cl, hi, lo, ini, fin, T, S, MEDIA_EXCESO[S], C1_POR_MINI)
    nr = len(tab["ses"])
    print(f"\n   celda {T}pt:{S}pt, ranuras cada {PASO} barras, sesiones reales.")
    print(f"   {nses:,} sesiones, {nr:,} ranuras ({nr/nses:.2f} por sesion).")
    print(f"   Comision y deslizamiento MEDIDOS ya adentro de la tabla.")

    rng = np.random.default_rng(SEMILLA)
    lado_azar = rng.integers(0, 2, nr)

    # volatilidad previa a cada ranura, para el candidato lento
    rango = hi - lo
    vprev = np.array([rango[max(0, i - PASO):i].mean() if i > 0 else rango[0]
                      for i in tab["idx"]])
    umbral = np.quantile(vprev, 1 / 3)
    masc_lento = (vprev <= umbral).astype(float)

    mejor = (tab["pnl"][1] > tab["pnl"][0]).astype(int)      # 1 = largo fue mejor
    acierta = rng.random(nr) < Q
    lado_vent = np.where(acierta, mejor, 1 - mejor)
    dif = np.abs(tab["pnl"][1] - tab["pnl"][0])

    cands = {
        "C0 (todas, lado azar)": (np.ones(nr), lado_azar),
        "C_LENTO (vol baja)": (masc_lento, lado_azar),
        f"C_VENT (q={Q})": (np.ones(nr), lado_vent),
    }

    print("\n" + "=" * 100)
    print("LOS TRES CANDIDATOS - patron observado")
    print("=" * 100)
    print(f"\n   {'candidato':>24}{'operaciones':>13}{'op/sesion':>11}{'tenencia':>11}"
          f"{'abiertas':>10}{'$/sesion':>11}{'error':>9}")
    obs = {}
    for nom, (masc, lado01) in cands.items():
        v = por_sesion(tab, masc, lado01, nses)
        te, ab = tenencia(tab, masc, lado01)
        obs[nom] = v
        print(f"   {nom:>24}{int(masc.sum()):>13,}{masc.sum()/nses:>11.2f}{te:>10.0f}b"
              f"{ab:>9.1f}%{v.mean():>+11.2f}{v.std(ddof=1)/np.sqrt(nses):>9.2f}")

    ventaja_decl = (Q - 0.5) * dif.mean()
    op_ses = nr / nses
    # La NOMINAL es la esperanza sobre sorteos de 'acierta'. La REALIZADA es la de ESTE
    # sorteo, y es calculable exacta: sum (acierta - 1/2) * (mejor - peor) por operacion.
    q_real = acierta.mean()
    ventaja_real = ((acierta.astype(float) - 0.5) * dif).mean()
    print(f"\n   VENTAJA INYECTADA EN C_VENT, declarada por formula antes de medirla:")
    print(f"      E[|P&L largo - P&L corto|] = ${dif.mean():.2f} por operacion")
    print(f"      NOMINAL  = (q - 0,5) * E[|dif|] = {Q-0.5:.2f} * {dif.mean():.2f} = "
          f"${ventaja_decl:.2f}/op  ->  ${ventaja_decl*op_ses:.2f}/sesion")
    print(f"      REALIZADA en este sorteo (q observada {q_real:.4f}) = "
          f"${ventaja_real:.2f}/op  ->  ${ventaja_real*op_ses:.2f}/sesion")
    print(f"      La nominal es la ESPERANZA sobre sorteos; la realizada es la de ESTE.")
    print(f"      El control se juzga contra la REALIZADA, que es la que de verdad se puso.")

    # -------------------------------------------------------------------------------------
    print("\n" + "=" * 100)
    print("LAS DOS NULAS")
    print("   A rotacion: corre (ranuras, lados) sobre la grilla. Destruye CUANDO.")
    print("   B signo: da vuelta los lados. Destruye QUE LADO, conserva todo lo demas.")
    print("=" * 100)
    print(f"\n   {'candidato':>24}{'nula':>10}{'nula $/ses':>12}{'desvio':>9}"
          f"{'observado':>11}{'VENTAJA':>10}{'en desvios':>12}{'PISO':>10}")
    resultados = {}
    for nom, (masc, lado01) in cands.items():
        for etiqueta in ("A rotacion", "B signo"):
            rp = np.random.default_rng(SEMILLA + 101)
            medias = np.empty(NPERM)
            for i in range(NPERM):
                if etiqueta == "A rotacion":
                    k = int(rp.integers(1, nr))
                    m2, l2 = np.roll(masc, k), np.roll(lado01, k)
                else:
                    m2, l2 = masc, np.where(rp.random(nr) < 0.5, 1 - lado01, lado01)
                medias[i] = por_sesion(tab, m2, l2, nses).mean()
            mu, sd = medias.mean(), medias.std(ddof=1)
            o = obs[nom].mean()
            vent = o - mu
            resultados[(nom, etiqueta)] = (mu, sd, vent, vent / sd if sd else 0.0)
            print(f"   {nom:>24}{etiqueta:>10}{mu:>+12.2f}{sd:>9.2f}{o:>+11.2f}"
                  f"{vent:>+10.2f}{vent/sd if sd else 0:>+12.1f}{-mu:>+10.2f}")

    # -------------------------------------------------------------------------------------
    print("\n" + "=" * 100)
    print("EL CONTROL")
    print("   C0 y C_LENTO: ventaja CERO dentro del error. C_VENT: recupera la inyectada.")
    print("   Que la nula B recupere la inyectada esta casi FORZADO por construccion; la que")
    print("   informa es la nula A, y que las dos den cero en los dos sin ventaja.")
    print("=" * 100)
    ok = True
    print(f"\n   {'candidato':>24}{'nula':>10}{'ventaja':>10}{'nominal':>10}"
          f"{'REALIZADA':>11}{'desvio':>9}{'vs realiz.':>12}{'recupera':>10}"
          f"{'veredicto':>11}")
    for nom in cands:
        es_v = nom.startswith("C_VENT")
        nom_esp = ventaja_decl * op_ses if es_v else 0.0
        real_esp = ventaja_real * op_ses if es_v else 0.0
        for etiqueta in ("A rotacion", "B signo"):
            mu, sd, vent, z = resultados[(nom, etiqueta)]
            zz = (vent - real_esp) / sd if sd else 0.0
            bien = abs(zz) <= 3.0
            ok &= bien
            rec = f"{vent/real_esp*100:.0f}%" if es_v else "-"
            print(f"   {nom:>24}{etiqueta:>10}{vent:>+10.2f}{nom_esp:>+10.2f}"
                  f"{real_esp:>+11.2f}{sd:>9.2f}{zz:>+12.1f}{rec:>10}"
                  f"{('OK' if bien else 'MAL'):>11}")
    print(f"\n   CONTROL {'PASADO' if ok else 'FALLADO'}")
    print(f"   RESOLUCION del test: el desvio de la nula es +-${resultados[(f'C_VENT (q={Q})', 'B signo')][1]:.2f} "
          f"por sesion, o sea "
          f"+-{resultados[(f'C_VENT (q={Q})','B signo')][1]/(ventaja_real*op_ses)*100:.0f}% "
          f"de la ventaja inyectada.")
    print(f"   Con {nr:,} operaciones no se puede afinar mas que eso, y decirlo importa:")
    print(f"   'recupera la inyectada' significa 'dentro de esa resolucion', no 'clavada'.")

    # -------------------------------------------------------------------------------------
    print("\n" + "=" * 100)
    print("CUANTO SE CORRE LA TENENCIA BAJO LA NULA A - la limitacion que avise antes")
    print("=" * 100)
    print(f"\n   {'candidato':>24}{'tenencia obs':>14}{'tenencia rotada':>17}"
          f"{'abiertas obs':>14}{'abiertas rotada':>17}")
    rp = np.random.default_rng(SEMILLA + 55)
    for nom, (masc, lado01) in cands.items():
        te, ab = tenencia(tab, masc, lado01)
        tes, abs_ = [], []
        for _ in range(50):
            k = int(rp.integers(1, nr))
            t2, a2 = tenencia(tab, np.roll(masc, k), np.roll(lado01, k))
            tes.append(t2); abs_.append(a2)
        print(f"   {nom:>24}{te:>13.0f}b{np.mean(tes):>16.0f}b{ab:>13.1f}%"
              f"{np.mean(abs_):>16.1f}%")
    print("\n   Si la tenencia rotada se aleja de la observada, la nula A no esta apareada")
    print("   en tenencia y hay que mirar tambien la nula B, que si la conserva exacta.")
    return resultados


if __name__ == "__main__":
    main()
