# P01 — PRE-REGISTRO de la PRUEBA AGRUPADA de reglas de calendario de terceros

**VENTANA L. NO CORRIDO. NO PRE-REGISTRADO TODAVÍA. K sigue en 261.**

> **ESTE DOCUMENTO NO GASTA CARTUCHO. CORRERLO SÍ.**
> Sería el primer cartucho desde agosto y **K pasaría de 261 a 262**. La decisión es de Roberto y se
> toma con este diseño en la mano. Mientras este documento no esté commiteado y la corrida no se
> haya hecho, no hay pre-registro: hay un borrador de pre-registro.

**Por qué existe:** ninguna candidata del inventario alcanza sola la vara del juez. Agrupar ataca los
dos problemas a la vez, porque **una sola hipótesis con muchos eventos baja la multiplicidad y sube
la potencia en el mismo movimiento**.

---

# 0. Corrección previa, y hay que leerla antes que nada

En entregas anteriores publiqué factores de "falta" anclados a la tabla de MDE de
`salida_piso_ventaja.txt`. **Esa tabla está calculada para brackets**, y yo mismo lo dejé escrito en
`FILTROS.md`: *"sirve para ordenar y para descartar por factores de 2 o más; no para decidir un
empate."* Las candidatas de este pre-registro **no usan bracket**: miden un retorno en una ventana
declarada.

**El ancla correcta es el desvío del retorno en la ventana de cada candidata, no la MDE de un
bracket.** Recalculado así, los factores cambian. La conclusión de fondo **no** cambia —ninguna
alcanza sola— pero los números sí, y los corrijo acá en vez de arrastrarlos.

| candidata | factor publicado antes | **recalculado con el ancla correcta** |
|---|---|---|
| L11 | 1,9× | **1,7×** |
| L10 | 2,1× | **2,3×** |
| L08 | 28× | **0,9×** — *sola ya casi alcanza, como panel de diez monedas* |

**El cambio grande es L08**, y viene de que su prueba es un panel de diez monedas: 480 observaciones
en vez de 48 operaciones. Los factores viejos la trataban como si operara una moneda.

---

# a) CUÁLES CINCO, Y POR QUÉ ESAS

## El criterio de inclusión, declarado ahora y cerrado

Entra una candidata si y sólo si el paper publicado por terceros contiene **las tres cosas**:

1. **FECHA.** Una regla de calendario externa y escrita que fija **cuándo** ocurre el evento,
   conocible con un año de anticipación, y que **no ocurre todas las sesiones**.
2. **SIGNO.** Una regla que fija la dirección usando **sólo información disponible antes del
   evento**.
3. **MAGNITUD.** Un número publicado, con su dispersión o su estadístico, en unidades convertibles.

**Las tres tienen que estar EN EL PAPER. Si una la ponemos nosotros, la candidata no entra**, porque
entonces la regla ya no es de un tercero y el ejercicio pierde todo su sentido.

## Aplicación del criterio

| candidata | fecha | signo | magnitud | **entra** |
|---|---|---|---|---|
| **L11** Savor y Wilson | calendario de anuncios macro | **siempre largo** | 10,3 pb | **SÍ** |
| **L10** Harvey et al. | último día del mes | signo del desvío acciones contra bonos | 17 pb por desvío | **SÍ** |
| **L08** Melvin y Prins | último día hábil, 16:00 Londres | signo del retorno bursátil del mes | coef. 0,0142 | **SÍ** |
| **L07** Ito y Yamada | días *gotobi* | compra de moneda extranjera, sesgo declarado predecible | **"varios puntos básicos"** | **CONDICIONAL** |
| **L03** Kurov et al. | calendario de publicaciones | **NO** | 5,4 a 10,4 pb | **NO** |

### Las dos exclusiones, con su motivo, cerradas ahora

**L03 queda AFUERA, y es la que más duele.** Es determinista en fecha y hora, tiene la mejor
magnitud por evento y es sobre ES. **Pero su signo no está publicado.** El paper mide la deriva
**condicionando a la sorpresa que salió después**, y esa no se conoce al entrar. Convertirla en una
regla operable exige que **nosotros** elijamos el sustituto del signo, y una regla que ponemos
nosotros vuelve a ser una hipótesis de nuestro generador. **Excluida por el criterio, no por el
resultado.**

**L07 entra SÓLO SI se puede extraer del paper una magnitud publicada con su dispersión.** El texto
dice "varios puntos básicos" y no tabula. **Ese es un paso de literatura, no de datos, y se resuelve
abriendo el paper.** Si al abrirlo no hay un número, queda afuera y esa exclusión queda declarada
desde ahora. **No se puede decidir después de ver el resultado.**

### Por qué no entran las otras seis

L01, L02, L04, L05, L06 y L09 fallan el punto 1: su evento **ocurre todas las sesiones**. No son
reglas de calendario: son reglas de reloj. Mezclarlas rompería la hipótesis, que es específicamente
sobre calendarios externos.

## El conteo de eventos

| candidata | instrumento | eventos por año | eventos 2016-2019 | observaciones |
|---|---|---|---|---|
| L11 | ES | **44** | 176 | 176 |
| L10 | ES | 12 | 48 | 48 |
| L08 | 10 monedas | 12 | 48 | **480** (panel) |
| *L07, condicional* | 6J | *72* | *288* | *288* |
| **total sin L07** | | **68** | **272** | **704** |
| **total con L07** | | **140** | **560** | **992** |

Los 44 anuncios de L11 son la cifra de Ai, Bansal y Guo: comité de política monetaria, empleo,
índice de precios al consumidor, índice de precios al productor y producto bruto.

**Solapamiento declarado:** L10 y L08 caen ambos el último día hábil del mes, y L07 también incluye
esa fecha. Son instrumentos distintos pero **la misma fecha**, así que no son independientes. **Los
errores estándar se agrupan por fecha.** Ver el punto (g), control 4.

---

# b) CÓMO SE COMBINAN

## La estandarización, declarada ahora con su fórmula y su fuente

Para el evento `i` de la candidata `j`:

```
y_ij  =  retorno realizado en la ventana declarada de j, en el instrumento de j,
         en puntos básicos del nocional, CON EL SIGNO que la regla publicada predice
         (positivo = la regla acertó la dirección)

z_ij  =  y_ij / m_j                    m_j = la magnitud publicada de j
```

`z` es **la fracción de la magnitud publicada que se realizó**. `z = 1` significa que el efecto
apareció entero; `z = 0`, que no apareció; `z < 0`, que apareció al revés.

## Las magnitudes `m_j`, cada una con su fuente exacta

| j | `m_j` | unidad | fuente literal |
|---|---|---|---|
| **L11** | **10,3** | pb, retorno de la sesión | Savor y Wilson (2013), *JFQA* 48(2): 11,4 pb en días de anuncio contra 1,1 pb en el resto. **La diferencia es la magnitud, no los 11,4** |
| **L10** | **17,0** | pb, retorno del día siguiente, por desvío estándar de la señal de calendario | Harvey, Mazzoleni y Melone (2025), NBER 33554, resumen |
| **L08** | **0,0142** | coeficiente: pb de moneda por punto porcentual de retorno bursátil del mes | Melvin y Prins (2015), *JFM* 22, ecuación 4 |
| *L07* | *a extraer* | *pb, ventana 9:53–9:57 JST* | *Ito y Yamada (2017), JIE 109. **Si no hay número, no entra*** |

**Las tres primeras son cifras publicadas y verificadas contra el texto. Ninguna es mía.**

## Las dos que dependen de la señal, y cómo se escalan

L10 y L08 publican su magnitud **por unidad de señal**, no incondicionalmente. Se declara ahora:

```
L10:  m_i  =  17,0 pb  ×  (señal_i / desvío estándar de la señal en 2016-2019)
L08:  m_i  =  0,0142  ×  (retorno bursátil del mes hasta el penúltimo día hábil, en %)
```

**El desvío estándar de la señal de L10 se mide sobre 2016-2019 ANTES de mirar ningún resultado**, y
se puede: es la dispersión de una serie de señal, no depende del signo del resultado. **Medir el
ruido no destapa el efecto.**

## La ponderación

Ponderación por **varianza inversa**, declarada ahora:

```
peso_j  =  n_j / σ_j²          σ_j = desvío estándar de z dentro de la candidata j
```

**Los `σ_j` se miden sobre 2016-2019 antes de la corrida**, con el mismo argumento: la dispersión de
la ventana no depende del signo predicho. **La medición de los `σ_j` es un paso separado, se
commitea con sus números, y recién después se corre la prueba.** Si los `σ_j` se eligieran después
de ver los `z`, sería la trampa que este documento existe para evitar.

**Alternativa declarada por si alguien objeta la varianza inversa:** ponderación igual por evento.
**Se reportan las dos.** Si difieren en el veredicto, el veredicto es NO CONCLUYENTE. Eso está en
(d).

---

# c) LA HIPÓTESIS

> **Las reglas de calendario publicadas por terceros —fecha, signo y magnitud tomados del paper sin
> modificación— conservan su signo y al menos una cuarta parte de su magnitud publicada en los datos
> de 2016-2019.**

Formalmente: `θ = E[z] ≥ 0,25`, contra la nula `θ = 0`.

**Por qué 0,25 y no otro número:** McLean y Pontiff (2016) miden que los retornos de anomalías
publicadas caen **26 % fuera de muestra y 58 % después de publicadas**. Un 58 % de caída deja
`θ = 0,42`. **El umbral de 0,25 es más exigente que el decaimiento típico documentado**, y se elige
por eso y no por lo que la prueba puede detectar. Queda fijado acá.

**Lo que la hipótesis NO dice, para que no se pueda estirar después:**
- No dice que alguna candidata individual funcione.
- No dice que se pueda operar.
- No dice nada sobre 2020-2026.
- No dice que el mecanismo declarado sea el correcto.

---

# d) LA REGLA DE DECISIÓN, escrita antes

Sea `t = θ̂ / SE(θ̂)`, con `SE` agrupado por fecha.

| resultado | condición numérica | qué se concluye |
|---|---|---|
| **SOBREVIVEN** | `t ≥ 3,0` **y** `θ̂ ≥ 0,25` **y** las dos ponderaciones coinciden | las reglas de terceros transfieren, al menos en una cuarta parte |
| **NO SOBREVIVEN** | `t < 3,0` **y** el intervalo de `θ̂` a dos desvíos **excluye 0,25** | las reglas publicadas **no** transfieren con la magnitud declarada |
| **NO CONCLUYENTE** | cualquier otro caso, incluido que las dos ponderaciones difieran | la prueba no alcanzó |

**La vara es 3,0 desvíos y no 3,7, y el motivo se declara acá:** el juez sube la vara con las
variantes probadas, y **esta prueba tiene una sola variante**. Todo lo que se podía elegir —qué
candidatas, qué magnitudes, qué ponderación, qué umbral— está fijado en este documento antes de
mirar. `variantes_probadas = 1`.

**Y la condición que lo invalidaría, escrita: si al correrla se cambia cualquier elemento de las
secciones (a) o (b), el resultado no vale y hay que volver a empezar con un pre-registro nuevo y
otro cartucho.**

---

# e) LA POTENCIA — el número que justifica el cartucho

## Método

Para cada candidata, la señal por evento es `r_j = m_j / σ_j`, o sea magnitud publicada sobre
dispersión de la ventana. El estadístico agrupado bajo `θ = 1` es:

```
t(θ=1)  =  √( Σ_j  n_j · r_j² )                y en general    t(θ) = θ · t(θ=1)
```

## Los números, con la procedencia de cada uno

| j | `m_j` | `σ_j` de la ventana | fuente de `σ_j` | `r_j` | `n_j` | `n_j·r_j²` |
|---|---|---|---|---|---|---|
| L11 | 10,3 pb | ≈ 60 pb, cierre a cierre | mediana 8,75 pt de la Compuerta 1, con cola. **Estimado** | 0,172 | 176 | 5,2 |
| L10 | 17,0 pb | ≈ 60 pb, cierre a cierre | ídem. **Estimado** | 0,283 | 48 | 3,8 |
| L08 | — | — | `F = 25,52` sobre ≈ 1.040 obs. → `t = 5,05` → `r = 0,157`. **Publicado** | 0,157 | 480 | 11,8 |
| | | | | | **704** | **20,8** |

```
t(θ=1)  =  √20,8  =  4,56
θ mínimo detectable a 3,0 desvíos  =  3,0 / 4,56  =  0,66
```

**La prueba agrupada detecta el 66 % de la magnitud publicada.** Con L07 dentro, más.

## Contra el piso, que es lo que Roberto pidió ver

**Primero, contra las candidatas por separado.** `θ` mínimo detectable de cada una sola, a 3,0
desvíos:

| | sola | agrupada |
|---|---|---|
| L11 | **1,32** | |
| L10 | **1,53** | **0,66** |
| L08 | 0,87 | |

**Dos de las tres no detectan ni el 100 % de su propio efecto publicado. Agrupadas detectan el 66 %
del efecto medio.** Ése es el salto.

**Segundo, contra el piso en dólares.** El 66 % de la magnitud publicada, por evento:

| | magnitud publicada | **66 % de ella** | costo de ida y vuelta |
|---|---|---|---|
| L11 | $134 | **$88** | ≈ $17 |
| L10 | $221 | **$146** | ≈ $17 |
| L08 | $70 | **$46** | por medir en 6E |

**Es la primera prueba del inventario cuyo efecto mínimo detectable es varias veces el costo de
operarlo.** En L01 el efecto mínimo detectable estaba por debajo del costo; acá está entre cinco y
nueve veces por encima.

## La honestidad sobre estos números

**Dos de los tres `σ_j` son estimaciones mías, no mediciones.** Los de L11 y L10 salen de convertir
la mediana nocturna de la Compuerta 1 a un desvío, y esa serie tiene cola gorda —el p99 es 71,81
puntos contra una mediana de 8,75—, **lo que hace que el desvío verdadero sea mayor y la potencia
real, menor**.

**Por eso `t(θ=1) = 4,56` es una cota optimista**, exactamente igual que la fila de entrada pasiva
del piso. **El paso de medir los `σ_j` sobre 2016-2019 y commitearlos antes de correr la prueba no
es una formalidad: es lo que convierte esta estimación en un número.** Si al medirlos `t(θ=1)` cae
por debajo de 3,0/0,25 = 12, hay que decidir si vale la pena, y esa decisión se toma **antes** de la
corrida.

---

# f) QUÉ PASA SI SALE NEGATIVO

**Un negativo acá NO dice "no hay ventaja en el mercado". Dice algo mucho más específico y más
útil.**

## Lo que SÍ se concluye

- **Las reglas de calendario publicadas por terceros, aplicadas sin modificación, no transfieren a
  ES y divisas en 2016-2019 con al menos una cuarta parte de su magnitud publicada.**
- Que el generador externo —la literatura académica— **no resolvió por sí solo** el problema que el
  generador interno no pudo resolver en 261 intentos. **Eso es información sobre el generador, que
  es exactamente lo que esta ventana existe para producir.**
- Que la explicación más simple del decaimiento documentado —McLean y Pontiff— es **compatible** con
  lo observado.

## Lo que NO se puede concluir, y va escrito antes

- **NO** que las candidatas individuales sean falsas. La prueba agrupa; un promedio bajo puede
  esconder una viva y dos muertas.
- **NO** que no exista ventaja en el calendario. Una regla que **nosotros** derivemos podría
  funcionar; lo que se probó es que las **publicadas** no.
- **NO** que se hayan muerto. Podrían no haber existido nunca en estos instrumentos, o **haberse
  mudado de ventana** en vez de morir. Ese criterio está en `F7`.
- **NO** nada sobre 2020-2026. La caja no se toca.
- **NO** que el mecanismo declarado sea falso. Un mecanismo puede ser real y su magnitud haber
  caído por debajo del costo.

## Y lo que hay que hacer con un negativo

**Publicarlo en el repo con la misma prolijidad que un positivo, y NO reintentar con otro
agrupamiento.** Un segundo agrupamiento después de ver el primero es multiplicidad pura y gasta otro
cartucho, y el segundo veredicto valdría menos que el primero.

---

# g) LOS CONTROLES, cada uno con su condición de falla

**Control 1 — Placebo de fecha.** Repetir todo desplazando cada evento **cinco sesiones hacia
adelante**, manteniendo instrumento, ventana y signo.
**Condición de falla: si el placebo da `t ≥ 2,0`, la prueba está midiendo algo que no es el
calendario y el resultado principal no vale.**

**Control 2 — Placebo de signo.** Repetir asignando el signo **al azar** en cada evento, mil veces.
**Condición de falla: si la distribución de `t` del placebo no está centrada en cero, hay un error
de construcción.** Es la nula de signo que el juez ya usa.

**Control 3 — Recuperación de una ventaja inyectada.** Sumar artificialmente `0,5 · m_j` a cada
evento y volver a correr.
**Condición de falla: si `θ̂` no sube en aproximadamente 0,5, la prueba no mide lo que dice medir.**
Es el mismo control que `juez_controles.py` ya usa y con el que ya se pescó un error de 62 % contra
100 %.

**Control 4 — Agrupamiento por fecha.** Reportar los errores estándar **con y sin** agrupar por
fecha.
**Condición de falla: si agrupar cambia el veredicto, el veredicto es NO CONCLUYENTE**, porque
significa que lo decide el solapamiento de fin de mes y no la evidencia.

**Control 5 — Deja-una-afuera.** Correr la prueba sacando una candidata por vez.
**Condición de falla: si el veredicto depende de una sola candidata, se reporta como "el resultado
es de esa candidata", no como "las reglas transfieren".**

**Control 6 — Reproducir una magnitud publicada.** Sobre L08, correr la regresión original de Melvin
y Prins tal cual sobre su propio período, 2004-2012, si se compran esos datos.
**Condición de falla: si no se reproduce el 0,0142, la implementación está mal y nada de lo demás
vale.** Es caro y es opcional; si no se hace, se declara que no se hizo.

---

# Lo que hace falta antes de poder correrla

| paso | qué es | costo | ¿bloquea? |
|---|---|---|---|
| 1 | Abrir Ito y Yamada y extraer la magnitud de L07, o excluirla | literatura | no, pero cambia la potencia |
| 2 | Calendario 2016-2019 de los 44 anuncios de L11 | gratis, medio día | **sí** |
| 3 | Serie diaria de bonos para la señal de L10 | gratis | **sí** |
| 4 | **Diez pares de divisas intradiarios y diez índices bursátiles diarios para L08** | **compra, sin cotizar** | **sí, y es el único gasto** |
| 5 | Medir los `σ_j` y la dispersión de la señal de L10, y commitearlos | gratis, sobre datos del repo | **sí** |
| 6 | Cotizar el paso 4 con el script que ya existe | gratis | **sí** |

**L08 aporta el 57 % de la potencia agrupada y es lo único que hay que comprar.** Sin ella,
`t(θ=1) = √9,0 = 3,0` y `θ` mínimo detectable sube a **1,0**, o sea que la prueba deja de servir.

**Ésa es la decisión concreta que hay debajo del cartucho: cotizar los datos de divisas, y recién
con el precio en la mano decidir.**
