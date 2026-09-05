"""
VENTANA G - motor de reconstruccion del libro FIFO desde mbo (market-by-order) de Databento GLBX.

NO GASTA CARTUCHO. K = 261. Es infraestructura de medicion, no una prueba de estrategia. La caja
sellada no se toca. Se importa; no se corre solo.

mbo trae order_id, asi que el libro se reconstruye EXACTO: A (alta), C (baja), M (modificacion),
F (ejecucion de una orden en reposo), R (reset). T (print de trade) se ignora para el libro -las
reducciones vienen por F-. side: B = bid, A = ask.

reconstruir(path) devuelve, en RTH:
  bbo: (tc, bid, ask, bsz, asz) en cada cambio del MEJOR PRECIO (bid o ask). Es el dwell verdadero,
       contando cada cambio del tope, no solo los que caen en una operacion (que es lo que ve tbbo).
  fills: (tf, f_es_bid, fprice, fsize) de cada F, para descontar la cola de una orden pasiva.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

import databento as db

TICK = 0.25
RTH_INI, RTH_FIN = 13 * 60 + 30, 20 * 60 + 15   # 08:30-15:15 CT en UTC (CDT, todos los dias Abr-Sep)


def _cargar(path):
    df = db.DBNStore.from_file(str(path)).to_df(price_type="float", pretty_ts=True)
    ts = df.index.tz_convert("UTC").view("int64")           # ns UTC
    return (ts, df["action"].to_numpy(str), df["side"].to_numpy(str),
            df["price"].to_numpy(float), df["size"].to_numpy(np.int64),
            df["order_id"].to_numpy(np.int64))


def reconstruir(path, solo_rth=True):
    ts, act, side, price, size, oid = _cargar(path)
    n = len(ts)
    omap = {}                       # order_id -> [es_bid, price, size]
    bids, asks = {}, {}             # price -> size total
    best_bid, best_ask = -1.0, 1e18

    # salidas
    tc_l, bid_l, ask_l, bsz_l, asz_l = [], [], [], [], []
    tf_l, fb_l, fp_l, fs_l = [], [], [], []

    for i in range(n):
        a = act[i]
        if a == "A":
            p = price[i]; sz = size[i]; es_bid = side[i] == "B"
            if sz <= 0 or p != p:
                continue
            omap[oid[i]] = [es_bid, p, sz]
            if es_bid:
                bids[p] = bids.get(p, 0) + sz
                if p > best_bid:
                    best_bid = p
            else:
                asks[p] = asks.get(p, 0) + sz
                if p < best_ask:
                    best_ask = p
        elif a == "C" or a == "F":
            o = omap.get(oid[i])
            if o is None:
                continue
            es_bid, p, sz = o
            ex = sz if a == "C" else size[i]
            if es_bid:
                v = bids.get(p, 0) - ex
                if v > 0:
                    bids[p] = v
                else:
                    bids.pop(p, None)
                    if p >= best_bid:
                        best_bid = max(bids) if bids else -1.0
            else:
                v = asks.get(p, 0) - ex
                if v > 0:
                    asks[p] = v
                else:
                    asks.pop(p, None)
                    if p <= best_ask:
                        best_ask = min(asks) if asks else 1e18
            if a == "C":
                omap.pop(oid[i], None)
            else:
                sz -= ex
                if sz > 0:
                    o[2] = sz
                else:
                    omap.pop(oid[i], None)
                tf_l.append(ts[i]); fb_l.append(es_bid); fp_l.append(p); fs_l.append(ex)
        elif a == "M":
            o = omap.get(oid[i])
            p2 = price[i]; sz2 = size[i]; es_bid2 = side[i] == "B"
            if o is not None:
                eb0, p0, sz0 = o
                if eb0:
                    v = bids.get(p0, 0) - sz0
                    if v > 0:
                        bids[p0] = v
                    else:
                        bids.pop(p0, None)
                        if p0 >= best_bid:
                            best_bid = max(bids) if bids else -1.0
                else:
                    v = asks.get(p0, 0) - sz0
                    if v > 0:
                        asks[p0] = v
                    else:
                        asks.pop(p0, None)
                        if p0 <= best_ask:
                            best_ask = min(asks) if asks else 1e18
            if sz2 > 0 and p2 == p2:
                omap[oid[i]] = [es_bid2, p2, sz2]
                if es_bid2:
                    bids[p2] = bids.get(p2, 0) + sz2
                    if p2 > best_bid:
                        best_bid = p2
                else:
                    asks[p2] = asks.get(p2, 0) + sz2
                    if p2 < best_ask:
                        best_ask = p2
            else:
                omap.pop(oid[i], None)
        elif a == "R":
            omap.clear(); bids.clear(); asks.clear()
            best_bid, best_ask = -1.0, 1e18
            continue
        else:
            continue
        if (best_bid > 0 and best_ask < 1e17 and
                (not bid_l or best_bid != bid_l[-1] or best_ask != ask_l[-1])):
            tc_l.append(ts[i]); bid_l.append(best_bid); ask_l.append(best_ask)
            bsz_l.append(bids.get(best_bid, 0)); asz_l.append(asks.get(best_ask, 0))

    tc = np.array(tc_l, np.int64)
    bid = np.array(bid_l); ask = np.array(ask_l)
    bsz = np.array(bsz_l, np.int64); asz = np.array(asz_l, np.int64)
    tf = np.array(tf_l, np.int64); fb = np.array(fb_l, bool)
    fp = np.array(fp_l); fs = np.array(fs_l, np.int64)

    if solo_rth:
        seg = ((tc // 60_000_000_000) % 1440)
        m = (seg >= RTH_INI) & (seg < RTH_FIN)
        tc, bid, ask, bsz, asz = tc[m], bid[m], ask[m], bsz[m], asz[m]
        segf = ((tf // 60_000_000_000) % 1440)
        mf = (segf >= RTH_INI) & (segf < RTH_FIN)
        tf, fb, fp, fs = tf[mf], fb[mf], fp[mf], fs[mf]
    return dict(tc=tc, bid=bid, ask=ask, bsz=bsz, asz=asz, tf=tf, fb=fb, fp=fp, fs=fs)


def bbo_en(rec, t):
    """bid, ask, bsz, asz vigentes en el instante t (ns), por busqueda en la serie de cambios."""
    j = np.searchsorted(rec["tc"], t, side="right") - 1
    j = np.clip(j, 0, len(rec["tc"]) - 1)
    return rec["bid"][j], rec["ask"][j], rec["bsz"][j], rec["asz"][j], j


def mid_en(rec, t):
    b, a, _, _, _ = bbo_en(rec, t)
    return (b + a) / 2.0
