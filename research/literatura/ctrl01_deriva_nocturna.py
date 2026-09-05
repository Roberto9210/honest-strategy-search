"""
CTRL01 - CONTROL DEL INSTRUMENTO, NO CANDIDATA. Reproduce la deriva nocturna publicada de
Boyarchenko, Larsen y Whelan (NY Fed SR 917, ES 1998-2020) sobre ES 1-min 2016-2019.

VENTANA L. NO GASTA CARTUCHO. K = 261. Dinero: $0. La caja sellada no se toca (solo 2016-2019).
Corrido por instruccion de Roberto (ronda 22). Lee los datos con el cargador de la VENTANA G,
sin modificar nada de su territorio.

CRITERIOS SELLADOS ANTES DE CORRER (CTRL01_deriva_nocturna_para_G.md, seccion 3, en unidades
de desvio porque la tabla en pb de BLW no esta disponible):
  theta_pub(2:00-3:00 ET)  = 1,1 / raiz(252) = 0,0693 desvios por dia (Sharpe antes de costos)
  theta_pub(1:30-3:30 ET)  = 1,3 / raiz(252) = 0,0819
  theta_obs = media / desvio de los retornos de la ventana, 2016-2019
  error estandar de theta_obs = 1 / raiz(n)
  REPRODUCE     si theta_obs > 0  y  |theta_obs - theta_pub| <= 2 / raiz(n)
  NO REPRODUCE  si theta_obs < 0, o si |theta_obs - theta_pub| > 2 / raiz(n)
  potencia declarada: t esperada = theta_pub * raiz(n) ~ 2,2 si el efecto es estacionario
  LECTURA SELLADA de un NO REPRODUCE: primero el reloj (chequeo abajo), despues dos lecturas
  -no estacionario en 2016-2019, o el instrumento no lo ve- SIN ELEGIR.
Ventana: precio a las HH:MM del este = cierre de la ultima barra de un minuto que abre antes de
HH:MM, hora de America/New_York manejada fecha por fecha (horario de verano incluido).
"""
import os
import sys

import numpy as np
import pandas as pd

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(RAIZ, "research", "ventana_g"))
from razon_escalas import cargar_con_sesion  # noqa: E402  (lectura; no se modifica nada de G)

SR252 = np.sqrt(252.0)
VENTANAS = {"2:00-3:00 ET": (120, 180, 1.1), "1:30-3:30 ET": (90, 210, 1.3)}


def precio_a(df_dia, minuto_et):
    """cierre de la ultima barra que ABRE antes del minuto pedido (ts_event = apertura de barra)."""
    sub = df_dia[df_dia["m_et"] < minuto_et]
    if sub.empty:
        return np.nan
    return float(sub["close"].iloc[-1])


def main():
    df = cargar_con_sesion()
    ts = pd.to_datetime(df["ts_event_utc"], utc=True)
    et = ts.dt.tz_convert("America/New_York")
    df["fecha_et"] = et.dt.strftime("%Y-%m-%d")
    df["m_et"] = et.dt.hour * 60 + et.dt.minute
    df["anio"] = et.dt.year
    print("CTRL01 - control del instrumento: la deriva nocturna de BLW sobre ES 1-min 2016-2019")
    print(f"   {df['sess'].nunique():,} sesiones limpias del cargador de G; {len(df):,} barras")
    print()
    # ---------------------------------------------------------------- reloj: donde esta el pico
    df["r1"] = np.log(df["close"]).diff()
    df.loc[df["sess"] != df["sess"].shift(1), "r1"] = np.nan
    absr = df.groupby("m_et")["r1"].apply(lambda s: np.nanmean(np.abs(s)))
    top = absr.sort_values(ascending=False).head(3)
    print("CHEQUEO DE RELOJ - los tres minutos del este con mayor |retorno| medio de 1 min (espero 09:30 y 08:30):")
    for m, v in top.items():
        print(f"   {int(m)//60:02d}:{int(m)%60:02d} ET   {v*1e4:.2f} pb")
    print()
    # ---------------------------------------------------------------- las ventanas
    grupos = df.groupby("fecha_et", sort=True)
    for nombre, (m0, m1, sr_pub) in VENTANAS.items():
        rets, anios = [], []
        for fecha, g in grupos:
            if g["m_et"].min() > m0 - 30 or g["m_et"].max() < m1:
                continue      # el dia no cubre la ventana (fines de semana, feriados, sesiones cortas)
            p0, p1 = precio_a(g, m0), precio_a(g, m1)
            if np.isnan(p0) or np.isnan(p1):
                continue
            rets.append(np.log(p1 / p0))
            anios.append(int(fecha[:4]))
        r = np.array(rets) * 1e4
        a = np.array(anios)
        n = len(r)
        media, desvio = r.mean(), r.std(ddof=1)
        theta = media / desvio
        se = 1.0 / np.sqrt(n)
        t = media / (desvio / np.sqrt(n))
        theta_pub = sr_pub / SR252
        t_esp = theta_pub * np.sqrt(n)
        dentro = abs(theta - theta_pub) <= 2 * se
        veredicto = "REPRODUCE" if (theta > 0 and dentro) else "NO REPRODUCE"
        print(f"VENTANA {nombre}   n = {n} dias   (BLW: Sharpe {sr_pub} antes de costos -> theta_pub = {theta_pub:.4f})")
        print(f"   media = {media:+.3f} pb   desvio = {desvio:.2f} pb   t = {t:+.2f}   (t esperada si estacionario: {t_esp:.2f})")
        print(f"   theta_obs = {theta:+.4f}   +/- {se:.4f}   intervalo de reproduccion [{theta_pub-2*se:+.4f}, {theta_pub+2*se:+.4f}]")
        print(f"   VEREDICTO SELLADO: {veredicto}")
        print("   por anio:")
        for y in sorted(set(a)):
            m = a == y
            ry = r[m]
            print(f"      {y}: n = {m.sum():3d}   media = {ry.mean():+.3f} pb   desvio = {ry.std(ddof=1):.2f}   t = {ry.mean()/(ry.std(ddof=1)/np.sqrt(m.sum())):+.2f}")
        print()
    print("LO QUE ESTE CONTROL NO ES: no es una candidata (1 por dia, F17), no produce una regla, no toca")
    print("la caja, y 2016-2019 esta ADENTRO de la muestra de BLW: informa sobre el instrumento, no sobre el mercado.")


if __name__ == "__main__":
    main()
