# Resultado — Escalera por hora del día: la palanca no es el tiempo, es la hora, y dentro de la rueda es corta

**Ejecuta `terreno_horas_preregistro.md` (`6e9d036`, solo).** Salida cruda en `terreno_horas.txt`,
commiteada antes de este archivo. Una corrida. **ES a 1 minuto de Databento, 2016–2019, P-escalera
de 971 sesiones**, la misma de `terreno_tenencia_resultado.md`.

> **Limitaciones, antes del primer número:** es **ES, no MES** (libros separados; el traslado es un
> supuesto). Una tenencia de horario fijo **no es una estrategia**. **Los NIVELES son de 2016–2019, un
> período la mitad de violento que 2016–2026**: las razones entre ventanas pueden trasladarse, los
> niveles no, y **que las razones aguanten un régimen violento NO está verificado** y no se verifica
> sin abrir la caja. No se miró rentabilidad de ninguna hora.

---

## 1 · EL CONTROL — da distinto, como debía

Sobre las 970 sesiones con las 23 ventanas cubiertas:

| lado | S = suma de 23 horas, mediana | T = tenencia continua, mediana | S/T mediana | sesiones con S < T |
|---|---|---|---|---|
| largo | 50,25 | 8,75 | **5,54** | **0** de 970 |
| corto | 50,75 | 10,38 | **4,79** | **0** de 970 |

**La suma de las horas sueltas es 5 veces la tenencia continua**, y en ninguna sesión es menor. Una
tenencia continua compensa lo que 23 tenencias separadas pagan una por una. El cálculo se sostiene.

Cobertura: 1 sesión sin barra en dos ventanas nocturnas; hasta 10 sesiones sin barra exacta a `h:00`
entre las 18:00 y la 01:00 (la apertura de la ventana corre unos minutos). Contado, no corregido.

## 2 · LA ESCALERA — razón de cada percentil contra la hora de la apertura (08:30 → 09:30)

Referencia, puntos de ES: largo p50 4,00 · p95 16,88 · p99 24,07; corto p50 4,00 · p95 14,88 · p99 27,42.

| hora de arranque CT | largo p50 | largo p95 | largo p99 | corto p50 | corto p95 | corto p99 |
|---|---|---|---|---|---|---|
| 17:00 reapertura | 0,31 | 0,42 | 0,68 | 0,38 | 0,45 | 0,42 |
| 18:00 | 0,25 | 0,33 | 0,49 | 0,25 | 0,39 | 0,37 |
| 19:00 | 0,31 | 0,41 | 0,58 | 0,38 | 0,45 | 0,40 |
| 20:00 | 0,31 | 0,36 | 0,47 | 0,31 | 0,41 | 0,41 |
| 21:00 | 0,25 | 0,33 | 0,47 | 0,25 | 0,34 | 0,34 |
| 22:00 | 0,19 | 0,27 | 0,42 | 0,19 | 0,24 | 0,30 |
| 23:00 | **0,19** | **0,25** | 0,35 | **0,19** | 0,27 | 0,39 |
| 00:00 | 0,25 | 0,28 | **0,34** | 0,25 | 0,29 | **0,30** |
| 01:00 | 0,31 | 0,34 | 0,38 | 0,31 | 0,47 | 0,49 |
| 02:00 (abre Europa) | 0,50 | 0,52 | 0,58 | 0,44 | 0,52 | 0,50 |
| 03:00 | 0,38 | 0,40 | 0,55 | 0,38 | 0,45 | 0,40 |
| 04:00 | 0,31 | 0,39 | 0,55 | 0,38 | 0,42 | 0,41 |
| 05:00 | 0,38 | 0,39 | 0,52 | 0,38 | 0,38 | 0,36 |
| 06:00 | 0,38 | 0,35 | 0,46 | 0,38 | 0,45 | 0,41 |
| 07:00 | 0,44 | 0,47 | 0,59 | 0,44 | 0,57 | 0,57 |
| 08:00 (contiene la apertura) | 0,88 | 0,80 | 0,84 | 0,88 | 0,81 | 0,75 |
| **08:30 → 09:30, referencia** | **1,00** | **1,00** | **1,00** | **1,00** | **1,00** | **1,00** |
| 09:00 (datos de las 10:00 ET) | 0,81 | 0,93 | **1,26** | 0,88 | 0,87 | 0,79 |
| 10:00 | 0,69 | 0,82 | 0,97 | 0,75 | 0,82 | 0,72 |
| 11:00 | 0,56 | 0,66 | 0,89 | 0,56 | 0,64 | 0,82 |
| 12:00 | **0,56** | 0,67 | 0,90 | **0,50** | **0,62** | **0,57** |
| 13:00 | 0,62 | 0,79 | 0,96 | 0,62 | 0,79 | 0,82 |
| 14:00 (cierre de contado) | 0,69 | 0,81 | **1,16** | 0,75 | 0,84 | 0,89 |
| 15:00 (con el corte 15:15–15:30) | 0,38 | 0,40 | 0,54 | 0,44 | 0,45 | 0,42 |

Los puntos de cada hora están en la salida cruda.

## 3 · Lo que la columna dice

1. **La U es real, y tiene dos brazos.** La hora de la apertura y la hora del cierre de contado
   (14:00 → 15:00 CT) son las más caras. La madrugada (23:00 → 01:00 CT) cuesta **un cuarto** de la
   apertura en la mediana y **un tercio** en el p95. Hay una joroba a las 02:00 CT, la apertura de
   Europa, que llega a la mitad de la referencia.
2. **Pero dentro de la rueda el valle es poco profundo.** La hora más barata de la rueda, 12:00 → 13:00
   CT, retiene **el 56 % de la mediana y el 62–67 % del p95** de la hora de la apertura. Ninguna hora
   de la rueda baja del 50 % en la mediana ni del 60 % en el p95. **La palanca «elegir la hora» compra
   entre un tercio y la mitad del riesgo de la primera hora, no un orden de magnitud.**
3. **La cola no obedece a la U igual que la mediana.** En p99, la hora de las 09:00 CT (que contiene
   los datos de las 10:00 ET) **supera** a la de la apertura en el lado largo (1,26), y la hora del
   cierre también (1,16). Las horas «tranquilas» del mediodía retienen ~0,9 del p99 de la apertura en
   largo. **Lo que la hora del medio ahorra es sobre todo excursión típica; la excursión rara es casi
   igual de grande a cualquier hora de la rueda.**
4. **Respuesta a la pregunta:** el tiempo por sí solo no es palanca (la escalera anterior ya lo dijo:
   15 minutos retienen un quinto del riesgo de 23 horas). **La hora sí es palanca, pero corta**: mueve
   la mediana entre 0,56 y 1,0 dentro de la rueda, y casi no mueve el p99. La única palanca grande
   es no estar en la rueda, y eso es donde está la mitad del volumen y todo lo que una prop firm
   deja operar. **Se dice como terreno, no como consejo.**

## 4 · Lo que esta medición NO dice

- No dice si alguna hora es rentable. No se miró. No dice cuándo entrar ni cuándo salir.
- No dice nada de MES.
- **No dice qué pasa en 2020 ni en 2022.** Las razones de esta tabla son de un régimen tranquilo. En
  un régimen violento la U puede aplastarse (todo caro) o exagerarse; no se sabe y no se va a saber
  sin abrir la caja.
- Las horas nocturnas con pocas barras tienen su apertura corrida unos minutos en hasta 10 sesiones.
- La excursión es exacta sólo para una entrada en la apertura de la ventana.
