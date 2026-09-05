"""
VENTANA G - C8 (candidato en el borde) sobre VARIAS SEMILLAS: apunta de verdad al borde?

NO GASTA CARTUCHO. K = 261. Construir la herramienta no es usarla: candidatos sinteticos. La caja
sellada no se toca.

Con una sola semilla, C8 (q=0,56) puede caer NO SUPERA en los dos modos y no probar nada esa corrida.
Aca se corre sobre muchas semillas y se reporta en que fraccion CRUZA a una categoria mas alta al
pasar de cruce a pasivo (el desplazamiento de nivel), SIN llegar nunca a SUPERA.

Orden de las categorias (rung): NO SUPERA < APUESTA AL REGIMEN < REQUIERE MEDICION PASIVA. SUPERA
seria un fallo. 'cruza' = el veredicto pasivo esta un escalon mas arriba que el de cruce.

CONDICION DE FALLA (corregida): que en ALGUNA semilla el juez devuelva SUPERA en modo PASIVO. SUPERA
en CRUCE NO es fallo -cruce es el modo que aprueba-; mi primera version lo marcaba mal. La garantia
'pasivo nunca aprueba' ademas es ESTRUCTURAL (techo_pasivo convierte cualquier SUPERA en REQUIERE
MEDICION), asi que no depende de la semilla.
Diagnostico de borde (no es fallo): en que fraccion C8 esta EN el borde, o sea cruce NO SUPERA y el
piso pasivo mas bajo lo levanta a una categoria mas alta sin llegar a SUPERA. Si es minoria, q esta
mal centrado (o el candidato queda por encima del borde -SUPERA en cruce- o por debajo -APUESTA sin
cruzar-). Se barren dos q para elegir el mejor centrado.
"""
import os
import sys
import tempfile

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import juez as J          # noqa: E402
import juez_controles as C  # noqa: E402

NPERM = int(os.environ.get("JUEZ_NPERM", "150"))
SEMILLAS = list(range(1, 13))
QS = [0.545, 0.55, 0.56]
RUNG = {"NO SUPERA": 1, "APUESTA AL REGIMEN": 2, J.REQUIERE_MEDICION: 3, "SUPERA": 99}


def main():
    print("=" * 96)
    print(f"C8 SOBRE {len(SEMILLAS)} SEMILLAS y {len(QS)} valores de q - centra en el borde? ({NPERM} perm)")
    print("NO GASTA CARTUCHO. K = 261. La caja sellada no se toca.")
    print("=" * 96)
    m = J.cargar_mercado()
    idx = C.grilla(m, [2016, 2017, 2018])
    pL, pS = C.ambos_lados(m, idx)
    dL = pL * J.PUNTO["ES"] - J.COMISION["ES"]; dS = pS * J.PUNTO["ES"] - J.COMISION["ES"]
    mejor = dL >= dS
    hay_supera_pasivo = False
    resumen = {}
    for q in QS:
        print(f"\n  q = {q}:   {'semilla':>7}{'CRUCE':>22}{'PASIVO':>34}{'en borde?':>11}")
        en_borde = sup_cru = 0
        for sd in SEMILLAS:
            rng = np.random.default_rng(sd)
            lado = np.where(rng.random(len(idx)) < q, mejor, ~mejor)
            cand = C.candidato(f"C8_q{q}_s{sd}", m, idx, lado)
            vs = {}
            for pas in (False, True):
                reg = os.path.join(tempfile.gettempdir(), f"c8s_{q}_{sd}_{pas}.jsonl")
                if os.path.exists(reg):
                    os.remove(reg)
                try:
                    s = J.juzgar(cand, m, npermuta=NPERM, registro=reg, pasivo=pas)
                    vs[pas] = s["periodos"]["trabajo"]["veredicto"]
                except (J.NoMedible, J.Rechazo):
                    vs[pas] = "NO MEDIBLE/RECH"
            vc, vp = vs[False], vs[True]
            if vp == "SUPERA":
                hay_supera_pasivo = True
            if vc == "SUPERA":
                sup_cru += 1
            borde = vc != "SUPERA" and RUNG.get(vp, 0) > RUNG.get(vc, 0)  # cruce reject, pasivo lo sube
            en_borde += int(borde)
            print(f"       {sd:>7}{vc:>22}{vp:>34}{('SI' if borde else 'no'):>11}")
        resumen[q] = (en_borde, sup_cru)
        print(f"     -> en el borde {en_borde}/{len(SEMILLAS)} = {en_borde/len(SEMILLAS):.0%}   "
              f"(por encima del borde / SUPERA en cruce: {sup_cru})")
    print("\n" + "=" * 96)
    mejor_q = max(QS, key=lambda q: resumen[q][0])
    print(f"   q mejor centrado en el borde: {mejor_q} ({resumen[mejor_q][0]}/{len(SEMILLAS)} en borde)")
    print(f"   SUPERA en modo PASIVO en alguna semilla/q (tiene que ser NO): "
          f"{'SI - FALLA' if hay_supera_pasivo else 'no - OK (garantia estructural de techo_pasivo)'}")
    print("=" * 96)
    if hay_supera_pasivo:
        raise SystemExit("FALLO: C8 devolvio SUPERA en modo pasivo en alguna semilla")


if __name__ == "__main__":
    main()
