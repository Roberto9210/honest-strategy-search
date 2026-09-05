# H01 — Hechos medidos publicados por los economistas del regulador

**VENTANA L. NO MIDE CANDIDATAS; corre CONTROLES DEL INSTRUMENTO desde el 2026-09-05 (rol ampliado por Roberto, ver `INDICE`). K sigue en 261.**

**Cuarto generador, y con el objetivo cambiado por Roberto, que es lo que lo hace valioso:**

> **No estamos cortos de ideas: estamos cortos de HECHOS MEDIDOS.** Llevamos 261 hipótesis nuestras y
> 11 de la literatura. Lo que frena no es la falta de ideas, es que casi ninguna se puede medir
> contra el piso. **Una fuente que produce hechos medidos sobre el instrumento exacto que operamos,
> sin costo en dinero, ataca el cuello de botella real.**

**Por eso esta fuente NO se evalúa como generadora de candidatas. Se evalúa como fuente de hechos, y
se apunta a lo que ya tenemos abierto.**

**Alcance: Roberto lo amplió a ocho documentos más sobre los tres iniciales. Van siete: seis con
hecho y uno muerto por instrumento. Haynes y Roberts, que no bajaba por tamaño, bajó por otra vía
y es el Hecho 6.** Criterio de muerte, fijado por él: **si no describe nuestro
instrumento o nuestro período, se mata y se dice por qué.**

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

# HECHO 4 — Qué fracción del volumen del E-mini es de alta frecuencia, y cómo cambió

**Fuente:** Coughlan, Ryan y Orlov, Alexei, Comisión de Comercio de Futuros, *"High-Frequency Trading
and Market Quality: Evidence from Futures Markets"*, julio de 2022. SSRN 4069573.
**Datos: registro de transacciones del regulador, nueve contratos, 2012 a 2021.** Usan como
experimento natural el cambio de 2015 en la liquidación de los agrícolas del CME.

## Los números para nuestro instrumento, y sólo para el nuestro

| E-mini del S&P 500 | participación de alta frecuencia en el volumen |
|---|---|
| **2012** | **31,8 %** |
| **2021** | **49,7 %** |
| promedio del período | **45,0 %** |
| variación | **+56,3 %** |

**El período cubre el nuestro entero: 2016-2019 está adentro de 2012-2021.** Es el primer documento
del regulador que describe nuestro instrumento en nuestro período **sin borde.**

## Por qué importa acá

**Es un número de `F10` —cuánta gente adentro— medido por quien tiene el registro completo.** Cerca
de la mitad del volumen del ES en nuestro período está del lado de lo que Coughlan y Orlov llaman alta
frecuencia. *(Que ese grupo sea el de los "menos de 200 ms" del Hecho 1 es una identificación mía entre
dos definiciones de dos documentos distintos. **Falla** si la definición de Coughlan y Orlov incluye
cuentas que no son las del Hecho 1. Ver `A06`.)*

**Y toca a L03 por donde ya estaba tocada:** su salida es una ventana de segundos después de una
publicación. **La contraparte en esa ventana es, por construcción, de este grupo.**

**Frontera del factor 25, aplicada:** el 45 % es una fracción del VOLUMEN, o sea ponderada por
observación. **Describe lo que un contrato nuestro encuentra enfrente, que es la pregunta correcta
para nosotros.** No describe al participante típico, y no lo necesitamos.

## Lo que lo mataría

**La definición de alta frecuencia del paper.** No la transcribo porque no la tengo fijada del texto,
y una definición por umbral de mensajes o de inventario cambia la fracción. **El 45 % es "su
definición", y hasta que la copie textual se lee como orden de magnitud.**

---

# HECHO 5 — Quiénes son los de alta frecuencia en el E-mini, con la definición copiada textual

**Fuente:** Kirilenko, Kyle, Samadi y Tuzun, *"The Flash Crash: The Impact of High Frequency Trading
on an Electronic Market"*, trabajo bajo contrato de la Oficina del Economista Jefe, autorizado para
distribución el 21 de febrero de 2014. SSRN 1686004.
**Datos: registro de auditoría del E-mini del S&P 500, cuentas identificadas, 3 al 6 de mayo de 2010.**

## Los números, y son del instrumento correcto

| | número |
|---|---|
| cuentas que operaron el 6 de mayo de 2010 | **15.422** |
| cuentas clasificadas como alta frecuencia | **16** |
| cuentas clasificadas como creadores de mercado | 179 |
| **participación de las 16 en el volumen**, 3 al 5 de mayo | **34,22 %** |
| participación de los 179 creadores de mercado | 10,49 % |
| vida media del inventario de las 16 | **unos 140 segundos por regresión, "probablemente menos"** |

## La definición, copiada porque es la que le faltaba al Hecho 4

Una cuenta es alta frecuencia o creador de mercado si y sólo si: **(1)** operó 10 contratos o más en
al menos uno de los tres días previos; **(2)** el valor absoluto de su posición neta al cierre **no
supera el 5 % de su volumen del día**; **(3)** la desviación de su inventario intradía respecto del
cierre, sumada sobre los 405 minutos, **no supera el 1,5 % de su volumen del día**. De las 195
cuentas que cumplen las tres, **las 16 con más operaciones son alta frecuencia**, y el corte está
donde hay un salto grande entre la cuenta 16 y la 17.

## Por qué importa acá

**Dieciséis cuentas sobre 15.422 son el 0,10 % de las cuentas y el 34 % del volumen.** Es el mismo
patrón que el crudo de Raman, Robe y Yadav y que el factor 25 del Hecho 1, **ahora en NUESTRO
instrumento.**

**Y engancha con el Hecho 4 sin que lo haya buscado:** alta frecuencia más creadores de mercado
suman **44,7 %** del volumen en 2010; Coughlan y Orlov miden **45,0 %** de promedio para 2012-2021.
**Son definiciones distintas y no se suman; que caigan cerca es orden de magnitud, no confirmación.**

## Lo que lo mata, y lo mata para los números

> **El período: cuatro días de mayo de 2010, uno de ellos el Flash Crash.** Ningún número de acá
> describe 2016-2019. **Lo que sobrevive es la ESTRUCTURA** —cómo se define alta frecuencia con
> inventario y volumen, y que una fracción ínfima de cuentas es un tercio del volumen— y **la
> definición sirve para leer el Hecho 4.**

---

# HECHO 6 — Cuánto del E-mini es automático, cuánto es de cuentas chicas, y qué tan rápido netean las grandes

**Fuente:** Haynes, Richard y Roberts, John S., Oficina del Economista Jefe, *"Automated Trading in
Futures Markets — Update"*, 29 de marzo de 2017. Actualiza el documento blanco de marzo de 2015.
`cftc.gov/.../oce_automatedtrading_update.pdf` (11,6 MB; no lo bajó la herramienta de lectura y lo bajé
con `curl`).
**Datos: transacciones del CME, dos períodos: 12-nov-2012 → 31-oct-2014 y 1-nov-2014 → 31-oct-2016.**
"Automático" es la marca del propio CME sobre cada lado de cada operación.

## Los números para el E-mini del S&P 500, y sólo para él

| Tabla 3 — por tipo de las dos puntas | 2012-14 | **2014-16** |
|---|---|---|
| automático contra automático | 43,4 % | **50,6 %** |
| automático contra manual | 42,6 % | **39,3 %** |
| manual contra manual | 13,8 % | *(ilegible en mi extracción; ~10 % por diferencia)* |

| Tabla 5 — por tamaño de cuenta (grande = ≥ 0,5 % del volumen del día) | 2012-14 | **2014-16** |
|---|---|---|
| cuentas **chicas**, número | 126.675 | **143.363** |
| volumen de las chicas, automático / manual | 19,2 % / 29,3 % | **19,5 % / 25,5 %** |
| cuentas **grandes**, número | 469 | **423** |
| volumen de las grandes, automático / manual | 45,5 % / 5,8 % | **50,8 % / 4,0 %** |

| Tabla 8 — cuentas grandes automáticas: fracción de su volumen que **netean** dentro de la ventana | 2012-14 | **2014-16** |
|---|---|---|
| en **1 minuto** | 57,7 % | **66,8 %** |
| en 3 minutos | 69,3 % | 77,0 % |
| en 5 minutos | 73,5 % | 80,4 % |
| en el día entero | 86,7 % | 90,8 % |

## Por qué importa acá, en tres líneas

1. **Roberto está en la fila "cuentas chicas, manual"** —25,5 % del volumen— y al automatizar pasa
   a "chicas, automático", 19,5 %. **Es la primera vez que una fuente pone un número a la población
   a la que él pertenece, en su instrumento.**
2. **423 cuentas hacen el 54,8 % del volumen; 143.363 hacen el 45 %.** El factor 25 otra vez, con
   el registro completo del CME y no una muestra.
3. **Tabla 8 es Kirilenko en la caja de herramientas del regulador**: `mín(compras, ventas) / volumen`
   por ventana. **Las grandes automáticas netean dos tercios de su volumen en un minuto.** Para `D11`
   y `D12`: netear en un minuto es lo que se mide; que sea *liquidación de inventario* es lectura
   mía, porque netear compras y ventas dentro de un minuto es consistente con creación de mercado
   **y** con absorción-y-liquidación, y la tabla no las distingue. *(**Falla** si el neteo viene de
   cotizar los dos lados y no de deshacer inventario. Ver `A06`.)* **Y no dice si ocurre en 5 o en 50
   segundos**, que es lo que `D11` necesita.

## Lo que lo mataría

**El período termina en octubre de 2016: se solapa con el nuestro en diez meses.** El instrumento es
el correcto. **Y "automático" no es "alta frecuencia"**: el 50,6 % de Tabla 3 y el 45 % de Coughlan
y Orlov son definiciones distintas, **y que caigan cerca no es confirmación de nada.**

---

# MUERTO — Raman, Robe y Yadav, *"Electronic Market Makers, Trader Anonymity and Invisible Liquidity"*, regulador, 2012

**Instrumento: crudo WTI. Períodos: 2006, 2008 y 2011.** Cincuenta y dos creadores de mercado
electrónicos —definidos como más de 2.000 operaciones por día y menos del 5 % de la posición al
cierre— son el **0,35 % de las cuentas y cerca del 50 % del volumen.**

> **Se mata por instrumento: es crudo, no E-mini. Ningún número se transfiere.**

**Lo único que queda, y como estructura, no como número:** el 0,35 % de las cuentas hace el 50 % del
volumen. **Es el factor 25 otra vez, visto desde el lado de las cuentas.** Cualquier cosa que
promedie "por participante" en un mercado así describe al 99,65 % que hace la otra mitad.

---

# BALANCE de la fuente, con siete documentos

| | |
|---|---|
| **hechos con número extraídos** | **7**: latencia de 200 ms, factor 25 de ponderación, cinco niveles del libro del E-mini en 2013-2016, la categoría de tamaño que define el costo, **45 % de volumen de alta frecuencia en el ES, 2012-2021**, **16 cuentas = 34 % del volumen en 2010, con la definición textual**, y **la población de Roberto: cuentas chicas manuales = 25,5 % del volumen del E-mini en 2014-16, y las grandes automáticas netean el 67 % en un minuto** |
| hechos cualitativos | 1: el diseño de la liquidación afecta el comportamiento en la ventana |
| **confirmaciones externas de números de la casa** | **2**: la latencia y el modelo de costo. Son la **tercera y la cuarta** del proyecto |
| huecos nombrados | **1**: el tercer escalón de latencia, que no bloquea a ninguna candidata actual |
| **documentos muertos por instrumento** | **1**: Raman, Robe y Yadav, crudo |
| candidatas producidas | **0**, como estaba previsto |
| **hechos que hay que corregir por fecha** | **1**: los cinco niveles del Hecho 3 eran de 2013-2016; **hoy son diez.** Ver `D10` |

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
