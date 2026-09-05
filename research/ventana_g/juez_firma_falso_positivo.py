"""
A1 - LA TASA DE FALSO POSITIVO DE LA FIRMA DE TIMING.

NO GASTA CARTUCHO. K = 261. Candidatos SINTETICOS nulos sobre ES 1-min 2016-2018 (periodo de
trabajo). La caja sellada no se toca.

EL AGUJERO QUE SE MIDE. La firma solo puede CONTRADECIR, nunca confirmar. Se declara 'timing' y el
juez omite la nula de signo si mide rotacion >= 3,0sd con |signo| < 1,0sd. Un candidato NULO que sea
falso positivo de la rotacion sale con firma 'timing' y se le saca la nula de signo justo cuando mas
falta hacia. C10 no toca ese caso: su firma sale 'indefinida', o sea que aprueba por el camino facil.

LA PREGUNTA: con que frecuencia un candidato nulo saca firma 'timing'?
  <= 0,1%  -> el segundo cerrojo (la pasiva, que NUNCA se omite) alcanza.
  >  0,1%  -> el umbral de firma esta mal puesto y hay que subirlo.
LO HARIA FALLAR: una tasa por encima de lo que la pasiva sola puede contener. Por eso no se mide
solo la firma: se mide tambien cuantos de esos falsos positivos de firma llegarian a APROBACION,
que es lo unico que hace dano.

POR QUE HACE FALTA UNA TABLA DE DESENLACES. Mil candidatos x 200 rotaciones x ~3.700 operaciones son
~740 millones de resoluciones de bracket; el juez las hace con un bucle de Python y tardaria dias. El
desenlace de una operacion depende SOLO de (ranura, lado): se precalcula UNA vez para cada barra del
periodo y las 740 millones pasan a ser indexado. La tabla se verifica contra J.resolver antes de
usarla (control 0): si no coincide exactamente, el resto no vale nada.
"""

import math
import os
import sys
import time

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import juez as J  # noqa: E402

CELDA = dict(tipo="bracket", objetivo_pt=5, stop_pt=20)
PASO = 300                      # la misma grilla que usa el control C1
ANIOS = (2016, 2017, 2018)
NPERM = 200
N_CAND = int(os.environ.get("N_CAND", "1000"))
SEMILLA = 20260905


# =========================================================================================
# La tabla de desenlaces: para CADA barra del periodo, el resultado de entrar ahi de cada lado
# =========================================================================================
def tabla_desenlaces(m, ses, regla, exceso):
    """pts/ten por barra y por lado, para todas las barras de las sesiones `ses`.

    Mismo criterio que J.resolver, incluida la barra ambigua contada PERDIDA y la marca a mercado
    al corte de sesion. Vectorizado por sesion con una matriz triangular de maximos/minimos
    corridos: para la entrada i, el primer j>i donde el maximo de hi[i+1..j] toca el objetivo o el
    minimo de lo[i+1..j] toca el stop.
    """
    T, S = float(regla["objetivo_pt"]), float(regla["stop_pt"])
    n_bar = m["n"]
    ptsL = np.full(n_bar, np.nan); ptsS = np.full(n_bar, np.nan)
    tenL = np.zeros(n_bar, np.int64); tenS = np.zeros(n_bar, np.int64)
    cl, hi, lo = m["cl"], m["hi"], m["lo"]
    for k in ses:
        a, b = int(m["ini"][k]), int(m["fin"][k])
        n = b - a
        if n < 2:
            # Sesion de una sola barra: J.resolver no tiene ventana (hi[a+1:b] es vacio), marca a
            # mercado contra el propio cierre de entrada -> 0 puntos, 0 barras. Se rellena igual en
            # vez de dejar NaN: una rotacion puede caer ahi y un solo NaN envenena todo el candidato.
            ptsL[a:b] = 0.0; ptsS[a:b] = 0.0; tenL[a:b] = 0; tenS[a:b] = 0
            continue
        c = cl[a:b].astype(np.float64)
        h = hi[a:b].astype(np.float64); l = lo[a:b].astype(np.float64)
        # runmax[i, j] = max(h[i+1..j]) para j > i; -inf en j <= i
        Hm = np.broadcast_to(h, (n, n)).copy()
        Lm = np.broadcast_to(l, (n, n)).copy()
        tri = np.tril(np.ones((n, n), bool))            # j <= i
        Hm[tri] = -np.inf
        Lm[tri] = np.inf
        runmax = np.maximum.accumulate(Hm, axis=1)
        runmin = np.minimum.accumulate(Lm, axis=1)
        for lado, pts_out, ten_out in ((+1, ptsL, tenL), (-1, ptsS, tenS)):
            if lado > 0:
                golpe_obj = runmax >= (c + T)[:, None]
                golpe_stop = runmin <= (c - S)[:, None]
            else:
                golpe_obj = runmin <= (c - T)[:, None]
                golpe_stop = runmax >= (c + S)[:, None]
            algo = golpe_obj | golpe_stop
            hay = algo.any(axis=1)
            j = algo.argmax(axis=1)                      # primer True; 0 si no hay
            ii = np.arange(n)
            solo_obj = golpe_obj[ii, j] & ~golpe_stop[ii, j]
            pts = np.where(solo_obj, T, -(S + exceso))
            # sin golpe: marca a mercado en el ultimo cierre de la sesion
            mtm = lado * (c[n - 1] - c)
            pts_out[a:b] = np.where(hay, pts, mtm)
            ten_out[a:b] = np.where(hay, j - ii, np.maximum(n - 1 - ii, 0))
    return ptsL, ptsS, tenL, tenS


def control_0_tabla(m, ses, ptsL, ptsS, tenL, tenS, exceso, rs):
    """CONTROL 0: la tabla tiene que dar EXACTAMENTE lo mismo que J.resolver.
    LO HARIA FALLAR: una sola ranura donde no coincida."""
    cand = np.concatenate([np.arange(int(m["ini"][k]), int(m["fin"][k]) - 1) for k in ses[:400]])
    idx = rs.choice(cand, size=3000, replace=False)
    okp = okt = True
    for lado, pt_t, ten_t in ((+1, ptsL, tenL), (-1, ptsS, tenS)):
        p, t = J.resolver(m, idx, np.full(len(idx), float(lado)), CELDA, exceso)
        okp &= bool(np.allclose(p, pt_t[idx], atol=1e-9))
        okt &= bool(np.array_equal(t, ten_t[idx]))
    return okp, okt, len(idx)


# =========================================================================================
# El camino rapido: zA, zB, z_pas de un candidato, con la tabla
# =========================================================================================
def constantes(m, contratos=1, inst="ES"):
    T, S = float(CELDA["objetivo_pt"]), float(CELDA["stop_pt"])
    p = S / (S + T)
    signo_corr = 1 - 2 * p
    o_cons = J.O_SOBREPASO * (1 + J.O_ERROR_REL) if signo_corr > 0 else J.O_SOBREPASO * (1 - J.O_ERROR_REL)
    return dict(punto=J.PUNTO[inst], c1=J.COMISION[inst] * contratos, contratos=contratos,
                sesgo_pt=o_cons * signo_corr,
                error_o_pt=J.O_SOBREPASO * J.O_ERROR_REL * abs(signo_corr),
                exceso=J.EXCESO_STOP[int(S)])


def evaluar(m, K, idx, sgn, tab, rp, npermuta=NPERM, detalle=False):
    """Devuelve (zA, zB, z_pas, obs). Replica juzgar_periodo en modo CRUCE, sin regimen ni cadena.

    detalle=True devuelve ademas sd_tot, n_ses y rot_indep, que hacen falta para aplicar las mismas
    negativas que el juez (NO MEDIBLE por ventana angosta o por resolucion). Se agrego DESPUES de la
    corrida de 20.000 y por eso es opcional: el camino por defecto queda identico y la salida
    commiteada de A1 sigue siendo reproducible."""
    ptsL, ptsS, tenL, tenS = tab
    punto, contratos, c1 = K["punto"], K["contratos"], K["c1"]
    sesgo_pt = K["sesgo_pt"]
    ses_de, slip = m["ses_de"], m["slip_ses_pt"]

    def dolares(pts, ii):
        return (pts - sesgo_pt) * punto * contratos - c1 - slip[ses_de[ii]] * punto * contratos

    lo_b, hi_b = int(idx.min()), int(m["fin_de"][idx.max()] - 1)
    ses_lo, ses_hi = int(ses_de[lo_b]), int(ses_de[hi_b])
    n_ses = ses_hi - ses_lo + 1
    L = hi_b - lo_b + 1
    largo = sgn > 0
    pts = np.where(largo, ptsL[idx], ptsS[idx])
    ten = np.where(largo, tenL[idx], tenS[idx])
    v_obs = np.bincount(ses_de[idx] - ses_lo, weights=dolares(pts, idx), minlength=n_ses)
    obs = float(v_obs.mean())

    medA = np.empty(npermuta)
    for i in range(npermuta):
        k = int(rp.integers(1, L))
        i2 = lo_b + ((idx - lo_b + k) % L)
        p2 = np.where(largo, ptsL[i2], ptsS[i2])
        medA[i] = np.bincount(ses_de[i2] - ses_lo, weights=dolares(p2, i2),
                              minlength=n_ses).mean()
    dL, dS = dolares(ptsL[idx], idx), dolares(ptsS[idx], idx)
    ses_rel = ses_de[idx] - ses_lo
    VB = np.empty((npermuta, n_ses))
    for i in range(npermuta):
        flip = rp.random(len(sgn)) < 0.5
        VB[i] = np.bincount(ses_rel, weights=np.where(largo ^ flip, dL, dS), minlength=n_ses)
    medB = VB.mean(axis=1)

    expo_prom = float((sgn * contratos * ten).sum() / L)
    pasiva = expo_prom * (m["cl"][hi_b] - m["cl"][lo_b]) * punto / n_ses
    sd_perm = max(medA.std(ddof=1), medB.std(ddof=1))
    err_o = K["error_o_pt"] * punto * contratos * (len(idx) / n_ses)
    sd_tot = math.sqrt(sd_perm ** 2 + err_o ** 2)
    if detalle:
        return dict(zA=(obs - medA.mean()) / sd_tot, zB=(obs - medB.mean()) / sd_tot,
                    z_pas=(obs - pasiva) / sd_tot, obs=obs, sd_tot=sd_tot, n_ses=n_ses,
                    n_op=len(idx), rot_indep=n_ses / J.L_ESTRELLA_SES)
    return ((obs - medA.mean()) / sd_tot, (obs - medB.mean()) / sd_tot,
            (obs - pasiva) / sd_tot, obs)


def wilson(k, n, z=1.96):
    if n == 0:
        return 0.0, 1.0
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


def main():
    R = []
    A = R.append
    A("=" * 98)
    A("A1 - TASA DE FALSO POSITIVO DE LA FIRMA DE TIMING, sobre candidatos NULOS")
    A("NO GASTA CARTUCHO. K = 261. La caja sellada no se toca.")
    A("=" * 98)
    m = J.cargar_mercado()
    ses = np.flatnonzero(np.isin(m["anio_ses"], ANIOS))
    K = constantes(m)
    rs = np.random.default_rng(SEMILLA)

    t0 = time.time()
    tab = tabla_desenlaces(m, ses, CELDA, K["exceso"])
    A(f"\n   tabla de desenlaces: {len(ses):,} sesiones, {int(m['fin'][ses[-1]] - m['ini'][ses[0]]):,} "
      f"barras, los dos lados, en {time.time()-t0:.0f}s")
    b0, b1 = int(m["ini"][ses[0]]), int(m["fin"][ses[-1]])
    huecos = int(np.isnan(tab[0][b0:b1]).sum() + np.isnan(tab[1][b0:b1]).sum())
    okp, okt, nver = control_0_tabla(m, ses, *tab, K["exceso"], rs)
    A(f"   CONTROL 0 (la tabla contra J.resolver, {nver:,} ranuras al azar de los dos lados):")
    A(f"      puntos identicos: {'SI' if okp else 'NO'}      tenencia identica: {'SI' if okt else 'NO'}"
      f"      barras sin rellenar: {huecos} (tienen que ser 0: una rotacion cae ahi y envenena todo)")
    if not (okp and okt and huecos == 0):
        A("      LA TABLA NO COINCIDE. Todo lo que sigue seria basura. Se corta aca.")
        print("\n".join(R))
        return 1

    # --- los mil candidatos nulos ----------------------------------------------------------
    A(f"\n   {N_CAND:,} candidatos NULOS: grilla de {PASO} barras con corrimiento al azar sobre "
      f"{ANIOS[0]}-{ANIOS[-1]},")
    A(f"   lado por moneda, {NPERM} rotaciones y {NPERM} signos cada uno. Es el mismo C1 mil veces.")
    z_req = J.z_requerido(1)
    filas = []
    t0 = time.time()
    for c in range(N_CAND):
        off = int(rs.integers(0, PASO))
        idx = np.concatenate([np.arange(int(m["ini"][k]) + off, int(m["fin"][k]) - 1, PASO)
                              for k in ses])
        sgn = np.where(rs.random(len(idx)) < 0.5, 1.0, -1.0)
        rp = np.random.default_rng(SEMILLA + 1 + c)
        zA, zB, zp, obs = evaluar(m, K, idx, sgn, tab, rp)
        filas.append((zA, zB, zp, obs))
        if (c + 1) % 100 == 0:
            print(f"      ... {c+1}/{N_CAND}  ({time.time()-t0:.0f}s)", file=sys.stderr)
    F = np.array(filas)
    zA, zB, zp = F[:, 0], F[:, 1], F[:, 2]
    A(f"   corridos en {time.time()-t0:.0f}s")

    firma_timing = (zA >= J.Z_BASE) & (np.abs(zB) < 1.0)
    firma_dir = (zA >= J.Z_BASE) & (zB >= J.Z_BASE)
    n = len(zA)
    A("")
    A("-" * 98)
    A("   LO QUE DA LA NULA")
    A("-" * 98)
    A(f"   zA (rotacion): media {zA.mean():+.3f}  desvio {zA.std(ddof=1):.3f}  "
      f"max {zA.max():+.2f}   |   zB (signo): media {zB.mean():+.3f}  desvio {zB.std(ddof=1):.3f}  "
      f"max {zB.max():+.2f}")
    A(f"   correlacion zA con zB: {np.corrcoef(zA, zB)[0,1]:+.3f}   "
      f"(si fueran independientes, la firma timing seria casi imposible; si van pegadas, tampoco)")
    A("")
    A(f"   {'muestra':>10}  {'zA>=3 sola':>12}  {'FIRMA timing':>14}  {'IC95 arriba':>12}  "
      f"{'FIRMA direcc.':>14}")
    for nsub in sorted({min(1000, n), n}):
        k1 = int((zA[:nsub] >= J.Z_BASE).sum())
        k2 = int(firma_timing[:nsub].sum())
        k3 = int(firma_dir[:nsub].sum())
        _, hs = wilson(k2, nsub)
        A(f"   {nsub:>10,}  {k1:>4} = {k1/nsub:>6.2%}  {k2:>4} = {k2/nsub:>7.3%}  {hs:>11.3%}  "
          f"{k3:>4} = {k3/nsub:>6.2%}")
    kt = int(firma_timing.sum())
    lo, hi = wilson(kt, n)
    A("")
    A("   POR QUE SALE ASI: bajo la nula zA y zB miden el MISMO observado contra dos nulas distintas")
    A("   pero centradas en lo mismo. Un candidato nulo que por azar quede alto contra la rotacion")
    A("   tiende a quedar alto tambien contra el signo, y entonces su firma es 'direccional', no")
    A("   'timing'. La firma de timing exige la combinacion RARA: alto contra una y neutro contra la")
    A("   otra. Eso es lo que la hace dificil de sacar por azar.")

    # --- lo unico que hace dano: que ademas APRUEBE -----------------------------------------
    A("")
    A("-" * 98)
    A("   LA PREGUNTA QUE IMPORTA: cuantos de esos llegarian a APROBACION")
    A("-" * 98)
    A("   Sacar firma 'timing' por azar no aprueba nada por si solo. Para que un nulo se APRUEBE")
    A("   declarando 'timing' hace falta que ADEMAS pase el informativo relajado, que sigue siendo")
    A(f"   min(rotacion, PASIVA) >= {z_req:.2f}. La pasiva NUNCA se omite: es el segundo cerrojo.")
    z_info_relaj = np.minimum(zA, zp)
    z_info_estr = np.minimum(np.minimum(zA, zB), zp)
    aprob_relaj = firma_timing & (z_info_relaj >= z_req)
    aprob_estr = z_info_estr >= z_req
    ka = int(aprob_relaj.sum())
    loa, hia = wilson(ka, n)
    A("")
    A(f"   nulos que pasarian el informativo ESTRICTO (min de las tres):      {int(aprob_estr.sum())}/{n}"
      f" = {aprob_estr.mean():.2%}")
    A(f"   nulos con firma timing que pasarian el RELAJADO (min rot, pasiva): {ka}/{n} = {ka/n:.2%}"
      f"   IC95 [{loa:.2%}; {hia:.2%}]")
    A(f"   costo del arreglo, en falsos positivos: {ka - int(aprob_estr.sum()):+d} sobre {n} candidatos")
    if kt:
        sub = z_info_relaj[firma_timing]
        A(f"   de los {kt} con firma timing, la pasiva los frena a: min {sub.min():+.2f} / "
          f"mediana {np.median(sub):+.2f} / max {sub.max():+.2f} desvios "
          f"(hace falta {z_req:.2f})")

    A("")
    A("=" * 98)
    A("   VEREDICTO DE A1")
    A("=" * 98)
    vara = 0.001
    if kt / n <= vara:
        A(f"   La tasa de firma 'timing' es {kt/n:.2%}, por DEBAJO de la vara de {vara:.1%}.")
    else:
        A(f"   La tasa de firma 'timing' es {kt/n:.2%}, POR ENCIMA de la vara de {vara:.1%}.")
    if ka == 0:
        A(f"   Y NINGUNO de los {n:,} nulos llega a aprobacion declarando 'timing': la pasiva, que")
        A(f"   nunca se omite, los frena a todos. El segundo cerrojo alcanza.")
    else:
        A(f"   Y {ka} de {n:,} llegarian a aprobacion. El umbral de firma hay que subirlo.")
    A("")
    A(f"   HONESTIDAD SOBRE ESTE NUMERO: con {n:,} candidatos, el limite superior del intervalo es")
    A(f"   {hi:.2%} para la firma y {hia:.2%} para la aprobacion. Una tasa verdadera por debajo de")
    A(f"   ese limite no queda descartada por esta corrida; lo que queda medido es la cota.")
    A("=" * 98)
    print("\n".join(R))
    return 0


if __name__ == "__main__":
    sys.exit(main())
