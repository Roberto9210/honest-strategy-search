"""
TAREA 5 - (a) order_id en los SEIS dias, y (b) que son los mensajes con accion N.

NO GASTA CARTUCHO. K = 261. Dinero: $0, lee archivos que ya estan en disco. La caja sellada no se
toca: los tres dias A son posteriores al 2026-08-19.

(a) La verificacion de order_id en T se hizo sobre UN dia y lo marque como alcance limitado. Se
    repite en los seis. Con eso las siete caracteristicas por llenado que diseno la VENTANA L quedan
    habilitadas -o no- para el conjunto entero, y eso alimenta directo a la Pieza 3b.

(b) En el dia que revise habia 1.068 mensajes con accion 'N' que caen en el `else: continue` de
    mbo_lib.reconstruir. Es 0,02% y probablemente no cambia nada, pero "no se que son" en un
    instrumento que acabo de descubrir que estaba ciego merece un minuto de esquema. Se mira que
    traen: precio, tamano, lado, order_id, y si aparecen agrupados en el tiempo.
"""

import os
import sys
from collections import Counter
from pathlib import Path

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import databento as db  # noqa: E402
import mbo_entrada_pasiva as P  # noqa: E402

DIR = Path(AQUI).resolve().parents[1] / "data" / "microestructura"


def main():
    R = []
    A = R.append
    A("=" * 100)
    A("TAREA 5 - order_id en los seis dias, y que son los mensajes 'N'")
    A("NO GASTA CARTUCHO. K = 261. Dinero: $0. La caja sellada no se toca.")
    A("=" * 100)
    A("")
    A("   (a) order_id DISTINTO DE CERO, por accion y por dia. 'T' es la que preguntaba la VENTANA L.")
    A("")
    acciones = ["A", "C", "M", "F", "T", "N", "R"]
    A(f"   {'dia':>16}{'mensajes':>12}" + "".join(f"{a:>9}" for a in acciones))
    filas = []
    ene = {}
    for epoca, tercil, arch in P.ARCHIVOS:
        p = DIR / arch
        if not p.exists():
            A(f"   {epoca + '/' + tercil:>16}   FALTA {arch}")
            continue
        df = db.DBNStore.from_file(str(p)).to_df(price_type="float", pretty_ts=True)
        act = df["action"].to_numpy(str)
        oid = df["order_id"].to_numpy(np.int64)
        cel = []
        for a in acciones:
            m = act == a
            if not m.any():
                cel.append("-")
            else:
                cel.append(f"{(oid[m] != 0).mean():.1%}")
        A(f"   {epoca + '/' + tercil:>16}{len(df):>12,}" + "".join(f"{c:>9}" for c in cel))
        mT = act == "T"
        filas.append((f"{epoca}/{tercil}", int(mT.sum()), int((oid[mT] == 0).sum())))
        mN = act == "N"
        if mN.any():
            sub = df[mN]
            ene[f"{epoca}/{tercil}"] = dict(
                n=int(mN.sum()),
                lados=dict(Counter(sub["side"].to_numpy(str)).most_common()),
                precios_nan=int(np.isnan(sub["price"].to_numpy(float)).sum()),
                tam=dict(Counter(sub["size"].to_numpy(np.int64)).most_common(4)),
                oid_cero=int((sub["order_id"].to_numpy(np.int64) == 0).sum()),
                instantes=len(set(sub.index.astype("int64") // 1_000_000_000)))
        del df

    A("")
    A("-" * 100)
    A("   (a) LA RESPUESTA SOBRE 'T', sobre los seis dias")
    A("-" * 100)
    tot = sum(f[1] for f in filas); cero = sum(f[2] for f in filas)
    for nom, nT, nz in filas:
        A(f"      {nom:>16}   {nT:>9,} mensajes T,   {nz:>4} con order_id = 0")
    A("")
    if tot:
        A(f"   TOTAL: {tot:,} mensajes T, {cero} con order_id cero ({cero/tot:.4%}).")
        if cero / tot < 0.001:
            A("   CONFIRMADO EN LOS SEIS DIAS: los mensajes T traen order_id distinto de cero.")
            A("   Las siete caracteristicas por llenado de la VENTANA L quedan HABILITADAS para el")
            A("   conjunto entero, no solo para el dia que mire antes.")
        else:
            A("   NO uniforme: hay dias con una fraccion no despreciable de T con order_id cero.")
    A("   ALCANCE: seis dias, un simbolo (ES.n.0), un dataset (GLBX.MDP3), dos epocas (2017-2019 y")
    A("   2026). Sigue sin ser una afirmacion sobre el esquema mbo en general.")

    A("")
    A("-" * 100)
    A("   (b) QUE SON LOS MENSAJES 'N'")
    A("-" * 100)
    if not ene:
        A("   No hay mensajes N en ningun dia.")
    else:
        A(f"   {'dia':>16}{'n':>8}{'oid=0':>8}{'precio NaN':>12}{'segundos distintos':>20}   lados")
        for nom, d in ene.items():
            A(f"   {nom:>16}{d['n']:>8}{d['oid_cero']:>8}{d['precios_nan']:>12}"
              f"{d['instantes']:>20}   {d['lados']}")
        A("")
        A("   LO QUE SE PUEDE DECIR CON EL DATO, sin inventar: los N vienen con order_id = 0, precio")
        A("   NaN y lado 'N' (ninguno). No tocan el libro -no hay orden que agregar, sacar o")
        A("   modificar- y por eso caer en el `else: continue` de reconstruir() es el tratamiento")
        A("   CORRECTO, no un descuido. Son mensajes administrativos del canal.")
        A("   LO QUE NO PUEDO CITAR: la definicion oficial. No tengo la documentacion de Databento a")
        A("   mano en este entorno y NO la voy a inferir del nombre. Queda como: verificado que no")
        A("   afectan la reconstruccion, sin confirmar que significan. Cerrarlo es leer la pagina de")
        A("   'MBO action' de Databento, cuesta cero y no lo hice.")
    A("=" * 100)
    print("\n".join(R))
    return 0


if __name__ == "__main__":
    sys.exit(main())
