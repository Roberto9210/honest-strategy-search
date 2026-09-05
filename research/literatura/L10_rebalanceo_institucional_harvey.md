# L10 — Cuando las acciones quedan sobreponderadas, los fondos institucionales tienen que venderlas

**VENTANA L. Ficha de literatura. NO MEDIDA. No gasta cartucho, K sigue en 261.**

**RECUPERADA.** El filtro nocturno viejo la había matado. Con el filtro de ventana de exposición
(`FILTROS.md`) sobrevive, y pasa a ser **la candidata de mayor magnitud declarada sobre futuros ES
de todo el inventario**.

---

## 1. Cita completa

Harvey, Campbell R.; Mazzoleni, Michele G.; Melone, Alessandro (2025). **"The Unintended Consequences
of Rebalancing."** NBER Working Paper 33554, marzo de 2025.

- NBER: https://www.nber.org/papers/w33554
- PDF: https://www.nber.org/system/files/working_papers/w33554/revisions/w33554.rev0.pdf
- Versión AFA: https://afajof.org/management/viewp.php?n=144452

Harvey es de Duke y del NBER, Melone de Ohio State, Mazzoleni de Capital Group.

## 2. El efecto, en una frase

Los fondos institucionales tienen que mantener una proporción fija entre acciones y bonos, así que
cuando las acciones suben más que los bonos **están obligados a vender acciones**, y como lo hacen
casi todos a fin de mes y casi todos al mismo tiempo, el mercado baja de forma predecible.

## 3. Instrumento y período de la muestra original

- **Futuros del S&P 500 y futuros del bono del tesoro a 10 años**, retornos **diarios**.
- **1997 → 2023**, 27 años.
- Validan además con datos de posiciones de la Comisión de Comercio de Futuros de Materias Primas.

**Es, junto con L01, una de las dos únicas candidatas cuya muestra original ES el instrumento que
Roberto opera.** Y a diferencia de L01, acá el ES no es uno de sesenta contratos: es la mitad del
objeto de estudio.

## 4. Magnitud declarada

Construyen dos señales de desvío de la cartera respecto del objetivo:

- **Umbral**: dispara cuando los pesos se apartan más de una distancia predefinida. Captura el
  rebalanceo rápido intramensual.
- **Calendario**: captura el rebalanceo programado de fin de mes.

| señal | efecto sobre acciones al día siguiente | efecto sobre bonos |
|---|---|---|
| Umbral | **−16 puntos básicos** | +4 pb |
| **Calendario** | **−17 puntos básicos** | +2 pb |

**Es por un desvío estándar de la señal**, no incondicional. Con un desvío típico realizado menor,
el movimiento esperado baja proporcionalmente.

Y agregan que **las presiones de rebalanceo se revierten casi por completo en dos semanas**,
consistente con que el rebalanceo es un subproducto de mandatos institucionales que no transporta
información sobre fundamentos. **Esa reversión es un test de mecanismo separable, y está en
[M01](M01_mecanismo_reversion.md).**

Los autores dicen explícitamente que **sus resultados son conservadores**: sin las operaciones
diarias reales de todos los rebalanceadores, la señal es sólo un sustituto de un rebalanceador
representativo, así que el efecto documentado es probablemente **una cota inferior**.

Costo estimado del rebalanceo para los inversores: **$16 mil millones al año**, unos $200 por hogar
estadounidense. Y dicen sin rodeos que la predictibilidad **permite a ciertos participantes ganar
adelantándose a las órdenes de los fondos grandes**.

### Traducción a dólares por evento por contrato ES

17 puntos básicos, con 1 pb = $13 en 2016-2019 y $32 en 2026:

| | ES 2016-2019 | ES 2026 |
|---|---|---|
| bruto | **$221** | $544 |
| neto de ≈ $17 de ida y vuelta | **$204** | $527 |

**Es la magnitud por operación más grande de todo el inventario**, unas **doce veces** la de L01.

## 5. Antes o después de costos

**Antes.** No proponen estrategia con costos: el paper es sobre el costo que el rebalanceo impone a
los inversores, no sobre cómo explotarlo. Pero 17 pb sobre ES son $221 contra un costo de ida y
vuelta de ≈ $17: **el costo se lleva el 8 % del efecto bruto.** Es la única candidata donde el costo
no es una preocupación de primer orden.

## 6. Mecanismo declarado

**Obligación de mandato, no comportamiento.** Los fondos de pensión, soberanos y mutuos tienen
mandatos ajustados y objetivos de asignación cercanos al clásico 60/40. Cuando el mercado mueve los
pesos, **tienen que operar para volver al objetivo**, y no porque quieran.

La concentración a fin de mes tiene tres causas nombradas: los fondos de pensión maduros venden
activos a fin de mes para juntar caja y pagar beneficios; las reglas de reporte de cartera y los
mecanismos de coordinación empujan a esas fechas; y varias series de referencia se rebalancean
trimestralmente. Citan a Etula, Rinne, Suominen y Vaittinen (2020) para el ciclo de caja mensual.

**Evidencia de que el mecanismo es el declarado y no otro:** la predictibilidad de la señal de
calendario es **fuerte a fin de mes y ausente fuera de esos días**, y aumenta hacia el fin de
trimestre. Un patrón estadístico sin mecanismo no tendría por qué respetar el calendario contable.

Y los resultados son robustos a controles por momento, reversiones, actividad macroeconómica e
indicadores de sentimiento.

## 7. CLASIFICACIÓN

**DETERMINISTA en la fecha y en el signo, ESTADÍSTICA en la magnitud.**

- **Fecha**: fin de mes, y con más fuerza fin de trimestre. Escrita.
- **Signo**: el del desvío acumulado de acciones contra bonos, **calculable con datos públicos
  antes de entrar**.
- **Magnitud**: proporcional al desvío, con coeficiente publicado, pero con dispersión.

Es, junto con **L08**, la única del inventario donde fecha y signo se saben antes de entrar. Y a
diferencia de L08, **la magnitud alcanza**.

## 8. Estado de replicación

**Es lo más débil de esta ficha y hay que decirlo primero: es un documento de trabajo de 2025 sin
publicar en revista, y no tiene replicación independiente.**

Lo que sí tiene:
- **27 años de muestra**, 1997-2023, que es más larga que la de casi todo el inventario.
- **Validación en cantidades** con datos de posiciones de la Comisión de Comercio de Futuros, o sea
  que verifican que el flujo existe y no sólo que el precio se mueve.
- **Antecedente independiente del mismo mecanismo**: Etula et al., *RFS* 2020, sobre el ciclo mensual
  de caja institucional, que está en `DESCARTADAS.md`.
- Se apoya en, y a la vez corrige, a Parker, Schoar y Sun (2023), que encuentran que el rebalanceo de
  fondos de fecha objetivo afecta el corte transversal pero que su efecto agregado es despreciable
  dado su tamaño actual. Harvey et al. argumentan que la mayoría de los inversores tiene mandatos
  más ajustados.

**Advertencia de decaimiento, y es específica:** los propios autores dicen que la predictibilidad
**permite adelantarse a las órdenes**. Un paper del NBER firmado por Campbell Harvey que dice
públicamente cómo adelantarse a un flujo de $16 mil millones al año **es exactamente el tipo de
publicación que McLean y Pontiff (2016) miden que reduce el retorno un 58 %**. Publicado en 2025;
los datos del proyecto terminan en 2019, o sea **seis años antes**. Para esta candidata, 2016-2019 es
período pre-publicación, que es lo bueno; y significa que un resultado positivo ahí **no dice nada
sobre 2026**, que es lo malo.

## 8-bis. Quiénes son los autores, que corta para los dos lados

**Mazzoleni trabaja en Capital Group**, una de las gestoras más grandes del mundo. Harvey es de Duke
y del NBER, Melone de Ohio State. El paper aclara que no está financiado y que los autores no
declaran conflictos, y que las opiniones no reflejan las de Capital Group.

**Es información mejor y es un conflicto, las dos cosas, y no resuelvo cuál pesa más.**

- **A favor:** las dos señales del paper —umbral y calendario— salen de **las políticas de inversión
  declaradas de las instituciones**, no de un barrido sobre datos. Saber cómo rebalancean de verdad
  los fondos de pensión y los mutuos es conocimiento de adentro.
- **En contra:** Capital Group es **uno de los rebalanceadores** cuyo flujo el paper describe como
  predecible y explotable. Y el paper dice explícitamente que la predictibilidad permite adelantarse
  a las órdenes de los fondos grandes.

**Es el mismo patrón en tres de las once fichas** —L01, L08 y ésta— **y las tres son de efectos de
flujo de calendario. Que las tres vengan de gente que ve el flujo no es casualidad.**

## 9. Cuántas variantes probaron los autores

Contable de lo publicado: **2 señales** (umbral y calendario) × **2 activos** (acciones y bonos) ×
varios horizontes (día siguiente, dos semanas para la reversión) × **otros esquemas de ponderación**
que declaran haber considerado (nota 2) × cortes estacionales por fin de mes, por meses dentro del
trimestre, y por trimestre × controles por momento, reversiones, macro y sentimiento.

**Para el juez: `variantes_probadas` = 30 como mínimo.** Con los esquemas de ponderación alternativos
que mencionan sin tabular, 100 es la lectura conservadora.

**Atenuante real:** la señal **no se ajusta a los datos**. El umbral y el calendario salen de las
políticas de inversión declaradas de las instituciones, no de un barrido. Una señal derivada de un
reglamento externo tiene mucha menos libertad que una calibrada.

## 10. Qué haría falta para probarla acá

**Datos de precio: NINGUNO NUEVO para la parte de acciones.** ES 1-min 2016-2019.

**Dato que falta y es gratis:** una serie diaria de retornos de bonos para construir el desvío
acciones contra bonos. El paper usa futuros del bono a 10 años. **Alternativa sin comprar nada:** un
índice de bonos diario público. Es una decisión de construcción que **se declara antes de correr**.

### La aritmética, antes de medir

| | |
|---|---|
| ventana de exposición | ≈ 23 h, cierre a cierre |
| ¿stop posible dentro de E? | **sí** |
| instrumento | ES o **MES** |
| A neto por evento, ES 2016-2019 | **$204** |
| eventos por año | 12 con la señal de calendario, hasta 24 sumando la de umbral |
| eventos requeridos por año (F5, 10 variantes) | **25** |
| **falta** | **2,1×**, o **1,0× si son 24 eventos** |

**Es la única candidata del inventario que llega a rozar la vara con los datos que hay.** Con la
señal de calendario sola no alcanza; sumando la de umbral queda **justo en la línea**, y "justo en la
línea" no es un aprobado: es donde una decisión de construcción tomada mirando el resultado decide el
veredicto. **Por eso la construcción se declara antes.**

### Sobre el riesgo, que es lo que la había matado

La posición se sostiene de un cierre al siguiente. Con **1 ES** eso es una noche contra 40 puntos de
drawdown, y la Compuerta 1 midió que una noche sola se lleva el drawdown **8,38 % de las veces por el
lado largo**. Con **1 MES** son 400 puntos, y el peor movimiento nocturno medido en 955 noches fue de
118,75 puntos.

**En MES la ventaja baja a $22 por evento y el riesgo de ruina por noche prácticamente desaparece.**
Si ese intercambio conviene lo decide el costo por punto del MES, que está medido dentro del juez y
que no tengo. **Es una consulta, no un estudio.**

### Y una advertencia contra el atajo

**Restringirla a 9:30–16:00 para hacerla intradiaria sería cambiar la regla del paper.** El efecto
publicado es el retorno del día siguiente de cierre a cierre. Una regla que modificamos nosotros para
que entre en nuestras restricciones **vuelve a ser una hipótesis de nuestro generador**, que es lo que
esta ventana existe para evitar. Si alguien la mide así, eso hay que declararlo y `variantes_probadas`
tiene que reflejarlo.
