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
