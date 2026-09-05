# L12 — La deriva nocturna del ES: Boyarchenko, Larsen y Whelan. **Publicada como NO RENTABLE después de costos, sobre nuestro instrumento, por 23 años.**

**VENTANA L. Ficha de literatura. NO MEDIDA. K sigue en 261.** Leída por Roberto el 2026-09-05; las
frases textuales son suyas del documento, y la interpretación es de esta ventana.

## 1. Cita

Boyarchenko, Nina; Larsen, Lars C.; Whelan, Paul. **"The Overnight Drift"**. Federal Reserve Bank of
New York, *Staff Report* n.º 917, febrero de 2020, revisado agosto de 2022. 99 páginas.

## 2. Instrumento y muestra

**E-mini S&P 500 (ES)**, retornos del punto medio del mejor bid-offer, **5 de enero de 1998 → 31 de
diciembre de 2020, 23 años.** **Nuestro 2016-2019 está ADENTRO de su muestra.**

## 3. El efecto y la magnitud, textual (p. 6)

> *"Pre-transaction costs, a trading strategy that goes long the S&P 500 futures between 2:00 and 3:00
> earns a Sharpe ratio of 1.1 and accounting for bid-ask spreads this reduces to −0.5. Extending the
> trading interval to the sub-period between 1:30 – 3:30 increases the pre-transaction cost Sharpe
> ratio to 1.3 but with an associated post-transaction Sharpe ratio equal to 0.3."*

Y p. 31: *"With transaction costs, the OD is not profitable in practice."*

## 4. En nuestras unidades (`scratchpad/cuenta_overnight.py`)

Una operación por día. `θ = Sharpe / √252` es la ventaja por operación en desvíos de la ventana.

| ventana | `θ` antes de costos | `θ` después | **costo implícito por operación** | **nuestro costo en esa ventana** |
|---|---|---|---|---|
| 2:00-3:00 | 0,069 | −0,031 | **0,101 σ** | 0,084 σ *(0,94 pb sobre 11,3 pb de las cajas #16-17 de G; ρ = 0, FRÁGIL)* |
| 1:30-3:30 | 0,082 | 0,019 | **0,063 σ** | 0,054 σ *(sobre 17,5 pb, cajas #15-18)* |

**Consistentes, y del mismo lado:** su costo por operación es un 15-20 % mayor que el nuestro —su
muestra empieza en 1998, con diferenciales más anchos, y descuentan el diferencial entero—. Lo que
sobra después del costo, 0,019 desvíos por operación, es **la sexta parte de lo que nuestro instrumento
puede ver a una operación por día en cuatro años (0,112)**, y **ni ellos con 23 años lo ven**: la `t`
de un Sharpe de 0,3 sobre 23 años es **1,44**. Su Sharpe de 1,3 antes de costos sí es firme (t = 6,2).

## 5. Veredictos

| filtro | resultado |
|---|---|
| **F17, frecuencia** | **NO ENTRA**: una operación por día, el extremo lento |
| balanza ciega `D06`, 4 años, `t* = 3,0` | **CIEGA**: margen **0,20** después de costos, **0,87** antes. Sin descuento por decaimiento (informe de staff, no revista) y **dentro de su propia muestra** |
| **R03 / F16 fila 11** | su ventana es la **madrugada de Globex** (2:00-3:00 del este). La firma exige cerrar a las 16:45 pero su día corre de 18:00 a 17:00: **abrir y cerrar en la madrugada PUEDE estar permitido. Condicional a la fila 11, que sigue abierta. No se asume** |

## 6. El mecanismo, textual (p. 7), y qué es respecto de lo que G midió

> *"...market makers position their limit orders in a way that brings their inventory closer to their
> targets, and do so by making the trade, which pays the bid-ask spread, non-profitable. Finally, we
> note that although the documented high frequency return patterns of this paper are not easily
> profitable..."*

**Es el mismo relato que G midió en 3a/3b sin conocerlos.** Con el estándar de Kirilenko y
Coughlan-Orlov: **¿es el mismo objeto?** No. BLW comparan el retorno de una ventana **horaria** contra
el diferencial, sobre 1998-2020; G mide el markout de un llenado pasivo a **segundos**, sobre seis días
de 2016-2019 y 2026. Mismo tema —el diferencial está puesto donde la ventaja predecible deja de pagar—,
distinto objeto, distinto período, distinta medición. **Consistencia externa de MECANISMO sobre el
mismo instrumento; NO confirmación de un número. Las confirmaciones siguen siendo cuatro.**

## 7. Lo que trae para otros documentos

- **`D18`**: un **nulo después de costos publicado sobre el ES**, por 23 años, en la grilla horaria. Es
  (B) en esa grilla, sobre nuestro instrumento.
- **`D12` y G**: p. 27, regresión de retornos horarios nocturnos entre 18:00 y 23:00 *"on order flow
  imbalance at the end of the preceding trading day"*. **El desbalance de flujo del cierre como
  predictor de la noche siguiente**: es la clase 1 de `INVENTARIO_2` a escala de horas, y G tiene el
  dato para mirarla sin comprar nada. No es candidata: 1/día.

## 8. Lo que la mataría del todo, y lo que no

Ya está cerrada por F17 y por la balanza. **Lo único que la reabriría es la fila 11 de F16 dando "sí" Y
un costo por operación por debajo de 0,02 σ de la ventana** —un quinto del nuestro—, que es lo que su
propio número dice que hace falta para que quede algo.

**Costos:** dinero cero, cartuchos cero, K en 261.
