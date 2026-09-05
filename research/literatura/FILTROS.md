# LOS FILTROS, CORREGIDOS — y qué recuperan

**VENTANA L. NO MEDIDO. No gasta cartucho, K sigue en 261.**

Roberto corrigió el filtro nocturno y agregó dos filtros. Este documento los deja escritos con sus
umbrales **derivados de números ya medidos en el repo**, nunca elegidos a ojo, y aplica los tres a
todo el inventario.

---

# F1' — VENTANA DE EXPOSICIÓN SIN FRENO

## Qué preguntaba mal el filtro viejo

El filtro viejo preguntaba **"¿cruza el cierre del día?"**. Esa pregunta no es la que produjo el
número que se quería respetar.

La Compuerta 1 no cerró su rama porque fuera de noche. La cerró por esto, textual:

> *"TMAC/BTIC/TACO fijan el precio por fórmula, no por el libro. Ejecutar así significa entrar en un
> cierre y salir en otro: **no hay objetivo ni stop intradiario**, la posición queda expuesta toda la
> noche **sin freno**. Y los Micro E-mini **no son elegibles**, así que la unidad mínima es un ES
> completo, $50/punto — **no se puede bajar el tamaño**, que es la palanca habitual."*

**"Sin freno" significa que la mecánica de ejecución PROHÍBE poner un stop. No significa que el reloj
diga que es de noche.** Y la segunda mitad de la cita importa igual: la rama murió **por tamaño**, y
lo dice el propio veredicto — *"La Compuerta 1 murió por tamaño, no por ventaja."*

## Las tres preguntas del filtro nuevo

Una candidata declara su **ventana de exposición E** y responde tres cosas:

**1. ¿La regla permite un stop dentro de E?**
Si la mecánica de ejecución fija el precio por fórmula o el instrumento no cotiza durante E, la
respuesta es no y la candidata muere acá. Es el caso que mató a la Compuerta 1 y **no es el caso de
ninguna candidata de esta carpeta**: todas entran y salen contra el libro.

**2. ¿Cuánto puede moverse el precio en E, contra el drawdown?**
El drawdown en puntos es `D = $2.000 / valor del punto`.

| instrumento | valor del punto | **D en puntos** |
|---|---|---|
| ES | $50 | **40** |
| MES | $5 | **400** |

**3. ¿Cuántas veces hay que exponerse?**
La cadena de la evaluación necesita **al menos diez** (Compuerta 1, veredicto).

## Los umbrales, derivados y no elegidos

Todo lo que sigue está medido en `CRITERIO_RESULTADO.md`, Compuerta 1, sobre ES 1-min 2016-2019,
**955 noches**, sólo pares con el mismo contrato.

**Movimiento de una noche, en puntos de ES:**

| | puntos | contra D = 40 (ES) | contra D = 400 (MES) |
|---|---|---|---|
| mediana \|mov\| | 8,75 | 22 % del drawdown | 2,2 % |
| p90 | 32,75 | 82 % | 8,2 % |
| p99 | 71,81 | **180 %** | 18 % |
| máximo medido | **118,75** | **297 %** | **30 %** |

**Frecuencia con que una noche sola se lleva el drawdown entero, en ES:**

| | % | frecuencia |
|---|---|---|
| excursión adversa, largo | **8,38 %** | 1 de cada 12 noches |
| excursión adversa, corto | 5,03 % | 1 de cada 20 noches |

**Muerte antes de completar N noches, lado al azar, sin ninguna estrategia:**

| N noches | intradía histórico |
|---|---|
| 5 | 34,9 % |
| 10 | **54,9 %** |
| 20 | 73,4 % |

**Y la palanca, que es la tabla que decide todo:**

| drawdown | puntos | muerte en 10 noches |
|---|---|---|
| $2.000 con 1 ES | 40 | **54,9 %** |
| $4.500 con 1 ES | 90 | 18,7 % |
| $9.000 con 1 ES | 180 | 3,7 % |

## La consecuencia, y es la que recupera candidatas

**Un ES con drawdown de $2.000 son 40 puntos. Un MES con el mismo drawdown son 400 puntos.**

La tabla de la palanca está escrita en puntos, no en dólares, así que se lee directo: **operar 1 MES
contra $2.000 es equivalente a operar 1 ES contra un drawdown de $20.000.** La fila más generosa que
la Compuerta 1 llegó a calcular es 180 puntos, y ya ahí la muerte en diez noches cae a **3,7 %**.
Cuatrocientos puntos están **más del doble** más allá.

Y el peor movimiento nocturno medido en 955 noches son **118,75 puntos**: no llega ni a un tercio de
los 400.

**Traducido: la exposición nocturna que cerró la Compuerta 1 es un problema de TAMAÑO DEL CONTRATO,
no un hecho del mercado. En MES, con el mismo drawdown, deja de serlo.**

La Compuerta 1 no podía usar esa palanca porque **para TMAC/BTIC/TACO el micro no es elegible**. Esa
restricción es de esa mecánica de ejecución, no de la cuenta: **el juez de este proyecto acepta `ES`
y `MES` como instrumento**, las dos con comisión medida (`JUEZ_COMO_SE_USA.md`).

### Las dos deudas que van pegadas, y no las resuelvo

1. **La tabla de la palanca se corta en 180 puntos y la distribución de excursión más allá de
   118,75 no está publicada.** Extenderla a 400 puntos es una medición sobre datos que ya están en
   el repo. **Es de la VENTANA G, no mía.** La dirección no tiene ambigüedad; el número exacto sí.
2. **El MES divide la ventaja por diez, y el costo por punto NO se divide por diez.** La comisión de
   un micro es mucho menor en dólares pero mayor por punto. **Ese cociente es el que decide si la
   palanca sirve, está medido dentro del juez, y yo no lo tengo.** Es una consulta, no un estudio.

**El filtro corregido no aprueba nada por sí solo: traslada la decisión a un número que la VENTANA G
ya tiene. Eso es exactamente lo que un filtro debería hacer.**

---

# F5 — MÍNIMO DE EVENTOS POR AÑO

Es el filtro que realmente mordía y que faltaba. **El umbral se deriva de la tabla de potencia del
proyecto, no se elige.**

## La derivación, paso a paso

**Paso 1.** `salida_piso_ventaja.txt` da la diferencia mínima detectable en dólares por operación:
**$29 a $58 con 1.000 operaciones**, punto medio **$43**. Esa tabla está calculada a **α = 0,05 una
cola y 80 % de potencia**.

**Paso 2.** Esa combinación corresponde a un efecto de `z(0,95) + z(0,80) = 1,645 + 0,842 = **2,487
desvíos**`. O sea que la MDE publicada **no** es la vara del juez: es una vara más baja.

**Paso 3.** El juez pide **3,0 desvíos con una variante declarada, 3,7 con diez, 4,3 con cien**. La
ventaja requerida es entonces la MDE multiplicada por `t_juez / 2,487`:

| variantes declaradas | vara del juez | multiplicador sobre la MDE |
|---|---|---|
| 1 | 3,0 σ | ×1,21 |
| **10** | **3,7 σ** | **×1,49** |
| 100 | 4,3 σ | ×1,73 |

**Paso 4.** La MDE escala con la raíz de n: `MDE(n) = $43 × √(1000/n)`. Despejando n, y usando la
vara de diez variantes que es la que corresponde a casi toda esta carpeta:

```
n_mínimo  =  1.000 × ( 64,1 / A_neto )²          A_neto en dólares por operación, ES 2016-2019

eventos por año mínimos  =  250 × ( 64,1 / A_neto )²        (la caja medible son 4 años)
```

**Verificación del anclaje:** con `A_neto = $64,1` la fórmula pide 1.000 operaciones, y
`$43 × 1,49 = $64,1`. Cierra.

## Aviso sobre la unidad

La tabla de MDE está calculada para **brackets**. Las candidatas de salida por tiempo tienen otra
distribución de resultado, así que `n_mínimo` es **una aproximación de orden**, no un número exacto.
**Sirve para ordenar y para descartar por factores de 2 o más; no para decidir un empate.**

## Corrección a un número que publiqué en la entrega anterior

En las fichas L03 y L08 escalé la resolución del juez (±33 % con 5.000 operaciones) y saqué
±167 % y ±337 %. **Ese anclaje supone que la ventaja tiene el tamaño de referencia del juez**, y para
candidatas con ventaja grande por operación exagera el problema. **La MDE es el anclaje correcto** y
lo uso de acá en adelante. Con la MDE, L03 queda corta por un factor de 2,9 y no por uno de 5.
**Queda anotado como corrección mía, no como cambio de los datos.**

---

# F6 — MEDIBLE Y RENTABLE SON DOS PREGUNTAS

Las mezclé en la entrega anterior. Van separadas porque **el nocional del ES se multiplicó por 2,46
entre la muestra donde se puede medir y el mercado donde se cobraría**.

| | **MEDIBLE** | **RENTABLE** |
|---|---|---|
| pregunta | ¿alcanzan los datos para distinguirla de la moneda? | ¿queda plata después del costo? |
| nocional | ES 2016-2019, ≈ $130.000 | ES 2026, ≈ $320.000 |
| vara | `A_neto ≥ $43 × √(1000/n) × 1,49` | `A_bruto_2026 > costo` |
| costo | — | ≈ $17 por ida y vuelta, ES |
| lo decide | el número de eventos | el nivel del índice |

**Un efecto declarado en porcentaje o en puntos básicos vale 2,46 veces más dólares hoy que en la
muestra donde puede probarse. Un efecto declarado en puntos de índice vale lo mismo.** Casi todos los
de esta carpeta son del primer tipo.

**Consecuencia, y es incómoda:** una candidata puede ser **rentable y no demostrable a la vez**, y
eso no es una contradicción — es la posición normal de casi todo este inventario.

---

# APLICACIÓN 1 — Las siete que mató el filtro viejo, revisadas

| descartada | ventana E | ¿stop posible? | instrumento | veredicto con F1' |
|---|---|---|---|---|
| Deriva previa a la Fed — Lucca y Moench 2015 | 24 h | **sí** | ES / MES | **sobrevive a F1'**, pero sigue descartada: replicación fallida documentada, desapareció después de 2015. Y 8 eventos por año |
| Subastas del Tesoro — Lou, Yan y Zhang 2013 | varios días | sí | **ZN** | sigue descartada: el juez no acepta ZN, y la excursión multi-día no está medida |
| Goldman roll — Mou 2010 | 5 días | sí | spread de materias primas | sigue descartada: instrumento no soportado, y decaimiento con el capital de arbitraje declarado por el autor |
| **Rebalanceo institucional — Harvey, Mazzoleni y Melone 2025** | ≈ 23 h | **sí** | **ES y ZN** | **RECUPERADA** → ficha [L10](L10_rebalanceo_institucional_harvey.md) |
| Tesoro a fin de mes — Hartley y Schwarz 2019 | varios días | sí | **ZN** | sigue descartada por instrumento |
| Ciclo mensual de caja — Etula et al. 2020 | varios días | sí | mixto | sigue descartada: magnitud por evento sin cerrar y exposición multi-día |
| **Prima de días de anuncio — Savor y Wilson 2013** | una sesión | **sí** | **ES y MES** | **RECUPERADA** → ficha [L11](L11_prima_dias_anuncio_savor_wilson.md) |

**Dos recuperadas de siete. Y son las dos de mayor magnitud declarada de todo el inventario.** Eso no
es casualidad: el filtro viejo estaba correlacionado con la magnitud, porque los efectos grandes de
esta literatura se miden en retornos de un día entero y los chicos en ventanas de media hora.

# APLICACIÓN 2 — La que el filtro viejo dejó pasar

**La deriva nocturna del E-mini (Boyarchenko, Larsen y Whelan, *RFS* 2023). Roberto pidió que la
revise al revés, y la respuesta honesta es que NO muere por el filtro nuevo.**

- **E = 60 minutos**, de 2:00 a 3:00 hora del este.
- **¿Stop posible?** Sí. Es la apertura de los mercados europeos, que es precisamente cuando el libro
  del ES se llena; el paper entero trata de que ahí llega el flujo comprador. Un bracket puesto al
  entrar es un freno y no requiere estar despierto.
- **La objeción de "el operador duerme" es operativa, no de mercado**, y se resuelve con una orden
  bracket. No es el caso de la Compuerta 1, donde la mecánica **prohibía** el stop.

**Sigue descartada, pero por los dos motivos correctos:**
1. **F4, magnitud**: 3,7 % anual son ≈ $19 por sesión por contrato ES, que no cubre ni el costo de
   una ida y vuelta.
2. **Replicación**: está muerta desde 2021 y lo documentaron los propios autores en 2026, con el
   mecanismo medido — la dispersión del volumen firmado de cierre cayó de 6,5 % a 2,9 %.

**Lo importante del ejercicio: el filtro viejo la dejaba pasar por la razón equivocada y la habría
seguido dejando pasar. El filtro nuevo también la deja pasar, pero ahora se ve que lo que la mata es
otra cosa. Un filtro que acierta por el motivo equivocado vuelve a fallar en el próximo caso.**

---

# APLICACIÓN 3 — F5 y F6 sobre todo el inventario

`A_neto` es la ventaja por operación en dólares sobre nocional ES 2016-2019, ya restado el costo de
≈ $17 de una ida y vuelta. **La columna "falta" es el factor por el que la candidata se queda corta
de eventos.** Aritmética mía sobre números publicados.

| ficha | A neto/op | eventos/año disponibles | eventos/año requeridos | **falta** | MEDIBLE | RENTABLE 2026 |
|---|---|---|---|---|---|---|
| **L11** Savor y Wilson | $117 | 40 | 75 | **1,9×** | no | **sí**, ≈ $313 |
| **L10** Harvey et al. | $204 | 12 a 24 | 25 | **2,1×** | no | **sí**, ≈ $527 |
| **L03** Kurov et al. | $86 | 48 | 139 | **2,9×** | no | **sí**, ≈ $229 |
| **L07** fixing de Tokio | ≈ $35 | 250 | 838 | **3,4×** | no | marginal, el yen no escaló |
| **L01** Baltussen et al. | $18 | 252 | 3.170 | **12,6×** | no | **sí**, ≈ $69 |
| **L02** Gao et al. | $17 | 252 | 3.553 | **14,1×** | no | **sí**, ≈ $67 |
| **L08** Melvin y Prins | ≈ $55 | 12 | 340 | **28×** | no | marginal |
| **L06** VIX | ≈ $11 | 252 | 8.489 | **34×** | no | sin cerrar |
| L04 rebalanceo de ETF | = L01 | 252 | 3.170 | 12,6× | no | sí |
| L09 crudo | sin cerrar | 250 | — | — | — | — |
| L05 gamma | es un eje, no una regla | — | — | — | — | — |

## El resultado, dicho sin adornos

**Ninguna de las once es MEDIBLE sobre 2016-2019 a la vara del juez. La mejor se queda corta por un
factor de dos.**

**Y todas las de ES son RENTABLES a nocional 2026.** Las dos preguntas dan respuestas opuestas para
todo el inventario, que es exactamente lo que F6 existe para hacer visible.

## Lo que cambia el orden, y es lo más útil de esta tabla

**El orden viejo era por facilidad de acceso a los datos. El orden nuevo es por distancia a un
veredicto, y no se parece en nada.**

L01 y L02 encabezaban la lista vieja porque se corren con lo que ya hay. En la lista nueva están
quintas y sextas, **cortas por un factor de trece**, mientras que las dos recuperadas — que ni
figuraban — están primeras, cortas por un factor de dos.

## Qué compraría la caja sellada

**No lo decido y no lo propongo. Lo dejo calculado porque es la única palanca que cierra la brecha.**

La caja es ES diario 2020-01-02 → 2026-08-19, unas **1.660 sesiones**, un solo uso. Sumada a las
1.007 que hay, el presupuesto de eventos se multiplica por **2,65**.

| ficha | eventos con 2016-2019 | eventos sumando la caja | requeridos | ¿alcanzaría? |
|---|---|---|---|---|
| L11 | 160 | 424 | 300 | **sí** |
| L10 | 48 a 96 | 127 a 254 | 99 | **sí** |
| L03 | 192 | 509 | 555 | casi, corta por 1,1× |
| L01 / L02 | 1.007 | 2.670 | 12.700 a 14.200 | no, ni cerca |

**Las dos recuperadas son las únicas del inventario que la caja volvería medibles.** Es un hecho
aritmético sobre números publicados, no una recomendación: la caja tiene un solo uso, hay un
protocolo escrito para abrirla, y esa decisión es de Roberto.

---

# F9 — LA PIEZA QUE FALTA: ¿SE PUEDE AJUSTAR?

**Criterio permanente. Escrito 2026-09-05 porque yo mismo apliqué mal el criterio anterior.**

## El criterio equivocado, y por qué lo era

Al armar la prueba agrupada exigí que **fecha, signo y magnitud estuvieran todos en el paper**, y
excluí a L03 —la de mejor magnitud del inventario— porque su signo no está publicado y lo
tendríamos que poner nosotros.

**Eso es demasiado estricto, y confunde dos cosas.** Nunca se pidió pureza. Se pidió **escapar de
NUESTRO generador de hipótesis**, el que produjo 261 negativos. Cerrarle la puerta a una idea de
afuera porque le falta una pieza nuestra no es lo mismo que evitar nuestro generador: es tirar la
idea de afuera.

## El criterio correcto

**La pregunta no es "¿la pieza la ponemos nosotros?" sino "¿la pieza que agregamos tiene una decisión
que se pueda AJUSTAR?"**

| tipo de pieza | ejemplos | qué es | qué cuesta |
|---|---|---|---|
| **SIN grado de libertad** | una fórmula pública, un calendario oficial, una construcción especificada en el paper, quitar de una fórmula un término que exige información futura | **IMPLEMENTACIÓN** | nada. La idea sigue siendo de terceros |
| **CON grado de libertad** | elegir entre dos definiciones defendibles, calibrar un umbral, seleccionar una variante entre varias, definir una línea de base | **HIPÓTESIS NUESTRA** | cartucho, y suma a `variantes_probadas` |

## Por qué la línea está ahí y no en otro lado

**Una pieza sin ajuste no puede convertir un negativo en positivo. Una pieza con ajuste sí.**

Ése es todo el argumento y es suficiente. El peligro que el proyecto combate no es que toquemos la
idea: es que la toquemos **hasta que dé**. Una pieza que no tiene perilla no se puede girar.

## El ejemplo, para que dentro de seis meses nadie repita la exclusión

**L03, la deriva previa a los anuncios macro.** El paper mide la deriva condicionando a la sorpresa
que se publicó después, que no se conoce al entrar. Yo concluí que la regla operable la teníamos que
inventar nosotros y la saqué.

**Estaba mal por dos motivos, y los dos son generales:**

1. **No busqué si la pieza ya estaba publicada.** Lo estaba: **Bernile, Hu y Tang (2016), *Journal of
   Financial Economics* 121(3), 496-520** establecen que **el desbalance anormal de órdenes del
   E-mini antes del anuncio va en la dirección de la sorpresa posterior y predice la reacción del
   mercado**. El observable existe, está publicado y está medido en el instrumento del proyecto.
2. **Aun sin ese paper, quitar de la fórmula de ganancia de Kurov et al. el término que exige la
   sorpresa no es elegir entre alternativas: hay una sola forma de quitar un término
   inobservable.** Eso es implementación, no hipótesis.

**Regla de orden que sale de esto, y es la parte accionable: ANTES de armar la pieza uno mismo, hay
que buscar si ya está publicada.** Cuesta lo mismo que el resto de la búsqueda de literatura y
decide si la candidata gasta crédito nuestro o no.

## Cómo se aplica

1. Nombrar **exactamente** qué pieza falta.
2. Preguntar si tiene grado de libertad, y **escribir por qué sí o por qué no**.
3. Si lo tiene, **buscar la versión publicada** antes de construirla.
4. Si sigue teniéndolo, la candidata no se descarta: se marca **HÍBRIDA CON AJUSTE**, la declaración
   se hace **antes de correr**, y **suma a `variantes_probadas`**.
5. Si no lo tiene, la candidata es **HÍBRIDA** y vuelve al inventario principal sin penalidad.

**Y una distinción que hay que conservar, porque la confundí una vez:** una pieza que **no existe
para nadie** —como el posicionamiento del manipulador en la liquidación del VIX— no es una pieza
faltante. Es un descarte, y el motivo correcto es "la pieza no existe", no "la tendríamos que poner
nosotros".

**El inventario de híbridas está en [HIBRIDAS.md](HIBRIDAS.md).**

---

# F11 — CUÁNTO ESFUERZO MERECE UNA CANDIDATA QUE SÓLO SIRVE PARA ENTENDER

**Regla permanente. Decidida por Roberto el 2026-09-05.**

> ## **UNA CANDIDATA QUE SÓLO SIRVE PARA ENTENDER MERECE ESFUERZO SI SU RESULTADO CAMBIA LO QUE HACEMOS DESPUÉS. SI NO LO CAMBIA, NO.**

## Por qué hizo falta escribirla

**El objetivo del inventario se corrió de "encontrar una ventaja" a "entender la literatura", y se
corrió solo.** Las dos mejores pruebas que produje —L08 y L07— son **explícitamente no operables**, y
la de L07 la propongo sabiendo que los propios autores dicen que su retorno no cubre el diferencial
de compra y venta.

Puede ser el movimiento correcto dado que ninguna candidata es medible como ventaja. **Pero estaba
pasando de hecho en vez de por decisión, y sin límite.** Ahora está decidido y tiene límite.

## Cómo se aplica, en una pregunta

**Antes de gastar esfuerzo en una candidata que no se puede operar, hay que escribir qué haríamos
distinto según cada resultado posible. Si las dos ramas llevan al mismo lugar, no se gasta.**

## Los tres casos del inventario, resueltos con la regla

| candidata | ¿qué cambia su resultado? | **¿merece esfuerzo?** |
|---|---|---|
| **L07** | contesta si las reglas publicadas por terceros transfieren fuera de su muestra, por el precio más bajo del inventario. **Un negativo baja el valor esperado de la prueba agrupada; un positivo lo sube.** Las dos ramas cambian qué se hace después | **SÍ** |
| **L08** | aporta el 54 % de la potencia de la prueba agrupada. Sin ella la agrupada no se corre | **SÍ**, pero como insumo de la agrupada, no por sí misma |
| **L05** | reconstruir la gamma cuesta semanas, y `M02` ya propone una prueba de una tarde que decide si hace falta. **Hasta que M02 se corra, el esfuerzo en L05 no cambia nada** | **NO TODAVÍA** |

## El límite que la regla impone, y es el que importa

**El esfuerzo en candidatas no operables se justifica por lo que habilita, nunca por lo interesante
que sea el resultado.** Una prueba de mecanismo que sale positiva y no cambia el orden de trabajo,
ni el presupuesto, ni la decisión sobre un cartucho, **es curiosidad pagada con tiempo del
proyecto**.

**Y la regla corta para el otro lado también: si el resultado sí cambia lo que hacemos, entonces el
esfuerzo se justifica aunque la candidata no se pueda operar nunca.** Eso es lo que salva a L07.

---

# F12 — ANTES DE DISCUTIR UN CAMBIO DE MÉTODO, CALCULAR SI CAMBIARÍA ALGÚN VEREDICTO

**Regla permanente. Decidida por Roberto el 2026-09-05.**

> ## **ANTES DE DISCUTIR UN CAMBIO DE MÉTODO, CALCULÁ SI CAMBIARÍA ALGÚN VEREDICTO ACTUAL. SI NO CAMBIA NINGUNO, NO SE DISCUTE.**

## Por qué es la versión correcta, y no la que yo había propuesto

Yo propuse un disparador con esta forma: *"cuando un cambio metodológico rescataría material que hoy
no pasa, escribir las dos posiciones antes del veredicto"*. **Y señalé su defecto en la misma frase:
"¿esto rescataría el inventario?" es un juicio, y alguien motivado contesta que no y se saltea el
ejercicio.**

**`F12` no depende de ningún juicio. Es una cuenta.** Se toman los veredictos vigentes, se recalculan
con la regla nueva, y se compara. **Un motivado puede mentir sobre una intuición; le cuesta mucho más
mentir sobre una tabla que otro puede rehacer.**

## Mi propio caso es el que la justifica

Discutí durante una tanda entera si el castigo por multiplicidad debía tratar distinto a la selección
ajena. **La cuenta que `F12` habría exigido son cinco minutos:**

| | vara 4,0 | vara 3,0 | ¿cambia el veredicto? |
|---|---|---|---|
| L11 sola | θ ≥ 1,86 | θ ≥ 1,40 | **no**, sigue arriba de 1 |
| L10 sola | θ ≥ 2,04 | θ ≥ 1,53 | **no** |
| prueba agrupada `P01` | ya usa 3,0 | ya usa 3,0 | **no la toca** |
| L07 sola `P05` | ya usa 3,0 | ya usa 3,0 | **no la toca** |

**Ningún veredicto cambiaba. El debate no se debería haber abierto.**

**Y hay que decir lo que el debate sí produjo, para no leer la regla como que fue tiempo perdido:**
descubrió una contaminación de mirada hacia adelante en `F7` que invalidaba el orden del inventario.
**Ese hallazgo fue un subproducto, no el objetivo, y `F12` lo habría impedido.** Es el costo conocido
de la regla y se acepta: **una regla que evita muchos debates inútiles también evita algunos
hallazgos laterales.**

## Cómo se aplica

1. Listar los veredictos vigentes.
2. Recalcular cada uno **con la regla propuesta**.
3. Si ninguno cambia, **se anota la cuenta y se cierra**. No se discute el fondo.
4. Si alguno cambia, **entonces sí** se abre el debate, y ahí entra la disciplina de escribir las dos
   posiciones antes del veredicto y commitearlas por separado.

**El paso 3 no es "la idea es mala": es "la idea no es decidible con lo que tenemos hoy".** Puede
volver cuando el inventario cambie, y entonces la cuenta dará distinto.

**Alcance de `F12`, fijado por Roberto el 2026-09-05:** se aplica a debates sobre **método externo**
—*¿deberíamos usar la técnica de tal paper?*—. **NO se aplica a revisiones de nuestro propio
trabajo. Un debate sobre si nosotros nos equivocamos siempre se abre.**

---

# F13 — EL FILTRO QUE NOS MIRA A NOSOTROS

**Regla permanente. 2026-09-05.**

## El agujero que tapa

**Los doce filtros anteriores miran hacia afuera: evalúan candidatas.** Ninguno evalúa **nuestras
propias afirmaciones**.

**El caso de uso es real y es mío:** el ranking contaminado —calificar con grado A usando evidencia
cuya muestra cubría el período de prueba— **pasó los doce filtros sin que ninguno lo tocara**, porque
los doce preguntaban por el paper y ninguno preguntaba por el filtro.

## Las cuatro preguntas

Se aplican a **cada afirmación nuestra que gobierne una decisión**: un orden, un umbral, un
veredicto, una recomendación de gasto.

**1. ¿De cuántos números SIN MEDIR depende?**
Más de uno → **FRÁGIL**, marcado arriba del documento y no en una nota al pie. El inventario vive en
[FRAGILIDAD.md](FRAGILIDAD.md).

**2. ¿Usa información del período que pretende juzgar?**
Es la contaminación de mirada hacia adelante. Aplica a la evidencia que usamos para **elegir**, no
sólo a la que usamos para medir. **Con la asimetría de `F7`: descalifica la confirmación positiva, no
la refutación negativa.**

**3. ¿Sigue siendo cierta después del último cambio de número?**
Cada vez que se mide algo que antes se estimaba, **todo documento que use el número viejo queda
sospechoso hasta que se revise**. Un documento que se lee solo y miente es peor que uno que no
existe.

**4. ¿La escribí cuando me convenía?**
Si una afirmación propia apareció justo cuando rescataba algo que queríamos rescatar, **las dos
posiciones se escriben y se commitean antes del veredicto** (`D01` y `D02`).

## Por qué éste sí puede funcionar y `F12` no lo cubre

`F12` decide **qué debates abrir**. `F13` decide **qué afirmaciones nuestras siguen en pie**. Son
cosas distintas y el ranking contaminado lo prueba: **no era un debate, era una afirmación vigente
que nadie estaba revisando.**

## Su límite, dicho de entrada

**`F13` es un procedimiento manual, no un chequeo automático.** Hay que correrlo, y nada obliga.
**Su punto 3 es el que más se va a incumplir**, porque exige revisar documentos viejos cada vez que
cambia un número, y esta carpeta ya tiene treinta.

**La forma mínima que sí se puede sostener: todo documento que publique un número de potencia lista
sus dependencias en el encabezado.** Eso está aplicado desde hoy en los míos.
