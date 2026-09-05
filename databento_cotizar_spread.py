"""COTIZACION SOLAMENTE - no se compra ni se descarga nada.

VENTANA G. K = 261. No gasta cartucho: es compra de datos (fase 1, cotizar), no medicion.

Cotiza UN dia de mercado normal de ES (contrato mas cercano) en GLBX.MDP3 en dos schemas:
  tbbo  - cada operacion con el mejor precio de compra y venta en ese instante (mide el spread)
  mbo   - libro completo con cola (contestaria si se puede entrar pasivo sin cruzar el spread)

Solo usa endpoints de METADATOS, que Databento no factura:
  metadata.get_dataset_range, list_unit_prices, get_cost, get_billable_size, get_record_count.
NUNCA llama a timeseries.get_range ni a batch.submit_job. Si alguien agrega esa llamada, esta
haciendo otra cosa que lo que dice el nombre del archivo.

La clave se lee de la variable de entorno DATABENTO_API_KEY (o de ./.env, que esta en .gitignore)
y NO se imprime nunca. El repo es publico.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")
key = os.environ.get("DATABENTO_API_KEY")
if not key:
    print("DATABENTO_API_KEY no esta definida (env o .env). No se hace ninguna llamada.")
    sys.exit(2)

import databento as db  # noqa: E402

DATASET = "GLBX.MDP3"
# Dia propuesto: 2026-09-02 (miercoles). Fuera de la caja sellada (que termina 2026-08-19), actual,
# sin feriado (Labor Day es 2026-09-07), sin roll (ESU6 vence 2026-09-18; el roll es ~2026-09-10),
# sin vencimiento de opciones. Alternativa si no esta disponible: 2026-08-26 (miercoles).
DIA = os.environ.get("COTIZAR_DIA", "2026-09-02")
SIMBOLOS = [("ESU6", "raw_symbol"), ("ES.n.0", "continuous")]
# Sesion CME completa del dia DIA: 17:00 CT del dia anterior -> 16:00 CT (CDT = UTC-5).
# RTH: 08:30 -> 15:15 CT.
import datetime as dt  # noqa: E402

d = dt.date.fromisoformat(DIA)
prev = d - dt.timedelta(days=1)
nxt = d + dt.timedelta(days=1)
VENTANAS = {
    "sesion completa (17:00 CT ant. -> 16:00 CT, 23 h)": (f"{prev}T22:00:00Z", f"{d}T21:00:00Z"),
    "solo RTH (08:30 -> 15:15 CT)": (f"{d}T13:30:00Z", f"{d}T20:15:00Z"),
    # mbo: el libro se reconstruye desde un snapshot sintetico que Databento pone a las 00:00 UTC.
    # Un rango que no arranque ahi no tiene el estado inicial del libro (BentoWarning). Para mbo
    # la ventana usable es el dia UTC entero; cubre toda la RTH y termina despues del cierre CME.
    "dia UTC 00:00 -> 24:00 (incluye el snapshot del libro para mbo)": (f"{d}T00:00:00Z", f"{nxt}T00:00:00Z"),
}
SCHEMAS = ["tbbo", "mbo"]

client = db.Historical(key)
print(f"COTIZACION (sin descargar) - dataset {DATASET}, dia {DIA}")
rango = client.metadata.get_dataset_range(DATASET)
print(f"rango disponible del dataset: {rango}")
print()
try:
    precios = client.metadata.list_unit_prices(DATASET)
    print("precio unitario por schema (USD por GB, segun Databento):")
    for fila in precios:
        modo = fila.get("mode", "?")
        for sch, usd in sorted(fila.get("unit_prices", {}).items()):
            if sch in SCHEMAS or sch == "ohlcv-1m":
                print(f"   {modo:<12} {sch:<10} {usd:>8.2f}")
except Exception as e:  # noqa: BLE001
    print(f"(list_unit_prices no disponible: {e!r})")
print()

print(f"{'schema':<7}{'simbolo':<9}{'ventana':<50}{'USD':>9}{'MB fact.':>10}{'registros':>13}")
resumen = {}
for sch in SCHEMAS:
    for sym, stype in SIMBOLOS:
        for nom, (ini, fin) in VENTANAS.items():
            kw = dict(dataset=DATASET, symbols=[sym], schema=sch, start=ini, end=fin, stype_in=stype)
            try:
                cost = client.metadata.get_cost(**kw)
                size = client.metadata.get_billable_size(**kw)
                n = client.metadata.get_record_count(**kw)
                print(f"{sch:<7}{sym:<9}{nom:<50}{cost:>9.2f}{size/1e6:>10.1f}{n:>13,}")
                resumen[(sch, sym, nom)] = (cost, size, n)
            except Exception as e:  # noqa: BLE001
                print(f"{sch:<7}{sym:<9}{nom:<50}   ERROR {e!r}")
print()
print("Nada de lo anterior se factura: son endpoints de metadatos. NO se descargo nada.")
print("Credito declarado por Roberto: USD 107 (de 125). No se renueva.")
