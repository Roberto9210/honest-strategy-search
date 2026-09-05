"""
VENTANA G - CUANTO SE MUEVE EL PISO AL COBRAR EL DESLIZAMIENTO DE ENTRADA MEDIDO.

NO GASTA CARTUCHO. K = 261. Recalculo descriptivo del piso de referencia (entradas al azar) con el
deslizamiento de entrada que microestructura_tbbo.py acaba de medir, contra el piso publicado que lo
trataba como cero. La caja sellada no se toca.

El deslizamiento de entrada es casi plano entre regimenes (0,1267 / 0,1334 / 0,1330 pt por tercil),
asi que se cobra por operacion segun el tercil ex-ante de la sesion de entrada -igual que en el juez-
y al lado se muestra la version plana para que se vea que la diferencia por regimen es chica.
"""
import numpy as np

from aritmetica import C1_POR_MINI
from dolares_por_tiempo import MEDIA_EXCESO, PUNTO_ES, SESION, secuencial
from juez import DESLIZAMIENTO_ENTRADA
from razon_escalas import cargar_con_sesion

CELDAS = [(5, 20), (20, 10)]
O_SOBREPASO = 0.0642
MIN_BARRAS = 60


def main():
    print("=" * 92)
    print("CUANTO SE MUEVE EL PISO AL COBRAR EL DESLIZAMIENTO DE ENTRADA MEDIDO")
    print("NO GASTA CARTUCHO. K = 261. La caja sellada no se toca.")
    print("=" * 92)
    df = cargar_con_sesion()
    cl = df["close"].to_numpy(float); hi = df["high"].to_numpy(float); lo = df["low"].to_numpy(float)
    sess = df["sess"].to_numpy()
    corte = np.flatnonzero(sess[1:] != sess[:-1]) + 1
    ini = np.concatenate(([0], corte)); fin = np.concatenate((corte, [len(cl)]))
    keep = (fin - ini) >= MIN_BARRAS
    ini, fin = ini[keep], fin[keep]
    # tercil ex-ante en bps de la sesion anterior, igual que el juez
    rango = hi - lo
    vol_bps = np.array([(rango[a:b].mean()) / (cl[a:b].mean()) * 1e4 for a, b in zip(ini, fin)])
    prev = np.concatenate([[np.nan], vol_bps[:-1]])
    p33, p66 = np.nanquantile(prev, [1 / 3, 2 / 3])
    terc = np.where(np.isnan(prev), 1, np.where(prev <= p33, 0, np.where(prev <= p66, 1, 2)))
    slip_ses = np.array([DESLIZAMIENTO_ENTRADA[int(t)] for t in terc])   # puntos por sesion
    slip_flat = float(np.mean([DESLIZAMIENTO_ENTRADA[k] for k in (0, 1, 2)]))

    print(f"\n   deslizamiento de entrada por tercil (pt): {DESLIZAMIENTO_ENTRADA}   plano: {slip_flat:.4f}")
    print(f"\n   {'celda':>10}{'piso viejo':>12}{'piso con entrada':>18}{'movimiento':>12}{'op/ses':>8}")
    for T, S in CELDAS:
        exc = MEDIA_EXCESO[S]; p = S / (S + T)
        sesgo = O_SOBREPASO * (1 - 2 * p) * PUNTO_ES
        # por lado: dolares por sesion con y sin deslizamiento de entrada (por regimen)
        pisos = {}
        for et in ("viejo", "entrada"):
            acc = np.zeros(len(ini)); nop = 0
            for lado in ("largo", "corto"):
                v, no, na = secuencial(cl, hi, lo, ini, fin, T, S, lado, exceso=exc, c1=C1_POR_MINI)
                if et == "entrada":
                    # restar el deslizamiento de entrada por operacion: aproximado como
                    # slip_ses[sesion] * PUNTO_ES por operacion de esa sesion. secuencial no expone
                    # ops por sesion, asi que se usa op_lado medio * slip por sesion (plano dentro de
                    # la sesion): exacto en la media, que es lo que gobierna el piso.
                    op_ses_lado = no / len(ini)
                    v = v - slip_ses * op_ses_lado * PUNTO_ES
                acc += v / 2.0; nop += no
            op_lado = nop / 2.0 / len(ini)
            piso = -(acc.mean() - sesgo * op_lado)
            pisos[et] = (piso, op_lado)
        pv, ol = pisos["viejo"]; pe, _ = pisos["entrada"]
        print(f"   {f'{T}pt:{S}pt':>10}{pv:>+12.2f}{pe:>+18.2f}{pe - pv:>+12.2f}{ol:>8.2f}")
    print("\n   El movimiento es slip * PUNTO * op/ses: el deslizamiento de entrada es del orden de la")
    print("   comision, asi que el piso -lo que un candidato tiene que superar por sesion- sube fuerte.")


if __name__ == "__main__":
    main()
