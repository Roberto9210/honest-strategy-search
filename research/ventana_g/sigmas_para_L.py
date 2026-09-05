"""
C1 - LOS DOS DESVIOS QUE LA VENTANA L USO COMO ESTIMACION, MEDIDOS.

NO GASTA CARTUCHO. K = 261. La caja sellada (2020-01-02 .. 2026-08-19) NO se toca; todo lo de aca
es ES 1-min 2016-2019, que ya esta mirado.

QUE PIDE P01. En la tabla de potencia de la prueba agrupada, dos de los tres sigma_j son
estimaciones y el propio documento lo dice: "Dos de los tres sigma_j son estimaciones mias, no
mediciones... por eso t(theta=1) = 4,69 es una cota optimista".

    L11  m = 11,4 pb (corregida en P03)  n = 176   sigma ESTIMADO ~ 60 pb  -> r = 0,190  n*r2 = 6,35
    L10  m = 17,0 pb                     n =  48   sigma ESTIMADO ~ 60 pb  -> r = 0,283  n*r2 = 3,84
    L08  publicado                       n = 480                                        n*r2 = 11,83
                                                            t(theta=1) = sqrt(22,02) = 4,69

Medir la dispersion NO destapa nada: la dispersion de una ventana no depende del signo predicho.

EL ESTIMADOR, declarado antes de mirar. Se usa el DESVIO COMUN (segundo momento), y el motivo es
que el estadistico que se quiere calibrar es t = m/(sigma/sqrt(n)), y el error estandar de una MEDIA
depende del segundo momento, no de la escala robusta. Un estimador robusto (MAD) descarta a
proposito la cola, y con cola gorda daria un sigma MENOR y por lo tanto una potencia MAYOR: seria
justo el error que este paso existe para evitar. Se reporta igual el robusto al lado, para que se
vea cuanto de sigma es cola. Y se reporta el peso de la cola con su propia medicion, no con la de
otra serie.

LO QUE ESTA MEDICION NO PUEDE HACER, dicho antes del numero:
  - L11 opera 176 dias de ANUNCIO y esas fechas exigen el calendario macro, que no esta en el repo.
    Se mide el desvio INCONDICIONAL de las 1.006 sesiones. Los dias de anuncio son MAS volatiles que
    el resto, asi que el incondicional es una COTA OPTIMISTA para L11: el sigma verdadero es mayor y
    la potencia verdadera, menor. Queda dicho como cota, no como medicion.
  - L10 SI se puede fechar exacto: sus eventos son el ultimo dia habil del mes y su ventana es la
    sesion SIGUIENTE. Ese sigma se mide sobre sus 48 sesiones.
"""

import math
import os
import sys

import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import juez as J  # noqa: E402

M_L11, N_L11 = 11.4, 176          # P03, corregida
M_L10, N_L10 = 17.0, 48           # P01
NR2_L08 = 11.83                   # publicado, no se toca
VARA_T = 3.0                      # la regla de decision de P01
THETA_H = 0.25                    # la hipotesis de P01


def robusto(x):
    return 1.4826 * float(np.median(np.abs(x - np.median(x))))


def main():
    R = []
    A = R.append
    A("=" * 98)
    A("C1 - LOS DOS SIGMA DE LA PRUEBA AGRUPADA DE LA VENTANA L, MEDIDOS SOBRE ES 2016-2019")
    A("NO GASTA CARTUCHO. K = 261. La caja sellada no se toca.")
    A("=" * 98)
    m = J.cargar_mercado()
    ses = np.arange(len(m["ini"]))
    cierre = m["cl"][m["fin"] - 1]                     # cierre de cada sesion
    fecha = pd.to_datetime([m["ts"][m["fin"][k] - 1] for k in ses]).normalize()
    anio = m["anio_ses"]
    ok = (anio >= 2016) & (anio <= 2019)
    # retorno cierre a cierre en puntos basicos del nocional
    ret = np.full(len(ses), np.nan)
    ret[1:] = (cierre[1:] / cierre[:-1] - 1.0) * 1e4
    val = ok & ~np.isnan(ret)
    r = ret[val]; f_all = fecha[val]; a_all = anio[val]
    A(f"\n   {len(r):,} sesiones 2016-2019 con retorno cierre a cierre, en pb del nocional.")

    # ------------------------------------------------------------------ el peso de la cola, medido
    A("")
    A("-" * 98)
    A("   EL PESO DE LA COLA EN ESTA SERIE (no en otra): |retorno| de sesion")
    A("-" * 98)
    ab = np.abs(r)
    q99, med = float(np.percentile(ab, 99)), float(np.median(ab))
    # para una normal, p99(|z|)/mediana(|z|) = 2,5758 / 0,6745
    normal = 2.5758293 / 0.6744898
    A(f"   p99/mediana de |retorno| = {q99:.1f}/{med:.1f} = {q99/med:.2f}    "
      f"una normal daria {normal:.2f}    exceso de curtosis {float(pd.Series(r).kurtosis()):.1f}")
    A(f"   Cola gorda, si. Y por eso el desvio comun es el estimador CORRECTO aca: es el que la")
    A(f"   incluye. El robusto la descartaria y regalaria potencia que no existe.")

    # ------------------------------------------------------------------ L11: cota incondicional
    A("")
    A("-" * 98)
    A("   L11 - sigma INCONDICIONAL (cota optimista: no estan las 176 fechas de anuncio)")
    A("-" * 98)
    s11 = float(np.std(r, ddof=1))
    A(f"   desvio comun  {s11:.2f} pb        robusto (1,4826*MAD)  {robusto(r):.2f} pb   "
      f"-> la cola aporta {s11/robusto(r):.2f}x")
    A(f"   por anio:  " + "   ".join(
        f"{y}: {float(np.std(r[a_all == y], ddof=1)):.1f} pb" for y in (2016, 2017, 2018, 2019)))
    A(f"   ESTIMADO por L: ~60,0 pb.   MEDIDO: {s11:.2f} pb.   "
      f"{'el estimado se queda CORTO' if s11 > 60 else 'el estimado era GENEROSO'}"
      f" por {abs(s11-60)/60:.0%}")

    # ------------------------------------------------------------------ L10: fechable exacto
    A("")
    A("-" * 98)
    A("   L10 - sigma de SUS 48 eventos (ultimo dia habil del mes -> retorno de la sesion SIGUIENTE)")
    A("-" * 98)
    # ultimo dia habil de cada mes, y la sesion siguiente
    df = pd.DataFrame(dict(f=f_all, r=r, i=np.arange(len(r))))
    df["ym"] = df["f"].values.astype("datetime64[M]")
    ult = df.groupby("ym")["i"].max()
    sig = ult.values + 1
    sig = sig[sig < len(df)]
    # los eventos de 2016-2019: el ultimo dia habil de dic-2015 no esta en la serie, y el de
    # dic-2019 llevaria al 2020-01-02, que es EL PRIMER DIA DE LA CAJA SELLADA. Se corta ahi.
    r10 = df["r"].values[sig]
    f10 = df["f"].values[sig]
    A(f"   {len(r10)} eventos fechados dentro de 2016-2019 (el primero {pd.Timestamp(f10[0]).date()}, "
      f"el ultimo {pd.Timestamp(f10[-1]).date()})")
    A("")
    A("   *** AVISO PARA LA VENTANA L, y no es un detalle de forma ***")
    A("   El evento numero 48 de L10, tal como P01 lo especifica -ultimo dia habil de cada mes de")
    A("   2016 a 2019, retorno del dia SIGUIENTE-, es el ultimo habil de dic-2019, y su dia")
    A("   siguiente es el 2020-01-02: EL PRIMER DIA DE LA CAJA SELLADA. Corrida al pie de la letra,")
    A("   la prueba agrupada toca la caja. Hay que declarar 47 eventos, o correr el conteo un mes")
    A("   hacia atras (ultimo habil de dic-2015 a nov-2019). Es una decision de L, no mia; aca se")
    A(f"   usan los {len(r10)} que caen dentro de 2016-2019 sin tocar nada.")
    A("")
    s10 = float(np.std(r10, ddof=1))
    A(f"   desvio comun  {s10:.2f} pb        robusto  {robusto(r10):.2f} pb        "
      f"n = {len(r10)}, error relativo del propio sigma ~{1/math.sqrt(2*(len(r10)-1)):.0%}")
    A(f"   ESTIMADO por L: ~60,0 pb.   MEDIDO: {s10:.2f} pb.")

    # ------------------------------------------------------------------ el estadistico, recalculado
    A("")
    A("=" * 98)
    A("   EL ESTADISTICO AGRUPADO, CON LOS SIGMA MEDIDOS")
    A("=" * 98)
    filas = []
    for nom, mj, sj_est, sj_med, nj in (("L11", M_L11, 60.0, s11, N_L11),
                                        ("L10", M_L10, 60.0, s10, N_L10)):
        filas.append((nom, mj, sj_est, sj_med, nj, nj * (mj / sj_est) ** 2, nj * (mj / sj_med) ** 2))
    A(f"   {'j':<5}{'m_j (pb)':>10}{'sigma EST':>11}{'sigma MED':>11}{'n_j':>6}"
      f"{'n*r2 EST':>11}{'n*r2 MED':>11}")
    for nom, mj, se, sm, nj, ce, cm in filas:
        A(f"   {nom:<5}{mj:>10.1f}{se:>11.1f}{sm:>11.2f}{nj:>6}{ce:>11.2f}{cm:>11.2f}")
    A(f"   {'L08':<5}{'publicado':>10}{'-':>11}{'-':>11}{480:>6}{NR2_L08:>11.2f}{NR2_L08:>11.2f}")
    tot_e = sum(f[5] for f in filas) + NR2_L08
    tot_m = sum(f[6] for f in filas) + NR2_L08
    t_e, t_m = math.sqrt(tot_e), math.sqrt(tot_m)
    A(f"   {'':<5}{'':>10}{'':>11}{'':>11}{704:>6}{tot_e:>11.2f}{tot_m:>11.2f}")
    A("")
    A(f"   t(theta=1)          {t_e:.2f}  ->  {t_m:.2f}      ({(t_m/t_e-1):+.0%})")
    A(f"   theta min detectable a {VARA_T:.1f} desvios   {VARA_T/t_e:.2f}  ->  {VARA_T/t_m:.2f}")
    A(f"   t que daria la hipotesis theta = {THETA_H}       {THETA_H*t_e:.2f}  ->  {THETA_H*t_m:.2f}")
    A("")
    A("-" * 98)
    A("   LO QUE ESTO DECIDE")
    A("-" * 98)
    if t_m >= VARA_T:
        A(f"   El {t_e:.2f} pasa a {t_m:.2f} y sigue POR ENCIMA de la vara de {VARA_T:.1f}: la prueba")
        A(f"   agrupada conserva resolucion. NO cae debajo de 3.")
    else:
        A(f"   El {t_e:.2f} CAE a {t_m:.2f}, DEBAJO de la vara de {VARA_T:.1f}: la prueba agrupada no")
        A(f"   justifica el cartucho como esta especificada.")
    A(f"   Pero la vara que importa no es esa. P01 fija la hipotesis en theta >= {THETA_H} y su")
    A(f"   propia regla dice que hace falta t >= {VARA_T:.1f} PARA ESE theta, o sea t(theta=1) >= "
      f"{VARA_T/THETA_H:.0f}.")
    A(f"   Con sigma medido t(theta=1) = {t_m:.2f}: la prueba detecta theta = {VARA_T/t_m:.2f}, no "
      f"{THETA_H}. Esa brecha")
    A(f"   ya estaba en P01 ({VARA_T/t_e:.2f} contra {THETA_H}) y la medicion la "
      f"{'agranda' if t_m < t_e else 'achica'}, no la crea.")
    A("")
    A("   Y LA ADVERTENCIA QUE NO SE ARREGLA MIDIENDO: con n = 48 y esta cola (p99/mediana "
      f"{q99/med:.1f}")
    A("   contra 3,8 de una normal), la aproximacion normal del propio estadistico es optimista.")
    A("   Medir sigma bien no arregla que el teorema central del limite converja lento. El control")
    A("   2 de P01 -el placebo de signo, mil veces- es lo que mide eso, y hay que leerlo asi.")
    A("=" * 98)
    print("\n".join(R))
    return 0


if __name__ == "__main__":
    sys.exit(main())
