"""
VENTANA G - BOOTSTRAP POR BLOQUES APAREADO EN LA TASA DE SIN-RESOLVER. El test que decide.

NO GASTA CARTUCHO. K = 261. Validacion de instrumento y medicion de una nula. No hay
hipotesis de mercado contra el alfa heredado, no se elige entre candidatas, no se declara
ninguna regla de operacion. La caja sellada (2020-01-02 -> 2026-08-19) no se toca.

EL DEFECTO QUE REPARA. La nula IID del test anterior dejaba 1,6% sin resolver a una sesion
donde ES real deja 35,6% (20pt:10pt). No eran comparables en el termino MAS GRANDE del
calculo. Un bootstrap por BLOQUES conserva la estructura serial adentro del bloque, resuelve
mas lento, y el largo del bloque se puede CALIBRAR contra la tasa real de sin-resolver.

LAS DOS RESPUESTAS POSIBLES, escritas antes de correr:
  - el residuo DESAPARECE -> era estructura serial. Corrige la LINEA DE BASE y NO produce
    direccion. Es una correccion de la vara, no una ventaja.
  - el residuo SOBREVIVE -> es algo que todavia no sabemos nombrar. Se reporta el numero y
    su significancia con el error bueno, y no se le inventa explicacion.

CUATRO MODOS, y el cuarto existe por una honestidad que hay que decir: un bootstrap por
bloques conserva TODA la estructura serial del bloque, no solo el agrupamiento de
volatilidad. Tambien conserva la tendencia local. Por eso va un modo con cada bloque
centrado a media cero por separado: eso saca la tendencia local y deja la volatilidad.

  1. IID (L=1)                    - la nula vieja, con K grande
  2. BLOQUES L*                   - L calibrado contra la tasa real de sin-resolver
  3. CONTROL: bloques sobre datos BARAJADOS - tiene que reproducir la nula IID
  4. BLOQUES L* con cada bloque centrado - separa tendencia local de volatilidad

CONTROL, con su condicion de falla declarada. Sobre datos SIN agrupamiento -los mismos
tripletes barajados al azar- el bootstrap por bloques tiene que dar lo mismo que L=1.
   QUE LO HARIA FALLAR: un residuo distinto de cero ahi. Significaria que el metodo de
   bloques mete sesgo propio y entonces nada de lo que mida sirve.

TEST DE DIRECCION, adentro de la misma corrida. Se reporta el sesgo de CADA LADO por
separado, corregido por su propia censura:
   mismo signo en los dos -> efecto de volatilidad o de forma, sin direccion, sin ventaja.
   signo opuesto          -> direccional.
   ANTI-IDENTIDAD: para T = S el largo y el corto usan LOS MISMOS DOS NIVELES con las
   etiquetas dadas vuelta, asi que ahi el test NO PUEDE dar otra cosa que signo opuesto: es
   vacio. Para T != S los niveles son distintos y el test si mide algo. Se verifica
   numericamente comparando gana(largo) contra pierde(corto).

K SUBIDO. Con 10 series el desvio del desvio es 1/raiz(2(K-1)) = 23,6%. Con 32 baja a 12,7%.

NOTA de construccion: los tripletes ya excluyen los 16 saltos de contrato, pero un bloque
puede quedar a caballo de uno de esos cortes. Son 16 sobre 1,36 millones de posiciones: por
debajo del 2% de los arranques posibles con el L mas largo de la grilla.
"""
import numpy as np

from linea_base import cargar, replica
from sintetico import armar, tripletes

SESION = 1380
HORIZONTES = [("1 sesion", SESION), ("5 sesiones", 5 * SESION)]
BRACKETS = [(10, 10), (20, 10), (5, 20)]
NPATHS = 30_000
SEMILLA = 20260904
K_GRANDE = 32
K_CTRL = 8
K_CENTRADO = 12
BRACKET_CAL = (20, 10)
LS_CAL = [1, 5, 15, 60, 240, 780, 1380, 2760, 5520, 11040]

# MEDIDO sobre ES real, salida_linea_base.txt, pooled, entradas al azar.
REAL_SIN_RES = {"1 sesion": {(10, 10): 19.0, (20, 10): 35.6, (5, 20): 17.4},
                "5 sesiones": {(10, 10): 0.7, (20, 10): 4.0, (5, 20): 1.1}}
# Sesgo pooled MEDIDO sobre ES real, sin des-driftar, mismos horizontes.
REAL_SESGO = {"1 sesion": {(10, 10): 0.0, (20, 10): -6.08, (5, 20): +5.17},
              "5 sesiones": {(10, 10): 0.0, (20, 10): -2.146, (5, 20): +1.517}}
# Sesgo por lado MEDIDO sobre ES real, 1 sesion (salida_linea_base.txt).
REAL_LADOS = {(10, 10): (+2.6, -2.6), (20, 10): (-4.7, -7.3), (5, 20): (+5.8, +4.6)}


def bloques(d, up, dn, n, L, rng, centrar=False):
    """Bootstrap por bloques moviles: se pegan bloques de L barras consecutivas."""
    if L <= 1:
        k = rng.integers(0, len(d), n)
        return d[k], up[k], dn[k]
    nb = int(np.ceil(n / L))
    ini = rng.integers(0, len(d) - L, nb)
    idx = (ini[:, None] + np.arange(L)[None, :])
    dd, uu, ll = d[idx], up[idx], dn[idx]
    if centrar:
        m = dd.mean(axis=1, keepdims=True)
        dd, uu, ll = dd - m, uu - m, ll - m
    return dd.ravel()[:n], uu.ravel()[:n], ll.ravel()[:n]


def medir(cl, hi, lo, con, T, S, horizonte, npaths=NPATHS):
    """Sesgo pooled y por lado, cada uno corregido por SU propia censura. Devuelve tambien
    gana(largo) y pierde(corto), que es lo que decide si el test de direccion es vacio."""
    asum = S / (S + T)
    asim = (T - S) / (T + S)
    g = res = viv = nn = 0
    lado_resid, lado_crudo, cnt = {}, {}, {}
    for lado in ("largo", "corto"):
        r = replica(cl, hi, lo, con, T, S, lado, horizonte, npaths=npaths)
        ri = r["gana"] + r["pierde"] + r["amb"]
        sr = r["vivo"] / r["n"] * 100
        crudo = (r["gana"] / ri - asum) * 100
        lado_crudo[lado] = crudo
        lado_resid[lado] = crudo - (-0.5 * asim * sr)
        cnt[lado] = r
        g += r["gana"]; res += ri; viv += r["vivo"]; nn += r["n"]
    p = g / res
    sin_res = viv / nn * 100
    sesgo = (p - asum) * 100
    return dict(sesgo=sesgo, resid=sesgo - (-0.5 * asim * sin_res), sin_res=sin_res,
                se_binom=np.sqrt(p * (1 - p) / res) * 100,
                largo=lado_resid["largo"], corto=lado_resid["corto"],
                largo_crudo=lado_crudo["largo"], corto_crudo=lado_crudo["corto"],
                gana_largo=cnt["largo"]["gana"], pierde_corto=cnt["corto"]["pierde"])


def main():
    print("=" * 100)
    print("BOOTSTRAP POR BLOQUES APAREADO EN LA TASA DE SIN-RESOLVER")
    print("NO GASTA CARTUCHO. K = 261. La caja sellada no se toca.")
    print("=" * 100)

    cl, hi, lo, con = cargar()
    n = len(cl)
    d, up, dn = tripletes(cl, hi, lo, con)
    mu = d.mean()
    dc, upc, dnc = d - mu, up - mu, dn - mu
    del cl, hi, lo, con
    con_s = np.zeros(n, dtype=np.int8)
    T0, S0 = BRACKET_CAL
    obj = REAL_SIN_RES["1 sesion"][BRACKET_CAL]

    # ------------------------------------------------------------------------------------
    print(f"\n{'=' * 100}")
    print(f"CALIBRACION DEL LARGO DE BLOQUE contra la tasa real de sin-resolver")
    print(f"   Objetivo: {T0}pt:{S0}pt a una sesion deja {obj:.1f}% sin resolver en ES real.")
    print(f"   La nula IID dejaba ~1,6%: por eso no eran comparables.")
    print("=" * 100)
    print(f"\n   {'L (barras)':>12}{'sin resolver':>15}{'dif vs real':>14}")
    mejor, mejor_err = None, np.inf
    for L in LS_CAL:
        rg = np.random.default_rng(SEMILLA + 31 * L)
        c2, h2, l2 = armar(*bloques(dc, upc, dnc, n, L, rg))
        r = medir(c2, h2, l2, con_s, T0, S0, SESION)
        e = abs(r["sin_res"] - obj)
        if e < mejor_err:
            mejor, mejor_err = L, e
        print(f"   {L:>12,}{r['sin_res']:>14.1f}%{r['sin_res']-obj:>+14.1f}")
        del c2, h2, l2
    LC = mejor
    print(f"\n   -> L* = {LC:,} barras ({LC/SESION:.2f} sesiones). Diferencia {mejor_err:.1f} pt.")

    # ------------------------------------------------------------------------------------
    modos = [("IID (L=1)", 1, False, False, K_GRANDE),
             (f"bloques L*={LC}", LC, False, False, K_GRANDE),
             ("CONTROL barajado", LC, True, False, K_CTRL),
             ("bloques centrados", LC, False, True, K_CENTRADO)]
    acum = {}
    binom = {}
    for nom, L, barajar, centrar, KK in modos:
        print(f"\n   corriendo modo '{nom}' con K = {KK} ...")
        base = (dc, upc, dnc)
        if barajar:
            rp = np.random.default_rng(SEMILLA + 99)
            k = rp.permutation(len(dc))
            base = (dc[k], upc[k], dnc[k])
        for kk in range(KK):
            rg = np.random.default_rng(SEMILLA + 7919 * kk + 13 * L)
            c2, h2, l2 = armar(*bloques(*base, n, L, rg, centrar=centrar))
            for hn, h in HORIZONTES:
                for T, S in BRACKETS:
                    r = medir(c2, h2, l2, con_s, T, S, h)
                    acum.setdefault((nom, hn, (T, S)), []).append(r)
                    binom[(hn, (T, S))] = r["se_binom"]
            del c2, h2, l2
        del base

    def col(nom, hn, b, campo):
        return np.array([r[campo] for r in acum[(nom, hn, b)]])

    # ------------------------------------------------------------------------------------
    print("\n" + "=" * 100)
    print("APAREO - la nula por bloques reproduce la tasa de sin-resolver del ES real?")
    print("=" * 100)
    for hn, _ in HORIZONTES:
        print(f"\n   horizonte {hn}")
        print(f"   {'bracket':>11}{'ES real':>10}{'IID':>10}{'bloques L*':>13}"
              f"{'centrados':>12}")
        for b in BRACKETS:
            print(f"   {f'{b[0]}pt:{b[1]}pt':>11}{REAL_SIN_RES[hn][b]:>9.1f}%"
                  f"{col('IID (L=1)', hn, b, 'sin_res').mean():>9.1f}%"
                  f"{col(f'bloques L*={LC}', hn, b, 'sin_res').mean():>12.1f}%"
                  f"{col('bloques centrados', hn, b, 'sin_res').mean():>11.1f}%")

    # ------------------------------------------------------------------------------------
    print("\n" + "=" * 100)
    print("CONTROL - bloques sobre datos BARAJADOS deben reproducir la nula IID")
    print("   QUE LO HARIA FALLAR: residuo distinto de cero ahi. Seria sesgo del metodo.")
    print("=" * 100)
    ok = True
    print(f"\n   {'bracket':>11}{'IID media':>12}{'IID desvio':>12}{'barajado':>11}"
          f"{'desvio':>9}{'dif':>8}{'en desvios':>12}{'veredicto':>11}")
    for b in BRACKETS:
        a = col("IID (L=1)", "5 sesiones", b, "resid")
        c = col("CONTROL barajado", "5 sesiones", b, "resid")
        se = np.sqrt(a.var(ddof=1) / len(a) + c.var(ddof=1) / len(c))
        z = (c.mean() - a.mean()) / se if se > 0 else 0.0
        bien = abs(z) <= 3.0
        ok &= bien
        print(f"   {f'{b[0]}pt:{b[1]}pt':>11}{a.mean():>+12.3f}{a.std(ddof=1):>12.3f}"
              f"{c.mean():>+11.3f}{c.std(ddof=1):>9.3f}{c.mean()-a.mean():>+8.3f}"
              f"{z:>+12.1f}{('OK' if bien else 'MAL'):>11}")
    print(f"\n   CONTROL {'PASADO' if ok else 'FALLADO'}")

    # ------------------------------------------------------------------------------------
    print("\n" + "=" * 100)
    print("LA PREGUNTA - el residuo real sobrevive a la nula APAREADA?")
    print("   Todo con el error de ENTRE SERIES, no con el binomial.")
    print("=" * 100)
    for hn, _ in HORIZONTES:
        print(f"\n   horizonte {hn}")
        print(f"   {'bracket':>11}{'REAL':>9}{'nula':>9}{'desvio':>9}{'binomial':>10}"
              f"{'subest':>8}{'en desvios':>12}{'min':>8}{'max':>8}{'adentro?':>10}")
        for b in BRACKETS:
            v = col(f"bloques L*={LC}", hn, b, "resid")
            asim = (b[0] - b[1]) / (b[0] + b[1])
            real = REAL_SESGO[hn][b] - (-0.5 * asim * REAL_SIN_RES[hn][b])
            sd = v.std(ddof=1)
            z = (real - v.mean()) / sd if sd > 0 else 0.0
            print(f"   {f'{b[0]}pt:{b[1]}pt':>11}{real:>+9.2f}{v.mean():>+9.2f}{sd:>9.3f}"
                  f"{binom[(hn, b)]:>10.3f}{sd/binom[(hn,b)]:>7.1f}x{z:>+12.1f}"
                  f"{v.min():>+8.2f}{v.max():>+8.2f}"
                  f"{('SI' if v.min() <= real <= v.max() else 'NO'):>10}")

    print(f"\n   Desvio del desvio: 1/raiz(2(K-1)) con K={K_GRANDE} -> "
          f"{1/np.sqrt(2*(K_GRANDE-1))*100:.1f}%  (con K=10 era 23,6%)")

    print("\n   Y con la tendencia local sacada (cada bloque centrado), K =", K_CENTRADO)
    print(f"   {'bracket':>11}{'nula':>9}{'desvio':>9}{'vs bloques':>12}")
    for b in BRACKETS:
        v = col("bloques centrados", "5 sesiones", b, "resid")
        w = col(f"bloques L*={LC}", "5 sesiones", b, "resid")
        print(f"   {f'{b[0]}pt:{b[1]}pt':>11}{v.mean():>+9.2f}{v.std(ddof=1):>9.3f}"
              f"{v.mean()-w.mean():>+12.2f}")

    # ------------------------------------------------------------------------------------
    print("\n" + "=" * 100)
    print("TEST DE DIRECCION - el residuo tiene el mismo signo comprando y vendiendo?")
    print("   mismo signo -> volatilidad o forma, sin direccion. Opuesto -> direccional.")
    print("=" * 100)
    print("\n   ANTI-IDENTIDAD: para T=S el largo y el corto usan los mismos dos niveles con")
    print("   las etiquetas al reves, asi que gana(largo) tiene que ser IGUAL a pierde(corto)")
    print("   y el test es VACIO. Para T!=S los niveles difieren y el test mide algo.")
    print(f"\n   {'bracket':>11}{'gana(largo)':>14}{'pierde(corto)':>15}{'iguales?':>11}"
          f"{'el test es':>14}")
    vacio = {}
    for b in BRACKETS:
        gl = col("IID (L=1)", "1 sesion", b, "gana_largo")[0]
        pc = col("IID (L=1)", "1 sesion", b, "pierde_corto")[0]
        vacio[b] = (gl == pc)
        print(f"   {f'{b[0]}pt:{b[1]}pt':>11}{gl:>14,}{pc:>15,}"
              f"{('SI' if gl == pc else 'no'):>11}"
              f"{('VACIO' if gl == pc else 'valido'):>14}")

    print(f"\n   Sobre ES real, 1 sesion, cada lado corregido por su propia censura:")
    print(f"   {'bracket':>11}{'largo':>9}{'corto':>9}{'signos':>11}"
          f"{'desvio nula largo':>20}{'lectura':>26}")
    for b in BRACKETS:
        asim = (b[0] - b[1]) / (b[0] + b[1])
        cens = -0.5 * asim * REAL_SIN_RES["1 sesion"][b]
        rl = REAL_LADOS[b][0] - cens
        rc = REAL_LADOS[b][1] - cens
        sdl = col(f"bloques L*={LC}", "1 sesion", b, "largo").std(ddof=1)
        mismo = (rl > 0) == (rc > 0)
        if vacio[b]:
            lect = "vacio por identidad"
        else:
            lect = "sin direccion" if mismo else "DIRECCIONAL"
        print(f"   {f'{b[0]}pt:{b[1]}pt':>11}{rl:>+9.2f}{rc:>+9.2f}"
              f"{('mismo' if mismo else 'opuesto'):>11}{sdl:>20.3f}{lect:>26}")
    return acum


if __name__ == "__main__":
    main()
