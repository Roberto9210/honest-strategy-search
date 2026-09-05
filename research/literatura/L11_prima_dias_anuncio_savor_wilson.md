# L11 — Los días en que hay dato macro programado, el mercado paga diez veces más

**VENTANA L. Ficha de literatura. NO MEDIDA. No gasta cartucho, K sigue en 261.**

> **MUERTA POR REGLAMENTO — 2026-09-05.** La firma cierra toda posición a las 16:45 del este y prohíbe la noche; la prima de Savor y Wilson es cierre a cierre y necesita la noche. Aplicación de [R03](R03_cierre_por_reglamento.md) rama 3, sellada antes de leer el reglamento. Ya estaba CIEGA por 0,26 (`D06`); ahora además es inoperable.

> **DESACTUALIZADA en un punto:** su fuerza se apoyaba en la extensión de Ai, Bansal y Guo, cuya muestra **cubre 2016-2019**. Esa extensión existe, pero **ya no otorga grado A**. Ver [F7](F7_EDAD_DE_LA_EVIDENCIA.md).

**RECUPERADA.** El filtro nocturno viejo la había matado. Con el filtro de ventana de exposición
(`FILTROS.md`) sobrevive, y es **la candidata que menos lejos queda de ser medible** con lo que hay.

---

## 1. Cita completa

Savor, Pavel; Wilson, Mungo (2013). **"How Much Do Investors Care About Macroeconomic Risk? Evidence
from Scheduled Economic Announcements."** *Journal of Financial and Quantitative Analysis*, vol. 48,
n.º 2, pp. 343–375.

- Editorial: https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/abs/how-much-do-investors-care-about-macroeconomic-risk-evidence-from-scheduled-economic-announcements/C6A48B33065D93550C87FEB53C029A0B
- SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1312091
- RePEc: https://ideas.repec.org/a/cup/jfinqa/v48y2013i02p343-375_00.html

**Continuación de los mismos autores:** "Asset pricing: A tale of two days", *Journal of Financial
Economics* (2014). https://www.sciencedirect.com/science/article/abs/pii/S0304405X14000890

## 2. El efecto, en una frase

En los días en que está programado un dato macroeconómico importante sobre inflación, desempleo o
tasas, el mercado rinde **diez veces más** que en los demás días, porque quien está adentro cobra por
soportar el riesgo de que el dato salga mal.

## 3. Instrumento y período de la muestra original

- **Mercado accionario estadounidense agregado**, retornos **diarios**.
- **1958 → 2009**, cincuenta y un años.
- Los anuncios programados son los de inflación, desempleo y decisiones de tasas.

Trasladado a ES es directo: el efecto está en el índice, no en un corte transversal.

## 4. Magnitud declarada

| | retorno en exceso medio diario |
|---|---|
| **días con anuncio programado** | **11,4 puntos básicos** |
| todos los demás días | **1,1 puntos básicos** |
| **diferencia** | **10,3 pb** |

- **Más del 60 % de la prima de riesgo accionaria anual acumulada se gana en días de anuncio.**
- **La razón de Sharpe es diez veces mayor** en esos días.
- La tasa libre de riesgo es detectablemente **menor** en días de anuncio, consistente con un motivo
  de ahorro precautorio. Ése es un control fuerte: si fuera un artefacto de medición del retorno
  accionario, no tendría por qué aparecer del otro lado del balance.

### Traducción a dólares por evento por contrato ES

Uso la **diferencia** de 10,3 pb, que es la ventaja sobre estar siempre adentro, no los 11,4 brutos.

| | ES 2016-2019 | ES 2026 |
|---|---|---|
| bruto | **$134** | $330 |
| neto de ≈ $17 de ida y vuelta | **$117** | $313 |

**Segunda magnitud por operación más grande del inventario**, detrás de L10.

## 5. Antes o después de costos

**Antes, y sin estrategia propuesta.** Es un paper de valoración de activos, no de anomalías: la
pregunta es cuánto le importa a los inversores el riesgo macroeconómico. **Nadie verificó que
sobreviva a los costos**, aunque con $134 brutos contra ≈ $17 de costo el margen es amplio.

## 6. Mecanismo declarado

**Prima de riesgo por riesgo programado, no ineficiencia.**

El argumento es que los inversores **exigen una compensación** por quedar expuestos a la
incertidumbre macroeconómica que se va a resolver en una fecha conocida. Como la fecha se conoce, el
riesgo es anticipable, y quien decide quedarse adentro ese día cobra por hacerlo.

**Esto es importante para clasificarla bien y lo digo derecho: si el mecanismo es una prima de
riesgo, entonces el retorno NO ES GRATIS.** Se está cobrando por soportar un riesgo real, y la
distribución de ese día tiene cola. **No es una ineficiencia que se arbitra: es un pago por un
servicio.** Un veredicto positivo del juez sobre esta candidata significaría "acá se paga bien por
soportar riesgo", no "acá hay dinero tirado".

Para este proyecto esa distinción tiene consecuencia directa: **una prima de riesgo con cola
izquierda es exactamente lo que mata una cuenta con drawdown trailing**, y el juez ya calcula
`P(pasar)` por la cadena de evaluación justamente porque *"una media positiva con cola izquierda
gorda fracasa igual"*.

El control de la tasa libre de riesgo apoya la explicación de prima: en días de anuncio los
inversores pagan por seguridad, lo que es la otra cara de exigir más por el riesgo.

## 7. CLASIFICACIÓN

**DETERMINISTA en la fecha, y el signo está fijado por el mecanismo.**

- **Fecha**: el calendario de publicaciones del Buró de Estadísticas Laborales, del Buró de Análisis
  Económico y de la Reserva Federal, publicado con un año de anticipación.
- **Signo**: siempre largo. No hay que estimarlo. **Es la única candidata del inventario donde el
  lado no se calcula: se sabe.**
- **Magnitud**: media de una distribución con cola. Estadística.

## 8. Estado de replicación

**Es la mejor replicada del inventario, y por lejos.**

- **Los mismos autores** la extienden en *Journal of Financial Economics* (2014), "Asset pricing: A
  tale of two days", donde el patrón de anuncios organiza el corte transversal completo, no sólo el
  índice.
- Generó una literatura entera sobre **la prima de anuncio macroeconómico**, con modelos teóricos que
  la derivan de preferencias (Ai y Bansal y sucesores). **Que exista teoría que la deriva y no sólo
  evidencia que la encuentra es una diferencia de categoría** frente a todo lo demás de esta carpeta.
- **Cincuenta y un años de muestra**, 1958-2009. Ninguna otra candidata se acerca.

**En contra:**
- La muestra termina en **2009**, o sea siete años antes de los datos del proyecto.
- **No encontré una replicación publicada específica sobre futuros ES para 2016-2019.**
- **El pariente cercano murió.** La deriva previa a la Fed de Lucca y Moench, que es una prima
  concentrada en un anuncio programado concreto, **desapareció después de 2015**
  (`DESCARTADAS.md`, 1.1). Que un miembro de la misma familia se haya extinguido justo antes del
  período de prueba **es la advertencia más concreta que tiene esta ficha**, y va escrita acá arriba
  y no al final.

## 9. Cuántas variantes probaron los autores

Contable: la definición de **qué anuncios cuentan** como importantes es la decisión principal, y son
tres familias (inflación, desempleo, tasas) elegidas entre las decenas que se publican. Más:
subperíodos a lo largo de cincuenta y un años, la tasa libre de riesgo como verificación, y en el
trabajo de 2014 el corte transversal completo.

**Para el juez: `variantes_probadas` = 30 como mínimo.**

**Atenuante, y acá es más fuerte que en cualquier otra ficha:** el resultado es una **predicción de
teoría de valoración de activos** — si los inversores tienen aversión al riesgo macroeconómico, tiene
que haber prima en los días en que ese riesgo se resuelve. El signo estaba predicho antes de mirar.
Y el control de la tasa libre de riesgo es una predicción adicional que también se cumplió.

## 10. Qué haría falta para probarla acá

**Datos de precio: NINGUNO NUEVO.** ES 1-min 2016-2019.

**Dato que falta y es gratis:** el calendario 2016-2019 de las publicaciones de índice de precios al
consumidor, situación del empleo y reuniones del comité de política monetaria. Están archivados y
publicados. **Medio día de trabajo.**

**Decisión de construcción que se declara antes:** cuáles anuncios cuentan. Los autores usan tres
familias; hay decenas de publicaciones. **Elegir el conjunto mirando el resultado sería exactamente
la trampa.** El conjunto se copia del paper y punto.

### La aritmética, antes de medir

| | |
|---|---|
| ventana de exposición | una sesión, cierre a cierre |
| ¿stop posible dentro de E? | **sí** |
| instrumento | ES o **MES** |
| A neto por evento, ES 2016-2019 | **$117** |
| eventos por año | ≈ 40 días de anuncio |
| eventos requeridos por año (F5, 10 variantes) | **75** |
| **falta** | **1,9×** |

**Es la que menos lejos queda de todo el inventario.** Y sigue quedando corta por casi el doble.

### Sobre el riesgo, y acá pesa más que en L10

La posición se sostiene de un cierre al siguiente, y **el día en cuestión es justamente el día en que
está programado que salga una noticia capaz de mover el mercado**. La cola no es una molestia
estadística: es el mecanismo. Con **1 ES** contra 40 puntos de drawdown eso es exactamente el
escenario que la Compuerta 1 midió como letal.

**Con 1 MES son 400 puntos y la ventaja baja a $12 por evento.** Ese intercambio es peor que el de
L10, porque la ventaja de partida es menor.

**Dicho claro: de las dos recuperadas, ésta tiene la mejor evidencia y el peor riesgo.** La otra
tiene la mejor magnitud y la peor evidencia. **No las ordeno entre sí. Ordenarlas por promesa es
seleccionar.**
