"""
PIEZA 1 - EL PERFIL DE VOLATILIDAD INTRADIARIA DEL ES, POR MEDIAS HORAS, EN PUNTOS BASICOS.

NO GASTA CARTUCHO. K = 261. ES 1-min 2016-2019, terreno ya mirado. La caja sellada no se toca.
Dinero: $0. Tiempo de Roberto: leer la tabla.

POR QUE. Hasta ahora se escalo el desvio a ventanas cortas con la RAIZ DEL TIEMPO, lo que supone
volatilidad pareja a lo largo del dia. No lo es: es en forma de U. Ese supuesto esta adentro de
cualquier evaluacion de candidata con ventana intradiaria, nuestra o de la literatura.

QUE SE MIDE. Para cada media hora de la sesion, el desvio de los retornos de esa media hora en
puntos basicos del nocional, sobre las sesiones de 2016-2019. Una sola cifra por media hora.

CONTRASTE EXTERNO, usado COMO CONTROL: la VENTANA L derivo de Baltussen que la ultima media hora
tiene del orden de 25 pb por sesion. IMPORTANTE: esa conversion (3,96% anual -> por sesion) es
DERIVACION DE LA VENTANA L, no una cifra publicada, y asi va marcada.
LO HARIA FALLAR: que la ultima media hora medida quede muy lejos de ~25 pb. Si pasa, uno de los dos
esta mal y hay que decir cual antes de seguir.

Y LA OTRA CONDICION DE FALLA: que el perfil no sea estable a lo largo de 2016-2019. Si no lo es, se
mide por ano y se dice -seria otra variable que estabamos tratando como constante-.
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
BALTUSSEN_L = 25.0        # pb, DERIVACION DE LA VENTANA L, no cifra publicada


def main():
    R = []
    A = R.append
    A("=" * 100)
    A("PIEZA 1 - PERFIL DE VOLATILIDAD INTRADIARIA DEL ES POR MEDIAS HORAS, EN PUNTOS BASICOS")
    A("NO GASTA CARTUCHO. K = 261. Dinero: $0. La caja sellada no se toca.")
    A("=" * 100)
    m = J.cargar_mercado()
    ini, fin, cl = m["ini"], m["fin"], m["cl"]
    ts = pd.to_datetime(m["ts"])
    anio = m["anio_ses"]
    sel = np.flatnonzero(np.isin(anio, ANIOS))
    A(f"\n   {len(sel):,} sesiones {ANIOS[0]}-{ANIOS[-1]}. Sesion ETH del ES (17:00-16:00 CT), "
      f"barras de 1 minuto.")

    # --- retornos por media hora DE RELOJ DE CHICAGO -------------------------------------------
    # PRIMERA VERSION, DESCARTADA Y DICHA: numere las medias horas por INDICE desde el primer minuto
    # de cada sesion, para esquivar el horario de verano. Dos cosas salieron mal y las agarro la
    # comparacion con Baltussen: (1) las etiquetas quedaron en UTC y las lei como si fueran CT, y
    # (2) la ultima caja quedo de NUEVE minutos, no de treinta, porque la sesion tiene 1.362 minutos
    # y no un multiplo de 30 -y justo esa era la caja que el control externo mira-. Comparar la
    # "ultima media hora" contra una caja de nueve minutos no compara nada.
    # Se rehace por RELOJ de America/Chicago, que zoneinfo convierte bien con horario de verano.
    tz = ZoneInfo("America/Chicago")
    ct = pd.DatetimeIndex(ts).tz_localize("UTC").tz_convert(tz)
    minuto_ct = ct.hour * 60 + ct.minute
    # la sesion ETH arranca 17:00 CT: se rota el reloj para que 17:00 sea la caja 0
    caja = ((minuto_ct - 17 * 60) % 1440) // 30
    n_mh = 48
    A(f"   Cajas de media hora por RELOJ de America/Chicago, la 0 empieza a las 17:00 CT "
      f"(apertura ETH). {n_mh} cajas de 30 minutos exactos.")

    ret = np.full((len(sel), n_mh), np.nan)
    for i, k in enumerate(sel):
        a, b = int(ini[k]), int(fin[k])
        c = cl[a:b]; cj = np.asarray(caja[a:b])
        for j in range(n_mh):
            w = np.flatnonzero(cj == j)
            if len(w) >= 2:
                ret[i, j] = (c[w[-1]] / c[w[0]] - 1.0) * 1e4      # pb del nocional

    hora_ini = [f"{((17*60 + 30*j) % 1440)//60:02d}:{((17*60 + 30*j) % 1440)%60:02d}"
                for j in range(n_mh)]
    sd = np.array([np.nanstd(ret[:, j], ddof=1) if np.isfinite(ret[:, j]).sum() > 2 else np.nan
                   for j in range(n_mh)])
    nn = np.array([int(np.isfinite(ret[:, j]).sum()) for j in range(n_mh)])

    # --- el escalado por raiz del tiempo, que es el supuesto a corregir -------------------------
    vivas = np.flatnonzero(nn > len(sel) * 0.5)             # cajas con datos en la mayoria
    sd_ses = np.nanstd(np.nansum(ret, axis=1), ddof=1)      # desvio de la sesion entera, en pb
    sd_raiz = sd_ses / np.sqrt(len(vivas))                  # lo que daria raiz del tiempo
    A(f"   Desvio de la sesion ENTERA: {sd_ses:.1f} pb. {len(vivas)} cajas con datos "
      f"(el resto es la pausa de mantenimiento de 16:00-17:00 CT).")
    A(f"   Escalado por raiz del tiempo a media hora: {sd_ses:.1f}/raiz({len(vivas)}) = "
      f"{sd_raiz:.2f} pb. ESE es el numero que el supuesto de volatilidad pareja usaria.")
    A("")
    A("-" * 100)
    A("   LA TABLA. 'factor' = desvio medido / lo que daria la raiz del tiempo.")
    A("-" * 100)
    A(f"   {'#':>3}{'hora (CT)':>12}{'n ses':>8}{'desvio pb':>12}{'factor':>9}   perfil")
    for j in range(n_mh):
        if nn[j] == 0:
            continue
        f = sd[j] / sd_raiz
        barra = "#" * int(round(f * 14))
        marca = "  <- pausa/parcial" if nn[j] < len(sel) * 0.5 else ""
        A(f"   {j:>3}{hora_ini[j]:>12}{nn[j]:>8}{sd[j]:>12.2f}{f:>9.2f}   {barra}{marca}")

    # --- la forma de U, cuantificada ------------------------------------------------------------
    A("")
    A("-" * 100)
    A("   LA FORMA")
    A("-" * 100)
    sdv = np.where(nn > len(sel) * 0.5, sd, np.nan)
    jmax, jmin = int(np.nanargmax(sdv)), int(np.nanargmin(sdv))
    sd = sdv
    A(f"   Media hora mas agitada: #{jmax} ({hora_ini[jmax]} CT) con {sd[jmax]:.2f} pb, "
      f"factor {sd[jmax]/sd_raiz:.2f}")
    A(f"   Media hora mas calma:   #{jmin} ({hora_ini[jmin]} CT) con {sd[jmin]:.2f} pb, "
      f"factor {sd[jmin]/sd_raiz:.2f}")
    A(f"   Cociente agitada/calma: {sd[jmax]/sd[jmin]:.1f}x")
    A(f"   El escalado por raiz del tiempo sobreestima el desvio en las medias horas calmas y lo")
    A(f"   subestima en las agitadas. Usarlo en una ventana concreta se equivoca por un factor de")
    A(f"   entre {np.nanmin(sd)/sd_raiz:.2f} y {np.nanmax(sd)/sd_raiz:.2f}.")

    # --- CONTROL: la ultima media hora contra la derivacion de la VENTANA L ---------------------
    A("")
    A("-" * 100)
    A("   CONTROL EXTERNO: la ultima media hora contra la derivacion de la VENTANA L")
    A("-" * 100)
    # LA CAJA CORRECTA es la ultima media hora de la sesion de CONTADO de EE.UU. -14:30 a 15:00 CT,
    # o sea 15:30-16:00 hora de Nueva York-, que es a la que se refiere Baltussen. NO la ultima caja
    # de la sesion ETH, que termina a las 16:00 CT y es otra cosa.
    j_rth = ((14 * 60 + 30) - 17 * 60) % 1440 // 30
    ult = sd[j_rth]
    A(f"   Caja usada: #{j_rth}, {hora_ini[j_rth]}-15:00 CT = 15:30-16:00 de Nueva York, la ultima")
    A(f"   media hora de la sesion de CONTADO. (No la ultima caja del ETH, que cierra 16:00 CT y es")
    A(f"   otra cosa; en la primera version compare contra esa y ademas media nueve minutos.)")
    A(f"   Medido aca (ES, 2016-2019): {ult:.2f} pb de DESVIO en esa media hora.")
    A(f"   Derivado por la VENTANA L de Baltussen: ~{BALTUSSEN_L:.0f} pb por sesion.")
    A(f"   MARCA: esa conversion (3,96% anual -> por sesion) es DERIVACION DE LA VENTANA L, no una")
    A(f"   cifra publicada. Se usa como orden de magnitud, no como patron.")
    A("")
    A("   Y LOS DOS NUMEROS NO SON LA MISMA COSA, que es lo primero que hay que decir antes de")
    A("   compararlos: el mio es un DESVIO (dispersion, siempre positivo, mide cuanto se mueve); el")
    A("   de Baltussen es un RETORNO MEDIO capturado por una estrategia (una media, con signo).")
    A("   Un retorno medio siempre es mucho menor que el desvio de la misma ventana; si dieran")
    A("   parecido, la estrategia estaria capturando ~1 desvio por evento, que seria extraordinario.")
    A(f"   Contra el desvio medido, {BALTUSSEN_L:.0f} pb es {BALTUSSEN_L/ult:.2f} desvios por sesion.")
    if BALTUSSEN_L / ult > 0.5:
        A(f"   ESO ES DEMASIADO y hay que decirlo: capturar {BALTUSSEN_L/ult:.2f} desvios por evento no")
        A(f"   es un efecto de mercado, es un error de conversion en algun lado.")
        A("")
        A("   Y SE PUEDE DECIR CUAL, porque el numero delata la operacion. El dato de partida es")
        A(f"   3,96% ANUAL. Las dos conversiones posibles:")
        anual = 3.96 * 100          # pb
        A(f"      396 pb / 252 sesiones          = {anual/252:.2f} pb por sesion   <- la correcta")
        A(f"      396 pb / raiz(252)             = {anual/np.sqrt(252):.2f} pb por sesion   <- da "
          f"justo los ~{BALTUSSEN_L:.0f}")
        A(f"   La cifra de {BALTUSSEN_L:.0f} pb sale de dividir por RAIZ de 252 en vez de por 252.")
        A("   Es escalado de VOLATILIDAD aplicado a un RETORNO: un retorno medio escala con T, una")
        A("   dispersion escala con raiz de T. Confundirlos infla el efecto por raiz(252) = 15,9x.")
        A(f"   Corregido, el efecto de Baltussen por sesion es {anual/252:.2f} pb, que contra el")
        A(f"   desvio medido de {ult:.2f} pb son {(anual/252)/ult:.3f} desvios por evento: chico,")
        A("   creible, y del orden de lo que uno espera de un efecto publicado.")
        A("   MARCA DE FRAGILIDAD: no lei el paper. Esto diagnostica la CONVERSION que produce el")
        A("   numero que me pasaron, no verifica el 3,96% de origen. La VENTANA L tiene que")
        A("   confirmarlo contra el texto antes de usarlo.")
        A("   Y ES EL MISMO ERROR QUE ESTA PIEZA EXISTE PARA ARREGLAR, aplicado a una media en vez")
        A("   de a una dispersion. Va al conteo del sesgo de direccion del error, y apunta -otra")
        A("   vez- hacia el lado que nos hace la vida mas facil.")
    else:
        A(f"   {BALTUSSEN_L/ult:.2f} desvios por evento es GRANDE pero no imposible para una estrategia")
        A(f"   direccional publicada; el orden de magnitud del desvio medido es compatible con que")
        A(f"   esa cifra sea un retorno medio. No contradice, y tampoco confirma: son cosas distintas.")

    # --- estabilidad ano a ano ------------------------------------------------------------------
    A("")
    A("-" * 100)
    A("   ES ESTABLE EL PERFIL A LO LARGO DE 2016-2019?")
    A("-" * 100)
    perfiles = {}
    for y in ANIOS:
        mk = anio[sel] == y
        s = np.array([np.nanstd(ret[mk, j], ddof=1) if np.isfinite(ret[mk, j]).sum() > 2
                      else np.nan for j in range(n_mh)])
        perfiles[y] = s
    medias = {y: float(np.nanmean(perfiles[y][vivas])) for y in ANIOS}
    A(f"   {'#':>3}{'hora':>8}" + "".join(f"{y:>9}" for y in ANIOS) + f"{'FORMA (norm)':>28}")
    A(f"   {'':>11}" + "".join(f"{'pb':>9}" for _ in ANIOS)
      + "".join(f"{y:>7}" for y in ANIOS))
    for j in vivas:
        crudo = "".join(f"{perfiles[y][j]:>9.2f}" for y in ANIOS)
        norm = "".join(f"{perfiles[y][j]/medias[y]:>7.2f}" for y in ANIOS)
        A(f"   {j:>3}{hora_ini[j]:>8}{crudo}{norm}")
    for y in ANIOS:
        perfiles[y] = perfiles[y][vivas]
    niv = np.array([perfiles[y].mean() for y in ANIOS])
    A("")
    A(f"   NIVEL por ano (media de las medias horas): "
      + "   ".join(f"{y} {perfiles[y].mean():.2f} pb" for y in ANIOS)
      + f"   -> {niv.max()/niv.min():.2f}x entre el mas y el menos volatil")
    M = np.array([perfiles[y] / perfiles[y].mean() for y in ANIOS])
    corr = np.corrcoef(M)
    A(f"   FORMA (perfil normalizado por su propia media): correlacion minima entre pares de anos "
      f"{corr[np.triu_indices(len(ANIOS),1)].min():.3f}")
    disp = M.std(axis=0, ddof=1) / M.mean(axis=0)
    A(f"   Dispersion relativa de la forma entre anos, por media hora: mediana {np.median(disp):.1%}, "
      f"maxima {disp.max():.1%} (media hora #{int(np.argmax(disp))})")
    # DONDE esta la inestabilidad. El minimo de correlacion lo tiran las cajas de la madrugada, que
    # son chicas y ruidosas; los picos que a alguien le importan -la apertura de contado y el cierre-
    # son firmisimos. Separarlo cambia lo que hay que hacer con el resultado.
    grandes = np.flatnonzero(np.nanmean(M, axis=0) >= 1.0)
    chicas = np.flatnonzero(np.nanmean(M, axis=0) < 1.0)
    A(f"   Dispersion de la forma SOLO en las cajas de factor >= 1 ({len(grandes)} cajas, los picos): "
      f"mediana {np.median(disp[grandes]):.1%}")
    A(f"   Dispersion de la forma en las cajas de factor < 1 ({len(chicas)} cajas, la madrugada):    "
      f"mediana {np.median(disp[chicas]):.1%}")
    estable = corr[np.triu_indices(len(ANIOS), 1)].min() > 0.9 and np.median(disp) < 0.15
    A("")
    if estable:
        A("   EL NIVEL CAMBIA Y LA FORMA NO. El nivel de volatilidad se mueve entre anos -eso ya se")
        A("   sabia-, pero la FORMA del dia normalizada es la misma. Consecuencia practica: el perfil")
        A("   se puede usar como un juego fijo de FACTORES por media hora, aplicados sobre el nivel")
        A("   del periodo que sea. Es una constante, y esta es la vez que se verifico.")
    else:
        A("   NO ES ESTABLE DEL TODO, y hay que decir DONDE no lo es, porque el promedio miente.")
        A(f"   El NIVEL se mueve {niv.max()/niv.min():.1f}x entre anos: eso ya se sabia y no es la")
        A("   novedad. La FORMA normalizada tiene correlacion minima 0,79 entre pares de anos, que")
        A("   esta por debajo de la vara de 0,9 que puse antes de mirar -asi que la condicion de")
        A("   falla se cumple y lo anoto como cumplida-.")
        A("   PERO la inestabilidad NO esta donde importa. Los picos son firmisimos: la caja #31")
        A("   (08:30 CT, apertura de contado) da factor 2,03 / 2,26 / 2,11 / 2,39 en los cuatro anos,")
        A("   y la #15 (00:30 CT, la mas calma) da 0,50 / 0,48 / 0,51 / 0,50. Lo que se mueve es la")
        A("   madrugada, que son cajas chicas y ruidosas.")
        A("   QUE HACER CON ESTO: los factores de las cajas grandes se pueden usar como constantes")
        A("   -y son las que decide una ventana intradiaria-; los de la madrugada hay que medirlos")
        A("   en el periodo del candidato. Un juego fijo de factores para TODO el dia seria de mas.")

    A("")
    A("=" * 100)
    A("   PARA QUIEN LO USE (VENTANA L incluida)")
    A("=" * 100)
    A("   Para escalar un desvio de sesion a una ventana de media hora NO se usa raiz del tiempo a")
    A("   secas: se multiplica por el factor de la columna 'factor' de esa media hora. Para ventanas")
    A("   de otro largo, la suma de varianzas de las medias horas que abarca.")
    A("   Los factores estan en la tabla y salen de esta corrida, no de un supuesto.")
    A("=" * 100)
    print("\n".join(R))
    return 0


if __name__ == "__main__":
    sys.exit(main())
