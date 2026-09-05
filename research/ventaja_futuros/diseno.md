# Diseño de medición — Ventana D, 2026-09-03

**Sólo para lo que la Tarea 2 dejó en pie.** La cuenta está en `potencia.txt`, generada por
`potencia.py` sin leer un precio. Este archivo no mide nada: dice cómo se mediría, y con qué control.
**No se escribe el medidor todavía.**

---

## 0 · Veredicto de potencia, por hipótesis y por la resolución que cada una declaró

| hipótesis | resolución declarada | población en esa resolución, **para MES** | N | ¿alcanza? | estado |
|---|---|---|---|---|---|
| H1 | intradiaria | minutos MES NT8 | 12 nominales, **0 legibles** | NO para ningún tamaño de efecto | **DESCARTADA por falta de datos** |
| H2 | intradiaria | minutos MES NT8 | 12 / 0 | NO | **DESCARTADA por falta de datos** |
| H3 | intradiaria | minutos MES NT8 | 12 / 0 | NO | **DESCARTADA por falta de datos** |
| H2d | diaria | diario MES NT8 | **1.821** | SÍ desde 55 % (potencia 0,995 a α 0,05; 0,979 a α 0,0125). NO a 52 % (0,508) | **SOBREVIVE** |

**Y la línea que no puede faltar:** las tres descartadas **no fueron falsadas**. Se descartan porque
la población de MES en su resolución es cero. Si mañana NT8 sirve meses de minutos, o si Roberto
admite la población ES de Databento (§3), vuelven con este mismo documento congelado, sin
reescribir nada.

Lectura de la tabla de potencia que conviene tener a mano:

| población | N | acierto mínimo detectable al 80 %, α 0,05 | ídem, α 0,0125 |
|---|---|---|---|
| diario MES NT8 | 1.821 | **52,9 %** | 53,6 % |
| minutos MES NT8 (nominal) | 12 | 85,9 % | 94,5 % |
| minutos ES Databento, sellado 2020–2026 | 1.715 | 53,0 % | 53,7 % |

Un efecto de 52 % **no es detectable en ninguna población que tengamos**: harían falta 3.862
decisiones independientes a α 0,05, y 5.938 a α 0,0125. Lo dice la fila A de `potencia.txt`.

**Tres operaciones por sesión** no arreglan eso salvo que sean independientes entre sí, y eso no se
sabe hasta medir la correlación intra-sesión. Con correlación total, tres valen lo mismo que una. Las
dos cotas están impresas; ninguna se elige.

---

## 1 · H2d — las cinco piezas y el control

### 1.1 · La regla completa

- **Datos:** los 252 CSV de Ventana A (guardián `37a0144`+), fuera de los repos, en
  `…\03cf4965-af02-4a1f-8eb0-bc27e9d414df\scratchpad\nt8-daily-csv\`. Se usan **sólo los 30 de `MES`**.
  Columnas `date,open,high,low,close,volume`. Serie hasta 2026-08-21.
- **Contrato por fecha:** el de mayor volumen de la raíz (regla verificada en `37a0144`: total, cero
  empates, cero retrocesos). Nada se calcula a través de un cambio de contrato: la fecha `t` entra
  sólo si `t` y `t−1` caen en el mismo contrato. Eso deja **1.821** pares (guardián, tabla M3).
- **Señal:** `gap_t = open_t − close_{t−1}`. Si `|gap_t| < 0,25` no hay operación.
- **Operación:** un contrato de MES, entrada en `open_t`, salida en `close_t`, sentido `sign(gap_t)`.
- **PnL neto por operación:** `sign(gap_t) × (close_t − open_t) × 5 − 3,90`. El 3,90 es
  `FRICTION_RT` de `factory/harness.py` (spec v1 §2). Supuesto declarado, no medido.
- **Acierto:** `PnL neto > 0`.
- **Estadístico principal:** proporción de aciertos, prueba binomial exacta **a dos colas** contra
  0,5. **Estadístico secundario, obligatorio:** media del PnL neto > 0 (t unilateral). Los dos tienen
  que pasar: un acierto del 55 % con pérdidas grandes y ganancias chicas no es una ventaja.
- **Nivel:** α = 0,05 si H2d es la única hipótesis que llega a correr. α = 0,0125 si Roberto admite
  la población ES para H1–H3 y corren las cuatro. Se fija **antes** de abrir el período intocado.
- **Sin parámetros libres.** El umbral de un tick no se mueve.

### 1.2 · La potencia

De `potencia.txt`, sección C, diario MES:

| intocado | n | 55 % a α 0,05 | 55 % a α 0,0125 | 58 % a α 0,0125 |
|---|---|---|---|---|
| 30 % | 546 | 0,749 — **no alcanza** | 0,528 | 0,932 |
| **50 %** | **910** | **0,909** | 0,768 | 0,995 |

**La partición 70/30 convencional no alcanza para 55 % en el intocado.** Por eso la partición de
abajo es 50/50, y se puede: la regla no tiene nada que ajustar en el período mirado.

Descuento que hay que tener presente: los días con `|gap| < 0,25` no operan. Si en MES son como en
el diario de Yahoo (15,7 % de aperturas idénticas al cierre previo), el intocado queda en ~765
operaciones y la potencia a 55 % / α 0,05 baja a ~0,85. Sigue alcanzando. Si son muchos más, no, y
eso lo dice el control C0 antes de abrir nada.

### 1.3 · La partición

| período | fechas | sesiones aprox. | para qué |
|---|---|---|---|
| **MIRADO** | 2019-05-06 → 2022-12-31 | ~920 | controles C0–C5; **ninguna cifra de acierto de H2d se publica de acá** hasta que el intocado esté corrido |
| **INTOCADO** | 2023-01-01 → 2026-08-21 | ~900 | la única corrida |

La frontera es una fecha de calendario fijada acá, no un porcentaje calculado sobre los datos.
Ninguna sesión del mirado entra al intocado (regla del ledger, fase 2, «CAMBIO DE REGLAS §4.4/§7.1»).

> **Solapamiento a declarar:** el intocado 2023–2026 cae dentro del calendario de la caja fuerte
> 2020–2026 del ES de Databento. Distinto instrumento, distinta resolución, **los mismos días de
> mercado**. Si algún día se abre la otra caja para H1–H3, los dos resultados no son independientes
> entre sí y no se pueden sumar como cuatro pruebas separadas.

### 1.4 · El costo va adentro

Cada fila de operación lleva su PnL neto calculado antes de cualquier agregado. El acierto se decide
sobre el neto. No existe una columna «bruto» en la salida principal; si se imprime, va **después** y
rotulada como diagnóstico. Control de escala (C4): con 2 contratos el bruto da exactamente el doble y
la fricción también.

### 1.5 · Una sola corrida, y qué pasa si falla

1. El script del intocado se corre **una vez**. Su salida cruda se commitea **antes** de escribir una
   palabra de interpretación (práctica de este repo: `8e337ff`, `38ab3ff`).
2. Si el binomial a dos colas no rechaza 0,5, o la media neta no es > 0: **H2d muere.** Se anota
   DESCARTADA con fecha al pie de `hipotesis_congeladas.md`. No hay variante, no hay filtro por
   tamaño de hueco, no hay «probemos 2 ticks», no hay segunda corrida. El intocado queda **gastado**
   para cualquier hipótesis diaria sobre huecos, incluidas las que aparezcan en la sección 4.
3. Si rechaza con proporción **< 0,5**: tampoco confirma H2d. Lo medido es el gap fill, la
   regularidad pública opuesta. Se anota así, y una hipótesis de gap fill sería **nueva**, iría a la
   sección 4 y no tendría intocado donde probarse.
4. Si pasa: es evidencia de **una** regularidad sobre el hueco de mantenimiento o nocturno según
   diga C0, en un contrato, sin deslizamiento medido. No autoriza dinero. Autoriza lo mismo que
   autorizó BOT C: forward en Sim101 con datos reales.

### 1.6 · Los controles — contra qué se compara

Se corren en el **mirado**. Se imprimen **arriba** del resultado, y cada uno declara qué tumba.

| control | qué mide | criterio, fijado ahora | qué tumba si falla |
|---|---|---|---|
| **C0 · PRECONDICIÓN** | % de fechas con `open_t == close_{t−1}` exacto, y la fracción de la varianza cierre→cierre que carga el tramo cierre→apertura | si identidad > 10 % **o** varianza < 10 %: H2d **no es medible como hueco nocturno** con estas columnas | el **rótulo** de H2d: pasa a «hueco de mantenimiento». Roberto decide si vale la pena abrir el intocado para esa pregunta. Es un HECHO A VERIFICAR |
| **C1 · PLACEBO DE SIGNO** | la misma regla con los signos de `gap` permutados al azar, semilla `20260903`, 1.000 permutaciones | el acierto real del mirado tiene que caer fuera de la banda 2,5–97,5 % de las permutaciones **para que el mirado sugiera algo**; no es el test | si cae adentro, no hay señal ni para justificar abrir el intocado |
| **C2 · EXPLICACIÓN RIVAL: momentum diario** | la misma regla con `sign(close_{t−1} − close_{t−2})` en lugar de `sign(gap_t)` | se imprime al lado; si iguala o supera al real, lo que hay es continuación de un día, no hueco | la **atribución** al hueco; no el número |
| **C3 · OTRO LIBRO** | la misma regla sobre `ES` diario, mismas fechas, sin derivar nada de MES | los signos de los dos resultados tienen que coincidir; la magnitud puede diferir (Ventana A: OHLC distintos) | si los signos difieren, hay un artefacto de contrato y se declara **antes** del intocado |
| **C4 · ESCALA** | 2 contratos | exactamente 2× bruto y 2× fricción | **todo** |
| **C5 · UNIONES** | cuántas fechas se descartan por cambio de contrato y dónde caen | se imprime el conteo (esperado 29) y que caen en los trimestres | nada; es el sesgo declarado por Ventana A, impreso para que no se olvide |

---

## 2 · H1, H2, H3 — descartadas sobre MES; diseño **CONDICIONAL** sobre ES de Databento

Esto no es una tercera hipótesis ni una ampliación. Es el diseño que se aplicaría **si Roberto decide**
que una regularidad del índice medida en ES a 1 minuto es evidencia admisible para operar MES. La
ventana no toma esa decisión. Argumentos en los dos sentidos, para que la tome con ellos a la vista:

- **A favor:** H1, H2 y H3 son afirmaciones sobre la estructura horaria del índice, no sobre el
  libro de MES. Las tres fuentes públicas están medidas en SPY, en el ES o en el índice, nunca en
  MES. El costo se aplica en puntos (0,78 por ida y vuelta), que es la unidad común.
- **En contra:** la regla de Ventana A —ninguna raíz se deriva de otra— nació de ver 8 puntos de
  diferencia en la apertura del mismo día entre ES y MES. Una ruptura de rango nocturno por 2 ticks
  en ES puede no existir en MES. H2 es la más expuesta a eso; H1 la menos.
- **Y el precio:** el intocado sería la caja fuerte 2020–2026 de la búsqueda 1, que `ARTICLE.md`
  prometió abrir **una sola vez**. Correr H1–H3 la gasta. Es un uso irreversible de un compromiso
  publicado, y es de Roberto.

### 2.1 · Regla (las tres, tal como están congeladas)

- **Datos:** `data/es_1min_databento.csv`, `ts_event_utc` = apertura de la barra. Conversión a ET con
  horario de verano; la sesión RTH es 09:30–16:00 ET. **Prerrequisito que la fase 2 dejó bloqueado:**
  el mapeo barra → día de negociación CME (`INTRADAY_TRADING_DAY_MAPPING_READY`, ledger G4-bordes).
  Sin ese mapeo probado, no se corre nada.
- **Exclusiones:** los 23 días `degraded` de Databento dentro de 2016+, y los días con menos de 380
  barras en RTH (sesión acortada). Ambos se cuentan e imprimen.
- **Fricción:** 0,78 puntos por ida y vuelta (3,90 USD / 5 USD por punto de MES), aplicada sobre
  puntos de ES. H1 no opera y no paga. H2 y H3 una operación por sesión.
- **H1:** evento `R1 > mediana(R2..R6)`, proporción, binomial unilateral.
- **H2:** evento A (frecuencia) contra control de hora 2; evento B (dirección) sobre acierto neto.
- **H3:** `sign(rL) == sign(r1)` con `r1` desde el cierre del día anterior, acierto neto.

### 2.2 · Potencia

De `potencia.txt`, sección B, población «sellado 2020–2026», N = 1.715: **55 % se detecta con
0,993 a α 0,05 y 0,970 a α 0,0125.** 52 % no (0,487 / 0,270). No hace falta partición nueva: el
intocado ya existe y tiene 1.715 sesiones enteras.

### 2.3 · Partición

| período | fechas | sesiones | estado |
|---|---|---|---|
| MIRADO | 2016-01-04 → 2019-12-31 | 1.032 | **ya abierto y barrido** por la búsqueda 1: 57 configuraciones, incluidas 20 de ruptura de apertura y las de gaps de F4 |
| INTOCADO | 2020-01-02 → 2026-08-18 | 1.715 | la caja fuerte de la búsqueda 1, sellada, **una apertura para las tres juntas** |

**Contaminación declarada:** H2 sobre el mirado no es una hipótesis nueva sobre datos nuevos; es una
familia que ya murió (F1-ORB, PF 1,07) con una definición distinta (primera hora, rango nocturno
completo). Lo que el mirado diga sobre H2 vale menos que lo que diga sobre H1 y H3.

### 2.4 · Costo adentro

Igual que §1.4. Para H3 es lo que decide: 30 minutos de tenencia contra 0,78 puntos. En el mirado se
imprime la mediana de `|rL|` al lado de 0,78 para que se vea si el efecto **puede** pagar el costo
antes de abrir nada.

### 2.5 · Una sola corrida

Las tres en **un** script, **una** ejecución sobre 2020–2026, salida cruda commiteada antes de
interpretarse. α = 0,0125 (cuatro hipótesis, con H2d). La que falle muere. La caja fuerte queda
gastada para toda la fase, no sólo para estas tres.

### 2.6 · Controles

| hipótesis | control | qué tumba si falla |
|---|---|---|
| H1 | (a) la hora 2 como candidata, mismo estadístico; (b) permutación de las etiquetas de hora **dentro** de cada sesión, semilla `20260903`, 1.000 veces | (a) que sea «la apertura»; (b) que sea algo |
| H2 | (a) tasa de ruptura de la hora 2 contra el rango 18:00 → 10:29; (b) para el evento B, signos de ruptura permutados | (a) «tiende a romperse en la apertura»; (b) «la ruptura sirve» |
| H3 | (a) el predictor de la **segunda** media hora, que en Gao et al. no predice; (b) signos de `r1` permutados | (a) el mecanismo publicado; (b) el número |
| las tres | escala 2 contratos = 2×; conteo de sesiones excluidas por `degraded` y por RTH corta | todo / nada |

---

## 3 · Lo que quedó ambiguo, rotulado

| | qué es | quién decide |
|---|---|---|
| ES de Databento como población para H1–H3 operadas en MES | **DECISIÓN**, no medición | Roberto |
| abrir la caja fuerte 2020–2026 para esta fase | **DECISIÓN**, irreversible, compromiso publicado | Roberto |
| la apertura diaria histórica de NT8 es la reapertura de 17:00 CT | **HECHO VERIFICADO sobre una barra** por el guardián; **NO VERIFICADO** para 2019–2025. C0 lo mide en el mirado | C0 |
| «cinco días de minutos» | **NO VERIFICADO**: no está en ningún documento; lo medido es 12 archivos hábiles ilegibles | — |
| costo 3,90 USD ida y vuelta | **SUPUESTO DECLARADO** (spec v1). El 1,50 del encargo, NO VERIFICADO y no usado | Roberto si quiere cambiarlo, **antes** del intocado |
| independencia de tres operaciones por sesión | **HIPÓTESIS PARA MEDIR** en el mirado, si alguna regla llega a tres | el mirado |
| la potencia de la tabla | **HECHO**: aritmética, `potencia.py`, sin datos | — |
| H2d tiende a extenderse | **HIPÓTESIS PARA MEDIR**, propia, a dos colas | el intocado, una vez |

---

# NOTA FECHADA — 2026-09-03 — este diseño quedó enmendado por `hipotesis_congeladas.md`, Enmiendas 1 y 2

**Nada de arriba se reescribe.** Lo que ya no rige, y dónde está lo que rige:

- **§1.1 población:** MES → **ES diario de NT8**. Traslado a MES medido (96,6 % de acuerdo de signo). E1.3, E2.1.
- **§1.2 potencia:** las cifras de arriba usan α = 0,05 y 0,0125. **Rige α = 0,05/262** (K heredado). Con él,
  el intocado detecta desde **55,6 %**, no desde 55 %. E2.2, `potencia_heredada.txt`.
- **§1.3 partición:** **RETIRADA.** Ponía el mirado adentro de la caja del programa (2020-01-01 → 2026-08-19,
  un solo uso). Rige: mirado 2016-08-23 → 2019-12-31 (851 pares de ES), intocado = la caja (1.687). E1.2, E2.3.
- **§1.6 C3 «otro libro»:** el otro libro pasa a ser MES sobre sus 167 pares de 2019, con el criterio de E1.4.
- **§2 (H1–H3 sobre ES Databento):** sigue condicional y ahora con una condición más: su intocado es **la
  misma caja del programa** que la de H2d y la de las familias G de la fase 2. **Un solo uso para todo.**
- **§1.4, §1.5 y el resto de §1.6:** sin cambios.

# NOTA FECHADA — 2026-09-03, más tarde — Enmienda 3 y descarte de H2d

- **Rige el protocolo de la spec** (Enmienda 3): K se cobra en A con la compuerta 1 sobre el mirado, la caja
  se examinaría a 0,05. El α de 0,05/262 sobre el intocado de la nota anterior **ya no rige**.
- **H2d DESCARTADA** por C0: el hueco de las columnas diarias de NT8 carga el 4,01 % de la varianza cierre a
  cierre (criterio congelado: < 10 % dispara). `h2d_compuerta1.txt`. Nada de C1–C5 ni del resultado se calculó.
- **§1 entero queda como registro de un diseño que no llegó a correr su regla.** La caja no se gastó.
