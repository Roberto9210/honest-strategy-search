# D19 — El feed cambió de formato en marzo de 2017, en medio de nuestra muestra. **Para la VENTANA G.**

**VENTANA L. NO MIDE CANDIDATAS; corre CONTROLES DEL INSTRUMENTO desde el 2026-09-05 (rol ampliado por Roberto, ver `INDICE`). K sigue en 261.**

**Fuente:** catálogo oficial de Databento, conjunto `GLBX.MDP3`, **leído por Roberto el 2026-09-05**
(`F16` en acción: a esta ventana la página le devolvió sólo la palabra "Databento"). Tres frases
textuales:

> *"Since March 2017, MDP 3.0 has changed from providing aggregated depth at every price level (like
> CME's legacy FAST feed) to providing full granularity of every order event for every instrument's
> direct book."*

> *"Data prior to 2017-05-21 is retrieved from FIX flat files and does not have capture timestamps."*

> *"Timestamps prior to 2015-11-20 are limited to millisecond resolution."*

Y del mismo catálogo: cobertura desde **2010-06-06**; esquemas MBO, MBP-1, **MBP-10**, TBBO, Trades,
BBO-1s, BBO-1m, OHLCV; captura en Aurora DC3 con tarjeta FPGA y sellado por hardware, sincronizado a
UTC con PTP.

---

# Lo que esto le hace a tres cosas de G, dicho sin medir nada

## 1. La comparación entre épocas: **10,6× más eventos de libro por día en 2026 que en 2017**

**Si los días de 2017 que entraron a esa cuenta son anteriores a 2017-05-21 —o al cambio de marzo—,
parte del 10,6× es FORMATO, no mercado:** un feed que publica profundidad agregada por nivel de precio
emite por construcción menos eventos que uno que publica cada orden. **La única forma de separar
mercado de formato es comparar días de 2017 posteriores al cambio con días de 2018-2019 y con 2026.**
No sé qué días usó G; **lo verifica G contra sus fechas, en una línea.**

## 2. Los seis días de `mbo` de la Pieza 3 (3a, 3b, `D12`)

**Si alguno de los seis días es anterior a marzo de 2017, su "mbo" no puede contener eventos por orden
reales**: el feed de la época no los publicaba. Databento no puede fabricar `order_id` que el CME no
emitió. **La reconstrucción FIFO de `mbo_lib.py` supone identidad de orden; para un día pre-2017 esa
identidad tendría que ser sintética o estar ausente.** G tiene las seis fechas; el chequeo es contra
2017-03 y 2017-05-21.

## 3. La antigüedad del estado del libro: **7.321 ms en 2017 contra 318 ms en 2026**

**Los datos anteriores a 2017-05-21 no tienen sellos de captura**, y los anteriores a 2015-11-20 tienen
resolución de milisegundo. Una mediana de antigüedad medida sobre días sin sello de captura está
medida sobre otro reloj que la de 2026. **Si los días de 2017 son anteriores al 21 de mayo, la
comparación de relojes no es entre iguales.**

---

# Lo que confirma, para dos documentos míos

- **`D10`**: el esquema **MBP-10** existe en el catálogo → el canal público del ES publica diez niveles
  hoy, confirmado por la fuente que vende el dato. **La fecha exacta del paso de cinco a diez sigue sin
  saberse**, pero marzo de 2017 es un borde de era del feed que la acota por arriba.
- **`D14` y `D08`**: Databento empieza en 2010-06-06: **no llega a la era del piso**; la conclusión de
  `D08` sobre los datos de 1987-1996 queda respaldada por la fuente, no por mi memoria.

# Lo que NO cambia

**Las barras de un minuto de 2016-2019** —lo que usan el juez, el perfil intradiario y todo el inventario
viejo— son OHLCV: **el cambio de formato del libro no las toca.** Los desvíos, los factores por caja y
los veredictos de `D13` no dependen de esto.

**Costos:** dinero cero, cartuchos cero, K en 261. **Tiempo de G: comparar seis fechas y las de 2017
contra 2017-03 y 2017-05-21.**
