# D07 — Las tres NO EVALUABLES, resueltas con cotas recuperadas

**VENTANA L. NO MIDE CANDIDATAS; corre CONTROLES DEL INSTRUMENTO desde el 2026-09-05 (rol ampliado por Roberto, ver `INDICE`). K sigue en 261.**

**La técnica es la de hoy:** de Baltussen saqué 25 puntos básicos por sesión a partir de un 3,96 %
anual que el paper no reporta en esas unidades. **Se aplica lo mismo a L04, L05 y L09.**

**Regla, la misma de `D06`: la cota es OPTIMISTA. Si ni así superan su umbral, están ciegas. Si lo
superan, pasan a "requiere medición" y a nada mejor.**

---

# L04 — Rebalanceo de ETF apalancados. **CIEGA.**

## La magnitud se recupera

**Barbon, Beckmeyer, Buraschi y Moerke (2022) publican una magnitud RELATIVA**, no absoluta:

> un aumento de un desvío estándar en los flujos de rebalanceo de los ETF apalancados sube el retorno
> de fin de día en un **430 % del retorno medio de la última media hora**.

**Ese "retorno medio de la última media hora" sí está medido en otro paper de esta carpeta.**
Baltussen et al., Tabla 6: la estrategia *Always Long* sobre la última media hora de futuros de
índice rinde **0,44 % anual**.

```
0,44 % / 252 sesiones  =  0,1746 pb por sesión
0,1746 × 4,30          =  0,751 pb  por desvío estándar de flujo
```

**Elección optimista declarada:** uso el retorno medio de la última media hora **medido sobre
futuros de índice**, y no el de acciones individuales que es el objeto de Barbon et al. Una
comprobación alternativa —repartir una prima de riesgo del 6 % anual entre trece medias horas— da
0,183 pb y un resultado de **0,79 pb**, prácticamente igual. **Tomo 0,79, el mayor de los dos.**

## El veredicto

| | |
|---|---|
| ventana | última media hora |
| `n` | 1.007 |
| `σ` optimista | 12,1 pb |
| **(a) detectable** | **1,143 pb** |
| **(b) publicada, recuperada** | **0,79 pb** |
| (c) esperada | 0,33 pb |

> ## **CIEGA con la magnitud ENTERA, por factor 1,45. Con el decaimiento, por 3,6.**

**Y hay que decir que el número recuperado es todavía optimista por dos motivos más:** es la magnitud
**por un desvío estándar de flujo**, o sea el día extremo y no el día promedio; y Barbon et al. la
miden sobre acciones individuales, donde el efecto de flujo es mayor que sobre el índice.

**Coherente con lo que ya sabíamos:** Ivanov y Lenkey concluyeron que el efecto sobre los retornos de
fin de día es **económicamente insignificante**, y la revisión de Lenkey (2024) que los efectos de
los ETF apalancados **disminuyeron con el tiempo**. **La cota recuperada dice lo mismo con un
número.**

---

# L05 — La gamma neta. **NO EVALUABLE COMO REGLA, y su máxima contribución posible no alcanza.**

## Por qué no tiene magnitud propia

**L05 no produce un retorno: es un eje de condicionamiento.** Su "magnitud" sería **la mejora que le
da a otra candidata**, y eso es un objeto distinto.

## Lo que SÍ se puede acotar

**Baltussen et al. publican el reparto: entre 1996 y mayo de 2020 hubo 2.930 días de gamma neta
negativa contra 3.158 de positiva**, o sea **48 % negativos**. Y la Tabla 7 dice que el momento
intradiario **persiste sólo cuando la gamma es negativa**.

**Supuesto máximamente favorable: que TODO el efecto de L01 viva en ese 48 % de días y que en el
resto sea exactamente cero.** Es el mejor caso concebible para el eje.

```
efecto total de L01   =  2,72 pb × 1.007 sesiones
concentrado en 48 %   =  2,72 / 0,48  =  5,67 pb  en cada uno de 483 días
```

| | sin condicionar | **condicionado por gamma, mejor caso** |
|---|---|---|
| `n` | 1.007 | **483** |
| magnitud | 2,72 pb | **5,67 pb** |
| (a) detectable | 1,143 | **1,652** |
| (c) esperada | 1,143 | **2,381** |
| **margen** | **1,00×** | **1,44×** |

## Y acá se cae

**Con la corrección del patrón en U de `A03` —factor 2,07 sobre el desvío de la última media hora—:**

```
(a) = 3,0 × 25,05 / √483 = 3,42        (c) = 2,381        →  CIEGA
```

> ## **El eje de gamma NO salva a L01. En el mejor caso concebible la lleva de la línea exacta a un margen de 1,44×, y la corrección del patrón en U se lo come entero.**

**Eso cierra una pregunta que estaba abierta desde `M02`:** si vale la pena reconstruir la gamma neta.
**Con este número, la respuesta es que ni en el mejor caso alcanza**, y por `F11` —una candidata que
sólo sirve para entender merece esfuerzo si su resultado cambia lo que hacemos— **el eje caro deja de
justificarse**.

**`M02`, la prueba barata de una tarde, sigue en pie**, porque su costo es cero y su resultado
informa sobre el eje que la VENTANA G ya tiene.

---

# L09 — Momento intradiario en el crudo. **NO EVALUABLE DEFINITIVA.**

## No hay nada convertible

Wen, Gong, Ma y Xu reportan que la estrategia *"genera ganancias sustanciales"* y **no publican
retorno anual, razón de Sharpe, estadístico t de la estrategia ni número de operaciones en unidades
que se puedan convertir a puntos básicos por evento.**

**Busqué en el resumen, en la ficha de RePEc y en la del editor. No hay número.**

## Pero se puede cerrar igual, con un trasplante declarado

**Le concedo la magnitud más grande de su propia familia: la de Gao et al., 6,67 % anual = 2,65 pb
por sesión.** Es un trasplante, no una cota del paper, y va marcado como tal.

**Y el crudo es más volátil que el S&P.** Con un desvío diario del orden del doble:

| | |
|---|---|
| `σ` de 30 min en CL, ≈ 2× el del ES | 24,2 pb |
| **(a) detectable**, n = 1.007 | **2,29 pb** |
| (c) esperada, con la magnitud trasplantada | **1,11 pb** |

> ## **CIEGA por factor 2,06 — a menos que el efecto en el crudo sea al menos DOS VECES mayor en términos porcentuales que el del S&P. El paper no da ningún número con el que verificarlo.**

**Se cierra como NO EVALUABLE DEFINITIVA**, con esa línea: **no es que no la evaluamos, es que su
paper no publica lo que haría falta, y bajo el único supuesto razonable disponible sale ciega.**

*(El factor 2 de volatilidad del crudo contra el ES es una **estimación mía: FRÁGIL**. Con un factor
1,5 el umbral bajaría a 1,72 y seguiría por encima de 1,11.)*

---

# EL CONTEO ACTUALIZADO DE LAS ONCE

| veredicto | cuántas | cuáles |
|---|---|---|
| **CIEGA** | **6** | L02, **L04**, L06, **L09**, L10, L11 |
| **REQUIERE MEDICIÓN REAL DEL DESVÍO** | **4** | L01, L03, L07, L08 |
| **NO EVALUABLE COMO REGLA** | **1** | L05, con su contribución máxima acotada e insuficiente |

**De once, seis están cerradas con número.** Las cuatro que quedan están bloqueadas: dos esperando el
perfil de volatilidad intradiaria de la VENTANA G, y dos esperando una decisión de compra que no es
mía.

**Y las dos que esperan el perfil —L01 y L03— ya tienen su signo de riesgo escrito en `A03`: la
medición pendiente va a mover el número en su contra.**
