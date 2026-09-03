# La fecha discordante 2016-11-16, y cuántas más hay — 2026-09-03

Salidas crudas: `discordancia_20161116.txt` (barra contra barra, 828 fechas comunes) y
`nt8_barras_truncadas.txt` (sólo los CSV diarios del guardián, cuatro raíces, todo el período).

## 1 · 2016-11-16: **NT8 está equivocada. Es una barra truncada.** SE DETERMINA.

| fuente | open | high | low | close | volumen |
|---|---|---|---|---|---|
| NT8 diario `ES 12-16` | 2179,00 | 2180,00 | 2178,25 | 2179,00 | **6.336** |
| Databento, sesión 17:00 → 16:00 CT | 2179,00 | 2185,00 | 2168,75 | 2172,25 | **1.317.471** |

Tres cosas lo cierran:

1. **El volumen de NT8 es el 0,5 % del de un día normal** (los vecinos tienen 1,3–1,8 M en las dos
   fuentes, idénticos al contrato). Una barra diaria con 6.336 contratos no es un día.
2. **El OHLC de NT8 es el de los primeros minutos de la tarde del 15-nov.** Databento tiene la
   apertura en 2179,00 a las 17:00 CT, y su tarde-noche entera (17:00 → 23:59) hace máximo 2185,00 y
   mínimo 2178,25: el mínimo de NT8 (2178,25) es el mínimo de esa primera franja, y su máximo (2180,00)
   se alcanza antes de las 18:23, cuando Databento marca 2185,00.
3. **NT8 se contradice a sí misma:** su cierre del 16-nov es 2179,00 y su apertura del 17-nov es
   2172,50. Databento cierra el 16-nov en 2172,25, a un tick de esa apertura. **La serie de NT8 tiene
   un salto de 6,5 puntos entre dos barras propias consecutivas que Databento no tiene.**

**El mismo día está truncado en `NQ 12-16` de NT8** (volumen 760, 0,35 % de la mediana local). Es un
defecto del servidor histórico de NT8 en esa fecha, no del contrato.

**Efecto sobre el terreno del guardián:** ese día la excursión larga de ES vale 0,75 en vez de 10,25.
Sobre 828 fechas no mueve ningún percentil (los cinco dieron 0,00 % de diferencia con la barra mal
incluida), pero **la clase de error sí importa para la cola**, porque una barra truncada siempre
achica la excursión.

## 2 · Cuántas más — el conteo, no sólo las nombradas

**Sobre las 828 fechas comunes, discordancia en la excursión (largo o corto):**

| umbral | fechas | a ≤ 3 sesiones de un cambio de contrato | lejos de todo roll |
|---|---|---|---|
| > 2 pts | **4** | 0 | 4 |
| > 5 pts | 1 | 0 | 1 |
| > 9 pts | 1 | 0 | 1 |

> **Corrección a mi propio reporte anterior:** dije que las fechas discordantes «se agrupan en días de
> roll». Es falso para las que importan: las cuatro de más de 2 puntos están a 9, 17, 22 y 23 sesiones
> del roll más cercano en cualquiera de las dos fuentes. Las que sí caen en semanas de roll (2018-12,
> 2019-09-16) difieren 1–1,5 puntos y no cuentan acá.

Las otras tres, con lo que hay: **NO SE DETERMINA.**

| fecha | discordancia | campo | nota |
|---|---|---|---|
| 2019-09-02 | 4,00 / 4,00 | sólo `open` | sesión del Labor Day (cierre 12:00 CT); volumen coincide (1,047); los dos proveedores toman una apertura distinta y no hay tercera fuente |
| 2017-01-18 | 2,75 / 3,75 | `open`, `high` 1,00 | volumen 1,16; high/low/close casi iguales; sólo la apertura difiere |
| 2017-01-19 | 2,25 / 2,25 | sólo `open` | ídem |

Por campo, sobre las 828: `open`, `high` y `low` coinciden al tick en **799–800 (96,5 %)**; el volumen
coincide **exactamente** (mediana de la razón 1,0000, p10 = p90 = 1,0000).

## 3 · Colateral: **el `close` diario de NT8 no es el último precio, es la liquidación** — evidencia fuerte, no prueba

El `close` coincide al tick con la barra de Databento de las **15:59 CT en sólo 225 de 798** fechas
(28 %), pero con la de las **15:14 CT en 512 (64 %)** y con la de las 15:15, cuando existe, en 50 de 68
(73 %). Mediana de la diferencia: 0,25 contra la 15:14, 0,75 contra la 15:59. **La liquidación de ES se
fija sobre 15:14:30–15:15:00 CT.** Rotulado **HIPÓTESIS CON EVIDENCIA**: consistente con la liquidación,
no verificado contra un archivo de liquidaciones de CME.

**Consecuencia que ya toca a lo congelado:** en las columnas diarias de NT8, `close_{t−1}` es la
liquidación de las 15:15 y `open_t` es la reapertura de las 17:00. El «hueco» de H2d es entonces el de
**15:15 → 17:00**, que incluye 30 minutos de negociación (15:30 → 16:00) más el corte. El control C0
del diseño ya lo atrapaba por el lado de la varianza; ahora se sabe también **qué es** lo que mide.
Lo mismo vale para el M3 y el M4 del guardián: son liquidación a liquidación, y `close − open` es
liquidación menos reapertura. No están mal; miden eso.

## 4 · Barras truncadas en todo el diario del guardián (sin tocar Databento ni 2020+ de minutos)

Criterio: volumen < 5 % de la mediana de las 10 barras anteriores y 10 siguientes, contrato elegido.

| raíz | fechas | marcadas | truncadas de verdad | feriado/sesión parcial esperable |
|---|---|---|---|---|
| ES | 2.579 | 4 | **2016-11-16** (V 6.336), **2023-04-18** (V 7.243), **2025-08-29** (V 2) | 2026-04-03 (Viernes Santo, V 71.443, rango 40) |
| NQ | 2.582 | 1 | **2016-11-16** (V 760) | — |
| MES | 1.880 | 1 | — | 2023-07-04 (4 de julio, V 35.119) |
| MNQ | 1.897 | 3 | **2023-04-06** (V 8.188) | 2025-01-01 (Año Nuevo, V 3, barra fantasma), 2026-09-03 (el día en curso) |

**Cinco barras truncadas de verdad en cuatro raíces, tres de ellas en 2020+**, donde esta ventana no
puede cruzar contra minutos. Y **dos barras fantasma de feriado con volumen 2–3** (ES 2025-08-29 es un
viernes normal con volumen 2: truncada, no feriado; MNQ 2025-01-01 es Año Nuevo). Se reporta a Roberto
para el guardián; **acá no se arregla nada.**
