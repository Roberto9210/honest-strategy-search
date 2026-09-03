# Resultado — Terreno por duración de tenencia: cuánto baja el daño cuando la tenencia es más corta

**Ejecuta `terreno_tenencia_preregistro.md` (`63797ee`, solo).** Salida cruda en `terreno_tenencia.txt`,
commiteada antes de este archivo. Una corrida. **ES a 1 minuto de Databento, 2016-01-04 → 2019-12-31.**

> **Antes del primer número, las limitaciones del pre-registro, sin ablandar:** esto es **ES, no MES**.
> Son libros separados que no comparten OHLC (Ventana A). **Lo medido es el terreno de ES; su
> traslado a MES es un supuesto.** Los «USD de MES» son puntos de ES × 5. Y una tenencia de horario
> fijo **no es una estrategia**: es otra tenencia pasiva, más corta. No se miró si alguna gana.

---

## 1 · EL CONTROL — PASA, y más de lo que el criterio pedía

Población: **828 fechas comunes** (2016-08-23 → 2019-12-31, desde donde empieza el diario del
guardián), un solo contrato, no `degraded`, con barra a las 17:00 CT, y con barra diaria de ES en NT8
bajo la regla de máximo volumen sin cambio de contrato.

| lado | fuente | p50 | p90 | p95 | p99 | máx |
|---|---|---|---|---|---|---|
| largo | Databento, minutos → 17:00→16:00 | 8,50 | 34,98 | 51,82 | 90,85 | 161,25 |
| largo | NT8 diario, mismas fechas | 8,50 | 34,98 | 51,82 | 90,85 | 161,25 |
| corto | Databento, minutos → 17:00→16:00 | 10,50 | 30,25 | 40,66 | 60,39 | 129,25 |
| corto | NT8 diario, mismas fechas | 10,50 | 30,25 | 40,66 | 60,39 | 129,25 |

**Diferencia relativa: 0,00 % en los cinco percentiles, los dos lados.** Criterio pre-registrado:
PASA con menos del 5 %.

Por fecha, lado largo, 820 fechas con excursión NT8 > 0: mediana de la razón **1,0000** (p10 y p90
también 1,0000), **807 fechas dentro de un tick (98,4 %)**, 816 dentro de 2 puntos (99,5 %),
correlación 0,9998.

**Lo que esto dice:** dos proveedores que no se conocen —Databento desde el feed de CME, NT8 desde su
servidor histórico— reconstruyen la **misma** barra diaria a partir de la sesión 17:00 → 16:00 CT.
Eso confirma por segunda vía, y ahora sobre **828 barras históricas**, lo que el guardián había
medido sobre **una** barra escrita el 2026-09-02: la barra diaria de NT8 **es** la sesión ETH que
arranca a las 17:00 CT del día anterior. Ese punto pasa de «esperable, NO VERIFICADO» a **VERIFICADO
para 2016-08 → 2019-12** en la raíz ES. Para MES y para 2020+ sigue sin verificar.

**Las 13 fechas que no coinciden al tick**, con las 8 peores impresas en la salida: una sola es grande
(2016-11-16: Databento 10,25, NT8 0,75). Las demás difieren 1–4 puntos y se agrupan en días de roll
(2016-12, 2018-12, 2019-09), donde el contrato de máximo volumen de NT8 y el front por open interest
de Databento pueden no ser el mismo. **No se resolvió cuál tiene razón; se deja nombrado.**

## 2 · LA ESCALERA — P-escalera, 971 sesiones

Población: P-base (1.005) menos 1 sesión sin barra exacta a las 08:30 CT y **33 con cierre
anticipado** (sin barra a las 14:59 CT). Las cuatro ventanas se calculan sobre exactamente estas 971.

### Lado largo (`open − min(low)`)

| ventana | p50 | p90 | p95 | p99 | máx | p50 USD MES | p95 USD MES | p99 USD MES | > 1.000 USD MES |
|---|---|---|---|---|---|---|---|---|---|
| **T23** 17:00→16:00 | 8,75 | 34,25 | 51,12 | 89,02 | 161,25 | 44 | 256 | 445 | **0,00 %** |
| **RTH** 08:30→15:00 | 7,50 | 27,75 | 38,62 | 70,30 | 105,00 | 38 | 193 | 351 | 0,00 % |
| **H1** 08:30→09:30 | 4,00 | 12,75 | 16,88 | 24,07 | 36,75 | 20 | 84 | 120 | 0,00 % |
| **M15** 08:30→08:45 | 2,50 | 6,75 | 9,00 | 12,75 | 21,00 | 12 | 45 | 64 | 0,00 % |

### Lado corto (`max(high) − open`)

| ventana | p50 | p90 | p95 | p99 | máx | p50 USD MES | p95 USD MES | p99 USD MES | > 1.000 USD MES |
|---|---|---|---|---|---|---|---|---|---|
| **T23** | 10,25 | 30,25 | 40,25 | 57,87 | 129,25 | 51 | 201 | 289 | **0,00 %** |
| **RTH** | 7,50 | 22,50 | 31,88 | 50,35 | 100,25 | 38 | 159 | 252 | 0,00 % |
| **H1** | 4,00 | 11,25 | 14,88 | 27,42 | 79,00 | 20 | 74 | 137 | 0,00 % |
| **M15** | 2,50 | 6,75 | 8,75 | 15,57 | 49,25 | 12 | 44 | 78 | 0,00 % |

**El «> 1.000 USD con un contrato de MES» da 0,00 % en las cuatro ventanas**, y no por poca muestra:
en 2016–2019 la excursión máxima de una sesión entera de ES fue **161 puntos = 806 USD de MES**. Ese
umbral no se tocó ni una vez en cuatro años. El guardián midió 0,54 % de días sobre MES en
2019-05 → 2026-08, que incluye 2020 y 2022. **Es el período, no la ventana**: la mediana de T23 acá
(8,75) es la mitad de la publicada por el guardián para ES en 2016–2026 (17,50). Lo que mide esta
escalera son **razones dentro del mismo período**, y ésas son la respuesta; los niveles absolutos son
los de 2016–2019.

## 3 · LA TABLA — cuánto compra acortar la exposición

Caída de cada percentil respecto de la tenencia de 23 horas, `1 − percentil_ventana / percentil_T23`.

| ventana | duración | caída p50 | caída p90 | caída p95 | caída p99 |
|---|---|---|---|---|---|
| **lado largo** | | | | | |
| RTH 08:30→15:00 | 6,5 h (28 % de T23) | 14,3 % | 19,0 % | **24,4 %** | 21,0 % |
| H1 08:30→09:30 | 1 h (4 %) | 54,3 % | 62,8 % | **67,0 %** | 73,0 % |
| M15 08:30→08:45 | 15 min (1 %) | 71,4 % | 80,3 % | **82,4 %** | 85,7 % |
| **lado corto** | | | | | |
| RTH | 6,5 h | 26,8 % | 25,6 % | **20,8 %** | 13,0 % |
| H1 | 1 h | 61,0 % | 62,8 % | **63,0 %** | 52,6 % |
| M15 | 15 min | 75,6 % | 77,7 % | **78,3 %** | 73,1 % |

**Lo que la columna dice:**

1. **Sacar la noche compra poco.** Pasar de 23 horas a la rueda de Nueva York recorta la excursión
   un 13–27 % según percentil y lado, con un 72 % menos de tiempo expuesto. La rueda concentra tres
   cuartos del daño.
2. **Acortar dentro de la rueda compra mucho menos que proporcional.** La primera hora es el 4 % del
   tiempo de T23 y retiene un tercio de la excursión (p95: 16,9 contra 51,1). Los quince minutos son
   el 1 % del tiempo y retienen casi un quinto (p95: 9,0 contra 51,1). Es la forma en U de la
   volatilidad intradía, la misma regularidad pública de H1: **la apertura es la hora más cara por
   minuto**. Una tenencia corta que empieza a las 08:30 está parada exactamente ahí.
3. **El lado corto se acorta menos en la cola.** En p99 la rueda recorta 13 % contra 21 % del largo,
   y la primera hora 53 % contra 73 %. El máximo de la primera hora en corto (79 puntos) es más del
   doble que en largo (36,75): las subas violentas de apertura son más grandes que las bajas, en
   este período.

## 4 · Lo que esta medición NO dice — repetido del pre-registro

- **No dice si existe una ventaja. No buscó ninguna.** No se miró si alguna ventana es rentable.
- **No dice nada de MES.** Dice de ES. El traslado a MES es un supuesto; Ventana A vio 8 puntos de
  diferencia de apertura entre los dos el mismo día.
- **Una tenencia de horario fijo no es una estrategia**, y un percentil de excursión no es un stop:
  es lo que una tenencia pasiva aguanta sin salir.
- **Es 2016–2019.** Un período con la mitad de la excursión mediana del período completo. Las
  razones son del período; los niveles también.
- **La excursión es exacta sólo para una entrada en la apertura de la ventana.** No secuencia el
  camino: sólo mínimo y máximo.
- **Sin comisiones ni deslizamiento.**
