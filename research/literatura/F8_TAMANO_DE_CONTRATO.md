# F8 — EL EJE DE TAMAÑO DE CONTRATO

**VENTANA L. NO MEDIDO. No gasta cartucho, K sigue en 261.**

La Compuerta 1 concluyó, textual, que **"murió por tamaño, no por ventaja"**, y el filtro que salió de
ella no preguntaba por el tamaño. Este documento pone el eje que faltaba.

**Y arranca corrigiendo algo que afirmé en la entrega anterior**, porque el repo ya tenía medido que
mi afirmación era la mitad de la historia.

---

# 1. La corrección, primero

En la entrega anterior escribí que la palanca del MES hace que **"la exposición nocturna deje de ser
el problema"**, porque el drawdown pasa de 40 puntos a 400 y el peor movimiento nocturno medido fue de
118,75 puntos.

**Eso es cierto y es incompleto, y el censo de instrumentos ya lo había demostrado**
(`research/ventana_g/salida_censo.txt`):

> *"holgura = 2000/adv$ y esfuerzo = 3000/fav$: LAS DOS son 1/(tamaño del movimiento). Un instrumento
> que se mueve menos en dólares compra holgura y paga esfuerzo en la misma proporción."*

Y su conclusión: *"No hay un instrumento estructuralmente distinto: hay seis versiones del mismo
problema a distinta escala."*

**Achicar el contrato compra supervivencia y la paga en el objetivo de ganancia, uno a uno.** El
cociente holgura sobre esfuerzo **no cambia**. Ir de ES a MES es exactamente el mismo intercambio que
el censo ya midió entre instrumentos, aplicado al mismo instrumento a un décimo de escala.

## Pero el intercambio no es neutral, y ahí está lo que sí queda en pie

**Las dos barreras no son del mismo tipo.**

| | drawdown | objetivo de ganancia |
|---|---|---|
| qué pasa al tocarlo | **la cuenta muere. Es absorbente** | se tarda más |
| es reversible | **no** | sí |
| lo que cuesta | la cuenta y el progreso acumulado | tiempo |

**Achicar el tamaño cambia un riesgo absorbente por un costo de tiempo.** Eso es un buen negocio **si
el tiempo no está acotado**, y es un mal negocio si hay fecha límite.

**Y ahí está el número que decide y que no tengo: ¿la evaluación de Tradeify tiene límite de
tiempo?** La VENTANA G leyó el widget oficial el 2026-09-03 y tiene los datos crudos en
`datos_crudos.md`. **Es una consulta, no un estudio, y decide si el eje de tamaño es una palanca real
o sólo un cambio de unidades.**

**Sin ese dato, mi afirmación anterior queda como una cota optimista, exactamente igual que la fila
de entrada pasiva del piso.**

---

# 2. El censo, que ya está medido y no hay que reinventar

`salida_censo.txt`, drawdown $2.000, objetivo $3.000, **un** contrato micro, diarios 2016-2019. El
control reproduce las tres frecuencias de la Compuerta 1 al centésimo.

| instrumento | $/pt | mov. adverso típico | en dólares | **holgura** | **esfuerzo** | holgura/esfuerzo |
|---|---|---|---|---|---|---|
| E-Micro Gold | 10,00 | 2,80 pt | $28,00 | **71,4** | 107,1 | 0,667 |
| Micro E-Mini Dow | 0,50 | 77,00 pt | $38,50 | 51,9 | 62,8 | **0,827** |
| Micro E-Mini Russell | 5,00 | 8,10 pt | $40,50 | 49,4 | 65,9 | 0,749 |
| **Micro E-Mini S&P 500** | **5,00** | **8,75 pt** | **$43,75** | **45,7** | **58,5** | **0,781** |
| Micro E-Mini Nasdaq | 2,00 | 28,38 pt | $56,75 | 35,2 | 44,8 | 0,787 |
| Micro Crude Oil | 100,00 | 0,59 pt | $59,00 | 33,9 | 48,4 | 0,701 |

**HOLGURA** = cuántos movimientos adversos típicos entran en el drawdown.
**ESFUERZO** = cuántos movimientos favorables típicos hacen falta para el objetivo.

El rango de holgura sobre esfuerzo en los seis va de 0,667 a 0,827: **el mejor es 1,24 veces el peor,
y sólo 1,06 veces el del MES.** No hay dónde esconderse cambiando de instrumento.

---

# 3. El eje, aplicado a las once

La excursión de referencia depende de **cuánto dura la ventana**, no del instrumento. Los dos números
que hacen falta ya están medidos:

| ventana | excursión de referencia, en puntos de ES | fuente |
|---|---|---|
| 30 minutos | rango medio **3,75 pt** | `HECHOS_MEDIDOS_ES.md` §2, 44.831 barras |
| una sesión (390 min) | rango medio **13,34 pt** | ídem, 2.984 barras |
| cierre a cierre | mediana **8,75**, p90 **32,75**, p99 **71,81**, máximo **118,75** | Compuerta 1 (b), 955 noches |

Contra el drawdown, que en puntos es `$2.000 / valor del punto`:

| candidata | ventana | excursión de referencia | **caso extremo** | 1 ES = 40 pt | 1 MES = 400 pt |
|---|---|---|---|---|---|
| L01, L02, L04 | 30 min | 3,75 pt | **no publicado** | entra, holgura 10,7 | entra, holgura 107 |
| L03 | 30 min pre-dato | 3,75 pt o más | **no publicado** | entra | entra |
| L06 | 30 min, VX | — | — | **sin micro verificado** | **sin micro verificado** |
| L07 | 4 min, 6J | — | — | **sin micro verificado** | **sin micro verificado** |
| L08 | 1 h, 6E | — | — | E-Micro EUR/USD existe, **sin precio en el repo** | ídem |
| L09 | 30 min, CL | 0,59 pt diario | — | Micro Crude Oil, holgura 33,9 | ídem |
| **L10** | cierre a cierre | **8,75 pt** | **118,75 pt** | **NO entra el extremo**: 118,75 > 40 | **entra**: 118,75 < 400 |
| **L11** | una sesión / cierre a cierre | **8,75 pt** | **118,75 pt** | **NO entra el extremo** | **entra** |

## Descartes duros por tamaño: ninguno, y tres bloqueos

**Ninguna de las once se descarta por tamaño.** Pero tres quedan bloqueadas por una razón anterior:

- **L06 (VX) y L07 (6J): no hay micro verificado.** El censo lista E-Micro Silver, E-Micro AUD/USD y
  E-Micro EUR/USD como candidatos sin precio, y **no lista ningún micro de yen ni de VIX**. No los
  invento. **Hasta que alguien lea la especificación oficial y verifique el permiso de la firma, el
  eje de tamaño para estas dos no se puede evaluar**, y eso es una compuerta previa a cualquier
  medición.
- **L08 (6E): el micro existe en la lista pero sin precio en el repo.** El censo dice de dónde
  saldría: Databento GLBX o un proveedor de futuros de divisas.

Y el censo pone su propia advertencia sobre toda la tabla, que traslado entera: **"permiso de
Tradeify NO VERIFICADO (specs sí, del exchange)"**.

## Lo que sí cambia el eje de tamaño

**Para L10 y L11 el eje es decisivo y es la razón de que estén en el inventario.** Con **un ES**, el
peor movimiento nocturno medido es **casi tres veces el drawdown entero**, y la Compuerta 1 midió que
una noche sola se lo lleva el **8,38 %** de las veces por el lado largo. Con **un MES**, ese mismo
peor movimiento ocupa el **30 %** del drawdown.

**En ES son indefendibles. En MES son defendibles y cuestan diez veces más tiempo.**

---

# 4. La deuda que queda anotada, y es barata

**El máximo de la excursión adversa a 30 minutos no está publicado en el repo.** Está el rango
**medio** (3,75 pt) y está el máximo **nocturno** (118,75 pt), pero no el extremo de la ventana corta,
que es justo la que usan L01, L02, L03 y L04.

Sin ese número, la fila de 30 minutos de la tabla de arriba dice "entra" apoyada en un promedio, y
**un promedio no es lo que mata una cuenta**. La Compuerta 1 hizo exactamente esa distinción para las
noches y por eso publicó la mediana, el p90, el p99 y el máximo.

**Es una medición sobre datos que ya están en el repo, del mismo tipo que las que ya se hicieron, y
la propone esta ficha sin correrla porque no es territorio de esta ventana.**
