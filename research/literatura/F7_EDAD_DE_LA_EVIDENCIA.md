# F7 — ¿EL EFECTO TODAVÍA EXISTE?

**VENTANA L. NO MEDIDO. No gasta cartucho, K sigue en 261.**

Los seis filtros anteriores preguntan si **podemos medir** una candidata. Ninguno pregunta si **sigue
existiendo**. Este documento agrega esa dimensión y la aplica a las once.

El caso que obliga a tenerlo: la deriva nocturna del E-mini valía más del 60 % del retorno anual del
contrato, se publicó en el *Review of Financial Studies* en 2023 con el mecanismo medido, y **ya
estaba muerta cuando se publicó**. Los propios autores lo documentaron en 2026. Ningún filtro de
magnitud, de eventos ni de exposición la habría detenido.

---

> # CORRECCIÓN — 2026-09-05: la confirmación no puede superponerse con el período de prueba
>
> **Este filtro tenía una contaminación de mirada hacia adelante, y la introduje yo.**
>
> Calificaba con grado A a las candidatas con confirmación posterior de terceros. **Pero varias de
> esas confirmaciones tienen muestras que CUBREN 2016-2019, que es donde queremos probar.** El grado
> A de L11 venía de que Ai, Bansal y Guo extendieron a 2023, y 2016-2019 está adentro de 2023.
>
> **Elegíamos la candidata número uno usando evidencia que cubre el período de prueba.**
>
> ## La regla corregida
>
> **La evidencia posterior cuenta como confirmación SÓLO si su muestra NO se superpone con
> 2016-2019. Si se superpone, no es confirmación independiente: es la misma búsqueda extendida.**
>
> **Y si la no superposición no se puede verificar, no se otorga el grado.** La carga está del lado
> de la confirmación, igual que con cualquier otro número que no se puede verificar en esta carpeta.
>
> ## Una asimetría que agrego, porque la regla simétrica sería un error
>
> **La superposición descalifica la confirmación POSITIVA, no la refutación NEGATIVA.**
>
> El daño que la regla evita es que elijamos una candidata porque alguien encontró que funciona en
> nuestro período. Si en cambio alguien encontró que **no** funciona ahí, no hay mirada hacia
> adelante favorable: hay información desfavorable que estaríamos ignorando. **Descontarla sería
> proteger a la candidata del dato malo.**
>
> Por eso la replicación fallida de Rosa sobre L02 **sigue contando**, aunque su período fuera de
> muestra se superponga con el nuestro.
>
> ## Resultado
>
> **NINGUNA de las once conserva grado A.** Ver la sección *Aplicación de la corrección*.

## La escala, y qué gatilla cada grado

| grado | significa | qué hace |
|---|---|---|
| **A — CONFIRMADA** | hay evidencia posterior a la publicación, de terceros, sobre datos nuevos | nada |
| **B — SIN EVIDENCIA POSTERIOR** | busqué y no hay | **riesgo declarado**, con esas palabras, en su ficha |
| **C — DEBILITADA O DISPUTADA** | alguien reportó que se achicó, o hay evidencia en contra | baja de posición |
| **D — MUERTA** | confirmada extinta | va a `DESCARTADAS.md` |

**Un grado B no descarta.** Es una etiqueta. Ninguna de las once quedó en D: las que están en D ya
salieron del inventario.

---

## Las once, una por una

### L11 — Prima de días de anuncio · **GRADO A**

| | |
|---|---|
| datos del paper original | hasta **2009** |
| evidencia posterior | **sí, de terceros, con datos hasta 2023** |
| ¿se debilitó? | **no, se fortaleció** |
| ¿dijeron algo los autores después? | sí, lo extendieron ellos mismos en *JFE* 2014 |

**Ai, Hengjie; Bansal, Ravi; Guo, Hongye. "Macroeconomic Announcement Premium."** NBER Working Paper
31923. https://www.nber.org/system/files/working_papers/w31923/w31923.pdf

Extienden la muestra a **1961-2023** y encuentran que unos **44 días de anuncio por año** cargan
**más del 71 %** de la compensación agregada por riesgo del mercado accionario. La cifra original de
Savor y Wilson era 60 % sobre 1958-2009. Y en el subperíodo **1997-2014** la prima explica
**prácticamente el 100 %** del premio accionario.

**Es la única candidata del inventario con confirmación independiente sobre datos que llegan hasta
2023.** También es la única con una literatura teórica que la deriva de preferencias en vez de
encontrarla buscando (Ai y Bansal, *Econometrica*).

---

### L08 — Fix de Londres de fin de mes · **GRADO A**

| | |
|---|---|
| datos del paper original | hasta **2012** |
| evidencia posterior | **sí, sobre el mecanismo** |
| ¿se debilitó? | el mecanismo no; la microestructura del instante cambió |

**Ito, Takatoshi; Yamada, Masahiro. "Did the Reform Fix the London Fix Problem?"** NBER Working
Paper 23327. https://www.nber.org/system/files/working_papers/w23327/w23327.pdf

Después de que WM/Reuters pasara en febrero de 2015 de una ventana de un minuto a una de cinco, **el
volumen total durante la ventana del fixing no se redujo**, lo que implica que **la demanda de operar
al fixing sigue alta**; el volumen simplemente se reparte más parejo dentro de la ventana.

**Eso es exactamente la confirmación que hace falta**: el flujo de cobertura de fin de mes es una
necesidad de mandato y la reforma no lo elimina. Lo que cambia es la forma del pico, no su existencia.

---

### L07 — Fixing de Tokio y días *gotobi* · **GRADO A−**

| | |
|---|---|
| datos del paper original | hasta **2013** |
| evidencia posterior | **sí, sobre 2018-2020** |
| ¿se debilitó? | no reportado |
| señal de alarma | **está empaquetada y vendida como robot minorista** |

**Bessho, H.; Sugimoto, T.; Suzuki, T. (2023). "Forex Trading Strategy That Might Be Executed Due to
the Popularity of Gotobi Anomaly."** arXiv:2301.13204. https://arxiv.org/abs/2301.13204

Analizan datos de USD/JPY de **2018 a 2020** y confirman que el movimiento difiere claramente entre
días gotobi y no gotobi, y que la tasa sigue subiendo hasta las 9:55 en los gotobi.

**Es A− y no A por dos motivos, los dos importantes:**
1. **Es arXiv, no está revisado por pares.**
2. **El título del propio paper es sobre la POPULARIDAD de la anomalía**, y la búsqueda devuelve
   robots comerciales para MetaTrader 4 y 5 que la venden como producto, además de guiones públicos
   de estrategia. **Un efecto que se vende empaquetado al minorista es un efecto con mucha gente
   adentro.** Eso no está medido, pero está a la vista.

---

### L10 — Rebalanceo institucional · **GRADO B — RIESGO DECLARADO**

| | |
|---|---|
| datos del paper original | hasta **2023**, los más recientes del inventario |
| evidencia posterior | **ninguna. Busqué y no hay** |
| ¿dijeron algo los autores después? | no |

**RIESGO DECLARADO: esta candidata no tiene ninguna evidencia posterior a su publicación.** Es un
documento de trabajo del NBER de marzo de 2025, sin revisión por pares y sin réplica.

**Atenuante honesto y único en el inventario:** su muestra llega a 2023, así que la brecha entre el
fin de los datos y hoy es de dos años, contra los catorce de Gao et al. **Tiene poca evidencia
posterior porque hay poco "posterior", no porque nadie haya mirado.**

---

### L01 — Momento intradiario en 60+ futuros · **GRADO B — RIESGO DECLARADO**

| | |
|---|---|
| datos del paper original | hasta **mayo de 2020** |
| evidencia posterior independiente | **ninguna que replique la regla tal cual. Busqué y no hay** |
| ¿se debilitó? | no medido por nadie |

**RIESGO DECLARADO: no encontré ninguna replicación independiente de la versión `rROD` sobre futuros
posterior a 2021.**

Hay una **falsa confirmación** que conviene desarmar, porque alguien la va a traer:

**Zarattini, Carlo; Aziz, Andrew; Barbon, Andrea (2024). "Beat the Market: An Effective Intraday
Momentum Strategy for S&P500 ETF (SPY)."** Swiss Finance Institute Research Paper 24-97,
SSRN 4824172. Reportan **2007 a principios de 2024**, retorno total de 1.985 %, **19,6 % anual neto
de costos y Sharpe 1,33**.

**No es una replicación, y hay que decir por qué:**
- **Cambia la regla.** Construyen "bandas de ruido" a partir del retorno intradiario promedio de los
  últimos 14 días y usan stops dinámicos de arrastre. Eso no es "el signo de `rROD`": es una
  estrategia nueva de la misma familia, con parámetros elegidos.
- **Y ya tiene descendencia que optimiza los parámetros:** Maróy, "Improvements to Intraday Momentum
  Strategies Using Parameter Optimization and Different Exit Strategies", SSRN 5095349. Es
  literalmente más búsqueda sobre los mismos datos.
- Dos de los tres autores son de la industria de la formación y la gestión, no académicos.

**Una estrategia modificada y optimizada que rinde bien sobre los mismos datos no confirma el efecto
original: reproduce el problema de este proyecto en otra gente.**

---

### L06 — Momento intradiario en futuros de VIX · **GRADO B — RIESGO DECLARADO**

Publicado en 2023 y **sin ninguna evidencia posterior**. Busqué y no hay. Es demasiado reciente.
Advertencia estructural aparte: el mercado de futuros de VIX cambió de forma drástica en febrero de
2018, cuando se destruyeron varios productos de volatilidad inversa; un efecto medido a través de ese
quiebre no es homogéneo.

---

### L09 — Momento intradiario en el crudo · **GRADO B — RIESGO DECLARADO**

Datos hasta 2018. La única continuación es **de los mismos autores**: Wen, Indriawan, Lien y Xu
(2023), "Intraday Return Predictability in the Crude Oil Market: The Role of EIA Inventory
Announcements", *The Energy Journal* 44(4). **Una continuación del mismo grupo no es evidencia
independiente.** Ninguna réplica de terceros.

---

### L03 — Deriva previa a los anuncios macro · **GRADO C — DEBILITADA, Y LO DICEN LOS AUTORES**

| | |
|---|---|
| datos del paper original | hasta **marzo de 2014** |
| evidencia posterior | **sí, de los mismos autores** |
| ¿se debilitó? | **SÍ, y está publicado** |

**Kurov, Alexander; Sancetta, Alessio; Wolfe, Marketa Halova (2022). "Drift Begone! Release policies
and preannouncement informed trading."** *Journal of International Money and Finance*, vol. 128.
https://www.sciencedirect.com/science/article/abs/pii/S0261560622001218
PDF: https://www.skidmore.edu/economics/documents/Kurov-Sancetta-Wolfe-2022-Drift-Begone.pdf

**Tres de los cuatro autores originales.** En 2017 la autoridad de estadística del Reino Unido
eliminó el acceso anticipado de funcionarios a datos macroeconómicos sensibles. Examinan el efecto
sobre el ajuste de precios en el mercado de futuros de divisas alrededor de los grandes anuncios
británicos. Tres anuncios —índice de precios al consumidor, producción industrial y ventas
minoristas— muestran evidencia fuerte de comercio informado antes de su publicación **hasta 2017**,
y **la deriva previa se debilita con el fin del acceso anticipado**. Y, consistente con menos
comercio informado, **la reacción del mercado en el momento oficial de la publicación se hace más
grande**.

**Éste es el caso más informativo de todo el inventario y es el que Roberto pidió buscar: los propios
autores volvieron sobre su efecto y reportaron que se debilita cuando se corta la fuente.**

**Dos matices que van pegados, y no los borro:**
1. El paper de 2022 es sobre **anuncios británicos y futuros de divisas**, no sobre los cuatro
   anuncios estadounidenses de las 10:00 en el ES. **No es una refutación directa de L03.**
2. Pero el mecanismo que documenta —el acceso anticipado— es el mismo que L03 propone, y **en Estados
   Unidos hubo cortes equivalentes en 2013 y 2014**, justo al final de la muestra original.

**Baja cinco posiciones. Y al mismo tiempo se vuelve la pregunta más interesante del inventario:
¿siguió existiendo en el ES entre 2016 y 2019, después de esos cortes?** Ese es un test de mecanismo,
está en `M01`, y ahora tiene una hipótesis previa concreta.

---

### L04 — Rebalanceo de ETF apalancados · **GRADO C — DEBILITADA**

| | |
|---|---|
| datos | Shum et al. hasta 2011; Ivanov y Lenkey hasta 2014 |
| evidencia posterior | **sí, una revisión de la literatura** |
| ¿se debilitó? | **sí** |

**Lenkey, Stephen L. (2024). "The market impact of leveraged ETFs: A survey of the literature."**
*Quantitative Finance and Economics*. https://www.aimspress.com/article/doi/10.3934/QFE.2024031

La revisión concluye que la literatura reporta asociaciones estadísticamente significativas de forma
consistente, pero que **la mayoría de los trabajos disponibles adolece de errores metodológicos
potencialmente serios** y que las asociaciones económicas parecen insignificantes. Y separa las dos
fuentes: **los efectos de gamma de las opciones son persistentes, mientras que los efectos de los
ETF apalancados han disminuido con el tiempo.**

**Que el autor de la revisión sea Lenkey, coautor del paper que ya decía que el efecto es
económicamente insignificante, hay que declararlo: no es un árbitro neutral.** Aun así, es la única
revisión sistemática del área y separa las dos fuentes de flujo, que es justo lo que L04 necesitaba.

**Nota que va a favor de L01 y no de L04:** si la gamma de opciones persiste y la de los ETF
apalancados no, entonces el mecanismo de L01 sobrevive **por la mitad que L04 no aporta**.

---

### L02 — Momento intradiario, versión original · **GRADO C — REPLICACIÓN FALLIDA**

| | |
|---|---|
| datos del paper original | hasta **2013** |
| evidencia posterior | **sí, y falla donde importa** |

Ya estaba en la ficha y acá se consolida:
- **Rosa (2022), *Journal of Futures Markets* 42, 2218-2234**: fuera de muestra sobre **futuros del
  E-mini**, la predictibilidad **desaparece**.
- **Limkriangkrai, Chai y Zheng (2023), *Pacific-Basin Finance Journal* 80**: no aparece en Hong
  Kong ni en Singapur.
- Las "confirmaciones" posteriores cambian la regla, ver L01.

**Es la única del inventario con una replicación fallida publicada en el instrumento exacto que
Roberto opera.** Baja cuatro posiciones.

---

### L05 — La gamma neta como eje · **GRADO C — DISPUTADA EN EL NIVEL**

Contradicha por Dim, Eraker y Vilkov (2023) en el nivel: encuentran que la gamma de inventario de
los creadores de mercado es **en promedio positiva**, lo que invierte el efecto medio. Y hay trabajo
posterior en curso sobre la cuestión: "Where does gamma hedge drive the intraday market move?"
(2024), https://afajof.org/management/viewp.php?n=129472

A favor: la revisión de Lenkey (2024) dice que **los efectos de gamma de opciones son persistentes**,
que es la mitad de L05 que importa.

---

# El reordenamiento

**Regla de combinación, declarada antes de aplicarla:** primero por grado, después por distancia a un
veredicto dentro del grado. Es lexicográfica a propósito. **Una candidata cuyo efecto está
documentado como debilitado no debe medirse antes que una confirmada, por cerca que esté de ser
medible.**

| posición | ficha | grado | falta (eventos) | posición vieja | movimiento |
|---|---|---|---|---|---|
| 1 | **L11** Savor y Wilson | **A** | 1,9× | 1 | = |
| 2 | **L07** fixing de Tokio | **A−** | 3,4× | 4 | **↑ 2** |
| 3 | **L08** Melvin y Prins | **A** | 28× | 8 | **↑ 5** |
| 4 | **L10** Harvey et al. | B | 2,1× | 2 | ↓ 2 |
| 5 | **L01** Baltussen et al. | B | 12,6× | 5 | = |
| 6 | **L06** VIX | B | 34× | 9 | ↑ 3 |
| 7 | **L09** crudo | B | — | 10 | ↑ 3 |
| 8 | **L03** Kurov et al. | **C** | 2,9× | 3 | **↓ 5** |
| 9 | **L04** ETF apalancados | **C** | 12,6× | 7 | ↓ 2 |
| 10 | **L02** Gao et al. | **C** | 14,1× | 6 | **↓ 4** |
| 11 | **L05** gamma | C | — | 11 | = |

**Ocho de once cambian de posición. Tres se quedan donde estaban.**

Los tres movimientos grandes:
- **L08 sube cinco lugares.** Era la penúltima por distancia y es de las dos únicas con confirmación
  posterior de terceros.
- **L03 baja cinco lugares.** Era tercera y sus propios autores publicaron que el efecto se debilita
  cuando se corta el acceso anticipado.
- **L02 baja cuatro.** Es la única con replicación fallida publicada en futuros del E-mini.

**Que el filtro reordene ocho de once es la medida de cuánto valía.** Y costó cuatro búsquedas: es
una pregunta de literatura, no de datos, y ninguna de las respuestas requirió tocar un precio.

## Lo que este filtro NO puede hacer

**No detecta la muerte silenciosa.** La deriva nocturna murió en 2021 y se documentó en 2026: hubo
cinco años en los que la búsqueda habría devuelto grado A. **El grado A significa "nadie publicó
todavía que se murió", no "está vivo".**

---

# REPESAJE — por lo reciente de los DATOS, no de la publicación

El grado de arriba mide **si alguien miró**. Este repesaje mide **qué tan vieja es la evidencia más
nueva**. Son riesgos distintos y no se sustituyen.

## Hasta dónde llegan los datos que sostienen cada candidata

| candidata | datos del paper original | **datos más recientes que la sostienen** | fuente de esos datos |
|---|---|---|---|
| **L10** | 2023 | **2023** | el propio paper |
| **L11** | 2009 | **2023** | Ai, Bansal y Guo, extensión de terceros |
| L05 | 2020 | 2023 | Dim, Eraker y Vilkov, **contradiciendo** |
| L06 | ≈ 2021 | ≈ 2021 | el propio paper |
| L01 | mayo de 2020 | mayo de 2020 | el propio paper |
| L07 | 2013 | **2020** | Bessho, Sugimoto y Suzuki, arXiv |
| L03 | marzo de 2014 | ≈ 2019, **otro mercado** | Kurov et al. 2022, sobre datos británicos |
| L09 | 2018 | 2018 | el propio paper |
| L08 | 2012 | ≈ 2016 | Ito y Yamada sobre la reforma |
| L04 | 2014 | 2014 | Ivanov y Lenkey. La revisión de 2024 no trae datos nuevos |
| L02 | 2013 | 2013 | el propio paper |

## El orden nuevo, y qué cambia

| # | por edad de los datos | # anterior, por grado | movimiento |
|---|---|---|---|
| 1 | **L11** (2023, con confirmación de terceros) | 1 | **=** |
| 2 | **L10** (2023, sin confirmación) | 4 | ↑ 2 |
| 3 | L06 (≈ 2021) | 6 | ↑ 3 |
| 4 | L01 (2020) | 5 | ↑ 1 |
| 5 | L07 (2020) | 2 | ↓ 3 |
| 6 | L03 (2019, otro mercado) | 8 | ↑ 2 |
| 7 | L09 (2018) | 7 | = |
| 8 | L08 (2016) | 3 | **↓ 5** |
| 9 | L04 (2014) | 9 | = |
| 10 | L02 (2013) | 10 | = |
| 11 | L05 (eje, no regla) | 11 | = |

**Seis de once cambian de posición. El primer puesto NO cambia.**

## Cómo hay que leer los dos órdenes juntos

**L11 queda primera en los dos**, y por motivos independientes: tiene confirmación de terceros **y**
esa confirmación llega a 2023. Es la única del inventario que gana en las dos dimensiones.

**L08 es el desacuerdo más grande, y hay que entenderlo antes de usarlo:** es tercera por grado
—tiene confirmación publicada de que el mecanismo sobrevivió a la reforma— y octava por edad, porque
esa confirmación es sobre datos de alrededor de 2016. **Está confirmada, con datos viejos.** Las dos
cosas son ciertas y ninguna anula a la otra.

**Y hay una convergencia que sí decide: L04 y L02 son novena y décima en los dos órdenes.** Una
candidata que pierde en las dos dimensiones no tiene defensa por ningún lado. **Ése es el uso
correcto de tener dos órdenes: no promediarlos, sino mirar dónde coinciden.**

**No reemplazo el orden del índice.** El del índice sigue siendo el de grado, porque "alguien lo
verificó" es evidencia más dura que "los datos son recientes". Este repesaje va como segunda
dimensión y como advertencia sobre las que ganan en una sola.

---

# PASO DE LECTURA INTERNA — leer el paper original buscando declive adentro

**Agregado 2026-09-05. El filtro buscaba evidencia posterior AFUERA y no leía el paper original
buscando declive ADENTRO.**

El caso que lo obliga estaba en un texto que yo ya tenía extraído y no usé, porque la búsqueda
apuntaba a seguimientos: **Ito y Yamada reportan que la correlación entre los precios de fijación de
los dos bancos era del 80 % antes de 2008 y cayó a menos del 50 % después.** Es una medida
cuantitativa de que el mecanismo se debilitó, dentro del mismo paper al que le puse grado A menos.

## El paso

**Antes de asignar grado, leer el paper original buscando: particiones cronológicas con resultados
distintos, afirmaciones de que el efecto se concentra en una época, o medidas del mecanismo que
cambian a lo largo de la muestra.**

## La advertencia que va pegada, y es mía

**Un declive dentro de la muestra puede ser un cambio de régimen puntual y no decaimiento del
efecto.** El corte de Ito y Yamada es 2008, que es la crisis financiera global: **puede ser el efecto
apagándose o puede ser la crisis.** Con lo publicado **no se puede distinguir**, y cuando no se puede,
se dice.

## Cómo modifica el grado

**Un paso, nunca más:**

- **declive interno** → el grado baja un escalón;
- **crecimiento o estabilidad** verificados sobre una partición cronológica completa → sube un
  escalón, **nunca por encima de A**, porque el grado A lo gana sólo la evidencia externa de terceros;
- **si hay evidencia externa en contra, la lectura interna NO sube el grado.** Una estabilidad
  interna no puede borrar una replicación fallida publicada.

## Las once, leídas por dentro

| candidata | qué dice el propio paper | efecto |
|---|---|---|
| **L11** | mitades 1958-1983 y 1984-2009: la diferencia va de **8,7 a 11,4 pb**. **Creció** | ya era A, se queda |
| **L01** | sección 3.4, submuestras **1974-1999 y 2000-2020**: *"los resultados son similares en la primera y la segunda mitad"*, y `rROD` gana la comparación directa en las dos | **B → A−** |
| **L02** | `r1` *"es siempre significativo, haya crisis o no"*; `r12` viene *"en gran parte del período de la crisis financiera"*. El predictor que promueven es el estable | **sin cambio**: tiene replicación fallida externa, y la regla no permite subir |
| **L07** | **dos señales de declive**: la correlación entre bancos cae de 80 % a menos de 50 % después de 2008, y el sesgo del precio de fijación pasa de estar sobre el **máximo** transado a estar sobre la **mediana** | **A− → B** |
| L03 | extiende la muestra hacia atrás, no hacia adelante. La lectura interna queda **superada** por el paper externo de 2022 de los mismos autores | sin cambio |
| L04 | sin partición cronológica utilizable | sin cambio |
| L05 | la cuota de mercado de los ETF apalancados **sube** a lo largo de 2006-2020, o sea que el impulsor del mecanismo crece | sin cambio: hay contradicción externa |
| L08 | **ninguna partición temporal** | sin cambio |
| L10 | sólo la nota al pie de la **primera** mitad, cualitativa | sin cambio |
| L06, L09 | texto no disponible | **no leído**, y se anota así |

## El reordenamiento

| # | ficha | grado | movimiento contra el orden anterior |
|---|---|---|---|
| 1 | **L11** | A | = |
| 2 | **L08** | A | ↑ 1 |
| 3 | **L01** | **A−** | **↑ 2** |
| 4 | L10 | B | = |
| 5 | **L07** | **B** | **↓ 3** |
| 6 | L06 | B | = |
| 7 | L09 | B | = |
| 8 | L03 | C | = |
| 9 | L04 | C | = |
| 10 | L02 | C | = |
| 11 | L05 | C | = |

**Tres de once cambian de posición. El primer puesto no cambia.**

Los dos movimientos, y los dos son informativos:

- **L07 baja tres lugares** por un declive que estaba escrito en su propio paper y que yo no había
  leído. **Con la advertencia puesta: puede ser la crisis de 2008 y no el efecto.**
- **L01 sube dos lugares** por lo contrario: es el único paper del inventario que **verifica
  estabilidad sobre una partición cronológica de cuarenta y seis años** y la publica. Eso es más
  fuerte que la ausencia de un seguimiento externo, que era todo lo que tenía antes.

**El paso costó cero: los textos ya estaban extraídos de rondas anteriores. Es el filtro más barato
de los diez y encontró dos cosas.**

---

# APLICACIÓN DE LA CORRECCIÓN — ninguna conserva grado A

| candidata | en qué se apoyaba su grado | muestra de esa evidencia | ¿se superpone con 2016-2019? | grado |
|---|---|---|---|---|
| **L11** | Ai, Bansal y Guo extienden a 2023 | **1961-2023** | **SÍ** | **A → B** |
| **L08** | Ito y Yamada sobre la reforma, 2017 | **no verificable**: el documento es de abril de 2017 y estudia la reforma de febrero de 2015. **No pude confirmar que termine antes de 2016** | **no verificado** | **A → B** |
| **L07** | Bessho, Sugimoto y Suzuki | **2018-2020** | **SÍ** | ya era B por lectura interna |
| **L01** | lectura interna: estabilidad entre mitades | la segunda mitad es **2000-2020** | **SÍ**: la estabilidad que la ascendió incluye nuestro período | **A− → B** |
| L05 | Dim, Eraker y Vilkov | hasta ~2023 | sí, y además contradice | sigue C |
| L02 | Rosa, replicación **fallida** | se superpone | **la refutación SÍ cuenta**, por la asimetría | sigue C |
| L03 | Kurov et al. 2022, **mercado británico** | 2019, pero **otro mercado y otro instrumento** | **NO contamina nuestros datos** | sigue C |
| L04 | revisión de Lenkey, sin datos nuevos | subyacentes hasta 2014 | no | sigue C |
| L06, L09 | sin evidencia posterior | — | — | siguen B |

**El caso de L08 hay que decirlo bien: no probé que se superponga. No pude probar que NO se
superponga, y la carga está del lado de la confirmación.** Se restaura leyendo el período de muestra
del paper, que es un paso de literatura y cuesta cero.

## El orden nuevo

| # | ficha | grado | falta | movimiento |
|---|---|---|---|---|
| 1 | **L11** | B | 1,9× | **=** |
| 2 | L10 | B | 2,1× | ↑ 2 |
| 3 | L07 | B | 3,4× | ↑ 2 |
| 4 | L01 | B | 12,6× | ↓ 1 |
| 5 | **L08** | B | 28× | **↓ 3** |
| 6 | L06 | B | 34× | = |
| 7 | L09 | B | — | = |
| 8 | L03 | C | 2,9× | = |
| 9 | L04 | C | 12,6× | = |
| 10 | L02 | C | 14,1× | = |
| 11 | L05 | C | — | = |

**Cuatro de once cambian. El primer puesto NO se cae.**

## Pero L11 conserva el puesto por otro motivo, y eso es lo importante

**L11 sigue primera, pero ya no porque tenga confirmación: la perdió.** Sigue primera porque, con
todas en grado B, **el desempate lo hace la distancia a un veredicto**, y ella es la que menos lejos
está.

> ## **Con la contaminación corregida, la dimensión de evidencia DEJA DE DISCRIMINAR entre las
> primeras siete. El índice vuelve a estar ordenado por distancia, que es como estaba antes de que
> existiera `F7`.**

**Ése es el resultado honesto de arreglar mi propio filtro: el filtro, corregido, casi no aporta
información arriba.** Sigue aportándola abajo, donde separa a las cuatro de grado C, y **ahí sí
distingue: L03 tiene el efecto debilitado por sus propios autores y L02 tiene una replicación fallida
publicada.** Eso no lo tocó la corrección.

---

# CRITERIO GENERAL — antes de descartar por muerto, preguntar si se MUDÓ

**Éste es un criterio permanente del filtro, no una nota de una tanda.**

El caso que lo obliga está en la entrada de L03. Kurov, Sancetta y Wolfe (2022) no reportaron sólo
que la deriva previa se debilitó cuando se cortó el acceso anticipado. Reportaron **las dos mitades**:

> la deriva previa se debilita con el fin del acceso anticipado, **y —consistente con menos comercio
> informado antes de los anuncios— la reacción del mercado en el momento oficial de la publicación
> se hace MÁS GRANDE.**

**La información no dejó de entrar al precio. Entró más tarde y de golpe.** El movimiento no
desapareció: **cambió de ventana.**

## Por qué importa para todo el inventario

Un efecto se puede apagar de dos maneras muy distintas, y **el filtro de edad las confunde si no se
lo obliga a separarlas**:

| | qué pasó | qué queda |
|---|---|---|
| **MUERTE** | el mecanismo dejó de operar, o el flujo que lo causaba se secó | nada |
| **MUDANZA** | el mecanismo sigue, pero cambió el momento, el instrumento o el horizonte | **el efecto, en otra ventana** |

La deriva nocturna del E-mini es una **muerte**: los propios autores midieron que la causa se secó,
la dispersión del volumen firmado de cierre cayó de 6,5 % a 2,9 %. **No se mudó: se apagó la fuente.**

La deriva previa a los anuncios es una **mudanza**: la fuente —el acceso anticipado— se cortó, y el
ajuste de precio se corrió a la ventana siguiente.

## La pregunta que hay que hacerse, y en qué orden

**Antes de mandar una candidata a `DESCARTADAS.md` por grado D, hay que contestar tres cosas:**

1. **¿Se secó la CAUSA, o se movió el MOMENTO?** Si el paper que reporta la desaparición también
   reporta que el ajuste aparece en otro lado, es mudanza.
2. **¿La regla original sigue describiendo lo mismo?** Una mudanza deja la regla vieja apuntando a
   una ventana vacía. Eso se lee como muerte y no lo es.
3. **¿La ventana nueva es operable?** Una mudanza a una ventana de segundos alrededor de una
   publicación es peor que inútil para este proyecto, aunque el efecto sea más grande que antes.

**El punto 3 es el que evita el entusiasmo:** que un efecto se haya mudado y hasta agrandado no
significa que sirva. La deriva de L03 se mudó de una ventana de treinta minutos —operable— a un salto
en el instante de la publicación —no operable con lo que hay—. **Es un efecto más grande en un lugar
peor.**

## Consecuencia para la clasificación

Se agrega una etiqueta al grado, no un grado nuevo:

- **C-mudada** — el efecto se debilitó en su ventana original y hay evidencia publicada de que el
  ajuste apareció en otra. **L03 es C-mudada.**
- **D-muerta** — la causa se secó y no hay ventana de reemplazo. **La deriva nocturna es D-muerta.**

**La diferencia práctica: una C-mudada sigue siendo un buen sujeto para un test de mecanismo, porque
la pregunta "¿dónde está ahora?" tiene respuesta. Una D-muerta no.**
