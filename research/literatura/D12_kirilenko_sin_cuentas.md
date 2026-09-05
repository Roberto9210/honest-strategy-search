# D12 — Kirilenko sin cuentas: qué se puede observar de la orden que nos pegó, en un `mbo` sin identificador. **Para la VENTANA G.**

**VENTANA L. NO MIDE CANDIDATAS; corre CONTROLES DEL INSTRUMENTO desde el 2026-09-05 (rol ampliado por Roberto, ver `INDICE`). K sigue en 261.**

**Roberto corrigió el descarte:** dije que sin cuenta la definición de Kirilenko no se puede aplicar.
**Es cierto para clasificar CUENTAS y no hace falta clasificar cuentas.** La pregunta de G es *"cuando
una orden pasiva nuestra se ejecuta, ¿quién nos pegó?"*, y eso se caracteriza por el **comportamiento
de la orden**, que el `mbo` sí trae. **No clasifica participantes: clasifica llenados.** Y clasificar
llenados es lo que la Pieza 3b necesita.

---

# 1. Lo que el `mbo` de G trae, según el propio código de G

De `mbo_lib.py`, encabezado, sin tocarlo: *"mbo trae order_id, así que el libro se reconstruye EXACTO:
A (alta), C (baja), M (modificación), F (ejecución de una orden en reposo), R (reset). T (print de
trade) se ignora para el libro —las reducciones vienen por F—. side: B = bid, A = ask."*

**Lo que eso da por orden EN REPOSO:** identidad de la orden (`order_id`), instante de alta, precio,
tamaño, cada modificación, y su fin: cancelación o ejecución. **Una orden en reposo tiene biografía
completa.**

**Lo que da de la orden AGRESORA —la que cruza y nos pega—: un registro `T` con lado, precio y tamaño.**
Si ese `T` trae un `order_id` distinto de cero en el GLBX de Databento **no lo pude verificar**: la
documentación no me cargó dos veces. **G lo verifica en una línea sobre un archivo que ya tiene.**
Si lo trae, la agresora también tiene biografía cuando su remanente queda en reposo; si no, la
agresora es sólo tamaño, lado e instante.

# 2. La traducción, criterio por criterio. Lo más literal posible, y qué se pierde

| Kirilenko, por CUENTA y por DÍA | traducción a lo observable en `mbo` sin cuenta | **qué se pierde** |
|---|---|---|
| **(1) Volumen**: la cuenta operó ≥ 10 contratos en al menos uno de los tres días previos | **NO SE TRADUCE.** No hay cuenta, no hay "volumen de la cuenta" | todo. Es un criterio de filtro mínimo y su pérdida es la menos grave |
| **(2) Inventario al cierre** ≤ 5 % del volumen del día | **Sólo a nivel POBLACIÓN**: el flujo agresor neto firmado (compras agresoras − ventas agresoras, en contratos) integrado sobre el día. Si las cuentas de bajo inventario dominan, el flujo agresor neto del día es chico respecto del volumen | la partición: se ve la suma de todos, no quién la produce. **Es el factor 25 de `H01` en su forma pura** |
| **(3) Inventario intradía** ≤ 1,5 % del volumen | **Sí, a nivel población, y es exactamente la regresión de Kirilenko**: cambio del flujo agresor neto en el segundo `t` contra los cambios de precio de los 20 segundos anteriores. Kirilenko la corre sobre el inventario de las 16 cuentas; G la puede correr sobre el flujo agresor total. Si sale **positivo en 0-4 s y negativo en 10-20 s**, la firma de absorción-y-liquidación está en el mercado | el coeficiente sale **mezclado** con todos los demás agresores. Se sabe si la firma existe y cuánto pesa en el agregado, no de quién es |
| **(4) Las 16 con más operaciones**, con un salto entre la 16 y la 17 | **NO SE TRADUCE** para la agresora. **SÍ para las vecinas de cola**: vida de la orden (alta → fin), número de modificaciones, tamaño, y si el mismo nivel se repone en menos de `x` ms después de una cancelación. Órdenes de vida corta, muchas modificaciones y reposición inmediata son el comportamiento que Kirilenko atribuye a alta frecuencia y creadores de mercado | la agresora no tiene vida en el libro. **Su única "velocidad" observable es la de reacción** (fila siguiente) |

## Y lo que Kirilenko NO tiene y el `mbo` SÍ: la latencia de reacción de la agresora

**`H01` Hecho 1: la mediana de respuesta de los algorítmicos es < 200 ms; la de los manuales > 9 s.**
En el `mbo` se puede medir, para cada `T` que nos pega, **el tiempo desde el último evento que pudo
dispararla**: un cambio del mejor precio de cualquier lado, o una ejecución en el nivel opuesto.

| tiempo desde el disparador hasta el `T` que nos llenó | lectura |
|---|---|
| **< 200 ms** | reacción algorítmica, escalón 1 |
| **> 9 s** | escalón 2 o sin disparador |
| entre medio | **el escalón 3 de `H01`, el nuestro, o nada** |

**Es una clasificación por fill, no por cuenta, y usa el número del regulador como corte. Lo que se
pierde: nada del regulador, pero el corte es de 2013-2016.**

# 3. Lo que la Pieza 3b puede llevarse de acá: siete características por LLENADO

Para cada `F` nuestro, todas observables sin cuenta:

| # | característica | de dónde sale | qué distingue |
|---|---|---|---|
| 1 | **tamaño de la agresora** | `T` | grande y barre varios niveles = flujo direccional; chica y de un nivel = otra cosa |
| 2 | **niveles barridos** por la misma agresora | `T` consecutivos con el mismo instante | idem |
| 3 | **latencia de reacción** | `T` menos último cambio del tope | algorítmica o no, con el corte del regulador |
| 4 | **ráfaga de cancelaciones en NUESTRO nivel** en los `x` ms previos al fill | `C` de las vecinas | **"nos dejaron solos"**: las vecinas informadas se fueron antes del golpe. Es selección adversa vista desde la cola |
| 5 | **flujo agresor neto del mismo lado en los 10-20 s siguientes** | `T` posteriores | la liquidación de Kirilenko, a nivel población: si el que nos pegó era absorción, alguien deshace enseguida |
| 6 | **reposición del nivel opuesto** en < `x` ms | `A` posteriores | presencia de creadores de mercado del otro lado |
| 7 | **markout** a 1, 10, 30, 60 s | precio | lo que G ya mide. Es la variable a explicar; las seis anteriores son las que la explican |

> ## **La traducción rinde: de los cuatro criterios de Kirilenko se pierden dos enteros y dos se convierten a población; y aparecen tres observables que Kirilenko no tenía —latencia de reacción, ráfaga de cancelaciones, reposición— porque él tenía cuentas y no libro.**

# 4. Lo que hay que decir antes de que G lo use

1. **Todo esto es DESCRIPTIVO del fill, no del mecanismo.** Que un fill tenga latencia < 200 ms y
   flujo reverso a 15 s no prueba que fue un algorítmico de inventario bajo; es consistente con eso.
2. **Los umbrales —200 ms, 9 s, 10-20 s, 5 s— son de 2010 y 2013-2016.** Sirven como cortes
   declarados de antemano, no como hechos del 2019. Si G los usa, que los use **fijos y escritos antes**,
   que es lo que vale de ellos.
3. **La correlación entre las siete y el markout es, en sí misma, una medición sobre datos ya
   mirados**: no pre-registra nada y no gasta cartucho, pero **cualquier "regla de entrada" que salga
   de ahí es una hipótesis nueva y cuesta un cartucho.** Lo escribo porque es exactamente el borde
   donde este proyecto se ha equivocado.
4. **Verificación de una línea para G, antes de nada:** si los `T` del GLBX traen `order_id ≠ 0`.
   Cambia cuánto se puede decir de la agresora. **CONTESTADA por G (commit `7de1fe2`): SÍ, 203.213 de
   203.215 en el día medido.** La agresora tiene identidad de orden, y las siete características se
   pueden calcular.

**Costos:** dinero cero, cartuchos cero, K en 261. Tiempo de Roberto: leer y pasárselo a G.
