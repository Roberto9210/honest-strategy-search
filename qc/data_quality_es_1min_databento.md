# Informe de calidad — es_1min_databento.csv (ES.n.0, GLBX.MDP3, OHLCV-1m)

Generado: 2026-08-19 15:25 EDT. Fuente: Databento `timeseries.get_range` (dataset GLBX.MDP3, schema ohlcv-1m, symbol `ES.n.0` = front-month por open interest, `stype_in=continuous`, 2010-06-06 → hoy). `ts_event_utc` es la **apertura** de la barra, en UTC. Precios sin ajustar por roll; la columna `symbol` dice qué contrato compone cada barra. Nada se corrigió.

Criterios: hueco = más de 3 días hábiles (lun–vie) faltantes entre barras consecutivas; salto = |cierre/cierre previo − 1| > 20 %; precio absurdo = high < low, precio ≤ 0, OHLC incoherente. 'Día de negociación' = sesión CME 18:00 ET → 17:00 ET, etiquetado por la fecha en que termina.

## 1. Resumen

- Filas: **4,904,294**; rango: 2010-06-07 00:00 UTC → 2026-08-18 23:59 UTC (2010-06-06 20:00 EDT → 2026-08-18 19:59 EDT)
- Días de negociación distintos: 4,183; contratos distintos: 66 (tickers distintos: 40; los tickers se repiten cada década)
- Índice monótono creciente: sí; timestamps duplicados: 0
- NaN en OHLC: 0; NaN en volumen: 0; NaN en contract: 0
- Volumen total: 6,370,924,668; volumen mediano por barra: 246

## 1b. Condición del dataset según Databento (`metadata.get_dataset_condition`)

- Días listados: 5,111; por condición: {'available': 5080, 'degraded': 31}
- Días NO 'available' (degraded/pending/missing): **31**

| date | condition | last_modified_date |
|---|---|---|
| 2014-06-11 | degraded | 2026-05-03 |
| 2014-06-12 | degraded | 2026-05-03 |
| 2014-06-13 | degraded | 2026-05-04 |
| 2014-06-15 | degraded | 2026-05-02 |
| 2014-09-22 | degraded | 2026-05-02 |
| 2014-09-23 | degraded | 2026-05-02 |
| 2014-09-24 | degraded | 2026-05-02 |
| 2014-09-25 | degraded | 2026-05-03 |
| 2017-11-13 | degraded | 2026-02-20 |
| 2018-10-21 | degraded | 2026-05-24 |
| 2019-01-15 | degraded | 2026-05-22 |
| 2019-02-22 | degraded | 2026-05-22 |
| 2019-03-13 | degraded | 2026-05-22 |
| 2019-03-26 | degraded | 2026-05-22 |
| 2020-02-27 | degraded | 2026-05-27 |
| 2020-02-28 | degraded | 2026-05-28 |
| 2020-06-30 | degraded | 2026-05-22 |
| 2020-07-01 | degraded | 2026-05-22 |
| 2021-12-05 | degraded | 2026-05-18 |
| 2022-01-02 | degraded | 2026-04-03 |
| 2024-09-18 | degraded | 2026-04-21 |
| 2025-09-17 | degraded | 2026-06-11 |
| 2025-09-24 | degraded | 2026-06-12 |
| 2025-11-28 | degraded | 2026-06-09 |
| 2026-01-31 | degraded | 2026-06-04 |
| 2026-03-15 | degraded | 2026-06-05 |
| 2026-03-16 | degraded | 2026-06-06 |
| 2026-03-21 | degraded | 2026-05-18 |
| 2026-04-10 | degraded | 2026-05-21 |
| 2026-05-24 | degraded | 2026-06-05 |
| 2026-07-30 | degraded | 2026-07-31 |

## 2. Huecos

**Huecos > 3 días hábiles: 0**

_(ninguna)_

Huecos > 1 min entre barras consecutivas: 29,875 — corte diario 17:00→18:00 ET: 2,070, fin de semana vie 17:00→dom 18:00: 808, **otros: 26,997**

Los 40 huecos 'otros' más grandes (festivos con cierre temprano, sesiones sin cotizar, o barras faltantes):

| desde | hasta | hueco |
|---|---|---|
| 2014-06-11 19:59 EDT | 2014-06-15 18:00 EDT | 3 days 22:01:00 |
| 2011-12-23 17:25 EST | 2011-12-27 06:00 EST | 3 days 12:35:00 |
| 2011-12-30 17:25 EST | 2012-01-03 06:00 EST | 3 days 12:35:00 |
| 2014-09-22 19:56 EDT | 2014-09-26 07:22 EDT | 3 days 11:26:00 |
| 2020-12-24 13:14 EST | 2020-12-27 18:00 EST | 3 days 04:46:00 |
| 2015-12-24 13:14 EST | 2015-12-27 18:00 EST | 3 days 04:46:00 |
| 2020-04-09 16:59 EDT | 2020-04-12 18:00 EDT | 3 days 01:01:00 |
| 2017-12-22 16:59 EST | 2017-12-25 18:00 EST | 3 days 01:01:00 |
| 2022-04-14 16:59 EDT | 2022-04-17 18:00 EDT | 3 days 01:01:00 |
| 2016-03-24 16:59 EDT | 2016-03-27 18:00 EDT | 3 days 01:01:00 |
| 2023-12-22 16:59 EST | 2023-12-25 18:00 EST | 3 days 01:01:00 |
| 2022-12-30 16:59 EST | 2023-01-02 18:00 EST | 3 days 01:01:00 |
| 2022-12-23 16:59 EST | 2022-12-26 18:00 EST | 3 days 01:01:00 |
| 2020-12-31 16:59 EST | 2021-01-03 18:00 EST | 3 days 01:01:00 |
| 2015-12-31 16:59 EST | 2016-01-03 18:00 EST | 3 days 01:01:00 |
| 2024-03-28 16:59 EDT | 2024-03-31 18:00 EDT | 3 days 01:01:00 |
| 2016-12-30 16:59 EST | 2017-01-02 18:00 EST | 3 days 01:01:00 |
| 2025-04-17 16:59 EDT | 2025-04-20 18:00 EDT | 3 days 01:01:00 |
| 2023-12-29 16:59 EST | 2024-01-01 18:00 EST | 3 days 01:01:00 |
| 2017-12-29 16:59 EST | 2018-01-01 18:00 EST | 3 days 01:01:00 |
| 2021-12-23 16:59 EST | 2021-12-26 18:00 EST | 3 days 01:01:00 |
| 2018-03-29 16:59 EDT | 2018-04-01 18:00 EDT | 3 days 01:01:00 |
| 2017-04-13 16:59 EDT | 2017-04-16 18:00 EDT | 3 days 01:01:00 |
| 2016-12-23 16:59 EST | 2016-12-26 18:00 EST | 3 days 01:01:00 |
| 2019-04-18 16:59 EDT | 2019-04-21 18:00 EDT | 3 days 01:01:00 |
| 2013-02-15 17:28 EST | 2013-02-18 18:00 EST | 3 days 00:32:00 |
| 2013-05-24 17:29 EDT | 2013-05-27 18:00 EDT | 3 days 00:31:00 |
| 2013-03-28 17:30 EDT | 2013-03-31 18:00 EDT | 3 days 00:30:00 |
| 2014-01-17 17:34 EST | 2014-01-20 18:00 EST | 3 days 00:26:00 |
| 2014-02-14 17:35 EST | 2014-02-17 18:00 EST | 3 days 00:25:00 |
| 2014-04-17 17:35 EDT | 2014-04-20 18:00 EDT | 3 days 00:25:00 |
| 2013-01-18 17:35 EST | 2013-01-21 18:00 EST | 3 days 00:25:00 |
| 2013-08-30 17:35 EDT | 2013-09-02 18:00 EDT | 3 days 00:25:00 |
| 2010-12-23 18:02 EST | 2010-12-26 18:00 EST | 2 days 23:58:00 |
| 2011-04-21 19:11 EDT | 2011-04-24 18:00 EDT | 2 days 22:49:00 |
| 2014-08-22 17:35 EDT | 2014-08-24 22:00 EDT | 2 days 04:25:00 |
| 2018-04-27 16:59 EDT | 2018-04-29 18:30 EDT | 2 days 01:31:00 |
| 2018-08-03 17:00 EDT | 2018-08-05 17:59 EDT | 2 days 00:59:00 |
| 2014-12-30 18:59 EST | 2015-01-01 18:00 EST | 1 days 23:01:00 |
| 2013-12-24 17:18 EST | 2013-12-26 06:00 EST | 1 days 12:42:00 |

Huecos 'otros' de ≤ 30 min (barras de 1 min sin imprimir — Databento sólo emite barra si hubo trade): 25,040; minutos faltantes acumulados en ellos: 51,641
De ellos, con fin dentro de 09:30–16:00 ET: 51

## 3. Cobertura por día de negociación

Barras por día de negociación: mediana 1363, p5 122, mín 1 (2010-12-24), máx 1380 (2021-06-28). Un día completo son ~1.380 min (23 h).
Días con < 600 barras: 568

| trading_day | barras | dia_semana |
|---|---|---|
| 2010-06-08 | 150 | Tuesday |
| 2010-06-09 | 153 | Wednesday |
| 2010-06-10 | 151 | Thursday |
| 2010-06-11 | 141 | Friday |
| 2010-06-15 | 184 | Tuesday |
| 2010-06-16 | 96 | Wednesday |
| 2010-06-17 | 144 | Thursday |
| 2010-06-18 | 147 | Friday |
| 2010-06-22 | 144 | Tuesday |
| 2010-06-23 | 151 | Wednesday |
| 2010-06-24 | 145 | Thursday |
| 2010-06-25 | 152 | Friday |
| 2010-06-29 | 146 | Tuesday |
| 2010-06-30 | 152 | Wednesday |
| 2010-07-01 | 153 | Thursday |
| 2010-07-02 | 150 | Friday |
| 2010-07-07 | 145 | Wednesday |
| 2010-07-08 | 151 | Thursday |
| 2010-07-09 | 148 | Friday |
| 2010-07-13 | 158 | Tuesday |
| 2010-07-14 | 150 | Wednesday |
| 2010-07-15 | 143 | Thursday |
| 2010-07-16 | 148 | Friday |
| 2010-07-20 | 154 | Tuesday |
| 2010-07-21 | 169 | Wednesday |
| 2010-07-22 | 143 | Thursday |
| 2010-07-23 | 146 | Friday |
| 2010-07-27 | 135 | Tuesday |
| 2010-07-28 | 140 | Wednesday |
| 2010-07-29 | 148 | Thursday |
| 2010-07-30 | 140 | Friday |
| 2010-08-03 | 143 | Tuesday |
| 2010-08-04 | 138 | Wednesday |
| 2010-08-05 | 135 | Thursday |
| 2010-08-06 | 139 | Friday |
| 2010-08-10 | 127 | Tuesday |
| 2010-08-11 | 142 | Wednesday |
| 2010-08-12 | 154 | Thursday |
| 2010-08-13 | 144 | Friday |
| 2010-08-17 | 141 | Tuesday |
| 2010-08-18 | 150 | Wednesday |
| 2010-08-19 | 149 | Thursday |
| 2010-08-20 | 147 | Friday |
| 2010-08-24 | 151 | Tuesday |
| 2010-08-25 | 150 | Wednesday |
| 2010-08-26 | 149 | Thursday |
| 2010-08-27 | 150 | Friday |
| 2010-08-31 | 171 | Tuesday |
| 2010-09-01 | 151 | Wednesday |
| 2010-09-02 | 216 | Thursday |
| 2010-09-03 | 147 | Friday |
| 2010-09-08 | 161 | Wednesday |
| 2010-09-09 | 143 | Thursday |
| 2010-09-10 | 131 | Friday |
| 2010-09-14 | 114 | Tuesday |
| 2010-09-15 | 87 | Wednesday |
| 2010-09-16 | 147 | Thursday |
| 2010-09-17 | 183 | Friday |
| 2010-09-21 | 194 | Tuesday |
| 2010-09-22 | 157 | Wednesday |

_(mostrando 60 de 568)_

Días de negociación etiquetados en sábado (no debería haber): 1

Por año:

| año | barras | dias | vol | barras_por_dia |
|---|---|---|---|---|
| 2010 | 59533 | 150 | 267868168 | 397 |
| 2011 | 120862 | 259 | 546024139 | 467 |
| 2012 | 159562 | 260 | 422505374 | 614 |
| 2013 | 268487 | 254 | 402044174 | 1057 |
| 2014 | 264633 | 254 | 364875364 | 1042 |
| 2015 | 298194 | 259 | 380554640 | 1151 |
| 2016 | 348774 | 258 | 415998587 | 1352 |
| 2017 | 344324 | 257 | 313146796 | 1340 |
| 2018 | 348914 | 259 | 383669234 | 1347 |
| 2019 | 349453 | 258 | 339265946 | 1354 |
| 2020 | 350265 | 259 | 427975212 | 1352 |
| 2021 | 353296 | 259 | 348329858 | 1364 |
| 2022 | 354118 | 258 | 439595503 | 1373 |
| 2023 | 353154 | 258 | 390217836 | 1369 |
| 2024 | 354799 | 259 | 351035838 | 1370 |
| 2025 | 352538 | 258 | 351405000 | 1366 |
| 2026 | 223388 | 164 | 226412999 | 1362 |

## 3b. Barras de 'sesión comprimida' (defecto de la fuente, años tempranos)

Criterio: barra cuyo volumen supera el **30 % del volumen total de su día de negociación**. En un día sano ningún minuto se acerca a eso. Verificado contra el ticker crudo `ESU0` (2010-06-22, pedido aparte): la barra de las 23:59 UTC (19:59 EDT / 18:59 EST) lleva el OHLC y el volumen de TODA la sesión y coincide con el diario de Yahoo; sólo la franja 18:00→ ET de esos días tiene minutos reales. Origen probable: archivos FIX históricos sin timestamps intradía (Databento documenta que los datos pre-2017-05-21 vienen de flat files).

Barras con > 30 % del volumen del día: **720** en 611 días de negociación (2010-06-07 19:59 EDT → 2018-08-05 17:59 EDT)

| año | dias_con_barra_comprimida | dias_negociacion | %_dias_afectados |
|---|---|---|---|
| 2010 | 138 | 150 | 92.0 |
| 2011 | 224 | 259 | 86.5 |
| 2012 | 185 | 260 | 71.2 |
| 2013 | 62 | 254 | 24.4 |
| 2014 | 66 | 254 | 26.0 |
| 2015 | 44 | 259 | 17.0 |
| 2018 | 1 | 259 | 0.4 |

Por día de la semana del día de negociación afectado:

| año | Tuesday | Wednesday | Thursday | Friday | Saturday | Sunday |
|---|---|---|---|---|---|---|
| 2010 | 23 | 30 | 30 | 55 | 0 | 0 |
| 2011 | 36 | 47 | 51 | 90 | 0 | 0 |
| 2012 | 33 | 40 | 39 | 72 | 1 | 0 |
| 2013 | 11 | 16 | 18 | 17 | 0 | 0 |
| 2014 | 16 | 19 | 16 | 15 | 0 | 0 |
| 2015 | 10 | 12 | 11 | 11 | 0 | 0 |
| 2018 | 0 | 0 | 0 | 0 | 0 | 1 |

Hora UTC de la barra comprimida (top):

| utc_hhmm | n |
|---|---|
| 23:59 | 586 |
| 21:25 | 12 |
| 22:28 | 10 |
| 21:24 | 10 |
| 22:34 | 9 |
| 21:26 | 8 |
| 21:27 | 7 |
| 21:30 | 6 |

Últimas 10 ocurrencias (para ver hasta cuándo llega el defecto):

| ny | contract | open | high | low | close | volume | share_% |
|---|---|---|---|---|---|---|---|
| 2015-11-05 18:59 EST | ESZ5 | 2093.0 | 2104.75 | 2084.0 | 2092.0 | 1525212 | 45.3 |
| 2015-11-09 18:59 EST | ESZ5 | 2072.5 | 2075.0 | 2071.5 | 2072.25 | 46657 | 90.3 |
| 2015-11-10 18:59 EST | ESZ5 | 2072.75 | 2079.0 | 2064.5 | 2075.5 | 1278789 | 52.9 |
| 2015-11-11 18:59 EST | ESZ5 | 2069.25 | 2069.75 | 2067.75 | 2068.5 | 32436 | 84.5 |
| 2015-11-12 18:59 EST | ESZ5 | 2043.0 | 2077.5 | 2039.5 | 2040.5 | 1784758 | 45.7 |
| 2015-11-13 17:32 EST | ESZ5 | 2044.25 | 2046.0 | 2011.5 | 2013.0 | 2114648 | 54.1 |
| 2015-11-16 18:59 EST | ESZ5 | 2047.0 | 2050.75 | 2047.0 | 2048.75 | 58011 | 87.9 |
| 2015-11-17 18:59 EST | ESZ5 | 2048.0 | 2063.5 | 2041.5 | 2049.75 | 1601531 | 99.7 |
| 2015-11-18 18:59 EST | ESZ5 | 2047.75 | 2082.5 | 2043.0 | 2081.5 | 1524522 | 54.9 |
| 2018-08-05 17:59 EDT | ESU8 | 2841.5 | 2841.5 | 2841.25 | 2841.5 | 302 | 100.0 |

Días de negociación con < 600 barras (ya listados arriba): 568; de ellos, con barra comprimida: 547

## 4. Precios y volumen

- high < low: **0**
- precio ≤ 0: **0**
- OHLC incoherente: **0**
- Barras con volumen 0: **0** (0.000 %)
- Saltos |cierre/cierre previo − 1| > 20 %: **0**
- Mayor |retorno| barra-a-barra: 6.66 % en 2011-08-09 18:00 EDT

Movimientos barra-a-barra > 2 % (informativo): 61

| ny | symbol_prev | symbol | ret | close |
|---|---|---|---|---|
| 2010-06-10 18:00 EDT | ESM0 | ESM0 | +3.06 % | 1085.75 |
| 2010-06-29 18:00 EDT | ESU0 | ESU0 | -3.70 % | 1034.0 |
| 2010-07-07 18:00 EDT | ESU0 | ESU0 | +3.64 % | 1059.25 |
| 2010-07-16 17:30 EDT | ESU0 | ESU0 | -2.81 % | 1063.25 |
| 2010-07-22 18:00 EDT | ESU0 | ESU0 | +2.30 % | 1088.0 |
| 2010-08-11 18:00 EDT | ESU0 | ESU0 | -3.32 % | 1076.5 |
| 2010-09-01 18:00 EDT | ESU0 | ESU0 | +2.71 % | 1080.25 |
| 2010-12-01 18:00 EST | ESZ0 | ESZ0 | +2.29 % | 1204.5 |
| 2011-03-01 18:00 EST | ESH1 | ESH1 | -2.22 % | 1299.0 |
| 2011-03-16 18:00 EDT | ESH1 | ESH1 | -2.72 % | 1251.0 |
| 2011-06-01 18:00 EDT | ESM1 | ESM1 | -2.45 % | 1311.5 |
| 2011-08-02 18:00 EDT | ESU1 | ESU1 | -2.73 % | 1246.5 |
| 2011-08-04 18:00 EDT | ESU1 | ESU1 | -4.71 % | 1198.5 |
| 2011-08-07 18:00 EDT | ESU1 | ESU1 | -2.65 % | 1165.75 |
| 2011-08-09 18:00 EDT | ESU1 | ESU1 | +6.66 % | 1176.75 |
| 2011-08-10 18:00 EDT | ESU1 | ESU1 | -4.31 % | 1121.5 |
| 2011-08-11 18:00 EDT | ESU1 | ESU1 | +3.50 % | 1166.5 |
| 2011-08-18 18:00 EDT | ESU1 | ESU1 | -3.81 % | 1142.0 |
| 2011-08-23 18:00 EDT | ESU1 | ESU1 | +3.43 % | 1159.75 |
| 2011-09-02 17:26 EDT | ESU1 | ESU1 | -2.52 % | 1169.75 |
| 2011-09-07 18:00 EDT | ESU1 | ESU1 | +2.94 % | 1200.25 |
| 2011-09-09 17:32 EDT | ESU1 | ESU1 | -2.30 % | 1158.25 |
| 2011-09-21 18:00 EDT | ESZ1 | ESZ1 | -3.63 % | 1156.25 |
| 2011-09-22 18:00 EDT | ESZ1 | ESZ1 | -2.40 % | 1129.0 |
| 2011-09-30 17:27 EDT | ESZ1 | ESZ1 | -3.02 % | 1122.25 |
| 2011-10-04 18:00 EDT | ESZ1 | ESZ1 | +2.62 % | 1114.75 |
| 2011-10-06 18:00 EDT | ESZ1 | ESZ1 | +2.18 % | 1157.75 |
| 2011-10-18 18:00 EDT | ESZ1 | ESZ1 | +2.12 % | 1216.5 |
| 2011-10-27 18:00 EDT | ESZ1 | ESZ1 | +3.12 % | 1281.5 |
| 2011-11-03 18:00 EDT | ESZ1 | ESZ1 | +2.53 % | 1256.0 |
| 2011-11-09 18:00 EST | ESZ1 | ESZ1 | -3.67 % | 1226.0 |
| 2011-11-11 17:24 EST | ESZ1 | ESZ1 | +2.12 % | 1261.75 |
| 2011-11-30 18:00 EST | ESZ1 | ESZ1 | +4.32 % | 1244.0 |
| 2011-12-08 18:00 EST | ESZ1 | ESZ1 | -2.39 % | 1234.25 |
| 2011-12-20 18:00 EST | ESH2 | ESH2 | +2.51 % | 1235.75 |
| 2012-06-01 17:23 EDT | ESM2 | ESM2 | -2.54 % | 1273.75 |
| 2012-06-06 18:00 EDT | ESM2 | ESM2 | +2.19 % | 1316.0 |
| 2012-06-21 18:00 EDT | ESU2 | ESU2 | -2.04 % | 1322.0 |
| 2012-06-29 17:23 EDT | ESU2 | ESU2 | +3.11 % | 1358.25 |
| 2012-07-27 17:24 EDT | ESU2 | ESU2 | +2.09 % | 1382.5 |

_(mostrando 40 de 61)_

## 5. Rolls de contrato (cambios de `symbol`)

Rolls detectados: **65** (esperados ≈ 4/año ⇒ ~64 en el rango). Contratos: ESM0, ESU0, ESZ0, ESH1, ESM1, ESU1, ESZ1, ESH2 … ESM9, ESU9, ESZ9, ESH0

| primer_bar_nuevo (ET) | de | a | close_prev | open_nuevo | escalon_% | dia_semana |
|---|---|---|---|---|---|---|
| 2010-06-15 20:00 EDT | ESM0 | ESU0 | 1112.25 | 1107.25 | -0.45 | Tuesday |
| 2010-09-14 20:00 EDT | ESU0 | ESZ0 | 1119.25 | 1113.25 | -0.536 | Tuesday |
| 2010-12-15 19:00 EST | ESZ0 | ESH1 | 1238.0 | 1230.5 | -0.606 | Wednesday |
| 2011-03-16 20:00 EDT | ESH1 | ESM1 | 1253.5 | 1251.5 | -0.16 | Wednesday |
| 2011-06-15 20:00 EDT | ESM1 | ESU1 | 1265.5 | 1261.0 | -0.356 | Wednesday |
| 2011-09-14 20:00 EDT | ESU1 | ESZ1 | 1184.5 | 1183.0 | -0.127 | Wednesday |
| 2011-12-14 19:00 EST | ESZ1 | ESH2 | 1212.0 | 1206.25 | -0.474 | Wednesday |
| 2012-03-13 20:00 EDT | ESH2 | ESM2 | 1396.5 | 1390.0 | -0.465 | Tuesday |
| 2012-06-12 20:00 EDT | ESM2 | ESU2 | 1325.25 | 1318.0 | -0.547 | Tuesday |
| 2012-09-18 20:00 EDT | ESU2 | ESZ2 | 1461.0 | 1454.5 | -0.445 | Tuesday |
| 2012-12-18 19:00 EST | ESZ2 | ESH3 | 1445.75 | 1440.75 | -0.346 | Tuesday |
| 2013-03-12 20:00 EDT | ESH3 | ESM3 | 1553.0 | 1547.25 | -0.37 | Tuesday |
| 2013-06-18 20:00 EDT | ESM3 | ESU3 | 1651.5 | 1646.0 | -0.333 | Tuesday |
| 2013-09-17 20:00 EDT | ESU3 | ESZ3 | 1705.75 | 1698.75 | -0.41 | Tuesday |
| 2013-12-17 19:00 EST | ESZ3 | ESH4 | 1778.0 | 1773.75 | -0.239 | Tuesday |
| 2014-03-18 20:00 EDT | ESH4 | ESM4 | 1871.75 | 1864.75 | -0.374 | Tuesday |
| 2014-06-17 20:00 EDT | ESM4 | ESU4 | 1941.5 | 1933.75 | -0.399 | Tuesday |
| 2014-09-16 20:00 EDT | ESU4 | ESZ4 | 2000.0 | 1991.75 | -0.413 | Tuesday |
| 2014-12-16 19:00 EST | ESZ4 | ESH5 | 1975.25 | 1968.5 | -0.342 | Tuesday |
| 2015-03-17 20:00 EDT | ESH5 | ESM5 | 2075.0 | 2066.75 | -0.398 | Tuesday |
| 2015-06-16 20:00 EDT | ESM5 | ESU5 | 2098.0 | 2089.75 | -0.393 | Tuesday |
| 2015-09-15 20:00 EDT | ESU5 | ESZ5 | 1979.5 | 1969.5 | -0.505 | Tuesday |
| 2015-12-15 19:00 EST | ESZ5 | ESH6 | 2045.25 | 2036.75 | -0.416 | Tuesday |
| 2016-03-15 20:00 EDT | ESH6 | ESM6 | 2018.25 | 2009.0 | -0.458 | Tuesday |
| 2016-06-14 20:00 EDT | ESM6 | ESU6 | 2071.25 | 2062.5 | -0.422 | Tuesday |
| 2016-09-13 20:00 EDT | ESU6 | ESZ6 | 2129.25 | 2122.75 | -0.305 | Tuesday |
| 2016-12-13 19:00 EST | ESZ6 | ESH7 | 2272.5 | 2267.25 | -0.231 | Tuesday |
| 2017-03-14 20:00 EDT | ESH7 | ESM7 | 2367.5 | 2364.25 | -0.137 | Tuesday |
| 2017-06-13 20:00 EDT | ESM7 | ESU7 | 2440.0 | 2437.75 | -0.092 | Tuesday |
| 2017-09-12 20:00 EDT | ESU7 | ESZ7 | 2496.25 | 2494.5 | -0.07 | Tuesday |
| 2017-12-12 19:00 EST | ESZ7 | ESH8 | 2662.0 | 2664.75 | 0.103 | Tuesday |
| 2018-03-13 20:00 EDT | ESH8 | ESM8 | 2764.0 | 2768.25 | 0.154 | Tuesday |
| 2018-06-12 20:00 EDT | ESM8 | ESU8 | 2788.5 | 2792.75 | 0.152 | Tuesday |
| 2018-09-18 20:00 EDT | ESU8 | ESZ8 | 2907.0 | 2912.25 | 0.181 | Tuesday |
| 2018-12-18 19:00 EST | ESZ8 | ESH9 | 2540.75 | 2543.0 | 0.089 | Tuesday |
| 2019-03-12 20:00 EDT | ESH9 | ESM9 | 2790.5 | 2795.75 | 0.188 | Tuesday |
| 2019-06-18 20:00 EDT | ESM9 | ESU9 | 2924.25 | 2928.5 | 0.145 | Tuesday |
| 2019-09-17 20:00 EDT | ESU9 | ESZ9 | 3004.25 | 3007.0 | 0.092 | Tuesday |
| 2019-12-17 19:00 EST | ESZ9 | ESH0 | 3190.75 | 3194.5 | 0.118 | Tuesday |
| 2020-03-18 20:00 EDT | ESH0 | ESM0 | 2457.0 | 2444.0 | -0.529 | Wednesday |
| 2020-06-17 20:00 EDT | ESM0 | ESU0 | 3102.0 | 3091.0 | -0.355 | Wednesday |
| 2020-09-15 20:00 EDT | ESU0 | ESZ0 | 3401.75 | 3391.25 | -0.309 | Tuesday |
| 2020-12-15 19:00 EST | ESZ0 | ESH1 | 3693.5 | 3686.25 | -0.196 | Tuesday |
| 2021-03-16 20:00 EDT | ESH1 | ESM1 | 3964.5 | 3954.75 | -0.246 | Tuesday |
| 2021-06-15 20:00 EDT | ESM1 | ESU1 | 4247.0 | 4237.0 | -0.235 | Tuesday |
| 2021-09-14 20:00 EDT | ESU1 | ESZ1 | 4451.0 | 4441.25 | -0.219 | Tuesday |
| 2021-12-14 19:00 EST | ESZ1 | ESH2 | 4636.5 | 4627.25 | -0.2 | Tuesday |
| 2022-03-15 20:00 EDT | ESH2 | ESM2 | 4256.75 | 4248.5 | -0.194 | Tuesday |
| 2022-06-14 20:00 EDT | ESM2 | ESU2 | 3756.5 | 3759.75 | 0.087 | Tuesday |
| 2022-09-13 20:00 EDT | ESU2 | ESZ2 | 3939.5 | 3958.5 | 0.482 | Tuesday |
| 2022-12-13 19:00 EST | ESZ2 | ESH3 | 4022.0 | 4055.5 | 0.833 | Tuesday |
| 2023-03-14 20:00 EDT | ESH3 | ESM3 | 3919.25 | 3952.25 | 0.842 | Tuesday |
| 2023-06-13 20:00 EDT | ESM3 | ESU3 | 4371.75 | 4417.0 | 1.035 | Tuesday |
| 2023-09-12 20:00 EDT | ESU3 | ESZ3 | 4465.25 | 4514.0 | 1.092 | Tuesday |
| 2023-12-12 19:00 EST | ESZ3 | ESH4 | 4652.0 | 4704.0 | 1.118 | Tuesday |
| 2024-03-12 20:00 EDT | ESH4 | ESM4 | 5179.5 | 5242.75 | 1.221 | Tuesday |
| 2024-06-18 20:00 EDT | ESM4 | ESU4 | 5495.5 | 5564.75 | 1.26 | Tuesday |
| 2024-09-17 20:00 EDT | ESU4 | ESZ4 | 5644.25 | 5705.75 | 1.09 | Tuesday |
| 2024-12-17 19:00 EST | ESZ4 | ESH5 | 6049.75 | 6123.75 | 1.223 | Tuesday |
| 2025-03-18 20:00 EDT | ESH5 | ESM5 | 5621.25 | 5672.5 | 0.912 | Tuesday |
| 2025-06-17 20:00 EDT | ESM5 | ESU5 | 5971.0 | 6024.75 | 0.9 | Tuesday |
| 2025-09-16 20:00 EDT | ESU5 | ESZ5 | 6615.25 | 6672.25 | 0.862 | Tuesday |
| 2025-12-16 19:00 EST | ESZ5 | ESH6 | 6790.25 | 6845.25 | 0.81 | Tuesday |
| 2026-03-17 20:00 EDT | ESH6 | ESM6 | 6714.75 | 6766.25 | 0.767 | Tuesday |
| 2026-06-16 20:00 EDT | ESM6 | ESU6 | 7523.75 | 7592.0 | 0.907 | Tuesday |

Rolls hacia un contrato 'anterior' (ida y vuelta): 0
Rolls que ocurren un lunes/domingo-noche (OI se evalúa al cierre del viernes): 0 de 65

## 6. Contraste con Yahoo ES=F diario (es_daily.csv)

- Días comunes: 4,074 (2010-06-07 → 2026-08-19)
- Correlación de retornos diarios (cierre 17:00 ET Databento vs cierre Yahoo): **0.8371**
- Correlación con Yahoo desplazado +1 día: -0.0484; −1 día: 0.0278
- |close_db/close_yh − 1|: mediana 0.054 %, p95 0.892 %, máx 7.034 %
- Volumen: mediana (vol_db / vol_yh) = 0.966

Correlación de retornos diarios y diferencia de cierre por año (muestra desde cuándo el intradía es usable):

| año | n | corr | mediana_|dif_close|_% | p95_|dif_close|_% |
|---|---|---|---|---|
| 2010 | 146 | 0.3185 | 0.1708 | 1.9629 |
| 2011 | 252 | 0.3203 | 0.1322 | 2.6636 |
| 2012 | 250 | 0.6347 | 0.0704 | 1.3198 |
| 2013 | 252 | 0.8464 | 0.0487 | 0.5267 |
| 2014 | 249 | 0.7974 | 0.0486 | 0.7133 |
| 2015 | 252 | 0.8628 | 0.0615 | 0.7904 |
| 2016 | 250 | 0.9798 | 0.0459 | 0.337 |
| 2017 | 251 | 0.9721 | 0.0307 | 0.1205 |
| 2018 | 251 | 0.9784 | 0.0376 | 0.2527 |
| 2019 | 252 | 0.9736 | 0.041 | 0.2055 |
| 2020 | 253 | 0.9442 | 0.0697 | 0.5408 |
| 2021 | 252 | 0.9671 | 0.0639 | 0.2901 |
| 2022 | 251 | 0.9671 | 0.1104 | 0.618 |
| 2023 | 251 | 0.9487 | 0.0577 | 0.4058 |
| 2024 | 252 | 0.9046 | 0.0578 | 0.6026 |
| 2025 | 252 | 0.955 | 0.0548 | 0.5934 |
| 2026 | 158 | 0.9608 | 0.0688 | 0.3801 |

Mayores diferencias de cierre (candidatos: roll en fechas distintas entre proveedores):

| día | close_db | close_yh | dif_% | symbol_db |
|---|---|---|---|---|
| 2020-03-20 | 2266.5 | 2437.97998046875 | -7.034 | ESM0 |
| 2011-08-09 | 1103.25 | 1171.75 | -5.846 | ESU1 |
| 2011-08-04 | 1257.75 | 1198.75 | 4.922 | ESU1 |
| 2011-08-10 | 1172.0 | 1123.5 | 4.317 | ESU1 |
| 2011-11-30 | 1192.5 | 1246.0 | -4.294 | ESZ1 |
| 2011-11-09 | 1272.75 | 1225.75 | 3.834 | ESZ1 |
| 2011-08-18 | 1187.25 | 1143.5 | 3.826 | ESU1 |
| 2011-09-21 | 1199.75 | 1155.75 | 3.807 | ESZ1 |
| 2010-06-29 | 1073.75 | 1035.25 | 3.719 | ESU0 |
| 2011-08-11 | 1127.0 | 1168.5 | -3.552 | ESU1 |
| 2010-07-07 | 1022.0 | 1059.25 | -3.517 | ESU0 |
| 2020-06-19 | 3057.75 | 3161.260009765625 | -3.274 | ESU0 |
| 2011-08-23 | 1121.25 | 1158.5 | -3.215 | ESU1 |
| 2011-10-27 | 1242.75 | 1282.5 | -3.099 | ESZ1 |
| 2011-09-22 | 1156.75 | 1123.5 | 2.96 | ESZ1 |

- Días de negociación en Databento sin fila en Yahoo: 109 — primeros 30: 2010-07-05, 2010-09-06, 2010-11-25, 2010-12-24, 2011-01-17, 2011-02-21, 2011-04-22, 2011-05-30, 2011-07-04, 2011-09-05, 2011-11-24, 2012-01-16, 2012-02-20, 2012-04-06, 2012-05-28, 2012-07-04, 2012-07-21, 2012-09-03, 2012-10-29, 2012-10-30, 2012-11-22, 2013-07-04, 2013-11-28, 2014-05-26, 2014-07-04, 2014-09-01, 2014-11-27, 2014-12-25, 2015-01-19, 2015-02-16
- Fechas en Yahoo (dentro del rango) sin día en Databento: 3 — primeros 30: 2014-06-13, 2014-09-24, 2014-09-25
