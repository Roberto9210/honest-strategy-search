"""
VENTANA G - CUANTO BAJA EL PISO CON MODO PASIVO, y cuanto de esa bajada es real y cuanto es deuda.

NO GASTA CARTUCHO. K = 261. Recalculo descriptivo del piso de referencia (entradas al azar) en modo
pasivo, contra el modo cruce. La caja sellada no se toca.

El piso en modo pasivo baja por DOS componentes:
  (1) SUSTITUCION DE ENTRADA: en vez de pagar el medio-spread (~+0,13 pt de costo) se captura el
      markout medido (~+0,04 pt de ganancia). Mejor precio de entrada.
  (2) LLENADO PARCIAL: solo se llena ~47-51% de las senales; el resto no opera. Menos operaciones de
      esperanza negativa -> menos perdida.
Las dos son REALES para un participante AL AZAR. Para un CANDIDATO son DEUDA: sus llenados estan
seleccionados por su senal, asi que el markout de (1) puede darse vuelta y el 53% no llenado de (2)
podria ser justo sus ganadores. Hasta medirlo sobre el candidato (mbo_lib, paso b), la bajada del
piso en modo pasivo es una COTA OPTIMISTA.
"""
import numpy as np

from aritmetica import C1_POR_MINI
from dolares_por_tiempo import MEDIA_EXCESO, PUNTO_ES, secuencial
from juez import DESLIZAMIENTO_ENTRADA, LLENADO_PASIVO, MARKOUT_PASIVO
from razon_escalas import cargar_con_sesion

CELDAS = [(5, 20), (20, 10)]
O_SOBREPASO = 0.0642
MIN_BARRAS = 60


def main():
    print("=" * 96)
    print("CUANTO BAJA EL PISO CON MODO PASIVO (entradas al azar) - y cuanto es real vs deuda")
    print("NO GASTA CARTUCHO. K = 261. La caja sellada no se toca.")
    print("=" * 96)
    df = cargar_con_sesion()
    cl = df["close"].to_numpy(float); hi = df["high"].to_numpy(float); lo = df["low"].to_numpy(float)
    sess = df["sess"].to_numpy()
    corte = np.flatnonzero(sess[1:] != sess[:-1]) + 1
    ini = np.concatenate(([0], corte)); fin = np.concatenate((corte, [len(cl)]))
    keep = (fin - ini) >= MIN_BARRAS
    ini, fin = ini[keep], fin[keep]
    vol_bps = np.array([(hi[a:b] - lo[a:b]).mean() / cl[a:b].mean() * 1e4 for a, b in zip(ini, fin)])
    prev = np.concatenate([[np.nan], vol_bps[:-1]])
    p33, p66 = np.nanquantile(prev, [1 / 3, 2 / 3])
    terc = np.where(np.isnan(prev), 1, np.where(prev <= p33, 0, np.where(prev <= p66, 1, 2)))
    slip = np.array([DESLIZAMIENTO_ENTRADA[int(t)] for t in terc])
    mk = np.array([MARKOUT_PASIVO[int(t)] for t in terc])
    fi = np.array([LLENADO_PASIVO[int(t)] for t in terc])

    print(f"\n   {'celda':>10}{'cruce':>10}{'sust. entrada':>15}{'+ llenado (PASIVO)':>20}"
          f"{'bajada total':>14}{'op/ses':>8}")
    for T, S in CELDAS:
        exc = MEDIA_EXCESO[S]; p = S / (S + T)
        sesgo = O_SOBREPASO * (1 - 2 * p) * PUNTO_ES
        # dolares por sesion por lado, brutos (comision + exceso del stop, SIN entrada)
        vs, nop = {}, 0
        for lado in ("largo", "corto"):
            v, no, na = secuencial(cl, hi, lo, ini, fin, T, S, lado, exceso=exc, c1=C1_POR_MINI)
            vs[lado] = v; nop += no
        op_lado = nop / 2.0 / len(ini)
        cru = np.mean([vs[l] - slip * op_lado * PUNTO_ES for l in ("largo", "corto")], axis=0)
        sub = np.mean([vs[l] + mk * op_lado * PUNTO_ES for l in ("largo", "corto")], axis=0)
        pas = np.mean([fi * (vs[l] + mk * op_lado * PUNTO_ES) for l in ("largo", "corto")], axis=0)
        piso_cru = -(cru.mean() - sesgo * op_lado)
        piso_sub = -(sub.mean() - sesgo * op_lado)
        piso_pas = -(pas.mean() - (fi * sesgo * op_lado).mean())
        print(f"   {f'{T}pt:{S}pt':>10}{piso_cru:>+10.2f}{piso_sub:>+15.2f}{piso_pas:>+20.2f}"
              f"{piso_cru - piso_pas:>+14.2f}{op_lado:>8.2f}")
        c1 = piso_cru - piso_sub
        c2 = piso_sub - piso_pas
        print(f"   {'':>10}   descomposicion: sustitucion de entrada {c1:+.2f}  +  llenado parcial {c2:+.2f}"
              f"  =  bajada {piso_cru - piso_pas:+.2f}")
    print("\n   REAL vs DEUDA: para entradas al azar las dos componentes son reales. Para un CANDIDATO,")
    print("   la parte del markout (dentro de 'sustitucion') y TODO el 'llenado parcial' son DEUDA:")
    print("   sus llenados estan seleccionados por su senal. La bajada del piso en modo pasivo es una")
    print("   COTA OPTIMISTA hasta medirlo sobre el candidato (mbo_lib, paso b).")


if __name__ == "__main__":
    main()
