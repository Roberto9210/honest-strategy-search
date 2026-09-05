# Regla: antes de publicar un negativo, medir la resolución del instrumento

**VENTANA G. K = 261, no gasta cartucho.** Dinero: $0.

## El enunciado

> **Antes de publicar un negativo, medir la resolución del instrumento contra la escala del efecto
> buscado. Un negativo sin esa medición no es un "no": es un "no medido", y se reporta así.**

## El caso que la enseña, y que casi cuesta caro

La Pieza 3b preguntaba si el estado del libro antes de un llenado predice si ese llenado fue
envenenado. Las tablas dieron `rho` entre −0,067 y +0,050 y el filtro empeoraba el markout en todos
los umbrales. **Estaba a un renglón de publicar "el libro no avisa".**

Lo cierto era otra cosa: `mbo_lib.reconstruir` anotaba el BBO **sólo cuando cambiaba el precio**, así
que el desbalance quedaba congelado desde el último cambio de precio. Medido: **669 ms de antigüedad
mediana** en el instante del llenado, y **67%** de los llenados con estado más viejo que 100 ms. Las
filas de "adelanto" estaban comparando el mismo número consigo mismo.

Arreglado (`con_tamano=True`), la antigüedad mediana consultando con 100 ms de adelanto baja a
**48,6 ms** — 14× mejor — y **recién ahí** la pregunta se puede contestar.

**Y el negativo que se habría publicado habría cerrado la palanca más grande que tenemos**, la que
lleva el piso de $78 a $15. Un negativo mal fundado no es sólo un error: es una puerta que se cierra.

## La verificación retroactiva, que era mi propia condición de muerte

Mi criterio era: *"si TODOS los negativos ya publicados traen su verificación de resolución, el paso
existe de hecho y no hace falta escribirlo como regla"*. **No la traen.** La regla se escribe.

### Los que SÍ la traen

| negativo | cómo la verifica |
|---|---|
| firma `timing`: 0 falsos positivos en 20.000 nulos | IC95 de Wilson, cota superior 0,019% |
| nulos **estructurados**: 0,130% en la familia agrupada | IC95 por familia; y **por eso** se detectó que fallaba la vara |
| cortes de tercil sensibles al tamaño de muestra | bootstrap a n = 3…500, con el error de etiqueta |
| **3a / 3b / 3c rehechas** | antigüedad del instrumento medida **antes**, más σ y monotonía por umbral |
| **el juez mismo, en cada veredicto** | imprime la resolución y devuelve **NO MEDIBLE** cuando el error supera la ventaja de referencia |

### Los que NO la traen — quedan marcados **NO ESTABLECIDO**

Verificado por grep sobre las salidas commiteadas: ninguna contiene una afirmación de resolución,
error, potencia ni intervalo.

| negativo publicado | archivo | estado |
|---|---|---|
| "el eje de **dirección** no separa los pisos; es volatilidad disfrazada" | `salida_juez_regimen_direccion.txt` | **NO ESTABLECIDO** |
| "la **latencia** de 250 ms no abolla los llenados" | `salida_microestructura_latencia.txt` | **NO ESTABLECIDO** |
| "el **costo de entrada no cambió** en diez años" | `salida_microestructura_tbbo.txt` | **NO ESTABLECIDO** |
| "el piso **pasivo** es $15,45 / $32,33" | `salida_piso_pasivo.txt` | **NO ESTABLECIDO** |
| "el 53% no llenado / el markout pasivo sobrevive" | `salida_mbo_entrada_pasiva.txt` | **NO ESTABLECIDO** |

*"NO ESTABLECIDO" no quiere decir "falso". Quiere decir que no sabemos si el instrumento podía ver
el efecto que dice no haber visto, y que hasta medirlo no se puede citar como un "no".*

### La ironía, y es la parte accionable

**El juez sí tiene la disciplina metida en el código** —calcula la resolución de cada candidato y se
niega con NO MEDIBLE cuando no alcanza— **y los scripts que le calibraron las constantes no la
tienen.** Está al revés: las constantes son aguas arriba del juez. `MARKOUT_PASIVO`,
`LLENADO_PASIVO`, `DESLIZAMIENTO_ENTRADA` y `EXCESO_STOP` entran al juez sin que nadie haya medido si
el instrumento que las produjo podía verlas.

**Y ya hay un caso confirmado:** `LLENADO_PASIVO` (0,477 / 0,514 / 0,469) se calibró con el libro
viejo. Con el libro arreglado, el mismo simulador a la misma latencia y misma muerte da **0,387 a
0,436**: entre 10% y 20% menos de llenado. El markout también se mueve. **La constante que sostiene
el piso pasivo de $15,45 está calibrada sobre el instrumento roto**, y recalibrarla es trabajo
pendiente y declarado.

## Cómo se aplica, en tres líneas

1. **Nombrar la escala del efecto buscado** antes de medir (un tick, 100 ms, $20 por sesión).
2. **Medir la resolución del instrumento en esas mismas unidades** (antigüedad del estado, error
   estándar, MDE, tamaño de muestra).
3. Si la resolución no es holgadamente menor que la escala, **el resultado es "no medido"** y se
   escribe así, con el número de resolución al lado.

## Procedencia

`desbalance_diagnostico.py` · `desbalance_libro_v2.py` + `salida_desbalance_v2.txt` ·
`mbo_lib.py` (`con_tamano`) · `juez_firma_falso_positivo.py` · `juez_firma_nulos_estructurados.py` ·
`cortes_tercil_muestra.py`. La lista de "NO ESTABLECIDO" sale de revisar las salidas commiteadas
nombradas; **es la lista de los negativos que pude enumerar, no una prueba de que sean todos.**
