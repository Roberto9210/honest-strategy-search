# A06 — Frases mías que generalizan más allá de lo medido, con su condición de falla

**VENTANA L. NO MIDE NADA. K sigue en 261.**

**Regla nueva de la casa, adoptada de la VENTANA G:** *una frase que generaliza más allá de lo que se
midió es un error del mismo tipo que un número mal calculado, y tiene que llevar su condición de falla
igual que un control.* G la descubrió en su propia frase —"los factores de las cajas grandes sirven
como constantes", cierta en promedio y falsa caja por caja— y yo la apliqué a mis documentos de las
últimas tres rondas. **Cinco frases. Las cinco quedan corregidas en su lugar con la condición al lado.**

| # | documento | la frase | qué se midió de verdad | **condición de falla, ahora escrita al lado** |
|---|---|---|---|---|
| 1 | `T01` | *"Los cinco viven en picos. Ninguno vive en un valle. Eso no es casualidad: los flujos se concentran donde hay volumen"* | cinco casos | falla en cuanto una candidata con flujo documentado viva en un valle; la primera la anula |
| 2 | `T01` | *"los cinco márgenes van a BAJAR cuando llegue el perfil"* | tres bajaron (`D13`); dos no están medidas | para L07 y L08 falla si el desvío medido de su ventana resulta menor que el del escalado uniforme (4,7 y 11,4 pb) |
| 3 | `H01` Hecho 4 | *"cerca de la mitad del volumen del ES está del lado de los que responden en menos de 200 ms"* | 45 % "alta frecuencia" según Coughlan y Orlov; < 200 ms según otro documento con otra definición | es una identificación mía entre dos definiciones; falla si la de Coughlan y Orlov incluye cuentas que no son las del Hecho 1 |
| 4 | `H01` Hecho 6 | *"la liquidación rápida de inventario no es una rareza de mayo de 2010, es la norma en 2014-2016"* | que las cuentas grandes automáticas netean el 67 % de su volumen en un minuto | netear en un minuto es consistente con creación de mercado y con absorción-y-liquidación, y la tabla no las distingue; falla si el neteo viene de cotizar los dos lados y no de deshacer inventario |
| 5 | `D09` | *"el futuro del S&P 500 era de los más líquidos que existían"* | nada: es afirmación mía sin fuente | FRÁGIL; falla si las estadísticas de volumen del CME de 1987-1996 lo ponen por debajo de otros contratos con comité de liquidación |

**Lo que NO entra en la lista, y por qué:** las reglas (`R01`, `R02`, `F16`) generalizan por diseño
—una regla que no generaliza no es regla— y su control es la lectura A/B declarada antes, no una
condición de falla empírica.

**Y la regla queda en `F13` como séptima pregunta**, para que se haga antes de commitear y no
después.

**Costos:** dinero cero, cartuchos cero, K en 261.
