# CAJA — MANCHA DECLARADA 01: lo que se leyó cuya muestra cruza la caja sellada. Y la regla para que no vuelva a pasar por reflejo.

**VENTANA L. NO MIDE CANDIDATAS; corre CONTROLES DEL INSTRUMENTO desde el 2026-09-05 (rol ampliado por Roberto, ver `INDICE`). K sigue en 261. La caja sellada (2020-01-01 → 2026-08-19, un solo uso para
todo el programa) no se abrió.** Este documento vive en `research/literatura/` porque esta ventana no
escribe en el territorio donde vive la caja (`research/ventaja_futuros/caja_alcance_y_uso.md`,
`factory/spec_fase2.md` §3.3 y §7.1). **Es el registro de la mancha; quien administre la caja lo copia
donde corresponda.**

---

# 1. El fallo de Roberto, ejecutado y no discutido

> **Leer un número publicado cuya muestra incluye 2020 o más SÍ cuenta como contaminación parcial de la
> caja. No se disimula: se declara.**

# 2. Lo que se leyó — la entrada que pidió Roberto, y las que salen de aplicar la regla hacia atrás

**Roberto pidió registrar BLW. Aplicar la regla del §4 hacia atrás sobre todo lo leído en 22 rondas
encuentra CUATRO más.** Se registran todas, porque una mancha declarada a medias es una mancha
disimulada.

| # | fuente | muestra publicada | **qué parte de la caja toca** | qué número leímos que la contiene |
|---|---|---|---|---|
| **1** | **Boyarchenko, Larsen y Whelan**, NY Fed SR 917 (`L12`) | ES, 1998-01-05 → 2020-12-31 | **2020 entero, un año de veintitrés**, dentro de un promedio, sin desglose anual publicado | Sharpe 1,1 y 1,3 antes de costos, −0,5 y 0,3 después, ventanas 2:00-3:00 y 1:30-3:30 del este |
| **2** | **Baltussen, Da, Lammers y Martens 2021**, *JFE* (`L01`) | futuros de índice, ES desde 1982-04-23 → **2020-05-01** | **2020-01 → 2020-05, incluido marzo de 2020**, dentro de un promedio de 38 años | retorno anual 6,86 %, desvío 3,96 %, Sharpe 1,73, coeficiente 5,98 |
| **3** | **Harvey, Mazzoleni y Melone 2025**, NBER (`L10`) | 1997-09-10 → **2023-03-17** | **2020-01 → 2023-03, 3,2 años de la caja**, la mayor de las cinco | los 17 pb del día siguiente, los 4 pb de bonos, todas sus tablas |
| **4** | **Coughlan y Orlov 2022**, CFTC (`H01` Hecho 4) | E-mini, 2012 → **2021** | **2020 y 2021** | participación de alta frecuencia 49,7 % en 2021, promedio 45 % |
| 5 | Huang et al. 2023, futuros de VIX (`L06`), *JBF* 148 | **NO VERIFICABLE desde esta ventana**: el editorial devuelve 403 y la página de RePEc (leída el 2026-09-05) trae el resumen entero y **ninguna fecha de muestra**; el resumen dice "multiple sub-periods" sin nombrarlos. Publicado en 2023 sobre un contrato que existe desde 2004: **es probable que llegue a 2020 o más**, y así se marca | **desconocida, probable** | retorno anualizado "de hasta casi 18 %" |

## 2b. La MAGNITUD de cada mancha, en años — para quien abra la caja algún día

La caja son **6,63 años** (2020-01-01 → 2026-08-19). Una mancha de un mes y una de tres años no pesan lo
mismo. (`cuenta_anios.py` para las fechas; la de Coughlan-Orlov supone que "2021" es el año entero:
**FRÁGIL**.)

| # | fuente | solapamiento con la caja | **años** | **fracción de la caja** | fracción de la muestra de la fuente | qué contiene el número leído sobre esos años |
|---|---|---|---|---|---|---|
| 1 | BLW | 2020-01-01 → 2020-12-31 | **1,00** | 15 % | 1 de 23 = 4 % | un promedio de Sharpe de 23 años; **incluye marzo de 2020** |
| 2 | Baltussen | 2020-01-01 → 2020-05-01 | **0,33** | 5 % | 0,33 de 38 = 0,9 % | **son cuatro meses, no un mes** —Roberto escribió "un mes"—, e **incluyen marzo de 2020**, el mes más volátil de la caja; dentro de un promedio de 38 años |
| **3** | **Harvey, Mazzoleni y Melone** | 2020-01-01 → 2023-03-17 | **3,21** | **48 %** | 3,2 de 25,5 = 12,6 % | **la más pesada, por diez veces**: casi la mitad de la caja, dentro del promedio de los 17 pb y de todas sus tablas de robustez |
| 4 | Coughlan y Orlov | 2020-01-01 → 2021-12-31 | **2,0** (FRÁGIL) | 30 % | 2 de 10 = 20 % | la participación de alta frecuencia por año: **2020 y 2021 están desglosados** (31,8 % en 2012, 49,7 % en 2021), o sea que de esta fuente sí se sabe algo **por año** de la caja: la estructura del volumen, no el precio |
| 5 | Huang et al. | desconocido | **?** | ? | ? | un retorno anualizado promedio; sin fechas no se puede pesar |

**Lectura de la tabla:** dos manchas son de precio y promedio largo (BLW, Baltussen), una es de precio y
grande (Harvey: la mitad de la caja), una es de estructura de mercado con desglose anual (Coughlan-Orlov:
no dice nada del precio, dice quién operaba), y una no se puede pesar. **Quien abra la caja sabe, con esta
tabla, que lo que más pesa es el 17 pb de Harvey sobre 2020-2023, y que de 2023-04 a 2026-08 no hay
ninguna mancha declarada.**

**Lo que NO cruza, para que quede el borde claro:** Gao (→ 2013), Kurov (→ 2014-03), Ito-Yamada (→ 2013),
Melvin-Prins (→ 2012), Savor-Wilson (→ 2009), Kirilenko (2010), Fett-Haynes (→ 2016), Haynes-Roberts
(→ 2016-10), Onur-Reiffen (2012), Menkveld (2007-08), Brogaard-Hendershott-Riordan (2008-09), Scholtus
(→ 2011), Wen et al. (→ 2018), Breedon-Ranaldo (parcial, anterior), Yamamoto (2012).

# 3. La consecuencia, declarada

1. **Ninguna decisión sobre la caja puede apoyarse en ninguno de esos números.** Ni en el Sharpe de BLW
   para la madrugada, ni en el 17 pb de Harvey para el fin de mes, ni en el 45 % de Coughlan-Orlov para
   quién está enfrente, ni en el 1,73 de Baltussen para la última media hora.
2. **Si la caja alguna vez se abre, esta mancha va en la lectura**, con esta tabla al lado del resultado:
   *"el que abrió conocía cinco promedios publicados que incluyen parte del período."*
3. **Qué NO contamina, dicho con el mismo cuidado:** los promedios son de 23, 38, 26 y 10 años; **ninguno
   dice qué pasó en 2020-2026 por separado**. Es contaminación **parcial** —la palabra de Roberto—: se
   sabe que un promedio largo que incluye el período dio tal número; no se sabe nada del período.
4. **`R02` no se toca**: su dominio se calcula sobre 2016-2019 y no usa ninguno de estos números.
5. **`D14` no se toca**: sus cuentas de años usan fechas, no los números.

# 4. LA REGLA — F19, para que no vuelva a pasar por reflejo

> ## **Antes de leer cualquier fuente externa, verificar si su muestra cruza la caja (2020-01-01 en adelante). Si cruza, declararlo ANTES de leer: en el registro, con la fuente y las fechas, y leer después. Nosotros lo hicimos al revés cinco veces.**

**Cómo se aplica:** la fecha de fin de muestra está en el resumen o en la sección de datos de cualquier
paper, y se puede leer sin leer el resultado. **Primero esa línea; después la decisión de seguir; después
el resto.** Si un paper llega hasta hoy y su resultado es sobre nuestro instrumento, la decisión de
leerlo es de Roberto, no de la ventana.

**Condición de falla de la regla:** que una fuente cruce la caja sin que se pueda saber antes de leerla
(un resumen sin fechas). Entonces se declara al descubrirlo, en el mismo día, como se hace acá.

# 5. Lo que esto le cuesta al proyecto, en una línea

**Nada hoy, y una nota permanente al lado de cualquier lectura futura de la caja.** El costo de no
declararlo habría sido que alguien, algún día, leyera un resultado de la caja creyendo que nadie sabía
nada de esos años.

**Costos:** dinero cero, cartuchos cero, K en 261.
