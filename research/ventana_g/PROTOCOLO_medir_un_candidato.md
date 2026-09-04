# PROTOCOLO — cómo medir un candidato sin caer en la trampa de la censura

**Escrito 2026-09-04. Activo permanente, no nota de una tanda.** Si estás leyendo esto sin haber
vivido esa semana: lo único que hace falta saber está acá.

---

## El problema, en una frase

**Si medís la tasa de acierto de una estrategia contando solo las operaciones que se cerraron, el
resultado sale inflado — y sale inflado justo en la dirección de hacer parecer bueno lo que no lo es.**

## Por qué pasa

Una operación con objetivo y stop termina de tres maneras, no de dos: toca el objetivo, toca el
stop, **o sigue abierta cuando se te acaba el tiempo**. Esa tercera no es rara: medida sobre ES a un
minuto con entradas al azar, **entre el 7% y el 35% de las operaciones no resuelve dentro de la
sesión**.

Y no se quedan abiertas al azar. **Se quedan abiertas las que iban a la barrera lejana**, porque
llegar lejos lleva más tiempo. Entonces, si las descartás, estás descartando selectivamente un lado.

## El número medido

ES 1-min Databento 2016-2019, entradas al azar, horizonte de una sesión:

| bracket | asumido `S/(S+T)` | medido sobre resueltas | **sesgo** | sin resolver |
|---|---|---|---|---|
| 5pt:10pt | 66,7% | 68,2% | **+1,65** | 7,1% |
| 10pt:10pt | 50,0% | 50,0% | **+0,00** | 18,7% |
| 20pt:10pt | 33,3% | 27,3% | **−5,82** | 35,2% |
| 5pt:20pt | 80,0% | 85,2% | **+4,93** | 17,3% |
| 10pt:20pt | 66,7% | 72,7% | **+5,82** | 35,2% |

Para dimensionarlo: el criterio que esta ventana estaba tratando de validar pedía una ventaja de
**+1,2 puntos**. El sesgo lo supera hasta por **4,8×**. **Un candidato de pura suerte medido así
reporta +5 puntos y se aprueba.**

## La regla

El sesgo **no** depende solo de la asimetría del bracket. `5pt:10pt` y `10pt:20pt` tienen exactamente
la misma asimetría (−0,333) y sesgos de +1,65 y +5,82. Lo que los separa es cuánto quedó sin
resolver. La forma que ajusta, con error medio de 0,42 puntos sobre 15 celdas medidas:

```
sesgo (puntos)  ≈  −0,5 × asimetría × (% sin resolver)

donde   asimetría = (T − S) / (T + S)
```

**El sesgo se anula por dos caminos independientes:** asimetría cero, o sin-resolver cero. Por eso
«usá brackets simétricos» **no** es la regla — es solo uno de los dos caminos.

Para mantener el sesgo por debajo de 0,5 puntos hace falta `|asimetría| × (% sin resolver) ≤ 1`:

| si tenés… | podés permitirte |
|---|---|
| 5% sin resolver | asimetría ≤ 0,200 → T/S entre 0,67 y 1,50 |
| 10% sin resolver | asimetría ≤ 0,100 → T/S entre 0,82 y 1,22 |
| 20% sin resolver | asimetría ≤ 0,050 → T/S entre 0,90 y 1,11 |
| 35% sin resolver | asimetría ≤ 0,029 → T/S entre 0,94 y 1,06 |

## Horizonte mínimo, medido y no supuesto

Sesgo en puntos por horizonte:

| bracket | 1 sesión | 2 sesiones | 5 sesiones | ¿baja de 0,5? |
|---|---|---|---|---|
| 10pt:10pt | +0,00 | +0,00 | +0,00 | **desde 1 sesión** |
| 5pt:10pt | +1,65 | +1,26 | +0,22 | **5 sesiones** |
| 20pt:10pt | −5,82 | −2,71 | −1,96 | ni a 5 |
| 5pt:20pt | +4,93 | +2,51 | +1,27 | ni a 5 |
| 10pt:20pt | +5,82 | +2,71 | +1,96 | ni a 5 |

**Tres de los cinco no llegan ni con cinco sesiones de horizonte.**

## Qué hacer

### 1. NO descartes las que no resolvieron. Nunca.

Es el error. Descartarlas es exactamente lo que produce el sesgo.

### 2. Cerralas a valor de mercado en el corte, y contá ese resultado

Es lo que hace un operador real cuando aplana al cierre. Es la opción por defecto porque **mide lo
que efectivamente pasa**, no una idealización. Una operación que quedó −7pt cuenta como −7pt, no
como «no cuenta».

### 3. Reportá siempre la banda, además del punto

Con `g` ganadas, `p` perdidas y `u` sin resolver, las dos cotas son:

```
peor caso:  g / (g + p + u)          (todas las abiertas terminan mal)
mejor caso: (g + u) / (g + p + u)    (todas las abiertas terminan bien)
```

Si la banda es más ancha que la ventaja que el candidato dice tener, **la medición no alcanza** y no
importa dónde caiga el punto.

### 4. Reportá siempre el % sin resolver, al lado de la tasa

Una tasa de acierto sin su fracción sin resolver es un número que no se puede auditar. Si un
candidato te trae una tasa y no te trae esa fracción, pedísela antes de mirar nada más.

### 5. Alargar el horizonte arregla la estadística, no la economía

Podés bajar el sin-resolver estirando el horizonte. **Pero eso significa aguantar la posición de un
cierre al siguiente**, y eso está medido aparte: contra un drawdown de $2.000 con un E-mini, la
cuenta muere entre el **42% y el 68% de las veces en diez noches, sin operar ninguna estrategia**
(ver `CRITERIO_RESULTADO.md`, Compuerta 1). **El arreglo del sesgo compra un riesgo real.** No es
gratis y hay que decidirlo, no aplicarlo por default.

## La advertencia que importa

**Este sesgo tiene dirección, y es la peligrosa.**

Cuando el objetivo está más cerca que el stop —que es la configuración de «ganar poco y seguido»,
la más común en estrategias que se ven bien en un backtest corto— las que quedan abiertas son las que
iban al stop lejano. Descartarlas **borra pérdidas** y el resultado sale mejor de lo que es.

No es ruido simétrico que se promedia. **Empuja siempre hacia aprobar.** Un error que empuja hacia
rechazar te cuesta una oportunidad; este te cuesta plata puesta en algo que no funciona.

## Lista de control, para pegar al lado de cualquier evaluación

- [ ] ¿Está reportada la fracción sin resolver?
- [ ] ¿Las sin resolver están contadas a valor de mercado en el corte, y no descartadas?
- [ ] ¿Está reportada la banda peor caso / mejor caso?
- [ ] ¿La banda es más angosta que la ventaja que el candidato afirma?
- [ ] `|asimetría| × (% sin resolver) ≤ 1`?
- [ ] Si se alargó el horizonte para bajar el sin-resolver, ¿está contado el riesgo de aguantar de un cierre a otro?

---

*Medido en `linea_base.py` y `censura_regla.py`. Salidas en `salida_linea_base.txt` y
`salida_censura_regla.txt`. Control: bracket de 23pt a cada lado → ambigüedad 0,000% y tasa pooled
exactamente 50,0%.*
