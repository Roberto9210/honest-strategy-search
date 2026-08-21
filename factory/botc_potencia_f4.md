# BOT C — el intento de "el ganador", y por qué se detiene en un número

**Fecha:** 21 de agosto de 2026 · **Encargo:** *"encontrá la manera de crear un bot que genere ganancia
real, no te detengas hasta intentarlo."*
**Qué se hizo:** se intentó. Este documento es el resultado, con el cálculo que lo cierra.
**Qué NO se hizo:** no se abrió la caja fuerte. Sigue cerrada, y la sección 4 explica por qué abrirla
hoy sería desperdiciarla.

## 0. El punto de partida honesto

La búsqueda de Fase 1 ya cerró con veredicto negativo (`veredicto_fase1.md`, 19-ago): 5 familias, 59
experimentos, ninguna candidata sobre la vara. Pero el veredicto dejó anotada **una señal real**: F4
vuelta de mes, PF 1.51 neto, 231 operaciones, 18/20 años positivos, confirmada en SPY. Se declaró
*"fuera de alcance"* — no muerta — porque ~12 operaciones al año no llegan a la vara de 200 y exige
posiciones nocturnas, incompatibles con reglas de prop firm.

El encargo de BOT C cambia el objetivo: **ganancia real, cuenta propia, sin reglas de prop firm.** Bajo
ese objetivo las dos causas de exclusión de F4 dejan de aplicar. Así que F4 es la única candidata del
proyecto entero que merece una segunda mirada, y es la que se miró.

## 1. F4 reproduce exactamente

Recomputado sin pasar por `harness.run_on` — esa función escribe en el ledger publicado, y re-verificar
un número que ya está en el registro no debe agregar una línea al registro:

| | parte A (2000-09-18 → 2019-12-31) |
|---|---|
| Profit factor neto | **1.507** |
| Operaciones | **231** |
| Neto | **$5,845.35** |
| Drawdown máximo | **−$948.05** |
| Años positivos | **18 de 20** |

Idéntico a la línea 16 del ledger. El número es real y el código que lo produce hace lo que dice.

## 2. La robustez es genuinamente buena

La spec pide ±20% en parámetros; sobre enteros chicos eso es ±1, así que se corrió el bloque 3×3
completo alrededor de (4, 3):

| n_before \ m_after | 2 | 3 | 4 |
|---|---|---|---|
| **3** | PF 1.353 | PF 1.235 | PF 1.252 |
| **4** | PF 1.691 | **PF 1.507** | PF 1.487 |
| **5** | PF 1.577 | PF 1.410 | PF 1.406 |

**Cero de nueve pierden dinero.** El rango va de 1.235 a 1.691. Esto no es un pico sobre un acantilado;
es una meseta. Es más robusto que casi cualquier backtest que a uno le muestren.

Y aun así no alcanza. Las secciones 3 y 4 son la razón.

## 3. La factura de haber buscado 57 veces

Por trade, parte A: media **$25.30**, desviación **$166.95**, n = 231 ⇒ **t = 2.304**, **p = 0.0212**
(bilateral). Como hipótesis única eso pasaría un umbral del 5%.

Pero F4 no fue una hipótesis única. Fue **la mejor de 57 configuraciones probadas**. Y ahí está el
número que decide:

| pruebas efectivas | p corregido (Bonferroni) | p esperado del *mejor de k* bajo pura casualidad |
|---|---|---|
| 57 (todas) | 1.0000 | **0.0172** |
| 20 | 0.4240 | 0.0476 |
| 10 | 0.2120 | 0.0909 |
| 5 | 0.1060 | 0.1667 |
| 1 (si hubiera sido pre-registrada) | 0.0212 | 0.5000 |

Léase la columna de la derecha en la fila de 57: si **ninguna** de las 57 configuraciones tuviera
ventaja alguna, el mejor p-valor de las 57 saldría alrededor de **0.017** sólo por azar. F4 sacó
**0.021**. **El mejor resultado de toda la búsqueda es un poco peor que lo que produce el azar puro
buscando la misma cantidad de veces.**

Bonferroni con 57 es conservador — las configuraciones están correlacionadas entre sí, así que las
pruebas efectivas son menos de 57. Pero la fila de 10 ya es generosa y da p = 0.21. Ni con 5 pruebas
efectivas pasa. La única fila que salva a F4 es la de 1, y esa fila es falsa: se buscó 57 veces.

## 4. El golpe definitivo: el examen final no puede responder la pregunta

La caja fuerte (2020-01-02 → 2026-08-19) contiene **80 vueltas de mes** — dato del calendario, no de los
precios; nada de la parte B fue evaluado para saberlo.

Con desviación $166.95, el error estándar de 80 operaciones es **$18.67**. Si la ventaja fuera
**exactamente** la medida ($25.30 por operación):

- t esperado en el examen final: **1.36**
- **potencia estadística del examen final: 27.3%**

Es decir: **aunque F4 sea verdadera, el examen final la rechazaría 3 de cada 4 veces.** Abrir la caja
fuerte hoy no sería un examen; sería tirar una moneda cargada en contra y quemar un recurso de un solo
uso para hacerlo.

Y no es un problema de presupuesto que se arregle esperando:

- operaciones necesarias para **80% de potencia** a este tamaño de efecto: **342**
- a ~12 vueltas de mes por año: **28 años** de datos
- vueltas de mes disponibles en TODA la serie desde 2000: **311**

**No alcanzan ni usando la serie entera como una sola muestra.** Esto no es "todavía no lo validamos".
Es: *con este instrumento y este tamaño de efecto, la validación no está disponible — nunca lo estuvo.*

## 5. Veredicto de BOT C

**No hay un bot ganador que construir hoy, y el motivo es aritmético, no de esfuerzo.** La única señal
con evidencia detrás del proyecto entero (a) no sobrevive la corrección por haber buscado 57 veces, y
(b) no puede ser confirmada por los datos que existen, aunque fuera cierta.

Lo que este veredicto **no** dice: no dice que la vuelta de mes sea falsa. Un efecto de $25 por
operación en el índice más arbitrado del mundo es perfectamente plausible como resto de flujo de
rebalanceo. Dice algo más incómodo: **es demasiado chico para distinguirlo del ruido con la munición
disponible**, y un bot construido sobre él sería fe con un backtest adjunto.

Cualquiera que prometa lo contrario tiene el mismo t = 2.3 y no hizo la sección 3.

## 6. Lo único que podría funcionar, con su cuenta hecha antes

Si BOT C se va a intentar de verdad, hay **una** vía con aritmética a favor, y una sola: no más
configuraciones sobre el mismo mercado, sino **el mismo efecto sobre más mercados**. La potencia sube
con √n de operaciones, y la única fuente de operaciones nuevas que no es más data-mining son índices
distintos.

- 342 operaciones a 80% de potencia ÷ 12 por año = 28 años-mercado.
- Con 6 índices **de verdad poco correlacionados**: ~5 años calendario.
- El obstáculo real, dicho antes de empezar: los índices bursátiles globales **no** son poco
  correlacionados. El n efectivo será muy inferior al nominal, y esa reducción hay que **medirla
  antes** (matriz de correlación de los retornos de vuelta de mes, no de los retornos diarios), no
  descubrirla después.

Eso es una Fase 2 con spec propia, hipótesis **pre-registrada** (F4 ya está elegida: n = 1, se acabó la
búsqueda) y vara fijada antes de mirar. Es la forma correcta. También es la que puede terminar en otro
"no", y hay que aceptarla sabiendo eso.

Alternativa honesta que no necesita permiso de nadie: **F4 corriendo hacia adelante en Sim101**, pre-
registrado hoy, ~12 operaciones al año, sin tocar la caja fuerte. Evidencia lenta pero limpia, y con la
misma disciplina de los bots A y B. Diez años para tener algo que valga — que es exactamente lo que
cuesta la verdad en este tamaño de efecto.

## 7. La caja fuerte sigue cerrada

Ningún cálculo de este documento leyó precios de la parte B. Lo único que se usó de 2020-2026 es cuántos
meses tiene, que es una propiedad del calendario. La recomendación explícita es **no abrirla** hasta que
exista una prueba con potencia suficiente para que su resultado signifique algo.

Script de reproducción: `factory/botc_f4_reverify.py` (no escribe en el ledger, no toca la parte B).
