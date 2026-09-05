# D10 — La trampa de profundidad: cuántos niveles del libro del ES ve cada uno. **Para la VENTANA G.**

**VENTANA L. NO MIDE NADA. K sigue en 261.**

**Por qué es urgente y por qué es para G:** el Hecho 3 de `H01` dice que el canal público del E-mini
publica **cinco** niveles. La VENTANA G está reconstruyendo el libro con datos `mbo` y estudiando la
entrada pasiva. **Si el número de niveles que usa G no es el número de niveles que la plataforma de
Roberto recibe, la estrategia se diseña sobre un libro que no va a ver.**

---

# (a) ¿Cuántos niveles entrega HOY el canal público del ES, y desde cuándo?

| fuente | qué dice | fecha |
|---|---|---|
| **Guía de referencia de CME Globex** (`cmegroup.com`, documento del operador del mercado) | *"All CME Globex futures markets are 10 orders deep"* | **vigente** |
| Preguntas frecuentes de profundidad de mercado de CME DataMine | el libro es *"five to ten orders deep"* según el producto | vigente. **No pude bajar el documento primario: dos intentos, conexión cortada.** El texto lo tengo de un resumen de búsqueda, **fuente secundaria** |
| Fett y Haynes, regulador (`H01`, Hecho 3) | E-mini: **cinco** niveles; bono y crudo: diez | **2013 a mediados de 2016** |
| MDP 3.0, la especificación del canal | la profundidad es **por instrumento** y se declara en la etiqueta `264-MarketDepth` de la definición de seguridad | vigente |

> ## **HOY el ES publica DIEZ niveles por precio. En 2013-2016 publicaba CINCO. Los dos son verdad, en épocas distintas. La fecha exacta del cambio de cinco a diez NO la tengo, y no la invento: está entre mediados de 2016 y hoy.**

**Lo que sí puedo decir con la especificación en la mano:** el número correcto **no es un hecho de
memoria, es un campo del dato.** Cada definición de instrumento en MDP 3.0 lleva su propia
profundidad. **Si G tiene datos `mbo` o `mbp` del ES, la profundidad de ESE archivo está declarada
adentro del archivo, y ése es el número que manda para ese período.**

## Y el detalle que se escribe AL LADO del número de Fett y Haynes, no al pie

**Fett y Haynes muestrearon el libro sólo el primer martes y el primer jueves de cada mes.** Sus
cifras de profundidad son de **dos días por mes, sobre tres años**, unos 80 días. Los cinco niveles
son un hecho de estructura del canal y no dependen del muestreo; **cualquier número de profundidad
PROMEDIO de ese paper sí depende, y no se transfiere a un día cualquiera.**

---

# (b) Hay VARIOS canales, con profundidad y precio distintos. El costo va en la cuenta de la estrategia.

| canal | profundidad | quién lo recibe |
|---|---|---|
| **MBP** — por nivel de precio | los **10** mejores niveles de cada lado, agregados por precio | es el dato "de mercado" estándar que reciben las plataformas minoristas |
| **MBO limitado** | las órdenes individuales de los **10** mejores niveles | producto de datos, se paga aparte |
| **MBO completo** | **todas** las órdenes, sin límite de profundidad | producto de datos, se paga aparte. **Es lo que Databento vende como `mbo` y lo que G reconstruye** |

> ## **La VENTANA G reconstruye la cola FIFO con MBO completo. Roberto opera con lo que su plataforma le muestre. Son DOS libros distintos. Si la estrategia necesita ver la cola —y una entrada pasiva la necesita para saber dónde está parada—, el precio del dato que la muestra en vivo es un costo de la estrategia y se le carga a ella, igual que el diferencial.**

**No tengo el precio del MBO en vivo para un participante minorista.** Lo que tengo es que **el dato
histórico y el dato en vivo se compran por separado**, y que el histórico ya se compró. **El en vivo,
no.**

---

# (c) Lo que importa: qué profundidad entrega la firma de fondeo a la plataforma de Roberto

**Es la única pregunta de las tres que decide algo, y es la que menos pude verificar.**

| afirmación | estado | fuente |
|---|---|---|
| Tradeify entrega **Nivel 1** sin cargo después de firmar el acuerdo de datos no profesionales | **verificada en fuente secundaria** (`damnpropfirms`) | no es la firma |
| **Nivel 2 no se puede comprar** en la plataforma de Tradeify | **NO VERIFICADA.** Sale de un resumen de búsqueda. La página de ayuda de la firma (`help.tradeify.co`) devolvió **403 dos veces** | ninguna utilizable |
| NinjaTrader muestra hasta **20** niveles nativos | **no verificada**, afirmación del proveedor | proveedor |
| Rithmic entrega MBO completo | **no verificada**, afirmación del proveedor | proveedor |

> ## **Nada de esto vale lo que vale abrir el DOM y CONTAR. Roberto tiene la plataforma. Diez segundos mirando cuántas filas de precio aparecen a cada lado del mejor precio, en horario de contado, le dan el número exacto que ninguna de mis fuentes le puede dar. Ese número es el (c), y va a `H01` como hecho medido por la casa.**

**Dos cosas más para cuando cuente:**

1. **Contar en horario de contado y en horario nocturno.** Si aparecen diez filas a las 10:00 y
   diez a las 03:00, es la profundidad del canal. Si aparecen diez y tres, la profundidad del canal
   es diez y la de las 03:00 es del mercado.
2. **Mirar si la plataforma muestra órdenes o precios.** Diez filas de precio con un número de
   contratos al lado es MBP. Órdenes individuales con su tamaño es MBO. **Lo primero es lo esperable
   sin pagar.**

---

# Qué le cambia esto a G, dicho sin exagerar

| si Roberto ve | qué le pasa al estudio de entrada pasiva |
|---|---|
| 10 niveles agregados por precio, sin órdenes | **la cola FIFO que G reconstruyó no es visible en vivo.** La estrategia sabe a qué precio está, no en qué lugar de la cola. El estudio sigue valiendo como estimación **ex-ante** de llenado; **en vivo hay que operar a ciegas dentro del nivel** |
| MBO en vivo, pagado | la estrategia ve lo que G reconstruyó. **El costo del dato entra al piso** |
| menos de 10 niveles | **la plataforma recorta el canal.** Hay que saber a cuántos antes de diseñar nada que dependa del segundo nivel |

**Costos:** dinero **cero**. Cartuchos **cero**, K sigue en 261. **Tiempo de Roberto: diez segundos
con el DOM abierto, y anotar dos números.**
