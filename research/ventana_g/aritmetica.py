"""
VENTANA G - Aritmetica de la evaluacion de cuentas de fondeo de futuros.

Modelo: operador SIN NINGUNA VENTAJA. Cada operacion es una moneda simetrica de amplitud b
dolares, menos un costo fijo c (comision + deslizamiento). Esperanza por operacion = -c,
varianza = b^2. La probabilidad efectiva de ganar queda apenas por debajo de 0,5.

Caminata con dos barreras absorbentes: el objetivo de ganancia y el drawdown maximo, con el
tipo de drawdown (trailing intradia / trailing al cierre / piso fijo) simulado explicitamente,
mas el limite de perdida diario y los dias minimos de operacion.

Todas las cifras de reglas vienen de research/ventana_g/datos_crudos.md (paginas oficiales,
leidas 2026-09-03). Los parametros de MERCADO (b, c) son supuestos declarados, no datos scrapeados.
"""
import numpy as np

RNG = np.random.default_rng(20260903)
NPATHS = 200_000
TRADES_PER_DAY = 5

# ---------------------------------------------------------------------------
# Supuesto de costo por operacion (NO es un dato de las firmas, es del modelo).
# Micro E-mini S&P (MES): valor del punto $5, tick $1,25.
# Comision ida y vuelta ~ $1,25 + deslizamiento de 1 tick $1,25  ->  c1 = $2,50 por micro.
# Amplitud de la operacion: stop/objetivo de 10 puntos -> b1 = 10 * $5 = $50 por micro.
# ---------------------------------------------------------------------------
# MEDIDO (2026-09-04), deuda saldada. Pagina oficial de Tradeify:
#   https://help.tradeify.co/en/articles/10468315-trading-commission-fees
# Costo IDA Y VUELTA por contrato, y la pagina declara que YA INCLUYE exchange fees, NFA
# fees, clearing fees y comision: es el costo total de ejecucion, no solo la comision.
#   micros (MES, MNQ, MYM, M2K): $1,82 por contrato ida y vuelta
#   minis  (ES, NQ, YM, RTY):    $5,76 por contrato ida y vuelta
# OJO: esto NO incluye deslizamiento. El deslizamiento esta medido aparte y se aplica solo
# a la rama perdedora (media_exceso.py), que es donde ocurre.
C1_POR_MICRO = 1.82
C1_POR_MINI = 5.76
# Un mini equivale exactamente a 10 micros de exposicion, y Tradeify lo confirma en el
# limite de contratos del 50K: "4 minis/40 micros" (datos_crudos.md). Por micro-equivalente
# el mini cuesta $0,576, un 68% menos que operar 10 micros sueltos.
C1_POR_MICRO_VIA_MINI = C1_POR_MINI / 10.0
B1_POR_MICRO = 50.0

TAMANOS = {"5 micros": 5, "10 micros (1 mini)": 10, "20 micros (2 minis)": 20}


def sim_etapa(target, dd, trail, b, c, lock_off=0.0, dll=None, min_days=0,
              qual_days=0, qual_amt=0.0, max_days=250, npaths=NPATHS, rng=None):
    """Devuelve (prob_exito, saldo_final_medio_de_los_exitosos, dias_medianos).

    target   : ganancia (en $) sobre el saldo inicial que hay que alcanzar
    dd       : distancia del drawdown maximo (en $)
    trail    : 'intraday' | 'eod' | 'static'
    lock_off : el piso deja de subir cuando llega a saldo_inicial + lock_off
    dll      : limite de perdida diario (None = no hay). Bloquea el dia, no reprueba.
    min_days : dias minimos de operacion
    qual_days/qual_amt : hacen falta qual_days dias con ganancia >= qual_amt
    """
    rng = rng or RNG
    bal = np.zeros(npaths)
    peak = np.zeros(npaths)      # pico de saldo (para trailing intradia)
    eod_high = np.zeros(npaths)  # maximo de cierres diarios (para trailing EOD)
    days = np.zeros(npaths, dtype=np.int32)
    quals = np.zeros(npaths, dtype=np.int32)
    alive = np.ones(npaths, dtype=bool)
    won = np.zeros(npaths, dtype=bool)
    dias_al_exito = np.full(npaths, -1, dtype=np.int32)

    def resolver(act_mask):
        """El objetivo se evalua con la MISMA granularidad que la ruptura: por operacion.
        Si no, el camino que sube al objetivo y despues baja al piso dentro del mismo dia
        se contaria como fracaso, y el control con U=D dejaria de dar 50%."""
        nonlocal won, alive
        ok = act_mask & (bal >= target) & (days >= min_days) & (quals >= qual_days)
        nuevos = ok & ~won
        dias_al_exito[nuevos] = days[nuevos]
        won |= ok
        alive &= ~ok

    for _ in range(max_days):
        if not alive.any():
            break
        days += alive.astype(np.int32)   # el dia en curso ya cuenta como dia operado
        day_start = bal.copy()
        blocked = ~alive  # bloqueado hoy (muerto o toco el DLL)

        for _ in range(TRADES_PER_DAY):
            act = alive & ~blocked
            if not act.any():
                break
            step = np.where(rng.random(npaths) < 0.5, b, -b) - c
            bal = np.where(act, bal + step, bal)
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
    return won.mean(), sin_resolver


def cerrada(target, dd, b, c):
    """Forma cerrada (difusion) con piso FIJO. Sirve de contraste y para el control."""
    k = 2 * c / b**2
    if k == 0:
        return dd / (target + dd)
    return (1 - np.exp(-k * dd)) / (np.exp(k * target) - np.exp(-k * dd))


# ===========================================================================
# CONTROL OBLIGATORIO: objetivo = drawdown, costo cero, ventaja cero -> ~50%
# ===========================================================================
def control():
    print("=" * 78)
    print("CONTROL: objetivo == drawdown, costo CERO, ventaja CERO, piso FIJO")
    print("Debe dar ~50%. Si no, no se publica ninguna cifra.")
    print("=" * 78)
    ok = True
    for U in (1000.0, 2000.0, 3000.0):
        for b in (100.0, 250.0, 500.0):
            p_sim, sr = sim_etapa(U, U, "static", b, 0.0, npaths=100_000, max_days=4000)
            p_cf = cerrada(U, U, b, 0.0)
            flag = "OK " if abs(p_sim - 0.5) < 0.01 else "MAL"
            if abs(p_sim - 0.5) >= 0.01:
                ok = False
            print(f"  {flag} U=D=${U:>6.0f}  b=${b:>5.0f}  simulacion={p_sim:.4f}  "
                  f"cerrada={p_cf:.4f}  sin resolver={sr:.4f}")
    print(f"\nCONTROL {'PASADO' if ok else 'FALLADO'}\n")
    return ok


# ===========================================================================
# LAS FIRMAS. Solo reglas leidas en paginas oficiales (ver datos_crudos.md).
# Cuenta de 50K en todos los casos: es el unico tamano que las 8 ofrecen.
# 'precio' = el mas barato efectivamente publicado en la pagina (cupon incluido si la
#            pagina lo muestra); 'precio_lista' = sin cupon.
# ===========================================================================
FIRMAS = {
    "Apex (Intraday 50K)": dict(
        precio=24.90, precio_lista=249.00, activacion=59.0, reset=None,
        eval=dict(target=3000, dd=2000, trail="intraday", lock_off=0, dll=None,
                  min_days=1, max_days=21),
        fund=dict(target=2600, dd=2000, trail="intraday", lock_off=0, dll=None,
                  min_days=5, qual_days=5, qual_amt=200),
        pago=500.0, split=1.00),

    "Topstep (50K)": dict(
        precio=49.00, precio_lista=49.00, activacion=149.0, reset=49.0,
        eval=dict(target=3000, dd=2000, trail="eod", lock_off=0, dll=None,
                  min_days=0, max_days=21),
        fund=dict(target=1500, dd=2000, trail="eod", lock_off=0, dll=None,
                  min_days=5, qual_days=5, qual_amt=150),
        pago=750.0, split=0.90),

    "Lucid Pro (50K)": dict(
        precio=115.40, precio_lista=192.00, activacion=0.0, reset=115.0,
        eval=dict(target=3000, dd=2000, trail="eod", lock_off=0, dll=1200,
                  min_days=1, max_days=250),
        fund=dict(target=2600, dd=2000, trail="eod", lock_off=100, dll=None,
                  min_days=0, qual_days=0, qual_amt=0),
        pago=500.0, split=0.90),

    "FundedNext Flex (50K)": dict(
        precio=69.99, precio_lista=133.99, activacion=0.0, reset=77.99,
        eval=dict(target=2500, dd=1500, trail="eod", lock_off=0, dll=None,
                  min_days=0, max_days=250),
        fund=dict(target=1000, dd=1500, trail="eod", lock_off=0, dll=None,
                  min_days=5, qual_days=5, qual_amt=200),
        pago=500.0, split=0.95),

    "BluSky Launch (50K)": dict(
        precio=59.00, precio_lista=59.00, activacion=99.0, reset=49.0,
        eval=dict(target=3000, dd=2000, trail="eod", lock_off=0, dll=None,
                  min_days=2, max_days=21),
        fund=dict(target=3000, dd=2000, trail="eod", lock_off=0, dll=None,
                  min_days=0, qual_days=0, qual_amt=0),   # FASE BUFFER, no es el pago
        pago=250.0, split=0.90, nota="cadena cortada: el DD estatico de la Sim Funded no se determina"),

    "Take Profit Trader (50K)": dict(
        precio=170.00, precio_lista=170.00, activacion=130.0, reset=None,
        eval=dict(target=3000, dd=2000, trail="eod", lock_off=0, dll=None,
                  min_days=3, max_days=21),
        fund=dict(target=2500, dd=2000, trail="intraday", lock_off=0, dll=None,
                  min_days=0, qual_days=0, qual_amt=0),
        pago=500.0, split=0.80),

    "Tradeify Growth (50K)": dict(
        precio=83.00, precio_lista=165.00, activacion=0.0, reset=109.0,
        eval=dict(target=3000, dd=2000, trail="eod", lock_off=0, dll=None,
                  min_days=1, max_days=250),
        fund=dict(target=3000, dd=2000, trail="eod", lock_off=0, dll=None,
                  min_days=5, qual_days=5, qual_amt=150),
        pago=1500.0, split=0.90),

    "MyFundedFutures Rapid (50K)": dict(
        precio=104.50, precio_lista=209.00, activacion=0.0, reset=None,
        eval=dict(target=3000, dd=2000, trail="eod", lock_off=0, dll=None,
                  min_days=2, max_days=250),
        fund=dict(target=2600, dd=2000, trail="intraday", lock_off=100, dll=None,
                  min_days=0, qual_days=0, qual_amt=0),
        pago=500.0, split=0.90),
}


def corrida(n_micros):
    b = n_micros * B1_POR_MICRO
    c = n_micros * C1_POR_MICRO
    filas = []
    for nombre, f in FIRMAS.items():
        p_ev, sr_ev = sim_etapa(b=b, c=c, **f["eval"])
        p_fu, sr_fu = sim_etapa(b=b, c=c, max_days=500, **f["fund"])
        p_tot = p_ev * p_fu
        cobro = f["pago"] * f["split"]
        costo = f["precio"] + f["activacion"]
        esperanza = p_tot * cobro - costo
        p_equilibrio = costo / cobro
        filas.append(dict(firma=nombre, p_ev=p_ev, p_fu=p_fu, p_tot=p_tot,
                          cobro=cobro, costo=costo, E=esperanza, p_eq=p_equilibrio,
                          sr_ev=sr_ev, sr_fu=sr_fu, nota=f.get("nota", "")))
    return b, c, filas


if __name__ == "__main__":
    if not control():
        raise SystemExit("CONTROL FALLADO - no se publica nada")

    for etiqueta, n in TAMANOS.items():
        b, c, filas = corrida(n)
        p_eff = 0.5 - c / (2 * b)
        print("=" * 108)
        print(f"TAMANO DE POSICION: {etiqueta}   b=${b:.0f}/operacion   c=${c:.2f}/operacion   "
              f"p efectiva={p_eff:.4f}")
        print("=" * 108)
        print(f"{'firma':<30}{'P(pasa)':>9}{'P(cobra|f)':>11}{'P(total)':>10}"
              f"{'cobra $':>9}{'cuesta $':>10}{'E $':>10}{'p equil.':>10}")
        print("-" * 108)
        for r in sorted(filas, key=lambda x: -x["E"]):
            print(f"{r['firma']:<30}{r['p_ev']:>9.3f}{r['p_fu']:>11.3f}{r['p_tot']:>10.3f}"
                  f"{r['cobro']:>9.0f}{r['costo']:>10.2f}{r['E']:>10.2f}{r['p_eq']:>10.3f}")
        print()

    # Sensibilidad al supuesto de costo, con 10 micros
    print("=" * 78)
    print("SENSIBILIDAD AL COSTO SUPUESTO (10 micros, b=$500), eval de 50K generica U=3000 D=2000 EOD")
    print("=" * 78)
    for c1 in (1.0, 1.5, 2.5, 4.0, 6.0):
        c = 10 * c1
        p, _ = sim_etapa(3000, 2000, "eod", 500.0, c, npaths=100_000, max_days=500)
        print(f"  costo ${c1:.2f}/micro -> c=${c:.0f}/operacion  P(pasa la eval)={p:.4f}")
