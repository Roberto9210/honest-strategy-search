# Veredicto del día cero — la matriz, contra la regla escrita antes

**Fecha:** 26 de agosto de 2026. **Orden de los hechos:** spec y predicción commiteadas (`7c0e4d0`),
corrección de calendario commiteada (`250d298`), cambios de regla en el ledger (`1ff6891425c4bcd0`
AFLOJA, `6d39040a0706df6f` ENDURECE), controles 15/15 — y recién entonces se corrió
`factory/mm_matriz.py`, una sola vez. Salida completa: `factory/mm_matriz_resultado.json`.

## La matriz (2000-2019, post-roll, desmediada — jamás una media, jamás un P&L)

| | ES *(ref.)* | NQ | YM | NKD |
|---|---|---|---|---|
| **ES** *(ref.)* | 1 | 0,8162 | **0,9540** | 0,7140 |
| **NQ** | 0,8162 | 1 | 0,7395 | 0,5948 |
| **YM** | **0,9540** | 0,7395 | 1 | 0,7102 |
| **NKD** | 0,7140 | 0,5948 | 0,7102 | 1 |

Períodos comunes: NQ-YM 210 · NQ-NKD 126 · YM-NKD 126 (ES contra cada uno: 230/210/126).

## Las compuertas, tal como quedaron escritas

| | n_efectivo | umbral | veredicto |
|---|---|---|---|
| **Compuerta 1** (matriz medida, N = 778) | **361,3** | 342 | PASA |
| **Compuerta 2** (cota superior 90 % de cada ρ) | **346,7** | 342 | PASA — **por 1,4 %** |

> ## LA FASE SE ABRE.
>
> Y hay que decir cómo: **al filo exacto que la compuerta 2 existía para vigilar.** 346,7 contra 342
> es un margen de 4,7 operaciones efectivas. Con la potencia nominal en **82,1 %** contra el δ
> pre-registrado — que es un máximo seleccionado de 57: al 75 % de ese efecto la potencia real es
> **57,9 %**, y al 50 % es **30,2 %**. La fase se abre con derecho a un "no detectado" perfectamente
> esperable. δ mínimo detectable al 80 %: 0,147387, apenas debajo del 0,151542 medido.

## La predicción, contrastada — y volvió a fallar en magnitud

| predicho (`mm_prediccion.md`, sellado antes) | medido | ¿cumple? |
|---|---|---|
| NQ–ES ≥ 0,85 | 0,8162 | **no** — quedó corto |
| NQ–YM en 0,70–0,85 | 0,7395 | **sí** |
| NKD–NQ y NKD–YM en 0,35–0,55 | 0,5948 y 0,7102 | **no — los dos por ARRIBA** |
| matriz toda positiva, ningún par < 0,15 | mínimo 0,5948 | sí |
| ρ̄ ponderada ~0,55–0,65 | **0,691** | **no — por arriba** |
| compuerta 1 pasa con n_ef ≈ 380–450, cerca del filo | pasó con **361,3**, más al filo aún | dirección sí, magnitud no |
| la compuerta 2 es la que está en duda real | pasó por 1,4 % | sí — era exactamente ahí |

**Tres de siete fallaron, y las tres en la misma dirección: subestimé la correlación.** Es la falla
opuesta a la del 24-ago (donde sobrestimé el agrupamiento CL/GC/BTC), y deja la misma lección con el
signo cambiado: los índices de acciones comparten la vuelta de mes mucho más de lo que el relato de
"pozos por familia de índice" sugería.

**Lo que la matriz dice del mecanismo, sin maquillar:**

- **YM–ES = 0,954.** El Dow en la ventana de vuelta de mes ES el S&P. El aviso pre-declarado en §b.1
  ("el candidato más débil por mecanismo") se quedó corto: el criterio de falsación era NQ–YM > 0,85 y
  no se disparó (0,7395), pero la fila de ES muestra que el pozo del Dow es indistinguible del pozo del
  descubrimiento. YM aporta poco n efectivo nuevo, y ese poco está contado — para eso era la matriz.
- **NKD–YM = 0,7102** rozó el criterio de falsación del "pozo japonés independiente" (> 0,70 con los
  dos; NKD–NQ 0,5948 no lo confirmó). La versión que sobrevive: la vuelta de mes tiene un componente
  global grande y un componente local real pero menor. NKD sigue siendo el que más n efectivo aporta
  por operación, y menos del que el argumento de §b.1 prometía.

## La divulgación D1, con sus números

- Bloque A (≤ 2019-11, calendario compartido con el descubrimiento): N = 566, **n_ef = 265,8**.
- Bloque B (2019-12 →, calendario que ninguna búsqueda vio): N = 212, **n_ef = 95,7**.
- La fila de ES contra los tres mercados de la fase: 0,8162 / 0,9540 / 0,7140.

**Traducción obligatoria:** el 73 % del n efectivo de la fase vive en fechas donde F4 fue seleccionada
como la mejor de 57, sobre un índice que correlaciona 0,82-0,95 con dos de los tres mercados nuevos.
El bloque B solo tiene ~31 % de potencia. Si el resultado final es positivo y viene empujado por el
bloque A, la frase de la spec se aplica textual: *réplica de la muestra de selección, no confirmación
independiente* — y la salida honesta será mirar los dos bloques por separado, cosa que la spec ya
obliga a publicar.

## Lo que sigue — y NO es hoy

Abrir la fase significa: pre-registrar en el ledger la prueba única (K = 1, los tres mercados juntos,
`turn_of_month(4,3)` congelada, fricción dentro del número) ANTES de calcular el primer P&L
multi-mercado, con las seis prohibiciones de §f vigentes. Hoy no se corrió ningún backtest: los únicos
números de estrategia que existen sobre NQ/YM/NKD siguen siendo cero.

**La caja fuerte de ES (2020-2026) sigue sellada.** Nada de hoy la tocó: la matriz se midió en
2000-2019, y los conteos del bloque B son calendario, no precios.
