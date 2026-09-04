# INVENTARIO — qué afirmación de esta ventana aguanta el punto porcentual y cuál no

**2026-09-04. No gasta cartucho. K = 261.**

Este documento **marca, no corrige**. Nada de lo que está en `CRITERIO_RESULTADO.md`,
`BRACKET_RESULTADO.md` o `CIERRE_VENTANA_G.md` se borró ni se reescribió. Lo que no se podía dejar
era una afirmación precisa sin la advertencia al lado; esta es la advertencia, y vive acá para que
sea una sola y no quince notas al pie.

## Por qué hace falta

Dos mediciones de hoy mueven el piso de casi todo lo publicado en esta ventana:

1. **`S/(S+T)` está corrido sobre ES real.** Residuo −1,32 (20pt:10pt) y +0,78 (5pt:20pt), y contra
   una nula de 10 series sintéticas sin estructura queda a **6,6 y 4,2 desvíos, afuera del recorrido
   completo**. No es el replicador: es el mercado. Fuente: `sintetico.py`, `sintetico_ensamble.py`.
2. **Mis barras de error estaban chicas.** El error binomial subestima **1,2–1,8×** el desvío del
   sesgo *pooled* y **≈5×** el de la separación largo/corto (0,41 declarado contra 2,08 real).

El criterio publicado es **+1,2 puntos**. El residuo es **1,3** y su corrección de barra de error es
**0,24**. Las tres cifras son del mismo orden.

---

## A — Escritas al punto porcentual y apoyadas en `S/(S+T)`: NO valen hoy

| # | afirmación | dónde | qué le pasa | ¿se mantiene el signo? |
|---|---|---|---|---|
| A1 | «5pt:20pt necesita **81,2%** contra el **80,0%** de la moneda: **+1,2 puntos** de ventaja real» | `CRITERIO_RESULTADO.md` § *Veredicto: ahora SÍ hay criterio* | el 80,0% es `S/(S+T)` afirmado, no medido. Medido sobre ES a una sesión, *pooled*: **85,2%**. El +1,2 además **no está definido** hasta fijar horizonte y tratamiento de las no resueltas | **no aplica**: el número no está definido, no es que esté corrido |
| A2 | la vara **1,181×** / **1,192×** y la elasticidad **7,9×** | ídem § *La reconciliación con la vara de 1,181×* | el denominador `P(pasar)` de la moneda usa `p = S/(S+T)`. Un punto de corrimiento se amplifica ~8× | sí: la vara sigue > 1 con margen |
| A3 | tabla **34,1% / 35,0% / 33,3%** | ídem § *Qué significa exactamente el 34,1%* | el 33,3% es `S/(S+T)` | sí: (ii) < (i) es aritmética, no depende de la nula |
| A4 | los dos criterios por bracket: **+2,3 / +2,3 / +1,9 / +1,2 / +1,4** | ídem § *Los dos criterios, que no son el mismo* | columna «moneda» = `S/(S+T)` | sí: (ii) < (i) en las cinco celdas |
| A5 | pisos de rentabilidad **2,26 / 2,30 / 1,94 / 1,20 / 1,43** puntos | ídem § *El piso* | mismo ancla | sí |
| A6 | razones detectabilidad ÷ rentabilidad **1,63× … 2,62×** | ídem § *La regla que sale de esto* | hereda A5 en el denominador | sí: ningún bracket llega con 250 ni 1.000, y ahí el margen es grande |
| A7 | tabla de 48 celdas, esperanza negativa en 8 firmas × 3 tamaños | `aritmetica.py`, `f55fe57` | `p_win` por defecto = `S/(S+T)` | **sí, y con mucho margen**: 48 de 48 negativas |
| A8 | el positivo de **+$10** y el **−$72** a precio de lista | `CRITERIO_RESULTADO.md` § *El positivo está muerto tres veces* | ya estaba muerto por deslizamiento de entrada, caída de tasa y precio | **sí**: esto lo mata una cuarta vez |

**Lo que NO se mueve dentro de este grupo:** las **MDE** (7,45 / 3,70 / 2,13 …) son *diferencias* y
dependen de `p₀(1−p₀)`, que casi no se corre con un punto de desplazamiento. La MDE aguanta; lo que
no aguanta es el **ancla** contra la que se la compara.

## B — Escritas con la barra de error vieja: los intervalos están mal, no los puntos

| # | afirmación | qué le pasa |
|---|---|---|
| B1 | «Ruido de Monte Carlo: **±0,3 puntos** en los requeridos» | subestimado 1,2–1,8×. Hoy sería **±0,4 a ±0,5** |
| B2 | residuo **−1,32** y **+0,78** | los puntos quedan, pero medidos contra la nula real (media +0,26 / −0,20, no cero) son **−1,58** y **+0,98**: la corrección los agranda |
| B3 | separación largo/corto **+5,67** | el error no es 0,41 sino **2,08**. Sigue afuera de la nula, pero a **2,9 desvíos**, no a 14 |
| B4 | factor de des-drift **0,425** | arrastra **±0,18** desde B3. Es **0,43 ± 0,18**, no 0,425 |
| B5 | «el drift vive casi enteramente en la separación y casi nada en el *pooled*» | correcta en magnitud (11,85 contra 0,50, factor 24) pero **«casi nada» no es «nada»**: ese medio punto es del tamaño del criterio |
| B6 | «el modelo de barreras sin drift NO describe este mercado» | **se mantiene y se refuerza.** La razón que di (sobrevive al des-drift) usaba la barra de error mala; hoy está sostenida por la nula sintética, que es mejor evidencia |

## C — No tocadas por nada de esto

- Comisiones **medidas**: $1,82/micro, $5,76/mini, fuente oficial `help.tradeify.co`.
- El cobro **$1.350 = $1.500 × 90%** y la cuota **$83 promocional / $165 de lista**.
- Medias de exceso de deslizamiento **0,722** y **0,982** puntos, y los percentiles.
- **Compuerta 1** (rama de ejecución nocturna): es cierre a cierre, no usa `S/(S+T)`.
- **Censo de instrumentos**: holgura y esfuerzo en puntos y ticks, sin modelo de barreras.
- Las reglas de las 8 firmas en `datos_crudos.md`, con URL y fecha de lectura.
- Las **identidades de construcción** `P_pooled(20:10) = 1 − P_pooled(10:20)` y
  `P_pooled(10:10) = ½`: son álgebra, valen para cualquier serie.
- **`P_ABIERTA` y `P_RESUELTA` están MEDIDAS, no asumidas.** La cadena del tercer estado
  (`tercer_estado.py`) es la **única** pieza del modelo que no se apoya en `S/(S+T)`, y por eso es la
  que menos se mueve. El `control_consistencia()` que la protege es el que cazó la ventaja fantasma.

---

## D — Auditoría hacia atrás: qué controles publicados NO podían fallar

Regla nueva, aplicada también a lo ya escrito: un control que no puede dar otra cosa no es un
control. Tres categorías.

### VACÍOS — no podían fallar de ninguna manera

| control | dónde | por qué no podía fallar |
|---|---|---|
| «*pooled* = 50,0% clavado» en el bracket ancho | `salida_linea_base.txt` línea 18 | identidad de construcción: los dos lados usan los mismos niveles y las mismas entradas. Ya autocorregido el 2026-09-04 |
| «con costo cero el equilibrio por operación = `S/(S+T)`», error 1e-16 | `salida_criterio_control.txt` línea 45 | es álgebra: en `p = S/(S+T)` vale `p·T − (1−p)·S ≡ 0`. Verifica una identidad contra sí misma |
| «drawdown ÷ valor del punto = $2.000 / $50 = 40 puntos» | `salida_censo.txt` línea 4 | es una división |
| «sesgo(20:10) + sesgo(10:20) = 0 exacto» | `desdrift.py` | ya lo marqué al escribirlo: vale para cualquier serie |

### SÓLO DE CÓDIGO — forzados por la construcción, pero atrapan una clase de bug

| control | por qué está forzado | qué sí atraparía |
|---|---|---|
| «ambigüedad = 0,000% con bracket de 23pt por lado» (`salida_linea_base.txt`) | el ancho se eligió como `ceil(máximo/2)+5 = 23`, o sea 46pt de separación contra un rango máximo observado de 36pt. **Ninguna barra puede contener las dos** | un error en el test de toque que hiciera disparar las dos condiciones a la vez |
| «con tamaño de posición CERO las cuatro medidas dan 0,00%» (`salida_compuerta_nocturna.txt`) | con `contratos = 0` el paso es 0 y el balance no se mueve | un error de signo que pusiera el piso **en** el balance inicial en vez de debajo |
| «costo = 0 → vara ≤ 1,0», peor celda 0,9711 (`salida_bracket.txt`) | con costo cero el requerido coincide con la moneda, así que la vara es 1 más ruido | que el ruido de Monte Carlo lo empujara arriba de 1, o un error en la cadena |

### VÁLIDOS — podían dar otra cosa, y varios dieron otra cosa

| control | resultado |
|---|---|
| «objetivo = drawdown, costo cero → ~50%» (`aritmetica.py`) | **FALLÓ en la primera implementación** (0,376–0,499) y destapó que el piso se chequeaba por operación y el objetivo sólo a fin de día. Se descartó la corrida sin publicarla |
| «la misma tabla con costo cero debe dar 50,0%» (`salida_criterio_control.txt`) | **FALLÓ 32 de 32**, y la falla era la información: el umbral escrito a mano estaba mal para brackets asimétricos |
| consistencia: esperanza por operación ≈ 0 (`tercer_estado.py`) | **FIRÓ** y cazó la ventaja fantasma de +199,6% por mezclar tasa asumida con M2M medido |
| `p_abierta = 0` reproduce el modelo viejo **exacto** (`tercer_estado.py`) | PASADO. Podía fallar fácil: el camino nuevo podía consumir números aleatorios |
| población: 971 sesiones exactas (`media_exceso.py`) | PASADO. Cualquier cambio de filtro lo rompe |
| la inversa reproduce la directa (`piso_ventaja.py`) | PASADO tras **dos** arreglos: la primera búsqueda binaria falló porque la potencia binomial exacta no es monótona en n |
| reproducir una celda publicada de `BRACKET_RESULTADO.md` (`salida_criterio_verif.txt`) | PASADO dentro de tolerancia declarada |
| el censo reproduce las tres frecuencias ya medidas (`salida_censo.txt`) | PASADO |
| **los de hoy**: generador, horizonte largo, separación, identidad en el ensamble, real contra la nula | dos **fallaron** contra el binomial y ese fallo fue el hallazgo |

**Balance: de 16 controles publicados en esta ventana, 4 eran vacíos y 3 sólo de código.** Siete de
dieciséis no medían lo que yo decía que medían. Los nueve válidos incluyen cuatro que efectivamente
fallaron, y cada falla encontró un error real — que es la única evidencia de que la categoría
«válido» está bien asignada.
