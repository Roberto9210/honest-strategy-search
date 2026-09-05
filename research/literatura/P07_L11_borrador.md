# P07 — L11, preparada hasta el borde. BORRADOR, NO REGISTRADO

**VENTANA L. NO REGISTRADO. NO CORRIDO. K sigue en 261.**

> **En este proyecto el cartucho se gasta al PRE-REGISTRAR, no al correr.** Este documento llega
> hasta el borde y **no lo cruza**. Registrarlo gastaría el cartucho **262**.
>
> **Y la aritmética de la sección 5 dice que no conviene registrarlo. Eso es el resultado de haberlo
> preparado, no un fracaso de la preparación.**

---

# 1. Los datos que faltaban — fuentes oficiales, verificadas

Regla aplicada: **fuente oficial, nunca secundaria.**

| serie | organismo | fuente verificada | qué trae |
|---|---|---|---|
| Índice de precios al consumidor | Oficina de Estadísticas Laborales | `bls.gov/schedule/2016/home.htm` … `/2019/home.htm`, desde el archivo `bls.gov/bls/archived_sched.htm` | fecha y hora exactas, **08:30 hora del este** |
| Situación del empleo | ídem | ídem | ídem, **08:30** |
| Decisiones de tasas | Junta de la Reserva Federal | `federalreserve.gov/monetarypolicy/fomchistorical<AÑO>.htm` | fechas de reunión y comunicados |

**Verificación hecha, no supuesta.** Abrí el archivo de 2019 de la Oficina de Estadísticas Laborales
y contiene las dos series con fecha y hora para el año completo: por ejemplo, el índice de precios
del 11 de enero de 2019 a las 08:30 y la situación del empleo del 6 de diciembre de 2019 a las 08:30.
Y abrí la página histórica del comité de política monetaria de 2019, que lista sus nueve reuniones.

**Ninguna de las dos series está en el repo. Las dos son gratuitas y de acceso público.**

## Un hallazgo de la verificación que cambia la regla

**La página de 2019 del comité lista NUEVE reuniones, y una de ellas —la del 4 de octubre— fue NO
PROGRAMADA.**

Savor y Wilson miden **anuncios programados**. Todo su mecanismo es que la fecha se conoce de
antemano y por eso el riesgo es anticipable. **Una reunión no programada es exactamente lo contrario
y no puede entrar.**

**Queda declarado ahora: se excluyen las reuniones no programadas, y la exclusión se hace por la
etiqueta de la página oficial, no por criterio nuestro.**

## Lo que NO hice, y por qué

**No transcribí las 128 fechas.** Extraerlas pasa por un resumidor automático, y una fecha mal
copiada dentro de un documento que después habilita un cartucho es un error que no se detecta y que
envenena el resultado.

**La extracción es mecánica y hay que hacerla contra las páginas primarias, con verificación de
conteo: 12 índices de precios, 12 situaciones del empleo y 8 reuniones programadas por año.** Si un
año no da esos conteos, hay un error de extracción y no un dato faltante.

**Es la misma disciplina que aplico con los desvíos: un número que no medí no lo escribo.**

---

# 2. El archivo de entrada del juez

Formato leído de `JUEZ_COMO_SE_USA.md` al 2026-09-05, con el campo `clase_ventaja` que la VENTANA G
agregó.

```json
{
  "nombre": "L11_prima_dias_anuncio_savor_wilson",
  "instrumento": "MES",
  "contratos": 1,
  "limite_contratos": 4,
  "variantes_probadas": 30,
  "clase_ventaja": "direccional",
  "familia": "calendario_anuncios_macro",
  "regla_salida": {"tipo": "tiempo", "n_barras": 1380},
  "operaciones": [
    {"ts": "2019-01-10T15:00:00", "lado": "largo"}
  ]
}
```

**Una operación por anuncio programado: entrada en la barra del cierre de la sesión anterior, lado
siempre largo.** El ejemplo de arriba es la entrada correspondiente al índice de precios del 11 de
enero de 2019.

**No hay ningún campo de resultado.** Ni `pnl`, ni `precio_salida`, ni `ts_salida`. El juez calcula
los desenlaces él mismo y rechaza la entrada entera si huele a resultado. **Este archivo pasa esa
puerta limpio por construcción: sólo tiene instantes y lados.**

## Las tres decisiones de construcción, declaradas ahora

**1. `instrumento`: MES y no ES.** Por `F8`: la ventana es de cierre a cierre, y con un ES el peor
movimiento nocturno medido es casi tres veces el drawdown, con una noche sola llevándoselo el 8,38 %
de las veces por el lado largo. Con un MES el drawdown son 400 puntos y el peor movimiento medido
ocupa el 30 %. **Es una decisión nuestra y suma a las variantes.**

**2. `n_barras`: pendiente de confirmar contra el indexado del juez.** La regla del paper es de
cierre a cierre. Cuántas barras de un minuto hay entre dos cierres consecutivos del ES depende de
cómo el juez cuente el corte nocturno. **1.380 es mi cuenta y no la verifiqué contra el código. Es
una de las dos cosas que la tarea de cañería tiene que confirmar** (ver `P09`).

**3. El instante de entrada es el cierre de la sesión anterior**, en la barra de las 15:00 hora
central. Savor y Wilson miden el retorno diario, o sea de cierre a cierre.

---

# 3. `clase_ventaja` = `direccional`, y en qué me baso

El juez define: `direccional` si la ventaja está en **qué lado**; `timing` si está en **cuándo**, con
el lado indiferente o al azar. Y mide la firma sobre los desvíos de las dos nulas: rotación alta con
signo ≈ 0 → `timing`; **las dos altas → `direccional`**.

**Razonamiento, contra las dos nulas:**

- **Nula de signo**, que destruye qué lado: L11 es **siempre largo** y el lado **no es indiferente**.
  Aleatorizar el lado deja la esperanza en cero. **Desvío alto.**
- **Nula de rotación**, que destruye cuándo: rotar las entradas a días sin anuncio cambia la
  esperanza de 11,4 a 1,1 puntos básicos. **Desvío alto.**

**Las dos altas → `direccional`.**

**Y lo digo derecho: declarar `direccional` no compra nada.** Es el camino estricto, el que aplica el
mínimo de las tres nulas. La relajación es de `timing`, y declararla acá sería un error que el juez
detectaría con bandera roja. **Declaro la que no me sirve porque es la que corresponde.**

---

# 4. `variantes_probadas` = 30

**Los autores NO declaran cuántas variantes probaron.** Eso es información, no un cero, y va escrito
en el pre-registro tal cual.

Los 30 son **mi conteo de lo visible**, y es una cota inferior:

| fuente de variantes | cuántas |
|---|---|
| elegir tres familias de anuncios entre las decenas que se publican | la decisión principal |
| dos subperíodos, más diez quinquenios | 12 |
| la tasa libre de riesgo como serie de verificación | 1 |
| la extensión de los mismos autores en 2014, con el corte transversal completo | varias |
| **nuestras**: lista de anuncios pinchada a la fuente primaria, instrumento MES, definición del cierre | **3** |

Con 30 declaradas, la vara del juez queda **cerca de 4,0 desvíos**, interpolando entre el 3,7 de diez
y el 4,3 de cien.

---

# 5. LA HIPÓTESIS, LA REGLA DE DECISIÓN Y LA POTENCIA

## Hipótesis, en una frase que no se puede estirar

> **En los días de anuncio macroeconómico programado de 2016-2019, un MES comprado al cierre anterior
> y vendido al cierre del día del anuncio rinde, neto de costos medidos, más que la nula más
> exigente de las tres, con al menos una cuarta parte de los 11,4 puntos básicos que Savor y Wilson
> reportan para 1984-2009.**

## Regla de decisión

| resultado | condición |
|---|---|
| **SOBREVIVE** | el juez devuelve SUPERA, y la ventaja medida es ≥ 0,25 × 11,4 pb |
| **NO SOBREVIVE** | el juez devuelve NO SUPERA |
| **NO CONCLUYENTE** | NO MEDIBLE, o APUESTA AL REGIMEN, o bandera roja de clase |

**El 0,25 es el mismo umbral de `P01` y `P05` y no se toca.**

## La potencia — y acá está el resultado de haber preparado esto

`t(θ=1) = r · √n`, con `r = 11,4 / σ` y `σ` el desvío del retorno de una sesión de cierre a cierre.

| | |
|---|---|
| magnitud objetivo, último subperíodo | **11,4 pb** |
| `σ` estimado, cierre a cierre | ≈ 60 pb |
| `r` por evento | 0,190 |
| eventos, con la lista primaria: 12 + 12 + 8 por año | **128** |
| **`t(θ=1)`** | **2,15** |
| vara del juez con 30 variantes | ≈ 4,0 desvíos |
| **`θ` mínimo detectable** | **1,86** |

> ## **L11 SOLA NECESITARÍA EL 186 % DE SU PROPIA MAGNITUD PUBLICADA PARA PASAR.**
>
> **No es una candidata marginal: es una candidata imposible con el presupuesto de eventos que hay.**

**Robustez:** con `σ = 45 pb` en vez de 60, `θ` mínimo sería 1,39. **Sigue por encima de 1.** La
conclusión no depende de mi estimación de `σ`.

**Y la lista larga tampoco la salva:** con los 44 anuncios anuales de Ai, Bansal y Guo en vez de los
32 de la fuente primaria, son 176 eventos, `t(θ=1) = 2,52` y `θ` mínimo **1,59**. Sigue arriba de 1.

## Qué significa y qué NO significa un negativo

**SÍ significa:** que la prima de días de anuncio, aplicada tal como la publican y con un MES, no
supera las nulas del juez en 2016-2019 con el presupuesto de eventos disponible.

**NO significa:** que el efecto no exista. Con `θ` mínimo detectable en 1,86, **un negativo es el
resultado esperado aunque el efecto esté vivo y completo.** Sería un falso negativo por potencia, no
evidencia sobre el mercado.

---

# 6. LA RECOMENDACIÓN, que es no registrarlo

**Registrar L11 sola gastaría el cartucho 262 en una prueba que devuelve NO SUPERA con altísima
probabilidad aunque el efecto sea real y completo.**

**Y hay una alternativa que ya está escrita: la prueba agrupada de `P01` mete a L11 y L10 juntas, con
L08, y da `θ` mínimo detectable de 0,64 gastando UN cartucho en vez de dos.**

| | cartuchos | θ mínimo detectable |
|---|---|---|
| L11 sola | 1 | **1,86** |
| L10 sola | 1 | **2,04** — ver `P08` |
| las dos por separado | **2** | 1,86 y 2,04 |
| **la agrupada de `P01`, con L08** | **1** | **0,64** |

**Dos cartuchos compran dos pruebas que no pueden ganar. Uno compra una que sí.**

**No lo decido yo. Pero preparar esto hasta el borde sirvió exactamente para poder poner esa tabla
antes de gastar nada.**
