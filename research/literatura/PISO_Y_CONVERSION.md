# El piso y la conversión a dólares — referencia única de esta carpeta

**VENTANA L. NO MEDIDO. No gasta cartucho, K sigue en 261.**

Todas las fichas de `research/literatura/` traducen la magnitud publicada a **dólares por sesión por
contrato ES** y la comparan contra el piso del proyecto. Las dos operaciones se definen acá una sola
vez, con su procedencia, para que ninguna ficha invente su propia aritmética.

---

## 1. Hay DOS pisos y no son el mismo número

El encargo de esta ventana hablaba de un piso de **"~$43 a $73 por sesión por contrato mini"**. Ese
número existe, es correcto, y es **uno de los dos**. Conviene tenerlos separados porque descartan
cosas distintas.

### Piso de RENTABILIDAD — la ventaja que hace que operar deje de perder plata

Es el costo. Comisión, deslizamiento en el stop, y —desde el commit `bc2424f`— el
**deslizamiento de entrada** por cruzar el spread.

| momento | 5pt:20pt | 20pt:10pt | fuente |
|---|---|---|---|
| **antes** de cobrar la entrada | +$43 | +$73 | el número del encargo |
| **ahora**, entrada por mercado | **+$78,24** | **+$92,81** | `research/ventana_g/salida_piso_pasivo.txt` |
| entrada pasiva, **cota optimista** | +$15,45 | +$32,33 | ídem, ver advertencia |

Son **dólares por sesión**, con **5,39** operaciones por sesión en 5pt:20pt y **3,04** en 20pt:10pt.

**El piso subió mientras esta ventana trabajaba.** El costo de entrar cruzando el spread es ~0,13
puntos de medio-spread, ~$6,5 por operación por mini, y no cambió en diez años (commit `bc2424f`).
Cobrarlo movió el piso de referencia +$35 en 5pt:20pt y +$20 en 20pt:10pt.

**La fila pasiva NO se puede usar para descartar ni para aprobar.** El propio juez la imprime con
advertencia obligatoria: está calibrada sobre **entradas al azar**, y para un candidato real los
llenados están seleccionados por su señal, así que es una **cota optimista** hasta medirla sobre el
candidato (`JUEZ_COMO_SE_USA.md`, modo `--pasivo`).

### Piso de DETECTABILIDAD — la ventaja mínima que el presupuesto puede distinguir de la moneda

Es la potencia. No cambió.

| presupuesto | MDE en puntos de tasa de acierto | MDE en dólares por operación |
|---|---|---|
| 250 operaciones | 6,03 a 8,02 | $59 a $121 |
| **1.000 operaciones** | **3,70 a 3,98** | **$29 a $58** |
| 3.000 operaciones | 1,81 a 2,28 | $17 a $34 |

Fuente: `research/ventana_g/salida_piso_ventaja.txt`, sin cambios desde el 4/9 11:56.

**Manda el más alto de los dos.** Y para las candidatas de esta carpeta —que hacen **una** operación
por sesión sobre 1.007 sesiones— el que manda casi siempre es el de detectabilidad, porque el
presupuesto de operaciones es chico.

## 2. El costo de una operación de las de esta carpeta

Las candidatas L01, L02, L06 y L09 no usan bracket: entran, esperan 30 minutos y salen a mercado.
El piso de rentabilidad tabulado arriba es de brackets con 3 a 5,4 operaciones por sesión, así que
**no aplica directo**. Los componentes publicados, para **una** ida y vuelta por sesión:

| componente | por contrato ES | fuente |
|---|---|---|
| entrada cruzando el spread | ≈ $6,50 | medio-spread ~0,13 pt, commit `bc2424f` |
| salida a mercado a los 30 min | ≈ $6,50 | mismo medio-spread |
| comisión ida y vuelta | ≈ $4 | help.tradeify.co, 2026-09-03 |
| **total aproximado** | **≈ $17 por sesión** | **suma mía de componentes publicados** |

**Ese $17 es aritmética mía sobre números publicados, no una medición.** Lo dejo marcado como tal.
Quien mida lo calcula bien con el juez, que ya cobra los tres componentes.

## 3. Conversión de porcentajes a dólares por sesión por contrato ES

El contrato ES vale **$50 por punto** de índice; el MES, **$5**.

| período | nivel del índice | nocional de 1 ES | 1 punto básico |
|---|---|---|---|
| **2016-2019** (los datos que hay) | ≈ 2.600 | **$130.000** | **$13** |
| 2026 (fuera de la caja) | ≈ 6.400 | $320.000 | $32 |

Las dos fórmulas que usan las fichas:

```
retorno de x % del nocional en una sesión   →   x · $1.300   por contrato ES (2016-2019)

retorno anualizado de R %, una operación
por sesión, 252 sesiones por año            →   R · $5,16    por sesión por contrato ES (2016-2019)
```

Verificación de la segunda: `6,67 % → 6,67 × 5,16 = $34,4`, que es lo que aparece en la ficha L02.

**Advertencia sobre el nivel del índice.** El nocional casi se multiplicó por 2,5 entre 2016 y 2026.
Una ventaja publicada en porcentaje vale hoy más dólares que en la muestra donde se puede medir, y
una publicada en puntos de índice vale lo mismo. **Las fichas dan las dos columnas a propósito: la
de 2016-2019 es la que decide si se puede MEDIR, la de 2026 es la que decide si se puede COBRAR.**
No son la misma pregunta y confundirlas hace parecer operable algo indemostrable.

## 4. La cuenta de potencia que se repite en las fichas

El juez publica su resolución: **±33 % de la ventaja con ~5.000 operaciones**. El error escala con
la raíz de n, así que para un presupuesto distinto:

```
resolución (%)  =  33 % · raíz(5.000 / n)
```

| operaciones disponibles | resolución | qué significa |
|---|---|---|
| 5.000 | ±33 % | la vara del juez |
| **1.007** (una por sesión, 2016-2019) | **±74 %** | una ventaja de $35 se mide como $35 ± $26 |
| 192 (los eventos de L03) | ±167 % | no medible |

**Para llegar a 3 desvíos hace falta que la resolución sea ≤ 33 %, o sea ~5.000 operaciones.** Con
una operación por sesión eso son **veinte años**. Es el mismo muro que el proyecto ya conoce, dicho
en la unidad de estas candidatas.
