"""
VENTANA G - los dos filtros de terreno, SEPARADOS por lo que cada uno mide.

NO GASTA CARTUCHO. K se queda en 261.

Motivo de este archivo: en BRACKET_RESULTADO.md los dos filtros se aplicaron juntos y con
el mismo peso, y eso escondia dos cosas distintas.

FILTRO DE MERCADO (deslizamiento) - NO NEGOCIABLE
    Mide el exceso por encima del stop DENTRO de la barra que lo toca
    (terreno_stop_resultado.md seccion 4). Esta condicionado a que el stop ya fue tocado:
    describe como se mueve el mercado una vez que atraviesa ese nivel. Una ventaja del
    candidato cambia CUANTAS veces te tocan, no cuanto se pasa el mercado cuando te toca.
    Por eso vale igual con ventaja o sin ella.
    Salvedad: no es invariante a la eleccion de HORA. El propio terreno (seccion 3) muestra
    que a D=8 la hora de las 23:00 CT toca 1,2% contra 24,0% de la apertura. El p95 usado
    aca es el de la poblacion mezclada.

FILTRO DE AZAR (tenencia) - CONDICIONADO AL CANDIDATO
    Mide con que frecuencia una entrada PASIVA Y SIN VENTAJA, tomada en la apertura de la
    ventana, alcanza cierta distancia. Es una propiedad de la entrada al azar, no del
    mercado. Una ventaja mueve esa frecuencia por definicion, y el terreno no puede decir
    en que direccion porque nunca se midio sobre entradas con ventaja. Frente a un
    candidato con ventaja este filtro NO rechaza: queda INDETERMINADO.

Y ADEMAS, error propio, independiente de la ventaja: en bracket.py el filtro de tenencia
uso SOLO el lado adverso (que tan seguido te tocan el stop) como si fuera la probabilidad
de que la operacion se RESUELVA. Una operacion tambien se resuelve tocando el objetivo. El
terreno tiene los dos lados y se uso uno:
    terreno_tenencia_resultado.md - lado largo = open - min(low)  -> ADVERSA de un largo
                                    lado corto = max(high) - open -> FAVORABLE de un largo
Corregirlo cambia veredictos.
"""

# terreno_stop_resultado.md seccion 2, las dos columnas, las cuatro ventanas.
TOQUE = {
    "T23": {"largo": {2: 87.3, 4: 75.5, 6: 65.0, 8: 54.9, 10: 46.2, 15: 30.4, 20: 21.4, 30: 12.2},
            "corto": {2: 90.6, 4: 81.5, 6: 70.5, 8: 60.6, 10: 51.8, 15: 34.1, 20: 22.2, 30: 10.3}},
    "RTH": {"largo": {2: 84.9, 4: 70.9, 6: 58.1, 8: 47.7, 10: 38.8, 15: 23.7, 20: 16.8, 30: 8.5},
            "corto": {2: 86.1, 4: 73.0, 6: 60.0, 8: 47.4, 10: 38.0, 15: 22.3, 20: 14.2, 30: 5.7}},
}
VENTANA_MIN = {"T23": 1380, "RTH": 390}

# terreno_stop_resultado.md seccion 4: exceso p95 sobre el stop, en puntos, dentro de la
# barra que toca. T23 lado largo donde esta medido; "23 horas juntas" para D=30.
EXCESO_P95 = {4: 2.10, 10: 2.50, 20: 3.82, 30: 10.25}
EXCESO_FUENTE = {4: "T23 largo", 10: "T23 largo", 20: "T23 largo", 30: "23h juntas"}

# Los dos cortes son ESCRITOS A MANO. Quedan aca arriba y con nombre para que se vea que
# no estan derivados de nada, que es justo el modo de fallo que este proyecto ya cazo dos
# veces (el "< 3 %" de terreno_stop y el "50,0%" del control anterior).
CORTE_DESLIZAMIENTO = 0.25   # a mano
CORTE_RESOLUCION = 50.0      # a mano

# Los cuatro de la tabla publicada mas dos con stop de 20pt, que la correccion de las dos
# barreras reabre: a 20pt el deslizamiento pasa con MARGEN (19,1%) y no al borde como a 10pt.
BRACKETS = [(5, 10), (10, 10), (20, 10), (8, 4), (5, 20), (10, 20), (20, 20)]


def cota_inf_toque(D_pt, tabla):
    """Cota INFERIOR rigurosa de P(tocar D) usando solo valores medidos: tocar un nivel
    mas lejano implica haber tocado el mas cercano, asi que P(tocar D) >= P(tocar D') para
    cualquier D' >= D medido. Devuelve (valor, D_usado, es_exacto)."""
    arriba = [d for d in tabla if d >= D_pt]
    if not arriba:
        return None, None, False
    d = min(arriba)
    return tabla[d], d, (d == D_pt)


def filtro_mercado(S_pt):
    """Deslizamiento. Propiedad del mercado, invariante a la ventaja del candidato."""
    if S_pt not in EXCESO_P95:
        return None, None, f"no medido a D={S_pt:g}pt"
    ratio = EXCESO_P95[S_pt] / S_pt
    return ratio <= CORTE_DESLIZAMIENTO, ratio, EXCESO_FUENTE[S_pt]


def filtro_azar(T_pt, S_pt, ventana, lado="largo"):
    """Resolucion de la operacion dentro de la ventana, con LAS DOS barreras.
    La operacion se resuelve si el camino toca el objetivo O toca el stop, asi que
    P(resolver) = P(A union B) >= max(P(A), P(B)).  Medido sobre entradas SIN ventaja."""
    fav_tab = TOQUE[ventana]["corto" if lado == "largo" else "largo"]
    adv_tab = TOQUE[ventana]["largo" if lado == "largo" else "corto"]
    p_fav, d_fav, ex_fav = cota_inf_toque(T_pt, fav_tab)
    p_adv, d_adv, ex_adv = cota_inf_toque(S_pt, adv_tab)
    if p_fav is None or p_adv is None:
        return None
    inf = max(p_fav, p_adv)
    sup = min(100.0, p_fav + p_adv) if (ex_fav and ex_adv) else None
    return dict(p_fav=p_fav, d_fav=d_fav, ex_fav=ex_fav,
                p_adv=p_adv, d_adv=d_adv, ex_adv=ex_adv, inf=inf, sup=sup)


def veredicto_azar(r):
    if r is None:
        return "no medido"
    if r["inf"] >= CORTE_RESOLUCION:
        return "pasa"
    if r["sup"] is not None and r["sup"] < CORTE_RESOLUCION:
        return "RECHAZA"
    return "indeterminado"


def informe():
    print("=" * 108)
    print("FILTROS DE TERRENO SEPARADOS - que descarta el mercado y que descarta el azar")
    print("NO GASTA CARTUCHO. K = 261.")
    print("=" * 108)

    print("\n1) FILTRO DE MERCADO (deslizamiento). Invariante a la ventaja. NO NEGOCIABLE.")
    print(f"   corte escrito a mano: exceso p95 <= {CORTE_DESLIZAMIENTO*100:.0f}% del stop")
    print(f"   {'stop':>8}{'exceso p95':>13}{'ratio':>9}{'veredicto':>13}   fuente")
    for S in sorted({s for _, s in BRACKETS}):
        ok, ratio, fuente = filtro_mercado(S)
        v = "no medido" if ok is None else ("pasa" if ok else "RECHAZA")
        r = "  ---  " if ratio is None else f"{ratio*100:6.1f}%"
        e = "  ---  " if S not in EXCESO_P95 else f"{EXCESO_P95[S]:6.2f}pt"
        print(f"   {S:>6.0f}pt{e:>13}{r:>9}{v:>13}   {fuente}")

    print("\n2) FILTRO DE AZAR (tenencia). Medido sobre entradas SIN ventaja.")
    print("   Frente a un candidato CON ventaja no rechaza: queda INDETERMINADO.")
    print(f"   corte escrito a mano: P(resolver en la ventana) >= {CORTE_RESOLUCION:.0f}%")
    print("   Corregido: usa LAS DOS barreras (objetivo y stop), no solo el stop.")
    for ventana in ("T23", "RTH"):
        print(f"\n   ventana {ventana} ({VENTANA_MIN[ventana]} min), entrada larga")
        print(f"   {'bracket':>14}{'P(toca obj)':>14}{'P(toca stop)':>14}"
              f"{'cota inf':>11}{'cota sup':>11}{'veredicto':>16}")
        for T, S in BRACKETS:
            r = filtro_azar(T, S, ventana)
            if r is None:
                print(f"   {f'{T}pt:{S}pt':>14}{'no medido':>14}")
                continue
            marca_f = "" if r["ex_fav"] else f" (>=D{r['d_fav']})"
            marca_a = "" if r["ex_adv"] else f" (>=D{r['d_adv']})"
            col_f = f"{r['p_fav']:.1f}%" + marca_f
            col_a = f"{r['p_adv']:.1f}%" + marca_a
            sup = "  ---  " if r["sup"] is None else f"{r['sup']:.1f}%"
            print(f"   {f'{T}pt:{S}pt':>14}{col_f:>14}{col_a:>14}"
                  f"{r['inf']:>10.1f}%{sup:>11}{veredicto_azar(r):>16}")

    print("\n" + "=" * 108)
    print("3) TABLA DE FACTIBILIDAD RECONCILIADA")
    print("=" * 108)
    print(f"   {'bracket':>14}{'mercado (no neg.)':>20}{'azar T23':>16}{'azar RTH':>16}"
          f"{'veredicto':>28}")
    for T, S in BRACKETS:
        ok_m, ratio, _ = filtro_mercado(S)
        vm = "no medido" if ok_m is None else ("pasa" if ok_m else "RECHAZA")
        v23 = veredicto_azar(filtro_azar(T, S, "T23"))
        vrth = veredicto_azar(filtro_azar(T, S, "RTH"))
        if ok_m is False:
            final = "INFACTIBLE (mercado)"
        elif v23 == "pasa" and vrth == "pasa":
            final = "pasa ambos, al borde"
        else:
            final = "sin decidir (azar)"
        print(f"   {f'{T}pt:{S}pt':>14}{vm:>20}{v23:>16}{vrth:>16}{final:>28}")

    print("\n   Recordatorio: los dos cortes (25% y 50%) son ESCRITOS A MANO, no derivados.")
    print("   Todo lo que 'pasa' arriba, pasa por uno o dos puntos porcentuales.")
    impacto()


# terreno_stop_resultado.md seccion 4: "Lo tipico es un tick: mediana 0,25 en casi todas
# las celdas". El costo del modelo (C1 = $2,50/micro) ya incluye 1 tick de deslizamiento,
# asi que la mediana YA esta contada. Lo que el modelo NO captura es la cola.
MEDIANA_EXCESO_PT = 0.25

# Acierto requerido por vara_criterio.py, N=10, Tradeify, costo $2,50 (una corrida cada uno).
REQUERIDO_TRADEIFY = {(5, 10): 69.3, (10, 10): 51.6, (20, 10): 34.1,
                      (5, 20): 80.9, (10, 20): 67.1}


def impacto():
    """El filtro de mercado normaliza el exceso contra el STOP, pero lo que paga es el
    OBJETIVO. La unidad correcta para comparar contra un criterio expresado en tasa de
    acierto es: cuantos PUNTOS de acierto agrega el deslizamiento al punto de equilibrio.
    No hace falta ningun corte escrito a mano para leer esto."""
    print("\n" + "=" * 108)
    print("4) EL DESLIZAMIENTO EN LA UNIDAD DEL CRITERIO - puntos de acierto que agrega")
    print("=" * 108)
    print("   equilibrio del bracket con exceso e:  p = (S+e)/(S+e+T)")
    print(f"   el costo del modelo ya cuenta la MEDIANA ({MEDIANA_EXCESO_PT}pt = 1 tick);")
    print("   lo NO modelado es el tramo de la mediana al p95.\n")
    print(f"   {'bracket':>12}{'moneda':>9}{'requerido':>11}{'ventaja ped.':>14}"
          f"{'p95 no modelado':>18}{'cuantas veces':>15}")
    for (T, S), req in sorted(REQUERIDO_TRADEIFY.items(), key=lambda kv: kv[1]):
        if S not in EXCESO_P95:
            continue
        moneda = 100.0 * S / (S + T)
        p_mediana = 100.0 * (S + MEDIANA_EXCESO_PT) / (S + MEDIANA_EXCESO_PT + T)
        p_p95 = 100.0 * (S + EXCESO_P95[S]) / (S + EXCESO_P95[S] + T)
        ventaja_pedida = req - moneda
        no_modelado = p_p95 - p_mediana
        veces = no_modelado / ventaja_pedida if ventaja_pedida > 0 else float("inf")
        print(f"   {f'{T}pt:{S}pt':>12}{moneda:>8.1f}%{req:>10.1f}%"
              f"{ventaja_pedida:>+13.1f}{no_modelado:>+17.1f}{veces:>14.1f}x")
    print("\n   En TODAS las celdas el tramo de deslizamiento que el modelo no captura es")
    print("   mas grande que la ventaja entera que el criterio le pide al candidato.")
    print("   El promedio del exceso -que decidiria el punto- NO ESTA MEDIDO: el terreno")
    print("   publico mediana, p95, p99 y maximo, no la media.")


if __name__ == "__main__":
    informe()
