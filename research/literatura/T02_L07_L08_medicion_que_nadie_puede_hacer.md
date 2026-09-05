# T02 — L07 y L08: la corrección que el perfil del ES NO les hace, y quién podría hacérsela

**VENTANA L. NO MIDE NADA. K sigue en 261. EL RANKING SIGUE CONGELADO.**

**Roberto lo vio en la tabla de `T01` y yo no saqué la consecuencia:** el perfil de volatilidad
intradiaria del ES descongela a **tres** candidatas —L01, L03, L10—, no a cinco. **L07 vive en el
pico local del yen y L08 en el pico de divisas de Londres. La U del ES no las toca.** Sus márgenes
de 1,72 y 1,33 (`D06`) salen del mismo escalado uniforme equivocado, y la medición que ya llegó no
los corrige.

> **Y la candidata que hoy va primera entre los sobrevivientes —L07, por `D09`— es la que tiene la
> corrección menos planificada.**

---

# Primero, un hecho que cambia el estado de las otras tres: el perfil del ES YA ESTÁ EN EL REPO

**Commit `7461919` de la VENTANA G, `salida_perfil_intradia.txt`.** ES 1-min 2016-2019, 1.007 sesiones,
cajas de media hora por reloj de Chicago, desvío en puntos básicos del nocional.

| caja | hora del este | desvío medido | contra raíz del tiempo (11,58 pb) | quién vive ahí |
|---|---|---|---|---|
| #31 | **09:30 – 10:00** | **23,39 pb** | factor **2,02**, la más agitada del día | **L03** |
| #42 | 15:00 – 15:30 | 16,93 pb | 1,46 | L10, primera mitad |
| #43 | **15:30 – 16:00** | **20,92 pb** | 1,81 | **L01**, y L10 segunda mitad |
| #15 | 00:30 – 01:00 CT | 5,45 pb | 0,47, la más calma | nadie |

**No aplico estos números a ningún margen: la instrucción es que el ranking no se toca hasta que
Roberto lo descongele.** Los dejo transcriptos para que la corrección de las tres del ES sea de diez
minutos cuando él lo decida. **Para L10 hace falta una decisión que no es mía: la caja de una hora
no está en la tabla de G; combinar #42 y #43 exige un supuesto sobre la correlación entre las dos
medias horas.**

---

# (a) Qué medición exacta necesita L07

| | |
|---|---|
| **instrumento** | **6J**, futuro de yen del CME, contrato cercano. *(El paper mide USD/JPY spot en EBS; el 6J cotiza yenes por dólar, la dirección está invertida y el signo de la regla se invierte con ella.)* |
| **franja** | **00:50:00 – 01:00:00 GMT**, con el cambio de lado en 00:55:00. Cinco minutos antes y cinco después del fixing de Tokio de las 9:55 JST |
| **qué se mide** | el **desvío del retorno de diez minutos** de esa ventana exacta —o mejor, de sus dos mitades por separado, porque la regla es larga la primera y corta la segunda— **sobre todos los días hábiles de 2016-2019**, ~1.000 días |
| **por qué todos los días y no sólo gotobi** | el desvío es propiedad de la ventana, no del día; y `P05` usa los ~1.000 días, no los 286 gotobi |
| **período** | **2016-2019.** Es el único período en que el resto del proyecto está calibrado, y el paper termina en 2013 |

**Lo que hoy tiene en su lugar: `σ` de 4,6 a 8 pb en `P05` y `D06`, que salió de repartir un desvío
diario de USD/JPY de ~55 pb en forma pareja.** Y esa ventana **contiene un pico transitorio
documentado** (Ito y Yamada: "varios puntos básicos en pocos segundos" en 00:55 GMT). El desvío de
una ventana que contiene un pico **no es el promedio del día: es más alto**, en una proporción que
nadie midió.

# (b) Qué medición exacta necesita L08

| | |
|---|---|
| **instrumento** | **6E** como principal, y los otros cinco de la cotización de G (`salida_cotizacion_divisas.txt`) si se quiere el panel |
| **franja** | **15:00 – 16:00 hora de Londres**, la hora previa al fixing WM/Reuters. **En GMT cambia con el horario de verano británico**: 14:00-15:00Z en verano, 15:00-16:00Z en invierno. G ya lo manejó fecha por fecha en la cotización |
| **qué se mide** | el **desvío del retorno de una hora** de esa ventana, **sobre los 47 últimos días hábiles de mes con datos** de 2016-2019 (2018-03-30 no operó) |
| **por qué sólo los 47 eventos** | porque la prueba usa sólo esos días, y con `n = 47` el error relativo del propio `σ` es ~10 %, tolerable. **Medirlo sobre todos los días sería más preciso y respondería otra pregunta**: el fin de mes es precisamente el día en que el flujo que buscamos infla la varianza |
| **período** | 2016-2019, y todo es posterior a la reforma WM/Reuters de 2015, que cambió la ventana del fixing de uno a cinco minutos |

**Lo que hoy tiene en su lugar: `σ` ≈ 11,4 pb en `D06`, de un desvío diario de divisas repartido
en forma pareja.** Y la hora previa al fixing de Londres es **el tramo de mayor volumen del día de
divisas** (solapamiento Londres–Nueva York), así que el desvío verdadero es mayor.

---

# (c) ¿Existe publicado? **El PATRÓN sí. Un NÚMERO utilizable, no.**

Busqué en tres papers, dos de ellos ya en el repo:

| fuente | qué tiene | ¿sirve como `σ` de la ventana? |
|---|---|---|
| **Ito y Hashimoto**, NBER 12413, 2006. EBS, USD/JPY y EUR/USD, **1999-2001**, 1 minuto, volatilidad = media del retorno absoluto de 1 minuto por hora GMT | **Confirma el PATRÓN**: la volatilidad de USD/JPY salta en la hora GMT 0 (apertura de Tokio, donde vive L07) y tiene picos en las horas 12-14 en verano y 13-15 en invierno (solapamiento Londres–NY, donde vive L08). Los valles: horas 3, 10-11, 21 | **NO.** Las cifras están en figuras, escaladas ×500, sin tabla. Y son de 1999-2001 |
| **Ito y Yamada** (el paper de L07), EBS 2006-2013 | Tabla 6: desvíos de **2 a 2,6 pb**, pero son del **gap entre la tasa de fixing y el precio de mercado**, no del retorno de diez minutos | **NO.** Es otro objeto |
| **Melvin y Prins** (el paper de L08), 2000-2012 | Tabla 1: regresión del **logaritmo del cociente** entre la volatilidad 15-17 GMT y la de 08-15 GMT | **NO.** Es un cociente, sin el nivel |
| Andersen y Bollerslev 1998, DM/$ 1992-93 | el trabajo clásico del perfil intradiario de divisas | **no pude extraer el texto** del PDF; no le atribuyo números |

> ## **Conclusión de (c): la literatura confirma que las dos ventanas son picos, y no da ningún desvío en puntos básicos de la ventana exacta. No hay número publicado que ahorre la medición.**

---

# (d) ¿El juez puede cargar 6J o 6E? **NO. Y no es sólo el juez.**

Lo leí en el código de G y en su nota `PARA_VENTANA_L.md`, sección 4, **sin tocar nada**:

| pieza | estado | fuente |
|---|---|---|
| `cargar_mercado()` | llama a `razon_escalas.cargar_con_sesion()` → `load_databento()`: **sólo lee ES 1-min** | `juez.py` línea 241 |
| instrumentos completos del juez | `COMPLETOS = ("ES", "MES")` | `instrumentos.py` línea 151 |
| plomería por instrumento | **"NO IMPLEMENTADA y marcada"**; cuatro constantes se leen de los globales del ES | `juez.py` líneas 429-430; `PARA_VENTANA_L.md` §4 |
| ficha de calibración de 6E/6J | empezada: punto, tick, sesión. **Falta la comisión de divisas y el medio-spread por régimen** | `PARA_VENTANA_L.md` §4 |
| **los datos** | **cotizados, no comprados.** L08: USD 0,25. L07: USD 0,06. Crédito disponible: USD 98,92 | `salida_cotizacion_divisas.txt` |
| el script del perfil | `perfil_volatilidad_intradia.py` está cableado a ES 1-min | su encabezado |

> ## **L07 y L08 no están "esperando una medición". Están esperando una medición que HOY NADIE PUEDE HACER: no hay datos comprados, ningún cargador lee otra cosa que ES, y el juez no tiene la plomería.**

**Y separo las dos cosas, porque cuestan distinto:**

| para | hace falta | costo |
|---|---|---|
| **medir `σ`** de las dos ventanas | comprar (USD 0,31, decisión de Roberto) + un cargador de `ohlcv-1m` de divisas (territorio de G, chico) | centavos y una tarde de G |
| **juzgar** L07 o L08 | lo anterior + comisión de divisas (una lectura) + medio-spread por régimen (compra `tbbo`, cotizada USD 0,48) + la plomería por instrumento **que está marcada como no implementada** | la misma compra, más trabajo de G de tamaño que no estimo |

---

# Lo que esto le hace al inventario, dicho sin reordenar

**Las cinco sobrevivientes se parten en dos grupos que no eran visibles hasta hoy:**

| grupo | candidatas | corrección de margen | quién la hace |
|---|---|---|---|
| **A** | L01, L03, L10 | **el número ya existe** en el repo desde `7461919` | Roberto, cuando descongele |
| **B** | L07, L08 | **nadie puede hacerla hoy** | compra + cargador + G |

**No digo cuál es la mejor candidata: es exactamente lo que está congelado.** Digo que **el grupo A
puede tener su orden correcto mañana y el grupo B no**, y que si el orden se descongela sólo para A,
L07 queda comparada con su margen viejo contra márgenes nuevos. **Eso sería una comparación entre
calibraciones distintas, y `F13` 6b lo prohíbe.** La salida limpia es descongelar los cinco juntos
o declarar los dos grupos por separado.

**Costos:** dinero **cero** —no compré nada; la compra es de USD 0,31 y la decide Roberto—, cartuchos
**cero**, K en 261. Tiempo de Roberto: leer y decidir la compra.
