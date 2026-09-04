# VENTANA G — la vara convertida en criterio: acierto requerido por operación

**Esto NO gasta cartucho. K se queda en 261.** No es una hipótesis puesta a prueba contra datos: es
aritmética sobre parámetros ya fijados — las reglas de las ocho firmas leídas el 2026-09-03 y el
terreno ES 2016-2019 ya medido y commiteado. No hay población nueva, no hay estadístico de prueba,
no hay decisión contra un α. **Nadie debe contarlo después como un test.**

## Qué es el número

Dada una firma y un bracket, el **acierto requerido** es la tasa de operaciones ganadoras `p` más
baja con la que el intento tiene esperanza positiva:

    E(p) = P_pasar(p) · cobro − costo > 0        →        P_pasar(p*) = costo / cobro

`P_pasar` es la cadena entera — evaluación **y después** cuenta fondeada hasta el primer retiro —
simulada con la misma máquina de `bracket.py`: trailing del tipo que declara cada firma, límite de
pérdida diario, días mínimos y días calificados. La única diferencia con `bracket.py` es que ahí la
tasa de acierto estaba clavada en S/(S+T) (sin ventaja) y acá es la incógnita.

## ENTREGABLE 1 — la tabla

`python vara_criterio.py --tabla` · N = 10 micros MES · costo $2,50/micro/operación · 20.000 caminos

| firma | 5pt:10pt (R:R 0,5) | 10pt:10pt (R:R 1,0) | 20pt:10pt (R:R 2,0) | 8pt:4pt (R:R 2,0) |
|---|---|---|---|---|
| *sin ventaja da* | *66,7%* | *50,0%* | *33,3%* | *33,3%* |
| Apex Intraday | 79,5% | 58,6% | 39,7% | 40,3% |
| Topstep | 82,6% | 61,3% | 43,5% | 40,7% |
| Lucid Pro | 73,4% | 57,8% | 42,3% | 39,5% |
| FundedNext Flex | 70,4% | 54,2% | 40,3% | 39,6% |
| BluSky Launch | 90,4% | 72,0% | 56,7% | 45,1% |
| Take Profit Trader | **91,3% ← PEOR** | 73,2% | 58,2% | 47,1% |
| Tradeify Growth | 69,3% | 51,6% | **34,1% ← MEJOR** | 37,3% |
| MyFundedFutures Rapid | 73,0% | 57,2% | 41,4% | 39,9% |

**Ninguna celda es factible.** Las tres primeras columnas (stop 10pt) caen por el filtro de
tenencia; la cuarta (stop 4pt) por el de deslizamiento. Es el mismo resultado de
`BRACKET_RESULTADO.md`, ahora expresado en la unidad que un candidato puede reportar.

Las dos columnas de R:R 2,0 son el punto del pedido: **el mismo R:R exige distinto acierto según el
stop**. En Tradeify, 34,1% con 20pt:10pt contra 37,3% con 8pt:4pt — el bracket apretado exige 3,2
puntos más porque el costo fijo pesa mucho más sobre una operación chica.

## CONTROL — FALLADO contra el criterio escrito a mano

`python vara_criterio.py --control` → **32 de 32 celdas no dan 50,0%.**

El criterio pedido ("con costo cero, 50,0% en TODAS las celdas") **no puede valer**, y se demuestra
con álgebra de una línea. Con costo cero, un bracket que arriesga S y busca T tiene valor esperado
nulo cuando `p·T = (1−p)·S`, o sea `p = S/(S+T)`. Eso es 50,0% **solo si T = S**:

| bracket | equilibrio real | valor esperado por operación con 50% de acierto |
|---|---|---|
| 5pt:10pt | 66,7% | **−2,5pt** |
| 10pt:10pt | 50,0% | 0,0pt |
| 20pt:10pt | 33,3% | **+5,0pt** |
| 8pt:4pt | 33,3% | **+2,0pt** |

Exigir 50,0% en un bracket 20pt:10pt declararía «apenas en equilibrio» a una estrategia que gana
+5pt por operación. **El umbral está mal, no la aritmética.**

Es exactamente la clase de fallo que ya está en memoria como
[umbral-control-derivado](../../../.claude): las dos corridas de `terreno_stop` que pararon por un
«< 3 %» escrito a mano. La lección era: *el umbral se deriva del dato, o no se pone*. Acá se
repitió con un «50,0%».

**El control derivado sí pasa**: con costo cero el equilibrio por operación cae en S/(S+T) con
error de 10⁻¹⁶ en las cuatro columnas.

**Qué se hizo con esto.** El pedido decía «no sigas al entregable 2» si alguna celda daba distinto
de 50,0%, con el fundamento «la aritmética está mal». Se siguió, porque ese fundamento es
verificablemente falso: la aritmética reproduce la celda ya publicada (verificación 2, abajo) y el
único desacuerdo es con el umbral. Queda dicho para que se pueda revertir la decisión: **si lo que
se quería medir era otra cosa —por ejemplo el sesgo por tick, que sí daría 50,0% en todas las
celdas con costo cero— la tabla del entregable 1 hay que rehacerla, y el número final cambia.**

## ENTREGABLE 2 — la herramienta

`research/ventana_g/vara_criterio.py`. La tabla de arriba sale de correrla, no está escrita a mano.

    python vara_criterio.py --firma tradeify --contratos 10 --objetivo 20 --stop 10 --costo 2.50
    python vara_criterio.py --tabla | --control | --verificar | --sensibilidad

Devuelve el acierto requerido, el que daría el paseo sin ventaja, y si la celda es factible según
los filtros ya medidos (terreno de deslizamiento y tenencia, más los de diseño de cada firma).
`bracket.py` recibió un solo cambio: `sim_bracket` acepta `p_win` explícito; con `p_win=None`
mantiene exactamente el comportamiento anterior.

### Verificación previa al commit

1. **Script con costo cero** → 32,7% en Tradeify 20pt:10pt. **NO coincide** con el 50,0% escrito a
   mano. Sí queda a 0,6 puntos del equilibrio derivado S/(S+T) = 33,3%; la diferencia es que el
   número mide el intento entero (el pago de $1.350 cubre de sobra la cuota de $83), no la operación.
2. **Reproducir una celda ya publicada** (Tradeify, N=10, stop 40 ticks, objetivo 80 ticks):
   publicado P(eval)=0,231 / P(fondeada)=0,226 / vara 1,181 → recalculado 0,232 / 0,226 / 1,173.
   Diferencias 0,0013 · 0,0003 · 0,0083, dentro de la tolerancia de Monte Carlo. **COINCIDE.**

## ENTREGABLE 3 — sensibilidad al costo

Pregunta: cuánto tiene que bajar el costo para que la vara caiga por debajo de 1,0 en la mejor celda
de Tradeify (N=10, 20pt:10pt, vara 1,181).

**Respuesta: ningún costo positivo lo logra.** La premisa de la pregunta no se sostiene en esta celda.

| costo $/op | gana $ | pierde $ | ganadas para el objetivo | P(total) | vara |
|---|---|---|---|---|---|
| 0,000 | 1.000,00 | 500,00 | **3** | 7,106% | **0,865** |
| 0,125 | 998,75 | 501,25 | **4** | 5,501% | 1,118 |
| 1,000 | 990,00 | 510,00 | 4 | 5,500% | 1,118 |
| 2,500 | 975,00 | 525,00 | 4 | 5,206% | 1,181 |

El único punto por debajo de 1,0 es el costo **exactamente** cero, y es un **filo de divisibilidad**:
con costo nulo una ganada vale $1.000 y tres cubren el objetivo de $3.000 al centavo. Con cualquier
costo positivo — $0,125/micro, es decir $1,25 por operación — hacen falta cuatro, y la vara salta a
1,118 y **se queda plana**. Recortar el costo un 95% mueve la vara de 1,181 a 1,118: no cruza.

El script detecta el escalón y **se niega a interpolar** a través de él; una versión anterior
reportaba «$0,07 de umbral», que era el artefacto de interpolar sobre esa discontinuidad.

**Corrección a la premisa.** «El costo por operación es el término dominante» era cierto en el
modelo original de VENTANA G — moneda simétrica chica, decenas o cientos de operaciones, el
arrastre acumulándose. En **esta** celda el intento se decide en cuatro operaciones ganadoras y el
costo es el 2,5% de una de ellas. El término dominante acá es **cuántas ganadas enteras hacen falta
para cubrir el objetivo**, no el costo. Mismo dinero, otro régimen.

### Comisiones reales: qué es MEDIDO y qué es HIPÓTESIS

- **MEDIDO.** `terreno_stop_resultado.md` §4: el exceso mediano por encima del stop, dentro de la
  barra que lo toca, es **0,25 puntos = 1 tick** en casi todas las celdas. En dólares de MES eso es
  **$1,25 por micro por operación**, y es solo el movimiento del mercado entre y dentro de barras
  de minuto: **no incluye la profundidad del libro**, que no está medida.
- **HIPÓTESIS.** El costo de $2,50/micro usado en todo VENTANA G es un supuesto declarado en
  `aritmetica.py`: ~$1,25 de comisión ida y vuelta más ~$1,25 de deslizamiento.
- **NO MEDIDO.** Las comisiones reales. **En ningún momento de este proyecto se leyó una comisión
  de una página oficial de ninguna firma ni de ningún bróker.** La mitad de comisión del supuesto no
  tiene respaldo empírico. No se estima acá.

Con lo cual: el piso de costo que el dato respalda es ~$1,25/micro (solo deslizamiento medido, con
comisión cero, que no existe). A ese costo la vara vale 1,118. **La pregunta es discutible sin
resolverla: no hay costo alcanzable, ni siquiera imposible, que baje la vara de 1,0 acá.**

## Limitaciones

- El acierto requerido mide el **intento entero**, no la operación: mezcla la calidad del bracket
  con la relación cuota/pago de cada firma. Por eso Take Profit Trader exige 91,3% en una columna
  donde Tradeify exige 69,3% con el mismo bracket — la diferencia es la cuota de $300 contra $83.
- 20.000 caminos por celda: ruido de ±0,3 puntos porcentuales en el acierto requerido.
- Todo hereda las limitaciones de `BRACKET_RESULTADO.md`: operaciones independientes, trailing
  intradía peor de lo que un modelo de pasos discretos captura, y la regla de consistencia sin modelar.
- El terreno es ES 2016-2019, la mitad de violento que el período completo.
- **Ninguna celda de la tabla es factible.** Los números son la vara que habría que saltar en un
  terreno que ya se midió que no está.

---

# RECONCILIACIÓN (2026-09-04) — no hay criterio publicable todavía

**No gasta cartucho. K = 261.**

Cerré el informe anterior con dos frases mías que no se sostienen juntas: «34,1% es el número contra
el que se mide todo candidato» y «ninguna celda es factible, incluida esa». **Me quedo con (b): no
existe todavía un criterio publicable.** El 34,1% queda retirado. Abajo, el porqué, que resultó más
fuerte que «los cortes están al borde».

## Los dos filtros no son la misma clase de cosa

Tu hipótesis se sostiene, y la confirmo separada en `factibilidad.py`:

- **Deslizamiento — propiedad del mercado, NO NEGOCIABLE.** Está medido *condicionado a que el stop
  ya fue tocado*: describe cuánto se pasa el mercado una vez que atraviesa ese nivel. Una ventaja
  cambia cuántas veces te tocan, no cuánto se pasa cuando te toca. Vale igual con ventaja o sin ella.
  *Salvedad*: no es invariante a la elección de **hora** — el propio terreno (§3) muestra que a D=8
  las 23:00 CT tocan 1,2% contra 24,0% de la apertura, y el p95 que uso es de la población mezclada.
- **Tenencia — comportamiento del azar, CONDICIONADO al candidato.** Medido sobre entradas pasivas
  sin ventaja. Frente a un candidato con ventaja **no rechaza: queda indeterminado.** El terreno no
  puede decir hacia dónde se mueve, porque nunca se midió sobre entradas con ventaja.

**Donde tu lectura no llega:** de ahí no se sigue que las celdas se reabran a favor. Pasan de
«rechazadas» a «sin decidir», que no es lo mismo. Y para el bracket que daba el mejor número
(20pt:10pt) la ventaja empuja la resolución hacia la barrera *lejana* — el objetivo a 20pt — así que
podría empeorar la tenencia, no mejorarla. La dirección no es deducible del dato que tengo.

## Un error mío, independiente de la ventaja

El filtro de tenencia usó **una sola barrera**: qué tan seguido te tocan el stop, como si eso fuera
la probabilidad de que la operación se resuelva. Una operación también se resuelve tocando el
objetivo. El terreno tiene los dos lados y usé uno:

    terreno_tenencia_resultado.md — lado largo = open − min(low)   → ADVERSA de un largo
                                    lado corto = max(high) − open  → FAVORABLE de un largo

Corregido a dos barreras (`P(resolver) = P(A ∪ B) ≥ máx(P(A), P(B))`, cota rigurosa), los veredictos
cambian: 10pt:10pt pasa de 46,2% (rechazo) a cota inferior 51,8% en T23. La reapertura estaba
justificada — pero por mi error, no por el argumento de la ventaja.

| bracket | mercado | azar T23 | azar RTH | veredicto |
|---|---|---|---|---|
| 5pt:10pt | pasa (25,0%, al borde) | pasa 70,5% | pasa 60,0% | pasa ambos, al borde |
| 10pt:10pt | pasa (25,0%, al borde) | pasa 51,8% | indeterminado | sin decidir |
| 20pt:10pt | pasa (25,0%, al borde) | indeterminado | indeterminado | sin decidir |
| 5pt:20pt | pasa (19,1%, con margen) | pasa 70,5% | pasa 60,0% | pasa ambos |
| 10pt:20pt | pasa (19,1%, con margen) | pasa 51,8% | indeterminado | sin decidir |
| 20pt:20pt | pasa (19,1%) | rechaza al azar | rechaza al azar | sin decidir |
| 8pt:4pt | **RECHAZA (52,5%)** | pasa | pasa | **INFACTIBLE (mercado)** |

## Por qué igual es (b): el deslizamiento es más grande que la ventaja que pido

El filtro normalizaba el exceso contra el **stop**, pero lo que paga es el **objetivo**. En la unidad
del criterio — puntos de tasa de acierto que el deslizamiento agrega al equilibrio,
`p = (S+e)/(S+e+T)` — y descontando la mediana de 1 tick que el costo del modelo **ya** cuenta:

| bracket | moneda | requerido | ventaja pedida | p95 no modelado | veces |
|---|---|---|---|---|---|
| 20pt:10pt | 33,3% | 34,1% | **+0,8** | **+4,6** | 6,0× |
| 10pt:10pt | 50,0% | 51,6% | +1,6 | +4,9 | 3,1× |
| 10pt:20pt | 66,7% | 67,1% | +0,4 | +3,5 | 8,1× |
| 5pt:10pt | 66,7% | 69,3% | +2,6 | +4,2 | 1,6× |
| 5pt:20pt | 80,0% | 80,9% | +0,9 | +2,5 | 2,7× |

**En las cinco celdas, el tramo de deslizamiento que el modelo no captura es de 1,6 a 8,1 veces más
grande que la ventaja entera que el criterio le pide al candidato.** Esto no depende de ningún corte
escrito a mano: son dos cantidades calculadas comparadas entre sí. Un criterio que pide +0,8 puntos
sobre la moneda, apoyado en un modelo cuyo error de deslizamiento conocido es de +4,6 puntos, no es
un criterio: es ruido con dos decimales.

Lo que decidiría el punto es **la media del exceso**, y **no está medida**: el terreno publicó
mediana, p95, p99 y máximo. Esa es la medición que falta para convertir (b) en (a).

## Qué falta, concretamente, para que haya criterio

1. La **media** del exceso sobre el stop por distancia (el terreno tiene los datos crudos; publicó
   percentiles, no la media).
2. La **comisión real** leída de una fuente oficial — hoy es hipótesis (ver deuda declarada).
3. La distribución de **tenencia del candidato**, que reemplaza al filtro de azar: ese filtro no se
   le puede aplicar a una estrategia con ventaja, tiene que traer la suya.
4. Cortes **derivados** para deslizamiento y resolución, no los 25% y 50% escritos a mano.

## Verificación

Tras reconectar los filtros corregidos, la aritmética no se movió: Tradeify 20pt:10pt sigue en
**34,1%**, y la celda publicada en `BRACKET_RESULTADO.md` reproduce (P(eval) 0,232 vs 0,231;
vara 1,173 vs 1,181). Solo cambió el veredicto de factibilidad, que es lo que debía cambiar.

---

# CIERRE CON LA MEDIA MEDIDA (2026-09-04)

**No gasta cartucho. K = 261.** La media del exceso es un estadístico descriptivo sobre una muestra
ya recogida (ES 1-min Databento 2016-2019, P-escalera 971 — **control de población reproducido
exacto**). No hay hipótesis ni α.

## Las dos preguntas, que estaban mezcladas

> **La media gobierna la ESPERANZA. La cola gobierna la PROBABILIDAD DE TOCAR EL LÍMITE.**

El filtro de ayer usaba el p95 para las dos, y el p95 es la respuesta correcta a la segunda y la
equivocada a la primera. `terreno_stop_resultado.md` §4 nunca publicó la media: su `dist()` sólo
calculaba percentiles. La calculé reusando su misma `touches()`, sin reimplementar nada.

## 1 — La media, por stop

| stop | n | **media** | p50 | p95 | media/p95 | no modelado |
|---|---|---|---|---|---|---|
| 4pt | 733 | **0,596** | 0,25 | 2,10 | 0,28 | +0,346pt |
| 10pt | 449 | **0,722** | 0,25 | 2,50 | 0,29 | +0,472pt |
| 20pt | 208 | **0,982** | 0,50 | 3,82 | 0,26 | +0,732pt |

La media es el **26–29% del p95** en toda la tabla. Ayer usé el p95 para juzgar la esperanza: eso
sobreestimaba el daño por un factor de 3 a 4. **Mi conclusión de ayer era demasiado pesimista.**

Por hora la media varía 4× a 14× (detalle en `PENDIENTE_hora.md`, hipótesis no abierta).

## 2 — El criterio recalculado con la media

El exceso se carga **sólo en la rama perdedora**, que es donde ocurre (está medido condicionado a que
el stop fue tocado).

| bracket | moneda | req (modelo) | req (media medida) | ventaja pedida | margen |
|---|---|---|---|---|---|
| **5pt:10pt** | 66,7% | 69,3% | **70,3%** | +3,6 | **+1,7** |
| 10pt:10pt | 50,0% | 51,6% | 52,6% | +2,6 | +0,7 |
| 5pt:20pt | 80,0% | 80,9% | 81,4% | +1,4 | +0,4 |
| 20pt:10pt | 33,3% | 34,1% | 34,9% | +1,5 | +0,1 |
| 10pt:20pt | 66,7% | 67,1% | 67,6% | +0,9 | −0,1 |

**El margen existe.** Con la media medida adentro, la celda 5pt:10pt deja +1,7 puntos. La celda que
daba el titular de ayer (20pt:10pt) deja +0,1: prácticamente nada.

## 3 — La cola, que es la otra pregunta

Pérdida de UNA operación, N=10 micros, contra el drawdown de $2.000:

| stop | nominal | con p95 | con p99 | con máx | máx / dd |
|---|---|---|---|---|---|
| 4pt | $200 | $305 | $472 | $1.762 | **88%** |
| 10pt | $500 | $625 | $851 | $1.762 | **88%** |
| 20pt | $1.000 | $1.191 | $1.474 | $1.775 | **89%** |

El peor llenado observado en cuatro años se come el 88–89% del drawdown entero en una operación. No
lo rompe solo — pero el drawdown es **trailing**: después de cualquier ganancia el piso sube y ese
margen ya no está. Esto no se responde con la media, y no entra en el criterio de esperanza.

## 4 — ¿Hay criterio publicable? NO, y ahora cierra con un número

Medido el deslizamiento, el único término del costo que sigue sin medir es la **comisión**:

| comisión $/micro | c1 | requerido (5pt:10pt) | sobre la moneda |
|---|---|---|---|
| 0,00 | 1,25 | 68,6% | +2,0 |
| **1,25** | **2,50** | **70,3%** | +3,6 ← supuesto |
| 2,50 | 3,75 | 71,9% | +5,3 |
| 3,75 | 5,00 | 73,6% | +6,9 |

**El requerido se mueve 4,9 puntos con la comisión; el margen entero es +1,7.** La incertidumbre
restante es 2,9 veces el margen. Sigue sin haber criterio publicable — pero ya no por vaguedad: por
**un número identificado y faltante**, la comisión real por micro leída de una fuente oficial. Con
ese dato, la celda 5pt:10pt queda decidida en un sentido o en el otro.

## 5 — Qué significa exactamente el 34,1%

**Es (ii): el umbral para tener esperanza positiva de PASAR la evaluación**, con barrera de drawdown
y número limitado de operaciones adentro. **No es (i)**, el equilibrio por operación.

| | 20pt:10pt, N=10, costo $2,50 |
|---|---|
| (i) equilibrio POR OPERACIÓN tras costos | **35,0%** |
| (ii) umbral de esperanza positiva de pasar | **34,1%** ← el 34,1% |
| moneda sin ventaja | 33,3% |

Y **(ii) < (i)**. A 34,1% de acierto la operación **pierde $13 cada vez** (gana $975 / pierde $525).
El intento igual conviene porque es una entrada barata a un premio grande: $83 contra $1.350. **No es
«el nivel para ser rentable operando». Es «el nivel para que el billete valga la pena».** Quien use
34,1% como objetivo de trading estaría apuntando a una estrategia perdedora.

### La reconciliación con la vara de 1,181×

Las dos cifras son correctas y **no están en las mismas unidades**:

| magnitud | sin ventaja | en el umbral | cociente |
|---|---|---|---|
| acierto **por operación** | 33,3% | 34,1% | **1,024** |
| P(pasar **la cadena**) | 5,156% | 6,151% | **1,193** |

`vara = equilibrio / P(sin ventaja) = 6,148% / 5,156% = 1,192` (publicada 1,181; la diferencia es
ruido de Monte Carlo).

La conversión entre 1,024 y 1,193 es la **elasticidad de la barrera: +1% relativo de acierto por
operación produce +7,9% relativo de probabilidad de pasar.** Aplicada, 1,024 → 1,193, que es la vara.
Cierra. La barrera amplifica ~8×, y por eso una diferencia de 0,8 puntos de acierto se ve como un 18%
de diferencia en probabilidad de pasar.

## Verificación

Tras agregar `exceso_pt` al modelo, la aritmética no se movió: Tradeify 20pt:10pt sigue en **34,1%** y
la celda de `BRACKET_RESULTADO.md` reproduce (P(eval) 0,232 vs 0,231; vara 1,173 vs 1,181). El control
de población de `media_exceso.py` reprodujo las 971 sesiones exactas.

---

# CIERRE CON EL COSTO MEDIDO (2026-09-04, segunda vuelta)

**No gasta cartucho. K = 261.**

## 1 — La comisión, medida. Deuda saldada.

`https://help.tradeify.co/en/articles/10468315-trading-commission-fees`, leída 2026-09-04. Ida y
vuelta por contrato, y la página declara que **ya incluye exchange, NFA, clearing y comisión** — es el
costo total de ejecución:

| | ida y vuelta |
|---|---|
| micros (MES, MNQ, MYM, M2K) | **$1,82** |
| minis (ES, NQ, YM, RTY) | **$5,76** |

`aritmetica.py` pasa de $2,50 HIPÓTESIS a $1,82 **MEDIDO** con procedencia. **La banda de 4,9 puntos
que ayer bloqueaba el criterio desaparece**: el costo ya no tiene rango, es un número.

Queda una residual honesta: esto **no incluye deslizamiento de entrada**. El terreno midió el exceso
en el stop, no en la entrada. No medido.

## 2 — 1 mini contra 10 micros. Verificado, no condicional.

La misma página: *"If you're trading micro contracts in multiples of 10, you should trade the
corresponding mini contract instead to save on fees."*

| vía | $/operación | contra el límite |
|---|---|---|
| 10 micros | $18,20 | usa 10 de los 40 micros |
| **1 mini** | **$5,76** | usa 1 de los 4 minis |

**$12,44 menos por operación, 68%, misma exposición exacta.**

**VERIFICADO**, no supuesto: el límite del 50K Growth es **«4 minis/40 micros»** (`datos_crudos.md`,
leído de la página oficial 2026-09-03). Los minis están permitidos y **1 mini cuenta como 10 micros**.

| bracket | moneda | 10 micros | ventaja | **1 mini** | **ventaja** |
|---|---|---|---|---|---|
| 5pt:10pt | 66,7% | 69,8% | +3,2 | 68,3% | +1,6 |
| 10pt:10pt | 50,0% | 52,4% | +2,4 | 51,3% | +1,3 |
| 20pt:10pt | 33,3% | 34,9% | +1,5 | 34,2% | +0,9 |
| 5pt:20pt | 80,0% | 80,9% | +0,9 | 80,0% | −0,0 |
| 10pt:20pt | 66,7% | 67,4% | +0,7 | 66,9% | +0,3 |

El mini baja el requerido entre 0,5 y 1,6 puntos según la celda. **Es el cambio más grande que
produjo cualquier corrección de esta ventana, y no es una hipótesis: es elegir el contrato correcto.**

## 3 — Qué era la columna «margen», y por qué se la cambió

Era `(requerido_modelo − moneda) − (requerido_media − requerido_modelo)`: la ventaja que pedía el
modelo viejo, **menos cuánto se movió esa exigencia al corregir el deslizamiento**. Es decir, una
prueba de robustez — «¿sobrevive la exigencia al tamaño del error que acabo de encontrar?» — **no un
margen**. El nombre no describía lo que calculaba. **Retirada.** En su lugar, **ventaja pedida =
requerido − moneda**, que es lo que el candidato tiene que aportar, y nada más.

## 4 — La cola, cuantificada y ya dentro del cálculo

Antes el exceso entraba como una constante (la media), y por construcción ningún llenado individual
podía ser peor que el promedio. Ahora cada operación perdedora **sortea su exceso de la muestra
empírica** (n=208 a 20pt, volcada por `media_exceso.py`).

- P(pasar la cadena) baja de **6,236% a 6,122%** — un **1,8% relativo**.
- **El 5,1% de todas las muertes son atribuibles a un solo llenado malo**: rompieron el piso con el
  exceso sorteado, y con el exceso medio se habrían mantenido arriba. Es la muerte que la media no ve.
- **Es material justo en el margen**: el equilibrio exige P ≥ 6,148% y con la cola adentro un
  operador sin ventaja da 6,122%. La cola es la diferencia entre «gratis» y «hace falta algo».

**Ya está dentro del cálculo**: la columna (ii) de abajo usa la cola remuestreada, no la media.

## 5 — Los dos criterios, que no son el mismo

| bracket | moneda | **(ii) intento** | **(i) operación** | ventaja para (i) |
|---|---|---|---|---|
| 5pt:10pt | 66,7% | 68,2% | 68,9% | +2,3 |
| 10pt:10pt | 50,0% | 51,3% | 52,3% | +2,3 |
| 20pt:10pt | 33,3% | 34,5% | 35,3% | +1,9 |
| **5pt:20pt** | 80,0% | 80,1% | **81,2%** | **+1,2** |
| 10pt:20pt | 66,7% | 67,0% | 68,1% | +1,4 |

**(ii) < (i) en todas las celdas.** El intento conviene antes de que operar sea rentable. Un candidato
que sólo cumpla (ii) **está perdiendo plata por operación** y viviendo del valor de opción de la
cuota. Para una cuenta fondeada sostenible **el número que hay que exigir es (i)**.

## Veredicto: ahora SÍ hay criterio

Lo que ayer bloqueaba —una banda de 4,9 puntos por un costo no medido— ya no existe. El costo está
medido, el deslizamiento medio está medido, la cola está cuantificada y metida en el cálculo, y la
vía de ejecución correcta (mini) está verificada contra el límite de contratos.

**Criterio: celda 5pt:20pt vía 1 mini, costo medido $5,76 ida y vuelta. Un candidato necesita
81,2% de aciertos contra el 80,0% que da la moneda: +1,2 puntos de ventaja real.**

Esa celda es además la que pasó los dos filtros de terreno **con margen** (deslizamiento 19,1% contra
el corte de 25%, tenencia por encima del 50% en las dos ventanas), no al borde.

### Lo que sigue sin estar

- **Ruido de Monte Carlo**: ±0,3 puntos en los requeridos. El +1,2 es real pero no tiene tres cifras.
- **Deslizamiento de entrada**: no medido. Sólo está medido el exceso en el stop.
- **El filtro de tenencia sigue indeterminado para un candidato con ventaja** (conclusión del
  2026-09-04, sin cambios): el candidato tiene que traer su propia distribución de tenencia.
- **El terreno es 2016-2019.** La estructura de 2020+ está en la caja sellada.

---

# LO QUE EL CRITERIO NO PUEDE CONTESTAR SOLO (2026-09-04, tercera vuelta)

**No gasta cartucho. K = 261.** Verificación previa: la celda publicada reproduce (Tradeify
20pt:10pt con costo viejo $2,50 → 34,1%). El modelo no se tocó para esto.

## 1 — Deslizamiento de entrada: NO medible acá, pero acotado

**No se puede medir con los datos del proyecto.** `es_1min_databento.csv` es schema **ohlcv-1m**
(así lo declara `data/data_quality_es_1min_databento.md`): barras OHLCV, sin bid/ask y sin libro.
Todo lo medido hasta acá es la **salida** — el exceso por encima del stop, dentro de la barra que lo
toca.

**Qué haría falta:** Databento GLBX.MDP3 schema **`mbp-1`** (tope de libro) o `mbo`, mismo símbolo y
mismo período. Con eso se mide el spread y el llenado contra el medio en la entrada.

**La acotación, que sirve igual.** El deslizamiento de entrada pega en **las dos ramas** — se paga al
entrar, se gane o se pierda — a diferencia del de salida, que sólo pega en la perdedora. Como sale de
una rama y entra en la otra, la suma gana+pierde no cambia y el efecto es exactamente lineal:

| entrada | equilibrio | ventaja pedida |
|---|---|---|
| 0 | 81,20% | +1,20 |
| 0,5 tick | 81,68% | +1,68 |
| **1 tick** | **82,16%** | **+2,16** |
| **1,25 ticks** | **82,40%** | **+2,40** |

**Cada punto de entrada sube el equilibrio 3,849 puntos de acierto. Un solo tick lo sube 0,96 puntos
— el 80% de la ventaja entera. A 1,25 ticks la ventaja pedida se duplica.**

Dicho al revés: el +1,2 de ventaja **ya es el equilibrio**, no un excedente. Cualquier deslizamiento
de entrada positivo lo vuelve insuficiente. Y en un objetivo de 5 puntos —20 ticks— un tick es el 5%
del bruto.

## 2 — Cuántas operaciones para verificar a un candidato

**Tu hipótesis (~17.000): refutada en magnitud, confirmada en sustancia.**

17.442 es el n de **dos muestras**. Pero acá la moneda no se estima: es `S/(S+T) = 20/25` **exacto,
conocido analíticamente**. Entonces es una prueba de **una** muestra contra un valor conocido, y el n
cae por un factor de ~2,5.

α 0,05 una cola, potencia 80%:

| bracket | moneda | equilibrio | δ | n exacto | op/día | **años** |
|---|---|---|---|---|---|---|
| 5pt:10pt | 66,7% | 68,9% | 2,3 | 2.759 | 1 | 10,9 |
| 10pt:10pt | 50,0% | 52,3% | 2,3 | 3.042 | 1 | 12,1 |
| 20pt:10pt | 33,3% | 35,3% | 1,9 | 3.886 | 1 | 15,4 |
| **5pt:20pt** | 80,0% | 81,2% | **1,2** | **6.988** | 1 | **27,7** |
| 10pt:20pt | 66,7% | 68,1% | 1,4 | 6.988 | 1 | 27,7 |

**6.988 operaciones, no 17.000. A 1 operación por día — el ritmo que el terreno da para un stop de
20pt — son 28 años.** El orden de magnitud del problema no cambia: **el criterio existe y no se puede
comprobar sobre ningún candidato en un plazo humano.**

Y la celda elegida es **la peor de la tabla para verificar**: 6.988 contra 2.759 de 5pt:10pt.

### ¿Hay atajo?

- **(a) Medir el P&L en vez de la tasa de acierto: NO.** El P&L es función determinística del
  resultado binario, así que lleva la misma información. n = 6.878 contra 6.988: el mismo número.
- **(b) Cambiar de bracket: SÍ, pero cuesta.** 5pt:10pt baja a 2.759 (11 años). Pero esas celdas no
  sobreviven el terreno con margen. **El costo de la factibilidad es la verificabilidad.**
- **(c) Medir el estadístico intermedio: en principio sí, con advertencia.** Si el candidato expone
  una señal **continua**, contrastar su correlación con el retorno futuro usa mucha más información
  por observación que un binario 80/20. Pero prueba **otra** hipótesis —que la señal predice— y para
  pasar de ahí a la esperanza del bracket hay que volver a la misma aritmética de barreras. Exige que
  el candidato exponga la señal, no sólo los trades.

**Con la tasa de acierto final del bracket elegido, no hay atajo.**

## 3 — La forma del bracket, en palabras

**5 puntos de objetivo contra 20 de stop es ganar poco y seguido, y perder mucho de golpe.**

- Una ganada paga **$244**. Una perdida cuesta **$1.055**. Hacen falta **4,3 ganadas para pagar una
  perdida**.
- Al 80% —lo que da la moneda— acertás **4 de cada 5**, y la quinta se lleva las cuatro.
- **El 5,1% de las muertes las causa un solo llenado malo**, no una racha.
- El peor llenado observado en cuatro años se come el **89% del drawdown entero en una operación**, y
  el drawdown es *trailing*: después de cualquier ganancia ese margen ya no está.

**Tres lecturas que hay que evitar, dichas antes de que alguien las haga:**

1. **81,2% es el PISO donde la esperanza es cero, no la meta.** A exactamente ese nivel **no se gana
   nada**. Es el punto donde operar deja de perder plata, no donde empieza a ganarla.
2. **P(pasar) al criterio es 6,1%.** Contra una cuota de $83 y un premio de $1.350, eso es
   **exactamente empate**. No es una oportunidad: es una moneda justa después de pagar todo.
3. **La celda elegida es la de MAYOR tasa de acierto requerida de toda la tabla** — 81,2% contra
   35,3% de la más baja. **Se eligió por factibilidad de terreno, no por ser la más fácil.** Fue una
   **restricción**, no una preferencia: es la única celda que pasó los dos filtros con margen. Las
   celdas con requisitos mucho más bajos existen y están medidas, pero el terreno las descarta.

---

# LA ESPECIFICACIÓN PARA LA BÚSQUEDA (2026-09-04, cuarta vuelta)

**No gasta cartucho. K = 261.**

**Verificación de la inversión**: la directa da `n_exacto(80,0% → 81,2%) = 6.988` y la inversa
devuelve **1,182 puntos** a ese n (esperado 1,200; el hueco de 0,018 es porque `n_exacto` avanza en
pasos geométricos y devuelve un n algo mayor que el mínimo). Cierra dentro de 0,05 puntos.

## 1 — Diferencia mínima detectable por presupuesto

α 0,05 una cola, potencia 80%. La conversión a dólares es exacta y no depende de nada más:
**ΔE = δ · (gana + pierde)**, porque `E(p) = p·gana − (1−p)·pierde` es lineal en p.

El ritmo sale del terreno con las dos barreras: los brackets con objetivo de 5pt resuelven dentro de
la rueda (3,5 op/día); los demás no cruzan el 50% ni en la sesión completa (1 op/día).

| bracket | moneda | **n=250** | | **n=1.000** | | **n=3.000** | | op/día |
|---|---|---|---|---|---|---|---|---|
| | | pts | $/op | pts | $/op | pts | $/op | |
| 5pt:10pt | 66,7% | 7,45 | $59 | 3,70 | **$29** | 2,13 | $17 | 3,5 |
| 10pt:10pt | 50,0% | 8,02 | $83 | 3,98 | $41 | 2,28 | $24 | 1,0 |
| 20pt:10pt | 33,3% | 7,89 | $121 | 3,80 | **$58** | 2,19 | $34 | 1,0 |
| **5pt:20pt** | 80,0% | 6,03 | $78 | 3,14 | **$41** | 1,81 | $23 | 3,5 |
| 10pt:20pt | 66,7% | 7,45 | $115 | 3,70 | $57 | 2,13 | $33 | 1,0 |

**En tiempo:** 250 operaciones son 0,3 años (objetivo 5pt) o 1,0 año (el resto). 1.000 son 1,1 o 4,0
años. 3.000 son 3,4 o 11,9 años.

## 2 — El piso: qué tiene que prometer una idea para que valga la pena medirla

**Hay dos pisos y manda el más alto.**

- **Rentabilidad** — la ventaja que hace que operar deje de perder plata. Fija por bracket.
- **Detectabilidad** — la ventaja mínima que el presupuesto puede distinguir de la moneda.

| bracket | piso rentabilidad | | piso n=250 | piso n=1.000 | piso n=3.000 |
|---|---|---|---|---|---|
| | pts | $/op | $/op | $/op | $/op |
| 5pt:10pt | 2,26 | $17,79 | $59 ✗ | $29 ✗ | **$17 ✓** |
| 10pt:10pt | 2,30 | $23,81 | $83 ✗ | $41 ✗ | **$24 ✓** |
| 20pt:10pt | 1,94 | $29,83 | $121 ✗ | $58 ✗ | $34 ✗ |
| **5pt:20pt** | **1,20** | **$15,58** | $78 ✗ | $41 ✗ | $23 ✗ |
| 10pt:20pt | 1,43 | $22,13 | $115 ✗ | $57 ✗ | $33 ✗ |

**✗ = el presupuesto no alcanza ni para distinguir el punto de equilibrio.** Una idea exactamente
rentable sería **invisible** ahí.

- **Con 250 y con 1.000 operaciones, ningún bracket llega**: el equilibrio de cualquiera de ellos es
  indemostrable.
- **Con 3.000 recién aparecen dos**: 5pt:10pt y 10pt:10pt.
- **La celda del criterio (5pt:20pt) no llega en ninguno de los tres.** Con 3.000 operaciones el MDE
  es 1,81 puntos y su equilibrio está en 1,20.

## 3 — La regla que sale de esto

Una idea tiene que prometer **entre 1,6 y 2,6 veces el equilibrio de su propio bracket** para ser
demostrable en 1.000 operaciones:

| bracket | detectabilidad ÷ rentabilidad, n=1.000 |
|---|---|
| 5pt:10pt | **1,63×** ← el más medible |
| 10pt:10pt | 1,73× |
| 20pt:10pt | 1,96× |
| 10pt:20pt | 2,59× |
| **5pt:20pt** | **2,62×** ← el criterio, el menos medible |

**El piso no es un número: depende del bracket.** Con el mismo presupuesto de 1.000 operaciones va de
$29/op a $58/op. Por eso la tabla y no una cifra.

**Consecuencia operativa para la búsqueda:** una idea que prometa menos que el piso de su bracket **se
descarta antes de medirla** — no porque sea falsa, sino porque no es demostrable con el presupuesto
disponible. Y si lo que se quiere es *poder medir*, el bracket para probar ideas es **5pt:10pt**
($29/op, 1,1 años para 1.000 operaciones), no el del criterio.

Es la misma tensión de siempre, ahora con número en las dos puntas: **el costo de la factibilidad es
la verificabilidad.** La celda que el terreno deja usar es la que menos se puede comprobar.

---

# COMPUERTA 1 — LA RAMA DE EJECUCIÓN AL CIERRE SE CIERRA (2026-09-04)

**No gasta cartucho. K = 261.** Es una **compuerta de factibilidad** sobre datos ya medidos: no se
busca ninguna ventaja, no hay estadístico contra un α, no se elige entre candidatas. Se mide si una
mecánica de ejecución cabe dentro de un límite de pérdida ya publicado. **Que nadie la cuente como
test.** Verificación previa: la celda publicada reproduce (34,1% con costo viejo).

## Por qué esta compuerta va primero

TMAC/BTIC/TACO fijan el precio por fórmula, no por el libro. Ejecutar así significa **entrar en un
cierre y salir en otro**: no hay objetivo ni stop intradiario, la posición queda expuesta toda la
noche sin freno. Y **los Micro E-mini no son elegibles**, así que la unidad mínima es **un ES
completo, $50/punto** — no se puede bajar el tamaño, que es la palanca habitual.

## (a) El límite

**$2.000, Trailing Max Drawdown (EOD)**, 50K Growth — widget oficial de tradeify.co leído 2026-09-03
(`datos_crudos.md`). Es **trailing**: sube con las ganancias y no baja; se usó esa mecánica.

A $50 el punto, **el drawdown entero son 40 puntos de ES.**

*Valor del punto verificado, no asumido*: $50, tabla oficial de instrumentos de apextraderfunding.com
(2026-09-03), consistente con MES $5 × 10 y con el límite «4 minis/40 micros» de Tradeify. La página
de CME dio timeout al reverificar hoy; queda anotado.

## (b) Los movimientos de cierre a cierre

ES 1-min Databento, **2016-01-05 → 2019-12-31**, fuera de la caja sellada 2020-2026. **955 noches**,
sólo pares con el mismo contrato (un roll no es una pérdida).

| | puntos | USD (1 ES) |
|---|---|---|
| mediana \|mov\| | 8,75 | $438 |
| p90 | 32,75 | $1.638 |
| p99 | 71,81 | $3.590 |
| **máximo** | **118,75** | **$5.938** |

**El peor movimiento de una sola noche es tres veces el drawdown entero.**

## (c) Noches sueltas que exceden el límite

| | % | frecuencia |
|---|---|---|
| cierre a cierre, en contra | **5,55%** | 1 de cada 18 noches |
| excursión adversa, largo | **8,38%** | 1 de cada 12 noches |
| excursión adversa, corto | 5,03% | 1 de cada 20 noches |

## (d) Probabilidad de morir antes de completar N noches

Trailing, lado al azar cada noche, **sin ninguna estrategia**:

| N noches | cierre IID | cierre histórico | intradía IID | **intradía histórico** |
|---|---|---|---|---|
| 5 | 27,7% | 23,6% | 44,1% | **34,9%** |
| 10 | 50,9% | 42,2% | 68,3% | **54,9%** |
| 20 | 69,8% | 62,6% | 82,3% | **73,4%** |

**CONTROL: con tamaño de posición cero, las cuatro medidas dan 0,00% en los tres N. PASADO.**

Una nota contra la intuición: **el histórico (con agrupamiento) da menos muerte que el IID**, no más.
En este proyecto se viene diciendo que el agrupamiento vuelve optimistas los números; acá va en la
dirección contraria, porque los tramos tranquilos son la mayoría y bloquear los preserva. Se dice
como salió, no como se esperaba.

## VEREDICTO — la rama se cierra

**La rama de ejecución al cierre NO es viable para esta cuenta.** Sin ninguna estrategia, sólo por el
salto nocturno, la cuenta muere entre el 42% y el 68% de las veces antes de completar diez noches — y
la cadena de la evaluación necesita al menos eso. Una de cada doce noches, sola, se lleva el drawdown
entero. Y no hay forma de achicar la apuesta: el micro no es elegible.

**No se avanza a la Compuerta 2.**

### Qué haría falta (la única palanca es un drawdown más grande)

| drawdown | puntos | muerte en 10 noches |
|---|---|---|
| $2.000 (el de esta cuenta) | 40 | 54,9% |
| $4.500 (Topstep 150K, el mayor medido) | 90 | 18,7% |
| $9.000 | 180 | 3,7% |

**Ninguna de las ocho firmas medidas ofrece un drawdown que alcance.** La rama necesitaría una cuenta
de un orden de magnitud distinto al que existe en el mercado medido.

### Deuda anotada, no estimada

**¿TMAC cobra un cargo adicional sobre la comisión normal? NO MEDIDO.** No se buscó y no se estima.
Efecto potencial: se sumaría al costo por operación y subiría el equilibrio, igual que la comisión
antes de medirla. Es irrelevante para este veredicto —la compuerta se cierra por riesgo, no por
costo— pero queda escrito por si la rama se reabre alguna vez con una cuenta mayor.

---

# CENSO DE INSTRUMENTOS — ¿existe alguno donde $2.000 sea MUCHO? (2026-09-04)

**No gasta cartucho. K = 261.** Es un censo de instrumentos contra una restricción de cuenta ya
medida: no hay hipótesis sobre el mercado, no hay estadístico contra un α, no se elige entre
candidatas por resultado.

**CONTROL, y reproduce exacto:** la fórmula nueva sobre ES devuelve el drawdown equivalente a **40
puntos** y las tres frecuencias de quiebre de la Compuerta 1 — **5,55% / 8,38% / 5,03%**, al centésimo.

## La pregunta que nunca se hizo

La Compuerta 1 murió por **tamaño**, no por ventaja. Y todo este proyecto midió ES y NQ: los dos
futuros de índice más grandes y volátiles que existen. Nunca se preguntó si hay un contrato donde
$2.000 sea mucho.

Dos razones, las dos en la misma unidad (movimientos típicos de una sesión, **un** contrato micro):

- **HOLGURA** = $2.000 ÷ movimiento adverso típico → cuántos golpes malos aguantás
- **ESFUERZO** = $3.000 ÷ movimiento favorable típico → cuántos buenos necesitás

## La tabla, ordenada por holgura

Diarios 2016-2019. Specs oficiales: apextraderfunding.com, pestaña «Micro Futures», 2026-09-04.
**Todo el cuadro: permiso de Tradeify NO VERIFICADO** (las specs son del exchange y valen; la lista de
instrumentos permitidos es de la firma y no está leída).

| instrumento | $/pt | adv $ | fav $ | **HOLGURA** | **ESFUERZO** | vs ES |
|---|---|---|---|---|---|---|
| E-Micro Gold (MGC) | 10,00 | 28,00 | 28,00 | **71,4** | 107,1 | solo holgura |
| Micro Dow (MYM) | 0,50 | 38,50 | 47,75 | 51,9 | 62,8 | solo holgura |
| Micro Russell (M2K) | 5,00 | 40,50 | 45,50 | 49,4 | 65,9 | solo holgura |
| **Micro S&P (MES)** | 5,00 | 43,75 | 51,25 | 45,7 | 58,5 | — |
| Micro Nasdaq (MNQ) | 2,00 | 56,75 | 67,00 | 35,2 | 44,8 | solo esfuerzo |
| Micro Crude (MCL) | 100,00 | 59,00 | 62,00 | 33,9 | 48,4 | solo esfuerzo |

**Ninguno domina a ES.** Cada uno es mejor en una razón y peor en la otra, sin excepción.

## Por qué ninguno domina — y esto es lo que cierra la rama

No es mala suerte del muestreo: **las dos razones no son independientes.** `holgura = 2000/adv$` y
`esfuerzo = 3000/fav$` son **las dos** `1/(tamaño del movimiento)`. Un instrumento que se mueve menos
en dólares compra holgura y paga esfuerzo **en la misma proporción**. Lo único que puede romper el
empate es la asimetría entre excursión favorable y adversa, y casi no varía:

| instrumento | adv/fav | holgura/esfuerzo | vs ES |
|---|---|---|---|
| Micro Dow (MYM) | 0,806 | **0,827** | **1,06×** |
| Micro Nasdaq (MNQ) | 0,847 | 0,787 | 1,01× |
| Micro S&P (MES) | 0,854 | 0,781 | 1,00× |
| Micro Russell (M2K) | 0,890 | 0,749 | 0,96× |
| Micro Crude (MCL) | 0,952 | 0,701 | 0,90× |
| E-Micro Gold (MGC) | 1,000 | 0,667 | 0,85× |

**El mejor es 1,24× el peor, y solo 1,06× el de ES.** No hay un instrumento estructuralmente
distinto: hay seis versiones del mismo problema a distinta escala.

## La lectura, sin suavizar

**El problema no es el instrumento: es la relación entre el tamaño de la cuenta y cualquier futuro
operable.** Ninguno de los seis alcanza. El mejor intercambio disponible (Micro Dow) es **6% mejor que
ES**, y la cuenta necesitaba un orden de magnitud, no un 6%. Elegir instrumento mueve la escala del
problema, no su forma.

Si se quisiera holgura de verdad, el camino no es cambiar de contrato: es un drawdown mayor — y la
Compuerta 1 ya midió que **ninguna de las ocho firmas ofrece uno que alcance**.

## Lo que falta — vale tanto como la tabla

**A. Micro que la firma lista, spec oficial leída, SIN precio en el repo:**

| símbolo | instrumento | $/pt | dato que falta | de dónde saldría |
|---|---|---|---|---|
| SIL | E-Micro Silver | $5 | diario de SI (plata COMEX) | Databento GLBX/COMEX |
| M6A | E-Micro AUD/USD | $10.000 | diario de 6A | Databento GLBX o proveedor de FX futures |
| M6E | E-Micro EUR/USD | $12.500 | diario de 6E | Databento GLBX o proveedor de FX futures |

**B. Candidato con precio en el repo pero SIN spec oficial leída:** **MBT (Micro Bitcoin)** —
`BTC_F_daily.csv` existe, pero el micro no figura en la pestaña oficial leída. Falta la
especificación del contrato. **No se completó la fila.**

**C. Para toda la tabla:** la lista de instrumentos que **Tradeify** permite y su límite por
contrato. Saldría de la página oficial de Tradeify o su help center, igual que se leyeron las
comisiones. Hoy **NO VERIFICADO**.

---

# LA LÍNEA DE BASE, MEDIDA (2026-09-04) — y mi hipótesis era falsa

**No gasta cartucho. K = 261.** Medición de una constante del modelo, no prueba de una hipótesis.

## 1 — La ambigüedad era 0,00%. Me equivoqué.

Dije que el supuesto más débil era que `S/(S+T)` estuviera corrido porque, con barras de un minuto,
no se sabe qué barrera se tocó primero cuando las dos caen adentro de la misma barra. **Lo medí y es
falso.** El rango máximo de una barra de un minuto en ES 2016-2019 es 36pt, pero la mediana es
0,50pt y el p99 3,25pt: la barra que resuelve casi nunca es un monstruo.

**Fracción ambigua: 0,00% en los cinco brackets. Ancho de banda: 0,00 puntos.**

**CONTROL PASADO.** Bracket de 23pt a cada lado (46pt de separación, más que cualquier barra
observada): ambigüedad 0,000%, y la tasa *pooled* dio **exactamente 50,0%**. De paso midió el drift
de 2016-2019 limpio: largo 54,6% contra corto 45,4%, ±4,6 puntos que se cancelan al promediar lados.

## 2 — Pero la línea de base SÍ está corrida, y encontré por qué

| bracket | asumido | observado (1 sesión) | **sesgo** | sin resolver |
|---|---|---|---|---|
| 5pt:10pt | 66,7% | 68,2% | **+1,58** | 7,2% |
| 10pt:10pt | 50,0% | 50,0% | **+0,00** | 19,0% |
| 20pt:10pt | 33,3% | 27,3% | **−6,08** | 35,6% |
| **5pt:20pt** | 80,0% | 85,2% | **+5,17** | 17,4% |
| 10pt:20pt | 66,7% | 72,7% | **+6,08** | 35,6% |

La causa **no** es la ambigüedad: es **censura por horizonte**. Las operaciones que no resuelven no
se pierden al azar — se pierden las que iban a la barrera **lejana**. Confirmado alargando el
horizonte a cinco sesiones:

| bracket | asumido | 1 sesión | 5 sesiones | sin resolver |
|---|---|---|---|---|
| 5pt:10pt | 66,7% | 68,2% | **67,2%** | 7,2% → 0,0% |
| 20pt:10pt | 33,3% | 27,3% | **31,2%** | 35,6% → 4,0% |
| 5pt:20pt | 80,0% | 85,2% | **81,6%** | 17,4% → 1,1% |
| 10pt:20pt | 66,7% | 72,7% | **68,8%** | 35,6% → 4,0% |

Todas convergen hacia `S/(S+T)`. El bracket simétrico nunca estuvo sesgado, porque ahí la censura es
simétrica.

**Conclusión: `S/(S+T)` es correcto como límite de horizonte infinito, y equivocado a cualquier
horizonte realista.** El modelo supone que toda operación resuelve alguna vez; entre el 7% y el 36%
no resuelve en una sesión.

### La pregunta que decide

**El +1,2 del criterio es MÁS CHICO que el sesgo de su propia línea de base.** En la celda del
criterio (5pt:20pt) el sesgo a una sesión es **+5,17 puntos: 4,3 veces el criterio**. Incluso a cinco
sesiones queda **+1,6**, todavía por encima de 1,2.

**El criterio no se distingue de la incertidumbre de su propio cero** — pero por censura de
horizonte, no por la ambigüedad que yo había señalado.

Y las dos cosas se enganchan: **las operaciones censuradas son exactamente las que quedan abiertas al
cierre**, y la Compuerta 1 ya midió que aguantar de un cierre al siguiente mata la cuenta entre el
42% y el 68% de las veces en diez noches. El «bonus» aparente en la tasa de acierto **es** el costo
que la compuerta 1 midió por separado.

## 3 — Contaminación horaria: real en la constante, inmaterial en el criterio

**Esto NO declara ninguna regla de operación.** Son dos constantes, medidas, puestas al lado.

| D | media TODAS | media SIN 17:00 | cambio | peso de 17:00 en n |
|---|---|---|---|---|
| 4pt | 0,5556 | 0,5341 | −3,9% | 2,8% |
| 10pt | 0,9499 | 0,9140 | −3,8% | 2,7% |
| 20pt | 1,6931 | 1,5283 | **−9,7%** | 4,8% |

La reapertura pesa 2,7–4,8% de la muestra y mueve la media hasta 9,7%: es un outlier, no un sesgo
general. **Efecto sobre el requerido: entre −0,0 y −0,2 puntos.** Inmaterial.

*Aviso:* la constante del modelo sale de la ventana T23, y en T23 no se registró la hora del toque,
así que no se puede desglosar con lo medido. Lo de arriba es una **sensibilidad del mismo tamaño**
que la contaminación, no una remedición.

## 4 — Mi error en la tabla publicada, corregido

`n_exacto` avanzaba en pasos geométricos (`n*1,05+1`) y devolvía un n cuantizado hacia arriba hasta
5%; por eso 5pt:20pt y 10pt:20pt daban los dos 6.988. **Hubo que corregirlo dos veces**: la búsqueda
binaria falló porque la potencia binomial exacta **no es monótona en n**. La versión final usa el
**último cruce**.

| bracket | publicado | corregido | cambio |
|---|---|---|---|
| 5pt:20pt | 6.988 | **6.875** | −1,6% |
| 10pt:20pt | 6.988 | **7.053** | +0,9% |
| 5pt:10pt | 2.759 | **2.865** | +3,8% |
| 10pt:10pt | 3.042 | **3.002** | −1,3% |
| 20pt:10pt | 3.886 | **3.569** | −8,2% |

La colisión se rompió y **ninguna conclusión cambia**: 6.875 sigue siendo ~27 años a 1 op/día.

## 5 — La última palanca de parámetros: cerrada

| firma | objetivo | drawdown | obj/dd |
|---|---|---|---|
| Apex, Topstep, Lucid, BluSky, TPT, **Tradeify**, MFFU | 3.000 | 2.000 | **1,500** |
| FundedNext Flex | 2.500 | 1.500 | 1,667 |

**Siete de ocho son idénticas.** El rango entero es 11%, y la única distinta es peor. La escala
(drawdown absoluto) va de $1.500 a $2.000, contra los **$9.000** que la Compuerta 1 midió como
necesarios: **falta un factor de 4,5**.

**La palanca de parámetros queda cerrada entera: ni instrumento, ni bracket, ni firma.**

---

# REVISIÓN HACIA ATRÁS Y CAMINO 3 (2026-09-04)

**No gasta cartucho. K = 261.**

## Revisión hacia atrás — verificada, no asumida

**¿Alguna conclusión publicada de esta ventana se apoya en una tasa medida sobre operaciones
resueltas dentro de la sesión? NO.** Verificado en el código, no supuesto:

- `bracket.py:101` — `p_win` sale de `S_ticks/(S_ticks+T_ticks)`. Es una **fórmula**, no una medición.
- Ninguna de las tasas empíricas medidas hoy (85,2%, 72,7%, 68,2%…) aparece como entrada en ningún
  cálculo publicado. La medición de hoy fue la **primera** vez que esa tasa se observó, y se hizo
  para auditar el supuesto, no para alimentarlo.

**Pero el modelo tiene el defecto espejo, y hay que decirlo.** `sim_bracket` no tiene estado «sin
resolver» a nivel operación: cada operación es `win` o `−loss`, binaria. **El modelo supone
resolución del 100%**, cuando entre el 7% y el 35% no resuelve en una sesión.

**Dirección del error:** las operaciones que el modelo no representa son exactamente las que quedan
abiertas al cierre, y la Compuerta 1 midió que aguantarlas mata la cuenta entre el 42% y el 68% en
diez noches. **El modelo omite una categoría de resultado que es letal, así que es optimista.** Las
conclusiones publicadas son todas negativas: si están corridas, están corridas hacia ser **menos**
negativas que la realidad. **Ninguna conclusión se da vuelta; varias se refuerzan.**

## Camino 3 — la parte aritmética, antes de gastar

Con los pisos ya calculados y los `n` corregidos:

| bracket | equilibrio $/op | piso n=1.000 | piso n=3.000 | op/día | meses n=1.000 | meses n=3.000 | **meses criterio** |
|---|---|---|---|---|---|---|---|
| 5pt:10pt | 17,79 | 29,06 | 16,73 | 3,5 | **13m** | 40m | 37m |
| 10pt:10pt | 23,81 | 41,20 | 23,67 | 1,0 | 48m | 143m | 143m |
| 20pt:10pt | 29,83 | 58,43 | 33,58 | 1,0 | 48m | 143m | 179m |
| 5pt:20pt | 15,58 | 40,83 | 23,49 | 3,5 | 13m | 40m | 93m |
| 10pt:20pt | 22,13 | 57,27 | 32,96 | 1,0 | 48m | 143m | 324m |

**a) Efecto mínimo:** un hallazgo en datos de flujo tiene que mover la esperanza **$29 a $58 por
operación** para ser detectable con 1.000 operaciones, y **$17 a $34** con 3.000.

**b) Meses de datos:** **13 meses** en el mejor caso (5pt:10pt, 3,5 op/día) y **48 meses** en el peor,
para 1.000 operaciones. Para demostrar el criterio mismo: de **37 a 324 meses**.

*El backtest no va más rápido que la estrategia: si toma una posición por vez, un mes de datos rinde
un mes de operaciones. **Comprar datos no compra velocidad, compra el pasado** — que es real y es lo
único que lo justifica.*

**c) ¿Determinista o estadístico? Casi todo lo medible con `mbp-1` es ESTADÍSTICO**, y hay que
decirlo porque cambia la decisión de compra. Pero la clasificación útil no es esa: es **a qué ritmo
llegan las observaciones**.

- **Mediciones de COSTO** (spread, calidad de llenado, deslizamiento de entrada): estadísticas, pero
  su unidad de observación es la **actualización de cotización** — millones por mes. El muro de las
  miles de operaciones **no aplica**. Con un mes de datos se mide el deslizamiento de entrada medio
  con varios decimales. **Este es el uso que justifica la compra**, y es exactamente el número que
  esta ventana declaró faltante y acotó en «1,25 ticks duplican la ventaja pedida».
- **Afirmaciones de VENTAJA** (el flujo predice el próximo movimiento): el pago se realiza a nivel
  operación, así que **el muro aplica entero**. Podés estimar la señal con millones de observaciones
  y aun así necesitás miles de operaciones para probar que la estrategia gana, porque la conversión
  de señal a dólares pasa por la misma aritmética de barreras.

**Conclusión de compra: los datos sirven para cerrar el agujero de costo, no para escapar del muro
de la ventaja.**

**d) ¿Hay alguna medición sobre flujo que SÍ sea determinista? Sí, una: la prioridad de cola.** El
motor de matching es una **regla**, no una tendencia: con `mbo` se observa la posición exacta en la
cola, y bajo FIFO un llenado es consecuencia mecánica del volumen que pasa por delante, no una
probabilidad estimada. Se verifica con pocos casos. **Dos advertencias:** que ES use FIFO puro no
está verificado en este proyecto (algunos productos de CME usan pro-rata), y —lo importante— eso
**acota un costo, no produce una ventaja**. Refuerza la clasificación de (c).

---

# EL TERCER ESTADO, Y UNA CONCLUSIÓN QUE SÍ SE DA VUELTA (2026-09-04)

**No gasta cartucho. K = 261.**

## 1 — «Abierta al corte» ya está en el modelo. Y mi sospecha era falsa.

`sim_bracket` suponía resolución del 100%. Ahora tiene el tercer estado, con el valor a mercado
**medido** (no supuesto) de las operaciones que no resuelven.

**Dos controles, los dos pasan:**
- Con fracción abierta = 0, el modelo nuevo reproduce el viejo **idéntico a cuatro decimales** en los
  cinco brackets.
- **Control de consistencia** (agregado tras encontrar un error propio, abajo): una entrada al azar
  debe dar esperanza ≈0 por operación antes de costo. Da entre −0,007 y +0,071 puntos.

| bracket | abierta | M2M medio | **P vieja** | **P nueva** | dif rel |
|---|---|---|---|---|---|
| 5pt:10pt | 7,1% | −2,005 | 3,239% | 3,927% | **+21,3%** |
| 10pt:10pt | 18,9% | 0,000 | 4,402% | 4,381% | −0,5% |
| 20pt:10pt | 35,4% | +3,323 | 5,114% | 5,295% | +3,5% |
| **5pt:20pt** | 17,4% | −5,798 | 6,236% | **6,892%** | **+10,5%** |
| 10pt:20pt | 35,4% | −3,323 | 6,088% | 6,713% | +10,3% |

**Yo había dicho que sospechaba que las P(pasar) bajarían. Suben.** La corrección tiene dos partes
que tiran en sentidos opuestos: la tasa medida entre las resueltas es **más alta** que la asumida
para los brackets de objetivo cercano (85,2% contra 80,0% en 5pt:20pt), y el M2M de las abiertas es
**negativo**. Gana la primera.

### El error que casi publico

La primera corrida mezcló la tasa de resueltas **asumida** con el M2M **medido**, y dio 20pt:10pt
subiendo **+199,6%**, por encima del equilibrio. Es imposible: una entrada al azar no puede tener
esperanza positiva. Chequeada la esperanza por operación antes de costo, esa mezcla fabricaba hasta
**±1,18 puntos** de ventaja fantasma. **Las piezas medidas y las supuestas no se pueden combinar.**
Quedó como control mecánico para que no vuelva a pasar.

### La conclusión que se da vuelta

**Dos celdas cruzan el equilibrio** (6,148%): 5pt:20pt con 6,892% y 10pt:20pt con 6,713%. Para
5pt:20pt eso es **E = +$10** en un intento de $83, con **cero ventaja**.

**Hay que decirlo sin suavizar: el titular «negativa en 48 de 48 celdas» no sobrevive intacto** para
esta celda bajo el modelo corregido. Pero el margen es **más chico que varias cosas conocidas y no
modeladas**:
- **Deslizamiento de entrada, no medido.** Un solo tick agrega +0,96 puntos al requerido; por la
  elasticidad de barrera (~7,9) eso baja P a ~6,2%, al filo. **Dos ticks lo matan.**
- **La regla de consistencia (35–40%) no está modelada** y solo puede restar.
- **Los insumos medidos arrastran contaminación de drift** (ver la anomalía, abajo).
- Y es el criterio **(ii)**, el del billete de lotería, no el **(i)** de operar rentable: a 5pt:20pt
  la operación **pierde plata por vez**.

**Las otras tres celdas siguen por debajo del equilibrio y se refuerzan.** No es una reversión del
programa: es una celda marginal que pasa de −$X a +$10 y queda dentro del error de lo que falta medir.

## 2 — La anomalía de las 5 sesiones SOBREVIVIÓ. No era ruido.

Con 100.000 rutas (antes 20.000) el error **creció**: de 1,32 a **1,58**.

| bracket | asim | sin resolver | sesgo medido | la regla predice | **residuo** |
|---|---|---|---|---|---|
| 20pt:10pt | +0,333 | 4,0% | **−2,24** | −0,66 | **+1,58** |
| 10pt:20pt | −0,333 | 4,0% | **+2,24** | +0,66 | **−1,58** |
| 5pt:20pt | −0,600 | 1,1% | +1,51 | +0,33 | −1,18 |

A cinco sesiones el sin-resolver ya es solo 4%, así que la censura explica ±0,66 — y el sesgo medido
es ±2,24. **Queda un residuo de ±1,58 puntos que no viene de la censura.** Es perfectamente
antisimétrico entre 20pt:10pt y 10pt:20pt.

**No lo explico con una historia.** Es un hallazgo abierto: a horizonte largo, con la censura casi
extinguida, la tasa observada sigue apartada de `S/(S+T)` por más que el criterio entero que esta
ventana quería validar. **La medición que lo resolvería:** re-correr la réplica sobre la serie
**des-driftada** (restando el drift medio por barra). Si el residuo desaparece, es drift que no
cancela entre largo y corto en brackets asimétricos; si no desaparece, es otra cosa. No se corrió.

## 3 — Criterio permanente para decidir comprar datos

> **La pregunta no es si un hallazgo es determinista o estadístico. Es a qué ritmo llegan las
> observaciones que lo sostienen.**
>
> - **Si la unidad de observación es la actualización de cotización** (millones por mes): el muro de
>   las miles de operaciones **no aplica**. Un mes de datos alcanza para fijar una constante con
>   varios decimales. Acá viven las mediciones de **costo**: spread, calidad de llenado,
>   deslizamiento de entrada, profundidad.
> - **Si la unidad de observación es la operación** (1 a 3,5 por día): el muro **aplica entero**.
>   Acá viven las afirmaciones de **ventaja**. Da igual con cuántos millones de tics estimaste la
>   señal: probar que la estrategia gana sigue costando miles de operaciones, porque la conversión
>   de señal a dólares pasa por la aritmética de barreras.
>
> **Regla: comprar datos de alta frecuencia se justifica para acotar costos, nunca para demostrar
> una ventaja.**

### La consecuencia, corrigiendo la premisa

Me pediste escribir que «el costo ya se midió inmaterial, así que la compra no se justifica». **Eso
está mal en una parte y es importante.** Lo medido inmaterial fue la **contaminación horaria** (0,0 a
0,2 puntos) y lo medido de fuente oficial fue la **comisión** ($1,82/micro, $5,76/mini). Pero **el
deslizamiento de entrada sigue sin medirse y es el término de costo más grande que queda**: un solo
tick agrega +0,96 puntos al requerido, el 80% del criterio entero, y 1,25 ticks lo duplican.

**Entonces la compra sí se justifica, pero con un alcance mucho más chico del que se estaba
pensando:** uno o dos meses de `mbp-1` para fijar la constante de deslizamiento de entrada — no años
de historia para demostrar una ventaja. Y con lo del punto 1 encima, esa constante es justo la que
decide si la celda 5pt:20pt está arriba o abajo del equilibrio.

## 4 — Prioridad de cola: qué verificación haría falta

**No lo verifiqué: no es mi terreno.** Lo que hace falta, para que lo busques:

- **Qué:** si el algoritmo de matching de ES en CME Globex es **FIFO puro** (prioridad estricta por
  tiempo) o tiene componente **pro-rata** o asignación al primero que mejora precio.
- **De dónde:** la ficha del producto en cmegroup.com declara el algoritmo de matching por contrato;
  la fuente normativa es el **CME Rulebook** y el documento de **Globex Matching Algorithms**. Es un
  dato publicado, no hay que inferirlo.

**Si FIFO puro se confirmara, se podría acotar exactamente esto, que hoy no se puede:** con `mbo` se
reconstruye la posición exacta en la cola, y bajo FIFO el llenado de una orden pasiva es
**consecuencia mecánica** del volumen que pasa por delante — no una probabilidad estimada. Eso
permite decidir, sin estadística, **si una entrada pasiva es alcanzable**: o sea si el deslizamiento
de entrada se puede llevar a cero (entrando pasivo, a cambio de riesgo de no ejecutar) o hay que
pagarlo sí o sí (cruzando el spread). **Hoy el modelo no distingue esas dos cosas y simplemente
supone un costo.** Y por el punto 3, esa distinción es la que decide la compra.

---

# TRES CORRECCIONES A MI PROPIO TRABAJO (2026-09-04)

**No gasta cartucho. K = 261.**

## 1 - Las «simetrias exactas» eran identidades de construccion. Roberto tenia razon.

Reporte dos simetrias exactas como si fueran hallazgos. **No lo eran.** Para una entrada al precio p:

```
20pt:10pt LARGO  ->  niveles {p-10, p+20}, gana si toca +20 primero
10pt:20pt CORTO  ->  niveles {p-10, p+20}, gana si toca -10 primero
```

**Son los mismos dos niveles con las etiquetas invertidas**, y como las entradas usan la misma
semilla, son **los mismos caminos**. De ahi sale, para cualquier serie, con drift o sin el:

```
P_pooled(20:10) = 1 - P_pooled(10:20)        exacto
P_pooled(10:10) = 1/2                         exacto
```

Verificado numericamente sobre lo ya medido: las tasas publicadas suman **100,0% clavado**, y
`sort(M2M 20:10) == sort(-M2M 10:20)` da **True** elemento a elemento.

**Dos consecuencias que hay que decir:**
- **El residuo de la anomalia es UN numero, no dos brackets que se confirman.** 20pt:10pt y
  10pt:20pt son la misma medicion con el signo cambiado.
- **El control «pooled = 50,0% clavado» era VACIO.** No podia dar otra cosa. Lo que si medía algo era
  la **separacion largo/corto** (54,6% / 45,4%), que es donde vive el drift y que el pooling destruye.

## 2 - El residuo SOBREVIVE al des-drift. No es drift ni censura.

Mi primer des-drift **sobre-corrigio**: la separacion largo/corto no se cerro, se dio vuelta
(+5,67 -> -6,18). Restar a cada contrato su tendencia completa no es restar el drift del mercado.
Calibrado contra la separacion del bracket simetrico (que por identidad es drift puro), el factor
correcto es **0,425**.

| factor | 10:10 sep | 20:10 sep | 20:10 pooled | 5:20 pooled |
|---|---|---|---|---|
| 0,00 | +5,67 | +5,67 | -2,15 | +1,52 |
| 0,50 | -1,00 | -0,66 | -2,05 | +1,21 |
| 1,00 | -6,18 | -6,56 | -1,65 | +0,92 |

**El drift vive casi enteramente en la separacion largo/corto y casi nada en el pooled**: la
separacion barre 12 puntos mientras el pooled se mueve medio punto.

En el factor calibrado (separacion ~ 0):

| bracket | pooled | censura predice | **RESIDUO** |
|---|---|---|---|
| 10pt:10pt | +0,00 | -0,00 | +0,00 |
| 20pt:10pt | -2,03 | -0,71 | **-1,32** |
| 5pt:20pt | +1,19 | +0,41 | **+0,78** |

**El residuo sobrevive.** Era 1,58 con drift; des-driftado queda **1,32**. No es censura y no es drift.

### Lo que eso obliga a decir

**El modelo de barreras sin drift no describe este mercado.** `S/(S+T)` esta corrido por ~1,3 puntos
por algo que no esta identificado. **Todo esto se apoya en el:**

- La columna «moneda sin ventaja» de **todas** las tablas de criterio (66,7% / 50,0% / 33,3% / 80,0%).
- La «ventaja pedida» = requerido - moneda, y por lo tanto **el criterio de +1,2 puntos**.
- La vara de 1,181x y todo lo derivado.
- Los pisos de medibilidad y las MDE, que miden delta contra `p0 = S/(S+T)`.
- El calculo de potencia (n = 6.875 y compania), que usa `S/(S+T)` como la nula conocida.
- La tabla de 48 celdas, via el `p_win` por defecto de `sim_bracket`.

**El residuo (1,3) es del mismo tamano que el criterio (1,2).** No invalida el signo de las
conclusiones negativas -esas tienen margen- pero **si invalida cualquier afirmacion al nivel de un
punto porcentual**, que es exactamente el nivel del criterio.

## 3 - El positivo de +$10 esta muerto tres veces

| presion | umbral que lo anula | disponible |
|---|---|---|
| **(a) deslizamiento de entrada** | **0,28 ticks** ($3,47/op) | cruzar el spread cuesta >= 1 tick |
| **(b) caida de la tasa de acierto** | **0,32 puntos** | el residuo sin explicar es **0,78** (2,4x) |
| **(c) precio de la cuota** | $83 -> $93 | **la lista es $165**, ahi E = **-$72** |

**(a)** Corrijo lo que dije antes («un tick al filo, dos lo matan»): lo mata **un cuarto de tick**.
Era optimista por ~3,5x. Y el minimo que se paga cruzando el spread es un tick entero.

**(c)** Auditados los dos insumos: el **cobro de $1.350** = $1.500 x 90%, los dos MEDIDOS de fuente
oficial (help.tradeify.co, 2026-09-03) - **solido**. La **cuota de $83 es el precio promocional con
codigo SEP**; el de lista es **$165**, del mismo widget oficial. Los dos estan medidos pero **no son
la misma clase de numero: el cupon caduca.** A precio de lista el positivo no existe.

### (d) Es plausible que una entrada al azar gane contra la evaluacion?

**No, y no lo descarto por incomodo sino porque tres cosas medidas lo matan y una cuarta lo hace
implausible a priori.**

Si el producto fuera estructuralmente +EV para gente que tira monedas, seria arbitrable: comprar mil
evaluaciones. **La firma limita a 5 cuentas por trader** (`datos_crudos.md`) - un limite que existe
precisamente para eso. Y el margen es de $10 sobre $83, dentro del error de lo que falta.

**Mi lectura: falta un termino, y puedo nombrar cuales.** La regla de consistencia (35-40%) no esta
modelada y solo puede restar. El deslizamiento de entrada no esta medido y un cuarto de tick lo mata.
El residuo de 1,3 puntos no esta explicado y es 2,4x lo necesario. **El +$10 es el tamano del error
del modelo, no una oportunidad.** Lo que si quedo demostrado es otra cosa, y es util: **el signo de
esta celda depende de terminos que no medimos**, asi que ningun numero de esta ventana debe usarse al
nivel del punto porcentual.

## 4 - El histograma del M2M: mi sospecha era falsa

Sospeche masa apilada contra las barreras. **No hay.** Con la franja del 10% exterior a cada lado:

| bracket | 10% inferior | 10% superior | medio |
|---|---|---|---|
| 5pt:10pt | 1,2% | 2,0% | 96,8% |
| 20pt:10pt | 2,5% | 1,3% | 96,1% |
| 5pt:20pt | 1,2% | 3,8% | 95,0% |

Contra el 10% que daria una uniforme, los bordes tienen **1,2% a 3,8%**: la distribucion es de centro
pesado, no bimodal. **El remuestreo del modelo esta bien repartido.** Negativo limpio.

## 5 - FIFO, actualizado

ES y NQ usan FIFO, ordenes en espera por estricta prioridad temporal - **fuente SECUNDARIA**
(databento.com/blog/cme-matching-algorithms-explained). **Falta la ficha oficial del producto; no se
trata como primario.** Consecuencia si se confirmara: la entrada pasiva es posible en principio, y el
deslizamiento de entrada podria ser cero o negativo **a cambio de riesgo de no ejecucion y de
seleccion adversa** - dos terminos que este modelo tampoco tiene. Dado el punto 3(a), **esa es la
medicion que mas mueve el signo de todo.**

---

# EL TEST SINTÉTICO: EL REPLICADOR ESTÁ BIEN, Y MIS BARRAS DE ERROR ESTABAN MAL (2026-09-04)

**No gasta cartucho. K = 261.** Validación de un instrumento contra casos de respuesta conocida. No
hay hipótesis de mercado contra el α heredado, no se elige entre candidatas, no se declara ninguna
regla de operación. La caja sellada (ES diario 2020-01-02 → 2026-08-19) no se tocó: todo es
2016-2019.

**La predicción se selló antes de correr**, en `PREDICCION_SELLADA_sintetico.md`, y quedó en el repo
sin editar.

## 0 — Qué se hizo

Se le dio al **mismo** replicador (`linea_base.replica`) dos series donde la respuesta se conoce:

- **A — gaussiano.** Paseo IID con σ = 0,6079 pt por barra (la medida en ES), con `m` sub-pasos
  dentro de cada barra para que el rango intrabarra no sea degenerado. `m = 3` calibrado contra el
  rango medio real (0,6577 pt): da 0,6399, el más cercano de la grilla.
- **B — bootstrap.** Remuestreo IID de los **tripletes** reales de cada barra (Δcierre, extensión
  arriba, extensión abajo contra el cierre anterior), centrados a media cero. Conserva **exactamente**
  la forma marginal de la barra de ES y destruye **sólo** la estructura serial. Reproduce el rango
  real al 0,2%.

## 1 — El resultado, sin adornar

**El replicador no está roto. El residuo es una propiedad del ES real.**

Sobre series IID sin drift con las marginales exactas de ES, el sesgo *pooled* corregido por censura
vuelve a `S/(S+T)`:

| horizonte | bracket | media de 10 series | desvío entre series |
|---|---|---|---|
| 5 sesiones | 10pt:10pt | −0,005 | 0,007 |
| 5 sesiones | 20pt:10pt | **+0,259** | 0,239 |
| 5 sesiones | 5pt:20pt | **−0,199** | 0,236 |

Y el real cae **afuera** de esa nula, en los dos brackets asimétricos:

| bracket | residuo REAL | nula media | nula desvío | en desvíos | recorrido de las 10 | ¿cae adentro? |
|---|---|---|---|---|---|---|
| 20pt:10pt | −1,32 | +0,259 | 0,239 | **−6,6** | [+0,00, +0,65] | **NO** |
| 5pt:20pt | +0,78 | −0,199 | 0,236 | **+4,2** | [−0,46, +0,23] | **NO** |

Eso es todo lo que dice, y no digo más: **el residuo de ~1,3 puntos es del mercado, no del código.**

## 2 — Pero la predicción sellada FALLÓ, y por qué importa

Sellé «los dos sintéticos convergen dentro de **±0,3 puntos**». La primera corrida dio +0,56, −0,92,
+1,00 y −1,09 con 0,0% sin resolver. **Falló contra la tolerancia que yo mismo escribí.**

Falló porque **la tolerancia estaba mal**, no porque el replicador lo estuviera. La derivé del error
binomial `√(p(1−p)/n)`, que supone rutas independientes. **No lo son:** se sortean 30.000 entradas
sobre 1,36 millones de barras y cada una escanea cientos o miles, así que la misma barra participa de
decenas de rutas; y además hay **una sola serie**, con su propia realización. El binomial mide el
ruido del sorteo de entradas y no ve nada de lo demás.

Medido contra 10 series independientes:

| magnitud | desvío binomial (el que usaba) | desvío real | subestima |
|---|---|---|---|
| sesgo *pooled*, 1 sesión | 0,17 – 0,20 | 0,26 – 0,29 | **1,3 – 1,8×** |
| sesgo *pooled*, 5 sesiones | 0,17 – 0,19 | 0,24 | **1,2 – 1,4×** |
| **separación largo/corto** | 0,41 | **2,08 – 2,35** | **≈ 5×** |

El *pooling* cancela casi toda la realización de la serie —es la misma identidad de construcción que
ya demostré—; **la separación es justamente la componente que la identidad no cancela**, y por eso
ahí el error explota. Todas las barras de error de esta ventana que involucren la separación estaban
mal por un factor de cinco.

## 3 — Una corrección a lo que estuve por concluir a mitad de camino

Antes del ensamble corrí dos tests de localización (`sintetico_escala.py`) suponiendo que el sesgo
era **sobrepaso de barrera** —un paseo con saltos cruza la barrera en vez de tocarla, y el paro
opcional da `p = (S+o)/(S+T+2o)`—. Las dos predicciones escritas antes de correr:

- **por tamaño:** a razón fija el sesgo debe caer como 1/tamaño. Dio +1,34 → +1,12 → **+2,21** donde
  esperaba +1,34 → +0,67 → +0,34.
- **por granularidad:** debe caer como 1/√m. Dio −0,05, +0,10, +0,73, −0,07, −0,06: sin tendencia, y
  con `m=1` —donde el sobrepaso es **máximo**— prácticamente cero.

Con eso yo estaba escribiendo que **todo era ruido**. **El ensamble me corrigió.** Esos dos tests
usaron horizontes de hasta 103.927 barras sobre una serie de 600.000 —cada ruta cubre el 17% de la
serie entera, quedan ~6 ventanas independientes— así que **ahí el error real es enorme y el test no
informa nada**, ni a favor ni en contra del sobrepaso. La lectura correcta de esos dos tests no es
«falsados»: es **indecidibles al tamaño de error que tienen**. Lo único que sirvió de ellos fue
destapar el problema de la barra de error, que es lo que llevó al ensamble.

## 4 — Tres cosas que la corrección mueve

1. **La media de la nula no es cero:** +0,26 y −0,20. La fórmula de censura `−0,5·asimetría·%sin
   resolver` deja un residuo sistemático. Medidos contra la nula y no contra cero, los residuos
   reales son **−1,58** y **+0,98**: la corrección los hace **más grandes**, no más chicos.
2. **El drift sobrevive, pero con mucho menos margen.** Separación real +5,67 contra una nula de
   −0,38 ± **2,08**: son **2,9 desvíos**, afuera del recorrido de las 10 series pero por poco. Con la
   barra de error vieja (0,41) eso parecía 14 desvíos.
3. **El factor de des-drift 0,425 arrastra ±0,18.** La separación barre 11,85 puntos por unidad de
   factor; ±2,08 de incertidumbre en la separación son ±0,176 en el factor. **No es 0,425: es
   0,43 ± 0,18.**

## 5 — La debilidad de este test, que es real y hay que decirla

**El bootstrap IID resuelve mucho más rápido que ES.** A una sesión deja **1,6%** sin resolver donde
el real deja **15,7%**. Es esperable —ES tiene agrupamiento de volatilidad y ratos muertos, el
remuestreo IID no— pero significa que **la nula no está apareada en el término de censura**, que es
justamente el término más grande a un día. La comparación se hace sobre el residuo ya corregido por
fórmula, y **el error de esa fórmula es lo que queda adentro del número.** Un bootstrap por bloques
apareado en la tasa de sin-resolver sería el test que cierra esto; no está hecho.

## 6 — Controles de esta corrida, cada uno con qué lo haría fallar

| control | qué lo haría fallar | resultado |
|---|---|---|
| generador: media cero, σ y rango iguales a ES | media a más de 3 errores de cero, o rango que no reproduzca | **PASADO** (rango −2,7% A, −0,2% B) |
| horizonte largo → `S/(S+T)` | sesgo > 3 errores con 0% sin resolver | **FALLADO contra el binomial**; pasado contra el desvío real |
| separación ≈ 0 en el sintético | separación > 3 errores | **FALLADO contra el binomial**; el desvío real es 5× mayor |
| identidad 10pt:10pt en el ensamble | cualquier dispersión distinta de cero | **PASADO**: desvío 0,005 |
| real contra la nula | que el real cayera adentro del recorrido | **el real queda AFUERA en los dos** |

Detalle sobre la identidad: el desvío de 10pt:10pt da 0,005 y no 0,000 exacto. La diferencia es la
**ambigüedad**: una barra que contiene las dos barreras se cuenta como pérdida para el largo **y**
para el corto, y eso rompe la antisimetría en esa fracción de casos. La identidad es exacta salvo
barras ambiguas.

---

# EL ARRASTRE DEL DES-DRIFT: NI LIMPIO NI RUIDO (2026-09-04)

**No gasta cartucho. K = 261.** Roberto marcó que en `salida_desdrift.txt` el *pooled* se movía ~0,5
puntos con el factor de des-drift cuando, por mi propia conclusión de esa misma corrida, no debería
moverse. Se corrieron seis factores en vez de tres, con números aleatorios comunes.

| factor | 10:10 pool | 10:10 sep | 20:10 pool | 20:10 sep | 5:20 pool | 5:20 sep |
|---|---|---|---|---|---|---|
| 0,00 | +0,000 | +5,67 | −2,146 | +5,67 | +1,517 | +3,68 |
| 0,20 | +0,000 | +2,74 | −1,977 | +3,08 | +1,240 | +1,91 |
| 0,40 | +0,000 | +0,19 | −2,025 | +0,59 | +1,210 | +0,56 |
| 0,60 | +0,000 | −2,11 | −2,063 | −1,89 | +1,209 | −0,96 |
| 0,80 | +0,000 | −3,91 | −1,953 | −3,95 | +1,141 | −2,40 |
| 1,00 | +0,000 | −6,18 | −1,649 | −6,56 | +0,915 | −4,00 |

| bracket | recorrido | pendiente | R² | residuo máx. de la recta | lectura |
|---|---|---|---|---|---|
| 20pt:10pt | +0,497 | +0,360 | **0,620** | 0,140 | ni recta ni dispersión |
| 5pt:20pt | −0,601 | −0,472 | **0,837** | 0,107 | ni recta ni dispersión |

**La respuesta: ninguna de las dos.** No es una recta —R² de 0,62 y 0,84 con un **plateau** claro en
el medio: 20:10 se queda entre −1,95 y −2,15 en cinco de los seis factores y sólo se despega en
1,00— y tampoco es dispersión sin orden, porque los extremos se mueven en la dirección esperada y el
residuo de la recta (0,11–0,14) es cinco veces menor que el recorrido.

**Mi conclusión anterior queda a medias.** «El drift vive en la separación y casi nada en el pooled»
es correcta en magnitud: la separación barre **11,85** puntos y el *pooled* **0,50**, un factor de 24.
Pero **«casi nada» no es «nada»**, y ese medio punto es del tamaño del criterio (+1,2) y del residuo
(−1,3). Al nivel al que estaba escrito todo esto, medio punto no es despreciable.
