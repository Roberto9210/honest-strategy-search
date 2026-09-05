# L08 — El último día del mes, a las 16:00 de Londres, los que cubren carteras de acciones mueven la moneda

**VENTANA L. Ficha de literatura. NO MEDIDA. No gasta cartucho, K sigue en 261.**

---

## 1. Cita completa

Melvin, Michael; Prins, John (2015). **"Equity hedging and exchange rates at the London 4 p.m.
fix."** *Journal of Financial Markets*, vol. 22, pp. 50–72.

Ambos autores estaban en **BlackRock** al escribirlo. Presentado en el Tercer Taller de Microestructura
Cambiaria del Banco Central Europeo, diciembre de 2013.

- Editorial: https://www.sciencedirect.com/science/article/abs/pii/S1386418114000779
- RePEc: https://ideas.repec.org/a/eee/finmar/v22y2015icp50-72.html
- Borrador BCE: https://www.ecb.europa.eu/events/pdf/conferences/131216/Third_FX_Workshop_MELVIN_PRINS_Equity%20hedging%20and%20exchange%20rates%20Nov%202013.pdf

**Evidencia complementaria:** Evans, Martin D. D. (2018). "Forex trading and the WMR Fix."
*Journal of Banking & Finance*. https://www.sciencedirect.com/science/article/abs/pii/S0378426617302327

## 2. El efecto, en una frase

Los gestores de carteras internacionales de acciones ajustan su cobertura cambiaria **una sola vez
por mes, en el fixing de las 16:00 de Londres del último día hábil**, y el monto que tienen que
operar se calcula del retorno de la bolsa de ese país durante el mes — así que si la bolsa de un
país subió, su moneda tiende a **caer** en la hora previa a ese fixing.

## 3. Instrumento y período de la muestra original

- **Diez monedas** contra el dólar, con retornos demediados en el corte transversal para que el
  dólar sea una moneda más.
- **28 de abril de 2004 → 31 de diciembre de 2012**, o sea **8,66 años ≈ 104 fines de mes**.
- Cotizaciones muestreadas de un minuto antes a un minuto después de las 16:00, y ofertas y demandas
  cada segundo de 30 segundos antes a 30 segundos después.
- Instrumento operable para Roberto: futuros de moneda del CME (**6E**, **6J**, **6B**, **6A**).

## 4. Magnitud declarada

La regresión del panel, con el retorno cambiario de la hora previa al fixing de fin de mes contra el
retorno bursátil del mes:

```
r(cambiario, hora previa al fix)  =  0,0142 · r(bursátil del mes)      R² = 0,03,  F = 25,52,  p < 0,001
```

**Una apreciación bursátil del 10 % en el mes predice 14 puntos básicos de depreciación de esa moneda
en la hora previa al fixing de fin de mes.**

Los propios autores dicen que **parece un efecto bastante chico**, y dan dos argumentos para que no
se descarte: el retorno bursátil ocurre a lo largo de un mes y el cambiario en **una hora**, así que
puesto en la misma escala de tiempo (×24 horas ×21 días hábiles) el movimiento cambiario es **seis
veces mayor**; y como el papel de los coberturistas es conocido en el mercado, parte del movimiento
debería estar ya incorporado antes.

**Y reportan que la depreciación se revierte al menos parcialmente el día siguiente al fixing.**

### Traducción a dólares por evento por contrato

Un movimiento bursátil mensual típico es de **3 a 4 %**, no de 10 %. Con 3,5 %:
`0,0142 × 3,5 % = 5,0 puntos básicos`.

| contrato | nocional aprox. | 5 pb |
|---|---|---|
| 6E (125.000 €) | ≈ $140.000 | **≈ $70** |
| 6J (12,5 M ¥) | ≈ $115.000 | ≈ $58 |

**Por evento supera el piso de detectabilidad por operación** ($29 a $58, `PISO_Y_CONVERSION.md`).
El problema, como en L03, **no es la magnitud: es que hay doce eventos por año.**

## 5. Antes o después de costos

**Antes, y el paper no propone estrategia ni calcula costos.** Es un test de una hipótesis de
economía internacional —el "canal de cobertura del ajuste cambiario"—, no una búsqueda de ventaja.

Eso corta para los dos lados: **la presión de búsqueda hacia un resultado operable es baja**, lo que
es bueno; y **nadie verificó que sobreviva a los costos**, lo que es malo.

## 6. Mecanismo declarado

**Cobertura cambiaria de carteras internacionales de acciones, concentrada en un instante por una
convención institucional.**

La cadena es explícita y cada eslabón es verificable:

1. El tipo de cambio del **fixing de las 16:00 de Londres** es el precio de referencia con el que se
   valúan las carteras internacionales.
2. Los gestores quieren operar **a ese precio** para minimizar el error de seguimiento contra su
   índice de referencia. Es un deber fiduciario, no una preferencia.
3. **No ajustan la cobertura todos los días: la ajustan en el último fixing del mes.**
4. El monto del ajuste **se calcula mecánicamente** del retorno relativo de sus tenencias
   extranjeras desde el último ajuste.
5. Los clientes pasan las órdenes a los bancos **alrededor de una hora antes** del fixing, y los
   bancos se comprometen a darles el precio de fixing —que todavía no existe—, así que asumen el
   riesgo y se cubren antes.

**El punto 4 es lo que hace la señal calculable sin datos privados:** no hay datos públicos de las
operaciones de cobertura, pero el retorno bursátil del mes es un sustituto directo, y es lo que los
autores usan.

## 7. CLASIFICACIÓN

**DETERMINISTA en la fecha y la hora, y el signo es CALCULABLE de antemano.**

Es, junto con L04, la candidata más determinista del lote:

- **Fecha**: último día hábil del mes. Escrita en el calendario.
- **Hora**: 16:00 de Londres, y la ventana es la hora previa. Escrita en la convención del mercado.
- **Signo**: el del retorno bursátil del mes, conocido antes de entrar.
- **Magnitud**: proporcional a ese retorno, con un coeficiente publicado.

**Las cuatro cosas se saben antes de entrar.** Ninguna otra ficha del lote tiene las cuatro.

## 8. Estado de replicación

- **Evans (2018), "Forex trading and the WMR Fix", *Journal of Banking & Finance***, estudia el
  comportamiento del tipo de cambio alrededor del fixing de Londres y documenta la
  **autocorrelación negativa entre el período previo y el posterior al fixing, particularmente el
  último día hábil del mes**, y —según lo reportan Ito y Yamada al citarlo— **se observa en todos
  los períodos y todos los pares**. Es una replicación independiente del patrón de reversión.
- **Cambio institucional que hay que tener en cuenta antes de medir:** el **15 de febrero de 2015**
  WM/Reuters pasó de calcular el fixing con una ventana de **un minuto** a una de **cinco minutos**
  (±2,5 min), a pedido del Consejo de Estabilidad Financiera y para dificultar la manipulación.
  **La muestra del paper termina en diciembre de 2012, o sea enteramente ANTES de la reforma.**
- Hay literatura posterior sobre si la reforma funcionó: "Did the Reform Fix the London Fix
  Problem?" (NBER WP 23327, Ito y Yamada) y estudios **preregistrados** en *Pacific-Basin Finance
  Journal* (2024) sobre la representatividad de la metodología WM/R.

**La lectura honesta: el flujo de cobertura de fin de mes es una necesidad real que la reforma no
elimina —los gestores siguen teniendo que cubrirse—, pero la ventana de cinco minutos cambia la
microestructura del pico. El efecto de la hora previa debería sobrevivir; el del instante del
fixing, no necesariamente.** Los datos del proyecto (2016-2019) son **todos posteriores** a la
reforma.

## 9. Cuántas variantes probaron los autores

Contable de lo publicado: **10 monedas** estimadas en panel **y una por una**; días de control
contra el último día del mes; una variable indicadora del último día de cada mes; una hora previa
como ventana principal, más otras ventanas alrededor del fixing; y análisis de permanencia del
impacto con razones de varianza.

**Para el juez: `variantes_probadas` = 30 como mínimo** (10 monedas × 3 ventanas). Con el resto de
los cortes, 100 es la lectura conservadora.

**Atenuante real, del mismo tipo que en L07:** el paper prueba una **hipótesis estructural** —el
canal de cobertura— que predice el signo **antes** de mirar los datos. Un signo predicho por teoría
y confirmado es una evidencia distinta de un signo encontrado barriendo. No es una defensa
verificable, pero es una diferencia.

## 10. Qué haría falta para probarla acá

**Datos: NO LOS TENEMOS, y hacen falta dos cosas.**

1. **6E o 6J en barras de un minuto**, 2016-2019, cubriendo las 16:00 de Londres (**11:00 ET** en
   horario estándar, 12:00 ET en verano — y el desfase de los cambios de horario entre Reino Unido
   y Estados Unidos hay que resolverlo, no ignorarlo).
2. **El retorno mensual del índice bursátil** de cada país, hasta el penúltimo día del mes. Es
   gratis y trivial de conseguir.

**Obstáculo del juez, otra vez:** sólo acepta `ES` y `MES`. Habría que medir comisión y
deslizamiento de 6E.

### El número que la mata, y hay que decirlo antes

**Doce eventos por año. Cuarenta y ocho en 2016-2019.**

Con 48 operaciones, la resolución del juez es `33 % · raíz(5000/48) = ±337 %`. Una ventaja de $70 se
mediría como **$70 ± $236**. **El juez debería devolver NO MEDIBLE**, y la regla de "pocas
operaciones" existe exactamente para esto.

Aun poniendo las cuatro monedas que Roberto podría operar simultáneamente (hasta 4 contratos), son
192 operaciones y ±167 %. **Sigue sin ser medible.**

**Para llegar a 3 desvíos harían falta ~5.000 eventos: 416 años con una moneda, o 104 años con
cuatro.**

### Entonces, ¿para qué queda anotada?

Porque **es determinista en la fecha, la hora y el signo**, y las candidatas deterministas no se
juzgan por acumulación: **se verifican por casos**. La pregunta "en los 48 fines de mes de
2016-2019, ¿la moneda del país cuya bolsa subió más se depreció en la hora previa al fixing?" es una
pregunta descriptiva sobre un mecanismo, con 48 casos, **y contestarla no requiere una ventaja
estadísticamente significativa ni gastar un cartucho del contador de multiplicidad.**

Lo que **no** puede hacer es convertirse en un negocio: 12 operaciones por año a $70 son **$840 al
año por contrato**, antes de costos. **Eso no paga una cuenta de fondeo.**

**Es una candidata para entender el mercado, no para operarlo. Lo digo así para que nadie la ascienda
después.**
