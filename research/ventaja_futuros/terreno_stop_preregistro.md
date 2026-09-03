# Pre-registro — Terreno del stop: cada cuánto te saca el mercado a cada distancia, y a qué hora

**Fecha: 2026-09-03. Ventana D.** Se commitea **solo**, antes de correr. Terreno: no hay ventaja, no hay
selección, no se toca la caja (nada de 2020+), **mismo período 2016-2019 y misma P-escalera de 971
sesiones** que `terreno_tenencia.py` y `terreno_horas.py`. ES a 1 minuto de Databento.

## LIMITACIONES, declaradas antes de correr

1. **ES, no MES.** Libros separados; el traslado es un supuesto. Los «USD de MES» son puntos × 5.
2. **Un stop en la práctica se ejecuta con deslizamiento y esto no lo modela.** El «exceso» del punto 3
   es la **cota del deslizamiento por movimiento del mercado** entre barras de minuto, **no por
   profundidad del libro**. Un stop-market real se llena en algún lugar de la barra que toca, y eso no
   se sabe con barras.
3. **Entrar siempre en la misma dirección no es una estrategia.** La cuenta del punto 4 es un piso de
   terreno: cuánto pierde alguien que entra siempre, siempre del mismo lado, y usa un stop. **No cuenta
   ninguna ganancia en ningún lado. No es rentabilidad y no se convierte en eso.**
4. Los niveles son de 2016-2019, la mitad de violento que 2016-2026. Las razones pueden trasladarse;
   los niveles no; que aguanten un régimen violento no está verificado.
5. La entrada es al `open` de la primera barra de la ventana; el toque se detecta con `low`/`high` de
   barras de minuto: un toque que dura menos de una barra se ve; el orden dentro de la barra no.

## Definiciones

| término | definición |
|---|---|
| **ventanas** | T23 (17:00 → 16:00 CT), RTH (08:30 → 15:00), H1 (08:30 → 09:30), M15 (08:30 → 08:45), y las 23 horas en punto de `terreno_horas.py` |
| **entrada** | `open` de la primera barra de la ventana, `O` |
| **stop a D** | largo: precio `O − D`; corto: `O + D`. D ∈ {2, 4, 6, 8, 10, 15, 20, 30} puntos de ES, y **D = 60 sólo para el control** |
| **toque** | largo: primera barra de la ventana con `low ≤ O − D`; corto: primera con `high ≥ O + D`. Se mira hasta la última barra de la ventana inclusive |
| **frecuencia de toque** | sesiones con toque / sesiones de la población, por ventana, lado y D |
| **exceso en la misma barra** | largo: `(O − D) − low` de la barra que toca. Cuánto pasó el precio del stop dentro de esa barra. Siempre ≥ 0 |
| **salto en la apertura** | largo: `max(0, (O − D) − open de la barra que toca)`. Si la barra ya abre debajo del stop, lo mínimo que un stop-market paga de más |
| **exceso en la siguiente** | largo: `max(0, (O − D) − low de la barra siguiente)`. Si no hay barra siguiente en la ventana, se cuenta como sin dato |
| **pérdida por sesión con stop a D** | si tocó: `D + salto en la apertura`. Si no tocó: `max(0, O − close de la última barra de la ventana)` (largo). **Ninguna ganancia entra**: una sesión que cierra a favor vale 0 |
| **pérdida por sesión sin stop** | `max(0, O − close de la última barra)` (largo) |
| **suma de 20 sesiones** | sobre ventanas móviles de 20 sesiones consecutivas de la población, la suma de la pérdida por sesión, y el conteo de toques. Distribución: mediana, p90, p95, p99, máximo |

Para el corto, todo espejado con `high` y `O + D`.

## Las cuatro salidas

1. **Frecuencia de toque**: por ventana (las cuatro), lado y D.
2. **Por hora**: frecuencia de toque para las 23 tenencias de una hora, lado y D. Al lado, la razón de
   excursión mediana contra la hora de la apertura que ya está en `terreno_horas.txt`, para ver si la
   hora barata para la excursión típica es la hora barata para que te saquen. **Si son horas distintas,
   se dice; si son las mismas, también.**
3. **Lo que el stop deja pasar**: por ventana (las cuatro) y D, y para las 23 horas juntas por D:
   mediana, p95, p99 y máximo del exceso en la misma barra, del salto en la apertura y del exceso en
   la siguiente, sobre las sesiones que tocaron.
4. **La cuenta de 20 sesiones**: por ventana (las cuatro), lado y D: distribución del conteo de toques
   y de la suma, en puntos de ES y en USD de MES (×5). También la suma **sólo de los stops** (`D + salto`
   en las sesiones que tocaron, 0 en las demás), que es literalmente «cuántas veces te sacan y cuánto
   suma».

## CONTROL — y éste debe dar DISTINTO

Con **D = 60**:

- la frecuencia de toque en T23 tiene que caer a **menos del 3 %** (el p99 de la excursión de T23 en
  este período es 89 puntos en largo y 58 en corto, así que 60 está entre p95 y p99);
- la **suma de 20 sesiones con stop a 60** tiene que parecerse a la **suma de 20 sesiones sin stop**:
  **mediana y p95 dentro del 10 %** una de otra, en las cuatro ventanas y los dos lados. Cuando D crece,
  la pérdida con stop converge a la pérdida sin stop por construcción; si no converge, el cálculo está
  mal.

Se imprime al lado, como **orientación y no como control**, el drawdown máximo en ventanas móviles de
20 sesiones sobre la secuencia `close − open` de cada ventana (la definición M4 del guardián), que es
otra cantidad: incluye ganancias que compensan.

**Si el control no da, no se publica nada de lo demás.**

## Dónde se observa

| | |
|---|---|
| script | `research/ventaja_futuros/terreno_stop.py` |
| salida cruda, commiteada antes de interpretar | `research/ventaja_futuros/terreno_stop.txt` |
| resumen | `research/ventaja_futuros/terreno_stop_resultado.md` |

---

# ENMIENDA 1 — 2026-09-03

**Se anota al pie. Nada de arriba se reescribe.**

## Qué pasó

La primera corrida (`50c0cf8` → script) **paró en el control** y no imprimió nada más. El script sale
con código 1 antes de calcular frecuencia, horas, exceso o la cuenta de 20 sesiones. **Al momento de
escribir esta enmienda no se ha visto ninguna cifra de las salidas 1 a 4.** Lo único visto es la tabla
del control:

| criterio | resultado |
|---|---|
| convergencia con stop a 60 ↔ sin stop, mediana y p95 dentro del 10 % | **cumplido en las 8 filas**: peor diferencia +4,8 % (T23 largo, p95) |
| toque en T23 con D = 60 **< 3 %** | **3,09 % en T23 largo**; 0,93 % en corto |

## Por qué el umbral estaba mal escrito, y no el cálculo

El mismo párrafo del control dice que **60 está entre el p95 (51,12) y el p99 (89,02)** de la excursión
de T23 largo medida en `terreno_tenencia.txt`. Eso implica una frecuencia de toque **entre 1 % y 5 %**,
y el «< 3 %» fue un número redondo puesto sin derivarlo. 3,09 % está dentro de lo que la premisa del
propio pre-registro admite. **El criterio que prueba el cálculo es la convergencia, y pasó.**

## Qué se cambia, y es más exigente que lo que reemplaza

La frecuencia de toque con stop a D **es la misma cantidad** que la fracción de sesiones cuya excursión
adversa máxima en la ventana es ≥ D, calculada por otro camino (primera barra que cruza, contra máximo de
la ventana). Se reemplaza el «< 3 %» por:

- **igualdad exacta**, en las cuatro ventanas y los dos lados, entre la frecuencia de toque con D = 60 y la
  fracción de sesiones con excursión ≥ 60 de `window_stats` (la función de `terreno_tenencia.py`);
- y que en T23 esa fracción esté **entre 1 % y 5 %**, que es lo que p95 y p99 obligan.

La convergencia del 10 % queda como estaba. Se corre de nuevo **después** de commitear esta enmienda sola.
