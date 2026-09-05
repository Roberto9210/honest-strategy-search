# R01 — Regla para octubre de 1987 y para cualquier atípico futuro. SELLADA ANTES DE MIRAR.

**VENTANA L. NO MIDE NADA. K sigue en 261.**

> ## SELLADO
>
> **No existe ningún dato de 1987-1996 en el repo.** No se compró, no se miró, no se puede haber
> mirado. **Este documento se commitea con la regla y sin resultados, y el historial es la prueba.**
> Las dos versiones —con regla y sin regla— las produce quien corra la prueba, si alguna vez se
> corre, y se reportan las dos.

---

# 1. Por qué no es una decisión sobre ESE mes

**Yo había propuesto "declarar antes si octubre de 1987 entra o sale, y reportar las dos versiones".
Roberto tiene razón en que eso sigue siendo una decisión sobre un mes con nombre, y una decisión
sobre un mes con nombre es una preferencia.**

**Lo que corresponde es una regla que maneje a octubre de 1987 y a cualquier atípico futuro EXACTAMENTE
IGUAL, sin que nadie tenga que nombrarlo.**

---

# 2. LA REGLA — usa el instrumento que la casa ya tiene

**La VENTANA G construyó un eje de régimen: terciles de volatilidad ex-ante del período previo,
medidos en puntos básicos** (`juez_regimen_bps.py`, `juez_regimen_exante.py`). Y lo midió en puntos
básicos precisamente porque, en palabras de su propio commit, **es "la unidad que viaja entre
épocas"**.

**Ese eje tiene un DOMINIO: el rango de volatilidad ex-ante sobre el que fue calibrado.**

> ## **REGLA R01: un evento entra a la prueba si y sólo si su volatilidad ex-ante, en puntos básicos, cae DENTRO del dominio del eje de régimen. Un evento cuya volatilidad ex-ante excede el máximo observado en el período de calibración del eje está FUERA DEL DOMINIO del instrumento y se excluye POR REGLA.**

**No es un umbral que yo elija: es el borde de un instrumento que ya existe.** Y trata a octubre de
1987, a marzo de 2020 si la caja se abre, y a cualquier mes futuro con la misma mecánica.

## Cómo se aplica, paso a paso

1. Para cada fin de mes candidato, calcular la volatilidad ex-ante en puntos básicos **con la misma
   definición que usa el eje de la VENTANA G**, sin cambiarle nada.
2. Compararla contra el **máximo** de esa misma medida en el período de calibración del eje.
3. **Si la excede, el evento se excluye, y se lista.**
4. La lista de excluidos se publica **entera, con sus valores**, al lado del resultado.

## Lo que la regla hace que hay que decir antes, porque es incómodo

**1987-1996 fue una época más volátil que 2016-2019.** Es posible que la regla excluya **más meses que
octubre de 1987**: noviembre de 1987 casi seguro —su volatilidad ex-ante es la de la semana
posterior al 19 de octubre—, y quizás otros de 1987-1991.

> **Eso no es un defecto de la regla: es la regla funcionando.** Si exclusiones múltiples vacían la
> prueba, el resultado es *"el eje de la casa no cubre esa época"*, que es información sobre el eje,
> no una razón para aflojar la regla.

**Y la dirección del sesgo, declarada:** excluir los meses más volátiles **quita ruido**, así que
**baja el umbral de detección**. Si la prueba pasa sólo con la regla puesta, hay que decirlo así:
*pasa en el régimen que el eje cubre, no en el régimen completo.*

---

# 3. El segundo argumento, independiente del primero: ¿es EL MISMO OBJETO?

**Es la misma pregunta que usé bien con el rango de cierre en `D09`, aplicada al mes.**

**El mecanismo de L10 es un flujo de rebalanceo: fondos con mandato que venden lo que subió y
compran lo que bajó, ordenadamente, cerca del cierre del último día hábil.** Eso presupone un
mercado en el que se puede rebalancear ordenadamente.

**Octubre de 1987 no era ese mercado.** El informe de la comisión presidencial que investigó el
episodio (Brady, 1988) documenta descubrimiento de precios roto entre contado y futuros, colas de
ejecución, y un régimen de liquidez sin precedente en la historia del contrato. Los cortacircuitos
que hoy existen se crearon **como consecuencia** de ese mes.

> ## **El fin de mes de octubre de 1987 no es el mismo objeto que los otros fines de mes: no hay un flujo de rebalanceo ordenado que medir en un mercado cuyo mecanismo de formación de precios estaba roto. Queda afuera por CONSTRUCCIÓN, no por preferencia, y eso es independiente de la regla R01.**

**Los dos argumentos apuntan al mismo lado y son independientes: si uno se cae, el otro queda.**

---

# 4. Las dos versiones, cuando se mire

Quien corra la prueba reporta **las dos**, con este formato y sin agregar una tercera:

| versión | qué incluye |
|---|---|
| **A — con R01** | sólo los fines de mes dentro del dominio del eje. **Es la versión principal** |
| **B — sin R01** | todos los fines de mes de 1987-1996, incluido octubre de 1987 |

**Y la lectura de la diferencia queda escrita ahora:**
- Si A y B dan lo mismo, los atípicos no mandan y el resultado es robusto.
- Si A pasa y B no, **el resultado vive en el régimen que el eje cubre**, y así se dice.
- **Si B pasa y A no, el resultado lo produce el atípico, y NO cuenta.** Un efecto que aparece sólo
  cuando entra octubre de 1987 no es un efecto de rebalanceo.

---

# 5. Costos

| | |
|---|---|
| **dinero** | **cero** por esta regla. Los datos de 1987-1996 siguen sin comprarse |
| **cartuchos** | **cero.** Es una regla de construcción, no una hipótesis. K sigue en 261 |
| **tiempo de Roberto** | leer esto |
