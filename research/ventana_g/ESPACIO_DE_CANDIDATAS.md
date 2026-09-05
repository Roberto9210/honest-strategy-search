# El espacio de candidatas, enumerado — qué grados de libertad quedan

**VENTANA G. K = 261, no gasta cartucho.** Dinero: $0. No mide nada nuevo: junta lo medido y cuenta.

**Mi condición de muerte, declarada antes de listar:** *si al enumerarlas el espacio sigue siendo
grande, enumerar no sirve y hay que seguir buscando. Si queda chico, enumerarlo es una tarea finita.*

---

## Las restricciones, por fuente

### A — Del reglamento de la firma (externas, verificables, no negociables)

| # | restricción | qué acota | fuente |
|---|---|---|---|
| **R2** | tenencia mediana **> 10 s** en más del 50% de operaciones y ganancia | **piso** al horizonte | help.tradeify.co, 2026-09-05 |
| **R3** | nada abierto de noche; todo cerrado 16:45 ET | **techo** al horizonte: ≤ 1 sesión | ídem |
| **R7** | ningún día > 20/35/40% de la ganancia | **piso** al número de días ganadores (≥ 5 para el 20%) | ídem |
| **R6** | 4 minis / 40 micros en $50k | **techo** al tamaño | ídem |
| **R1** | "no HFT bots", **sin definición numérica** | zona gris entre 10 s y ~1 min | ídem |
| — | automatización permitida con dueño único, prohibido el mismo bot en otra firma | forma de operación | ídem |

### B — Del costo (medidas por esta ventana)

| # | restricción | número |
|---|---|---|
| **C1** | la ventaja debe superar **0,98 ticks por operación** en ES (1,98 en MES) sólo para empatar | `frecuencia_con_costo.py` |
| **C2** | el movimiento escala con **√T** (exponente 0,476): acortar achica el movimiento y no el costo | ídem |
| **C3** | operar micro cuesta **2,01×** más por unidad de exposición | ídem |

### C — De la detectabilidad (medidas por esta ventana)

| # | restricción | número |
|---|---|---|
| **D1** | hacen falta **1.262 operaciones** para ver 0,10 σ/op; **5.047** para 0,05 | `frecuencia_y_potencia.py` |
| **D2** | con 4 años, una candidata de **1 por mes o 1 por semana no es medible** a ningún tamaño de efecto | ídem |
| **D3** | el cruce exigida/detectable está en **~4,1–4,6 op/día**; por debajo, una ventaja rentable es invisible | `cruce_frecuencia_celdas.py` |

### D — De la plomería (limitaciones nuestras, no del mundo)

| # | restricción | consecuencia |
|---|---|---|
| **P1** | sólo **ES y MES**; la plomería por instrumento está **NO IMPLEMENTADA** | divisas y todo lo demás, fuera |
| **P2** | terreno **2016-2019** (2020+ es la caja sellada) | 1.006 sesiones y nada más |
| **P3** | barras de **1 minuto**: no se puede verificar R2 ni juzgar nada sub-minuto | piso efectivo de 60 s |
| **P4** | regla de salida: **bracket** o **tiempo**, declarada y uniforme | ventaja de *salida* inexpresable |
| **P5** | ninguna constante tiene **verificación de resolución** | todo veredicto lleva la marca |

---

## Los grados de libertad que quedan

Cruzando todo, una candidata queda descrita por **cinco** cosas, y cuatro están casi fijas:

| grado de libertad | rango que sobrevive | por qué |
|---|---|---|
| **instrumento** | **ES o MES** — y MES es 2× peor por C3 | P1 + C3 ⇒ prácticamente **ES solo** |
| **horizonte de tenencia** | **60 s … 1 sesión** | R2 pone 10 s, P3 lo sube a 60 s, R3 lo corta en la sesión |
| **frecuencia** | **≥ 4–5 op/día** para ser medible; **≥ 5 días ganadores** por R7 | D3 + R7 |
| **tamaño** | **1–4 minis** | R6, y R7 empuja hacia abajo mientras el costo empuja hacia arriba |
| **regla de entrada** | **libre** | ← el único grado de libertad realmente abierto |

### La ventana de horizonte, en números

- **Piso:** 60 s (P3 — no 10 s, porque no lo podemos verificar).
- **Techo:** 390 min de contado (R3).
- **Pero D3 exige ≥ 4–5 op/día**, lo que implica un horizonte de **≤ ~80–95 min**.
- **Y R7 exige ≥ 5 días ganadores**, lo que a 4 minis choca con que la mediana al objetivo es **2
  días** (`consistencia_r7.py`).

**La ventana operable de horizonte queda entre ~1 y ~90 minutos**, con frecuencia entre 4 y ~390
op/día, sobre **un instrumento**, con un tamaño entre 1 y 4 minis.

---

## Entonces: ¿es enumerable?

**Sí, y por poco.** Contando de la forma más gruesa que sigue siendo honesta:

```
instrumento          1   (ES; MES es dominado, no una alternativa)
horizonte            ~6  franjas (1, 5, 15, 30, 60, 90 min)
tamaño               4   (1 a 4 minis)
regla de salida      2   (bracket, tiempo)  x  parámetros del bracket
                         (~8 celdas dentro del span caracterizado 20-35 pt)
-------------------------------------------------------------------
esqueleto           ~1 x 6 x 4 x 2..8  =  del orden de 50-200 combinaciones
```

**El esqueleto es finito y chico. La regla de ENTRADA no lo es** — y es el único grado de libertad
que queda abierto.

### Lo que eso cambia de método, y es concreto

1. **El esqueleto se puede recorrer entero** con el mismo cartucho, si se declara como **una sola
   hipótesis con una grilla declarada** (que es exactamente lo que hace `variantes_probadas`). No
   hace falta gastar un cartucho por combinación.
2. **La búsqueda deja de ser sobre "qué estrategia"** y pasa a ser sobre **qué regla de entrada**,
   con las otras cuatro dimensiones fijadas de antemano por las restricciones y no por gusto.
3. **Y hay combinaciones que se pueden descartar sin correrlas**: cualquiera con frecuencia < 4
   op/día es invisible (D3), cualquiera con horizonte < 60 s es injuzgable (P3), cualquiera en MES es
   dominada (C3), cualquiera que llegue al objetivo en < 5 días no cobra (R7).

---

## Mi condición de muerte, contestada

**El espacio NO sigue siendo grande: el esqueleto queda del orden de 10² combinaciones**, contra el
espacio implícito de antes, que era cualquier estrategia sobre cualquier instrumento a cualquier
horizonte. **Enumerarlo es una tarea finita** y el proyecto puede cambiar de método.

**Con dos honestidades pegadas, y las dos importan:**

1. **El grado de libertad que queda abierto —la regla de entrada— es el que contiene toda la
   dificultad.** Enumerar el esqueleto no enumera las candidatas: enumera los *envases*. Decir "el
   espacio es chico" y dejar la entrada libre es cambiar un problema infinito por un problema
   infinito con menos decoración.
2. **Cuatro de las restricciones que más atan (P1, P2, P3, P5) son NUESTRAS, no del mundo.** Si la
   plomería estuviera terminada y los datos fueran de mayor resolución, el espacio volvería a
   crecer. Lo que enumeramos hoy es *el espacio que nuestro instrumento puede juzgar*, que no es lo
   mismo que *el espacio donde puede haber ventaja*. Confundir los dos sería exactamente el error
   que la auditoría de potencia no pudo descartar para las 261.

---

## Procedencia

`frecuencia_con_costo.py` · `frecuencia_y_potencia.py` · `cruce_frecuencia_celdas.py` ·
`consistencia_r7.py` · `instrumentos.py` · `REGLA_resolucion_del_instrumento.md` · `juez.py`.
Reglamento: help.tradeify.co, leído 2026-09-05 (R1, R2, R3, R6, R7), relevado por otra ventana y
citado como recibido.
