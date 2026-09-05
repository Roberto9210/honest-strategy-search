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
