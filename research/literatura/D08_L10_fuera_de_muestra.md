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
