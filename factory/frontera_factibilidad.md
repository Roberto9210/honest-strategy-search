# La frontera de factibilidad — cuánto tendría que ganar una operación para pasar la barra

**Fecha:** 24 de agosto de 2026 · **Cartuchos gastados: 0.** Esto es aritmética sobre lo ya medido.
No corre un solo backtest nuevo, no toca la parte B más que su calendario, y de la parte A mira
**sólo dispersión**: ninguna media, ningún signo, ningún P&L de ninguna regla nueva.
Script: `scratchpad` de la sesión; los insumos son públicos (`experiments_ledger.jsonl`, `data/`).

## 0. La pregunta

El cartucho 2 dejó una frase que hay que llevar hasta el número:

> La única palanca que vuelve alcanzable la potencia —operar más seguido— es la misma que le entrega
> la ventaja a los costos.

Y hay un mecanismo que lo agrava: **la fricción es un costo fijo en dólares** ($3.90 ida y vuelta),
así que su peso *relativo* crece al acortar la tenencia, justo cuando la potencia mejora. Dos fuerzas
en direcciones opuestas. Si su suma nunca baja de lo que una regla simple puede producir, la Fase 2
no tiene dónde buscar — y eso se sabe **antes** de gastar los 198 cartuchos restantes.

## 1. Las dos curvas

Para cada tenencia *h* (en sesiones), sobre la parte A (2000-09-18 → 2019-12-31, 4.865 sesiones), con
σ medido **incondicionalmente** —la dispersión del retorno de *h* sesiones, sin mirar su media— y
n_B = máximo de operaciones no solapadas que caben en las 1.669 sesiones de la parte B:

| Tenencia | σ por operación | n_B máx | Potencia exige | Fricción cuesta | **BRUTO exigido** | en dólares |
|---|---|---|---|---|---|---|
| **1 d** | $81.06 | 1.669 | 0.0686 σ | 0.0481 σ | **0.1167 σ** | **$9.46** |
| 2 d | $112.07 | 834 | 0.0970 σ | 0.0348 σ | 0.1318 σ | $14.77 |
| 3 d | $134.01 | 556 | 0.1188 σ | 0.0291 σ | 0.1479 σ | $19.82 |
| 5 d | $170.43 | 333 | 0.1535 σ | 0.0229 σ | 0.1764 σ | $30.07 |
| 7 d | $196.87 | 238 | 0.1816 σ | 0.0198 σ | 0.2014 σ | $39.65 |
| 10 d | $231.01 | 166 | 0.2174 σ | 0.0169 σ | 0.2343 σ | $54.13 |
| 20 d | $317.85 | 83 | 0.3075 σ | 0.0123 σ | 0.3198 σ | $101.64 |

La potencia manda en todas las filas: la línea de decisión por multiplicidad (|t| ≥ 3.726) nunca llega
a ser la restricción activa, porque la parte B es un tercio de la parte A.

**La tenaza se ve entera acá:** la columna de potencia sube 4,5× de 1 d a 20 d; la de fricción baja
3,9× en el mismo tramo. **Su suma tiene un mínimo en 1 sesión: 0.1167 σ, o $9.46 brutos por
operación.** Ese es el punto más barato de toda la fase.

### Y hacia el otro lado el mínimo también se confirma

Extendido al régimen intradía, con σ aproximado por raíz de *t* desde la pata diurna medida ($79.63):

| Tramo | σ | n_B | Potencia | Fricción | BRUTO exigido |
|---|---|---|---|---|---|
| sesión entera | $79.63 | 1.669 | 0.0686 σ | 0.0490 σ | 0.1176 σ |
| ¼ de sesión | $39.81 | 6.676 | 0.0343 σ | 0.0980 σ | 0.1322 σ |
| ~30 min | $22.08 | 21.697 | 0.0190 σ | 0.1766 σ | **0.1956 σ** |

Al bajar de una sesión la fricción se dispara más rápido de lo que mejora la potencia. **El mínimo de
la tenaza está en ~1 sesión y es 0.1167 σ.** No hay un punto mejor en ninguna dirección.

## 2. Contra qué se juzga "plausible"

No contra una intuición. Contra lo que las reglas de este proyecto **midieron de verdad**.

**Advertencia primero, porque la referencia obvia es falsa.** Ordenando las 58 configuraciones del
registro por ganancia bruta por operación, las 6 primeras son variantes de F2 con **9, 18, 28, 63, 73
y 56 operaciones** en veinte años (hasta $1.093 brutos por operación). El veredicto de la Fase 1 ya
las nombró: *"las 'ganadoras' son exposición al alza del índice, no estrategia"*. Usarlas como vara de
plausibilidad sería exactamente el error que la Fase 1 documentó. **La mediana del registro completo
es $1.61 brutos por operación**, y ese número tampoco sirve: mezcla reglas de frecuencias distintas.

Las únicas anclas honestas son las tres configuraciones con **muchas operaciones y σ conocido**:

| Ancla | Tenencia | Ops en A | Bruto/op | **Bruto en σ** |
|---|---|---|---|---|
| **F4 vuelta de mes** — lo mejor que el proyecto midió en 58 configuraciones | ~7 d | 231 | $29.20 | **0.1749 σ** |
| **G2 cartucho 1** (k=3, hold=3) | 3 d | 244 | $17.91 | **0.1070 σ** |
| **G2 cartucho 2** (k=1, hold=1) | 1 d | 1.510 | $3.73 | **0.0440 σ** |

## 3. El resultado: cada ancla contra la exigencia de SU tenencia

| Ancla | h | logrado | exigido a esa tenencia | **logrado / exigido** |
|---|---|---|---|---|
| G2 cartucho 2 | 1 d | 0.0440 σ | 0.1167 σ | **38 %** |
| G2 cartucho 1 | 3 d | 0.1070 σ | 0.1479 σ | **72 %** |
| F4 vuelta de mes | 7 d | 0.1749 σ | 0.2014 σ | **87 %** |

*(La columna "exigido" supone que la regla opera espalda con espalda a esa tenencia. Con la frecuencia
que esas configuraciones realmente tuvieron —F4 opera 12 veces al año, no 34— los porcentajes caen a
52 %, 33 % y 26 %. La tabla de arriba es la versión **generosa**.)*

**Lo logrado crece con la tenencia y lo exigido también, pero el cociente mejora al alargar —
y en ningún punto medido llega a 1.**

El motivo estructural: la ventaja **se acumula** con el tiempo en posición (aproximadamente lineal en
dólares) mientras σ crece sólo con la raíz, así que la ventaja en unidades de σ crece como √h. Lo
exigido también crece como √h, más un término de fricción que decae. Escrito:

```
logrado(h)  ≈  c · √h
exigido(h)  =  0.0686 · √h  +  0.0481 / √h
```

Las dos curvas se cruzarían en alguna tenencia **sólo si c > 0.0686.** Los tres valores medidos de c:

| Ancla | c = logrado / √h |
|---|---|
| G2 cartucho 2 (h=1) | 0.0440 |
| G2 cartucho 1 (h=3) | 0.0618 |
| **F4 (h=7) — el mejor de todo el proyecto** | **0.0661** |
| *umbral para que exista alguna tenencia factible* | *0.0686* |

**Los tres están por debajo del umbral. El mejor —F4, lo mejor que este proyecto encontró en 58
configuraciones— queda en el 96 % de lo que haría falta.** Es decir: la curva de lo logrado corre por
debajo de la de lo exigido **para toda tenencia**, y por eso el cociente mejora al alargar pero tiende
asintóticamente a 0.92, no a 1.

## 4. Veredicto de la frontera, con su límite dicho

**Con el material medido, la frontera está vacía: no hay ninguna tenencia en la que una regla del tipo
que sabemos construir alcance la barra de la Fase 2 sobre MES a costos minoristas.**

Lo que esto **no** dice, y hay que decirlo con la misma claridad que en la Fase 1:

- **No es una imposibilidad demostrada.** El coeficiente c está estimado con **tres puntos**, y el
  mejor de ellos queda a un **4 %** del umbral. Un margen así no soporta el peso de la palabra
  "imposible". Es una indicación fuerte, no un teorema.
- **No dice que no exista ventaja.** Dice que la ventaja que sabemos producir, neta de $3.90 por
  operación, no alcanza para que el examen final pueda *distinguirla del ruido* — que es el mismo
  diagnóstico de F4, ahora generalizado a toda la fase en vez de a una candidata.
- **No dice que otros no puedan.** Dice que con reglas explícitas de una página, sobre el índice más
  arbitrado del planeta, a costos de minorista, la potencia y la fricción casi no tienen intersección.

## 5. Si hay una ventana, es ésta

Formalmente la frontera es más baja en **1–3 sesiones de tenencia, operando todas las sesiones, sin
filtros**. Cualquier filtro reduce la frecuencia y por lo tanto **sube** la barra: un estado de
cuartil sobre una regla de 1 día deja n_B = 417 y exige 0.1853 σ en vez de 0.1167 σ. Es decir: **G3 y
G5, que condicionan por estado, empeoran la aritmética por construcción.**

Y acá el hallazgo se cierra sobre sí mismo. La celda más barata de todo el espacio de diseño —una
operación por sesión, tenencia de ~1 sesión, sin filtro— es **exactamente G1**, la prima nocturna. Es
la primera del orden declarado, la que la criba de medibilidad marcó como la más holgada, y **la única
que la serie diaria congelada no puede medir** (el tramo cierre→apertura de ES=F en Yahoo carga el
3,3 % de la varianza: es la reapertura de las 18:00 ET, no un hueco nocturno).

> **La única celda donde la aritmética deja lugar es la única que los datos no pueden contestar.**

Eso convierte la decisión sobre G1 en la decisión sobre la fase. Las opciones, con su precio:

1. **Desbloquear el régimen intradía** (implementar y probar el mapeo de día de negociación CME) y
   medir G1 sobre la serie de 1 minuto, donde el hueco nocturno sí existe. Toca `ventanas`, que el
   acta congeló — **exige una fase nueva o una enmienda declarada**, y en cualquier caso un
   `CAMBIO_DE_REGLAS` con su dirección.
2. **Declarar G1 fuera de alcance** con motivo escrito, perder sus 40 cartuchos (sin retirarlos del
   denominador ni reasignarlos), y con eso aceptar que la celda más barata queda sin medir.
3. **Cerrar la Fase 2 por frontera vacía**, publicar este documento como su veredicto estructural, y
   no gastar los 198 cartuchos restantes de a uno para llegar al mismo lugar.

## 6. Por qué la opción 3 no es un fracaso

Si la frontera está vacía, eso **es** el veredicto de la Fase 2, y vale mucho más que 198 cartuchos
gastados uno por uno. Sería la Fase 1 entendida de verdad: no *"estas cinco familias fallaron"* sino
**"en este instrumento, a estos costos, la potencia y la fricción no tienen intersección"** — que es
una afirmación sobre la estructura del problema, no sobre nuestra suerte, y que cualquier tercero
puede recalcular con los tres números públicos de la §3.

La Fase 1 costó una semana y $0 para aprender que cinco familias no tenían ventaja. La Fase 2 costó
**dos cartuchos** para aprender por qué ninguna podía tenerla de forma demostrable. Ese es el
progreso: la segunda vez el "no" viene con su mecanismo.
