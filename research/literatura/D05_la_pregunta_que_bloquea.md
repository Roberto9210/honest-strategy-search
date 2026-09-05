# D05 — La pregunta que bloquea: la respuesta es (D). P01 SE CIERRA.

**VENTANA L. NO MIDE NADA. K sigue en 261.**

---

# 0. Reproduzco el número de Roberto antes de discutirlo

Con los desvíos **medidos** por la VENTANA G —**82,0 pb** en días de anuncio y **82,8 pb** en fines de
mes— en lugar de mi estimación de 60:

| j | `m_j` | `σ_j` | `r_j` | `n_j` | `n_j·r_j²` |
|---|---|---|---|---|---|
| L11 | 11,4 pb | **82,0** (medido) | 0,139 | 176 | 3,40 |
| L10 | 17,0 pb | **82,8** (medido) | 0,205 | 48 | 2,02 |
| L08 | — | — | 0,157 (de `F` publicado) | 480 | 11,83 |
| | | | | **704** | **17,26** |

```
t(θ=1) = √17,26 = 4,15        θ mínimo detectable a 3,0 σ = 3,0 / 4,15 = 0,72
```

**Reproduce el 0,72 de Roberto.** Y confirma lo que anuncié en `P10`: **el desvío medido salió mayor
que mi estimación, y las cuentas empeoraron.** 82 contra 60 es un **37 % más**, y `θ` mínimo pasó de
0,64 a 0,72.

---

# LA ELECCIÓN: **(D) NO ES MEDIBLE.**

**Elijo (D) y abajo está el número que descarta a las otras tres.**

---

# El argumento decisivo, en una tabla

| | valor de `θ` |
|---|---|
| lo que la prueba puede **detectar** | **0,72** |
| lo que la hipótesis **pide** | 0,25 |
| **lo que la literatura espera bajo decaimiento normal** | **0,42** |

McLean y Pontiff miden que las anomalías publicadas pierden el **58 %** después de publicarse. Eso
deja `θ = 0,42`, y **0,42 está por debajo de 0,72.**

> ## **La prueba devuelve el MISMO resultado si las reglas transfirieron con el decaimiento normal de la literatura que si están muertas. Un instrumento que da la misma respuesta bajo las dos hipótesis de interés no es un instrumento.**

**Eso no se arregla corriéndola. Es una propiedad del diseño, y por eso la ruta se cierra en vez de
ejecutarse.**

---

# Por qué no (A) MÁS EVENTOS

## El número exacto

Para detectar `θ = 0,25` a 3,0 desvíos hace falta `t(θ=1) ≥ 3,0/0,25 = 12,0`, o sea
`Σ n_j·r_j² ≥ 144,0`.

```
tenemos    17,26
hace falta 144,0
factor       8,35
```

| | ahora | hace falta |
|---|---|---|
| observaciones | 704 | **5.875** |
| años al ritmo actual de eventos | 4 | **33,4** |
| eventos de fin de mes para L10 | 48 | **401** |

## De dónde saldrían, y si existen

**Más años hacia adelante — la caja sellada.** 2020-01-02 a 2026-08-19 son 6,63 años. Sumados a los
4 que hay, el factor es 2,66, no 8,35.

```
con la caja:  Σ = 45,9   →   t(θ=1) = 6,77   →   θ mínimo = 0,44
```

**Sigue por encima de 0,42.** La caja **no alcanza**, gastaría su único uso, y dejaría el veredicto en
una moneda.

**Más años hacia atrás — están contaminados por construcción.** L10 va de 1997 a 2023 y L08 de 2004 a
2012: cualquier año anterior a 2016 está **dentro** de la muestra de los autores.

**Más instrumentos.** Melvin y Prins usan diez monedas y usar más cambia su demediado transversal, o
sea la regla. Y agregar candidatas nuevas ahora sería elegirlas **después** de conocer el problema de
potencia, que es exactamente la trampa que el criterio de inclusión cerrado de `P01` existe para
evitar.

## El número que lo cierra, dicho claro

**L10 necesitaría 401 fines de mes. El contrato E-mini del S&P 500 empezó a cotizar en septiembre de
1997, así que hasta agosto de 2026 existen unos 348 fines de mes en TODA su historia.**

> ## **Hacen falta más eventos de los que el instrumento ha tenido desde que existe.**

Y eso contando **toda** su historia, incluida la que está dentro de la muestra de los autores. **Los
eventos limpios de L10 son los posteriores a 2023: unos 32.**

---

# Por qué no (B) MENOS DESVÍO

## La idea es correcta y el tamaño no alcanza

Normalizar por volatilidad ex-ante es lo que la VENTANA G ya hace en su eje de régimen, y **no
inventa señal**. Si la señal escala con la volatilidad —y Gao et al. reportan que el efecto es más
fuerte en días volátiles, lo que apunta en esa dirección— entonces dividir por la volatilidad previa
quita ruido sin quitar señal.

**La ganancia es de la forma `√(1 + CV²)`, donde `CV` es el coeficiente de variación del nivel de
volatilidad.**

## Cuánto bajarían, y de dónde sale ese cuánto

> **ESTIMACIÓN MÍA. FRÁGIL.** Sale de un hecho ya medido en el repo —el agrupamiento de volatilidad
> del ES es **de cola y no de centro**: mediana 1,00× y p95 1,51×— del que **derivo** un `CV ≈ 0,25`
> suponiendo forma lognormal. **La derivación es mía, no la medición.**

```
ganancia ≈ √(1 + 0,25²) = 1,031        →        3 %
hace falta                                       735 %
```

**Tres por ciento contra ochocientos treinta y cinco. Y si la señal NO escala con la volatilidad, la
normalización EMPEORA las cosas**, porque dividiría una señal constante por un número que varía.

**El hecho medido que la mata es del propio proyecto: el agrupamiento de volatilidad del ES está en la
cola, no en el centro. Justamente donde la normalización no compra nada.**

---

# Por qué no (C) OTRA HIPÓTESIS

## Cuál sería

La única hipótesis que este instrumento puede contestar es **`θ ≥ 0,72`**: *"las reglas transfieren
con casi tres cuartos de su magnitud publicada"*.

## Por qué eso ya no es la misma idea

**El 0,25 no lo elegí para que la prueba pasara: salió de McLean y Pontiff, que es un número ajeno y
anterior.** Subirlo a 0,72 sería **exigir menos decaimiento que el que la literatura documenta como
típico**, o sea preguntar si las reglas se mantuvieron **mejor de lo normal**.

**Ésa es una pregunta distinta y menos interesante**, y peor: **un negativo no distinguiría "murió" de
"decayó como se esperaba"**, que es exactamente el problema que ya tenemos.

**Y sería mover la vara después de ver la potencia**, que es lo que `P01` prohíbe en su propia sección
(c): *"moverlo después de recalcular la potencia sería ajustar la vara al instrumento."*

**Gastaría su propio cartucho para contestar una pregunta peor. No.**

---

# (D) — Qué se cierra y qué NO se cierra

## Se cierra

**La prueba agrupada de `P01`, tal como está diseñada, no se ejecuta y no se pre-registra.** Su
diseño, su criterio de inclusión y sus ocho controles quedan escritos y son reutilizables. **Lo que
se cierra es la ejecución, no el documento.**

## NO se cierra

- **`P05`, L07 sola.** Su potencia depende de otro desvío, el de USD/JPY en diez minutos, que **no
  está medido**. **Advertencia derivada de esta tanda: mi estimación de ES salió 37 % baja, así que
  la de USD/JPY probablemente también lo esté.** Corrigiendo por el mismo factor, `θ` mínimo de L07
  pasaría de 0,24-0,42 a **0,33-0,58**. **Sigue por debajo de 0,72 y sigue siendo la ruta más
  barata.** *(Trasladar un factor de calibración de un instrumento a otro es una inferencia mía:
  FRÁGIL.)*
- **Los tests de mecanismo de `M01` y `M02`.** No dependen de esta hipótesis ni de este umbral.
- **El inventario.** Cerrar una prueba no descarta candidatas.

## Lo que este cierre cuesta y lo que ahorra

| | |
|---|---|
| **dinero** | ahorra la compra de seis pares de divisas que `P04` especificaba. **No la cuantifico: nunca se cotizó** |
| **cartuchos** | ahorra **uno**: el 262 no se gasta. K se queda en 261 |
| **tiempo de Roberto** | ahorra la decisión sobre el cartucho y sobre la caja sellada. **Cuesta leer este documento** |

---

# Lo que este cierre deja escrito, que vale más que la prueba

**El diseño no falló por una mala idea: falló por una cuenta que no se podía hacer hasta tener el
desvío medido.** Y el desvío medido llegó **porque lo pedí en `P10` sabiendo que probablemente
empeoraría mis números**.

> **Una ruta cerrada con un número es un resultado. Ésta se cierra con tres: 0,72 de detección, 0,42
> de expectativa, y 401 eventos necesarios contra 348 que existen.**
