# Spec — BOT C multi-mercado: F4 congelada sobre índices distintos de ES

**Fecha:** 26 de agosto de 2026 · **Estado:** día cero de la fase. **Esta spec no abre la fase: fija
las reglas con las que se decide si se abre.** Escrita ANTES de medir la matriz de correlación, que es
lo único que se mide hoy.

**Origen:** §6 de `botc_potencia_f4.md` (21-ago) — *"no más configuraciones sobre el mismo mercado,
sino el mismo efecto sobre más mercados"*. **No se reabre ninguna búsqueda.**

**Alcance (corrección de Roberto, 26-ago):** sólo **mercado de FUTUROS**. SPY sale: en la Fase 1 fue
confirmación, no mercado a operar. Todos los candidatos ya eran futuros, así que el diseño no cambia;
lo que cambia es que aparece una amenaza de primer orden que un ETF no tiene — **el roll** (§A).

**Orden de los hechos, para que sea auditable y no una promesa.** Antes de este commit se ejecutaron
`factory/mm_descarga_qc.py` (bajada y control de calidad) y `factory/mm_muestra.py` (calendario, bandas
de roll, conteos). **Ninguno de los dos calcula un retorno de estrategia, una media, una suma ni un
P&L**: producen propiedades del PROVEEDOR y del CALENDARIO. La matriz de correlación — lo único que
lleva la respuesta adentro — se corre **después** de commitear esta spec y la predicción.

---

## a) La hipótesis única y sus parámetros congelados

> **F4 — vuelta de mes. `kind = turn_of_month`, `n_before = 4`, `m_after = 3`, largo, un contrato.**
> Entrada en la **apertura** de la cuarta sesión desde el final del mes M; salida en la **apertura** de
> la tercera sesión del mes M+1. Sin filtros, sin stops, sin sizing, sin variantes.

**Procedencia exacta.** Ledger `factory/experiments_ledger.jsonl`, entrada
`hash = 049b809f5e9def5c`, `prev = c07cf6110f7f5c57`, `family = "F4-calendario"`,
`config = {"kind":"turn_of_month","n_before":4,"m_after":3}`, `part = "A"`:
PF 1.507 · 231 operaciones · neto $5.845,35 · DD −$948,05.
*(Los documentos previos la llaman "línea 16"; es la **17.ª línea física** del archivo. El hash es el
identificador que no admite discusión — se cita el hash.)*

**Código congelado:** `factory/familias_4_5.py::turn_of_month`, sin tocar. Cualquier reimplementación
queda prohibida: la selección de índices de sesión ES la hipótesis.

**Prohibido, y no por gusto** (§0 de `multimercado_dia0.md`, que se hereda entero): re-optimizar
`n_before`/`m_after` por mercado, agregar cualquier filtro, cambiar el lado, cambiar el horario. Un solo
mercado con un parámetro retocado contamina el conjunto entero, porque el conjunto se reporta como **una
sola prueba**.

---

## A) LA REGLA DE ROLL — escrita y congelada antes de tocar datos

Un futuro no tiene serie continua: hay que empalmar contratos y la costura inyecta un escalón
artificial. **F4 es una estrategia de calendario.** Un artefacto de roll dentro de la ventana de vuelta
de mes fabrica o destruye el efecto y **se ve exactamente igual que un resultado real en todos los
reportes** — la misma forma que el aviso sobre el Simulated Data Feed de §6.

### A.1 De dónde sale la serie, y por qué eso obliga a esta regla

Las cuatro series son **Yahoo Finance `=F`**, que es **front-month continuo SIN ajustar por roll**.
No es una interpretación: está escrito en el control de calidad del propio proyecto
(`qc/data_quality_yahoo.md` §2): *"en los cambios de contrato (mar/jun/sep/dic) puede haber escalones de
precio que no son movimiento de mercado"*. **No construimos ninguna serie continua propia** — no hay
contratos individuales disponibles en esta fuente — así que la regla no puede ser "ajustar hacia atrás
por diferencia o por ratio": **no tenemos con qué**. La única regla honesta con esta fuente es
**excluir**.

### A.2 La regla, idéntica en forma para los cuatro mercados

> **BANDA DE ROLL** = las **8 sesiones que terminan en el último día de negociación** del contrato
> trimestral (marzo, junio, septiembre, diciembre), **inclusive**.
> **EXCLUSIÓN**: se elimina de la muestra **toda vuelta de mes cuya ventana `[sesión de entrada .. sesión
> de salida]` toque aunque sea una sesión de la banda**, y se cuenta cuántas fueron.

Por qué 8: el período de roll estándar de CME en índices de acciones **empieza una semana antes del
vencimiento**; 8 sesiones lo cubren con una sesión de margen. La regla es **idéntica en forma** para los
cuatro mercados y se aplica al vencimiento **propio de cada uno**:

| mercado | convención de vencimiento usada | verificado |
|---|---|---|
| ES, NQ, YM | tercer viernes del mes de contrato | convención estándar CME de índices de acciones |
| **NKD** | **jueves anterior al segundo viernes** (liquidación = SOQ del segundo viernes) | **sí** — ficha de producto CME: liquidación en efectivo contra la SOQ del Nikkei, *"usually based on the opening of the second Friday of the contract month"* |

*Deliberadamente conservadora y deliberadamente ciega al resultado:* no se estima el día exacto en que el
proveedor cambió de contrato (ver A.4, donde se muestra que para NKD **no se puede** estimar), se excluye
una banda que lo contiene bajo cualquier convención plausible.

### A.3 Las fechas contadas, en toda la muestra (`factory/mm_muestra.py`)

**La expectativa era cero. No es cero, y para un mercado es catastrófica.**

| mercado | vueltas de mes totales | **tocadas por la banda de roll** | en muestra | de las tocadas, en el bloque A (≤ 2019-11) |
|---|---|---|---|---|
| ES *(referencia)* | 311 | **2** (2017-08, 2023-08) | 309 | **1** |
| NQ | 311 | **2** (2017-08, 2023-08) | 309 | 1 |
| YM | 292 | **3** (2006-08, 2017-08, 2023-08) | 289 | 2 |
| **NKD** | 270 | **90 — el 100 % de las trimestrales** | **180** | 64 |

*(Corrección del 26-ago, misma tanda, antes de medir la matriz: la primera versión de esta tabla decía
0/0/1/63 en la última columna — 2017-08 está DENTRO de 2000-2019 y la tabla se copió mal de la consola.
La atrapó el control [1] de `tests/multimercado/test_matriz.py` antes de que se corriera nada.)*

Los dos casos de ES/NQ son agosto→septiembre: cuando el tercer viernes de septiembre cae el día 15, la
banda llega hacia atrás hasta la tercera sesión del mes, que es justo la sesión de salida. **Por una
sesión.**

**NKD pierde el 33 % de su muestra y la pérdida es estructural**, no un accidente de calendario: su
vencimiento está atado al **segundo** viernes, no al tercero, así que la banda de roll vive sobre las
primeras sesiones del mes — exactamente donde F4 sale. **Los cuatro trimestres, todos los años.**

**Consecuencia sobre el número publicado de ES, dicha sin maquillar:** una de las dos exclusiones de ES
(2017-08) cae **dentro** del calendario de descubrimiento. La muestra congelada de ES en el bloque A
tiene **230** vueltas, una menos que las 231 del ledger. **El número del ledger no se toca** — es el
registro del descubrimiento, medido sin regla de roll, y así queda. Lo que esta fase mide (la fila de
referencia de ES en la matriz) usa la muestra congelada de 230. La regla de roll le costó exactamente
un trade al mercado de descubrimiento, y se paga: retocar la banda para salvarlo sería elegir la regla
por el resultado.

### A.4 El control empírico, y por qué NO decide

Diagnóstico independiente: la **base** `log(futuro / contado)` contra el índice de contado (^GSPC, ^NDX,
^DJI, ^N225). El contado no rulea, así que un escalón en la base delata el empalme.

| mercado | contado | ruido de la base sd(Δ) | posición en el mes del mayor escalón trimestral (mediana / p10 / p90) |
|---|---|---|---|
| ES | ^GSPC | 0,280 % | **13** / 10 / 15 |
| NQ | ^NDX | 0,389 % | **13** / 10 / 15 |
| YM | ^DJI | 0,262 % | **13** / 10 / 15 |
| **NKD** | ^N225 | **1,495 %** | 8 / 1 / 18 |

Para ES, NQ e YM el empalme real vive a mitad de mes (sesión 13 mediana) — **confirma por un camino
independiente que la ventana de vuelta de mes está limpia**, y que la banda de 8 sesiones es margen de
seguridad, no una necesidad.

**Para NKD el diagnóstico es inservible y se dice así:** el ruido de la base es **1,495 %**, cinco veces
el de los otros tres, porque ^N225 es el cierre de Tokio y NKD=F es la sesión de CME — lo que mide es el
desfase horario, no el roll. Un escalón de roll de 0,1–0,3 % no es detectable dentro de ese ruido.
**Por eso decide la regla de calendario (A.2) y no el detector.** Un umbral sobre esa serie habría sido
un grado de libertad elegido después de ver los datos.

---

## b) La lista de mercados — cerrada, uno por uno, por mecanismo

**El mecanismo que se prueba:** la vuelta de mes es **flujo de rebalanceo de índices de acciones**
— aportes que llegan a fin de mes, rebalanceo mecánico de fondos indexados y de fecha objetivo. El flujo
se denomina por **familia de índice** y por **base de inversores**, no por país ni por bolsa. Entra un
mercado si se puede **nombrar** ese flujo.

### b.1 Los que entran

| | mercado | el flujo de fin de mes, nombrado | por qué es real |
|---|---|---|---|
| 1 | **NQ** — E-mini Nasdaq-100 | rebalanceo y aportes del complejo indexado al Nasdaq-100 (QQQ y su familia de derivados) | familia de índice propia, con su propia base de inversores y su propio ciclo de aportes. Solapa constituyentes con el S&P 500, pero **el dinero que sigue al Nasdaq-100 es otro pozo** |
| 2 | **YM** — E-mini Dow | rebalanceo y aportes del complejo indexado al Dow Jones Industrial Average (DIA y su familia) | flujo real y nombrable. **Se declara ahora, antes de medir: su pozo es un orden de magnitud más chico que el del S&P/Nasdaq y sus 30 constituyentes viven dentro del universo de gran capitalización de EE.UU.** Es el candidato más débil por mecanismo, y se espera que sea el que más correlacione con NQ |
| 3 | **NKD** — Nikkei 225 (USD), CME | rebalanceo y aportes del complejo indexado al Nikkei 225: fondos japoneses, ciclo de aportes de pensión japonés | **el único pozo genuinamente independiente que sobrevive**: otra familia de índice, otra moneda subyacente, otra base de inversores, otro calendario fiscal |

### b.2 Los que se descartan, y por qué

| mercado | descartado por | detalle |
|---|---|---|
| **ES** | **es el mercado de descubrimiento** | F4 se seleccionó sobre ES y sólo sobre ES. Entra únicamente como **fila de referencia** en la matriz (§D1), nunca al conteo de operaciones |
| **SPX/SPY** | fuera de alcance | no es futuro (corrección de alcance del 26-ago) |
| **FESX** — Euro Stoxx 50 | **NO EXISTE LA SERIE** | ver b.3. Es la baja más cara del paquete: era el segundo pozo independiente |
| **RTY** — Russell 2000 | **dos motivos independientes** | (i) mecanismo/estructura: el Russell se mudó CME→ICE (2008)→CME (2017); no hay historia continua defendible. (ii) **dato duro**: la serie de Yahoo empieza el **2017-07-10**, 2.299 filas, **109 vueltas de mes en total y 29 en 2000-2019**. Confirmado, no asumido |
| **DAX, ASX/SPI, HSI, KOSPI** *(el quinto mercado que Roberto invitó a proponer)* | **ninguno tiene serie de futuros** | probados uno por uno contra el proveedor: `FDAX=F`, `SPI=F`, `HSI=F`, `KOSPI=F` vacíos; `DAX=F` devuelve 48 filas basura (2014→2026). El mecanismo de varios de ellos es defendible; **la serie no existe, y ése es el filtro que los mata**. No hay quinto mercado |
| **índices de bonos** *(el ejemplo legítimo que Roberto marcó: la extensión de duración a fin de mes)* | fuera de esta fase | El flujo es real y está documentado — los índices agregados de bonos extienden duración el último día hábil del mes y los fondos que los siguen tienen que comprar duración. **Pero es OTRO mecanismo, con otro signo, otro instrumento (ZN/ZB) y otra ventana.** Meterlo acá sería probar dos hipótesis y llamarlas una. Queda anotado como candidato a fase propia, no como cuarto mercado de ésta |

### b.3 FESX: la baja que decide el tamaño de la fase

Roberto lo puso en la lista y su mecanismo es impecable (Europa: otra familia de índice, otra base de
inversores, otro pozo). **No entra porque no hay serie.** Verificado, no asumido:

- **Yahoo:** `FESX=F`, `STXE=F`, `SX5E=F` — **los tres vacíos**. El contado `^STOXX50E` existe pero
  **empieza el 2007-03-30**, y además es contado, no futuro (fuera de alcance).
- **Databento:** el dataset que este proyecto ya usa es **GLBX.MDP3 (CME), disponible desde 2010-06-06**
  (`databento_estimate.py`, `qc/data_quality_es_1min_databento.md`). Eurex es otro dataset, pago, y
  empieza aún más tarde. **No hay 2000-2010 de FESX a ningún precio que este proyecto vaya a pagar**, y
  un paquete de día cero no compra datos (precedente `multimercado_dia0.md`).
- **Stooq:** probado; el servidor devuelve HTML de verificación para **todos** los símbolos, incluidos
  los que con certeza existen (`^spx`). **No se puede distinguir "no hay dato" de "me bloqueó": se
  declara como NO EVALUADO**, no como ausente.

### b.4 Calidad de datos de los tres admitidos (`factory/mm_descarga_qc.py`)

Fuente: **Yahoo Finance vía yfinance 1.6.0**, `Ticker.history(period="max", interval="1d",
auto_adjust=False, prepost=False)` — la misma fuente y el mismo código que bajaron `ES=F`
(`download_data.py`). Los CSV van a `data/`, gitignored: no se redistribuyen.

| mercado | ticker | filas | desde | hasta | cobertura vs días hábiles | **huecos > 3 hábiles** | NaN OHLC | precio ≤ 0 |
|---|---|---|---|---|---|---|---|---|
| NQ | `NQ=F` | 6.549 | **2000-09-18** | 2026-08-26 | 0,968 | **0** | 0 | 0 |
| YM | `YM=F` | 6.140 | **2002-04-05** | 2026-08-26 | 0,965 | **0** | 0 | 0 |
| NKD | `NKD=F` | 5.669 | **2004-02-17** | 2026-08-26 | 0,965 | **0** | 0 | 0 |
| *ES (ref.)* | `ES=F` | 6.544 | 2000-09-18 | 2026-08-19 | 0,968 | 0 | 0 | 0 |

**Cero huecos mayores a 3 días hábiles en las tres series.** La cobertura de 0,965–0,968 contra el
calendario lun-vie es el complemento exacto de los feriados de EE.UU.: no falta nada.

*(El CSV de ES es el que ya estaba en `data/` desde el 19-ago y llega al 2026-08-19; los otros tres se
bajaron hoy y llegan al 2026-08-26. ES es sólo referencia, así que la diferencia de una semana no toca
ningún número de la fase. Se declara igual.)*

### b.5 **Correcciones a las fechas que dio Roberto** — verificadas contra el proveedor

Roberto pidió explícitamente que se le corrigiera. Sus fechas son de **lanzamiento del contrato**; lo que
manda para esta fase es la **cobertura real de la serie**, y no son lo mismo:

| | Roberto dijo | **la serie dice** | efecto |
|---|---|---|---|
| ES | 1997 | 2000-09-18 | excluido igual (mercado de descubrimiento) |
| NQ | 1999 | **2000-09-18** | entra; ~1,5 años menos que el contrato |
| **NKD** | **1990** | **2004-02-17** | **el contrato es de 1990; la serie del proveedor empieza en 2004.** NKD aporta 270 vueltas, no ~430 |
| YM | 2002 | **2002-04-05** | correcto |
| RTY | (excluido) | 2017-07-10 | **excluido, y con un segundo motivo independiente** |
| **FESX** | 1998, entra | **no hay serie** | **sale de la lista. De cuatro mercados quedan tres** |

> **La lista queda cerrada en TRES: NQ, YM, NKD.** Una vez escrita no se toca. Ningún mercado se
> agrega después de conocer un número.

### b.6 El precedente que hace admisible a NKD con 22 años y no 26

NKD empieza en 2004, no en 2000. **La cantidad de historia no es un filtro de admisión en este
proyecto: es un insumo del cálculo de potencia.** El precedente es directo y anterior a hoy:
`multimercado_dia0.md` §1 admitió **BTC con 2.185 sesiones (2017-2026) y 130 operaciones**, por
mecanismo, y lo contó honestamente en la aritmética. Se aplica el mismo estándar. Lo que descalifica a un
mercado es **serie inexistente** (FESX, DAX, HSI, ASX, KOSPI), **historia sucia o empalmada por
nosotros** (RTY), o **mecanismo no nombrable** — nunca "tiene menos años que otro".

### b.7 Un cambio de regla que se declara, y AFLOJA

`multimercado_dia0.md` §2 exigía **un mercado por pozo de flujo INDEPENDIENTE**, y con ese criterio
rechazó a HG por compartir disparador con GC. Aplicado literalmente acá, **NQ e YM son el mismo pozo de
gran capitalización de EE.UU. y uno de los dos debería salir.**

**No se aplica, y se dice por qué:** §2 existía porque allí ρ **se iba a suponer**. Acá ρ **se mide** —
es el entregable del día. Un filtro a priori contra la dependencia es redundante frente a la medición
directa de esa misma dependencia, y sustituirlo por la medición es estrictamente más informativo.

**Esto AFLOJA una regla y entra al ledger como tal, con su argumento.** Lo que lo compensa es que la
dependencia NQ-YM no queda escondida: es exactamente el número que la matriz publica, y §D1 obliga a
reportarla suelta, sin promediar.

### b.8 Operabilidad — se declara, NO selecciona (corrección C de Roberto)

El encargo de BOT C (§0 de `botc_potencia_f4.md`) es **ganancia real en cuenta propia, sin reglas de
prop firm**. Que un prop firm ofrezca o no un mercado es irrelevante para el test. Se anota para que el
resultado sea interpretable; **elegir la lista por esto sería volver a seleccionar por conveniencia.**

| mercado | instrumento chico | multiplicador | tick | nocional aprox. | operable en cuenta propia |
|---|---|---|---|---|---|
| NQ | **MNQ** (Micro E-mini Nasdaq-100) | $2 × índice | 0,25 pts = $0,50 | ~$50.000 | sí — cualquier broker de futuros de EE.UU. |
| YM | **MYM** (Micro E-mini Dow) | $0,50 × índice | 1 pt = $0,50 | ~$22.500 | sí — el más barato de los tres |
| **NKD** | **no consta un micro** | **$5 × índice** | **5 pts = $25** | **~$225.000** | sí por acceso (CME, broker de EE.UU.), **pero el tamaño mínimo es 4-10 veces el de los otros dos**. Es una restricción de **capital**, no de acceso |

*Especificaciones de MNQ y MYM: **no verificadas contra la página de CME**, que no carga desde acá
(mismo problema declarado en `multimercado_dia0.md` §7). Las de NKD sí: $5 × índice, tick 5 puntos = $25.
Las tres entran a `qc/` antes de pre-registrar. Ninguna de ellas selecciona nada, y §c.3 las neutraliza
por si estuvieran mal.*

---

## c) Efecto mínimo detectable y potencia objetivo, con la fórmula

### c.1 La maquinaria, que es la del proyecto y no una nueva

`factory/harness_f2.py` §3.2, sin cambios:

```
z_(alfa/2) = 1,959964   (0,05 bilateral, prueba única: K = 1)
z_(1-beta) = 0,841621   (80 % de potencia)
POWER_CONST = 2,801585
potencia   = 0,5 * erfc( -(ncp - 1,959964) / raiz(2) )
n exigido para 80 %  =  (2,801585 / delta)^2
```

**Efecto pre-registrado (δ).** De ES parte A, neto de fricción MES: media **$25,30** por operación,
desviación **$166,95** ⇒ `δ = 25,30/166,95 = 0,151542`. De ahí salen los dos números del veredicto,
reproducidos exactos: `t = 0,151542·√231 = 2,3032` (publicado 2,304) y potencia sobre 80 operaciones =
**27,27 %** (publicado 27,3 %).

> **n exigido para 80 % de potencia = (2,801585 / 0,151542)² = 341,77 ⇒ 342 operaciones.**

**Su procedencia, dicha entera:** `δ = 0,151542` es **el máximo de 57 configuraciones probadas sobre
ES** (§3 de `botc_potencia_f4.md`). Es un **máximo seleccionado**: la maldición del ganador dice que el
efecto verdadero es casi con seguridad **menor**. Powerear contra él hace la potencia **optimista**.
Se usa igual, con el mismo criterio con que `multimercado_dia0.md` §10 usó su propio máximo sesgado —
declarándolo — y §c.4 mide cuánto duele.

### c.2 Cómo se combinan tres mercados: el efecto de diseño

Se corrige, como en `multimercado_dia0.md` §9, la fórmula del encargo: el conglomerado son los **m
mercados observados a la vez**, no todas las operaciones juntas, así que es `(m−1)` y no `(N−1)`.

Y se **generaliza a la matriz completa**, porque Roberto pide operaciones efectivas reales y no un
escalar. Con `T_i` = conjunto de vueltas de mes del mercado i, `R` la matriz de correlación de los
retornos de vuelta de mes **estandarizados**, y `N = Σ|T_i|`:

```
n_efectivo  =  N²  /  Σ_(i,j) [ R_ij · |T_i ∩ T_j| ]
```

Se comprueba que se reduce **exactamente** al escalar del proyecto: con m mercados de k operaciones cada
uno y `R_ij = ρ` fuera de la diagonal, el denominador vale `m·k·m·(1+(m−1)ρ)/m` y queda
`n_ef = N/(1+(m−1)ρ)`. **Es la misma fórmula, sin promediar la matriz.**

**Estadístico de la prueba** (se fija ahora, no después): se estandariza cada mercado por su **propio
σ** — medido a ciegas, sin media, con los controles de `tests/multimercado/test_ciego.py` — y se
promedia sobre las N operaciones. Con eso `R` es exactamente la matriz de correlación y la fórmula de
arriba es exacta, no una aproximación.

### c.3 Los costos van adentro del número, nunca en una nota al pie

`δ` es **neto**. El bruto de ES es `δ_bruto = 0,151542 + 3,90/166,95 = 0,174903`. Por mercado:

```
f_i  = costo_vuelta_completa_i / sigma_i        (sigma medido a ciegas, en USD)
δ_i  = min( δ_bruto − f_i ,  0,151542 )
δ̄    = Σ_i ( n_i · δ_i ) / N
```

**El `min(...)` es fail-closed y es deliberado.** Si un mercado paga **menos** fricción por unidad de
riesgo que MES —lo que la tabla de `multimercado_dia0.md` §7 hizo esperar para contratos grandes, y NKD
es un contrato grande— la fórmula le daría un `δ` **mayor** que el de ES y **aflojaría la vara**.
Con especificaciones **no verificadas contra el exchange** (§b.8), una vara más floja apoyada en un dato
sin verificar es exactamente la clase de error que este proyecto existe para no cometer.
**Una fricción no verificada puede endurecer la vara; nunca aflojarla.**

> **Umbral operativo:** con el tope activo, `δ̄ = 0,151542` y el número que decide es
> **342 operaciones efectivas**. Si algún `f_i` resultara mayor que el de ES, `δ̄` baja y el umbral
> **sube** a `(2,801585/δ̄)²`. **El umbral se recalcula con la fórmula, no se elige.**

### c.4 El efecto mínimo detectable, que es el entregable honesto

La pregunta invertida de `multimercado_dia0.md` §9: dado lo que sobrevivió, **qué tamaño de efecto
detecta este diseño al 80 %**:

```
δ mínimo detectable = 2,801585 / raiz(n_efectivo)
```

Se reporta siempre junto a `δ̄`, y se reporta además la potencia contra un `δ` deflactado al **75 %** y al
**50 %** del medido — no como criterio, sino porque el `δ` medido es un máximo seleccionado de 57 y el
lector tiene derecho a ver qué pasa si la maldición del ganador se cobró un tercio o la mitad.

---

## d) LA REGLA DE DECISIÓN — escrita antes de medir

**Muestra congelada de la fase** (`factory/mm_muestra.py`, historia completa 2000-2026, post-exclusión
de roll). El **bloque A** es el calendario del descubrimiento: períodos hasta **2019-11** inclusive — el
turno 2019-12 sale en enero de 2020, el ledger de ES nunca lo contuvo, y medirlo exigiría leer precios
de 2020, que hoy está prohibido para los cuatro mercados:

| mercado | vueltas en muestra | bloque A (≤ 2019-11) | bloque B (2019-12 →) |
|---|---|---|---|
| NQ | **309** | 230 | 79 |
| YM | **289** | 210 | 79 |
| NKD | **180** | 126 | 54 |
| **N nominal** | **778** | 566 | 212 |

Períodos comunes por par (historia completa / bloque A): NQ-YM **289 / 210** · NQ-NKD **180 / 126** ·
YM-NKD **180 / 126**.

*(Corrección del 26-ago, misma tanda, antes de medir: la primera versión de esta tabla partía en
"año ≤ 2019", que asignaba el turno 2019-12 al bloque A y no restaba las exclusiones de roll del bloque —
decía 231/211/127 y 569/209. La definición corregida es la de arriba y es la que usa la medición.)*

### La regla

> **COMPUERTA 1 (la que pidió Roberto).** La fase **SE ABRE** si y sólo si
> `n_efectivo ≥ (2,801585 / δ̄)²`, que con el tope de §c.3 es **`n_efectivo ≥ 342`**.
> Si `n_efectivo < 342`, **la fase NO se abre** y el paquete se publica como NEGATIVO — igual que
> `multimercado_dia0.md` el 24-ago.
>
> **COMPUERTA 2 (agregada hoy; ENDURECE; entra al ledger).** La misma cuenta rehecha con cada
> correlación en su **cota superior al 90 %** (`ρ + 1,2816·SE`, `SE = (1−ρ²)/√(n_par − 3)`)
> también tiene que dar **≥ 342**. **Las dos tienen que pasar.**
>
> *Por qué se agrega:* con `N = 778` la correlación de quiebre es `ρ = 0,765`. Correlaciones entre
> índices bursátiles del orden de 0,7-0,9 son lo esperable, así que **el veredicto va a caer cerca del
> filo** — y una decisión al filo sobre un parámetro estimado con ~130-210 observaciones se decide por
> el error de estimación. Ante ambigüedad, **fail-closed: no se abre.** Se declara ahora, con el signo
> puesto antes de conocer el número.

**Traducido a la correlación, para que no se pueda re-discutir después:** con N = 778 y los solapamientos
de arriba, la compuerta 1 se cae cuando la correlación media ponderada por par supera **0,765**.

### D1) Divulgación obligatoria: cuánto de la evidencia comparte calendario con el descubrimiento

**No es una compuerta. Es una obligación de reporte, y es el punto metodológico más serio del paquete.**

F4 se eligió como la mejor de 57 sobre **el camino realizado de ES en 2000-2019**. NQ e YM corren sobre
**esas mismas fechas** y están fuertemente correlacionados con ES. Si el resultado de ES sobre esas
fechas fue en parte suerte, **NQ e YM heredan esa misma suerte en proporción a su correlación con ES.**
Ninguna fórmula de efecto de diseño arregla eso: la fórmula corrige la **varianza**, no el hecho de que
la **selección** se hizo sobre un camino que estas series comparten.

Por eso el reporte **tiene que** publicar, siempre:

1. La matriz **completa**, sin promediar, **incluyendo la fila de ES** medida en 2000-2019. ES ya está
   completamente minado en esa ventana: mirarlo no filtra nada nuevo, y sin esa fila no se puede saber
   cuánta de la "evidencia nueva" es ES otra vez.
2. `n_efectivo` **partido en dos bloques**: bloque A ≤ 2019-11 (566 nominales, calendario compartido
   con el descubrimiento) y bloque B desde 2019-12 (212 nominales, calendario que ninguna búsqueda vio).
3. La frase, si corresponde: **un resultado positivo empujado por el bloque 2000-2019 es una réplica de
   la muestra de selección, no una confirmación independiente.**

*(Aclaración, porque importa: 2020-2026 de NQ/YM/NKD **no es** la caja fuerte. La caja fuerte es
2020-2026 de **ES** y sigue sellada, sin abrir, y nada de esta fase la toca.)*

---

## e) Qué se publica si el resultado es negativo

**Se publica igual, completo y con el mismo detalle que si fuera positivo.** Las dos ramas quedan
selladas hoy, copiando la disciplina de `multimercado_dia0.md` §10:

- **(a) Si el conjunto confirma** — `p ≤ 0,05` bilateral, prueba única, K = 1 — se afirma exactamente:
  *"una regla congelada, elegida en ES y jamás ajustada, superó una prueba única sobre tres índices que
  ninguna búsqueda había tocado"*. Con su fuerza declarada: **una sola prueba, sin partición, y NO es
  una estimación insesgada del rendimiento futuro** — el `δ` que la powerea es un máximo de 57.
  Y con la frase de D1 si el resultado viene del bloque 2000-2019.
- **(b) Si NO confirma** se afirma *"no pudimos confirmarla"*. **Jamás** *"la vuelta de mes no existe"*.
  Con la potencia real al lado: si el diseño corre con ~80 %, un no-resultado deja ~20 % de haberse
  perdido un efecto real **del tamaño supuesto**, y el tamaño supuesto ya es optimista.
- **(c) Si la fase NO se abre** (hoy) se publica el paquete entero: la lista con sus descartes, la regla
  de roll con sus 90 exclusiones de NKD, la matriz completa, `n_efectivo`, el efecto mínimo detectable y
  la predicción fallada o acertada. **Un día cero negativo es un resultado**, y este proyecto ya publicó
  uno.

---

## f) Cómo cuenta esto contra K

**K = 1 para esta prueba.** Coincido con Roberto, y el motivo tiene que quedar escrito hoy:

1. La hipótesis está **pre-registrada** y sus parámetros **congelados** con hash del ledger (§a).
2. **No hay búsqueda**: una sola configuración, un solo lado, un solo estadístico, un solo p-valor.
3. La multiplicidad de haber buscado 57 veces **ya se pagó** sobre ES y **no se cobra dos veces** — es
   exactamente el argumento de `spec_fase2.md` §3.3 (*"prueba única pre-registrada; la multiplicidad ya
   se pagó en A"*) y el de `multimercado_dia0.md` §0.
4. **K = 257 sigue intacto y se hereda**: es el contador de la BÚSQUEDA, y **no se reinicia nunca**.
   Cualquier búsqueda futura arranca de 257. Esta fase no es una búsqueda, así que no le suma.

**Lo que convertiría K = 1 en una mentira, escrito hoy para que se pueda auditar después:**
re-optimizar `n_before`/`m_after` en cualquiera de los tres mercados; cambiar la lista después de ver un
número; correr la fase dos veces; probar también el lado corto; agregar un filtro; o reportar el mejor
subconjunto de los tres mercados en vez de los tres juntos. **Cualquiera de esas seis convierte el
diseño en la Fase 2 otra vez, y la Fase 2 cerró en negativo.**

**Y el precio de la aritmética, dicho sin adornos:** si en lugar de una hipótesis congelada se corriera
una grilla de 3 × 3 (la vecindad de robustez de §2 de `botc_potencia_f4.md`) sobre 3 mercados, K = 27 y
el z bilateral exigido salta de 1,960 a **3,113**. El `n_efectivo` para 80 % de potencia sube de 342 a
**681**, y la correlación de quiebre se desploma de **0,765 a 0,085** — un valor que ningún par de
índices bursátiles tiene. **Un solo barrido de parámetros mata la fase.**

---

## Lo que esta spec NO hace

No pre-registra nada. No abre la fase. No gasta cartuchos. No compra datos. **No toca la caja fuerte de
ES (2020-2026), que sigue sellada y de un solo uso.** No corre un backtest: hoy no se calcula ni una
media, ni un P&L, ni un profit factor de ningún mercado. Lo único que se mide después de este commit es
la **matriz de correlación de los retornos de vuelta de mes sobre 2000-2019**, con salida ciega
(desmediada, matriz y σ solamente), y se la contrasta contra la regla de decisión que acaba de quedar
escrita arriba.
