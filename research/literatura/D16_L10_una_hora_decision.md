# D16 — L10 en una hora: tres salidas, una recomendación. **(C) CERRARLA, con la razón nombrada.**

**VENTANA L. NO MIDE NADA. K sigue en 261.**

**El objeto:** la única fila del inventario con margen > 1 (1,44 en cota optimista, `D13`), cuya ventana
—la última hora del último día hábil del mes— **la elegí yo en `F15`**. El paper mide su 17 pb *"over
the next day"*, cierre a cierre.

---

# Los números que deciden, y son tres

**1. La magnitud en una hora no está publicada, y su rango es enorme.** Entre *"todo el efecto cae en la
hora"* (17 pb → margen **1,44**) y *"el efecto se reparte como la varianza"* (11,75 % × 17 = 2,0 pb →
margen **0,17**). **Un factor de ocho entre las dos lecturas, y ninguna de las dos está en el paper.**

**2. Incluso la forma publicada está adentro de la muestra del paper.** Harvey, Mazzoleni y Melone:
**1997-09-10 → 2023-03-17** (`rebal.txt`, línea 602). **2016-2019 es in-sample.** El único fuera de
muestra que existe es el piso 1987-1997 (`D09`) y lo que quede de la caja después de 2023-03.

**3. Con todos los años que existen fuera de muestra, la forma publicada sigue ciega:** `n* = 18,2`
(`D14`) contra 13,4 años disponibles → margen 0,86.

---

# Las tres salidas, costadas

## (A) Declararla candidata nueva — un cartucho, K → 262

**Es lo honesto sobre lo que es: un rediseño nuestro de la idea de otro.** Pero un cartucho sobre un
margen que va de 0,17 a 1,44 según un supuesto que nadie midió, en un período que está adentro de la
muestra del paper, **no es una apuesta que yo le recomendaría a Roberto.** `P07` y `P08` ya mostraron
que L10 y L11 solas necesitaban el 186-204 % de su magnitud para pasar; ésta necesitaría que el 100 %
de un efecto de un día se concentre en una hora. **No escribo el preregistro porque escribirlo sería
darle forma concreta a algo que no recomiendo.** Si Roberto la quiere igual, se escribe en una tarde
sobre `P08`.

## (B) La ventana que implica el mecanismo: los últimos 30 segundos

**Lo que Roberto preguntó, contestado derecho: NO, con el ES de 1 minuto que está en el repo no se puede
medir el ruido de los últimos 30 segundos.** Una barra de un minuto no resuelve medio minuto. Haría
falta `trades` o `tbbo` de Databento para 47 ventanas de 30 segundos: **costo de centavos** (un día
entero de `tbbo` cotizó USD 0,79; 47 medios minutos son una fracción ínfima de eso).

**Pero el dato no es lo que la bloquea.** La magnitud publicada tampoco es de esa ventana —es del día
siguiente entero— y la liquidación del CME es el promedio ponderado de esos 30 segundos: **medir "el
retorno de la ventana de liquidación" es medir el retorno contra el precio de liquidación, que es cero
por construcción para quien sale en la liquidación.** La derivación por mecanismo lleva a una ventana
en la que la regla no tiene salida. **(B) está bloqueada dos veces: por magnitud y por definición.**

## (C) Cerrarla

> ## **RECOMENDACIÓN: (C).** Razón nombrada: **la magnitud publicada no vive en ninguna ventana intradiaria, y la ventana en la que vive está ciega con todos los años que existen fuera de muestra.** El inventario de la literatura queda en **cero limpio**: ocho ciegas con número, tres sin número, dos que nadie puede medir. K sigue en 261.

**Lo que la reabriría, para que no sea un cierre por cansancio:** que los autores —o una réplica
publicada— localicen el efecto **dentro del día** con una magnitud para esa ventana. **El correo
pendiente no pregunta eso**, y está bien que no lo pregunte: tiene una sola pregunta por diseño. Si
Roberto lo autoriza y contestan, la respuesta decide la ventana de 1987-1996, no ésta.

**Costos:** dinero cero, cartuchos cero, K en 261 —y sigue en 261 porque se recomienda (C)—. Tiempo de
Roberto: decidir.
