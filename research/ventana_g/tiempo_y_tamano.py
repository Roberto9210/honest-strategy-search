"""
C2 - LA EVALUACION TIENE LIMITE DE TIEMPO? Y ES ASIMETRICO ACHICAR EL CONTRATO?

NO GASTA CARTUCHO. K = 261. Flujo SINTETICO sin ventaja sobre ES 1-min 2016-2018. La caja sellada
no se toca.

LA PREGUNTA. El drawdown es barrera absorbente: tocarlo termina el intento. El objetivo, en cambio,
solo cuesta TIEMPO: no llegar hoy no mata. Si la evaluacion tiene limite de tiempo, achicar el
contrato cobra el objetivo -tardas mas y te quedas sin plazo-; si no lo tiene, no deberia cobrarlo.
Eso es lo que hay que verificar, porque hay una tercera cosa que cobra igual y no depende del plazo.

LA ARITMETICA DE FONDO, escrita antes de medir. Con N contratos: el P&L por sesion escala con N,
pero las barreras estan fijas en DOLARES ($2.000 de drawdown, $3.000 de objetivo). Entonces:
  - sesiones hasta resolver ~ 1/N^2  (la distancia en desvios por sesion crece como 1/N)
  - costo por sesion ~ N
  - costo TOTAL hasta recorrer la misma distancia en dolares ~ (1/N^2) * N = 1/N
Achicar el contrato MULTIPLICA el costo total de ejecucion aunque no haya limite de tiempo. Sin
costos, P(objetivo antes que drawdown) = dd/(dd+objetivo) = 0,40 y no depende de N: es el resultado
clasico de dos barreras. Con costos, N chico se come la diferencia.
LO HARIA FALLAR esta descripcion: que P(pasar) resulte plana en N -entonces el costo no manda- o que
suba al achicar -entonces la aritmetica esta al reves-.
"""

import os
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import juez as J  # noqa: E402
from vehiculo import matriz, simular  # noqa: E402

CELDA = dict(tipo="bracket", objetivo_pt=5, stop_pt=20)
PASO = 300
ANIOS = (2016, 2017, 2018)
TAMANOS = (1, 2, 3, 5, 7, 10, 14, 20, 30, 40)   # micro-equivalentes
SIN_LIM = "sin limite del producto (tope: el rango de datos)"
PLAZOS = ((SIN_LIM, 250), ("90 sesiones", 90), ("60 sesiones", 60), ("30 sesiones", 30))
SEMILLA = 20260905


def main():
    R = []
    A = R.append
    A("=" * 98)
    A("C2 - LIMITE DE TIEMPO DE LA EVALUACION, Y LA ASIMETRIA DE ACHICAR EL CONTRATO")
    A("NO GASTA CARTUCHO. K = 261. La caja sellada no se toca.")
    A("=" * 98)

    A("")
    A("-" * 98)
    A("   PARTE 1 - QUE DICEN LOS DATOS CRUDOS (datos_crudos.md, leidos 2026-09-03)")
    A("-" * 98)
    A("   APEX          'ONE-TIME FEE. NO REBILL. EVAL ACTIVE FOR 30 DAYS. WILL EXPIRE AFTER 30")
    A("                 DAYS. NO RESETS.'  -> LIMITE DURO Y EXPLICITO: 30 dias.")
    A("   TOPSTEP       Combine por suscripcion mensual ($49/mes en 50K). No expira, pero el tiempo")
    A("                 CUESTA: cada mes extra es otra cuota. Limite BLANDO, y es dinero.")
    A("   MYFUNDEDFUT.  'Charged once today. This plan does not renew and is not a subscription.'")
    A("                 Minimo 2 dias. No se leyo vencimiento.")
    A("   TRADEIFY      La ficha registra precio, objetivo, drawdown, reset, consistencia y")
    A("                 activacion. NO registra plazo de vencimiento ni dias minimos.")
    A("")
    A("   RESPUESTA HONESTA, con la convencion del propio documento ('lo que no aparece aca es NO")
    A("   SE DETERMINA'): para TRADEIFY el limite de tiempo NO ESTA DETERMINADO. No es lo mismo que")
    A("   'no tiene'. Lo que SI esta determinado es que es pago unico sin activacion y sin cuota")
    A("   mensual de la evaluacion, o sea que NO hay un reloj que cobre por mes como en Topstep.")
    A("   Para APEX el limite existe y son 30 dias, medido y citado.")
    A("   QUE LO CERRARIA: una lectura de los terminos de Tradeify buscando 'expire'/'time limit'.")
    A("   Mientras tanto se miden las DOS ramas, porque la decision cambia entre una y otra.")

    # ------------------------------------------------------------------ el flujo sin ventaja
    m = J.cargar_mercado()
    ses = np.flatnonzero(np.isin(m["anio_ses"], ANIOS))
    idx = np.concatenate([np.arange(int(m["ini"][k]), int(m["fin"][k]) - 1, PASO) for k in ses])
    rs = np.random.default_rng(SEMILLA)
    sgn = np.where(rs.random(len(idx)) < 0.5, 1.0, -1.0)
    ex = J.EXCESO_STOP[CELDA["stop_pt"]]
    pts, _ = J.resolver(m, idx, sgn, CELDA, ex)
    p = CELDA["stop_pt"] / (CELDA["stop_pt"] + CELDA["objetivo_pt"])
    sc = 1 - 2 * p
    o_cons = J.O_SOBREPASO * (1 + J.O_ERROR_REL) if sc > 0 else J.O_SOBREPASO * (1 - J.O_ERROR_REL)
    sesgo = o_cons * sc
    slip = m["slip_ses_pt"][m["ses_de"][idx]]
    ses_lo = int(m["ses_de"][idx.min()])
    n_ses = int(m["ses_de"][idx.max()]) - ses_lo + 1
    rep = dict(ses=m["ses_de"][idx] - ses_lo, pts=pts - sesgo - slip,
               ab=np.zeros(len(idx), int))
    M = matriz(rep, n_ses)
    s0 = np.arange(n_ses)
    C = J.CADENA
    op_ses = len(idx) / n_ses
    slip_med = float(slip.mean())              # medio-spread de entrada, en puntos, por micro

    A("")
    A("-" * 98)
    A(f"   PARTE 2 - MEDIDO. Flujo SIN ventaja: {len(idx):,} operaciones, {n_ses:,} sesiones,")
    A(f"   bracket 5pt:20pt, comision y deslizamiento cobrados. Cadena Tradeify Growth 50K:")
    A(f"   drawdown ${C['dd']:,.0f} EOD trailing, objetivo ${C['target']:,.0f}, cuota ${C['cuota']:.0f},")
    A(f"   pago esperado ${C['pago']:,.0f}. Un intento por cada sesion de arranque.")
    A("-" * 98)

    tabla = {}
    for etiq, plazo in PLAZOS:
        for N in TAMANOS:
            c_rt = J.COMISION["ES"] * (N // 10) + J.COMISION["MES"] * (N % 10)
            cap = np.minimum(n_ses - s0, plazo)
            res, used, _ = simular(M, s0, N, c_rt, C["dd"], C["target"], C["trail"],
                                   C["lock_off"], C["qual_days"], C["qual_amt"],
                                   plazo, C["max_fund"], cap=cap)
            tabla[(etiq, N)] = dict(
                p_obj=float(np.isin(res, (1, 2, 4)).mean()),
                p_pago=float((res == 2).mean()),
                p_dd=float((res == 0).mean()),
                p_tiempo=float((res == 3).mean()),
                e_ses=float(used.mean()),
                # costo de ejecucion pagado por intento: sesiones x operaciones por sesion x
                # (comision + medio-spread de entrada), todo al tamano N. Es la columna que muestra
                # el 1/N: N chico paga menos por operacion pero hace muchisimas mas.
                costo=float(used.mean() * op_ses * (c_rt + slip_med * 5.0 * N)),
                E=float((-C["cuota"] + (res == 2) * C["pago"]).mean()))

    for etiq, _plazo in PLAZOS:
        A("")
        A(f"   PLAZO DE LA EVALUACION: {etiq}")
        A(f"   {'N micros':>9}{'P(pasa eval)':>14}{'P(toca DD)':>12}{'P(se acaba)':>13}"
          f"{'E sesiones':>12}{'costo ejec.':>13}{'P(pago)':>10}")
        for N in TAMANOS:
            t = tabla[(etiq, N)]
            A(f"   {N:>9}{t['p_obj']:>14.3f}{t['p_dd']:>12.3f}{t['p_tiempo']:>13.3f}"
              f"{t['e_ses']:>12.1f}{t['costo']:>12,.0f}$"
              f"{t['p_pago']:>10.3f}")

    # ------------------------------------------------------------------ lectura
    sinlim = [tabla[(SIN_LIM, N)] for N in TAMANOS]
    lim30 = [tabla[("30 sesiones", N)] for N in TAMANOS]
    A("")
    A("=" * 98)
    A("   LA LECTURA")
    A("=" * 98)
    mejor = TAMANOS[int(np.argmax([t["p_obj"] for t in sinlim]))]
    A(f"   1) SI, ES ASIMETRICO, Y SE VE EN LA COLUMNA 'P(se acaba)'.")
    A(f"      AVISO SOBRE LA FILA 'sin limite': no es infinita. El intento no puede pasarse del")
    A(f"      rango de datos, asi que ahi 'se acaba' significa 'se acabaron las sesiones que")
    A(f"      tengo', no un plazo del producto. Por eso con {TAMANOS[0]} micro ya da "
      f"{sinlim[0]['p_tiempo']:.3f}: ese participante")
    A(f"      tarda {sinlim[0]['e_ses']:.0f} sesiones y muchos arranques no llegan al final de la serie.")
    A(f"      Con eso dicho, la comparacion es limpia porque el mismo tope corre en las cuatro filas:")
    A(f"      {TAMANOS[0]} micro pasa de {sinlim[0]['p_tiempo']:.3f} (tope del rango) a "
      f"{lim30[0]['p_tiempo']:.3f} con plazo de 30, y su P(toca DD)")
    A(f"      se derrumba de {sinlim[0]['p_dd']:.3f} a {lim30[0]['p_dd']:.3f}: el plazo lo mata ANTES de "
      f"que el drawdown lo alcance.")
    A(f"      {TAMANOS[-1]} micros no se entera: {sinlim[-1]['p_tiempo']:.3f} contra "
      f"{lim30[-1]['p_tiempo']:.3f}, porque resuelve en {sinlim[-1]['e_ses']:.1f} sesiones.")
    A(f"      El plazo SOLO castiga al chico. Confirmado: con limite, achicar cobra el objetivo.")
    A("")
    A(f"   2) PERO SIN LIMITE TAMPOCO ES GRATIS, Y ESTO NO ESTABA EN LA PREGUNTA.")
    A(f"      El intento pasa de {sinlim[-1]['e_ses']:.1f} sesiones con {TAMANOS[-1]} micros a "
      f"{sinlim[0]['e_ses']:.1f} con {TAMANOS[0]}: "
      f"{sinlim[0]['e_ses']/max(sinlim[-1]['e_ses'],1e-9):.0f}x mas largo.")
    A(f"      El costo de ejecucion pagado por intento va de ${sinlim[-1]['costo']:,.0f} a "
      f"${sinlim[0]['costo']:,.0f}: {'sube' if sinlim[0]['costo']>sinlim[-1]['costo'] else 'baja'}"
      f" {sinlim[0]['costo']/max(sinlim[-1]['costo'],1e-9):.1f}x.")
    A(f"      Es el 1/N anunciado: menos por operacion, muchisimas mas operaciones. 'Sin limite no")
    A(f"      te cobra el objetivo' es cierto para el PLAZO y falso para el BOLSILLO.")
    A("")
    A(f"   3) Y NO ES MONOTONO: el maximo esta en {mejor} micros "
      f"({max(t['p_obj'] for t in sinlim):.3f}), con {TAMANOS[0]} da "
      f"{sinlim[0]['p_obj']:.3f} y con {TAMANOS[-1]} da {sinlim[-1]['p_obj']:.3f}.")
    A(f"      Y el maximo NO esta en cualquier lado: esta en 10 y el segundo en 20. Es el ESCALON")
    A(f"      DE COMISION que la propia Tradeify publica -'if you're trading micro contracts in")
    A(f"      multiples of 10, you should trade the corresponding mini instead to save on fees'-:")
    A(f"      la ida y vuelta por micro-equivalente es $0,58 en multiplos de 10 y $1,82 fuera de")
    A(f"      ellos, 3,2x. El optimo cae donde se cruzan tres cosas: comision barata (multiplo de")
    A(f"      10), intento no tan largo que el costo lo desangre, y no tan grande que el drawdown")
    A(f"      TRAILING lo saque en {sinlim[-1]['e_ses']:.1f} sesiones. Sin costos y con piso FIJO la "
      f"teoria daria {C['dd']/(C['dd']+C['target']):.2f}")
    A(f"      para cualquier N; lo que rompe la invariancia son las dos cosas que el producto")
    A(f"      agrega: el costo por operacion y que el piso PERSIGUE al maximo.")
    A(f"      RESOLUCION DE ESTA COLUMNA: {n_ses:,} intentos, asi que {max(t['p_obj'] for t in sinlim):.3f} "
      f"son {int(round(max(t['p_obj'] for t in sinlim)*n_ses))} intentos. El")
    A(f"      escalon de 10 y 20 contra el resto es estructural; el orden fino entre 30 y 40 no.")
    A("")
    A(f"   4) EL SIGNO DE TODO, para que no se lea al reves. P(pago) es {sinlim[0]['p_pago']:.3f} en")
    A(f"      TODAS las filas y E $/intento es ${sinlim[0]['E']:+.0f} en todas: la cuota, y nada mas.")
    A(f"      Con cero ventaja NADIE cobra a ningun tamano, asi que 'el tamano optimo' es el que")
    A(f"      pierde mas despacio, no el que gana. Elegir tamano no es una palanca de esperanza:")
    A(f"      es elegir con que velocidad se pierde la cuota.")
    A("=" * 98)
    print("\n".join(R))
    return 0


if __name__ == "__main__":
    sys.exit(main())
