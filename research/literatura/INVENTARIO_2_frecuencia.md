# INVENTARIO 2 — La búsqueda nueva, con F17 primero. Resultado: CERO, y es un cero distinto del anterior.

**VENTANA L. NO MIDE NADA. K sigue en 261.** Catalogar es gratis. `F17` se commiteó antes de abrir esta
búsqueda; el historial lo muestra.

**Qué se buscó:** mecanismos publicados que produzcan **≥ 5 operaciones por día (línea por defecto de
F17) o ≥ 20 (línea de Roberto)** en el E-mini, con tenencia mediana > 10 s, intradiarios, en el corpus
de microestructura del E-mini, del regulador, y de flujo, libro y horario. **Para cada clase, las cinco
preguntas de Roberto: (a) operaciones por día con el número, (b) tenencia mediana y si supera 10 s,
(c) magnitud publicada en unidades convertibles, (d) si el juez lo puede cargar hoy, (e) superposición
con nuestro período o con la caja.**

**Límite de la búsqueda, dicho antes del resultado:** diez fuentes leídas en texto (siete del regulador,
Kirilenko, Scholtus, Cont y Gould en resumen); SSRN devolvió 403 dos veces (Baron et al.; Scholtus lo
conseguí por otra vía). **No es una búsqueda sistemática de la literatura de microestructura: es la
que se pudo hacer en una ronda con las fuentes accesibles.** Eso acota el cero.

---

# Las clases, una por una

## 1. Desbalance del libro al mejor precio y desbalance de flujo de órdenes (OFI)

**Fuentes:** Gould y Bonart 2016 (10 acciones de Nasdaq; *"la dirección del siguiente movimiento del
punto medio"*); Cont, Kukanov y Stoikov 2014 (50 acciones de NYSE, 2010; relación **contemporánea**
lineal entre OFI y cambio de precio; **sin afirmación predictiva** en el resumen); Kirilenko et al. 2014
(E-mini, mayo 2010: los de alta frecuencia compran en la dirección del precio durante 0-4 s).

| | |
|---|---|
| (a) ops/día | **ilimitadas**: hay señal en cada cambio del libro. Pasa la frecuencia de sobra |
| (b) tenencia | **el siguiente movimiento del punto medio: segundos.** Mediana **< 10 s** → cerradura R2. Y **< 60 s** → NO MEDIBLE con barras de un minuto (`f5d129f`) |
| (c) magnitud | probabilidades de dirección del siguiente tick, **no puntos básicos ni ticks netos por operación**. Cont et al. es contemporáneo, no predictivo |
| (d) instrumento | ES vía `mbo`: **seis días** en el repo, no cuatro años |
| (e) evidencia | acciones 2010-2015; E-mini sólo Kirilenko 2010 |
| **lo que la casa ya midió** | **G, `9a02717`**: la versión de cruce (3a) **muerta**: separación 0,505 ticks a 1 s contra ~1 tick de cruzar. La versión pasiva con el desbalance como predictor de selección adversa (3b): **ρ entre −0,019 y +0,009** a 30 s de markout, en seis días de dos épocas. **Cero.** |

> **NO ENTRA: tenencia bajo la cerradura R2 y bajo la resolución del dato. Y su versión de 30 segundos, la única medible con lo que hay, G ya la midió en cero.**

## 2. Ajuste de precio en los segundos posteriores a una publicación

**Fuente:** Scholtus, van Dijk y Frijns 2014, *JBF*. **Un ETF del índice en NASDAQ**, 2009-01-06 →
2011-12-12; **800 publicaciones en 520 de 736 días**; una demora de **300 ms** reduce el retorno de la
estrategia con previsión perfecta un 3,08 % (1 s: 7,33 %); en promedio sobre 707 publicaciones, la
pérdida por 300 ms es **0,44 pb** (1 s: 1,04 pb).

| | |
|---|---|
| (a) ops/día | **~1 por día** (800 en 736 días) → **no pasa F17** |
| (b) tenencia | segundos: la mayor parte del ajuste ocurre en los primeros 5 s |
| (c) magnitud | en pb, pero **con previsión perfecta de la sorpresa**: no es operable sin saberla |
| (d) instrumento | ETF, no ES |
| (e) evidencia | 2009-2011; fuera del nuestro |

> **NO ENTRA: frecuencia de 1 por día, y latencia de milisegundos —escalón 1—.**

## 3. Riesgo y retorno de la alta frecuencia en el E-mini

**Fuente:** Baron, Brogaard, Hagströmer y Kirilenko, *JFQA* 2019, E-mini 2010-2012 (SSRN 403: **sin
números, no los invento**). Documenta que las ganancias se concentran en los más rápidos y agresivos.

> **NO ENTRA: es la clase que el reglamento prohíbe por nombre ("HFT") y que el escalón 3 de latencia no alcanza.** Vale como descripción de la contraparte (`D12`), no como candidata.

## 4. La liquidación de inventario de alta frecuencia a los 10-20 segundos

**Fuente:** Kirilenko et al. 2014 (`H01` Hecho 5): compran 0-4 s en la dirección del precio y deshacen
en 10-20 s. La idea sería **operar contra esa liquidación**.

| | |
|---|---|
| (a) ops/día | muchas: cada movimiento grande |
| (b) tenencia | **10-20 s: la zona gris exacta** de R2 y "HFT", y **< 60 s → NO MEDIBLE** con el repo |
| (c) magnitud | **ninguna publicada como retorno**: el paper mide inventarios, no rentabilidad de operar contra ellos |
| (e) evidencia | cuatro días de mayo de 2010 |

> **NO ENTRA: sin magnitud, en la zona gris, y no medible con barras de un minuto.**

## 5. Los efectos de horario dentro de la sesión, apilados

Apertura 09:30, publicaciones 10:00, cierre europeo 11:30, FOMC 14:00, desbalance de cierre 15:50, última
media hora. **Cada uno es un mecanismo distinto de una vez por día.** Apilarlos da 5-6 por día **y son
5-6 hipótesis**: `F17` §4 lo prohíbe, y `F9`/`F10` ya lo prohibían.

> **NO ENTRA. Y las piezas sueltas ya están en el inventario viejo, ciegas (L01, L03) o cerradas (L10).**

## 6. VPIN — toxicidad del flujo en el E-mini

**Fuente:** Easley, López de Prado y O'Hara 2012, *RFS*, E-mini S&P 500. **Predice volatilidad, no
dirección.** No es una regla con signo: es un eje de régimen, territorio de `M02`.

> **NO ENTRA como candidata: no pasa `F6` (no hay lado que operar). Puede entrar como eje, que no es de este inventario.**

## 7. Adelanto ES contra SPY y NQ

**Fuentes:** Hasbrouck 2003; Budish, Cramton y Shim 2015, *QJE* (arbitraje ES-SPY a escala de
milisegundos). Horizonte de milisegundos, y necesita la pata de contado o colocación.

> **NO ENTRA: R2, "HFT", escalón 1 de latencia, y un instrumento que el juez no carga.**

## 8. Periodicidad de media hora en acciones

**Fuente:** Heston, Korajczyk y Sadka 2010, *JF*. Es un efecto **de corte transversal entre acciones**, no
del índice. Para el índice, lo que queda es el momento intradiario de Gao (L02), ya ciego.

> **NO ENTRA: no existe para el ES.**

## 9. El corpus del regulador, releído con F17 puesto

Siete documentos en `H01`. **Todos describen calidad de mercado, poblaciones y latencia; ninguno
describe un efecto direccional repetible a ≥ 5 por día.** Cero candidatas, como estaba previsto, y ahora
con el filtro que lo confirma.

---

# EL RESULTADO

> ## **CERO candidatas pasan F17, a 5 por día y a 20 por día. Y el cero tiene forma: todo lo que la literatura documenta a ≥ 5 por día en el E-mini vive por debajo de los 10 segundos —la cerradura del reglamento— y por debajo de los 60 segundos —la resolución del dato—; y entre un minuto y media hora, a ≥ 5 por día, no encontré nada publicado sobre el E-mini. La única clase con la forma correcta (libro y flujo) la casa ya la midió en cero en su versión de 30 segundos.**

**Es un cero distinto del de `D13`.** Aquél decía *"no las podíamos medir"*. Éste dice **"no existen
candidatas publicadas de la forma que sí podríamos medir"** —con el límite de búsqueda declarado
arriba—.

| | inventario 1 (`D13`) | **inventario 2** |
|---|---|---|
| candidatas catalogadas | 11 | 9 clases |
| pasan el filtro previo | 11 (F1'-F16) | **0** (F17) |
| por qué mueren | el instrumento no las ve | **no tienen la forma que el instrumento ve** |

# Lo que mataría este cero, escrito antes de que alguien lo intente

1. **Un paper sobre el E-mini con horizontes de 1 a 30 minutos, ≥ 5 señales por día del mismo
   mecanismo, y magnitud publicada ≥ 1 tick neto por operación.** No lo encontré; SSRN cerrado dos
   veces acota lo que pude ver. Dónde viviría: *Journal of Futures Markets*, *JFQA*, *Journal of
   Financial Markets*, 2015-2025.
2. **Que `COSTO_OP` baje** con la verificación de G: el umbral de F17 bajaría de 5 hacia 2-3 por día y
   la clase 5 (horario) dejaría de necesitar apilamiento… no: seguiría siendo un mecanismo por hora.
   **No la salva.**
3. **Que la casa produzca una hipótesis propia de esa forma con el `mbo` de G** —eso no es literatura,
   es el generador viejo, y cuesta un cartucho.

**Costos:** dinero cero, cartuchos cero, K en 261. Tiempo de Roberto: leer.
