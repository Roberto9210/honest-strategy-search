# D09 — ¿La calidad de los datos del piso mata la ventana de L10? **NO. Lo que la achica es un error mío.**

**VENTANA L. NO MIDE NADA. K sigue en 261.**

---

# El planteo de Roberto, y tiene razón

**Yo dimensioné el bloqueo como "hace falta la serie continua de barras y esos datos son una
reconstrucción". Es más chico que eso.**

**Para el retorno de la última hora hacen falta DOS PRECIOS por evento**, el de una hora antes del
cierre y el del cierre. **No hace falta la serie continua.** Es una pregunta distinta y mucho más
fácil.

---

# (a) ¿Los proveedores entregan un precio a una hora fija? **SÍ, y desde 1987, no desde 1982.**

**PortaraCQG** declara **barras de un minuto desde 1987** y datos por tick desde 1987, con más de
45 años de historia intradiaria. Y **maneja explícitamente el problema del piso**: publica variantes
separadas por contrato —la del piso con su horario de sesión, la de Globex, y una tercera que empalma
las dos donde la liquidez saltó de una a otra a mediados de los noventa.

**TickData** ofrece historia intradiaria de trades y cotizaciones de profundidad comparable.

> ## **CORRECCIÓN A `D08`: la ventana utilizable no es 1982-1996, es 1987-1996. Son 120 fines de mes, no 177.**

**El contrato existe desde 1982 pero la cobertura intradiaria empieza en 1987. Y 1987 incluye octubre
de 1987, que es un problema de régimen aparte.**

---

# (b) ¿Qué error tiene un precio de esa época? **Está acotado por regla, y la regla es de un minuto.**

**El hecho, y es de la fuente correcta:** la reglamentación del CME exige que **los miembros
registren la hora de ejecución de cada operación con precisión al minuto**, con la hora arriba de la
tarjeta y el minuto en cada línea.

**Y la literatura sobre datos del piso lo confirma desde el otro lado:** los datos se reconstruyen de
reportes de tick, registros de compensación y auditoría, lo que hace **improbables las operaciones
espurias u omitidas**, pero **las marcas temporales son menos ciertas**, y el error importa sobre todo
cuando **reordena** las operaciones.

> **O sea: los PRECIOS son confiables y las HORAS tienen un minuto de incertidumbre. El error entra
> por el reloj, no por el precio.**

## Cuánto vale un minuto de incertidumbre, en puntos básicos

*(Derivación mía. **FRÁGIL**.)* Con un desvío diario de la época del orden de **100 puntos básicos**
—era más volátil que hoy, y el período incluye octubre de 1987— repartido sobre una sesión de piso de
unos **405 minutos**:

```
σ por minuto  ≈  100 / √405  =  4,97 pb          →   ε ≈ 5 pb por precio
```

---

# (c) LA TOLERANCIA, calculada explícitamente. **El asesino propuesto NO dispara.**

**El error entra en los dos extremos del retorno.** Con errores independientes de desvío `ε` en cada
precio, la varianza del retorno se infla en `2ε²`:

```
σ_total  =  √( σ_real²  +  2ε² )
```

## Pero antes hay que corregir un error mío, y es más grande que el de Roberto

**El margen de 4,40 que publiqué en `D08` usa el escalado uniforme de volatilidad que `A03` ya había
marcado como equivocado.** Una hora no tiene `60/405` de la varianza del día: **la última hora carga
mucho más, por el patrón en U.**

*(Uso 17,5 % de la varianza diaria en la última hora. **ESTIMACIÓN MÍA, FRÁGIL.** Es el hecho
estilizado estándar y no lo tengo medido para el ES.)*

| | escalado uniforme, lo que publiqué | **con patrón en U** |
|---|---|---|
| L10 moderna, ventana de 1 h, n = 46 | margen **2,25** | **1,11** |
| L10 en 1987-1996, ventana de 1 h, n = 120 | margen **4,40** | **1,48** |

> ## **Mi número de `F15` estaba inflado por un factor de dos. El margen real de la ventana vieja es 1,48, no 4,40.**

## Y ahora sí, la tolerancia

Con `σ_real = 41,8 pb` y `n = 120`, para que el margen caiga a 1,0 hace falta:

```
σ_total  =  17,0 × √120 / 3,0  =  62,07 pb
2ε²      =  62,07² − 41,8²  =  2.106          →   ε = 32,4 pb
```

| | valor |
|---|---|
| **error de precio que el margen tolera** | **≈ 32 puntos básicos** |
| **error plausible por la incertidumbre de un minuto** | **≈ 5 puntos básicos** |
| **holgura** | **factor 6,5** |

> ## **La calidad de los datos del piso NO mata la ventana. Haría falta un error equivalente a más de media hora de incertidumbre horaria para que dispare, y la regla del mercado exige precisión al minuto.**

**Roberto propuso el asesino y el asesino no dispara. Lo digo así porque el cálculo lo pidió él y el
resultado va en contra de su hipótesis.**

---

# (d) El rango de cierre: **cambia la construcción, no la clase de objeto.**

**En la era del piso el cierre era un RANGO, y el precio de liquidación se derivaba de él.**

**Pero eso no es tan distinto del presente:** la liquidación moderna del ES es un promedio ponderado
por volumen de los últimos treinta segundos. **Las dos son números derivados de la actividad de la
ventana final, no un único print.**

| | pit, 1987-1996 | electrónico, hoy |
|---|---|---|
| qué es el cierre | derivado del rango de cierre | promedio ponderado de los últimos 30 s |
| ¿es un único print? | **no** | **no** |
| ¿es el número al que el mercado marca? | **sí** | **sí** |

**El riesgo real es otro: cuando no hay operaciones en el rango, un comité fija el precio.** Eso pasa
en contratos ilíquidos, **y el futuro del S&P 500 era de los más líquidos que existían.** *(Afirmación
mía sin fuente: **FRÁGIL**. **Falla** si las estadísticas de volumen del CME de 1987-1996 lo ponen por
debajo de otros contratos que tuvieron precio fijado por comité. Ver `A06`.)*

**La incertidumbre que agrega el rango se suma a `ε`, y `ε` tiene un factor 6,5 de holgura.**

---

# EL VEREDICTO DE LA TAREA 1

**La objeción de datos que yo levanté era más grande de lo que corresponde. La retiro.**

| objeción | estado |
|---|---|
| "hace falta la serie continua de barras" | **falsa.** Hacen falta dos precios por evento |
| "los datos no existen para esa época" | **parcialmente falsa.** Existen desde **1987**, no desde 1982, y de un proveedor nuevo |
| "el error de reconstrucción mata el margen" | **falsa, con factor 6,5 de holgura** |
| "el cierre de 1985 no es el mismo objeto" | **débil.** Es un derivado de la ventana final, igual que hoy |
| **"el mecanismo probablemente no estaba"** | **EN PIE, y es la única que queda** |
| **"mi margen de 4,40 estaba inflado"** | **NUEVA, y es mía: el real es 1,48** |

> ## **L10 en 1987-1996 no se cierra por datos. Queda bloqueada por UNA sola cosa: si el flujo de rebalanceo existía entonces. Y con margen 1,48 dejó de ser la mejor del inventario: L07 tiene 1,72 y L03 tiene 1,67.**

**Con la advertencia que vale para las tres: los tres márgenes están calibrados con el escalado
uniforme que `A03` marcó. La medición del perfil de volatilidad que la VENTANA G tiene pendiente los
corrige a todos a la vez, y hasta entonces NINGÚN ORDEN ENTRE LOS SOBREVIVIENTES ES CONFIABLE.**

---

# TAREA 2 — El correo: **ahora SÍ pasa `F12`, y sale sólo con autorización**

## La cuenta de `F12`, rehecha

**Roberto dijo que el correo no pasaba porque su respuesta sólo importa si el problema de datos se
resuelve a favor. Se resolvió a favor. Entonces la cuenta cambia:**

| respuesta posible | qué veredicto cambia |
|---|---|
| *"antes de 1997 el flujo no era material"* | **cierra la ventana 1987-1996 definitivamente**, con razón nombrada |
| *"no conseguimos datos anteriores"* | **abre 120 fines de mes** con margen 1,48, y L10 vuelve al inventario activo |

**Las dos ramas cambian un veredicto. Pasa `F12`.**

## Y el caso queda anotado en `F12` como ejemplo

**Es mi propia idea la que no pasaba mi propio filtro, y ése es el caso más difícil de ver.** La
secuencia correcta fue la que impuso Roberto: **primero resolver la dependencia, después preguntar si
la pregunta importa.** Preguntar antes habría sido gastar una consulta cuya respuesta no cambiaba
nada.

## El borrador, que NO sale sin autorización

**Primera versión, retirada:** decía *"estamos evaluando la replicabilidad fuera de muestra"* y
*"la distinción decide si el período anterior es un fuera de muestra utilizable"*. **Las dos frases
revelan qué estamos haciendo y por qué.** Roberto fijó los criterios: una sola pregunta, nada del
proyecto ni del dinero, sin pedir datos ni código ni colaboración, cortés y corto.

**Versión que cumple los cuatro criterios:**

> Estimados profesores Harvey, Mazzoleni y Melone:
>
> Leí con interés *The Unintended Consequences of Rebalancing*. Tengo una sola pregunta: la muestra
> empieza en 1997. ¿Esa fecha responde a la disponibilidad de datos, o a que consideran que el
> rebalanceo institucional con mandato no era material antes?
>
> Gracias por su tiempo.

**Los autores publican en inglés; si se autoriza, sale en inglés y ésta es la traducción literal:**

> Dear Professors Harvey, Mazzoleni and Melone,
>
> I read *The Unintended Consequences of Rebalancing* with interest and have a single question: the
> sample begins in 1997. Is that date driven by data availability, or by a view that mandated
> institutional rebalancing was not material before then?
>
> Thank you for your time.

**Cuenta contra los criterios:** una pregunta, sí. Del proyecto y del dinero, nada. Datos, código,
colaboración: no se piden. Cuatro renglones.

> **CERRADO — 2026-09-05: el correo quedó DESCARTADO por decisión de Roberto. No sale. El borrador se
> conserva como registro y no como pendiente.** La ventana 1987-1996 de L10 queda bloqueada por
> mecanismo sin la respuesta de los autores, y L10 en una hora se cerró en `D16`.

**Costos:** dinero **cero**. Cartuchos **cero**, no registra ninguna hipótesis. **Tiempo de Roberto:
leerlo y decidir si sale.** **Regla de la casa: ningún correo sale sin su autorización.**
