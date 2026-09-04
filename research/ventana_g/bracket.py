"""
VENTANA G - siguiente paso. Misma maquinaria, sin datos nuevos. Solo Tradeify Growth (50K),
la firma elegida por evidencia en el paso anterior (mejor esperanza, -$29,53, vara 1,5x).

Pregunta: existe una forma de operar (contratos, objetivo en ticks, stop en ticks) que baje
la vara de 1,5?

Cambio de modelo respecto de aritmetica.py: ahi cada operacion era una moneda SIMETRICA de
amplitud b (objetivo = stop). Aca el bracket es ASIMETRICO: T ticks de objetivo, S ticks de
stop, N contratos (micros MES). Sin ventaja, la probabilidad de tocar el objetivo antes que
el stop DENTRO de una operacion es la de un paseo aleatorio sin drift entre dos barreras:

    P(gana la operacion) = S / (S + T)      (no depende de N ni de la escala en dolares)

El costo (comision + deslizamiento) se resta en las dos ramas, ganada o perdida, porque se
paga siempre. Con esto el valor esperado de UNA operacion es exactamente -costo (sin drift),
igual que en el modelo anterior, y el control se hace sobre esta ley.

Terreno (research/ventaja_futuros/terreno_stop_resultado.md y terreno_tenencia_resultado.md,
ES 2016-2019, ya commiteado, sin generar nada nuevo): frecuencia de toque de un stop de D
puntos en la ventana T23 (17:00->16:00 CT, sesion completa) y exceso de deslizamiento sobre
el stop dentro de la barra que toca (p95, T23 lado largo, y "23 horas juntas" donde T23 no
tiene el dato). Puntos ES == puntos MES en este supuesto (1 punto = 4 ticks = $5 = $1,25/tick).
"""
import numpy as np

RNG = np.random.default_rng(20260903)
TICK = 1.25          # $/tick por micro (MES)
C1 = 2.50             # $ costo por micro por operacion (igual que aritmetica.py)

# Tradeify Growth (50K) - de datos_crudos.md, sin cambios
EVAL = dict(target=3000, dd=2000, trail="eod", min_days=1, max_days=250, dll=None,
            qual_days=0, qual_amt=0.0)
FUND = dict(target=3000, dd=2000, trail="eod", min_days=5, max_days=500, dll=None,
            qual_days=5, qual_amt=150.0)
PRECIO, ACTIVACION = 83.00, 0.0
PAGO, SPLIT = 1500.0, 0.90
COBRO = PAGO * SPLIT
COSTO = PRECIO + ACTIVACION
P_EQUILIBRIO = COSTO / COBRO

# --------------------------- terreno (citas en el reporte) ---------------------------------
# terreno_stop_resultado.md, seccion 2, T23, lado largo: % de sesiones que tocan un stop de D
# puntos antes de las 16:00 CT del dia siguiente (23 horas de tenencia pasiva).
TOQUE_T23_LARGO = {2: 87.3, 4: 75.5, 6: 65.0, 8: 54.9, 10: 46.2, 15: 30.4, 20: 21.4, 30: 12.2}
# terreno_stop_resultado.md, seccion 4: exceso p95 sobre el stop, DENTRO de la barra que toca,
# en puntos. T23 lado largo donde esta medido (D=4,10,20); "23 horas juntas" (poblacion mas
# amplia, mismo estadistico) donde T23 no lo midio (D=30). D=2 no esta medido en ningun lado.
EXCESO_P95 = {4: 2.10, 10: 2.50, 20: 3.82, 30: 10.25}
EXCESO_FUENTE = {4: "T23 largo", 10: "T23 largo", 20: "T23 largo", 30: "23h juntas (T23 no lo mide)"}

# Ventanas de terreno_tenencia_resultado.md (minutos) y su tabla de toque (seccion 2 de
# terreno_stop_resultado.md). Se usan para derivar cuantas operaciones por dia son realistas
# a cada distancia de stop, EN VEZ de una constante inventada: si a D puntos el toque ya supera
# el 50% en una ventana chica, una operacion tipica se resuelve rapido y caben muchas por dia;
# si ni en las 23 horas de sesion llega al 50%, la mayoria de las veces sigue abierta al cierre
# y 1 operacion por dia ya es optimista.
VENTANAS_MIN = {"M15": 15, "H1": 60, "RTH": 390, "T23": 1380}
TOQUE_POR_VENTANA = {  # % de toque, lado largo, de terreno_stop_resultado.md seccion 2 y 3
    2: {"M15": 59.0, "H1": 74.0, "RTH": 84.9, "T23": 87.3},
    4: {"M15": 29.7, "H1": 51.6, "RTH": 70.9, "T23": 75.5},
    10: {"M15": 4.0, "H1": 16.6, "RTH": 38.8, "T23": 46.2},
    20: {"M15": 0.2, "H1": 2.9, "RTH": 16.8, "T23": 21.4},
    30: {"M15": 0.0, "H1": 0.3, "RTH": 8.5, "T23": 12.2},
}
SESION_MIN = 1380.0    # T23: la sesion completa de 23 horas, ya que Tradeify no restringe horario
TRADES_DIA_TOPE = 30   # limite de sentido comun: nadie ejecuta mas de esto en una sesion humana


def trades_por_dia(D_pt):
    """Primer D del terreno a la ventana mas chica donde el toque cruza 50%: esa es la tenencia
    tipica de una operacion a esa distancia de stop. trades/dia = sesion / tenencia tipica."""
    tabla = TOQUE_POR_VENTANA.get(D_pt)
    if tabla is None:
        return 1
    for nombre, minutos in sorted(VENTANAS_MIN.items(), key=lambda kv: kv[1]):
        if tabla[nombre] >= 50.0:
            return int(min(TRADES_DIA_TOPE, max(1, round(SESION_MIN / minutos))))
    return 1  # ni en 23 horas cruza el 50%: la operacion tipica no cierra en el dia


def sim_bracket(target, dd, trail, N, S_ticks, T_ticks, c1=C1, dll=None, min_days=0,
                 qual_days=0, qual_amt=0.0, max_days=250, npaths=150_000, lock_off=0.0,
                 trades_per_day=None, rng=None):
    """Devuelve (P_exito, trades_medios_hasta_resolver, fraccion_sin_resolver).
    trades_per_day=None -> se deriva del terreno segun S_ticks/4 (ver trades_por_dia)."""
    rng = rng or RNG
    if trades_per_day is None:
        trades_per_day = trades_por_dia(round(S_ticks / 4))
    c = c1 * N
    win = T_ticks * TICK * N - c
    loss = S_ticks * TICK * N + c
    p_win = S_ticks / (S_ticks + T_ticks)

    bal = np.zeros(npaths)
    peak = np.zeros(npaths)
    eod_high = np.zeros(npaths)
    days = np.zeros(npaths, dtype=np.int32)
    quals = np.zeros(npaths, dtype=np.int32)
    trades = np.zeros(npaths, dtype=np.int32)
    alive = np.ones(npaths, dtype=bool)
    won = np.zeros(npaths, dtype=bool)
    trades_al_final = np.zeros(npaths, dtype=np.int32)

    def resolver(mask):
        nonlocal won, alive
        ok = mask & (bal >= target) & (days >= min_days) & (quals >= qual_days)
        nuevos = ok & ~won
        trades_al_final[nuevos] = trades[nuevos]
        won |= ok
        alive &= ~ok

    for _ in range(max_days):
        if not alive.any():
            break
        days += alive.astype(np.int32)
        day_start = bal.copy()
        blocked = ~alive

        for _ in range(trades_per_day):
            act = alive & ~blocked
            if not act.any():
                break
            step = np.where(rng.random(npaths) < p_win, win, -loss)
            bal = np.where(act, bal + step, bal)
            trades += act.astype(np.int32)
            peak = np.maximum(peak, bal)

            if trail == "intraday":
                floor = np.minimum(peak - dd, lock_off)
            elif trail == "eod":
                floor = np.minimum(eod_high - dd, lock_off)
            else:
                floor = np.full(npaths, -dd)

            breach = act & (bal <= floor)
            alive &= ~breach
            resolver(act & ~breach)

            if dll is not None:
                blocked |= act & ((bal - day_start) <= -dll)

        eod_high = np.maximum(eod_high, np.where(alive, bal, eod_high))
        if qual_days:
            quals += (alive & ((bal - day_start) >= qual_amt)).astype(np.int32)
        resolver(alive.copy())

    sin_resolver = alive.mean()
    trades_medios = trades_al_final[won].mean() if won.any() else np.nan
    return won.mean(), trades_medios, sin_resolver


def horizonte_estimado(N, S_ticks, T_ticks, c1, target, dd):
    """Estimacion gruesa (Wald, sin trailing ni DLL) de cuantas operaciones hacen falta en
    promedio para que el paso aleatorio SIN VENTAJA recorra del piso al objetivo:
    E[operaciones] ~ (objetivo * drawdown) / Var(un paso). Sirve para descartar, ANTES de
    simular, las celdas cuyo paso es tan chico frente a la distancia que ningun horizonte de
    trading real las resuelve -- no es un fallo del modelo, es que esa combinacion tardaria
    siglos en decidirse."""
    c = c1 * N
    win = T_ticks * TICK * N - c
    loss = S_ticks * TICK * N + c
    p = S_ticks / (S_ticks + T_ticks)
    var_paso = p * (1 - p) * (win + loss) ** 2
    if var_paso <= 0:
        return np.inf
    return (target * dd) / var_paso


def factible_horizonte(N, S_ticks, T_ticks, c1, target, dd, max_days, trades_per_day=None,
                        margen=3.0):
    if trades_per_day is None:
        trades_per_day = trades_por_dia(round(S_ticks / 4))
    presupuesto = max_days * trades_per_day
    return horizonte_estimado(N, S_ticks, T_ticks, c1, target, dd) <= presupuesto / margen


def factible_escala(N, S_ticks, T_ticks, target):
    """Si una sola operacion ganadora ya cubre buena parte del objetivo, un trade decide todo
    y el trailing EOD lo castiga al dia siguiente (una ganancia enorme sube el piso y una sola
    perdida corriente lo rompe) -- no es la pregunta de 'cuantas operaciones hacen falta en
    promedio', es una apuesta de una sola vez. Se exige que ganar UNA operacion cubra a lo
    sumo un tercio del objetivo, para que de verdad haga falta acumular."""
    return T_ticks * TICK * N <= target / 3.0


def factible_dia(N, S_ticks, T_ticks, c1, target, dd, trades_per_day=None):
    """Con el ritmo de operaciones que da el terreno (mas alto cuanto mas chico el stop), un
    solo dia en racha ya puede mover mas que todo el objetivo o todo el drawdown -- el mismo
    problema de 'una sola jugada decide todo' pero a nivel del DIA en vez de la operacion.
    Se exige que ni el mejor dia posible ni el peor dia posible, jugando todas las operaciones
    del dia del mismo lado, superen por si solos la distancia entera al objetivo o al piso."""
    if trades_per_day is None:
        trades_per_day = trades_por_dia(round(S_ticks / 4))
    c = c1 * N
    win = T_ticks * TICK * N - c
    loss = S_ticks * TICK * N + c
    return (trades_per_day * win <= target) and (trades_per_day * loss <= dd)


def factible_calificar(N, S_ticks, T_ticks, c1=C1, trades_per_day=None):
    """La etapa fondeada exige un dia con >= qual_amt de ganancia (Tradeify Growth: $150).
    Si ni ganando las trades_per_day operaciones del dia se llega a esa cifra, la combinacion
    es geometricamente inviable -- no es una celda de la grilla, es una que no existe."""
    if trades_per_day is None:
        trades_per_day = trades_por_dia(round(S_ticks / 4))
    win_mejor_caso = T_ticks * TICK * N - c1 * N
    return trades_per_day * win_mejor_caso >= FUND["qual_amt"]


def control():
    """Con costo cero, la vara (p_equilibrio / P_total) tiene que caer a <=1,0 en TODAS las
    celdas FACTIBLES. Las que no pueden calificar el dia ni en el mejor de los casos se excluyen:
    no son un resultado del modelo, son una imposibilidad aritmetica de la regla de payout."""
    print("=" * 100)
    print("CONTROL: costo=0 -> vara debe ser <=1,0 en cada celda factible. Si no, no se publica nada.")
    print("=" * 100)
    ok = True
    excluidas = 0
    peor = (None, -1)
    for N in (1, 4, 10, 20, 40):
        for S in (8, 16, 40, 80, 120):
            for k in (0.5, 1, 2, 4):
                T = k * S
                if not factible_calificar(N, S, T, c1=0.0):
                    excluidas += 1
                    continue
                if not factible_escala(N, S, T, EVAL["target"]):
                    excluidas += 1
                    continue
                if not (factible_dia(N, S, T, 0.0, EVAL["target"], EVAL["dd"])
                        and factible_dia(N, S, T, 0.0, FUND["target"], FUND["dd"])):
                    excluidas += 1
                    continue
                if not (factible_horizonte(N, S, T, 0.0, EVAL["target"], EVAL["dd"], EVAL["max_days"])
                        and factible_horizonte(N, S, T, 0.0, FUND["target"], FUND["dd"], FUND["max_days"])):
                    excluidas += 1
                    continue
                p_ev, _, _ = sim_bracket(c1=0.0, N=N, S_ticks=S, T_ticks=T, npaths=40_000, **EVAL)
                p_fu, _, _ = sim_bracket(c1=0.0, N=N, S_ticks=S, T_ticks=T, npaths=40_000, **FUND)
                p_total0 = p_ev * p_fu
                vara0 = P_EQUILIBRIO / p_total0 if p_total0 > 0 else np.inf
                if vara0 > peor[1]:
                    peor = ((N, S, T), vara0)
                if vara0 > 1.0 + 1e-6:
                    ok = False
    print(f"  {excluidas} celdas excluidas por inviables (ni ganando 5/5 llegan a los $150/dia "
          f"que exige la etapa fondeada, aunque el costo sea cero)")
    print(f"  peor celda factible (mas vara con costo cero): N,S,T={peor[0]}  vara={peor[1]:.4f}")
    print(f"CONTROL {'PASADO' if ok else 'FALLADO'}\n")
    return ok


def filtro_terreno(S_ticks):
    """Aplica los dos filtros de terreno sobre el stop S (en ticks). Devuelve (sobrevive, motivo)."""
    Spt = S_ticks / 4.0
    d_grid = min(TOQUE_T23_LARGO.keys(), key=lambda d: abs(d - Spt))
    toque = TOQUE_T23_LARGO[d_grid]
    exceso = EXCESO_P95.get(d_grid)

    motivos = []
    filtro_b_ok = toque >= 50.0
    if not filtro_b_ok:
        motivos.append(f"tenencia excede la sesion: solo {toque:.1f}% de toque en T23 a D={d_grid}pt "
                        f"(<50%, la mayoria sigue abierta a las 23h)")

    if exceso is None:
        filtro_a_ok = None
        motivos.append(f"exceso de deslizamiento p95 NO SE DETERMINA en D={d_grid}pt (no medido)")
    else:
        ratio = exceso / d_grid
        filtro_a_ok = ratio <= 0.25
        if not filtro_a_ok:
            motivos.append(f"deslizamiento domina: exceso p95={exceso}pt es {ratio*100:.0f}% del "
                            f"stop de {d_grid}pt (>25%), fuente {EXCESO_FUENTE[d_grid]}")

    sobrevive = (filtro_a_ok is True) and filtro_b_ok
    return sobrevive, filtro_a_ok, filtro_b_ok, "; ".join(motivos) if motivos else "sobrevive ambos filtros"


if __name__ == "__main__":
    if not control():
        raise SystemExit("CONTROL FALLADO - no se publica nada")

    print("=" * 100)
    print("FILTRO DE TERRENO por distancia del stop (S en ticks -> D en puntos ES/MES)")
    print("=" * 100)
    for S in (8, 16, 40, 80, 120):
        sobrevive, fa, fb, motivo = filtro_terreno(S)
        print(f"  S={S:>3} ticks (D={S/4:.0f}pt): filtroA(deslizamiento)={fa}  "
              f"filtroB(tenencia<sesion)={fb}  -> {'SOBREVIVE' if sobrevive else 'DESCARTADA'}  ({motivo})")
    print()

    print("=" * 130)
    print(f"{'N':>3}{'S':>5}{'T':>5}{'k=T/S':>7}{'p_ev':>8}{'p_fu':>8}{'P_tot':>9}"
          f"{'trades_ev':>10}{'trades_fu':>10}{'arrastre$':>10}{'E $':>10}{'vara':>8}{'terreno':>12}")
    print("-" * 130)

    resultados = []
    inviables = 0
    for N in (1, 4, 10, 20, 40):
        for S in (8, 16, 40, 80, 120):
            sobrevive, _, _, _ = filtro_terreno(S)
            for k in (0.5, 1, 2, 4):
                T = k * S
                if not factible_calificar(N, S, T):
                    inviables += 1
                    continue
                if not factible_escala(N, S, T, EVAL["target"]):
                    inviables += 1
                    continue
                if not (factible_dia(N, S, T, C1, EVAL["target"], EVAL["dd"])
                        and factible_dia(N, S, T, C1, FUND["target"], FUND["dd"])):
                    inviables += 1
                    continue
                if not (factible_horizonte(N, S, T, C1, EVAL["target"], EVAL["dd"], EVAL["max_days"])
                        and factible_horizonte(N, S, T, C1, FUND["target"], FUND["dd"], FUND["max_days"])):
                    inviables += 1
                    continue
                p_ev, tr_ev, _ = sim_bracket(N=N, S_ticks=S, T_ticks=T, npaths=150_000, **EVAL)
                p_fu, tr_fu, _ = sim_bracket(N=N, S_ticks=S, T_ticks=T, npaths=150_000, **FUND)
                p_tot = p_ev * p_fu
                arrastre = (np.nan_to_num(tr_ev) + np.nan_to_num(tr_fu)) * C1 * N
                E = p_tot * COBRO - COSTO
                vara = P_EQUILIBRIO / p_tot if p_tot > 0 else np.inf
                resultados.append(dict(N=N, S=S, T=T, k=k, p_ev=p_ev, p_fu=p_fu, p_tot=p_tot,
                                        tr_ev=tr_ev, tr_fu=tr_fu, arrastre=arrastre, E=E,
                                        vara=vara, sobrevive=sobrevive))

    print(f"  ({inviables} celdas de la grilla excluidas: inviables por diseno, no llegan a "
          f"calificar $150/dia ni ganando siempre)\n")
    for r in sorted(resultados, key=lambda x: x["vara"])[:25]:
        print(f"{r['N']:>3}{r['S']:>5}{r['T']:>5.0f}{r['k']:>7.1f}{r['p_ev']:>8.3f}{r['p_fu']:>8.3f}"
              f"{r['p_tot']:>9.4f}{r['tr_ev']:>10.1f}{r['tr_fu']:>10.1f}{r['arrastre']:>10.0f}"
              f"{r['E']:>10.2f}{r['vara']:>8.3f}{('SI' if r['sobrevive'] else 'no'):>12}")

    print()
    mejor_global = min(resultados, key=lambda x: x["vara"])
    print(f"MEJOR VARA DE TODA LA GRILLA (sin filtrar terreno): {mejor_global['vara']:.3f}x "
          f"en N={mejor_global['N']} S={mejor_global['S']} T={mejor_global['T']:.0f} "
          f"(sobrevive terreno: {mejor_global['sobrevive']})")

    sobrevivientes = [r for r in resultados if r["sobrevive"]]
    if sobrevivientes:
        mejor_sobrev = min(sobrevivientes, key=lambda x: x["vara"])
        print(f"MEJOR VARA ENTRE LAS QUE SOBREVIVEN EL TERRENO: {mejor_sobrev['vara']:.3f}x "
              f"en N={mejor_sobrev['N']} S={mejor_sobrev['S']} T={mejor_sobrev['T']:.0f}")
    else:
        print("NINGUNA combinacion sobrevive los dos filtros de terreno a la vez.")
