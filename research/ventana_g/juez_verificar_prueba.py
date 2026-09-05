"""
VENTANA G - EJERCITAR LA RUTA --verificar: el candado que guarda 2019.

NO GASTA CARTUCHO. K = 261. Candidato SINTETICO sin ventaja; se prueba el mecanismo, no el mercado.
La caja sellada (2020-2026) no se toca: 2019 es el periodo de VERIFICACION reservado, no la caja.

POR QUE. La ruta --verificar es el candado principal del juez -guarda 2019 hasta que el resultado de
trabajo (2016-2018) este anotado en el registro- y era la unica parte del juez SIN UNA SOLA CORRIDA
encima. "Escrito" y "alguna vez ejercitado" son dos numeros distintos, y hasta ahora este candado
tenia el primero y no el segundo.

SE PRUEBA EN LAS DOS DIRECCIONES, porque un candado que solo se probo abriendolo con la llave correcta
no esta probado:
  (1) CERRADO: --verificar en un registro LIMPIO (sin trabajo anotado) -> tiene que NEGARSE.
  (2) sin --verificar -> juzga trabajo, lo anota, y RETIENE 2019 avisando como verlo.
  (3) ABIERTO: --verificar con el trabajo ya anotado -> tiene que MOSTRAR 2019, con informe completo.

LO HARIA FALLAR: que (1) muestre 2019 sin el trabajo anotado, o que (3) salga vacio o mal formado.
"""
import os
import sys
import tempfile

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import juez as J            # noqa: E402
import juez_controles as C  # noqa: E402

NPERM = int(os.environ.get("JUEZ_NPERM", "150"))


def main():
    print("=" * 98)
    print("EJERCITAR LA RUTA --verificar: el candado que guarda 2019, probado en las DOS direcciones")
    print("NO GASTA CARTUCHO. K = 261. La caja sellada (2020-2026) no se toca.")
    print("=" * 98)
    m = J.cargar_mercado()
    # candidato SIN ventaja que abarca trabajo (2016-2018) Y verificacion (2019)
    idx = C.grilla(m, [2016, 2017, 2018, 2019])
    rng = np.random.default_rng(20260904)
    lado = rng.random(len(idx)) < 0.5
    cand = C.candidato("prueba_verificar", m, idx, lado)
    anios = m["anio_ses"][m["ses_de"][idx]]
    print(f"\n   candidato sin ventaja: {len(idx):,} operaciones, "
          f"{int((anios <= 2018).sum()):,} en TRABAJO 2016-2018 y {int((anios == 2019).sum()):,} en 2019.")

    reg = os.path.join(tempfile.gettempdir(), "prueba_verificar.jsonl")
    if os.path.exists(reg):
        os.remove(reg)

    ok = {}
    # ---------------------------------------------------------------- (1) candado CERRADO
    print("\n(1) CANDADO CERRADO: --verificar sobre registro LIMPIO (trabajo NO anotado).")
    print("    Tiene que NEGARSE a mostrar 2019.")
    s1 = J.juzgar(cand, m, npermuta=NPERM, registro=reg, verificar=True)
    v1 = s1["verificacion"]
    mostro1 = "verificacion" in s1["periodos"]
    print(f"    verificacion: {v1[:120]}")
    print(f"    mostro 2019? {'SI - FALLA' if mostro1 else 'NO - el candado aguanta'}")
    ok["1 cerrado"] = (not mostro1) and v1.startswith("RETENIDO")

    # ---------------------------------------------------------------- (2) sin --verificar
    print("\n(2) SIN --verificar: juzga trabajo, lo anota, y retiene 2019 avisando como verlo.")
    s2 = J.juzgar(cand, m, npermuta=NPERM, registro=reg, verificar=False)
    v2 = s2["verificacion"]
    mostro2 = "verificacion" in s2["periodos"]
    print(f"    veredicto TRABAJO: {s2['periodos']['trabajo']['veredicto']}")
    print(f"    verificacion: {v2[:120]}")
    ok["2 retiene"] = (not mostro2) and v2.startswith("RETENIDO")

    # ---------------------------------------------------------------- (3) candado ABIERTO
    print("\n(3) CANDADO ABIERTO: --verificar con el trabajo YA anotado. Tiene que MOSTRAR 2019.")
    s3 = J.juzgar(cand, m, npermuta=NPERM, registro=reg, verificar=True)
    v3 = s3["verificacion"]
    mostro3 = "verificacion" in s3["periodos"]
    print(f"    verificacion: {v3[:120]}")
    print(f"    mostro 2019? {'SI' if mostro3 else 'NO - FALLA'}")
    ok["3 abierto"] = mostro3 and v3.startswith("MOSTRADO")

    # ---------------------------------------------------------------- el informe sale bien?
    print("\n(4) EL INFORME DE VERIFICACION, tal cual lo imprime el juez:")
    txt = J.informe(s3)
    lineas = txt.splitlines()
    i = next((k for k, ln in enumerate(lineas) if "VERIFICACION 2019" in ln), None)
    bien = False
    if i is not None:
        bloque = lineas[i:i + 22]
        for ln in bloque:
            print(f"      {ln}")
        # el bloque tiene que traer el veredicto y la tabla de dolares, no estar vacio
        bien = (any("VEREDICTO (VERIFICACION 2019)" in ln for ln in lineas)
                and any("OBSERVADO (neto)" in ln for ln in bloque)
                and any("nula" in ln for ln in bloque))
    print(f"\n    informe de verificacion completo (veredicto + tabla + nulas): "
          f"{'SI' if bien else 'NO - FALLA'}")
    ok["4 informe"] = bien

    # ---------------------------------------------------------------- resumen
    print("\n" + "=" * 98)
    for k, v in ok.items():
        print(f"   {k:<12} {'PASADO' if v else 'FALLADO'}")
    todos = all(ok.values())
    print(f"\n   EL CANDADO DE 2019 {'FUNCIONA EN LAS DOS DIRECCIONES' if todos else 'FALLA'}: "
          f"se niega sin el trabajo anotado y abre cuando esta.")
    print("=" * 98)
    if not todos:
        raise SystemExit("FALLO: la ruta --verificar no se comporta como dice el codigo")


if __name__ == "__main__":
    main()
