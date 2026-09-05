# Los números de época A (2026) contra B (2017-2019) — commiteados y citables

**VENTANA G. K = 261, no gasta cartucho.** Dinero: $0. La caja sellada no se toca: los tres días A
son posteriores al 2026-08-19.

*Este documento existe porque la VENTANA L tenía estos números etiquetados como RELEVADO —pasados de
boca— y tenía razón en no confiarles nada hasta que existieran en un archivo. **Existían**, en
`salida_desbalance_diag.txt` (commit `79dd615`), pero una salida cruda no es una fuente citable.
Acá quedan con su procedencia y con una corrección que no estaba en el número original.*

## Los seis días

| época | tercil | fecha | mensajes mbo |
|---|---|---|---|
| B | bajo | 2017-06-07 | 3.180.744 |
| B | medio | 2019-05-01 | 5.342.691 |
| B | alto | 2018-04-25 | 7.552.918 |
| A | bajo | 2026-08-26 | 8.359.691 |
| A | medio | 2026-09-02 | 9.654.846 |
| A | altoREL | 2026-09-01 | 12.115.743 |

## 1. Cambios del MEJOR PRECIO por sesión — 10,6×

| época/tercil | cambios de mejor precio | antigüedad mediana del estado en un llenado |
|---|---|---|
| B/bajo (2017) | **24.349** | **7.320,9 ms** |
| B/medio (2019) | 59.127 | 1.733,8 ms |
| B/alto (2018) | 106.424 | 704,6 ms |
| A/bajo (2026) | 185.303 | 633,5 ms |
| A/medio (2026) | 229.411 | 519,4 ms |
| A/altoREL (2026) | **259.262** | **318,3 ms** |

**259.262 / 24.349 = 10,6×.** Antigüedad mediana del estado: **7.321 → 318 ms**, 23× más fresco.

**Fuente:** `desbalance_diagnostico.py` → `salida_desbalance_diag.txt`, commit `79dd615`.

## 2. La corrección que el número original no traía — 3,7×, no 10,6×

El 10,6× cuenta **cambios de precio**. Con el libro arreglado (`con_tamano=True`), que cuenta también
los cambios de **tamaño** al mejor precio, la misma comparación da:

| época/tercil | filas de BBO (precio **y** tamaño) |
|---|---|
| B/bajo (2017) | 1.550.909 |
| B/medio (2019) | 2.614.351 |
| B/alto (2018) | 3.201.114 |
| A/bajo (2026) | 3.641.066 |
| A/medio (2026) | 4.229.492 |
| A/altoREL (2026) | 5.660.704 |

**5.660.704 / 1.550.909 = 3,7×.**

**Y eso es un hecho distinto y más interesante que el 10,6×:** entre 2017 y 2026 crecieron **más los
cambios de precio (10,6×) que los de tamaño (3,7×)**. El libro no sólo se aceleró — **cambió de
composición**: en 2026 una fracción mucho mayor de la actividad mueve el precio en vez de sólo
engrosar o adelgazar la cola.

**Fuente:** `desbalance_libro_v2.py` → `salida_desbalance_v2.txt`, commit `9a02717`.

## 3. Qué se puede y qué NO se puede concluir de esto

**SE PUEDE:** los días A y B difieren en actividad de libro por factores de 3,7× a 10,6×. Cualquier
medición de microestructura calibrada en una época y aplicada a la otra arrastra esa diferencia.

**NO SE PUEDE** —y ésta es la parte que hay que separar antes de contárselo a nadie—:

| lo que es **CONTRACTUAL** | lo que es **DE MERCADO** |
|---|---|
| la comisión de ida y vuelta ($5,76 ES / $1,82 MES) | la calidad de llenado |
| el valor del punto, el tick, el horario | la posición en la cola |
| el objetivo, el drawdown, la consistencia | la selección adversa |
| | el medio-spread **efectivo** |

**La estabilidad de lo primero no dice nada sobre lo segundo, y las veníamos tratando como una sola
cosa.** Cuando en esta ventana se dijo *"el costo no cambió en diez años"*, lo que estaba medido era
el **medio-spread**, que está anclado al tick mínimo de 0,25 puntos — o sea que es lo único que **no
podía** cambiar aunque todo lo demás cambiara. Es una observación sobre el reglamento del CME, no
sobre el mercado.

**Ese negativo está marcado NO ESTABLECIDO** en
[`REGLA_resolucion_del_instrumento.md`](REGLA_resolucion_del_instrumento.md).

## 4. Lo que falta medir, nombrado

La comparabilidad A/B **no está resuelta**. Para resolverla harían falta tres mediciones que
**no hice**: profundidad al mejor precio, tamaño medio de orden, y vida media de una orden, cada una
comparada entre épocas. Con los seis días en disco cuestan **$0** y una corrida.

*Mi condición de muerte para la idea, declarada: si las tres dan lo mismo entre A y B, la
comparabilidad se sostiene y esto queda como una diferencia de conteo sin consecuencia.*

## Procedencia

`desbalance_diagnostico.py` · `salida_desbalance_diag.txt` (`79dd615`) · `desbalance_libro_v2.py` ·
`salida_desbalance_v2.txt` (`9a02717`) · `verificar_acciones_mbo.py` · `salida_acciones_mbo.txt`
(`cf0b1c6`).
