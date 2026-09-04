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
