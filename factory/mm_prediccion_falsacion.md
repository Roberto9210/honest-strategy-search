# Predicciones firmadas — ronda de falsación (cuatro pruebas, K 258–261)

**Fecha:** 26 de agosto de 2026. **Commiteadas ANTES de correr cualquiera de las cuatro.** Cuarta
tanda de predicciones del método; las tres anteriores fallaron en algo y cada falla fue información.
Regla de conclusión declarada en spec §k: **"EL MECANISMO AGUANTA" ⟺ las cuatro pasan.** Una sola
falla ⇒ "EL MECANISMO NO ES LO QUE CREÍAMOS", nombrando cuál y qué significa.

Referencia fija para toda la ronda: **δ̂_TOM = 0,101767** (neto, `mm_prueba_resultado.json`);
en bruto por mercado: NQ 0,0991 · YM 0,1377 · NKD 0,0878 (el neto + f_i, con f_i = fricción/σ).

---

## PRUEBA 1 — Placebo de calendario

**Definición mecánica, fijada acá y no se ajusta:** entrada en la apertura de la **8.ª sesión** del
mes, salida en la apertura de la **14.ª sesión** del mismo mes (6 pasos apertura→apertura, la misma
longitud que F4). Meses con menos de 14 sesiones: no operan. Misma fricción por instrumento, misma
exclusión por banda de roll (la ventana que toque una banda se excluye y se cuenta — esto va a comerse
los meses trimestrales, igual que le pasa a NKD en la prueba principal; se reporta el conteo).
Distancia a la vuelta de mes: ≥ 4 sesiones de la salida previa (sesión 3) y ≥ 4 de la entrada
siguiente (~sesión 18).

**Predicción firmada:** δ̂_placebo (neto, agrupado, mismos tres mercados) en **[−0,02, +0,05]** —
compatible con deriva incondicional, que en 6 sesiones de un mes de ~21 es aproximadamente
(6/21) × deriva mensual, y la deriva mensual estandarizada por σ de 6 sesiones es chica.

**"Claramente menor", en números y antes de correr:** la prueba **PASA ⟺ δ̂_placebo < 0,0509**
(la mitad de δ̂_TOM). **FALLA ⟺ δ̂_placebo ≥ 0,0509.**

**Consecuencia declarada si falla:** F4 era deriva alcista disfrazada de calendario, y el documento lo
dice con esas palabras. En ese caso se agrega cuánto habría rendido estar comprado TODO el mes en vez
de un tercio.

## PRUEBA 2 — El contado como testigo

**Definición:** ^NDX, ^DJI, ^N225 (bajados hoy: 10.305 / 8.724 / 15.154 filas; N225 tiene 1 fila con
NaN en OHLC que se descarta mecánicamente y se reporta). La MISMA regla de ventana (entrada apertura
de la 4.ª sesión desde el final del mes M, salida apertura de la 3.ª de M+1), **sobre el calendario
propio de cada índice**, recortado al rango de fechas de su futuro (NQ 2000-09→, YM 2002-04→,
NKD 2004-02→). Sin fricción y sin exclusión de roll: el contado no tiene ni una ni otra.

**Las dos precisiones del encargo, declaradas:** (a) la comparación es **bruto contra bruto** — el
δ̂ bruto del futuro es el neto + f_i, y el contado, sin fricción ni roll, debería mostrar un efecto
igual o mayor; (b) ^N225 cotiza en fechas de Tokio y NKD en fechas de EE.UU. — por §h.1 los días de
NKD llevan calendario de EE.UU., así que **el par Nikkei NO es un par apareado por fechas**: la prueba
sobre ^N225 responde "¿el efecto existe en el índice de contado sobre su propio calendario?", que es
exactamente la pregunta del mecanismo, y así se interpreta.

**Predicción firmada:** los tres contados **positivos**, y cada δ̂ bruto de contado dentro de
**±0,05** del δ̂ bruto de su futuro.

**PASA ⟺ δ̂ bruto > 0 en los TRES contados. FALLA ⟺ alguno ≤ 0.**

**Consecuencia declarada si falla:** el efecto vive en los futuros y no en el índice ⇒ artefacto de
futuro (roll/base), no fenómeno de mercado ⇒ **F4 muere**.

## PRUEBA 3 — Concentración en la frontera

**Definición:** el retorno BRUTO de cada ventana (la fricción es una constante por operación y no
pertenece a ninguna sesión) se descompone en sus 6 pasos apertura→apertura:
`[−4→−3, −3→−2, −2→−1, −1→+1, +1→+2, +2→+3]`. Cada paso se estandariza por el σ del retorno
completo de su mercado, así los 6 pasos suman el δ̂ bruto del mercado. **FRONTERA** = los 3 pasos
centrales `{−2→−1, −1→+1, +1→+2}`. Participación = (suma agrupada de los pasos frontera) / (suma
de los 6).

**Predicción firmada:** la frontera carga **~65 %** del total (parejo sería 50 %).

**PASA ⟺ participación ≥ 0,60. FALLA ⟺ < 0,60** — y si queda cerca de 0,50, se escribe que el
efecto se parece a deriva y refuerza a la prueba 1.

## PRUEBA 4 — El signo del rebalanceo (de Roberto)

**Definición mecánica del corte, un solo corte, jamás un umbral:** para la vuelta de mes del mes M, el
condicionante es el **SIGNO del retorno del mes que está terminando**, conocido a la entrada:
`r_cond = close(sesión −5 de M) / close(última sesión de M−1) − 1`. La sesión −5 es la anterior a la
entrada (−4), así que r_cond está íntegramente en el pasado del primer fill. *(Lectura declarada del
encargo: "el mes anterior" es el mes cuyo fin la operación cabalga — el rebalanceo de fin de M
responde al movimiento de M. Se mide hasta la sesión −5 para no usar ni un precio futuro.)* Meses sin
sesión −5 o sin cierre previo: fuera, contados.

**Predicción firmada, con signo:** δ̂(tras mes en baja) > δ̂(tras mes en alza), con brecha
estandarizada **≥ 0,05**. El fondo balanceado COMPRA acciones después de que caen.

**PASA ⟺ brecha = δ̂_baja − δ̂_alza ≥ 0,02. FALLA ⟺ brecha < 0,02** (invertido o plano) — y en ese
caso la explicación de flujo de rebalanceo NO se sostiene aunque el efecto exista, y el documento lo
dice. Un efecto sin mecanismo entendido es más frágil, no menos.

**Prohibición pre-escrita:** un resultado a favor NO autoriza operar "sólo después de meses en baja".
Estrategia nueva ⇒ K propia y pre-registro propio. La prueba 4 explica, no habilita.

---

## Mi expectativa global, para poder fallar entera

Espero **3 de 4 PASA** con la duda puesta en la **prueba 3** (la concentración puede salir en 0,50-0,60
si parte del efecto es pre-fin-de-mes difuso). Probabilidades subjetivas: las cuatro pasan (**"EL
MECANISMO AGUANTA"**): **45 %**; falla exactamente una: 40 % (de eso, la 3 es la más probable); fallan
dos o más: 15 %. Si falla la 1 o la 2, F4 no es lo que creíamos en el sentido fuerte (deriva o
artefacto); si falla sólo la 4, el efecto existe pero el relato de rebalanceo era un cuento.
