# CTRL01 — CONTROL DEL INSTRUMENTO, no candidata: ¿nuestros datos reproducen la deriva nocturna publicada de Boyarchenko, Larsen y Whelan? **Diseño para la VENTANA G.**

**VENTANA L. NO MIDE NADA. K sigue en 261.** **Esto es un CONTROL**, del mismo tipo que los diez del juez:
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
