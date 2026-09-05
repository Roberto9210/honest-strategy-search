# L13 — Menkveld 2013: el creador de mercado de alta frecuencia gana TODO en el diferencial y pierde en la posición. **La lectura más importante de las diez, y lo que transfiere al ES es el mecanismo, no un solo euro.**

**VENTANA L. Ficha de literatura. NO MEDIDA. K sigue en 261.** Leída por Roberto el 2026-09-05; las frases
textuales son suyas; la interpretación, de esta ventana.

## 1. Cita

Menkveld, Albert J. **"High Frequency Trading and the New-Market Makers"**. *Journal of Financial
Markets* 16(4), 2013, 712-740. Versión leída: Tinbergen Institute Discussion Paper TI 11-076/2/DSF.

## 2. Instrumento y muestra

Acciones del índice holandés; **un** creador de mercado de alta frecuencia identificado; **1.397
operaciones por acción por día**; 2007-2008, alrededor de la entrada de Chi-X. **Otro mercado, otra
época, otro agente.**

## 3. Los números, textual (p. 4 y p. 20)

> *"The gross profit per trade is €0.88 which is the result of a €1.55 profit on the spread net of fees
> and a €0.68 'positioning' loss. This loss decomposes into a €0.45 profit on positions of less than
> five seconds, but a loss of €1.13 on longer duration positions. The realized maximum capital
> committed due to margin requirements is €2.052 million per stock which implies an annualized Sharpe
> ratio of 9.35."*

> *"It earns an average €1416 per stock per day. The positioning loss is consistent across all stocks as
> the cross-sectional range is €−1.79 to €−0.07."*

## 4. (a) Qué transfiere al ES y qué no — con el estándar de "¿es el mismo objeto?"

| | **MECANISMO — transfiere** | **OBJETO — no transfiere** |
|---|---|---|
| la descomposición `ganancia = diferencial cobrado − pérdida de posición` | **es una identidad contable**: vale en cualquier mercado | los euros: 1,55 / 0,68 / 0,88 son de acciones holandesas con su tick y su diferencial de 2007-2008 |
| **el signo de la posición: NEGATIVO** | es selección adversa: la orden en reposo se llena cuando el precio está por moverse en contra. **Es lo que G midió en 3b sobre el ES** | la magnitud relativa 0,68/1,55 = 44 % es de ese mercado; G midió en el ES que la selección adversa devuelve "la mayoría" del medio-spread: **peor** |
| la ventaja del pasivo **decae con la tenencia**: gana en < 5 s, pierde en > 5 s | mecanismo: la información del flujo se incorpora en segundos; después sólo queda el inventario impuesto | **el umbral de 5 segundos es del objeto**: en el ES de 2019 la incorporación es más rápida (`H01` Hecho 1, < 200 ms) |
| **ganancia por operación chica × muchas operaciones = Sharpe alto** | la escala de F17: **Sharpe por operación ≈ 9,35 / √(1.397 × 252) = 0,016** *(derivación mía; supone independencia entre operaciones: **FRÁGIL**)* | 1.397 por día y el capital de €2,05 M son del objeto |
| **unanimidad entre acciones** (§6) | que la pérdida de posición sea negativa en TODAS las acciones dice que es estructura, no una acción rara | — |

**Por `F13`, nada de esto cuenta como evidencia sobre el ES en ninguna dirección.** Lo que cuenta es la
identidad contable y el signo, **y el signo ya está medido en la casa sobre el ES** (`9a02717`).

## 5. (b) ¿Es un argumento de cierre, o Roberto se adelanta? **Cierra, pero no por la premisa que usó.**

**La premisa de Roberto:** *"el profesional pierde en dirección y gana sólo en el diferencial; nosotros no
podemos cobrar el diferencial y estamos obligados a operar arriba de 10 s, que es justo donde él
pierde."* **Dos cosas están corridas, y corregirlas hace el cierre más fuerte, no más débil:**

1. **El creador de mercado no "apuesta en dirección" y pierde: SUFRE posiciones que otros le imponen.**
   Su pérdida de posición no es una apuesta fallida, es selección adversa: **alguien del otro lado
   sabía.** La −€1,13 en posiciones largas es **la ganancia de los agresores informados** —los que
   Brogaard, Hendershott y Riordan (`L14`) ven operar en la dirección de los cambios permanentes—.
   *"El profesional pierde en dirección"* es una lectura invertida: **el profesional pierde contra la
   dirección de otro que acertó.**
2. **La regla de 10 segundos es sobre NUESTRA tenencia, y la de 5 segundos es sobre la SUYA.** No nos
   pone "donde él pierde": nos pone donde **el agresor informado gana y el agresor desinformado pierde
   más**, porque ahí el precio continúa.

**Y entonces el cierre, con el número correcto:** **la ganancia bruta del creador de mercado por
operación ES la pérdida neta del tomador promedio por operación.** El tomador promedio paga €1,55 de
diferencial y recupera €0,68 de continuación: **−€0,88 por operación, en promedio, por identidad.**
Para que un tomador gane tiene que ser **más informado que el tomador promedio por más de €1,55**, o
sea recuperar en continuación más que el diferencial entero.

> ## **En nuestras unidades es exactamente la línea de `F17` y `D17`: un tick neto por operación. Menkveld no agrega el número —lo teníamos—; agrega que el número no es un umbral nuestro: es la contabilidad del otro lado. Lo que cerró no es "operar arriba de 10 segundos": es que ninguna medición de la casa ni ninguna publicación leída muestra una señal que nos haga mejores que el tomador promedio por un tick, y el tomador promedio pierde por identidad.**

**Dónde sí se adelanta Roberto:** al usar los euros y los 5 segundos como si fueran del ES. La
conclusión no los necesita.

## 6. (c) El rango entre acciones: −€1,79 a −€0,07. **Negativo en todas.**

**Ésa es la fuerza del hallazgo, no el promedio.** Un promedio negativo puede ser tres acciones
horribles y once neutras; un rango enteramente negativo es estructura. **Anotado así: la pérdida de
posición del proveedor de liquidez es negativa en cada acción de la muestra, sin excepción.**

## 7. (d) La tabla de Sharpes — coherente sólo si cada fila lleva su nivel de agregación

| quién | Sharpe anualizado | **nivel** | qué hace | fuente |
|---|---|---|---|---|
| Baltussen et al., la mejor del inventario viejo | 1,73 | **una estrategia, una cartera de índices** | paga el diferencial, 1 por día | `L01` |
| **Menkveld, el creador de mercado** | **9,35** | **un agente, UNA acción** | **cobra** el diferencial, 1.397 por día, colocado | `L13`, textual |
| Virtu | ~50 | **una FIRMA, miles de instrumentos** | cobra el diferencial | derivación de Roberto sobre el S-1, verificada 50,1 |
| **lo que exige la franja de 10-60 s** | **~257** | **una estrategia, un instrumento** | paga el diferencial | `D17` |

**La escala es coherente con una corrección:** Virtu no pertenece a la misma fila que Menkveld. Una firma
que corre muchos libros independientes suma Sharpe por diversificación: `50/9,35 = 5,4`, que son **~29
libros efectivamente independientes** —plausible para Virtu, y es aritmética, no ventaja—. **El comparador
correcto para la franja de `D17` —una estrategia, un instrumento— es Menkveld: 257 contra 9,35, 27
veces el mejor cobrador de diferencial documentado sobre un solo instrumento.** `D17` decía "cinco veces
Virtu"; **lo corrijo a 27 veces Menkveld, que es la comparación que corresponde.**

## 8. Veredicto

**No es candidata: es la contabilidad de la contraparte.** Entra al inventario como **hecho de
estructura** y como el número que explica por qué F17 y D17 dan lo que dan. **Consistencia externa de
mecanismo con 3a/3b de G sobre el ES; no confirmación de número. Siguen siendo cuatro.**

**Costos:** dinero cero, cartuchos cero, K en 261.
