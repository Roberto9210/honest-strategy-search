# Informe de calidad de datos — deadman-search/data

Generado: 2026-08-19 14:24 EDT. Fuente: Yahoo Finance vía yfinance 1.6.0 (`Ticker.history`, `auto_adjust=False`, sin pre/post market). Nada se corrigió: lo que sigue es lo que vino del proveedor.

Criterios: hueco = más de 3 días hábiles (lun–vie, sin calendario de festivos) faltantes entre filas consecutivas; salto = |variación de cierre a cierre| > 20 % entre filas consecutivas (y aparte |apertura vs cierre previo| > 20 %); precio absurdo = high < low, precio ≤ 0, o high/low incoherentes con open/close.

## 1. Resumen por archivo

| archivo | símbolo | intervalo | filas | desde | hasta | días distintos |
|---|---|---|---|---|---|---|
| es_daily.csv | ES=F | 1d | 6544 | 2000-09-18 | 2026-08-19 | 6544 |
| es_1h.csv | ES=F | 1h | 13695 | 2024-03-27 00:00 EDT | 2026-08-19 14:00 EDT | 725 |
| es_5m.csv | ES=F | 5m | 13728 | 2026-06-09 00:05 EDT | 2026-08-19 14:10 EDT | 60 |
| spy_daily.csv | SPY | 1d | 8446 | 1993-01-29 | 2026-08-19 | 8446 |

Notas de contexto (no son errores, pero condicionan cualquier uso):
- `ES=F` en Yahoo es el **front-month continuo sin ajustar por roll**: en los cambios de contrato (mar/jun/sep/dic) puede haber escalones de precio que no son movimiento de mercado.
- La última fila de cada archivo corresponde a la sesión del día de descarga y puede estar **incompleta** (descarga hecha a las 14:24 EDT).
- Las marcas temporales intradía están en hora de Nueva York (offset incluido en el CSV). El día 'date' de los diarios de ES lo asigna Yahoo; la convención de sesión (18:00–17:00 ET) se contrasta abajo con la correlación ES/SPY a distintos lags.
- SPY es precio **sin ajustar** por dividendos/splits (`auto_adjust=False`).

## 2. Detalle por archivo

### es_daily.csv (ES=F, 1d)

- Filas: **6544**; rango: 2000-09-18 → 2026-08-19
- Índice monótono creciente: sí; timestamps duplicados: 0
- Filas con NaN en OHLC: 0; NaN en volumen: 0
- Mayor |retorno| cierre-a-cierre entre filas consecutivas: 14.11 % (en 2008-10-13)

**Huecos > 3 días hábiles entre filas consecutivas: 0**

_(ninguna)_

**Días con volumen cero: 11**

| date | open | high | low | close | volume |
|---|---|---|---|---|---|
| 2001-09-11 00:00:00 | 1096.25 | 1103.0 | 1068.0 | 1095.75 | 0 |
| 2003-08-29 00:00:00 | 1001.25 | 1009.25 | 999.0 | 1007.75 | 0 |
| 2015-09-16 00:00:00 | 1979.75 | 1999.0 | 1972.75 | 1998.25 | 0 |
| 2015-09-17 00:00:00 | 1997.0 | 2021.5 | 1982.5 | 1987.75 | 0 |
| 2018-02-23 00:00:00 | 2712.75 | 2750.25 | 2710.0 | 2748.75 | 0 |
| 2025-06-05 00:00:00 | 5974.25 | 6016.5 | 5928.75 | 5946.0 | 0 |
| 2025-06-18 00:00:00 | 5977.25 | 6020.75 | 5964.75 | 5981.5 | 0 |
| 2025-07-03 00:00:00 | 6276.5 | 6333.25 | 6270.5 | 6324.25 | 0 |
| 2025-07-04 00:00:00 | 6320.75 | 6322.75 | 6276.5 | 6283.5 | 0 |
| 2025-08-29 00:00:00 | 6516.0 | 6518.0 | 6455.5 | 6472.75 | 0 |
| 2025-11-03 00:00:00 | 6878.0 | 6909.5 | 6849.5 | 6882.75 | 0 |

**high < low: 0**

**Precio ≤ 0: 0**

**OHLC incoherente (high < open/close o low > open/close, con high ≥ low): 10**

| date | open | high | low | close | volume | tercer_viernes_trimestral |
|---|---|---|---|---|---|---|
| 2002-01-31 00:00:00 | 1115.5 | 1130.0 | 1113.0 | 1130.5 | 232762 | False |
| 2004-03-19 00:00:00 | 1124.75 | 1128.0 | 1122.0 | 1120.1800537109375 | 649991 | True |
| 2004-12-17 00:00:00 | 1203.5 | 1206.75 | 1193.5 | 1190.449951171875 | 821953 | True |
| 2005-06-17 00:00:00 | 1210.5 | 1217.5 | 1210.0 | 1222.6800537109375 | 802869 | True |
| 2006-03-17 00:00:00 | 1303.5 | 1309.0 | 1303.5 | 1310.1600341796875 | 603136 | True |
| 2007-09-21 00:00:00 | 1519.75 | 1532.25 | 1516.5 | 1533.3800048828125 | 1346720 | True |
| 2008-03-18 00:00:00 | 1279.75 | 1292.5 | 1278.0 | 1332.5 | 753289 | False |
| 2008-09-19 00:00:00 | 1201.0 | 1263.0 | 1197.25 | 1279.31005859375 | 4007416 | True |
| 2010-03-19 00:00:00 | 1166.25 | 1170.0 | 1164.75 | 1172.949951171875 | 2165925 | True |
| 2011-09-16 00:00:00 | 1210.0 | 1216.0 | 1201.5 | 1216.739990234375 | 2661191 | True |

**Saltos |cierre/cierre previo − 1| > 20 %: 0**

**Saltos |apertura/cierre previo − 1| > 20 %: 0**

**Filas fechadas en sábado/domingo: 0**

Distribución de |retorno diario| (informativo): >5 %: 41 días, >10 %: 3 días. Top 10 por magnitud:

| fecha | retorno | close |
|---|---|---|
| 2008-10-13 | +14.11 % | 1016.75 |
| 2008-10-28 | +12.46 % | 938.75 |
| 2020-03-16 | -10.38 % | 2416.25 |
| 2020-03-12 | -9.90 % | 2469.0 |
| 2008-10-15 | -9.88 % | 903.25 |
| 2020-03-24 | +9.80 % | 2438.0 |
| 2025-04-09 | +9.38 % | 5491.0 |
| 2020-03-13 | +9.19 % | 2696.0 |
| 2020-03-23 | -8.92 % | 2220.5 |
| 2008-12-01 | -8.88 % | 815.75 |

### es_1h.csv (ES=F, 1h)

- Filas: **13695**; rango: 2024-03-27 00:00 EDT → 2026-08-19 14:00 EDT
- Índice monótono creciente: sí; timestamps duplicados: 0
- Filas con NaN en OHLC: 0; NaN en volumen: 0
- Mayor |retorno| cierre-a-cierre entre filas consecutivas: 6.73 % (en 2025-04-09 13:00 EDT)

**Huecos > 3 días hábiles entre filas consecutivas: 0**

_(ninguna)_

Huecos intradía mayores que el intervalo nominal (0 days 01:00:00): 623 en total (incluye el corte diario 17:00–18:00 ET y los fines de semana, que son normales). Los 15 mayores:

| desde | hasta | hueco |
|---|---|---|
| 2025-08-29 16:00 EDT | 2025-09-02 00:00 EDT | 3 days 08:00:00 |
| 2026-05-22 16:00 EDT | 2026-05-26 00:00 EDT | 3 days 08:00:00 |
| 2026-01-30 10:00 EST | 2026-02-02 13:00 EST | 3 days 03:00:00 |
| 2025-04-17 16:00 EDT | 2025-04-20 18:00 EDT | 3 days 02:00:00 |
| 2024-03-28 16:00 EDT | 2024-03-31 18:00 EDT | 3 days 02:00:00 |
| 2026-07-02 23:00 EDT | 2026-07-05 18:00 EDT | 2 days 19:00:00 |
| 2026-04-02 23:00 EDT | 2026-04-05 18:00 EDT | 2 days 19:00:00 |
| 2026-06-18 23:00 EDT | 2026-06-21 18:00 EDT | 2 days 19:00:00 |
| 2026-05-01 16:00 EDT | 2026-05-04 00:00 EDT | 2 days 08:00:00 |
| 2025-07-11 16:00 EDT | 2025-07-14 00:00 EDT | 2 days 08:00:00 |
| 2026-01-16 16:00 EST | 2026-01-18 23:00 EST | 2 days 07:00:00 |
| 2025-07-04 12:00 EDT | 2025-07-06 18:00 EDT | 2 days 06:00:00 |
| 2024-11-29 12:30 EST | 2024-12-01 18:00 EST | 2 days 05:30:00 |
| 2025-11-28 12:30 EST | 2025-11-30 18:00 EST | 2 days 05:30:00 |
| 2025-07-25 16:00 EDT | 2025-07-27 20:00 EDT | 2 days 04:00:00 |

Barras por día calendario: mediana 23, mín 1 (2026-01-18), máx 24 (2024-07-09); días con menos de la mitad de la mediana: 133

| día | barras |
|---|---|
| 2024-03-31 | 6 |
| 2024-04-07 | 6 |
| 2024-04-14 | 6 |
| 2024-04-21 | 6 |
| 2024-04-28 | 6 |
| 2024-05-05 | 6 |
| 2024-05-12 | 6 |
| 2024-05-19 | 6 |
| 2024-05-26 | 6 |
| 2024-06-02 | 6 |
| 2024-06-09 | 6 |
| 2024-06-16 | 6 |
| 2024-06-21 | 11 |
| 2024-06-23 | 6 |
| 2024-06-30 | 6 |
| 2024-07-03 | 4 |
| 2024-07-07 | 6 |
| 2024-07-14 | 6 |
| 2024-07-21 | 6 |
| 2024-07-28 | 6 |
| 2024-08-04 | 6 |
| 2024-08-11 | 6 |
| 2024-08-18 | 6 |
| 2024-08-25 | 6 |
| 2024-09-01 | 6 |
| 2024-09-08 | 6 |
| 2024-09-15 | 6 |
| 2024-09-20 | 11 |
| 2024-09-22 | 6 |
| 2024-09-29 | 6 |

_(mostrando 30 de 133)_

**Barras con volumen cero: 490** (3.58 % de las filas), repartidas en 480 días. Por hora del día (ET), las barras con volumen 0:

| hora_ET | barras_vol0 |
|---|---|
| 0 | 3 |
| 1 | 1 |
| 6 | 1 |
| 9 | 3 |
| 12 | 2 |
| 14 | 1 |
| 16 | 6 |
| 18 | 471 |
| 20 | 1 |
| 23 | 1 |

Días con más barras a volumen 0:

| día | barras_vol0 |
|---|---|
| 2025-12-16 | 5 |
| 2025-12-17 | 4 |
| 2025-07-14 | 2 |
| 2026-05-04 | 2 |
| 2024-03-27 | 2 |
| 2026-07-08 | 1 |
| 2026-07-09 | 1 |
| 2026-07-13 | 1 |
| 2026-07-14 | 1 |
| 2026-07-15 | 1 |
| 2026-07-16 | 1 |
| 2026-07-17 | 1 |
| 2026-07-20 | 1 |
| 2026-07-21 | 1 |
| 2026-07-22 | 1 |

De ellas, dentro de la sesión regular de acciones (09:30–16:00 ET): **3**

| datetime | open | high | low | close | volume |
|---|---|---|---|---|---|
| 2025-06-19 12:00:00-04:00 | 5922.25 | 5935.0 | 5922.25 | 5926.0 | 0 |
| 2025-12-16 14:00:00-05:00 | 6846.5 | 6853.5 | 6771.0 | 6791.75 | 0 |
| 2025-12-17 12:00:00-05:00 | 6753.25 | 6815.0 | 6741.25 | 6749.25 | 0 |

**high < low: 0**

**Precio ≤ 0: 0**

**OHLC incoherente (high < open/close o low > open/close, con high ≥ low): 0**

**Saltos |cierre/cierre previo − 1| > 20 %: 0**

**Saltos |apertura/cierre previo − 1| > 20 %: 0**

### es_5m.csv (ES=F, 5m)

- Filas: **13728**; rango: 2026-06-09 00:05 EDT → 2026-08-19 14:10 EDT
- Índice monótono creciente: sí; timestamps duplicados: 0
- Filas con NaN en OHLC: 0; NaN en volumen: 0
- Mayor |retorno| cierre-a-cierre entre filas consecutivas: 0.89 % (en 2026-06-11 13:25 EDT)

**Huecos > 3 días hábiles entre filas consecutivas: 0**

_(ninguna)_

Huecos intradía mayores que el intervalo nominal (0 days 00:05:00): 97 en total (incluye el corte diario 17:00–18:00 ET y los fines de semana, que son normales). Los 15 mayores:

| desde | hasta | hueco |
|---|---|---|
| 2026-07-02 23:55 EDT | 2026-07-05 18:00 EDT | 2 days 18:05:00 |
| 2026-06-18 23:55 EDT | 2026-06-21 18:00 EDT | 2 days 18:05:00 |
| 2026-08-14 16:55 EDT | 2026-08-16 18:10 EDT | 2 days 01:15:00 |
| 2026-07-10 16:55 EDT | 2026-07-12 18:10 EDT | 2 days 01:15:00 |
| 2026-06-26 16:55 EDT | 2026-06-28 18:10 EDT | 2 days 01:15:00 |
| 2026-07-24 16:55 EDT | 2026-07-26 18:10 EDT | 2 days 01:15:00 |
| 2026-08-07 16:55 EDT | 2026-08-09 18:10 EDT | 2 days 01:15:00 |
| 2026-06-12 16:55 EDT | 2026-06-14 18:10 EDT | 2 days 01:15:00 |
| 2026-07-17 16:55 EDT | 2026-07-19 18:10 EDT | 2 days 01:15:00 |
| 2026-07-31 16:55 EDT | 2026-08-02 18:10 EDT | 2 days 01:15:00 |
| 2026-07-17 01:05 EDT | 2026-07-17 05:10 EDT | 0 days 04:05:00 |
| 2026-07-09 16:55 EDT | 2026-07-09 18:00 EDT | 0 days 01:05:00 |
| 2026-08-05 16:55 EDT | 2026-08-05 18:00 EDT | 0 days 01:05:00 |
| 2026-07-14 16:55 EDT | 2026-07-14 18:00 EDT | 0 days 01:05:00 |
| 2026-07-08 16:55 EDT | 2026-07-08 18:00 EDT | 0 days 01:05:00 |

Barras por día calendario: mediana 275, mín 70 (2026-06-14), máx 276 (2026-06-15); días con menos de la mitad de la mediana: 10

| día | barras |
|---|---|
| 2026-06-14 | 70 |
| 2026-06-21 | 72 |
| 2026-06-28 | 70 |
| 2026-07-05 | 72 |
| 2026-07-12 | 70 |
| 2026-07-19 | 70 |
| 2026-07-26 | 70 |
| 2026-08-02 | 70 |
| 2026-08-09 | 70 |
| 2026-08-16 | 70 |

**Barras con volumen cero: 46** (0.34 % de las filas), repartidas en 45 días. Por hora del día (ET), las barras con volumen 0:

| hora_ET | barras_vol0 |
|---|---|
| 0 | 2 |
| 16 | 3 |
| 18 | 41 |

Días con más barras a volumen 0:

| día | barras_vol0 |
|---|---|
| 2026-06-09 | 2 |
| 2026-06-10 | 1 |
| 2026-06-11 | 1 |
| 2026-06-15 | 1 |
| 2026-06-16 | 1 |
| 2026-06-17 | 1 |
| 2026-06-18 | 1 |
| 2026-06-22 | 1 |
| 2026-06-23 | 1 |
| 2026-06-24 | 1 |
| 2026-06-25 | 1 |
| 2026-06-29 | 1 |
| 2026-06-30 | 1 |
| 2026-07-01 | 1 |
| 2026-07-02 | 1 |

De ellas, dentro de la sesión regular de acciones (09:30–16:00 ET): **0**

**high < low: 0**

**Precio ≤ 0: 0**

**OHLC incoherente (high < open/close o low > open/close, con high ≥ low): 0**

**Saltos |cierre/cierre previo − 1| > 20 %: 0**

**Saltos |apertura/cierre previo − 1| > 20 %: 0**

### spy_daily.csv (SPY, 1d)

- Filas: **8446**; rango: 1993-01-29 → 2026-08-19
- Índice monótono creciente: sí; timestamps duplicados: 0
- Filas con NaN en OHLC: 0; NaN en volumen: 0
- Mayor |retorno| cierre-a-cierre entre filas consecutivas: 14.52 % (en 2008-10-13)

**Huecos > 3 días hábiles entre filas consecutivas: 1**

| desde | hasta | dias_calendario | dias_habiles_faltantes |
|---|---|---|---|
| 2001-09-10 | 2001-09-17 | 7 | 4 |

**Días con volumen cero: 0**

_(ninguna)_

**high < low: 0**

**Precio ≤ 0: 0**

**OHLC incoherente (high < open/close o low > open/close, con high ≥ low): 0**

**Saltos |cierre/cierre previo − 1| > 20 %: 0**

**Saltos |apertura/cierre previo − 1| > 20 %: 0**

**Filas fechadas en sábado/domingo: 0**

Distribución de |retorno diario| (informativo): >5 %: 44 días, >10 %: 4 días. Top 10 por magnitud:

| fecha | retorno | close |
|---|---|---|
| 2008-10-13 | +14.52 % | 101.3499984741211 |
| 2008-10-28 | +11.69 % | 93.76000213623048 |
| 2020-03-16 | -10.94 % | 239.8500061035156 |
| 2025-04-09 | +10.50 % | 548.6199951171875 |
| 2008-10-15 | -9.84 % | 90.0199966430664 |
| 2020-03-12 | -9.57 % | 248.1100006103516 |
| 2020-03-24 | +9.06 % | 243.1499938964844 |
| 2008-12-01 | -8.86 % | 82.11000061035156 |
| 2020-03-13 | +8.55 % | 269.32000732421875 |
| 2008-09-29 | -7.84 % | 111.37999725341795 |

## 3. Correlación de retornos diarios ES vs SPY

- Fechas comunes con retorno en ambos: **6515** (2000-09-19 → 2026-08-19)
- Fechas en ES sin SPY: 28; fechas en SPY sin ES (dentro del rango de ES): 2
  - ES sin SPY (primeras 30): 2001-09-11, 2002-02-18, 2002-05-27, 2002-07-04, 2002-09-02, 2002-11-28, 2003-01-20, 2003-02-17, 2003-05-26, 2003-09-01, 2003-11-27, 2004-01-19, 2004-02-16, 2004-05-31, 2004-06-11, 2004-07-05, 2004-09-06, 2004-11-25, 2005-11-24, 2006-01-16, 2006-02-20, 2006-05-29, 2006-07-04, 2006-09-04, 2006-11-23, 2023-11-23, 2025-01-09, 2025-07-04
  - SPY sin ES, dentro del rango de ES (primeras 30): 2016-10-10, 2016-11-11

- **Pearson, mismo día: 0.9762**
- ES(t) vs SPY(t+1): -0.0872; ES(t) vs SPY(t−1): -0.0683 (si alguno de los lags superara al contemporáneo, la fecha de las velas de ES estaría desplazada).
- Spearman, mismo día: 0.9740
- Desv. típica diaria: ES 1.218 %, SPY 1.209 %; std de la diferencia (ES−SPY): 0.265 %

Por año (mismo día):

| año | n | corr |
|---|---|---|
| 2000 | 72 | 0.954 |
| 2001 | 248 | 0.9636 |
| 2002 | 252 | 0.9949 |
| 2003 | 252 | 0.9862 |
| 2004 | 252 | 0.9785 |
| 2005 | 252 | 0.9751 |
| 2006 | 251 | 0.9766 |
| 2007 | 251 | 0.9879 |
| 2008 | 253 | 0.9901 |
| 2009 | 252 | 0.9645 |
| 2010 | 252 | 0.9788 |
| 2011 | 252 | 0.9834 |
| 2012 | 250 | 0.9713 |
| 2013 | 252 | 0.9631 |
| 2014 | 252 | 0.9629 |
| 2015 | 252 | 0.9644 |
| 2016 | 250 | 0.9768 |
| 2017 | 251 | 0.9677 |
| 2018 | 251 | 0.9611 |
| 2019 | 252 | 0.9818 |
| 2020 | 253 | 0.9487 |
| 2021 | 252 | 0.9857 |
| 2022 | 251 | 0.997 |
| 2023 | 250 | 0.9759 |
| 2024 | 252 | 0.9554 |
| 2025 | 250 | 0.9865 |
| 2026 | 158 | 0.9843 |

Mayores divergencias diarias |ES − SPY| (informativo; candidatos a roll de contrato, festivo parcial o sesión desalineada):

| fecha | ret_ES | ret_SPY | |dif| |
|---|---|---|---|
| 2020-03-23 | -8.92 % | -2.56 % | 6.36 % |
| 2020-03-20 | +1.45 % | -4.87 % | 6.31 % |
| 2001-09-24 | +7.21 % | +3.52 % | 3.69 % |
| 2009-03-23 | +3.53 % | +7.18 % | 3.65 % |
| 2009-03-20 | +0.66 % | -2.82 % | 3.48 % |
| 2008-09-19 | +6.76 % | +3.37 % | 3.39 % |
| 2008-09-22 | -5.12 % | -2.26 % | 2.86 % |
| 2024-12-23 | +3.35 % | +0.60 % | 2.75 % |
| 2020-06-19 | +1.68 % | -1.01 % | 2.69 % |
| 2001-09-21 | -4.11 % | -1.45 % | 2.66 % |
| 2018-12-24 | -5.11 % | -2.64 % | 2.46 % |
| 2015-12-18 | -0.09 % | -2.36 % | 2.28 % |
| 2020-06-22 | -1.60 % | +0.64 % | 2.24 % |
| 2000-12-15 | -0.37 % | -2.56 % | 2.18 % |
| 2001-03-16 | -0.13 % | -2.27 % | 2.14 % |
