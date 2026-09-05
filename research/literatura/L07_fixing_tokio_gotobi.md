# L07 — El fixing de Tokio de las 9:55: el precio sube antes y vuelve después, todos los días a la misma hora

**VENTANA L. Ficha de literatura. NO MEDIDA. No gasta cartucho, K sigue en 261.**

> **DESACTUALIZADA en un punto:** esta ficha dice grado **A−**. Tras corregir la contaminación de mirada hacia adelante, **es grado B**. Ver [F7](F7_EDAD_DE_LA_EVIDENCIA.md) y [A02](A02_pasada_de_coherencia.md).

Ésta es la candidata con la **hora escrita más precisa** de todo el lote: no es un día del mes ni una
ventana de media hora, es un minuto fijo de todas las ruedas.

---

## 1. Cita completa

Ito, Takatoshi; Yamada, Masahiro (2017). **"Puzzles in the Forex Tokyo 'Fixing': Order Imbalances and
Biased Pricing by Banks."** *Journal of International Economics*, vol. 109, pp. 214–234.

Circuló como **NBER Working Paper 22820**, noviembre de 2016.

- NBER: https://www.nber.org/papers/w22820
- PDF: https://www.nber.org/system/files/working_papers/w22820/w22820.pdf
- SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2868918
- Columbia WP 352: https://business.columbia.edu/sites/default/files-efs/imce-uploads/Research/Research_Papers/WP_352.Ito-Yamada.Tokyo_Fixing_Puzzles.pdf

**Antecedente del mismo par de autores:** "Was the Forex Fixing Fixed?", NBER WP 21518 (2015).

## 2. El efecto, en una frase

Todos los días a las 9:55 de la mañana en Tokio, los bancos japoneses fijan el tipo de cambio al que
le van a vender dólares a sus clientes; el precio **sube en los minutos previos y baja en los
posteriores**, porque los bancos se adelantan a una demanda de dólares que ya saben que existe.

## 3. Instrumento y período de la muestra original

- **USD/JPY** principalmente, y también EUR/JPY y EUR/USD.
- Datos de **ICAP EBS**: nivel 5 de **enero de 2006 a diciembre de 2013**, nivel 2 de **enero de
  1999 a diciembre de 2005**. Más las tasas de fixing publicadas por BTMU (desde 1999) y Mizuho
  (desde 2002).
- El instrumento operable para Roberto sería el **futuro del yen (6J)** del CME: 12.500.000 yenes,
  unos **$115.000** de nocional con el yen a 108.

## 4. Magnitud declarada

El patrón, en palabras de los autores: el precio **sube ligeramente de 9:53 a 9:55**, hace un **pico
de varios puntos básicos en pocos segundos** justo en el fixing, y **baja de 9:55 a 9:57**.

**El paper no publica una tabla de "gane X pips operando esto".** Lo que publica es:

- El pico es de **varios puntos básicos en pocos segundos**, y vuelve a su lugar en los segundos
  siguientes.
- Antes de 2008, los precios de fixing que fijaban los bancos estaban **sesgados hacia arriba y por
  encima del precio más alto transado** durante la ventana del fixing.
- Aun después de 2008, los precios de fixing anunciados siguen **por encima de la mediana** de los
  precios transados en la ventana, lo que implica **ganancia predecible para los bancos**.
- La correlación de retornos alrededor del fixing es **negativa para todos los pares**, pero **no
  para intervalos de más de un minuto**.

### MAGNITUD CERRADA — 2026-09-05

**El bloqueo se levantó. El paper SÍ publica la magnitud, y publica además una estrategia operable
completa que yo no había encontrado.** Sección 5.2, discusión de la Figura 6:

> calculamos el retorno medio de la inversión que consiste en **mantener USD/JPY largo durante cinco
> minutos y después corto durante los cinco minutos siguientes**. […] Durante 15 años de esta
> estrategia simple, si el momento del cambio es el instante del fixing de Tokio (00:55 GMT), **el
> retorno medio resulta 1,8 puntos básicos**. Este retorno está **apenas por encima del costo de
> transacción del diferencial de compra y venta**. […] este retorno anormal es muy distinto del de
> cualquier otro momento del día. **El 1 % superior e inferior de los retornos está truncado, y los
> resultados no están impulsados por valores atípicos.** Y, como ya examinamos, hay mucha liquidez
> disponible en ese momento. **La falta de liquidez no explica este retorno.**

| | |
|---|---|
| **regla publicada** | **largo cinco minutos, corto los cinco siguientes, cambio en el fixing** |
| **magnitud** | **1,8 puntos básicos** |
| ventana total | **10 minutos**, de 00:50 a 01:00 GMT |
| muestra | 15 años |
| tratamiento de atípicos | 1 % superior e inferior truncados |

**Y la condición de calendario, en el mismo párrafo:** *"el retorno se vuelve particularmente alto
los días 5 y 10 —excepto los cercanos al fin de mes— y el día 31 o el fin de mes."*

### Traducción a dólares por evento por contrato 6J

1,8 puntos básicos sobre $115.000 de nocional: **≈ $21 por evento.**

**Muy por debajo de lo que yo había estimado.** Mi lectura de "varios puntos básicos" como 4 daba
$46; el número publicado es menos de la mitad. **La estimación que marqué como mía estaba mal por un
factor de dos, y en la dirección que me favorecía.**

## 5. Antes o después de costos — y acá se decide todo

**Los propios autores lo dicen: el retorno de 1,8 pb está "apenas por encima del costo de transacción
del diferencial de compra y venta".**

**Eso mata la versión operable y hay que decirlo sin adornos.** Con $21 brutos por evento y un costo
que se lleva la mayor parte, L07 **no supera ningún piso de rentabilidad de este proyecto**. No es
una candidata para operar.

**Pero para PROBAR es otra cosa completamente distinta, y es lo más interesante de esta ficha.**

Un efecto de 1,8 pb sobre una ventana de diez minutos tiene una razón señal-ruido **muy alta por
evento**, porque el desvío de USD/JPY en diez minutos es del orden de 4 a 6 puntos básicos. Es el
perfil clásico de un efecto de microestructura: **enorme estadísticamente y despreciable
económicamente.**

**Es el ejemplo más puro del principio que ya apareció con L08: las peores para operar son las
mejores para entender.**

### Consecuencia para la prueba agrupada

**L07 NO debe entrar a la prueba agrupada, y el motivo es que entraría demasiado fuerte.**

Con `m = 1,8 pb` y un desvío de diez minutos de 4,6 a 8 pb, su señal por evento queda entre 0,22 y
0,39, contra 0,19 de L11 y 0,28 de L10. Y ocurre **todos los días**, no doce veces al año.

| escenario | contribución de L07 | contribución de L11 + L10 |
|---|---|---|
| σ = 4,6 pb, 1.000 eventos | ≈ 152 | 10,2 |
| σ = 8 pb, 1.000 eventos | ≈ 51 | 10,2 |

**En los dos casos L07 aporta entre cinco y quince veces más que las otras dos juntas.** La prueba
agrupada dejaría de ser una prueba sobre "las reglas de calendario de terceros" y pasaría a ser una
prueba sobre L07, y el control de dejar-una-afuera de `P01` lo detectaría de inmediato.

**Lo correcto no es meterla en el grupo: es correrla sola.** Ver `P05`.

## 5-bis. Lo que el paper regala, y lo que esconde

**Dos controles regalados.** El paper publica dos afirmaciones que funcionan como controles con
condición de falla, y quien mida esto no las tiene que inventar:

1. **Placebo de hora.** *"Este retorno anormal es muy distinto del de cualquier otro momento del
   día."* → Repetir la regla cambiando de largo a corto en otras horas **tiene que dar
   aproximadamente cero**. Si da lo mismo, lo que se mide es el método y no el fijación.
2. **Descarte de la liquidez.** *"Hay mucha liquidez disponible en este momento. La falta de liquidez
   no explica este retorno."* → Si el efecto vive sólo en los días de volumen más bajo, es un
   artefacto de horario delgado y contradice al paper.

Los dos están escritos como controles en [P05](P05_L07_sola.md).

**Y una trampa de tabla, que hay que dejar señalada donde alguien la va a buscar.**

**La Tabla 5 trae coeficientes de calendario grandes y significativos al 1 % para los días 5 y 10 y
para el fin de mes** —del orden de 0,046 a 0,101 según el banco y la especificación—. **Es la tabla
equivocada.**

Su variable dependiente es **la brecha entre el precio de fijación que anuncia el banco y el precio
de mercado**, o sea **el margen que el banco se cobra**. No es el movimiento del precio de mercado,
que es lo que se puede operar.

| lo que está tabulado con números | lo que sólo está descrito |
|---|---|
| el efecto *gotobi* sobre **la ganancia del banco** | el efecto *gotobi* sobre **el precio de mercado** |

**Quien busque la magnitud del efecto de calendario va a encontrar la Tabla 5 primero, y son
coeficientes de otra cosa.** El único número publicado para el movimiento de precio es el **1,8 pb**
de la sección 5.2, y es un promedio de **todos los días**, no de los *gotobi*.

## 6. Mecanismo declarado

**Desbalance de órdenes de clientes, estructural y predecible en su signo.**

Los importadores japoneses tienen que pagar a sus proveedores en dólares, y liquidan al precio del
fixing. Eso hace que **las órdenes de clientes estén sesgadas hacia la compra de moneda extranjera**,
y que ese sesgo **sea predecible** — es el hallazgo (2) del resumen del paper.

Los bancos, que tienen que entregar dólares al precio del fixing sin importar a qué precio los
consiguieron, tienen dos motivos para comprar antes de las 9:55:

1. **Defensivo**: cubrirse del desbalance de sus propios clientes, que conocen antes que el mercado.
2. **Ofensivo**: adelantarse (front-running) para que el precio de fixing quede por encima de su
   precio de inventario, que es de donde sale su margen.

Los autores lo enmarcan como **comercio predatorio** (Brunnermeier y Pedersen 2005) contra clientes
cautivos: en la ventana del fixing de Tokio los clientes minoristas no pueden irse a otro lado. Y
señalan que Londres previene esa posibilidad tomando la **mediana** de las transacciones de la
ventana en vez de un precio fijado por el banco.

### El calendario, que es lo que hace valiosa a esta ficha

El hallazgo (5) del resumen es que **los efectos de calendario también importan** para la
determinación del precio del fixing. Los autores usan variables de calendario para:

- **Los días 5 y 10** del mes (y por extensión 15, 20, 25 y fin de mes): los llamados días
  **"gotobi"**, cuando en Japón se concentran los vencimientos de pagos corporativos. El paper dice
  que la situación se hace más evidente **cuando hay grandes montos de pagos por vencer, típicamente
  los días 5, 10, 15, 20, 25 y fin de mes**.
- **Los viernes.**
- **El último día hábil del mes.**

**Eso es una regla escrita con fecha, y del tipo que el encargo pide preferir**: no es un patrón
estadístico, es una costumbre de pago del comercio japonés que cae en fechas fijas del calendario.

## 7. CLASIFICACIÓN

**DETERMINISTA en la fecha y la hora, ESTADÍSTICA en la magnitud.**

- El **cuándo** no se descubre buscando: 9:55 JST, y los días 5/10/15/20/25/fin de mes. Se lee en un
  calendario y en una costumbre contable.
- El **cuánto** es una distribución con cola, y el signo es tendencia, no garantía.

De todo el lote, **es la que más se acerca a lo que el encargo llama "regla escrita con fecha"**,
junto con L04 y L08.

## 8. Estado de replicación

- **Ito y Yamada replican su propio hallazgo en dos regímenes**: antes y después de 2008. El sesgo
  se **reduce** después de 2008 (los precios de fixing pasan de estar arriba del **máximo** transado
  a estar arriba de la **mediana**) pero **no desaparece**. Esa atenuación con reforma parcial es un
  dato de decaimiento medido, no supuesto.
- El escándalo de manipulación de fixings salió a la luz en **2013** y trajo multas y acuerdos. **La
  muestra del paper termina en diciembre de 2013**, o sea justo antes de que el mercado reaccionara.
- La reforma de WM/Reuters de **febrero de 2015** (ventana de cinco minutos en vez de un minuto)
  aplica al **fixing de Londres**, no al de Tokio. El de Tokio siguió siendo un precio fijado por
  cada banco.
- **No encontré una replicación publicada del fixing de Tokio para 2016-2019.** Es un hueco real: es
  exactamente el período de los datos del proyecto, y es enteramente posterior al escándalo.

**Evidencia adyacente en el fixing de Londres:** Evans (2014) documenta la autocorrelación negativa
del tipo de cambio entre el período previo y el posterior al fixing, **particularmente el último día
hábil del mes**, y dice que se observa en todos los períodos y todos los pares. Es el mismo patrón
en el otro fixing, y es la puerta de entrada a **L08**.

## 9. Cuántas variantes probaron los autores

**Muchas, y el paper es transparente al respecto porque su objetivo no era encontrar una estrategia.**
Contable: 3 pares de divisas × 2 regímenes temporales (pre y post 2008) × varias definiciones de
"pico" y de "reversión" × un conjunto de variables de calendario (día 5, día 10, viernes, fin de mes)
× regresiones con volatilidad, desbalance de órdenes, spread, profundidad, conteo de cotizaciones y
VWAP como controles.

**Para el juez: `variantes_probadas` = 100.** Un paper que corre un panel con cuatro variables de
calendario y seis controles sobre tres pares probó del orden de cien especificaciones, aunque
publique diez.

**Matiz honesto a favor:** este paper **no buscaba una anomalía operable**. Buscaba mostrar que los
bancos fijan precios sesgados. Cuando el objetivo declarado del autor no es la rentabilidad, la
presión de búsqueda hacia un resultado operable es menor. **No es una defensa que se pueda
verificar, pero es una diferencia real con un paper de anomalías.**

## 10. Qué haría falta para probarla acá

**Datos: NO LOS TENEMOS.** Hace falta **6J 1-min** (o USD/JPY spot) cubriendo las 9:53–9:57 JST de
2016-2019. Son las **00:53–00:57 GMT**, es decir **19:53–19:57 ET del día anterior** en horario
estándar: dentro de la sesión de Globex, sin cruzar ningún cierre diario.

**Costo: probablemente el más barato del lote.** La VENTANA G tiene el script de cotización sin
descarga (`databento_cotizar_spread.py`) y ya cotizó ES: un día de `tbbo` cuesta $0,79. 6J en barras
de un minuto debería ser una fracción de eso, y hay ~1.000 sesiones.

**Obstáculo del juez, y es el mismo que L06:** el campo `instrumento` acepta **sólo `ES` o `MES`**,
las únicas dos con comisión medida. **El juez no puede juzgar 6J.** Habría que medirle comisión y
deslizamiento primero.

### Lo que sí tiene a favor, y es mucho

**El número de eventos.** A diferencia de L03 (192 eventos) y L08 (48 eventos), esto ocurre **todos
los días**: ~250 por año, **~1.000 en 2016-2019**. Y la versión gotobi da ~72 por año, ~290 en total.

Con 1.000 operaciones la resolución del juez es ±74 % (`PISO_Y_CONVERSION.md`), la misma que L01 y
L02. **No es mejor en potencia. Es mejor en que la ventaja por evento declarada (~$46) es mayor que
la de L01/L02 (~$35) sobre un nocional más chico**, o sea que el efecto relativo es más grande.

**Orden correcto si alguna vez se toca:**
1. Abrir el paper y convertir "varios puntos básicos" en un número con su desvío.
2. Si sobrevive al costo de ida y vuelta en 6J, cotizar los datos.
3. Medir comisión y deslizamiento de 6J y extender el juez.
4. Declarar antes de correr si se prueba **todos los días** o **sólo los gotobi**. Probar los dos y
   quedarse con el mejor es la trampa que este proyecto ya conoce.
