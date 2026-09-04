# VENTANA G — ¿a partir de qué ventaja conviene dejar el alquiler?

**2026-09-04. No gasta cartucho. K = 261.** Continuación del punto (b) de `VEHICULO_RESULTADO.md`:
la comparación A (evaluación) contra B (capital propio, 1 micro) se hizo para **cero ventaja**. El
valor del techo de pérdida de A es proporcional al déficit de ventaja, así que con ventaja real la
cosa cambia. Acá se inyecta ventaja de tamaño declarado —el mismo mecanismo del motor de permutación:
con probabilidad q se elige el lado que resultó mejor, q=0,5 es la moneda— y se despeja a qué ventaja
B supera a A. Ventaja **realizada, no nominal** (se mide la que de verdad quedó en cada sorteo). La
caja sellada no se toca. Todo es ES 1-min 2016-2019, 1.006 sesiones reales, 3 réplicas por q.

---

## El resultado, en una frase

**El cruce está en una ventaja de ~+$5/sesión por micro (comisión barata) a ~+$8-11/sesión (todo
incluido), que es aproximadamente el propio piso de equilibrio de la evaluación.** Por debajo la
evaluación gana; por encima, operar capital propio gana. Y —contra la hipótesis previa— **el cruce
NO baja con el capital**: es plano y si acaso sube un poco, porque más capital también ayuda a A.

## 1 — El cruce (capital grande: A sin restricción de caja, B sin ruina)

Ventaja realizada a 1 micro. A en su mejor tamaño N por cada nivel de ventaja.

| q | edge $/ses (1 micro) | edge/mini | B free $/ses | B all-in $/ses | A mejor $/ses | N\* | gana |
|---|---|---|---|---|---|---|---|
| 0,50 | +0,00 | +0,00 | −5,15 | −10,73 | −0,60 | 1 | A |
| 0,52 | +4,37 | +43,66 | −0,88 | −6,58 | −0,49 | 1 | A |
| 0,55 | +12,44 | +124,37 | +7,11 | +1,30 | −0,35 | 1 | **B** |
| 0,58 | +21,55 | +215,49 | +16,07 | +10,06 | +0,99 | 1 | **B** |
| 0,60 | +29,10 | +290,98 | +23,54 | +17,43 | +3,03 | 1 | **B** |
| 0,65 | +42,35 | +423,48 | +36,57 | +30,16 | +6,89 | 2 | **B** |
| 0,70 | +58,81 | +588,10 | +52,77 | +46,01 | +22,24 | 10 | **B** |

(celda 5pt:20pt; 20pt:10pt es igual en forma. `salida_vehiculo_ventaja.txt`.)

**El cruce, interpolado en ventaja realizada por sesión a 1 micro:**

| celda | B a comisión Free ($0,78) | B a todo incluido ($1,82) |
|---|---|---|
| 5pt:20pt | **+$4,77/sesión** (= +$47,70/mini) | **+$10,71/sesión** (= +$107,14/mini) |
| 20pt:10pt | **+$4,79/sesión** (= +$47,91/mini) | **+$8,19/sesión** (= +$81,85/mini) |

### Traducido a la vara publicada

- El **piso de equilibrio** de la evaluación era **+$44,64/mini** por sesión (5pt:20pt). El cruce con
  comisión barata cae en **+$47,70/mini**: prácticamente el mismo número. **Con comisión de bróker
  barata, se abandona la evaluación a la misma ventaja que la evaluación necesita para no perder** —
  apenas por encima.
- Con comisión todo incluido (B paga lo mismo que adentro de A), el cruce sube a **~2,4× el piso**
  (+$107/mini). La diferencia entre los dos cruces es entera la ventaja de comisión del bróter barato.
- En puntos de acierto sobre la moneda, el cruce está en **+2 a +5 puntos nominales** (q entre 0,52 y
  0,55). La ventaja realizada, que es lo que se debe usar, es la columna de dólares.

## 2 — El control (reproduce vehiculo.py) — y una corrección de mi propio control

A q=0,5 el resultado tiene que reproducir `vehiculo.py`. **Mi primera versión del control decía "A
domina a TODO capital" y dio FALLADO. El control estaba mal escrito, no la máquina:** `vehiculo.py`
ya mostraba ayer que en la banda baja ($83-$250) B pierde menos que A **por la ruina** (P(ruina)≈1),
y que A domina de $500 en adelante. La máquina reprodujo eso exacto. Corregido el control para que
compare contra el resultado real de ayer —A domina con capital alto (donde B no se arruina), y en la
banda baja B "gana" solo con ruina alta—, **PASA**:

| C | A $ | B free $ | P(ruina B) | lectura |
|---|---|---|---|---|
| 83 | −83 | −17 | 0,966 | B menos, por RUINA |
| 250 | −188 | −105 | 0,921 | B menos, por RUINA |
| 1.000 | −198 | −567 | 0,738 | A domina |
| 10.000 | −198 | −1.289 | 0,000 | A domina (sin ruina) |
| 50.000 | −198 | −1.289 | 0,000 | A domina (sin ruina) |

Lo que lo haría fallar: que B le gane a A con capital alto, o que gane en la banda baja **sin** ruina.
Ninguna pasó.

## 3 — La curva: el cruce según el capital — contra la hipótesis

Para cada capital, la mínima ventaja donde B supera a A, con la fricción real de cada lado (ruina de
B, caja de A). Celda 5pt:20pt:

| C | q\* free | edge\* free | q\* all-in | edge\* all-in |
|---|---|---|---|---|
| 83 | 0,50 | +0,00 (ruina) | 0,50 | +0,00 (ruina) |
| 250 | 0,50 | +0,00 (ruina) | 0,50 | +0,00 (ruina) |
| 500 | 0,52 | +4,37 | 0,55 | +12,44 |
| 1.000 | 0,52 | +4,37 | 0,55 | +12,44 |
| 5.000 | 0,55 | +12,44 | 0,55 | +12,44 |
| 50.000 | 0,55 | +12,44 | 0,55 | +12,44 |

**La hipótesis previa era que con más capital el cruce BAJA (menos ventaja hace falta). Los datos
dicen lo contrario:** por encima de la banda de ruina el cruce es plano y si acaso **sube** ($4,37 →
$12,44 al pasar de $500 a $5.000). El motivo es que **más capital también fortalece a A**: A puede
comprar más intentos y tener más tiros al pago grande y grumoso ($1.350), mientras que B, una vez por
encima del umbral de ruina, ya captura toda su ventaja por sesión. A mejora con el capital más rápido
que B en la zona del cruce. Por debajo de ~$500 el "B gana" es el artefacto de ruina, no un cruce.

## 4 — El lastre de las reglas, separado de la cuota

Captura limpia (B a N micros, todo incluido) − A realizada = cuota amortizada + **lastre de reglas**.
A su mejor N por q. Celda 5pt:20pt:

| q | N\* | B a N (limpio) | A realizada | cuota/ses | **lastre/ses** |
|---|---|---|---|---|---|
| 0,50 | 1 | −10,73 | −0,60 | +0,60 | **−10,73** (protege) |
| 0,52 | 1 | −6,58 | −0,49 | +0,49 | **−6,58** (protege) |
| 0,55 | 1 | +1,30 | −0,35 | +0,35 | **+1,30** |
| 0,58 | 1 | +10,06 | +0,99 | +0,32 | **+8,74** |
| 0,60 | 1 | +17,43 | +3,03 | +0,26 | **+14,14** |
| 0,65 | 2 | +60,33 | +6,89 | +0,54 | **+52,90** |
| 0,70 | 10 | +460,05 | +22,24 | +4,95 | **+432,87** |

**Dos lecturas, las dos importantes:**

1. **La cuota es despreciable.** Amortizada sobre la vida del intento vale $0,26 a $0,60 por sesión
   (a N=1). **Casi nada del efecto de A es la cuota.** El préstamo es barato, como ya se dijo.
2. **El lastre de las reglas es todo, y cambia de signo en el cruce.** Sin ventaja, el lastre es
   **negativo** (las reglas te **protegen**: perderías $10,73/sesión por tu cuenta y la evaluación lo
   absorbe por la cuota — es el techo de pérdida, dicho como lastre). Con ventaja, se vuelve
   **positivo y grande** (las reglas te **estorban**: a q=0,70 la captura limpia es +$460/sesión y A
   solo te deja realizar +$22). El cruce de cero del lastre cae **justo en la ventaja del cruce**
   (~q=0,55). La misma estructura que protege al que no tiene ventaja castiga al que la tiene.

**Consistencia 35% al pago: NO MEDIDO.** Dirección: castiga el día grande, baja P(pago), **AUMENTA el
lastre**. Los números de arriba son una **cota inferior** del lastre real con ventaja.

## 5 — El techo de pérdida se encoge con la ventaja

Valor del techo = `E[(pérdida de B − cuota)+]`, 1 micro, todo incluido, sobre la vida de un intento
(139 sesiones). Celda 5pt:20pt:

| q | edge $/ses | valor del techo | P(pérdida > cuota) |
|---|---|---|---|
| 0,50 | +0,00 | **$1.529** | 0,833 |
| 0,52 | +4,37 | $1.014 | 0,665 |
| 0,55 | +12,44 | **$298** | 0,373 |
| 0,58 | +21,55 | $105 | 0,135 |
| 0,60 | +29,10 | $3 | 0,018 |
| 0,65 | +42,35 | $0 | 0,000 |

**El techo pierde ~80% de su valor justo en la ventaja del cruce** (de $1.529 a $298 en q=0,55) y se
anula en q=0,60. Ese decaimiento es la otra mitad de la respuesta: la única cosa que hacía valiosa a
la evaluación —acotar la pérdida— deja de valer exactamente cuando tenés ventaja suficiente para que
operar lo propio convenga.

## La síntesis

En la ventaja del cruce (~q=0,55, ~+$5 a +$12/sesión por micro) coinciden tres cosas medidas:

1. el rendimiento por sesión de B pasa a positivo;
2. el lastre de las reglas cruza de protección (−$10/ses) a estorbo (+$1/ses y subiendo);
3. el valor del techo de pérdida ya cayó ~80% (de $1.529 a $298).

Por debajo, la evaluación es el vehículo (te protege barato). Por encima, es puro lastre.

## Reproducir

    cd research/ventana_g
    python vehiculo_ventaja.py > salida_vehiculo_ventaja.txt

Aborta si el control no reproduce `vehiculo.py`. Fuentes de (B) con URL y fecha: `datos_crudos.md`.
