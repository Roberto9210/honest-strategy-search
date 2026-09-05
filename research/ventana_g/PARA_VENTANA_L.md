# PARA LA VENTANA L — lo que la VENTANA G midió, encontró y cotizó para su prueba agrupada

**VENTANA G. K = 261, no gasta cartucho.** Nada de esto corre la prueba agrupada ni la pre-registra.

*Este archivo vive en `research/ventana_g/` porque la VENTANA G no escribe en `research/literatura/`.
Lo leí de ahí, no lo toqué.*

---

## 1. DOS COSAS DE FECHAS QUE ROMPEN LA ESPECIFICACIÓN TAL COMO ESTÁ ESCRITA

### 1.1 — El evento 48 de L10 cae DENTRO de la caja sellada

`P01` especifica, para L10: **último día hábil de cada mes de 2016 a 2019, retorno del día
SIGUIENTE**. El último hábil de diciembre de 2019 es el **2019-12-31**, y su día siguiente es el
**2020-01-02** — que es exactamente `CAJA[0]`, **el primer día de la caja sellada**.

**Corrida al pie de la letra, la prueba agrupada toca la caja.**

Dos salidas, y la decisión es de la VENTANA L, no mía:
- declarar **47 eventos** en vez de 48, o
- correr el conteo un mes hacia atrás (último hábil de **dic-2015 a nov-2019**), que da 48 eventos
  todos dentro de 2016-2019.

*(Para medir los σ de abajo usé los 47 que caen dentro de 2016-2019, sin tocar nada.)*

### 1.2 — 2018-03-30 es Viernes Santo: no es un día hábil del CME

"El último día hábil del mes" **no es** "el último día hábil del CME". Al cotizar los datos de
divisas, la fecha **2018-03-30** —último viernes de marzo de 2018— devolvió **0 registros y USD
0,00** en los seis símbolos: el mercado no operó.

Verificado en `salida_cotizacion_divisas.txt`. **Son 47 fechas con datos, no 48**, y eso mueve la
potencia del panel de L08 igual que mueve la de L10.

Recomendación: construir las fechas contra el **calendario de sesiones real** (el que ya está en el
repo para ES sirve: mismo calendario Globex) y no contra `weekday() < 5`.

---

## 2. LOS DOS σ QUE ESTABAN ESTIMADOS, MEDIDOS

`P01` los declaró como estimaciones —*"dos de los tres `σ_j` son estimaciones mías, no
mediciones… por eso `t(θ=1) = 4,69` es una cota optimista"*— y pidió medirlos antes de correr.
Medidos sobre ES 1-min 2016-2019 (`sigmas_para_L.py`, salida commiteada):

| j | m_j | σ_j **estimado** | σ_j **MEDIDO** | n_j | n·r² estimado | n·r² medido |
|---|---|---|---|---|---|---|
| L11 | 11,4 pb | ~60,0 | **82,00 pb** | 176 | 6,35 | **3,40** |
| L10 | 17,0 pb | ~60,0 | **82,82 pb** | 48 | 3,85 | **2,02** |
| L08 | publicado | — | — | 480 | 11,83 | 11,83 |
| | | | | **704** | **22,04** | **17,25** |

```
t(θ=1)                          4,69  ->  4,15      (-12%)
θ mínimo detectable a 3,0σ      0,64  ->  0,72
```

**No cae debajo de 3.** La prueba conserva resolución. Pero la brecha que ya estaba sigue estando: la
hipótesis es `θ ≥ 0,25` y la regla de decisión pide `t ≥ 3,0` **para ese θ**, o sea `t(θ=1) ≥ 12`.
Con σ medido la prueba detecta **θ = 0,72**, no 0,25. La medición **agranda** esa brecha; no la crea.

### El estimador, y por qué ése

Usé el **desvío común** (segundo momento) y no uno robusto. El estadístico a calibrar es
`t = m/(σ/√n)` y el error estándar de una **media** depende del segundo momento; un estimador robusto
descarta la cola a propósito, daría un σ menor y una potencia **mayor** — sería justo el error que
este paso existe para evitar. El robusto va al lado sólo para ver cuánta de σ es cola: **53,81 pb**
para L11, o sea que la cola aporta **1,52×**.

La cola medida **en esta serie** (no en otra): `p99/mediana` de |retorno| = **7,29** contra **3,82**
de una normal; exceso de curtosis **6,4**.

### Dos límites de esta medición, dichos antes que el número

1. **L11 es una COTA OPTIMISTA.** Sus 176 eventos son días de anuncio y esas fechas exigen el
   calendario macro, que no está en el repo. Medí el desvío **incondicional** de las 1.006 sesiones.
   Los días de anuncio son **más** volátiles, así que el σ verdadero de L11 es **mayor** y el 4,15
   también está alto. Con el calendario de los 44 anuncios/año (paso 2 de P01, gratis) esto se cierra.
2. **El TCL no lo arregla medir σ.** Con n = 48 y esta cola, la aproximación normal del **propio
   estadístico** es optimista. Eso lo mide el **control 2** de P01 (el placebo de signo, mil veces), y
   hay que leerlo con esa expectativa: si la distribución de `t` del placebo no sale centrada y con
   colas normales, la vara de 3,0 no vale lo que dice.

---

## 3. LA COTIZACIÓN DE LOS DATOS: USD 0,87 EN TOTAL

`databento_cotizar_divisas.py` — **cotizado, NO comprado.** El script no tiene modo `--comprar` por
diseño. Crédito declarado restante: **USD 98,92**.

| bloque | schema | símbolos | ventanas | MB | registros | **USD** | sirve a |
|---|---|---|---|---|---|---|---|
| L08 fix de Londres | ohlcv-1m | 6 | 48 × 4 h | 3,8 | 67.402 | **0,25** | L + G |
| L07 gotobi (plan B) | ohlcv-1m | 1 | 286 | 1,0 | 17.017 | **0,06** | L |
| microestructura 6E | tbbo | 1 | 3 días | 18,5 | 231.645 | **0,48** | G |
| terciles diarios | ohlcv-1d | 6 | 2016-2019 | 0,4 | 7.458 | **0,07** | G + L |
| **TOTAL** | | | | | | **0,87** | |

Ningún ítem se acerca al tope de USD 3,00 por pedido; el total no se acerca al de USD 25,00.

**Lo que P04 preguntaba y ya está contestado:** el precio no es la restricción. **L08 y L07 cuestan
juntas USD 0,31.** Se pueden comprar las dos y seguir teniendo USD 98 de crédito. La decisión sobre
el cartucho 262 no depende del costo de los datos.

Dos avisos sobre la cotización misma:
- **El horario de verano se manejó fecha por fecha**, como P04 pide: 14:00–18:00 de Londres sale
  13:00–17:00Z en verano y 14:00–18:00Z en invierno. Visible en la salida.
- **L07 quedó cotizada del lado caro**: usé una ventana de **una hora** en vez de los 10 minutos de
  P04, y extrapolé 24 fechas exactas a 286. Sobra ~6× y aun así da USD 0,06, así que afinarlo no
  cambia ninguna decisión.

---

## 4. LO QUE EL JUEZ TODAVÍA NO PUEDE HACER CON DIVISAS

Para que la VENTANA L no cuente con algo que no existe: **el juez no puede juzgar 6E ni 6J hoy**, y
comprar los datos **no alcanza**.

- La **ficha de calibración** de 6E/6J está empezada (`instrumentos.py`): lo que sale de la
  especificación del CME —punto, tick, equivalencia en micros, sesión— ya está y es gratis. Falta la
  **comisión de divisas** (una lectura de la página de Tradeify, gratis: la que tenemos cubre índices)
  y el **medio-spread por régimen** más los **cortes de tercil** (eso sí es la compra de arriba).
- Y aunque la ficha se complete, **el cálculo sigue cableado al ES**: quedan cuatro constantes
  leyéndose de los globales del ES y `cargar_mercado()` sólo sabe leer ES 1-min. Está **marcado como
  NO IMPLEMENTADO** y hay una cerradura dentro del cálculo que lo impide en silencio.
- **Buena noticia para L07 y L08:** ninguna usa bracket —miden el retorno de una ventana declarada—,
  así que no necesitan las dos constantes más caras (exceso en el stop y constante de sobrepaso).

---

## 5. Y UNA ADVERTENCIA DE MUESTRA QUE APLICA A CUALQUIER INSTRUMENTO NUEVO

Medido en `cortes_tercil_muestra.py`: si los **cortes de tercil de volatilidad** se estiman sobre
pocas sesiones, la etiqueta de régimen se equivoca mucho.

| n sesiones | 3 | 25 | 50 | 100 | 250 | 500 |
|---|---|---|---|---|---|---|
| % de sesiones **mal etiquetadas** (sorteo al azar) | **34%** | 15% | 10% | 7% | **4,7%** | 3,3% |
| ídem con una ventana **contigua** (comprar n días seguidos) | 43% | 39% | 36% | 32% | **29%** | 20% |

La segunda fila es la que importa al comprar: **comprar días seguidos no arregla el problema aunque
sean muchos** — es sesgo, no varianza. Hay que comprar días **repartidos por régimen**, que es lo que
se hizo con los seis días de microestructura del ES.

---

## Procedencia

`sigmas_para_L.py` · `salida_sigmas_para_L.txt` · `databento_cotizar_divisas.py` ·
`salida_cotizacion_divisas.txt` · `cortes_tercil_muestra.py` · `salida_cortes_muestra.txt` ·
`instrumentos.py`. Documentos de la VENTANA L **leídos y no modificados**: `P01`, `P03`, `P04`.
