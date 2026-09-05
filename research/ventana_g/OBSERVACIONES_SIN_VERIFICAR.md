# VENTANA G — observaciones sin verificar

**Esto NO son hallazgos.** Es lo que vi de paso mientras medía otra cosa, anotado a pedido.
Ninguna de estas observaciones fue pre-registrada, ninguna se probó contra una hipótesis, ninguna
gastó cartucho. **K = 261.** Nada de acá debe citarse como resultado.

Fecha: 2026-09-04.

---

## 1 — Lo que salió distinto de lo que esperaba y no reporté

### 1.1 La reapertura de las 17:00 CT no es «cara»: es otra cosa

`salida_media_exceso.txt` §2. Media del exceso de deslizamiento por hora de entrada, D=4pt:

| hora CT | media | n |
|---|---|---|
| **17:00** | **1,317** | 126 |
| 22:00 (la segunda peor) | 0,883 | 62 |
| 03:00 (la más barata) | 0,336 | 169 |

Reporté «varía 3,9× a 14× con la hora», que es cierto y engañoso. Lo que muestra la tabla es que
**una hora es un valor atípico y las otras veintidós son una banda razonablemente apretada**. A
D=10 la reapertura da 2,271 y a D=20 da 4,969. Con n=126 a D=4 no es ruido.

Por qué importa y no lo dije: **el p95 agrupado que usé en todo el filtro de deslizamiento está
contaminado por una hora.** La constante de costo del proyecto es un promedio sobre una
distribución con un outlier identificado.

### 1.2 La asimetría de la excursión se da vuelta entre 20 y 30 puntos

`terreno_stop_resultado.md` §2, ventana T23:

| D | 2 | 4 | 6 | 8 | 10 | 15 | 20 | **30** |
|---|---|---|---|---|---|---|---|---|
| largo (abajo) | 87,3 | 75,5 | 65,0 | 54,9 | 46,2 | 30,4 | 21,4 | **12,2** |
| corto (arriba) | 90,6 | 81,5 | 70,5 | 60,6 | 51,8 | 34,1 | 22,2 | **10,3** |

La excursión **hacia arriba** toca más seguido que la de abajo en **todas** las distancias de 2 a 20
puntos — y **se invierte en 30**. Movimientos chicos: más a menudo hacia arriba. Movimientos
grandes: más a menudo hacia abajo. Es el sesgo clásico de índices de acciones, medido limpio, con
el cruce localizado **entre 20 y 30 puntos**.

Usé esta tabla en cada filtro de los últimos tres días y nunca mencioné el cruce.

### 1.3 Aguantar largo de noche rompe 67% más seguido que aguantar corto

`salida_compuerta_nocturna.txt` (c). Contra el umbral de 40 puntos:

- excursión adversa de un **largo**: **8,38%** de las noches (1 de cada 12)
- excursión adversa de un **corto**: **5,03%** de las noches (1 de cada 20)

Puse los dos números en la tabla y sólo discutí el peor. **La razón 1,67× es un hecho aparte**, y
es coherente con 1.2: la cola de abajo es más gorda.

### 1.4 La forma de la distribución del exceso es casi invariante de escala

`salida_media_exceso.txt` §1. La razón **media/p95**, restringida a las **46 celdas con n≥100**,
va de **0,20 a 0,33**. Eso cubre cuatro ventanas de tenencia (15 min a 23 horas, un rango de 92×),
los dos lados, y ocho distancias de stop (2 a 30 puntos, un rango de 15×).

Reporté «26–29%» para el subconjunto T23-largo y no noté que se sostenía en toda la tabla. Si esa
invariancia es real, **la cola es predecible desde la media a distancias que nunca se midieron**.

*(Los valores de 0,46 a 0,89 que aparecen en la tabla completa son celdas de n=2 y n=3, donde el
percentil no significa nada. Por eso el corte en n≥100.)*

### 1.5 El resultado de la evaluación está cuantizado, y más fuerte de lo que dije

`salida_criterio_media.txt`. P(total) es **idéntica a cuatro cifras (5,501%) en ocho niveles de
costo consecutivos**, de $0,125 a $0,875 por micro. Expliqué el mecanismo —lo que manda es el
número entero de ganadas— pero no dije lo total que es el efecto: **dentro de una banda ancha, el
costo es literalmente irrelevante.**

### 1.6 Un artefacto de mi propia función, en una tabla publicada

`salida_entrada_potencia.txt`. Dos brackets distintos (5pt:20pt y 10pt:20pt) devolvieron
**exactamente n=6.988**, con p0 y δ diferentes. No es una coincidencia del mercado: mi `n_exacto`
avanza en pasos geométricos (`n*1,05+1`) y los dos cayeron en el mismo escalón. **Los n publicados
están cuantizados hacia arriba hasta un 5%.** No cambia ninguna conclusión, pero está en una tabla
publicada y no lo señalé.

---

## 2 — Dónde creo que estamos midiendo mal

### El supuesto más débil: que la tasa de acierto sin ventaja es exactamente S/(S+T)

**Qué es.** Todo el enfoque descansa en que un operador sin ventaja gana una operación con
probabilidad `S/(S+T)` — 80,0% para el bracket 5pt:20pt. Sale del resultado de barreras para un
paseo aleatorio sin drift.

**Por qué sospecho.** Es una idealización. Los caminos reales a un minuto tienen rebote de
bid-ask, autocorrelación a rezagos cortos y una grilla de ticks discreta. Y sobre todo: **con
barras de un minuto no puedo saber cuál barrera se tocó primero cuando las dos caen dentro del
rango de la misma barra.** Para un objetivo de 5 puntos eso no es raro: 5 puntos está adentro del
rango de una barra de minuto con frecuencia. Mi modelo resuelve esa ambigüedad **por supuesto, no
por observación**.

**Por qué invalidaría más trabajo que cualquier otra cosa.** El criterio ES la brecha entre la
tasa sin ventaja y el equilibrio: **+1,2 puntos**. Si la tasa real sin ventaja fuera 79% u 81% en
vez de 80,0%, el criterio está errado por su propio tamaño. La vara, el 81,2%, el piso, el MDE, la
regla de 1,6×–2,6× — todo se mide desde esa línea de base.

**Qué medición lo resuelve.** Replicar el bracket sobre los datos de ES a un minuto que ya están en
el repo, con entradas al azar, y contar la tasa de acierto realizada contra `S/(S+T)`. Y por
separado, contar qué fracción de operaciones tiene **las dos barreras dentro de una misma barra**
—los casos ambiguos—. Las dos son baratas y usan datos ya comprados. **No lo hice: afirmé la línea
de base y construí encima.**

### Segundo candidato, más chico

`trades_por_dia` (1 ó 3,5 por día) sale de una regla que inventé: «la ventana más chica donde el
toque cruza 50%». **Todas** las conclusiones de tiempo calendario —los 28 años, los meses de
datos— escalan linealmente con ese número, y no está validado contra ninguna medición de tiempo
hasta resolución.

---

## 3 — Ideas propias, etiquetadas por origen

> Mis ideas se agrupan en **calidad de medición**, no en ventaja de mercado. Es el lugar honesto
> donde puedo aportar algo: cualquier estrategia que proponga es la muestra 262 del mismo pozo.

### DEL DATO

**3.1 — La constante de costo agrupa dos regímenes horarios.**
Recalcular el criterio excluyendo la reapertura de las 17:00, que es el outlier de 1.1.
*Qué la mata:* si excluirla mueve el criterio menos que el ruido de Monte Carlo (±0,3 puntos), la
heterogeneidad no importa y esto es contabilidad, no hallazgo.

**3.2 — La cola del deslizamiento puede ser extrapolable.**
Si la razón media/p95 es constante (1.4), el exceso a distancias no medidas se predice desde la
media, y el modelo de costo deja de tener que parar en D∈{4,10,20,30}.
*Qué la mata:* ajustar la forma por celda; si el parámetro de forma se corre sistemáticamente con
D o con la ventana, no es invariante de escala y la extrapolación es inválida.

**3.3 — Largo y corto no son el mismo riesgo de noche.**
El proyecto los trató como simétricos; 1.3 dice que no lo son a 40 puntos.
*Qué la mata:* es 2016-2019, un mercado alcista sostenido. Si la asimetría se invierte o desaparece
en otro régimen es artefacto de período. **Y ese otro régimen está en la caja sellada**, así que
verificarlo cuesta la caja.

### DE MI RAZONAMIENTO

**3.4 — El óptimo del bracket puede ser un artefacto de mi grilla.**
Como el resultado está cuantizado en ganadas enteras (1.5), P(pasar) es una función escalonada del
tamaño del objetivo, y una grilla gruesa puede caer justo en el borde de un escalón.
*Qué la mata:* barrer el objetivo de a un tick y ver si P(pasar) es suave o escalonada. Si es
escalonada, **cualquier óptimo elegido es artefacto de mi modelo y no del mercado** — sería un
resultado contra mis propias tablas, no a favor.

**3.5 — No tengo una idea de mercado que valga darte.**
Todo lo que propondría como estrategia sale del mismo generador que las 261 y no tengo ninguna
razón anclada en dato para preferir una sobre otra. Lo digo en vez de llenar el casillero.
*Qué la mata:* que el proyecto tuviera una medición mostrando que alguna clase de hipótesis de este
generador rinde sistemáticamente distinto. No la tiene; tiene la contraria.
