"""
VENTANA G - COSTO DE ENTRAR CRUZANDO EL SPREAD (tbbo), por regimen y por epoca.

NO GASTA CARTUCHO. K = 261. Es una MEDICION de una constante de costo (como la comision o el
deslizamiento del stop), no una prueba de estrategia: no hay estadistico contra un alfa, no se elige
entre candidatas, no se declara regla de operacion. La caja sellada (diario 2020-2026) no se toca;
estos son dias sueltos de ES intradiario, seis, comprados y clasificados por tercil ex-ante en bps.

DATOS: 6 archivos tbbo de data/microestructura/ (NO en el repo). Cada operacion trae el mejor bid y
ask en ese instante (schema tbbo de Databento GLBX.MDP3).
  B (2017-2019, el terreno que juzga el juez):  bajo 2017-06-07, medio 2019-05-01, alto 2018-04-25
  A (2026, el costo de hoy):                     bajo 2026-08-26, medio 2026-09-02, altoREL 2026-09-01
El altoREL de 2026 NO es tercil alto: es el dia mas agitado posterior a la caja, todavia medio por
los cortes historicos. El regimen alto en 2026 no existe fuera de la caja. Marcado como extrapolacion.

QUE SE MIDE.
  spread cotizado  = ask - bid (en el instante de cada operacion).
  medio-spread efectivo = |precio - punto medio|, con punto medio = (bid+ask)/2: lo que paga de
                    verdad quien cruza para entrar, relativo al medio. Es el DESLIZAMIENTO DE ENTRADA
                    que el juez trata hoy como CERO.
Para un tamano de 1-2 contratos (lo que Roberto puede operar) no se camina el libro -el tope de ES
tiene cientos de contratos-, asi que el costo de cruzar es el medio-spread cotizado; el impacto de
mercado es despreciable y se dice.

CONTROL, con condicion de falla escrita: el spread MEDIANO de ES tiene que dar 1 tick (0,25 pt) en
los seis dias. Es el contrato mas liquido del mundo. LO HARIA FALLAR: una mediana distinta de 1 tick
en cualquiera de los seis -> hay un error en la lectura de los datos, no en el mercado.

SALIDA: escribe deslizamiento_entrada.json con el medio-spread efectivo medio por tercil (de B,
2017-2019, que es el terreno que juzga el juez) para que juez.py lo cargue.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np

import databento as db

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "data" / "microestructura"
TICK = 0.25
PUNTO = {"ES": 50.0, "MES": 5.0}
ARCHIVOS = [
    ("B", "bajo", "2017-06-07", "tbbo_ESn0_B_bajo_2017-06-07.dbn.zst"),
    ("B", "medio", "2019-05-01", "tbbo_ESn0_B_medio_2019-05-01.dbn.zst"),
    ("B", "alto", "2018-04-25", "tbbo_ESn0_B_alto_2018-04-25.dbn.zst"),
    ("A", "bajo", "2026-08-26", "tbbo_ESn0_A_bajo_2026-08-26.dbn.zst"),
    ("A", "medio", "2026-09-02", "tbbo_ESn0_A_medio_2026-09-02.dbn.zst"),
    ("A", "altoREL", "2026-09-01", "tbbo_ESn0_A_altoREL_2026-09-01.dbn.zst"),
]
TERCIL_ID = {"bajo": 0, "medio": 1, "alto": 2, "altoREL": 2}


def medir_archivo(path):
    df = db.DBNStore.from_file(str(path)).to_df(price_type="float", pretty_ts=True)
    bid, ask, price = df["bid_px_00"].to_numpy(), df["ask_px_00"].to_numpy(), df["price"].to_numpy()
    ok = (bid > 0) & (ask > 0) & (ask >= bid) & np.isfinite(price)
    bid, ask, price = bid[ok], ask[ok], price[ok]
    quoted = ask - bid
    mid = (bid + ask) / 2.0
    eff_half = np.abs(price - mid)
    return dict(n=int(ok.sum()), n_bruto=len(df),
                q_med=float(np.median(quoted)), q_mean=float(quoted.mean()),
                q_p95=float(np.quantile(quoted, 0.95)), q_max=float(quoted.max()),
                eh_mean=float(eff_half.mean()), eh_med=float(np.median(eff_half)),
                eh_p95=float(np.quantile(eff_half, 0.95)))


def main():
    print("=" * 98)
    print("COSTO DE ENTRAR CRUZANDO EL SPREAD (tbbo), por regimen y por epoca")
    print("NO GASTA CARTUCHO. K = 261. La caja sellada no se toca.")
    print("=" * 98)
    res = {}
    print(f"\n(a) SPREAD POR DIA. 1 tick = {TICK} pt. $/op = medio-spread efectivo * valor del punto (una entrada).")
    print(f"   {'epoca':>6}{'tercil':>9}{'fecha':>12}{'operac.':>10}{'spread med':>12}{'spread medio':>13}"
          f"{'p95':>7}{'1/2sp ef':>9}{'$/op MES':>9}{'$/op ES':>9}")
    ctrl_ok = True
    for epoca, tercil, fecha, fn in ARCHIVOS:
        p = DIR / fn
        if not p.exists():
            print(f"   {epoca:>6}{tercil:>9}{fecha:>12}   FALTA {fn}")
            continue
        r = medir_archivo(p)
        res[(epoca, tercil)] = r
        med_tk = r["q_med"] / TICK
        if abs(r["q_med"] - TICK) > 1e-9:
            ctrl_ok = False
        print(f"   {epoca:>6}{tercil:>9}{fecha:>12}{r['n']:>10,}{med_tk:>10.2f}tk"
              f"{r['q_mean']/TICK:>11.3f}tk{r['q_p95']/TICK:>6.1f}tk{r['eh_mean']/TICK:>8.3f}tk"
              f"{r['eh_mean']*PUNTO['MES']:>9.3f}{r['eh_mean']*PUNTO['ES']:>9.2f}")
    print(f"\n   CONTROL (spread mediano = 1 tick en los seis dias): {'PASADO' if ctrl_ok else 'FALLADO'}")
    if not ctrl_ok:
        raise SystemExit("CONTROL FALLADO - error en la lectura, no en el mercado")

    print("\n(b) CAMBIO EL COSTO EN DIEZ ANIOS? Emparejado por tercil de bps (para eso se eligieron).")
    print(f"   {'tercil':>9}{'2017-2019':>22}{'2026':>22}{'cambio medio-spread ef.':>26}")
    for tercil, a26 in (("bajo", "bajo"), ("medio", "medio"), ("alto", "altoREL")):
        b = res.get(("B", tercil)); a = res.get(("A", a26))
        if not (b and a):
            continue
        nota = "" if a26 != "altoREL" else "  (2026 NO es alto: extrapolacion)"
        cambio = (a["eh_mean"] - b["eh_mean"]) / b["eh_mean"] * 100
        print(f"   {tercil:>9}{b['eh_mean']/TICK:>10.3f}tk ${b['eh_mean']*PUNTO['ES']:>6.2f}"
              f"{a['eh_mean']/TICK:>13.3f}tk ${a['eh_mean']*PUNTO['ES']:>6.2f}{cambio:>+18.1f}%{nota}")
    print("   'cambio' > 0 = mas caro hoy. Emparejar por tercil evita comparar un dia calmo de una")
    print("   epoca contra uno agitado de la otra, que seria mezclar regimen con epoca.")

    # deslizamiento de entrada por tercil, de B (2017-2019), para el juez
    slip = {TERCIL_ID[t]: round(res[("B", t)]["eh_mean"], 4) for t in ("bajo", "medio", "alto")}
    out = dict(fuente="microestructura_tbbo.py, tbbo ES GLBX.MDP3, B 2017-2019",
               unidad="puntos (medio-spread efectivo medio)", por_tercil_exante_bps=slip,
               nota="deslizamiento de ENTRADA: costo de cruzar el spread una vez al entrar, "
                    "relativo al punto medio. Aplicar por operacion segun el tercil de la sesion.")
    with open(Path(__file__).resolve().parent / "deslizamiento_entrada.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"\n   Deslizamiento de entrada por tercil (B 2017-2019), en puntos: {slip}")
    print(f"   -> escrito en deslizamiento_entrada.json para que juez.py lo cargue.")
    print("\n   LIMITACIONES: (1) media ponderada por operacion, no por tiempo ni por las entradas del")
    print("   candidato; el spread es casi siempre 1 tick, asi que pesa poco, pero se dice. (2) el")
    print("   regimen alto de 2026 no existe fuera de la caja: la fila alto compara 2018 contra un dia")
    print("   medio de 2026, no es un emparejamiento. (3) 1-2 contratos no caminan el libro; para")
    print("   tamanos grandes habria impacto de mercado que esto NO mide.")


if __name__ == "__main__":
    main()
