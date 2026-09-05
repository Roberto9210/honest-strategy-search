# L01 — El retorno del día hasta 30 minutos antes del cierre predice la última media hora, en más de 60 futuros

**VENTANA L. Ficha de literatura. NO MEDIDA. No gasta cartucho, K sigue en 261.**

Clasificada antes de cualquier medición, según la regla del proyecto: *"un p-valor calculado sobre
datos en los que otro ya seleccionó no es un p-valor."*

---

## 1. Cita completa

Baltussen, Guido; Da, Zhi; Lammers, Sten; Martens, Martin (2021). **"Hedging demand and market
intraday momentum."** *Journal of Financial Economics*, vol. 142, n.º 1, pp. 377–403.
Recibido 16/01/2020, aceptado 23/09/2020, en línea 04/05/2021.

- Editorial: https://www.sciencedirect.com/science/article/abs/pii/S0304405X21001598
- PDF del autor: https://academicweb.nd.edu/~zda/intramom.pdf
- RePEc: https://ideas.repec.org/a/eee/jfinec/v142y2021i1p377-403.html

## 2. El efecto, en una frase

Si el mercado subió en lo que va del día, la última media hora antes del cierre también tiende a
subir; si bajó, tiende a bajar — y esto pasa en casi todos los futuros líquidos del mundo, no sólo
en acciones estadounidenses.

## 3. Instrumento y período de la muestra original

- **Más de 60 futuros**: índices bursátiles, bonos de gobierno, materias primas y monedas.
- **1974 → mayo de 2020**. El futuro del S&P 500 (ticker **ES**) entra con muestra
  **1982-04-23 → 2020-05-01, 9.535 sesiones**, ventana 09:30–16:00.
- Los resultados por clase de activo se arman como cartera 1/N dentro de cada clase.

**Esto importa: es el único paper del lote cuya muestra original ES el instrumento que Roberto
opera.** No hay que trasladar de un ETF a un futuro.

## 4. Magnitud declarada

La regla es: mirar el signo del retorno desde el cierre anterior hasta 30 minutos antes del cierre
(lo llaman `rROD`), y tomar posición en esa dirección durante la última media hora.

| cartera de futuros de índice | retorno anual | desvío anual | Sharpe | tasa de acierto |
|---|---|---|---|---|
| señal `rROD` | 6,86 % | 3,96 % | **1,73** | 55 % |
| señal `rONFH` (primera media hora) | 4,21 % | 3,95 % | 1,07 | 55 % |
| señal combinada, sólo cuando coinciden | 5,47 % | 3,42 % | 1,60 | **61 %** |
| *referencia*: siempre largo la última media hora | 0,44 % | 4,20 % | 0,11 | 53 % |

Coeficiente de `rROD` sobre la última media hora en el índice S&P 500: **5,98 (t = 4,78), R² = 3,28 %**
(Tabla 12, cierre 16:00, 1982–2020).

### Traducción a dólares por sesión por contrato ES

Con la convención de conversión del índice de esta carpeta (ES 2016-2019, nocional ≈ $130.000):

| | ES 2016-2019 | ES a precios de 2026 |
|---|---|---|
| 6,86 % anual, una operación por sesión | **≈ $35 / sesión** | ≈ $87 / sesión |

**Queda por debajo del piso de detectabilidad del proyecto** ($29 a $58 por operación con
presupuesto de 1.000 operaciones). Y hay que restarle el costo: con una ida y vuelta por sesión son
**≈ $17** entre medio-spread de entrada, medio-spread de salida y comisión, así que de los $35 brutos
quedan **≈ $18 netos**. Ver `PISO_Y_CONVERSION.md` para las dos definiciones de piso y la
procedencia de cada número. Ver el punto 10: ése es el problema central de esta candidata.

## 5. Antes o después de costos

**Antes.** Los autores lo dicen explícitamente: *"no consideramos costos de transacción"*, y
advierten que con rebalanceo frecuente la estrategia tal como está presentada puede no ser
explotable para muchos inversores.

Pero agregan una frase que apunta directo al caso de Roberto: **explotar el efecto en los futuros
del S&P 500 da un Sharpe neto positivo suponiendo un costo de un tick**, nivel que describen como
el que enfrenta habitualmente un operador avanzado en ese mercado. Un tick de ES son 0,25 puntos =
$12,50 por contrato por lado.

Esa afirmación no viene con tabla en el paper. Es una aseveración de los autores, no un resultado
tabulado. **Anotarla como afirmación, no como número medido.**

## 6. Mecanismo declarado

**Cobertura de gamma corta.** Los creadores de mercado de opciones y los emisores de ETF apalancados
suelen quedar netos cortos de gamma. Para mantenerse neutrales en delta tienen que **comprar cuando
el precio sube y vender cuando baja**. Ese flujo va en la misma dirección que el movimiento y
produce momento intradiario. Concentrado al cierre porque ahí es cuando se rebalancea.

Evidencia que los autores dan a favor:
- El efecto persiste **sólo cuando la exposición neta a gamma (NGE) de los creadores de mercado es
  negativa** (Tabla 7). Con NGE positiva, no.
- Corte transversal: los mercados con más presencia de ETF apalancados tienen t-estadísticos de
  `rROD` más altos (Figura 4, submuestra 2006–2020).
- El efecto **se revierte en los días siguientes**, lo que es la firma de una presión de precio
  temporal y no de información nueva.

Esa última parte es la que hace al mecanismo falsable: si fuera información, no se revertiría.

## 7. CLASIFICACIÓN

**ESTADÍSTICA.** Es una tendencia, no una garantía. Cae de lleno bajo el muro de miles de
operaciones: el veredicto se decide por acumulación, no por casos.

La parte del mecanismo que sí tiene forma determinista —el rebalanceo de los ETF apalancados es una
fórmula escrita en el prospecto— está separada en la ficha **L04**.

## 8. Estado de replicación

Mixto, y hay que leerlo con cuidado.

**A favor:**
- Este paper *es* la replicación en futuros de Gao et al. (2018) — ver **L02** — con muestra 12 años
  más larga y 60 instrumentos en vez de un ETF.
- Extendido a bonos del tesoro chinos (Zhang, Wang y Li, 2021), crudo (**L09**) y futuros de VIX
  (**L06**), con el mismo signo.
- Li, Sun y Wang (2021) reportan el efecto en 16 mercados desarrollados.

**En contra, y es serio:**
- **Rosa, Carlo (2022). "Understanding intraday momentum strategies." *Journal of Futures Markets*,
  vol. 42, n.º 12, pp. 2218–2234.** DOI 10.1002/fut.22375. Estudia el desempeño **fuera de muestra**
  de la versión donde el retorno nocturno predice la última media hora, y **la predictibilidad
  desaparece en el período fuera de muestra**. Un modelo de cambio de régimen identifica dos
  regímenes y sugiere que la predictibilidad depende de la fuerza de la señal, no del calendario.
- Limkriangkrai, Chai y Zheng (2023), *Pacific-Basin Finance Journal* 80, 102086: en Asia-Pacífico
  el efecto aparece en China y Japón, es débil en Corea del Sur y **no aparece en Hong Kong ni en
  Singapur**. Y se debilita durante la crisis de COVID en los mercados donde sí existe.
- Contexto general: McLean y Pontiff (2016) miden que los retornos de anomalías publicadas caen
  **26 % fuera de muestra y 58 % después de publicadas**. Este paper se publicó en 2021.

**No encontré una replicación independiente de la versión `rROD` en ES posterior a 2021.** Eso es un
hueco, no una ausencia de evidencia negativa.

## 7-bis. Dos condicionamientos publicados que apuntan a lados distintos

**El paper trae dos formas de concentrar el efecto, y no son la misma. Las dos van escritas y
NINGUNA elegida, porque elegir entre ellas es un grado de libertad nuestro.**

**Condicionamiento 1 — cuando los signos DIFIEREN.** Sección 3.4 y Tabla 3: el retorno del día
completo gana la comparación directa contra el de la primera media hora en las dos submuestras, *"y
especialmente cuando sus signos difieren"*. En futuros de índice, bonos y materias primas, cuando
difieren **el coeficiente de la primera media hora tiene el signo equivocado y el del día completo
sigue positivo y muy significativo**.

**Condicionamiento 2 — cuando los signos COINCIDEN.** La estrategia combinada de la Tabla 6 toma
posición **sólo cuando los dos predictores tienen el mismo signo** y no opera cuando difieren. Es la
que da la **tasa de acierto más alta del paper, 61 %**, contra 55 % de las otras dos.

## Por qué no son contradictorios, y por qué igual son una trampa

**No se contradicen: hablan de cosas distintas.** El primero es sobre **qué predictor es mejor**; el
segundo es sobre **cuándo operar**. Que el día completo sea el mejor predictor justo cuando los
signos difieren es compatible con que la estrategia más segura sea no operar esos días.

**Pero para nosotros son dos reglas operables distintas que salen del mismo paper, y quedarnos con
una es una decisión nuestra.** Por `F9`, es una pieza **con grado de libertad**.

| si se elige | qué se gana | qué se paga |
|---|---|---|
| operar sólo cuando **coinciden** | tasa de acierto de 61 % | menos días, y es la regla que el paper presenta como estrategia |
| operar sólo cuando **difieren** | el predictor está en su mejor momento | el paper **no** reporta una estrategia para ese caso |
| operar **siempre** con el día completo | es la regla principal del paper, 6,86 % anual y Sharpe 1,73 | no usa ninguno de los dos condicionamientos |

**La tercera fila es la única que no exige que elijamos.** Si alguna vez se mide L01, ésa es la que
no gasta un grado de libertad, y las otras dos se declaran como variantes si se usan.

**Queda anotado y no resuelto, a propósito.**

## 8-bis. Quiénes son los autores, que corta para los dos lados

**Baltussen y Martens trabajan en Robeco Asset Management**, y lo declaran en la portada del paper.
Da y Lammers son académicos.

**Es información mejor y es un conflicto, las dos cosas, y no resuelvo cuál pesa más.**

- **A favor:** el mecanismo que proponen —cobertura de gamma de creadores de mercado y emisores de
  ETF apalancados— es un flujo que se ve desde adentro de una gestora y no desde una base de datos.
  Un académico puro probablemente no lo habría propuesto.
- **En contra:** una gestora tiene interés en que su marco de referencia circule, y quien publica
  desde adentro elige qué publicar.

**Es el mismo patrón en tres de las once fichas** —esta, L08 y L10— **y las tres son de efectos de
flujo de calendario.** Que las tres vengan de gente que ve el flujo no es casualidad, y por eso la
nota va en las tres.

## 9. Cuántas variantes probaron los autores

**Declarable con honestidad: no menos de una docena, y el paper no publica un barrido completo.**

Lo que se puede contar de lo publicado:
- **3 señales** distintas (`rONFH`, `rROD`, la combinada) sobre la misma ventana de salida.
- **3 ventanas de salida** en la Tabla 12: última media hora, últimos 15 minutos, últimos 5 minutos.
- **4 predictores** en la Tabla 12: `rONFH`, `rM`, `rSLH`, `rROD`.
- **4 clases de activo** × más de 60 contratos, con carteras 1/N por clase.
- **2 definiciones de cierre** para el S&P 500 (16:00 del contado y 16:15 del futuro).
- Submuestras por década, por régimen de NGE, y por cuota de mercado de ETF apalancados.

Para el campo `variantes_probadas` del juez, **declarar 10 como mínimo** (umbral de 3,7 desvíos), y
argumentar que 100 (umbral 4,3) es la lectura conservadora si se cuenta el producto de ventanas ×
predictores × clases.

## 10. Qué haría falta para probarla acá

**Datos: NINGUNO NUEVO.** Se prueba entera con ES 1-min Databento 2016-2019, que ya está en el repo
(1.357.785 barras, 1.007 sesiones de contrato único).

**Forma de entrada para el juez** (`research/ventana_g/JUEZ_COMO_SE_USA.md`):

```
señal   : signo del retorno desde el cierre de la sesión anterior hasta 30 min antes del cierre
entrada : una operación por sesión, a la barra de 30 min antes del cierre
salida  : {"tipo": "tiempo", "n_barras": 30}
```

Es una regla de salida por tiempo, que el juez acepta. **No hace falta elegir bracket**, y por lo
tanto **no hay sesgo de contabilidad que corregir** (`PROTOCOLO_medir_un_candidato.md`): a los 30
minutos la posición se cierra a mercado, resuelva o no.

### El problema, dicho antes de medir

**Con una operación por sesión, 2016-2019 da ~1.007 operaciones, y eso no alcanza.**

El juez publica su propia resolución: ±33 % de la ventaja con ~5.000 operaciones. Escalando por
raíz de n, con 1.007 operaciones la resolución es de ±74 %. Una ventaja real de $35 por sesión se
mediría como **$35 ± $26**. Eso es 1,3 desvíos contra una nula, y el juez pide **3,7** con diez
variantes declaradas.

En tasa de acierto el diagnóstico es el mismo: la ventaja declarada es de **2 puntos** (55 % contra
53 % de la posición pasiva), y la diferencia mínima detectable del proyecto con 1.000 operaciones
está entre **3,70 y 3,98 puntos** (`salida_piso_ventaja.txt`). **La ventaja publicada es la mitad
del piso de detección.**

**Traducido: si esta candidata es cierta y se la mide tal cual sobre 2016-2019, el resultado
esperable es NO SUPERA — y ese NO SUPERA no dirá nada sobre el mercado.** Sería exactamente el
falso negativo estructural que el juez ya declara no cubrir.

### Las tres salidas, ninguna gratis

1. **Más operaciones por sesión.** Para llegar a ~5.000 operaciones sobre 1.007 sesiones harían
   falta ~5 por sesión. El paper no define cinco entradas por sesión; inventarlas es volver al
   generador de siempre.
2. **Más sesiones.** ~5.000 sesiones son ~20 años. Sale de la caja sellada 2020-2026, que tiene
   un solo uso y no es de esta ventana.
3. **Condicionar por régimen y medir sólo donde el efecto es grande.** Es lo que el propio paper
   propone con la gamma neta (ver **L05**), y es lo que la VENTANA G ya construyó con el eje de
   volatilidad de la sesión anterior. **Ésta es la única de las tres que no cuesta ni datos nuevos
   ni cartuchos** — pero elegir el tercil después de mirar es selección, así que el tercil se
   declara antes.

**No resuelvo cuál. No es mi trabajo medir.**

---

## Pregunta abierta que dejo anotada, sin resolver

Los autores encuentran que el efecto vive donde la gamma neta es negativa. La VENTANA G midió que
el **piso** de la evaluación va de $5,07 a $105,34 por sesión entre el tercil bajo y el alto de
volatilidad de la sesión anterior — **20,8× — y monótono** (`juez_regimen_exante.py`).

Si el efecto de la literatura crece con la volatilidad *y* el piso también crece con la volatilidad,
**no está dicho que el cociente mejore**. Puede empeorar. Es una pregunta de dos números medidos y
un cociente, y **no la contesto acá**.

Ver la misma pregunta planteada desde el paper de calibración en **L02**.
