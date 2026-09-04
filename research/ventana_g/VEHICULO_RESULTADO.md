# VENTANA G — ¿es la evaluación el vehículo correcto?

**2026-09-04. No gasta cartucho. K = 261.** Aritmética sobre reglas de producto y sobre un flujo
de operaciones ya medido (entradas al azar sobre ES 1-min Databento 2016-2019). No se busca
ventaja, no se elige entre candidatas, no se declara ninguna regla de operación. La caja sellada
(2020-01-02 → 2026-08-19) no se toca.

**Este documento cambia lo que creíamos.** La expectativa escrita antes de correr era: A pierde
menos que B por sesión, y la curva no cruza. La curva **sí** cruza, pero al revés de como se lee
naturalmente, y el motivo es estructural. Va detallado por eso.

---

## La pregunta

Para un participante **sin ventaja**, en las mismas unidades (dólares por sesión, con marca a
mercado, sobre el mismo flujo de operaciones):

- **(A)** comprar evaluaciones de prop firm y operar bajo sus reglas
- **(B)** operar capital propio, 1 micro, sin evaluación, sin objetivo, sin drawdown impuesto

Firma de referencia para A: **Tradeify Growth 50K**, la de mejor esperanza medida de las ocho
(`aritmetica.py`). Cuota $83 con cupón. Solo se cuenta el **primer** pago ($1.350), o sea A en su
versión más favorable. La regla de consistencia (35% al pago) **no** se modela, y solo puede bajar A.

## El control, que discrimina

Con costo cero y sin reglas de firma, A y B tienen que dar **la misma** esperanza por micro y por
sesión, porque sin fricción el envoltorio no hace nada.

| celda | A (marca a mercado) | B | diferencia | error | veredicto |
|---|---|---|---|---|---|
| 5pt:20pt | −1,3022 | −1,3022 | +0,0000 | 0,0852 | **IGUALES** (+0,0 err) |
| 20pt:10pt | −4,3016 | −4,3016 | −0,0000 | 0,1006 | **IGUALES** (−0,0 err) |

Y con el defecto viejo puesto a propósito (A descartando las abiertas al corte) **falla** por +270 y
−144 errores. **CONTROL PASADO: la comparación no tiene ningún término que no venga de la fricción o
de las reglas.** Puede pasar y puede fallar: A pasa por el simulador de intentos, B por la suma
directa.

## MEDIDO contra ESTRUCTURA del producto — sin mezclar

- **MEDIDO (del dato):** el flujo de operaciones y su marca a mercado (el $/sesión de B); que un
  intento sin ventaja **dura ~147 sesiones** en resolverse; que por eso caben **~2,3 intentos
  independientes por año**; la cola de la pérdida de B (el valor del techo); las probabilidades de
  ruina de B. Comisiones y márgenes, de página oficial.
- **ESTRUCTURA del producto (no medición):** el techo de pérdida de A **es la cuota, por
  construcción**; la esperanza de A **se satura** porque solo caben ~2,3 intentos; la esperanza es
  **lineal en la cantidad de intentos** (el signo no cambia nunca).
- **NO MEDIDO:** exchange + clearing + NFA por micro (CME sin respuesta ×3, NFA 403 el 2026-09-04) —
  el costo real de B por ida y vuelta está **entre $0,78 y algo más**; se usa $1,82 (micro de
  Tradeify, todo incluido) como cota superior. Horario del margen intradía. Deslizamiento de entrada
  (cero en los dos, igual que en toda la ventana). Costo de oportunidad del capital (crece con C y
  solo empeora B).

## El resultado central: A cuesta ~$0,56/sesión, B cuesta ~$5,50 a $11/sesión

Para el participante sin ventaja, **1 micro**:

| | A (N=1) | B, solo comisión Free | B, todo incluido $1,82 |
|---|---|---|---|
| $/sesión, 5pt:20pt | **−0,56** | −5,51 | −11,12 |
| $/sesión, 20pt:10pt | **−0,56** | −6,68 | −9,86 |

A es **diez veces más barata por sesión** que operar tu propio micro. El motivo es entero
estructural: en A las pérdidas de trading son de la cuenta simulada de la firma, y el participante
**solo pierde la cuota**; en B cada dólar de pérdida es suyo. A su vez, A en su versión más favorable
(N=1) **nunca cobra** (P(pago)=0,000): su mejor caso es «pagar $83 y perder exactamente eso». La
cuota **es** toda la historia de A.

## La curva — y por qué se invierte

Capital propio C, horizonte de un año (250 sesiones). A juega mientras la caja alcance la cuota, los
pagos reponen. B opera 1 micro hasta la ruina en el margen. Esperanza en dólares del año:

| C | A | B (Free, margen $50) | B ($1,82, margen $50) | domina en esperanza |
|---|---|---|---|---|
| $50 | 0 (no puede jugar) | −32 | −44 | A (no juega) |
| $83 | −83 | −48 | −65 | **B**, apenas |
| $100 | −83 | −54 | −78 | **B**, apenas |
| $250 | −180 | −173 | −214 | límite |
| $500 | −193 | −342 | −434 | **A** |
| $1.000 | −193 | −647 | −853 | **A** |
| $3.000 | −193 | −1.164 | −2.106 | **A** |
| $10.000 | −193 | −1.378 | −2.774 | **A** |
| $50.000 | −193 | −1.378 | −2.780 | **A** |

(cifras de `salida_vehiculo.txt`, celda 5pt:20pt; 20pt:10pt es igual en forma: A satura en −$200, B
en −$1.671 / −$2.465.)

**La esperanza de A se satura en ~−$193 a todo capital**, porque solo caben ~2,3 intentos
independientes en un año y el peor caso de cada intento es la cuota. **La esperanza de B crece con el
capital** hasta ~−$1.378 (Free) o ~−$2.780 (todo incluido), porque más capital **quita la ruina que
venía frenando el sangrado**. B pierde menos que A en un solo lugar —la banda C ≈ $83 a $300— y ahí
pierde menos **solo porque la ruina lo liquida antes**, que no es «convenir».

**No existe un nivel de capital por encima del cual B le gane a A en esperanza.** Con el margen de
exchange ($2.608, si el intradía no rige de noche) B ni siquiera es factible hasta ese capital, y A
domina en todo el rango factible.

## El techo de pérdida, cuantificado

En A el peor caso por intento es **−$83, por construcción**. En B no hay techo. El valor del techo =
`E[(pérdida de B − cuota)+]`, lo que costaría asegurar B a la altura de la cuota, 1 micro:

| horizonte | B Free | B todo incluido | P(pérdida > cuota) |
|---|---|---|---|
| 147 sesiones (un intento) | **$924** | **$1.616** | 70–87% |
| 250 sesiones (un año) | **$1.429** | **$2.693** | 77–92% |

O sea: la cuota de $83 te compra la salida de **$900 a $1.600 de pérdida esperada de plata propia**
sobre la vida de un intento, y ~$1.400 a $2.700 sobre un año. El techo vale órdenes de magnitud más
que la cuota — **para un participante sin ventaja.** Ésa es la salvedad que decide todo (ver abajo).

Si B autofinancia la **misma exposición** que A (1 micro, capital $2.000 + margen, 147 sesiones): B
da −$717 a −$1.259 con 26–46% de ruina, contra los −$83 de A.

## La apuesta repetida

n intentos independientes de A. **La esperanza es lineal en n: el signo no cambia nunca**; la
repetición solo escala la pérdida. P(terminar arriba) es máxima en n=1 (y ya vale 0,000 a 1 micro,
porque un solo pago casi nunca ocurre) y cae por debajo de 10% en n=2. **La repetición no da vuelta
el signo ni a partir de ningún número de intentos: solo multiplica la pérdida.**

El préstamo, dicho en su unidad: $83 compran $2.000 de drawdown a 1 micro durante ~147 sesiones =
**$0,56/sesión = 4,2% por intento, ~7% anualizado** sobre los $2.000. Ése es el precio del préstamo,
y es barato; lo que no es barato es lo que el préstamo financia, que en esperanza pierde.

## Reproducir

    cd research/ventana_g
    python vehiculo.py > salida_vehiculo.txt

Aborta si el control no discrimina. Fuentes de (B) con URL y fecha: `datos_crudos.md`.
