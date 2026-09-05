"""B3 - COTIZACION (SIN COMPRAR) DEL PAQUETE DE DIVISAS QUE SIRVE A LAS DOS VENTANAS.

VENTANA G. K = 261. No gasta cartucho: es cotizacion de datos, no medicion. NO DESCARGA NADA.
Este script no tiene modo --comprar. La compra, si Roberto la aprueba, va por
databento_comprar_microestructura.py, que ya tiene las compuertas en el codigo.

LA REGLA: ninguna compra sin una pregunta escrita que conteste. Cada bloque lleva su pregunta.

POR QUE UN SOLO PAQUETE. La VENTANA L necesita divisas para su prueba agrupada (L08: seis futuros,
48 fechas, la ventana del fixing de Londres; y el plan B L07: 6J en los dias gotobi). La VENTANA G
necesita, para que el juez pueda JUZGAR divisas, la calibracion por instrumento que hoy figura como
FALTA en instrumentos.py. Son los mismos instrumentos y en parte los mismos dias, asi que se cotiza
una sola compra y se dice que parte sirve a quien.

LA CLAVE se lee de DATABENTO_API_KEY (env o ./.env, cubierto por .gitignore) y NO se imprime nunca,
ni entera ni en pedazos.
"""
from __future__ import annotations

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")
key = os.environ.get("DATABENTO_API_KEY")
if not key:
    print("DATABENTO_API_KEY no esta definida (env o .env). No se hace ninguna llamada.")
    sys.exit(2)

import databento as db  # noqa: E402

DATASET = "GLBX.MDP3"
CREDITO_DECLARADO = 98.92        # calculado tras la compra de microestructura (commit 07c903a)
TOPE_ITEM = 3.00
TOPE_TOTAL = 25.00
LON = ZoneInfo("Europe/London")
UTC = ZoneInfo("UTC")
SEIS = ["6E.n.0", "6J.n.0", "6B.n.0", "6A.n.0", "6C.n.0", "6S.n.0"]
MUESTRA_L07 = 24                 # de las 288 fechas gotobi se cotizan 24 exactas y se extrapola

client = db.Historical(key)


def ultimo_habil_del_mes(anios=(2016, 2017, 2018, 2019)):
    """Ultimo dia habil (lun-vie) de cada mes. Feriados del CME no descontados: si cae feriado, el
    dia existe igual y su costo es ~0, asi que la cotizacion queda del lado caro."""
    out = []
    for a in anios:
        for mth in range(1, 13):
            d = datetime(a + (mth == 12), (mth % 12) + 1, 1) - timedelta(days=1)
            while d.weekday() >= 5:
                d -= timedelta(days=1)
            out.append(d.date())
    return out


def gotobi(anios=(2016, 2017, 2018, 2019)):
    """Dias gotobi: dia del mes en {5,10,15,20,25} y fin de mes, corridos al habil siguiente si caen
    en fin de semana. Aproximacion para COTIZAR (el precio escala con la cantidad de dias); la
    definicion exacta es de la VENTANA L."""
    out = []
    for a in anios:
        for mth in range(1, 13):
            fin = (datetime(a + (mth == 12), (mth % 12) + 1, 1) - timedelta(days=1)).day
            for dd in (5, 10, 15, 20, 25, fin):
                d = datetime(a, mth, min(dd, fin))
                while d.weekday() >= 5:
                    d += timedelta(days=1)
                if d.year == a:
                    out.append(d.date())
    return sorted(set(out))


def ventana_utc(fecha, h_ini, h_fin, tz):
    """[h_ini, h_fin) hora local del tz en esa fecha, convertida a UTC fecha por fecha. El Reino
    Unido y Estados Unidos no cambian la hora el mismo fin de semana: un desfase fijo seria un
    error silencioso, y P04 lo avisa."""
    a = datetime.combine(fecha, datetime.min.time(), tzinfo=tz).replace(hour=h_ini)
    b = datetime.combine(fecha, datetime.min.time(), tzinfo=tz).replace(hour=h_fin)
    f = "%Y-%m-%dT%H:%M:%S"
    return a.astimezone(UTC).strftime(f), b.astimezone(UTC).strftime(f)


def costo(symbols, schema, ini, fin, stype="continuous"):
    kw = dict(dataset=DATASET, symbols=symbols, schema=schema, start=ini, end=fin, stype_in=stype)
    return (client.metadata.get_cost(**kw),
            client.metadata.get_billable_size(**kw) / 1e6,
            client.metadata.get_record_count(**kw))


def bloque(nombre, pregunta, symbols, schema, ventanas, sirve, escala=1.0):
    usd = mb = n = 0.0
    for ini, fin in ventanas:
        c, s, r = costo(symbols, schema, ini, fin)
        usd += c; mb += s; n += r
        print(f"      {ini} .. {fin}   USD {c:6.4f}   {s:7.2f} MB   {r:>10,}", flush=True)
    return dict(nombre=nombre, pregunta=pregunta, sirve=sirve, schema=schema,
                simbolos=len(symbols), ventanas=len(ventanas), escala=escala,
                usd=usd * escala, mb=mb * escala, n=n * escala, medido=len(ventanas))


def main():
    print("=" * 100)
    print("B3 - COTIZACION DEL PAQUETE DE DIVISAS. NO SE DESCARGA NADA. K = 261, no gasta cartucho.")
    print("=" * 100)
    fechas_l08 = ultimo_habil_del_mes()
    fechas_l07 = gotobi()
    print(f"\n   L08: {len(fechas_l08)} fechas (ultimo habil de cada mes 2016-2019), "
          f"{len(SEIS)} simbolos, 14:00-18:00 Londres")
    print(f"   L07: {len(fechas_l07)} fechas gotobi, 1 simbolo (6J), 9:50-10:00 Tokio "
          f"(se cotizan {MUESTRA_L07} exactas y se extrapola)")

    bloques = []

    print(f"\n   [1] L08 - ohlcv-1m, {len(SEIS)} simbolos, {len(fechas_l08)} fechas x 4 h")
    v = [ventana_utc(f, 14, 18, LON) for f in fechas_l08]
    bloques.append(bloque(
        "L08_fix_londres",
        "Las reglas de calendario publicadas conservan su signo y un cuarto de su magnitud en "
        "2016-2019? L08 aporta el 54% de la potencia de la prueba agrupada.",
        SEIS, "ohlcv-1m", v, sirve="VENTANA L (prueba agrupada) + VENTANA G (cortes de tercil)"))

    print(f"\n   [2] L07 plan B - ohlcv-1m, 6J, {MUESTRA_L07} de {len(fechas_l07)} fechas x 10 min")
    paso = max(1, len(fechas_l07) // MUESTRA_L07)
    vm = [ventana_utc(f, 9, 10, ZoneInfo("Asia/Tokyo")) for f in fechas_l07[::paso][:MUESTRA_L07]]
    bloques.append(bloque(
        "L07_gotobi",
        "Sustituto de L08 si L08 sale cara: el sesgo gotobi del yen sigue vivo en 2016-2019? "
        "Mismo numero de simbolo-dia con una ventana 24 veces mas corta.",
        ["6J.n.0"], "ohlcv-1m", vm,
        sirve="VENTANA L (plan B)", escala=len(fechas_l07) / len(vm)))

    print(f"\n   [3] VENTANA G - tbbo de 6E, 3 dias (uno por tercil de volatilidad), dia UTC entero")
    dias_g = ["2017-06-14", "2018-04-25", "2019-08-05"]     # los mismos dias B ya usados en ES
    vg = [(f"{d}T00:00:00", f"{d}T23:59:59") for d in dias_g]
    bloques.append(bloque(
        "G_microestructura_6E",
        "Cuanto cuesta ENTRAR cruzando en 6E, por regimen? Sin ese numero el juez no puede cobrar "
        "el deslizamiento de entrada y se NIEGA a juzgar 6E (instrumentos.py, origen FALTA).",
        ["6E.n.0"], "tbbo", vg, sirve="VENTANA G (calibracion del juez)"))

    print(f"\n   [4] VENTANA G - ohlcv-1d de los 6 simbolos, 2016-2019 entero (cortes de tercil)")
    bloques.append(bloque(
        "G_terciles_diario",
        "Cuales son los cortes de tercil de volatilidad ex-ante (rango/precio de la sesion "
        "anterior) de cada divisa? El eje de regimen del juez es del instrumento, no heredado.",
        SEIS, "ohlcv-1d", [("2016-01-01T00:00:00", "2020-01-01T00:00:00")],
        sirve="VENTANA G (eje de regimen) + VENTANA L (contexto)"))

    print("\n" + "=" * 100)
    print(f"   {'bloque':<22}{'schema':<10}{'sim':>4}{'ventanas':>10}{'MB':>9}{'registros':>13}{'USD':>9}")
    total = 0.0
    for b in bloques:
        total += b["usd"]
        extra = "" if b["escala"] == 1.0 else f" (x{b['escala']:.0f} extrapolado de {b['medido']})"
        print(f"   {b['nombre']:<22}{b['schema']:<10}{b['simbolos']:>4}"
              f"{int(b['ventanas']*b['escala']):>10}{b['mb']:>9.1f}{int(b['n']):>13,}{b['usd']:>9.2f}"
              f"{extra}")
    print(f"   {'TOTAL':<68}{total:>9.2f}")
    print("")
    for b in bloques:
        print(f"   [{b['nombre']}] sirve a: {b['sirve']}")
        print(f"        pregunta: {b['pregunta']}")
    print("")
    print(f"   Credito declarado restante: USD {CREDITO_DECLARADO:.2f} (calculado, NO leido de la cuenta)")
    print(f"   Tope por item USD {TOPE_ITEM:.2f} | tope total USD {TOPE_TOTAL:.2f}")
    ex = [b["nombre"] for b in bloques if b["usd"] > TOPE_ITEM]
    print(f"   COMPUERTA por item: {'superan el tope -> ' + ', '.join(ex) if ex else 'ninguno supera el tope'}")
    print(f"   COMPUERTA total: {'SUPERA' if total > TOPE_TOTAL else 'no supera'} el tope de "
          f"USD {TOPE_TOTAL:.2f}")
    print("")
    print("   NO SE DESCARGO NADA. Este script no tiene modo --comprar por diseno.")
    print("=" * 100)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
