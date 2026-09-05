# A03 — Dónde tratamos una variable como si fuera una constante

**VENTANA L. NO MIDE CANDIDATAS; corre CONTROLES DEL INSTRUMENTO desde el 2026-09-05 (rol ampliado por Roberto, ver `INDICE`). K sigue en 261.**

**El hallazgo que originó esto:** la exposición de L10 es de **uno o de tres días** según en qué día
de la semana cae el fin de mes, y nuestros filtros razonan sobre uno.

**Es de la misma familia que el filtro nocturno mal escrito.** Los dos son filtros que razonan sobre
una constante cuando la realidad es una variable. Este documento busca los demás casos.

---

# 1. La que sí importa: la volatilidad intradiaria NO es uniforme

**En `D06` escalé el desvío medido de 82 puntos básicos por sesión a ventanas cortas con la raíz del
tiempo:**

```
σ(T)  ≈  82 · √(T / 1380)          →   30 min: 12,1 pb
```

**Esa fórmula supone que la volatilidad está repartida pareja a lo largo del día. NO LO ESTÁ.** El
patrón en U es uno de los hechos más viejos y más replicados de la microestructura, y **los propios
papers de esta carpeta lo usan como parte de su mecanismo**: Baltussen et al. dedican una figura a la
forma de U del volumen y la volatilidad, y Gao et al. la usan para explicar por qué la primera y la
última media hora son especiales.

## A quiénes afecta, y son justo dos de los cuatro sobrevivientes

| candidata | su ventana | dónde cae en la U |
|---|---|---|
| **L01** | última media hora | **pico de la tarde** |
| **L03** | 9:30 a 10:00 | **pico de la mañana, el más alto del día** |
| L02 | última media hora | pico de la tarde |
| L07, L08 | ventanas de divisas fuera de la sesión del ES | la U del ES no aplica |

## Cuánto, con el número del propio paper

**Baltussen et al. reportan 3,96 % anual de desvío para su cartera de índices, o sea unos 25 puntos
básicos por sesión en la última media hora.** Contra los 12,1 que da el escalado uniforme:

```
factor de subestimación  ≈  25 / 12,1  =  2,07
```

## Qué le hace a cada una

| candidata | (a) con escalado uniforme | (a) con el factor 2,07 | (c) esperada | efecto |
|---|---|---|---|---|
| **L01** | 1,143 | **2,37** | 1,143 | **pasaría de la línea exacta a CIEGA** |
| **L03** | 2,62 | **5,42** | 4,37 | **pasaría de sobrevivir a CIEGA** |

> **Con el patrón en U puesto, DOS de los cuatro sobrevivientes se caen.** Quedarían **L07 y L08**,
> que son los dos de divisas y los dos que exigen comprar datos.

## Por qué el veredicto de `D06` NO se corrige

**Porque `D06` usa la cota optimista a propósito, y ésta es la dirección desfavorable.** Su veredicto
para L01 y L03 ya era **"REQUIERE MEDICIÓN REAL DEL DESVÍO"**, no una aprobación.

**Lo que esto agrega es el signo del riesgo: la medición pendiente va a mover el número hacia arriba,
no hacia abajo.** Y el factor 2,07 es una **transferencia mía** desde el desvío implícito de un paper
hacia otra ventana: **FRÁGIL**, y es exactamente el número que la medición reemplaza.

**Es también la razón por la que esa medición es urgente y no cosmética: puede cerrar dos candidatas
más, y está en datos que ya están en el repo.**

---

# 2. Las demás, con su filtro y su fracción

| # | variable tratada como constante | filtro afectado | fracción mal evaluada | ¿cambia un veredicto? |
|---|---|---|---|---|
| 1 | **exposición de L10**: 1 día, o 3 cuando el fin de mes cae viernes | `F1'`, `F8` | ≈ **20 %** de los eventos | **no**: L10 ya es CIEGA |
| 2 | **exposición de L11**: 1 día, o 3 cuando el anuncio cae lunes, o cuando la sesión previa fue feriado | `F1'`, `F8` | **no cuantificada**, faltan las fechas | **no**: L11 ya es CIEGA |
| 3 | **costo de ida y vuelta ≈ $17**, constante | `F6`, `PISO_Y_CONVERSION` | **100 %** de los eventos de L03 y L11, que operan alrededor de publicaciones donde el diferencial se abre | **no**: la balanza ciega no usa el costo. **Sí importaría si L03 llegara a medirse** |
| 4 | **nocional del ES ≈ $130.000**, constante | todas las conversiones a dólares | el ES fue de ~1.900 a ~3.200 en el período: hasta **±25 %** por evento | **no**: los veredictos están en puntos básicos y en `θ`, que son escalares |
| 5 | **`σ` constante dentro de una candidata** | las cuentas de potencia | la VENTANA G midió que el piso varía **20,8×** entre terciles ex-ante | **no**, y hay que decir por qué: para la potencia agregada lo que importa es el desvío cuadrático medio, y usar uno solo es correcto. **No es un error, es una elección válida** |
| 6 | **`t*` de la vara del juez, constante en 3,0** en `D06` | `D06` | todas | **no**: está declarado como la elección más favorable |

**Sólo el número 1 y el número 2 son errores de la misma clase que el filtro nocturno. El 3 es una
deuda real. El 4, 5 y 6 son elecciones declaradas y no defectos.**

---

# 3. Lo que este ejercicio deja como criterio

**La pregunta que ninguno de los trece filtros hace: ¿este filtro razona sobre un promedio cuando la
realidad tiene dispersión, y la dispersión importa?**

**No siempre importa.** El caso 5 muestra que a veces el promedio es lo correcto. **Lo que hay que
poder decir es CUÁL de los dos es, y hasta hoy no lo decíamos: lo suponíamos.**

**Y el patrón que se repite en los tres casos donde sí importa —el filtro nocturno, la exposición de
L10 y el escalado uniforme de la volatilidad— es el mismo: el promedio subestima el caso malo.**
Ninguno de los tres iba en la dirección de hacernos la vida más difícil por accidente. **Los tres nos
la hacían más fácil.**
