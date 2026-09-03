# Pre-registro — Escalera por hora del día: ¿el tiempo es palanca, o sólo lo parecía?

**Fecha: 2026-09-03. Ventana D.** Se commitea **solo**, antes de correr. Sigue siendo terreno: no hay
hipótesis, no se elige nada, no se mira rentabilidad de ninguna hora. **No gasta la caja fuerte**: no se
lee nada de 2020 en adelante.

## La pregunta

La escalera anterior (`terreno_tenencia_resultado.md`) dijo que acortar la tenencia dentro de la rueda
compra menos que proporcional, y lo atribuyó a la U: la apertura es la hora más cara por minuto. Eso
se midió con ventanas que **todas empiezan a las 08:30**. Si la U es real, una hora del medio del día
tiene que ser mucho más barata que la hora de la apertura. Si toda hora retiene una fracción parecida
del riesgo, el tiempo no es palanca.

## Método — el mismo, la misma población, el mismo período

- Datos, zona horaria, sesión, excursión adversa (largo `open − min(low)`, corto `max(high) − open`),
  población **P-escalera (971 sesiones)**: exactamente como en `terreno_tenencia_preregistro.md`.
- **Ventanas:** 23 tenencias de una hora, `[h:00, h+1:00)` en CT, con `h` desde las 17:00 de la
  reapertura hasta las 15:00 del día siguiente. La última, 15:00 → 16:00, contiene el corte de
  15:15 → 15:30. Embaldosan la sesión entera sin hueco ni solapamiento.
- **Referencia:** la hora de la apertura, **08:30 → 09:30** (la misma H1 de la escalera anterior).
- **Apertura de la ventana:** el `open` de la primera barra con hora ≥ `h:00`. Si no hay barra exacta
  a `h:00`, se usa la siguiente y se **cuenta**: por ventana, cuántas sesiones no tienen barra exacta y
  cuántas no tienen ninguna barra. Una ventana sin barra en una sesión se excluye de esa ventana y se
  cuenta.
- **Por hora de arranque:** n, mediana, p90, p95, p99, en puntos, largo y corto.
- **La columna que importa:** `percentil_hora / percentil_08:30→09:30`, para p50, p90, p95 y p99.

## CONTROL — y éste debe dar DISTINTO

Por sesión: `S = Σ` de las 23 excursiones horarias, contra `T = excursión de la tenencia continua
17:00 → 16:00` del mismo lado. **`S` tiene que ser mayor que `T`**: una tenencia continua compensa
movimientos que tenencias separadas no compensan. Formalmente, `open_0 − low_{k*} = Σ_{j<k*}(open_j −
open_{j+1}) + (open_{k*} − low_{k*})` y cada sumando está acotado por la excursión de su hora salvo que
haya un hueco entre la última barra de una hora y la primera de la siguiente.

Se imprime: media y mediana de `S` y de `T`, la razón `S/T` mediana, y **el conteo de sesiones con
`S < T`**. Criterio: `S ≥ T` en la práctica totalidad de las sesiones; las que no, se listan con la
diferencia. Si `S` no es mayor que `T` en agregado, **el cálculo está mal en algún lado y no se
publica la escalera**.

## LIMITACIONES, declaradas antes de correr

1. **ES, no MES.** Libros separados que no comparten OHLC. Lo medido es el terreno de ES; el traslado a
   MES es un supuesto.
2. **Una tenencia de horario fijo no es una estrategia.** Es otra tenencia pasiva.
3. **Los NIVELES son de 2016–2019**, un período que esta misma ventana midió como **la mitad de violento**
   que 2016–2026 (mediana T23 de ES 8,75 contra 17,50 publicado por el guardián). **Las RAZONES entre
   ventanas pueden trasladarse; los niveles no.** Y **que las razones se sostengan en un régimen violento
   NO está verificado y no se va a verificar sin abrir la caja.** Queda escrito para que ninguna tabla
   de acá se lea como un stop para 2026.
4. Sin comisiones ni deslizamiento. Excursión exacta sólo para una entrada en la apertura de la ventana.
5. Las horas de la noche tienen poco volumen; una barra faltante a `h:00` corre la apertura de la
   ventana unos minutos. Se cuenta, no se corrige.

## Dónde se observa

| | |
|---|---|
| script | `research/ventaja_futuros/terreno_horas.py` |
| salida cruda, commiteada antes de interpretar | `research/ventaja_futuros/terreno_horas.txt` |
| resumen | `research/ventaja_futuros/terreno_horas_resultado.md` |
