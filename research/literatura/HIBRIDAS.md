# HÍBRIDAS — candidatas que necesitan una pieza nuestra

**VENTANA L. NO MEDIDO. K sigue en 261.**

**Este documento existe porque me equivoqué de criterio.** En `P01` excluí a L03 de la prueba
agrupada porque su signo no está publicado y lo tendríamos que poner nosotros. **Roberto corrigió el
criterio y tiene razón: nunca se pidió pureza. Se pidió escapar de NUESTRO generador, que produjo
261 negativos. No es lo mismo.**

---

# EL CRITERIO CORRECTO

**La pregunta no es "¿la pieza la ponemos nosotros?" sino "¿la pieza que agregamos tiene una decisión
que se pueda AJUSTAR?"**

| tipo de pieza | qué es | qué cuesta |
|---|---|---|
| **SIN grado de libertad** — mecánica, pública, sin parámetros a elegir | **implementación** | nada. La idea sigue siendo de terceros |
| **CON grado de libertad** — elegir entre alternativas, calibrar un umbral, seleccionar una variante | **hipótesis nuestra** | cartucho, y arrastra multiplicidad |

**La diferencia práctica que lo justifica: una pieza sin ajuste no puede convertir un negativo en
positivo. Una con ajuste sí, y ahí es donde uno se engaña solo.**

**Aclaración de estado, porque puede haberse leído mal: L03 nunca se borró del inventario.** Sigue
siendo la candidata número 8 del índice. Lo que hice fue excluirla **de la prueba agrupada**, y es
esa exclusión la que se revisa acá.

---

# 1. ¿EXISTE PUBLICADA LA VERSIÓN OPERABLE DE L03?

**SÍ. Y en el instrumento que importa.**

**Bernile, Gennaro; Hu, Jianfeng; Tang, Yuehua (2016). "Can information be locked up? Informed
trading ahead of macro-news announcements."** *Journal of Financial Economics*, vol. 121, n.º 3,
pp. 496–520.
https://www.sciencedirect.com/science/article/abs/pii/S0304405X16300812

Lo que establecen, y es exactamente la pieza que faltaba:

> los **desbalances anormales de órdenes del futuro E-mini del S&P 500** van **en la dirección de la
> sorpresa de política posterior** y **contienen información que predice la reacción del mercado al
> anuncio**.

**Eso convierte un observable —el desbalance de órdenes antes de la publicación— en un predictor de
la reacción, publicado, sobre el E-mini.** No hace falta conocer la sorpresa: hace falta mirar el
flujo.

Y el propio paper de L03 aporta el resto de la especificación:
- **Ventana de entrada:** `[t − 30 min, t − 5 s]`, publicada.
- **Ventana de salida:** precio medio ponderado por volumen en `[t + 5 s, t + 1 min]`, publicada.
- **Construcción del desbalance:** volumen firmado acumulado sobre la ventana, **winsorizado en los
  percentiles 1 y 99**, publicada.
- **La correlación entre el signo de la sorpresa y el flujo de órdenes en el ES es +0,19**, publicada.

## ¿Queda algún grado de libertad?

**Uno, y hay que nombrarlo en vez de esconderlo: qué quiere decir "anormal".** Bernile et al. usan
desbalance *anormal*, y anormal exige una línea de base.

**Se elimina pinchándolo a la construcción de Kurov et al., que sí está especificada:** desbalance
acumulado crudo sobre la ventana, winsorizado 1/99, sin línea de base. **Declarado así, no queda
ninguna decisión ajustable.**

**Hay un segundo, y es el que más importa: los dos papers estudian conjuntos de anuncios distintos.**
Bernile et al. encuentran el efecto en los embargos del comité de política monetaria y **NO** en
nóminas no agrícolas, índice de precios al productor ni producto bruto. Kurov et al. encuentran los
cuatro de las 10:00. **Elegir el conjunto sería un grado de libertad.**

**Se elimina declarando ahora: el conjunto es el de Kurov et al. —ISM no manufacturero, ventas de
viviendas pendientes, ISM manufacturero, ventas de viviendas usadas— porque son los cuatro que ese
paper documenta con deriva EN EL ES**, que es el instrumento del proyecto. Bernile et al. entran
sólo como la evidencia publicada de que el observable predice la reacción.

## Veredicto sobre L03

**HÍBRIDA SIN GRADO DE LIBERTAD, una vez pinchadas las dos decisiones de arriba. Vuelve al
inventario principal y vuelve a ser elegible para la prueba agrupada.**

**El costo real no es conceptual, es de datos:** el desbalance de órdenes firmado **no se reconstruye
con barras de un minuto**. Hace falta `tbbo` o `mbo` de los días de anuncio. La VENTANA G ya tiene
cotizado que un día de ES en `tbbo` cuesta $0,79, y son 192 días. **Del orden de $150.**

---

# 2. LA LISTA DE HÍBRIDAS

Revisadas las once, no sólo L03.

| candidata | pieza que falta | ¿grado de libertad? | ¿publicada? | veredicto |
|---|---|---|---|---|
| **L03** | qué observable reemplaza a la sorpresa | **NO**, pinchada a Kurov + Bernile | **SÍ**, Bernile et al. 2016 | **HÍBRIDA. Vuelve** |
| **L02** | qué es "el cierre anterior" en ES: reapertura 17:00 CT, cierre 16:00 ET, o liquidación del CME | **SÍ**, tres alternativas defendibles | no para SPY→ES | **HÍBRIDA CON AJUSTE** |
| **L07** | qué días son *gotobi*: el texto dice 5, 10, 15, 20, 25 y fin de mes; las regresiones usan 5, 10, viernes y fin de mes | **SÍ**, dos conjuntos distintos en el mismo paper | ambos, en el mismo paper | **HÍBRIDA CON AJUSTE** |
| **L11** | qué anuncios cuentan: Savor y Wilson dicen inflación, desempleo y tasas; Ai, Bansal y Guo listan 44 días concretos | **SÍ**, dos listas publicadas distintas | ambas | **HÍBRIDA CON AJUSTE** |
| L10 | serie diaria de bonos | **NO**: el paper especifica futuros del bono a 10 años | sí, en el paper | falta el **dato**, no la pieza |
| L04 | patrimonio diario de los ETF apalancados | **NO**: la fórmula del flujo es la de Cheng y Madhavan | sí | falta el **dato** |
| L01, L05, L06, L08, L09 | ninguna | — | — | no son híbridas |

**Cuatro híbridas. Una sin grado de libertad, tres con.**

## Cómo se le quita el ajuste a las tres restantes

**No se les quita midiendo. Se les quita DECLARANDO, antes de correr, y aceptando que la
declaración es nuestra.**

- **L02:** declarar la definición que usa L01, que es el mismo efecto medido sobre ES con sesión
  9:30–16:00 pinchada por Baltussen et al. **Con eso L02 deja de tener ajuste propio y pasa a ser
  una réplica de L01 con otro predictor.**
- **L07:** declarar el conjunto del **texto** —5, 10, 15, 20, 25 y fin de mes— porque es la convención
  contable externa, que es lo que el filtro de calendario pide, y no el conjunto de las regresiones,
  que mezcla viernes y no es una regla de liquidación.
- **L11:** declarar la lista de **Savor y Wilson**, que es la fuente primaria, y no la de Ai, Bansal
  y Guo, que es una extensión posterior. Cuesta eventos: menos de 44 al año.

**Cada una de esas tres declaraciones es una decisión nuestra, y por lo tanto suma a
`variantes_probadas`. Con las tres declaradas, la prueba agrupada pasa de una variante a cuatro, y la
vara del juez sube de 3,0 a algo entre 3,0 y 3,7.** Ese costo es real y va escrito.

---

# 3. REVISIÓN HACIA ATRÁS DE LAS TRECE DESCARTADAS

**Resultado: ninguna vuelve. Y una merece una corrección de motivo.**

Repasadas las trece con el criterio nuevo, **ninguna fue descartada por "la pieza la ponemos
nosotros"**. Los motivos fueron ventana de exposición, muchos instrumentos, magnitud debajo del
piso, replicación fallida y acceso al mercado. **El criterio equivocado que Roberto corrigió sólo lo
apliqué en un lugar: la exclusión de L03 de la prueba agrupada.**

**La única que roza el asunto, con su corrección de motivo:**

**Griffin y Shams (2018), "Manipulation in the VIX?"** La descarté en parte por "no tiene signo
predecible", que suena a pieza faltante. **No lo es, y la distinción importa:** el signo depende de
cómo esté posicionado el manipulador, que **no es observable por nadie, ni por nosotros ni por un
tercero**. No es una pieza que haya que construir: **es una pieza que no existe**.

**Sigue descartada, y el motivo corregido es "la pieza no existe", no "la tendríamos que poner
nosotros".** Son cosas distintas y la segunda ahora es recuperable.

---

# 4. QUÉ CAMBIA EN P01

La prueba agrupada pasa de tres candidatas más una condicional a **cuatro más una condicional**.

| j | estado | `n_j` |
|---|---|---|
| L11 | entra, con la lista de anuncios declarada | 176 |
| L10 | entra | 48 |
| L08 | entra | 480 |
| **L03** | **entra, HÍBRIDA sin grado de libertad** | **192** |
| L07 | condicional | 288 |

**No recalculo el estadístico agrupado con L03 adentro, y digo por qué:** su `r_j` depende del
desbalance de órdenes, y **la magnitud publicada de 5,4 a 10,4 puntos básicos es la respuesta a la
sorpresa, no al desbalance**. La correlación entre los dos es +0,19, así que la señal del observable
es **mucho más chica** que la del inobservable.

**Poner un número ahí sería inventarlo.** La magnitud de la versión operable **hay que sacarla de
Bernile et al.**, que es un paso de literatura pendiente, y hasta entonces L03 entra a `P01` como
candidata declarada **sin peso asignado**.

**Ésa es la deuda concreta que deja este documento, y es de literatura, no de datos.**
