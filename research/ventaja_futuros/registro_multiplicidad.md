# Registro de multiplicidad de Ventana D — 2026-09-03

**Qué es este archivo.** El cotejo de todo lo que se probó antes contra lo que Ventana D piensa probar,
con el número que manda en cada caso. Se escribe **antes** de medir H2d y después de la lectura cruzada
del repo de ALAYA (commit `6480708`, documento `reports/edge/lectura_cruzada_walk_forward_20260903.md`
de Ventana E, y el código verificado por esta ventana: `core/backtest/engine.py`,
`core/backtest/execution_model.py`, `core/backtest/data_loader.py`, `research/validation/walk_forward.py`,
los tres JSON de `backtests/walk_forward/`).

## 0 · La regla que manda, y es de este repo

`factory/spec_fase2.md` §1.1: **«K = toda configuración de estrategia que alguna vez se evaluó contra
datos de mercado en este proyecto, desde la primera línea del ledger. No se reinicia por cambio de fase,
de familia, de instrumento, de objetivo ni de persona.»** Y §1.6: **«Cualquier fase futura empieza con
K = 257 y le suma su propio presupuesto declarado.»** El ledger va por **K = 261** (`f21fe78`).

## 1 · Lo de ALAYA, uno por uno — y cuántos entran en K: **cero, y se dice por qué**

Todas sobre `BTC/USDT` y `ETH/USDT`, velas de 1 hora, 180 días, largo-solo, costos en puntos básicos
del nocional de Kraken spot. Leídas por E en el código de cada estrategia; esta ventana leyó el motor y
las tres corridas reales, no las cinco estrategias, y lo dice.

| # | qué se probó exactamente | corridas | resultado | estado del registro |
|---|---|---|---|---|
| S1 | `AnalystEngine.get_market_signals`: EMA(9) > EMA(21) y RSI(14) < 70 ⇒ largo; TP/SL del grid | 2 walk-forward reales del 13-ago: `walk_forward_20260813_154207.json` (cero trades en train en 9 de 9 ventanas, OOS vacío) y `walk_forward_20260813_155741.json` | **9 de 9 ventanas OOS negativas**; PF entre 0,05 y 0,93 | otro proyecto, otra población |
| S2 | `VolExpansionStrategy`: ruptura tras compresión de Bollinger(20) con persistencia simple | 1 walk-forward real: `walk_forward_VolExpansionStrategy_20260813_161812.json`; 2 reportes del 19-feb (uno repetido idéntico) | **7 de 9 negativas**; las dos positivas +23,7 (18 trades) y +2,8 (10 trades) | otro proyecto, otra población; los de febrero **INVERIFICABLES** |
| S3 | `PullbackTrendStrategy`: retroceso a EMA20 con precio sobre EMA200 | 1 reporte del 19-feb | −46,73 / 9 trades / PF 0,54 | **INVERIFICABLE** |
| S4 | `PullbackTrendStrategyV101`: S3 + pendiente EMA200 + ADX > 18 + percentil ATR > 40; salidas por ATR | 2 reportes del 19-feb (distinto n: 12 y 3 trades) | −52,65 y −28,29 | **INVERIFICABLE** |
| S5 | `PullbackTrendStrategyV102`: ADX14 > 16 + vela verde de rechazo; espejo bajista escrito, nunca corre | 1 reporte del 19-feb | −34,64 / 2 trades | **INVERIFICABLE** |

**Por qué los seis de febrero son INVERIFICABLES y no «rechazados».** `DataLoader` cachea en
`data/backtest/candles/{símbolo}_{tf}_{días}d.json`, **sin fecha ni hash en el nombre**, y el cache que
existe hoy es del 2026-02-14 → 2026-08-13, bajado el 13-ago. Los reportes del 19-feb corrieron sobre un
cache anterior que **fue sobrescrito**. Se sabe qué se probó; **no se sabe sobre qué 180 días**. Y el
validador que los dictaminó, `research/validation/walk_forward.py::WalkForwardValidator`, **no es un
walk-forward**: corre un backtest entero y lo rebana en tres ventanas de 30 días; su propio comentario
dice «Simplified sliding window simulation … assumes strategy is mostly stateless». Un rechazo que no
se puede reproducir no es evidencia de la misma clase que uno que sí.

**Conteo para el anexo:** 5 fuentes de señal; **3 walk-forwards reales** (1 vacío) con 27 combinaciones ×
9 ventanas = **243 ajustes de grid** cada uno; **6 reportes** de febrero = 5 corridas distintas + 1
repetida. Ninguna promovida.

**¿Entran en K?** **No, y no por corazonada sino por la regla:** K cuenta lo evaluado **en este
proyecto, desde la primera línea del ledger**. ALAYA es el proyecto anterior, sin ledger, cuyos meses
son exactamente lo que este repo existe para no repetir (`ARTICLE.md`). Además:

- **Ninguna está cerca de H2d.** H2d es el signo del hueco `open_t − close_{t−1}` en barras **diarias** de
  un **futuro de índice**, sin parámetros. Las cinco son **cripto, horarias, de tendencia o de ruptura,
  con TP/SL en % ajustados por grid**. Ni el instrumento, ni la resolución, ni el mecanismo, ni la forma
  de la regla coinciden. **Lo digo fuerte porque se pidió fuerte: nada de ALAYA es H2d ni una variante.**
- Lo más cercano en **familia** a algo de este repo es S2 (ruptura tras compresión) con la **F5** de la
  búsqueda 1 (volatilidad, compresión → expansión, 7 configuraciones, ya contadas en K₁ = 57), y S1 con
  la **F2** (tendencia intradía, cruces de medias, 14 configuraciones, ya contadas). Es decir: **la clase
  de idea ya está pagada en K por este proyecto, sobre ES**. Las corridas de ALAYA sobre cripto no
  agregan una configuración de este proyecto; agregan evidencia adversa en otra población.
- **Si Roberto prefiere la lectura conservadora** y las suma igual (8 evaluaciones distintas, o 5 fuentes),
  el efecto sobre la vara es: `0,05/261 = 1,916 × 10⁻⁴` → `0,05/269 = 1,859 × 10⁻⁴`; el |z| unilateral
  exigido pasa de 3,55 a 3,56. **No mueve nada.** Queda anotado para que la decisión sea suya y barata.

## 2 · LA CORRECCIÓN QUE SÍ ES A MI CUENTA — y no viene de ALAYA

Al cotejar contra §1.6 apareció esto: **`potencia.py` calculó la potencia con α = 0,05 y α = 0,0125
(Bonferroni sobre las 4 hipótesis congeladas). No aplicó el denominador heredado del proyecto.** Si
Ventana D es una fase de **este** proyecto, la regla dice α / (261 + K_D), con K_D = 4 si corren las
cuatro hipótesis, o K_D = 1 si sólo corre H2d. Eso cambia el veredicto de potencia:

Aproximación normal, unilateral, `z_α = Φ⁻¹(1 − 0,05/265) ≈ 3,55`, `potencia ≈ Φ(δ√n/0,5 − z_α)`:

| población | n | acierto 55 % | 58 % | 60 % |
|---|---|---|---|---|
| diario MES, intocado 50 % | 910 | δ√n/σ = 3,02 → **≈ 0,30** | 4,83 → ≈ 0,90 | 6,03 → ≈ 0,99 |
| diario MES, completo | 1.821 | 4,27 → ≈ 0,76 | 6,83 → > 0,99 | > 0,99 |
| ES Databento, sellado 2020–2026 | 1.715 | 4,14 → ≈ 0,72 | 6,63 → > 0,99 | > 0,99 |

**Con el α heredado, H2d al 55 % NO es detectable en el intocado del diario (potencia ≈ 0,30); lo es
desde 58 %.** Con α = 0,05 la tabla decía 0,91 al 55 %. **La diferencia es la regla §1.6, y mi tabla la
omitió.** Dos lecturas posibles, y la decisión es de Roberto, no mía:

1. **Ventana D hereda K.** Entonces `potencia.py` se regenera con la columna α = 0,05/(261 + K_D), el
   diseño de H2d cambia su umbral de detección de 55 % a 58 %, y la partición 50/50 sigue siendo la
   correcta. Es la lectura literal de §1.6 («cualquier fase futura»).
2. **Ventana D es otro proyecto** con ledger propio que empieza en `394d023`. Entonces K_D arranca en 0,
   la tabla actual vale, y hay que decirlo por escrito en `hipotesis_congeladas.md` §4 con fecha, porque
   es exactamente el «reinicio del contador» que §1.1 prohíbe dentro del proyecto.

**Hasta que Roberto elija, la lectura que rige es la 1, porque es la más exigente y es la escrita.**
No se corre nada de H2d mientras tanto; el diseño ya decía que no se corre nada todavía.

## 3 · La máquina de ALAYA — lo que verifiqué en el código, con símbolo

| supuesto | dónde lo vi | verificado |
|---|---|---|
| serie continua 24×7, sin sesión ni huecos | `run_walk_forward`: `candles_per_day = {'1h': 24, '4h': 6, '1d': 1}`; ninguna función de sesión en `engine.py` ni `data_loader.py` | **sí** |
| stops llenados al **cierre de la vela**, no al nivel | `_process_shadow_signal`: `fill = self.execution_model.execute(..., price=current_candle['close'])` tras `exit_reason = "STOP_LOSS"`, con el comentario «Let's pass close for now, slippage handles the rest» | **sí**; y el TP también se llena al cierre |
| PnL agregado entre símbolos al elegir el grid, sin piso de trades | `run_range` itera los símbolos en un mismo `trial`; `calculate_summary()["net_pnl"]` suma todos los `closed_trades`; selección `if pnl > best_pnl` sin `total_trades` mínimo; empate ⇒ gana la primera combinación del `itertools.product` | **sí** |
| trains solapados 50 %, tests contiguos, sin embargo, sin holdout | `train_n 720, test_n 360, step_n 360`; `test_start = train_end`; el bucle consume `min_len` entero | **sí** |
| costos en bps del nocional | `ExecutionModel(fee_bps=16, slippage_bps=5, spread_bps=2.5)`; `fee = notional × fee_bps/10000` | **sí**; calibrados de Kraken spot según el docstring, forma equivocada para futuros (comisión por contrato, deslizamiento en ticks) |
| **posiciones abiertas al final de cada rango se descartan** | `run_range` crea un `BacktestEngine` nuevo por rango; sólo `closed_trades` cuentan; el `inventory` muere con el objeto | **sí, y E lo nombró para el train; vale igual para el test**: el último trade abierto de cada ventana OOS, ganador o perdedor, no existe |
| cantidad fraccionaria, nocional $1.000, drawdown sobre $10.000 ficticios | `qty = notional / close`; `_calculate_max_drawdown(initial_capital=10000)` | **sí** |
| cache de velas sin fecha ni hash | `cache_file = f"{symbol}_{timeframe}_{days}d.json"` | **sí** |
| la entrada usa el cierre de la vela cuya señal se calculó con esa misma vela | `history_window = full_history[...:current_idx+1]` y `price=current_candle['close']` | **sí**: no es look-ahead, pero supone fill exacto al cierre |

**Lo que le falta además de multiplicidad y potencia** (mío, sobre lo de E): el cierre de posiciones al
final de cada rango (o su arrastre), un piso de trades en la selección, intervalos sobre métricas OOS con
n de 8 a 22, procedencia de los datos por hash, y una regla de agregación entre ventanas que el motor no
tiene: devuelve una lista y no dictamina.

## 4 · Veredicto: **RECHAZAR ENTERA. No se toma ninguna de las tres piezas.** Con el motivo

**No es que la máquina sea mala para lo que hace; es que su forma no es la de la pregunta de Ventana D.**

1. **La forma de la partición (ventanas rodantes con grid en train) resuelve un problema que H2d no
   tiene.** H2d no tiene parámetros: no hay nada que elegir en train. Un walk-forward sobre una regla sin
   parámetros es un backtest rebanado, es decir, **exactamente lo que `research/validation/walk_forward.py`
   hace y que E llamó por su nombre**. Y rebanar en nueve ventanas multiplica las miradas al dato sin
   agregar potencia: nueve tests de n ≈ 100 valen menos que uno de n ≈ 900. Mi partición —un período
   mirado para controles y precondiciones, un intocado con una sola corrida— es la correcta para una regla
   sin parámetros, y ya está congelada en `diseno.md` §1.3. **Lo mismo vale para H1, H2 y H3**, que tampoco
   tienen parámetros libres por decisión de `hipotesis_congeladas.md` §3.
2. **La interfaz de costos es la forma equivocada y mi arnés ya tiene la correcta.** `factory/harness.py`:
   `FRICTION_RT = COMMISSION_RT + 2 × SLIPPAGE_TICKS_PER_SIDE × TICK × POINT_VALUE` = 3,90 USD **por
   contrato**, en ticks, restado por el propio arnés antes de que nadie mire un número. Heredar la interfaz
   de bps para luego parametrizarla a cero y reescribir la fórmula es heredar una forma para no usarla.
3. **El esquema de salida por ventana no aporta nada que un `dict` no tenga**, y arrastra la unidad
   equivocada (`net_pnl` en USDT de nocional, `max_drawdown_pct` sobre $10.000).

**Qué supuestos heredaría si tomara cada pieza, nombrados** — por eso no las tomo:

| pieza | supuesto heredado |
|---|---|
| forma de la partición | ventanas por **índice de vela** = tiempo continuo 24×7; estado reiniciado por rango = posiciones al borde descartadas; tests contiguos sin embargo |
| interfaz de costos | fricción **proporcional al nocional**; fill al **cierre de la vela**, también para el stop |
| esquema de salida | métrica de selección = PnL neto sin n mínimo; PnL **agregado entre símbolos** |

**Lo que mi arnés ya resuelve mejor que la máquina, y vale más que la máquina:**

- **Sesión.** La población de Ventana D está construida por sesión CME en hora de Chicago con horario de
  verano, con exclusión contada de cierres anticipados, sesiones con dos contratos y días `degraded`
  (`terreno_tenencia.py`), y **verificada contra otro proveedor con 0,00 % de diferencia en cinco
  percentiles** (`terreno_tenencia.txt` §1). La máquina no tiene una línea de sesión; es la precondición
  que le costó a ALAYA el día entero.
- **Fill del stop.** `terreno_stop.txt` §4 midió, en barras de **un minuto**, cuánto se pasa el precio del
  nivel del stop: mediana un tick, p95 2–4 puntos, máximo 31. La máquina llena el stop al cierre de una
  vela de **una hora**, con signo desconocido. **Mi diseño no modela el fill del stop todavía** (lo dice
  `terreno_stop_preregistro.md`), pero ya tiene la cota medida para cuando lo modele.
- **Caja fuerte como código.** `harness.py::VaultViolation` y `run_on(..., examen_final=...)`: el arnés se
  niega a evaluar sobre la parte B salvo que la llamada se declare examen final. La máquina no tiene
  holdout.
- **Ledger con cadena de hashes y K que no se reinicia.** `experiments_ledger.jsonl` (`prev`, `hash`,
  `rules_digest`). La máquina no registra ni siquiera qué velas usó.
- **Potencia antes de medir y umbrales de control derivados**, `potencia.py` y las enmiendas de
  `terreno_stop_preregistro.md`. La máquina elige por PnL neto sin n mínimo.

**Lo único que ALAYA le deja a Ventana D es el §1 de este archivo: cinco intentos en otra población,
adversos, y seis rechazos que no se pueden reproducir.** Se registran. No se cuentan en K. No se hereda
código.
