# L06 — El mismo momento intradiario, en el futuro de VIX

**VENTANA L. Ficha de literatura. NO MEDIDA. No gasta cartucho, K sigue en 261.**

---

## 1. Cita completa

Huang, Hong-Gia; Tsai, Wei-Che; Weng, Pei-Shih; Yang, J. Jimmy (2023). **"Intraday momentum in the
VIX futures market."** *Journal of Banking & Finance*, vol. 148, artículo 106680.

- Editorial: https://www.sciencedirect.com/science/article/abs/pii/S0378426622003260
- RePEc: https://ideas.repec.org/a/eee/jbfina/v148y2023ics0378426622003260.html

## 2. El efecto, en una frase

En el futuro sobre el índice de volatilidad VIX pasa lo mismo que en los futuros de índice bursátil:
el movimiento de la rueda predice el de la última parte del día.

## 3. Instrumento y período de la muestra original

- **Futuros de VIX** del Cboe (ticker **VX**), contratos con distintos vencimientos.
- **Período de muestra: NO LO PUDE CERRAR.** El editor devuelve 403 y los resúmenes públicos no lo
  dicen. Publicado en 2023. **Quien vaya a usar esta ficha tiene que abrir el paper y anotar el
  período antes de nada.**

## 4. Magnitud declarada

- Retorno **anualizado medio de hasta casi 18 %** para estrategias basadas en el momento
  intradiario.
- Robusto entre contratos con distintos vencimientos, entre intervalos intradiarios de distinta
  duración, entre sesiones de negociación y entre múltiples subperíodos.

### Traducción a dólares por sesión por contrato VX — CON UNA ADVERTENCIA GRANDE

El contrato VX vale **$1.000 por punto de VIX**. Con VIX en 15, el nocional es **$15.000**.

| | por sesión, VIX ≈ 15 | por sesión, VIX ≈ 20 |
|---|---|---|
| 18 % anual, una operación por sesión | **≈ $11** | ≈ $14 |

**Eso queda MUY POR DEBAJO del piso del proyecto** ($29 a $58 por operación con 1.000 operaciones,
`PISO_Y_CONVERSION.md`), y ni siquiera cubre el costo de una ida y vuelta.

**Pero la cuenta descansa en un supuesto que no verifiqué: que el 18 % es retorno sobre el nocional
del futuro.** Si fuera retorno sobre el margen, o si anualizaran de otra manera, el número cambia
por un factor grande. **No lo doy por bueno. Es una cuenta que hay que rehacer con el paper
abierto, y hasta que se rehaga esta candidata tiene la magnitud SIN CERRAR.**

Si al abrir el paper la cuenta se confirma, **esta candidata se descarta por piso** y hay que
anotarlo en `DESCARTADAS.md`.

## 5. Antes o después de costos

**No verificado.** El VX es mucho menos líquido que el ES y el costo de ida y vuelta es una fracción
mucho mayor del nocional. Para un contrato de $15.000 de nocional, un tick de VX (0,05 puntos = $50)
es **33 puntos básicos**, contra los 2 puntos básicos que cuesta un tick de ES sobre su nocional.

**Ésa es la razón estructural por la que sospecho de la magnitud del punto 4, y es una razón que se
puede escribir antes de medir nada:** el mismo efecto porcentual en VX cuesta unas **quince veces
más** de operar que en ES.

## 6. Mecanismo declarado

**El mismo que L01 y L05: cobertura de gamma.** Los autores proponen que la demanda de cobertura de
los creadores de mercado de **opciones sobre VIX** contribuye al momento intradiario, y lo
respaldan con dos hallazgos condicionales:

1. El momento **persiste sólo cuando la gamma neta de las opciones sobre VIX es negativa**.
2. El efecto **se debilita cuando los inversores europeos no están en el mercado**.

El segundo es un control poco común y vale anotarlo: si el efecto fuera un artefacto de medición o
de microestructura del propio VX, no tendría por qué depender de qué continente está despierto.

## 7. CLASIFICACIÓN

**ESTADÍSTICA.**

## 8. Estado de replicación

- Es en sí misma una **replicación** de Gao et al. (2018, **L02**) y Baltussen et al. (2021,
  **L01**) en un mercado nuevo, y **con el mismo condicionante de gamma**. Que el eje de régimen se
  reproduzca en un mercado tan distinto es el argumento más fuerte de toda la familia.
- **No encontré replicación posterior** de este paper en particular. Es de 2023.
- Advertencia estructural: el mercado de futuros de VIX cambió mucho entre 2018 y 2023
  (el episodio del 5 de febrero de 2018 destruyó varios ETP de volatilidad inversa). Un efecto
  medido a través de ese quiebre no es un efecto homogéneo.

## 9. Cuántas variantes probaron los autores

Del resumen se cuentan al menos: **múltiples vencimientos × múltiples intervalos intradiarios ×
múltiples sesiones × múltiples subperíodos**, más el corte por signo de gamma. **Producto de cuatro
dimensiones de robustez.**

Para el juez, si se probara: **`variantes_probadas` = 100.** Un paper que declara robustez en cuatro
dimensiones probó al menos esas cuatro dimensiones.

## 10. Qué haría falta para probarla acá

**Datos: NO LOS TENEMOS.** Hace falta VX 1-min. Los futuros de VIX se negocian en el **Cboe Futures
Exchange (CFE)**, no en el CME, y **hay que verificar antes de nada que el proveedor de datos del
proyecto (Databento) sirva CFE** y a qué precio. La VENTANA G ya tiene armado el script de
cotización sin descarga (`databento_cotizar_spread.py`, commit 1aa1039), así que preguntar el precio
es barato.

**Y hay un obstáculo del juez, no de los datos:** `JUEZ_COMO_SE_USA.md` dice que el campo
`instrumento` acepta **`ES` o `MES`, las únicas dos con comisión medida**. **El juez no puede juzgar
VX tal como está.** Habría que medir la comisión y el deslizamiento del VX primero, que es trabajo
de la VENTANA G, no de literatura.

**Orden correcto, si alguna vez se toca:**
1. Abrir el paper y cerrar la magnitud del punto 4. Si queda debajo del piso, se termina acá.
2. Cotizar VX en Databento.
3. Medir comisión y deslizamiento de VX y extender el juez.
4. Recién entonces, medir.

**Tres pasos antes del primer número. Por eso está abajo en el índice.**
