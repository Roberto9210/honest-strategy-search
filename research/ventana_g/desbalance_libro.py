"""
PIEZA 3 - DESBALANCE DEL LIBRO: PREDICE EL PRECIO (3a) Y PREDICE LA SELECCION ADVERSA (3b/3c)?

NO GASTA CARTUCHO. K = 261. Dinero: $0 - los 6 dias de mbo ya estan comprados y en disco.
La caja sellada no se toca: los tres dias A son posteriores al 2026-08-19.

CONTABILIDAD DECLARADA POR ADELANTADO, y va en el documento porque no la dejamos pasar de
contrabando: MEDIR como se comporta el costo es gratis en cartuchos, igual que medir la comision.
Pero el dia que este filtro se USE dentro de una estrategia, esa estrategia es una candidata DISTINTA
de la misma sin filtro, y eso se declara y probablemente cuesta cartucho.

LAS TRES MEDICIONES
  3a  Cuanto predice el desbalance el movimiento futuro del precio, EN TICKS del ES, a 1 s, 5 s y
      30 s. En ticks y no en unidades normalizadas, porque cruzar el spread cuesta del orden de un
      tick y se quiere comparar directo. Si la prediccion es menor que eso, la version "adivinar la
      direccion" esta muerta y se cierra con numero.
  3b  La que importa. NO hacia donde va el precio, sino: cuando una orden pasiva NUESTRA se ejecuta,
      el estado del libro JUSTO ANTES predice si ese llenado fue bueno o envenenado? Se condiciona
      el markout posterior al llenado sobre el desbalance previo.
  3c  Si 3b da positivo: cuantos llenados SOBREVIVEN al filtro y cuanto del spread conservan. El
      conteo va SIEMPRE al lado de la mejora. Una mejora sin el conteo no se acepta.

EL ADELANTO, QUE ES LO QUE HACE HONESTA A 3b. Medir el desbalance en el instante exacto del llenado
es hacer trampa por dos motivos: (1) nadie puede retirar una orden en cero segundos, y (2) el propio
llenado consume la cola de nuestro lado, asi que el desbalance en t_fill esta CONTAMINADO por el
evento que se quiere predecir. Se mide con ADELANTO d = 0, 100 ms, 500 ms y 1 s antes del llenado, y
se reporta como se degrada. Si el filtro solo funciona a d = 0, no es "selectivo": es imposible.

DEFINICION. I = (tam_bid - tam_ask) / (tam_bid + tam_ask) en el mejor precio. I > 0 = mas cola del
lado comprador. Para una compra pasiva (descansando en el bid) el estado FAVORABLE es I > 0.
"""

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
ARCHIVOS = P.ARCHIVOS
N_ENTRADAS = 3000
LAT_MS = 250                      # latencia realista, la que ya se uso
MUERTE_TICKS = 1
HORIZ_3A = [1, 5, 30]             # segundos
HORIZ_3B = 30                     # el markout de referencia del piso pasivo
ADELANTOS_MS = [0, 100, 500, 1000]
SEMILLA = 20260906
# referencias publicadas contra las que se compara (piso en $/sesion)
PISO_PASIVO = {"5pt:20pt": 15.45, "20pt:10pt": 32.33}
PISO_CRUCE = {"5pt:20pt": 78.24, "20pt:10pt": 92.81}


def imbalance_en(rec, t):
    """I en el instante t (ns). Vectorizado sobre t."""
    b, a, bs, as_, _ = M.bbo_en(rec, t)
    tot = bs + as_
    return np.where(tot > 0, (bs - as_) / np.maximum(tot, 1), 0.0)


def bloque_3a(rec, rs, A):
    """Cuanto predice I el movimiento del mid, en TICKS."""
    tc = rec["tc"]
    if len(tc) < 1000:
        return None
    # instantes de muestreo: una grilla al azar dentro del rango, no los cambios de BBO
    # (muestrear los cambios sobreponderaria los momentos agitados)
    t0, t1 = tc[0], tc[-1] - 60 * 1_000_000_000
    if t1 <= t0:
        return None
    t = np.sort(rs.integers(t0, t1, N_ENTRADAS))
    I = imbalance_en(rec, t)
    mid0 = M.mid_en(rec, t)
    out = {}
    for H in HORIZ_3A:
        midH = M.mid_en(rec, t + H * 1_000_000_000)
        dm = (midH - mid0) / TICK          # en TICKS
        # deciles de I
        q = np.quantile(I, np.linspace(0, 1, 11))
        q[0] -= 1e-9; q[-1] += 1e-9
        dec = np.clip(np.digitize(I, q) - 1, 0, 9)
        medias = np.array([dm[dec == d].mean() if (dec == d).any() else np.nan
                           for d in range(10)])
        # el estadistico que decide: la diferencia entre el decil mas comprador y el mas vendedor
        spread_pred = medias[9] - medias[0]
        rho = float(np.corrcoef(I, dm)[0, 1])
        out[H] = dict(medias=medias, spread=spread_pred, rho=rho,
                      sd=float(dm.std(ddof=1)))
    return out


def bloque_3b(rec, rs, A):
    """Markout de NUESTROS llenados pasivos, condicionado al desbalance previo."""
    tc = rec["tc"]
    if len(tc) < 1000:
        return None
    t0, t1 = tc[0], tc[-1] - 400 * 1_000_000_000
    if t1 <= t0:
        return None
    ent = np.sort(rs.integers(t0, t1, N_ENTRADAS))
    lado = np.where(rs.random(N_ENTRADAS) < 0.5, 1.0, -1.0)
    filled, t_fill, lim, mid_e = P.simular(rec, ent, lado, LAT_MS * 1_000_000, MUERTE_TICKS)
    if filled.sum() < 50:
        return None
    tf = t_fill[filled]; lf = lim[filled]; sf = lado[filled]
    midH = M.mid_en(rec, tf + HORIZ_3B * 1_000_000_000)
    mk = (midH - lf) * sf                       # markout en PUNTOS, positivo = llenado bueno
    res = dict(n_senales=N_ENTRADAS, n_llenos=int(filled.sum()),
               llenado=float(filled.mean()), mk_todos=float(mk.mean()), por_adelanto={})
    for d in ADELANTOS_MS:
        I = imbalance_en(rec, tf - d * 1_000_000)
        # FAVORABLE = la cola esta de nuestro lado: para una compra (s=+1), I > 0
        fav = I * sf
        res["por_adelanto"][d] = dict(
            I_fav=fav, mk=mk,
            rho=float(np.corrcoef(fav, mk)[0, 1]) if len(mk) > 3 else float("nan"))
    return res


def main():
    R = []
    A = R.append
    A("=" * 100)
    A("PIEZA 3 - DESBALANCE DEL LIBRO. 3a prediccion en ticks, 3b seleccion adversa, 3c el filtro.")
    A("NO GASTA CARTUCHO. K = 261. Dinero: $0, los datos ya estan en disco. Caja sellada intacta.")
    A("=" * 100)
    A("")
    A("CONTABILIDAD DECLARADA: medir el comportamiento del costo es gratis en cartuchos. Pero el dia")
    A("que este filtro se USE dentro de una estrategia, esa estrategia es una candidata DISTINTA de")
    A("la misma sin filtro. Se declara y probablemente cuesta cartucho. No pasa de contrabando.")

    recs = {}
    for epoca, tercil, arch in ARCHIVOS:
        p = DIR / arch
        if not p.exists():
            A(f"\n   FALTA {arch}: se saltea.")
            continue
        t0 = time.time()
        recs[(epoca, tercil)] = M.reconstruir(str(p))
        print(f"   reconstruido {arch} en {time.time()-t0:.0f}s", file=sys.stderr, flush=True)
    A(f"\n   {len(recs)} dias reconstruidos (RTH 08:30-15:15 CT). "
      f"B = 2017-2019 (el terreno que juzga el juez); A = 2026, posterior a la caja.")

    # ------------------------------------------------------------------ 3a
    A("")
    A("-" * 100)
    A("   3a - CUANTO PREDICE EL DESBALANCE, EN TICKS DEL ES")
    A("-" * 100)
    A("   'spread' = movimiento medio del decil mas comprador MENOS el del mas vendedor, en ticks.")
    A("   Es la separacion maxima que el desbalance puede darte si lo usaras para adivinar el lado.")
    A(f"   {'dia':>16}" + "".join(f"{'H=' + str(h) + 's':>22}" for h in HORIZ_3A))
    A(f"   {'':>16}" + "".join(f"{'spread tk':>11}{'rho':>11}" for _ in HORIZ_3A))
    res3a = {}
    # semilla por INDICE, no por hash del nombre: el hash de un str cambia entre procesos.
    for i_d, (k, rec) in enumerate(recs.items()):
        rs = np.random.default_rng(SEMILLA + 101 * i_d)
        o = bloque_3a(rec, rs, A)
        res3a[k] = o
        if o is None:
            A(f"   {k[0]+'/'+k[1]:>16}   (sin datos suficientes)")
            continue
        A(f"   {k[0]+'/'+k[1]:>16}" + "".join(f"{o[h]['spread']:>11.3f}{o[h]['rho']:>11.3f}"
                                              for h in HORIZ_3A))
    vivos = [o for o in res3a.values() if o]
    if vivos:
        A("")
        for h in HORIZ_3A:
            sp = np.array([o[h]["spread"] for o in vivos])
            A(f"   H={h:>2}s: spread entre deciles extremos {sp.mean():+.3f} ticks de media "
              f"(rango {sp.min():+.3f} a {sp.max():+.3f})")
        A("")
        sp1 = np.mean([o[HORIZ_3A[0]]["spread"] for o in vivos])
        A(f"   CONTRA EL COSTO DE CRUZAR: cruzar cuesta del orden de 1 tick (medio-spread ~0,5 tick")
        A(f"   por lado). La separacion maxima a H=1s es {sp1:.3f} ticks.")
        if abs(sp1) < 1.0:
            A(f"   {abs(sp1):.3f} < 1 tick: la version 'adivinar la direccion con el desbalance y")
            A(f"   cruzar' esta MUERTA, y se cierra con numero. No alcanza ni para pagar la entrada.")
        else:
            A(f"   {abs(sp1):.3f} >= 1 tick: no se puede cerrar por costo. Hay que mirarla mas.")

    # ------------------------------------------------------------------ 3b
    A("")
    A("-" * 100)
    A("   3b - EL DESBALANCE COMO PREDICTOR DE SELECCION ADVERSA EN NUESTROS LLENADOS")
    A("-" * 100)
    A(f"   Orden pasiva al mejor precio, latencia {LAT_MS} ms, muerte a {MUERTE_TICKS} tick, "
      f"markout a H={HORIZ_3B}s.")
    A("   'I favorable' = desbalance con el signo de nuestro lado: >0 = la cola esta de nuestro lado.")
    A("   rho = correlacion entre I favorable y el markout. Positivo = el libro SI avisa.")
    A("")
    A(f"   {'dia':>16}{'llenado':>9}{'n llenos':>10}{'markout':>10}"
      + "".join(f"{'rho d=' + str(d):>11}" for d in ADELANTOS_MS))
    res3b = {}
    for i_d, (k, rec) in enumerate(recs.items()):
        rs = np.random.default_rng(SEMILLA + 7 + 101 * i_d)
        o = bloque_3b(rec, rs, A)
        res3b[k] = o
        if o is None:
            A(f"   {k[0]+'/'+k[1]:>16}   (pocos llenados)")
            continue
        A(f"   {k[0]+'/'+k[1]:>16}{o['llenado']:>9.3f}{o['n_llenos']:>10}{o['mk_todos']:>+10.4f}"
          + "".join(f"{o['por_adelanto'][d]['rho']:>+11.3f}" for d in ADELANTOS_MS))

    # ------------------------------------------------------------------ 3c
    A("")
    A("-" * 100)
    A("   3c - EL FILTRO: cuantos llenados sobreviven, y cuanto mejora. SIEMPRE JUNTOS.")
    A("-" * 100)
    A("   Filtro: se retira la orden cuando I favorable < umbral, con adelanto d antes del llenado.")
    A("   'sobreviven' = fraccion de los llenados originales que quedan. 'mk' en puntos.")
    A("")
    todos = [o for o in res3b.values() if o]
    if not todos:
        A("   Sin llenados suficientes en ningun dia.")
    else:
        for d in ADELANTOS_MS:
            A(f"   ADELANTO d = {d} ms")
            A(f"      {'umbral I':>10}{'sobreviven':>12}{'n':>8}{'mk filtrado':>14}"
              f"{'mk sin filtro':>15}{'mejora':>10}")
            for u in (-0.5, -0.25, 0.0, 0.25, 0.5):
                fav = np.concatenate([o["por_adelanto"][d]["I_fav"] for o in todos])
                mk = np.concatenate([o["por_adelanto"][d]["mk"] for o in todos])
                sel = fav >= u
                if sel.sum() < 10:
                    A(f"      {u:>10.2f}{sel.mean():>12.1%}{int(sel.sum()):>8}"
                      f"{'(muy pocos)':>14}")
                    continue
                A(f"      {u:>10.2f}{sel.mean():>12.1%}{int(sel.sum()):>8}"
                  f"{mk[sel].mean():>+14.4f}{mk.mean():>+15.4f}"
                  f"{mk[sel].mean()-mk.mean():>+10.4f}")
            A("")
    A("=" * 100)
    print("\n".join(R))
    return 0


if __name__ == "__main__":
    sys.exit(main())
