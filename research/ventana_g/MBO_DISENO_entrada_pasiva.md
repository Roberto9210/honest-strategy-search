# Diseño — ¿se puede entrar PASIVO sin cruzar el spread? (mbo, sin correr todavía)

**VENTANA G. No gasta cartucho. K = 261.** Esto es un **diseño**, no una medición. No corre nada.
Apurarlo sería repetir el error de medir antes de saber contra qué. La caja sellada no se toca.

## La pregunta, y por qué es de investigación y no un cálculo

El juez ahora cobra el deslizamiento de entrada como **medio-spread por mercado** (~0,13 pt, ~$6,5
por operación por mini), y mueve el piso +$35 (5pt:20pt) y +$20 (20pt:10pt). Esa es la entrada
**cruzando**. Un candidato podría entrar **pasivo** —poner una orden límite en el mejor precio y
esperar a que lo llenen— y **no pagar ese medio-spread**. Pero a cambio corre dos riesgos que el
tbbo no puede ver y el mbo sí:

1. **No ejecución:** la orden límite puede no llenarse nunca, y justo no se llena cuando el precio
   se va en contra (te llenan cuando el precio viene hacia vos, o sea cuando estabas por perder).
2. **Selección adversa:** de los llenados pasivos, los que ocurren son sistemáticamente los peores
   (te llenan porque alguien con información cruzó contra vos). El ahorro del medio-spread puede
   quedar comido por esto, entero o más.

Estas dos no son constantes de costo: son propiedades de una **estrategia de ejecución**, y medirlas
mal a favor del candidato es exactamente el sesgo que esta ventana viene cazando. Por eso van con
controles antes de correr.

## Qué datos hacen falta y qué traen

`mbo` (market-by-order) de los seis días ya comprados: la **cola completa** de cada nivel, orden por
orden, con altas, bajas y ejecuciones. Con el snapshot sintético del libro a las 00:00Z (ya en la
ventana comprada) se puede **reconstruir el libro tick a tick** y seguir una orden límite propia
dentro de la cola: en qué posición entra, cuánto avanza, si la ejecutan y a qué precio terminó el
mercado después.

## El experimento

Para cada bar de entrada que el candidato marcaría (o, para calibrar, entradas al azar):

1. **Colocar** una orden límite de 1 contrato en el mejor precio del lado que toca (bid para comprar,
   ask para vender) en el instante de la señal.
2. **Seguir la cola FIFO:** posición inicial = tamaño delante en ese nivel; se descuenta con cada
   ejecución en ese nivel; sube si el nivel se despuebla; la orden **muere** si el precio se aleja un
   nivel sin haberla llenado (se cancela y se recoloca, o se cuenta como no ejecución, según la regla
   declarada).
3. **Registrar tres cosas por intento:** (a) si se llenó, (b) el tiempo de espera hasta el llenado,
   (c) el precio del mercado un horizonte fijo después del llenado (para medir selección adversa: el
   movimiento posterior condicionado a haber sido llenado).

## Las métricas

- **Tasa de llenado** por régimen: fracción de órdenes límite que se ejecutan antes de que el precio
  se aleje. Si es baja, la entrada pasiva no es viable como mecánica.
- **Tiempo de espera** hasta el llenado: si es largo, la señal ya caducó cuando entrás.
- **Selección adversa:** `E[movimiento posterior | llenado]`, por lado. Si es negativo (el precio se
  va en contra justo después de llenarte), el medio-spread que ahorraste vuelve como pérdida.
- **El neto:** `medio-spread ahorrado − selección adversa − valor de las señales no ejecutadas`. Ésa
  es la única cifra que decide, y es la resta de tres cosas medidas, no el medio-spread solo.

## Controles, escritos ANTES de correr

- **C-mbo-1, reconstrucción:** el mejor bid/ask reconstruido del mbo tiene que coincidir con el
  bid/ask que trae el tbbo del mismo día, tick a tick. **Lo haría fallar:** que difieran. Sería un
  error de reconstrucción del libro, no del mercado. Es el control de que el libro está bien armado.
- **C-mbo-2, no ejecución no gratis:** una orden límite que "siempre se llena instantáneo" da un
  ahorro de medio-spread completo y selección adversa cero. Ese resultado es IMPOSIBLE y **tiene que
  fallar** el experimento: si sale, la simulación de la cola no está descontando la no ejecución.
- **C-mbo-3, selección adversa tiene signo:** sobre entradas AL AZAR (sin señal), el neto de la
  entrada pasiva tiene que ser **peor o igual** que cero de ventaja, nunca mejor: sin información, la
  cola no puede regalar plata. **Lo haría fallar:** un neto positivo con entradas al azar → la
  selección adversa está mal medida a favor.
- **C-mbo-4, contra el tbbo:** el costo de entrada pasiva medido acá, para un candidato que en
  realidad cruza, tiene que **converger** al medio-spread del tbbo cuando la regla es "cruzá si no te
  llenan en N segundos". **Lo haría fallar:** que no converja al ~0,13 pt ya medido.

## Lo que este diseño todavía no resuelve, y hay que decirlo

- **Tamaño y prioridad:** con 1 contrato la orden entra al final de una cola de cientos; para tamaños
  mayores la dinámica cambia y este diseño no la cubre.
- **Latencia:** la simulación supone colocación y cancelación instantáneas. La latencia real degrada
  la tasa de llenado y agrava la selección adversa; queda como límite superior optimista.
- **Un día por régimen** (y ninguno en régimen alto de 2026): la tasa de llenado por régimen sale de
  un solo día por celda. Es un piso de diseño, no una constante establecida.

## Decisión pedida a Roberto antes de correr

Confirmar la **regla de cancelación** (¿cruzar tras N segundos, o contar como no ejecución?) y el
**horizonte** para medir selección adversa. Los dos cambian el neto, y elegirlos después de ver el
resultado sería elegir el número que gusta.
