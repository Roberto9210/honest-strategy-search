"""
VENTANA G - EL ESTUDIO DE ENTRADA PASIVA (mbo): la entrada pasiva AHORRA el medio-spread o lo DEVUELVE
como seleccion adversa?

NO GASTA CARTUCHO. K = 261. Medicion de una constante de ejecucion sobre datos ya comprados; entradas
AL AZAR (no una estrategia). No se elige entre candidatas ni se declara regla. La caja sellada no se
toca. Diseno fijado en MBO_DISENO_entrada_pasiva.md.

MECANICA (pasiva pura, decision D1 de Roberto): en la senal, tras una latencia L, se coloca una orden
limite en el mejor precio del lado que toca (bid para largo, ask para corto). La orden:
  - se LLENA cuando el volumen ejecutado (eventos F) en su precio y lado, despues de entrar, supera la
    cola que tenia adelante al entrar (FIFO; los cancels adelante NO cuentan -> conservador, llena mas
    lento que la realidad);
  - MUERE cuando el mejor precio se aleja un escalon (o dos, sensibilidad): para un bid, cuando el
    mejor bid sube d ticks (el mercado se fue para arriba y me lo perdi);
  - si no pasa nada en 300 s, queda SIN LLENAR.

LO QUE DECIDE: el markout del llenado = (mid(t_llenado + H) - precio_limite) * lado. El limite esta a
medio-spread del mid, asi que en el instante del llenado el markout vale ~+medio-spread (~+0,13 pt); si
a horizonte H se mantiene en +0,13 la pasiva AHORRA el spread; si cae a 0 la seleccion adversa se lo
comio; si es negativo es peor que cruzar. Se barre H (D2: es medicion, no decision).

DOS LATENCIAS (0 ms y 250 ms), DOS UMBRALES DE MUERTE (1 y 2 ticks), y todo SEPARADO POR RAFAGA Y
CALMA (definicion medida abajo). Latencia 250 ms = ida y vuelta residencial a Aurora.

SUPUESTOS DE LOS QUE CUELGA EL NUMERO (impresos con el resultado): 1 contrato al final de la cola;
cancels adelante no descuentan (conservador); orden en el mejor precio; muerte al alejarse d ticks;
un dia por regimen, sin agitado en 2026; latencia 250 ms de ingenieria, anclada al dwell medido.
"""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np

import mbo_lib as M

TICK = 0.25
DIR = Path(__file__).resolve().parents[2] / "data" / "microestructura"
ARCHIVOS = [("B", "bajo", "mbo_ESn0_B_bajo_2017-06-07.dbn.zst"),
            ("B", "medio", "mbo_ESn0_B_medio_2019-05-01.dbn.zst"),
            ("B", "alto", "mbo_ESn0_B_alto_2018-04-25.dbn.zst"),
            ("A", "bajo", "mbo_ESn0_A_bajo_2026-08-26.dbn.zst"),
            ("A", "medio", "mbo_ESn0_A_medio_2026-09-02.dbn.zst"),
            ("A", "altoREL", "mbo_ESn0_A_altoREL_2026-09-01.dbn.zst")]
N_ENTRADAS = 3000
LATENCIAS_MS = [0, 250]
MUERTES = [1, 2]
HORIZONTES_S = [1, 5, 30, 60, 300]
VENTANA_NS = 300 * 1_000_000_000        # 300 s tope para llenar/morir
SEMILLA = 20260904
CON_TAMANO = os.environ.get("MBO_CON_TAMANO") == "1"


def dwell_ms(rec):
    d = np.diff(rec["tc"]) / 1e6
    return float(np.median(d)), float(d.mean())


def simular(rec, entradas, lado, L_ns, d_ticks):
    """entradas: ts de senal (ns). lado: +1 largo, -1 corto. Devuelve por entrada:
    filled(bool), t_fill(ns o -1), lim(precio), mid_entry, y el markout se calcula afuera."""
    tc, bid, ask, bsz, asz = rec["tc"], rec["bid"], rec["ask"], rec["bsz"], rec["asz"]
    tf, fb, fp, fs = rec["tf"], rec["fb"], rec["fp"], rec["fs"]
    n = len(entradas)
    filled = np.zeros(n, bool); t_fill = np.full(n, -1, np.int64)
    lim = np.zeros(n); mid_e = np.zeros(n)
    for k in range(n):
        te = entradas[k] + L_ns
        b, a, bs, as_, _ = M.bbo_en(rec, te)
        mid_e[k] = (b + a) / 2.0
        s_k = lado[k]
        if s_k > 0:
            mi = b; cola = bs; thr = mi + d_ticks * TICK
            es_bid = True
        else:
            mi = a; cola = as_; thr = mi - d_ticks * TICK
            es_bid = False
        lim[k] = mi
        # muerte: primer cambio de bbo en (te, te+ventana] con el mejor precio alejado d ticks
        j0 = np.searchsorted(tc, te, side="right")
        j1 = np.searchsorted(tc, te + VENTANA_NS, side="right")
        t_muerte = np.int64(te + VENTANA_NS)
        if j1 > j0:
            if s_k > 0:
                w = np.flatnonzero(bid[j0:j1] >= thr)
            else:
                w = np.flatnonzero(ask[j0:j1] <= thr)
            if len(w):
                t_muerte = tc[j0 + w[0]]
        # llenado: volumen F acumulado en mi precio y lado, despues de te, alcanza la cola
        i0 = np.searchsorted(tf, te, side="right")
        i1 = np.searchsorted(tf, te + VENTANA_NS, side="right")
        t_ll = np.int64(-1)
        if i1 > i0:
            sel = (fb[i0:i1] == es_bid) & (np.abs(fp[i0:i1] - mi) < 1e-6)
            if sel.any():
                vol = np.cumsum(fs[i0:i1] * sel)
                hit = np.flatnonzero(vol >= cola)
                if len(hit):
                    t_ll = tf[i0 + hit[0]]
        if t_ll >= 0 and t_ll <= t_muerte:
            filled[k] = True; t_fill[k] = t_ll
    return filled, t_fill, lim, mid_e


def main():
    print("=" * 100)
    print("ESTUDIO DE ENTRADA PASIVA (mbo): ahorra el medio-spread o lo devuelve como seleccion adversa?")
    print("NO GASTA CARTUCHO. K = 261. Entradas AL AZAR. La caja sellada no se toca.")
    print("=" * 100)
    rng = np.random.default_rng(SEMILLA)
    agg = {}
    for epoca, tercil, fn in ARCHIVOS:
        p = DIR / fn
        if not p.exists():
            print(f"\n[{epoca} {tercil}] FALTA {fn}"); continue
        # MBO_CON_TAMANO=1 usa el libro que ve tambien los cambios de TAMANO al mejor precio. La
        # calibracion original (MARKOUT_PASIVO / LLENADO_PASIVO) se hizo SIN eso, con el libro que
        # solo veia cambios de precio: el tamano de cola que decide el llenado estaba congelado
        # desde el ultimo cambio de precio (669 ms de antiguedad mediana, desbalance_diagnostico.py).
        # Por defecto queda apagado para que la salida vieja siga siendo reproducible.
        rec = M.reconstruir(str(p), con_tamano=CON_TAMANO)
        tc = rec["tc"]
        dwm, dwmean = dwell_ms(rec)
        # entradas al azar en el rango cubierto, dejando 300s de cola
        t0, t1 = tc[0], tc[-1] - VENTANA_NS
        ent = np.sort(rng.integers(t0, t1, N_ENTRADAS))
        lado = rng.choice([-1, 1], N_ENTRADAS)
        # rafaga vs calma: cambios de bbo en el segundo previo a cada senal; corte = mediana
        j_prev = np.searchsorted(tc, ent) - np.searchsorted(tc, ent - 1_000_000_000)
        corte = int(np.median(j_prev)); es_rafaga = j_prev > corte
        print(f"\n[{epoca} {tercil}]  bbo changes {len(tc):,}  fills {len(rec['tf']):,}  "
              f"dwell true ms: med {dwm:.2f} / mean {dwmean:.0f}   corte rafaga (cambios/seg) = {corte}")
        for d in MUERTES:
            for L in LATENCIAS_MS:
                filled, t_fill, lim, mid_e = simular(rec, ent, lado, L * 1_000_000, d)
                fr = filled.mean()
                # markout en el llenado a cada horizonte, side-signed (positivo = favorable)
                mk = {}
                for H in HORIZONTES_S:
                    tt = t_fill[filled] + H * 1_000_000_000
                    midH = M.mid_en(rec, tt)
                    mk[H] = float(np.mean((midH - lim[filled]) * lado[filled]))
                fr_raf = filled[es_rafaga].mean() if es_rafaga.any() else float("nan")
                fr_cal = filled[~es_rafaga].mean() if (~es_rafaga).any() else float("nan")

                def mk_sub(H, mask):
                    mm = filled & mask
                    if not mm.any():
                        return float("nan")
                    midH = M.mid_en(rec, t_fill[mm] + H * 1_000_000_000)
                    return float(np.mean((midH - lim[mm]) * lado[mm]))
                mk_raf = {H: mk_sub(H, es_rafaga) for H in (1, 30)}
                mk_cal = {H: mk_sub(H, ~es_rafaga) for H in (1, 30)}
                agg[(epoca, tercil, d, L)] = dict(fr=fr, fr_raf=fr_raf, fr_cal=fr_cal, mk=mk,
                                                  mk_raf=mk_raf, mk_cal=mk_cal, n_fill=int(filled.sum()))
                mkstr = "  ".join(f"H{H}s {mk[H]:+.4f}" for H in HORIZONTES_S)
                print(f"   muerte {d}tk  lat {L:>3}ms  llenado {fr*100:5.1f}%  "
                      f"(rafaga {fr_raf*100:4.1f}% / calma {fr_cal*100:4.1f}%)  markout pt: {mkstr}")
                if d == 1:
                    print(f"      markout por regimen (pt): rafaga H1s {mk_raf[1]:+.4f} H30s {mk_raf[30]:+.4f}"
                          f"   |   calma H1s {mk_cal[1]:+.4f} H30s {mk_cal[30]:+.4f}")
        # cruce independiente: markout de los llenados REALES (todos los F en el mejor precio)
        # -> seleccion adversa agregada del mercado, sin mi modelo de cola
        real_markout(rec)
    resumen(agg)


def real_markout(rec):
    """Markout de TODOS los fills reales en el mejor precio, como cruce del modelo de cola."""
    tf, fb, fp = rec["tf"], rec["fb"], rec["fp"]
    b, a, _, _, _ = M.bbo_en(rec, tf)
    en_mejor = (fb & (np.abs(fp - b) < 1e-6)) | (~fb & (np.abs(fp - a) < 1e-6))
    s = np.where(fb, 1.0, -1.0)[en_mejor]
    fpx = fp[en_mejor]; tt = tf[en_mejor]
    out = []
    for H in (1, 30, 300):
        midH = M.mid_en(rec, tt + H * 1_000_000_000)
        out.append(f"H{H}s {np.mean((midH - fpx) * s):+.4f}")
    print(f"   [cruce] markout de {en_mejor.sum():,} fills REALES en el mejor precio (pt): " + "  ".join(out))


def resumen(agg):
    print("\n" + "=" * 100)
    print("RESUMEN - markout a H=30s (pt) y llenado, muerte 1 tick. medio-spread ahorrado ~ +0,13 pt.")
    print("=" * 100)
    print(f"   {'epoca':>6}{'tercil':>9}{'lat ms':>8}{'llenado':>9}{'markout H30s':>14}{'veredicto':>26}")
    for (epoca, tercil, d, L), r in agg.items():
        if d != 1:
            continue
        m30 = r["mk"][30]
        ver = ("AHORRA (~medio-spread)" if m30 > 0.09 else
               "DEVUELVE (adversa se lo come)" if m30 < 0.04 else "parcial")
        print(f"   {epoca:>6}{tercil:>9}{L:>8}{r['fr']*100:>8.1f}%{m30:>+14.4f}{ver:>26}")


if __name__ == "__main__":
    main()
