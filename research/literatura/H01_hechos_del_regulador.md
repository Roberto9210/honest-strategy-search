# H01 — Hechos medidos publicados por los economistas del regulador

**VENTANA L. NO MIDE NADA. K sigue en 261.**

**Cuarto generador, y con el objetivo cambiado por Roberto, que es lo que lo hace valioso:**

> **No estamos cortos de ideas: estamos cortos de HECHOS MEDIDOS.** Llevamos 261 hipótesis nuestras y
> 11 de la literatura. Lo que frena no es la falta de ideas, es que casi ninguna se puede medir
> contra el piso. **Una fuente que produce hechos medidos sobre el instrumento exacto que operamos,
> sin costo en dinero, ataca el cuello de botella real.**

**Por eso esta fuente NO se evalúa como generadora de candidatas. Se evalúa como fuente de hechos, y
se apunta a lo que ya tenemos abierto.**

**Alcance: máximo cinco documentos. Van dos.**

---

# HECHO 1 — Latencia de respuesta en el E-mini, y confirma a la VENTANA G

**Fuente:** Oficina del Economista Jefe, Comisión de Comercio de Futuros de Materias Primas.
*"Speed and Latency in Treasury and e-Mini Futures Contracts – Part 2"*.
`cftc.gov/sites/default/files/idc/groups/public/@economicanalysis/documents/file/oce_speedandlatency2.pdf`
**Datos: registro de auditoría del CME.** El documento referencia hechos de 2013 a 2016; **no pude
fijar la ventana exacta de la muestra y lo digo en vez de suponerla.**

## El número

**Midiendo el tiempo entre recibir un mensaje de ejecución y enviar una orden nueva:**

| grupo | mediana de respuesta |
|---|---|
| **operadores algorítmicos por cuenta propia** | **menos de 200 milisegundos** |
| operadores manuales por cuenta propia | **más de 9 segundos** |

## Por qué importa acá

**La VENTANA G midió que el tope del ES vive en 113 a 197 milisegundos**, y que la latencia es
inmaterial para los llenados hasta 250 ms.

> ## **Los 113-197 ms de la casa caen justo dentro del "menos de 200 ms" que el regulador mide como mediana del grupo más rápido. Es la TERCERA vez que un número de este proyecto se confirma desde afuera**, después del costo del diferencial contra Kurov y del umbral de 3,0 desvíos contra Harvey, Liu y Zhu.

## Y un segundo hecho del mismo documento, que es metodológico y vale más

**Cuando se pondera por PARTICIPANTE en vez de por OBSERVACIÓN, la mediana del grupo algorítmico
sube por un factor de 25, de menos de 200 milisegundos a poco más de 5 segundos.**

**Es exactamente la familia de `A03`: una variable tratada como constante.** Agrupar observaciones de
participantes heterogéneos y reportar una mediana **da un número que describe a los más activos, no
al participante típico.**

> **Cualquier medición nuestra que promedie sobre eventos generados por poblaciones distintas tiene
> este problema, y el factor puede ser de 25.**

## Lo que lo mataría

**El período.** Un número de latencia de 2013-2016 no describe el mercado de 2019, y menos el de
2026. **La confirmación de los 113-197 ms es de orden de magnitud, no de precisión.**

---

# HECHO 2 — Reglas de liquidación al cierre. **Extraído y con su límite escrito.**

**Fuente:** Onur y Reiffen, Oficina del Economista Jefe de la misma comisión,
*"The Effect of Settlement Rules on the Incentive to Bang the Close"*.
`cftc.gov/sites/default/files/2019-05/onur_reiffen_Manuscript_ada.pdf`

**Datos: conjunto propietario de transacciones individuales en futuros de maíz de la división del
Chicago Board of Trade, período MARZO-JUNIO DE 2012**, alrededor de un cambio de regla de
liquidación.

## Qué establece

**Que el diseño de la regla de liquidación —cómo se calcula el precio de cierre a partir de las
operaciones de la ventana final— cambia el incentivo a operar en esa ventana.** Relaciona posiciones
con patrones de negociación usando datos que identifican al participante.

## Lo que lo mata para nosotros, y lo escribo yo

> **Es maíz, es 2012, y es alrededor de un cambio de regla específico de ese contrato.** Un número de
> ese mercado y ese año **no describe la ventana de liquidación del ES en 2019**.

**Se anota como hecho de estructura de la categoría (A) de `F14` —el diseño de la regla de
liquidación afecta el comportamiento en la ventana final— y NO como número transferible.**

**Toca a la familia de L10 y a cualquier candidata que opere cerca del cierre, pero como advertencia
cualitativa: la ventana de liquidación no es un momento neutro.**

---

# HECHO 3 — Lo que un participante chico ve del libro del E-mini

**Fuente:** Fett, Nicholas y Haynes, Richard, Oficina del Economista Jefe de la Comisión de Comercio
de Futuros. *"Liquidity in Select Futures Markets"*.
`cftc.gov/sites/default/files/idc/groups/public/@economicanalysis/documents/file/oce_liquidityfuturesmarkets.pdf`
**Datos: E-mini del S&P 500, bono a diez años y crudo, de 2013 a mediados de 2016**, con el libro
muestreado el **primer martes y el primer jueves de cada mes**.

| hecho | número |
|---|---|
| niveles del libro que publica el canal público del **E-mini** | **cinco** mejores ofertas y demandas |
| lo mismo para bono a diez años y crudo | **diez** |
| ventana de su medida de profundidad | 8:00 a 16:00 hora de Chicago, tres mejores niveles |

## Y el hecho que confirma nuestro modelo de costo

**Los autores separan explícitamente por tamaño de operación:**

> **para operaciones muy chicas** —que representan el interés de firmas pequeñas o de operadores
> minoristas individuales— **el costo se representa mejor por el diferencial medio de compra y
> venta**, porque una operación agresiva chica se ejecuta contra una orden **del tope del libro**.
> La profundidad importa para operaciones que tienen que caminar el libro.

> ## **Roberto opera de uno a cuatro contratos: está exactamente en la categoría "muy chica" que el regulador define. Su costo es el diferencial, no la profundidad. Eso confirma desde afuera el modelo de costo que la VENTANA G usa —medio diferencial por cruzar— y es la CUARTA confirmación externa de un número o un criterio de esta casa.**

**Y observan que las reducciones de profundidad del período fueron **especialmente en el E-mini**, y
que coinciden con episodios de volatilidad alta.

## Lo que lo mataría

**El período, 2013 a mediados de 2016.** Nuestro rango medible es 2016-2019, así que **se solapa
apenas en el borde.** La afirmación sobre la categoría de tamaño es estructural y no depende del año;
**las cifras de profundidad sí.**

---

# HUECO NOMBRADO — el tercer escalón de latencia, que nadie midió

**Roberto corrigió mi lectura del Hecho 1 y la corrección importa.**

**Yo escribí que los 9 segundos del operador manual describen a Roberto. No lo describen, y los 200
milisegundos tampoco.**

| escalón | quién | latencia | fuente |
|---|---|---|---|
| **1** | firmas algorítmicas por cuenta propia, con la máquina dentro del edificio del mercado | **menos de 200 ms**, mediana | Hecho 1, regulador |
| **2** | operadores manuales por cuenta propia | **más de 9 s**, mediana | Hecho 1, regulador |
| **3** | **NinjaTrader en una máquina de casa, pasando por el router de la firma de fondeo** | **SIN MEDIR** | **nadie** |

> ## **El proyecto va a automatizar, así que no es el escalón 2. Y no está colocado, así que no es el 1. El escalón que le corresponde no está medido ni escrito en ningún lado.**

**No lo mido yo: no es mi territorio. Queda como hueco nombrado para la VENTANA G.**

## Qué candidatas dependerían de la respuesta

**Y acá hay una buena noticia que conviene decir con el hueco:**

| candidata | ¿depende de la latencia? |
|---|---|
| L01, L07, L08, L10 | **NO.** Entran y salen a **horas de reloj anunciadas de antemano**. No hay que reaccionar a nada |
| **L03** | **PARCIALMENTE.** Su salida es el promedio ponderado de la ventana de 5 segundos a 1 minuto **después** de una publicación. La hora se conoce, pero **el mercado se mueve violentamente ahí y la calidad del llenado depende de la latencia** |

> ## **El hueco es real y hoy no bloquea a ninguna candidata del inventario, porque todas entran a hora fija. Bloquearía a cualquier candidata futura que exija REACCIONAR a un evento.**

**Ésa es la razón para medirlo antes de necesitarlo y no después: define qué clase de candidata puede
entrar al inventario en el futuro.**

---

# CORRECCIÓN — la frontera del factor 25, resuelta por Roberto

**Yo dejé el factor 25 como advertencia general. Roberto le puso la frontera correcta y la escribo
acá porque es la regla, no el caso:**

| pregunta | ponderación correcta | ¿aplica el factor 25? |
|---|---|---|
| **"qué me pasa a mí por evento"** | **por observación** | **NO** |
| "qué hace el miembro típico de una población" | por participante | **SÍ** |

**Nuestras mediciones de costo son del primer tipo.** Cuando la VENTANA G mide el *markout* posterior
a un llenado nuestro, **cada llenado es una operación nuestra**, así que ponderar por llenado es lo
correcto y el factor no aplica.

**Dónde SÍ aplicaría: si alguna vez estimamos algo sobre la POBLACIÓN DE CONTRAPARTES** — por ejemplo
qué fracción del flujo es informado. **Ahí la unidad es el participante y no la observación.**

**Queda anotado con esa frontera y no como advertencia general.**

---

# BALANCE de la fuente, con tres de cinco documentos

| | |
|---|---|
| **hechos con número extraídos** | **4**: latencia de 200 ms, factor 25 de ponderación, cinco niveles del libro del E-mini, y la categoría de tamaño que define el costo |
| hechos cualitativos | 1: el diseño de la liquidación afecta el comportamiento en la ventana |
| **confirmaciones externas de números de la casa** | **2**: la latencia y el modelo de costo. Son la **tercera y la cuarta** del proyecto |
| huecos nombrados | **1**: el tercer escalón de latencia, que no bloquea a ninguna candidata actual |
| candidatas producidas | **0**, como estaba previsto |

**La fuente rinde para lo que Roberto la apuntó y no rinde para lo otro, exactamente como se
esperaba.**

**Y el hallazgo que no esperaba: el hecho más útil de los dos documentos no es sobre el mercado, es
sobre CÓMO SE MIDE.** El factor 25 entre ponderar por observación y ponderar por participante es una
advertencia metodológica que aplica a mediciones nuestras, no a candidatas.

## Costos

| | |
|---|---|
| **dinero** | **cero**: los dos documentos son públicos en el sitio del regulador |
| **cartuchos** | **cero**: leer y extraer hechos no registra ninguna hipótesis. K sigue en 261 |
| **tiempo de Roberto** | leer este documento |
