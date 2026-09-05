# INVENTARIO — qué afirmación de esta ventana aguanta el punto porcentual y cuál no

**2026-09-04. No gasta cartucho. K = 261.**

Este documento **marca, no corrige**. Nada de lo que está en `CRITERIO_RESULTADO.md`,
`BRACKET_RESULTADO.md` o `CIERRE_VENTANA_G.md` se borró ni se reescribió. Lo que no se podía dejar
era una afirmación precisa sin la advertencia al lado; esta es la advertencia, y vive acá para que
sea una sola y no quince notas al pie.

## Por qué hace falta

Dos mediciones de hoy mueven el piso de casi todo lo publicado en esta ventana:

1. **`S/(S+T)` está corrido sobre ES real.** Residuo −1,32 (20pt:10pt) y +0,78 (5pt:20pt), y contra
   una nula de 10 series sintéticas sin estructura queda a **6,6 y 4,2 desvíos, afuera del recorrido
   completo**. No es el replicador: es el mercado. Fuente: `sintetico.py`, `sintetico_ensamble.py`.
2. **Mis barras de error estaban chicas.** El error binomial subestima **1,2–1,8×** el desvío del
   sesgo *pooled* y **≈5×** el de la separación largo/corto (0,41 declarado contra 2,08 real).

El criterio publicado es **+1,2 puntos**. El residuo es **1,3** y su corrección de barra de error es
**0,24**. Las tres cifras son del mismo orden.

---

## A — Escritas al punto porcentual y apoyadas en `S/(S+T)`: NO valen hoy

| # | afirmación | dónde | qué le pasa | ¿se mantiene el signo? |
|---|---|---|---|---|
| A1 | «5pt:20pt necesita **81,2%** contra el **80,0%** de la moneda: **+1,2 puntos** de ventaja real» | `CRITERIO_RESULTADO.md` § *Veredicto: ahora SÍ hay criterio* | el 80,0% es `S/(S+T)` afirmado, no medido. Medido sobre ES a una sesión, *pooled*: **85,2%**. El +1,2 además **no está definido** hasta fijar horizonte y tratamiento de las no resueltas | **no aplica**: el número no está definido, no es que esté corrido |
| A2 | la vara **1,181×** / **1,192×** y la elasticidad **7,9×** | ídem § *La reconciliación con la vara de 1,181×* | el denominador `P(pasar)` de la moneda usa `p = S/(S+T)`. Un punto de corrimiento se amplifica ~8× | sí: la vara sigue > 1 con margen |
| A3 | tabla **34,1% / 35,0% / 33,3%** | ídem § *Qué significa exactamente el 34,1%* | el 33,3% es `S/(S+T)` | sí: (ii) < (i) es aritmética, no depende de la nula |
| A4 | los dos criterios por bracket: **+2,3 / +2,3 / +1,9 / +1,2 / +1,4** | ídem § *Los dos criterios, que no son el mismo* | columna «moneda» = `S/(S+T)` | sí: (ii) < (i) en las cinco celdas |
| A5 | pisos de rentabilidad **2,26 / 2,30 / 1,94 / 1,20 / 1,43** puntos | ídem § *El piso* | mismo ancla | sí |
| A6 | razones detectabilidad ÷ rentabilidad **1,63× … 2,62×** | ídem § *La regla que sale de esto* | hereda A5 en el denominador | sí: ningún bracket llega con 250 ni 1.000, y ahí el margen es grande |
| A7 | tabla de 48 celdas, esperanza negativa en 8 firmas × 3 tamaños | `aritmetica.py`, `f55fe57` | `p_win` por defecto = `S/(S+T)` | **sí, y con mucho margen**: 48 de 48 negativas |
| A8 | el positivo de **+$10** y el **−$72** a precio de lista | `CRITERIO_RESULTADO.md` § *El positivo está muerto tres veces* | ya estaba muerto por deslizamiento de entrada, caída de tasa y precio | **sí**: esto lo mata una cuarta vez |

**Lo que NO se mueve dentro de este grupo:** las **MDE** (7,45 / 3,70 / 2,13 …) son *diferencias* y
dependen de `p₀(1−p₀)`, que casi no se corre con un punto de desplazamiento. La MDE aguanta; lo que
no aguanta es el **ancla** contra la que se la compara.

## B — Escritas con la barra de error vieja: los intervalos están mal, no los puntos

| # | afirmación | qué le pasa |
|---|---|---|
| B1 | «Ruido de Monte Carlo: **±0,3 puntos** en los requeridos» | subestimado 1,2–1,8×. Hoy sería **±0,4 a ±0,5** |
| B2 | residuo **−1,32** y **+0,78** | los puntos quedan, pero medidos contra la nula real (media +0,26 / −0,20, no cero) son **−1,58** y **+0,98**: la corrección los agranda |
| B3 | separación largo/corto **+5,67** | el error no es 0,41 sino **2,08**. Sigue afuera de la nula, pero a **2,9 desvíos**, no a 14 |
| B4 | factor de des-drift **0,425** | arrastra **±0,18** desde B3. Es **0,43 ± 0,18**, no 0,425 |
| B5 | «el drift vive casi enteramente en la separación y casi nada en el *pooled*» | correcta en magnitud (11,85 contra 0,50, factor 24) pero **«casi nada» no es «nada»**: ese medio punto es del tamaño del criterio |
| B6 | «el modelo de barreras sin drift NO describe este mercado» | **se mantiene y se refuerza.** La razón que di (sobrevive al des-drift) usaba la barra de error mala; hoy está sostenida por la nula sintética, que es mejor evidencia |

## C — No tocadas por nada de esto

- Comisiones **medidas**: $1,82/micro, $5,76/mini, fuente oficial `help.tradeify.co`.
- El cobro **$1.350 = $1.500 × 90%** y la cuota **$83 promocional / $165 de lista**.
- Medias de exceso de deslizamiento **0,722** y **0,982** puntos, y los percentiles.
- **Compuerta 1** (rama de ejecución nocturna): es cierre a cierre, no usa `S/(S+T)`.
- **Censo de instrumentos**: holgura y esfuerzo en puntos y ticks, sin modelo de barreras.
- Las reglas de las 8 firmas en `datos_crudos.md`, con URL y fecha de lectura.
- Las **identidades de construcción** `P_pooled(20:10) = 1 − P_pooled(10:20)` y
  `P_pooled(10:10) = ½`: son álgebra, valen para cualquier serie.
- **`P_ABIERTA` y `P_RESUELTA` están MEDIDAS, no asumidas.** La cadena del tercer estado
  (`tercer_estado.py`) es la **única** pieza del modelo que no se apoya en `S/(S+T)`, y por eso es la
  que menos se mueve. El `control_consistencia()` que la protege es el que cazó la ventaja fantasma.

---

## D — Auditoría hacia atrás: qué controles publicados NO podían fallar

Regla nueva, aplicada también a lo ya escrito: un control que no puede dar otra cosa no es un
control. Tres categorías.

### VACÍOS — no podían fallar de ninguna manera

| control | dónde | por qué no podía fallar |
|---|---|---|
| «*pooled* = 50,0% clavado» en el bracket ancho | `salida_linea_base.txt` línea 18 | identidad de construcción: los dos lados usan los mismos niveles y las mismas entradas. Ya autocorregido el 2026-09-04 |
| «con costo cero el equilibrio por operación = `S/(S+T)`», error 1e-16 | `salida_criterio_control.txt` línea 45 | es álgebra: en `p = S/(S+T)` vale `p·T − (1−p)·S ≡ 0`. Verifica una identidad contra sí misma |
| «drawdown ÷ valor del punto = $2.000 / $50 = 40 puntos» | `salida_censo.txt` línea 4 | es una división |
| «sesgo(20:10) + sesgo(10:20) = 0 exacto» | `desdrift.py` | ya lo marqué al escribirlo: vale para cualquier serie |

### SÓLO DE CÓDIGO — forzados por la construcción, pero atrapan una clase de bug

| control | por qué está forzado | qué sí atraparía |
|---|---|---|
| «ambigüedad = 0,000% con bracket de 23pt por lado» (`salida_linea_base.txt`) | el ancho se eligió como `ceil(máximo/2)+5 = 23`, o sea 46pt de separación contra un rango máximo observado de 36pt. **Ninguna barra puede contener las dos** | un error en el test de toque que hiciera disparar las dos condiciones a la vez |
| «con tamaño de posición CERO las cuatro medidas dan 0,00%» (`salida_compuerta_nocturna.txt`) | con `contratos = 0` el paso es 0 y el balance no se mueve | un error de signo que pusiera el piso **en** el balance inicial en vez de debajo |
| «costo = 0 → vara ≤ 1,0», peor celda 0,9711 (`salida_bracket.txt`) | con costo cero el requerido coincide con la moneda, así que la vara es 1 más ruido | que el ruido de Monte Carlo lo empujara arriba de 1, o un error en la cadena |

### VÁLIDOS — podían dar otra cosa, y varios dieron otra cosa

| control | resultado |
|---|---|
| «objetivo = drawdown, costo cero → ~50%» (`aritmetica.py`) | **FALLÓ en la primera implementación** (0,376–0,499) y destapó que el piso se chequeaba por operación y el objetivo sólo a fin de día. Se descartó la corrida sin publicarla |
| «la misma tabla con costo cero debe dar 50,0%» (`salida_criterio_control.txt`) | **FALLÓ 32 de 32**, y la falla era la información: el umbral escrito a mano estaba mal para brackets asimétricos |
| consistencia: esperanza por operación ≈ 0 (`tercer_estado.py`) | **FIRÓ** y cazó la ventaja fantasma de +199,6% por mezclar tasa asumida con M2M medido |
| `p_abierta = 0` reproduce el modelo viejo **exacto** (`tercer_estado.py`) | PASADO. Podía fallar fácil: el camino nuevo podía consumir números aleatorios |
| población: 971 sesiones exactas (`media_exceso.py`) | PASADO. Cualquier cambio de filtro lo rompe |
| la inversa reproduce la directa (`piso_ventaja.py`) | PASADO tras **dos** arreglos: la primera búsqueda binaria falló porque la potencia binomial exacta no es monótona en n |
| reproducir una celda publicada de `BRACKET_RESULTADO.md` (`salida_criterio_verif.txt`) | PASADO dentro de tolerancia declarada |
| el censo reproduce las tres frecuencias ya medidas (`salida_censo.txt`) | PASADO |
| **los de hoy**: generador, horizonte largo, separación, identidad en el ensamble, real contra la nula | dos **fallaron** contra el binomial y ese fallo fue el hallazgo |

**Balance: de 16 controles publicados en esta ventana, 4 eran vacíos y 3 sólo de código.** Siete de
dieciséis no medían lo que yo decía que medían. Los nueve válidos incluyen cuatro que efectivamente
fallaron, y cada falla encontró un error real — que es la única evidencia de que la categoría
«válido» está bien asignada.

---

# E — LA CORRECCIÓN DEL 5×, APLICADA (2026-09-04)

**Marca, no corrige.** Mi idea (c3) del reporte anterior —«toda barra de error de esta ventana que
involucre una diferencia largo/corto está ~5× chica, no sólo las que revisé»— ahora está **medida**,
en `sep_nula.py`, con 20 series independientes por horizonte.

## La regla, con número

No es un 5× parejo. Depende del bracket y del horizonte, y **crece con los dos**, porque los dos
alargan el tiempo de resolución y por lo tanto el pisado entre rutas.

| desvío de la nula para la **separación largo/corto** | binomial | real | subestima |
|---|---|---|---|
| 5pt:10pt, 1 sesión | 0,385 | 1,051 | 2,7× |
| 5pt:20pt, 1 sesión | 0,328 | 1,050 | 3,2× |
| 10pt:10pt, 1 sesión | 0,409 | 1,769 | 4,3× |
| 20pt:10pt, 1 sesión | 0,397 | 1,889 | 4,8× |
| 20pt:10pt, 5 sesiones | 0,386 | 2,051 | **5,3×** |

**A quién se le aplica y a quién no.** El binomial falla cuando las rutas se pisan **y** el
estadístico no se beneficia de la cancelación del *pooling*:

- ***pooled*** de rutas que se pisan → **×1,2 a ×1,4**. Poco.
- **diferencia largo/corto** de rutas que se pisan, una sola serie → **×2,7 a ×5,3**. Mucho.
- **diseños con observaciones que NO se pisan** —una por noche, una por sesión, una por día— **el 5×
  NO se aplica**. Eso deja afuera, y por lo tanto **intactos**: la compuerta nocturna (una
  observación por noche), el censo de instrumentos (una por día) y las medias de exceso de
  deslizamiento (una por sesión). Lo digo explícito porque aplicar el 5× ahí sería exagerar el error
  y borrar cosas que sí están.

## Qué cambia de estado

| afirmación | valor | ¿se distingue de cero con el error bueno? | ¿cambia de estado? |
|---|---|---|---|
| separación 5pt:10pt, 1 sesión | +3,70 | **+4,3 desvíos** — sí | no |
| separación 10pt:10pt, 1 sesión | +5,20 | **+3,2 desvíos** — sí, apenas | **sí: pasa de «clavado» a «apenas»** |
| separación 20pt:10pt, 1 sesión | +2,60 | +1,6 desvíos — **no** | **SÍ: pasa a indistinguible de cero** |
| separación 10pt:20pt, 1 sesión | +2,60 | +1,6 desvíos — **no** | **SÍ: pasa a indistinguible de cero** |
| separación 5pt:20pt, 1 sesión | +1,20 | +1,7 desvíos — **no** | **SÍ: pasa a indistinguible de cero** |
| separación 10pt:10pt, 5 sesiones (`+5,67`) | +5,67 | +2,9 desvíos — al borde | ya marcado en B3 |
| factor de des-drift | 0,425 | ±0,16 desde la separación de 10:10 | ya marcado en B4 |
| control ancho 23pt: 54,6% / 45,4% (sep 9,2) | +9,2 | **no medido**: su nula pide un bracket de 23pt y no se corrió. Por la tendencia (más ancho → más desvío) su desvío es ≥ 2,05, o sea ≤ 4,5 desvíos | **sí: se publicó SIN ninguna barra de error** |

**Tres de las cinco separaciones por bracket que publiqué en `salida_linea_base.txt` no se distinguen
de cero.** No es que estén mal medidas: es que nunca tuvieron una barra de error al lado, y con la
buena no alcanzan.

## Una identidad más, que hay que anotar

`20pt:10pt` y `10pt:20pt` dan **exactamente la misma separación** (+2,60) y **exactamente el mismo
desvío nulo** (1,889). No es coincidencia, es la identidad de construcción otra vez:

Por la identidad, `sesgo_largo(T:S) = −sesgo_corto(S:T)` y `sesgo_corto(T:S) = −sesgo_largo(S:T)`.
Restando, `sep(T:S) = sep(S:T)` **exacto**. Los reporté como dos brackets; **son un número solo**. Es
la tercera vez en esta ventana que la misma identidad convierte dos mediciones en una.

## Y un hallazgo lateral que no buscaba

**La media de la nula de la separación NO es cero: va de −0,34 a −0,78.** En series construidas sin
drift, con las marginales exactas de la barra de ES, el lado corto sale sistemáticamente medio punto
mejor que el largo. Eso no puede ser drift —lo saqué por construcción— así que es **asimetría de la
forma de la barra**: las mechas de ES no son simétricas y el bracket lo nota. Consecuencia práctica:
**parte de la separación real es forma de barra, no dirección**, y por eso todas las cifras de la
tabla de arriba se comparan contra la media de la nula y no contra cero.

---

# F — CORRECCIÓN DE ESTE MISMO DOCUMENTO (2026-09-04, más tarde)

Este inventario se escribió unas horas antes que el bootstrap por bloques apareado. **Dos de sus
entradas quedaron obsoletas por esa medición y no se borran: se marcan acá.**

| entrada | qué decía | qué corresponde hoy |
|---|---|---|
| **B2** | «residuo −1,32 y +0,98 contra la nula: la corrección los agranda» | los números son correctos **contra la nula IID**, que no estaba apareada en la tasa de sin-resolver. Contra la nula **apareada** el residuo queda en **−1,9 y +1,4 desvíos**, y **a una sesión desaparece del todo** (+0,1 y +0,4). **El residuo no está establecido.** |
| **B6** | «"el modelo de barreras sin drift NO describe este mercado" se mantiene y se refuerza» | **QUEDA SIN SOSTÉN.** Una serie **sin drift** con la estructura serial de ES —bloques de 4 sesiones— produce residuos del mismo signo y del mismo tamaño. Lo que el modelo no captura no es el drift: es la **estructura serial**, y con ella adentro el modelo describe lo que se observa. |
| **«Por qué hace falta», punto 1** | «`S/(S+T)` está corrido sobre ES real … no es el replicador: es el mercado» | la primera mitad se mantiene: `S/(S+T)` **sí** está corrido y no hay que usarlo como línea de base. La segunda mitad hay que precisarla: el corrimiento es **censura más estructura serial**, las dos cosas reproducibles en una serie sin ventaja. **No es una propiedad explotable del mercado.** |

**Lo que NO cambia de todo lo de arriba:** los grupos A y C quedan igual, y la razón es la misma por
la que se escribieron — el problema con `S/(S+T)` como ancla **es el mismo o peor**, porque ahora
sabemos que el corrimiento correcto es de **+4,5 puntos** en 5pt:20pt a una sesión, casi todo censura.
La sección D (auditoría de controles) tampoco se toca, y se le suma una entrada:

| control nuevo | categoría | por qué |
|---|---|---|
| «bloques sobre datos barajados reproducen la nula IID», fila 10pt:10pt | **VACÍO, y peor: rompe al revés** | su nula tiene varianza ~0 por la identidad de construcción, así que cualquier diferencia de 0,004 puntos da 4,4 desvíos y el control «falla» siempre. Un control cuya nula no tiene varianza no se puede juzgar con un cociente z |

Esa última fila es la lección nueva de hoy: **hasta acá venía marcando controles que no podían
fallar; este es uno que no podía pasar.** Las dos fallas son la misma — un control sin varianza en su
nula no mide nada — y las dos se detectan con la misma pregunta: *¿qué resultado distinto de éste era
posible?*
