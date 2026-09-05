# D15 — Dos generadores, un resultado: el instrumento que nadie auditó. Con su condición de falla.

**VENTANA L. NO MIDE NADA. K sigue en 261.**

> ## ENUNCIADO
>
> **Dos generadores de hipótesis completamente distintos —261 nuestras y 11 de la literatura
> publicada— produjeron el mismo resultado: cero medibles.** El generador cambió y el resultado no.
> **Lo que no cambió entre las dos rutas es el instrumento de medición**, y nadie lo auditó desde
> afuera. Este documento lo audita, y termina con la observación que distinguiría *"el instrumento
> está mal"* de *"no hay nada que encontrar"*. **Si esa distinción no se pudiera escribir, este
> documento sería una excusa; se puede, y por eso no lo es. Pero su alcance es más chico de lo que
> la frase de arriba sugiere, y eso también va escrito.**

---

# 1. (a) Los parámetros que nunca se cuestionaron, y (b) si son decisión o restricción

| # | parámetro | valor | **decisión o restricción** | quién lo fijó |
|---|---|---|---|---|
| 1 | **la vara** | `t* = 3,0` por una variante; 3,7 por diez; 4,3 por cien | **decisión**, tomada de Harvey, Liu y Zhu. **Y es GENEROSA, no estricta: ver §2** | el juez |
| 2 | **el `n`** | cuatro años, 2016-2019 | **decisión**: la caja 2020-2026 se selló por elección; 2010-2015 no se compró (centavos). **Con una restricción real encima**: las épocas (`D14` §3) | el programa |
| 3 | **el instrumento** | ES y MES | **decisión con restricción**: sólo se compró ES; la plomería del juez para otros está no implementada con tercer candado | el programa, G |
| 4 | **el decaimiento** | `(c) = 0,42 × publicada` | **decisión**: un número externo (McLean y Pontiff) aplicado parejo a todo lo que salió en revista | esta ventana |
| 5 | **la resolución temporal** | barras de 1 minuto | **restricción del dato comprado**: no ve nada de menos de un minuto —la liquidación de 30 s del CME, el pico de segundos del fixing de Tokio— | el programa |
| 6 | **las formas de salida** | bracket o tiempo | **decisión del juez**: una salida por precio medio ponderado (L03) o por hora de reloj hay que forzarla a una de las dos | el juez |
| 7 | **el modelo de costo y de escala** | medio-spread 0,13 pt, comisión, drawdown $2.000, 1-4 contratos; piso $29-58 por operación | **restricción real**: es la cuenta de Roberto. **Pero convierte la pregunta**: el instrumento no mide *"¿existe el efecto?"* sino *"¿es rentable a esta escala con estos costos?"* | G, con la firma |
| 8 | **la potencia implícita** | CIEGA si `(c) < (a)`, con `(a) = t*·σ/√n` | **decisión**: exigir `(c) ≥ (a)` es diseñar con potencia ~50 % contra el efecto esperado. Generoso | esta ventana |
| 9 | **los filtros previos** | F1' exposición, F5 eventos, F6 medible-rentable | **decisión**: sacaron candidatas ANTES de medir | esta ventana, Roberto |
| 10 | **la contabilidad de multiplicidad** | un cartucho por hipótesis; K = 261; vara del programa `α = 0,05/K` | **decisión**, y correcta: es la que protege contra 261 intentos | el programa |

**Un parámetro que no está en la lista porque no es del instrumento sino del uso:** ninguna de las 11
se midió. **Las ocho ciegas se cerraron por la cuenta previa, no por el juez.** El juez, con la
literatura, no corrió una sola vez.

---

# 2. La vara de 3,0, verificada con el número exacto y no con la afirmación

Roberto: *"con K = 261, Bonferroni al 5 % pediría cerca de z = 3,9"*. **Verificado (`cuenta_anios.py`,
bisección sobre `erfc`):**

| | `α/K` | `z` |
|---|---|---|
| K = 261, **bilateral** | 1,916 × 10⁻⁴ | **3,730** |
| K = 261, unilateral | 1,916 × 10⁻⁴ | 3,551 |
| K = 262, bilateral | 1,908 × 10⁻⁴ | 3,731 |
| sin corrección, bilateral 5 % | — | 1,960 |

**Es 3,73, no 3,9; 3,9 correspondería a K ≈ 520.** Y el programa ya usa 3,73 como línea (la memoria de
la casa la registra como `α = 0,05/262`). **La conclusión de Roberto se sostiene con el número exacto:
3,0 está por DEBAJO de la vara del programa. El parámetro queda absuelto de "estricto": es generoso.**

**Consecuencia que no había escrito:** todos los márgenes de `D06`, `D13` y `D14` usan 3,0. Con la vara
del programa, **se multiplican por 3,0/3,73 = 0,80.** L03 en 5,75 años pasa de 1,03 a 0,83. **La cota
optimista era más optimista de lo que decía.**

---

# 3. (c) LA CONDICIÓN DE FALLA — qué observación distingue "mal calibrado" de "no hay nada"

**Primero la trampa, con nombre:** *"el instrumento es demasiado estricto"* es exactamente lo que dice
quien no encontró nada y no quiere aceptarlo. Por eso la distinción tiene que ser una **observación**,
no un argumento.

## 3.1 "Mal calibrado" es falsable, y ya se falsó

**Un instrumento mal calibrado no recupera un efecto de tamaño conocido que se le inyecta, o produce
falsos positivos con un placebo.** Los dos controles existen en la casa: el control 3 de G (ventaja
inyectada) y el control 2 (placebo de signo), y **los siete controles del juez pasan** (commit
`ea720df`). **El instrumento recupera lo que dice recuperar, al umbral que dice tener.**

> ## **"Mal calibrado" está falsado por los controles. El instrumento no está mal: mide exactamente lo que fue diseñado para medir —rentabilidad a escala de firma de fondeo, con vara 3,0, en cuatro años de un instrumento— y lo mide bien.**

## 3.2 Entonces la pregunta real es otra: ¿tuvo POTENCIA contra lo que se le pidió encontrar?

**La observación que distingue "no hay nada" de "no se podía ver":**

> **Una prueba con potencia —`(c) ≥ (a)`, el efecto esperado por encima del umbral— que devuelve
> negativo, es evidencia de que no hay nada. Una prueba sin potencia que devuelve negativo no es
> evidencia de nada: es el instrumento devolviendo su propio umbral.**

**El conteo, para la ruta de la literatura:** de once candidatas, **cero** tuvieron potencia contra su
magnitud esperada (`D06`, `D13`). **Once resultados negativos, cero informativos sobre el mercado; once
informativos sobre el instrumento.**

**El conteo, para las 261:** **NO ESTÁ HECHO**, y es la auditoría que este documento pide y no hace.
`REGISTRO_JUEZ.jsonl` tiene, para cada prueba, la resolución del juez. La pregunta por fila es: **¿la
magnitud que la hipótesis afirmaba estaba por encima de la resolución con la que se la juzgó?** Cuántas
sí, cuántas no.

## 3.3 La condición de falla de ESTE documento, con la dureza de una candidata

| si la auditoría de las 261 muestra que… | entonces |
|---|---|
| **una fracción sustancial tuvo potencia y aun así dio negativo** | **la explicación "instrumento" MUERE para la ruta propia.** Este documento queda reducido a la ruta de la literatura: once sin potencia, y nada más |
| **casi ninguna tuvo potencia** | el resultado del programa —272 negativos— es **un resultado sobre el alcance del instrumento, no sobre el mercado**, y hay que decirlo así en cualquier cierre |
| **la única prueba con potencia alcanzable (L03 con 2014-2015, `D14`) se corre y da negativo** | "no hay nada" gana para esa candidata, con número, y es la primera vez que se puede decir |

**Y las movidas que convertirían este documento en la excusa que Roberto teme, declaradas prohibidas:**
bajar `t*`; agregar años hasta que algo cruce; cambiar el 0,42; contar como "con potencia" una prueba
después de ver su resultado. **Cualquiera de las cuatro anula el documento.**

---

# 4. Lo que el documento afirma, reducido a su tamaño exacto

1. El instrumento **no está mal calibrado**: los controles lo prueban.
2. El instrumento **mide rentabilidad a escala, no existencia**, y a esa pregunta contestó *no* 272
   veces.
3. **Para la ruta de la literatura, ninguna de las once pruebas tenía potencia**, así que las once son
   informativas sobre el instrumento y no sobre el mercado.
4. **Para la ruta propia, no se sabe**, y saberlo es una auditoría de una tarde sobre un archivo que
   existe.
5. **La vara es generosa, no estricta**, y con la del programa los márgenes bajan otro 20 %.

**Costos:** dinero cero, cartuchos cero, K en 261. Tiempo de Roberto: leer, y decidir si la auditoría
del punto 4 se hace.
