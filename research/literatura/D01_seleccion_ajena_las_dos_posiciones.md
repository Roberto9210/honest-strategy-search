# D01 — Cómo tratar la selección AJENA: las dos posiciones, SIN veredicto

**VENTANA L. NO MIDE NADA. K sigue en 261.**

> ## ESTE DOCUMENTO SE COMMITEA SIN VEREDICTO, A PROPÓSITO
>
> El veredicto va en `D02`, en un commit posterior. **El orden en el historial de git es la única
> prueba de que las dos posiciones se escribieron antes de decidir cuál gana**, igual que con una
> predicción sellada.
>
> **Y Roberto puso la condición correcta cuando dijo por qué no lo adopta todavía: la idea le
> convence justo cuando rescataría todo el inventario, y ésa es exactamente la condición bajo la
> cual uno razona motivado.** El mismo argumento le habría parecido flojo hace una semana.

---

# La cuestión, en una frase

**El juez sube la vara de desvíos según `variantes_probadas`. Ese campo se llena hoy con las
variantes que probaron los AUTORES del paper. ¿Corresponde?**

---

# POSICIÓN A FAVOR — la selección ajena y la propia son problemas distintos

## Los dos problemas no son el mismo problema

**Selección propia.** Probamos treinta variantes y reportamos la mejor. El p-valor está mal porque la
búsqueda tocó los mismos datos con los que se calcula. **No hay dato limpio disponible**: el que
tenemos ya fue mirado treinta veces. El remedio es **descontar** lo que no se puede limpiar, y subir
el umbral es una forma de descontar.

**Selección ajena.** Otro probó treinta, publicó una, y nosotros implementamos **esa** sin ninguna
libertad, sobre datos que su búsqueda no tocó. Acá **sí hay dato limpio**. El remedio no tiene por
qué ser un descuento: puede ser **usar el dato limpio**.

## Por qué fuera de muestra ELIMINA en vez de compensar

Una moneda elegida entre treinta por haber salido cara muchas veces. Si la tiro **mil veces más**,
esas mil tiradas estiman su sesgo **sin sesgo**. Las treinta importaron para interpretar las caras
originales, no para interpretar las nuevas.

**Subir el umbral es un ajuste que se aplica cuando no se pueden conseguir tiradas nuevas.**
Aplicarlo **además** de tener tiradas nuevas descuenta dos veces el mismo problema.

## La forma técnica del argumento

La tasa de error familiar se define **sobre la familia de pruebas que uno corre**. Si corremos una
prueba pre-registrada, nuestra familia tiene tamaño uno. **Las pruebas de otro no entran en nuestra
tasa de error.** Ésa es la definición, no una interpretación conveniente.

## Qué implicaría adoptarlo

Que `variantes_probadas` se llene con **nuestras** variantes —las decisiones de construcción que
declaramos en `HIBRIDAS` y en `P07`— y no con el conteo de lo que hicieron los autores. Para L11
serían **3** en vez de 30, y la vara bajaría de unos 4,0 desvíos a 3,0.

**Y el conteo de los autores no se tira: se reporta al lado, como contexto, sin entrar en la vara.**

---

# POSICIÓN EN CONTRA

## 1. Hay selección NUESTRA, y no está contada en ningún lado

**Elegimos qué papers entran al inventario, de una literatura mucho más grande.** Harvey, Liu y Zhu
catalogan **316 factores publicados**; Hou, Xue y Zhang replican **452 anomalías**.

**Once, ¿de cuántos?** Corrí del orden de treinta búsquedas y miré entre sesenta y ochenta papers
distintos. **No tengo el número exacto, y no tenerlo es parte del problema.**

**¿Se cuenta hoy? No.** El contador de cartuchos cuenta pre-registros. `variantes_probadas` cuenta
variantes **de una idea**. **Nada cuenta cuántas ideas se tamizaron antes de traer ésta.** Es un
agujero que existe hoy y que la posición a favor agrandaría, porque sacaría el único número que
hoy tapa una parte de él.

## 2. Y peor: filtramos por MAGNITUD, que es filtrar por resultado

> **CORREGIDO el 2026-09-05, después del veredicto. Ver [D03](D03_recorte_harvey_liu.md).**
>
> **Este argumento es más flojo de lo que lo escribí.** Harvey y Liu establecen que el recorte por
> multiplicidad es **no lineal**: las magnitudes altas se penalizan poco porque son las que más
> probablemente son descubrimientos verdaderos. Calculado sobre nuestras propias candidatas, la de
> `t` más alto pierde 16 % y la de `t` más bajo pierde 40 %.
>
> **Nuestro filtro `F4`, que descarta lo chico, selecciona hacia el lado que el recorte castiga
> menos.** El argumento no es nulo —seguimos seleccionando sobre una variable de resultado— pero es
> **de segundo orden, no de los fuertes**.
>
> **No cambia el veredicto de `D02`**, que se apoyó en el argumento 4, el de las fechas de muestra.

**`F4` descarta candidatas cuya magnitud declarada esté por debajo del piso.** Eso es **seleccionar
sobre la variable de resultado**.

La magnitud publicada está inflada por la maldición del ganador. **Quedarse con las magnitudes más
grandes es quedarse con las MÁS infladas.** Nuestro propio filtro concentra el sesgo que la posición
a favor dice que fuera de muestra elimina.

**Esto no lo puso Roberto en su lista y es de los más fuertes.**

## 3. El fuera de muestra que tenemos es chico, y ya sabemos que no confirma

`P07` y `P08` lo muestran con números: L11 necesitaría el 186 % de su magnitud y L10 el 204 %.
**Bajar la vara de 4,0 a 3,0 deja a L11 en 1,40 y a L10 en 1,53. Las dos siguen arriba de uno.**

**Un remedio que exige fuera de muestra pero cuyo fuera de muestra no puede confirmar nada no es un
remedio: es sacar una guarda sin comprar potencia.**

## 4. EL FUERA DE MUESTRA ES FALSO PARA LA MITAD DEL INVENTARIO

**Ésta es la que no vi venir al escribir la posición a favor.**

| candidata | muestra del paper | ¿2016-2019 está adentro? |
|---|---|---|
| **L10** | 1997-2023 | **SÍ, entero** |
| **L01** | 1974 – mayo 2020 | **SÍ, entero** |
| **L05** | 1996 – mayo 2020 | **SÍ** |
| L06 | publicado 2023 | **probablemente sí** |
| L09 | 2006-2018 | **parcialmente** |
| L11 | hasta 2009 | no… pero ver abajo |
| L02, L03, L04, L07, L08 | terminan en 2013 o antes | no |

**Las dos candidatas que la regla rescataría —L10 y L01— tienen nuestros datos ENTERAMENTE DENTRO de
la muestra de su propio paper.** Para ellas no existe ningún fuera de muestra. **La precondición del
remedio falla precisamente donde el remedio serviría.**

## 5. Y hay una contaminación peor, que es de nuestra propia construcción

**El filtro `F7` califica a las candidatas por confirmación posterior a la publicación. Para L11, el
grado A viene de que Ai, Bansal y Guo extendieron la muestra a 2023 y encontraron el premio más
fuerte.**

**2016-2019 está adentro de 2023.**

**O sea que elegimos a L11 como primera del inventario usando evidencia que cubre el período en el
que la queremos probar.** Eso es mirar hacia adelante en el paso de selección, y **lo introdujo un
filtro mío**, no la literatura.

Afecta por lo menos a **L11** (extensión a 2023), **L07** (Bessho, 2018-2020) y **L05** (Dim, Eraker
y Vilkov, hasta ~2023). **Es un problema del filtro F7 que existe independientemente de este debate y
que hay que anotar aparte.**

## 6. "Cero grados de libertad" es una afirmación sobre nosotros mismos

La posición a favor descansa en que implementamos **exactamente** lo publicado. **`HIBRIDAS` muestra
que eso casi nunca es literalmente cierto**: tres de cuatro híbridas tienen piezas ajustables, y las
"desactivamos" **declarando**. Una declaración no es una ausencia de libertad: **elegimos la
declaración.**

En `P07` declaré tres decisiones nuestras para L11: la lista de anuncios, el instrumento, la
definición del cierre. **Cada una pudo haber sido otra.**

## 7. La asimetría de las consecuencias

Si la vara estricta está mal, perdemos una ventaja: cuesta oportunidad. Si la vara laxa está mal,
operamos una ventaja falsa con plata real contra un drawdown de $2.000 que la Compuerta 1 ya midió
que se lleva una noche sola el 8,38 % de las veces. **La función de pérdida no es simétrica, y la
vara no se fija sólo por elegancia estadística.**

## 8. Cómo sabríamos que pasó por la regla nueva y no porque era real

**No sabríamos.** No tenemos ningún caso con respuesta conocida contra el cual calibrar la regla. Y
la regla se adoptaría **exactamente en el momento en que rescata el inventario**, que es la peor
condición posible para atribuir después.

**El historial del proyecto es un registro de este modo de falla: 261 negativos de un generador que
en cada paso tenía un buen argumento.**

## 9. La debilidad del ejercicio, dicha por quien lo hace

**Las dos posiciones las escribí yo.** Soy el mismo generador que produjo la idea, así que la
posición en contra está limitada por lo que se me ocurra en contra de mí mismo. **Los argumentos 4 y
5 aparecieron sólo porque fui a verificar fechas de muestra; si no hubiera ido, no estarían.**

---

# LO QUE DICE LA LITERATURA, que Roberto pidió buscar primero

**Es un problema conocido y hay respuesta publicada. Y la respuesta más directa a nuestra pregunta
está en contra de la posición a favor, aunque no del todo.**

## Los que dicen que la vara sube para todos

**Harvey, Campbell R.; Liu, Yan; Zhu, Heqing (2016). "…and the Cross-Section of Expected Returns."**
*Review of Financial Studies* 29(1), 5-68. https://academic.oup.com/rfs/article/29/1/5/1843824

Construyen el umbral de significación teniendo en cuenta **todas las pruebas de la profesión**, no
las de uno. Su conclusión: un factor nuevo necesita **t mayor que 3,0**, y usar el 2,0 habitual *"no
tiene ningún sentido económico ni estadístico"* dada la minería de datos acumulada.

**Es exactamente la posición contraria a la de A FAVOR: la selección ajena NO recibe indulto, y de
hecho es la razón por la que la vara sube.**

## Y los que dicen CÓMO tratar un resultado ya publicado

**Harvey, Campbell R.; Liu, Yan (2015). "Backtesting."** *Journal of Portfolio Management*.
SSRN 2345489. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2345489

**Es la respuesta publicada más cercana a nuestra pregunta.** Proponen **recortar la razón de Sharpe
publicada** por multiplicidad, con un recorte **no lineal**: las razones altas se penalizan poco y
las marginales mucho, hasta llevarlas a cero. Y advierten que el recorte fijo del 50 % *"es un error
serio"*.

**El remedio que la literatura propone para un resultado preseleccionado NO es bajar el umbral de
significación: es RECORTAR LA MAGNITUD ESPERADA.**

## Los que dicen que el problema está exagerado

- **Jensen, Theis Ingerslev; Kelly, Bryan; Pedersen, Lasse Heje (2023). "Is There a Replication
  Crisis in Finance?"** *Journal of Finance* 78, 2465-2518. Con un modelo bayesiano jerárquico
  encuentran que **la mayoría de los factores sí replican**, funcionan fuera de muestra en 93 países,
  y que la evidencia **se fortalece, no se debilita, con el número de factores observados**.
- **Chen, Andrew Y. (2022). "Most claimed statistical findings in cross-sectional return
  predictability are likely true."** arXiv:2206.15365.
- **Chen y Zimmermann, "Publication Bias in Asset Pricing Research."** arXiv:2209.13623.

**Estos apoyan a la posición A FAVOR en el fondo —la selección ajena no invalida tanto como se
teme— pero su remedio tampoco es bajar el umbral: es MODELAR el sesgo jerárquicamente**, que
necesita muchas anomalías a la vez y no once.

## Lo que la literatura NO resolvió

**No encontré trabajo publicado sobre el caso exacto: un tercero implementando una regla publicada
sin grados de libertad sobre un período fuera de muestra, y cómo debe fijar su umbral.** La
literatura trata el problema **desde el lado del que descubre**, no desde el lado del que copia.

---

**NO HAY VEREDICTO EN ESTE DOCUMENTO. Va en `D02`, commiteado después.**
