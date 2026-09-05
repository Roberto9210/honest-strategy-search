# AUD01 — La auditoría de las 261, versión parcial: ¿cuántas tenían potencia contra una ventaja que apenas cubre el costo? **Especificación para la VENTANA G, dueña de los archivos. NO la corre esta ventana.**

**VENTANA L. NO MIDE CANDIDATAS; corre CONTROLES DEL INSTRUMENTO desde el 2026-09-05. K sigue en 261.**
**Esta auditoría no es una medición del mercado ni un control: es lectura de un registro. No gasta
cartucho, no toca la caja, no pre-registra nada.**

**Lo que decide (`D15` §3.2-3.3):** si los 272 negativos del programa hablan del **mercado** o del
**instrumento**. La versión completa exigía la magnitud afirmada por hipótesis; **la parcial no la
necesita**: basta saber, por hipótesis, si la resolución con que se la juzgó era más fina que la
ventaja que apenas cubre el costo —el tick neto de `F17`—. Una prueba que no podía ver ni el costo
no podía decir "sí" aunque la hipótesis fuera cierta y rentable al mínimo.

---

# 1. Dónde viven las 261 — lo que encontré mirando los archivos, sin correr nada

| archivo | qué tiene | qué NO tiene |
|---|---|---|
| `research/ventana_g/REGISTRO_JUEZ.jsonl` | **3 registros** (ejemplos del juez). Campos: `nombre, veredicto, obs, ventaja_B, z_info, z_rent, n_op, variantes_declaradas, instrumento, regla{tipo, objetivo_pt, stop_pt}, firma_30, hash, prev_hash`. **El registro más nuevo trae además `resolucion_mde`, `magnitud_afirmada`, `tenencia_mediana_seg`, `z_exigido`** | las 261: no están acá |
| `factory/experiments_ledger.jsonl` | **114 líneas.** Campos: `ts, family, config, part (A/B), result{trades, net_pnl, profit_factor, win_rate, max_drawdown, per_year}, note, prev, hash` | **ni σ por operación, ni resolución, ni magnitud afirmada.** Sólo `trades` y `net_pnl` |

> **Primera conclusión, antes de contar nada: 114 líneas no son 261 hipótesis.** La cuenta de K vive en la
> especificación y en el ledger por reglas propias (`caja_alcance_y_uso.md` §2: *"el 'un solo uso' vive
> en la spec y en el ledger, no en una comprobación"*). **El primer paso de la auditoría es la
> conciliación: qué registros del ledger corresponden a cuáles de las 261, cuáles hipótesis contaron
> para K sin dejar registro (las descartadas por compuerta, como H2d), y cuáles líneas son autotests.**
> Eso lo sabe quien lleva K; no esta ventana.

# 2. La unidad, el campo y la comparación

**Unidad:** cada hipótesis que contó para K. Tres estados posibles por hipótesis: **CON POTENCIA**, **SIN
POTENCIA**, **SIN REGISTRO** (contó para K y no hay resolución reconstruible).

**El campo que se lee:** `result.trades` del ledger (= `n_op` en el registro del juez). **Y el que falta y
hay que reconstruir:** `σ_op`, el desvío en dólares del resultado de una operación **para esa regla de
salida**. G lo tiene por celda de bracket (`calibrar_por_regimen.py`, `aritmetica.py`: $436,65 para
5pt:20pt en ES, otras celdas otros valores). **La asignación `config → σ_op` es de G.**

**La comparación, por hipótesis:**

```
resolucion_i  =  T_STAR · σ_op(config_i) / √(trades_i)         en $ por operación
costo_op      =  $12,26  (ES, 1 mini, ida y vuelta con medio-spread: e288ffc)   ·  MES: $2,47
                 escalado por contratos si la hipótesis operaba más de uno

SIN POTENCIA   si  resolucion_i  >  costo_op
CON POTENCIA   si  resolucion_i  ≤  costo_op
```

**Equivalente en operaciones, para que se vea el orden de magnitud:** con `T_STAR = 3,55` y `σ_op =
$436,65`, `n_min = (3,55 × 436,65 / 12,26)² ≈ 16.000` operaciones. **Con la vara vieja de 3,0, ≈ 11.400.**
Se corre con las dos varas y se reportan las dos: la que rigió cuando se juzgó cada hipótesis, y la del
programa.

**Lo que se reporta:** el conteo de los tres estados, **y la tabla por familia y por `trades`** (la
resolución es `1/√n`: la auditoría es, en el fondo, un histograma de `trades` contra `n_min(config)`).

# 3. Las dos lecturas, SELLADAS antes de ver el conteo

| si el conteo da… | entonces |
|---|---|
| **casi ninguna CON POTENCIA** (digamos, menos de una de cada diez) | **los 272 negativos son sobre el instrumento**: `D15` se resuelve hacia *"no medimos"*. Ninguna hipótesis fue refutada; fueron **no vistas**. El cero del programa es un cero de alcance |
| **la mayoría CON POTENCIA** | **son sobre el mercado**: `D15` se resuelve hacia *"medimos y no hay"*, al menos al nivel del costo. El capítulo "instrumento" se cierra como excusa |
| **mixto** | se reporta la fracción **por familia y por frecuencia**, y `D15` se resuelve por partes: las familias con potencia son "no hay"; las sin potencia, "no vimos" |
| **muchas SIN REGISTRO** | el resultado es sobre el registro, no sobre el mercado ni el instrumento: **K contó cosas que no se pueden auditar**, y eso también se escribe |

**Y la condición que ya estaba escrita:** si el ledger no permite reconstruir `σ_op` por hipótesis —porque
`config` no identifica la regla de salida—, **no hay nada que contar y se dice así.** No se estima `σ_op`
con un promedio: un promedio convertiría la auditoría en la misma clase de error que la vara de 3,0 en
`D06`.

# 4. Lo que la versión parcial NO responde

- **Potencia contra el costo no es potencia contra lo afirmado.** Una hipótesis podía afirmar diez veces
  el costo; contra eso la prueba pudo tener potencia aunque no la tuviera contra el costo pelado. La
  parcial da una **cota inferior** de "sin potencia": las que no veían ni el costo, seguro no veían nada
  útil; las que sí, no se sabe si veían su propia afirmación.
- **Para las hipótesis futuras la auditoría es trivial**: el registro del juez ya guarda
  `resolucion_mde` y `magnitud_afirmada`. **La versión completa existe desde el registro más nuevo en
  adelante.** Lo parcial es sólo para el pasado.

# 5. Costos

Dinero cero. Cartuchos cero. **Tiempo de G: la conciliación (que puede ser lo más largo), la asignación
`config → σ_op`, y una corrida de lectura.** Tiempo de Roberto: decidir si se asigna.
