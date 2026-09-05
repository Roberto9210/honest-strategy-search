# D18 — El hueco entre un minuto y media hora: ¿nadie miró, o miraron y no hay nada?

**VENTANA L. NO MIDE NADA. K sigue en 261.**

**La pregunta de Roberto:** reporté que entre 1 y 30 minutos no encontré nada publicado sobre el ES a
≥ 5 operaciones por día. Eso es una de dos: **(A)** nadie miró —y es el único terreno virgen que
queda—, o **(B)** miraron y no hay nada que publicar. **Y lo que la ausencia no prueba, dicho antes:
la literatura publica lo que funciona y lo que es novedoso; un hueco puede ser un cementerio de nulos
que nadie publicó, y eso no se distingue desde afuera.**

---

# 1. Evidencia de (B) que SÍ está publicada — adentro de papers que buscaban otra cosa

**Los nulos que escapan al sesgo de publicación son los que aparecen como resultado secundario en un
paper que se publicó por otro hallazgo.** Hay tres en el corpus que ya tengo en texto.

| fuente | qué miraron | qué encontraron | grano |
|---|---|---|---|
| **Gao, Han, Li y Zhou 2018**, `gao_orig.txt` §6.4 *"Other time frames"*, Tabla 13 | regresión de la última media hora sobre **las otras doce medias horas**, SPY 1993-2013 | *"at the 5% significant level, only r1 and r12 matter. This is generally true across other ETFs as well"* — **diez de doce medias horas intermedias no predicen nada** | media hora |
| Gao et al. 2018, líneas 329 y 357 | el efecto por régimen de volatilidad | *"insignificant in either period"*, *"an insignificant coefficient for r1"* en volatilidad intermedia | media hora |
| **Baltussen, Da, Lammers y Martens 2021**, `baltussen.txt` línea 1347 | el momento intradiario en futuros de divisas | *"this effect is not significant in currency futures"* | media hora |

> **En la grilla de media hora, para el índice, la respuesta es (B) y está publicada: el paper que
> encontró el efecto primera→última media hora buscó en las otras doce y dijo que no hay nada.** Eso
> es exactamente el hueco 30-390 minutos cerrado por quien tenía el incentivo contrario.

# 1b. Lo que trajo la lectura de Roberto, 2026-09-05 — un (B) sobre NUESTRO instrumento, y dos parciales

| fuente | qué miraron | qué encontraron | **grilla que toca** |
|---|---|---|---|
| **Boyarchenko, Larsen y Whelan 2020/2022**, NY Fed SR 917 → `L12` | **el ES**, 1998-2020, retornos del punto medio; estrategias largas en ventanas **horarias** de la madrugada | Sharpe 1,1 → **−0,5** después del diferencial (2:00-3:00); 1,3 → **0,3** (1:30-3:30); *"With transaction costs, the OD is not profitable in practice"* | **horaria, 1 por día, 60-120 minutos.** Es el extremo lento |
| Breedon y Ranaldo 2013, *JMCB* (SNB 2011) — **PARCIAL**: sólo el fragmento indexado | estrategias de hora del día en divisas | *"most of these simple time-of-day trading strategies are not profitable when trading costs are included"* | horaria, divisas. **Toca a L07 y L08 por el lado adverso**, mismo mercado |
| Yamamoto 2012, *JBF* — **PARCIAL**: sólo el fragmento | reglas técnicas intradiarias con desbalance de flujo y de libro, acciones de Tokio | *"not profitable when transaction costs are included"* | minutos, **otro mercado**: por `F13` no cuenta para el ES en ninguna dirección; cuenta como (B) de la clase 1 de `INVENTARIO_2` en general |

**Sobre qué franja queda tocada, con precisión, porque Roberto lo pidió así:**

| franja | estado después de esta vuelta |
|---|---|
| **60-120 min, 1 por día, ES** | **(B), publicado, sobre nuestro instrumento, 23 años.** BLW |
| 30 min, 1 por día, índice | **(B), publicado.** Gao Tabla 13 (§1) |
| **1-30 min, ≥ 5 por día, ES** | **SIN TOCAR.** BLW no mira ahí: sus ventanas son horarias. Nada de lo leído entra en esta franja |
| segundos, ES | el nulo propio de G a 30 s (`9a02717`) |

> **La respuesta de la Tarea 2 no cambia de tamaño: BLW cierra la grilla horaria del ES, no el hueco de
> 1 a 30 minutos.** Lo que agrega es que el cierre de la grilla gruesa ahora está en **nuestro
> instrumento** y no sólo en SPY.

**Y una lectura del mecanismo de BLW que sí alcanza a la franja fina, como argumento y no como
medición:** si el creador de mercado fija el diferencial donde la operación horaria deja de pagar, con
más razón lo fija donde la de minutos deja de pagar —el diferencial es el mismo y el movimiento es
menor (`D17`)—. Es un argumento; la franja de 1-30 min sigue **sin medición publicada**.

# 2. Evidencia de (B) por mecanismo, en la grilla de 1 a 5 minutos — de memoria y FRÁGIL, para que Roberto la verifique

**Estas tres las cito de memoria; no tengo el texto y van a la lista de lecturas de Roberto.**

| fuente | lo que recuerdo que dice | qué probaría |
|---|---|---|
| Chordia, Roll y Subrahmanyam 2005, *JFE*, *"Evidence on the speed of convergence to market efficiency"* | en acciones del NYSE, la predictibilidad de retornos a partir del desbalance de órdenes rezagado **existe a 5 minutos y desaparece dentro de la hora**, y el horizonte se acorta con los años (1993-2002) | que la franja de minutos **fue mirada** y lo que había se agotó |
| Chordia, Roll y Subrahmanyam 2008, *JFE*, *"Liquidity and market efficiency"* | la eficiencia a horizontes de 5 minutos **mejora con la liquidez y con el tiempo**; la predictibilidad de corto plazo cae a lo largo de las décadas | idem, con la tendencia |
| Brogaard, Hendershott y Riordan 2014, *RFS*, *"High-frequency trading and price discovery"* | los de alta frecuencia **operan en la dirección de los cambios permanentes de precio y contra los errores transitorios**, a horizontes de segundos | que lo que hubiera en la franja de segundos a minutos **lo consume el escalón 1**, y no queda residuo para el escalón 3 |

**Y una cuarta que no es de memoria:** Haynes y Roberts (`H01` Hecho 6), Tabla 8: las cuentas grandes
automáticas del E-mini **netean el 67 % de su volumen en un minuto**. El minuto es donde viven ellas.

# 3. Lo que la ausencia NO prueba, con la misma dureza

1. **Nada de lo anterior es sobre el ES a 1-5 minutos.** Gao y Baltussen son de media hora; Chordia es de
   acciones y de otra década; Brogaard es de acciones. **Para el ES entre 1 y 5 minutos, con
   ≥ 5 señales por día, no encontré ni un hallazgo ni un nulo publicado.** Ahí (A) y (B) **no se
   distinguen desde afuera.**
2. **El cementerio existe por construcción.** Cada firma de propietarios que probó y no encontró no
   publicó. Cada tesis que dio nulo tampoco. Lo que se puede decir es que **el terreno no está virgen
   de intentos: está virgen de publicaciones**, y ésas son cosas distintas.
3. **Y lo que sí se puede decir con lo medido en la casa:** G midió el desbalance del libro como
   predictor a 30 s en cero (`9a02717`), y los markouts pasivos a 60-300 s negativos. **Es un nulo
   propio, en el ES, en 2016-2019 y 2026, a la escala de segundos a minutos.** No es literatura, pero
   es el único dato del ES en esa franja que existe en este proyecto, y dice (B).

# 4. La respuesta, en el tamaño exacto que la evidencia permite

> ## **Grilla de media hora: (B), publicado, por los mismos autores del efecto. Grilla de 1 a 5 minutos en acciones: (B) con mecanismo —la predictibilidad existió, se acortó y la consumió la alta frecuencia—, de memoria y pendiente de verificación. Grilla de 1 a 5 minutos en el ES: NO SE DISTINGUE desde afuera; el único dato es el nulo propio de G a 30 s.**

**Consecuencia para `INVENTARIO_2`:** el cero no es "terreno virgen que nadie miró". En la grilla gruesa
está cerrado con nombre y apellido; en la fina, lo que se sabe apunta al mismo lado y lo que no se sabe
no se puede saber leyendo.

# 5. Lo que cambiaría la respuesta

- Un paper sobre **el ES** con horizontes de 1 a 5 minutos y ≥ 5 señales por día que reporte **un nulo
  explícito** convierte la grilla fina en (B). Uno que reporte **un efecto ≥ 1 tick neto** convierte el
  cero de `INVENTARIO_2` en una candidata. **Las dos búsquedas son la misma y van a la lista de Roberto.**
- Que las tres citas de memoria del §2 no digan lo que recuerdo. Entonces el §2 se borra y queda el
  §1, que alcanza para la grilla gruesa y no para la fina.

**Costos:** dinero cero, cartuchos cero, K en 261.
