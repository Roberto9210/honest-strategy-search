"""
VENTANA G - EL MARCO NUEVO A PRUEBA: dolares por unidad de tiempo contra tasas de acierto.

NO GASTA CARTUCHO. K = 261. Es la validacion de un metodo de medicion contra una conclusion
ya publicada. No hay hipotesis de mercado contra el alfa heredado, no se elige entre
candidatas, no se declara ninguna regla de operacion. La caja sellada (2020-01-02 ->
2026-08-19) no se toca: todo es 2016-2019.

QUE CONCLUSION SE REHACE, Y POR QUE ESA. Se rehace el CRITERIO publicado:

    "celda 5pt:20pt via 1 mini, costo medido $5,76 ida y vuelta. Un candidato necesita
     81,2% de aciertos contra el 80,0% que da la moneda: +1,2 puntos de ventaja real."
    (CRITERIO_RESULTADO.md, seccion "Veredicto: ahora SI hay criterio")

Es la que se elige porque es donde el marco de tasas trabajo MAS duro, no una trivial: para
llegar a ese numero hicieron falta la biseccion del acierto requerido, la separacion de los
dos criterios (i) por operacion y (ii) por intento, la elasticidad de barrera de 7,9x que
convierte 1,024 en 1,193, la media medida del exceso de deslizamiento, los dos filtros de
terreno y la verificacion de la via de ejecucion en minis. Ademas es la conclusion que se
publico como EL entregable de la ventana. Si el marco contamina algo, contamina esto.

EL MARCO NUEVO, en una linea: no se cuentan aciertos, se suman DOLARES, y ninguna operacion
se descarta. La que no resolvio al corte se marca a mercado. La unidad de tiempo es la
SESION, que es ademas la unidad en la que las firmas miden todo.

TRES COSAS QUE ARREGLA DE UNA:
  1. No hay nula que calibrar. Cero es cero. Las cuatro perillas medidas del marco de tasas
     -horizonte, tratamiento de las no resueltas, estructura serial, forma de la barra- no
     tienen donde entrar.
  2. No hay censura. La operacion abierta al corte vale su marca a mercado, no se borra.
  3. Las operaciones son SECUENCIALES y por lo tanto NO SE PISAN. Eso elimina de raiz el
     problema del error estandar que en esta ventana llego a ser 5x, porque cada sesion es
     una observacion independiente de verdad.

PREDICCION SELLADA, escrita antes de correr:
  - El bruto con entradas al azar sobre ES real da levemente POSITIVO (ES subio 2016-2019).
  - Neto de comision medida y deslizamiento medido da NEGATIVO.
  - O sea: el marco de tasas decia que una entrada al azar SUPERA el equilibrio (85,2%
    observado contra 81,2% de equilibrio) y el marco de dolares tiene que decir que PIERDE.
    EL SIGNO SE MUEVE. Si no se mueve, el marco de tasas era inofensivo y lo digo.

CONTROL, con su condicion de falla declarada. Sobre datos SIN ventaja -bootstrap IID sin
drift- y con costo CERO, el marco nuevo tiene que dar esperanza CERO dentro de su error.
   QUE LO HARIA FALLAR: una esperanza sistematicamente distinta de cero. Significaria que el
   marco nuevo tiene sesgo propio y no resolvimos nada.
   QUE LO HACE CAPAZ DE FALLAR, que es lo que ya me mordio dos veces: no es una identidad de
   construccion -el resultado depende de los datos- y su nula TIENE varianza, medida entre
   sesiones y entre series. Y para demostrar que tiene dientes se corre a proposito el mismo
   control con el defecto viejo puesto de nuevo (CONTROL B: descartar las no resueltas en
   vez de marcarlas a mercado). Ese TIENE que fallar. Si el control A pasa y el B falla, el
   control discrimina; si pasan los dos, no mide nada y hay que tirarlo.

VERIFICACION EXTRA DEL ERROR ESTANDAR. Se compara el error entre sesiones de UNA serie
contra la dispersion entre K series independientes. Si coinciden, el error del marco nuevo
es honesto. Es la misma comprobacion que destapo el 5x, aplicada al metodo nuevo antes de
recomendarlo.
"""
import numpy as np

from aritmetica import C1_POR_MINI
from linea_base import cargar
from sintetico import armar, bootstrap, tripletes

SESION = 1380
PUNTO_ES = 50.0
MEDIA_EXCESO = {10: 0.722, 20: 0.982}
CELDAS = [(5, 20), (20, 10)]
K_SINT = 10
SEMILLA = 20260904

# La conclusion publicada que se rehace, en sus propias unidades.
EQUILIBRIO_TASA = 81.2      # % de acierto que pide el equilibrio por operacion
MONEDA_TASA = 80.0          # % que le atribuia la moneda
OBSERVADO_TASA = 85.2       # % que da una entrada AL AZAR, medido (salida_linea_base.txt)


def secuencial(cl, hi, lo, ini, fin, T, S, lado, exceso=0.0, c1=0.0, m2m=True):
    """Replay SECUENCIAL: una posicion por vez, se abre en la barra siguiente al cierre de
    la anterior, y al corte de sesion lo que quede abierto se marca a mercado.

    Devuelve dolares por sesion (un vector, una entrada por sesion) y el conteo de
    operaciones. Las sesiones no se pisan: son observaciones independientes.
    """
    sgn = 1.0 if lado == "largo" else -1.0
    por_sesion = np.zeros(len(ini))
    n_op = n_abierta = 0
    for k, (a, b) in enumerate(zip(ini, fin)):
        pos = a
        acum = 0.0
        while pos < b - 1:
            e = cl[pos]
            obj, stp = e + sgn * T, e - sgn * S
            h, l = hi[pos + 1:b], lo[pos + 1:b]
            if lado == "largo":
                toca_o, toca_s = h >= obj, l <= stp
            else:
                toca_o, toca_s = l <= obj, h >= stp
            algo = toca_o | toca_s
            if not algo.any():
                # abierta al corte: vale su marca a mercado, NO se descarta
                n_op += 1
                n_abierta += 1
                if m2m:
                    acum += (sgn * (cl[b - 1] - e)) * PUNTO_ES - c1
                break
            j = int(np.argmax(algo))
            n_op += 1
            if toca_o[j] and not toca_s[j]:
                r = T
            else:
                # stop, y la barra ambigua se cuenta como perdida: misma convencion que replica
                r = -(S + exceso)
            acum += r * PUNTO_ES - c1
            pos = pos + 1 + j + 1
        por_sesion[k] = acum
    return por_sesion, n_op, n_abierta


def resumen(v, n_op, n_ses):
    m, se = v.mean(), v.std(ddof=1) / np.sqrt(len(v))
    return dict(dia=m, se=se, z=m / se if se else 0.0, total=v.sum(),
                op_ses=n_op / n_ses, por_op=v.sum() / n_op if n_op else float("nan"))


def cortes(n, largo=SESION):
    ini = np.arange(0, n - largo, largo)
    return ini, ini + largo


def main():
    print("=" * 100)
    print("EL MARCO NUEVO A PRUEBA - dolares por sesion contra tasas de acierto")
    print("NO GASTA CARTUCHO. K = 261. La caja sellada no se toca.")
    print("=" * 100)

    cl, hi, lo, con = cargar()
    n = len(cl)
    # las sesiones reales: el corte esta donde cambia el bloque de 1380, se usa el mismo
    # criterio que en toda la ventana (contrato unico por sesion, series concatenadas)
    ini, fin = cortes(n)
    print(f"\n   ES 1-min 2016-2019, {n:,} barras, {len(ini):,} sesiones de {SESION} barras.")
    print(f"   1 mini ES = ${PUNTO_ES:.0f}/punto. Comision MEDIDA ${C1_POR_MINI}/ida y vuelta.")
    print(f"   Exceso de deslizamiento MEDIDO: {MEDIA_EXCESO} puntos segun distancia del stop.")

    # ------------------------------------------------------------------------------------
    print("\n" + "=" * 100)
    print("CONTROL A - datos SIN ventaja, costo CERO, con marca a mercado: debe dar $0")
    print("   QUE LO HARIA FALLAR: esperanza sistematicamente distinta de cero.")
    print("CONTROL B - el mismo, con el defecto viejo puesto de nuevo: descartar las no")
    print("   resueltas en vez de marcarlas. ESTE TIENE QUE FALLAR, y si no falla el")
    print("   control A no discrimina y hay que tirarlo.")
    print("=" * 100)
    d, up, dn = tripletes(cl, hi, lo, con)
    mu = d.mean()
    dc, upc, dnc = d - mu, up - mu, dn - mu
    ini_s, fin_s = cortes(n)
    medias = {}
    print(f"\n   {'celda':>10}{'modo':>22}{'$/sesion':>11}{'error':>9}{'en errores':>12}"
          f"{'$/operacion':>13}{'op/sesion':>11}{'abiertas':>10}{'veredicto':>11}")
    okA = okB = True
    for T, S in CELDAS:
        for modo, m2m in (("A: con marca a mercado", True), ("B: descartando abiertas", False)):
            vs, zs = [], []
            for k in range(K_SINT):
                rg = np.random.default_rng(SEMILLA + 7919 * k)
                c2, h2, l2 = armar(*bootstrap(dc, upc, dnc, n, rg))
                acc = np.zeros(len(ini_s)); nop = nab = 0
                for lado in ("largo", "corto"):
                    v, no, na = secuencial(c2, h2, l2, ini_s, fin_s, T, S, lado, m2m=m2m)
                    acc += v / 2.0; nop += no; nab += na
                vs.append(acc.mean())
                zs.append(resumen(acc, nop, len(ini_s)))
                del c2, h2, l2
            m = float(np.mean(vs))
            se_entre = float(np.std(vs, ddof=1))
            z = m / se_entre if se_entre else 0.0
            medias[(T, S, m2m)] = (m, se_entre, zs[0])
            bien = abs(z) <= 3.0
            if m2m:
                okA &= bien
            else:
                okB &= (not bien)
            print(f"   {f'{T}pt:{S}pt':>10}{modo:>22}{m:>+11.2f}{se_entre:>9.2f}{z:>+12.1f}"
                  f"{zs[0]['por_op']:>13.3f}{zs[0]['op_ses']:>11.2f}"
                  f"{nab/nop*100:>9.1f}%"
                  f"{('CERO' if bien else 'SESGADO'):>11}")
    print(f"\n   CONTROL A (debe dar cero):        {'PASADO' if okA else 'FALLADO'}")
    print(f"   CONTROL B (debe dar sesgado):     {'PASADO' if okB else 'FALLADO'}")
    print(f"   -> el control {'DISCRIMINA' if okA and okB else 'NO DISCRIMINA'}: "
          f"pasa con el metodo bueno y falla con el defecto viejo puesto a proposito.")

    # ------------------------------------------------------------------------------------
    print("\n" + "=" * 100)
    print("EL ERROR ESTANDAR DEL MARCO NUEVO ES HONESTO? (la comprobacion que destapo el 5x)")
    print("   Se compara el error ENTRE SESIONES de una serie contra la dispersion ENTRE")
    print("   K series independientes. Si coinciden, el error es honesto.")
    print("   QUE LO HARIA FALLAR: que el de entre sesiones sea mucho menor que el de entre")
    print("   series, como pasaba con el binomial en el marco de tasas.")
    print("=" * 100)
    print(f"\n   {'celda':>10}{'entre sesiones':>17}{'entre series':>15}{'cociente':>11}"
          f"{'veredicto':>11}")
    okse = True
    for T, S in CELDAS:
        m, se_entre, uno = medias[(T, S, True)]
        coc = se_entre / uno["se"] if uno["se"] else float("nan")
        bien = 0.5 <= coc <= 2.0
        okse &= bien
        print(f"   {f'{T}pt:{S}pt':>10}{uno['se']:>16.2f}${se_entre:>14.2f}${coc:>11.2f}"
              f"{('OK' if bien else 'MAL'):>11}")
    print(f"\n   {'HONESTO' if okse else 'NO HONESTO'}: en el marco de tasas este cociente "
          f"llegaba a 5,3.")

    # ------------------------------------------------------------------------------------
    print("\n" + "=" * 100)
    print("LA CONCLUSION REHECHA - celda 5pt:20pt sobre ES REAL")
    print("=" * 100)
    print(f"\n   {'celda':>10}{'costo':>26}{'$/sesion':>11}{'error':>9}{'en errores':>12}"
          f"{'$/operacion':>13}{'op/sesion':>11}{'signo':>10}")
    resu = {}
    for T, S in CELDAS:
        for etiqueta, exc, c1 in (("bruto (sin costo)", 0.0, 0.0),
                                  ("neto, comision medida", 0.0, C1_POR_MINI),
                                  ("neto, comision + desliz.", MEDIA_EXCESO[S], C1_POR_MINI)):
            acc = np.zeros(len(ini)); nop = 0
            for lado in ("largo", "corto"):
                v, no, na = secuencial(cl, hi, lo, ini, fin, T, S, lado, exceso=exc, c1=c1)
                acc += v / 2.0; nop += no
            r = resumen(acc, nop, len(ini))
            resu[(T, S, etiqueta)] = r
            print(f"   {f'{T}pt:{S}pt':>10}{etiqueta:>26}{r['dia']:>+11.2f}{r['se']:>9.2f}"
                  f"{r['z']:>+12.1f}{r['por_op']:>13.2f}{r['op_ses']:>11.2f}"
                  f"{('POSITIVO' if r['dia'] > 0 else 'NEGATIVO'):>10}")

    # ------------------------------------------------------------------------------------
    T, S = 5, 20
    r = resu[(T, S, "neto, comision + desliz.")]
    b = resu[(T, S, "bruto (sin costo)")]
    print("\n" + "=" * 100)
    print("SE MUEVE EL SIGNO?")
    print("=" * 100)
    print(f"\n   MARCO DE TASAS, celda 5pt:20pt:")
    print(f"      equilibrio por operacion .......... {EQUILIBRIO_TASA:.1f}%")
    print(f"      entrada AL AZAR, medida ........... {OBSERVADO_TASA:.1f}%")
    print(f"      -> la moneda SUPERA el equilibrio por "
          f"{OBSERVADO_TASA-EQUILIBRIO_TASA:+.1f} puntos: POSITIVO")
    print(f"\n   MARCO DE DOLARES, la misma celda, las mismas entradas al azar:")
    print(f"      bruto ............................. ${b['dia']:+.2f} por sesion")
    print(f"      neto de comision y deslizamiento .. ${r['dia']:+.2f} por sesion "
          f"(error ${r['se']:.2f}, {r['z']:+.1f} errores)")
    print(f"      por operacion ..................... ${r['por_op']:+.2f}")
    movio = (OBSERVADO_TASA - EQUILIBRIO_TASA > 0) != (r["dia"] > 0)
    print(f"\n   EL SIGNO {'SE MUEVE' if movio else 'NO SE MUEVE'}.")

    # ------------------------------------------------------------------------------------
    print("\n" + "=" * 100)
    print("EL CRITERIO NUEVO - que tiene que prometer un candidato, en dolares")
    print("=" * 100)
    print(f"\n   {'celda':>10}{'hay que superar':>18}{'error por sesion':>19}"
          f"{'MDE 250 ses':>14}{'MDE 1.000 ses':>15}{'MDE 3.000 ses':>15}")
    for T, S in CELDAS:
        r = resu[(T, S, "neto, comision + desliz.")]
        sd = r["se"] * np.sqrt(len(ini))
        for nn, et in ((250, "250"), (1000, "1.000"), (3000, "3.000")):
            pass
        mdes = [2.487 * sd / np.sqrt(nn) for nn in (250, 1000, 3000)]
        print(f"   {f'{T}pt:{S}pt':>10}{-r['dia']:>+17.2f}${sd/np.sqrt(len(ini)):>18.2f}"
              f"{mdes[0]:>13.2f}${mdes[1]:>14.2f}${mdes[2]:>14.2f}$")
    print("\n   'hay que superar' = lo que un candidato tiene que agregar por sesion solo")
    print("   para llegar a cero. MDE con alfa 0,05 una cola y potencia 80% (z 1,645+0,842).")
    return resu


if __name__ == "__main__":
    main()
