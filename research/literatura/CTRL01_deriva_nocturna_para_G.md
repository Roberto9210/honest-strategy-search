# CTRL01 — CONTROL DEL INSTRUMENTO, no candidata: ¿nuestros datos reproducen la deriva nocturna publicada de Boyarchenko, Larsen y Whelan? **Diseño para la VENTANA G.**

**VENTANA L. NO MIDE CANDIDATAS; corre CONTROLES DEL INSTRUMENTO desde el 2026-09-05 (rol ampliado por Roberto, ver `INDICE`). K sigue en 261.** **Esto es un CONTROL**, del mismo tipo que los diez del juez:
corre sobre datos ya mirados, no pre-registra nada, no produce una regla, y **no gasta cartucho**. Su
única pregunta: **¿el instrumento de la casa ve un resultado publicado sobre el ES cuando ese resultado
está adentro de los datos?** Es la primera vez que se probaría.

**Por qué no es candidata, dicho antes:** es una operación por día. `F17` no la deja entrar aunque salga
positiva, y `L12` ya la dio ciega. **Si el control "pasa", no cambia ningún veredicto ni abre ninguna
prueba.**

---

# 1. Lo publicado que se intenta reproducir (`L12`)

Boyarchenko, Larsen y Whelan, NY Fed SR 917: ES, retornos del punto medio, 1998-2020. **Dos objetos:**

| objeto | lo publicado | lo que hace falta de ellos y no tengo |
|---|---|---|
| **A — la deriva**: retorno medio de la posición larga **2:00-3:00 del este** | Sharpe **1,1** antes de costos → `t ≈ 1,1 × √23 = 5,3` sobre 23 años | **el retorno medio en pb por día y su error estándar** (tabla de la deriva por hora) |
| **B — la regresión** (p. 27): retornos horarios nocturnos **18:00-23:00** sobre el **desbalance de flujo del final del día anterior** | existe; el fragmento no trae el coeficiente | **la definición exacta del desbalance** (¿última hora? ¿día entero? ¿firmado por agresor?), **el coeficiente, su `t` y la unidad** |

**Sin esos números el control no tiene objetivo sellable. Roberto los tiene a una página de distancia
(p. 27 y la tabla de la deriva por hora).** El diseño de abajo deja los criterios escritos **como
funciones de esos números**, para que se sellen en cuanto lleguen y no después de mirar.

# 2. Con qué datos, y qué se puede y qué no

| pieza | dato de la casa | ¿alcanza? |
|---|---|---|
| retornos horarios nocturnos del ES | ES 1-min 2016-2019, 1.007 sesiones | **sí**, para A y para la variable dependiente de B |
| **desbalance de flujo** del final del día | **NO está en barras de un minuto**: no hay lado agresor | **con barras, sólo un sustituto** (volumen firmado por regla de tick sobre cierres de barra: **degradado**). **Exacto: `trades` o `tbbo` de la última hora de cada día**, ~1.007 ventanas de 60 min. *Costo estimado desde la cotización de G —un día entero de `tbbo` fue $0,79—: del orden de **$30-40**. **FRÁGIL**, y la decisión de comprar es de Roberto* |

# 3. El diseño, con los criterios como funciones de lo publicado

**A — la deriva (no necesita compra).** Para cada sesión, el retorno del punto medio (o del cierre de
barra, declarado cuál) entre las **2:00:00 y las 3:00:00 del este**, con el horario de verano manejado
fecha por fecha como en `A01`. Media, error estándar, `t`.

- **potencia declarada antes**: si el efecto de 23 años es estacionario, en 4 años se espera
  `t ≈ 5,3 × √(4/23) ≈ 2,2`. **El control tiene potencia marginal, y eso se dice antes.**
- **criterio de "reproduce"**: **signo positivo Y media dentro del intervalo de ±2 errores estándar de
  la media publicada** (con su número). No se usa la vara de 3,0: un control pregunta *"¿vemos lo que
  dicen?"*, no *"¿es real?"*.
- **criterio de "no reproduce"**: media de signo contrario, o fuera del intervalo con `|t| ≥ 2` en la
  diferencia.
- **lectura sellada de un "no reproduce"**: **antes** de atribuirlo al instrumento hay que descartar el
  reloj —la ventana de ellos es hora del este; nuestras barras están en Chicago; el horario de verano
  desplaza una hora dos veces al año—. Si el reloj está bien y no reproduce, **hay dos lecturas y se
  reportan las dos**: el efecto no fue estacionario en 2016-2019 (ellos lo tienen adentro de un
  promedio de 23 años), o el instrumento no lo ve. **No se elige.**

**B — la regresión (necesita la definición y, para hacerlo exacto, la compra).** `r_{t,h} = a_h + b_h ·
OFI_{t−1} + e`, para `h` = 18-19, 19-20, 20-21, 21-22, 22-23 del este, con `OFI_{t−1}` definido **como
ellos** y no como nos convenga.

- **criterio**: el signo de `b_h` coincide con el publicado en las horas donde ellos lo reportan
  significativo, y la magnitud cae dentro de su intervalo. Potencia: nuestro error estándar es
  `√(23/4) ≈ 2,4` veces el de ellos; **si su `t` es menor que ~5, el control B no tiene potencia y no
  se corre**: se declara "sin potencia" y listo.

# 3b. CTRL01-B — CERRADO SIN GASTAR, 2026-09-05

**Roberto fue al paper.** BLW p. 26, textual: *"Panel (b) extends the regression to include the previous 12
lagged hours of RSVt for the night hours. Most of the point estimates in the table are insignificant.
However, focusing on the highlighted purple diagonal estimates we find economically large and
statistically significant return predictability arising from order imbalances at close of regular U.S.
trading hours. More specifically, the point estimates are large at exactly the opening of Tokyo and
European regular market opening times, even after controlling for all imbalances subsequent to U.S.
close."* Y del panel (a): *"There is only one significant hour between 23:00 – 24:00 and the sign is
positive not negative."*

**El estadístico `t` exacto de la Tabla VIII no se pudo extraer** —Roberto lo dice así en vez de
estimarlo, y así queda—. **La compuerta sellada era `t ≥ 5` para que B tuviera potencia con nuestro
error estándar 2,4 veces mayor.** El texto describe la mayoría de las estimaciones como no
significativas y las significativas concentradas en una diagonal: **con eso, B no pasa la compuerta y
no se corre. Los ~$30-40 no se gastan.**

**Lo que sí trae, y va a la casa:** p. 27, *"ex-ante volatility has a strong amplification effect on the
relationship between order imbalance and overnight returns between 2:00 – 3:00."* **Es el eje de régimen
de G —volatilidad ex-ante— confirmado desde afuera como el eje correcto para un fenómeno del ES.** Ver
`L12` §9 para cómo cuenta.

# 3c. CTRL01-A — CORRIDO, 2026-09-05, por instrucción de Roberto. **REPRODUCE, en las dos ventanas.**

Código: `ctrl01_deriva_nocturna.py` (esta carpeta), salida: `salida_ctrl01.txt`. Datos: ES 1-min
2016-2019 por el cargador de G (`razon_escalas.cargar_con_sesion`, leído, no tocado): 1.007 sesiones
limpias, 1.357.785 barras. **La caja no se tocó.** Criterios sellados en el encabezado del script antes
de correr, en unidades de desvío porque la tabla en pb de BLW no estaba disponible.

**Chequeo de reloj, primero:** los tres minutos del este con mayor |retorno| medio de un minuto son
**15:59, 09:31 y 09:35** — el cierre de contado y la apertura de contado, en hora del este, con el horario
de verano manejado fecha por fecha. **El reloj está bien.**

| ventana | n | media | desvío | **t** | t esperada si estacionario | `θ_obs` | `θ_pub` | intervalo sellado | **veredicto** |
|---|---|---|---|---|---|---|---|---|---|
| **2:00-3:00 ET** | 1.006 | **+0,785 pb** | 12,24 pb | **+2,03** | 2,20 | **0,0641** | 0,0693 | [0,006; 0,132] | **REPRODUCE** |
| **1:30-3:30 ET** | 1.006 | **+1,409 pb** | 19,71 pb | **+2,27** | 2,60 | **0,0715** | 0,0819 | [0,019; 0,145] | **REPRODUCE** |

**Por año, 2:00-3:00:** 2016 +1,80 pb (t 1,80) · 2017 +0,43 (1,31) · 2018 +1,30 (1,49) · **2019 −0,41
(−0,57)**. La deriva no es pareja: 2019 es negativa. Es lo que se espera de un promedio de 23 años que
incluye años flojos; se anota, no se interpreta.

## Lo que el control dice, en su tamaño exacto

> ## **El instrumento de la casa —los datos, el cargador, el reloj y la aritmética— reproduce un resultado publicado sobre el ES por otro equipo, con la potencia que se declaró antes (t 2,0 contra 2,2 esperada) y con el punto estimado a un 8 % del publicado (0,064 contra 0,069).** Es la primera reproducción de un resultado externo sobre nuestro instrumento en 22 rondas.

**Y lo que NO dice, con la misma dureza:**
- **El criterio era débil por diseño**: el intervalo ±2 errores estándar admitía desde 0,006 hasta
  0,132. Que el punto haya caído a 8 % del publicado es más de lo que el criterio exigía, y es un dato,
  no una prueba de precisión.
- **Las dos ventanas no son independientes**: una contiene a la otra.
- **No cambia ningún veredicto de candidata.** L12 sigue ciega y fuera de F17: t = 2,0 antes de costos,
  y después de costos su propio paper dice 0,3 de Sharpe.
- **No es evidencia sobre el mercado**: 2016-2019 está adentro de la muestra de BLW.
- **Lo que sí cambia**: `D15` §3.1 tenía "mal calibrado, falsado por los controles inyectados"; ahora
  tiene además "reproduce un resultado publicado en el mismo instrumento". **El instrumento ve lo que
  hay cuando lo que hay es del tamaño que puede ver.**

**El desvío de la ventana 2:00-3:00, medido: 12,24 pb.** Mi estimación desde las cajas de G con ρ = 0
(`L12` §4) era 11,3: la correlación entre medias horas vecinas no es cero. Anotado como corrección de
un FRÁGIL por un medido.

# 4. Lo que el control NO es, escrito para que nadie lo convierta

- **No es una prueba de L12**: L12 está ciega y fuera de F17. Un control que reproduce no la resucita.
- **No produce una regla**: nadie opera la madrugada por esto. Si alguien quisiera, es una hipótesis
  nueva y cuesta un cartucho.
- **No toca la caja**: 2016-2019 solamente.
- **No cuenta como evidencia de mercado**: 2016-2019 está **adentro** de la muestra de ellos. Es una
  reproducción, y una reproducción sólo informa sobre el instrumento.

# 5. Qué le pido a Roberto y qué a G

| a quién | qué |
|---|---|
| **Roberto** | de SR 917: **la tabla de la deriva por hora** (media en pb y error estándar para 2:00-3:00), y de la **p. 27**: la definición del desbalance, el coeficiente, su `t` y la unidad. Y la decisión sobre los ~$30-40 si B se quiere exacto |
| **G** | correr A con los números sellados; decidir si B tiene potencia; y **el chequeo de reloj antes de cualquier "no reproduce"** |

**Costos:** dinero **cero para A; ~$30-40 FRÁGIL para B exacto, decisión de Roberto**. Cartuchos cero: es
un control. K en 261.
