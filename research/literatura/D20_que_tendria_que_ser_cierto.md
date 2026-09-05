# D20 — Si el profesional gana sólo en el diferencial y nosotros no podemos cobrarlo, ¿queda alguna forma de candidata? La lista de lo que tendría que ser cierto, con lo medido y lo no medido.

**VENTANA L. NO MIDE NADA. K sigue en 261.** Sin esperanza: la lista, y al lado de cada línea si está
medida.

---

# 1. Lo que ya está establecido, y de dónde

| hecho | fuente | ¿medido en el ES? |
|---|---|---|
| la ganancia bruta del creador de mercado por operación es la pérdida neta del tomador promedio: `−€0,88` en Menkveld | `L13`, identidad contable | la identidad vale en cualquier mercado; el número es holandés |
| las órdenes en reposo son seleccionadas en contra, hasta las de la alta frecuencia | `L14` (NASDAQ), `L13` (todas las acciones), **G 3b (ES)** | **sí**: markout pasivo a 30 s de 0,00 a +0,08 pt; negativo a 60-300 s |
| cruzar cuesta ~1 tick y la ventaja exigida es ~1 tick neto por operación a cualquier frecuencia | **G `e288ffc`** | **sí** |
| pasivo neto de comisión: negativo en todos los días medidos | `D17` §4 sobre G | **sí**, seis días |
| la información que hay a escala de segundos la toma el escalón 1 | `L14`, `H01` Hecho 1 | acciones; en el ES, la latencia sí (< 200 ms) |
| tenencia obligada > 10 s; nada abierto a las 16:45; "HFT" prohibido sin definición | `R03`, `F17` | reglamento, leído |

**Conclusión de partida:** el tomador promedio pierde por identidad, y el proveedor pierde por selección
adversa. **Cualquier candidata tiene que ser un tomador NO promedio.**

# 2. Lo que tendría que ser cierto, todo a la vez

| # | condición | **¿está medida?** |
|---|---|---|
| **1** | **Existe una señal, computable antes de cruzar, tal que el precio continúa en nuestra dirección más de 1 tick neto en promedio** dentro de la tenencia. Es *ser más informado que el tomador promedio por más que el diferencial entero* | **el requisito sí** (G: 0,98 ticks). **La existencia NO**: `INVENTARIO_2` no encontró ninguna publicada para el ES a ≥ 5/día; **G midió la clásica —el desbalance del libro— en cero** (ρ de −0,02 a +0,01 a 30 s) |
| **2** | **La señal sobrevive a nuestra latencia**: lo que queda después de que el escalón 1 tomó lo suyo (segundos) tiene que seguir valiendo un tick cuando llegamos | **NO.** El escalón 3 no está medido (`H01` hueco, `F16` fila 5). Lo que se sabe: la alta frecuencia predice "a segundos" (`L14`) y la firma nos obliga a > 10 s |
| **3** | **La señal es lenta**: persiste más de 10 s (R2) y menos del cierre de 16:45, en una tenencia donde el movimiento típico todavía es ≥ 1 tick con holgura —o sea **minutos, no segundos**: a 30 s haría falta capturar el 57 % del movimiento (`D17`) | **el requisito sí** (`D17`). **La existencia NO**: entre 1 y 30 minutos, ≥ 5/día, no hay nada publicado sobre el ES (`D18`) |
| **4** | **No es un artefacto de la regla de salida** (bracket, tiempo, censura) | **sí**: los diez controles del juez (`49bc992`), 9/10 y 10/10 |
| **5** | **La firma deja cobrar**: R7 no la bloquea | **medido en flujo sintético** (`6d4bc1c`): a 4 minis, un candidato que funciona llega al objetivo en 2 días y el tope del 35 % bloquea el 99,8 %. **Una candidata buena y rápida se bloquea por buena.** Se resuelve con tamaño y ritmo, no con la candidata |
| **6** | **La zona gris no la alcanza**: la firma no llama "HFT" a una tenencia de minutos | **no medible**: riesgo de negocio (`F17` §3) |

**Y las tres salidas que NO son "ser mejor tomador", con su estado:**

| salida | qué tendría que ser cierto | estado |
|---|---|---|
| **cobrar el diferencial** en vez de pagarlo | que la selección adversa devuelva menos que la comisión (0,115 pt) | **medida y muerta**: G 3a/3b, y `L13`/`L14` dicen que le pasa a todos |
| **bajar el costo** por operación | reembolsos, comisión menor, o un micro más barato por exposición | **medido**: el micro cuesta **2,01× más** por exposición (`e288ffc`); reembolsos no existen para una cuenta minorista de futuros |
| **operar donde el tomador promedio NO es el de siempre**: ventanas de flujo obligado (rebalanceos, fixings, publicaciones) | que ahí el proveedor esté ausente o el flujo sea desinformado y grande | **medido/cerrado**: es el inventario viejo entero, 1/día, ciego (`D13`, `D14`) |

# 3. La respuesta, sin esperanza

> ## **Queda UNA forma lógica: un tomador que, a tenencias de minutos, esté informado por más de un tick neto respecto del creador de mercado, a ≥ 5 operaciones por día del mismo mecanismo. Todo lo que la casa midió (3a, 3b, la tabla de costos, los controles) y todo lo que se leyó (Menkveld, Brogaard, Boyarchenko, Gao, nueve clases del inventario 2) dice que esa forma NO tiene ningún ejemplar conocido. Las condiciones 1 y 3 no están medidas como existencia; están medidas como requisito, y ningún objeto cumple el requisito.**

**Lo que convertiría la lista en una candidata, y lo que cuesta:** una señal propia, sobre el `mbo` o
`tbbo` de G, cuyo markout a 1-5 minutos después de cruzar supere 1 tick más comisión en 2016-2019. **Eso
es el generador viejo —una hipótesis nuestra— y cuesta un cartucho.** No es literatura, y este documento no
la propone: dice qué forma tendría que tener para que valiera el cartucho.

**Costos:** dinero cero, cartuchos cero, K en 261.
