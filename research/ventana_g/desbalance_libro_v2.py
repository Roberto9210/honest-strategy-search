"""
PIEZA 3, REHECHA CON EL LIBRO ARREGLADO. Diagnostico + 3a + 3b + 3c en una sola pasada.

NO GASTA CARTUCHO. K = 261. Dinero: $0, los 6 dias ya estan en disco; la compra queda SUSPENDIDA
porque el defecto era del instrumento y no de la cantidad de dias. La caja sellada no se toca.

QUE CAMBIO. mbo_lib.reconstruir(con_tamano=True) anota el BBO tambien cuando cambia el TAMANO al
mejor precio, no solo cuando cambia el precio. Con la version vieja el estado del libro tenia 669 ms
de antiguedad MEDIANA en el instante de un llenado y en 67% de los casos ya era mas viejo que 100 ms:
la pregunta de 3b no se podia contestar y el negativo era un "sin medir", no un "no".

COSTO DECLARADO ANTES DE CORRER: la serie de BBO pasa de decenas de miles a millones de filas por
dia. Son 5 arrays x 8 bytes: del orden de 100-250 MB por dia. NO entran seis dias juntos, asi que
este script procesa DE A UN DIA y libera antes del siguiente. Tiempo de corrida: el bucle de
reconstruccion es el mismo, con mas appends; se espera 1,5-2x el original (17-60 s por dia).

ORDEN, y no se saltea: (b) primero se verifica que el arreglo bajo la antiguedad a la escala del
efecto. Si no bajo, NO se corre 3b, porque correrla sobre un instrumento que sigue ciego seria
repetir el error que este archivo existe para no repetir.

CONTABILIDAD: medir el comportamiento del costo es gratis en cartuchos. El dia que este filtro se USE
dentro de una estrategia, esa estrategia es una candidata DISTINTA de la misma sin filtro, se declara
y probablemente cuesta cartucho.
"""

import gc
import os
import sys
import time
from pathlib import Path

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import mbo_lib as M  # noqa: E402
import mbo_entrada_pasiva as P  # noqa: E402

TICK = 0.25
DIR = Path(AQUI).resolve().parents[1] / "data" / "microestructura"
N_ENTRADAS = 3000
LAT_MS = 250
MUERTE_TICKS = 1
HORIZ_3A = [1, 5, 30]
HORIZ_3B = 30
ADELANTOS_MS = [0, 100, 500, 1000]
SEMILLA = 20260906
# lo que dio el libro VIEJO, para comparar
VIEJO_ANTIG_MED = 669.0
VIEJO_3A = {1: 0.102, 5: 0.182, 30: 0.189}
VIEJO_MK = 0.0335
UMBRAL_ANTIG_MS = 100.0     # la escala del efecto: el adelanto mas corto que se quiere distinguir


def imbalance_en(rec, t):
    b, a, bs, as_, _ = M.bbo_en(rec, t)
    tot = bs + as_
    return np.where(tot > 0, (bs - as_) / np.maximum(tot, 1), 0.0)


def main():
    R = []
    A = R.append
    A("=" * 100)
    A("PIEZA 3 REHECHA CON EL LIBRO ARREGLADO (con_tamano=True)")
    A("NO GASTA CARTUCHO. K = 261. Dinero: $0, compra SUSPENDIDA. La caja sellada no se toca.")
    A("=" * 100)
    A("")
    A("   COSTO DECLARADO: ~100-250 MB por dia de serie de BBO. Se procesa de a un dia y se libera.")
    A("   CONTABILIDAD: medir es gratis en cartuchos; USAR el filtro en una estrategia la convierte")
    A("   en una candidata distinta y eso se declara aparte.")

    diag, r3a, r3b = [], {}, {}
    pool = {d: {"fav": [], "mk": []} for d in ADELANTOS_MS}
    for i_d, (epoca, tercil, arch) in enumerate(P.ARCHIVOS):
        p = DIR / arch
        if not p.exists():
            A(f"\n   FALTA {arch}: se saltea.")
            continue
        t0 = time.time()
        rec = M.reconstruir(str(p), con_tamano=True)
        seg = time.time() - t0
        tc = rec["tc"]
        mem = sum(x.nbytes for x in (rec["tc"], rec["bid"], rec["ask"], rec["bsz"], rec["asz"])) / 1e6
        print(f"   {arch}: {len(tc):,} filas, {mem:.0f} MB, {seg:.0f}s",
              file=sys.stderr, flush=True)

        # ---- (b) la verificacion del arreglo, ANTES de usar nada -------------------------
        rs = np.random.default_rng(SEMILLA + 7 + 101 * i_d)
        t0n, t1n = tc[0], tc[-1] - 400 * 1_000_000_000
        ent = np.sort(rs.integers(t0n, t1n, N_ENTRADAS))
        lado = np.where(rs.random(N_ENTRADAS) < 0.5, 1.0, -1.0)
        filled, t_fill, lim, _ = P.simular(rec, ent, lado, LAT_MS * 1_000_000, MUERTE_TICKS)
        tf = t_fill[filled]
        # LA ANTIGUEDAD SE MIDE DESDE EL INSTANTE QUE SE CONSULTA, no desde el llenado. Medirla en
        # tf da 0,0 ms TRIVIALMENTE: el propio llenado es un mensaje F que cambia el tamano al mejor
        # precio, asi que con con_tamano=True crea su PROPIA fila de BBO en tf. Eso no es resolucion,
        # es contaminacion -y por eso d=0 no sirve como lectura, esta mirando el efecto del llenado-.
        # Lo que decide es cuan viejo esta el estado cuando se lo consulta con adelanto d.
        ant = {}
        for d in ADELANTOS_MS:
            tq = tf - d * 1_000_000
            jq = np.clip(np.searchsorted(tc, tq, side="right") - 1, 0, len(tc) - 1)
            ant[d] = (tq - tc[jq]) / 1e6
        diag.append((f"{epoca}/{tercil}", len(tc), mem, seg,
                     {d: float(np.median(ant[d])) for d in ADELANTOS_MS},
                     {d: float(np.percentile(ant[d], 90)) for d in ADELANTOS_MS}))

        # ---- 3a ---------------------------------------------------------------------------
        rsa = np.random.default_rng(SEMILLA + 101 * i_d)
        ta = np.sort(rsa.integers(tc[0], tc[-1] - 60 * 1_000_000_000, N_ENTRADAS))
        I = imbalance_en(rec, ta)
        mid0 = M.mid_en(rec, ta)
        o = {}
        for H in HORIZ_3A:
            dm = (M.mid_en(rec, ta + H * 1_000_000_000) - mid0) / TICK
            q = np.quantile(I, np.linspace(0, 1, 11)); q[0] -= 1e-9; q[-1] += 1e-9
            dec = np.clip(np.digitize(I, q) - 1, 0, 9)
            med = np.array([dm[dec == k].mean() if (dec == k).any() else np.nan for k in range(10)])
            o[H] = dict(spread=float(med[9] - med[0]), rho=float(np.corrcoef(I, dm)[0, 1]))
        r3a[(epoca, tercil)] = o

        # ---- 3b ---------------------------------------------------------------------------
        if filled.sum() >= 50:
            lf = lim[filled]; sf = lado[filled]
            mk = (M.mid_en(rec, tf + HORIZ_3B * 1_000_000_000) - lf) * sf
            porad = {}
            for d in ADELANTOS_MS:
                fav = imbalance_en(rec, tf - d * 1_000_000) * sf
                porad[d] = float(np.corrcoef(fav, mk)[0, 1])
                pool[d]["fav"].append(fav); pool[d]["mk"].append(mk)
            r3b[(epoca, tercil)] = dict(llenado=float(filled.mean()), n=int(filled.sum()),
                                        mk=float(mk.mean()), rho=porad)
        del rec, I, mid0
        gc.collect()

    # ------------------------------------------------------------------ (b) el veredicto
    A("")
    A("-" * 100)
    A("   (b) LA VERIFICACION DEL ARREGLO. Si esto no baja, NO se corre 3b.")
    A("-" * 100)
    A("   Antiguedad = cuanto hace que se congelo el estado, MEDIDA DESDE EL INSTANTE QUE SE")
    A("   CONSULTA (tf - d). En tf da 0 trivialmente: el llenado crea su propia fila.")
    A("")
    A(f"   {'dia':>16}{'filas BBO':>12}{'MB':>7}{'seg':>6}"
      + "".join(f"{'med d=' + str(d):>11}" for d in ADELANTOS_MS))
    for f in diag:
        A(f"   {f[0]:>16}{f[1]:>12,}{f[2]:>7.0f}{f[3]:>6.0f}"
          + "".join(f"{f[4][d]:>11.2f}" for d in ADELANTOS_MS))
    A("")
    A(f"   {'':>16}{'p90:':>37}" + "".join(f"{np.mean([f[5][d] for f in diag]):>11.1f}"
                                           for d in ADELANTOS_MS))
    med_new = float(np.median([f[4][100] for f in diag]))
    A("")
    A(f"   Antiguedad MEDIANA consultando con 100 ms de adelanto: {med_new:.2f} ms")
    A(f"      antes (libro viejo, misma consulta): {VIEJO_ANTIG_MED:.0f} ms   ->  "
      f"{VIEJO_ANTIG_MED/max(med_new,1e-9):.0f}x mejor")
    ok = med_new < UMBRAL_ANTIG_MS
    if ok:
        A(f"   ARREGLO SUFICIENTE: la antiguedad mediana ({med_new:.1f} ms) esta por debajo de la")
        A(f"   escala del efecto ({UMBRAL_ANTIG_MS:.0f} ms). Los adelantos SI distinguen estados")
        A("   distintos, y 3b se puede contestar.")
    else:
        A(f"   ARREGLO INSUFICIENTE: la antiguedad mediana ({med_new:.1f} ms) sigue por encima de")
        A(f"   {UMBRAL_ANTIG_MS:.0f} ms. 3b sigue SIN MEDIR y no se reporta como negativo.")

    # ------------------------------------------------------------------ 3a
    A("")
    A("-" * 100)
    A("   (d) 3a CON EL LIBRO ARREGLADO - cuanto se movio el numero")
    A("-" * 100)
    A(f"   {'dia':>16}" + "".join(f"{'H=' + str(h) + 's':>22}" for h in HORIZ_3A))
    A(f"   {'':>16}" + "".join(f"{'spread tk':>11}{'rho':>11}" for _ in HORIZ_3A))
    for k, o in r3a.items():
        A(f"   {k[0] + '/' + k[1]:>16}" + "".join(f"{o[h]['spread']:>11.3f}{o[h]['rho']:>11.3f}"
                                                  for h in HORIZ_3A))
    A("")
    A(f"   {'H':>4}{'nuevo':>10}{'viejo':>10}{'cambio':>10}")
    for h in HORIZ_3A:
        nv = float(np.mean([o[h]["spread"] for o in r3a.values()]))
        A(f"   {h:>4}{nv:>10.3f}{VIEJO_3A[h]:>10.3f}{nv - VIEJO_3A[h]:>+10.3f}")
    nv1 = float(np.mean([o[HORIZ_3A[0]]["spread"] for o in r3a.values()]))
    A("")
    A(f"   Cruzar cuesta del orden de 1 tick. La separacion a H=1s es {nv1:.3f} ticks.")
    if abs(nv1) < 1.0:
        A(f"   Sigue MUERTA, y ahora con el libro que si ve: haria falta {1.0/max(abs(nv1),1e-9):.0f}x")
        A("   mas para pagar el cruce. La conclusion de 3a queda firme, no solo con margen.")
    else:
        A("   YA NO ESTA MUERTA con el libro arreglado. Hay que mirarla de nuevo.")

    # ------------------------------------------------------------------ 3b / 3c
    if not ok:
        A("")
        A("   3b y 3c NO se corren: el instrumento no llego a la escala del efecto.")
        A("=" * 100)
        print("\n".join(R))
        return 0

    A("")
    A("-" * 100)
    A("   (c) 3b - EL DESBALANCE COMO PREDICTOR DE SELECCION ADVERSA")
    A("-" * 100)
    A(f"   Orden pasiva al mejor precio, latencia {LAT_MS} ms, muerte {MUERTE_TICKS} tick, "
      f"markout H={HORIZ_3B}s.")
    A(f"   {'dia':>16}{'llenado':>9}{'n llenos':>10}{'markout':>10}"
      + "".join(f"{'rho d=' + str(d):>11}" for d in ADELANTOS_MS))
    for k, o in r3b.items():
        A(f"   {k[0] + '/' + k[1]:>16}{o['llenado']:>9.3f}{o['n']:>10}{o['mk']:>+10.4f}"
          + "".join(f"{o['rho'][d]:>+11.3f}" for d in ADELANTOS_MS))
    rho_prom = {d: float(np.mean([o["rho"][d] for o in r3b.values()])) for d in ADELANTOS_MS}
    A("")
    A("   rho promedio entre dias: " + "   ".join(f"d={d}ms {rho_prom[d]:+.3f}"
                                                  for d in ADELANTOS_MS))

    A("")
    A("-" * 100)
    A("   (c) 3c - EL FILTRO. La mejora y el CONTEO, siempre juntos.")
    A("-" * 100)
    for d in ADELANTOS_MS:
        fav = np.concatenate(pool[d]["fav"]); mk = np.concatenate(pool[d]["mk"])
        A(f"   ADELANTO d = {d} ms   (base: {len(mk):,} llenados, markout medio "
          f"{mk.mean():+.4f} pt)")
        A(f"      {'umbral I':>10}{'sobreviven':>12}{'n':>8}{'mk filtrado':>14}{'mejora':>10}"
          f"{'error':>9}{'sigmas':>8}{'mejora x n':>12}")
        mejoras = []
        for u in (-0.5, -0.25, 0.0, 0.25, 0.5):
            sel = fav >= u
            if sel.sum() < 10:
                A(f"      {u:>10.2f}{sel.mean():>12.1%}{int(sel.sum()):>8}{'(muy pocos)':>14}")
                continue
            mej = mk[sel].mean() - mk.mean()
            # error de la DIFERENCIA entre el subgrupo y el total: se = sd*sqrt(1/n_sel - 1/n)
            se = mk.std(ddof=1) * np.sqrt(max(1.0 / sel.sum() - 1.0 / len(mk), 0.0))
            z = mej / se if se > 0 else 0.0
            mejoras.append(mej)
            A(f"      {u:>10.2f}{sel.mean():>12.1%}{int(sel.sum()):>8}{mk[sel].mean():>+14.4f}"
              f"{mej:>+10.4f}{se:>9.4f}{z:>+8.2f}{mej * sel.mean():>+12.4f}")
        # una relacion REAL es monotona en el umbral; el zigzag es la firma del ruido
        if len(mejoras) >= 3:
            dif = np.diff(mejoras)
            mono = bool(np.all(dif >= 0) or np.all(dif <= 0))
            A(f"      monotona en el umbral: {'SI' if mono else 'NO - zigzag, firma de ruido'}"
              f"   (cambios de signo: {int((dif[:-1] * dif[1:] < 0).sum())} de {len(dif)-1})")
        A("")
    A("   'mejora x n' es la mejora POR LLENADO ORIGINAL: es lo unico comparable entre umbrales,")
    A("   porque un filtro que mejora mucho y deja 4% de llenados no mejora la estrategia.")
    A("   'sigmas' es la mejora sobre su propio error. Una mejora de menos de 2 sigmas no es una")
    A("   mejora, y una que zigzaguea al mover el umbral tampoco, aunque tenga sigmas.")
    A("=" * 100)
    print("\n".join(R))
    return 0


if __name__ == "__main__":
    sys.exit(main())
