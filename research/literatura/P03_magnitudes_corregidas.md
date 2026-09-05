# P03 — La regla P02, aplicada

**VENTANA L. NO MIDE NADA. K sigue en 261.**

Aplicación de la regla escrita en [P02](P02_REGLA_magnitud_objetivo.md), que se commiteó **antes**
que este documento y sin haber mirado ningún subperíodo. El orden está en el historial de git.

---

# Lo que encontró cada paper

## L11 — Savor y Wilson (2013) · **CORREGIDA**

**Sí publica partición cronológica**, y publica dos:

| partición | ¿utilizable según R1? | ¿cuál manda según R2? |
|---|---|---|
| **mitades: 1958-1983 y 1984-2009** | **sí**, con el número en el texto | **ésta**: es la más gruesa que aísla el final |
| quinquenios, 10 períodos | **no**: reportan sólo el **signo**, que la diferencia es mayor en 9 de 10, sin magnitudes | descartada por R1 |

**El texto, sección III.G:**

> la diferencia entre el retorno accionario de días de anuncio y de días sin anuncio es de
> **8,7 puntos básicos en 1958-1983** contra **11,4 puntos básicos en 1984-2009**, y las tasas libres
> de riesgo −0,7 y −0,6 puntos básicos, **casi iguales entre las dos submuestras**.

| | magnitud objetivo |
|---|---|
| muestra completa, la que usaba `P01` | 10,3 pb |
| **último subperíodo, 1984-2009** | **11,4 pb** |

**LA CORRECCIÓN SUBE EL OBJETIVO, NO LO BAJA.** El efecto **no decayó entre las mitades: creció**,
de 8,7 a 11,4.

**Se aplica igual, por R4.** Quedarse con 10,3 porque es más fácil de alcanzar sería elegir el
objetivo cómodo. Y es coherente con lo que ya estaba en `F7`: Ai, Bansal y Guo encuentran el premio
más fuerte en el período reciente, no más débil.

## L10 — Harvey, Mazzoleni y Melone (2025) · **SIN CORREGIR**

**No publica una magnitud de último subperíodo.** Lo único cronológico que hay es una nota al pie de
robustez, la 14:

> *"repetimos el análisis usando sólo la PRIMERA MITAD de la muestra y encontramos resultados
> cualitativamente similares, con la predictibilidad volviéndose insignificante para valores de
> [umbral] mayores a 2,5 %."*

**Es la primera mitad, no la última, y es cualitativa.** Falla R1 por las dos razones. La única otra
partición del paper es por meses dentro del trimestre y por semana del mes, que **son cortes
estacionales, no cronológicos**, y R2 los descarta.

| | magnitud objetivo |
|---|---|
| muestra completa 1997-2023 | **17,0 pb** ← se conserva |

**Atenuante que no cambia la clasificación pero se anota:** su muestra completa termina en 2023, así
que el promedio está mucho menos "diluido por décadas viejas" que el de L11. **Es la candidata que
menos necesita la corrección.**

## L08 — Melvin y Prins (2015) · **SIN CORREGIR**

**No publica ninguna partición temporal.** El período es 2004-2012 completo, y los cortes que hacen
son por moneda y contra días de control, ninguno cronológico.

| | magnitud objetivo |
|---|---|
| muestra completa 2004-2012 | **coeficiente 0,0142** ← se conserva |

## L07 — Ito y Yamada (2017) · **condicional, y ahora con un problema más**

**Sí tiene partición cronológica**: antes y después de 2008, y es de las que R2 acepta.

> *"Antes de 2008, los precios de fixing fijados por los bancos estaban sesgados hacia arriba y por
> encima del precio más alto transado durante la ventana. Aun después de 2008, los precios de fixing
> anunciados por los bancos seguían por encima del precio mediano transado."*

**Pero eso es la descripción del sesgo del precio de fixing, no la magnitud del movimiento
9:53–9:57**, que es lo que L07 necesita. Y la magnitud del movimiento sigue siendo "varios puntos
básicos" sin tabular.

**L07 sigue CONDICIONAL, y ahora hay que extraer dos cosas del paper y no una: la magnitud, y su
valor después de 2008.**

---

# El estadístico agrupado, corregido

| j | `m_j` viejo | **`m_j` corregido** | estado | `σ_j` | `r_j` | `n_j` | `n_j·r_j²` |
|---|---|---|---|---|---|---|---|
| L11 | 10,3 pb | **11,4 pb** | **CORREGIDA** | ≈ 60 pb | 0,190 | 176 | **6,35** |
| L10 | 17,0 pb | 17,0 pb | SIN CORREGIR | ≈ 60 pb | 0,283 | 48 | 3,84 |
| L08 | coef. 0,0142 | ídem | SIN CORREGIR | — | 0,157 | 480 | 11,83 |
| | | | | | | **704** | **22,02** |

```
                          antes        corregido
t(θ = 1)                   4,56    →      4,69
θ mínimo detectable        0,66    →      0,64
```

## Cómo hay que leer esto

**La corrección casi no mueve nada, y lo poco que mueve va a favor.** El objetivo se hizo **más
exigente** —11,4 en vez de 10,3— y aun así el estadístico **mejora**, porque una magnitud mayor con
el mismo ruido es una señal por evento mayor.

**Roberto dijo que si empeoraba también valía. No empeoró, y el motivo es más informativo que el
número:** el único paper del trío que publica una partición cronológica utilizable **reporta que su
efecto creció entre mitades**. La corrección se diseñó esperando decaimiento y encontró lo contrario
en el único lugar donde se podía mirar.

## Las tres advertencias que van pegadas al número

1. **Dos de tres siguen `SIN CORREGIR`.** Por R6, si esas dos decayeron, sus objetivos quedan altos,
   sus `z` bajos, y **el `θ` agrupado sale sesgado hacia abajo**. La prueba es conservadora, no
   optimista, en esa dimensión.
2. **Que L11 creciera entre 1958-1983 y 1984-2009 no dice nada sobre 2016-2019.** El último
   subperíodo del paper termina en 2009 y nuestros datos empiezan en 2016. **Hay siete años sin
   observar entre uno y otro.** La corrección achica la brecha; no la cierra.
3. **`t(θ=1) = 4,69` sigue siendo cota optimista** por lo dicho en `P01`: dos de los tres `σ_j` son
   estimaciones mías sobre una serie de cola gorda. **La corrección de magnitud no arregla el
   problema del denominador.**

---

# Qué hay que cambiar en P01

Un solo número, y queda anotado acá para que se cambie **en la copia final del pre-registro, antes de
correr**:

```
m_L11  =  11,4 pb        (era 10,3)        fuente: Savor y Wilson (2013), sección III.G,
                                           subperíodo 1984-2009
```

Todo lo demás de `P01` —candidatas, criterio de inclusión, ponderación, hipótesis, regla de decisión,
controles— **queda exactamente igual**. La hipótesis sigue siendo `θ ≥ 0,25`, y ese umbral **no se
toca**, porque moverlo después de recalcular la potencia sería ajustar la vara al instrumento.
