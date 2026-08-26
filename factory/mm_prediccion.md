# Predicción — matriz de correlación de vuelta de mes (NQ, YM, NKD, +ES referencia)

**Fecha:** 26 de agosto de 2026. **Escrita y commiteada ANTES de correr `mm_matriz.py`.** Igual que la
predicción sobre ρ del 24-ago (`multimercado_dia0.md` §5), que falló y cuya consecuencia pre-declarada
se aplicó sin renegociar. Ésta se contrasta con la misma regla: se publica al lado del resultado, falle
o acierte.

## Lo que se predice, con magnitudes, para poder fallar

Sobre 2000-2019 (parte A), retornos de vuelta de mes estandarizados, ventanas post-exclusión de roll:

1. **NQ–ES ≥ 0,85.** Mismo país, mismas mega-caps, mismas fechas exactas. Es casi la misma serie.
2. **NQ–YM en 0,70 – 0,85.** Los dos son gran capitalización de EE.UU. sobre fechas idénticas; el Dow
   pesa por precio y le falta la tecnología pura, y eso es lo único que los separa.
3. **NKD contra NQ e YM en 0,35 – 0,55, claramente menor que cualquier par EE.UU.–EE.UU.** La ventana
   de vuelta de mes contiene noches compartidas (el flujo global corre en las mismas fechas), así que no
   va a salir baja; pero Tokio tiene su propio pozo y su propio calendario, así que tampoco alta.
4. **Toda la matriz positiva.** Ningún par negativo ni ~0: son índices de acciones sobre el mismo
   calendario. Si algún par sale < 0,15, sospecharé antes un error de alineación de fechas que una
   diversificación milagrosa.

## El veredicto que espero

Correlación media ponderada implícita: **~0,55 – 0,65**, contra un quiebre de **0,765** (spec §d).

> **Espero que la COMPUERTA 1 PASE, con `n_efectivo` ≈ 380 – 450 contra el umbral de 342 — y espero
> que pase CERCA del filo, no con holgura.** La compuerta 2 (cota superior al 90 % de cada ρ) es la que
> está en duda real: si los pares EE.UU.–EE.UU. salen en la parte alta de mi rango, la cota los empuja
> por encima del quiebre y **la fase no se abre**. Mi probabilidad subjetiva de que la fase se abra:
> **~55 %.** Esto no es una predicción cómoda de "pasa seguro": es un casi-empate declarado antes de
> mirar, y la regla ya está escrita para las dos ramas.

## Qué falsea qué

- Si NQ–YM sale **> 0,85**: el pozo del Dow no es distinguible del pozo S&P/Nasdaq ni siquiera en la
  ventana de vuelta de mes — el argumento de mecanismo de §b.1 (fila 2) queda tocado, además del número.
- Si NKD sale **> 0,70** con los dos: el "pozo japonés independiente" era un relato — la vuelta de mes
  sería un solo flujo global, y entonces agregar mercados NO agrega evidencia, que es la premisa entera
  de la fase. Ésa sería la mala noticia grande, la análoga a la lección del 24-ago: la correlación alta
  saldría DE LA MISMA FUENTE que haría verosímil al mecanismo global.
- Si NKD sale **< 0,20**: sospecha de artefacto (alineación de fechas, huecos), no celebración.
