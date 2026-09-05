# DESCARTADAS — lo que busqué, encontré, y no pasa los filtros

**VENTANA L. NO MEDIDO. No gasta cartucho, K sigue en 261.**

Este documento existe para que nadie las vuelva a traer. Cada entrada tiene **cuál filtro la mata**,
no una opinión. Varias son buenos papers y algunas son efectos probablemente reales: **están acá por
incompatibles con la forma de operar de Roberto, no por falsas.**

Los filtros:

- **F1** — ~~necesita mantener posición de un día para otro~~ **CORREGIDO Y REEMPLAZADO**
- **F1'** — **ventana de exposición sin freno**, definido en [FILTROS.md](FILTROS.md)
- **F2** — necesita muchos instrumentos a la vez
- **F3** — no declara mecanismo
- **F4** — magnitud declarada por debajo del piso
- **F5** — mínimo de eventos por año, con el umbral derivado en `FILTROS.md`

> ## AVISO — dos de este documento fueron RECUPERADAS
>
> El filtro F1 estaba mal escrito: preguntaba si la posición cruza el cierre del día, cuando lo que
> se quería evitar era la exposición **sin posibilidad de frenarla**. La Compuerta 1 cerró su rama
> porque la mecánica de ejecución **prohibía poner un stop**, no porque fuera de noche.
>
> Con el filtro corregido, **dos de las siete del Grupo 1 sobreviven y salieron de este documento**:
>
> - **1.4 Harvey, Mazzoleni y Melone** → ficha [L10](L10_rebalanceo_institucional_harvey.md)
> - **3.4 Savor y Wilson** → ficha [L11](L11_prima_dias_anuncio_savor_wilson.md)
>
> Sus entradas quedan abajo **tachadas**, con el motivo por el que salieron. Las otras cinco del
> Grupo 1 siguen descartadas, pero varias por un motivo distinto del que decía antes. La revisión
> completa de las siete está en `FILTROS.md`.

---

## Grupo 1 — Muere por F1' (exposición) o por otro filtro

**Era el grupo más grande y por eso se revisó el filtro. Cinco de siete siguen acá.**

### 1.1 La deriva previa al anuncio de la Fed

Lucca, David O.; Moench, Emanuel (2015). "The Pre-FOMC Announcement Drift." *The Journal of
Finance*, vol. 70, n.º 4. https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12196

**El efecto:** de septiembre de 1994 a marzo de 2011, el retorno sube en promedio **49 puntos
básicos en las 24 horas previas** a los anuncios programados del comité de política monetaria, lo
que explica alrededor del **80 % del retorno anual**. Otras versiones lo cifran en **27,1 pb** de
deriva media contra menos de 2 pb en la misma ventana de días normales.

**Mata F1, y de la peor manera:** la ventana **es** de 24 horas, de las 14:00 del día anterior a las
14:00 del día del anuncio. No hay versión intradiaria: el efecto **es** el traslado nocturno.

**Y además está muerto.** "The disappearing pre-FOMC announcement drift", *Finance Research Letters*
(2021), https://www.sciencedirect.com/science/article/abs/pii/S1544612320315956 — extendiendo la
muestra a diciembre de 2019, la deriva **desapareció esencialmente después de 2015**, tanto en los
anuncios con conferencia de prensa como en los que no. Ver también "The pre-FOMC announcement drift:
short-lived or long-lasting?" (*Applied Economics*, 2024).

**Doble motivo. No volver.**

### 1.2 El ciclo de las subastas del Tesoro

Lou, Dong; Yan, Hongjun; Zhang, Jinfan (2013). "Anticipated and Repeated Shocks in Liquid Markets."
*The Review of Financial Studies*, vol. 26, n.º 8, pp. 1891–1912.
https://academic.oup.com/rfs/article-abstract/26/8/1891/1589893

**El efecto:** los precios de los bonos del Tesoro **caen en los días previos a una subasta y se
recuperan poco después**, aunque la fecha y el monto se anuncian con anticipación. Costo oculto de
emisión estimado en **9 a 18 puntos básicos** del tamaño de la subasta, más de medio billón de
dólares para el volumen de 2007. Mecanismo declarado: capacidad limitada de los intermediarios para
tomar riesgo, más movilidad imperfecta del capital de los inversores finales.

**Mata F1:** el efecto se despliega sobre **varios días** alrededor de la subasta.

**Vale anotarlo igual porque la forma es ejemplar:** fecha publicada de antemano, mecanismo nombrado,
magnitud medida. Es exactamente el tipo de candidata que el encargo pide, y muere sólo por el
horizonte.

### 1.3 Adelantarse al roll de los índices de materias primas ("Goldman roll")

Mou, Yiqun (2010/2011). "Limits to Arbitrage and Commodity Index Investment: Front-Running the
Goldman Roll." Tesis doctoral, Columbia University.
https://academiccommons.columbia.edu/doi/10.7916/D8H41ZDD

**El efecto:** los índices de materias primas rollean sus posiciones en los **días hábiles 5 a 9 de
cada mes**, según una regla publicada. El impacto de precio de esa actividad es estadística y
económicamente significativo. Estrategias que lo explotan dieron **Sharpe anual de hasta 4,4** entre
enero de 2000 y marzo de 2010, y estima que se ganaron hasta **$26 mil millones** con ese arbitraje
entre 2000 y 2009.

**Mata F1:** la posición se sostiene a lo largo de la ventana de roll, varios días.

**Y tiene decaimiento declarado por el propio autor:** la rentabilidad **decrece con el capital de
arbitraje empleado** y crece con el tamaño de los fondos indexados relativo al mercado. Un Sharpe de
4,4 publicado en una tesis de 2010 y trece años de arbitraje después no es un Sharpe de 4,4.

### ~~1.4~~ RECUPERADA — El rebalanceo institucional de fin de mes y de trimestre

> **SALIÓ DE ESTE DOCUMENTO.** Ficha completa en [L10](L10_rebalanceo_institucional_harvey.md).
> Su ventana de exposición son ~23 horas y **admite un stop**, así que no muere por F1'. Con la
> palanca del MES —400 puntos de drawdown contra 40— la exposición nocturna deja de ser el problema
> que cerró la Compuerta 1. **Es la de mayor magnitud declarada sobre futuros ES del inventario.**

Lo que decía la entrada original, que sigue siendo correcto:

Harvey, Campbell R.; Mazzoleni, Michele G.; Melone, Alessandro (2025). "The Unintended Consequences
of Rebalancing." NBER Working Paper 33554.
https://www.nber.org/system/files/working_papers/w33554/revisions/w33554.rev0.pdf

**El efecto:** cuando las acciones quedan sobreponderadas contra el objetivo, los fondos venden
acciones y compran bonos, y eso **baja el retorno de las acciones 17 puntos básicos al día
siguiente** (4 pb de suba en bonos). Usan **futuros del S&P 500 y del bono a 10 años, 1997–2023**.
La predictibilidad de calendario **es fuerte a fin de mes y ausente fuera de esos días**, y aumenta
hacia el fin de trimestre. Costo estimado para los inversores: **$16 mil millones al año**, unos
$200 por hogar estadounidense.

**Mata F1:** la ventana es el retorno del **día siguiente**, cierre a cierre. Incluye la noche.

**Es la descartada que más duele**, y por eso la anoto con detalle: instrumento exacto (ES y ZN),
calendario escrito, mecanismo mecánico, 17 pb ≈ **$221 por contrato ES** en 2016-2019 — muy por
encima de cualquier piso. **Sólo el horizonte la mata.**

**Advertencia contra el arreglo obvio:** restringirla a 9:30–16:00 del día siguiente para que sea
intradiaria **es cambiar la regla del paper**, y una regla cambiada por nosotros para que entre en
nuestras restricciones **vuelve a ser una hipótesis de nuestro generador**. Si alguien la mide así,
ese es el hallazgo que hay que declarar, y `variantes_probadas` tiene que reflejarlo.

### 1.5 El retorno predecible del Tesoro a fin de mes

Hartley, Jonathan; Schwarz, Krista (2019). "Predictable End-of-Month Treasury Returns."
SSRN 3440417. https://www.kristaschwarz.com/EOM.pdf

**El efecto:** los retornos en exceso de los bonos del Tesoro con cupón son positivos y altamente
significativos **en los últimos días del mes** y no se distinguen de cero el resto del tiempo. Una
posición larga sólo esos días da un **Sharpe anualizado de alrededor de 1**. En el bono a 10 años,
**~25 pb por mes**. Muestra **1990–2018**. Mecanismo: picos temporales de demanda por maquillaje de
carteras y rebalanceo contra índices de referencia, con evidencia en cantidades de que las
**aseguradoras de vida** son grandes compradoras netas en las fechas de rebalanceo de los índices.
Reportan efecto también en **futuros** del Tesoro y en swaps, y que el spread típico fuera de
emisión (2 a 3 pb) es un orden de magnitud menor que el efecto.

**Mata F1:** son "los últimos días del mes", varios días de tenencia.

### 1.6 El ciclo mensual de necesidades de caja institucionales

Etula, Erkko; Rinne, Kalle; Suominen, Matti; Vaittinen, Lauri (2020). "Dash for Cash: Monthly Market
Impact of Institutional Liquidity Needs." *The Review of Financial Studies*, vol. 33, n.º 1,
pp. 75–111. https://academic.oup.com/rfs/article/33/1/75/5494694

**El efecto:** el ciclo mensual de pagos induce patrones sistemáticos en mercados líquidos de todo el
mundo, con aumentos temporales del costo del capital de deuda y de acciones en las fechas clave
asociadas a las necesidades de caja de fin de mes.

**Mata F1:** patrón de varios días alrededor del cambio de mes.

### 1.7 La deriva nocturna del propio E-mini

Boyarchenko, Nina; Larsen, Lars Christian; Whelan, Paul (2023). "The Overnight Drift." *The Review of
Financial Studies*, vol. 36, n.º 9, pp. 3502–3547.
NY Fed Staff Report 917: https://www.newyorkfed.org/research/staff_reports/sr917

**El efecto:** casi el **100 % de la prima de riesgo accionaria** estadounidense se gana en la
ventana de **2:00 a 3:00 de la mañana hora del este**, la apertura de los mercados europeos. En los
futuros del E-mini S&P 500, entre 1998 y 2020, esa hora dio **~3,7 % anual**, más del 60 % del
retorno anual del contrato. Mecanismo: los proveedores de liquidez absorben el desbalance de órdenes
del cierre a descuento y lo liberan cuando llegan los compradores europeos.

**Técnicamente NO mata F1**: entrar a las 2:00 y salir a las 3:00 es dentro de una misma sesión de
Globex, sin cruzar ningún cierre diario. **Mata F4**: 3,7 % anual son **≈ $19 por sesión** por
contrato ES a nocional 2016-2019, por debajo de todo piso y sin cubrir el costo de una ida y vuelta.

**Y está muerto, dicho por los mismos autores.** "The Disappearing Overnight Drift", Liberty Street
Economics, julio de 2026, https://libertystreeteconomics.newyorkfed.org/2026/07/the-disappearing-overnight-drift/
y SSRN 7035838. El patrón **se desvaneció después de 2021**: de enero a diciembre de 2025 la ventana
de 2:00 a 3:00 promedió cerca de cero. Lo atribuyen **exclusivamente** a la compresión de los
desbalances de órdenes del cierre: la dispersión del volumen firmado relativo de fin de día cayó de
**6,5 % a 2,9 %**, más de la mitad. La volatilidad y la liquidez nocturna no cambiaron.

**El dato que cierra la historia:** dos ETF (NSPY y NIWM) creados en junio de 2022 justamente para
capturar esta deriva **cerraron catorce meses después**.

**Es la entrada más valiosa de este documento** y la explico en el reporte: un efecto publicado en
una revista de primera línea, con mecanismo medido, que valía más del 60 % del retorno anual del
contrato, **murió entre la escritura y la publicación**, y los propios autores lo documentaron.

---

## Grupo 2 — Muere por F2 (muchos instrumentos)

### 2.1 La reversión de fin de día en el corte transversal

Baltussen, Guido; Da, Zhi; Soebhag, Amar (2024). "End-of-Day Reversal." SSRN 5039009, 17 de
diciembre de 2024. https://academicweb.nd.edu/~zda/EOD.pdf

**El efecto:** las acciones individuales revierten fuerte en los **últimos 30 minutos** de la rueda;
las que cayeron durante el día rebotan. Es distinto del momento intradiario de mercado y viene
sobre todo de presión compradora sobre las perdedoras del día. Mecanismos propuestos: compras
minoristas inducidas por atención y gestión de riesgo de los vendedores en corto al final del día.
**No lo explican ni la liquidez ni la cobertura de gamma.**

**Mata F2:** es un efecto **de corte transversal** entre acciones. Necesita una cartera larga-corta
de muchos papeles. No hay versión de un instrumento.

**Anotar el contraste, que es informativo:** en el índice hay **momento** en la última media hora
(L01, L02); en las acciones individuales hay **reversión** en la misma ventana, con mecanismos
distintos. Las dos cosas conviven porque son objetos distintos.

### 2.2 La reversión intradiaria del retorno nocturno

Berkman, Henk; Koch, Paul D.; Tuttle, Laura A.; Zhang, Ying (2012). "Paying Attention: Overnight
Returns and the Hidden Cost of Buying at the Open." *Journal of Financial and Quantitative Analysis*,
vol. 47, n.º 4, pp. 715–741.

**El efecto:** retornos positivos en el período nocturno seguidos de **reversión durante la rueda**,
por un precio de apertura alto respecto de los precios intradiarios. Concentrado en acciones que
atrajeron atención de inversores minoristas, más pronunciado en las difíciles de valuar y costosas
de arbitrar.

**Mata F2:** corte transversal de acciones, condicionado por atención minorista por papel.

### 2.3 Flujos de rebalanceo de ETF apalancados y opciones sobre acciones

Barbon, Beckmeyer, Buraschi y Moerke (2022), SFI Research Paper 22-40. **Mata F2** por sí solo
(acciones individuales), pero **el mecanismo agregado sí sirve** y está en la ficha **L04**.

---

## Grupo 3 — Muere por F4 (magnitud) o por no tener signo predecible

### 3.1 El salto del VIX en su liquidación

Griffin, John M.; Shams, Amin (2018). "Manipulation in the VIX?" *The Review of Financial Studies*,
vol. 31, n.º 4, pp. 1377–1417. https://academic.oup.com/rfs/article-abstract/31/4/1377/4060543

**El efecto:** en el momento de la liquidación del VIX el volumen se dispara en opciones SPX fuera
del dinero —justo las que entran en el cálculo del índice— y **el VIX salta 31 puntos básicos en
promedio** con las medidas más conservadoras. Las pruebas son inconsistentes con cobertura y con
comercio de liquidez coordinado, y consistentes con manipulación.

**Descartada por dos motivos independientes:**
1. **No tiene signo predecible.** La manipulación empuja el VIX hacia arriba o hacia abajo según de
   qué lado esté posicionado el manipulador, y eso no se sabe antes.
2. **Necesita opciones SPX de muchos strikes** para operarlo directamente: F2.

### 3.2 El efecto del día previo a feriado

Ariel, Robert A. (1990). "High Stock Returns before Holidays: Existence and Evidence on Possible
Causes." *The Journal of Finance*, vol. 45, n.º 5.
https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.1990.tb03731.x

**El efecto original:** los retornos medios de los índices estadounidenses en los días previos a
feriado son **9 a 14 veces más altos**; más de un tercio del retorno total del período 1963–1982 se
ganó en los **ocho días** por año previos a cierres por feriado.

**Descartada por replicación fallida, que es el motivo más fuerte de todos:**
Ko y Welch (2021), "The Pre-Holiday Premium of Ariel (1990) Has Largely Become A Small-Firm Effect
Out of Sample", *Critical Finance Review*.
https://cfr.ivo-welch.info/published/papers/ko2021pre.pdf
Extendiendo a **1983–2019**, el efecto **existe sólo entre empresas chicas**; para las grandes la
diferencia entre días previos a feriado y el resto **es insignificante, y especialmente después de
1990**. Ver también "Pre-holiday effects: International evidence on the decline and reversal of a
stock market anomaly", *Journal of International Money and Finance*.

**El S&P 500 es el índice de las empresas grandes. El efecto está muerto justo donde Roberto opera.**

### 3.3 Los efectos del día de vencimiento trimestral

Stoll, Hans R.; Whaley, Robert E. (1987, 1990, 1991, 1997) y trabajos derivados.

**El efecto:** presión de precio anormal cuando vencen simultáneamente futuros de índice, opciones
de índice y opciones sobre futuros. Después de que en 1987 la liquidación pasó al **precio de
apertura del viernes**, los efectos se mudaron a la apertura del viernes.

**Descartada por F4, con la cita de los propios autores:** la actividad de negociación y las
reversiones de precio **no parecen haber cambiado en sentido estadístico desde junio de 1987, ni son
grandes en términos absolutos**. Cuando los descubridores de un efecto dicen que no es grande, no
hace falta medirlo.

**Motivo secundario:** son **4 eventos por año**, 16 en 2016-2019. No medible por acumulación.

### ~~3.4~~ RECUPERADA — La prima de los días de anuncio macro

> **SALIÓ DE ESTE DOCUMENTO.** Ficha completa en [L11](L11_prima_dias_anuncio_savor_wilson.md).
> Su ventana de exposición es una sesión y **admite un stop**, así que no muere por F1'. **Es la
> candidata que menos lejos queda de ser medible con los datos que hay**, corta por un factor de
> 1,9 en eventos. Advertencia que va con ella: su pariente cercano, la deriva previa a la Fed de
> la entrada 1.1, **murió después de 2015**.

Lo que decía la entrada original, que sigue siendo correcto:

Savor, Pavel; Wilson, Mungo (2013). "How Much Do Investors Care About Macroeconomic Risk? Evidence
from Scheduled Economic Announcements." *Journal of Financial and Quantitative Analysis*, vol. 48,
n.º 2, pp. 343–375.

**El efecto:** el retorno en exceso medio en días de anuncio programado es de **11,4 puntos
básicos** contra **1,1 pb** en los demás días, 1958–2009, lo que implica que **más del 60 % de la
prima de riesgo accionaria anual acumulada se gana en días de anuncio**. La razón de Sharpe es diez
veces mayor.

**Mata F1:** el retorno medido es el del **día** completo, cierre a cierre. Restringirlo a
9:30–16:00 es cambiar la regla (misma advertencia que en 1.4).

**Anotar la magnitud igual, porque es grande:** 11,4 pb ≈ **$148 por contrato ES** en 2016-2019, con
~40 días de anuncio por año. Si alguien alguna vez decide que una regla intradiaria derivada vale la
pena, **esta es la de mayor magnitud declarada de todo lo que encontré.**

---

## Grupo 4 — Descartadas por acceso al mercado, no por el efecto

### 4.1 Momento intradiario en bonos del Tesoro chinos

Zhang, Wei; Wang, Pengfei; Li, Yi (2021). "Bond intraday momentum." *Journal of Behavioral and
Experimental Finance*, vol. 31. DOI 10.1016/j.jbef.2021.100515

**El efecto:** en los futuros de bonos del Tesoro **chinos**, el retorno de los primeros quince
minutos predice el de los últimos quince. Más fuerte en días de bajo volumen, alta volatilidad,
primer cuarto de hora positivo y sin publicación de noticias antes.

**Descartada:** mercado chino, sin acceso práctico. Y el corte "sin noticias previas" es una
condición elegida entre varias.

### 4.2 Momento intradiario en Asia-Pacífico

Limkriangkrai, Manapon; Chai, Daniel; Zheng, Gaoping (2023). "Market intraday momentum: APAC
evidence." *Pacific-Basin Finance Journal*, vol. 80, 102086. Acceso abierto.

**No es una candidata: es evidencia de replicación**, y la uso como tal en L01 y L02. Reporta que el
efecto está en China y Japón, es débil en Corea del Sur y **no está en Hong Kong ni en Singapur**.

---

## Grupo 5 — Lo que NO es literatura académica y no entra

Durante la búsqueda aparecieron varios textos con forma de paper que **no son revisados por pares** y
que reproducen exactamente el problema que esta ventana existe para evitar: un autor solo, buscando
en datos, publicando lo que encontró.

El ejemplo claro: **Mesfin, Mathias (2026), "Structural Limits of OHLCV-Based Intraday Signals in
MNQ Futures: A Systematic Falsification Study", arXiv:2605.04004.** Evalúa **catorce familias de
señales** sobre **947 ruedas de datos de cinco minutos de 2021–2025** en el micro Nasdaq, con
criterios de t ≥ 2,0, al menos 30 operaciones y consistencia entre años. **Ninguna de las catorce
familias cumple todos los criterios.** El retorno bruto antes de costos va de 0,07 a 1,50 puntos por
operación, por debajo del costo de fricción supuesto de dos puntos de ida y vuelta.

**No le hago ficha, por dos motivos, y el segundo importa más que el primero:**
1. No está revisado por pares.
2. **Es el mismo generador que este proyecto.** Un individuo probando catorce familias de señales
   sobre OHLCV es exactamente la muestra tomada 261 veces, tomada una vez más. Que dé negativo no es
   información sobre el mercado.

**Lo dejo anotado igualmente, porque su resultado negativo es consistente con el diagnóstico del
proyecto y porque alguien lo va a encontrar buscando y va a querer traerlo.**
