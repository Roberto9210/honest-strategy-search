# Diseño — ¿se puede entrar PASIVO sin cruzar el spread? (mbo, sin correr todavía)

**VENTANA G. No gasta cartucho. K = 261.** Es un **diseño**, no una medición. No corre el estudio mbo.
La caja sellada no se toca. Las decisiones abiertas quedaron resueltas por Roberto (abajo), así que los
controles ya son finales.

## La pregunta

El juez cobra el deslizamiento de entrada como **medio-spread por mercado** (~0,13 pt, ~$6,5/op por
mini). Un candidato podría entrar **pasivo** —poner una orden límite en el mejor precio y esperar a que
lo llenen— y no pagarlo. A cambio corre dos riesgos que el tbbo no ve y el mbo (la cola completa del
libro, orden por orden) sí:

1. **No ejecución:** la orden puede no llenarse.
2. **Selección adversa:** los llenados que ocurren pueden ser sistemáticamente los peores.

El neto —`medio-spread ahorrado − selección adversa − valor de las señales no ejecutadas`— es la única
cifra que decide, y es una resta de tres cosas **medidas**, no el medio-spread solo.

## Decisiones resueltas por Roberto

**D1 — Qué se hace cuando la orden no se llena: PASIVA PURA.** Se dejan pasar las señales que no se
llenan (no se cruza). Se miden **las dos ramas** —pasiva pura y "cruzar tras N"— pero la respuesta es la
pasiva pura, porque la rama de cruzar ya está acotada por arriba por el costo de mercado ya medido
(~$6,5/op mini). La que trae información nueva es la pura.

**D2 — El horizonte de la selección adversa: NO es decisión, es medición.** Se **barre** el horizonte
entero (1 s, 5 s, 30 s, 1 min, 5 min, hasta el cierre de la operación) y se reporta la **curva**, no un
punto. Elimina el grado de libertad donde alguien elegiría el horizonte que da el número que gusta. Si
hay que señalar un valor, el plazo de tenencia mediana del propio candidato.

## La pregunta central, reformulada (corrección a mí mismo)

En la versión anterior escribí que las señales que se saltean "son las peores: te entran las que venían
a favor y no las que venían en contra". **Eso no se sabe: es un supuesto, y justo es lo que la prueba
tiene que contestar.** Puede ser al revés —que te llenen cuando el precio se te viene en contra, que es
la selección adversa clásica—. Cuál gana es EL resultado. Entra al diseño como **dos ramas medidas, no
una supuesta**:

- **Condicionado a que te LLENARON:** ¿qué hizo el precio después (a cada horizonte del barrido)?
- **Condicionado a que NO te llenaron:** ¿qué habría hecho el precio si hubieras entrado igual?

El signo de la diferencia entre las dos ramas es la selección adversa, con su signo medido, no asumido.

## La latencia es parte del diseño, no una nota al pie

Es el supuesto que más favorece al candidato (la dirección peligrosa), así que se mide, no se advierte.
Se corre la prueba con **dos latencias en paralelo** y se reportan al lado:

- **0 ms (techo idealizado):** colocación instantánea. Es el mejor caso imposible.
- **250 ms (residencial realista):** un ida y vuelta de internet común a Aurora, el datacenter de CME.

**El ancla medida del dato** (microestructura_latencia.py, RTH): el mejor precio de ES **vive
~113 ms (día agitado) a ~197 ms (día calmo)** entre cambios. Los 250 ms de latencia son del **mismo
orden** que la vida de una cotización, así que la latencia es **material** —una orden que llega 250 ms
tarde aterriza sobre un libro que ya se movió alrededor de una vez—. **Corrección a mi (b) anterior:**
dije que los llenados "se derrumbarían" con latencia; el tope de ES es más persistente de lo que supuse
y eso no está garantizado; lo decide la medición. **Matiz que agranda el efecto:** tbbo sólo ve la
cotización en el instante de cada operación, así que **subestima** los cambios del libro; el dwell real
es más corto y sólo el mbo lo mide, con lo cual la latencia puede pesar más que lo que sugiere el ancla.

Si la tasa de llenado se derrumba de 0 ms a 250 ms, **la entrada pasiva no es real para un retail
aunque el modelo idealizado diga que sí — y eso es el resultado, no un asterisco.**

## Supuestos de los que cuelga el número — van impresos CON el resultado

Quien lea la cifra tiene que ver de qué cuelga. Estos van en la salida, no sólo acá:

1. **1 contrato, al final de la cola.** No se compra prioridad ni se modela tamaño grande.
2. **La orden se coloca en el mejor precio**, no un escalón más adentro esperando mejor.
3. **La orden "muere" al alejarse el precio un escalón.** Umbral elegido por mí → se corre también con
   **dos escalones** y se reporta si la respuesta cambia (sensibilidad, no una constante).
4. **Un día por régimen, y ninguno agitado en 2026:** el régimen alto sólo lo cubre 2018. La tasa de
   llenado por régimen sale de un solo día por celda: piso de diseño, no constante establecida.
5. **Dos latencias (0 y 250 ms)** reportadas al lado; la de 250 ms anclada en el dwell medido.
6. **tbbo subestima los cambios de cotización** (sólo muestrea en operaciones); el mbo los ve todos, y
   por eso es el instrumento correcto para el dwell y la cola.

## Controles finales, cada uno con su condición de falla (puede pasar y puede fallar)

- **C-mbo-1, reconstrucción.** El mejor bid/ask reconstruido del mbo tiene que coincidir con el del
  tbbo del mismo día, en los timestamps de las operaciones. **FALLA:** que difieran → error de armado
  del libro, no del mercado. (Pasa si coinciden al tick; falla si no.)
- **C-mbo-2, la no ejecución no es gratis.** Pasiva pura a 0 ms de latencia: la tasa de llenado tiene
  que ser **estrictamente < 100%**. **FALLA:** 100% → la cola o la regla de muerte no está descontando
  las órdenes que el precio deja atrás. (Pasa <100%; falla =100%.)
- **C-mbo-3, sin ventaja no hay plata.** Con entradas AL AZAR, el neto de la pasiva pura
  (ahorro − selección adversa − valor de las no ejecutadas) tiene que ser **≤ 0** dentro de su error:
  sin información, la cola no puede regalar plata. **FALLA:** un neto positivo con entradas al azar → la
  selección adversa está mal medida a favor del candidato. (Puede dar ≤0 y pasar, o >0 y fallar.)
- **C-mbo-4, la latencia no ayuda.** La tasa de llenado no puede **crecer** con la latencia: a 250 ms
  tiene que ser ≤ que a 0 ms. **FALLA:** que suba con la latencia → error en el modelo de latencia.
  (Pasa si baja o queda igual; falla si sube.)

## Lo que este diseño todavía no cubre

- **Tamaño y prioridad de cola** más allá de 1 contrato.
- **La latencia de 250 ms es de ingeniería**, anclada por el dwell medido pero no medida como tal; el
  broker real puede ser peor.
- **Un día por régimen**, sin régimen alto en 2026.

## Estado

Decisiones resueltas, controles finales, latencia y selección adversa dentro del diseño como
mediciones. **Falta correr el estudio mbo** (reconstruir la cola FIFO y las cuatro métricas por
régimen, latencia y horizonte). Es la tanda siguiente; esta fue diseño.
