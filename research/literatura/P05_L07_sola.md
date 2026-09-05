# P05 — L07 sola: la prueba más barata y mejor apuntada del inventario

**VENTANA L. NO CORRIDO. Borrador de pre-registro. K sigue en 261.**
> ## FRÁGIL — las cifras de potencia de este documento dependen de números SIN MEDIR: **E1, E2, E3, E5 y E6**.
> Ver [FRAGILIDAD.md](FRAGILIDAD.md). Las conclusiones cualitativas no dependen de ellos; **las tablas de potencia sí**.

Al levantar el bloqueo de magnitud de L07 apareció algo que cambia el plan B de `P04`:
**L07 no sustituye a L08 dentro de la prueba agrupada, porque la dominaría. Se corre sola, y así es
más barata y está mejor apuntada que la prueba agrupada entera.**

---

# Lo que el paper publica, y es una regla completa

Ito y Yamada (2017), *Journal of International Economics* 109, sección 5.2:

| pieza | valor publicado |
|---|---|
| **regla** | largo USD/JPY cinco minutos, corto los cinco siguientes, **cambio en el instante del fixing** |
| **momento** | 00:55 GMT, todos los días hábiles |
| **magnitud** | **1,8 puntos básicos** |
| muestra | 15 años |
| atípicos | 1 % superior e inferior truncados |
| calendario | el retorno es *"particularmente alto"* los días 5 y 10, y el 31 o fin de mes |

**Las tres piezas que el criterio `F9` exige —momento, signo y magnitud— están las tres en el paper.
No hace falta que pongamos nada.** Es la única candidata del inventario donde eso pasa sin
condiciones.

---

# La hipótesis

> **La regla publicada por Ito y Yamada conserva su signo y al menos una cuarta parte de su magnitud
> publicada de 1,8 puntos básicos en USD/JPY entre 2016 y 2019.**

`θ = E[z] ≥ 0,25` contra la nula `θ = 0`, con `z = retorno realizado / 1,8 pb`.

El umbral 0,25 es **el mismo de `P01` y no se toca**, por la misma razón: moverlo después de calcular
la potencia sería ajustar la vara al instrumento.

---

# La potencia, y el número que la vuelve atractiva

`t(θ=1) = r · √n`, con `r = 1,8 / σ` y `σ` el desvío del retorno de la ventana de diez minutos.

| σ supuesto | `r` | n = 1.000 días | `t(θ=1)` | **θ mínimo detectable a 3,0 σ** |
|---|---|---|---|---|
| 4,6 pb | 0,39 | 1.000 | 12,3 | **0,24** |
| 6 pb | 0,30 | 1.000 | 9,5 | **0,32** |
| **8 pb, conservador** | **0,22** | 1.000 | **7,1** | **0,42** |
| 12 pb, muy conservador | 0,15 | 1.000 | 4,7 | 0,63 |

**Aun en el escenario muy conservador iguala a la prueba agrupada completa con L08 adentro, que da
0,64. En el escenario conservador la supera con holgura.**

**`σ` es una estimación mía y hay que medirlo.** Sale de un desvío diario típico de USD/JPY de unos
55 puntos básicos repartido en la ventana. **Se mide sobre los datos comprados, antes de mirar
ningún signo, y se commitea. Igual que en `P01`.**

---

# El costo, contra el de la prueba agrupada

| | prueba agrupada con L08 | **L07 sola** |
|---|---|---|
| símbolos | 6 | **1**, sólo 6J |
| fechas | 48 | 1.000, todas las sesiones |
| ventana por fecha | 4 horas | **10 minutos** |
| esquema | ohlcv-1m | ohlcv-1m |
| θ mínimo detectable | 0,64 | **0,24 a 0,42** |

**Un solo símbolo y diez minutos por día.** Si el proveedor cobra por volumen es la compra más chica
que este proyecto haya considerado. **La cotiza la VENTANA G con el script que ya existe.**

---

# El control que el propio paper regala

**El paper predice que el retorno es *particularmente alto* los días 5 y 10 y a fin de mes.** Eso es
una predicción publicada sobre una partición de calendario externa, y se puede contrastar sin datos
adicionales.

**Control de calendario, con su condición de falla:**

```
θ̂(días gotobi)   contra   θ̂(días no gotobi)
```

| resultado | qué significa |
|---|---|
| gotobi > no gotobi, las dos positivas | el efecto y su condicionamiento de calendario transfieren |
| las dos positivas e **iguales** | el efecto transfiere pero **el calendario no explica nada**. La historia de los pagos corporativos queda sin apoyo |
| **las dos negativas** | el efecto no transfiere |
| **no gotobi > gotobi** | **condición de falla**: contradice al paper, y hay que revisar la construcción antes de interpretar nada |

**Ojo con una tentación que declaro cerrada ahora:** la magnitud publicada de 1,8 pb es el promedio
de **todos los días**. El paper **no tabula** un número para los días gotobi, sólo dice que es más
alto. Por la regla `P02`/R1 —que exige un número, no una descripción— **el denominador es 1,8 pb para
los dos grupos**. Usar un denominador distinto para gotobi sería inventarlo.

---

# Los otros controles

**Control 1 — Placebo de hora.** Repetir la regla con el cambio a las 00:25 y a las 01:25 GMT.
**Falla si el placebo da `t ≥ 2,0`**: el efecto sería del método y no del fixing. El paper afirma
justamente que el retorno anormal *"es muy distinto del de cualquier otro momento del día"*, así que
este control contrasta una afirmación publicada.

**Control 2 — Placebo de signo.** Signo al azar, mil repeticiones. **Falla si la distribución de `t`
no está centrada en cero.**

**Control 3 — Ventaja inyectada.** Sumar `0,5 × 1,8 pb` a cada evento. **Falla si `θ̂` no sube en
aproximadamente 0,5.**

**Control 4 — Truncamiento.** El paper trunca el 1 % superior e inferior. **Se replica ese
truncamiento, y se reporta también sin truncar. Falla el veredicto si las dos versiones difieren**,
porque entonces lo decide la cola y no el efecto.

**Control 5 — Liquidez.** El paper afirma que la falta de liquidez no explica el retorno.
**Se reporta el volumen de la ventana. Falla la interpretación si el efecto vive sólo en los días de
volumen más bajo**, porque entonces es un artefacto de horario delgado y no el fixing.

---

# Qué NO prueba, escrito antes

- **NO prueba que sea operable, y hay evidencia publicada de que no lo es.** Los propios autores
  dicen que 1,8 pb está *apenas por encima del costo del diferencial*. En 6J son unos **$21 brutos
  por evento**. **Un positivo acá no produce una estrategia.**
- **NO se traslada al presente.** `F10` encontró que la anomalía se vende como robot de MetaTrader
  desde alrededor de 2023, y que hay un paper académico de 2023 cuyo título trata sobre su
  popularidad. **Un positivo sobre 2016-2019 no dice nada sobre 2026.**
- **NO habla de ES.** Es USD/JPY.

# Entonces, ¿para qué correrla?

**Porque contesta la pregunta central de esta ventana por el precio más bajo del inventario:
¿transfieren las reglas publicadas por terceros a un período fuera de su muestra?**

L07 es el caso más limpio que existe para preguntarlo: **momento, signo y magnitud los pone el paper,
no nosotros; la muestra es de quince años; los atípicos ya están tratados; y hay un control de
calendario y uno de hora publicados como predicciones.**

**Si las reglas de terceros no transfieren ni acá, la prueba agrupada sobre L11, L10 y L08 tiene mucho
menos sentido. Y si transfieren acá, la agrupada vale más.** En los dos casos, **L07 sola va
primero**, y cuesta una fracción.
