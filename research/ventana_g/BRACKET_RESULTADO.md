# VENTANA G — siguiente paso: ¿existe una forma de operar que baje la vara de 1,5?

Solo Tradeify Growth (50K), la firma elegida por evidencia. Misma máquina de Monte Carlo de
`aritmetica.py`, generalizada: en vez de una moneda simétrica de amplitud `b`, cada operación es
ahora un bracket **asimétrico** — `T` ticks de objetivo, `S` ticks de stop, `N` micros (MES). Sin
ventaja, la probabilidad de tocar el objetivo antes que el stop dentro de una operación es la de
un paseo aleatorio sin drift entre dos barreras: `P(gana) = S/(S+T)`, y el costo se resta siempre
(ganada o perdida), así que el valor esperado de una operación sigue siendo exactamente `-costo`,
sin drift — la misma ley que en el paso anterior, generalizada.

**"La vara"** = `p_equilibrio / P(total, cero ventaja)`, la misma definición del reporte anterior
(sección 4): cuántas veces más seguido, que lo que el paseo aleatorio-menos-costos ya logra, hace
falta pasar para llegar a esperanza cero. Tradeify Growth partía de 1,5x.

## Grilla

`N` ∈ {1,4,10,20,40} micros (40 = el máximo de Tradeify en 50K) · `S` ∈ {8,16,40,80,120} ticks
(= 2,4,10,20,30 puntos ES/MES, los mismos `D` que mide `terreno_stop_resultado.md`) · `T = k·S`
con `k` ∈ {0,5, 1, 2, 4}. 100 celdas. Antes de simular se excluyen las que son inviables **por
diseño**, no por resultado (83 de 100 en la corrida con costo real):
- no llegan a calificar los $150/día que exige la etapa fondeada ni ganando las 5 operaciones;
- una sola operación ganadora ya cubre más de un tercio del objetivo de $3.000 (una apuesta de una
  sola vez, no una pregunta de "cuántas operaciones hacen falta");
- un solo día jugado siempre para el mismo lado ya mueve más que todo el objetivo o todo el
  drawdown (mismo problema, a nivel del día);
- el paso es tan chico frente a la distancia a recorrer que ni con generosidad de tiempo se
  resuelve (estimación de Wald, `objetivo×drawdown/Var(paso) > presupuesto de operaciones/3`).

**El ritmo de operaciones por día no es una constante inventada**: se deriva del propio terreno
(`terreno_tenencia_resultado.md`, minutos de cada ventana, y `terreno_stop_resultado.md` sección 2,
% de toque). Se busca la ventana más chica (M15=15min, H1=60min, RTH=390min, T23=1380min) donde el
toque a esa distancia ya supera 50%, y `operaciones/día = sesión / esa ventana` (tope de sentido
común: 30/día). A 2 puntos eso da 30/día; a 10, 20 o 30 puntos, ninguna ventana medida llega al
50% ni en la sesión completa, así que el piso es 1/día.

## CONTROL

Con costo cero, la vara tiene que caer a ≤1,0 en cada celda factible. Peor celda:
**N=4, S=80, T=80 → vara=0,9711.** CONTROL PASADO.

## El resultado, sin filtrar terreno todavía

| N | S(ticks) | T(ticks) | k | P(eval) | P(fondeada) | P(total) | operaciones ev. | operaciones fond. | arrastre $ | E $ | **vara** |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 10 | 120 | 60 | 0,5 | 0,303 | 0,304 | 0,0923 | 7,8 | 7,9 | 392 | **+41,60** | **0,666** |
| 4 | 120 | 120 | 1,0 | 0,272 | 0,272 | 0,0739 | 18,4 | 18,5 | 368 | +16,73 | 0,832 |
| 4 | 80 | 160 | 2,0 | 0,247 | 0,245 | 0,0607 | 15,9 | 16,2 | 321 | -1,03 | 1,013 |
| 10 | 40 | 80 | 2,0 | 0,231 | 0,226 | 0,0521 | 11,3 | 12,0 | 584 | -12,70 | **1,181** |
| 20 | 40 | 40 | 1,0 | 0,223 | 0,214 | 0,0478 | 7,3 | 7,9 | 761 | -18,43 | 1,285 |
| 10 | 40 | 40 | 1,0 | 0,201 | 0,199 | 0,0401 | 22,1 | 22,1 | 1.105 | -28,92 | 1,535 |
| 4 | 40 | 80 | 2,0 | 0,174 | 0,174 | 0,0304 | 58,6 | 58,5 | 1.171 | -42,01 | 2,025 |

(tabla completa en `salida_bracket.txt`)

**Sí existe, matemáticamente**: `N=10, S=120 ticks (30pt), T=60 ticks (15pt)` da vara **0,666x**,
por debajo hasta de 1,0 — esperanza *positiva* ($41,60) con cero ventaja de mercado. Esto no es un
error: el bracket "objetivo chico, stop ancho" (relación riesgo:beneficio 2:1 en contra) da 66,7%
de acierto por operación, y frente a los $3.000/$2.000 fijos de la cuenta, el paseo aleatorio sin
drift resuelve mejor de lo que el equilibrio exige. Es una asimetría real del diseño de Tradeify
(objetivo/drawdown = 1,5, no 1,0), no del mercado.

## El cruce con el terreno — por qué esa combinación no sirve

| S (ticks→pt) | filtro A: deslizamiento p95 / stop | filtro B: % toque en T23 (23h) | veredicto |
|---|---|---|---|
| 8 → 2pt | **no se determina** (no medido en `terreno_stop_resultado.md`) | 87,3% (pasa) | descartada |
| 16 → 4pt | 2,10pt / 4pt = **52%** (>25%, falla) | 75,5% (pasa) | descartada |
| 40 → 10pt | 2,50pt / 10pt = 25% (al borde, pasa) | **46,2%** largo / 51,8% corto (falla por el lado largo) | **al borde** |
| 80 → 20pt | 3,82pt / 20pt = 19% (pasa) | 21,4% (falla) | descartada |
| 120 → 30pt | 10,25pt / 30pt = **34%** (>25%, falla) | 12,2% (falla) | descartada |

Los dos filtros vienen de mediciones ya commiteadas, ES 2016-2019 (`terreno_stop_resultado.md`
secciones 2 y 4): **filtro A** descarta un stop si el exceso de deslizamiento p95 *dentro de la
misma barra que lo toca* supera el 25% de la distancia del stop nominal — el "stop limpio" del
modelo de ticks deja de existir. **Filtro B** descarta un stop si se toca menos del 50% de las
veces en la sesión completa de 23 horas — la tenencia típica excede lo que una cuenta con drawdown
EOD puede sostener sin acumular riesgo de un día para el otro.

La combinación ganadora (S=120, D=30pt) **falla los dos filtros a la vez**, y por mucho: se toca
solo 1 de cada 8 veces en 23 horas (la posición sigue abierta la mayor parte del tiempo) y, cuando
sí se toca, el precio ya se movió en promedio un tercio más de lo que el stop nominal asumía —
es decir, la pérdida real típica no es $1.525 (el número limpio del modelo) sino bastante más.
**El terreno no mide directamente cuánto más — eso sería un dato nuevo — pero mide que la premisa
del modelo (un stop que se ejecuta a la distancia S) ya falla en ese punto en un 34% en la cola.**

El único punto donde algo sobrevive parcialmente es **S=40 ticks (10 puntos)**: el filtro de
deslizamiento pasa justo (25%), pero el de tenencia falla por el lado largo (46,2% < 50%) y pasa
por el lado corto (51,8%) — **un empate técnico que depende de qué lado se opera**, no una holgura
real. Ahí, y solo ahí, aparecen varas por debajo de 1,5 en la grilla: la mejor es **1,181x**
(N=10, T=80 ticks/20pt, k=2), y le siguen 1,285x y 1,535x. Son minoría: la mayoría de las
combinaciones con S=40 igual quedan por encima de 1,5 (2,03x, 3,43x).

## Conclusión

Ninguna combinación baja de 1,5 **sobreviviendo con margen** los dos filtros de terreno. Existe una
franja puramente matemática que sí baja — hasta 0,666x, con esperanza positiva — pero exige un
stop de 20 a 30 puntos que el terreno mata dos veces (tenencia que excede la sesión, deslizamiento
medido que ya es 25-52% del stop antes de contar el libro). El único punto de fricción real es un
stop de 10 puntos, donde la vara SÍ cruza por debajo de 1,5 en una combinación (1,18x) — pero ese
mismo stop se resuelve dentro de la sesión completa apenas el 46-52% de las veces, literalmente en
el borde del criterio, y cambia de lado según el signo de la operación. No es una victoria clara.

## Limitaciones

- El filtro de deslizamiento (A) usa el p95 de una sola dirección/ventana (T23 largo) para D=4,10,20
  y una población distinta ("23 horas juntas") para D=30; D=2 no tiene dato y se descartó por eso,
  no porque se haya medido que falla.
- El umbral de 50% de toque (filtro B) y el de 25% de exceso (filtro A) son criterios de sentido
  común, no derivados estadísticamente de los datos — quedan explícitos para que se puedan mover.
- El terreno es ES 2016-2019, la mitad de violento que el período completo (Ventana D). Un régimen
  más violento empeora el filtro A (más exceso) y probablemente mejora el B (toca más rápido);
  no se puede saber la neta sin abrir la caja de 2020+.
- El modelo de bracket asume que el precio se mueve tick a tick sin saltos dentro de la operación
  (coherente con el hallazgo de `terreno_stop_resultado.md` de que ES nunca "abre" más allá del
  stop entre barras de minuto) pero no modela el exceso *dentro* de la barra salvo por el filtro A.
- `operaciones/día` es una derivación gruesa (ventana donde el toque cruza 50%), no una medición
  directa del tiempo hasta resolución de un bracket de dos barreras.
