# F7 — ¿EL EFECTO TODAVÍA EXISTE?

**VENTANA L. NO MEDIDO. No gasta cartucho, K sigue en 261.**

Los seis filtros anteriores preguntan si **podemos medir** una candidata. Ninguno pregunta si **sigue
existiendo**. Este documento agrega esa dimensión y la aplica a las once.

El caso que obliga a tenerlo: la deriva nocturna del E-mini valía más del 60 % del retorno anual del
contrato, se publicó en el *Review of Financial Studies* en 2023 con el mecanismo medido, y **ya
estaba muerta cuando se publicó**. Los propios autores lo documentaron en 2026. Ningún filtro de
magnitud, de eventos ni de exposición la habría detenido.

---

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
