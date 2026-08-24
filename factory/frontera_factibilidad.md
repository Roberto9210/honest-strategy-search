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
operación) — una operación por sesión, tenencia de ~1 sesión, sin filtro.

> **CORREGIDO el 24-ago-2026 (adenda 4, §23).** Acá decía *"todo filtro reduce la frecuencia y sube la
> barra, por lo que G3 y G5 empeoran la aritmética por construcción"*. **Es falso como afirmación
> general** y la corrección está en la §23: un filtro no sólo recorta operaciones, también **concentra
> la ventaja** en las que deja, y conviene si esa concentración supera un umbral computable
> (1.24× para un filtro de mediana, 1.59× para uno de cuartil). G3 y G5 **no** están excluidas por
> construcción: tienen una vara, y esa vara es la hipótesis que cada filtro debe declarar.

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

---

# Adenda 2 — la frontera de la hipótesis de contado, calculada ANTES de tocar el mapeo

*Aplicar a nuestra propia decisión de herramientas la misma regla que le exigimos a las estrategias.*

El mapeo de día CME no rescata a G1: **la reemplaza** por otra hipótesis, *"el flujo se concentra en
horario de contado"*. Entonces la pregunta no es si vale gastar horas en rescatar G1, sino si vale
gastarlas en habilitar una hipótesis nueva **cuya factibilidad no calculamos**. Se calcula primero.

## 14. La trampa del cálculo ingenuo

Extrapolar el c diario hacia las ventanas cortas asumiría que el efecto **no** se concentra — que es
exactamente lo contrario de la hipótesis. Sería asumir la respuesta. Así que se le da a la hipótesis
**el máximo crédito posible**: que la ventaja se concentre *exactamente como la varianza*.

Con w = fracción de varianza de la ventana y τ = fracción de tiempo:

```
ventaja_ventana / ventaja_día = w         (se concentra como la varianza)
σ_ventana / σ_día             = √w
⟹ δ_ventana = √w · δ_día
⟹ c_ventana / c_día = √(w/τ)              ← el "bono de concentración"
```

Medido en SPY sobre la parte A —cuya apertura **sí** es la de contado—: el horario de contado carga
**68,8 % de la varianza en 27,1 % del tiempo**, o sea **2,54× de concentración por unidad de tiempo**.
El bono resultante es **√(0.688/0.271) = 1,594**.

## 15. El resultado

| Ventana | σ/op | n_B | Potencia | Fricción | Exigido | **c exigido** |
|---|---|---|---|---|---|---|
| Media sesión de contado | $47.54 | 3.338 | 0.0485 | 0.0820 | 0.1305 | **0.3547** |
| Sesión de contado completa | $67.24 | 1.669 | 0.0686 | 0.0580 | 0.1266 | **0.2432** |
| Contado a contado (24 h) | $81.06 | 1.669 | 0.0686 | 0.0481 | 0.1167 | **0.1167** |
| Fuera de horario (17,5 h) | $45.27 | 1.669 | 0.0686 | 0.0861 | 0.1547 | **0.1812** |

Y con el bono de concentración aplicado al c medido:

| Ventana | Bono | c lograble (c=0.0661 inflado) | **logrado/exigido** | con c=0.0498 |
|---|---|---|---|---|
| Media sesión de contado | 1,594 | 0.1054 | **30 %** | 22 % |
| Sesión de contado completa | 1,594 | 0.1054 | **43 %** | 33 % |
| Contado a contado (24 h) | 1,000 | 0.0661 | **57 %** | 43 % |
| Fuera de horario | 0,654 | 0.0432 | **24 %** | 18 % |

**Ninguna cruza, ni dándole a la hipótesis el máximo crédito de concentración y el c más inflado que
tenemos.** Y hay un motivo
estructural, precisado en la §22: estas ventanas **no son encadenables** — la sesión de contado ocurre
una vez por día, así que tienen el σ de una ventana corta y el n_B de una regla diaria. Lo peor de los
dos lados.

## 16. Veredicto sobre el mapeo: las horas no valen

**La mejor de las cuatro ventanas es "contado a contado" — una tenencia de un día con una operación
por sesión: exactamente el mismo σ y el mismo n_B que la celda que el cartucho 2 ya midió sobre la
serie DIARIA.** El mapeo de día CME **no habilita ninguna celda mejor que la que ya podemos medir sin
él**. Sus horas comprarían acceso a tres ventanas peores y a una que ya tenemos.

Por lo tanto, y conforme a la regla que le exigimos a cualquier estrategia: **la hipótesis de contado
no puede cruzar la frontera, así que G1 sale de alcance con ese motivo** — no por el defecto de la
serie diaria, sino porque la hipótesis que el arreglo habilitaría tampoco alcanza. La decisión formal
(perder sus 40 cartuchos, sin retirarlos del denominador ni reasignarlos) queda para Roberto, que es
irreversible.

*Nota sobre lo que este cálculo no dice:* no dice que no haya efecto de concentración de flujo en
horas de contado — la varianza demuestra que sí lo hay, 2,54× por unidad de tiempo. Dice que **aun
suponiendo que la ventaja se concentre en la misma proporción**, la ventana resultante exige más de lo
que sabemos producir. Es, otra vez, una afirmación sobre nuestro c, no sobre el mercado.

---

# Adenda 3 — el modelo detrás del bono, y el patrón que ata la fase entera

## 17. De dónde sale √(w/τ) = 1.594, con el álgebra

*El número se publica, así que tiene que sostenerse solo. Si un tercero no puede reconstruirlo, es
una afirmación en vez de un cálculo.*

**Notación.** Un día completo (24 h) tiene varianza `V` y ventaja bruta `E` (en dólares). Una ventana
cubre la fracción `τ` del **tiempo** y la fracción `w` de la **varianza**.

**Supuesto 1 — cómo escala σ.** La varianza es **aditiva entre ventanas disjuntas y no
correlacionadas**: `V_ventana = w·V`, por lo tanto

```
σ_ventana = √w · σ_día
```

Es el supuesto estándar de incrementos de precio no correlacionados (martingala), y es lo que
*significa* "fracción de varianza". Es también el supuesto bajo el cual w es medible: lo medimos en
SPY sumando las varianzas de las dos patas.

**Supuesto 2 — cómo se acumula la ventaja.** Acá hay tres ramas posibles, y la elección importa:

| Rama | `E_ventana / E_día` | Bono resultante | Valor |
|---|---|---|---|
| **Conservadora** — la ventaja se devenga con el **tiempo** | `τ` | `(τ/√w)/√τ = √(τ/w)` | **0.627×** |
| **Generosa** — la ventaja se concentra **como la varianza** | `w` | `(w/√w)/√τ = √(w/τ)` | **1.594×** |
| **Extrema** — **toda** la ventaja del día ocurre en la ventana | `1` | `(1/√w)/√τ` | **2.317×** |

**El álgebra, en tres líneas.** Con `δ = E/σ` y `c = δ/√h`, `h_ventana = τ`, `h_día = 1`:

```
δ_ventana = E_ventana / σ_ventana = (ρ·E_día) / (√w · σ_día) = (ρ/√w) · δ_día
c_ventana = δ_ventana / √τ        = (ρ / (√w·√τ)) · δ_día
c_ventana / c_día = ρ / √(w·τ)                        con ρ = E_ventana/E_día
```

Sustituyendo `ρ = w` sale `√(w/τ)`. **Chequeo interno:** el cociente entre la rama generosa y la
conservadora tiene que dar exactamente `w/τ` — la concentración de varianza por unidad de tiempo —, y
da **2.54**, que es el valor medido. El álgebra cierra sobre sí misma.

**Elegimos la rama generosa** (1.594×) porque le da a la hipótesis el máximo crédito compatible con
lo medido: el flujo se concentra, y suponemos que la ventaja se concentra en la misma proporción.

**Y con la rama EXTREMA, que ni siquiera es defendible** —suponer que el 100 % de la ventaja del día
ocurre en horario de contado y **cero** fuera—:

| Ventana | Bono extremo | c lograble | c exigido | logrado/exigido |
|---|---|---|---|---|
| Sesión de contado completa | 2.317 | 0.1531 | 0.2432 | **63 %** |
| Media sesión de contado | 2.317 | 0.1531 | 0.3547 | **43 %** |

**Tampoco cruza.** La conclusión no depende de qué rama se elija — y tampoco depende del bono en
absoluto, porque *contado a contado*, la mejor de las cuatro ventanas, tiene `τ = w = 1` y **bono
exactamente 1**: no usa el modelo para nada.

## 18. El patrón acumulado: la restricción somos nosotros

Cuatro rutas independientes, cuatro veces el mismo veredicto:

| Candidata | Murió por | Ruta |
|---|---|---|
| **F4** vuelta de mes | multiplicidad | p 0.0212 peor que el 0.0172 del azar en 57 búsquedas |
| **G2** multi-día | potencia, a **dos** tenencias | 84 y 518 operaciones contra 342 y 1.121 necesarias |
| **G4** bordes | fricción | 0.1766 σ de peaje, 3.6× su ventaja de potencia |
| **G1** nocturna | descomposición sub-diaria | partir el día recorta σ más rápido de lo que multiplica operaciones |

**Eso ya no son cuatro hallazgos: es uno medido cuatro veces.** Cada familia murió por un mecanismo
distinto y todas llegaron al mismo número — **c no alcanza**.

Y por la definición de la §9, **c es la calidad de las hipótesis que sabemos generar**. Entonces:

> **La restricción que ata la fase entera no es la estructura de ninguna familia. Somos nosotros.**

Cambiar de familia no cambia c, porque las cinco familias salen del mismo generador de hipótesis: el
nuestro. Es la misma muestra tomada cinco veces, no cinco muestras.

## 19. G6 es la única familia que muestrea un generador distinto

De las seis familias declaradas, **cinco nos miden a nosotros**. G1, G2, G3, G4 y G5 son mecanismos
que se nos ocurrieron a nosotros, escritos por nosotros, en el vocabulario que manejamos nosotros. Su
c es nuestro c, medido cinco veces.

**G6 —reglas propuestas por terceros— es la única que muestrea un generador distinto.** Es el único
lugar de toda la Fase 2 donde c podría ser **otro número** en vez del mismo número otra vez.

Eso cambia qué significa el orden declarado. Hoy **G6 está última**, con el presupuesto más chico
(20 de 200), y es el único sitio donde la restricción que ata todo lo demás podría no aplicar.

*(Lo que esto NO autoriza: reordenar. El orden está declarado en §4.2 y cambiarlo después de ver
resultados es exactamente lo que la spec impide. Si se reordenara, el argumento tendría que ser el
estructural —"G6 muestrea otro generador", que era cierto antes del primer cartucho— y nunca
"las otras vinieron mal"; y sería un `CAMBIO_DE_REGLAS` con su dirección y su justificación.)*

## 20. Qué haría falta para que una regla de un tercero entre a G6

Repasadas las compuertas una por una. **Casi todas aplican sin cambios** — son sobre la regla y los
datos, no sobre quién la pensó:

| Compuerta | ¿Aplica? | Detalle |
|---|---|---|
| 20 cartuchos del presupuesto | **sí, igual** | ya escrito en §4.2: una regla que te pasó otro consume presupuesto exactamente igual |
| Criba de medibilidad (familia y config) | **sí, sin cambios** | es frecuencia y σ; el origen no entra |
| Barra §3, compuerta de potencia, caja fuerte | **sí, sin cambios** | |
| Tope de concentración §2b | **sí** | G6 son 20 de 200 = 10 %, muy por debajo del 40 % |
| Pre-registro antes del resultado | **sí, con un agregado** | ver abajo |
| `mecanismo` declarado | **sí, con un agregado** | ver abajo |

**Lo que hay que agregar, y sólo tiene sentido para reglas ajenas:**

1. **Especificación completa antes de correr.** Las reglas de terceros llegan con huecos (umbral
   exacto, salida, tamaño). **Cada parámetro que rellenamos nosotros es un grado de libertad**, y si
   probamos varios rellenos, cada uno es un cartucho. La regla entra **completamente especificada**, o
   los huecos se fijan por declaración escrita antes de correr — nunca eligiendo.
2. **Mecanismo, aunque haya que reconstruirlo.** Muchas reglas ajenas vienen sin mecanismo ("a mí me
   funciona"). §2b lo exige. Si el proponente no lo da, lo escribimos nosotros **etiquetado como
   reconstrucción nuestra**, no como suya.
3. **Cuáles de sus reglas probamos es una elección NUESTRA.** Si un amigo manda cinco y probamos dos,
   esa selección es un cribado por plausibilidad. Se declara antes de correr ninguna: "se prueban
   todas", o "en el orden en que llegaron", o el criterio que sea — pero declarado.
4. **Registro de procedencia:** quién la propuso, cuándo, con qué palabras, y —lo que decide todo lo
   demás— **si nos dijo que funciona**.

## 21. Si una regla ajena midiera un c claramente mayor: qué se puede concluir y qué no

**El problema, dicho antes de que llegue la primera:** una regla que alguien reporta como ganadora
**ya viene seleccionada por su resultado**. Su c medido está sesgado exactamente como el de F4 — y
**peor**, porque con F4 sabíamos que K = 57. Con la regla de un tercero, K es **desconocido y
probablemente enorme**: todas las variantes que probó, más todos los traders cuyas reglas perdedoras
nunca escuchamos. Es el problema del cajón de los fracasos, sin denominador.

**Por lo tanto, se clasifican al ingreso —antes de correr— en dos clases:**

**Clase A — mecanismo sin selección sobre datos que compartimos.** Propuesta por su razonamiento, o
seleccionada sobre otro instrumento/mercado que nosotros no usamos como desarrollo. Su selección es
débil o inexistente respecto de nuestra parte A.
- **Su c ENTRA al estimador**, en su propio estrato de tenencia.
- Y sería **la primera evidencia de que c no es una constante de este equipo sino del generador**.

**Clase B — reportada como ganadora sobre datos que se solapan con los nuestros.**
- **Su c NO entra al estimador**, y la exclusión se publica con el motivo.
- **Se puede probar igual** (consume cartucho, se registra, se publica), pero su resultado **no puede
  interpretarse como evidencia sobre c**.
- Y algo más incómodo: **tampoco puede validarse contra nuestra barra**, porque `α/K` cubre *nuestra*
  multiplicidad y la de ellos no la conocemos ni podemos contarla. Un p-valor calculado sobre datos
  en los que otro ya seleccionó no es un p-valor.

**Lo único que valida honestamente una regla de Clase B** es evidencia que su selector no pudo haber
usado: un **forward test desde hoy**, sobre datos que todavía no existen. Es exactamente lo que
`botc_potencia_f4.md` §6 concluyó para F4, y aplica igual acá — con la misma advertencia sobre el feed.

**La clasificación se hace al ingreso, con el cuestionario, ANTES de medir nada.** Después de ver
nuestro propio número la clasificación se vuelve motivada: nadie clasifica como Clase B una regla que
acaba de medir un c espectacular. Por eso el cuestionario tiene que preguntar, explícitamente:
*¿cuántas variantes probaste antes de ésta?*, *¿la elegiste porque rindió bien?*, *¿sobre qué datos e
instrumento?*

**Y el resumen honesto de la respuesta a "¿qué se puede concluir?":** de una regla ajena reportada
como ganadora, **sobre c no se puede concluir nada**. De una regla ajena propuesta por su mecanismo,
se puede concluir tanto como de una nuestra — y es el único experimento de toda la fase que podría
mostrar que el techo no es del mercado sino nuestro.


---

# Adenda 4 — la consolidación: la región factible es una cuenca angosta, no un espacio

## 22. Dónde está el mínimo de verdad, y cuán ancho es

Juntando las dos fronteras, la región factible colapsa. Pero el número publicado en la §1 estaba
evaluado sólo en enteros h ≥ 1, y el mínimo real no cae ahí. Derivándolo:

```
exigido(h) = θ·√h + f/√h
d/dh = 0  ⟹  θ/(2√h) = f/(2h^{3/2})  ⟹  h* = f/θ
h* = 0.048113 / 0.068577 = 0.7016 sesiones ≈ 16,8 h
exigido(h*) = 0.11488 σ      exigido(1) = 0.11669 σ  →  h=1 está a 1,6 % del óptimo
```

**No es un punto: es una cuenca plana.**

| Dentro del … del mínimo | h admisible |
|---|---|
| 5 % | **[0,37 , 1,32] sesiones** |
| 10 % | [0,29 , 1,70] |
| 25 % | [0,18 , 2,81] |

**Y por qué las ventanas de contado no entran en la cuenca aunque tengan h < 1.** La fórmula supone
operaciones **encadenadas** (n_B = S_B/h). La sesión de contado ocurre **una vez por día**: tiene el σ
de una ventana corta y el n_B de una regla diaria — lo peor de los dos lados. **La cuenca sólo aplica
a lo encadenable.**

**Veredicto sobre la consolidación: correcta en lo esencial.** La región factible es una banda angosta
alrededor de ~0,7–1,3 sesiones, encadenable, sin filtro; y h = 1 está a 1,6 % del óptimo, así que el
cartucho 2 **sí** midió esa celda. Lo que no es correcto es llamarla "una celda": es una cuenca, y su
piso es 0.1149 σ, no 0.1167 σ.

## 23. Filtros: corrección a una afirmación que publiqué

Escribí que *"todo filtro reduce la frecuencia y sube la barra, así que G3 y G5 empeoran la aritmética
por construcción"*. **Está mal como afirmación general**, y la corrección importa porque decide si dos
familias vivas siguen teniendo sentido.

Un filtro no sólo recorta operaciones: **su propósito es concentrar la ventaja** en las que deja. Hay
que comparar las dos cosas.

Sea una regla base con n_B operaciones y ventaja bruta δ por operación. Un filtro deja la fracción
**φ** de las operaciones y la fracción **ψ** de la ventaja total (*"el filtro sirve"* significa ψ > φ).
La tenencia no cambia, así que σ por operación tampoco:

```
ventaja por operación filtrada = δ · ψ/φ          n_B filtrado = φ · n_B
```

Conviene filtrar si `δ'/exigido' > δ/exigido`, lo que se reduce a:

```
ψ  >  [ A·√φ + F·φ ] / (A + F)        con A = 2.8016/√n_B ,  F = fricción/σ
```

> **CORREGIDO el 24-ago-2026 (adenda 5, §26).** La tabla que estaba acá era el corte en **h = 1** y se
> publicó como si fuera una constante. **No lo es:** `A = θ√h` y `F = f/√h` dependen de la tenencia, y
> a lo largo de la propia cuenca la vara en φ = 0,50 va de **1,144×** (h = 0,374) a **1,270×**
> (h = 1,317). Un filtro con residuo h ≈ 1,3 necesita 1,270× y la tabla le pedía 1,243×: **dejaba pasar
> algo que no paga.** La vara correcta es una **función**, en la §26.

La tabla que se publicó, para referencia — **es el corte en h = 1 y no debe usarse como vara**:

| φ (frecuencia que queda) | ψ mínimo (h=1) | concentración (h=1) |
|---|---|---|
| ~~0,75~~ | ~~0,818~~ | ~~1,09×~~ |
| ~~0,50 (mediana)~~ | ~~0,622~~ | ~~1,24×~~ |
| ~~0,25 (cuartil)~~ | ~~0,397~~ | ~~1,59×~~ |
| ~~0,10~~ | ~~0,227~~ | ~~2,27×~~ |

**Respuesta a la pregunta 1: G3 y G5 no se salen de la cuenca por construcción.** Se salen si su
filtro no concentra lo suficiente — y ese umbral es **una función que cada filtro tiene que declarar y
superar antes de correr** (§26). Es una vara computable y verificable, en vez de una exclusión a mano
alzada.

## 24. El precio de la cobertura de estratos, antes de pagarlo

La cobertura sirve a la **medición**; la concentración en la cuenca sirve a la **búsqueda**. Ahora que
sabemos que fuera de la cuenca es estrictamente peor para buscar, **cada cartucho de cobertura es
gasto puro de medición** y tiene que justificarse solo.

**Cobertura hoy:** `corto` ✅ (cartucho 2, h=1) · `medio` ✅ (cartucho 1, h=3) · `largo` ❌ ·
`intradia` ❌ (sólo G4 puede cubrirlo).

| Gasto | Qué compra |
|---|---|
| **1 cartucho** (`largo`, h ≥ 6) | Cierra la obligación de §2b. Curva de 3 puntos. |
| **2 cartuchos** (+ `intradia` vía G4) | Curva de 4 puntos, uno por estrato: permite afirmar *"ningún estrato muestra c cerca de θ"* — groseramente, con barras de ±0.0143. |
| **26 cartuchos** (~6,6 por estrato) | Permite **detectar si c varía con h**: la diferencia observada entre estratos es 0.0661 − 0.0440 = 0.0221, y detectarla al 80 % exige SE por estrato ≤ 0.00558, o sea peso 32.141 = 6,6 cartuchos. |

**El precio, escrito antes de pagarlo:** 2 cartuchos = **1,3 %** de los 158 restantes, y compran una
curva de 4 puntos con barras anchas. 26 cartuchos = **17 %**, y compran la única evidencia capaz de
distinguir el modelo **persistente** del **transitorio** (§4, §11) — que es el parámetro del que
dependen los "8,8 años" contra los "20,7 años" de la §5.

**Recomendación:** pagar los 2 ahora (obligatorio + el estrato vacío) y **no** comprometer los 26. Los
26 se justifican sólo si el veredicto va a apoyarse en la forma de c(h); si el veredicto se apoya en
"c < θ en la cuenca", con la cuenca medida alcanza. Esa decisión se toma cuando esté el resultado de
G2/G3/G5, no ahora.

## 25. ¿Sigue calibrado el presupuesto de 200?

**No, y va en el veredicto.**

> **CORREGIDO el 24-ago-2026 (adenda 5, §27).** Acá decía "quedan **120** buscables", mezclando lo
> **asignado** con lo **restante**. Los 120 son la asignación declarada a familias buscables
> (G2 40 + G3 30 + G5 30 + G6 20); **restantes** son **118**, porque los 2 cartuchos ya gastados
> salieron de G2 — **no** se imputaron a G4, que conserva sus 40 intactos y todos de sólo-medición.

De los 200 declarados hay **120 asignados a familias buscables** y quedan **118 buscables sin gastar**:
G1 se fue con 40, G4 tiene 40 que sólo miden, y G2 ya gastó 2. Y la región factible resultó ser una
cuenca angosta en vez de un espacio de seis familias × ~33 configuraciones. **El presupuesto se
calibró para una geometría que ahora sabemos que no existe.**

**No se toca, y por la razón correcta:** el denominador es el presupuesto **declarado** (§1.4), y
bajarlo aflojaría la vara por un accidente de descubrimiento. Lo que cuesta estar sobre-presupuestado:

| K₂ | K_total | \|t\| exigido |
|---|---|---|
| **200 (declarado)** | **257** | **3.7260** |
| 120 (buscables de hoy) | 177 | 3.6299 |
| 60 | 117 | 3.5226 |

Sobre-presupuestar de 120 a 200 cuesta **2,62 % de rigor**, y se paga en la dirección
**conservadora**. Es exactamente el precio que §1.4 anticipó cobrar y no hay motivo para tocarlo.

**La fórmula, con sus denominadores exactos** (porque el número tiene que ser verificable, no
plausible):

> **CORREGIDO el 24-ago-2026 (adenda 6, §28).** La fórmula que estaba acá era
> `z(0.05/257)/z(0.05/177) − 1` y **no produce el número publicado**: leída como cuantil de una cola
> —que es como la lee cualquiera— da 3.547365/3.447896 − 1 = **2,8849 %**. Los z publicados son
> **bilaterales**, o sea `z_{1−α/(2K)}`, y sin el factor 2 la fórmula no es reconstruible. El número
> 2,6201 % es correcto; la fórmula escrita estaba mal. **El defecto: nadie ejecutó la fórmula
> publicada, sólo el código que la implementa.** Ahora hay un test que la ejecuta tal como está escrita
> (`tests/fase2/test_dia0.py` §19).

```
costo = z(α / (2·K_total_declarado)) / z(α / (2·K_total_alternativo)) − 1
      = z_{1−α/(2K_dec)} / z_{1−α/(2K_alt)} − 1        ← cuantil de UNA cola, bilateral al α
K_total = K₁ + K₂ = 57 + K₂            ← §1.1: el contador arrastra la Fase 1 y no se reinicia

z(0.05/(2·257)) = z(9.727626e-05) = 3.725987
z(0.05/(2·177)) = z(1.412429e-04) = 3.630853
costo = 3.725987 / 3.630853 − 1 = 2.6201 %
```

**Nota sobre una reproducción que da 3,77 %.** Ese valor sale de `z(0.05/200)/z(0.05/120) − 1 =
3.6623/3.5293 − 1`, que usa **K = K₂ sin sumar K₁ = 57**. Los dos cálculos son correctos por separado;
el que corresponde publicar es el de **K_total**, porque el denominador de la spec incluye las 57
configuraciones de la Fase 1 y ése es justamente el contador que no se reinicia (§1.1). Queda anotado
para que la diferencia sea reconstruible en vez de discutible.

**Lo que sí va escrito en el veredicto:** *el presupuesto se declaró antes de conocer la geometría del
problema, y la geometría resultó ser mucho más chica que el presupuesto.* Eso no es un error de la
spec — es la consecuencia inevitable de exigir que el número se declare antes. Un presupuesto
calibrado **después** de conocer la geometría no sería un presupuesto: sería un resultado disfrazado
de plan. El costo de hacerlo bien fue 2.6 % de rigor sobrante, pagado en la dirección segura.


---

# Adenda 5 — tres correcciones de una verificación externa

*Confirmadas por cálculo independiente y por el nuestro. Ninguna cambia el veredicto; las tres cambian
un número o una vara que se publica, que es motivo suficiente.*

## 26. La vara de un filtro es una FUNCIÓN, no una tabla

Los dos términos del requisito **dependen de la tenencia**:

```
A(h) = θ·√h        (potencia)      θ = 2.8016/√S_B = 0.068577
F(h) = f/√h        (fricción)      f = fricción/σ₁  = 0.048113
```

así que la vara de concentración también:

```
conc_min(φ, h) = [ θ·√h·√φ + (f/√h)·φ ] / [ φ · ( θ·√h + f/√h ) ]
```

| h ↓ / φ → | 0,75 | 0,50 | 0,25 | 0,10 |
|---|---|---|---|---|
| 0,3737 *(piso de la cuenca 5 %)* | 1,054× | **1,144×** | 1,348× | 1,752× |
| 0,7016 *(óptimo)* | 1,077× | **1,207×** | 1,500× | 2,081× |
| 1,0000 *(la tabla vieja)* | 1,091× | **1,243×** | 1,588× | 2,271× |
| 1,3171 *(techo de la cuenca 5 %)* | 1,101× | **1,270×** | 1,653× | 2,411× |
| 3,0000 | 1,125× | 1,336× | 1,811× | 2,752× |

**El fallo concreto de la tabla vieja:** un filtro con φ = 0,50 y residuo h ≈ 1,32 que declarara una
concentración de 1,26× **pasaba** la vara publicada (1,243×) y **no paga** la vara real (1,270×).

**Consecuencia declarada: las familias de filtro declaran TRES números antes de correr, no dos.**

| Número | Qué es |
|---|---|
| **φ** | fracción de operaciones que sobrevive al filtro |
| **ψ** | fracción de la ventaja total que sobrevive |
| **h_residuo** | **tenencia media de lo que sobrevive al filtro** |

La vara se evalúa **en h_residuo**. Y la regla que lo cierra: **si un filtro no puede declarar
h_residuo por adelantado, no puede declarar su hipótesis, y entonces no corre.** Cableado en
`preregister()` para G3 y G5; sin los tres números se niega, y con los tres se niega igual si la
concentración declarada no supera `conc_min(φ, h_residuo)`.

## 27. Las otras dos correcciones

**El costo de rigor.** El 2,62 % publicado es correcto pero se publicó sin su fórmula, que ahora está
en la §25 con los denominadores exactos. Una reproducción independiente da 3,77 % porque usa
`K = K₂` sin sumar `K₁ = 57`; ambos cálculos son correctos y el que corresponde es el de `K_total`,
porque **el contador arrastra la Fase 1 y no se reinicia** (§1.1). La diferencia queda anotada en la
§25 para que sea reconstruible.

**La cuenta de cartuchos.** Publiqué "120 buscables" mezclando **asignado** con **restante**. Lo
correcto: **120 asignados** a familias buscables, **118 restantes** — los 2 gastados salieron de G2,
**no** se imputaron a G4, que conserva sus 40 intactos y todos de sólo-medición. Corregido en la §25.


---

# Adenda 6 — la fórmula, el estimador y la distribución que no estaba declarada

*Tres correcciones de una verificación externa. La tercera cambia cuántos cartuchos vale la fase, así
que se resuelve antes de gastar el cartucho 4 y no después.*

## 28. La fórmula publicada no producía el número publicado

Está corregida en la §25, con el factor 2 explícito. El número (**2,6201 %**) siempre fue correcto; lo
que estaba mal era la fórmula escrita, que sin el factor 2 y leída como cuantil de una cola da
**2,8849 %**.

**El defecto de método, que importa más que el número:** publiqué esa fórmula *para que la diferencia
fuera reconstruible*, y como estaba escrita no lo era. **Nadie ejecutó la fórmula publicada — sólo el
código que la implementa.** Corregido con un test que **lee el documento y ejecuta la fórmula tal como
está escrita**, afirmando que iguala el número publicado a 4 decimales (`tests/fase2/test_dia0.py`
§19). Es la única forma de que un documento no vuelva a divergir de su implementación.

## 29. El estimador mezclaba dos estimadores

El punto publicado (−0.0461) era el **promedio simple no ponderado** de los dos mecanismos
(c = 0.022455), combinado con un **SE de DerSimonian-Laird**. Son dos estimadores distintos y el punto
y el τ tienen que salir del mismo.

**Se adopta el ponderado por inversa de varianza con pesos `1/(se_i² + τ²)`**, que es el que
corresponde al τ de DL:

| | Publicado (mezclado) | **Adoptado (DL ponderado)** |
|---|---|---|
| c | ~~0.022455~~ | **0.023700** |
| c − θ | ~~−0.046122~~ | **−0.044877** |
| SE | 0.027325 | 0.027327 |
| t | ~~−1.686~~ | **−1.6422** |

La conclusión no cambia —contiene el cero en ambos— pero el número publicado tiene que salir de un
solo estimador.

## 30. La distribución de referencia no estaba declarada, y vale tres cartuchos

Todos los p del bloque del estimador usaban la **normal**, tratando τ como conocido. **τ está estimado
a partir de m mecanismos: con m = 2, un grado de libertad.**

**¿Estaba declarada?** No. §1.2 declara `p_crudo = erfc(|t|/√2)` —la aproximación normal— pero **para
la barra de una candidata**, donde n ≥ 100 y t y z coinciden a 3 decimales. El bloque del estimador de
c es posterior y su distribución nunca se declaró.

**Se declara ahora, antes del cartucho 4: t con df = m − 1.** Motivo: τ está estimado y tratarlo como
conocido es anticonservador; la normal sólo estaría justificada con m grande.

**Lo que cambia:**

| | Bajo normal | **Bajo t(df = m−1)** |
|---|---|---|
| p del estado actual (m=2, t=−1.6422) | 0.1005 | **0.3482** |
| mecanismos para resolver al 95 % | 3 | **6** |

| m | df | SE | t | p normal | **p t(df)** |
|---|---|---|---|---|---|
| 2 | 1 | 0.027355 | 1.6405 | 0.1009 | **0.3485** |
| 3 | 2 | 0.022335 | 2.0092 | 0.0445 | 0.1823 |
| 4 | 3 | 0.019343 | 2.3201 | 0.0203 | 0.1031 |
| 5 | 4 | 0.017301 | 2.5939 | 0.0095 | 0.0604 |
| **6** | **5** | **0.015793** | **2.8415** | 0.0045 | **0.0362** |

**Y el modelo también se declara**, porque la §29 obligaba a elegir uno: rige **efectos aleatorios
(DerSimonian-Laird)**. Argumento: mecanismos distintos son fenómenos distintos, y suponer un c común a
todos es una asunción fuerte que no tenemos cómo sostener — efectos fijos sólo regiría si pudiéramos
afirmar que c es una constante del generador, y eso es justamente lo que estamos midiendo. **Con m = 1
el modelo no es computable y se reporta así, sin caer de vuelta a efectos fijos para tener un número.**

## 31. El "resuelve al 95 %" tenía un supuesto no declarado

**El supuesto:** que cada mecanismo nuevo caiga **en la media actual o por debajo**. Si cae por encima,
la brecha se angosta y no resuelve nada.

**Escrito como rango, que es lo que corresponde.** Para m = 6 (df = 5), con t crítico 2,5706 y
SE = 0.015793, hace falta |media − θ| ≥ 0.040598, o sea **media ≤ 0.027978**. Con los dos actuales en
0.023700, **los cuatro nuevos deben promediar c ≤ 0.0301**.

Los dos medidos promedian 0.0225, así que el supuesto es **plausible pero no está garantizado**. Si
los nuevos mecanismos vinieran sistemáticamente por encima de 0.0301, la fase no se resolvería con
seis: se resolvería en la otra dirección, que es un resultado igual de bueno y hoy no lo sabemos.

---

# Adenda 7 — procedencia de la etiqueta, n efectivo, y dos números que no reproducían

## 32. La etiqueta de mecanismo NO era post-hoc: caso (b), resuelto por procedencia

El contador (`cartuchos_por_mecanismo`) leía sólo el campo `mecanismo` y mandaba los cartuchos 1 y 2 a
un bucket heredado, mientras el estimador los agrupaba como *liquidez*. **El código y el análisis
discrepaban sobre el hecho que decide la fase.**

Resuelto **por procedencia, buscando en el ledger**, no por conveniencia. Los dos declararon su
mecanismo **en prosa, dentro de `hypothesis`, antes de correr** — el campo `mecanismo` todavía no
existía:

| Línea | Hash del pre-registro | Cita textual |
|---|---|---|
| **62** | `d38a1e04c6bfc0f8` | *"quien compra **provee liquidez a vendedores forzados** (límites de riesgo, llamadas de margen, rescates) y cobra por absorber ese flujo"* |
| **74** | `1871af782763cf6b` | *"**Mismo mecanismo que el cartucho 1**… Quien compra **provee liquidez a vendedores forzados** y cobra por absorber ese flujo"* |

Y el cartucho 3 (línea 89) declaró **antes de correr**: *"Mecanismo **DISTINTO** al de los cartuchos 1
y 2: no provisión de liquidez a vendedores forzados sino difusión gradual de información"*. **La
partición en dos mecanismos se declaró antes, no después de ver los resultados.**

**Migración `MIGRACION_ETIQUETA` (`968e2bdbd5d6652e`, `cd2266dae7f3924d`), que exige la cita textual
como prueba:** si la cita no aparece literal en el `hypothesis`, la migración se **rechaza** y la
etiqueta habría que declararla como defecto post-hoc. Las entradas originales no se editan.

**Y la unificación ENDURECE:** *liquidez* pasa a tener **3 de 4 cartuchos = 75 %**, por encima del tope
de concentración del 40 % (§2b) — así que **desde el cartucho 5 ese mecanismo queda bloqueado**.
`CAMBIO_DE_REGLAS 2b5307697e220f36`.

## 33. Las configs de un mecanismo NO son independientes: medido, y es grave

| | Solapamiento con las entradas del cartucho 4 |
|---|---|
| vs cartucho 1 (k=3, h=3) | 142 de 1.221 = 11,6 % |
| **vs cartucho 2 (k=1, h=1)** | **1.069 de 1.221 = 87,6 %** |
| vs 1 ∪ 2 | **87,6 %** |

Y en las sesiones donde el cartucho 2 y el 4 operan a la vez, la **correlación de P&L es +1.0000**: no
son parecidas, **son literalmente las mismas operaciones**.

**Regla declarada (§3.10):** dentro de un mecanismo, una operación se cuenta **una sola vez**.
Identidad = *(fecha de entrada, tenencia)*. La config **cronológicamente anterior** se queda con la
operación y las posteriores aportan sólo las nuevas — el orden lo fija el ledger, no los resultados.
`CAMBIO_DE_REGLAS b188649687532bcc`, **ENDURECE**.

**Y el hallazgo dentro del hallazgo:** las **152 operaciones genuinamente nuevas** del cartucho 4 dan
**c = −0.0746**. El +0.0395 que reportó era casi todo **heredado de las 1.069 duplicadas del cartucho
2**.

> **CORREGIDO el 24-ago-2026 (adenda 8, §37).** Acá seguía *"el cartucho 4 no confirmó el mecanismo: lo
> que agregó de nuevo apunta al otro lado"*. **Esa frase no está sostenida por los datos** y se retira:
> el −0.0746 se publicó sin intervalo, y con intervalo (± 0.0812) **cubre el cero y cubre el propio c
> de liquidez**. Lo correcto es *"el residuo no es distinguible ni del cero ni del propio mecanismo"*.
> El hallazgo del 87,6 % se sostiene solo y no necesitaba que el residuo fuera negativo.

| Estimador | Ingenuo (publicado) | **n efectivo (corregido)** |
|---|---|---|
| liquidez | +0.04617 ± 0.01699 | **+0.04190 ± 0.02044** |
| difusión | −0.00490 ± 0.02413 | −0.00490 ± 0.02413 |
| c global | +0.023510 ± 0.025374 | **+0.020260 ± 0.023336** |
| τ | 0.029474 | 0.024399 |
| t (df=1) | −1.7761 | **−2.0705** |
| p | 0.3265 | **0.2864** |

El SE publicado **subestimaba en un factor 1.20** porque contaba 1.069 operaciones dos veces.

## 34. La elección del umbral no accedió al P&L: ahora está garantizado, no supuesto

`m = 0.25` se eligió contando frecuencias. Eso es defendible porque el conteo es propiedad de la regla
y no de los retornos — pero **eso tenía que estar garantizado**. Test nuevo: se llama cinco veces a
`count_trades_only` con una estrategia cuyo P&L es **completamente distinto en cada llamada** y se
afirma que **el conteo no cambia**, que la estrategia se llamó las cinco veces (no hubo caché), que el
retorno es `int`, y que la salida de la criba **no expone ningún campo de P&L**.

Queda escrito: **la selección del umbral usó exclusivamente conteos de operaciones.**

## 35. Los dos números que no reproducían

**(a)** *"los dos medidos promedian 0.0225"* era un número **viejo**, anterior al cartucho 4. Con n
efectivo hay dos candidatos y hay que nombrar cuál:

- **media RE ponderada = 0.020257** — la que usa el estimador;
- **promedio simple = 0.018500** — la que corresponde a la **proyección**, porque ésta supone
  mecanismos **equiponderados**.

Se publica el **promedio simple**, nombrado como tal.

**(b)** Las cotas para m = 6, con τ² = 5.950948e-04 y v̄ = 5.000252e-04:

```
SE(m) = √((τ² + v̄)/m)          SE(6) = 0.013510      t_crit(df=5) = 2.5706
|media − θ| ≥ 2.5706 × 0.013510 = 0.034729

COTA A — la media de LOS SEIS         ≤ θ − 0.034729 = 0.033848
COTA B — el promedio de LOS 4 NUEVOS  ≤ (6·0.033848 − 2·0.018500)/4 = 0.041522
```

Lo publicado (**0.0301**) estaba **rotulado como cota B** y su valor cae cerca de la **cota A**. **Dos
errores, y los dos en contra nuestra**: el rótulo cambiado y la cota subestimada en un 27 %.

---

# Adenda 8 — la matriz completa, el intervalo que faltaba, y una premisa que no se sostiene

## 36. La matriz de los seis pares (§3.10, identidad = fecha de entrada + tenencia)

Medir un solo par era insuficiente y la matriz completa muestra por qué.

| Par | Operaciones idénticas | % de A | % de B | Fechas de entrada compartidas | % de A | **Salidas compartidas** | ρ (P&L) |
|---|---|---|---|---|---|---|---|
| **c1–c2** | **0** | 0,0 % | 0,0 % | **244** | **100,0 %** | 109 | **+0,6529** |
| c1–c3 | 0 | 0,0 % | 0,0 % | 0 | 0,0 % | 64 | +0,7036 |
| c1–c4 | 0 | 0,0 % | 0,0 % | 142 | 58,2 % | 79 | +0,4727 |
| c2–c3 | 0 | 0,0 % | 0,0 % | 0 | 0,0 % | 0 | — |
| **c2–c4** | **1.069** | 70,8 % | **87,6 %** | 1.069 | 70,8 % | 1.069 | **+1,0000** |
| c3–c4 | 0 | 0,0 % | 0,0 % | 0 | 0,0 % | 0 | — |

**Lo que la matriz muestra y el par no mostraba: el disparador de c1 es un SUBCONJUNTO ESTRICTO del de
c2.** Las 244 fechas de entrada de c1 son, el **100 %**, fechas de entrada de c2 — obvio en retrospectiva,
porque tres cierres consecutivos a la baja implican uno. Bajo §3.10 no son la misma operación (tenencias
3 y 1, P&L distinto), y sólo 109 sesiones tienen las dos operando a la vez, con ρ = +0,65.

**Pero eso obliga a publicar dos cotas en vez de un número**, porque "2,124 configs efectivas" es una
**cota superior** de la independencia de liquidez:

| Cota | Supuesto sobre c1 | liquidez | c global | τ | t (df=1) | p |
|---|---|---|---|---|---|---|
| **CONSERVADORA** *(ex "optimista")* | c1 aporta información propia | +0,04190 ± 0,02044 | **+0,020262 ± 0,023329** | 0,024385 | −2,0710 | **0,2864** |
| **GENEROSA** *(ex "conservadora")* | c1 totalmente dependiente de c2 | +0,03315 ± 0,02453 | **+0,013876 ± 0,019020** | 0,011475 | −2,8759 | **0,2130** |

> **RÓTULOS CORREGIDOS el 24-ago-2026 (adenda 9, §43):** estaban puestos por el supuesto sobre los
> datos y empujaban hacia la confirmación — la que llamaba "conservadora" da **p menor** y exige
> **menos mecanismos**. Van por su **efecto sobre el veredicto**: la que hace más difícil rechazar es
> la conservadora.

**Las dos se publican; ninguna se promedia y ninguna se elige.** El veredicto no cambia: bajo t(df = 1)
el intervalo contiene al cero en las dos.

Y **c3 no comparte ninguna operación ni ninguna fecha con c1 ni con c2**: sus disparadores son
complementarios.

> **CORREGIDO el 24-ago-2026 (adenda 9, §42).** Acá seguía *"la partición en dos mecanismos se
> sostiene"*. **La conclusión no se sigue de esa evidencia:** cero operaciones compartidas es
> **necesario, no suficiente**. Lo que el estimador necesita es **independencia estadística**, y c1 y c3
> correlacionan +0,7036 en las 64 sesiones donde ambos cierran (+0,070 entre los estimadores). La
> partición se sostiene **en cuanto a operaciones y fechas**, y todavía **no** en cuanto a independencia
> estadística.

## 37. El c del residuo no tenía intervalo, y con intervalo la afirmación se cae

Publiqué que las 152 operaciones nuevas del cartucho 4 daban **c = −0,0746** y escribí que *"lo que
agregó de nuevo apunta al otro lado"*. Con 152 operaciones contra 1.221, el error escala ×2,83:

```
c(152 nuevas) = −0,0746 ± 0,0812
IC 90 %: [−0,2082 , +0,0590]        IC 95 %: [−0,2338 , +0,0846]
```

**El intervalo cubre el cero (sí) y cubre el propio c de liquidez, +0,0419 (sí).**

> **CORREGIDO:** la frase *"lo que agregó de nuevo apunta al otro lado"* **no está sostenida por los
> datos** y se retira. Lo correcto: **el residuo del cartucho 4 no es distinguible ni del cero ni del
> propio mecanismo.**

El hallazgo del 87,6 % **se sostiene solo** y no necesitaba que el residuo fuera negativo.

## 38. Qué contabilidad rige el tope de concentración: la NOMINAL (§2d)

El mismo objeto se contaba de dos maneras: para el estimador el cartucho 4 vale **0,1245 configs**
(n efectivo); para el tope vale **1 config entera**.

| Contabilidad | liquidez / total | ¿supera el 40 %? |
|---|---|---|
| Nominal | 3 / 4 = **75,0 %** | sí |
| Efectiva | 2,124 / 3,124 = **68,0 %** | sí |

**El bloqueo se sostiene con cualquiera de las dos y la decisión operativa no cambia** — pero cuál rige
es una regla. **Rige la NOMINAL**, y el motivo no es comodidad: el n efectivo se calcula **después** de
correr, comparando operaciones, así que un tope que dependiera de él se evaluaría con información que
no existe al pre-registrar — y sería **manipulable**, porque bastaría elegir configs muy solapadas para
que "cuenten menos" y esquivar el tope. La nominal está fija en el momento del pre-registro y no se
puede fabricar. El n efectivo rige el **estimador**, donde su propósito es el opuesto: impedir que la
duplicación se haga pasar por evidencia nueva.

## 39. La premisa del "bug del contador costó un cartucho" no se sostiene

La afirmación era: con el tope en 40 %, al pre-registrar el cartucho 4 liquidez ya iba 2 de 3 = 66,7 %
y el tope debería haberlo rechazado; no disparó porque el bucket heredado escondía la cuenta.

**Verificado contra el ledger, y es falso:**

- al pre-registrar el cartucho 4 había **3 cartuchos gastados**;
- `CONCENTRACION_DESDE = 5`, declarado en §2b — *"a partir del quinto, para no trabar el arranque"*;
- el tope **sólo se evalúa si `gastado ≥ 5`**, y 3 ≥ 5 es falso.

**El tope no habría disparado ni con las etiquetas correctas.** El defecto del contador era real y está
corregido (§32), pero **no costó ese cartucho**: lo que lo dejó pasar fue la ventana de arranque
declarada, no el bucket heredado.

Y sobre *"un control que sólo mira hacia atrás no es un control"*: de acuerdo, y **ya mira hacia
adelante**. El tope se evalúa **dentro de `preregister()`, antes de escribir la entrada** — verificado
por posición en el código: el chequeo está en el carácter 4.867 y el primer `_append` en el 12.037. Un
pre-registro rechazado por concentración **no gasta cartucho**.

## 40. Las dos cotas de m = 6, explícitas y con su fórmula

Para que la próxima verificación no tenga que derivarlas. Con τ² = 5,950948e-04, v̄ = 5,000252e-04:

```
SE(m) = √((τ² + v̄)/m)                SE(6) = 0,013510
t_crit(df = 5, α = 0,05) = 2,5706     |media − θ| ≥ 2,5706 × 0,013510 = 0,034729

COTA A — promedio de LOS SEIS mecanismos   ≤ θ − 0,034729 = **0,033848**
COTA B — promedio de LOS CUATRO NUEVOS     ≤ (6 × 0,033848 − 2 × 0,018500)/4 = **0,041523**
```

El **0,0301** que publiqué quedaba **11,1 % por debajo de A** y **27,5 % por debajo de B**, y estaba
rotulado como B. El 27 % que reporté es correcto **contra B**.

---

# Adenda 9 — la asimetría verificada, el supuesto que faltaba, y los rótulos dados vuelta

## 41. La asimetría c1–c3 = 64 contra c2–c3 = 0: **no es un bug**, y revela qué medía la columna

Verificado como se pidió. Lo primero que aparece es **qué medía realmente mi columna "n co-op"**: en el
script de la matriz la serie por sesión se llena en la **fecha de SALIDA**, así que *n co-op* = sesiones
donde ambas configs **cierran** el mismo día. **No es solapamiento de exposición**, que es lo que el
rótulo sugería.

| Par | Entradas compartidas | Salidas compartidas |
|---|---|---|
| c1–c3 | **0** | 64 |
| c2–c3 | **0** | 0 |
| c1–c2 | 244 | 109 |

Y la descomposición pedida, de las 64 salidas compartidas c1–c3:

```
respecto de la entrada de c1: {D+3: 64}    ← exactamente su tenencia
respecto de la entrada de c3: {D+1: 64}    ← exactamente su tenencia
coincidencias en D (mismo día de entrada): 0 y 0
entradas compartidas c1–c3: 0
```

**Ninguna cae en D y los desplazamientos son exactamente los de la tenencia.** La asimetría es
consecuencia de que c1 sigue abierta en D+1 y D+2 cuando c2 ya cerró; **no hay error de indexado**.
La columna queda renombrada **"salidas compartidas"** en la §36 para que no vuelva a leerse como
exposición.

## 42. El modelo supone independencia entre mecanismos, y el supuesto se viola

La frase publicada era: *"c3 no comparte ninguna operación ni fecha con c1 ni c2 — la partición en dos
mecanismos se sostiene"*.

> **CORREGIDO.** La conclusión no se sigue de esa evidencia: **cero operaciones compartidas es
> necesario, no suficiente.** Lo que el estimador necesita es **independencia estadística**, y ésa es
> otra cosa.

**Declarado ahora (§3.8, punto 3):** DerSimonian-Laird supone que los m estimadores de mecanismo son
**sorteos independientes**. Medido, c1 y c3 correlacionan **+0,7036** en las 64 sesiones donde ambos
cierran. Pero eso **no es** la correlación entre los estimadores; la inducida entre las medias es:

```
Corr(media₁, media₃) ≈ ρ_par · n_solap / √(n₁·n₃) = 0,7036 · 64/√(244·1718) = +0,070
```

**Chico, pero no cero: el supuesto se viola levemente.** Se declara como **limitación conocida** en vez
de darse por cumplido, y **el veredicto tiene que publicarla**. Dirección del sesgo, dicha explícita:
una correlación positiva entre estimadores hace que **τ se subestime**, o sea que el SE de la media
salga más chico de lo debido y **la meta de mecanismos sea optimista**.

**Redacción correcta:** *la partición se sostiene en cuanto a operaciones y fechas —c3 no comparte
ninguna con c1 ni c2— y todavía **no** se sostiene en cuanto a independencia estadística, que es lo que
el estimador necesita.*

## 43. Los rótulos estaban dados vuelta y empujaban hacia la confirmación

| Supuesto sobre los datos | c global | τ | p | Meta de mecanismos |
|---|---|---|---|---|
| c1 aporta información propia | +0,020262 ± 0,023329 | 0,02438 | **0,2864** | **5** |
| c1 totalmente dependiente de c2 | +0,013874 ± 0,019018 | 0,01147 | **0,2130** | **4** |

La que yo llamaba *"conservadora"* —colapsar c1 dentro de c2— **achica τ² por un factor de 4,5**, y eso
achica el SE más de lo que achica la brecha. Es conservadora **sobre la independencia** y **generosa
sobre la conclusión**: da p menor y exige menos mecanismos. Hoy no cambia nada porque el intervalo
cubre el cero en las dos, **pero el día que diverjan el rótulo empuja hacia la que confirma**.

> **Renombradas por su efecto sobre el veredicto, no por su supuesto sobre los datos.** La que hace
> **más difícil rechazar** es la conservadora.

| Rótulo nuevo | Supuesto | p | Meta |
|---|---|---|---|
| **CONSERVADORA** | c1 aporta información propia | 0,2864 | **5** |
| **GENEROSA** | c1 totalmente dependiente de c2 | 0,2130 | **4** |

Con los números de hoy, **la que llamaba "optimista" pasa a ser la CONSERVADORA y viceversa**.

## 44. La meta de mecanismos estaba vieja, y ahora sale del código

Los **6** se fijaron en el estado del cartucho 3, y desde entonces el estimador cambió dos veces
(n efectivo, y las dos cotas). Recomputada con el estimador vigente:

| Cota | SE(meta) | t | t_crit | **Meta** |
|---|---|---|---|---|
| **CONSERVADORA** | 0,014796 | 3,2653 | 2,7764 (df=4) | **5** |
| **GENEROSA** | 0,013449 | 4,0673 | 3,1824 (df=3) | **4** |

**Y atada con un test**, porque es el mismo defecto de método que el de la fórmula sin el factor 2:
**un número publicado que dejó de derivarse de lo que lo produce.** `mechanism_target()` calcula la
meta desde el estimador vigente, y el test afirma que la meta publicada en este documento coincide con
la derivada, que es mínima (con un mecanismo menos no alcanza) y que `SE(meta)` reproduce su fórmula.

*Supuesto explícito de la proyección, que no cambia:* cada mecanismo nuevo cae **en la media actual** y
τ se mantiene. Si cayeran por encima, la brecha se angosta y la meta sube.
