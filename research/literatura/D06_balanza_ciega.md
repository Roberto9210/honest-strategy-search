# D06 — LA REGLA DE LA BALANZA CIEGA, aplicada a las once

**VENTANA L. NO MIDE CANDIDATAS; corre CONTROLES DEL INSTRUMENTO desde el 2026-09-05 (rol ampliado por Roberto, ver `INDICE`). K sigue en 261.**

> ## LA REGLA

> **Antes de correr una prueba, calcular qué devolvería si la idea estuviera muerta. Si eso es
> indistinguible de lo que devolvería si estuviera viva con el decaimiento típico, la prueba no
> informa y no se corre.**
>
> **Y el umbral de detección NO se compara contra la magnitud publicada: se compara contra la
> magnitud publicada DESPUÉS del decaimiento esperado.**

> **RIESGO NOMBRADO, no corrección:** el escalado de σ de este documento supone volatilidad intradiaria **uniforme**, y no lo es. Con el patrón en U, **L01 y L03 pasarían a CIEGAS**. Los veredictos NO se corrigen porque ya decían "requiere medición" y ésta es la dirección desfavorable. Ver [A03](A03_variables_tratadas_como_constantes.md).

---

# 1. Cómo se calcula, y por qué la cota es optimista a propósito

Para una candidata con `n` eventos, desvío `σ` en su ventana y vara del juez `t*`:

```
(a) magnitud detectable  =  t* · σ / √n          en puntos básicos
(b) magnitud publicada
(c) magnitud esperada    =  0,42 × (b)           tras el 58 % de McLean y Pontiff

CIEGA  si  (c) < (a)
```

## Las elecciones, todas a favor de la candidata

| elección | qué elegí | por qué es lo más favorable |
|---|---|---|
| vara del juez | **`t* = 3,0`** | la de **una** variante declarada, la más baja que el juez usa |
| número de eventos | **el máximo defendible** de cada candidata | más eventos, más potencia |
| magnitud publicada | **la mayor** cuando el paper da un rango | |
| desvío | **el menor plausible** | ver la sección 2 |

> **La cota optimista puede RECHAZAR pero nunca APROBAR.** Si con todo a favor la candidata no se ve,
> está muerta y el resultado es firme. Si con todo a favor sí se vería, **eso no es una aprobación:
> es "REQUIERE MEDICIÓN REAL DEL DESVÍO"**, y así queda escrito.

## Los desvíos no medidos: se invierte, no se estima

**Para las candidatas sin desvío medido no lo estimo.** Calculo **qué desvío haría falta** para que
`(a) = (c)`, y después digo si ese desvío es plausible.

**El ancla es el único desvío medido que tenemos: 82 puntos básicos por sesión completa de ES**
(VENTANA G). Para una ventana de `T` minutos dentro de una sesión de 1.380:

```
σ(T)  ≈  82 · √(T / 1380)          →   30 min: 12,1 pb    60 min: 17,1 pb    10 min: 7,0 pb
```

**Para divisas uso dos tercios de eso**, porque la volatilidad diaria de los pares mayores es del
orden de dos tercios de la del ES. *(La razón de dos tercios es MÍA: **FRÁGIL**. La regla de la raíz
del tiempo también, aunque es la convención estándar.)*

---

# 2. Dónde NO corresponde el 58 %

**El factor de McLean y Pontiff se midió sobre anomalías publicadas en revistas académicas.** Tres de
las once no encajan y hay que decirlo:

| candidata | por qué no le corresponde | qué uso |
|---|---|---|
| **L10** Harvey et al. | es un **documento de trabajo del NBER de 2025, sin revista**, y **nuestro período de prueba es ANTERIOR a su publicación**. El decaimiento post-publicación no puede haber ocurrido todavía | **la magnitud publicada entera, sin descontar** |
| **L05** | no es una regla con magnitud: es un eje | no aplica |
| **L04, L09** | su magnitud no está publicada en unidades convertibles | no aplica |

**Para L10 el resultado no cambia**: sale CIEGA con la magnitud entera, así que la discusión del
factor es irrelevante en su caso. **Se deja escrita igual, porque el criterio importa aunque el caso
no lo necesite.**

---

# 3. LA TABLA

Magnitudes en puntos básicos. `t* = 3,0` en todas.

| | candidata | ventana | `n` | `σ` usado | **(a) detectable** | **(b) publicada** | **(c) esperada** | **veredicto** |
|---|---|---|---|---|---|---|---|---|
| 1 | **L03** Kurov | 30 min | 192 | 12,1 | **2,62** | 10,4 | **4,37** | **REQUIERE MEDICIÓN** · margen 1,67× |
| 2 | **L07** Ito y Yamada | 10 min, 6J | 1.007 | *invertido* | **0,76** | 1,8 | **0,76** | **REQUIERE MEDICIÓN** · margen 1,72× |
| 3 | **L08** Melvin y Prins | 60 min, panel × 10 | 470 | *invertido* | **2,10** | 5,0 | **2,10** | **REQUIERE MEDICIÓN** · margen 1,33× |
| 4 | **L01** Baltussen | 30 min | 1.007 | 12,1 | **1,143** | 2,72 | **1,143** | **REQUIERE MEDICIÓN** · **margen 1,00×** |
| 5 | **L02** Gao | 30 min | 1.007 | 12,1 | **1,143** | 2,65 | **1,112** | **CIEGA** por 2,7 % |
| 6 | **L11** Savor y Wilson | sesión | 176 | **82,0 medido** | **18,54** | **11,4** | 4,79 | **CIEGA** — y **ciega con la magnitud ENTERA** |
| 7 | **L10** Harvey et al. | sesión | 46 | **82,8 medido** | **36,63** | **17,0** | *sin descuento* | **CIEGA** — factor 2,15 con la magnitud entera |
| 8 | **L06** VIX | 30 min, VX | 1.007 | *invertido* | **3,00** | 7,14 | 3,00 | **CIEGA** — ver abajo |
| 9 | L04 ETF apalancados | — | — | — | — | **no publicada en pb** | — | **NO EVALUABLE**; como regla es L01 |
| 10 | L09 crudo | — | — | — | — | **no publicada en pb** | — | **NO EVALUABLE** |
| 11 | L05 gamma | eje, no regla | — | — | — | — | — | **NO EVALUABLE** |

## Las tres inversiones, con su juicio de plausibilidad

| candidata | `σ` que haría falta | `σ` plausible según el ancla de 82 pb | ¿alcanza? |
|---|---|---|---|
| **L07** | ≤ **8,00 pb** en 10 min de USD/JPY | ≈ **4,7 pb** | **sí, con margen 1,7×** |
| **L08** | ≤ **15,18 pb** en 60 min de una moneda mayor | ≈ **11,4 pb** | **sí, con margen 1,33×** |
| **L06** | ≤ **31,7 pb** en 30 min de futuro de VIX, o sea **2,15 % diario** | los futuros de VIX se mueven mucho más que eso | **NO. CIEGA firme** |

---

# 4. Las cuatro ciegas, una por una

**L11 y L10 son las dos que yo tenía primera y segunda del inventario, y son las dos peores acá.**

**L11 es ciega con la magnitud ENTERA, sin descontar nada.** Su umbral de detección es 18,54 puntos
básicos y su magnitud publicada es 11,4. **Aunque el efecto hubiera transferido intacto, no se
vería.** No hace falta discutir el decaimiento.

**L10 igual, por factor 2,15**, y con la magnitud entera porque el descuento no le corresponde.

**L06 es ciega por un margen amplio** y la inversión lo confirma: haría falta que los futuros de VIX
tuvieran una volatilidad diaria del 2,15 %, y se mueven varias veces eso.

**L02 es ciega por 2,7 %**, que está dentro de la imprecisión de las entradas. **Se reporta CIEGA
porque la cota es optimista y aun así no pasa**, que es exactamente la asimetría que la regla pide
respetar.

# 5. La que queda en la línea exacta

**L01 da `(a) = 1,143` y `(c) = 1,143`.** No es una aproximación mía: es lo que dan los números con
las elecciones más favorables.

**Y con el desvío que implica su PROPIO paper —Baltussen reporta 3,96 % anual de desvío para la
cartera de índices, o sea unos 25 pb por sesión en la última media hora— el umbral sube a 2,36 y la
candidata queda CIEGA.**

> **L01 es el caso donde la regla de "la cota optimista no aprueba" hace todo el trabajo. Empatar en
> la línea con todo a favor, y perder con el número del propio paper, es tan informativo como perder
> directamente.**

---

# 6. EL CONTEO

| veredicto | cuántas | cuáles |
|---|---|---|
| **CIEGA** | **4** | L02, L06, L10, L11 |
| **REQUIERE MEDICIÓN REAL DEL DESVÍO** | **4** | L01, L03, L07, L08 |
| **NO EVALUABLE** por falta de magnitud publicada | **3** | L04, L05, L09 |

**Las once NO salen ciegas. La ruta entera no se cierra.**

## Y el orden se da vuelta

**Las dos que encabezaban el inventario por distancia a un veredicto son ciegas. Las tres que
sobreviven con margen estaban en los puestos 3, 5 y 8.**

**El motivo es estructural y conviene entenderlo:** la balanza ciega premia una magnitud grande
**respecto del ruido de su propia ventana**. Una ventana de treinta minutos tiene un octavo del ruido
de una sesión entera. **Las candidatas de cierre a cierre pagan el ruido de una sesión completa para
capturar un efecto de una sesión, y las intradiarias pagan sólo el ruido de su ventana.**

**Ninguno de los trece filtros anteriores medía eso.** `F5` contaba eventos y `F6` separaba medible de
rentable, pero **ninguno comparaba la magnitud contra el ruido de la ventana en la que vive.**

---

# 7. La pregunta pegada: ¿qué tendría que volverse cierto para que el DISEÑO de P01 fuera ejecutable?

**Respuesta: un contrato con más historia de fines de mes de la que tiene el E-mini, y que además
esté fuera de la muestra de Harvey et al.**

`P01` necesita `Σ n·r² = 144` y tiene 17,26, o sea un factor 8,35. Para L10 eso son **401 fines de
mes**.

| contrato | historia | fines de mes |
|---|---|---|
| E-mini S&P 500, desde septiembre de 1997 | 29 años | ≈ **348** |
| S&P 500 tamaño completo, desde abril de 1982 | 44 años | ≈ 528 |

**Existe un contrato con suficiente historia: el S&P 500 de tamaño completo.** Pero:

1. **1997-2023 está dentro de la muestra de Harvey et al.**, así que los fines de mes limpios serían
   los de 1982-1996 —unos 180— más 2024-2026 —unos 32—: **212, no 401.**
2. **No tenemos esos datos**, el juez sólo carga ES 1-min 2016-2019, y Roberto no opera el contrato
   grande.
3. **Cuarenta años de antigüedad**, con una microestructura que no se parece a la actual.

> ## **El diseño no es ejecutable, y no por una limitación nuestra: no existe la historia limpia que necesita en ningún contrato. Corresponde decir que el diseño está cerrado en la práctica, y no sólo la ejecución.**

**Corrijo mi propia frase de `D05`. Ahí escribí "se cierra la ejecución, no el diseño". Es más exacto
decir: se cierran las dos, y lo que sobrevive del documento son las PIEZAS —el criterio de inclusión,
la estandarización declarada, los ocho controles— que son reutilizables en otro diseño.**

---

# 8. Qué sigue, según esta tabla

**Las cuatro ciegas se cierran igual que `P01`.** No se pre-registran, no se miden, y su cierre queda
escrito con su número.

**Las cuatro que requieren medición necesitan exactamente una cosa: el desvío real de su ventana.**

| candidata | qué desvío hay que medir | dónde está el dato |
|---|---|---|
| **L01** | desvío de la última media hora del ES, 2016-2019 | **en el repo.** Ninguna compra |
| **L03** | desvío de la ventana 9:30-10:00 del ES, 2016-2019 | **en el repo.** Ninguna compra |
| L07 | desvío de 10 minutos de USD/JPY | requiere comprar 6J |
| L08 | desvío de 1 hora de una moneda mayor | requiere comprar 6E |

> **Dos de las cuatro se resuelven con datos que ya están en el repo y sin gastar un peso ni un
> cartucho. Ésa es la única acción concreta que sale de este documento.**
