# L15 — VPIN: mide toxicidad y riesgo de que la provisión de liquidez falle, no dirección. **Cerrada como candidata direccional.**

**VENTANA L. Ficha de literatura. NO MEDIDA. K sigue en 261.**

## 1. Fuente, con su etiqueta

**Documento de resumen del propio López de Prado** en quantresearch.org, 11 páginas, leído por Roberto el
2026-09-05. **NO es el paper revisado por pares** —Easley, López de Prado y O'Hara, *"Flow Toxicity and
Liquidity in a High-Frequency World"*, *RFS* 25(5), 2012—. **Es resumen del autor, y así se etiqueta.**

## 2. Lo que dice, textual

- **La palabra *"direction"* NO aparece en el documento** (Roberto lo verificó).
- p. 7: *"The purpose of the VPIN theory is understanding how toxicity is a source of volatility. VPIN is
  not a volatility forecasting model."*
- p. 5: se usa *"to monitor the stress to which Market makers are subjected by informed traders, thus
  providing a high-frequency metric of the probability that the liquidity provision process may fail."*

## 3. Veredicto

> ## **VPIN mide toxicidad del flujo y riesgo de ruptura de la liquidez. No mide dirección de precio, y su propio autor dice que tampoco es un modelo de pronóstico de volatilidad. Como candidata direccional, CERRADA.**

**Y como eje de régimen** —que era la única puerta que `INVENTARIO_2` le había dejado—: la casa ya tiene un
eje de régimen medido y calibrado (terciles ex-ante de volatilidad, `juez_regimen_bps.py`), y VPIN
exigiría clasificar el volumen por lado con una regla propia (*bulk volume classification*), que es un
parámetro más. **No se propone como eje. Si algún día se quisiera, es territorio de `M02` y de G, y no
cuesta cartucho hasta que se use en una regla.**

## 4. Lo que trae, aparte del cierre

La frase de la p. 5 es la misma estructura que `L13` y `L14`: **el proveedor de liquidez sometido a los
informados.** Tres papers distintos, tres mercados, la misma contabilidad. Para `D20`.

**Costos:** dinero cero, cartuchos cero, K en 261.
