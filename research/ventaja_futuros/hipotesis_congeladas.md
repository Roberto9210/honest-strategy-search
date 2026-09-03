# Hipótesis congeladas — Ventana D, búsqueda de ventaja en futuros

**Fecha: 2026-09-03.** Este archivo se commitea **solo**, antes de que esta ventana lea un solo
precio. El orden del `git log` es la garantía: si un número de medición existe en un commit
anterior a éste, el congelamiento no vale.

**Instrumento operado: MES (Micro E-mini S&P 500), un contrato.** Ninguna raíz se deriva de otra
(regla de Ventana A, guardián `8e5f5c8`): ES y MES son libros separados y no comparten OHLC.

**Escribe: Ventana D**, sólo en `research/ventaja_futuros/`. Lectura cruzada al repo del guardián
(`deadman-guardian`, commit **`f75d126`**, HEAD de `main` el 2026-09-03), sin tocar nada allá.

---

## 0 · Las poblaciones, POR RESOLUCIÓN — Tarea 1

Nada de esto se re-midió. Cada número trae de dónde salió. Son tres poblaciones, no dos, porque
en este mismo repo hay una serie de minutos que el encargo no mencionaba y que no se puede omitir.

### 0.1 · DIARIO, MES, NT8 — **la única población con resolución suficiente hoy**

| magnitud | valor | procedencia |
|---|---|---|
| contratos MES | 30 | guardián `docs/caracterizacion-diario-nt8-20260902.md` §2, commit `1d9d83a`+ |
| días distintos con barra | **1.880** (2019-05-06 → 2026-08-21) | ídem |
| fechas conservadas tras descartar cambios de contrato | **1.851** | guardián `docs/resultado-pregunta1-terreno.md`, commit `7761eb4`+ |
| **pares consecutivos dentro del mismo contrato** (cierre previo → día siguiente) | **1.821** | ídem, tabla M3, fila `MES` |
| agujeros dentro de la cobertura | 25 hábiles faltantes (1,3 %), 7 en `MES 06-23` (2023-04-06 → 04-14) | guardián §4 y `coverage_audit.txt` del scratchpad de Ventana A |

**N diario para una hipótesis que use apertura contra cierre previo: 1.821 sesiones.** Para una
que use sólo la barra del día: 1.851.

> **HECHO VERIFICADO por el guardián, con su límite declarado (§5 de la caracterización):** la barra
> diaria de NT8 está indexada por fecha de negociación y **la sesión que acumula arranca a las
> 17:00 CT del día calendario anterior**. Medido sobre **una** barra escrita el 2026-09-02 y sobre
> el ajuste actual del catálogo (`TradingHours = ETH`). Que las barras históricas también sean ETH
> es lo esperable y **NO ESTÁ VERIFICADO**. Consecuencia para H2d, abajo.

### 0.2 · MINUTOS, MES, NT8 — **población nominal, cero utilizable**

| magnitud | valor | procedencia |
|---|---|---|
| archivos de minuto `MES 09-26` | **15** `.ncd`, 2026-08-16 → 2026-09-02 | guardián `docs/datos-futuros-nt8-20260902.md` §2; listado del directorio reconfirmado hoy sin cambios |
| de ellos, en día hábil | **12** (17-21 ago, 24-27 ago, 31 ago, 1-2 sep; falta el viernes 28-ago) | nombres de archivo del listado |
| **legibles desde afuera** | **0**: los `.ncd` de minuto no usan el formato fijo del diario (124 de 125 fallan), y se decidió no escribir decodificador | guardián `datos-futuros` §3 |
| exportación de NT8 corrida | ninguna: `export\` vacía | ídem §5 |

**N minutos MES: 12 sesiones nominales, 0 utilizables hoy.** El «cinco días» del encargo **no aparece
en ningún documento del guardián** como conteo de barras en disco; lo que aparece es el período de
carga por defecto de NT8 (5 días) y la medición pendiente de «subir el período de carga muy por
encima de 5 días» (§5 del inventario). Tratar «cinco días» como NO VERIFICADO; lo medido es 12.

### 0.3 · MINUTOS, **ES** (no MES), Databento — en este repo, con QC ya publicado

| magnitud | valor | procedencia |
|---|---|---|
| archivo | `data/es_1min_databento.csv`, `ES.n.0` (front por open interest), OHLCV-1m, UTC | `data/data_quality_es_1min_databento.md`, generado 2026-08-19 |
| días de negociación totales | 4.183 (2010-06-07 → 2026-08-18) | ídem §1 |
| **utilizables como intradía** | desde **2016**: 2010–2015 tienen la sesión comprimida en una barra (92 % de los días de 2010, 71 % de 2012, cola hasta nov-2015) | ídem §3b y `ARTICLE.md` |
| sesiones 2016 → 2026-08-18 | **2.747** (258+257+259+258+259+259+258+258+259+258+164, tabla por año del QC) | ídem §3 |
| de ellas, **ya miradas** por la búsqueda 1 (parte A, 2016–2019) | **1.032** | `factory/spec_busqueda_estrategia.md` §4 y ledger |
| de ellas, **selladas** como caja fuerte de la búsqueda 1 (2020 → 2026) | **1.715** | `ARTICLE.md`: «The hold-out is still sealed: 2020–2026 … open it once» |
| días marcados `degraded` por Databento dentro de 2016+ | 23 de los 31 listados | QC §1b |

**N minutos ES: 2.747 sesiones, de las cuales 1.715 están selladas por una promesa anterior de este
repo y 1.032 ya fueron barridas por 57 configuraciones, incluida la familia «ruptura de rango de
apertura» y la familia «gaps de apertura».**

> **Esta población NO es MES.** Sirve para medir una regularidad **del índice** en la resolución que
> H1, H2 y H3 necesitan; no sirve para medir la ejecución en MES. **Si es admisible como población
> para hipótesis que se van a operar en MES es una decisión de Roberto, no de esta ventana.** Se deja
> planteada, no tomada.

---

## 1 · Definiciones comunes, sin huecos

| término | definición |
|---|---|
| **sesión** | un día de negociación CME del índice: 18:00 ET del día anterior → 17:00 ET, etiquetado por la fecha en que termina |
| **RTH** | 09:30 → 16:00 ET (contado abierto) |
| **noche** | 18:00 ET del día anterior → 09:29 ET |
| **primera hora** | 09:30 → 10:29 ET |
| **hora k de RTH** | bloques de 60 minutos desde 09:30; hay 6,5, el último es 15:30 → 16:00 (media hora) |
| **primera media hora / última media hora** | 09:30 → 09:59 y 15:30 → 16:00 ET |
| **rango de una ventana** | `max(high) − min(low)` de las barras de la ventana |
| **retorno de una ventana** | `close_última − close_anterior_a_la_ventana` en puntos |
| **contrato** | por fecha, el de mayor volumen de la raíz (regla de Ventana A, total, cero empates). Nada cruza un cambio de contrato |
| **acierto** | una operación cuyo PnL **neto de fricción** es > 0. La fricción va adentro de cada operación, nunca restada al final |
| **fricción** | `FRICTION_RT = 3,90 USD` por ida y vuelta por contrato de MES (`factory/harness.py`, spec v1 §2: comisión 1,40 + 2 ticks de deslizamiento). Es un **supuesto declarado**, no una medición. En puntos de MES: **0,78**. El «1,50 USD ida y vuelta» del encargo queda **NO VERIFICADO y no se usa** |
| **potencia** | 80 %, contra H0 = 50 % de acierto, α unilateral 0,05 y también α = 0,0125 (cuatro hipótesis, Bonferroni). La cuenta va en `potencia.py`, aparte y posterior a este archivo |

---

## 2 · Las hipótesis

Cada una trae los dos campos obligatorios: **RESOLUCIÓN QUE NECESITA** (declarada aquí, antes de la
cuenta de potencia) y **FALSADOR** (la observación concreta que la tira). Y el estado de su
protección contra pescar: **PÚBLICA** (regularidad publicada antes de que la miráramos) o
**HIPÓTESIS PROPIA**.

### H1 · La primera hora de Nueva York se mueve más que el resto del día

**Estado: PÚBLICA.** Es la forma en U de la volatilidad intradía: Wood, McInish y Ord (1985),
Harris (1986), y para el futuro del S&P 500 Andersen y Bollerslev (1997, *Journal of Finance*,
«Heterogeneous information arrivals and return volatility dynamics»), que miden volatilidad alta
tras la apertura y antes del cierre, y baja al mediodía.

**Definición completa.** Para cada sesión con RTH completa, `R1 = rango(09:30→10:29)` y
`Rk = rango(hora k)` para k = 2..6 (10:30→11:29 … 14:30→15:29; el bloque 15:30→16:00 se excluye por
ser media hora y por ser el otro brazo de la U). Evento por sesión: `R1 > mediana(R2..R6)`.

**RESOLUCIÓN QUE NECESITA: intradiaria** (barras de 1 minuto, o de 5 como mínimo).

**FALSADOR.** En el período intocado, la proporción de sesiones con `R1 > mediana(R2..R6)` **no
supera 0,5** al nivel declarado; **o** el control la iguala: la misma proporción calculada para
`R2 > mediana(R3..R6, R1)` (la hora 2 como candidata) no es menor que la de la hora 1. Si la hora 2
«gana» tanto como la primera, la regularidad no es de la apertura.

**Lo que H1 no es:** no es una regla operable. Un rango grande no dice hacia dónde. Su versión
operable sería otra hipótesis, y no se agrega.

### H2 · El rango de la noche tiende a romperse en la apertura

**Estado: PÚBLICA como regularidad de operadores, no académica.** «Opening range breakout» (Crabel,
1990, *Day Trading with Short Term Price Patterns and Opening Range Breakout*). Evidencia reciente
en contra sobre el micro del Nasdaq: Mesfin (2026, arXiv 2605.04004, MNQ 2021–2025, 947 sesiones de
5 minutos): ninguna de 14 familias OHLCV, incluidas rupturas y gaps, supera una fricción de 2 puntos.
**Evidencia previa de este repo, y es adversa:** la familia 1 de la búsqueda 1 (ORB 15/30 min, 20
configuraciones, 2016–2019) murió con PF 1,07 en su mejor variante (`factory/veredicto_fase1.md`).

**Definición completa.** `Hn, Ln` = máximo y mínimo de la noche (18:00 ET previo → 09:29 ET).
Evento A (frecuencia): en la primera hora hay al menos una barra con `high > Hn` o `low < Ln`.
Evento B (dirección, el único operable): tomada la **primera** ruptura de la primera hora, con
entrada al cierre de la barra que rompe y salida al cierre de RTH (16:00), la operación en el
sentido de la ruptura tiene PnL neto > 0. Una operación por sesión, la primera ruptura y ninguna
otra. Si rompe por los dos lados en la misma barra, no se opera.

**RESOLUCIÓN QUE NECESITA: intradiaria** (1 minuto; con 5 minutos la ruptura se detecta con hasta
4 minutos de retraso y se declara).

**FALSADOR.** (i) Evento A: la proporción de sesiones con ruptura en la primera hora **no supera** la
del control, que es la misma medición para la hora 2 contra el rango 18:00 → 10:29. (ii) Evento B:
la proporción de aciertos netos en el período intocado **no supera 0,5** al nivel declarado. Cualquiera
de los dos tira la parte que le corresponde: (i) tira «tiende a romperse en la apertura», (ii) tira
«la ruptura sirve para algo».

### H3 · Reescrita — el retorno de la primera media hora predice el signo de la última media hora

**Por qué se reescribió.** Tal como venía («el día cierra en la dirección de su última hora») no
tiene falsador: el cierre **es** el final de la última hora, así que el evento se cumple por
construcción salvo empate. Se reemplaza por la regularidad publicada más cercana.

**Estado: PÚBLICA.** Gao, Han, Li y Zhou (2018), «Market intraday momentum», *Journal of Financial
Economics* 129(2): 394–414: el retorno de la primera media hora (medido desde el cierre del día
anterior) predice el de la última media hora, en SPY 1993–2013 y en otros diez ETF; más fuerte en
días volátiles y de anuncios macro.

**Definición completa.** `r1 = close(09:59) − close(16:00 del día anterior)` en puntos (la
definición de Gao et al., que incluye el hueco nocturno). `rL = close(16:00) − close(15:29)`.
Operación: al cierre de la barra de 15:29, entrar en el sentido de `sign(r1)`, salir a las 16:00.
Una por sesión. Si `r1 = 0`, no se opera.

**RESOLUCIÓN QUE NECESITA: intradiaria** (1 o 5 minutos).

**FALSADOR.** La proporción de sesiones con `sign(rL) = sign(r1)` en el período intocado **no
supera 0,5** al nivel declarado, contada sobre acierto **neto** (30 minutos de tenencia contra 0,78
puntos de fricción: es la hipótesis a la que más le pesa el costo). Control: el mismo predictor
reemplazado por el retorno de la **segunda** media hora (10:00 → 10:29), que en Gao et al. no
predice; si predice igual, no es el mecanismo publicado.

### H2d · Versión diaria de H2 — el hueco de apertura tiende a extenderse durante el día

**Estado: HIPÓTESIS PROPIA.** Se buscó como regularidad publicada y **no se encontró en este
signo**. Lo publicado apunta al revés o depende del tamaño:

- Grant, Wolf y Yu (2005), «Intraday price reversals in the US stock index futures market: a
  15-year study», *Journal of Banking & Finance*: tras huecos de apertura grandes (≥ 0,10 %,
  0,20 %, 0,30 %) el futuro del S&P 500 muestra unos 10 minutos de continuación y luego una larga
  serie de **reversiones**.
- Lo popular entre operadores es el «gap fill»: sitios de estadística de trading reportan que
  alrededor del 70 % de los huecos de ES se cierran en la misma sesión, con tasas menores cuanto más
  grande el hueco. **NO VERIFICADO**: son páginas comerciales, no papers, y dos de ellas no se
  pudieron leer (captcha / 403). Se cita como «lo que se dice», no como dato.
- Mesfin (2026, arXiv 2605.04004): en MNQ el «gap fill fade» falla a toda hora de entrada, y la
  única señal cercana a la validez fue **continuación** del hueco en corto, t = 3,23, pero con 22
  operaciones en tres años.

Por eso H2d exige más evidencia que las otras tres, y su test es **a dos colas**: si el resultado es
< 0,5 con significación, lo que se habrá medido es el gap fill, y eso no confirma a H2d.

**Definición completa.** Sobre las columnas diarias que ya existen, dentro del mismo contrato:
`gap_t = open_t − close_{t−1}`. Si `|gap_t| ≥ 0,25` (un tick), operar en `sign(gap_t)` con entrada
en `open_t` y salida en `close_t`, un contrato. Acierto: PnL neto > 0. Una operación por sesión.

**RESOLUCIÓN QUE NECESITA: diaria.**

**FALSADOR.** (i) La proporción de aciertos netos en el período intocado **no difiere de 0,5** al
nivel declarado, a dos colas. (ii) **Precondición, y es el falsador que más pesa:** por el hecho
verificado del §0.1, la apertura diaria de NT8 es la reapertura de las 17:00 CT, así que `gap_t`
mide el hueco del **corte de mantenimiento de 60 minutos**, no el hueco nocturno hasta las 09:30.
La fase 2 de este repo midió lo mismo en el diario de Yahoo (`factory/experiments_ledger.jsonl`,
nota retrospectiva sobre G1-nocturna): 15,7 % de aperturas **idénticas** al cierre previo y el tramo
cierre→apertura carga 3,3 % de la varianza diaria. **Si en el diario MES de NT8 más del 10 % de las
aperturas son idénticas al cierre previo, o el tramo cierre→apertura carga menos del 10 % de la
varianza de cierre a cierre, H2d NO es medible como hipótesis de hueco nocturno con estas columnas**:
lo que quede será una hipótesis sobre el hueco de mantenimiento, y así se rotula. Esa precondición se
mide en el período mirado, y es un HECHO A VERIFICAR, no una hipótesis.

---

## 3 · Lo que NO entra

- Ninguna hipótesis además de estas cuatro. Ninguna variante «ya que estamos».
- Ningún parámetro libre. H1, H3 y H2d no tienen ninguno. H2 tiene uno fijado acá: la ventana de
  ruptura es **la primera hora**, no se prueba con 15 ni con 30 minutos.
- Ningún filtro (volatilidad, día de la semana, tamaño del hueco). Un filtro después de ver datos
  es una hipótesis después de ver datos, y va en la sección 4.

---

## 4 · Hipótesis surgidas después de ver datos

*(vacía al 2026-09-03; lo que se agregue acá lleva fecha y no hereda la protección de arriba)*
