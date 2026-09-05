# PROTOCOLO — cómo medir un candidato sin caer en la trampa de la censura

**Escrito 2026-09-04. Activo permanente, no nota de una tanda.** Si estás leyendo esto sin haber
vivido esa semana: lo único que hace falta saber está acá.

---

## El problema, en una frase

**Si medís la tasa de acierto de una estrategia contando solo las operaciones que se cerraron, el
resultado sale inflado — y sale inflado justo en la dirección de hacer parecer bueno lo que no lo es.**

## Por qué pasa

Una operación con objetivo y stop termina de tres maneras, no de dos: toca el objetivo, toca el
stop, **o sigue abierta cuando se te acaba el tiempo**. Esa tercera no es rara: medida sobre ES a un
minuto con entradas al azar, **entre el 7% y el 35% de las operaciones no resuelve dentro de la
sesión**.

Y no se quedan abiertas al azar. **Se quedan abiertas las que iban a la barrera lejana**, porque
llegar lejos lleva más tiempo. Entonces, si las descartás, estás descartando selectivamente un lado.

## El número medido

ES 1-min Databento 2016-2019, entradas al azar, horizonte de una sesión:

| bracket | asumido `S/(S+T)` | medido sobre resueltas | **sesgo** | sin resolver |
|---|---|---|---|---|
| 5pt:10pt | 66,7% | 68,2% | **+1,65** | 7,1% |
| 10pt:10pt | 50,0% | 50,0% | **+0,00** | 18,7% |
| 20pt:10pt | 33,3% | 27,3% | **−5,82** | 35,2% |
| 5pt:20pt | 80,0% | 85,2% | **+4,93** | 17,3% |
| 10pt:20pt | 66,7% | 72,7% | **+5,82** | 35,2% |

Para dimensionarlo: el criterio que esta ventana estaba tratando de validar pedía una ventaja de
**+1,2 puntos**. El sesgo lo supera hasta por **4,8×**. **Un candidato de pura suerte medido así
reporta +5 puntos y se aprueba.**

## La regla

El sesgo **no** depende solo de la asimetría del bracket. `5pt:10pt` y `10pt:20pt` tienen exactamente
la misma asimetría (−0,333) y sesgos de +1,65 y +5,82. Lo que los separa es cuánto quedó sin
resolver. La forma que ajusta, con error medio de 0,42 puntos sobre 15 celdas medidas:

```
sesgo (puntos)  ≈  −0,5 × asimetría × (% sin resolver)

donde   asimetría = (T − S) / (T + S)
```

**El sesgo se anula por dos caminos independientes:** asimetría cero, o sin-resolver cero. Por eso
«usá brackets simétricos» **no** es la regla — es solo uno de los dos caminos.

Para mantener el sesgo por debajo de 0,5 puntos hace falta `|asimetría| × (% sin resolver) ≤ 1`:

| si tenés… | podés permitirte |
|---|---|
| 5% sin resolver | asimetría ≤ 0,200 → T/S entre 0,67 y 1,50 |
| 10% sin resolver | asimetría ≤ 0,100 → T/S entre 0,82 y 1,22 |
| 20% sin resolver | asimetría ≤ 0,050 → T/S entre 0,90 y 1,11 |
| 35% sin resolver | asimetría ≤ 0,029 → T/S entre 0,94 y 1,06 |

## Horizonte mínimo, medido y no supuesto

Sesgo en puntos por horizonte:

| bracket | 1 sesión | 2 sesiones | 5 sesiones | ¿baja de 0,5? |
|---|---|---|---|---|
| 10pt:10pt | +0,00 | +0,00 | +0,00 | **desde 1 sesión** |
| 5pt:10pt | +1,65 | +1,26 | +0,22 | **5 sesiones** |
| 20pt:10pt | −5,82 | −2,71 | −1,96 | ni a 5 |
| 5pt:20pt | +4,93 | +2,51 | +1,27 | ni a 5 |
| 10pt:20pt | +5,82 | +2,71 | +1,96 | ni a 5 |

**Tres de los cinco no llegan ni con cinco sesiones de horizonte.**

## Qué hacer

### 1. NO descartes las que no resolvieron. Nunca.

Es el error. Descartarlas es exactamente lo que produce el sesgo.

### 2. Cerralas a valor de mercado en el corte, y contá ese resultado

Es lo que hace un operador real cuando aplana al cierre. Es la opción por defecto porque **mide lo
que efectivamente pasa**, no una idealización. Una operación que quedó −7pt cuenta como −7pt, no
como «no cuenta».

### 3. Reportá siempre la banda, además del punto

Con `g` ganadas, `p` perdidas y `u` sin resolver, las dos cotas son:

```
peor caso:  g / (g + p + u)          (todas las abiertas terminan mal)
mejor caso: (g + u) / (g + p + u)    (todas las abiertas terminan bien)
```

Si la banda es más ancha que la ventaja que el candidato dice tener, **la medición no alcanza** y no
importa dónde caiga el punto.

### 4. Reportá siempre el % sin resolver, al lado de la tasa

Una tasa de acierto sin su fracción sin resolver es un número que no se puede auditar. Si un
candidato te trae una tasa y no te trae esa fracción, pedísela antes de mirar nada más.

### 5. Alargar el horizonte arregla la estadística, no la economía

Podés bajar el sin-resolver estirando el horizonte. **Pero eso significa aguantar la posición de un
cierre al siguiente**, y eso está medido aparte: contra un drawdown de $2.000 con un E-mini, la
cuenta muere entre el **42% y el 68% de las veces en diez noches, sin operar ninguna estrategia**
(ver `CRITERIO_RESULTADO.md`, Compuerta 1). **El arreglo del sesgo compra un riesgo real.** No es
gratis y hay que decidirlo, no aplicarlo por default.

## La advertencia que importa

**Este sesgo tiene dirección, y es la peligrosa.**

Cuando el objetivo está más cerca que el stop —que es la configuración de «ganar poco y seguido»,
la más común en estrategias que se ven bien en un backtest corto— las que quedan abiertas son las que
iban al stop lejano. Descartarlas **borra pérdidas** y el resultado sale mejor de lo que es.

No es ruido simétrico que se promedia. **Empuja siempre hacia aprobar.** Un error que empuja hacia
rechazar te cuesta una oportunidad; este te cuesta plata puesta en algo que no funciona.

## Lista de control, para pegar al lado de cualquier evaluación

- [ ] ¿Está reportada la fracción sin resolver?
- [ ] ¿Las sin resolver están contadas a valor de mercado en el corte, y no descartadas?
- [ ] ¿Está reportada la banda peor caso / mejor caso?
- [ ] ¿La banda es más angosta que la ventaja que el candidato afirma?
- [ ] `|asimetría| × (% sin resolver) ≤ 1`?
- [ ] Si se alargó el horizonte para bajar el sin-resolver, ¿está contado el riesgo de aguantar de un cierre a otro?

---

*Medido en `linea_base.py` y `censura_regla.py`. Salidas en `salida_linea_base.txt` y
`salida_censura_regla.txt`. Control: bracket de 23pt a cada lado → ambigüedad 0,000% y tasa pooled
exactamente 50,0%.*

---

# SEGUNDA PARTE — EL MÉTODO: dólares por sesión, no tasas de acierto

**Escrito 2026-09-04, después de medirlo. Activo permanente.** Esto no es un anexo: es el mismo
problema de la primera parte visto una vez más, y la solución que lo cierra. **La censura era un
síntoma. La enfermedad era medir en tasas.**

## Por qué se abandona el marco de tasas

Medir una estrategia por su tasa de acierto obliga a compararla contra una tasa «sin ventaja». Esa
tasa nula **no es una constante**: depende de cuatro cosas, todas medidas en esta ventana, y
**ninguna de ellas es una propiedad de la estrategia.**

| perilla | cuánto mueve la nula | dónde se midió |
|---|---|---|
| **horizonte y trato de las no resueltas** (censura) | hasta **6,08 puntos** | `salida_linea_base.txt` |
| **estructura serial** del precio (agrupamiento de volatilidad) | **1,3–2,9 puntos** | `salida_bloques.txt` |
| **forma asimétrica de la barra** | **0,34–0,78 puntos** | `salida_sep_nula.txt` |
| **sobrepaso de barrera** | **0,5–1,1 puntos** | `salida_sintetico.txt` |

**El efecto que se buscaba era 1,2 puntos.** Tres de las cuatro perillas son de ese tamaño o más
grandes. Por eso el marco de tasas no podía dar una respuesta estable: cada vez que se medía mejor
una perilla, la conclusión se movía.

## El marco nuevo, en tres reglas

**1. Se suman DÓLARES, no aciertos.** Cada operación aporta su resultado en dinero, con la comisión
medida y el deslizamiento medido ya adentro.

**2. Ninguna operación se descarta. La que sigue abierta al corte se marca a mercado** y ese número
entra en la suma. Es la regla de la primera parte de este protocolo, ahora obligatoria y no
opcional.

**3. La unidad de tiempo es la SESIÓN**, que es además la unidad en la que las firmas miden el
drawdown, el objetivo y los días mínimos. Las operaciones van **secuenciales**: una por vez, la
siguiente se abre después de que cerró la anterior.

## Qué arregla, con número

- **Las cuatro perillas desaparecen.** No hay tasa nula que calibrar: el punto de comparación es
  cero dólares.
- **No hay censura**, por la regla 2.
- **El error estándar se vuelve honesto.** Las operaciones secuenciales **no se pisan**, así que
  cada sesión es una observación independiente de verdad. Verificado: el error entre sesiones de una
  serie contra la dispersión entre 10 series independientes da cociente **1,29 y 0,73**. En el marco
  de tasas ese mismo cociente llegaba a **5,3**.

## Lo que NO arregla, y hay que restarlo

**El marco nuevo tiene UN sesgo propio, y está medido.** El control lo destapó: sobre datos sin
ventaja y costo cero da −$10,77 y +$5,75 por sesión en vez de cero.

Es **sobrepaso de barrera de contabilidad**: el precio *cruza* la barrera, no la toca, pero se anota
exactamente `+T` o `−S`. Por paro opcional el sesgo por operación vale `o·(1−2p)` con
`p = S/(S+T)`. Medido con cinco brackets de igual span:

**`o = 0,0642 puntos = 0,26 ticks = $3,21 por operación por mini`**, con `R² = 0,986` y ordenada al
origen `−0,0004`.

**Cómo se usa:** el sesgo se calcula con la fórmula, se resta, y listo. **La diferencia con las
cuatro perillas del marco viejo es que éste es UNO, se calcula desde la geometría del bracket, tiene
signo predecible y es chico frente al efecto** (19% en 5pt:20pt, 5% en 20pt:10pt).

*Corrección a mí mismo: dije que este marco «no tiene nula que calibrar, cero es cero». **Es falso.**
Tiene una, chica y computable. La afirmación correcta es: pasa de cuatro perillas incontrolables a
un término que se resta.*

## La combinación antitética: para qué sirve y para qué no

Promediar largo y corto reduce el desvío **5,0× y 8,4×** porque los dos lados están
anticorrelacionados. **Sirve para medir la esperanza de una entrada al azar.** **No sirve para
dimensionar a un candidato direccional**, que elige lado y enfrenta el desvío de un lado solo
(≈$1.050 y ≈$1.072 por sesión, contra $210 y $128 del combinado).

**Hay que decir siempre cuál de las dos se está usando.** Cambia la MDE por un factor de 5.

## La receta, para pegar al lado de cualquier candidato

1. Replay **secuencial** sobre la muestra, una posición por vez.
2. Resuelta → `±T` o `−(S + exceso medido)`. **Abierta al corte → marca a mercado.** Siempre menos
   la comisión medida.
3. Sumar por **sesión**. Media y desvío **entre sesiones**.
4. **Restar el sesgo del marco:** `o·(1−2p)·$50·(operaciones por sesión)`, con `o = 0,0642`.
5. Comparar contra **cero**. No hay otra nula.
6. Declarar si la varianza es **antitética** o **de un lado**, y calcular la MDE con la que
   corresponda.
7. **Control obligatorio**, y tiene que poder fallar *y* poder pasar: correr lo mismo sobre
   bootstrap sin drift con costo cero. Debe dar cero dentro de su error. Para demostrar que el
   control discrimina, correrlo también con el defecto viejo puesto a propósito (descartar las
   abiertas): **ése tiene que fallar**. Si pasan los dos, el control no mide nada.

## Los números de referencia, ES 2016-2019, 1 mini

Entradas **al azar**, o sea sin ventaja ninguna. Neto de comisión y deslizamiento medidos, con el
sesgo del marco ya restado:

| celda | $/sesión | operaciones/sesión | $/operación | piso que hay que superar |
|---|---|---|---|---|
| 5pt:20pt | **−44,64** | 5,53 | −10,00 | **+$44,64 por sesión** |
| 20pt:10pt | **−71,71** | 3,13 | −21,87 | **+$71,71 por sesión** |

Y el detalle por lado, que el combinado esconde:

| celda | largo | corto |
|---|---|---|
| 5pt:20pt | −$2,36 (−0,1 errores) | −$108,23 (−3,3 errores) |
| 20pt:10pt | −$3,29 (−0,1 errores) | −$133,44 (−3,9 errores) |

**Procedencia:** `dolares_por_tiempo.py`, `sesgo_marco.py`, `dolares_lados.py`. Salidas en
`salida_dolares.txt`, `salida_sesgo_marco.txt`, `salida_dolares_lados.txt`.

---

# TERCERA PARTE — el piso es del CANDIDATO, y se saca por permutación

**Escrito 2026-09-04. Activo permanente.** La segunda parte dejó un piso de referencia calculado
con **entradas al azar**. Eso no es el piso de un candidato: un candidato entra condicionado y su
piso es otro. Esta parte lo arregla y **reemplaza al paso 5 de la receta anterior**.

## La regla

**El piso de un candidato se calcula con las entradas del propio candidato, permutadas.** Nunca con
entradas al azar, y nunca contra cero pelado.

## Las dos nulas, y cuándo va cada una

| nula | qué hace | qué conserva **exacto** | qué destruye | para qué sirve |
|---|---|---|---|---|
| **A — rotación** | corre `(ranuras, lados)` sobre la grilla | conteo, espaciado, secuencia de lados | **cuándo** | probar que el *momento* de entrada lleva información |
| **B — signo** | da vuelta los lados al azar | ranuras, **tenencia**, **fracción abierta**, conteo | **qué lado** | probar que la *dirección* lleva información |

**Van las dos, siempre.** Y hay que decir esto sin adornar: **para una señal que depende del precio
es imposible conservar la tenencia bajo una permutación temporal**, porque la tenencia la produce
el precio. Medido sobre un candidato de volatilidad baja: al rotar, la tenencia cae de **511 a 399
barras** y las abiertas de **35,0% a 30,6%**. Si eso pasa, la nula que manda es la **B**.

## Validado contra candidatos de propiedades conocidas

- **Sin ventaja, con patrón distinto** (opera 3× menos, aguanta 30% más): ventaja hallada **+0,87
  con desvío 12,49 — 0,1 desvíos**. Cero.
- **Con ventaja inyectada**: recuperada al **100% y 101%, a 0,0 desvíos**.

**Resolución del test: ±33% de la ventaja con 4.994 operaciones.** «Recupera» quiere decir «dentro
de esa resolución».

## Dos trampas, las dos ya pisadas

**1. Comparar contra la esperanza en vez de contra lo realizado.** La ventaja *nominal* inyectada
era $116,87/sesión; la *realizada en ese sorteo* fue $72,69. Comparando contra la nominal el test
parecía recuperar el **62%** y fallar a −1,8 desvíos; contra la realizada recupera **100%**.
**Siempre que se inyecte algo, calcular lo que se inyectó de verdad, no lo que se quería inyectar.**

**2. Confundir cuál mitad del control informa.** Que la nula B recupere una inyección *direccional*
está casi forzado por construcción, porque la inyección se define contra el promedio de los dos
lados, que es lo que B estima. **La que informa es la A**, y que las dos den cero en los candidatos
sin ventaja.

## El piso no es un número: es un número por régimen

Medido por año calendario sobre 5pt:20pt, el piso va de **$3,49 (2017) a $106,03 (2018)**: un
factor de **30**. El $42,93 de referencia es el promedio de 2016-2019.

**Cualquier piso que se publique tiene que decir sobre qué régimen de volatilidad se calculó.** Un
candidato medido en un año tranquilo enfrenta un piso treinta veces más bajo que en uno agitado, y
comparar los dos números sin la aclaración es un error.

## Correcciones a las partes anteriores

- **El paso 5 («comparar contra cero») queda reemplazado** por: comparar contra la nula de
  permutación del propio candidato, con las dos nulas.
- **Los cortes de sesión reales contra bloques fijos de 1.380 barras:** el piso se mueve **−$1,71 y
  +$1,22** contra errores de $6,69 y $4,09. **Inocuo.** Igual, de acá en adelante van los cortes
  reales; el piso de referencia es **+$42,93** (5pt:20pt) y **+$72,93** (20pt:10pt).
- **Sobrepaso y deslizamiento de entrada NO son el mismo término.** Verificado inyectando un tick
  entero de deslizamiento: la pendiente del sobrepaso se mueve **+0,0000** y la ordenada **−0,2500
  exacto**. Se restan los dos, por separado, sin miedo a contar dos veces.

**Procedencia:** `permutacion.py`, `doble_conteo.py`, `cortes_y_tramo.py`. Salidas en
`salida_permutacion.txt`, `salida_doble_conteo.txt`, `salida_cortes.txt`.
