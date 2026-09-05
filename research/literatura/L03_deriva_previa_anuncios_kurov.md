# L03 — El precio ya se mueve en la dirección correcta 30 minutos ANTES de que salga el dato macro

**VENTANA L. Ficha de literatura. NO MEDIDA. No gasta cartucho, K sigue en 261.**

> **GRADO ACTUALIZADO — 2026-09-05: esta ficha pasa de C a B.** La refutación de Kurov et al. 2022 es sobre anuncios británicos y futuros de divisas: **por la prueba de simetría de `F13`, evidencia de otro mercado no cuenta en NINGUNA de las dos direcciones.** El riesgo queda nombrado: el mecanismo depende del acceso anticipado y en Estados Unidos hubo cortes equivalentes en 2013-14, **pero no hay evidencia directa sobre el ES**. Y ver [D06](D06_balanza_ciega.md): su veredicto operativo es REQUIERE MEDICIÓN.

---

## 1. Cita completa

Kurov, Alexander; Sancetta, Alessio; Strasser, Georg; Wolfe, Marketa Halova (2019). **"Price Drift
before U.S. Macroeconomic News: Private Information about Public Announcements?"**
*Journal of Financial and Quantitative Analysis*, vol. 54, n.º 1, pp. 449–479.

Circuló como ECB Working Paper 1901 (2016). Borrador citado acá: 1 de marzo de 2017.

- Editorial: https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/abs/price-drift-before-us-macroeconomic-news-private-information-about-public-announcements/E1AE41FB94D4F2CA5134410D5C82A0E2
- PDF: https://www.skidmore.edu/economics/documents/KurovSancettaStrasserWolfe-2017PriceDriftBeforeUSMacro.pdf
- SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2637528

## 2. El efecto, en una frase

En ciertos anuncios macroeconómicos de fecha y hora publicadas de antemano, el precio del futuro
empieza a moverse en la dirección que después va a confirmar el dato **unos 30 minutos antes** de
que el dato salga.

## 3. Instrumento y período de la muestra original

- **Futuros del E-mini S&P 500 (ES)** y **futuros del bono del tesoro a 10 años (ZN)**, contrato
  cercano, del CME.
- **Datos segundo a segundo** de Genesis Financial Technologies, **1 de enero de 2008 → 31 de marzo
  de 2014**.
- **30 anuncios macroeconómicos** estadounidenses examinados. De los 20 que mueven mercados, **9
  muestran comercio informado sustancial** antes de la hora oficial.

**Los cuatro que muestran deriva en el ES son:**

| anuncio | organismo | hora de publicación (ET) | coeficiente ES | t |
|---|---|---|---|---|
| ISM no manufacturero | ISM | **10:00** | 0,104 | *** |
| Ventas de viviendas pendientes | NAR | **10:00** | 0,099 | *** |
| ISM manufacturero | ISM | **10:00** | 0,088 | *** |
| Ventas de viviendas usadas | NAR | **10:00** | 0,054 | *** |

En el ZN son nueve, y ahí entran también los de las 8:30 (peticiones de subsidio, ventas minoristas,
PIB preliminar, producción industrial y otros).

**Los cuatro del ES salen todos a las 10:00 ET.** No es coincidencia menor y los propios autores dan
la razón: a las 9:30 abre el contado y el volumen del ES se multiplica **por más de cinco**, así que
la media hora de 9:30 a 10:00 es el mejor momento del día para esconder una orden informada
(argumento de Kyle 1985). El operador informado elige la ventana más líquida.

## 4. Magnitud declarada

- **La deriva previa se lleva en promedio el 40 % del ajuste total de precio** del anuncio.
- Los coeficientes de la tabla son el movimiento porcentual del ES en la ventana
  `[t − 30 min, t − 5 s]` por **una desviación estándar** de sorpresa: entre **0,054 % y 0,104 %**,
  o sea **5,4 a 10,4 puntos básicos**.
- Ganancia total estimada de quien operó en la dirección correcta antes del dato, en poco más de
  seis años: **$95 millones en el ES** y **$89 millones en el ZN**.

### Traducción a dólares por evento por contrato ES

Con la convención del índice (ES 2016-2019, nocional ≈ $130.000): **1 punto básico ≈ $13**.

| | por evento, ES 2016-2019 | por evento, precios 2026 |
|---|---|---|
| 5,4 pb (ventas de viviendas usadas) | **≈ $70** | ≈ $173 |
| 10,4 pb (ISM no manufacturero) | **≈ $135** | ≈ $333 |

**Por evento supera el piso de detectabilidad por operación** ($29 a $58, `PISO_Y_CONVERSION.md`),
incluso después de restarle los ≈ $17 de costo de una ida y vuelta. **Es la única candidata del lote
cuya magnitud por operación no es marginal.** El problema no es la magnitud: es el número de
eventos. Ver punto 10.

## 5. Antes o después de costos

**Antes, pero con la comparación hecha.** Los autores reportan el **spread efectivo mediano** de su
muestra: **0,020 % en el ES** (2 puntos básicos, ≈ $26 por contrato en 2016-2019) y 0,013 % en el
ZN. Y observan que eso está **muy por debajo** de la banda de dos desvíos del retorno acumulado
alrededor de los anuncios con deriva, y que un operador con algoritmo de ejecución puede operar
cerca del punto medio.

Su conclusión textual es que las operaciones informadas alrededor de esos anuncios **son
rentables**. Es una conclusión sobre el informado, no sobre el que sigue la deriva sin saber nada.
Ver punto 10.

## 6. Mecanismo declarado

**Información privada sobre un anuncio público.** Los autores lo dicen sin eufemismo: alguien sabe.
Las fuentes que proponen son una combinación de:

- **Filtración de información** antes de la hora oficial. Citan el caso del ISM y el de Thomson
  Reuters/Universidad de Michigan, que vendía acceso anticipado a los datos a operadores por dos
  segundos, y que la SEC valoró en más de $100 millones de ganancias ilegales.
- **Pronóstico superior** que incorpora datos propietarios: alguien que reconstruye el dato antes de
  que salga con información privada que compró o recolectó.

Y explican por qué la deriva arranca recién 30 minutos antes y no horas antes: para minimizar la
exposición a riesgos no relacionados con el anuncio, y para esconderse en el volumen.

**Control que hacen y que importa:** también calculan la ganancia de operar en la dirección del
flujo de órdenes **en días sin anuncio**, y da **un orden de magnitud menos**. El efecto no es
"seguir el flujo siempre funciona".

## 7. CLASIFICACIÓN

**MIXTA, y hay que decirlo así en vez de forzarla a una de las dos casillas.**

- **DETERMINISTA en la FECHA Y LA HORA.** El calendario de publicación del ISM y de la NAR está
  escrito y publicado con meses de anticipación. La ventana `[9:30, 10:00]` de ciertos días
  concretos no se descubre buscando: se lee en un calendario. Eso es exactamente lo que el encargo
  pide preferir.
- **ESTADÍSTICA en el SIGNO.** El paper mide la deriva **condicionando a la sorpresa que después se
  publicó**, y la sorpresa no se conoce al entrar. Para operarlo sin información privada hay que
  reemplazar "la sorpresa" por un observable: el propio movimiento de precio o el flujo de órdenes
  de esa media hora. **Esa sustitución no está probada en el paper.**

**Ésta es la candidata con la mejor forma —fecha escrita, mecanismo nombrado, magnitud por encima
del piso— y con la traducción más peligrosa. La sustitución del signo es donde se cuela la búsqueda.**

## 8. Estado de replicación

- El paper mismo es una revisión al alza de literatura previa (Andersen et al. 2007 miraban diez
  minutos antes; Hautsch, Hess y Veredas 2011; Bernile, Hu y Tang 2016). El aporte es la ventana de
  30 minutos y la muestra moderna.
- **Cambio institucional posterior que hay que verificar antes de probar nada:** la muestra termina
  en marzo de 2014. En 2013–2014 hubo intervención regulatoria sobre las publicaciones anticipadas
  (el caso Thomson Reuters/Michigan se cerró en 2013; el ISM cambió sus procedimientos). **Los
  datos del proyecto son 2016-2019, o sea enteramente posteriores al cierre de la muestra y
  posteriores a esos cambios.** No encontré una replicación publicada del efecto en ES para
  2016-2019.
- **Eso corta para los dos lados.** Es fuera de muestra de verdad, que es lo que este proyecto
  quiere. Y es un período en el que el mecanismo declarado pudo haber sido desactivado por
  regulación, que es una razón concreta para esperar que no esté.

## 9. Cuántas variantes probaron los autores

**Declarable con precisión inusual, porque el paper lo dice: 30 anuncios × 2 mercados = 60 pruebas.**

De esas 60, reportan que 9 muestran deriva. Y la tabla completa de los 30 anuncios con sus
p-valores está publicada, lo que es honesto y raro.

Además: ventanas de `[t−30min, t−5s]` y otras; robustez en dos mercados adicionales (E-mini Dow y
bono a 30 años); datos segundo a segundo y minuto a minuto.

**Para el juez: `variantes_probadas` = 60 como mínimo.** Ése es el número que el propio paper
declara, y con 60 el umbral de desvíos del juez se va cerca de 4,3. **Es la candidata que llega con
la multiplicidad peor y mejor documentada del lote.**

## 10. Qué haría falta para probarla acá

**Datos de precio: NINGUNO NUEVO.** ES 1-min 2016-2019 alcanza para la versión de precio.

**Dato que falta y es gratis:** el calendario con fecha exacta de las publicaciones del **ISM
manufacturero, ISM no manufacturero, ventas de viviendas usadas y ventas de viviendas pendientes**
entre 2016 y 2019. Son públicas y archivadas (ISM y National Association of Realtors publican sus
calendarios históricos). Hay que armar el archivo a mano o rasparlo. **Es medio día de trabajo, no
un gasto.**

**Dato que falta y NO tenemos:** el flujo de órdenes firmado (qué parte del volumen fue iniciada por
el comprador). Con barras de un minuto no se reconstruye. La VENTANA G ya cotizó lo que cuesta:
**un día entero de ES en `tbbo` cuesta $0,79 y en `mbo` $0,90** (commit 1aa1039). Los cuatro
anuncios dan unos **48 eventos por año** → ~192 días de datos para 2016-2019 → **entre $150 y $175**
por el flujo firmado de esos días. Es barato en dinero. **No es barato en cartuchos.**

### El número que decide, dicho antes de medir

**Cuatro anuncios, doce publicaciones al año cada uno: ~48 eventos por año, ~192 eventos en
2016-2019.**

Con 192 operaciones y una ventaja por evento de $70 a $135, la resolución del juez (±33 % con ~5.000
operaciones, escalada por raíz de n) da **±167 %**. Una ventaja de $100 se mediría como
**$100 ± $167**. **No es medible. El juez debería devolver NO MEDIBLE, y tendría razón.**

Para llegar a 3 desvíos con esa ventaja harían falta del orden de **1.700 eventos**, o sea unos
**35 años** de esos cuatro anuncios.

**Salidas posibles, todas con su costo, y ninguna la elijo yo:**

1. **Agregar anuncios.** Los nueve del ZN dan más eventos, pero ZN no está en los datos del proyecto
   y su comisión no está medida (el juez sólo acepta ES y MES).
2. **Agregar los anuncios de las 8:30.** No están en la lista de los cuatro con deriva en ES;
   meterlos es cambiar la regla del paper.
3. **Aceptar que esta candidata es de las que se verifican por CASOS y no por acumulación**, y
   mirarla como candidata determinista: ¿en los ~192 eventos de 2016-2019, el precio derivó en la
   dirección del dato posterior? Eso es una pregunta descriptiva sobre el mecanismo, no una medición
   de ventaja, **y contestarla no requiere gastar un cartucho** — pero tampoco produce una ventaja
   operable.

---

## Cruce con L01 y L02 que dejo anotado y no resuelvo

Los cuatro anuncios con deriva en el ES salen **a las 10:00 ET**. La ventana de deriva es por lo
tanto **de 9:30 a 10:00 ET**, que es **exactamente la primera media hora de rueda** que Gao et al.
usan como predictor `r1` en **L02**.

Y Gao et al. reportan, por su lado, que el momento intradiario es **más fuerte en días con noticias
económicas importantes**.

**Las dos literaturas pueden estar describiendo el mismo día desde dos puntas.** Si en los días de
ISM la primera media hora contiene deriva informada hacia el dato de las 10:00, entonces `r1` en
esos días no es "el arranque de la rueda": es otra cosa.

**No sé si eso hace la señal mejor o peor, y no lo averiguo.** Lo dejo escrito porque quien mida L02
debería saber que los días de ISM no son días cualesquiera dentro de su muestra.
