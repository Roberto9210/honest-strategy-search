# M02 — La prueba de una tarde antes de gastar semanas

**VENTANA L. NO MEDIDO. Escrito para que la VENTANA G lo ejecute tal cual. K sigue en 261.**

## La pregunta, en una frase

La literatura dice que el eje que separa los días en que el momento intradiario existe de los días
en que no **es el signo de la gamma neta de los creadores de mercado**. Reconstruir ese eje cuesta
semanas de recolección de datos de opciones. **La VENTANA G ya tiene un eje construido y validado.
¿Sirve el barato como sustituto del caro?**

## Por qué la pregunta tiene sentido y no es una analogía suelta

Los dos ejes están conectados por la propia teoría que proponen los papers. Si los intermediarios
están cortos de gamma tienen que **operar a favor del movimiento** para mantenerse neutrales, y eso
**amplifica la volatilidad**. La gamma corta no es sólo un predictor del momento: es una causa
declarada de la volatilidad alta.

**Si esa cadena es cierta, los días de gamma negativa tienen que estar sobrerrepresentados en el
tercil alto de volatilidad. Y entonces el eje barato lleva información sobre el caro.**

## Qué predicen los papers, con números publicados

| fuente | predicción |
|---|---|
| Baltussen, Da, Lammers y Martens (2021), Tabla 7 | el momento intradiario **persiste sólo cuando la gamma neta es negativa** |
| Huang, Tsai, Weng y Yang (2023), futuros de VIX | idéntico, en un mercado sin relación |
| Barbon, Beckmeyer, Buraschi y Moerke (2022) | gamma muy negativa → momento; gamma muy positiva → **reversión** |
| **Gao, Han, Li y Zhou (2018), Tabla 3 Panel A** | **por tercil de volatilidad**: R² de **0,6 %** en el bajo con coeficiente **no significativo**, y **3,3 %** en el alto |

**La última fila es la clave: la predicción condicionada por volatilidad ya está publicada, con
números.** No hay que inferirla de la teoría. Gao et al. la midieron y ese es el patrón contra el que
se compara.

---

# LA ESPECIFICACIÓN

## Datos

**Ninguno nuevo. Todo está en el repo.**

- ES 1-min Databento **2016-01-01 → 2019-12-31**, 1.357.785 barras, 1.007 sesiones de contrato único.
- El eje de régimen **ex-ante** de la VENTANA G: terciles de volatilidad de la **sesión anterior**, en
  puntos básicos, ya construido y verificado en `juez_regimen_bps.py` y `juez_regimen_exante.py`.

**Respuesta directa a la pregunta de Roberto: no hay que comprar nada.** Ver la sección final para
qué compraría el eje caro si esta prueba sale inconclusa.

## Qué se calcula

Una sola regresión, corrida tres veces, una por tercil:

```
Para cada sesión t de 2016-2019:
    rROD(t)  = retorno desde el cierre de t-1 hasta 30 minutos antes del cierre de t
    rLH(t)   = retorno de la última media hora de t
    tercil(t) = tercil de volatilidad de la sesión t-1, en puntos básicos   [YA EXISTE]

Dentro de cada tercil g:
    rLH(t)  =  a_g  +  b_g · rROD(t)  +  e
```

Se reportan `b_g`, su estadístico t con errores a la Newey-West, y el R² por tercil. **Nada más. No
hay operaciones, no hay bracket, no hay costos, no hay veredicto.**

## Los tres resultados posibles, declarados antes de mirar

| resultado | qué significa | qué hacer |
|---|---|---|
| **`b_g` monótono creciente, y en el tercil bajo no significativo o negativo** | el eje barato reproduce el patrón publicado por Gao et al. y es compatible con la historia de gamma | **el eje barato sirve como sustituto.** No se compra el caro |
| **`b_g` plano entre terciles** | la volatilidad no lleva información sobre el régimen que gobierna el efecto | el eje barato **no** sustituye al caro. Ahí sí hay que decidir si se compra |
| **`b_g` monótono pero decreciente** | contradice a Gao et al. sobre el ES en este período | resultado en sí mismo, y hay que entenderlo antes de seguir |

**La condición de falla está escrita antes: si `b_g` es plano, el eje barato no sirve, y decirlo es el
resultado.**

## Los controles, y hacen falta tres

**Control 1 — placebo de partición.** Repartir las 1.007 sesiones en tres grupos **al azar** en vez de
por volatilidad, y repetir. Los tres `b_g` tienen que ser indistinguibles entre sí. Si una partición
al azar produce una separación parecida a la del eje de volatilidad, lo que se está midiendo es ruido
de submuestra.

**Control 2 — el eje tiene que ser ex-ante.** Correrlo también con la volatilidad de la **sesión
entera**, que la VENTANA G ya llama *hindsight* y usa sólo para describir. Si el patrón aparece con
hindsight y no con ex-ante, **no es un régimen conocible al entrar** y no sirve para nada operable.
Los dos resultados se publican con su nombre, como ya hace el juez.

**Control 3 — reproducir la referencia.** El `b` global sin condicionar tiene que dar del orden del
**5,98** publicado por Baltussen et al. para el índice S&P 500. Si el global no se parece, hay un
error de construcción y los terciles no significan nada.

## Qué NO prueba

- **No prueba que haya ventaja.** No hay operaciones ni costos.
- **No prueba que el mecanismo sea la gamma.** Prueba si el eje barato separa igual que el caro
  separaría **si la cadena teórica fuera cierta**. Un resultado positivo es compatible con la historia
  de gamma; no la demuestra.
- **No reemplaza a M01-d.** Aquélla mide la reversión, que es la firma que distingue presión de
  precio de información. Ésta mide si el régimen se puede etiquetar barato. Son dos preguntas.

## ¿Gasta cartucho?

**Argumento de que no, con la misma forma que usaron la Compuerta 1 y el censo de instrumentos:** no
se busca una ventaja, no hay estadístico contra un α para elegir entre candidatas, y no se decide
nada sobre operar. Se mide si dos etiquetas de régimen coinciden.

**Y la condición que lo convierte en gasto, dicha antes:** si el resultado se usa después para elegir
en qué tercil medir una candidata, **entonces sí seleccionó**. La forma de evitarlo es declarar el
tercil antes de correr el juez, y esa declaración es independiente de esta prueba.

**Quien lo ejecute tiene que sostener ese argumento en su propio pre-registro, no citarme a mí.**

---

# Qué compraría el eje caro, si esta prueba sale plana

**Sólo si `b_g` sale plano hace falta el eje caro, y ahí la pregunta pasa a ser de presupuesto.**

**Qué haría falta:** interés abierto por strike y vencimiento de las opciones SPX, diario, 2016-2019,
para reconstruir la exposición neta a gamma con la ecuación 15 de Baltussen et al.

**De dónde:**

| fuente | qué es | costo |
|---|---|---|
| OptionMetrics | lo que usaron los autores hasta 2017 | suscripción académica, **cara** |
| SqueezeMetrics | lo que usaron para 2018-2020 | producto comercial |
| Cboe, interés abierto de SPX | reconstrucción propia | recolección, **semanas de trabajo, no una descarga** |

**Ninguna de las tres está cotizada en este repo.** Cotizarlas es un paso previo, del mismo tipo que
la cotización de microestructura que la VENTANA G ya hizo con Databento.

**Y qué contestaría esa compra, en una línea:** si el momento intradiario del ES vive sólo en los días
de gamma negativa, como está publicado en dos mercados sin relación. **Si la respuesta fuera que sí,
el efecto no se mediría contra 1.007 sesiones sino contra las ~490 de gamma negativa** —el reparto
publicado es casi mitad y mitad, 2.930 días negativos contra 3.158 positivos entre 1996 y 2020— **y
esa reducción de muestra empeora la potencia, no la mejora.**

**Eso es lo incómodo y va escrito acá: el eje caro puede confirmar el mecanismo y al mismo tiempo
dejar la candidata menos medible que antes.** Es exactamente la interacción que quedó anotada sin
resolver en L02 entre el efecto y el piso, y aparece otra vez con otro eje.
