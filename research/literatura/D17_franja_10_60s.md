# D17 — La franja de 10 a 60 segundos está muerta por costo. La aritmética antes de los $800.

**VENTANA L. NO MIDE CANDIDATAS; corre CONTROLES DEL INSTRUMENTO desde el 2026-09-05 (rol ampliado por Roberto, ver `INDICE`). K sigue en 261.** Aritmética en `scratchpad/cuenta_franja.py`, corrida desde
el archivo. **Dinero: cero. Los $800 de `tbbo` no se gastan, y este documento dice por qué con número.**

**El origen:** en el reporte anterior propuse que la franja entre 10 y 60 segundos —permitida por la
firma (R2 dice 10 s) y ciega para el repo (barras de 1 minuto)— se volvía medible comprando `tbbo`
para los 1.007 días. Roberto hizo la cuenta de que está muerta por costo y pidió verificarla, porque
hoy ya se equivocó dos veces. **La verifiqué contra las filas que G midió. La cuenta de Roberto es
correcta, con una dirección invertida que no cambia nada.**

---

# 1. Las filas que G midió, reproducidas

Fuente: `salida_frecuencia_costo.txt`, commit `e288ffc`. Costo de cruzar $12,26 = 0,2452 pt = 0,98 ticks,
igual a todo horizonte. `σ(H)` medido sobre 1.006 sesiones de ES 1-min.

| H | σ medido, pt | **exigida/σ** | lo que G publicó |
|---|---|---|---|
| 390 min | 10,672 | 0,023 | 0,023 ✓ |
| 60 min | 4,329 | 0,057 | 0,057 ✓ |
| 20 min | 2,491 | 0,098 | 0,098 ✓ |
| 10 min | 1,769 | 0,139 | 0,139 ✓ |
| **1 min** | **0,596** | **0,411** | — (Roberto: 0,41 ✓) |

# 2. (a) La extrapolación por debajo de un minuto: válida como COTA, y la dirección del exponente

| exponente | σ a 30 s | ticks | **cruzando** | **pasivo** | σ a 10 s | **cruzando a 10 s** |
|---|---|---|---|---|---|---|
| 0,500, raíz pura | 0,421 pt | 1,69 | **0,582** | 0,273 | 0,243 pt | **1,008** |
| 0,476, medio de G | 0,429 pt | 1,71 | 0,572 | 0,269 | 0,254 pt | 0,965 |
| 0,458, local de G entre 1 y 2 min | 0,434 pt | 1,74 | 0,565 | 0,266 | 0,262 pt | 0,935 |

**Sobre la dirección que dijo Roberto, y está invertida:** un exponente **menor** a horizontes cortos
hace que `σ` se achique **más despacio** al acortar `H` —`0,5^0,458 = 0,728` contra `0,5^0,5 = 0,707`—,
así que a 30 s el movimiento típico es un poco **mayor** y la razón un poco **mejor**: 0,565 contra
0,582. **Diecisiete milésimas. No cambia nada, y la señalo porque la regla es señalar.**

**Lo que sí empeora el número, y no está en la extrapolación:** el exponente por debajo de 0,5 en los
horizontes cortos es la firma del **ruido de microestructura** —el rebote entre compra y venta entra
en el cierre de cada barra—. Ese rebote **no es movimiento capturable: es el costo mismo, medido desde
el otro lado.** La `σ` que un operador puede capturar a 30 s es la del precio eficiente, **menor** que
0,43 pt. Y sobre una grilla de 0,25 pt, un "movimiento típico" de 30 s es **1,7 ticks**: capturar 0,98
neto por operación es acertar el siguiente tick o dos en ~80 % de los casos sin selección adversa.

> ## **La extrapolación es válida como COTA SUPERIOR del movimiento capturable. La razón verdadera es peor que 0,57. El asesino es conservador.**

# 3. (b) ¿Existe algo publicado, en cualquier mercado, que capture ~58 % de un movimiento típico por operación?

**Primero qué significa el número.** Una ventaja de 0,58 desvíos por operación es un Sharpe **por
operación** de 0,58. Anualizado con el ritmo que la franja permite:

| ritmo | operaciones por año | **Sharpe anualizado implícito** |
|---|---|---|
| 40 por día | 10.080 | **58** |
| 200 por día | 50.400 | 130 |
| 780 por día (una cada 30 s) | 196.560 | 257 |

**Lo publicado, en la misma unidad:**

| quién | Sharpe anualizado | condición |
|---|---|---|
| Baltussen et al., la mejor estrategia intradiaria del inventario viejo (`L01`) | **1,73** | paga el spread, 1 por día |
| Virtu, la firma de alta frecuencia más documentada | **el dato, textual del S-1** (Virtu Financial Inc., 10 de marzo de 2014, registro 333-194473, p. 2): *"we had only one losing trading day during the period depicted, a total of 1,238 trading days"*. **El S-1 NO dice "Sharpe" en ninguna parte** (Roberto lo buscó en el documento completo). El **~48** es una **DERIVACIÓN de Roberto sobre ese dato**: cola de 1/1.238 → ~3 desvíos diarios bajo normalidad → × √252 ≈ 48. **Verificada con bisección sobre `erfc` (`cuenta_overnight.py`): z = 3,15, anualizado 50,1** —Roberto puso 3,03; la diferencia es del orden de magnitud de la aproximación y no cambia nada—. Supone normalidad y estacionariedad; vale como orden de magnitud y no como cifra de nadie | **cobra** el spread, colocada, miles de operaciones por día. Ingreso neto ajustado por día: $1,7 millones en 2013 |
| **Menkveld 2013**, el creador de mercado de alta frecuencia, **una acción** (`L13`, textual) | **9,35** | **cobra** el diferencial, 1.397 operaciones por día por acción, colocado. **Es el comparador correcto: una estrategia, un instrumento** |
| Baron, Brogaard, Hagströmer y Kirilenko 2019, alta frecuencia en el E-mini | sin números: SSRN bloqueado en dos vueltas | los más rápidos y agresivos |

**Corrección del 2026-09-05, con `L13`:** Virtu es una firma con miles de instrumentos y su ~50 lleva la
diversificación adentro (`50/9,35 = 5,4` → ~29 libros independientes, aritmética y no ventaja). **El
comparador de una estrategia sobre un instrumento es Menkveld: 257 contra 9,35, 27 veces el mejor
cobrador de diferencial documentado sobre un solo instrumento.** Lo de "cinco veces Virtu" se retira.

> ## **No. Ni la firma de alta frecuencia más rentable documentada llega a lo que la franja exige a alguien que PAGA el spread desde una máquina de casa: a una operación cada 30 segundos harían falta ~257, cinco veces lo que se deriva para la firma más rápida del mundo con la computadora dentro del mercado. La franja está muerta por costo, y los $800 no se gastan.**

# 4. (c) El caso pasivo: 0,27, y contra lo que G ya midió

Con entrada pasiva el costo baja a comisión sola: $5,76 = 0,115 pt = 0,46 ticks. **Exigida a 30 s:
0,266-0,273** (Roberto: 0,27 ✓). Un cuarto de un movimiento de 1,7 ticks, por llenado, neto.

**Lo que G midió** (`mbo`, seis días, entradas pasivas al azar, `9a02717` y anteriores): el markout a 30 s
que sobrevive es **de +0,00 a +0,08 pt**, y a 60-300 s es **negativo** (−0,08 a −0,10).

| markout medido a 30 s | menos la comisión 0,115 pt | **por llenado** |
|---|---|---|
| +0,00 | | **−0,115 pt = −0,46 ticks** |
| +0,04 | | −0,075 pt = −0,30 ticks |
| +0,08, el mejor día | | **−0,035 pt = −0,14 ticks** |

> ## **Negativo en todos los casos medidos, en el mejor día también. El caso pasivo ya estaba muerto con los números de G; el número que Roberto pidió por si acaso lo confirma: hace falta 0,27 y lo medido es de 0,00 a 0,08 antes de la comisión.**

# 5. Lo que los $800 comprarían, dicho exacto

**Visibilidad, no economía.** A una operación cada 30 s en cuatro años son 785.460 operaciones y el
umbral detectable baja a **0,004 desvíos**: la franja sería medible con enorme resolución. **Pero la
razón exigida/detectable sería 145: se mediría con precisión que hace falta ganar 145 veces lo mínimo
que se ve.** Los $800 comprarían la confirmación de un número que la aritmética ya fija.

**Y lo único que la compra agregaría —la `σ` real a 10 y 30 s— G lo puede sacar gratis de los seis
días de `mbo` que ya tiene, si alguna vez hace falta.**

# 6. Condición de falla de este cierre

- **Si G mide `σ(30 s)` en el `mbo` y da más de 0,60 pt** (40 % arriba de la extrapolación), la razón
  cruzando baja a 0,41: **sigue muerta.** El cierre sobrevive a cualquier `σ` plausible.
- **Lo único que la reviviría es un costo por operación por debajo de ~0,1 tick**: reembolsos por
  proveer liquidez, que los futuros no le pagan a una cuenta minorista de firma de fondeo.
- **Y la zona gris:** aun si un número la salvara, entre 10 s y un minuto la firma se reserva llamar
  "HFT" a lo que quiera (`F17` §3). Medible y no operable es peor que ciega.

**Costos:** dinero **cero, y cero ahorrado: $800 que no se gastan.** Cartuchos cero, K en 261.
