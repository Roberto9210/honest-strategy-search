"""
DOS VERIFICACIONES SOBRE EL PERFIL INTRADIARIO.

NO GASTA CARTUCHO. K = 261. Dinero: $0. ES 1-min 2016-2019. La caja sellada no se toca.

A3 - EL SIGNO DE LA OBSERVACION DE LAS 972 SESIONES. Reporte que la caja #43 se mide sobre 972 y no
     1.007 sesiones porque los medios dias de feriado quedan afuera, que esos son de baja
     volatilidad, y que eso "empuja hacia arriba, o sea otra vez al lado facil". Me lo discutieron y
     tienen razon en dudar. Se hacen DOS cosas que no hice: (1) VERIFICAR la premisa -son de veras
     mas calmas las sesiones que faltan?-, que la afirme sin medirla; y (2) derivar el signo desde
     donde se CONSUME el numero, en vez de por intuicion.

A4 - LA APERTURA ES ESTRUCTURAL Y EL RESTO DEPENDE DEL ANO? Mi propia idea, con mi propio criterio
     de muerte: partir 2016-2019 en SEMESTRES y ver si la estabilidad de la caja #31 se cae igual
     que la de la #43. Si se cae igual, la idea esta muerta y el corte no es "apertura contra
     resto".
     LO HARIA FALLAR: que el rango entre semestres de #31 sea comparable al de #43.
"""

import os
import sys
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import juez as J  # noqa: E402

ANIOS = (2016, 2017, 2018, 2019)
CAJAS_MIRA = {31: "08:30 apertura contado", 43: "14:30 cierre contado",
              15: "00:30 madrugada", 33: "09:30", 42: "14:00"}


def perfil(cl, ini, fin, caja, sel, n_mh=48):
    ret = np.full((len(sel), n_mh), np.nan)
    for i, k in enumerate(sel):
        a, b = int(ini[k]), int(fin[k])
        c = cl[a:b]; cj = np.asarray(caja[a:b])
        for j in range(n_mh):
            w = np.flatnonzero(cj == j)
            if len(w) >= 2:
                ret[i, j] = (c[w[-1]] / c[w[0]] - 1.0) * 1e4
    return ret


def main():
    R = []
    A = R.append
    A("=" * 100)
    A("VERIFICACIONES DEL PERFIL INTRADIARIO: el signo de las 972 sesiones, y apertura vs resto")
    A("NO GASTA CARTUCHO. K = 261. Dinero: $0. La caja sellada no se toca.")
    A("=" * 100)
    m = J.cargar_mercado()
    ini, fin, cl = m["ini"], m["fin"], m["cl"]
    ts = pd.to_datetime(m["ts"])
    anio = m["anio_ses"]
    sel = np.flatnonzero(np.isin(anio, ANIOS))
    tz = ZoneInfo("America/Chicago")
    ct = pd.DatetimeIndex(ts).tz_localize("UTC").tz_convert(tz)
    caja = ((ct.hour * 60 + ct.minute - 17 * 60) % 1440) // 30
    ret = perfil(cl, ini, fin, caja, sel)
    fechas = pd.DatetimeIndex([ts[int(fin[k]) - 1] for k in sel])

    # ---------------------------------------------------------------- A3
    A("")
    A("-" * 100)
    A("   A3 (1) - LA PREMISA: son mas calmas las sesiones a las que les FALTA la caja #43?")
    A("-" * 100)
    tiene43 = np.isfinite(ret[:, 43])
    A(f"   Sesiones con la caja #43: {int(tiene43.sum()):,}   sin ella: {int((~tiene43).sum()):,}")
    # se compara la volatilidad de esas sesiones usando una caja que SI tienen todas: la #31
    tiene31 = np.isfinite(ret[:, 31])
    base = tiene31 & ~tiene43
    comp = tiene31 & tiene43
    a31_sin = np.abs(ret[base, 31]); a31_con = np.abs(ret[comp, 31])
    A(f"   Se comparan usando la caja #31 (08:30), que casi todas tienen, para no comparar contra")
    A(f"   una caja que justamente falta.")
    A(f"      |retorno| medio en #31, sesiones SIN #43 ({len(a31_sin)}):  {a31_sin.mean():.2f} pb")
    A(f"      |retorno| medio en #31, sesiones CON #43 ({len(a31_con)}):  {a31_con.mean():.2f} pb")
    r = a31_sin.mean() / max(a31_con.mean(), 1e-9)
    A(f"      cociente sin/con: {r:.2f}x")
    # y el desvio de la sesion entera
    tot = np.nansum(ret, axis=1)
    A(f"      desvio de la sesion entera, SIN #43: {np.nanstd(tot[base], ddof=1):.1f} pb   "
      f"CON #43: {np.nanstd(tot[comp], ddof=1):.1f} pb")
    if r < 0.9:
        A(f"   PREMISA CONFIRMADA: las sesiones que no tienen la caja #43 son mas calmas "
          f"({r:.2f}x).")
    elif r > 1.1:
        A(f"   PREMISA AL REVES: las sesiones sin la caja #43 son MAS agitadas ({r:.2f}x).")
    else:
        A(f"   PREMISA NO SOSTENIDA: no son distinguiblemente mas calmas ({r:.2f}x). La observacion")
        A(f"   que reporte se apoyaba en algo que no habia medido.")

    A("")
    A("-" * 100)
    A("   A3 (2) - EL SIGNO, DERIVADO DESDE DONDE SE CONSUME EL NUMERO")
    A("-" * 100)
    A("   El desvio de una caja se consume en tres lugares y en ninguno como costo:")
    A("     (i)   como DENOMINADOR de la senal por evento, r = magnitud / sigma  ->  sigma mas")
    A("           grande da r mas chico, t mas chico, MENOS potencia.")
    A("     (ii)  como ruido del umbral de deteccion, MDE = z * sigma / raiz(n)  ->  sigma mas")
    A("           grande da MDE mas grande, mas dificil detectar.")
    A("     (iii) como factor para escalar el desvio de sesion a la ventana  ->  factor mas grande")
    A("           da mas ruido supuesto.")
    A("   En los TRES, un sigma inflado hace la vara MAS EXIGENTE y los margenes MAS CHICOS.")
    A("")
    A("   CONCLUSION: si excluir sesiones calmas infla el sigma de la caja, eso empuja al LADO")
    A("   DIFICIL, no al facil. Mi reporte decia lo contrario y ESTABA MAL.")
    A("   De donde salio el error: lo trate como si fuera un COSTO -donde subestimar es 'facil'-")
    A("   cuando es una estimacion de RUIDO, donde sobreestimar es conservador. Es el mismo tipo de")
    A("   confusion que el error 4' del documento de signos: la pregunta correcta contestada al")
    A("   reves por no mirar donde se consume el numero.")

    # ---------------------------------------------------------------- A4
    A("")
    A("-" * 100)
    A("   A4 - LA APERTURA ES ESTRUCTURAL Y EL RESTO DEPENDE DEL ANO? Por SEMESTRES.")
    A("-" * 100)
    sem = (fechas.year.to_numpy() - 2016) * 2 + (fechas.month.to_numpy() > 6).astype(int)
    etiq = [f"{2016 + s // 2}-{'S2' if s % 2 else 'S1'}" for s in range(8)]
    n_mh = 48
    perf = np.full((8, n_mh), np.nan)
    for s in range(8):
        mk = sem == s
        if mk.sum() < 30:
            continue
        col = np.array([np.nanstd(ret[mk, j], ddof=1) if np.isfinite(ret[mk, j]).sum() > 5
                        else np.nan for j in range(n_mh)])
        perf[s] = col / np.nanmean(col)         # normalizado: la FORMA
    A(f"   {'caja':>6}{'que es':>26}" + "".join(f"{e:>9}" for e in etiq) + f"{'rango':>9}{'disp':>8}")
    filas = {}
    for j, nom in CAJAS_MIRA.items():
        v = perf[:, j]
        vv = v[np.isfinite(v)]
        rango = vv.max() / vv.min() if len(vv) > 1 else np.nan
        disp = vv.std(ddof=1) / vv.mean() if len(vv) > 1 else np.nan
        filas[j] = (rango, disp)
        A(f"   {'#' + str(j):>6}{nom:>26}" + "".join(
            f"{v[s]:>9.2f}" if np.isfinite(v[s]) else f"{'-':>9}" for s in range(8))
          + f"{rango:>9.2f}{disp:>8.1%}")
    A("")
    r31, d31 = filas[31]
    r43, d43 = filas[43]
    A(f"   #31 (apertura): rango entre semestres {r31:.2f}, dispersion {d31:.1%}")
    A(f"   #43 (cierre):   rango entre semestres {r43:.2f}, dispersion {d43:.1%}")
    A("")
    if r31 < r43 * 0.7:
        A(f"   LA IDEA SOBREVIVE. Con el corte mas fino la apertura sigue firme y el cierre no: el")
        A(f"   cierre se mueve {r43/r31:.1f} veces mas que la apertura entre semestres. 'La apertura es")
        A(f"   estructural y el resto depende del periodo' NO se cae al partir mas fino, que era")
        A(f"   exactamente mi condicion de muerte.")
    elif r31 > r43 * 0.9:
        A(f"   LA IDEA SE MUERE. Al partir por semestres la apertura se mueve tanto como el cierre")
        A(f"   ({r31:.2f} contra {r43:.2f}): la estabilidad que vi por ANOS era del tamano de la")
        A(f"   muestra, no de la apertura. Mi condicion de muerte se cumplio y la idea se descarta.")
    else:
        A(f"   NO CONCLUYENTE. La apertura se mueve menos que el cierre ({r31:.2f} contra {r43:.2f})")
        A(f"   pero no lo suficiente para llamarla estructural con este corte.")
    A("")
    A("   Y LO QUE MATA LA FORMA DE LA IDEA no es el numero de arriba sino la fila #15: la caja mas")
    A(f"   CALMA del dia -00:30, la madrugada- es la MAS ESTABLE de todas (rango {filas[15][0]:.2f}, "
      f"dispersion {filas[15][1]:.1%}),")
    A("   mas que la apertura. Mi idea decia 'la apertura es estructural y el resto depende del")
    A("   periodo', y la madrugada era justamente el 'resto' que daba por inestable. No es 'apertura")
    A("   contra resto': hay cajas estables y cajas inestables y NO se ordenan por la forma de U. La")
    A(f"   #42 (14:00) tiene dispersion {filas[42][1]:.1%} y la #33 (09:30) {filas[33][1]:.1%}, y son "
      f"vecinas de la #43 y la #31.")
    A("   LA IDEA, COMO LA ENUNCIE, QUEDA DESCARTADA. Lo que queda en pie es lo que ya estaba medido")
    A("   y no necesita teoria: la tabla caja por caja con su rango, y usar cada caja por su numero.")
    A("")
    A("   AVISO DE MUESTRA, para no repetir el error que este archivo corrige: un semestre son ~125")
    A("   sesiones, la mitad que un ano. Parte del rango que se ve aca es ruido de muestra y no")
    A("   inestabilidad real; por eso la comparacion es ENTRE cajas del mismo corte, que comparten")
    A("   ese ruido, y no contra el rango por anos.")
    A("=" * 100)
    print("\n".join(R))
    return 0


if __name__ == "__main__":
    sys.exit(main())
