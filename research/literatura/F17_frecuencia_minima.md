# F17 — FRECUENCIA MÍNIMA. Escrito ANTES de buscar la primera candidata nueva.

**VENTANA L. NO MIDE CANDIDATAS; corre CONTROLES DEL INSTRUMENTO desde el 2026-09-05 (rol ampliado por Roberto, ver `INDICE`). K sigue en 261.** Catalogar es gratis; el cartucho se gasta al preregistrar,
y esa decisión es de Roberto.

> ## LA REGLA
>
> **Una candidata entra al inventario sólo si UN MISMO MECANISMO puede producir `OPS_MIN_POR_DIA`
> operaciones por día en el ES durante cuatro años, con tenencia mediana mayor a 10 segundos y
> nada abierto a las 16:45 del este. Si no las produce, NO ENTRA, por buena que se vea. No se discute
> su mérito: no se evalúa.**
>
> **Este filtro va PRIMERO**, antes de F1'…F16 y antes de la balanza ciega. Ese orden es lo que impide
> que la búsqueda nueva sea la vieja con esperanza pegada.

---

# 1. Por qué, con el número — y el número viene del archivo, no del prompt

**Roberto me relevó una tabla** (0,513 / 0,250 / 0,112 / 0,050 / 0,025; ventaja necesaria 0,028 desvíos
por operación; "más frecuencia siempre ayuda") **y a la vez me dio la regla de no relevar números entre
ventanas sino apuntar al archivo. Fui al archivo, y la regla atrapó exactamente lo que existe para
atrapar:**

| archivo de G | commit | qué dice |
|---|---|---|
| `salida_frecuencia_potencia.txt` | `3abaa66` | la tabla que Roberto relevó: costo/σ = **0,028 "SIEMPRE"**, y *"subir la frecuencia SOLO ayuda"* |
| **`salida_frecuencia_costo.txt`** | **`e288ffc`** | **G la corrige: *"mi conclusión de la tanda pasada estaba MAL"*.** El movimiento del ES escala con raíz del tiempo (exponente medido 0,476), así que **acortar el horizonte achica el movimiento y NO el costo** |

**La tabla corregida, ES, costo ida y vuelta $12,26 = comisión $5,76 + medio-spread $6,50, `t* = 3,55`:**

| op/día | H, min | **exigida por op, en σ del horizonte** | en ticks | **detectable en 4 años** | **razón exigida/detectable** |
|---|---|---|---|---|---|
| 1 | 390 | 0,023 | 0,98 | 0,112 | **0,2** — invisible |
| **5** | 60 | 0,057 | 0,98 | 0,050 | **1,1** — recién visible |
| 10 | 30 | 0,080 | 0,98 | 0,035 | 2,3 |
| 20 | 20 | 0,098 | 0,98 | 0,025 | 3,9 |
| 40 | 10 | 0,139 | 0,98 | 0,018 | 7,8 |

**Lectura, en dos frases que no son la misma:**
1. **La ventaja que cubre el costo es ~1 tick por operación a CUALQUIER frecuencia** (columna "en
   ticks": 0,98 siempre). Lo que cambia con la frecuencia es si esa ventaja **se ve**: a 1 por día un
   tick por operación es invisible (0,023 contra 0,112); **a 5 por día recién se ve (1,1); a 20 se ve
   con holgura (3,9).** Por eso las once de la literatura murieron: eran de 1 por mes a 1 por día.
2. **Pero "más frecuencia siempre ayuda" es falso, y G lo retiró:** de 1 a 40 por día la detectabilidad
   mejora 6,3× y la ventaja exigida por operación sube 6,0× en σ. **Subir la frecuencia mejora la
   resolución y empeora la economía más rápido** (la razón sube 38×). Una candidata de 40 por día
   necesita ganar 0,139 desvíos de un movimiento de diez minutos en cada operación.

> ## **El filtro no dice "cuanto más rápido mejor". Dice: por debajo de 5 por día no se ve nada, y por encima cada operación tiene que valer un tick neto.**

# 2. El umbral como PARÁMETRO, no cableado

```
exigida(H)          =  COSTO_OP / σ_$(H)                   σ_$(H) medido por G: escala como H^0,476
detectable(n)       =  T_STAR / √n                          n = OPS_POR_DIA × 1.007
OPS_MIN_POR_DIA     =  el menor ritmo con  exigida(390/ops) / detectable(n)  ≥  RAZON_MIN

parámetros nombrados:
  COSTO_OP   = $12,26   (comisión $5,76 de la firma, leída 2026-09-05, + medio-spread $6,50 medido). PENDIENTE de la verificación de G
  T_STAR     = 3,55     Bonferroni unilateral K = 261 (D15); es la vara que G ya usa
  RAZON_MIN  = 1        "una ventaja que cubre el costo se puede ver"
```

| `RAZON_MIN` | **ops/día** | ops en 4 años | qué significa |
|---|---|---|---|
| **1** | **5** | 5.035 | ver una ventaja de un tick por operación. **Valor por defecto** |
| 2 | 10 | 10.070 | verla con margen |
| 4 | 20 | 20.140 | la línea que Roberto pidió; sale de la tabla vieja |

**Las dos cifras del prompt de Roberto —"5.000 operaciones" y "20 por día"— no son la misma: 5.000 en
cuatro años son 5 por día, y 20 por día son 20.000.** Con la tabla corregida, **5.000 ≈ 5 por día es
justo donde la razón cruza 1, y es el valor por defecto.** El catálogo marca las dos líneas, 5 y 20,
para que Roberto elija sin reescribir nada. Si `COSTO_OP` cambia con la verificación de G, cambia la
tabla del §1 y no el filtro.

# 3. Las cerraduras del reglamento, ADENTRO del filtro

Leídas por Roberto en `help.tradeify.co` el 2026-09-05; G ya las puso en el juez como cerraduras.

| cerradura | regla | qué le hace al filtro | fuente |
|---|---|---|---|
| **R2 — tenencia mediana > 10 s** | más del 50 % de las operaciones **y** de la ganancia en operaciones de más de 10 s; bloquea el retiro | tenencia mediana ≤ 10 s → **NO ENTRA** | `f5d129f` |
| **resolución** | **con barras de un minuto la tenencia mínima representable es 60 s.** Un candidato sub-minuto es **NO MEDIBLE** con el dato del repo: hace falta `mbo`/`tbbo`, que hay para seis días | tenencia < 60 s → **NO MEDIBLE hoy**, y así se anota | `f5d129f` |
| **intradiaria estricta** | todo cerrado a las 16:45 del este, 12:59 en cierre temprano | nada que necesite la noche | `R03` |
| **"No HFT bots"** | sin definición numérica; los 10 s son el único número del reglamento | **zona gris entre 10 s y ~1 min: RIESGO DE NEGOCIO, no de medición.** Se puede medir y aun así no poder operarse | `f5d129f` |
| **R7 — consistencia** | ningún día > 40 / 35 / 20 % de la ganancia. **G midió (`6d4bc1c`, flujo sintético): con ventaja inyectada a 4 minis, la mediana hasta el objetivo es DOS días, y el tope de 35 % bloquea el 99,8 % de los intentos que llegan.** El mecanismo es la velocidad, no la suerte | **no se cumple sola con la frecuencia, al revés: cuanto mejor y más rápido el candidato, más lo ata.** Es una restricción de DISEÑO DE LA EVALUACIÓN (tamaño, ritmo), externa a la candidata; se declara, no se filtra | `6d4bc1c` |
| tamaño | 4 minis o 40 micros en $50k; **el micro cuesta 2,01× más por unidad de exposición** | igual que `F8`, peor en micro | `e288ffc` |

# 4. Lo que el filtro NO acepta como frecuencia

**Apilar cinco efectos de una vez por día no es un mecanismo de cinco por día: son cinco hipótesis, y
K sube cinco.** La frecuencia tiene que salir del mismo mecanismo, con la misma regla, sin parámetros
por horario. Es `F9` y `F10` aplicados a la frecuencia.

# 5. Dónde se busca, y por qué ahí

El corpus anterior —anomalías y factores— es lento por construcción. El corpus nuevo: **microestructura
intradiaria del E-mini; la oficina de investigación del regulador (`H01`); efectos de flujo, de libro
de órdenes y de horario dentro de la sesión.** Con las cerraduras del §3 puestas antes de abrir el
primer paper.

# 6. La condición de falla del filtro, declarada antes de aplicarlo

- **Si `COSTO_OP` cambia**, cambia el §1 y el umbral, no el filtro ni el orden.
- **Si el catálogo da cero**, se escribe como *"no existen candidatas publicadas de la forma que sí
  podríamos medir"*: distinto del cero de `D13` y más duro.
- **Lo que mataría al filtro mismo:** que el juez pudiera medir con potencia una candidata de 1 por
  día. `D14` dice que no: la única que cruza con años existentes lo hace por 3 % y a `t* = 3,0`.
- **Lo que mataría la lectura del §1:** que el exponente 0,476 no valga dentro de la sesión de contado
  —es un promedio de horizontes sobre la sesión ETH— o que el medio-spread de 0,13 pt no sea el de
  las horas en que la candidata opera. Las dos son mediciones de G, no mías.

**Costos:** dinero cero, cartuchos cero, K en 261.
