# Hechos medidos del ES — propiedades del mercado, no de una estrategia

**2026-09-04. No gasta cartucho. K = 261.**

Acá van números que salieron de la VENTANA G y que **no son ventaja ni conclusión**: son
propiedades medidas del ES que antes de esta semana no existían escritas en ningún lado. Se guardan
con su procedencia y su método **y sin interpretación**, para el día que alguien los necesite.

**Regla de este documento: nada de historias.** Si un número no tiene explicación, se deja sin
explicación. Poner una historia plausible al lado de un número medido es exactamente el error que
este proyecto ya midió 261 veces.

## Población, común a todo lo de acá

| | |
|---|---|
| instrumento | ES (E-mini S&P 500), futuro continuo |
| fuente | Databento, barras de 1 minuto |
| período | 2016-01-01 → 2019-12-31 |
| barras | 1.357.785 |
| sesiones | 1.007, todas con **contrato único** (las de roll quedan afuera) |
| exclusiones | sesiones degradadas (`DEGRADED_UTC`), y los 16 saltos de contrato dentro de la serie concatenada |
| caja sellada | ES diario 2020-01-02 → 2026-08-19. **No se tocó.** |
| valor del punto | $50 el mini, $5 el micro. Tick 0,25 |

---

## 1 — `L* = 5.520 barras = 4,00 sesiones`

**El plazo del agrupamiento de volatilidad del ES, en la escala que le importa a un bracket.**

### Qué es exactamente

El largo de bloque que hay que usar en un *bootstrap* por bloques móviles de barras de ES para que
la serie remuestreada **tarde en resolver un bracket lo mismo que tarda el ES real**.

No es «la autocorrelación de la volatilidad dura 4 días». Es: **si se pegan bloques de menos de 4
sesiones, la serie sintética resuelve los brackets más rápido que el mercado.**

### Método

1. De cada barra se toma el triplete `(Δcierre, extensión arriba, extensión abajo)`, las tres
   medidas contra el **cierre anterior**. Se excluyen los saltos de contrato.
2. Se resta la media global a los tres (desplazamiento uniforme: la barra queda coherente y la serie
   queda **sin drift**).
3. Se pegan `⌈n/L⌉` bloques de `L` tripletes consecutivos, con arranque al azar, y se acumulan a
   serie OHLC.
4. Se replica un bracket con **30.000 entradas al azar por lado**, horizonte de una sesión, y se
   mide la **fracción que no resuelve**.
5. Se barre `L` y se elige el que iguala la fracción real.

### El número, y su validación

Calibrado contra **una sola** tasa (20pt:10pt, 35,6% sin resolver en ES real) → `L* = 5.520`.
Con ese **único grado de libertad**, los otros dos brackets quedaron apareados solos:

| sin resolver, 1 sesión | ES real | nula IID (`L=1`) | **bloques `L*`** |
|---|---|---|---|
| 10pt:10pt | 19,0% | 0,3% | **18,4%** |
| 20pt:10pt | 35,6% | 7,4% | **35,0%** |
| 5pt:20pt | 17,4% | 1,6% | **17,3%** |

Que un parámetro apareara los tres **no estaba forzado**.

### Límites, que van pegados al número

- Calibrado a **horizonte de una sesión**. A cinco sesiones el apareo se degrada: 1,9% contra 4,0%
  real en 20pt:10pt. **No transfiere de horizonte.**
- Es un número de una familia de un parámetro. **No dice que la estructura del ES «sea» un bloque de
  4 sesiones**; dice qué largo de bloque la imita en este observable.
- Un bloque puede quedar a caballo de uno de los 16 saltos de contrato. Con el `L` más largo de la
  grilla eso afecta menos del 2% de los arranques posibles.

**Procedencia:** `bloques.py`, salida en `salida_bloques.txt`. Grilla barrida:
`1, 5, 15, 60, 240, 780, 1.380, 2.760, 5.520, 11.040`.

---

## 2 — La razón rango/σ de la barra se queda en **~76% del browniano**

**Desde los 5 minutos hasta la sesión entera. Sin explicación.**

### Qué es exactamente

`razón = E[máximo − mínimo de la barra] / desvío del incremento de cierre a cierre`, a la misma
escala. Para movimiento browniano vale `√(8/π) = 1,5958`, exacto y sin parámetros.

Las barras se agregan **dentro de cada sesión**, nunca a caballo del corte nocturno.

### La medición

| escala | barras | rango medio | desvío inc. | **razón** | % del browniano | `VR(k)` |
|---|---|---|---|---|---|---|
| 1 min | 1.357.784 | 0,6577 | 0,5961 | **1,103** | 69,2% | 1,000 |
| 2 min | 678.597 | 0,9455 | 0,8189 | 1,155 | 72,4% | 0,944 |
| 3 min | 452.332 | 1,1634 | 0,9956 | 1,169 | 73,2% | 0,930 |
| 5 min | 271.235 | 1,5102 | 1,2692 | 1,190 | 74,6% | 0,907 |
| 10 min | 135.340 | 2,1462 | 1,7801 | 1,206 | 75,6% | 0,892 |
| 15 min | 90.091 | 2,6373 | 2,1661 | 1,218 | 76,3% | 0,880 |
| 30 min | 44.831 | 3,7519 | 3,0576 | 1,227 | 76,9% | 0,877 |
| 60 min | 21.975 | 5,3367 | 4,3929 | 1,215 | 76,1% | 0,905 |
| 120 min | 10.972 | 7,6218 | 6,4172 | 1,188 | 74,4% | 0,966 |
| 240 min | 4.993 | 10,3881 | 8,3912 | **1,238** | 77,6% | 0,826 |
| 390 min | 2.984 | 13,3420 | 10,9909 | 1,214 | 76,1% | 0,872 |

`VR(k) = Var(incremento de k minutos) / (k · Var(incremento de 1 minuto))`, normalizado en `k=1`.

### Las dos explicaciones aburridas, y cuánto explican

- **Rebote entre precio de compra y de venta.** Existe y está medido: `VR(k)` cae a ~0,88, o sea la
  varianza del minuto está inflada **alrededor de un 12%** respecto de las escalas largas. Explica
  que la razón suba de 1,103 a ~1,19, que es **el 18% de la distancia hasta 1,596**.
- **Discretez de la grilla de ticks.** Explica el extremo corto —a 1 minuto el rango mediano es
  0,50 pt = **2 ticks**, y una barra que visita dos niveles no puede tener la razón de un
  browniano— pero **no el extremo largo**: a 390 minutos el rango medio es 13,34 pt = **53 ticks** y
  la razón sigue en 1,214.

### El hecho, y hasta acá llega

**La razón sube y se estanca en el 76% del browniano, y el 82% del hueco no está explicado.**

**No se le pone nombre.** Queda como hecho medido y abierto.

### Nota sobre un número mío que estaba mal

Reporté primero **1,082**. Ese desvío (0,6079) incluía los incrementos que cruzan el corte nocturno,
que son más grandes. Dentro de sesión el desvío es 0,5961 y la razón es **1,103**.

### Ruido conocido de la tabla

`VR(120 min) = 0,966` rompe la monotonía de sus vecinos (0,877 / 0,905 / 0,826). Con 10.972 barras
la estimación de varianza es ruidosa. **Es ruido de la cola de la tabla, no un rasgo.**

**Procedencia:** `razon_escalas.py`, salida en `salida_escalas.txt`.

---

## 3 — La forma de la barra del ES es asimétrica: **−0,34 a −0,78 puntos** a favor del corto

Éste no estaba en la lista que pidió Roberto; lo agrego porque es de la misma clase —propiedad
medida del mercado, no de una estrategia— y salió como subproducto.

### Qué es exactamente

Sobre series construidas **sin drift por construcción** (remuestreo IID de las barras reales,
centradas a media cero), la separación largo/corto de un bracket **no da cero**: da entre **−0,34 y
−0,78 puntos porcentuales**, siempre a favor del lado corto.

No puede ser drift: se sacó por construcción. Lo que queda en el remuestreo es la **forma marginal
de la barra** —dónde caen el máximo y el mínimo respecto del cierre anterior—, y esa forma no es
simétrica.

Dato relacionado y medido en la misma corrida: **el 3,30% de las barras de ES tienen su máximo por
debajo del cierre anterior.**

| bracket | media de la nula, 1 sesión | 5 sesiones |
|---|---|---|
| 5pt:10pt | −0,780 | −0,757 |
| 10pt:10pt | −0,511 | −0,448 |
| 20pt:10pt | −0,341 | −0,453 |
| 5pt:20pt | −0,550 | −0,548 |
| 10pt:20pt | −0,341 | −0,453 |

**Consecuencia práctica, que sí corresponde decir:** cualquier medición de separación largo/corto
sobre ES tiene que compararse contra **esta** media y no contra cero. Parte de lo que parecía
dirección es forma de barra.

**Sin explicación de por qué la forma es asimétrica.** No la busqué.

**Procedencia:** `sep_nula.py` y `sintetico.py`, salidas en `salida_sep_nula.txt` y
`salida_sintetico.txt`. 20 series independientes, desvío del desvío 16,2%.

---

## Lo que este documento NO dice

Ninguno de estos tres números es una ventaja, ni implica una regla de operación, ni se puede usar
para decidir cuándo entrar o salir. Son constantes del terreno. Si alguna vez se convierten en la
base de una hipótesis operativa, **esa hipótesis gasta cartucho** y hay que contarla contra K.
