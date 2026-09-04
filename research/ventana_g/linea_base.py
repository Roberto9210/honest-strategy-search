"""
VENTANA G - MEDIR la linea de base que se venia afirmando.

NO GASTA CARTUCHO. K = 261. Es la medicion de una CONSTANTE del modelo, no la prueba de una
hipotesis de mercado: no hay estadistico contra un alfa, no se elige entre candidatas, no se
declara ninguna regla de operacion.

EL PROBLEMA. Todo el trabajo de esta ventana mide una brecha de +1,2 puntos contra una tasa
de acierto "sin ventaja" que se AFIRMO como S/(S+T) -el resultado de barreras de un paseo
sin drift- y nunca se observo. Si esa linea de base esta corrida por mas de 1,2 puntos, el
criterio no se distingue de la incertidumbre de su propio cero.

QUE SE MIDE. Se replica el bracket sobre ES a un minuto con entradas AL AZAR, y se cuenta:
  - la fraccion AMBIGUA: barras donde el objetivo y el stop caen las dos adentro, y por lo
    tanto la barra de un minuto no dice cual se toco primero;
  - la tasa observada bajo las dos convenciones extremas (todos los ambiguos a favor, todos
    en contra). Eso da una BANDA, no un punto.

CONTROL. El mismo procedimiento con un bracket tan ancho que ninguna barra de un minuto
pueda contener las dos barreras: ahi la fraccion ambigua tiene que dar 0% y la tasa
observada tiene que coincidir con S/(S+T). Si no coincide, el defecto no es la ambiguedad.

DATOS: ES 1-min Databento 2016-2019, fuera de la caja sellada (2020-01-02 -> 2026-08-19).
"""
import os
import sys

import numpy as np

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(RAIZ, "research", "ventaja_futuros"))
from terreno_tenencia import load_databento, DEGRADED_UTC  # noqa: E402

CELDAS = [(5, 10), (10, 10), (20, 10), (5, 20), (10, 20)]
NMUESTRA = 40_000
HORIZONTE = 1380          # minutos: una sesion completa
HORIZONTE_CTRL = 6900     # cinco sesiones, para que el bracket ancho resuelva
SEMILLA = 20260904


def cargar():
    df = load_databento()
    degr = set(df.loc[df["utc_date"].isin(DEGRADED_UTC), "sess"].unique())
    ncon = df.groupby("sess")["contract"].nunique()
    limpias = set(ncon[ncon == 1].index) - degr
    df = df[df["sess"].isin(limpias)].sort_values("ts_event_utc").reset_index(drop=True)
    return (df["close"].to_numpy(float), df["high"].to_numpy(float),
            df["low"].to_numpy(float), df["contract"].to_numpy(str))


def replica(cl, hi, lo, con, T_pt, S_pt, lado, horizonte, npaths=NMUESTRA, semilla=SEMILLA):
    """Replica el bracket desde entradas al azar. Devuelve (n_resueltos, gana_limpio,
    pierde_limpio, ambiguo, sin_resolver)."""
    rng = np.random.default_rng(semilla)
    n = len(cl)
    ent = rng.integers(0, n - horizonte - 1, npaths)
    # el escaneo entero tiene que quedar dentro del mismo contrato: un roll no es precio
    ok = con[ent] == con[ent + horizonte]
    ent = ent[ok]
    entrada = cl[ent]
    if lado == "largo":
        objetivo, stop = entrada + T_pt, entrada - S_pt
    else:
        objetivo, stop = entrada - T_pt, entrada + S_pt

    vivo = np.ones(len(ent), dtype=bool)
    gana = np.zeros(len(ent), dtype=bool)
    pierde = np.zeros(len(ent), dtype=bool)
    ambiguo = np.zeros(len(ent), dtype=bool)

    for k in range(1, horizonte + 1):
        if not vivo.any():
            break
        j = ent + k
        h, l = hi[j], lo[j]
        if lado == "largo":
            toca_obj, toca_stop = h >= objetivo, l <= stop
        else:
            toca_obj, toca_stop = l <= objetivo, h >= stop
        amb = vivo & toca_obj & toca_stop        # la barra no dice cual fue primero
        g = vivo & toca_obj & ~toca_stop
        p = vivo & toca_stop & ~toca_obj
        ambiguo |= amb
        gana |= g
        pierde |= p
        vivo &= ~(amb | g | p)

    return dict(n=len(ent), gana=int(gana.sum()), pierde=int(pierde.sum()),
                amb=int(ambiguo.sum()), vivo=int(vivo.sum()))


def banda(r):
    """Tasa observada con todos los ambiguos a favor y todos en contra, sobre resueltos."""
    res = r["gana"] + r["pierde"] + r["amb"]
    if res == 0:
        return float("nan"), float("nan"), 0.0
    favor = (r["gana"] + r["amb"]) / res
    contra = r["gana"] / res
    return favor, contra, r["amb"] / res


def main():
    cl, hi, lo, con = cargar()
    rango = hi - lo
    print("=" * 100)
    print("LINEA DE BASE - la tasa sin ventaja, MEDIDA en vez de afirmada")
    print("NO GASTA CARTUCHO. K = 261. Medicion de una constante del modelo.")
    print("=" * 100)
    print(f"\nES 1-min Databento 2016-2019, {len(cl):,} barras (contrato unico por sesion).")
    print(f"Rango de una barra de un minuto: mediana {np.median(rango):.2f}pt, "
          f"p99 {np.percentile(rango,99):.2f}pt, MAXIMO {rango.max():.2f}pt")
    ancho_ctrl = int(np.ceil(rango.max() / 2) + 5)
    print(f"-> el bracket de CONTROL usa {ancho_ctrl}pt a cada lado ({2*ancho_ctrl}pt de "
          f"separacion): ninguna barra observada puede contener los dos.")

    print("\n" + "=" * 100)
    print("CONTROL - bracket tan ancho que la ambiguedad es imposible")
    print("=" * 100)
    print(f"   {'lado':<8}{'n':>8}{'ambiguo':>10}{'asumido':>10}{'observado':>11}{'dif':>9}")
    ok_ctrl = True
    for lado in ("largo", "corto", ):
        r = replica(cl, hi, lo, con, ancho_ctrl, ancho_ctrl, lado, HORIZONTE_CTRL)
        f, c, a = banda(r)
        asum = 0.5
        print(f"   {lado:<8}{r['n']:>8}{a*100:>9.3f}%{asum*100:>9.1f}%{c*100:>10.1f}%"
              f"{(c-asum)*100:>+8.1f}")
        if a > 1e-9:
            ok_ctrl = False
    # el pooled con lado al azar es el que aisla la ambiguedad del drift
    rl = replica(cl, hi, lo, con, ancho_ctrl, ancho_ctrl, "largo", HORIZONTE_CTRL)
    rc = replica(cl, hi, lo, con, ancho_ctrl, ancho_ctrl, "corto", HORIZONTE_CTRL)
    res = sum(x["gana"] + x["pierde"] + x["amb"] for x in (rl, rc))
    pool = (rl["gana"] + rc["gana"]) / res
    amb_pool = (rl["amb"] + rc["amb"]) / res
    print(f"   {'pooled':<8}{res:>8}{amb_pool*100:>9.3f}%{50.0:>9.1f}%{pool*100:>10.1f}%"
          f"{(pool-0.5)*100:>+8.1f}")
    print(f"\n   ambiguedad = 0%: {'OK' if ok_ctrl else 'MAL'}")
    print(f"   CONTROL {'PASADO' if ok_ctrl and abs(pool-0.5) < 0.02 else 'MIRAR'}"
          f"  (la tasa pooled tiene que dar ~50% si el defecto era solo la ambiguedad)")

    print("\n" + "=" * 100)
    print("LA BANDA POR BRACKET - entradas al azar, horizonte de una sesion")
    print("=" * 100)
    print(f"   {'bracket':>11}{'lado':>8}{'n':>8}{'ambiguo':>10}{'sin resolv':>12}"
          f"{'asumido':>10}{'contra':>9}{'a favor':>10}{'ancho':>8}")
    filas = []
    for T, S in CELDAS:
        asum = S / (S + T)
        pool_g = pool_a = pool_r = 0
        for lado in ("largo", "corto"):
            r = replica(cl, hi, lo, con, T, S, lado, HORIZONTE)
            f, c, a = banda(r)
            res_i = r["gana"] + r["pierde"] + r["amb"]
            pool_g += r["gana"]; pool_a += r["amb"]; pool_r += res_i
            print(f"   {f'{T}pt:{S}pt':>11}{lado:>8}{r['n']:>8}{a*100:>9.2f}%"
                  f"{r['vivo']/r['n']*100:>11.1f}%{asum*100:>9.1f}%{c*100:>8.1f}%"
                  f"{f*100:>9.1f}%{(f-c)*100:>7.1f}")
        pc, pf = pool_g / pool_r, (pool_g + pool_a) / pool_r
        filas.append((T, S, asum, pc, pf, pool_a / pool_r))
        print(f"   {'':>11}{'POOLED':>8}{pool_r:>8}{pool_a/pool_r*100:>9.2f}%"
              f"{'':>12}{asum*100:>9.1f}%{pc*100:>8.1f}%{pf*100:>9.1f}%"
              f"{(pf-pc)*100:>7.1f}")

    print("\n" + "=" * 100)
    print("LA PREGUNTA QUE DECIDE: el +1,2 del criterio contra el ancho de la banda")
    print("=" * 100)
    print(f"   {'bracket':>11}{'asumido':>10}{'banda observada':>20}{'ancho banda':>14}"
          f"{'sesgo vs asumido':>19}")
    for T, S, asum, pc, pf, amb in filas:
        ancho = (pf - pc) * 100
        sesgo = ((pc + pf) / 2 - asum) * 100
        print(f"   {f'{T}pt:{S}pt':>11}{asum*100:>9.1f}%"
              f"{f'{pc*100:.1f}% - {pf*100:.1f}%':>20}{ancho:>13.2f}{sesgo:>+18.2f}")
    print("\n   'ancho banda' = cuanto no se sabe por la ambiguedad de la barra de un minuto.")
    print("   'sesgo' = cuanto se corre el centro de la banda respecto de S/(S+T) afirmado.")

    # La ambiguedad dio 0% pero el sesgo no: el defecto es OTRO. La hipotesis es CENSURA por
    # horizonte -las operaciones que no resuelven se excluyen, y no se excluyen al azar: se
    # excluyen las que iban a la barrera LEJANA-. Si es eso, alargar el horizonte tiene que
    # hacer converger la tasa observada a S/(S+T).
    print("\n" + "=" * 100)
    print("DE DONDE VIENE EL SESGO - prueba de horizonte (la ambiguedad ya dio 0%)")
    print("=" * 100)
    print(f"   {'bracket':>11}{'asumido':>10}{'1 sesion':>11}{'sin resolv':>12}"
          f"{'5 sesiones':>13}{'sin resolv':>12}{'converge?':>12}")
    for T, S in CELDAS:
        asum = S / (S + T)
        obs = {}
        for h in (HORIZONTE, HORIZONTE_CTRL):
            g = r_ = v = nn = 0
            for lado in ("largo", "corto"):
                r = replica(cl, hi, lo, con, T, S, lado, h)
                g += r["gana"]; r_ += r["gana"] + r["pierde"] + r["amb"]
                v += r["vivo"]; nn += r["n"]
            obs[h] = (g / r_, v / nn)
        d1 = abs(obs[HORIZONTE][0] - asum) * 100
        d5 = abs(obs[HORIZONTE_CTRL][0] - asum) * 100
        print(f"   {f'{T}pt:{S}pt':>11}{asum*100:>9.1f}%{obs[HORIZONTE][0]*100:>10.1f}%"
              f"{obs[HORIZONTE][1]*100:>11.1f}%{obs[HORIZONTE_CTRL][0]*100:>12.1f}%"
              f"{obs[HORIZONTE_CTRL][1]*100:>11.1f}%"
              f"{('SI' if d5 < d1 else 'no'):>12}")
    print("\n   Si al alargar el horizonte la tasa se acerca a S/(S+T), el sesgo es CENSURA:")
    print("   las que no resuelven no se pierden al azar, se pierden las que iban a la")
    print("   barrera LEJANA. Y el modelo supone que toda operacion resuelve alguna vez.")
    return filas


if __name__ == "__main__":
    main()
