"""VENTANA G - la cuenta MAS CHICA de cada firma que la publica.

Cuatro firmas publican precio y reglas completas de una cuenta menor a 50K.
Las otras cuatro no: BluSky y FundedNext Flex arrancan en 50K; Take Profit Trader
no expuso el objetivo del 25K; Topstep arranca en 50K.
"""
from aritmetica import sim_etapa, control, B1_POR_MICRO, C1_POR_MICRO, TAMANOS

CHICAS = {
    "Apex Intraday 25K": dict(
        precio=16.70, precio_lista=167.00, activacion=59.0,
        eval=dict(target=1500, dd=1000, trail="intraday", lock_off=0, dll=None,
                  min_days=1, max_days=21),
        fund=dict(target=1600, dd=1000, trail="intraday", lock_off=0, dll=None,
                  min_days=5, qual_days=5, qual_amt=100),
        pago=500.0, split=1.00),

    "Lucid Pro 25K": dict(
        precio=70.60, precio_lista=123.00, activacion=0.0,
        eval=dict(target=1250, dd=1000, trail="eod", lock_off=0, dll=600,
                  min_days=1, max_days=250),
        fund=dict(target=1600, dd=1000, trail="eod", lock_off=100, dll=None,
                  min_days=0, qual_days=0, qual_amt=0),
        pago=500.0, split=0.90),

    "Tradeify Growth 25K": dict(
        precio=55.00, precio_lista=109.00, activacion=0.0,
        eval=dict(target=1500, dd=1000, trail="eod", lock_off=0, dll=None,
                  min_days=1, max_days=250),
        fund=dict(target=1500, dd=1000, trail="eod", lock_off=0, dll=None,
                  min_days=5, qual_days=5, qual_amt=100),
        pago=1000.0, split=0.90),

    "MyFundedFutures Rapid 25K": dict(
        precio=72.50, precio_lista=145.00, activacion=0.0,
        eval=dict(target=1500, dd=1000, trail="eod", lock_off=0, dll=None,
                  min_days=2, max_days=250),
        fund=dict(target=1600, dd=1000, trail="intraday", lock_off=100, dll=None,
                  min_days=0, qual_days=0, qual_amt=0),
        pago=500.0, split=0.90),
}

if __name__ == "__main__":
    assert control(), "CONTROL FALLADO"
    for etiqueta, n in TAMANOS.items():
        b, c = n * B1_POR_MICRO, n * C1_POR_MICRO
        print("=" * 104)
        print(f"CUENTA MAS CHICA - posicion {etiqueta}  b=${b:.0f}  c=${c:.2f}")
        print("=" * 104)
        print(f"{'firma':<28}{'P(pasa)':>9}{'P(cobra|f)':>11}{'P(total)':>10}"
              f"{'cobra $':>9}{'cuesta $':>10}{'E $':>10}{'p equil.':>10}")
        print("-" * 104)
        filas = []
        for nombre, f in CHICAS.items():
            p_ev, _ = sim_etapa(b=b, c=c, **f["eval"])
            p_fu, _ = sim_etapa(b=b, c=c, max_days=500, **f["fund"])
            cobro = f["pago"] * f["split"]
            costo = f["precio"] + f["activacion"]
            filas.append((nombre, p_ev, p_fu, p_ev * p_fu, cobro, costo,
                          p_ev * p_fu * cobro - costo, costo / cobro))
        for r in sorted(filas, key=lambda x: -x[6]):
            print(f"{r[0]:<28}{r[1]:>9.3f}{r[2]:>11.3f}{r[3]:>10.3f}"
                  f"{r[4]:>9.0f}{r[5]:>10.2f}{r[6]:>10.2f}{r[7]:>10.3f}")
        print()
