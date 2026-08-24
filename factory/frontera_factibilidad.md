# La frontera de factibilidad — y por qué el veredicto no es "vacía" sino "prematura"

**Fecha:** 24 de agosto de 2026 · **Cartuchos gastados: 0.** Aritmética sobre lo ya medido: no corre
un backtest nuevo, no toca la parte B más que su calendario, y de la parte A mira **sólo dispersión**
— ninguna media, ningún signo, ningún P&L de ninguna regla nueva.

> **Versión 2.** La v1 de este documento concluyó "la frontera está vacía". Cuatro correcciones de
> Roberto la reordenaron y **el veredicto cambió de nombre**. Las cuatro están incorporadas abajo, y
> la que manda es la §2: la fricción no decide si la frontera está vacía.

## 0. La pregunta

El cartucho 2 dejó una frase que había que llevar hasta el número:

> La única palanca que vuelve alcanzable la potencia —operar más seguido— es la misma que le entrega
> la ventaja a los costos.

La fricción es un costo **fijo en dólares** ($3.90 ida y vuelta), así que su peso *relativo* crece al
acortar la tenencia, justo cuando la potencia mejora. Dos fuerzas opuestas. ¿Su suma baja alguna vez
de lo que una regla simple puede producir?

## 1. Las dos curvas

Con σ medido **incondicionalmente** sobre la parte A (4.865 sesiones) y n_B = máximo de operaciones no
solapadas que caben en las 1.669 sesiones de la parte B:

| Tenencia | σ/op | n_B máx | Potencia exige | Fricción cuesta | **BRUTO exigido** | en $ |
|---|---|---|---|---|---|---|
| **1 d** | $81.06 | 1.669 | 0.0686 σ | 0.0481 σ | **0.1167 σ** | **$9.46** |
| 2 d | $112.07 | 834 | 0.0970 σ | 0.0348 σ | 0.1318 σ | $14.77 |
| 3 d | $134.01 | 556 | 0.1188 σ | 0.0291 σ | 0.1479 σ | $19.82 |
| 5 d | $170.43 | 333 | 0.1535 σ | 0.0229 σ | 0.1764 σ | $30.07 |
| 7 d | $196.87 | 238 | 0.1816 σ | 0.0198 σ | 0.2014 σ | $39.65 |
| 10 d | $231.01 | 166 | 0.2174 σ | 0.0169 σ | 0.2343 σ | $54.13 |
| 20 d | $317.85 | 83 | 0.3075 σ | 0.0123 σ | 0.3198 σ | $101.64 |

Bajando de una sesión el mínimo se confirma por el otro lado: a ~30 minutos la fricción sola cuesta
0.1766 σ y el total sube a 0.1956 σ. **El mínimo de la tenaza está en ~1 sesión: 0.1167 σ.**

## 2. La corrección que manda: la fricción no decide si la frontera está vacía

Reordenando la propia condición:

```
c·√h  ≥  θ·√h + f/√h        (multiplicando por √h > 0)
c·h   ≥  θ·h + f
(c − θ)·h  ≥  f
```

con **θ = 2.8016/√S_B** y **f = fricción/σ₁**. De ahí:

- **Si c > θ**, existe un h que cruza — `h ≥ f/(c−θ)` — **con cualquier fricción.**
- **Si c ≤ θ**, no cruza para ningún h, **ni con fricción cero.**

*(Verificado numéricamente con el control f = 0: con c = 0.0661 y θ = 0.0686 no cruza; con c = 0.0700
cruza. La fricción no participa de la decisión.)*

**La fricción decide DÓNDE cruza, no SI cruza.** Y θ sale **enteramente del largo de la parte B**:

```
θ = 2.8016 / √S_B = 2.8016 / √1669 = 0.068577
```

> **Entonces la frontera no está vacía por los costos. Está vacía —si lo está— porque la caja fuerte
> es corta.** Es una afirmación sobre cuántos datos guardamos, no sobre cuánto cobra el bróker.

## 3. La corrección al numerador: c está inflado por selección

La v1 comparó θ contra c = 0.0661, de F4. **F4 es el mejor de 58 configuraciones: c = 0.0661 es un
máximo de orden, sesgado hacia arriba.** Es la propia lógica de multiplicidad de la spec, aplicada a
la frontera.

**Cota grosera del sesgo.** Bajo la nula global, el mejor de 57 configuraciones da p ≈ 1/58 = 0.01724,
o sea |t| ≈ **2.3815**. F4 midió **t = 2.304**. El exceso sobre lo que produce la selección sola es
**−0.0775**: negativo. La corrección grosera por máximo de orden **deja el efecto de F4 en cero** — es
la cuenta de `botc_potencia_f4.md` §3, ahora aplicada a c en vez de a δ.

**Las únicas estimaciones de c libres de selección** son los dos cartuchos de la Fase 2, porque fueron
**pre-registrados antes de conocer su resultado** — el diseño de la fase es, sin haberlo buscado, la
única fuente insesgada que tenemos:

| Ancla | h | c = δ_bruto/√h | error estándar |
|---|---|---|---|
| Cartucho 1 (k=3, hold=3) | 3 | 0.0618 | ± 0.0371 |
| Cartucho 2 (k=1, hold=1) | 1 | 0.0440 | ± 0.0257 |
| **Combinados por precisión** | — | **0.0498** | **± 0.0211** |
| *IC 90 %* | | *[0.0150, 0.0846]* | |
| F4 (seleccionado, inflado) | 7 | 0.0661 | — |

**c − θ = −0.0188 ± 0.0211.** Está por debajo, **y no significativamente.** Roberto tiene razón en que
la brecha real es más ancha que el 4 % que reportaba la v1 — pero también es mucho más incierta, y esa
segunda mitad es la que cambia el veredicto.

## 4. La corrección al modelo: `c·√h` es generoso con las tenencias largas

`logrado = c·√h` supone **deriva constante por unidad de tiempo**: la ventaja en dólares crece lineal
en h mientras σ crece con la raíz. Vale si el mecanismo es **persistente** (una prima que se devenga
mientras estás en posición).

Si el mecanismo es **transitorio** —una corrección que se completa y después se agota— la ventaja en
dólares **se aplana** en algún h\*, y a partir de ahí en unidades de σ **decae como 1/√h**. El mejor
punto pasa a ser h = h\* y alargar más **empeora**. La condición de cruce sigue siendo (c−θ)·h ≥ f,
pero con **h ≤ h\***.

Y esto importa: los mecanismos declarados de este proyecto son **todos transitorios**. Flujo de
rebalanceo de fin de mes (F4), liquidez a vendedores forzados (G2): los dos se agotan en días.

## 5. La pregunta que decide: ¿cuánta caja fuerte falta?

Condición: `θ ≤ c − f/h` ⟹ **S_B ≥ (2.8016 / (c − f/h))²**. Con S_B = 1.669 hoy y 252 sesiones al año:

| c | Modelo | h operable | S_B necesario | Faltan | **Años de espera** |
|---|---|---|---|---|---|
| 0.0661 *(F4, inflado)* | persistente | 10 | 2.090 | 421 | **1,7 a** |
| 0.0661 *(F4, inflado)* | persistente | 20 | 1.935 | 266 | **1,1 a** |
| 0.0661 *(F4, inflado)* | transitorio h\*=7 | 7 | 2.238 | 569 | **2,3 a** |
| 0.0661 *(F4, inflado)* | transitorio h\*=3 | 3 | 3.132 | 1.463 | **5,8 a** |
| **0.0498** *(insesgado)* | persistente | 10 | 3.880 | 2.211 | **8,8 a** |
| **0.0498** *(insesgado)* | transitorio h\*=7 | 7 | 4.262 | 2.593 | **10,3 a** |
| **0.0498** *(insesgado)* | transitorio h\*=3 | 3 | 6.891 | 5.222 | **20,7 a** |
| 0.0846 *(IC 90 % alto)* | persistente | 10 | 1.234 | 0 | **ya alcanza** |

Y θ cae solo, porque la caja fuerte crece sola:

| | Hoy | +2 a | +5 a | +10 a | +20 a |
|---|---|---|---|---|---|
| S_B | 1.669 | 2.173 | 2.929 | 4.189 | 6.709 |
| θ | 0.0686 | 0.0601 | 0.0518 | 0.0433 | 0.0342 |
| c necesario (h=10) | 0.0734 | 0.0649 | 0.0566 | 0.0481 | 0.0390 |

## 6. Veredicto: **Fase 2 prematura**, no "frontera vacía"

Las dos cosas se publican muy distinto y sólo una es cierta:

- ❌ *"En este instrumento, a estos costos, la potencia y la fricción no tienen intersección."*
  **Falso como está escrito.** La fricción no decide si hay intersección (§2), y el c contra el que se
  midió estaba inflado por selección en una dirección y es estadísticamente indistinguible de θ en la
  otra (§3).
- ✅ **"La caja fuerte de 1.669 sesiones es demasiado corta para decidir si existe una ventaja
  explotable en MES, y la incertidumbre sobre el tamaño de efecto alcanzable es tan grande que el
  tiempo de espera va de cero a veinte años según cuál de dos números medidos sea el correcto."**

El rango honesto es **[ya alcanza, 20,7 años]** y su punto central está cerca de **9 años**. Ese rango
es la salida, no un número. Estrecharlo requiere más estimaciones **insesgadas** de c — es decir, más
cartuchos pre-registrados, que es exactamente para lo que existen los 198 restantes.

**Corolario incómodo y honesto:** cada cartucho pre-registrado sirve para dos cosas a la vez —
buscar una ventaja, y medir c sin sesgo. Lo segundo no depende de que la búsqueda encuentre nada.

## 7. La inconsistencia entre nuestros propios instrumentos, resuelta

La criba decía **G4 "VALIDABLE, holgada"** (δ_min 0.0485, la mejor de las cinco). La frontera decía que
las tenencias cortas son el peor lugar posible. **Las dos hablaban de la misma familia y apuntaban a
lados opuestos, porque la criba medía potencia y no miraba fricción.** Es el mismo defecto que ya
habíamos corregido entre `required_t_a` y `power_check`: dos compuertas con nombres parecidos midiendo
cosas distintas.

**Corregido** (`CAMBIO_DE_REGLAS` `3d5887b8c7630728`, dirección **ENDURECE**): la criba ahora exige σ
por operación —fail-closed sin él— y compara **bruto contra bruto**:
`exigido = 2.8016/√n_B + fricción/σ` contra la referencia bruta de F4 (0.1749).

| Familia | n_B máx | σ/op | Potencia | Fricción | **Exigido** | $/op | Manda | Veredicto |
|---|---|---|---|---|---|---|---|---|
| **G1** nocturna | 1.669 | $81.06 | 0.0686 | 0.0481 | **0.1167** | $9.46 | potencia | VALIDABLE |
| **G3** régimen | 834 | $81.06 | 0.0970 | 0.0481 | 0.1451 | $11.76 | potencia | VALIDABLE |
| **G5** cruzado | 834 | $81.06 | 0.0970 | 0.0481 | 0.1451 | $11.76 | potencia | VALIDABLE |
| **G2** multi-día | 589 | $81.06 | 0.1154 | 0.0481 | 0.1636 | $13.26 | potencia | VALIDABLE |
| **G4** bordes | 3.338 | $22.08 | 0.0485 | **0.1766** | **0.2251** | $4.97 | **fricción** | **NO VALIDABLE** |

**G4 pasa de la mejor a la peor.** Su fricción pesa **3,6 veces** su ventaja de potencia. Ya no puede
gastar cartuchos: `preregister()` la rechaza. Sus 40 siguen sin gastarse y la decisión de darla
formalmente fuera de alcance —con la pérdida de esos 40, sin retirarlos del denominador ni
reasignarlos— queda pendiente, porque es irreversible.

Y nótese la respuesta a la pregunta *"¿G4 es factible o no?"*: **no**, y el motivo es exactamente el
que la frontera predijo. Los dos instrumentos ahora coinciden porque miden lo mismo.

## 8. Qué queda sobre la mesa

La celda más barata de todo el espacio de diseño sigue siendo **G1** (0.1167 σ, $9.46 brutos por
operación) — una operación por sesión, tenencia de ~1 sesión, sin filtro. Todo filtro reduce la
frecuencia y **sube** la barra, por lo que G3 y G5 empeoran la aritmética por construcción.

Y G1 es la única que **la serie diaria congelada no puede medir**: el tramo cierre→apertura de ES=F en
Yahoo carga el 3,3 % de la varianza porque es la reapertura de las 18:00 ET.

> La celda más barata sigue siendo la que los datos no pueden contestar. Pero ahora sabemos que eso no
> cierra la fase: la cierra —o no— el largo de la caja fuerte, y ese número crece solo.
