"""
B2 - VERIFICACION DE UNA LINEA PARA LA VENTANA L: los mensajes T (trade) del GLBX traen order_id
distinto de cero?

NO GASTA CARTUCHO. K = 261. Dinero: $0, lee un archivo que ya esta en disco. La caja sellada no se
toca (se usa un dia B, de 2017-2019).

POR QUE. La VENTANA L no lo pudo confirmar en la documentacion, y de eso depende que se puedan
calcular las siete caracteristicas por llenado que diseno para clasificar quien nos pego. Es
exactamente lo que la Pieza 3b necesita para pasar de 'el libro avisa' a 'quien nos pego'.

QUE SE MIRA, y se mira por accion para no confundir T con F:
  A  alta de orden        C  baja        M  modificacion
  F  ejecucion de una orden EN REPOSO -esta es la que descuenta cola-
  T  print del trade      R  reset
La pregunta es especificamente sobre T.
"""

import os
import sys
from collections import Counter
from pathlib import Path

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import databento as db  # noqa: E402

DIR = Path(AQUI).resolve().parents[1] / "data" / "microestructura"
ARCH = "mbo_ESn0_B_medio_2019-05-01.dbn.zst"


def main():
    R = []
    A = R.append
    A("=" * 100)
    A("B2 - LOS MENSAJES T DEL GLBX TRAEN order_id DISTINTO DE CERO?")
    A("NO GASTA CARTUCHO. K = 261. Dinero: $0. La caja sellada no se toca.")
    A("=" * 100)
    p = DIR / ARCH
    if not p.exists():
        A(f"   FALTA {ARCH}. No se puede contestar.")
        print("\n".join(R))
        return 1
    df = db.DBNStore.from_file(str(p)).to_df(price_type="float", pretty_ts=True)
    A(f"\n   Archivo: {ARCH}   {len(df):,} mensajes   (GLBX.MDP3, schema mbo, ES.n.0)")
    act = df["action"].to_numpy(str)
    oid = df["order_id"].to_numpy(np.int64)
    A(f"   Acciones presentes: {dict(Counter(act).most_common())}")
    A("")
    A(f"   {'accion':>8}{'mensajes':>12}{'order_id = 0':>15}{'order_id != 0':>15}{'% no cero':>12}")
    for a in sorted(set(act)):
        m = act == a
        z = int((oid[m] == 0).sum())
        nz = int((oid[m] != 0).sum())
        A(f"   {a:>8}{int(m.sum()):>12,}{z:>15,}{nz:>15,}{nz/max(m.sum(),1):>11.1%}")

    mT = act == "T"
    A("")
    A("-" * 100)
    A("   LA RESPUESTA")
    A("-" * 100)
    if not mT.any():
        A("   NO HAY MENSAJES T EN ESTE ARCHIVO. La pregunta no se puede contestar con este dia, y")
        A("   ademas eso mismo es informacion: el flujo que tenemos descuenta cola por F, no por T.")
    else:
        nz = int((oid[mT] != 0).sum())
        tot = int(mT.sum())
        if nz == 0:
            A(f"   NO. Los {tot:,} mensajes T de este dia traen order_id = 0, TODOS.")
            A("   Consecuencia para la VENTANA L: no se puede identificar la orden agresora desde el")
            A("   mensaje T. Las caracteristicas por llenado que dependan de identificar a la")
            A("   contraparte por su order_id NO se pueden calcular con este esquema.")
            A("   LO QUE SI SE PUEDE: el mensaje F trae order_id de la orden EN REPOSO -la que fue")
            A("   ejecutada-, asi que se identifica a QUIEN FUE EJECUTADO, no a quien agredio. Para")
            A("   la Pieza 3b eso alcanza, porque la orden en reposo es la NUESTRA.")
        else:
            A(f"   SI. {nz:,} de {tot:,} mensajes T ({nz/tot:.1%}) traen order_id distinto de cero.")
            A("   Las caracteristicas por llenado que dependan del order_id del trade se pueden")
            A("   calcular.")
    mF = act == "F"
    if mF.any():
        nzF = int((oid[mF] != 0).sum())
        A("")
        A(f"   Y PARA COMPARAR, que es lo que de verdad usa el simulador: los {int(mF.sum()):,} "
          f"mensajes F traen order_id no cero en {nzF/max(mF.sum(),1):.1%} de los casos.")
    A("")
    A("   ALCANCE DE ESTA VERIFICACION, dicho para que no se generalice de mas: es UN dia "
      f"({ARCH[-23:-9]}),")
    A("   un simbolo (ES.n.0) y un dataset (GLBX.MDP3). No es una afirmacion sobre el esquema mbo en")
    A("   general ni sobre otros mercados. Si hace falta como propiedad del esquema, hay que")
    A("   repetirlo en los otros cinco dias, que ya estan en disco y cuestan cero.")
    A("=" * 100)
    print("\n".join(R))
    return 0


if __name__ == "__main__":
    sys.exit(main())
