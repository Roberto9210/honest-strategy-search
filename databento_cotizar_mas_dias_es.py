"""PIEZA 5 - COTIZACION (SIN COMPRAR) DE DIAS ADICIONALES DE ORDER FLOW DEL ES.

VENTANA G. K = 261. No gasta cartucho. NO DESCARGA NADA: este script no tiene modo --comprar.

POR QUE EXISTE, Y ES UNA CORRECCION A LA PREMISA DE LA PIEZA 5.
La Pieza 5 dice "compra el resto del paquete de microestructura que ya empezamos, cotiza $0,87".
Dos cosas no cierran y hay que decirlas antes de gastar un centavo:

  1. EL PAQUETE DE MICROESTRUCTURA YA ESTA COMPLETO. databento_plan_compra.json tiene 13 items y
     los 13 estan en disco (6 dias x 2 esquemas + 1 auxiliar, 781 MB). No hay "resto".
  2. LOS $0,87 SON DE OTRA COSA. Esa cotizacion es el paquete de DIVISAS (L08 + L07 + tbbo de 6E +
     diarios), de databento_cotizar_divisas.py. Comprarlo no agrega NI UN dia de order flow del ES,
     asi que no mueve la Pieza 3b ni un milimetro. Serviria a la VENTANA L y a la calibracion de
     6E, que son cosas buenas, pero no la que la Pieza 5 dice querer.

Lo que SI aumentaria los dias para medir seleccion adversa condicionada al desbalance es comprar
mas dias de ES en mbo (y tbbo al lado, que es barato y sirve de cotejo). Eso no estaba cotizado.
Aca esta el precio por dia, medido y no estimado, para que Roberto decida con numero.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")
key = os.environ.get("DATABENTO_API_KEY")
if not key:
    print("DATABENTO_API_KEY no esta definida (env o .env). No se hace ninguna llamada.")
    sys.exit(2)

import databento as db  # noqa: E402

DATASET = "GLBX.MDP3"
SIMBOLO = "ES.n.0"
CREDITO = 98.92
TOPE_ITEM = 3.00
TOPE_TOTAL = 25.00
client = db.Historical(key)

# Tres dias por tercil, distintos de los seis ya comprados, repartidos por regimen y por ano.
# La eleccion fina de fechas la hace databento_seleccion_dias.py; aca se cotiza una MUESTRA para
# sacar el precio por dia, que es lo que decide.
MUESTRA = [
    ("2017-08-10", "candidato bajo"),
    ("2018-02-08", "candidato alto"),
    ("2019-01-03", "candidato alto"),
    ("2019-10-02", "candidato medio"),
]
YA_COMPRADOS = 6            # dias con mbo+tbbo en disco


def costo(schema, ini, fin):
    kw = dict(dataset=DATASET, symbols=[SIMBOLO], schema=schema, start=ini, end=fin,
              stype_in="continuous")
    return (client.metadata.get_cost(**kw), client.metadata.get_billable_size(**kw) / 1e6,
            client.metadata.get_record_count(**kw))


def main():
    print("=" * 100)
    print("PIEZA 5 - DIAS ADICIONALES DE ORDER FLOW DEL ES: COTIZACION. NO SE DESCARGA NADA.")
    print("K = 261, no gasta cartucho. Dinero comprometido en esta corrida: $0.")
    print("=" * 100)
    print(f"\n   Ya en disco: {YA_COMPRADOS} dias con mbo + tbbo (13 archivos, 781 MB). "
          f"El plan de compra esta COMPLETO.")
    print(f"   Credito declarado restante: USD {CREDITO:.2f} (calculado, NO leido de la cuenta).")
    print(f"\n   {'fecha':<13}{'para que':<18}{'mbo USD':>10}{'tbbo USD':>10}{'dia USD':>10}"
          f"{'MB':>9}{'registros':>13}")
    tot = 0.0
    for f, para in MUESTRA:
        ini, fin = f"{f}T00:00:00", f"{f}T23:59:59"
        cm, mm, nm = costo("mbo", ini, fin)
        ct, mt, nt = costo("tbbo", ini, fin)
        tot += cm + ct
        print(f"   {f:<13}{para:<18}{cm:>10.2f}{ct:>10.2f}{cm+ct:>10.2f}{mm+mt:>9.0f}"
              f"{nm+nt:>13,}")
    pd_ = tot / len(MUESTRA)
    print(f"\n   PRECIO POR DIA (mbo + tbbo, dia UTC entero): USD {pd_:.2f}   "
          f"[rango de la muestra, {len(MUESTRA)} dias]")
    print(f"   Solo mbo: USD {sum(costo('mbo', f'{f}T00:00:00', f'{f}T23:59:59')[0] for f,_ in MUESTRA)/len(MUESTRA):.2f} por dia.")
    print("")
    print(f"   {'dias extra':>11}{'costo USD':>12}{'total dias':>12}{'credito que queda':>20}")
    for n in (3, 6, 12, 24, 48):
        c = n * pd_
        print(f"   {n:>11}{c:>12.2f}{YA_COMPRADOS + n:>12}{CREDITO - c:>20.2f}")
    print("")
    print(f"   COMPUERTAS: tope por item USD {TOPE_ITEM:.2f} (un dia cuesta USD {pd_:.2f}, "
          f"{'pasa' if pd_ <= TOPE_ITEM else 'NO pasa'});")
    print(f"               tope total USD {TOPE_TOTAL:.2f} -> caben {int(TOPE_TOTAL // pd_)} dias "
          f"sin pedir autorizacion nueva.")
    print("")
    print("   NO SE DESCARGO NADA. Este script no tiene modo --comprar por diseno. La compra, si")
    print("   Roberto la aprueba, va por databento_comprar_microestructura.py, que tiene la")
    print("   compuerta de $3 por item y $25 total en el codigo, y exige pregunta escrita por item.")
    print("=" * 100)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
