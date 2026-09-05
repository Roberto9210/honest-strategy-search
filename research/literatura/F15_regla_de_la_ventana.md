# F15 — LA REGLA DE LA VENTANA: qué forma debe tener una candidata antes de que exista

**VENTANA L. NO MIDE NADA. K sigue en 261. Regla de DISEÑO, no de descarte.**

> ## EL ENUNCIADO
>
> **La detectabilidad de una candidata depende de su efecto contra el ruido de LA VENTANA EN QUE
> VIVE, no contra el ruido del día.**
>
> **Entre dos formas de la misma idea, preferir aquella cuya ventana sea la más CORTA que todavía
> contenga el efecto entero.**

---

# 1. La matemática que lo sostiene

Para una candidata con `n` eventos, efecto `m` y ventana de `T` minutos dentro de una sesión de
`T_día`:

```
σ(T)      ≈  σ_día · √(T / T_día)                   raíz del tiempo
m_det     =  t* · σ(T) / √n        ∝  √T            lo que hace falta para verlo
```

**El umbral crece con la RAÍZ del largo de la ventana. Lo que decide es cómo crece el efecto.**

| si el efecto es… | `m` crece como | `m / m_det` crece como | qué conviene |
|---|---|---|---|
| **CONCENTRADO** — ocurre en un instante o en un tramo fijo | **constante** | **`1/√T`** | **acortar la ventana** |
| **DIFUSO** — se acumula parejo a lo largo de la ventana | `T` | `√T` | **alargar la ventana** |

**La regla no es "ventanas cortas siempre". Es: la forma de la ventana tiene que seguir a la forma
del efecto.**

## La pregunta que decide, en una línea

> **¿El efecto es un SALTO o es una DERIVA?**

**Un salto** —un flujo obligatorio que se ejecuta a una hora, una publicación, una liquidación— pide
la ventana más angosta que lo contenga. **Una deriva** —una prima de riesgo que se devenga mientras
uno está expuesto— pide la ventana completa en la que se devenga.

---

# 2. El caso que la descubrió

**L10, el rebalanceo institucional de fin de mes.**

| | |
|---|---|
| dónde ocurre el flujo | **cerca del cierre del último día hábil**. Es un SALTO |
| ventana que usa la regla publicada | **el retorno del día siguiente, de cierre a cierre: 1.380 minutos** |
| magnitud publicada | 17,0 pb |

**Paga el ruido de una sesión entera para capturar un flujo que se ejecuta en la última hora.**

| ventana | `σ` | **(a) detectable**, n = 46 | (b) = 17,0 | veredicto |
|---|---|---|---|---|
| sesión completa, 1.380 min | 82,8 medido | **36,63 pb** | 17,0 | **CIEGA por 2,15×** |
| última hora, 60 min | ≈ 17,1 | **7,56 pb** | 17,0 | **sobreviviría con margen 2,25×** |

> ## **La misma idea, con la ventana correcta, pasa de ciega a sobreviviente. El factor es 4,8, y sale sólo de dejar de pagar ruido que no compra señal.**

**Y no es un error de los autores:** ellos miden un efecto sobre retornos diarios porque su pregunta
es el costo del rebalanceo para los inversores, no una estrategia. **El error es NUESTRO al adoptar
su ventana sin preguntarnos si era la nuestra.**

---

# 3. EL CONFLICTO, que es la parte que hay que resolver antes de usar la regla

**Esta regla de diseño choca de frente con el criterio de reglas de terceros.**

| regla | dice |
|---|---|
| **F15**, ésta | usá la ventana más corta que contenga el efecto |
| **F9** y el criterio de `P01` | no cambies la regla del paper; si la pieza la ponemos nosotros y tiene grado de libertad, es hipótesis nuestra |

**Acortar la ventana de L10 de una sesión a una hora es exactamente el grado de libertad que `F9`
prohíbe: ¿última hora? ¿últimos treinta minutos? ¿últimas dos horas? Cada respuesta es nuestra.**

## La resolución, declarada

| situación | qué manda |
|---|---|
| **diseñamos nosotros la candidata** | **manda `F15`.** La ventana se elige por la forma del efecto, y esa elección se declara antes |
| **probamos la regla de un tercero** | **manda `F9`.** Se usa la ventana del paper, aunque sea la equivocada |
| **el paper mismo ofrece varias ventanas** | se usa la que el paper presenta como principal, y las otras suman a `variantes_probadas` |

> ## **Consecuencia que nadie había puesto precio: usar reglas de terceros nos obliga a heredar sus ventanas, y sus ventanas están elegidas para su pregunta y no para la nuestra. Ése es un costo del generador externo que no estaba contabilizado.**

**No lo dice para abandonar el generador externo.** Lo dice para saber que **una candidata de tercero
llega con una desventaja estructural** que una candidata propia no tiene, y que hay que sumarla al
lado de las ventajas que sí tiene.

---

# 4. QUÉ FORMA PREFERIR, de ahora en adelante

**Cuando una idea admite las dos formas, y la elección es nuestra:**

1. **Identificar cuándo ocurre el efecto**, no cuándo es cómodo medirlo. Si hay un mecanismo
   declarado, el mecanismo dice la hora: un flujo obligatorio ocurre cuando la regla obliga; una
   publicación, cuando se publica.
2. **Elegir la ventana más angosta que lo contenga entero**, con margen para el error de
   sincronización, y no más.
3. **Declarar la ventana antes de mirar nada**, porque el ancho es un grado de libertad.
4. **No acortar más allá de donde el efecto termina.** Cortar dentro del efecto pierde señal y el
   cociente empeora en las dos puntas.
5. **Si el efecto es una deriva, no acortar.** La regla se invierte.

## La contracara, que hay que escribir para que no se use mal

**Acortar la ventana no aumenta la ganancia en dólares: la deja igual y baja el ruido.** Los costos
de operar **no bajan** al acortar, así que **el cociente contra el piso de rentabilidad no mejora**.

> **`F15` mejora la DETECTABILIDAD, no la RENTABILIDAD.** Una candidata que con la ventana correcta
> se vuelve medible puede seguir sin superar el costo de operarla. **Son las dos preguntas que `F6`
> ya separa, y esta regla toca sólo una.**

---

# 5. Lo que esta regla NO explica, y hay que verificar aparte

**El escalado por raíz del tiempo supone volatilidad intradiaria uniforme, y no lo es.** El patrón en
U hace que una ventana pegada a la apertura o al cierre tenga más ruido del que la fórmula dice
(`A03`).

**Eso NO invalida la regla —el efecto de acortar sigue dominando— pero cambia los números.** Una
ventana de treinta minutos en el pico de la mañana no tiene el ruido de una ventana de treinta
minutos del mediodía.

**La forma correcta de la regla, una vez que exista el perfil medido, es usar el ruido REAL de esa
ventana en vez del escalado por raíz.** Hasta entonces, la regla ordena bien y calibra mal.
