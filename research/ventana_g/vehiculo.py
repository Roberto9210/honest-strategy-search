"""
VENTANA G - ES LA EVALUACION EL VEHICULO CORRECTO?

  (A) comprar evaluaciones de prop firm y operar bajo sus reglas
  (B) operar capital propio, 1 micro, sin evaluacion, sin objetivo, sin drawdown impuesto

para un participante SIN VENTAJA, en las MISMAS unidades: dolares por sesion, con marca a
mercado, sobre el MISMO flujo de operaciones.

NO GASTA CARTUCHO. K = 261. Es aritmetica sobre reglas de producto y sobre un flujo de
operaciones ya medido (entradas al azar sobre ES 1-min Databento 2016-2019). No se busca
ventaja, no se elige entre candidatas, no se declara ninguna regla de operacion. La caja
sellada (2020-01-02 -> 2026-08-19) no se toca.

COMO SE COMPARA. Se replica el bracket de forma secuencial (una posicion por vez, la abierta
al corte se marca a mercado) y se guarda CADA operacion en puntos. Ese flujo es el mismo para
A y para B. Lo unico que cambia es lo que se le pone encima:
   A: tamano N (micros), comision de la firma, objetivo, drawdown trailing EOD, dias
      calificados, cuota, pago y split. El participante solo pierde la cuota: las perdidas de
      trading son de la cuenta simulada de la firma.
   B: 1 micro, comision minorista, capital propio C con el margen como piso: cuando el saldo
      cae por debajo del margen no se puede abrir la siguiente operacion (ruina).

QUE ES MEDIDO Y QUE ES ESTRUCTURA DEL PRODUCTO. Va marcado en la salida. En resumen:
   MEDIDO (del dato): el flujo de operaciones y su marca a mercado; el exceso de
      deslizamiento medio en el stop (media_exceso.py); el sesgo de sobrepaso del marco
      (sesgo_marco.py, o = 0,0642 pt, +-7,6%); las comisiones con pagina oficial.
   ESTRUCTURA: objetivo, drawdown, cuota, pago, split (datos_crudos.md); el techo de perdida
      de A (= la cuota) y la ausencia de techo en B; el margen como piso de capital de B.
   NO MEDIDO: exchange + clearing + NFA por micro (las paginas de CME y NFA no respondieron
      el 2026-09-04), el margen de exchange de MES, el horario del margen intradia, el
      deslizamiento de entrada (se trata como cero en los dos caminos, igual que en toda la
      ventana), el costo de oportunidad del capital. Donde falta, la fila queda incompleta.

CONTROL, con condicion de falla escrita antes de correr. Con costo CERO y SIN reglas de
firma los dos caminos tienen que dar la MISMA esperanza por micro y por sesion, porque sin
friccion el envoltorio no hace nada.
   LO HARIA FALLAR: que difieran en mas de 3 errores del simulador de intentos. Querria
   decir que la comparacion tiene un termino que no viene ni de la friccion ni de las
   reglas: un error de contabilidad del simulador (recorte de sesiones, relleno de la
   matriz, vuelta circular, marca a mercado).
   PUEDE PASAR Y PUEDE FALLAR: no es una identidad. A pasa por el simulador de intentos
   (arranques en cada sesion, matriz rellena, vuelta circular, recorrido operacion por
   operacion); B pasa por la suma directa por sesion. Para probar que tiene dientes se corre
   ademas con el defecto viejo puesto a proposito -A descartando las abiertas al corte-:
   ESE TIENE QUE FALLAR. Si pasan los dos, el control no discrimina y hay que tirarlo.

EXPECTATIVA ESCRITA ANTES DE CORRER (no es prediccion sellada, es para que se vea si me
sorprendio): como en A las perdidas de trading son de la cuenta simulada y el participante
solo paga la cuota, espero que A pierda MENOS dolares por sesion que B a 1 micro, y que la
curva en esperanza no cruce. Lo que no se es cuantas sesiones dura un intento, y de eso
depende todo: si el intento muere en pocas sesiones, la cuota por sesion sube y B puede
ganar. Se mide.
"""
import numpy as np

from aritmetica import C1_POR_MINI, FIRMAS
from dolares_por_tiempo import MEDIA_EXCESO
from razon_escalas import cargar_con_sesion

PUNTO_MICRO = 5.0
O_SOBREPASO = 0.0642            # sesgo_marco.py; +-7,6% no propagado
MIN_BARRAS = 60
CELDAS = [(5, 20), (20, 10)]
SEMILLA = 20260904
H_ANIO = 250                    # sesiones: un anio (1.006 sesiones reales en 4 anios)
R_AZAR = 4                      # replicas de "lado al azar" = participantes distintos
NS = [1, 2, 3, 4, 5, 10]        # micros en A

# ------------------------------- (A) ESTRUCTURA DEL PRODUCTO -------------------------------
# Tradeify Growth 50K: la firma con mejor esperanza medida de las ocho (aritmetica.py).
# Todo de datos_crudos.md, paginas oficiales leidas 2026-09-03.
FIRMA = "Tradeify Growth (50K)"
FI = FIRMAS[FIRMA]
CUOTA = FI["precio"] + FI["activacion"]        # $83 con cupon (lista $165)
PAGO = FI["pago"] * FI["split"]                # $1.500 * 0,90 = $1.350
EVAL, FUND = FI["eval"], FI["fund"]
C1_MICRO_A = 1.82                              # micro ida y vuelta, todo incluido (tradeify)
C1_MINI_A = C1_POR_MINI                        # 5,76 el mini


def costo_A(N):
    """Comision de la firma para N micros: minis de a 10, micros sueltos el resto."""
    return C1_MINI_A * (N // 10) + C1_MICRO_A * (N % 10)


# --------------------------------- (B) LO QUE TAMBIEN CUESTA --------------------------------
# Fuentes oficiales leidas 2026-09-04. Lo que no se pudo leer es NO MEDIDO y no se estima.
#   https://ninjatrader.com/pricing/  -> comision por micro POR LADO: Free $0,39 | Monthly
#      $0,29 (+$99/mes) | Lifetime $0,09 (+$1.499 una vez). Texto: "Exchange, clearing, and
#      NFA fees apply on top of these commissions". Monto de esas tarifas: NO en la pagina.
#      Margen intradia: "$50 Margins" para Micro E-mini S&P 500. Horario en que aplica: NO.
#   https://www.tradovate.com/pricing/ -> mismas tres comisiones; margen day-trading "$25"
#      para micros estandar, MES no listado en esa pagina.
#   https://www.cmegroup.com/markets/equities/sp/micro-e-mini-sandp-500.margins.html (cargada en
#      el navegador, leida 2026-09-04 04:52 PM CT): MES 09/2026 MAINTENANCE LONG 2,608 USD,
#      MAINTENANCE SHORT 2,340 USD. Se usa el mayor.
#   cmegroup.com (tarifas de exchange/clearing): sin respuesta (ECONNRESET, timeout) en tres
#      intentos. nfa.futures.org: 403. -> NO MEDIDO.
COMISION_B_RT = {"NinjaTrader Free": 2 * 0.39,
                 "NinjaTrader Monthly (+$99/mes)": 2 * 0.29,
                 "NinjaTrader Lifetime (+$1.499)": 2 * 0.09}
EXCH_NFA_B = None                 # NO MEDIDO
REF_TODO_INCLUIDO = 1.82          # tarifa de micro de Tradeify, todo incluido: referencia superior
MARGEN_INTRADIA = 50.0            # ninjatrader.com/pricing, MES; horario en que rige: NO MEDIDO
MARGEN_EXCHANGE = 2608.0          # cmegroup.com, MES 09/2026 maintenance long, 2026-09-04
NIVELES_B = [("solo comision Free $0,78 (exch/NFA NO MEDIDO)", COMISION_B_RT["NinjaTrader Free"]),
             ("referencia todo incluido $1,82", REF_TODO_INCLUIDO)]
MARGENES = [("intradia $50", MARGEN_INTRADIA), ("exchange $2.608", MARGEN_EXCHANGE)]
CAPITALES = [50, 83, 100, 250, 500, 1000, 2000, 3000, 5000, 10000, 25000, 50000]


# ======================================= EL FLUJO =========================================
def replay(cl, hi, lo, ini, fin, T, S, exceso, modo, rng=None):
    """Replay secuencial. modo: 'largo' | 'corto' | 'azar' (moneda por operacion).
    Devuelve por operacion: sesion, puntos brutos (exceso del stop ya restado en la rama
    perdedora), abierta al corte (1/0), lado (+1/-1)."""
    ses, pts, ab, lado = [], [], [], []
    for k, (a, b) in enumerate(zip(ini, fin)):
        pos = a
        while pos < b - 1:
            if modo == "largo":
                sgn = 1.0
            elif modo == "corto":
                sgn = -1.0
            else:
                sgn = 1.0 if rng.random() < 0.5 else -1.0
            e = cl[pos]
            obj, stp = e + sgn * T, e - sgn * S
            h, l = hi[pos + 1:b], lo[pos + 1:b]
            if sgn > 0:
                to, ts = h >= obj, l <= stp
            else:
                to, ts = l <= obj, h >= stp
            algo = to | ts
            ses.append(k); lado.append(sgn)
            if not algo.any():
                pts.append(sgn * (cl[b - 1] - e)); ab.append(1)
                break
            j = int(np.argmax(algo))
            pts.append(T if (to[j] and not ts[j]) else -(S + exceso)); ab.append(0)
            pos = pos + 1 + j + 1
    return dict(ses=np.array(ses), pts=np.array(pts, float), ab=np.array(ab),
                lado=np.array(lado))


def corregir(rep, T, S):
    """Resta el sesgo de sobrepaso del marco, o*(1-2p) por operacion (sesgo_marco.py).
    verdad = replay - sesgo. Se aplica a todas las operaciones, como en el piso publicado."""
    p = S / (S + T)
    out = dict(rep)
    out["pts"] = rep["pts"] - O_SOBREPASO * (1 - 2 * p)
    return out


def matriz(rep, nses, sin_abiertas=False):
    """[nses, maxtr] de puntos por operacion, NaN de relleno AL FINAL de cada fila."""
    ses, pts = rep["ses"], rep["pts"]
    if sin_abiertas:
        keep = rep["ab"] == 0
        ses, pts = ses[keep], pts[keep]
    cnt = np.bincount(ses, minlength=nses)
    M = np.full((nses, max(1, cnt.max())), np.nan)
    order = np.argsort(ses, kind="stable")
    ses_o, pts_o = ses[order], pts[order]
    pos = np.arange(len(ses_o)) - np.repeat(np.cumsum(cnt) - cnt, cnt)
    M[ses_o, pos] = pts_o
    return M


# ==================================== EL SIMULADOR ========================================
def simular(M, s0, N, c_rt, dd, target, trail, lock_off, qual_days, qual_amt,
            max_eval, max_fund, cap=None):
    """Intentos en paralelo. El intento i arranca en la sesion s0[i] y recorre sesiones
    consecutivas, con vuelta circular al final de la serie (el P&L es aditivo por sesion:
    no hay salto de precio).
      dd=None      -> sin piso.   target=None -> sin objetivo ni etapa fondeada.
      trail='eod'  -> piso = min(max cierre - dd, lock_off), roto en tiempo real.
      trail='static' -> piso fijo en -dd (capital propio).
      cap          -> tope de sesiones por intento (array), ademas de max_eval/max_fund.
    result: 0 cayo en eval (o ruina), 1 cayo en fondeada, 2 pago, 3 tiempo en eval,
            4 tiempo en fondeada.
    Devuelve result, sesiones usadas, saldo final de trading."""
    nses, maxtr = M.shape
    valid = ~np.isnan(M)
    P = np.where(valid, np.nan_to_num(M) * PUNTO_MICRO * N - c_rt * N, 0.0)
    n = len(s0)
    bal = np.zeros(n); eod_high = np.zeros(n)
    alive = np.ones(n, bool); stage = np.zeros(n, int); quals = np.zeros(n, int)
    dstage = np.zeros(n, int); used = np.zeros(n, int); result = np.full(n, -1, int)
    for k in range(max_eval + max_fund):
        if not alive.any():
            break
        rows = (s0 + k) % nses
        Pk, Vk = P[rows], valid[rows]
        used[alive] += 1
        day_start = bal.copy()
        act = alive.copy()
        for j in range(maxtr):
            m = act & Vk[:, j]
            if not m.any():
                break
            bal[m] += Pk[m, j]
            if dd is not None:
                if trail == "eod":
                    floor = np.minimum(eod_high - dd, lock_off)
                else:
                    floor = np.full(n, -dd)
                breach = m & (bal <= floor)
                if breach.any():
                    result[breach] = np.where(stage[breach] == 0, 0, 1)
                    alive &= ~breach; act &= ~breach
        eod_high = np.maximum(eod_high, np.where(alive, bal, eod_high))
        dstage[alive] += 1
        if qual_days:
            quals += (alive & (stage == 1) & ((bal - day_start) >= qual_amt))
        if target is not None:
            st = stage.copy()
            hit = alive & (bal >= target) & ((st == 0) | (quals >= qual_days))
            promote, pay = hit & (st == 0), hit & (st == 1)
            stage[promote] = 1; bal[promote] = 0.0; eod_high[promote] = 0.0
            dstage[promote] = 0; quals[promote] = 0
            result[pay] = 2; alive &= ~pay
        tout = alive & (((stage == 0) & (dstage >= max_eval)) | ((stage == 1) & (dstage >= max_fund)))
        if cap is not None:
            tout |= alive & (used >= cap)
        result[tout] = np.where(stage[tout] == 0, 3, 4)
        alive &= ~tout
    return result, used, bal


def intento_A(M, s0, N, cap=None):
    return simular(M, s0, N, costo_A(N), EVAL["dd"], EVAL["target"], "eod", EVAL["lock_off"],
                   FUND["qual_days"], FUND["qual_amt"], EVAL["max_days"], 500, cap=cap)


def dolares_A(result):
    return -CUOTA + (result == 2) * PAGO


def carrera_A(M, s0, N, H):
    """Intentos consecutivos durante H sesiones, con caja ilimitada. El recorte por capital
    se hace despues (evaluar_A), porque un intento no cambia a los anteriores. Devuelve la
    matriz [participantes, intentos] de dolares por intento, NaN despues del ultimo."""
    n, nses = len(s0), M.shape[0]
    k = np.zeros(n, int); done = np.zeros(n, bool); hist = []
    while not done.all():
        ids = np.flatnonzero(~done)
        res, used, _ = intento_A(M, (s0[ids] + k[ids]) % nses, N, cap=H - k[ids])
        d = np.full(n, np.nan); d[ids] = dolares_A(res)
        hist.append(d)
        k[ids] += used
        done[ids] = k[ids] >= H
    return np.stack(hist, axis=1)


def evaluar_A(D, C):
    """Con capital C: se juega mientras la caja alcance para la proxima cuota. Los pagos
    reponen la caja. Devuelve resultado neto, intentos jugados, pagos, y si se quedo sin
    caja antes de que se acabaran las sesiones."""
    n, R = D.shape
    valid = ~np.isnan(D); Dz = np.nan_to_num(D)
    antes = C + np.concatenate([np.zeros((n, 1)), np.cumsum(Dz, axis=1)[:, :-1]], axis=1)
    ok = valid & (antes >= CUOTA)
    bad = ~ok
    fb = np.where(bad.any(1), bad.argmax(1), R)
    taken = np.arange(R)[None, :] < fb[:, None]
    neto = (Dz * taken).sum(1)
    ruina = fb < valid.sum(1)
    return neto, taken.sum(1), ((Dz > 0) & taken).sum(1), ruina


def rutas_B(M, c_rt, H):
    """Para cada arranque s (todas las sesiones, circular): la ruta acumulada por operacion
    de 1 micro durante H sesiones. Devuelve la lista de rutas (array por arranque)."""
    nses = M.shape[0]
    valid = ~np.isnan(M)
    P = np.where(valid, np.nan_to_num(M) * PUNTO_MICRO - c_rt, 0.0)
    flat = P[valid]                                   # orden: fila por fila = sesion por sesion
    cnt = valid.sum(1)
    start = np.concatenate([[0], np.cumsum(cnt)])     # indice del primer trade de cada sesion
    doble = np.concatenate([flat, flat])
    start2 = np.concatenate([start[:-1], start[:-1] + len(flat), [2 * len(flat)]])
    G = np.concatenate([[0.0], np.cumsum(doble)])
    rutas = []
    for s in range(nses):
        a, b = start2[s], start2[s + H]
        rutas.append(G[a + 1:b + 1] - G[a])
    return rutas


def evaluar_B(rutas, C, margen=MARGEN_INTRADIA):
    """Capital C, piso en el margen: ruina cuando el acumulado cae a -(C - margen)."""
    cap = max(C - margen, 0.0)
    fin = np.empty(len(rutas)); ruina = np.zeros(len(rutas), bool)
    for i, r in enumerate(rutas):
        if len(r) == 0:
            fin[i] = 0.0
            continue
        malo = r <= -cap
        if malo.any():
            j = int(np.argmax(malo)); fin[i] = r[j]; ruina[i] = True
        else:
            fin[i] = r[-1]
    return fin, ruina


def q(v, p):
    return float(np.percentile(v, p))


# ========================================= MAIN ===========================================
def main():
    print("=" * 100)
    print("ES LA EVALUACION EL VEHICULO CORRECTO? (A) evaluaciones contra (B) capital propio, 1 micro")
    print("NO GASTA CARTUCHO. K = 261. Participante SIN ventaja. La caja sellada no se toca.")
    print("=" * 100)

    df = cargar_con_sesion()
    cl = df["close"].to_numpy(float); hi = df["high"].to_numpy(float); lo = df["low"].to_numpy(float)
    sess = df["sess"].to_numpy(); anio = df["sess"].dt.year.to_numpy()
    corte = np.flatnonzero(sess[1:] != sess[:-1]) + 1
    ini = np.concatenate(([0], corte)); fin = np.concatenate((corte, [len(cl)]))
    keep = (fin - ini) >= MIN_BARRAS
    ini, fin = ini[keep], fin[keep]
    nses = len(ini); anio_ses = anio[ini]
    print(f"\n   ES 1-min 2016-2019, {len(cl):,} barras, {nses:,} sesiones reales, "
          f"{len(set(anio_ses.tolist()))} anios calendario (= observaciones independientes de regimen).")
    print(f"   Horizonte de comparacion: {H_ANIO} sesiones (un anio). Replicas de lado al azar: {R_AZAR}.")
    print(f"\n   (A) {FIRMA}: cuota ${CUOTA:.2f} (cupon; lista ${FI['precio_lista']:.2f}), "
          f"objetivo ${EVAL['target']:,}, DD ${EVAL['dd']:,} trailing EOD con piso en el saldo inicial,")
    print(f"       fondeada: objetivo ${FUND['target']:,}, {FUND['qual_days']} dias de >= ${FUND['qual_amt']:.0f}, "
          f"primer pago ${FI['pago']:,.0f} al {FI['split']*100:.0f}% = ${PAGO:,.0f}. Solo el PRIMER pago (cota inferior de A).")
    print(f"       objetivo confirmado al cierre de sesion; drawdown roto en tiempo real (la combinacion realista, Apex lo dice explicito).")
    print(f"       ESTRUCTURA DEL PRODUCTO, no medicion. Consistencia 35% al pago: NO modelada (solo puede bajar A).")
    print(f"   (B) 1 micro, comision minorista por ida y vuelta y margen como piso: ver bloque 4.")

    rng = np.random.default_rng(SEMILLA)
    s0_all = np.tile(np.arange(nses), R_AZAR)          # todos los arranques, por replica
    rep_id = np.repeat(np.arange(R_AZAR), nses)

    resultados = {}
    for T, S in CELDAS:
        exc = MEDIA_EXCESO[S]
        print("\n" + "#" * 100)
        print(f"CELDA {T}pt:{S}pt   (exceso medio en el stop {exc} pt, MEDIDO; sesgo del marco "
              f"{O_SOBREPASO*(1-2*S/(S+T)):+.4f} pt/op restado)")
        print("#" * 100)
        reps = {m: corregir(replay(cl, hi, lo, ini, fin, T, S, exc, m), T, S) for m in ("largo", "corto")}
        azar = [corregir(replay(cl, hi, lo, ini, fin, T, S, exc, "azar", rng), T, S) for _ in range(R_AZAR)]
        Ms = [matriz(r, nses) for r in azar]

        # ------------------------------------------------------------------ 1. B por sesion
        print("\n1) (B) 1 MICRO, DOLARES POR SESION. MEDIDO sobre el flujo. Error = entre sesiones.")
        print(f"   {'costo ida y vuelta':>48}{'lado':>10}{'$/sesion':>10}{'desvio':>9}{'error':>8}"
              f"{'en err':>8}{'op/ses':>8}{'abiertas':>10}")
        filaB = {}
        for et, c in [("costo CERO (control)", 0.0)] + [(k, v) for k, v in COMISION_B_RT.items()] + \
                     [("referencia todo incluido (Tradeify micro)", REF_TODO_INCLUIDO)]:
            for lado, r in list(reps.items()) + [("azar", None)]:
                if r is None:
                    vs = [np.bincount(a["ses"], weights=a["pts"] * PUNTO_MICRO - c, minlength=nses) for a in azar]
                    v = np.mean(vs, axis=0); ops = np.mean([len(a["ses"]) for a in azar]) / nses
                    abi = np.mean([a["ab"].mean() for a in azar]) * 100
                    # el desvio de UN participante, no del promedio de las replicas
                    sd = float(np.mean([x.std(ddof=1) for x in vs]))
                else:
                    v = np.bincount(r["ses"], weights=r["pts"] * PUNTO_MICRO - c, minlength=nses)
                    ops = len(r["ses"]) / nses; abi = r["ab"].mean() * 100; sd = v.std(ddof=1)
                se = sd / np.sqrt(nses)
                filaB[(et, lado)] = (v.mean(), sd, se, ops)
                print(f"   {et:>48}{lado:>10}{v.mean():>+10.2f}{sd:>9.2f}{se:>8.2f}{v.mean()/se:>+8.1f}"
                      f"{ops:>8.2f}{abi:>9.1f}%")
            print()

        # ------------------------------------------------------------------ 2. A por N
        print("2) (A) UN INTENTO, por tamano N (micros). Arranque en CADA sesion x 4 replicas "
              f"= {len(s0_all):,} intentos.")
        print("   $/sesion = E[$ intento] / E[sesiones intento] (tasa de renovacion: lo que cuesta por sesion repitiendo).")
        print(f"   {'N':>4}{'comision':>10}{'P(pasa ev)':>12}{'P(pago|f)':>11}{'P(pago)':>9}{'E ses':>8}"
              f"{'med ses':>9}{'E $/int':>10}{'$/sesion':>10}{'indep.':>8}{'P(tiempo)':>11}")
        tablaA = {}
        for N in NS:
            res = np.empty(len(s0_all), int); used = np.empty(len(s0_all), int)
            for r in range(R_AZAR):
                m = rep_id == r
                res[m], used[m], _ = intento_A(Ms[r], s0_all[m], N)
            fond = np.isin(res, (1, 2, 4))
            pasa = fond.mean()
            pago = (res == 2).mean()
            pago_f = (res[fond] == 2).mean() if fond.any() else float("nan")
            E = dolares_A(res).mean()
            tasa = E / used.mean()
            tablaA[N] = dict(res=res, used=used, E=E, tasa=tasa, pago=pago)
            print(f"   {N:>4}{costo_A(N):>10.2f}{pasa:>12.3f}{pago_f:>11.3f}{pago:>9.4f}{used.mean():>8.1f}"
                  f"{np.median(used):>9.0f}{E:>+10.2f}{tasa:>+10.3f}{nses/used.mean():>8.0f}"
                  f"{np.isin(res, (3, 4)).mean():>11.3f}")
        Nbest = max(NS, key=lambda n: tablaA[n]["tasa"])
        print(f"\n   'indep.' = sesiones / E[sesiones]: cuantos intentos NO solapados caben en la muestra por replica.")
        print(f"   'P(tiempo)' = intentos que se acaban por tope de dias (250 eval / 500 fondeada): cuentan como -cuota.")
        print(f"   N mas favorable para A en $/sesion: N = {Nbest}. Se usa ese para la curva (A en su mejor version).")
        tb = tablaA[Nbest]
        res, used = tb["res"], tb["used"]
        Es = used.mean()
        print(f"\n   Por anio de arranque (N={Nbest}):   [4 observaciones de regimen]")
        print(f"   {'anio':>8}{'intentos':>10}{'P(pago)':>9}{'E ses':>8}{'E $/int':>10}{'$/sesion':>10}")
        for a in sorted(set(anio_ses.tolist())):
            m = np.tile(anio_ses == a, R_AZAR)
            Ea = dolares_A(res[m]).mean()
            print(f"   {a:>8}{m.sum():>10,}{(res[m]==2).mean():>9.4f}{used[m].mean():>8.1f}{Ea:>+10.2f}"
                  f"{Ea/used[m].mean():>+10.3f}")

        # ------------------------------------------------------------------ 3. control
        print("\n3) CONTROL: costo cero y sin reglas -> A y B tienen que dar la misma esperanza por micro y sesion.")
        print("   LO HARIA FALLAR: diferencia > 3 errores. Y el defecto viejo (A sin abiertas) TIENE que fallar.")
        okc = True
        for et, sin_ab in (("A con marca a mercado (debe PASAR)", False), ("A descartando abiertas (debe FALLAR)", True)):
            difs = []
            for r in range(R_AZAR):
                Mr = matriz(azar[r], nses, sin_abiertas=sin_ab)
                m = rep_id == r
                _, u, bal = simular(Mr, s0_all[m], 1, 0.0, None, None, "static", 0.0, 0, 0.0, H_ANIO, 0)
                a_ses = bal / u                          # $/sesion por micro, simulador
                b_ses = np.bincount(azar[r]["ses"], weights=azar[r]["pts"] * PUNTO_MICRO, minlength=nses)
                difs.append((a_ses.mean(), b_ses.mean(), a_ses.std(ddof=1) / np.sqrt(len(a_ses))))
            am, bm, se = (np.mean([d[0] for d in difs]), np.mean([d[1] for d in difs]),
                          np.mean([d[2] for d in difs]) / np.sqrt(R_AZAR))
            z = (am - bm) / se if se else float("inf")
            pasa = abs(z) <= 3.0
            print(f"   {et:<40} A {am:+.4f}  B {bm:+.4f}  dif {am-bm:+.4f}  error {se:.4f}  {z:+.1f} err  "
                  f"-> {'IGUALES' if pasa else 'DIFIEREN'}")
            okc &= (pasa if not sin_ab else not pasa)
        print(f"   CONTROL {'PASADO: discrimina' if okc else 'FALLADO: NO se publica la comparacion'}")
        if not okc:
            raise SystemExit("CONTROL FALLADO")

        # ------------------------------------------------------------------ 4. costos de B
        print("\n4) LO QUE (B) TAMBIEN CUESTA. Fuente oficial o NO MEDIDO. Nada se estima.")
        print("   comision broker, micro, ida y vuelta: Free $0,78 | Monthly $0,58 (+$99/mes) | Lifetime $0,18 (+$1.499)")
        print("      fuente ninjatrader.com/pricing y tradovate.com/pricing, leidas 2026-09-04. MEDIDO.")
        print("   exchange + clearing + NFA por micro: la pagina dice que aplican 'on top'. Monto: NO MEDIDO")
        print("      (cmegroup.com sin respuesta x3, nfa.futures.org 403). La fila queda INCOMPLETA: el costo real")
        print("      de B esta ENTRE $0,78 y algo mas; la referencia superior usada es $1,82 (micro de Tradeify, todo incluido).")
        print("   margen intradia MES: $50 (ninjatrader.com/pricing). Horario en que aplica: NO MEDIDO.")
        print("   margen de mantenimiento de exchange, MES 09/2026: $2.608 largo / $2.340 corto (cmegroup.com, 2026-09-04). MEDIDO.")
        print("      La sesion replicada (17:00 -> 16:00 CT) incluye la noche: si el intradia del broker no rige de noche,")
        print("      el piso de capital de B es el de exchange. Por eso la curva lleva LOS DOS pisos.")
        print("   deslizamiento en el stop: MEDIDO (media_exceso.py), igual en A y B. Deslizamiento de entrada: cero en los dos (no medido).")
        print("   costo de oportunidad del capital C: NO MEDIDO. Crece con C y solo puede empeorar B.")
        print("   sin objetivo ni drawdown impuesto: ESTRUCTURA, no tiene precio; no obliga a operar ni a parar.")

        # ------------------------------------------------------------------ 5. techo de perdida
        print(f"\n5) EL TECHO DE PERDIDA. En A el peor caso por intento es -${CUOTA:.0f} por construccion.")
        print("   En B no hay techo: se mide la cola del acumulado de B sobre el MISMO horizonte que dura un intento.")
        print("   'valor del techo' = E[(perdida de B - cuota)+] = lo que costaria asegurar B a la altura de la cuota.")
        hA = int(round(Es))
        print(f"   horizonte = E[sesiones por intento] = {hA} sesiones; y tambien {H_ANIO}.")
        print(f"   {'horizonte':>10}{'tamano B':>10}{'costo':>8}{'media':>9}{'p50':>9}{'p5':>10}{'p1':>10}{'peor':>10}"
              f"{'P(perd>cuota)':>15}{'valor techo':>13}")
        techo = {}
        for h in (hA, H_ANIO):
            for Nb, etb in ((1, "1 micro"), (Nbest, f"{Nbest} micros")):
                for etc, c in NIVELES_B:
                    fin_h = []
                    for r in range(R_AZAR):
                        rutas = rutas_B(Ms[r], c, h)
                        fin_h.extend([x[-1] * Nb if len(x) else 0.0 for x in rutas])
                    fin_h = np.array(fin_h)
                    cuota_h = CUOTA if h == hA else CUOTA * H_ANIO / Es
                    put = np.maximum(-fin_h - cuota_h, 0).mean()
                    techo[(h, Nb, c)] = (fin_h, put)
                    print(f"   {h:>10}{etb:>10}{c:>8.2f}{fin_h.mean():>+9.0f}{q(fin_h,50):>+9.0f}{q(fin_h,5):>+10.0f}"
                          f"{q(fin_h,1):>+10.0f}{fin_h.min():>+10.0f}{(-fin_h > cuota_h).mean():>15.3f}{put:>13.2f}")
        print(f"   (en {H_ANIO} sesiones la 'cuota' de referencia es la cuota por el numero medio de intentos que caben: "
              f"${CUOTA * H_ANIO / Es:,.0f})")

        # ------------------------------------------------------------------ 6. la curva
        print(f"\n6) LA CURVA: capital propio C, horizonte {H_ANIO} sesiones. A con N={Nbest}; B con 1 micro.")
        print("   A: se juega mientras la caja alcance la cuota; los pagos reponen. B: ruina al caer al margen.")
        print("   'ruina' en A = se quedo sin caja para la proxima cuota antes de que se acaben las sesiones.")
        D = np.full((len(s0_all), 1), np.nan)
        Ds = []
        for r in range(R_AZAR):
            m = rep_id == r
            Ds.append(carrera_A(Ms[r], s0_all[m], Nbest, H_ANIO))
        R = max(d.shape[1] for d in Ds)
        D = np.full((len(s0_all), R), np.nan)
        for r in range(R_AZAR):
            m = rep_id == r
            D[m, :Ds[r].shape[1]] = Ds[r]
        rutasB = {c: [x for r in range(R_AZAR) for x in rutas_B(Ms[r], c, H_ANIO)] for _, c in NIVELES_B}
        combos = [(c, mg) for _, c in NIVELES_B for _, mg in MARGENES]
        print("   Columnas de B: costo ida y vuelta @ piso de margen. E$ = resultado medio del anio, P(ruina).")
        print(f"\n   {'C':>7}|{'A: E$':>8}{'p5':>7}{'peor':>7}{'P(ruina)':>9}{'P(gana)':>8}{'intent':>7}{'pagos':>6}|"
              + "".join(f"{f'B {c:.2f}@{mg:,.0f}':>16}{'P(ru)':>7}|" for c, mg in combos) + f"{'domina E':>10}")
        cruce = {cm: None for cm in combos}
        for C in CAPITALES:
            netoA, nat, npag, ruA = evaluar_A(D, C)
            fila = f"   {C:>7,}|{netoA.mean():>+8.0f}{q(netoA,5):>+7.0f}{netoA.min():>+7.0f}{ruA.mean():>9.3f}" \
                   f"{(netoA>0).mean():>8.3f}{nat.mean():>7.1f}{npag.mean():>6.2f}|"
            dom = []
            for c, mg in combos:
                if C < mg:
                    fila += f"{'no factible':>16}{'':>7}|"
                    dom.append("A")
                    continue
                finB, ruB = evaluar_B(rutasB[c], C, margen=mg)
                fila += f"{finB.mean():>+16.0f}{ruB.mean():>7.3f}|"
                if finB.mean() >= netoA.mean():
                    dom.append("B")
                    if cruce[(c, mg)] is None:
                        cruce[(c, mg)] = C
                else:
                    dom.append("A")
            print(fila + f"{'/'.join(dom):>10}")
        for c, mg in combos:
            print(f"   cruce en esperanza, B a ${c:.2f} con piso ${mg:,.0f}: "
                  + (f"C >= ${cruce[(c, mg)]:,}" if cruce[(c, mg)] is not None
                     else "NO CRUZA en la grilla: A pierde menos a todo capital"))
        print("   Detalle de B (p5, peor) por capital, costo $1,82, piso intradia:")
        for C in CAPITALES:
            if C < MARGEN_INTRADIA:
                continue
            finB, ruB = evaluar_B(rutasB[REF_TODO_INCLUIDO], C, margen=MARGEN_INTRADIA)
            print(f"      C={C:>7,}: E {finB.mean():+.0f}  p50 {q(finB,50):+.0f}  p5 {q(finB,5):+.0f}  "
                  f"p1 {q(finB,1):+.0f}  peor {finB.min():+.0f}  P(ruina) {ruB.mean():.3f}")

        # ------------------------------------------------------------------ 7. apuesta repetida
        print(f"\n7) LA APUESTA REPETIDA. n intentos de A, independientes (sorteo de intentos medidos), N={Nbest}.")
        print("   La esperanza es lineal en n: el signo NO cambia nunca. Lo que cambia es P(terminar arriba).")
        dA = dolares_A(res)
        print(f"   {'n':>5}{'E total':>10}{'peor':>8}{'P(arriba)':>11}{'E sesiones':>12}{'costo prestamo/ses':>20}")
        rng2 = np.random.default_rng(SEMILLA + 1)
        picoP, picoN, bajo10 = -1.0, 0, None
        for n in (1, 2, 3, 5, 8, 10, 15, 20, 30, 50, 100):
            tot = rng2.choice(dA, size=(20000, n)).sum(1)
            pa = (tot > 0).mean()
            if pa > picoP:
                picoP, picoN = pa, n
            if bajo10 is None and n > 1 and pa < 0.10:
                bajo10 = n
            print(f"   {n:>5}{tot.mean():>+10.0f}{-n*CUOTA:>+8.0f}{pa:>11.3f}{n*Es:>12.0f}{CUOTA/Es:>20.2f}")
        print(f"   P(arriba) maxima en n = {picoN} ({picoP:.3f}); baja de 10%: "
              + (f"n = {bajo10}" if bajo10 else "no en la grilla"))
        print(f"   El prestamo: ${CUOTA:.0f} por intento compran ${EVAL['dd']:,} de drawdown a {Nbest} micros durante "
              f"{Es:.1f} sesiones = ${CUOTA/Es:.2f}/sesion = {CUOTA/EVAL['dd']*100:.1f}% por intento, "
              f"{CUOTA/EVAL['dd']*H_ANIO/Es*100:.0f}% anualizado sobre los ${EVAL['dd']:,}.")

        # ------------------------------------------------------------------ 8. B mismo tamano que A
        print(f"\n8) (B') AUTOFINANCIAR LA MISMA EXPOSICION QUE A: {Nbest} micros, capital ${EVAL['dd']:,} + margen, "
              f"durante {hA} sesiones (lo que dura un intento).")
        for etc, c in NIVELES_B:
            for etm, mg in MARGENES:
                fin_h = []; ru = []
                for r in range(R_AZAR):
                    rutas = [x * Nbest for x in rutas_B(Ms[r], c, hA)]
                    f_, r_ = evaluar_B(rutas, EVAL["dd"] + mg * Nbest, margen=mg * Nbest)
                    fin_h.extend(f_); ru.extend(r_)
                fin_h = np.array(fin_h); ru = np.array(ru)
                print(f"   costo {c:.2f}, piso {etm} (capital ${EVAL['dd'] + mg * Nbest:,.0f}): "
                      f"E ${fin_h.mean():+.0f}  p5 ${q(fin_h,5):+.0f}  peor ${fin_h.min():+.0f}  "
                      f"P(ruina) {ru.mean():.3f}   contra A: E ${tb['E']:+.2f}, peor -${CUOTA:.0f}")
        resultados[(T, S)] = dict(Nbest=Nbest, tablaA=tablaA, Es=Es, cruce=cruce, techo=techo, filaB=filaB)
    return resultados


if __name__ == "__main__":
    main()
