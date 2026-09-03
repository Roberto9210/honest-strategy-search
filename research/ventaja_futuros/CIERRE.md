# CIERRE DE LA BÚSQUEDA DE VENTAJA — Ventana D — 2026-09-03

Decisión de Roberto del 2026-09-03: **se cierra la búsqueda de ventaja en este corpus.** No se abrió
la caja fuerte del programa. Este documento se escribe sin suavizar nada.

Si sólo vas a leer una sección, leé la **parte II**: es el terreno medido, que es el resultado útil de
esta fase y se puede usar sin haber leído nada de la parte I.

---

# PARTE I · POR QUÉ SE CIERRA

## 1 · Las tres cifras que lo cierran

| | |
|---|---|
| efecto que **existe** en la cola de la excursión adversa | **1,51×** |
| efecto **detectable** con α = 0,05/264, 951 sesiones | **2,00×** |
| efecto detectable **sin la deuda de multiplicidad** (α = 0,05) | **1,53×** |

Las tres se leen juntas en una sola frase: **el efecto es real, es demasiado chico para el α que este
programa arrastra, y habría sido detectable sin esa deuda.** El 1,53 contra el 1,51 es el margen: la
búsqueda pasó a dos centésimas de poder pronunciarse, y no se pronuncia.

## 2 · Las cuatro hipótesis muertas, y de qué murió cada una

| hipótesis | murió de | número que la mató |
|---|---|---|
| **H1** · la primera hora se mueve más que el resto del día | **sin población** | minutos de MES: 12 sesiones nominales, **0 utilizables**; los `.ncd` de minuto de NT8 no son legibles desde afuera |
| **H2** · el rango de la noche se rompe en la apertura | **sin población** | ídem |
| **H3** · el retorno de la primera media hora predice el de la última | **sin población** | ídem |
| **H2d** · el hueco de apertura tiende a extenderse | **control C0** | el hueco del diario de NT8 carga **4,01 %** de la varianza cierre→cierre, contra el 10 % exigido |
| **Forma 1** · ¿se conserva el orden de las horas? | **control K0** | excursión mediana **8,75 contra 8,75 pts**: la condición no separó por el estadístico que el control usaba |
| **Forma 3** · ¿la cola cruza el límite diario más seguido? | **potencia** | detectable desde **2,00×**, efecto real **1,51×** |

Dos aclaraciones que no se suavizan:

- **H1, H2 y H3 nunca llegaron a probarse.** Tenían un diseño condicional sobre los minutos de ES de
  Databento, y esa población requería una decisión de Roberto que el cierre alcanzó antes. Murieron
  sin población admitida, no por evidencia en contra.
- **La forma 1 no fue respondida: fue mal preguntada.** Su control K0 verificaba la condición con la
  **mediana**, y el efecto que la condición produce vive en la cola. El control funcionó como estaba
  escrito y mató una pregunta que quizás tenía respuesta. **No se aflojó el criterio después de verlo
  fallar**, y el cartucho se gastó igual. La lección está en `invariancia_orden_resultado.md` §3: la
  estadística del control se deriva de la pregunta.

## 3 · El contador queda en K = 263

261 heredados del programa (`spec_fase2.md` §1.1 y §1.6), más H2d, más la invariancia del orden. El
cartucho se gasta **al pre-registrar**, no al correr: H2d murió en su control sin producir una sola
operación y pagó igual; la invariancia del orden murió en el suyo y pagó igual.

**Cada pregunta futura de este programa paga más que la anterior.** La próxima corre a α = 0,05/264,
la siguiente a 0,05/265. El contador no se reinicia por cambio de fase, de instrumento, de objetivo ni
de persona, y el sobrante no se devuelve. Ésa es la mecánica que cierra esta búsqueda, y funcionó
exactamente como fue diseñada para funcionar.

## 4 · No se cierra por ausencia de efecto

**Esto es lo más importante del documento y no admite una redacción más suave.**

Se midió un efecto real: la excursión adversa del día que sigue a un rango grande tiene un p95 un 51 %
mayor. No es ruido, no es un artefacto: el control positivo del mismo diagnóstico separa con factor
2,29× y t = +10,32, así que la maquinaria detecta lo que hay que detectar.

Lo que ocurre es que **la deuda de multiplicidad acumulada excede lo que estos datos pueden mostrar.**
Con 951 sesiones, la línea de decisión a 0,05/264 exige 2,00× y el fenómeno da 1,51×. Con α = 0,05 el
umbral habría sido 1,53× y la pregunta habría sido decidible.

La afirmación correcta es: **«no pudimos distinguirlo del ruido al nivel que este programa exige»**.
Jamás **«el borde no existe»**. La distinción es la que `spec_fase2.md` §3.3 declaró de antemano para
el examen final, y rige acá igual.

## 5 · El corpus de Yahoo existe, alcanzaba, y no se usó

`data/es_daily.csv` (Yahoo, ES=F diario) está en este repo: 2000-09-18 → 2026-08-19, 6.544 filas, de
las cuales **4.875 son parte A**, fuera de la caja fuerte y **admitidas por la spec** (§4.4, régimen
diario). Tiene `open`, `high` y `low`, así que la excursión adversa es medible. El efecto mínimo
detectable ahí sería **1,36×**, por debajo del 1,51× que existe. **Alcanzaba.**

**No se usó, y el motivo se escribe entero:**

> `spec_fase2.md` §4.4, escrito el 2026-08-24, once días antes de que esta situación existiera:
> «Dentro de tres semanas, justo después de una candidata que quede cerca de la barra, alguien va a
> proponer "extender el histórico diario" [...]. **Va a tener razón técnicamente y va a estar haciendo
> trampa**, porque la ventana elegida después de ver un resultado es un parámetro más de la búsqueda —
> uno que no está contado en K y que nadie va a contar.»

Roberto reconoció que el argumento que iba a hacer tenía esa forma exacta y decidió no hacerlo. La
serie de Yahoo ya estaba declarada, así que usarla no habría sido ampliar una ventana; pero **elegirla
en el momento en que el otro corpus no alcanzó es exactamente el parámetro no contado del que habla la
cita.** Además es otra población —el día de Yahoo no es la sesión ETH de 17:00 → 16:00 que midió toda
la escalera— y el 1,51× fue medido en la población que se abandona, así que ni siquiera hay garantía
de que el efecto tenga ese tamaño allí.

También se evaluaron y se descartaron los minutos de 2010–2015: 797 sesiones que pasan filtros pero
con 72–84 % de días incompletos, **selladas por nombre en §4.4** («2010–2015 no se re-habilita»), y
que aun admitidas dejarían el umbral en 1,67×. Detalle en `corpus_2010_2015_resultado.md`.

## 6 · Si alguna vez se retoma

**Se retoma como programa nuevo**, no como continuación de éste. Las cuatro condiciones, escritas hoy
que no hay ninguna candidata a la que le convenga una respuesta u otra:

1. **La mudanza de población va declarada por delante**, en su propia spec, diciendo que el corpus
   anterior no alcanzó y que por eso se cambia. No al pie, no en un apéndice: en la primera página.
2. **El terreno se mide de nuevo en esa población.** Nada de la parte II traslada: son otras ventanas,
   otro instrumento nominal, otro régimen. Los cocientes trasladan mejor que los niveles, y aun así se
   miden otra vez.
3. **Ledger propio**, con su cadena de hashes, y el contador heredado: empieza en K = 263 y le suma su
   propio presupuesto declarado (§1.6).
4. **La caja fuerte del programa sigue siendo la misma**, 2020-01-01 → 2026-08-19, un solo uso para
   todo, y sigue cerrada. Un programa nuevo no estrena caja.

---

# PARTE II · LO QUE SÍ QUEDA: EL TERRENO MEDIDO

Esto se puede leer solo. Es lo que esta fase produjo y no depende de ninguna hipótesis.

**Población de todo lo intradiario:** ES 1-min de Databento, **971 sesiones**, 2016-01-04 → 2019-12-31,
día hábil, contrato único, no degradada, con barra a las 17:00 y a las 08:30 CT y RTH completa.
**Excursión adversa:** para el largo `apertura − mínimo`, para el corto `máximo − apertura`, en puntos
de ES. **Fricción:** 3,90 USD por ida y vuelta por contrato de MES = 0,78 puntos.

## A · Los instrumentos y sus datos

- **Diario de NT8** (guardián): 252 CSV, **ES 2.579 fechas, MES 1.880**. Contrato de máximo volumen
  por fecha, nada cruza un cambio de contrato. MES nace el **2019-05-06**.
- **La barra diaria de NT8 es la sesión ETH**, que empieza a las 17:00 CT del día anterior. Verificado
  sobre 828 barras de ES. Su `close` es la **liquidación** de ~15:14 CT, no el cierre de las 16:00.
- **Consecuencia dura:** `apertura − cierre previo` en ese diario mide el corte de mantenimiento de 60
  minutos, y carga **4,01 %** de la varianza cierre→cierre. La mediana de ese hueco es 1,00 punto
  contra 9,25 de cierre a cierre. **Ese diario no sirve para ninguna pregunta sobre el hueco nocturno**,
  sea MES, ES o NQ.
- **Databento y NT8 concuerdan:** 0,00 % de diferencia en los cinco percentiles de excursión sobre 828
  fechas comunes; 807 de 820 dentro de un tick.
- **Barras truncadas encontradas:** ES 2016-11-16, 2023-04-18, 2025-08-29; NQ 2016-11-16; MNQ
  2023-04-06; y una barra fantasma en MNQ 2025-01-01. Cuatro fechas con discordancia mayor a 2 puntos,
  **ninguna cerca de un roll**.
- **Traslado ES → MES:** el signo del hueco coincide el **96,61 %** de los días (98,44 % con hueco de
  un punto o más). ES contra NQ: 85,98 %, así que **NQ no es la misma pregunta**.

## B · Excursión adversa por duración de la tenencia

Percentiles en puntos de ES, lado largo, 971 sesiones:

| ventana | p50 | p90 | p95 | caída de p95 contra T23 |
|---|---|---|---|---|
| **T23** 17:00 → 16:00 | 8,75 | 32,75 | 51,12 | — |
| **RTH** 08:30 → 15:00 | 7,50 | 27,75 | 38,62 | 24,4 % |
| **H1** 08:30 → 09:30 | 4,00 | 12,75 | 16,88 | 67,0 % |
| **M15** 08:30 → 08:45 | 2,50 | 6,75 | 9,00 | 82,4 % |

**Cero sesiones superaron 1.000 USD** de excursión con un contrato de MES en ningún tramo. El máximo
absoluto fue **161,25 puntos = 806 USD**. Con p99 = 89,88 puntos, el 1 % peor está en 449 USD.

**El tiempo adentro es una palanca real y de rendimiento decreciente:** pasar de la sesión completa a
RTH ahorra un cuarto del p95; bajar a la primera hora ahorra dos tercios.

## C · La hora del día

23 tenencias de una hora, cociente contra la hora de la apertura (08:30 CT):

| hora CT | cociente p50 | cociente p95 |
|---|---|---|
| 23:00 | **0,19** | 0,25 |
| 12:00 | 0,56 | 0,67 |
| 08:30 (referencia) | 1,00 | 1,00 |
| 09:00 | — | p99 1,26 |
| 14:00 | — | p99 1,16 |

**La hora más barata cuesta un quinto de la apertura.** Control: la suma de las 23 excursiones horarias
supera la de la tenencia continua en las 971 sesiones, con cociente mediano 5,54; no hubo una sola
sesión donde fallara.

## D · Los stops

**Frecuencia de toque** (fracción de sesiones que alcanzan D puntos de excursión adversa):

| ventana / lado | D=2 | D=4 | D=10 | D=20 | D=30 |
|---|---|---|---|---|---|
| T23 largo | 87,3 % | 75,5 % | 46,2 % | 21,4 % | 12,2 % |
| RTH largo | 84,9 % | 70,9 % | 38,8 % | 16,8 % | 8,5 % |
| H1 largo | 74,0 % | 51,6 % | 16,6 % | 2,9 % | 0,3 % |
| M15 largo | 59,0 % | 29,7 % | 4,0 % | 0,2 % | 0,0 % |

Por hora: a las 23:00 CT un stop de 8 puntos se toca el **1,2 %** de las sesiones, contra **24,0 %** a
las 08:30.

**Desbordamiento más allá del stop:** mediana 0,25 puntos (un tick) en la misma barra, p95 entre 2 y 4,
máximo 31 en T23 largo; en la barra siguiente el máximo llega a 51. **La apertura de la barra que toca
el stop nunca lo atravesó**: 0,00 % en todas las ventanas y todos los D.

**Suma de pérdidas en 20 sesiones**, T23 largo, entrando siempre del mismo lado (no es una estrategia,
es terreno): con stop de 10 puntos, p50 = 90, p95 = 160, p99 = 180 puntos. Sin stop: p50 = 84 pero
**p95 = 353**. El stop no baja la pérdida típica; corta la cola, que es para lo que sirve.

## E · El agrupamiento de volatilidad, medido

El día que sigue a un rango grande (rango de ayer sobre su mediana móvil de 20) contra el resto:

| estadística de la excursión | cociente |
|---|---|
| mediana | **1,00×** |
| media | 1,25× |
| p90 | 1,37× |
| p95 | **1,51×** |
| p99 | 1,56× |

**No es un día típicamente más violento: es un día típicamente igual, con más probabilidad de ser
extremo.** El agrupamiento clásico sobre el rango está intacto (Spearman 0,58 entre rango de ayer y de
hoy), pero contra la **excursión adversa** cae a 0,29: el rango de ayer es un predictor flojo del
riesgo de hoy, y dimensionar contratos con él dimensiona contra poco.

## F · Limitaciones de todo lo anterior, sin excepción

1. **Es ES, no MES.** Sirve para la forma del terreno; la ejecución en MES no está medida. El traslado
   verificado es el del **signo del hueco** (96,61 %), nada más.
2. **Es 2016–2019**, un régimen aproximadamente la mitad de violento que el actual. **Los cocientes
   trasladan mejor que los niveles; los niveles no trasladan.** Nada de esto está verificado en
   régimen violento.
3. **Una tenencia de hora fija no es una estrategia**, y entrar siempre del mismo lado tampoco. Son
   sondas para medir el terreno.
4. **El deslizamiento no está modelado.** El desbordamiento medido está acotado por el movimiento del
   mercado, no por la profundidad del libro, que no se midió.
5. **La fricción de 3,90 USD es un supuesto declarado**, no una medición propia.
6. **El margen nocturno de MES sigue sin número verificado**, así que nada de esto autoriza declarar
   operable ninguna tenencia que cruce la noche.
7. **No hay ningún límite diario de cuenta fondeada verificado en este repo.** Se buscó.

---

## Índice de los archivos de esta fase

| archivo | qué tiene |
|---|---|
| `hipotesis_congeladas.md` | las cuatro hipótesis, sus enmiendas 1 a 3 y el descarte de H2d |
| `diseno.md` | el diseño de H2d con sus notas fechadas |
| `terreno_tenencia_*`, `terreno_horas_*`, `terreno_stop_*` | pre-registro, script, salida cruda y resultado de cada escalera |
| `discordancia_20161116_*`, `nt8_barras_truncadas.*` | el diagnóstico de las barras truncadas |
| `registro_multiplicidad.md` | la lectura cruzada de ALAYA y por qué se rechazó su máquina |
| `caja_alcance_y_uso.md` | qué es la caja fuerte, con citas textuales de la spec |
| `potencia_*.py/.txt` | todas las cuentas de potencia, incluida la de cola |
| `invariancia_orden_*` | el pre-registro, la corrida, el diagnóstico y la lección de K0 |
| `pregunta_cuanto_y_cuando.md` | las tres formas de pregunta de terreno y por qué las tres están cerradas |
| `corpus_2010_2015_resultado.md` | el inventario de lo que hay fuera de la caja |
| **`CIERRE.md`** | este documento |

**La caja fuerte del programa, 2020-01-01 → 2026-08-19, sigue sellada. Un solo uso, sin usar.**
