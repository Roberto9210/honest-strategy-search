# Pre-registro — Terreno por duración de tenencia: cuánto baja el daño cuando la tenencia es más corta

**Fecha: 2026-09-03. Ventana D.** Se commitea **solo**, antes de correr un cálculo. No busca ninguna
ventaja. No hay hipótesis, no hay ganador, no hay multiplicidad: es una medición de terreno, como la
pregunta 1 del guardián, y por eso **no gasta la caja fuerte**: la caja protege contra elegir una regla
que parece buena por azar, y acá no se elige nada.

---

## LIMITACIONES, DECLARADAS ANTES DE CORRER

1. **Esto es ES, no MES.** La serie es `data/es_1min_databento.csv` (ES front por open interest,
   Databento, OHLCV-1m). Ventana A verificó (guardián `8e5f5c8`) que ES y MES son **libros separados
   que no comparten OHLC**: el mismo día, la apertura difirió 8 puntos. **Lo que se mide acá es el
   terreno de ES. Su traslado a MES es un SUPUESTO, no una medición.** Los dólares «de MES» de abajo
   son puntos de ES multiplicados por 5, y se rotulan así.
2. **Una tenencia de horario fijo no es una estrategia.** Es otra tenencia pasiva, más corta. No dice
   nada de si conviene entrar, ni cuándo salir, ni si alguna duración es rentable. **No se mira si
   alguna duración gana.** Sólo cuánto se mueve en contra.
3. **Período: 2016-01-04 → 2019-12-31**, el tramo ya barrido por la búsqueda 1. Nada de 2020 en
   adelante se lee. El QC del archivo (`data/data_quality_es_1min_databento.md`) declara utilizable
   el intradía desde 2016; los días `degraded` de Databento dentro del período se excluyen y se
   cuentan.
4. **Es un proveedor distinto del guardián.** El guardián midió NT8/Kinetick; esto es Databento.
   Por eso existe el control 1, y por eso si el control falla se para.
5. **Sin comisiones ni deslizamiento**, igual que la pregunta 1: es excursión de precio, no PnL.

---

## Definiciones

| término | definición |
|---|---|
| **zona horaria** | todo en hora de Chicago (CT), con horario de verano, convertido desde el `ts_event_utc` de la barra (apertura de la barra) |
| **sesión** | 17:00 CT → 16:00 CT del día calendario siguiente. Se etiqueta por la fecha del cierre. Una barra con hora CT ≥ 17:00 pertenece a la sesión del día siguiente |
| **ventana `[a, b)`** | las barras cuya apertura CT está en `a ≤ t < b`, dentro de una misma sesión. La barra de las 15:59 es la última de una ventana que termina a las 16:00 |
| **apertura de la ventana** | `open` de la primera barra de la ventana |
| **excursión adversa, largo** | `open_ventana − min(low)` sobre la ventana. Exacta para una entrada en la apertura de la ventana |
| **excursión adversa, corto** | `max(high) − open_ventana` |
| **contrato** | el que Databento asigna (`contract`). Una sesión con **más de un contrato** adentro se excluye entera y se cuenta: la excursión no cruza contratos (misma regla que Ventana A) |

## Las cuatro ventanas

| nombre | ventana CT | duración |
|---|---|---|
| **T23** (referencia) | 17:00 día anterior → 16:00 | ~23 h |
| **RTH** | 08:30 → 15:00 | 6,5 h |
| **H1** | 08:30 → 09:30 | 1 h |
| **M15** | 08:30 → 08:45 | 15 min |

## Poblaciones — dos, y se dice cuál es cuál

- **P-control**: sesiones del período con barra de apertura a las **17:00 CT exactas** del día anterior,
  un solo contrato, no `degraded`, **y** con barra diaria de ES en los CSV del guardián en esa fecha
  bajo su regla (contrato de máximo volumen, fecha descartada si el contrato cambió). Es la
  intersección de las dos fuentes.
- **P-escalera**: sesiones del período con un solo contrato, no `degraded`, con barra exacta a las
  17:00 CT del día anterior, barra exacta a las **08:30 CT**, y última barra de RTH a las **15:59 CT**
  o después (sin cierre anticipado). **Las cuatro ventanas se calculan sobre exactamente estas
  sesiones**, para que la columna de caída compare lo mismo con lo mismo.

Se imprimen: total de sesiones del período, y cuántas excluye cada regla, por regla.

---

## 1 · EL CONTROL — y éste debe dar igual

Sobre P-control, para T23, largo y corto: mediana, p90, p95, p99 y máximo, en puntos. Contra la
misma medición hecha con las **barras diarias de ES del guardián** (CSV de `37a0144`, los 41 `ES_*.csv`,
regla de máximo volumen por fecha, `open − low` y `high − open`), **restringida al mismo período y
a las mismas fechas**. Los números publicados del guardián (`f75d126`, M1 raíz ES) son sobre
2016-08-23 → 2026-08-21 y se imprimen al lado sólo como orientación: no son el control, porque el
período no es el mismo.

Además del acuerdo por percentil, acuerdo **por fecha**: sobre las fechas comunes, la razón
`excursión_Databento / excursión_NT8` del lado largo, su mediana, y la fracción de fechas con
diferencia ≤ 1 tick (0,25) y ≤ 2 puntos.

**Criterio, fijado ahora:**

| resultado | criterio |
|---|---|
| **PASA** | p50, p90 y p95 difieren menos del **5 %** cada uno, y la mediana de la razón por fecha está en [0,97, 1,03] |
| **INDETERMINADO** | alguno entre 5 % y 10 %: se para igual, se reporta, y no se sigue sin decisión |
| **FALLA** | alguno ≥ **10 %**, o mediana de la razón fuera de [0,95, 1,05] |

El p99 y el máximo se reportan, no deciden: con ~800 sesiones, el p99 descansa sobre 8 observaciones.

**Si NO PASA, se para.** El resto no se corre ni se imprime. Dos proveedores en desacuerdo son
información, no un detalle.

## 2 · LA ESCALERA

Con el control pasado, sobre P-escalera, para cada ventana y para cada lado: mediana, p90, p95, p99
y máximo en puntos; los mismos en «dólares de MES» (×5); y el **porcentaje de sesiones con excursión
> 1.000 USD con un contrato de MES** (es decir, > 200 puntos).

## 3 · LA TABLA

Una fila por ventana y lado. Columnas: n, p50, p90, p95, p99, y para cada percentil **la caída
respecto de T23**: `1 − percentil_ventana / percentil_T23`, en porcentaje. Esa columna es la respuesta.

## Dónde se observa

| | |
|---|---|
| script | `research/ventaja_futuros/terreno_tenencia.py` |
| salida cruda, commiteada antes de interpretar | `research/ventaja_futuros/terreno_tenencia.txt` |
| resumen | `research/ventaja_futuros/terreno_tenencia_resultado.md` |

## Lo que esta medición NO dice — antes de verla

- No dice si existe una ventaja. No busca ninguna. No mira si alguna duración es rentable.
- No dice nada de MES: dice de ES, y el traslado es un supuesto.
- No secuencia el camino dentro de la ventana más allá del mínimo y el máximo: la excursión es
  exacta sólo para una entrada en la apertura de la ventana.
- Un percentil de excursión no es un stop: es lo que una tenencia pasiva aguanta sin salir.
