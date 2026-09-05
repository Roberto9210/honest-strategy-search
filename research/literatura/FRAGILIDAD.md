# FRAGILIDAD — de cuántos números SIN MEDIR cuelga cada conclusión

**VENTANA L. NO MIDE NADA. K sigue en 261.**

**Marcar "estimación" al lado de un número no alcanza cuando una cadena entera cuelga de él.** Este
documento hace el inventario al revés: por conclusión, no por candidata.

**Regla: una conclusión que dependa de MÁS DE UN número sin medir va marcada FRÁGIL arriba de su
documento, no en una nota al pie.**

---

# 1. Los números sin medir que están en circulación

| # | número | dónde lo uso | quién debería medirlo |
|---|---|---|---|
| **E1** | **σ ≈ 60 pb**, desvío del retorno de cierre a cierre del ES | `P01`, `P03`, `P07`, `P08` | VENTANA G, pedido en `P10` |
| **E2** | σ ≈ 4,6 a 8 pb, desvío de USD/JPY en diez minutos | `P05` | con los datos de 6J, si se compran |
| **E3** | σ ≈ 20 pb, desvío de una moneda mayor en una hora | `P01`, para L08 | con los datos de 6E, si se compran |
| **E4** | `n_barras = 1.380` entre dos cierres consecutivos | `P07`, `P08` | VENTANA G, pedido en `P09` |
| **E5** | nocional del ES ≈ $130.000 en 2016-2019 | todos los documentos que convierten a dólares | derivable del dato que ya hay |
| **E6** | costo de ida y vuelta ≈ $17 | `PISO_Y_CONVERSION`, y todas las magnitudes netas | **suma mía de tres componentes medidos** |

**E5 y E6 son distintos de los otros cuatro: son aritmética mía sobre números que sí están medidos.**
Los cuento igual, porque una suma mal hecha rompe una cadena igual que una estimación mal hecha, pero
son verificables sin medir nada nuevo.

**Y hay dos huecos que NO son estimaciones y por eso no cuentan acá, pero hay que tenerlos presentes:**
la magnitud operable de L03, que está declarada desconocida, y el máximo de la excursión adversa a 30
minutos, que está declarado no publicado en `F8`.

---

# 2. Las conclusiones, con su cuenta

| conclusión | documento | depende de | **¿frágil?** |
|---|---|---|---|
| la prueba agrupada detecta el 64 % de la magnitud publicada | `P01`, `P03` | **E1, E3, E5, E6** | **SÍ — cuatro** |
| L07 sola detecta entre el 24 y el 42 % | `P05` | **E2, E5, E6** | **SÍ — tres** |
| L07 dominaría la prueba agrupada | `P05` | **E1, E2, E3** | **SÍ — tres** |
| L11 sola necesitaría el 186 % | `P07` | **E1, E5, E6** | **SÍ — tres** |
| L10 sola necesitaría el 204 % | `P08` | **E1, E5, E6** | **SÍ — tres** |
| los archivos del juez pasan la puerta | `P07`, `P08`, `P09` | **E4** | no — uno |
| ninguna candidata es medible con 2016-2019 | `FILTROS` | **E6** más la tabla de potencia **medida** | no — uno |
| en ES la exposición de cierre a cierre es indefendible y en MES no | `F8` | **ninguno**: todo sale de la Compuerta 1 | **NO** |
| ninguna conserva grado A con evidencia no superpuesta | `F7` | **ninguno**: son fechas de muestra verificadas | **NO** |
| el veredicto de `D02`, que retira mi propia idea | `D02` | **ninguno**: son fechas de muestra verificadas | **NO** |
| el recorte de Harvey y Liu empeora el inventario | `D03` | **ninguno**: `t` publicados y aritmética | **NO** |

## Lo que salta a la vista

**Las cinco conclusiones frágiles son TODAS de potencia, y CUATRO de las cinco cuelgan del mismo
número, E1.**

**Y las cinco conclusiones robustas son todas cualitativas o basadas en hechos ya medidos por la
VENTANA G.** Ninguna afirmación mía que dependa de una estimación propia es robusta, y ninguna que
dependa sólo de trabajo ajeno es frágil. **Eso no es casualidad y conviene tenerlo presente al leer
esta carpeta.**

---

# 3. Un matiz que la regla como está no captura

**No es lo mismo depender de un número sin medir SIN mostrar cuánto importa, que depender de uno y
mostrar el rango.**

En `P07` mostré que con `σ = 45 pb` en vez de 60 la conclusión no cambia: L11 sigue arriba de 1. **Esa
conclusión es más sólida que su cuenta de dependencias sugiere.** Lo mismo con `P05`, donde di cuatro
escenarios de `σ` y el peor sigue igualando a la agrupada.

**Refinamiento que propongo y no aplico solo:** una conclusión con una sola dependencia **y un rango
de robustez demostrado** podría dejar de ser frágil. Pero con más de una dependencia el rango habría
que mostrarlo en el producto de todas, y eso ya casi nunca se hace. **Dejo la regla como Roberto la
escribió y anoto el matiz.**

---

# 4. El agujero que este documento tapa para un caso y deja abierto en general

**Ninguno de los doce filtros del inventario pregunta de cuántos números sin medir depende una
conclusión.** Los filtros miran a las candidatas; ninguno mira a nuestras propias afirmaciones.

**Este documento es un inventario, no un filtro: hay que rehacerlo a mano cada vez que se agrega una
conclusión, y nada obliga a hacerlo.** La forma de filtro sería exigir que todo documento que
publique un número de potencia liste sus dependencias en el encabezado. **Lo aplico desde ahora en
los míos, y no puedo obligar a nadie más.**
