"""COMPRA APROBADA de microestructura de ES, con la compuerta EN EL CODIGO.

VENTANA G. K = 261. No gasta cartucho: es compra de datos, no medicion. Descargar y medir son dos
pasos; este es el primero. No se mide nada aca.

LA REGLA QUE HACE SEGURA LA AUTORIZACION: ninguna compra sin una pregunta escrita que conteste.
Cada item lleva su pregunta y se imprime al lado del costo. Si no hay pregunta, no hay compra.

LA COMPUERTA, en el codigo y no en la memoria de nadie:
  - TOPE_ITEM  = USD 3,00  por pedido individual: el script se NIEGA a llamar a la descarga si
                 metadata.get_cost del item supera el tope.
  - TOPE_TOTAL = USD 25,00 para el paquete: se cotiza TODO primero; si la suma supera el tope no se
                 descarga NADA.
  Modo por defecto: --cotizar (no descarga). La descarga exige --comprar explicito.

La clave se lee de DATABENTO_API_KEY (o ./.env, en .gitignore) y no se imprime. Los datos van a
data/microestructura/, que .gitignore excluye (data/ y *.dbn.zst); el script lo verifica con
git check-ignore antes de descargar.

Uso:
    python databento_comprar_microestructura.py --cotizar
    python databento_comprar_microestructura.py --comprar
    python databento_comprar_microestructura.py --comprar --solo auxiliar     # un item por nombre
"""
from __future__ import annotations

import json
import os
import subprocess
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

TOPE_ITEM = 3.00
TOPE_TOTAL = 25.00
CREDITO_DECLARADO = 107.00          # dicho por Roberto, 2026-09-04; no se lee de la cuenta
DATASET = "GLBX.MDP3"
DESTINO = ROOT / "data" / "microestructura"
PLAN = ROOT / "databento_plan_compra.json"   # los items: pregunta, schema, ventana

client = db.Historical(key)


def cargar_plan():
    with open(PLAN, encoding="utf-8") as f:
        return json.load(f)


def destino_de(item):
    return DESTINO / f"{item['schema']}_{item['simbolo'].replace('.', '')}_{item['nombre']}.dbn.zst"


def verificar_gitignore():
    DESTINO.mkdir(parents=True, exist_ok=True)
    sonda = DESTINO / "sonda.dbn.zst"
    r = subprocess.run(["git", "check-ignore", "-q", str(sonda.relative_to(ROOT))], cwd=ROOT)
    if r.returncode != 0:
        raise SystemExit(f"ABORTADO: {sonda.relative_to(ROOT)} NO esta cubierto por .gitignore. "
                         f"Los datos no van al repo. Arreglar .gitignore antes de descargar.")
    print(f"gitignore OK: {DESTINO.relative_to(ROOT)}/*.dbn.zst queda fuera del control de versiones.")


def cotizar(items):
    print(f"\n{'item':<22}{'schema':<7}{'simbolo':<8}{'inicio (UTC)':<22}{'fin (UTC)':<22}{'USD':>7}{'MB':>9}{'registros':>13}")
    total = 0.0
    for it in items:
        kw = dict(dataset=DATASET, symbols=[it["simbolo"]], schema=it["schema"], start=it["inicio"],
                  end=it["fin"], stype_in=it.get("stype", "continuous"))
        it["usd"] = client.metadata.get_cost(**kw)
        it["mb"] = client.metadata.get_billable_size(**kw) / 1e6
        it["n"] = client.metadata.get_record_count(**kw)
        total += it["usd"]
        print(f"{it['nombre']:<22}{it['schema']:<7}{it['simbolo']:<8}{it['inicio']:<22}{it['fin']:<22}"
              f"{it['usd']:>7.2f}{it['mb']:>9.1f}{it['n']:>13,}")
    print(f"{'TOTAL':<86}{total:>7.2f}")
    return total


def main(argv):
    comprar = "--comprar" in argv
    solo = argv[argv.index("--solo") + 1] if "--solo" in argv else None
    plan = cargar_plan()
    items = [it for it in plan["items"] if (solo is None or it["nombre"] == solo)]
    for it in items:
        if not it.get("pregunta", "").strip():
            raise SystemExit(f"ABORTADO: el item {it['nombre']} no tiene pregunta escrita. Sin pregunta no hay compra.")
    print("PREGUNTAS QUE CONTESTA CADA ITEM:")
    for it in items:
        print(f"   [{it['nombre']}] {it['pregunta']}")
    total = cotizar(items)
    print(f"\nTope por item USD {TOPE_ITEM:.2f} | tope total USD {TOPE_TOTAL:.2f} | credito declarado USD {CREDITO_DECLARADO:.2f}")
    exceden = [it["nombre"] for it in items if it["usd"] > TOPE_ITEM]
    if exceden:
        print(f"COMPUERTA: estos items superan USD {TOPE_ITEM:.2f} y NO se descargan: {exceden}")
    if total > TOPE_TOTAL:
        print(f"COMPUERTA: el total USD {total:.2f} supera USD {TOPE_TOTAL:.2f}. NO se descarga NADA.")
        return 3
    if not comprar:
        print("\nModo --cotizar: no se descargo nada. Para comprar: --comprar")
        return 0
    verificar_gitignore()
    gastado = 0.0
    previo = 0.0          # items del plan ya en disco: se compraron en una corrida anterior
    for it in items:
        dst = destino_de(it)
        if it["usd"] > TOPE_ITEM:
            print(f"   SALTEADO {it['nombre']}: USD {it['usd']:.2f} > tope {TOPE_ITEM:.2f}")
            continue
        if dst.exists() and dst.stat().st_size > 0:
            previo += it["usd"]
            print(f"   ya existe {dst.relative_to(ROOT)} ({dst.stat().st_size/1e6:.1f} MB): no se vuelve a cobrar")
            continue
        print(f"   descargando {it['nombre']} {it['schema']} -> {dst.relative_to(ROOT)} (USD {it['usd']:.2f}) ...")
        client.timeseries.get_range(dataset=DATASET, symbols=[it["simbolo"]], schema=it["schema"],
                                    start=it["inicio"], end=it["fin"],
                                    stype_in=it.get("stype", "continuous"), path=str(dst))
        gastado += it["usd"]
        print(f"      listo: {dst.stat().st_size/1e6:.1f} MB en disco. Gastado hasta aca USD {gastado:.2f}")
    print(f"\nGASTADO en esta corrida (segun cotizacion): USD {gastado:.2f}")
    print(f"GASTADO ACUMULADO en items del plan (esta corrida + los que ya estaban en disco): "
          f"USD {gastado + previo:.2f}")
    print(f"CREDITO RESTANTE (calculado: declarado - acumulado del plan; NO leido de la cuenta): "
          f"USD {CREDITO_DECLARADO - gastado - previo:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
