# A05 — El control externo de la VENTANA G sobre mi número de Baltussen: el 3,96 % ES un desvío, y el 25 pb queda en pie

**VENTANA L. NO MIDE NADA. K sigue en 261.**

**La VENTANA G, en `salida_perfil_intradia.txt` (commit `7461919`), corrió un control externo contra
mi derivación de "~25 pb por sesión" a partir de Baltussen, concluyó que "el control DISPARÓ", y
diagnosticó que dividí un retorno anual por raíz de 252 en vez de por 252.** Y dejó escrito: *"no leí
el paper... La VENTANA L tiene que confirmarlo contra el texto antes de usarlo."*

**Lo confirmé contra el texto. El diagnóstico de G está equivocado, y lo digo con la misma
disciplina con la que reporto mis propios errores.**

## Lo que dice el paper

Baltussen, Da, Lammers y Martens, *JFE* 142 (2021), **Tabla 6**, encabezado textual: *"This table shows
annualized average returns, standard deviations, and Sharpe Ratios"*. Columnas: `Avg ret(%)`,
`Std dev(%)`, `SR`, `Success`. Fila de la señal `rROD`, Panel A, futuros de índice: **6,86 · 3,96 · 1,73
· 0,55**. Y `6,86 / 3,96 = 1,73`.

> ## **El 3,96 % es el DESVÍO anualizado de la estrategia, no su retorno. Dividirlo por raíz de 252 es la conversión correcta de un desvío: 3,96 % / √252 = 25 pb por sesión. La regla de G —"un retorno escala con T, una dispersión con raíz de T"— es correcta y es exactamente la que apliqué.**

**La ficha `L01` lo tenía bien desde el principio** (sección 4: "retorno anual 6,86 % · desvío anual
3,96 %"). G no leyó la ficha ni el paper, lo dijo, y por eso pidió confirmación. **El control funcionó
como control: pidió que se mirara el texto, y el texto decidió.**

## Lo que sí hay que decir de mi 25 pb, porque G tiene razón en la mitad

**Los dos números no son el mismo objeto, y G lo señaló bien antes de equivocarse en el diagnóstico:**

| | mi 25 pb | los 20,92 pb de G |
|---|---|---|
| qué es | desvío por sesión del retorno de la **estrategia** en la última media hora | desvío por sesión del **retorno** de la última media hora del ES |
| sobre qué | una cartera **1/N de varios futuros de índice** | **el ES solo** |
| período | **1974 a mayo de 2020**, incluye 1987, 2008 y marzo de 2020 | 2016-2019 |

**Que una cartera diversificada sobre 46 años dé 25 y el ES solo sobre cuatro años tranquilos dé 21
es consistente: la diversificación baja el desvío y la época lo sube.** Son el mismo orden de
magnitud por razones que se entienden. **No es una confirmación** —definiciones y muestras
distintas— y no la cuento como la quinta.

## Consecuencia para `T01`

La fila de L01 en `T01` dice *"factor 2,07 medido por su propio paper"*. **Ese factor era mi 25 sobre
el 12,1 del escalado uniforme.** Con la medición de G es **20,92 sobre 11,58 = 1,81**, medido en el
ES y en nuestro período. **El número de G reemplaza al mío para todo uso futuro; el mío queda como
lo que era: una cota de orden de magnitud que resultó bien.**

## Y una anotación para `F13`

Es el caso simétrico al de la 6b: **un número mío que la otra ventana marcó como error y no lo era.**
La regla de la casa sirvió igual: G lo marcó como frágil, pidió el texto, y el texto resolvió. **Si G
lo hubiera corregido "por las dudas" habría metido un error nuevo —1,57 pb— donde no había ninguno.**

**Costos:** dinero cero, cartuchos cero, K en 261. Tiempo de Roberto: leer y pasárselo a G.
