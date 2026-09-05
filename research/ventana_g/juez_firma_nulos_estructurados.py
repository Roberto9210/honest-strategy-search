"""
LA TASA DE FALSO POSITIVO DE LA FIRMA CONTRA NULOS **ESTRUCTURADOS**.

NO GASTA CARTUCHO. K = 261. Candidatos SINTETICOS nulos sobre ES 1-min 2016-2018. La caja sellada no
se toca.

POR QUE ESTE ARCHIVO. En A1 la tasa de firma 'timing' dio 0 sobre 20.000 nulos, y dio cero
ENTERAMENTE por una razon: bajo ese nulo zA y zB estan correlacionadas +0,91, asi que el que queda
alto contra la rotacion queda alto tambien contra el signo y su firma sale 'direccional'. Toda la
seguridad del arreglo descansa en esa correlacion. Pero ese nulo era de UNA sola forma: grilla
uniforme cada 300 barras con el lado por moneda. Si la correlacion se rompe, la firma se vuelve
barata, y nunca la medi contra un nulo con ESTRUCTURA -entradas agrupadas, o de un solo lado en un
tramo, que es la forma del ataque A1-.

C6 muestra que A1 no llega. Eso es UNA instancia, no una tasa. Aca esta la tasa.

LO HARIA FALLAR: que con nulos estructurados la firma 'timing' aparezca por encima de 0,1%.

LAS FAMILIAS, y por que cada una. Ninguna tiene ventaja: el lado y las ranuras se sortean sin mirar
ningun resultado.
  uniforme       la de A1, como linea de base dentro de esta misma corrida.
  agrupado       todas las entradas caen en un 25% de las sesiones, sorteadas. Es la familia
                 PELIGROSA y por eso existe: si por azar el grupo cae en sesiones agitadas, los dos
                 lados ganan a la vez -el bracket de 5pt lo toca cualquiera de los dos-, y entonces
                 el observado le gana a la rotacion (zA alto) pero queda en el centro de la nula de
                 signo (zB ~ 0). Esa es exactamente la firma de timing, fabricada por azar.
  rafaga         la ventana entera comprimida a ~120 sesiones seguidas. Menos rotaciones
                 independientes, nula de rotacion mas pobre.
  un_lado_tramo  solo-largo en un tramo contiguo de ~250 sesiones. Es el ataque A1 sorteado mil
                 veces en vez de una.
  un_lado_total  solo-largo en todo el periodo. La deriva del ES 2016-2018 es positiva, asi que este
                 SI le gana a la nula de signo: sirve para ver que la firma lo manda a
                 'direccional' y no a 'timing'.
  signo_en_bloques  el lado se sortea una vez cada 20 sesiones y se repite. Signo autocorrelacionado:
                 es la forma mas directa de atacar la nula de signo sin tocar las ranuras.

LAS NEGATIVAS DEL JUEZ SE APLICAN IGUAL. Un candidato al que el juez le diria NO MEDIBLE -menos de
200 operaciones, menos de 15 rotaciones independientes, o resolucion peor que la ventaja de
referencia- NO cuenta como falso positivo, porque nunca llega a tener veredicto. Se cuentan aparte y
se informan.
"""

import os
import sys
import time

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import juez as J  # noqa: E402
import juez_firma_falso_positivo as FP  # noqa: E402

ANIOS = (2016, 2017, 2018)
N_CAND = int(os.environ.get("N_CAND", "10000"))
SEMILLA = 20260906


def familias(m, ses, rs):
    """Devuelve un dict nombre -> generador(rs) que da (idx, sgn). Nada mira resultados."""
    ini, fin = m["ini"][ses], m["fin"][ses]
    n_ses = len(ses)

    def uniforme(r):
        off = int(r.integers(0, 300))
        idx = np.concatenate([np.arange(int(a) + off, int(b) - 1, 300) for a, b in zip(ini, fin)])
        return idx, np.where(r.random(len(idx)) < 0.5, 1.0, -1.0)

    def agrupado(r):
        # 25% de las sesiones, sorteadas, con entradas densas (cada 60 barras)
        k = r.choice(n_ses, size=n_ses // 4, replace=False)
        k.sort()
        off = int(r.integers(0, 60))
        idx = np.concatenate([np.arange(int(ini[j]) + off, int(fin[j]) - 1, 60) for j in k])
        return idx, np.where(r.random(len(idx)) < 0.5, 1.0, -1.0)

    def rafaga(r):
        j0 = int(r.integers(0, n_ses - 120))
        sel = np.arange(j0, j0 + 120)
        off = int(r.integers(0, 120))
        idx = np.concatenate([np.arange(int(ini[j]) + off, int(fin[j]) - 1, 120) for j in sel])
        return idx, np.where(r.random(len(idx)) < 0.5, 1.0, -1.0)

    def un_lado_tramo(r):
        j0 = int(r.integers(0, n_ses - 250))
        sel = np.arange(j0, j0 + 250)
        off = int(r.integers(0, 300))
        idx = np.concatenate([np.arange(int(ini[j]) + off, int(fin[j]) - 1, 300) for j in sel])
        lado = 1.0 if r.random() < 0.5 else -1.0
        return idx, np.full(len(idx), lado)

    def un_lado_total(r):
        off = int(r.integers(0, 300))
        idx = np.concatenate([np.arange(int(a) + off, int(b) - 1, 300) for a, b in zip(ini, fin)])
        lado = 1.0 if r.random() < 0.5 else -1.0
        return idx, np.full(len(idx), lado)

    def signo_en_bloques(r):
        off = int(r.integers(0, 300))
        trozos = [np.arange(int(a) + off, int(b) - 1, 300) for a, b in zip(ini, fin)]
        idx = np.concatenate(trozos)
        ses_de_op = np.concatenate([np.full(len(t), j) for j, t in enumerate(trozos)])
        bloque = ses_de_op // 20
        signo_bloque = np.where(r.random(bloque.max() + 1) < 0.5, 1.0, -1.0)
        return idx, signo_bloque[bloque]

    return dict(uniforme=uniforme, agrupado=agrupado, rafaga=rafaga,
                un_lado_tramo=un_lado_tramo, un_lado_total=un_lado_total,
                signo_en_bloques=signo_en_bloques)


def medible(d, K):
    """Las mismas negativas del juez. Devuelve (bool, motivo)."""
    if d["n_op"] < J.N_MIN_OP:
        return False, "pocas operaciones"
    if d["rot_indep"] < J.ROT_INDEP_MIN:
        return False, "ventana angosta"
    ref = J.REF_EDGE_OP_MINI * (d["n_op"] / d["n_ses"]) * (K["punto"] / 50.0) * K["contratos"]
    if ref and d["sd_tot"] / ref > 1.0:
        return False, "resolucion"
    return True, ""


def main():
    R = []
    A = R.append
    A("=" * 100)
    A("LA FIRMA DE TIMING CONTRA NULOS ESTRUCTURADOS - sobrevive la correlacion +0,91?")
    A("NO GASTA CARTUCHO. K = 261. La caja sellada no se toca.")
    A("=" * 100)
    m = J.cargar_mercado()
    ses = np.flatnonzero(np.isin(m["anio_ses"], ANIOS))
    K = FP.constantes(m)
    rs = np.random.default_rng(SEMILLA)
    t0 = time.time()
    tab = FP.tabla_desenlaces(m, ses, FP.CELDA, K["exceso"])
    b0, b1 = int(m["ini"][ses[0]]), int(m["fin"][ses[-1]])
    huecos = int(np.isnan(tab[0][b0:b1]).sum() + np.isnan(tab[1][b0:b1]).sum())
    okp, okt, nver = FP.control_0_tabla(m, ses, *tab, K["exceso"], rs)
    A(f"\n   tabla de desenlaces en {time.time()-t0:.0f}s. CONTROL 0 contra J.resolver sobre "
      f"{nver:,} ranuras de los dos lados:")
    A(f"      puntos identicos {'SI' if okp else 'NO'}   tenencia identica "
      f"{'SI' if okt else 'NO'}   barras sin rellenar {huecos}")
    if not (okp and okt and huecos == 0):
        A("      LA TABLA NO COINCIDE. Se corta aca.")
        print("\n".join(R))
        return 1

    fam = familias(m, ses, rs)
    z_req = J.z_requerido(1)
    A(f"\n   {N_CAND:,} candidatos por familia, {FP.NPERM} rotaciones y {FP.NPERM} signos cada uno.")
    res = {}
    for i_fam, (nombre, gen) in enumerate(fam.items()):
        zA = np.empty(N_CAND); zB = np.empty(N_CAND); zp = np.empty(N_CAND)
        ok = np.zeros(N_CAND, bool)
        motivos = {}
        t1 = time.time()
        for c in range(N_CAND):
            # semilla por indice de familia, NO por hash del nombre: el hash de un str en Python
            # cambia entre procesos y la corrida no seria reproducible.
            r = np.random.default_rng(SEMILLA + 1000003 * i_fam + c)
            idx, sgn = gen(r)
            d = FP.evaluar(m, K, idx, sgn, tab, r, detalle=True)
            zA[c], zB[c], zp[c] = d["zA"], d["zB"], d["z_pas"]
            m_ok, mot = medible(d, K)
            ok[c] = m_ok
            if not m_ok:
                motivos[mot] = motivos.get(mot, 0) + 1
        res[nombre] = dict(zA=zA, zB=zB, zp=zp, ok=ok, motivos=motivos, seg=time.time() - t1)
        print(f"      {nombre}: {time.time()-t1:.0f}s", file=sys.stderr, flush=True)
    # los z crudos, para poder rebarrer reglas sin volver a correr una hora. Fuera del repo.
    guarda = os.environ.get("GUARDAR_Z")
    if guarda:
        np.savez_compressed(guarda, **{f"{k}_{c}": v[c] for k, v in res.items()
                                       for c in ("zA", "zB", "zp", "ok")})
        print(f"      z guardados en {guarda}", file=sys.stderr, flush=True)

    A("")
    A("-" * 100)
    A("   LA CORRELACION, QUE ES EL NUMERO QUE EXPLICA TODO LO DEMAS")
    A("-" * 100)
    A(f"   {'familia':<18}{'n medibles':>12}{'corr(zA,zB)':>14}{'sd zA':>8}{'sd zB':>8}"
      f"{'media zA':>10}{'media zB':>10}")
    for nombre, d in res.items():
        s = d["ok"]
        if s.sum() < 10:
            A(f"   {nombre:<18}{int(s.sum()):>12}   (muy pocos medibles para correlacionar)")
            continue
        A(f"   {nombre:<18}{int(s.sum()):>12}{np.corrcoef(d['zA'][s], d['zB'][s])[0,1]:>14.3f}"
          f"{d['zA'][s].std(ddof=1):>8.2f}{d['zB'][s].std(ddof=1):>8.2f}"
          f"{d['zA'][s].mean():>10.2f}{d['zB'][s].mean():>10.2f}")

    A("")
    A("-" * 100)
    A("   LA TASA DE FIRMA, SOBRE LOS MEDIBLES (los que el juez NO rechaza de entrada)")
    A("-" * 100)
    A(f"   {'familia':<18}{'medibles':>10}{'zA>=3':>9}{'FIRMA timing':>15}{'IC95 arriba':>13}"
      f"{'FIRMA direcc':>14}{'APROBARIA':>11}")
    peor = 0.0
    for nombre, d in res.items():
        s = d["ok"]
        n = int(s.sum())
        if n == 0:
            A(f"   {nombre:<18}{0:>10}   ninguno medible")
            continue
        zA, zB, zp = d["zA"][s], d["zB"][s], d["zp"][s]
        ft = (zA >= J.Z_BASE) & (np.abs(zB) < 1.0)
        fd = (zA >= J.Z_BASE) & (zB >= J.Z_BASE)
        ap = ft & (np.minimum(zA, zp) >= z_req)
        _, hi = FP.wilson(int(ft.sum()), n)
        peor = max(peor, hi)
        A(f"   {nombre:<18}{n:>10}{int((zA>=J.Z_BASE).sum()):>9}"
          f"{int(ft.sum()):>7} = {ft.mean():>5.3%}{hi:>13.3%}"
          f"{int(fd.sum()):>7} = {fd.mean():>4.2%}{int(ap.sum()):>11}")

    A("")
    A("   LOS RECHAZADOS DE ENTRADA (el juez les diria NO MEDIBLE, nunca llegan a veredicto):")
    for nombre, d in res.items():
        no = N_CAND - int(d["ok"].sum())
        det = ", ".join(f"{k} {v:,}" for k, v in sorted(d["motivos"].items())) or "-"
        A(f"      {nombre:<18}{no:>7} de {N_CAND:,}   ({det})")

    # -------------------------------------------------------------------------------------
    # SI LA VARA SE PASA, HAY QUE SUBIR EL UMBRAL. Y se elige con un barrido, no a ojo.
    # -------------------------------------------------------------------------------------
    A("")
    A("-" * 100)
    A("   BARRIDO DE REGLAS DE FIRMA. Por que la actual falla y cual la reemplaza.")
    A("-" * 100)
    A("   La regla actual es |zB| < 1,0 ABSOLUTO. En la familia 'agrupado' zB esta COMPRIMIDO")
    A("   (sd 0,61), asi que |zB| < 1,0 se cumple casi siempre y el criterio deja de hacer trabajo:")
    A("   la firma se reduce a zA >= 3 a secas. La regla tiene que mirar zB EN RELACION a zA, que es")
    A("   lo que de verdad distingue 'la nula de signo no ve nada' de 'zB es chico porque todo es")
    A("   chico'. Referencia de una ventaja de timing REAL (control C9): zA = +23,1, zB = +0,1, o sea")
    A("   zB/zA = 0,004. Los falsos positivos de 'agrupado' viven en zB/zA ~ 0,3.")
    A("")
    ref_zA, ref_zB = 23.1, 0.1
    A(f"   {'regla':<34}" + "".join(f"{k[:9]:>10}" for k in res) + f"{'C9 real':>10}")
    reglas = [("|zB| < 1,0  (la actual)", lambda a, b: np.abs(b) < 1.0)]
    for k in (0.50, 0.30, 0.20, 0.15, 0.10):
        reglas.append((f"|zB| < min(1,0 ; {k:.2f}*zA)",
                       lambda a, b, k=k: np.abs(b) < np.minimum(1.0, k * a)))
    for et, f_ in reglas:
        fila = ""
        for nombre, d in res.items():
            s = d["ok"]
            zA_, zB_ = d["zA"][s], d["zB"][s]
            ft = (zA_ >= J.Z_BASE) & f_(zA_, zB_)
            fila += f"{ft.mean():>10.3%}"
        ok_c9 = "SI" if f_(np.array([ref_zA]), np.array([ref_zB]))[0] else "NO"
        A(f"   {et:<34}{fila}{ok_c9:>10}")
    A("")
    A("   Se elige la regla mas floja que deja TODAS las familias en 0 y sigue reconociendo la")
    A("   ventaja de timing real. Mas estricta que eso solo perderia ventajas verdaderas.")

    A("")
    A("=" * 100)
    A("   VEREDICTO")
    A("=" * 100)
    tot_ap = sum(int(((d["zA"][d["ok"]] >= J.Z_BASE) & (np.abs(d["zB"][d["ok"]]) < 1.0)
                      & (np.minimum(d["zA"][d["ok"]], d["zp"][d["ok"]]) >= z_req)).sum())
                 for d in res.values())
    A(f"   La cota superior mas alta de firma 'timing' entre las {len(res)} familias es {peor:.3%}.")
    A(f"   {'POR DEBAJO' if peor <= 0.001 else 'POR ENCIMA'} de la vara de 0,100%.")
    A(f"   Nulos que llegarian a APROBACION declarando 'timing', sumando todas las familias: {tot_ap}.")
    A("=" * 100)
    print("\n".join(R))
    return 0


if __name__ == "__main__":
    sys.exit(main())
