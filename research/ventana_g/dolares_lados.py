"""
VENTANA G - LA VARIANZA DEL MARCO NUEVO, POR LADO Y COMBINADA. Y un error mio de factor 2.

NO GASTA CARTUCHO. K = 261.

DOS COSAS QUE HAY QUE ARREGLAR ANTES DE PUBLICAR EL CRITERIO NUEVO.

(1) ERROR DE CONTABILIDAD, mio. En dolares_por_tiempo.py la columna "$/operacion" divide
    dolares-de-un-contrato por operaciones-de-LOS-DOS-LADOS. Esta subestimada por 2. Los
    dolares por sesion estan bien; el por-operacion no.

(2) DECISION DE VARIANZA que estaba tomada sin decirlo. Al promediar largo y corto se hace
    una combinacion ANTITETICA: los dos lados estan muy anticorrelacionados y el promedio
    cancela casi toda la varianza. Eso esta bien para medir la MEDIA -es reduccion de
    varianza legitima- pero la MDE que sale de ahi es la del INSTRUMENTO DE MEDICION, no el
    riesgo de alguien que opera un solo lado. Un candidato direccional elige lado y enfrenta
    la varianza de un lado solo.

    Si no se separa, el criterio nuevo saldria demasiado optimista. Se mide, no se supone.

CONTROL, con su condicion de falla: la media del combinado tiene que ser el promedio exacto
de las medias de los dos lados, porque es lo que es por construccion.
   QUE LO HARIA FALLAR: que no coincida. Seria un error de contabilidad en el promedio.
   Y AVISO: ese control es de CODIGO, no de datos. No puede fallar por como sea el mercado.
   El que si informa es la comparacion de DESVIOS, que no esta forzada por nada.
"""
import numpy as np

from aritmetica import C1_POR_MINI
from dolares_por_tiempo import MEDIA_EXCESO, PUNTO_ES, SESION, cortes, secuencial
from linea_base import cargar

CELDAS = [(5, 20), (20, 10)]
Z = 1.6448536269514722 + 0.8416212335729143   # alfa 0,05 una cola, potencia 80%
PRESUPUESTOS_OP = [250, 1000, 3000]


def main():
    print("=" * 100)
    print("LA VARIANZA DEL MARCO NUEVO, POR LADO Y COMBINADA")
    print("NO GASTA CARTUCHO. K = 261.")
    print("=" * 100)

    cl, hi, lo, con = cargar()
    ini, fin = cortes(len(cl), SESION)
    ns = len(ini)
    print(f"\n   ES 1-min 2016-2019, {ns:,} sesiones de {SESION} barras. 1 mini ES.")
    print(f"   Neto de comision MEDIDA ${C1_POR_MINI} y deslizamiento MEDIDO en el stop.\n")

    print(f"   {'celda':>10}{'serie':>12}{'$/sesion':>11}{'desvio/ses':>12}{'error':>9}"
          f"{'en errores':>12}{'op/sesion':>11}{'$/operacion':>13}")
    guardado = {}
    for T, S in CELDAS:
        exc = MEDIA_EXCESO[S]
        vs, nops = {}, {}
        for lado in ("largo", "corto"):
            v, no, na = secuencial(cl, hi, lo, ini, fin, T, S, lado, exceso=exc,
                                   c1=C1_POR_MINI)
            vs[lado], nops[lado] = v, no
        comb = (vs["largo"] + vs["corto"]) / 2.0
        op_lado = (nops["largo"] + nops["corto"]) / 2.0 / ns
        for nom, v in (("largo", vs["largo"]), ("corto", vs["corto"]),
                       ("combinado", comb)):
            sd = v.std(ddof=1)
            se = sd / np.sqrt(ns)
            print(f"   {f'{T}pt:{S}pt':>10}{nom:>12}{v.mean():>+11.2f}{sd:>12.2f}{se:>9.2f}"
                  f"{v.mean()/se:>+12.1f}{op_lado:>11.2f}{v.mean()/op_lado:>+13.2f}")
        guardado[(T, S)] = dict(comb=comb, largo=vs["largo"], corto=vs["corto"],
                                op_lado=op_lado)
        # control de codigo, marcado como tal
        ok = abs(comb.mean() - (vs["largo"].mean() + vs["corto"].mean()) / 2) < 1e-9
        print(f"   {'':>10}{'control':>12}  media combinada = promedio de las dos: "
              f"{'OK' if ok else 'MAL'}  (control de CODIGO, no puede fallar por el mercado)")
        print()

    print("=" * 100)
    print("CUANTO CUESTA LA COMBINACION ANTITETICA, Y A QUIEN LE SIRVE")
    print("=" * 100)
    print(f"\n   {'celda':>10}{'desvio 1 lado':>15}{'desvio combinado':>19}"
          f"{'reduccion':>11}")
    for T, S in CELDAS:
        g = guardado[(T, S)]
        sd1 = (g["largo"].std(ddof=1) + g["corto"].std(ddof=1)) / 2
        sdc = g["comb"].std(ddof=1)
        print(f"   {f'{T}pt:{S}pt':>10}{sd1:>14.2f}${sdc:>18.2f}${sd1/sdc:>10.1f}x")
    print("\n   La combinacion antitetica sirve para MEDIR la esperanza de una entrada al")
    print("   azar. NO sirve para dimensionar a un candidato DIRECCIONAL, que elige lado y")
    print("   enfrenta el desvio de un lado solo.")

    print("\n" + "=" * 100)
    print("EL CRITERIO NUEVO, EN DOLARES, CON LAS DOS VARIANZAS")
    print("=" * 100)
    print("\n   'hay que superar' = lo que un candidato tiene que agregar por sesion para")
    print("   llegar a cero, ya restado el sesgo de sobrepaso del propio marco.")
    print("   El presupuesto se cuenta en OPERACIONES para poder comparar contra la tabla")
    print("   vieja del marco de tasas.\n")
    # sesgo del marco, medido en sesgo_marco.py: o = 0,0642 pt, sesgo por op = o*(1-2p)
    O_SOBREPASO = 0.0642
    print(f"   {'celda':>10}{'piso $/ses':>12}{'presup. op':>12}{'sesiones':>10}"
          f"{'MDE antitet.':>14}{'razon':>8}{'MDE 1 lado':>13}{'razon':>8}")
    for T, S in CELDAS:
        g = guardado[(T, S)]
        p = S / (S + T)
        sesgo_ses = O_SOBREPASO * (1 - 2 * p) * PUNTO_ES * g["op_lado"]
        piso = -(g["comb"].mean() - sesgo_ses)
        sdc = g["comb"].std(ddof=1)
        sd1 = (g["largo"].std(ddof=1) + g["corto"].std(ddof=1)) / 2
        for nop in PRESUPUESTOS_OP:
            nses = nop / g["op_lado"]
            mdec = Z * sdc / np.sqrt(nses)
            mde1 = Z * sd1 / np.sqrt(nses)
            print(f"   {f'{T}pt:{S}pt':>10}{piso:>+11.2f}${nop:>12,}{nses:>10.0f}"
                  f"{mdec:>13.2f}${mdec/piso:>8.2f}{mde1:>12.2f}${mde1/piso:>8.2f}")
        print()
    print("   'razon' = MDE / piso. Por debajo de 1 el equilibrio es demostrable con ese")
    print("   presupuesto; por encima, no. En el marco de TASAS esta razon daba 2,62 para")
    print("   5pt:20pt con 1.000 operaciones, y ningun bracket llegaba.")
    return guardado


if __name__ == "__main__":
    main()
