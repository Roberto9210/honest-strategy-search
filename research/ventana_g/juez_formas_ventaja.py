"""
VENTANA G - EL JUEZ CONTRA OTRAS FORMAS DE VENTAJA: mide el punto ciego, no lo declara.

NO GASTA CARTUCHO. K = 261. Candidatos SINTETICOS de propiedades conocidas; se mide el instrumento,
no el mercado. No se elige entre candidatas reales ni se declara regla. La caja sellada no se toca.

EL PROBLEMA. Los ocho controles inyectan SIEMPRE la misma clase de ventaja: elegir el lado que resulto
mejor con probabilidad q. Direccional, por operacion, sin estructura temporal. Un candidato real puede
tener ventaja de otra forma, y si el juez no la reconoce el error es DESCARTAR ALGO BUENO, que es el
peor de los dos errores. Aca se inyectan dos formas nuevas y se mide si el instrumento las recupera.

FORMA A - VENTAJA DE TIMING. El candidato NO sabe el lado (moneda), sabe CUANDO: opera solo en el
tercio de ranuras donde el promedio de los dos lados es mejor. Es la forma que el juez declaro como
falso negativo estructural (la nula de SIGNO no puede verla, porque conserva las ranuras y solo da
vuelta el lado, y el promedio de los dos lados no cambia). Aca se mide DE QUE TAMANO es ese punto
ciego, en vez de declararlo.

FORMA B - VENTAJA DE TAMANO. El candidato acierta el lado como una moneda, pero ARRIESGA MAS cuando
tiene razon: en las ranuras donde su lado resulto el mejor, duplica la entrada (dos operaciones en la
misma barra = doble exposicion). La tasa de acierto es 50%, la esperanza no.

NO SE AGREGA UNA TERCERA, y se dice por que: la unica que faltaria es una ventaja de SALIDA (elegir
cuando cerrar), y el juez la prohibe por construccion -la regla de salida se DECLARA y el juez la
aplica igual a todas las operaciones-, asi que no hay forma de expresarla en su entrada.

PARA CADA UNA se reporta: la ventaja REALIZADA inyectada (calculada exacta, no la nominal), lo que
recupera cada nula, y el veredicto. Recupera / subestima / no la ve, con numero.
"""
import os
import sys
import tempfile

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import juez as J            # noqa: E402
import juez_controles as C  # noqa: E402

NPERM = int(os.environ.get("JUEZ_NPERM", "200"))
SEMILLA = 20260904


def informe_forma(nombre, cand, m, inyectada, comentario):
    reg = os.path.join(tempfile.gettempdir(), f"forma_{nombre}.jsonl")
    if os.path.exists(reg):
        os.remove(reg)
    try:
        s = J.juzgar(cand, m, npermuta=NPERM, registro=reg)
    except (J.NoMedible, J.Rechazo) as e:
        print(f"   [{nombre}] {type(e).__name__}: {str(e).splitlines()[0][:110]}")
        return None
    r = s["periodos"]["trabajo"]
    A = r["nulas"]["A rotacion"]; B = r["nulas"]["B signo"]
    print(f"\n   [{nombre}] veredicto: {r['veredicto']}")
    print(f"      ventaja INYECTADA (realizada, exacta): {inyectada:+.2f} $/sesion")
    print(f"      recupera nula A rotacion: {A[2]:+8.2f}  ({A[2]/inyectada*100:5.0f}% de la inyectada)  {A[3]:+.1f} desvios")
    print(f"      recupera nula B signo:    {B[2]:+8.2f}  ({B[2]/inyectada*100:5.0f}% de la inyectada)  {B[3]:+.1f} desvios")
    print(f"      pasiva: {r['pasiva']:+.2f} ({r['z_pas']:+.1f} desvios)   informativo = min de las tres = {r['z_info']:+.1f}")
    print(f"      obs {r['obs']:+.2f}  z_rent {r['z_rent']:+.1f}  z_req {r['z_req']:.2f}  op/sesion {r['op_ses']:.2f}")
    print(f"      -> {comentario}")
    return dict(v=r["veredicto"], A=A[2], B=B[2], zinfo=r["z_info"], iny=inyectada)


def main():
    print("=" * 100)
    print("EL JUEZ CONTRA OTRAS FORMAS DE VENTAJA - se mide el punto ciego, no se declara")
    print(f"NO GASTA CARTUCHO. K = 261. {NPERM} permutaciones. La caja sellada no se toca.")
    print("=" * 100)
    m = J.cargar_mercado()
    rng = np.random.default_rng(SEMILLA)
    idx = C.grilla(m, [2016, 2017, 2018])
    pL, pS = C.ambos_lados(m, idx)
    punto, c1 = J.PUNTO["ES"], J.COMISION["ES"]
    dL = pL * punto - c1; dS = pS * punto - c1
    prom = (dL + dS) / 2.0                       # lo que gana una moneda en cada ranura
    mejor_largo = dL >= dS
    ses = m["ses_de"][idx]
    nses = len(np.unique(ses))
    print(f"\n   grilla 2016-2018: {len(idx):,} ranuras, {nses:,} sesiones.")

    # ------------------------------------------------------------------ FORMA A: TIMING
    corte = np.quantile(prom, 2 / 3)
    sel = prom >= corte                          # el tercio de ranuras con mejor promedio de los dos lados
    lado_a = rng.random(len(idx)) < 0.5          # el lado es MONEDA: no sabe de que lado, sabe cuando
    # inyectada realizada = lo que gana por ELEGIR ESAS ranuras, contra operar la misma cantidad al azar
    iny_a = (sel.sum() / nses) * (prom[sel].mean() - prom.mean())
    cand_a = C.candidato("forma_A_timing", m, idx[sel], lado_a[sel])
    print(f"\n   FORMA A - TIMING: opera {int(sel.sum()):,} de {len(idx):,} ranuras ({sel.mean():.0%}), lado al azar.")
    ra = informe_forma("A timing", cand_a, m, iny_a,
                       "la nula de SIGNO conserva las ranuras: no puede ver una ventaja de cuando.")

    # ------------------------------------------------------------------ FORMA B: TAMANO
    lado_b = rng.random(len(idx)) < 0.5          # moneda pura: acierta el 50%
    acierta = (lado_b == mejor_largo)            # donde la moneda resulto ser el lado bueno
    # duplica la entrada donde acierta -> doble exposicion en las ganadoras (dos ops en la misma barra)
    idx_b = np.concatenate([idx, idx[acierta]])
    lado_bb = np.concatenate([lado_b, lado_b[acierta]])
    orden = np.argsort(idx_b, kind="stable")
    idx_b, lado_bb = idx_b[orden], lado_bb[orden]
    res_b = np.where(lado_b, dL, dS)
    iny_b = res_b[acierta].sum() / nses          # lo que agregan las operaciones duplicadas
    cand_b = C.candidato("forma_B_tamano", m, idx_b, lado_bb)
    cand_b["limite_contratos"] = 60              # permisivo: las duplicadas apilan exposicion a proposito
    print(f"\n   FORMA B - TAMANO: acierta {acierta.mean():.0%} (moneda), duplica en {int(acierta.sum()):,} "
          f"ranuras ganadoras -> {len(idx_b):,} operaciones.")
    rb = informe_forma("B tamano", cand_b, m, iny_b,
                       "las dos nulas deberian verla: dar vuelta el lado convierte las dobles en perdedoras.")

    # ------------------------------------------------------------------ veredicto del ejercicio
    print("\n" + "=" * 100)
    print("QUE VE EL JUEZ")
    print("=" * 100)
    for nom, r in (("A timing", ra), ("B tamano", rb)):
        if r is None:
            print(f"   {nom}: no evaluable")
            continue
        pa = r["A"] / r["iny"] * 100
        pb = r["B"] / r["iny"] * 100
        ve = "LA VE" if r["v"] in ("SUPERA", "APUESTA AL REGIMEN") else "NO LA VE"
        print(f"   {nom:<10} inyectada {r['iny']:+7.2f}  rotacion recupera {pa:5.0f}%  signo recupera {pb:5.0f}%"
              f"  -> veredicto {r['v']}  ({ve})")
    if ra:
        print(f"\n   EL PUNTO CIEGO, CUANTIFICADO: una ventaja de TIMING de {ra['iny']:+.2f} $/sesion -medida y")
        print(f"   recuperada al {ra['A']/ra['iny']*100:.0f}% por la nula de rotacion- se descarta igual, porque el")
        print(f"   'informativo' es el MINIMO de las tres nulas y la de signo la ve en {ra['B']/ra['iny']*100:.0f}%.")
        print(f"   No es un punto ciego chico: es TOTAL para una ventaja de timing pura, sea del tamano que sea.")


if __name__ == "__main__":
    main()
