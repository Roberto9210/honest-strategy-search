# El sesgo de dirección del error — la lista, con el signo de cada uno

**VENTANA G. K = 261, no gasta cartucho.** Este documento no arregla nada: nombra y le pone signo.
Arreglar cualquiera de estos es una decisión aparte, y algunos cambian veredictos.

**La regla, que no es de screening sino de auditoría:** cuando encontramos un error, **antes** de
arreglarlo, se anota **hacia qué lado empujaba**. Y proactivamente: dónde estamos usando un
**promedio** cuando lo que decide es el **caso malo**.

---

## Parte 1 — Los errores encontrados, y hacia dónde empujaban

> **REVISADO 2026-09-06.** La versión anterior de esta tabla decía "cuatro de cuatro al lado fácil,
> tres de la misma clase técnica". **Estaba mal en su entrada más llamativa**, y la corrección va
> abajo con nombre. El conteo cambió y la conclusión se debilitó.

| # | error | de quién | hacia dónde | clase |
|---|---|---|---|---|
| 1 | **El filtro nocturno** | otra ventana | **fácil** | selección de muestra |
| 2 | **La exposición variable de L10 tratada como fija** | otra ventana | **fácil** | escalado por tiempo |
| 3 | **La volatilidad uniforme a lo largo del día** (raíz del tiempo) | VENTANA G | **fácil** | escalado por tiempo |
| ~~4~~ | ~~396 pb / √252 en vez de /252 (Baltussen)~~ | — | **NO EXISTIÓ** | — |
| 4' | **Diagnosticar mal el error 4**: dije que el 3,96% era un retorno; es un **desvío** (6,86/3,96 = 1,73 = Sharpe), y un desvío **sí** se convierte con √252 | **VENTANA G** | **difícil** (×15,9 en contra del candidato) | escalado por tiempo |
| 5 | **"Los factores de las cajas grandes sirven como constantes"**, escrito habiendo mirado dos de quince | **VENTANA G** | **fácil** | **generalizar de más** |

| 6 | **El signo de la observación de las 972 sesiones**: dije que excluir los medios días calmos de la caja #43 infla su desvío y que eso "empuja al lado fácil" | **VENTANA G** | **difícil** — y yo lo reporté al revés | leer mal dónde se consume el número |

**Corrección del 6, que me la discutieron y tenían razón.** La premisa **sí** era cierta y la medí
después de afirmarla (`perfil_verificaciones.py`): las 35 sesiones sin la caja #43 son **0,57×** de
agitadas. Pero el signo estaba invertido. El desvío de una caja se consume en tres lugares —como
denominador de `r = magnitud/σ`, como ruido de `MDE = z·σ/√n`, y como factor para escalar el desvío
de sesión a la ventana— y en **los tres** un σ inflado hace la vara **más exigente**. Es el lado
**difícil**.

De dónde salió mi error: lo traté como si fuera un **costo**, donde subestimar es "fácil", cuando es
una estimación de **ruido**, donde sobreestimar es conservador. *Un signo al revés en el documento de
los signos es el peor lugar posible para tenerlo.*

### El conteo, que es conteo y no conclusión

- **Al lado fácil: 4** (1, 2, 3, 5). **Al lado difícil: 2** (4', 6). **Ya no es "todos al mismo lado".**
- **Escalado por tiempo: 3** (2, 3, 4') — pero uno de esos tres empuja al lado difícil, así que la
  clase existe como **peligro** y ya **no** como evidencia de sesgo direccional.
- **Clases distintas: 3** (selección de muestra; generalizar de más; leer mal dónde se consume un
  número). Mi condición de muerte para *"es hábito técnico y no sesgo"* pedía **dos o tres** de otra
  clase. **Llegaron dos.** Queda anotado como conteo, en revisión, y **no** se concluye todavía.
- **Y el patrón que sí aparece, con tres casos (4', 6, y la mitad del 3):** los tres errores míos de
  esta ronda son *la pregunta correcta contestada al revés por no mirar dónde se consume el número*.
  Eso es más específico y más buscable que "escalado por tiempo", y sugiere el chequeo:
  **antes de firmar un signo, escribir los lugares donde el número entra en una cuenta.**

### La corrección del error 4, en detalle, porque es mía y es instructiva

Diagnostiqué, sin leer el paper, que los 25 pb de la VENTANA L salían de dividir 396 pb por √252 en
vez de por 252. **La VENTANA L lo verificó contra la Tabla 6: el 3,96% anual es el DESVÍO, no el
retorno** (el retorno es 6,86%, y 6,86/3,96 = 1,73 es el Sharpe). **Un desvío sí se convierte con
√252.** La conversión de L era correcta y la mía era el error.

**Me hice la pregunta correcta —¿retorno o dispersión?— y la contesté al revés.** Eso es peor que no
habérmela hecho, porque la pregunta correcta con la respuesta equivocada da confianza injustificada.

**Lo que impidió el daño fue marcarlo FRÁGIL**, no el diagnóstico. El procedimiento funcionó y el
razonamiento no. Esa distinción vale más que el error: la marca de fragilidad no es cortesía, es la
barandilla que aguantó.

*(La VENTANA L confirma aparte que el número igual no sirve como control externo, por otra razón:
cartera 1/N 1974-2020 contra ES 2016-2019 no son el mismo objeto. Los 20,92 pb medidos lo reemplazan
para todo uso.)*

### La pregunta sigue en pie — es la respuesta la que hay que verificar

> **¿Lo que estoy escalando es un RETORNO MEDIO o una DISPERSIÓN?**
> Un retorno medio escala con **T**. Una dispersión escala con **√T**.
> Confundirlos a 252 sesiones se equivoca por **15,9×**.

Y ahora con el agregado que costó este error: **la respuesta a esa pregunta se verifica contra la
fuente, no se infiere del número.** Un Sharpe de 1,73 con un retorno de 6,86% y un desvío de 3,96%
son tres cifras que sólo se distinguen leyendo la tabla.

**Por qué el conteo ya no autoriza la conclusión que tenía antes:** con 4 al lado fácil y 1 al
difícil, "no hace falta buscar sesgo psicológico" es una afirmación que este documento **ya no
sostiene**. Lo que sostiene es más chico y más útil: *hay una clase técnica —escalar por tiempo sin
verificar qué se escala— que produjo tres errores en cuatro rondas, en las dos direcciones.*

*Lo que mataría la lectura que queda: que los próximos tres errores sean de clases todas distintas y
sin patrón de escalado. Ahí no hay ni hábito técnico ni sesgo, sólo errores.*

---

## Parte 2 — Dónde el juez usa un PROMEDIO cuando decide el CASO MALO

Auditoría proactiva de `juez.py`. **No se arregló nada**; ésta es la lista pedida.

| # | qué | por qué el caso malo es otro | signo |
|---|---|---|---|
| 1 | `EXCESO_STOP` = exceso **medio** en el stop (0,722 / 0,982 pt) | el stop se desliza mucho justo en las sesiones violentas; la media aplana la cola | **fácil** |
| 2 | `DESLIZAMIENTO_ENTRADA` = medio-spread **medio** por tercil | el spread se abre justo cuando uno quiere salir | **fácil** |
| 3 | `MARKOUT_PASIVO` / `LLENADO_PASIVO` = **medias** sobre entradas al azar | la selección adversa se agrupa: los llenados malos vienen juntos (deudas 1 y 2) | **fácil** |
| 4 | `fi_ses`: escalar el P&L por la fracción **media** de llenado | supone que el no-llenado es independiente del resultado; para un candidato está seleccionado por su señal | **fácil** |
| 5 | `tercil_exante` = rango **medio de barra** de la sesión anterior | es un promedio sobre 46 medias horas que difieren **4,3×** entre sí (`perfil_volatilidad_intradia.py`) | **fácil** |
| 6 | `O_SOBREPASO` aplicado **sólo** en la dirección conservadora | ya está tratado como caso malo, a propósito | **difícil** ✓ |
| 7 | `sd_perm = max(sdA, sdB)` | toma el máximo de las dos nulas, no el promedio | **difícil** ✓ |
| 8 | `cadena_pasar` | usa la distribución entera (P(pasa), P(pago), P(se acaba)), no una media | neutro ✓ |

**Cinco de ocho empujan hacia el lado fácil. Dos van a propósito hacia el difícil. Uno es neutro.**

### El más grande de los cinco, y por qué

El **#5** es el que más cuesta, porque no es una constante sino **el eje con el que se juzga**. El
régimen de una sesión se decide con el rango medio de barra de la anterior — un promedio sobre 46
cajas cuyo factor va de 0,47 a 2,02. Una candidata que opera **sólo la apertura** está siendo
clasificada por catorce horas de madrugada que no le tocan.

*Lo que lo mataría: que al recalcular el tercil ex-ante usando sólo las cajas que la candidata
realmente opera, las etiquetas coincidan con las actuales en más del 90% de las sesiones. Es
medible y no está medido.*

---

## Parte 3 — La regla que sale de todo esto, propuesta y NO implementada

Cada constante de `instrumentos.py` lleva hoy `origen`, `n` y `reparto`. Faltaría un cuarto campo:

```
estadistico: "media" | "cola"
```

…y que el juez **se niegue a usar una `media` donde la barrera es absorbente**. Cinco de las ocho
entradas de la Parte 2 cambiarían de forma.

*Lo que lo mataría: que al recalcular el piso con percentil 90 en vez de media en esas cinco, el piso
se mueva menos de lo que ya lo mueve el régimen (13× entre terciles). Sería ruido al lado de lo que
ya sabemos, y agregar un campo no valdría la complejidad.*

**Estado: NO implementado.** Va escrito para que Roberto decida, no como pendiente silencioso.

---

## Procedencia

`juez.py` · `instrumentos.py` · `perfil_volatilidad_intradia.py` + `salida_perfil_intradia.txt` ·
`calibrar_por_regimen.py` · `cortes_tercil_muestra.py`. Los errores 1 y 2 vienen de otras ventanas y
se citan como recibidos, no como medidos por ésta.
