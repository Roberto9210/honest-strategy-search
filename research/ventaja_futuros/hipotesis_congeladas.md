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

---

# ENMIENDA 1 — 2026-09-03

**Se anota al pie. Nada de arriba se reescribe.** Se commitea **sola**, antes de correr la cuenta de
potencia nueva y antes de la comprobación del traslado. **Ninguna cifra de H2d (acierto, PnL, signo de
`close − open`) se ha visto ni se verá con esta enmienda.**

## E1.1 · Decisión de Roberto: Ventana D HEREDA K

`factory/spec_fase2.md` §1.1 y §1.6: K = 261 al día de hoy (`f21fe78`), no se reinicia, y **cualquier fase
futura divide α entre 261 + su presupuesto**. Ventana D declara **K_D = 1: H2d, una configuración, una
población.** Si H1–H3 se admiten algún día, cada una suma 1 en el momento de admitirse. **α de H2d =
0,05 / 262 = 1,908 × 10⁻⁴**, a dos colas como estaba (§2, H2d).

Los seis reportes de febrero de ALAYA quedan **INVERIFICABLES** en `registro_multiplicidad.md` §1 y **no
se suman**.

## E1.2 · Lo que heredar K arrastra, y que el §0 y `diseno.md` no tenían: **la caja fuerte del programa**

`spec_fase2.md` §5 y §7: **«La parte B, 2020-01-01 → 2026-08-19, sigue sellada. Un solo uso para TODO
el programa»**, y **«la misma frontera de partición 2020-01-01, para que la caja fuerte siga siendo un
objeto único»**. Esa caja es el **diario de ES** (`es_daily.csv`, Yahoo). El diario de ES de NT8 desde
2020 es **la misma información** —los mismos días de mercado, la misma resolución— de otro proveedor.
**Leer NT8 2020+ para elegir o ajustar algo es abrir la caja por otra puerta.**

**Consecuencias, y son tres:**

1. **La partición de `diseno.md` §1.3 queda RETIRADA.** Ponía el período mirado de H2d en 2019-05-06 →
   2022-12-31, que está **adentro** de la caja del programa. No se corrió nada sobre ella. Se retira antes
   de que se corra.
2. **La frontera de H2d es 2020-01-01, la del programa.** Todo lo que se mire para controles (C0–C5 de
   `diseno.md` §1.6) se mira **antes** de esa fecha. El intocado de H2d **es** la caja del programa, y su
   única corrida gasta **el único uso del programa**, para H2d, para H1–H3 y para las familias G de la
   fase 2 a la vez. **Abrirla es una decisión de Roberto, no de esta ventana, y no se toma acá.**
3. **Las mediciones de terreno de esta ventana** (`terreno_tenencia`, `terreno_horas`, `terreno_stop`)
   corrieron sobre 2016–2019 y **no tocaron la caja**. La comprobación del traslado de E1.4 usa fechas de
   2020+ **sin evaluar ninguna hipótesis** (compara el signo del hueco entre dos libros, nunca contra el
   día): se declara acá como medición de procedencia, de la misma clase que el control del 2016-11-16.

## E1.3 · Población de H2d: pasa de MES a **ES diario de NT8**, y el motivo

H2d afirma algo del **índice** (el signo del hueco), no del contrato. Ventana A (`f75d126`, control de
período) midió medianas de excursión de ES y MES a 1,06 % una vez alineado el período. Y ES tiene
**2.498 pares consecutivos mismo contrato** contra 1.821 de MES (guardián, tabla M3), y sobre todo
**existe antes de 2020**: MES nace en 2019-05-06 y deja ~165 sesiones fuera de la caja; ES deja **852**.

| tramo | ES diario NT8 | MES diario NT8 |
|---|---|---|
| **MIRADO**: 2016-08-23 → 2019-12-31 | ~852 sesiones (guardián: 866 fechas, 14 de roll) | ~165 |
| **INTOCADO = caja del programa**: 2020-01-02 → 2026-08-21 | ~1.640 | ~1.650 |

**Y hay que decirlo antes de que la tabla lo muestre: cambiar a ES casi no cambia el N del intocado**,
porque el intocado lo fija la frontera del programa y MES ya existe casi entero adentro de ella. Lo que
ES compra es el **mirado**: 852 sesiones para C0–C5 en vez de 165. La potencia se calcula en
`potencia_heredada.py` sobre ambas poblaciones y con α heredado; los N exactos de pares mismo-contrato por
tramo los cuenta el script desde las fechas de los CSV (fechas y contratos, no precios).

**NQ: no es la misma hipótesis y no se agrega.** Un hueco del Nasdaq no es un hueco del S&P; correr H2d
sobre NQ sería una **segunda configuración evaluada contra datos de mercado** (§1.1) y pagaría K_D = 2.
Agrupar ES + NQ en una sola prueba tampoco: son los mismos días de mercado, correlacionados, y sumar sus
sesiones infla N sin agregar información independiente. **Decisión de esta ventana: K_D = 1, sólo ES.**
Si alguna vez se quiere NQ, se paga y se pre-registra aparte.

## E1.4 · El precio del traslado: qué se supone, y cómo se comprueba con lo que hay

**Supuesto de traslado, dicho exacto:** que el **signo** de `open_t − close_{t−1}` en ES coincide con el
de MES en la misma fecha, de modo que una regularidad de signo medida en ES sea la misma regularidad que
se operaría en MES. **No se supone** que coincidan los tamaños (Ventana A: 8 puntos de diferencia de
apertura el mismo día) ni la ejecución.

**Comprobación, sobre las fechas donde los dos existen y los dos están en el mismo contrato de su raíz
(≈ 1.821):** por fecha, `sign(gap_ES)` contra `sign(gap_MES)`. Se imprime: fechas con ambos huecos no
nulos y su acuerdo de signo; fechas con al menos un hueco nulo (`open == close_prev` exacto) y cuántas;
acuerdo restringido a `|gap| ≥ 0,25` en los dos; acuerdo por año. **Nada de `close − open` se calcula ni
se imprime.**

**Criterio, fijado ahora:**

| resultado | criterio sobre las fechas con ambos huecos no nulos |
|---|---|
| **PASA: el traslado deja de ser supuesto** | acuerdo de signo **≥ 95 %** |
| **INDETERMINADO** | entre 90 % y 95 %: se reporta y no se sigue sin decisión |
| **FALLA: H2d no se puede medir en ES para operar en MES** | **< 90 %** |

Y una lectura que se declara antes: si la fracción de fechas con hueco **nulo** es alta (la fase 2 midió
15,7 % en Yahoo; el `close` de NT8 es la liquidación, `discordancia_20161116_resultado.md` §3), eso no
es desacuerdo entre libros: es la precondición C0 de `diseno.md`, y se rotula como tal.

## E1.5 · Qué se corre ahora y qué no

Se corre: `potencia_heredada.py` (aritmética + conteo de fechas) y `traslado_signo.py` (E1.4). **No se
corre H2d. La caja sigue cerrada.** El veredicto —si H2d queda en pie, con qué población y con qué
umbral de efecto— va en la Enmienda 2, después de ver esas dos salidas y ninguna otra.

---

# ENMIENDA 2 — 2026-09-03 — el veredicto, después de `potencia_heredada.txt` y `traslado_signo.txt` y de nada más

**Se anota al pie. Nada de arriba se reescribe.** Ninguna cifra de H2d se ha visto: las dos salidas
cuentan fechas, contratos y signos de hueco entre libros; ninguna calcula `close − open`.

## E2.1 · El traslado deja de ser supuesto: **PASA, 96,61 %**

Sobre 1.845 fechas comunes (2019-05-07 → 2026-08-21, ambos en el mismo contrato de su raíz), 1.741 con
ambos huecos no nulos: **el signo coincide en 1.682, el 96,61 %.** Criterio E1.4: ≥ 95 % PASA.

| condición | fechas | acuerdo |
|---|---|---|
| ambos huecos no nulos | 1.741 | 96,61 % |
| alguno con \|gap\| ≥ 1 punto | 1.599 | 98,44 % |
| alguno con \|gap\| ≥ 2 puntos | 1.296 | 99,38 % |
| 2019 solo (los primeros meses de MES) | 148 | 89,19 % |
| 2020 → 2026, cada año | 155–247 | 95,1 % a 99,2 % |

Los 59 desacuerdos tienen mediana de \|gap\| de **0,50 en las dos raíces**: dos ticks. **Los libros
discrepan cuando el hueco es ruido de un par de ticks; cuando el hueco es de un punto o más, coinciden
98 de cada 100 veces.** La regla congelada opera desde un tick y **no se cambia por esto**: cambiar el
umbral después de ver esta tabla sería ajustar la regla con datos, aunque los datos no sean de H2d. Queda
dicho como costo conocido de la regla: en ~4 % de las fechas el signo de ES no es el de MES, y son las
fechas de hueco mínimo.

**Precondición C0, rotulada y no dictaminada:** 5,6 % de fechas con algún hueco nulo (ES 2,9 %, MES
3,1 %), **por debajo del 10 % que §2 fijó**. El `close` de NT8 es la liquidación de las 15:15 CT, así que
el hueco de las columnas es el de 15:15 → 17:00 y no el nocturno (`discordancia_20161116_resultado.md`
§3); pero no está degenerado como en Yahoo (15,7 %). La parte de varianza de C0 se mide en el mirado
cuando se mida.

**Orientación:** NQ contra MNQ da 94,86 %; **ES contra NQ da 85,98 %**: dos índices distintos no ven el
mismo hueco en 14 de cada 100 días. **Confirma E1.3: NQ no es la misma hipótesis.**

## E2.2 · La potencia con α heredado: **la población no resolvió sola el problema; la frontera manda**

Pares consecutivos mismo contrato, contados desde fechas y contratos (`potencia_heredada.txt`):

| población | mirado < 2020 | intocado ≥ 2020 (caja del programa) |
|---|---|---|
| ES | **851** | **1.687** |
| MES | 167 | 1.683 |

**El intocado de ES y el de MES tienen el mismo N (1.687 contra 1.683)**, porque MES nace en 2019-05 y
casi entero cae adentro de la caja. Lo que ES compra es el mirado: 851 contra 167. Eso es lo que E1.3
dijo antes de la tabla, y la tabla lo confirma.

Con α = 0,05/262 a dos colas (z = 3,73), potencia binomial exacta sobre el intocado de ES (n = 1.687):

| acierto real | 52 % | 55 % | 56 % | 57 % | 58 % | 60 % |
|---|---|---|---|---|---|---|
| potencia | 0,017 | **0,641** | **0,882** | 0,978 | 0,998 | 1,000 |

**Acierto mínimo detectable al 80 %: 55,6 %.** Con α = 0,05 era 53,4 %. **55 % ya no es alcanzable
(0,64); 56 % sí (0,88).** La pregunta concreta tiene respuesta concreta: **no, 55 % no volvió a ser
alcanzable; la decisión de población no resolvió el problema de potencia, y no podía, porque el N del
intocado lo fija la frontera 2020-01-01 y no el instrumento.** Sumar NQ a ES daría 0,98 al 55 % pero es
N inflado con los mismos días: no se usa, y está impreso para que se vea lo que inflaría. K_D = 1, 2 o 4
cambian la tercera cifra decimal; el denominador 261 es el que pesa.

## E2.3 · Veredicto: **H2d QUEDA EN PIE**, con esta población y este umbral

| | |
|---|---|
| **hipótesis** | H2d tal como está en §2, sin cambios de regla: un tick de umbral, entrada `open_t`, salida `close_t`, un contrato, dos colas |
| **población** | **ES diario de NT8** (CSV de `37a0144`), contrato de máximo volumen por fecha, pares consecutivos mismo contrato. **El traslado a MES está medido: 96,6 % de acuerdo de signo, 98,4 % con hueco de un punto o más** |
| **mirado** | 2016-08-23 → 2019-12-31, **851** pares. Sólo para C0 (varianza), C1–C5 de `diseno.md` §1.6, con C3 «otro libro» reescrito: ahora el otro libro es **MES** en sus 167 pares de 2019, y su criterio pasa a ser el de E1.4, que ya pasó |
| **intocado** | **la caja del programa, 2020-01-02 → 2026-08-21, 1.687 pares.** Una corrida, que gasta el único uso del programa. **Abrirla es decisión de Roberto** |
| **α** | 0,05 / 262 = 1,908 × 10⁻⁴, dos colas, K_D = 1 |
| **umbral de efecto** | **detectable al 80 % desde 55,6 % de acierto neto**; a 55 % la potencia es 0,64 y se declara así: si el efecto real es 55 %, hay 36 % de probabilidad de no verlo aunque exista |
| **costo** | 3,90 USD por ida y vuelta, adentro de cada fila, como en `diseno.md` §1.4 |
| **si falla** | como `diseno.md` §1.5: muere, se anota, no hay variante ni segunda corrida, y la caja queda gastada para todo el programa |

**Lo que cambió respecto del diseño original y por qué, en una línea cada uno:** población MES → ES
(existe antes de la frontera; traslado medido); partición 50/50 propia → frontera del programa (heredar
K hereda la caja); α 0,05 → 0,05/262 (§1.6); umbral 55 % → 55,6 % (consecuencia de las dos anteriores).
**Lo que no cambió: la regla de H2d, su falsador, su costo, y que no se corre nada hasta que Roberto
decida abrir la caja.**

---

# ENMIENDA 3 — 2026-09-03 — rige el protocolo de la spec: K se cobra en A, la caja se examina a 0,05

**Se anota al pie. Nada de arriba se reescribe. Al momento de escribir esto no se ha visto ningún
resultado de H2d:** ningún script de este repo ha calculado `close − open` sobre ninguna fecha de ES ni
de MES diario; lo único visto son fechas, contratos, signos de hueco entre libros (E2.1) y la dispersión
de la excursión adversa de los minutos de Databento (`potencia_terreno_condicional.txt`). El orden del
log es la garantía: esta enmienda se commitea sola, antes de `h2d_compuerta1.py`.

## E3.1 · Qué decía la Enmienda 2

Que H2d se probaba **una sola vez, en el intocado** (la caja del programa, 1.687 pares), con
**α = 0,05/262 a dos colas**, y que el mirado (851 pares) servía **sólo para los controles C0–C5**: ninguna
cifra de acierto del mirado se publicaba. El umbral de efecto salía de ahí: 55,6 % en B.

## E3.2 · En qué contradecía la spec

`factory/spec_fase2.md` (`e17cde9`), leído textual en `caja_alcance_y_uso.md` §2:

- §3.3 línea 359: "Significancia | p ≤ 0.05 bilateral (**prueba única pre-registrada; la multiplicidad ya
  se pagó en A**)".
- §3.1 línea 262–270: la compuerta 1 se pasa **en la parte A**, con n_A ≥ 100, |t_A| ≥ 3,726 (p ≤ 0,05/257),
  factor de ganancia neto ≥ 1,3, vecindad sin celda perdedora, |t_A| ≥ 3,726 sin el mejor 1 % de las
  operaciones, y operaciones no solapadas.
- §1.2 línea 82–86: el estadístico es `t = media(neto) / (desvío(neto, ddof=1) / √n)`, `p = erfc(|t|/√2)`,
  y "**No se sustituye por otro estadístico después de ver los resultados**".
- §3.3 línea 351: "La abre **la primera candidata que pase las compuertas 1 y 2**".
- Ledger, CAMBIO_DE_REGLAS del 2026-08-25: "la prueba sobre B NO arrastra la penalidad de la busqueda; esa
  vive en la compuerta 1 [...] y no se cobra dos veces".

La Enmienda 2 cobraba K en B y no exigía nada en A. La spec cobra K en A y examina B a 0,05. Son dos
protocolos distintos, y el de la enmienda **borraba una compuerta**: la que obliga a la candidata a ganarse
el derecho a la caja sobre datos ya vistos antes de gastar el único uso del programa.

## E3.3 · Cuál rige y por qué

**Decisión de Roberto, 2026-09-03: rige el protocolo de la spec.** El motivo no es sólo que esté escrito:
es que el tamiz en A es exactamente lo que impide gastar el único tiro en un candidato flojo, que fue el
motivo por el que no se abrió la caja. De la Enmienda 2 quedan en pie la población (ES diario de NT8, con
traslado medido), el mirado 2016-08-23 → 2019-12-31 y el intocado = la caja del programa; **cae el α sobre
B y cae la prohibición de publicar el acierto del mirado**, porque el mirado ahora es la parte A de la
compuerta 1.

## E3.4 · Lo que se corre ahora: la compuerta 1 de H2d sobre el mirado, y sólo eso

Población: ES diario de NT8 (CSV del guardián `37a0144`+), contrato de máximo volumen por fecha, pares
consecutivos mismo contrato, **2016-08-23 → 2019-12-31, 851 pares esperados**. La regla es la de §2 y de
`diseno.md` §1.1, sin cambios: `gap_t = open_t − close_{t−1}`; si `|gap_t| ≥ 0,25`, `sign(gap_t)`, entrada
`open_t`, salida `close_t`, un contrato; `neto = sign(gap_t) × (close_t − open_t) × 5 − 3,90` en USD de MES,
sobre puntos de ES (traslado E2.1). K_D = 1: esta corrida **es** la evaluación de H2d contra datos de
mercado (§1.1) y cuesta lo que ya está contado.

Orden de la salida y criterios, fijados antes de correr:

1. **C0 primero, y si dispara se para ahí.** Identidad `open_t == close_{t−1}` > 10 % de los pares, **o**
   varianza de `gap` < 10 % de la varianza de `close_t − close_{t−1}`: H2d **muere** como hipótesis de hueco
   nocturno con estas columnas (decisión de Roberto: no se sigue con una hipótesis rotulada "hueco de
   mantenimiento"). El script imprime C0 y termina sin calcular nada más.
2. **C1–C5 arriba del resultado**, como en `diseno.md` §1.6: C1 placebo de signo (1.000 permutaciones,
   semilla 20260903, banda 2,5–97,5 % del acierto y del t); C2 rival de momentum `sign(close_{t−1} −
   close_{t−2})`; C3 otro libro = **MES** en sus pares de 2019 (E2.3), coincidencia de signo de (acierto −
   0,5) y de la media neta; C4 escala 2 contratos = exactamente 2× bruto y 2× fricción; C5 uniones
   descartadas por cambio de contrato, conteo y meses.
3. **El resultado**, con: n, aciertos, acierto, binomial exacta a dos colas (el estadístico del falsador
   congelado, se imprime y se exige), **media neta, desvío, t_A y p_crudo (§1.2, el estadístico que decide)**,
   factor de ganancia neto, t_A sin el mejor 1 % de las operaciones, y la línea de la suerte 1/(K+1).
4. **Compuerta 1 pasa sólo si todo esto pasa:** n_A ≥ 100; **|t_A| ≥ 3,731** (= p ≤ 0,05/262 con K = 261
   heredado y K_D = 1; la spec escribe 3,726 para 257, y se usa la más dura); binomial a dos colas
   p ≤ 0,05/262 con acierto > 0,5 (< 0,5 con significación es gap fill, no confirma: §2); PF neto ≥ 1,3;
   t_A ≥ 3,731 sin el mejor 1 %; **vecindad**: el único parámetro es el umbral de un tick, que no tiene
   celda por debajo (los huecos son múltiplos de 0,25, así que 0 ticks es la misma regla); se imprime la
   celda **2 ticks (0,50)** como robustez, **sin adoptarla** (§9.5: adoptar cobra), y no puede perder plata.
5. **Compuerta 2**, con n_A real y n_B proyectado del **calendario** de la caja (1.687 pares × la tasa de
   operación medida en A; ningún precio de B): `|t_A| ≥ 2,8016 × √(n_A / n_B)`. Se imprime la vara y si
   pasa.
6. **Si no pasa la compuerta 1: H2d muere sin haber gastado nada**, se anota DESCARTADA al pie de este
   archivo, sin variante, sin filtro de tamaño, sin segunda corrida. **Si pasa: NO se abre la caja.** Se
   reporta y lo decide Roberto. La compuerta 3 sería sobre la caja a 0,05 bilateral, con PF ≥ 1,3 y ≥ 5 de
   7 años positivos (§3.3), y gastaría el único uso del programa.

Salida cruda a `h2d_compuerta1.txt`, commiteada antes de una palabra de interpretación. `diseno.md` no se
reescribe: su nota fechada remite acá.

---

# H2d · DESCARTADA — 2026-09-03 — C0 disparó; ninguna cifra de dirección se calculó

Salida cruda: `h2d_compuerta1.txt`. Población como se esperaba: 866 fechas, **851 pares** mismo contrato,
2016-08-23 → 2019-12-31. La caja no se leyó: el cargador descarta toda fila ≥ 2020-01-01 antes de calcular.

| C0, criterio congelado en §2 y `diseno.md` §1.6 | medido | dispara |
|---|---|---|
| identidad `open_t == close_{t−1}` > 10 % | 70 de 851 = **8,23 %** | no |
| varianza del hueco < 10 % de la varianza cierre→cierre | 18,56 de 462,27 = **4,01 %** | **sí** |

Mediana de |hueco| 1,00 pts contra 9,25 pts de cierre a cierre. Es lo que el hecho del §0.1 anticipaba:
la apertura diaria de NT8 es la reapertura de las 17:00 CT y el cierre es la liquidación de ~15:14 CT, así
que las columnas miden el corte de mantenimiento de 60 minutos, que carga el 4 % de la varianza del día.
La fase 2 había medido 3,3 % en el diario de Yahoo. **H2d no es medible como hipótesis de hueco nocturno
con estas columnas.**

**Decisión de Roberto, tomada antes de correr (E3.4 punto 1): muere ahí, sin rótulo de «hueco de
mantenimiento», sin variante.** Por el punto 1 el script terminó en C0: **C1 a C5 y el resultado no se
calcularon y no existen en ningún archivo.** Nadie sabe hacia dónde apuntaba el 4 %, y así queda.

Lo que esto deja escrito para lo que siga:

- **K_D = 1 queda gastado.** El cartucho se gasta al pre-registrar (spec §9.5), no al correr; que la regla
  no haya producido una operación no lo devuelve. K = 262 para la próxima configuración de este programa.
- **La caja no se gastó.** Sigue sellada; este archivo no leyó ninguna fila posterior a 2019-12-31.
- **Cualquier hipótesis de hueco nocturno sobre el diario de NT8 está muerta por la misma medición**, sea
  de MES, ES o NQ: el diario no tiene una apertura nocturna. Medir el hueco liquidación → 08:30 CT exige
  minutos, es decir la población de Databento (§0.3), y sería una configuración nueva que pagaría K. **No
  se agrega ninguna acá** (§3).
- H1, H2 y H3 siguen como estaban: congeladas, condicionales a que Roberto admita los minutos de ES.
