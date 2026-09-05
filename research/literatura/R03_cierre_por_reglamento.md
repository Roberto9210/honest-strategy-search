# R03 — Qué le pasa a cada candidata según lo que diga el reglamento de la firma. ESCRITO ANTES DE SABER LA RESPUESTA.

**VENTANA L. NO MIDE CANDIDATAS; corre CONTROLES DEL INSTRUMENTO desde el 2026-09-05 (rol ampliado por Roberto, ver `INDICE`). K sigue en 261.**

> ## SELLADO
>
> Roberto va a leer las filas 7, 8 y 9 de `F16` en el sitio de la firma. **Este documento fija qué
> pasa con cada candidata en cada rama ANTES de que él reporte.** Escribirlo antes es lo que impide
> acomodar la lectura al resultado; misma disciplina que la lectura A/B de `R01` y `R02`.
> Se commitea sin la respuesta, y el historial es la prueba.

---

# Rama 1 — ¿Están permitidos 6J y 6E? (fila 7)

## Si NO están permitidos

| candidata | qué pasa | apelación |
|---|---|---|
| **L07** | **MUERTA.** Su instrumento es 6J y no hay sustituto en ES | **ninguna.** No es una limitación de medición: es una prohibición de operar |
| **L08** | **MUERTA.** Su instrumento son las divisas mayores (6E, 6J, 6B, 6A) | **ninguna** |
| L10 | **no cambia.** Su pata operable es ES; la pata ZN es del paper, no de la regla que se operaría | — |
| el resto | no cambia | — |

**Consecuencia para `T02`:** la "medición que nadie puede hacer" deja de tener sentido hacerla. Se cierra
sin gastar los USD 0,31 ni el trabajo de G.

## Si SÍ están permitidos

| candidata | qué pasa | qué haría falta para medirla |
|---|---|---|
| **L07** | **viva, no medible hoy** | los datos (USD 0,06), un cargador de `ohlcv-1m` de divisas, y la comisión de divisas (fila 10). Para **juzgarla**, además la plomería del juez que G declaró no implementada con tercer candado |
| **L08** | **viva, no medible hoy** | lo mismo con USD 0,25 |

**Y una condición que va con esta rama:** si están permitidos **sólo los micros** (M6E, no 6E), la
holgura cambia y la ficha de calibración es otra. Se anota cuál.

---

# Rama 2 — ¿Hay restricción de operar alrededor de publicaciones económicas? (fila 8)

**La forma exacta de la regla decide, así que se escriben las tres formas que existen en las firmas:**

| forma de la regla | L03 | L11 | las demás |
|---|---|---|---|
| **A. "no se puede tener posición abierta durante una publicación"** (±X minutos) | **MUERTA.** Entra 09:30, la publicación es 10:00, sale 10:00:05-10:01. Está adentro por construcción | **MUERTA.** Su regla es tener posición todo el día del anuncio, cierre a cierre; la publicación cae adentro | no cambian, ver abajo |
| **B. "no se pueden enviar órdenes nuevas ±X minutos"** | **MUERTA** si X ≥ 1 min: su salida es una orden a 10:00:05. Si la regla permite salidas y prohíbe sólo entradas, sobrevive con la entrada a 09:30 fuera de la ventana; **se anota cuál** | **viva**: entra al cierre anterior y sale al cierre, ninguna orden cerca de la publicación | no cambian |
| **C. la regla se aplica sólo a una LISTA de publicaciones** | **depende de la lista.** Los cuatro anuncios de L03 son ISM manufacturero, ISM no manufacturero, viviendas pendientes y viviendas usadas. Si la lista incluye a los ISM y no a la NAR, **L03 queda con 96 eventos en vez de 192 y su margen ciego de 0,86 baja a 0,61** | depende de si la lista incluye inflación, desempleo y FOMC, que son los suyos. Si los incluye, como en A | no cambian |

**Las demás, revisadas una por una para que nadie las dé por no tocadas sin mirar:**

| candidata | ¿cae en una ventana de publicación? |
|---|---|
| L01 | última media hora del contado, 15:30-16:00. **No hay publicaciones programadas ahí.** Las decisiones del FOMC son a las 14:00 y las conferencias a las 14:30: fuera. No cambia |
| L10 una hora | 15:00-16:00 del último día hábil. Idem: fuera. No cambia. **L10 publicada** —cierre a cierre— cae bajo la forma A si el día siguiente tiene publicación; ya está ciega |
| L07 | 00:50-01:00 GMT. El fixing de Tokio **no es una publicación económica** y no figura en los calendarios que las firmas usan. No cambia |
| L08 | hora previa a las 16:00 de Londres = 10:00-11:00 del este en invierno. **Ojo: las publicaciones de las 10:00 del este caen en el borde de esa hora.** Bajo la forma A, los fines de mes con publicación a las 10:00 quedan afuera: se anota cuántos de los 47 |
| L02, L04, L05, L06, L09 | ya cerradas o no evaluables; no cambia nada |

## Si NO hay restricción

**Todo sigue igual.** L03 sigue ciega por 0,86 (`D13`), y `D11` sigue como costo nombrado.

---

# Rama 3 — ¿Se puede mantener posición a través del corte de 16:00-17:00 CT y de noche? (fila 9)

**No la pidió Roberto en esta tanda, pero es la que toca a L11 y la escribo antes de saber por la misma
razón.**

| si | L11 | L10 publicada |
|---|---|---|
| **NO se puede mantener de noche** | **MUERTA en su forma publicada**: la prima de Savor y Wilson es cierre a cierre, y el cierre anterior es del día previo. Una versión "sólo sesión de contado" sería un grado de libertad nuestro y tendría **menos** magnitud | ya ciega; además inoperable |
| **SÍ se puede, con límite de contratos nocturno** | viva en la forma publicada, con el límite anotado en la ficha | ya ciega |

---

# EJECUCIÓN — 2026-09-05, con las respuestas leídas por Roberto en `help.tradeify.co`

**Hecho medido por la casa (`F16` en acción):** Roberto leyó las páginas oficiales de la firma el
2026-09-05. Lo que encontró, y el veredicto de cada rama **aplicando el documento tal como se selló,
sin reinterpretarlo**:

| rama | lo que dice la firma | veredicto sellado que aplica |
|---|---|---|
| **1 — 6J y 6E** | **están en la tabla de tarifas**: 6J $6,20, 6E $6,20, M6E $1,60 ida y vuelta. Operables, y no sólo los micros | **"Si SÍ están permitidos": L07 y L08 VIVAS, NO MEDIBLES HOY.** La fila 10 de `F16` (comisión de divisas) queda resuelta: $6,20 |
| **2 — publicaciones** | **sin ninguna restricción**, texto literal *"free reign"*; Roberto verificó la política completa, no el resumen | **"Si NO hay restricción: todo sigue igual."** L03 sigue ciega por 0,86 (`D13`); `D11` sigue como costo nombrado |
| **3 — noche** | **PROHIBIDO.** Todo cerrado a las 16:45 del este, 12:59 en cierre temprano; lo cierran ellos, sin penalidad | **"NO se puede mantener de noche": L11 MUERTA en su forma publicada.** L10 publicada: ya ciega, y además inoperable |

> ## **Veredicto: la rama de la noche mata a L11 publicada. Ninguna otra rama mata a nadie. Coincide con la lectura de Roberto, y el veredicto sale del documento sellado, no de la lectura.**

## Estado final de L07 y L08, con precisión

> **L07 y L08 NO mueren por reglamento. Siguen bloqueadas por la plomería del juez que la VENTANA G
> declaró NO IMPLEMENTADA, con un tercer candado que se niega aunque se complete la ficha.** Es una
> limitación de medición, no una prohibición de operar. **Si algún día la plomería se habilita, las dos
> vuelven al estado "requiere medición" de `D06` con sus márgenes sin corregir (1,72 y 1,33) y la
> corrección pendiente de `T02`.**

## Lo que el reglamento trajo y R03 no había previsto — dos agujeros, y uno le toca a L07

1. **La sesión de la tarde-noche.** *"Todo cerrado a las 16:45"* es una regla sobre TENER posición al
   cierre; **no dice si se pueden abrir y cerrar operaciones entre las 18:00 del este y las 16:45 del
   día siguiente.** L07 opera a las **00:50-01:00 GMT = 19:50-20:00 o 20:50-21:00 del este**, diez
   minutos, sin cruzar ningún cierre. **R03 no la puso en la rama 3 y debió ponerla.** Su operabilidad
   depende de una línea que la lectura de Roberto no incluye. Queda como **fila 11 de `F16`**: *¿se
   puede operar en la sesión de Globex de la tarde-noche, entre las 18:00 y las 16:45 del este?*
2. **Consistencia** (ningún día > 35-40 % de la ganancia; 20 % en Lightning fondeada). Para una
   candidata de 12 eventos al año, un solo evento puede ser más del 35 % de la ganancia de una
   evaluación. **Toca a cualquier candidata de pocos eventos —L10 en una hora, ya cerrada por `D16`—
   y es una razón más para `F17`.**

**Y dos reglas nuevas que no tocan a las once y sí a lo que viene:** microscalping (tenencia > 10 s en
más del 50 % de las operaciones y de la ganancia) y *"No High-Frequency Trading bots"* sin definición.
Van adentro de `F17`.

---

# La lectura, fijada ahora

- **Ninguna rama resucita a nadie.** Una regla de firma puede matar; no puede convertir una ciega en
  visible.
- **La rama más probable que mata más:** 2-A. Mata a L03 y a L11 de una vez.
- **Si Roberto reporta algo que no cae en ninguna forma de arriba, se agrega la forma y se aplica; no
  se fuerza a la más parecida.**

**Costos:** dinero cero, cartuchos cero, K en 261. Tiempo de Roberto: cinco minutos en el sitio de la
firma, con la lista de `F16`.
