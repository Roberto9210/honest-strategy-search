# ¿HAY N NUEVO FUERA DE LA CAJA? — Ventana D, 2026-09-03

Pregunta de Roberto: los minutos de ES de Databento llegan a 2010; 2010–2015 está fuera de la caja
(que empieza en 2020) y fuera de lo que barrió la fase 1 (2016–2019). ¿Son N nuevo?

Salida cruda: `inventario_2010_2015.txt` (commit `d2bff1a`). El script cuenta barras y sesiones, no
evalúa ninguna estrategia y no mira ningún retorno. **No gasta cartucho.** La caja no se tocó.

## 1 · ¿Existen esos datos?

**Sí, el archivo los tiene, y no sirven.** `data/es_1min_databento.csv` va de 2010-06-07 a 2026-08-18.
Sesiones que pasan los filtros de la P-escalera (día hábil, contrato único, no degradada, barra a las
17:00 y a las 08:30 CT, RTH hasta las 15:00):

| año | pasan filtros | barras/día medianas | % días con < 1.300 barras |
|---|---|---|---|
| 2010 | 28 | 150 | 84,1 % |
| 2011 | 64 | 145 | 77,8 % |
| 2012 | 99 | 126 | 77,5 % |
| 2013 | 201 | 1.239 | 80,1 % |
| 2014 | 193 | 1.241 | 84,4 % |
| 2015 | 212 | 1.268 | 72,0 % |
| **2016** (referencia) | 245 | 1.362 | 5,0 % |

**Total 2010–2015: 797 sesiones.** Pero el número engaña: pasar los filtros sólo exige que existan la
barra de las 17:00, la de las 08:30 y una barra al cierre de RTH. **Entre el 72 % y el 84 % de esas
sesiones tienen menos de 1.300 barras**, contra el 5 % de 2016. Una sesión con 1.240 minutos de 1.380
tiene 140 minutos que no existen, y la excursión adversa se mide justamente sobre el mínimo y el
máximo: cada minuto ausente puede ser el que contenía el extremo. **Los años 2010–2012, con 126 a 150
barras por día medianas, no son una serie de minutos: son un resumen.**

Agregar un diario desde esos minutos es posible mecánicamente y no arregla nada: agregaría el diario
de una sesión que ya viene incompleta.

## 2 · ¿La spec los sella? Cita textual

Sí, y por nombre. `factory/spec_fase2.md` (`e17cde9`), §4.4:

> **«Ventana admitida: 2016-01-01 → 2026-08-18.»**

> **«2010–2015 no se re-habilita.** Si una re-curación futura de Databento arreglara esos años, eso es
> de hecho una fuente nueva: exige QC regenerado y publicado, y **declaración antes de que exista la
> candidata que se beneficiaría**.»

> **«Las ventanas de arriba quedan congeladas al firmar.** Está prohibido ampliarlas, recortarlas o
> cambiarles la fuente **después de** que haya corrido una sola configuración.»

Y el párrafo que anticipa esta conversación exacta, escrito el 2026-08-24, once días antes de que la
tuviéramos:

> «Dentro de tres semanas, justo después de una candidata que quede cerca de la barra, alguien va a
> proponer "extender el histórico diario" o **"recuperar 2013–2015 para intradía ahora que sabemos que
> el defecto era parcial"**. **Va a tener razón técnicamente y va a estar haciendo trampa**, porque la
> ventana elegida después de ver un resultado es un parámetro más de la búsqueda — uno que no está
> contado en K y que nadie va a contar.»

> «Si aun así se decide ampliar una ventana, la ampliación **es una fase nueva**: spec propia,
> presupuesto propio, y el contador heredado (§1.6). No es una corrección técnica de la Fase 2.»

La spec nombró el rango, el argumento y el momento. Estamos parados exactamente ahí.

## 3 · ¿Cuánto bajaría el efecto mínimo detectable?

El desvío del cociente de p95 escala como 1/√n. Base medida: 0,1514 con 951 sesiones.

| corpus | n | MDE del cociente de p95 | contra el 1,51× que existe |
|---|---|---|---|
| hoy | 951 | **2,00×** | no alcanza |
| + 2013–2015 | 1.557 | 1,72× | no alcanza |
| + 2010–2015 completo | 1.748 | **1,67×** | **no alcanza** |
| lo que haría falta | 2.686 | 1,51× | — |

**Aunque se admitieran las 797 sesiones malas, no alcanzaría.** Harían falta 1.735 sesiones nuevas,
casi siete años de negociación, y sólo existen 797 de calidad inferior. La respuesta a la pregunta es
**no por dos motivos independientes**: la spec las sella y, aun sin el sello, la aritmética no llega.

## 4 · Lo que sí apareció, y no estaba en la pregunta

Buscando lo anterior encontré que **este repo ya tiene una serie diaria que no está sellada**:
`data/es_daily.csv` (Yahoo, ES=F), 2000-09-18 → 2026-08-19, 6.544 filas. Su **parte A son 4.875
sesiones**, todas fuera de la caja, y la spec las declara admitidas para desarrollo (§4.4, régimen
diario). Tiene `open`, `high` y `low`, así que la excursión adversa diaria es medible sin minutos.

| corpus | n | MDE del cociente de p95 |
|---|---|---|
| parte A diaria sola | 4.875 | **1,36×** |
| parte A + las 951 | 5.826 | 1,32× |

**Con 1,36× el efecto de 1,51× sería detectable.** Antes de que eso suene a puerta abierta, las cuatro
cosas que hay que decir:

1. **No es la misma población, es otra.** El día de Yahoo no es la sesión ETH de 17:00 → 16:00 que
   midió toda la escalera. Es un continuo front-month sin ajustar por roll, con 10 filas de artefacto
   excluidas. Todo lo medido en la escalera **no traslada**: habría que medir el terreno de nuevo ahí.
2. **El 1,51× fue medido en la otra población.** No hay ninguna garantía de que el mismo efecto de
   cola exista con ese tamaño en el día de Yahoo, y suponerlo sería usar un número de un corpus para
   justificar una prueba en otro.
3. **Es la serie que la fase 2 barrió con las familias G.** Barrer no sella, pero cada configuración
   nueva sobre ella paga K igual, y K ya está en 263.
4. **Elegir esta serie ahora, después de que la anterior no alcanzó, es exactamente el movimiento que
   §4.4 llama trampa.** La diferencia es que esta serie **ya estaba declarada** en la spec y no hay
   que ampliar ninguna ventana para usarla. Esa diferencia es real, y aun así el pre-registro tendría
   que abrir diciendo por qué se cambió de corpus.

## 5 · Estado del corpus, para que quede escrito

- **Minutos de ES, 2016–2019:** 951 sesiones útiles. Barridas para dirección. MDE de cola 2,00×.
- **Minutos de ES, 2010–2015:** 797 sesiones que pasan filtros, con 72–84 % de días incompletos.
  **Selladas por §4.4.** Aun admitidas, MDE 1,67×: no alcanzan.
- **Minutos de ES, 2020–2026:** la caja. Un solo uso para todo el programa. **Sigue cerrada.**
- **Diario de Yahoo, 2000–2019:** 4.875 sesiones, admitidas, fuera de la caja, otra población. MDE
  1,36×. **Es el único corpus del repo donde una pregunta de cola sería decidible.**
- **Diario de NT8 (guardián):** ES 2.579 fechas, MES 1.880. Su hueco de apertura ya se midió y no
  sirve para preguntas nocturnas (4,01 % de la varianza).

**En el corpus de minutos, la búsqueda se cierra con estos números.** Si sigue, sigue en otra
población y con esa mudanza declarada por delante. Eso es decisión de Roberto.
