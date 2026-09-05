# M01 — Probar el MECANISMO en vez de la VENTAJA

**VENTANA L. NO MEDIDO. Escrito para que otra ventana lo ejecute. No gasta cartucho, K sigue en 261.**

Roberto pidió desarrollar mi idea (c1) de la entrega anterior: que probar la reversión sea probar el
mecanismo y no la ventaja, y por lo tanto **no tenga que superar el piso de rentabilidad**.

**La idea general es correcta y la desarrollo acá. La aplicación concreta que propuse —la reversión—
resultó ser la MENOS potente de su clase, y eso lo corrijo abajo en vez de defenderlo.**

---

# 1. Por qué un test de mecanismo esquiva parte del muro

Un test de ventaja pregunta: *¿esta regla deja plata?* Un test de mecanismo pregunta: *¿la causa que
los autores declaran existe en estos datos?* Son preguntas distintas y **la segunda es más barata por
cuatro motivos concretos**.

**1. El piso de rentabilidad no aplica.** No hay operación, así que no hay comisión, ni medio-spread
de entrada, ni deslizamiento en el stop. Los ≈ $17 por ida y vuelta que se llevan la mitad de la
ventaja de L01 y L02 simplemente no entran. **La ventaja disponible pasa de $18 a $35 en L01, que es
un factor de 4 en el n necesario.**

**2. No hay bracket, así que no hay sesgo de contabilidad.** `PROTOCOLO_medir_un_candidato.md` mide
que ese sesgo llega a 5,82 puntos y supera hasta por 4,8× la ventaja que se buscaba. Una regresión
sobre retornos continuos no tiene operaciones sin resolver, así que **no tiene el sesgo ni necesita
la corrección**.

**3. No se binariza.** Un test de ventaja convierte cada día en ganó o perdió. Una regresión usa la
magnitud. Tirar la magnitud cuesta potencia.

**4. La predicción es un SIGNO con una alternativa nombrada.** Baltussen et al. lo escriben así:
*bajo la explicación de cobertura esperamos reversión a la media en el futuro cercano, mientras que
bajo la explicación de comercio informado no esperamos reversión.* **Un resultado nulo informa**,
porque las dos hipótesis predicen cosas distintas, y no sólo dice "no detecté nada".

## Y por qué NO esquiva todo el muro

**El número de sesiones sigue siendo 1.007.** El test de mecanismo baja la vara, no agranda la
muestra. Cuánto baja la vara depende del caso, y en un caso —el que yo propuse— baja poco.

---

# 2. La corrección a mi propia idea

Roberto escribió que el tamaño de efecto de la reversión *"suele ser mucho mayor que la ventaja
neta"*. **En coeficiente tiene razón. En detectabilidad, no, y la diferencia importa.**

De Baltussen et al., futuros de índice bursátil, coeficientes multiplicados por 100:

| regresión | coeficiente | t | R² |
|---|---|---|---|
| momento: última media hora sobre el resto del día | **+5,98** | 4,78 | 3,28 % |
| reversión: retorno del día siguiente sobre la última media hora | −14,51 | −1,70 | 0,13 % |
| **reversión: retorno de los dos días siguientes** | **−29,05** | **−3,16** | **0,27 %** |
| reversión: retorno de los tres días siguientes | −27,98 | −2,61 | 0,17 % |

**El coeficiente de la reversión a dos días es 4,9 veces el del momento. Y su t es más chico y su R²
es doce veces menor.**

**Por qué:** la reversión reparte una cantidad de dólares parecida sobre **dos días de ruido** en vez
de sobre **treinta minutos de ruido**. El denominador crece mucho más rápido que el numerador. Un
coeficiente grande sobre una variable dependiente ruidosa **no es un efecto más detectable**.

**Eso invalida la premisa optimista de mi propia idea y hay que decirlo antes de que alguien gaste
una ventana en ella.**

---

# 3. Los cuatro tests de mecanismo disponibles, ordenados por potencia

Método de la estimación: el estadístico t escala con la raíz de n manteniendo el efecto y la
estructura de ruido. **Es una aproximación de orden, no una predicción**, y supone que el efecto en
2016-2019 es el mismo que en la muestra original — que es justamente lo que se quiere probar.

| test | de dónde sale la potencia | n original aprox. | n en 2016-2019 | **t esperado** |
|---|---|---|---|---|
| **M01-a — panel cambiario de fin de mes (L08)** | **10 monedas a la vez** | 1.040 | 480 | **≈ 3,4** |
| **M01-b — deriva contra la sorpresa publicada (L03)** | condiciona a un predictor exógeno fuerte | 296 | 192 | **≈ 2,7** |
| M01-c — señal de rebalanceo diaria (L10) | la señal es **continua y diaria**, no 12 eventos | 6.550 | 1.007 | ≈ 1,4 |
| M01-d — reversión de la presión de precio (L01) | mi idea original | ≈ 9.500 | 1.007 | ≈ 1,0 |

## El principio que reordena todo, y no lo había visto en la entrega anterior

**El filtro de "pocos instrumentos" y el de "pocos eventos" aplican a OPERAR, no a PROBAR.**

- **L08 estaba casi muerta para operar**: 12 eventos por año, corta por un factor de 28. **Como test
  de mecanismo es la más potente del inventario**, porque el panel de diez monedas multiplica n por
  diez y no hay que operar ninguna de ellas.
- **L10 dispara 12 a 24 veces por año para operar, pero su señal existe TODOS LOS DÍAS.** Como
  regresión son 1.007 observaciones en vez de 48: **un factor de 21 en n**.

**El orden de lo que conviene hacer cambia entero**, y en la dirección contraria a la intuición: las
candidatas peores para operar son las mejores para entender.

---

# 4. M01-d — La reversión, especificada para ejecutar

La desarrollo completa porque Roberto la pidió así, **con la advertencia de potencia del punto 2
puesta arriba**.

## Qué se mide, exactamente

Sobre ES 1-min Databento 2016-2019, 1.007 sesiones de contrato único:

```
Para cada sesión t:
  rLH(t)      = retorno de la última media hora de la sesión t
  rROD(t)     = retorno desde el cierre de t-1 hasta 30 minutos antes del cierre de t

Regresión 1 (momento, la referencia):   rLH(t)  =  a + b · rROD(t) + e
Regresión 2 (reversión, 1 día):         r(cierre t → cierre t+1)  =  a + c1 · rLH(t) + e
Regresión 3 (reversión, 2 días):        r(cierre t → cierre t+2)  =  a + c2 · rLH(t) + e
Regresión 4 (reversión, 3 días):        r(cierre t → cierre t+3)  =  a + c3 · rLH(t) + e
```

Errores estándar robustos a la Newey-West, que es lo que usa el paper. Los retornos superpuestos de
las regresiones 3 y 4 **obligan** a corregir la autocorrelación: sin eso los t salen inflados.

## Qué esperaría el paper

| | valor publicado | condición de falla |
|---|---|---|
| `b` (momento) | **+5,98** | si sale negativo, no hay nada que explicar |
| `c1` | −14,51 | — |
| **`c2`** | **−29,05** | **si `c2` ≥ 0, la explicación de cobertura NO describe estos datos** |
| `c3` | −27,98 | — |

**La predicción falsable es el SIGNO de `c2`, no su tamaño.**

- `c2` **negativo** → hubo presión de precio transitoria. Compatible con cobertura de gamma.
- `c2` **cero o positivo** → lo que movió la última media hora era información, no presión. La
  explicación de los autores no aplica acá.

## El control, y hacen falta dos

**Control 1 — placebo de ventana.** Correr las mismas cuatro regresiones reemplazando la última media
hora por **una media hora elegida al azar del medio de la rueda**, repetido sobre muchas ventanas.
Si el placebo produce reversión del mismo tamaño, lo que se midió es **reversión de corto plazo del
ES en general** y no algo de la última media hora. **Este control es obligatorio**: el repo ya midió
que el ES tiene rebote propio, con la razón rango sobre desvío estancada en el 76 % del browniano y
la varianza del minuto inflada alrededor de un 12 % (`HECHOS_MEDIDOS_ES.md`, sección 2).

**Control 2 — el que exige la propia estructura.** `b` y `c2` tienen que salir **con signos
opuestos**. Si los dos salen negativos o los dos positivos, hay un error de construcción, no un
hallazgo.

## Qué NO prueba

**No prueba que haya ventaja.** Un `c2` negativo y significativo dice que la última media hora
contiene presión transitoria; **no** dice que se pueda cobrar, porque cobrarla exige superar el piso
de rentabilidad que este test evita por construcción. Son dos preguntas y ésta contesta una.

---

# 5. M01-a y M01-b, en una línea cada uno, para que se puedan pedir

**M01-a — panel cambiario de fin de mes.** Regresar el retorno de cada moneda en la hora previa al
fix de las 16:00 de Londres del último día hábil contra el retorno bursátil de ese país en el mes,
las dos series demediadas en el corte transversal, sobre las diez monedas de Melvin y Prins,
2016-2019. Coeficiente publicado **+0,0142**, R² 0,03, p < 0,001. **Datos que faltan: diez pares de
divisas intradiarios y diez índices bursátiles diarios.** Control: los mismos días del mes que no son
el último. **Es el test más potente del inventario y ninguno de sus diez instrumentos hace falta
operarlo.**

**M01-b — deriva contra la sorpresa publicada.** Regresar el retorno del ES en la ventana de 30
minutos antes de la publicación contra la sorpresa estandarizada del dato que salió después, para
los cuatro anuncios de las 10:00 con deriva en Kurov et al., 2016-2019. Coeficientes publicados
**0,054 a 0,104**, todos al 1 %. **Datos que faltan: el calendario y el consenso de pronóstico.**
Control: los mismos cuatro anuncios con una sorpresa de un mes distinto, que tiene que dar cero.
**Prueba si sigue habiendo comercio informado antes del dato en un período posterior a los cambios
regulatorios de 2013-2014, que es una pregunta abierta y publicable en sí misma.**

---

# 6. Lo que este documento cambia

**Siete de las once candidatas tienen un mecanismo probable por separado de su rentabilidad**: L01,
L02, L03, L04, L07, L08 y L10. **L05 es enteramente un test de mecanismo.** Sólo L06 y L09 quedan
afuera, y no por su forma sino porque les falta el dato de partida.

**Ninguno de esos tests gasta un cartucho del contador de multiplicidad**, con el mismo argumento con
que la Compuerta 1 y el censo de instrumentos no lo gastaron: *no se busca ninguna ventaja, no hay
estadístico contra un α para elegir entre candidatas, se mide si un mecanismo declarado por un
tercero aparece en datos ya medidos.*

**Esa es la afirmación más consecuente de este documento y no la doy por cerrada: quien la ejecute
tiene que argumentarla en su propio pre-registro, no citarme a mí.** Si el test de mecanismo se usa
después para decidir cuál candidata se mide, **entonces sí seleccionó**, y ahí el cartucho se gasta.
La diferencia está en el orden: **primero se declara qué se va a hacer con el resultado, después se
mira.**
