# Inventario de constantes del juez, por régimen — ¿una ronda o diez?

**VENTANA G. K = 261, no gasta cartucho.** Dinero: $0. Hecho **leyendo el código**, no de memoria.

---

## EL CONTEO, arriba y no al final

> **Cinco constantes están medidas en el régimen ANCHO (5pt:20pt, tenencia de horas, p(stop) ≈ 0,08)
> y se usan sin corregir en el régimen ESTRECHO (span 3-7, tenencia de minutos, p(stop) ≈ 0,49).**
>
> - **1 es SUSTITUIDA literalmente** — `EXCESO_STOP`, y es el **53%** del piso de 3pt:4pt
> - **3 están CALIBRADAS CONTRA LA CELDA ANCHA** y se usan tal cual — `REF_EDGE_OP_MINI`,
>   `L_ESTRELLA_SES`, `Z_TERCIL`
> - **1 no sé si depende del régimen y no lo puedo descartar** — `MARKOUT_PASIVO`/`LLENADO_PASIVO`
>
> **Y tres de los diez controles (C5, C7, C9) también están calibrados contra la celda ancha**, que
> es lo que se vio al correrlos sobre 3pt:4pt.

**La respuesta a "¿una ronda o diez?": ni una ni diez. Son dos o tres corridas, todas de $0 y cero
cartuchos, más una decisión sobre `EXCESO_STOP` que puede necesitar dato de mayor resolución.**

---

## 1 · SUSTITUIDA literalmente

### `EXCESO_STOP` = {10: 0,722 · 20: 0,982} pt

| | |
|---|---|
| **régimen medido** | stops de **10 y 20 pt** únicamente (`media_exceso.py`) |
| **qué usa en 3pt:4pt** | 0,722 — el de un stop de 10, para un stop de **4** |
| **cuánto es** | **18% del stop** (36% en 2pt:2pt) contra 4,9% en un stop de 20 |
| **fracción del piso** | **53%** en 3pt:4pt · 51% en 2pt:3pt · **58%** en 2pt:2pt · 45% en 1pt:2pt |
| **dirección** | sobreestima el costo ⇒ conservadora, pero **domina el resultado** |
| **qué costaría medirla** | una corrida de `media_exceso.py` con stops de 2, 3, 4, 5 y 7 pt sobre ES 1-min. **$0, cero cartuchos, ~10 min.** |
| **el riesgo real** | el exceso es el recorrido **más allá** de la barrera dentro de una barra de 1 min. Con un stop de 2 pt y un rango medio de barra de 0,6 pt, es posible que el exceso medido con barras de un minuto sea **artefacto de resolución** igual que la ambigüedad. Si es así, hace falta tbbo — y eso ya está comprado para seis días. |

---

## 2 · CALIBRADAS CONTRA LA CELDA ANCHA, usadas sin corregir

### `REF_EDGE_OP_MINI` = 72,69/4,96 = **$14,66 por operación**

`permutacion.py` línea 58: `CELDA = (5, 20)`. **Verificado en el código.** Es la ventaja inyectada y
recuperada **en la celda ancha**, y el juez la usa como vara para decidir **NO MEDIBLE**
(`rel = sd_tot / ref_edge_ses > 1`). Pero σ por operación es **$411 en 5pt:20pt y $185 en 3pt:4pt**:
la misma vara absoluta significa cosas distintas. **Qué costaría:** re-inyectar y recuperar en la
celda estrecha, una corrida de `permutacion.py`. **$0, ~15 min.**

### `L_ESTRELLA_SES` = 4 sesiones

`bloques.py` lo calibra *"contra la tasa real de sin-resolver"*. **En 5pt:20pt casi nada resuelve
—p(stop) 0,08 y tenencia de 3-7 horas—; en 3pt:4pt resuelve casi todo.** La tasa contra la que se
calibró **no existe** en el régimen estrecho. Gobierna `ROT_INDEP_MIN`, o sea cuándo el juez dice
NO MEDIBLE por ventana angosta. **Qué costaría:** recalibrar L* con la celda estrecha, una corrida.
**$0, ~15 min.**

### `Z_TERCIL` = 2,0

El comentario en `juez.py` lo dice: *"Subido de 1,5 a 2,0: tres veces un tercil de un candidato NULO
cruzó 1,5sd por ruido (C1)"* — **C1 sobre 5pt:20pt**. La distribución nula por tercil en la celda
estrecha es otra. **Qué costaría:** barrer semillas de C1 en la celda estrecha, como se hizo con C8.
**$0, ~20 min.**

---

## 3 · NO SÉ, y no lo puedo descartar

### `MARKOUT_PASIVO` y `LLENADO_PASIVO`

Son del lado de la **entrada**, no de la salida, así que en principio no dependen del bracket. **Pero
no lo verifiqué**, y hay un motivo concreto para dudar: se calibraron con entradas al azar sobre
días cuya **tenencia era de horas**, y el markout se mide a H = 30 s. Para una candidata que sale en
56 minutos, la pregunta de si la entrada fue envenenada se resuelve dentro de su propia vida; para
una que sale en 7 horas, no. **No sé si eso cambia el número.** Además ya sabemos que **son
indistinguibles de cero** con los días que hay.

**"No sé de dónde sale ésta": ninguna.** Todas las constantes del juez tienen procedencia escrita en
`instrumentos.py` o en el comentario de `juez.py`. Eso es lo único cómodo de este inventario.

---

## 4 · NO dependen del régimen — verificado y sin trabajo pendiente

| constante | por qué no depende |
|---|---|
| `COMISION` (ES 5,76 · MES 1,82) | es un contrato, no una medición |
| `PUNTO`, `tick`, `micros_equiv`, `sesion` | especificación del CME |
| `DESLIZAMIENTO_ENTRADA` (0,1267/0,1334/0,1330) | medio-spread al cruzar: **medido por tercil de volatilidad, no por bracket**. Y `spread_por_caja.py` mostró que tampoco depende de la hora (1,02 / 0,98) |
| `o_por_span`, `tasa_ambigua_por_span` | **medidas de 3 a 25 pt** — son las que se arreglaron ayer. Con ±15% declarado |
| `Z_BASE`, `Z_POTENCIA`, `N_MIN_OP`, `SES_MIN_TERCIL` | estadística pura |
| `BUCKETS`, `JACCARD_FAMILIA`, `MINHASH_K` | estructura del registro |
| `CADENA` (dd, target, qual_days…) | reglas de la firma |

---

## 5 · Lo que esto le dice a Roberto

**No es un proyecto: son tres corridas de $0 y una pregunta.**

| # | trabajo | costo | qué desbloquea |
|---|---|---|---|
| 1 | `media_exceso.py` con stops de 2-7 pt | $0, ~10 min | **el 53% del piso** de la celda estrecha |
| 2 | `permutacion.py` sobre 3pt:4pt | $0, ~15 min | la vara de NO MEDIBLE |
| 3 | L* y `Z_TERCIL` en la celda estrecha | $0, ~35 min | los umbrales de régimen |
| 4 | recalibrar C5, C7, C9 | $0, ~30 min | que un veredicto de aprobación signifique algo |

**La pregunta que no es una corrida:** si el exceso del stop medido con barras de 1 min resulta ser
artefacto de resolución para stops de 2-4 pt —como lo fue la ambigüedad— entonces hace falta tbbo, y
ahí sí cambia de tamaño el problema. **Los seis días ya están comprados**, así que ni siquiera eso es
una compra; es otra corrida. **Lo que no tenemos es más de seis días.**

---

## 6 · Y el indicio que ordena todo esto

**La celda ancha y la estrecha no son dos tamaños: son dos regímenes de salida.** Tres números lo
dicen, y los tres salieron de columnas que nadie pidió:

- **p(stop)**: 0,08 en la ancha, **0,49** en la estrecha. Una sale por tiempo, la otra por stop.
- **la nula pasiva**: −0,1σ en la ancha —nunca frena nada— y **−18,6σ** en la estrecha, donde es la
  que manda.
- **la tenencia**: 3-7 horas contra 56 minutos.

Toda constante calibrada en un régimen describe el otro sólo por suerte. **Eso es lo que este
inventario cuenta: cinco constantes contando con esa suerte.**

---

## Procedencia

`juez.py` · `instrumentos.py` · `permutacion.py` (línea 58, `CELDA = (5, 20)`) · `bloques.py` ·
`media_exceso.py` · `piso_celdas_estrechas.py` + `salida_piso_estrechas.txt` ·
`salida_controles_3x4.txt` · `spread_por_caja.py`.
