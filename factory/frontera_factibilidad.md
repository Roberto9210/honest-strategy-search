# La frontera de factibilidad — y por qué el veredicto no es "vacía" sino "prematura"

**Fecha:** 24 de agosto de 2026 · **Cartuchos gastados: 0.** Aritmética sobre lo ya medido: no corre
un backtest nuevo, no toca la parte B más que su calendario, y de la parte A mira **sólo dispersión**
— ninguna media, ningún signo, ningún P&L de ninguna regla nueva.

> **Versión 2.** La v1 de este documento concluyó "la frontera está vacía". Cuatro correcciones de
> Roberto la reordenaron y **el veredicto cambió de nombre**. Las cuatro están incorporadas abajo, y
> la que manda es la §2: la fricción no decide si la frontera está vacía.

## 0. La pregunta

El cartucho 2 dejó una frase que había que llevar hasta el número:

> La única palanca que vuelve alcanzable la potencia —operar más seguido— es la misma que le entrega
> la ventaja a los costos.

La fricción es un costo **fijo en dólares** ($3.90 ida y vuelta), así que su peso *relativo* crece al
acortar la tenencia, justo cuando la potencia mejora. Dos fuerzas opuestas. ¿Su suma baja alguna vez
de lo que una regla simple puede producir?

## 1. Las dos curvas

Con σ medido **incondicionalmente** sobre la parte A (4.865 sesiones) y n_B = máximo de operaciones no
solapadas que caben en las 1.669 sesiones de la parte B:

| Tenencia | σ/op | n_B máx | Potencia exige | Fricción cuesta | **BRUTO exigido** | en $ |
|---|---|---|---|---|---|---|
| **1 d** | $81.06 | 1.669 | 0.0686 σ | 0.0481 σ | **0.1167 σ** | **$9.46** |
| 2 d | $112.07 | 834 | 0.0970 σ | 0.0348 σ | 0.1318 σ | $14.77 |
| 3 d | $134.01 | 556 | 0.1188 σ | 0.0291 σ | 0.1479 σ | $19.82 |
| 5 d | $170.43 | 333 | 0.1535 σ | 0.0229 σ | 0.1764 σ | $30.07 |
| 7 d | $196.87 | 238 | 0.1816 σ | 0.0198 σ | 0.2014 σ | $39.65 |
| 10 d | $231.01 | 166 | 0.2174 σ | 0.0169 σ | 0.2343 σ | $54.13 |
| 20 d | $317.85 | 83 | 0.3075 σ | 0.0123 σ | 0.3198 σ | $101.64 |

Bajando de una sesión el mínimo se confirma por el otro lado: a ~30 minutos la fricción sola cuesta
0.1766 σ y el total sube a 0.1956 σ. **El mínimo de la tenaza está en ~1 sesión: 0.1167 σ.**

## 2. La corrección que manda: la fricción no decide si la frontera está vacía

Reordenando la propia condición:

```
c·√h  ≥  θ·√h + f/√h        (multiplicando por √h > 0)
c·h   ≥  θ·h + f
(c − θ)·h  ≥  f
```

con **θ = 2.8016/√S_B** y **f = fricción/σ₁**. De ahí:

- **Si c > θ**, existe un h que cruza — `h ≥ f/(c−θ)` — **con cualquier fricción.**
- **Si c ≤ θ**, no cruza para ningún h, **ni con fricción cero.**

*(Verificado numéricamente con el control f = 0: con c = 0.0661 y θ = 0.0686 no cruza; con c = 0.0700
cruza. La fricción no participa de la decisión.)*

**La fricción decide DÓNDE cruza, no SI cruza.** Y θ sale **enteramente del largo de la parte B**:

```
θ = 2.8016 / √S_B = 2.8016 / √1669 = 0.068577
```

> **Entonces la frontera no está vacía por los costos. Está vacía —si lo está— porque la caja fuerte
> es corta.** Es una afirmación sobre cuántos datos guardamos, no sobre cuánto cobra el bróker.

## 3. La corrección al numerador: c está inflado por selección

La v1 comparó θ contra c = 0.0661, de F4. **F4 es el mejor de 58 configuraciones: c = 0.0661 es un
máximo de orden, sesgado hacia arriba.** Es la propia lógica de multiplicidad de la spec, aplicada a
la frontera.

**Cota grosera del sesgo.** Bajo la nula global, el mejor de 57 configuraciones da p ≈ 1/58 = 0.01724,
o sea |t| ≈ **2.3815**. F4 midió **t = 2.304**. El exceso sobre lo que produce la selección sola es
**−0.0775**: negativo. La corrección grosera por máximo de orden **deja el efecto de F4 en cero** — es
la cuenta de `botc_potencia_f4.md` §3, ahora aplicada a c en vez de a δ.

**Las únicas estimaciones de c libres de selección** son los dos cartuchos de la Fase 2, porque fueron
**pre-registrados antes de conocer su resultado** — el diseño de la fase es, sin haberlo buscado, la
única fuente insesgada que tenemos:

| Ancla | h | c = δ_bruto/√h | error estándar |
|---|---|---|---|
| Cartucho 1 (k=3, hold=3) | 3 | 0.0618 | ± 0.0371 |
| Cartucho 2 (k=1, hold=1) | 1 | 0.0440 | ± 0.0257 |
| **Combinados por precisión** | — | **0.0498** | **± 0.0211** |
| *IC 90 %* | | *[0.0150, 0.0846]* | |
| F4 (seleccionado, inflado) | 7 | 0.0661 | — |

**c − θ = −0.0188 ± 0.0211.** Está por debajo, **y no significativamente.** Roberto tiene razón en que
la brecha real es más ancha que el 4 % que reportaba la v1 — pero también es mucho más incierta, y esa
segunda mitad es la que cambia el veredicto.

## 4. La corrección al modelo: `c·√h` es generoso con las tenencias largas

`logrado = c·√h` supone **deriva constante por unidad de tiempo**: la ventaja en dólares crece lineal
en h mientras σ crece con la raíz. Vale si el mecanismo es **persistente** (una prima que se devenga
mientras estás en posición).

Si el mecanismo es **transitorio** —una corrección que se completa y después se agota— la ventaja en
dólares **se aplana** en algún h\*, y a partir de ahí en unidades de σ **decae como 1/√h**. El mejor
punto pasa a ser h = h\* y alargar más **empeora**. La condición de cruce sigue siendo (c−θ)·h ≥ f,
pero con **h ≤ h\***.

Y esto importa: los mecanismos declarados de este proyecto son **todos transitorios**. Flujo de
rebalanceo de fin de mes (F4), liquidez a vendedores forzados (G2): los dos se agotan en días.

## 5. La pregunta que decide: ¿cuánta caja fuerte falta?

Condición: `θ ≤ c − f/h` ⟹ **S_B ≥ (2.8016 / (c − f/h))²**. Con S_B = 1.669 hoy y 252 sesiones al año:

| c | Modelo | h operable | S_B necesario | Faltan | **Años de espera** |
|---|---|---|---|---|---|
| 0.0661 *(F4, inflado)* | persistente | 10 | 2.090 | 421 | **1,7 a** |
| 0.0661 *(F4, inflado)* | persistente | 20 | 1.935 | 266 | **1,1 a** |
| 0.0661 *(F4, inflado)* | transitorio h\*=7 | 7 | 2.238 | 569 | **2,3 a** |
| 0.0661 *(F4, inflado)* | transitorio h\*=3 | 3 | 3.132 | 1.463 | **5,8 a** |
| **0.0498** *(insesgado)* | persistente | 10 | 3.880 | 2.211 | **8,8 a** |
| **0.0498** *(insesgado)* | transitorio h\*=7 | 7 | 4.262 | 2.593 | **10,3 a** |
| **0.0498** *(insesgado)* | transitorio h\*=3 | 3 | 6.891 | 5.222 | **20,7 a** |
| 0.0846 *(IC 90 % alto)* | persistente | 10 | 1.234 | 0 | **ya alcanza** |

Y θ cae solo, porque la caja fuerte crece sola:

| | Hoy | +2 a | +5 a | +10 a | +20 a |
|---|---|---|---|---|---|
| S_B | 1.669 | 2.173 | 2.929 | 4.189 | 6.709 |
| θ | 0.0686 | 0.0601 | 0.0518 | 0.0433 | 0.0342 |
| c necesario (h=10) | 0.0734 | 0.0649 | 0.0566 | 0.0481 | 0.0390 |

## 6. Veredicto: **Fase 2 prematura**, no "frontera vacía"

Las dos cosas se publican muy distinto y sólo una es cierta:

- ❌ *"En este instrumento, a estos costos, la potencia y la fricción no tienen intersección."*
  **Falso como está escrito.** La fricción no decide si hay intersección (§2), y el c contra el que se
  midió estaba inflado por selección en una dirección y es estadísticamente indistinguible de θ en la
  otra (§3).
- ✅ **"La caja fuerte de 1.669 sesiones es demasiado corta para decidir si existe una ventaja
  explotable en MES, y la incertidumbre sobre el tamaño de efecto alcanzable es tan grande que el
  tiempo de espera va de cero a veinte años según cuál de dos números medidos sea el correcto."**

El rango honesto es **[ya alcanza, 20,7 años]** y su punto central está cerca de **9 años**. Ese rango
es la salida, no un número. Estrecharlo requiere más estimaciones **insesgadas** de c — es decir, más
cartuchos pre-registrados, que es exactamente para lo que existen los 198 restantes.

**Corolario incómodo y honesto:** cada cartucho pre-registrado sirve para dos cosas a la vez —
buscar una ventaja, y medir c sin sesgo. Lo segundo no depende de que la búsqueda encuentre nada.

## 7. La inconsistencia entre nuestros propios instrumentos, resuelta

La criba decía **G4 "VALIDABLE, holgada"** (δ_min 0.0485, la mejor de las cinco). La frontera decía que
las tenencias cortas son el peor lugar posible. **Las dos hablaban de la misma familia y apuntaban a
lados opuestos, porque la criba medía potencia y no miraba fricción.** Es el mismo defecto que ya
habíamos corregido entre `required_t_a` y `power_check`: dos compuertas con nombres parecidos midiendo
cosas distintas.

**Corregido** (`CAMBIO_DE_REGLAS` `3d5887b8c7630728`, dirección **ENDURECE**): la criba ahora exige σ
por operación —fail-closed sin él— y compara **bruto contra bruto**:
`exigido = 2.8016/√n_B + fricción/σ` contra la referencia bruta de F4 (0.1749).

| Familia | n_B máx | σ/op | Potencia | Fricción | **Exigido** | $/op | Manda | Veredicto |
|---|---|---|---|---|---|---|---|---|
| **G1** nocturna | 1.669 | $81.06 | 0.0686 | 0.0481 | **0.1167** | $9.46 | potencia | VALIDABLE |
| **G3** régimen | 834 | $81.06 | 0.0970 | 0.0481 | 0.1451 | $11.76 | potencia | VALIDABLE |
| **G5** cruzado | 834 | $81.06 | 0.0970 | 0.0481 | 0.1451 | $11.76 | potencia | VALIDABLE |
| **G2** multi-día | 589 | $81.06 | 0.1154 | 0.0481 | 0.1636 | $13.26 | potencia | VALIDABLE |
| **G4** bordes | 3.338 | $22.08 | 0.0485 | **0.1766** | **0.2251** | $4.97 | **fricción** | **NO VALIDABLE** |

**G4 pasa de la mejor a la peor.** Su fricción pesa **3,6 veces** su ventaja de potencia. Ya no puede
gastar cartuchos: `preregister()` la rechaza. Sus 40 siguen sin gastarse y la decisión de darla
formalmente fuera de alcance —con la pérdida de esos 40, sin retirarlos del denominador ni
reasignarlos— queda pendiente, porque es irreversible.

Y nótese la respuesta a la pregunta *"¿G4 es factible o no?"*: **no**, y el motivo es exactamente el
que la frontera predijo. Los dos instrumentos ahora coinciden porque miden lo mismo.

## 8. Qué queda sobre la mesa

La celda más barata de todo el espacio de diseño sigue siendo **G1** (0.1167 σ, $9.46 brutos por
operación) — una operación por sesión, tenencia de ~1 sesión, sin filtro. Todo filtro reduce la
frecuencia y **sube** la barra, por lo que G3 y G5 empeoran la aritmética por construcción.

Y G1 es la única que **la serie diaria congelada no puede medir**: el tramo cierre→apertura de ES=F en
Yahoo carga el 3,3 % de la varianza porque es la reapertura de las 18:00 ET.

> La celda más barata sigue siendo la que los datos no pueden contestar. Pero ahora sabemos que eso no
> cierra la fase: la cierra —o no— el largo de la caja fuerte, y ese número crece solo.

---

# Adenda del 24-ago-2026 (tarde) — qué es c, y las tres consecuencias del corolario

## 9. Qué es c, con precisión

**c no es una propiedad del mercado. c es la calidad de las hipótesis que sabemos generar.**

Formalmente: `c = δ_bruto / √h`, donde δ_bruto es la ventaja bruta por operación en unidades de σ que
**una regla nuestra** consigue, medida sobre este instrumento con estos datos. No sale de la
estructura del mercado: sale del cruce entre el mercado **y nuestro proceso de inventar reglas**.

Eso cambia por completo cómo se lee todo lo anterior:

| No estamos midiendo | Estamos midiendo |
|---|---|
| si el mercado tiene ventajas explotables | si **nosotros** sabemos encontrarlas |
| la eficiencia del S&P 500 | la calidad de nuestro generador de hipótesis |
| una constante de la naturaleza | una propiedad de este equipo, estas herramientas y esta serie |

Un veredicto negativo, entonces, **no es una afirmación sobre eficiencia de mercado** — es una
afirmación sobre nosotros. Y es la cantidad correcta para la pregunta que da origen a todo esto, que
nunca fue "¿es eficiente el mercado?" sino **"¿podemos nosotros sacarle algo?"**.

Consecuencia práctica: c puede **subir** si mejoramos el generador de hipótesis (mejores mecanismos,
mejores datos, otro instrumento). No es un techo físico. Es nuestro techo de hoy.

## 10. c está medido con dos configuraciones de una sola familia

Todo el veredicto descansa en c, y c sale hoy de **dos cartuchos de G2**. Peor: **dos configuraciones
de la misma regla a dos umbrales no son dos muestras independientes** de la calidad de nuestras
hipótesis. **m efectivo = 1.** Estamos midiendo G2, no el espacio.

La respuesta es la **política de asignación declarada** (`spec_fase2.md` §2b): tope de concentración
del 40 % por mecanismo **y por familia**, cobertura obligatoria de estratos de tenencia, y `mecanismo`
y `h` como campos obligatorios del pre-registro. Con la cuenta de cuántos cartuchos hacen falta —
**entre 3 y 30 según cuánto varíe c**— y la observación de que un cartucho a máxima frecuencia aporta
el mismo peso sea cual sea su tenencia, así que **diversificar tenencias no cuesta precisión**.

## 11. ¿Puede el estimador mezclar tenencias sin sesgo?

**Sólo bajo el modelo persistente.** Si `δ_bruto(h) = c·√h` con un único c, cada estimación es
insesgada y mezclar es correcto ponderando por `n·h`.

Si el mecanismo es **transitorio** (§4), `δ_bruto(h) = c·√h` vale sólo hasta h\*, y más allá decae. Una
regla medida con h > h\* da un c **sesgado hacia abajo**. Mezclar tenencias entonces **sesga c hacia
abajo**, y como un c bajo es lo que produce el veredicto "vacía", **el sesgo se autoconfirma**.

**Por lo tanto el estimador se estratifica por tenencia, no se agrupa**, hasta poder mostrar que c no
depende de h. Eso exige cobertura de los tres estratos, que es exactamente lo que la política §2b
obliga. Y el estrato **h < 1 sesión no tiene ningún dato** — es la única región sin cubrir, y la única
familia que puede cubrirla es G4.

## 12. G4 como SÓLO-MEDICIÓN: evaluación

**El argumento a favor es correcto y contradice mi propia recomendación anterior.** Una configuración
de G4 no puede pasar la barra jamás (exige 0.2251 σ contra la referencia 0.1749), pero **sí produce
una estimación insesgada de c a tenencias cortas** — la única región sin un solo dato. Retirarla tira
40 mediciones de la zona sin cubrir.

**¿Rompe algo de la spec?** Revisado punto por punto:

- **§3.5** dice que el presupuesto de una familia NO VALIDABLE se pierde. Eso se escribió suponiendo
  *"no validable = inútil"*, que es justamente lo que este argumento refuta. No es una contradicción
  lógica sino un supuesto tácito que quedó falso.
- **§1 (multiplicidad).** Acá está el punto delicado, y hay que decirlo derecho: **una corrida de
  sólo-medición SÍ revela rentabilidad** — c se calcula de la ventaja media, que es exactamente la
  respuesta. No es como el conteo de frecuencia. **Por lo tanto NO puede ser gratis: consume su
  cartucho igual.** Lo que cambia no es el precio sino el destino.
- **Fuga de información.** Aun sin poder reportarse como candidata, una corrida de sólo-medición
  enseña qué regiones lucen bien y podría orientar la búsqueda. Eso se paga con el cartucho (queda
  contado en K = 257) y se cierra prohibiendo permanentemente que esa configuración se re-registre
  como búsqueda — la misma maquinaria que ya usan las celdas de vecindad.

**Clasificación del cambio (§9.5c): AFLOJA.** Permite gastar cartuchos que las reglas de hoy
prohíben. No afloja *la barra* —las configuraciones de G4 nunca podrán pasarla, es una restricción
absoluta— pero permite un gasto hoy vedado, y ante la duda la spec manda clasificar como AFLOJA y
**exigir aprobación explícita**, que además queda marcada para siempre en el veredicto. Es lo correcto
para un cambio de este tipo, y no cuesta nada porque el que lo propone es quien aprueba.

**Recomendación:** aprobarlo, con estas cuatro condiciones escritas:

1. Estado `SOLO_MEDICION` distinto de `FUERA_DE_ALCANCE`, bloqueado en código: sus resultados **nunca**
   pueden reportarse como candidatas ni abrir la caja fuerte.
2. Consume cartucho normal. K_total sigue en 257.
3. Toda configuración corrida en modo sólo-medición queda **permanentemente vedada** para la búsqueda.
4. Su c entra al estimador **en su propio estrato de tenencia**, nunca agrupado.

## 13. El mapeo de día CME: trabajo acotado, pero puede no rescatar a G1

**¿Horas o investigación abierta? Horas.** Verificado sobre el archivo, no estimado:

- `es_1min_databento.csv` trae `ts_event_utc` en ISO-8601 UTC (`2010-06-07T00:00:00Z`).
- La transformación es determinista: convertir a `America/New_York` (DST resuelto por la librería) y
  aplicar *si la hora ET ≥ 18:00, el día de negociación es el siguiente; si no, el mismo*.
- **Hay blanco de verificación:** el QC publicado ya cuenta **4.183 días de negociación** con esa
  convención, más los conteos de barras por año. Si el mapeo los reproduce, está bien.
- El riesgo no es el algoritmo, es el volumen: 4,9 M de filas y 327 MB. Manejable.

**Pero —y esto pesa más que el costo— arreglarlo puede no rescatar a G1 tal como está declarada.** El
ES cotiza ~23 h por día: el mercado casi nunca está *cerrado*. El mecanismo declarado de G1
—"compensación por mantener exposición con el mercado cerrado"— **apenas aplica a un futuro que casi
no cierra**. Lo que la serie de 1 minuto sí daría es la partición **horario de contado (09:30–16:00
ET) contra fuera de horario**, que es una descomposición real y estudiada, pero cuyo mecanismo es
*"el flujo se concentra en horas de contado"*, no *"compensación por cierre"*.

Bajo §7.2 eso es **una hipótesis distinta** y hay que re-declararla. Es legítimo, pero conviene
decirlo antes de gastar las horas: el mapeo desbloquea **una variante de G1 con otro mecanismo**, no
la G1 que está escrita.
