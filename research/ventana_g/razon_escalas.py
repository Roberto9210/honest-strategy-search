"""
VENTANA G - LA RAZON RANGO/DESVIO A VARIAS ESCALAS: microestructura o estructura?

NO GASTA CARTUCHO. K = 261. Medicion descriptiva sobre muestra ya recogida. La caja sellada
(2020-01-02 -> 2026-08-19) no se toca: todo es 2016-2019.

LA OBSERVACION. La barra de un minuto de ES tiene un rango medio de 0,6577 pt y un desvio de
cierre a cierre de 0,6079 pt: razon 1,082. Una barra browniana da E[rango] = sigma*raiz(8/pi)
= 1,5958 veces su desvio. La barra de ES es MUCHO mas angosta respecto de su propio
incremento de lo que puede ser un paseo.

LA EXPLICACION ABURRIDA QUE HAY QUE DESCARTAR PRIMERO. El rebote entre precio de compra y de
venta mete un ruido que se da vuelta cada operacion. Ese ruido INFLA la varianza de cierre a
cierre sin agrandar el rango, y por lo tanto HUNDE la razon, sin que el mercado sea nada mas
direccional. Es la explicacion estandar y es la primera que hay que sacar del medio.

COMO SE DISTINGUE. El rebote es un ruido de un solo paso: su aporte a la varianza NO crece
con la escala, mientras que la varianza verdadera crece proporcional a la escala. Entonces:

  - si al agrandar la barra la razon SUBE hacia 1,596 -> es ruido de microestructura;
  - si se queda baja en TODAS las escalas -> es otra cosa.

MEDICION DIRECTA DEL REBOTE, ademas de la razon: la razon de varianzas
VR(k) = Var(incremento de k minutos) / (k * Var(incremento de 1 minuto)). Con rebote de
compra-venta VR(1) = 1 por definicion y VR(k) SUBE hacia 1 desde abajo... mas precisamente,
normalizando en k=1, el rebote hace que VR(k) BAJE por debajo de 1 al crecer k, porque el
denominador esta inflado. Es el diagnostico clasico y no depende del modelo de barreras.

QUE HARIA FALLAR LA LECTURA "es microestructura": que la razon se quede plana y que VR(k) se
quede en 1. Ahi el rebote no explicaria nada y habria que buscar en otro lado.

Las barras se agregan DENTRO de cada sesion, nunca a caballo del corte nocturno.
"""
import os
import sys

import numpy as np

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(RAIZ, "research", "ventaja_futuros"))
from terreno_tenencia import load_databento, DEGRADED_UTC  # noqa: E402

ESCALAS = [1, 2, 3, 5, 10, 15, 30, 60, 120, 240, 390]
BROWNIANO = np.sqrt(8.0 / np.pi)


def cargar_con_sesion():
    df = load_databento()
    degr = set(df.loc[df["utc_date"].isin(DEGRADED_UTC), "sess"].unique())
    ncon = df.groupby("sess")["contract"].nunique()
    limpias = set(ncon[ncon == 1].index) - degr
    df = df[df["sess"].isin(limpias)].sort_values("ts_event_utc").reset_index(drop=True)
    return df


def agregar(cl, hi, lo, ini, fin, k):
    """Barras de k minutos, sin cruzar el corte de sesion. Se descarta el resto parcial."""
    rangos, incs = [], []
    for a, b in zip(ini, fin):
        m = (b - a) // k
        if m < 2:
            continue
        c = cl[a:a + m * k].reshape(m, k)
        h = hi[a:a + m * k].reshape(m, k).max(axis=1)
        l = lo[a:a + m * k].reshape(m, k).min(axis=1)
        cc = c[:, -1]
        rangos.append(h - l)
        incs.append(np.diff(cc))
    return np.concatenate(rangos), np.concatenate(incs)


def main():
    print("=" * 100)
    print("RAZON RANGO/DESVIO A VARIAS ESCALAS - microestructura o estructura?")
    print("NO GASTA CARTUCHO. K = 261. La caja sellada no se toca.")
    print("=" * 100)

    df = cargar_con_sesion()
    cl = df["close"].to_numpy(float)
    hi = df["high"].to_numpy(float)
    lo = df["low"].to_numpy(float)
    sess = df["sess"].to_numpy()
    corte = np.flatnonzero(sess[1:] != sess[:-1]) + 1
    ini = np.concatenate(([0], corte))
    fin = np.concatenate((corte, [len(cl)]))
    print(f"\n   ES 1-min Databento 2016-2019, {len(cl):,} barras en "
          f"{len(ini):,} sesiones de contrato unico.")
    print(f"   Referencia browniana: E[rango] / desvio = raiz(8/pi) = {BROWNIANO:.4f}\n")

    print(f"   {'escala':>9}{'barras':>11}{'rango medio':>13}{'desvio inc':>12}"
          f"{'RAZON':>9}{'vs browniano':>14}{'VR(k)':>9}{'lectura VR':>14}")
    base_var = None
    razones = []
    for k in ESCALAS:
        rg, inc = agregar(cl, hi, lo, ini, fin, k)
        sd = inc.std()
        var = inc.var()
        if base_var is None:
            base_var = var
        vr = var / (k * base_var)
        razon = rg.mean() / sd
        razones.append(razon)
        print(f"   {f'{k} min':>9}{len(rg):>11,}{rg.mean():>13.4f}{sd:>12.4f}"
              f"{razon:>9.3f}{razon/BROWNIANO*100:>13.1f}%{vr:>9.3f}"
              f"{('inflado en 1min' if vr < 0.95 else 'sin rebote'):>14}")

    print("\n" + "=" * 100)
    print("LECTURA")
    print("=" * 100)
    sube = razones[-1] > razones[0]
    cerca = razones[-1] / BROWNIANO
    print(f"\n   razon a 1 minuto:   {razones[0]:.3f}  ({razones[0]/BROWNIANO*100:.1f}% del browniano)")
    print(f"   razon a {ESCALAS[-1]} minutos: {razones[-1]:.3f}  ({cerca*100:.1f}% del browniano)")
    print(f"   maximo de la curva: {max(razones):.3f} en "
          f"{ESCALAS[int(np.argmax(razones))]} min")
    if sube and cerca > 0.90:
        print("\n   -> SUBE hacia el browniano: es RUIDO DE MICROESTRUCTURA. La observacion")
        print("      de la razon 1,08 no es estructura del mercado y no hay que usarla.")
    elif sube:
        print("\n   -> sube pero NO llega al browniano. Parte es microestructura y parte no.")
        print("      Hace falta decir cuanto de cada cosa antes de usarla para algo.")
    else:
        print("\n   -> NO sube: se queda baja en todas las escalas. El rebote no lo explica.")
    print("\n   QUE HARIA FALLAR ESTA LECTURA: que la razon se quedara plana Y que VR(k) se")
    print("   quedara en 1. Ahi el rebote no explicaria nada.")
    return razones


if __name__ == "__main__":
    main()
