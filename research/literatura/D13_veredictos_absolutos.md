# D13 — Veredictos ABSOLUTOS de L01, L03 y L10 con el perfil medido por la VENTANA G. Sin orden: el ranking sigue congelado.

**VENTANA L. NO MIDE CANDIDATAS; corre CONTROLES DEL INSTRUMENTO desde el 2026-09-05 (rol ampliado por Roberto, ver `INDICE`). K sigue en 261.**

**Roberto corrigió un exceso de rigor mío:** dije que descongelar sólo el grupo A compararía
calibraciones distintas. **Eso vale para RANKEAR, no para JUZGAR.** *"¿L03 es ciega?"* es una pregunta
absoluta —el margen está debajo de 1 o no está— y no requiere comparar con nadie. **Acá van tres
veredictos absolutos, uno por uno, con el número y con el método al lado. Ningún orden.**

**Fuente de todos los desvíos:** `research/ventana_g/salida_perfil_intradia.txt` (commit `7461919`) y
`research/ventana_g/PARA_VENTANA_L.md` §0 (commit `50a1af3`). **Leídos del archivo, no relevados.**
Regla de cálculo: la de `D06` —`(a) = t*·σ/√n` con `t* = 3,0`, `(c) = 0,42 × publicada` salvo donde el
descuento no corresponde, CIEGA si `(c) < (a)`—, sin cambiarle nada.

**Método por candidata, como pidió Roberto:** la apertura (caja #31) es constante entre años —G lo
verificó: 2,03 / 2,26 / 2,11 / 2,39— y usa el desvío agregado. **La tarde (caja #43) NO es constante
—1,37 a 2,33— y usa la SERIE anual.** Para una media con eventos repartidos entre años, el desvío que
entra en `(a)` es la raíz de la media ponderada de las varianzas anuales: `σ_ef = √(Σ n_y σ_y² / n)`.

---

# L01 — Baltussen, última media hora (caja #43, 15:30-16:00 del este). **CIEGA, margen 0,57.**

| año | σ de la caja #43, pb (G) | factor de G |
|---|---|---|
| 2016 | 16,50 | 1,37 |
| 2017 | 10,52 | 1,89 |
| 2018 | **32,20** | **2,33** |
| 2019 | 18,15 | 1,80 |

- **método: SERIE.** Eventos: todas las sesiones con datos en la caja, `n = 972`, repartidas parejo.
  `σ_ef = √((16,50² + 10,52² + 32,20² + 18,15²)/4) = 20,91 pb`. *(Coincide con el agregado de G, 20,92,
  porque los eventos son todas las sesiones; la serie importaría si se concentraran en un año.)*
- `(a) = 3,0 × 20,91 / √972 = 2,01 pb`
- `(b) = 2,72 pb` (6,86 % anual / 252, del propio paper) → `(c) = 0,42 × 2,72 = 1,14 pb`
- **`(c)/(a) = 0,57` → CIEGA.** Con la magnitud entera, 2,72/2,01 = 1,35: seguiría sin ser una
  aprobación, y la regla usa `(c)`.

**Y el año por año muestra lo que el promedio esconde:** en 2017 sola `(a) = 3×10,52/√243 = 2,02` y en
2018 sola `(a) = 3×32,20/√243 = 6,20`. **Una prueba de L01 corrida sólo en 2018 sería tres veces más
ciega que una corrida sólo en 2017.**

# L03 — Kurov, media hora previa a las 10:00 (caja #31, 09:30-10:00 del este). **CIEGA, margen 0,86.**

- **método: CONSTANTE.** Caja #31, `σ = 23,39 pb` agregado (factor 2,02 sobre 11,58). Años: 24,47 /
  12,59 / 29,16 / 24,16; la raíz de la media de varianzas da 23,41, lo mismo.
- Eventos: 4 anuncios × 48 meses = `n = 192`, repartidos parejo.
- `(a) = 3,0 × 23,39 / √192 = 5,06 pb`
- `(b) = 10,4 pb` (la mayor de las cuatro) → `(c) = 0,42 × 10,4 = 4,37 pb`
- **`(c)/(a) = 0,86` → CIEGA.**

**Y es ciega con tres cosas a su favor que no le corresponden:** (i) el desvío es el de todos los días,
y los días de ISM son más volátiles que el promedio; (ii) la magnitud 10,4 es la respuesta a la
**sorpresa**, y lo operable es el **desbalance**, cuya correlación con la sorpresa es +0,19
(`HIBRIDAS.md`); (iii) la salida tiene un costo no incluido (`D11`). **Las tres apuntan al mismo lado:
más ciega.** Con la magnitud entera, 10,4/5,06 = 2,05 —lo anoto para que se vea— pero es la
magnitud del informado, no la del que sigue el desbalance.

# L10 — Harvey, Mazzoleni y Melone. **Dos veredictos, porque son dos objetos.**

## L10 tal como está publicada: retorno del día siguiente, cierre a cierre. **CIEGA, margen 0,46.**

Ya estaba en `D06` con el desvío medido por G (82,8 pb, `n = 46`): `(a) = 36,6`, `(b) = 17,0` entera,
factor 2,15. **El perfil intradiario no la toca porque su ventana es la sesión entera.** Con 47
eventos en vez de 46 cambia en el segundo decimal.

## L10 en ventana de una hora (cajas #42 + #43, 15:00-16:00 del este). **NO CIEGA en cota optimista: 1,44. Pero con un grado de libertad NUESTRO.**

| año | σ #42, pb | σ #43, pb | **σ de la hora, pb** (ρ = 0) |
|---|---|---|---|
| 2016 | 19,73 | 16,50 | 25,72 |
| 2017 | 7,91 | 10,52 | 13,16 |
| 2018 | 23,33 | 32,20 | **39,76** |
| 2019 | 12,20 | 18,15 | 21,87 |

- **método: SERIE.** Eventos: 47 fines de mes (12 / 12 / 12 / 11; el 48º cae en la caja y se declara
  fuera, decisión ya tomada). `σ_ef = √((12·25,72² + 12·13,16² + 12·39,76² + 11·21,87²)/47) = 26,99 pb`.
- **La hora no está en la tabla de G**: se suma la varianza de las dos medias horas, como G indica
  para ventanas de otro largo. **Supone correlación cero entre las dos medias horas: FRÁGIL.** Con
  ρ = 0,2 —del orden de lo que la literatura de momento intradiario documenta entre tramos vecinos—
  `σ_ef = 29,46`.
- `(a) = 3,0 × 26,99 / √47 = 11,81 pb` (ρ = 0) · `12,89 pb` (ρ = 0,2)
- `(b) = 17,0 pb`, **sin descuento** (documento de trabajo, período de prueba anterior a la publicación)
- **`(c)/(a) = 1,44` (ρ = 0) · `1,32` (ρ = 0,2) → NO CIEGA en la cota optimista.**

> ## **Pero el 17 pb NO está publicado para esa ventana.** El paper lo mide *"over the next day"*, cierre a cierre (`rebal.txt`, línea 42; ficha `L10` línea 210). La versión de una hora la construí yo en `F15`, y `F15` mismo la marcó como el grado de libertad que `F9` prohíbe. **El veredicto absoluto es: REQUIERE MEDICIÓN, con un grado de libertad nuestro declarado.** No es una sobreviviente limpia de la literatura: es una híbrida con ajuste, y así queda.

**Lo que la haría medible sin comprar nada:** el desvío de la última hora en los 47 fines de mes
está en el ES 1-min que ya tiene el repo. Es una medición de G, no mía, y no pre-registra nada.

## Y una corrección a `D09`, con número medido en vez de estimado

`D09` usó *"17,5 % de la varianza diaria en la última hora"*, marcado FRÁGIL. **La participación medida
por G de las cajas #42 + #43 en la varianza de la sesión es `724,3 / 78,5² = 11,75 %`.** Con eso, para
1987-1996: `σ_hora = 100 × √0,1175 = 34,3 pb`, `(a) = 3 × 34,3/√120 = 9,39`, **margen 1,81** en vez de
1,48. **Sigue FRÁGIL por dos transferencias:** la forma de 2016-2019 a 1987-1996, y el desvío diario de
100 pb de esa época que no está medido.

---

# Resumen, sin orden

| candidata | veredicto absoluto | margen | método |
|---|---|---|---|
| **L01** | **CIEGA** | **0,57** | serie anual, caja #43 |
| **L03** | **CIEGA** | **0,86** | constante, caja #31 |
| **L10 publicada** | **CIEGA** | 0,46 | desvío medido de sesión |
| **L10 una hora** | **REQUIERE MEDICIÓN, grado de libertad nuestro** | 1,44 / 1,32 | serie anual, #42 + #43, ρ = 0 / 0,2 |

# La respuesta derecha a la pregunta de Roberto: ¿queda algo vivo y medible en la ruta de la literatura?

**Casi cero, y el "casi" tiene nombre y etiqueta.**

| estado | cuántas | cuáles |
|---|---|---|
| CIEGA con número | **8** | L01 (0,57), L02, L03 (0,86), L06, L10 publicada (0,46), L11, y L04/L09 como familia de L01 |
| NO EVALUABLE | **1** | L05, es un eje |
| **medición que hoy nadie puede hacer** | **2** | L07, L08 (`T02`) |
| **viva y medible hoy, con grado de libertad nuestro** | **1** | **L10 en una hora**, margen 1,44 en cota optimista |

> ## **Once candidatas de la literatura, tres rondas de filtros y un perfil medido: lo único que queda con margen arriba de 1 y datos en el repo es una ventana que dibujé yo. Es un cero de la ruta de la literatura con once números detrás, más una híbrida que hay que declarar como lo que es.**

**Costos:** dinero cero, cartuchos cero, K en 261. Tiempo de Roberto: leer.
