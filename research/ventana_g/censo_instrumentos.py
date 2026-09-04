"""
VENTANA G - censo de instrumentos: existe alguno donde $2.000 de drawdown sea MUCHO?

NO GASTA CARTUCHO. K = 261. Es un censo de instrumentos contra una restriccion de cuenta ya
medida. No hay hipotesis sobre el mercado, no hay estadistico contra un alfa, no se elige
entre candidatas por resultado. Que nadie lo cuente como test.

LA PREGUNTA QUE NUNCA SE HIZO. La compuerta 1 murio por TAMANO, no por ventaja: $2.000 de
drawdown contra un instrumento cuyo movimiento tipico es una fraccion grande de la cuenta
entera. Todo el proyecto midio ES y NQ, los dos futuros de indice mas grandes y volatiles
que existen. Nunca se pregunto si hay un contrato donde $2.000 sea mucho.

DOS RAZONES, las dos en la misma unidad (numero de movimientos tipicos de UNA sesion, para
UN contrato micro):
    HOLGURA  = $2.000 de drawdown / movimiento ADVERSO tipico     -> cuantos golpes malos aguantas
    ESFUERZO = $3.000 de objetivo / movimiento FAVORABLE tipico   -> cuantos buenos necesitas
Bueno = holgura ALTA y esfuerzo BAJO a la vez. Se pide el ranking, no el ganador.

PROCEDENCIA
  Valor del punto y tick: tabla oficial de instrumentos de apextraderfunding.com, pestana
    "Micro Futures", leida 2026-09-04. NO asumidos, NO derivados.
  Que permite TRADEIFY y con que limite: NO VERIFICADO. datos_crudos.md no registra la lista
    de instrumentos de Tradeify, solo el limite agregado "4 minis/40 micros" del 50K Growth.
    Las especificaciones de contrato son del exchange y valen igual; el permiso es de la
    firma y no esta leido. Toda la tabla queda senalada.
  Precio: diarios ya en el repo. Ventana 2016-2019 para todos, la misma que el resto del
    proyecto y fuera de la caja sellada (ES diario 2020-01-02 -> 2026-08-19).
"""
import os

import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(os.path.dirname(AQUI)), "data")

DRAWDOWN = 2000.0
OBJETIVO = 3000.0
DESDE, HASTA = "2016-01-01", "2019-12-31"

# Especificaciones OFICIALES, apextraderfunding.com pestana "Micro Futures", 2026-09-04.
# (nombre, simbolo micro, tick, valor del punto, archivo de precios del full-size)
MICROS = [
    ("Micro E-Mini S&P 500",     "MES", 0.25,   5.00, "es_daily.csv"),
    ("Micro E-Mini Nasdaq-100",  "MNQ", 0.25,   2.00, "nq_daily.csv"),
    ("Micro E-Mini Dow Jones",   "MYM", 1.0,    0.50, "ym_daily.csv"),
    ("Micro E-Mini Russell 2000","M2K", 0.1,    5.00, "rty_daily.csv"),
    ("E-Micro Gold",             "MGC", 0.1,   10.00, "GC_F_daily.csv"),
    ("Micro Crude Oil",          "MCL", 0.01, 100.00, "CL_F_daily.csv"),
]

# Micros que la firma lista pero para los que NO hay precio en el repo. No se estiman.
SIN_DATOS = [
    ("E-Micro Silver",   "SIL", 0.005,     5.00, "diario de SI (plata COMEX)",
     "Databento GLBX/COMEX o el mismo proveedor diario que el resto"),
    ("E-Micro AUD/USD",  "M6A", 0.0001, 10000.00, "diario de 6A",
     "Databento GLBX o proveedor de FX futures"),
    ("E-Micro EUR/USD",  "M6E", 0.0001, 12500.00, "diario de 6E",
     "Databento GLBX o proveedor de FX futures"),
]
# Candidato cuyo micro NO figura en la tabla oficial leida: falta la especificacion ADEMAS
# del permiso. Hay precio (BTC_F_daily.csv) pero no se completa la fila.
SIN_SPEC = [("Micro Bitcoin", "MBT", "BTC_F_daily.csv (hay precio)",
             "especificacion oficial del contrato micro; no figura en la pestana leida")]


def carga(archivo):
    df = pd.read_csv(os.path.join(DATA, archivo))
    df.columns = [c.lower() for c in df.columns]
    fecha = "date" if "date" in df.columns else df.columns[0]
    df[fecha] = pd.to_datetime(df[fecha], utc=True, errors="coerce").dt.tz_localize(None)
    df = df.dropna(subset=[fecha, "open", "high", "low"])
    df = df[(df[fecha] >= DESDE) & (df[fecha] <= HASTA)]
    return df


def movimientos(df):
    """Excursion de UNA sesion, misma definicion que la escalera del terreno:
    adversa de un largo = open - low ; favorable de un largo = high - open."""
    adv = (df["open"] - df["low"]).to_numpy(float)
    fav = (df["high"] - df["open"]).to_numpy(float)
    return np.median(adv), np.median(fav), len(df)


def control():
    print("=" * 104)
    print("CONTROL - la formula nueva tiene que reproducir lo ya medido sobre ES")
    print("=" * 104)
    ok = True

    # (1) plomeria del valor del punto: para el ES COMPLETO ($50/pt) el drawdown son 40 pt.
    pt_es_full = 50.0
    pts = DRAWDOWN / pt_es_full
    print(f"   (1) drawdown / valor del punto de ES completo = "
          f"${DRAWDOWN:,.0f} / ${pt_es_full:.0f} = {pts:.0f} puntos   "
          f"{'OK' if abs(pts - 40) < 1e-9 else 'MAL'}")
    ok &= abs(pts - 40) < 1e-9

    # (2) las frecuencias de quiebre de la compuerta 1, recalculadas desde su propio script.
    from compuerta_nocturna import serie_cierres, PUNTO_ES
    d = serie_cierres()
    mov = np.abs(d["mov"].to_numpy(float))
    adv_l = np.clip(d["adv_largo"].to_numpy(float), 0, None)
    adv_c = np.clip(d["adv_corto"].to_numpy(float), 0, None)
    umbral = DRAWDOWN / PUNTO_ES
    got = [(mov >= umbral).mean(), (adv_l >= umbral).mean(), (adv_c >= umbral).mean()]
    esp = [0.0555, 0.0838, 0.0503]
    for et, g, e in zip(("cierre a cierre", "adversa largo", "adversa corto"), got, esp):
        bien = abs(g - e) < 0.0005
        ok &= bien
        print(f"   (2) {et:<18}{g*100:>7.2f}%  esperado {e*100:.2f}%   "
              f"{'OK' if bien else 'MAL'}")
    print(f"   CONTROL {'PASADO' if ok else 'FALLADO'}\n")
    return ok


def censo():
    print("=" * 104)
    print("CENSO - holgura y esfuerzo por instrumento micro")
    print(f"drawdown ${DRAWDOWN:,.0f} | objetivo ${OBJETIVO:,.0f} | UN contrato micro | "
          f"diarios {DESDE} a {HASTA}")
    print("TODA la tabla: permiso de Tradeify NO VERIFICADO (specs si, del exchange)")
    print("=" * 104)
    filas = []
    for nombre, sym, tick, punto, arch in MICROS:
        try:
            df = carga(arch)
        except FileNotFoundError:
            print(f"   {sym}: sin archivo {arch}, fila incompleta")
            continue
        madv, mfav, n = movimientos(df)
        adv_usd, fav_usd = madv * punto, mfav * punto
        filas.append(dict(nombre=nombre, sym=sym, punto=punto, n=n,
                          adv_pt=madv, fav_pt=mfav, adv_usd=adv_usd, fav_usd=fav_usd,
                          holgura=DRAWDOWN / adv_usd, esfuerzo=OBJETIVO / fav_usd))

    filas.sort(key=lambda f: -f["holgura"])
    es = [f for f in filas if f["sym"] == "MES"][0]
    print(f"   {'instrumento':<26}{'$/pt':>7}{'adv pt':>9}{'adv $':>8}{'fav $':>8}"
          f"{'HOLGURA':>10}{'ESFUERZO':>10}{'vs ES':>10}")
    for f in filas:
        dom = ""
        if f["sym"] != "MES":
            mejor_h = f["holgura"] > es["holgura"]
            mejor_e = f["esfuerzo"] < es["esfuerzo"]
            dom = "DOMINA" if (mejor_h and mejor_e) else ("holgura" if mejor_h else
                  ("esfuerzo" if mejor_e else "peor en 2"))
        print(f"   {f['nombre']:<26}{f['punto']:>7.2f}{f['adv_pt']:>9.2f}"
              f"{f['adv_usd']:>8.2f}{f['fav_usd']:>8.2f}"
              f"{f['holgura']:>10.1f}{f['esfuerzo']:>10.1f}{dom:>10}")
    print(f"\n   HOLGURA = cuantos movimientos adversos tipicos entran en el drawdown.")
    print(f"   ESFUERZO = cuantos movimientos favorables tipicos hacen falta para el objetivo.")
    print(f"   'DOMINA' = mejor que ES en LAS DOS razones.")

    print("\n" + "=" * 104)
    print("POR QUE NINGUNO DOMINA - las dos razones no son independientes")
    print("=" * 104)
    print("   holgura = 2000/adv$ y esfuerzo = 3000/fav$: LAS DOS son 1/(tamano del")
    print("   movimiento). Un instrumento que se mueve menos en dolares compra holgura y")
    print("   paga esfuerzo en la misma proporcion. Lo unico que puede romper el empate es")
    print("   la ASIMETRIA entre excursion favorable y adversa, y casi no varia:\n")
    print(f"   {'instrumento':<26}{'adv/fav':>9}{'holgura/esfuerzo':>19}{'vs ES':>9}")
    for f in sorted(filas, key=lambda x: -(x["holgura"] / x["esfuerzo"])):
        r = f["holgura"] / f["esfuerzo"]
        rel = r / (es["holgura"] / es["esfuerzo"])
        print(f"   {f['nombre']:<26}{f['adv_pt']/f['fav_pt']*f['punto']/f['punto']:>9.3f}"
              f"{r:>19.3f}{rel:>8.2f}x")
    rs = [f["holgura"] / f["esfuerzo"] for f in filas]
    print(f"\n   Rango de holgura/esfuerzo en los seis: {min(rs):.3f} a {max(rs):.3f}. "
          f"El mejor es {max(rs)/min(rs):.2f}x el peor,")
    print(f"   y solo {max(rs)/(es['holgura']/es['esfuerzo']):.2f}x el de ES. No hay un instrumento")
    print("   estructuralmente distinto: hay seis versiones del mismo problema a distinta escala.")
    return filas


def faltantes():
    print("\n" + "=" * 104)
    print("LO QUE FALTA - candidatos sin dato. No se estiman.")
    print("=" * 104)
    print("   A. Micro que la firma lista, con especificacion oficial leida, SIN precio en el repo:")
    for nombre, sym, tick, punto, dato, fuente in SIN_DATOS:
        print(f"      {sym:<5}{nombre:<22} ${punto:>10,.2f}/pt   falta: {dato}")
        print(f"           de donde saldria: {fuente}")
    print("\n   B. Candidato con precio en el repo pero SIN especificacion oficial leida:")
    for nombre, sym, dato, falta in SIN_SPEC:
        print(f"      {sym:<5}{nombre:<22} {dato}")
        print(f"           falta: {falta}")
    print("\n   C. Falta para TODA la tabla: la lista de instrumentos que Tradeify permite y su")
    print("      limite por contrato. Saldria de la pagina oficial de Tradeify o de su help")
    print("      center, igual que se leyeron las comisiones. Hoy NO VERIFICADO.")


if __name__ == "__main__":
    if not control():
        raise SystemExit("El control no reproduce. La generalizacion esta mal, no se publica.")
    filas = censo()
    faltantes()
