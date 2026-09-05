# P04 — Qué datos hay que comprar para L08, y el plan B

**VENTANA L. NO COMPRADO, NO COTIZADO. K sigue en 261.**

**Para la VENTANA G, que tiene el script de cotización y $99 de crédito.**

L08 aporta el **54 %** de la potencia de la prueba agrupada. **La pregunta del costo va antes que la
del cartucho**, porque sin estos datos la prueba no sirve y no hay nada que decidir.

---

# 1. EL MÍNIMO QUE SIRVE — no lo cómodo

## Instrumentos

**Futuros de divisas del CME sobre GLBX.** Melvin y Prins usan **spot** de EBS; los futuros son la
sustitución accesible y está declarada como desviación en el punto 4.

| nivel | símbolos | por qué |
|---|---|---|
| **MÍNIMO** | **6E, 6J, 6B, 6A, 6C, 6S** — euro, yen, libra, dólar australiano, dólar canadiense, franco suizo | las seis más líquidas. Con menos, el demediado transversal que el paper exige deja de tener sentido |
| completo | agregar 6N y 6M — dólar neozelandés y peso mexicano | se acerca a las diez del paper |

**Por qué seis y no menos:** el método publicado **demedia los retornos en el corte transversal**
para tratar al dólar como una moneda más. Con dos o tres monedas el demediado es ruido. **Seis es el
piso conceptual, no una comodidad.**

## Fechas — acá está el ahorro

**NO hacen falta cuatro años continuos. Hacen falta 48 días.**

```
el ÚLTIMO DÍA HÁBIL de cada mes, de enero de 2016 a diciembre de 2019
=  48 fechas
```

## Ventana horaria dentro de cada fecha

```
14:00 a 18:00 hora de Londres
```

Cubre la hora previa al fixing, que es donde vive el efecto publicado; el fixing de las 16:00; y dos
horas posteriores para el control de reversión. **Con menos de eso no se puede correr el control 1.**

**Ojo con el horario de verano:** el Reino Unido y Estados Unidos no cambian la hora el mismo fin de
semana. La ventana hay que pedirla **en hora de Londres convertida a UTC fecha por fecha**, no con un
desfase fijo. Es un error fácil y silencioso.

## Esquema y frecuencia

```
ohlcv-1m       barras de un minuto
```

**NO hace falta `tbbo` ni `mbo`.** El efecto publicado es un movimiento de precio de una hora, no de
microestructura. Pedir tick sería pagar de más por precisión que el método no usa.

## El pedido, en una línea

```
GLBX · ohlcv-1m · 6 símbolos · 48 fechas · 4 horas por fecha
=  288 símbolo-día, o 1.152 símbolo-hora si el proveedor cobra por hora
```

**Referencia de orden de magnitud que ya está en el repo:** un día entero de ES en `tbbo` cuesta
$0,79 (commit `1aa1039`). `ohlcv-1m` es un esquema mucho más chico. **No estimo el precio: lo cotiza
la VENTANA G con el script que ya existe.**

## Lo que además hace falta y es gratis

Retornos **mensuales** de los índices bursátiles de esos seis países, hasta el **penúltimo** día
hábil de cada mes. Es la señal, y es pública.

---

# 2. LO QUE NO HAY QUE COMPRAR, y por qué

| tentación | por qué no |
|---|---|
| cuatro años continuos de las seis monedas | el efecto vive en 48 fechas. El resto es 99 % de los datos y 0 % de la señal |
| `tbbo` o `mbo` | el método publicado no usa microestructura |
| las diez monedas del paper | 6N y 6M son mucho menos líquidos en futuros; **agregan más ruido que señal**. Ver el punto 4 |
| datos de spot en vez de futuros | es lo correcto y probablemente no está en el proveedor del proyecto. **Se declara la sustitución en vez de pagarla** |

---

# 3. EL PLAN B, escrito antes de saber el precio

## Sin L08

| | |
|---|---|
| L11 corregida | 6,35 |
| L10 | 3,84 |
| **total** | **10,19** |
| `t(θ=1)` | **3,19** |
| **θ mínimo detectable a 3,0 desvíos** | **0,94** |

**La prueba detectaría el 94 % de la magnitud publicada. La hipótesis es `θ ≥ 0,25`.**

**Traducido: sin L08 la prueba sólo puede confirmar transferencia casi completa, y cualquier
decaimiento la vuelve negativa o no concluyente. No podría distinguir `θ = 0,25` de `θ = 0`, que es
exactamente lo que se le pide.**

**Recomendación explícita: sin L08 ni un sustituto, la prueba agrupada NO se corre.** Correrla sería
gastar el cartucho 262 en un instrumento que no puede contestar su propia pregunta.

## El plan B real: L07 en lugar de L08

**L07 puede sustituirla, y sale más barato.**

| | L08 | **L07** |
|---|---|---|
| símbolos | 6 | **1** — sólo 6J |
| fechas | 48 | 288, los días *gotobi* de 2016-2019 |
| ventana | 4 horas | **10 minutos**, de 9:50 a 10:00 hora de Tokio |
| volumen del pedido | 288 símbolo-día | **288 símbolo-día**, pero de 10 minutos cada uno |

**Es el mismo número de símbolo-día con una ventana veinticuatro veces más corta.** Si el proveedor
cobra por volumen, L07 es mucho más barata; si cobra por símbolo-día, cuestan parecido y L07 gana por
usar un solo símbolo.

Con L07 dentro y L08 afuera, suponiendo una señal por evento comparable a la de L11:

| | |
|---|---|
| total con L11, L10 y L07 | ≈ 16,7 |
| `t(θ=1)` | ≈ **4,08** |
| **θ mínimo detectable** | ≈ **0,73** |

**Sirve.** Peor que con L08, que da 0,64, y mucho mejor que sin ninguna de las dos, que da 0,94.

## El bloqueo de L07, y es gratis de levantar

**L07 tiene la magnitud SIN CERRAR.** Antes de cotizar nada hay que abrir Ito y Yamada y extraer:

1. la magnitud del movimiento de 9:53 a 9:57 en puntos básicos, con su dispersión;
2. esa misma magnitud **después de 2008**, que es la partición cronológica que la regla `P02` exige.

**Es un paso de literatura y cuesta cero. Va antes de cualquier cotización.**

---

# 4. LAS DESVIACIONES, declaradas ahora

Cada una es una decisión nuestra y suma a `variantes_probadas`.

1. **Futuros en lugar de spot.** Melvin y Prins usan EBS. Para las seis mayores, en una ventana de
   una hora, la diferencia entre futuro y contado está gobernada por la paridad cubierta de tasas y
   es de segundo orden. **Para monedas menos líquidas no lo sería, y por eso 6N y 6M quedan afuera
   del mínimo.**
2. **Seis monedas en lugar de diez.** Cambia el demediado transversal respecto del publicado.
3. **Índices bursátiles de fuente pública** en lugar de la que usaron los autores.

**Las tres se declaran en el pre-registro antes de correr. Ninguna se elige después de ver
resultados.**

---

# 5. El orden en que hay que hacer esto

| # | paso | costo | quién |
|---|---|---|---|
| 1 | Abrir Ito y Yamada y cerrar la magnitud de L07 | **cero** | VENTANA L o quien lea |
| 2 | Cotizar el pedido de L08 del punto 1 | cero, script existente | VENTANA G |
| 3 | Cotizar el pedido de L07 del plan B | cero | VENTANA G |
| 4 | Decidir cuál se compra, o las dos, o ninguna | — | **Roberto** |
| 5 | Medir los `σ_j` sobre lo comprado y commitearlos | cero | VENTANA G |
| 6 | Recién ahí, decidir sobre el cartucho 262 | — | **Roberto** |

**Los tres primeros pasos cuestan cero y los tres cambian la decisión. Ninguno gasta cartucho.**
