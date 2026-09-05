# D14 — La cuenta que decide todo: ¿cuántos años necesitaría cada candidata, y esos años existen?

**VENTANA L. NO MIDE NADA. K sigue en 261.** Aritmética sobre veredictos ya emitidos, corrida desde
`scratchpad/cuenta_anios.py` (el código va a un archivo). **El ranking sigue congelado: esta tabla no
ordena, cuenta.**

**La pregunta de Roberto:** la máquina mide con cuatro años de un instrumento; el umbral baja con la
raíz de `n`. ¿Cuál sería el margen de cada candidata con 8, 12 y 16 años? Y para las que cruzan 1:
¿esos años existen, cuántos chocan con la caja, cuántos con la muestra del propio paper?

**Regla:** `margen(n) = margen(4) × √(n/4)`, con el mismo ritmo de eventos por año y el mismo desvío.
`n* = 4 / margen(4)²` es el año exacto de cruce.

---

# 1. LA TABLA — trece filas

| # | candidata | **4 años** | 8 | 12 | 16 | `n*` cruce | **cruce** | de dónde sale el margen |
|---|---|---|---|---|---|---|---|---|
| 1 | L01 Baltussen, última media hora | **0,57** | 0,80 | 0,98 | **1,14** | 12,4 | **entre 12 y 16** | `D13`, serie anual caja #43 |
| 2 | L02 Gao, última media hora | **0,55** | 0,78 | 0,96 | **1,10** | 13,1 | **entre 12 y 16** | `D06` (c) = 1,112 con σ de la caja #43 |
| 3 | L03 Kurov, 09:30-10:00 | **0,86** | **1,22** | 1,49 | 1,73 | **5,4** | **en 8** | `D13`, constante caja #31 |
| 4 | L04 ETF apalancados | — | — | — | — | — | no evaluable: sin magnitud en pb; como regla hereda la fila 1 | `D06` |
| 5 | L05 gamma neta | — | — | — | — | — | es un eje, no una regla | `D06` |
| 6 | L06 VIX, última media hora VX | 0,24 | 0,34 | 0,41 | 0,48 | 70 | **nunca** | **FRÁGIL**: σ diario VX 500 pb supuesto, factor 1,8; `D06` sólo dijo "ciega firme" |
| 7 | L07 Ito-Yamada, 10 min 6J | 1,72 | 2,43 | 2,98 | 3,44 | 1,4 | ya arriba **sin corregir** | `D06`, escalado uniforme; la corrección pendiente (`T02`) sólo baja |
| 8 | L08 Melvin-Prins, 60 min divisas | 1,33 | 1,88 | 2,30 | 2,66 | 2,3 | ya arriba **sin corregir** | idem |
| 9 | L09 crudo | — | — | — | — | — | no evaluable: sin magnitud en pb | `D06` |
| 10 | L10 publicada, día siguiente | 0,47 | 0,66 | 0,81 | 0,94 | 18,2 | **nunca en 16** | `D06` con n = 47 |
| 11 | L10 una hora (grado de libertad nuestro) | 1,44 | 2,04 | 2,49 | 2,88 | 1,9 | ya arriba, ventana mía | `D13`, ρ = 0 |
| 12 | L10 en 1987-1996, ventana de una hora | **1,81 con n = 120 fijo** | — | — | — | — | ventana fija de diez años; no escala | `D13`, FRÁGIL por transferencia |
| 13 | L11 Savor-Wilson, sesión | 0,26 | 0,37 | 0,45 | 0,52 | 60 | **nunca** | `D06` |

*(Trece: las once fichas, con L10 partida en publicada y una hora, más su ventana de 1987-1996. Si
Roberto contaba otras trece, que lo diga y se rehace.)*

**Todo margen de la tabla usa `t* = 3,0`. La vara del programa con K = 261 es 3,73 (`D15`): con ella
todos los márgenes se multiplican por 0,80, y L03 en 8 años queda en 0,98.** Lo dejo en 3,0 porque la
regla de `D06` es que la cota optimista rechaza y no aprueba, y así es comparable con todo lo anterior.

---

# 2. Para cada cruce: ¿existen esos años? (a) fechas, (b) caja, (c) muestra del paper

**Los datos, por instrumento:**

| instrumento | inicio de datos utilizables | fuente |
|---|---|---|
| ES, 1 minuto | **1997-09-09**, lanzamiento del contrato, en proveedores como PortaraCQG. **Databento GLBX: junio de 2010** *(de memoria: **FRÁGIL**; no pude abrir el catálogo hoy)* | `D09`; catálogo de Databento |
| SP en el piso, 1 minuto | **1987** | `D09` |
| 6J, 6E, 1 minuto | mismo Databento desde 2010 (FRÁGIL); los contratos existen desde 1972 y 1999 | — |
| **caja sellada** | **2020-01-02 → 2026-08-19 = 6,63 años, un solo uso**, para todos | regla del programa |

## L03 — cruza en 8 años, `n* = 5,4`

| | |
|---|---|
| (c) muestra del paper | **2008-01-01 → 2014-03-31, 6,25 años.** Adentro no es fuera de muestra |
| (b) caja | 6,63 años, 2020-2026 |
| **años fuera de las dos** | **2014-04 → 2019-12 = 5,75 años**, y 1997-09 → 2007-12 = 10,3 años **de otra época** |
| **con sólo los 5,75 posteriores al paper** | **margen 0,86 × √(5,75/4) = 1,03.** Cruza justo, sin mezclar épocas, y con las tres omisiones desfavorables de `D13` en contra |
| qué haría falta | ES 1-min de 2014-04 a 2015-12: 1,75 años de `ohlcv-1m`, **centavos** en Databento |
| **de qué época son** | **la transición**: Haynes y Roberts miden automático-automático 43 → 51 % del E-mini entre 2012-14 y 2014-16 (`H01` Hecho 6). Son años más parecidos a 2016 que a 2010, pero no iguales |

> **L03 es la única de las trece cuyo cruce se alcanza con años que existen, están fuera del paper y
> fuera de la caja, y cuestan centavos. Y lo alcanza por 3 %, con `t* = 3,0`, sin la corrección por
> anuncios, sin el costo de `D11`, y con la señal del desbalance en vez de la de la sorpresa.** Cuatro
> cosas en contra que no están en el número.

## L01 y L02 — cruzan entre 12 y 16, `n* ≈ 12-13`

| | L01 Baltussen | L02 Gao |
|---|---|---|
| (c) muestra del paper | **1982-04-23 → 2020-05-01**: cubre TODO lo anterior a la caja | 1993-02-01 → 2013-12-31 |
| (b) caja | 6,63 años; para L01 es **el único fuera de muestra que existe** (desde 2020-05: 6,3 años) | 6,63 |
| años fuera de las dos | **cero** | 2014-01 → 2019-12 = **6,0 años** |
| **los 12-13 años que necesita** | **NO EXISTEN fuera de muestra.** Con la caja entera, 6,3 años: margen 0,71 | 6,0 + la caja 6,6 = 12,6: **sólo gastando la caja**, margen 0,98 |
| de qué época | — | 2014-2019 y 2020-2026: **dos épocas** por la medición de G |

> **L01 y L02 no cruzan con ningún año que exista fuera de muestra. El cruce de la tabla es aritmética
> sobre años que serían del propio paper o de la caja.**

## L07, L08, L10 una hora — ya arriba de 1, pero no por años

- **L07**: paper 1999 → 2013. Fuera: 2014-01 → 2019-12 = 6,0 años. **No necesita años: necesita el
  desvío medido (`T02`) y la plomería que G declaró no implementada con tercer candado.**
- **L08**: paper 2004-04-28 → 2012-12-31. **La reforma WM/Reuters de 2015-02 parte el proceso en dos por
  construcción**: la ventana del fixing pasó de uno a cinco minutos. Fuera y post-reforma: 2015-02 →
  2019-12 = **4,87 años**. Con eso, `1,33 × √(4,87/4) = 1,47` en escalado uniforme. Idem: necesita la
  medición, no los años.
- **L10 una hora**: paper **1997-09-10 → 2023-03-17**: **2016-2019 está ADENTRO de su muestra.** Fuera:
  1987-09 → 1997-09 en el piso (10 años, `D09`) y 2023-03 → 2026-08 dentro de la caja (3,4). Decisión en
  `D16`.

## L10 publicada — `n* = 18,2`

Fuera de muestra existen 10 años de piso + 3,4 de caja = 13,4: `0,47 × √(13,4/4) = 0,86`. **Ciega con
todos los años que existen.**

## L11, L06 — `n* = 60` y `n* = 70`

Savor y Wilson 1958-2009: fuera de muestra 2010-2019 = 10 años: 0,41. **Muerta a cualquier `n`
alcanzable.** L06 igual, y además VX no es del CME ni lo lee el juez.

---

# 3. Las épocas, y lo que no resuelvo yo

**Lo que llegó de la VENTANA G por Roberto, y lo escribo con la etiqueta que trae:** *10,6× más eventos
de libro por día en 2026 que en 2017, y la antigüedad mediana del estado del libro de 7.321 ms a
318 ms.* **No lo encontré en un archivo commiteado de G al momento de escribir esto; queda como dato
RELEVADO, no leído de la fuente, hasta que G lo commitee.**

**Si es así, los años no son intercambiables.** Apilar 2010-2015 con 2016-2019 no baja el ruido: apila
dos procesos. Haynes y Roberts y Coughlan y Orlov (`H01`) miden la misma transición desde el lado del
regulador: 31,8 % de alta frecuencia en 2012, 49,7 % en 2021.

| candidata que cruza | años que necesita | de qué época son | ¿los puede usar? |
|---|---|---|---|
| **L03** | 2014-04 → 2015-12 (1,75 años, sobre los 4) | transición 2014-16 | **lo decide la medición de G** de épocas A contra B |
| L01 | ninguno existe fuera de muestra | — | no |
| L02 | 2014-2019 + caja | dos épocas | sólo gastando la caja |
| L08 | 2015-02 → 2015-12 (0,87 años) | post-reforma, una época por construcción | sí, si el desvío medido no la mata |

---

# 4. La respuesta que la tabla le da a Roberto

> ## **¿El cuello de botella fueron las ideas o los cuatro años?** Ninguno de los dos solo. **De trece filas, una sola cruza con años que existen fuera de muestra y fuera de la caja —L03, por 3 %, con cuatro cosas en contra que no están en el número—. Dos cruzan sólo con años del propio paper o de la caja. Cuatro no cruzan con ningún `n` alcanzable. Tres ya estaban arriba y no las frenan los años sino el instrumento y una ventana mía. Tres no tienen número.** Los cuatro años explican UNA fila. El resto lo explica `D15`: el instrumento mide otra cosa que existencia.

**Costos:** dinero cero, cartuchos cero, K en 261. Tiempo de Roberto: leer, y decidir si los centavos
de 2014-2015 para L03 valen la única medición con potencia que la ruta tendría.
