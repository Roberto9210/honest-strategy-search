# D04 — Jensen, Kelly y Pedersen: ¿aplica su marco al nuestro?

**VENTANA L. NO MIDE NADA. K sigue en 261.**

**Jensen, Theis Ingerslev; Kelly, Bryan; Pedersen, Lasse Heje (2023). "Is There a Replication Crisis
in Finance?"** *Journal of Finance* 78(5), 2465-2518.
https://onlinelibrary.wiley.com/doi/full/10.1111/jofi.13249

---

# PRIMERO, LA REGLA NUEVA, aplicada a esto mismo

> **`F12`: ANTES DE DISCUTIR UN CAMBIO DE MÉTODO, CALCULAR SI CAMBIARÍA ALGÚN VEREDICTO ACTUAL. SI NO
> CAMBIA NINGUNO, NO SE DISCUTE.**

**El cálculo, antes de leer nada en profundidad:**

| veredicto actual | ¿lo cambiaría un marco jerárquico bayesiano? |
|---|---|
| ninguna candidata es medible sola con 2016-2019 | **no**: el límite son los eventos, no la inferencia |
| no registrar L11 ni L10 por separado | **no**: por lo mismo |
| la prueba agrupada es la mejor apuesta con un cartucho | **no, y es más sutil**: ver abajo |
| L07 sola es la más barata | **no** |
| ninguna conserva grado A | **no**: eso lo deciden fechas de muestra |

**La respuesta es no en las cinco. Por `F12`, no se discute más, y este documento termina acá.**

**Cumplo con la regla y a la vez contesto la pregunta que Roberto hizo, porque contestarla ya está
hecho al aplicarla.**

---

# La respuesta, en tres párrafos

**Su marco NO aplica, y el motivo es una precondición que no cumplimos.**

**Lo que hacen:** un modelo bayesiano jerárquico sobre **153 factores agrupados en 13 temas**, con
datos de **93 países**. La jerarquía permite que cada factor "tome prestada fuerza" de la
distribución estimada del conjunto. **Por eso la evidencia se fortalece con el número de factores
observados en vez de debilitarse: más factores estiman mejor la distribución compartida.**

**Por qué no aplica:** ese préstamo de fuerza **exige estimar la distribución compartida, y para eso
hacen falta muchas unidades**. Nosotros tenemos **once candidatas, en mercados sin relación, con
mecanismos distintos** —cobertura de gamma, prima de riesgo, mandato institucional, desbalance de
órdenes de clientes—. **No son extracciones de una distribución común: son objetos distintos.** Con
tres unidades en la prueba agrupada, un modelo jerárquico **degenera exactamente en el modelo
agrupado que `P01` ya usa.**

**Y el punto que lo cierra: nuestra restricción es de POTENCIA, no de inferencia.** Un prior mejor
cambia cómo se combina la evidencia; no crea eventos. L11 tiene 128 y L10 tiene 48, y ningún prior
los multiplica.

---

# Lo que sí vale la pena llevarse, y ya lo estábamos haciendo

**El mecanismo de su marco —tomar prestada fuerza entre unidades para superar la falta de potencia
individual— es exactamente lo que hace la prueba agrupada de `P01`.**

`P01` es una versión pobre y de tres unidades de lo que ellos hacen con 153. **Que un paper del
*Journal of Finance* llegue a la misma idea desde el otro lado es una confirmación externa del
diseño de `P01`, no una alternativa a él.**

Y hay un detalle de su resultado que sí toca el diagnóstico central de este proyecto, aunque no
cambie ningún veredicto: encuentran que los factores **funcionan fuera de muestra en 93 países**.
**El remedio que ellos usan contra la selección es el mismo que yo propuse y perdí en `D02`: datos
nuevos.** Con la diferencia de que ellos los tienen y nosotros no.

---

# La tentación que declaro cerrada

**Su resultado es que la mayoría de los factores replica.** Leído sin cuidado, eso dice "la
literatura es más confiable de lo que temíamos" y sube el valor de todo este inventario.

**No lo uso para eso, por dos motivos:**

1. **Es sobre factores transversales de acciones**, que es el objeto que este proyecto no puede
   operar. Nuestro inventario es de efectos intradiarios y de calendario en futuros. **No hay razón
   para trasladar su tasa de replicación.**
2. **Es exactamente la clase de argumento que `D02` acaba de enseñarme a desconfiar: me convencería
   justo cuando sube el valor de lo que ya tengo.**

**Cerrado.**
