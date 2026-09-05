# El sesgo de dirección del error — la lista, con el signo de cada uno

**VENTANA G. K = 261, no gasta cartucho.** Este documento no arregla nada: nombra y le pone signo.
Arreglar cualquiera de estos es una decisión aparte, y algunos cambian veredictos.

**La regla, que no es de screening sino de auditoría:** cuando encontramos un error, **antes** de
arreglarlo, se anota **hacia qué lado empujaba**. Y proactivamente: dónde estamos usando un
**promedio** cuando lo que decide es el **caso malo**.

---

## Parte 1 — Los errores encontrados, y hacia dónde empujaban

| # | error | hacia dónde | clase técnica |
|---|---|---|---|
| 1 | **El filtro nocturno** | nos hacía la vida **más fácil** | selección de muestra |
| 2 | **La exposición variable de L10 tratada como fija** | **más fácil** | **escalado por tiempo** |
| 3 | **La volatilidad uniforme a lo largo del día** (raíz del tiempo) | **más fácil** | **escalado por tiempo** |
| 4 | **396 pb / √252 en vez de / 252** (conversión de Baltussen) | **más fácil**, ×15,9 | **escalado por tiempo** |

**Cuatro de cuatro apuntan al mismo lado.** Y —esto es lo que lo vuelve accionable— **tres de los
cuatro son la misma clase técnica**: algo escalado por tiempo con la ley equivocada.

**La pregunta que hay que hacerse cada vez que se escala algo por tiempo:**

> **¿Lo que estoy escalando es un RETORNO MEDIO o una DISPERSIÓN?**
> Un retorno medio escala con **T**. Una dispersión escala con **√T**.
> Confundirlos en un horizonte de 252 sesiones se equivoca por **15,9×**, y siempre en la dirección
> que agranda el efecto.

**Por qué esto importa más que "somos optimistas":** un sesgo de deseo no se puede buscar. Una clase
técnica sí. Cuatro de cuatro hacia el lado fácil, con tres de la misma familia, dice que **no hace
falta buscar sesgo psicológico: hay que auditar los escalados**.

*Lo que mataría esta lectura: encontrar dos o tres errores más que sean de otra clase y sigan
apuntando al lado fácil. Ahí sí sería sesgo y no un hábito de cálculo.*

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
