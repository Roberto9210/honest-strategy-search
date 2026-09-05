# D11 — La salida de L03 cae exactamente cuando los de alta frecuencia deshacen. El signo, razonado.

**VENTANA L. NO MIDE NADA. K sigue en 261. EL RANKING SIGUE CONGELADO: no recalculo ningún margen.**

---

# 1. Las dos cosas que se cruzan, con sus fuentes

**L03** (`HIBRIDAS.md` §1, de Kurov et al. y Bernile et al.):
- **dirección**: el signo del desbalance de órdenes acumulado en `[t − 30 min, t − 5 s]`;
- **salida**: el precio medio ponderado por volumen en **`[t + 5 s, t + 1 min]`**, con `t` la
  publicación de las 10:00.

**Kirilenko, Kyle, Samadi y Tuzun** (`H01` Hecho 5), E-mini, mayo de 2010, cuentas identificadas:
- los de alta frecuencia **compran en la dirección del cambio de precio durante los primeros ~5
  segundos** (coeficiente contemporáneo 32,09, t = 18,44);
- y **liquidan ese inventario entre 10 y 20 segundos después** (coeficientes negativos en los rezagos
  10-20). Vida media del inventario "probablemente menor" a 140 s.

> **La ventana de salida de L03, `[5 s, 60 s]`, CONTIENE ENTERA la ventana de liquidación `[10 s, 20 s]`.**
> No se rozan: una está adentro de la otra.

# 2. El signo, razonado

Sea `S` el signo de la sorpresa de las 10:00. El precio salta en la dirección de `S` en el primer
segundo. Los de alta frecuencia compran en la dirección de `S` hasta ~5 s y **venden en la dirección
de `S` —o sea, ejecutan del lado contrario a `S`— entre 10 y 20 s.**

L03 tiene una posición de signo `D`, fijada antes de las 10:00 por el desbalance. **Sale entre 5 y
60 s ejecutando del lado contrario a `D`.**

| caso | qué pasa entre 10 y 20 s | fills de L03 |
|---|---|---|
| **`D = S`** — L03 acertó | L03 vende lo mismo que ellos venden, **al mismo tiempo** | **competencia**: el precio se comprime transitoriamente contra la salida de L03 y se recupera cuando ellos terminan. **Peores** |
| **`D = −S`** — L03 erró | L03 vende lo que ellos compran | **ellos le dan liquidez.** Mejores |

> ## **El signo es ADVERSO, y de una forma peor que un costo parejo: los fills se deterioran EXACTAMENTE en las operaciones que ganan, y mejoran exactamente en las que pierden.**

**Lo que eso hace a la esperanza:** si `p = P(D = S)`, el costo neto por salida es
`p · c − (1 − p) · d`, con `c` el deterioro cuando compiten y `d` el descuento cuando les dan
liquidez. **Con `p = 0,5` se promedia a cero, que es el asesino que Roberto nombró. Con `p > 0,5`
—que es la hipótesis misma de L03— es un costo neto positivo.** El costo existe si y sólo si L03
funciona: **recorta la magnitud precisamente en el mundo donde hay magnitud que recortar.**

# 3. Cuánto vale `p`, y por qué no es 0,5

**`HIBRIDAS.md` línea 158: la correlación entre el desbalance de órdenes y la sorpresa es +0,19.**
Con eso `p` está apenas por encima de 0,5. **Traducción: el costo neto es una fracción chica de `c`,
del orden de la correlación.** No lo calculo en dólares: `c` no está medido y el ranking está
congelado. Lo anoto como lo que es:

> ## **COSTO DE L03 NO INCLUIDO EN SU MARGEN: deterioro de la salida por coincidir con la liquidación de inventario de alta frecuencia, de signo adverso, proporcional a la tasa de acierto. Se mide, no se estima.**

# 4. Lo que lo mataría, y lo que lo achica

| | |
|---|---|
| **lo mata** | que `D` no dependa de `S`. Con correlación cero, `p = 0,5` y el costo se promedia a cero. **La correlación publicada es +0,19, no cero, así que el asesino no dispara; pero deja el costo chico** |
| **lo achica** | que en 2019 la liquidación sea mucho más rápida que en 2010 —milisegundos, no 10-20 s— y termine **antes** de `t + 5 s`. Entonces las dos ventanas no se cruzan. **Kirilenko es de 2010; los 10-20 s no describen 2019.** Coughlan y Orlov (Hecho 4) dicen que hay más alta frecuencia en 2019, no que sea igual de lenta |
| **lo agranda** | que la salida de L03 se ejecute cruzando el spread en una ventana en la que el libro está más delgado de lo normal: Fett y Haynes (Hecho 3) observan las caídas de profundidad del E-mini en episodios de volatilidad |
| **lo que NO cambia** | que la salida de L03 es **por hora de reloj, no por reacción**: el hueco del tercer escalón de latencia (`H01`) no la toca por la entrada, pero **sí por la calidad del fill de salida**, que es esto mismo |

# 4b. EL CORTE, FIJADO — ≤ 60 segundos, y el perfil adentro sigue sin medir

**Roberto aceptó el criterio que salió de mi propia idea del dato:** la Tabla 8 de Haynes y Roberts
(`H01` Hecho 6) dice que las cuentas grandes automáticas del E-mini netean el **67 % de su volumen en
un minuto** en 2014-2016. **Eso permite fijar el corte de "liquidación" de antemano y con un número de
nuestro instrumento y casi de nuestro período, sin usar los 10-20 s de 2010.**

> ## **CORTE DECLARADO: la ventana de liquidación se fija en `[t, t + 60 s]`. Cualquier medición que G haga de este costo usa ese corte, y no otro elegido después de mirar.**

**Lo que el corte NO dice, y queda escrito con él:** la Tabla 8 es **por cuenta y por día**, y no dice
si el neteo ocurre a 5 o a 50 segundos. **Fija el techo, no el perfil.** Y `D11` vive del perfil: si
la liquidación termina antes de `t + 5 s`, la salida de L03 no se cruza con ella y el costo es cero.
**El perfil dentro de los 60 segundos sigue sin medir, y se dice así.**

**Y la salida limpia:** si la fila 8 de `F16` mata a L03 por reglamento (`R03` rama 2), esto se cierra
solo y no hace falta medir nada.

# 5. Qué se hace con esto

- **Se agrega a la ficha de L03 como costo nombrado y no incluido**, con puntero acá. Sin número.
- **Es medible sin comprar nada**: G tiene `mbo` del ES; la pregunta *"¿qué le pasa al precio entre
  `t + 5 s` y `t + 60 s` en los días de ISM y NAR, comparado con la misma ventana en días sin
  anuncio?"* se contesta con lo que hay. **No la pido: es territorio de G y no pre-registra nada.**
- **Si el costo se mide y resulta del orden de la magnitud publicada de L03 (5,4 a 10,4 pb), L03 se
  cierra por costo.** Eso es una lectura declarada antes, no un umbral.

**Costos:** dinero cero, cartuchos cero, K en 261. Tiempo de Roberto: leer.
