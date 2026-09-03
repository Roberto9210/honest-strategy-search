# Resultado — Terreno del stop: el stop compra cola y no mediana, el mercado nunca salta el stop entre barras pero sí adentro de la barra, y la hora barata es la misma

**Ejecuta `terreno_stop_preregistro.md` + Enmiendas 1 y 2** (`50c0cf8`, `166e091`, `9665573`, cada una
sola). Salida cruda en `terreno_stop.txt`, commiteada antes de este archivo. **ES a 1 minuto de
Databento, 2016–2019, P-escalera de 971 sesiones.** Tercera corrida: las dos primeras pararon en el
control por umbrales que escribí a mano, no por el cálculo; las enmiendas lo documentan y ninguna cifra
de las salidas 1 a 4 se vio antes de esta corrida.

> **Limitaciones, antes del primer número:** es **ES, no MES**. **Un stop real se ejecuta con
> deslizamiento y esto no lo modela**: el exceso del punto 3 es la cota del deslizamiento **por
> movimiento del mercado entre barras de minuto, no por profundidad del libro**. **Entrar siempre del
> mismo lado no es una estrategia**, y la cuenta del punto 4 **no cuenta ninguna ganancia**: es un piso
> de terreno. Los niveles son de 2016–2019, un régimen la mitad de violento que 2016–2026.

---

## 1 · EL CONTROL — da distinto, y los dos números lado a lado

Con D = 60, por ventana y lado: frecuencia de toque contra la fracción de sesiones con excursión ≥ 60
calculada por otro camino (`window_stats`), y la suma de 20 sesiones con stop contra sin stop.

| ventana | lado | toque D=60 | excursión ≥ 60 | banda que implican p95/p99 | con stop 60: p50 / p95 | sin stop: p50 / p95 | dif |
|---|---|---|---|---|---|---|---|
| T23 | largo | 3,09 % | 3,09 % | 1–5 % (p95 51,1 < 60 < p99 89,0) | 86,1 / 369,6 | 83,8 / 352,8 | +2,8 % / +4,8 % |
| T23 | corto | 0,93 % | 0,93 % | < 1 % (p99 57,9 < 60) | 142,5 / 281,4 | 142,5 / 295,3 | 0,0 % / −4,7 % |
| RTH | largo | 1,75 % | 1,75 % | 1–5 % | 74,4 / 307,4 | 74,4 / 318,7 | 0,0 % / −3,5 % |
| RTH | corto | 0,41 % | 0,41 % | < 1 % | 103,3 / 234,2 | 103,3 / 242,8 | 0,0 % / −3,5 % |
| H1, M15 | ambos | 0,00–0,21 % | idem | < 1 % | idénticos | idénticos | 0,0 % (H1 corto +2,7 %) |

**Ocho de ocho.** Con D = 60 casi nadie es sacado y la cuenta converge a la de sin stop. La primera
corrida ya mostraba estos mismos números; lo que falló dos veces fue el umbral escrito a mano («< 3 %»
para un lado cuyo p99 es 89, y luego la misma banda aplicada al lado cuyo p99 es 58). **Un umbral de
control se deriva del dato que ya se tiene, o no se pone.** Queda en las enmiendas.

## 2 · FRECUENCIA DE TOQUE — % de sesiones que tocan el stop antes del fin de la ventana

| ventana | lado | D=2 | D=4 | D=6 | D=8 | D=10 | D=15 | D=20 | D=30 |
|---|---|---|---|---|---|---|---|---|---|
| T23 | largo | 87,3 | 75,5 | 65,0 | 54,9 | 46,2 | 30,4 | 21,4 | 12,2 |
| T23 | corto | 90,6 | 81,5 | 70,5 | 60,6 | 51,8 | 34,1 | 22,2 | 10,3 |
| RTH | largo | 84,9 | 70,9 | 58,1 | 47,7 | 38,8 | 23,7 | 16,8 | 8,5 |
| RTH | corto | 86,1 | 73,0 | 60,0 | 47,4 | 38,0 | 22,3 | 14,2 | 5,7 |
| H1 | largo | 74,0 | 51,6 | 35,3 | 24,0 | 16,6 | 7,1 | 2,9 | 0,3 |
| H1 | corto | 72,3 | 51,3 | 33,4 | 21,3 | 13,4 | 5,0 | 2,5 | 0,7 |
| M15 | largo | 59,0 | 29,7 | 13,1 | 7,3 | 4,0 | 0,5 | 0,2 | 0,0 |
| M15 | corto | 60,1 | 30,2 | 14,1 | 6,4 | 3,8 | 1,2 | 0,3 | 0,1 |

**Un stop de 2 puntos (10 USD de MES) te saca 9 de cada 10 días si aguantás la sesión entera, y 6 de
cada 10 aunque sólo aguantes 15 minutos.** Para que un stop te saque menos de un día de cada cuatro en
la sesión entera hace falta D ≥ 20 (100 USD de MES); en la primera hora, D ≥ 8; en 15 minutos, D ≥ 4.

## 3 · POR HORA — ¿la hora barata para la excursión es la hora barata para que te saquen? **Sí, es la misma.**

Tenencia de una hora, % de sesiones que tocan, lado largo (corto en la salida cruda, igual de forma):

| hora de arranque CT | D=2 | D=4 | D=8 | D=15 | D=30 | razón exc. p50 vs 08:30 |
|---|---|---|---|---|---|---|
| **08:30 → 09:30, referencia** | 74,0 | 51,6 | 24,0 | 7,1 | 0,3 | 1,00 |
| 23:00 (la más barata) | 19,3 | 6,0 | 1,2 | 0,1 | 0,0 | 0,19 |
| 02:00 (Europa) | 51,2 | 22,9 | 6,3 | 0,8 | 0,0 | 0,50 |
| 07:00 | 48,1 | 21,2 | 5,3 | 0,8 | 0,3 | 0,44 |
| 09:00 (datos de las 10:00 ET) | 70,5 | 45,9 | 20,4 | **6,1** | **1,2** | 0,81 |
| 12:00 (la más barata de la rueda) | 56,3 | 30,1 | 10,3 | 3,6 | 0,3 | 0,56 |
| 14:00 (cierre de contado) | 65,6 | 39,2 | 15,0 | 4,5 | 1,0 | 0,69 |
| 15:00 (con el corte) | 38,2 | 15,3 | 3,0 | 0,9 | 0,1 | 0,38 |

**No hay hallazgo de horas distintas: el orden es el mismo.** La hora más barata para la excursión
típica (23:00 CT) es la hora en que menos te sacan a cualquier D, y la apertura es la peor a D chico.
Dos cosas sí cambian con el D, y las dos ya estaban en la cola de `terreno_horas`:

- **A D chico la hora pesa más que lo que la mediana de excursión decía.** A las 23:00 un stop de 8
  puntos te saca **20 veces menos** que en la apertura (1,2 % contra 24,0 %), mientras la excursión
  mediana es sólo 5 veces menor. La frecuencia de toque es más sensible a la hora que la mediana.
- **A D grande la hora de los datos de las 10:00 ET supera a la apertura.** Con D = 15, la hora de las
  09:00 CT saca al 6,1 % contra 7,1 % de la apertura, y con D = 30 saca al **1,2 % contra 0,3 %**: cuatro
  veces más. Es el p99 de 1,26 de la escalera por hora, visto desde el stop. **Un stop ancho a las 09:00
  CT te lo tocan más que a las 08:30.**

## 4 · LO QUE EL STOP DEJA PASAR — exceso sobre el stop, puntos de ES, sesiones que tocaron

**El salto en la apertura de la barra que toca es 0,00 en todos los percentiles y en el máximo, en las
cuatro ventanas y los dos lados** (una sola barra de 1,00 en las 23 horas juntas). **En ES a 1 minuto el
precio nunca «abre» más allá del stop: siempre lo cruza dentro de una barra.** Lo que se pasa, se pasa
adentro de la barra que toca, y en la siguiente.

| ventana | lado | D | n | misma barra p50 / p95 / p99 / máx | siguiente p50 / p95 / p99 / máx |
|---|---|---|---|---|---|
| T23 | largo | 4 | 733 | 0,25 / 2,10 / 5,43 / **31,25** | 0,25 / 2,75 / 7,00 / **51,25** |
| T23 | largo | 10 | 449 | 0,25 / 2,50 / 7,02 / 25,25 | 0,50 / 4,15 / 10,63 / 45,25 |
| T23 | largo | 20 | 208 | 0,50 / 3,82 / 9,47 / 15,50 | 0,50 / 5,99 / 13,18 / 35,25 |
| T23 | corto | 10 | 503 | 0,25 / 2,50 / 4,99 / 7,25 | 0,25 / 3,50 / 5,99 / 12,75 |
| RTH | largo | 10 | 377 | 0,50 / 2,50 / 4,62 / 9,00 | 0,50 / 3,50 / 7,09 / 17,25 |
| RTH | corto | 10 | 369 | 0,25 / 2,25 / 3,74 / 6,50 | 0,50 / 3,95 / 6,84 / 10,25 |
| H1 | largo | 10 | 161 | 0,50 / 3,00 / 4,70 / 9,00 | 0,75 / 4,00 / 7,50 / 12,00 |
| H1 | corto | 10 | 130 | 0,50 / 2,89 / 5,43 / 6,50 | 0,75 / 5,80 / 8,03 / 10,25 |
| M15 | largo | 4 | 288 | 0,25 / 2,16 / 4,53 / 8,25 | 0,50 / 3,75 / 5,75 / 8,75 |
| 23 horas juntas | largo | 4 | 4.581 | 0,25 / 2,00 / 4,00 / 31,25 | 0,25 / 3,00 / 5,75 / 51,25 |
| 23 horas juntas | largo | 30 | 55 | 1,50 / 10,25 / 12,63 / 14,25 | 3,00 / 18,19 / 24,64 / 25,25 |

**Lo típico es un tick: mediana 0,25 en casi todas las celdas.** Lo raro no: **p95 de 2 a 4 puntos (10 a
20 USD de MES) y p99 de 4 a 10 puntos (20 a 50 USD)** dentro de la misma barra de minuto, y un máximo
de **31 puntos en la misma barra y 51 en la siguiente** en la sesión nocturna del lado largo (una barra
de minuto de más de 30 puntos de rango). En la rueda, los máximos son de 9 a 13 puntos en la misma barra
y hasta 17–20 en la siguiente. **Esto es lo que el stop no te ahorra**: a un stop de 10 puntos hay que
sumarle 2,5 en el p95 y 5–7 en el p99 sólo por movimiento del mercado, antes de contar el libro. Y el
exceso **crece con D** (a D = 30, mediana 1,5 y p95 10 en las horas juntas): los stops anchos se tocan en
barras violentas.

## 5 · LA CUENTA DE 20 SESIONES — entra siempre, mismo lado, stop a D, sin contar ninguna ganancia

«Stops» = suma de `D + salto` en las sesiones que tocaron (salto = 0 siempre, ver punto 4). «Con stop» =
stops + pérdida al cierre de las sesiones que no tocaron. USD de MES = puntos × 5.

### T23, lado largo

| D | toques en 20: p50 / p95 / máx | stops pts p50 / p95 / p99 / máx | **stops USD MES p50 / p95 / p99 / máx** | con stop p50 / p95 / p99 |
|---|---|---|---|---|
| 2 | 18 / 20 / 20 | 36 / 40 / 40 / 40 | 180 / 200 / 200 / 200 | 36 / 40 / 40 |
| 4 | 15 / 19 / 20 | 60 / 76 / 76 / 80 | 300 / 380 / 380 / 400 | 60 / 76 / 76 |
| 6 | 13 / 18 / 19 | 78 / 108 / 114 / 114 | 390 / 540 / 570 / 570 | 82 / 108 / 114 |
| 8 | 11 / 17 / 19 | 88 / 136 / 144 / 152 | 440 / 680 / 720 / 760 | 92 / 136 / 144 |
| 10 | 9 / 16 / 19 | 90 / 160 / 180 / 190 | 450 / 800 / 900 / 950 | 100 / 160 / 180 |
| 15 | 5 / 14 / 17 | 75 / 210 / 225 / 255 | 375 / 1.050 / 1.125 / 1.275 | 96 / 210 / 233 |
| 20 | 3 / 11 / 15 | 60 / 220 / 260 / 300 | 300 / 1.100 / 1.300 / 1.500 | 97 / 233 / 268 |
| 30 | 1 / 8 / 12 | 30 / 240 / 300 / 360 | 150 / 1.200 / 1.500 / 1.800 | 90 / 286 / 352 |
| **sin stop** (control, D = 60) | — | — | — | **84 / 353 / —** |

### Las otras ventanas, lado largo, con stop (p50 / p95 / p99) y sin stop (p50 / p95)

| ventana | D=4 | D=10 | D=20 | sin stop |
|---|---|---|---|---|
| RTH | 58 / 76 / 76 | 80 / 143 / 170 | 79 / 220 / 294 | 74 / 319 |
| H1 | 42 / 69 / 72 | 48 / 110 / 134 | 46 / 120 / 139 | 46 / 110 |
| M15 | 28 / 51 / 56 | 28 / 59 / 68 | 27 / 56 / 66 | 27 / 56 |

El lado corto y el resto de las celdas están en la salida cruda; la forma es la misma.

## 6 · Lo que la cuenta dice

1. **El stop compra cola y no mediana.** En T23 largo, sin stop, 20 sesiones de pérdidas suman 84 en
   la mediana y **353 en el p95**. Con stop a 10: **100 en la mediana y 160 en el p95**. La mediana
   sube 20 %; el p95 baja 55 %. Con stop a 4: mediana 60, p95 76, p99 76: **la cola desaparece y la
   pérdida se vuelve casi determinista** (15 de 20 sesiones te sacan, y la suma es 15 × 4). **Un stop
   apretado convierte una cola gorda en un sangrado fijo.** Es terreno, no consejo: el sangrado fijo
   es lo que una prop firm cobra por día, y la cola es lo que la cierra.
2. **En la primera hora el stop no compra casi nada.** H1 largo: sin stop 46 / 110; con stop a 10,
   48 / 110 / 134. Ni la mediana ni el p95 se mueven, porque a una hora la excursión ya es chica y el
   stop de 10 apenas se toca (17 %). Sólo el stop de 4 recorta el p95 (110 → 69), y a cambio te saca
   10 sesiones de cada 20. **En ventanas cortas la tenencia ya hizo el trabajo del stop.**
3. **La suma con stop tiene un techo aritmético, y está cerca.** Con D chico casi todas las sesiones
   tocan, así que la suma es ≈ 20 × D: a D = 2 el p99 es 40 = 20 × 2. **El stop no acota el daño a D:
   lo acota a 20 × D por veinte sesiones**, más el exceso del punto 4, que a D = 2 es un tick típico
   pero puede ser 31 puntos una vez.
4. **Lo que nadie ve en una barra diaria:** con barras de minuto el precio nunca abre más allá del stop
   entre barras (salto 0,00 siempre), pero **dentro de la barra** se pasa 2–4 puntos en el p95 y hasta
   30 en la noche. La cota del deslizamiento por movimiento es esa; la del libro no está medida.

## 7 · Lo que esta medición NO dice

- **No dice si alguna combinación de ventana, hora y stop es rentable.** No se contó ninguna ganancia.
  La cuenta del punto 5 es lo que pierde alguien que entra siempre del mismo lado; nadie hace eso.
- **No dice nada de MES**: es ES, y los USD son ×5 como supuesto.
- **No modela el deslizamiento por profundidad del libro**, ni comisiones. Un stop-market real se
  llena en algún lugar de la barra que toca, entre el stop y el exceso del punto 4.
- **Es 2016–2019.** En 2020 o 2022 los toques a cada D, los excesos y las sumas serían otros, y que
  las razones aguanten no se verifica sin abrir la caja.
- La entrada es al primer minuto de la ventana; a otra hora de entrada, otros números.
