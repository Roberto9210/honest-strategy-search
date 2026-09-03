# PRE-REGISTRO — INVARIANCIA DEL ORDEN — Ventana D, 2026-09-03

**Se commitea solo, antes de escribir una línea del script que lo corre.** Decisión de Roberto del
2026-09-03: se pre-registra **sólo** la forma 1 de `pregunta_cuanto_y_cuando.md`; las formas 2 y 3 no
se pre-registran, porque cada pregunta pre-registrada gasta K_D aunque no se corra.

**Declaración obligatoria, arriba de todo: esta pregunta se eligió DESPUÉS de ver las escaleras de
tenencia, de horas y de stops.** Se eligió con esos datos vistos. Eso no la invalida y se escribe acá
para que quede en el log, como en `pregunta_cuanto_y_cuando.md` §0.

**Contador:** K = 262 tras el descarte de H2d. Esta configuración es **K_D = 1**, así que el α de esta
pregunta es **0,05 / 263 = 1,901 × 10⁻⁴**, dos colas, |z| ≥ 3,732. El cartucho se gasta al
pre-registrar (spec §9.5), no al correr.

---

## 1 · La decisión, con sus dos posiciones

**La palanca es «cuándo estar adentro».** Las dos posiciones existen hoy y son excluyentes:

- **Posición A — una sola tabla.** La escalera de horas incondicional (`terreno_horas_resultado.md`)
  se usa tal cual, siempre, para elegir en qué hora estar adentro. No se mira el estado de ayer.
- **Posición B — dos tablas.** La elección de hora depende del estado de ayer: una tabla para días que
  siguen a un rango grande, otra para el resto.

**Cualquiera sea el resultado, una posición queda elegida.** Si el orden se conserva, A queda elegida
para siempre y la pregunta «cuándo» se cierra con lo ya medido. Si se rompe, B, y la escalera
incondicional deja de ser suficiente. La pregunta decide en los dos sentidos; ese es el motivo de
correrla.

## 2 · La condición observable antes de decidir

**Estado de ayer, conocido a las 17:00 CT del día que se opera**, con datos que la cuenta ya tiene:

```
rango_ayer   = max(high) − min(low) de la sesión anterior completa (17:00 → 16:00 CT)
umbral_t     = mediana de rango_ayer sobre las 20 sesiones anteriores a ayer
ALTO   si rango_ayer >= umbral_t          BAJO   si rango_ayer < umbral_t
```

Todo es pasado respecto de la decisión: la sesión de ayer terminó a las 16:00 CT y la mediana móvil
usa sólo sesiones anteriores. La mediana móvil, y no un número fijo de puntos, para que la partición
no dependa del nivel de volatilidad de la época: en 2016–2019 un umbral fijo en puntos partiría por
año, no por estado.

**Es a propósito el predictor público.** El agrupamiento de volatilidad dice que bajo ALTO **todo**
sube; esta pregunta no mide eso, mide si el **orden** de las horas sobre-vive a que todo suba. Un
cociente de cocientes: el GARCH no dice nada sobre él.

## 3 · El resultado, en la moneda de la cuenta

Población: la **P-escalera** de `terreno_tenencia.py` (ES 1-min Databento, 2016-01-04 → 2019-12-31,
971 sesiones, contrato único, no degradadas, con barra a las 17:00 y a las 08:30 CT y RTH completa),
menos las sesiones sin 20 previas para la mediana móvil y sin sesión anterior completa. **La N final
la imprime el script**; se espera perder ~20 sesiones del arranque.

Medida por sesión y por hora: **excursión adversa** como en toda la escalera, `open − min(low)` para
el largo y `max(high) − open` para el corto, en puntos de ES, y su equivalente en **USD de MES**
(× 5). El par que decide es el que la escalera ya nombró como extremos:

```
r = excursión(23:00 CT) / excursión(08:30 CT)        por sesión, por lado
```

**Estadístico principal, fijado acá y no sustituible después** (spec §1.2): sobre
`d = log(max(exc_23, 0,25)) − log(max(exc_0830, 0,25))`,

```
D = media(d | ALTO) − media(d | BAJO)          t = D / error estándar de la diferencia
```

Se corre en el **lado largo** como principal, porque es donde la escalera midió el cociente publicado
(0,19 en p50). El lado corto se imprime como control C3, no decide.

**Secundarios obligatorios, impresos, que no deciden:** el ranking completo de las 23 horas por
estado con su correlación de Spearman; las cuatro ventanas de tenencia (T23, RTH, H1, M15) con su
orden por estado; y el cociente r en p50, p90 y p95 por estado, en puntos y en USD de MES.

## 4 · El umbral X, sacado de la cuenta y no del dato

**No hay ningún límite diario de cuenta fondeada verificado en este repo.** Se buscó: el único
bloqueante de costo registrado es `margen_nocturno_mes`, y está **AUSENTE / sin resolver**
(`factory/veredicto_fase2.md`, vence 2026-09-07). Así que X **no** puede salir de un límite diario, y
no se inventa uno.

El único número de cuenta que existe con fuente es la fricción: **3,90 USD por ida y vuelta por
contrato de MES** (`factory/harness.py`, spec §7.3). De ahí sale X, en dos umbrales, los dos escritos
antes de correr:

| umbral | definición | qué decide |
|---|---|---|
| **X₁ · inversión** | el cociente r cruza **1,00** en algún estado: la hora barata deja de ser la barata | posición **B**: hay que condicionar |
| **X₂ · indiferencia** | la diferencia `exc(08:30) − exc(23:00)` en el estado ALTO cae por debajo de **3,90 USD de MES** (= 0,78 pts) | la palanca «cuándo» deja de pagar: las dos horas son indistinguibles para la cuenta y da igual cuál se elija |

**Regla de decisión, completa:** posición **B** si se cumple X₁ **o** X₂ **y** el contraste D es
significativo a 0,05/263 a dos colas. Posición **A** en cualquier otro caso, incluido el caso en que D
sea significativo pero el cociente siga lejos de los dos umbrales: un cambio detectable que no cruza
ninguno de los dos no cambia la decisión, y se reporta así.

**Por qué X sale de ahí y no del dato.** X₂ es lo que la cuenta puede notar: una diferencia de
excursión menor que el costo de la operación no cambia ninguna decisión. X₁ es la decisión literal.
Ninguno de los dos se elige mirando el resultado.

## 5 · La potencia declarada para ese X

Calculada con las dispersiones **ya publicadas** en `potencia_terreno_condicional.txt` (commit
`62e9040`), sin medir nada nuevo: σ_log de la hora 23:00 largo = 0,931 y de la 08:30 largo = 1,071.

**Cota conservadora, correlación cero entre las dos horas:** σ_d ≤ √(0,931² + 1,071²) = **1,42**. Con
f = 0,5 (la mediana móvil parte por mitades) y n ≈ 951:

```
factor mínimo detectable en r  =  exp((3,732 + 0,842) × 1,42 × √(1/475 + 1/476))  =  1,52×
```

Las horas están correlacionadas positivamente, así que σ_d real será menor y el mínimo detectable
también; **el script imprime la correlación medida y el mínimo detectable efectivo**, y el criterio no
se mueve por eso.

**Contra los umbrales de §4:** r vale hoy 0,21 en p50. Para cruzar X₁ tendría que multiplicarse por
4,8×; para cruzar X₂, por unas 3,7× (de 0,21 a ~0,78). **Los dos están muy por encima de 1,52×, así
que la pregunta está sobre-potenciada para lo que decide.** Eso es deliberado: la respuesta que más
vale es la negativa —el orden se conserva, la posición A queda elegida para siempre— y una respuesta
negativa sólo vale si el diseño podía ver el efecto.

**Potencia declarada:** ≥ 0,80 para cualquier cambio de r de 1,52× o más; **> 0,999** para los
factores que cruzan X₁ o X₂. Si la N final o la partición real se apartaran de lo previsto de modo que
el mínimo detectable supere 2,0×, la pregunta **se archiva como no decidible** con estos datos, como
la compuerta 2 de la spec, y no se interpreta el resultado.

## 6 · Controles, arriba del resultado, con su criterio fijado ahora

| control | qué mide | criterio | qué tumba |
|---|---|---|---|
| **K0 · la condición es la condición** | fracción de sesiones ALTO, y excursión mediana de la sesión bajo ALTO contra BAJO | partición entre 40 % y 60 %; y ALTO tiene que tener excursión **mayor** en la sesión completa | si ALTO no es más violento, la condición no es lo que dice ser y la pregunta no se interpreta |
| **K1 · placebo de etiqueta** | 1.000 permutaciones de la etiqueta ALTO/BAJO, semilla `20260903`; banda 2,5–97,5 % de D | el D real tiene que caer fuera de la banda para que haya algo | si cae adentro, no hay señal |
| **K2 · rival sin contenido** | la misma pregunta con la condición reemplazada por «día de la semana par/impar» | no debería mover el orden; se imprime al lado | si el rival da lo mismo que la condición real, lo medido es ruido de partición |
| **K3 · el otro lado** | el mismo contraste en el lado corto | los signos de D tienen que coincidir | si difieren, es un artefacto de lado y se declara |
| **K4 · escala** | la misma medición en USD de MES | exactamente 5× los puntos, sin excepción | todo |
| **K5 · cobertura** | sesiones perdidas por falta de 20 previas o de sesión anterior, y dónde caen | se imprime el conteo y los meses | nada; es el sesgo de arranque, impreso |

## 7 · Qué se corre y qué no

Se corre **un** script, `invariancia_orden.py`, una vez, sobre el **mirado 2016–2019 de los minutos de
ES de Databento**. Su salida cruda se commitea antes de una palabra de interpretación.

- **No se toca la caja.** Ninguna sesión posterior a 2019-12-31 entra: el cargador ya corta ahí.
- **No se agregan condiciones.** Una sola condición, un solo par de horas, un solo lado principal. Un
  barrido de umbrales o de pares de horas sería otra configuración y pagaría K aparte.
- **No hay ajuste después.** Si el resultado es significativo pero no cruza X₁ ni X₂, la decisión es A
  y se reporta así; no se busca otro par de horas que sí lo cruce.
- **Esto no es una ventaja.** Es la palanca «cuándo» de `pregunta_cuanto_y_cuando.md` §1: cambia el
  denominador de la cuenta, no el numerador. Un resultado favorable no autoriza dinero.
- **Limitación de traslado, repetida:** es ES y no MES, y es 2016–2019, un régimen la mitad de
  violento. Los cocientes trasladan mejor que los niveles; nada de esto está verificado en régimen
  violento.
