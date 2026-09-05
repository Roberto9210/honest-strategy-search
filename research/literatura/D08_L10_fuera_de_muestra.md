# D08 — ¿Existe un fuera de muestra real para L10? LA DECLARACIÓN, ANTES DE INVESTIGAR

**VENTANA L. NO MIDE NADA. K sigue en 261.**

> ## ESTE DOCUMENTO SE COMMITEA EN DOS PARTES, A PROPÓSITO
>
> **Esta primera parte contiene la asimetría declarada y las cuatro preguntas. No contiene ninguna
> respuesta.** La segunda parte, en un commit posterior, trae la investigación.
>
> **El orden en el historial de git es la única prueba de que la asimetría se declaró antes.** Es el
> mismo procedimiento que `D01` y `D02`.

---

# 0. Por qué existe este documento: probablemente me equivoqué

**En el reporte anterior escribí que L10 "no tiene ningún fuera de muestra en ningún contrato
disponible", y la maté con eso.**

**Roberto señala que yo mismo reporté, la ronda anterior, que el contrato de tamaño completo del
S&P 500 cotiza desde abril de 1982.** Si la muestra de Harvey, Mazzoleni y Melone empieza en 1997,
**1982-1996 está fuera de su muestra**: unos 177 fines de mes que sus autores nunca miraron.

**Es la misma clase de error que la contaminación del ranking: un dato que ya estaba escrito en esta
carpeta y que no se conectó con una afirmación posterior mía.** Ver la sección final.

**Por qué importa el tamaño del error:** con la ventana corregida por `F15`, L10 tiene margen **2,25**,
el mejor de todo el inventario, por encima del 1,72 de L07 y del 1,33 de L08. **Si existe un fuera de
muestra real, deja de ser la mejor candidata de la literatura y pasa a ser la mejor candidata del
proyecto entero.**

---

# 1. LA ASIMETRÍA, DECLARADA AHORA

**El mecanismo de L10 es el rebalanceo de carteras institucionales hacia una asignación objetivo.
Ese flujo depende de que exista dinero institucional con mandato de asignación fija, y de que sea
grande respecto del mercado.**

> ## **SI EL DINERO INSTITUCIONAL CON MANDATO ERA MUCHO MENOR EN 1982-1996 QUE HOY, ENTONCES ESTA PRUEBA PUEDE CONFIRMAR PERO NO PUEDE REFUTAR.**

| resultado en 1982-1996 | qué significa |
|---|---|
| **el efecto aparece** | **confirmación fuera de muestra genuina.** El mecanismo existía y el efecto se ve donde los autores no miraron. **Vale como evidencia positiva de pleno derecho** |
| **el efecto NO aparece** | **AMBIGUO, y no se puede resolver.** Podría ser que el efecto no exista, o que el flujo todavía no estuviera. **NO cuenta como refutación** |

**Esto queda escrito antes de mirar nada, y no se mueve después.**

## Por qué la asimetría es legítima y no una excusa

**Porque el mecanismo declarado por los autores es un flujo, y un flujo tiene tamaño.** Si el tamaño
era distinto, el efecto esperado era distinto. **No es aflojar la vara: es que el objeto de la prueba
cambia con la época.**

**Y la contracara, para que no se use mal:** esta asimetría **sólo aplica si la sección 3 confirma
que el flujo era mucho menor**. Si resulta que el dinero con mandato ya era grande en los ochenta,
**la asimetría se cae y un resultado negativo cuenta como refutación con todas las letras.**

---

# 2. LAS CUATRO PREGUNTAS, sin responder

**(a) ¿Es correcto que 1982-1996 está fuera de la muestra de L10?** Si me equivoco en las fechas del
paper, esto se cierra acá.

**(b) ¿Existen datos intradiarios utilizables del contrato grande en 1982-1996?** `F15` exige una
ventana de una hora, no el día completo. **Ese contrato se operaba a viva voz en el piso, no
electrónicamente.** Hay que averiguar la fecha de inicio de cobertura intradiaria en los proveedores,
sin comprar nada. **Si no existen datos por hora de esa época, esto se cierra ahí, y el resultado es
negativo con razón nombrada, que vale más que el negativo que tengo hoy.**

**(c) ¿Hay una serie pública del tamaño del dinero institucional con mandato en ese período?** Si el
flujo no estaba, el mecanismo no podía estar.

**(d) La asimetría** — declarada arriba, antes de responder (b) y (c).

---

---

# PARTE 2 — LA INVESTIGACIÓN. Commiteada después de la declaración.

# (a) ¿Es correcto que 1982-1996 está fuera de muestra? **SÍ.**

**Verificado contra el texto del paper**, que ya estaba extraído en esta carpeta: Harvey, Mazzoleni y
Melone usan *"retornos diarios de futuros durante el período **1997-2023**"*.

**El contrato de tamaño completo del S&P 500 cotiza desde el 21 de abril de 1982.**

> **1982-1996 son 177 fines de mes que los autores nunca miraron. Roberto tiene razón y mi
> afirmación anterior era falsa.**

## Y la potencia sobre ese período sería la mejor del inventario

Con la ventana de una hora que pide `F15`, `σ ≈ 17,1 pb`, y **sin descuento por decaimiento porque el
período es anterior a la publicación**:

| | n = 46, 2016-2019 | **n = 177, 1982-1996** |
|---|---|---|
| (a) detectable | 7,56 pb | **3,86 pb** |
| (b) publicada | 17,0 pb | 17,0 pb |
| **margen** | 2,25× | **4,40×** |

> ## **Sobre el papel es la prueba mejor apuntada de todo el inventario, por encima del 2,25 de la propia L10 y del 1,72 de L07.**

**Lo que la bloquea no es la potencia. Son las dos preguntas siguientes.**

---

# (b) ¿Existen datos intradiarios utilizables de 1982-1996? **NO EN NUESTRO PROVEEDOR, y con la calidad en duda.**

| proveedor | qué cubre |
|---|---|
| **Databento**, el del proyecto | su conjunto de CME **no llega a los años ochenta ni noventa**. No sirve |
| TradeStation | declara datos de un minuto de contratos del piso **desde enero de 1982** |
| PortaraCQG, TickData | declaran historia intradiaria de futuros de esa profundidad |

**O sea que el dato existe en catálogos de terceros y no en el nuestro. Comprarlo sería abrir una
relación con un proveedor nuevo.**

## Y hay un problema de calidad que es estructural, no de proveedor

**Entre 1982 y 1996 el contrato grande se operaba A VIVA VOZ EN EL PISO.** No había motor de
casamiento. **Los precios los registraban reporteros del mercado observando la rueda**, y la marca
temporal de una operación del piso es una aproximación humana, no un sello de máquina.

**`F15` exige una ventana de UNA HORA a una hora concreta del día.** Eso depende exactamente de lo
más débil de esos datos: la marca temporal.

> **Una barra de un minuto de 1985 no es el mismo objeto que una barra de un minuto de 2019. La
> primera es una reconstrucción; la segunda es un registro.**

**No cierra la tarea, pero convierte "comprar datos" en "comprar datos de calidad desconocida a un
proveedor nuevo para una ventana que depende de su parte más débil".**

---

# (c) ¿Estaba el flujo? **La parte indexada era unas 36 veces menor. La parte con mandato no la pude cuantificar.**

## El número que sí encontré

| año | activos pasivos en acciones de EE.UU. | como % del mercado |
|---|---|---|
| **1993** | **$23 mil millones** | **0,44 %** |
| 2021 | $8,4 billones | 16 % |

Y la serie de fondos indexados: **$511 millones en 1985**, $55 mil millones en 1995, $4 billones hoy.

## Pero el mecanismo de L10 no es indexación

**Los autores hablan de fondos de pensión, mutuos y soberanos con mandatos de asignación**, no de
fondos indexados. **Esa población existía y era grande en los años ochenta**, y no encontré una serie
pública de su tamaño con concentración a fin de mes.

## El dato que probablemente cierra la pregunta, y está en el propio paper

> *"Durante **más de tres décadas**, los gestores de inversiones han empleado el rebalanceo regular…"*

**Escrito en 2025, "más de tres décadas" apunta a mediados de los noventa. Los propios autores no
reclaman que la práctica llegue a 1982.**

> ## **Su muestra empieza en 1997 probablemente no por falta de datos, sino porque es cuando creen que la práctica se volvió material. Si es así, 1982-1996 no es "fuera de muestra" en el sentido útil: es ANTES DE QUE EL MECANISMO EXISTIERA.**

---

# (d) LA ASIMETRÍA, APLICADA

**La sección (c) confirma que el flujo era mucho menor. Por lo tanto la asimetría declarada en la
parte 1 se activa:**

| resultado en 1982-1996 | qué vale |
|---|---|
| el efecto aparece | **confirmación fuera de muestra genuina** |
| el efecto no aparece | **ambiguo. NO cuenta como refutación** |

**Y la contracara que también escribí antes no se activa: el flujo NO era grande en los ochenta, así
que la asimetría no se cae.**

---

# EL VEREDICTO, y es una corrección de la mía, no una confirmación

**Mi afirmación anterior —"no existe ningún fuera de muestra para L10 en ningún contrato
disponible"— era FALSA.** Existe: 177 fines de mes, y sobre el papel con el mejor margen del
inventario.

**Pero está bloqueado por tres cosas a la vez, y ninguna es la potencia:**

1. **Datos que no tiene nuestro proveedor**, de un vendedor nuevo, y de una época en que el precio lo
   anotaba una persona mirando la rueda.
2. **Un mecanismo que probablemente no estaba**, con el propio paper fechando la práctica en
   *"más de tres décadas"*, o sea mediados de los noventa.
3. **La asimetría activada**: un negativo no significaría nada.

> ## **La conclusión práctica es la misma que la de antes —no se persigue hoy— pero la RAZÓN es completamente distinta, y ésa es la diferencia entre un negativo con razón nombrada y un negativo equivocado.**

**Y una cosa que sí queda como acción concreta y sin costo: si alguna vez se le pregunta algo a los
autores, la pregunta es por qué empieza en 1997.** Si la respuesta es "porque antes no había flujo",
esto se cierra del todo. Si es "porque no conseguimos datos", entonces 1982-1996 vuelve a estar
abierto y con el mejor margen del inventario.

---

# 3. La clase de error, y qué le agrega a `F13`

**Este error y el de la contaminación del ranking son el mismo error:** una afirmación mía que
contradice un hallazgo mío anterior, en la misma carpeta, sin que nada lo detecte.

**`A02` revisa si una afirmación sigue siendo cierta después de que cambió un NÚMERO. No revisa si
contradice un HALLAZGO.** Son cosas distintas: el número de 60 a 82 vino de afuera; el contrato desde
1982 lo escribí yo mismo dos rondas antes.

**Propongo agregar a `F13` una sexta pregunta**, y la escribo abajo en vez de sólo mencionarla:

> **¿Esta afirmación contradice un hallazgo propio de otra ronda?**
>
> Aplica sobre todo a afirmaciones de la forma **"no existe X"** o **"no hay ningún Y"**. Son las más
> frágiles, porque basta un solo contraejemplo para tumbarlas, y el contraejemplo puede estar escrito
> por uno mismo tres documentos atrás.

**Las dos veces que me pasó, la afirmación tenía esa forma:** *"no hay evidencia posterior no
superpuesta"* y *"no existe ningún fuera de muestra en ningún contrato disponible"*.
