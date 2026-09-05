# ORDEN DE TRABAJO — los tests de mecanismo, por potencia

**VENTANA L. NO MEDIDO. K sigue en 261.**

**Éste es el orden en que conviene trabajar de ahora en adelante, y no se parece al orden del
índice.** El índice ordena por cuán cerca está cada candidata de un **veredicto operable**. Esto
ordena por cuán probable es que un test **enseñe algo**.

Las dos listas difieren a propósito. **Una ordena qué operar, la otra ordena qué aprender**, y con
once candidatas de las que ninguna es medible como ventaja, la segunda es la que tiene trabajo
disponible hoy.

---

## Cómo se estimó la potencia

El estadístico t escala con la raíz del número de observaciones, manteniendo fijos el tamaño del
efecto y la estructura de ruido:

```
t_esperado  =  t_publicado  ×  √( n_disponible_2016-2019  /  n_del_paper )
```

**Es una aproximación de orden, no una predicción.** Y supone que el efecto en 2016-2019 es el mismo
que en la muestra original, **que es justamente lo que el test quiere averiguar**. Sirve para
ordenar; no sirve para prometer.

Los `n` de los papers son estimados a partir del período y la frecuencia declarados. **Donde el paper
no publica un t utilizable, lo digo en vez de inventarlo.**

---

## La lista

| # | test | de dónde sale la potencia | n del paper | n disponible | **t esperado** | grado F7 |
|---|---|---|---|---|---|---|
| **1** | **M01-a — panel cambiario de fin de mes** (L08) | **10 monedas a la vez** | ≈ 1.040 | 480 | **≈ 3,4** | **A** |
| **2** | **M01-b — deriva contra la sorpresa publicada** (L03) | predictor exógeno fuerte: la sorpresa que salió | ≈ 296 | 192 | **≈ 2,7** | **C** |
| **3** | M01-e — primera media hora predice la última (L02) | serie diaria completa | ≈ 5.200 | 1.007 | ≈ 1,8 | C |
| **4** | M01-c — señal de rebalanceo **diaria** (L10) | la señal existe todos los días, no 12 veces al año | ≈ 6.550 | 1.007 | ≈ 1,4 | B |
| **5** | M01-d — reversión de la presión de precio (L01) | mi idea original, la menos potente | ≈ 9.500 | 1.007 | ≈ 1,0 | B |
| **6** | **M02 — el eje barato contra el caro** (L05) | no es una t: es una comparación de particiones | — | 1.007 | **no aplica** | C |
| 7 | flujo obligatorio contra precio de cierre (L04) | — | — | 1.007 | **no derivable del paper** | C |
| 8 | forma del pico y días *gotobi* (L07) | — | ≈ 3.700 | 1.000 | **no derivable del paper** | A− |

**Ocho tests. Cinco con potencia derivable, tres sin ella.**

---

## Lo que hay que leer en esta tabla

**Sólo uno cruza la vara de 3 desvíos, y es el de la candidata más inservible para operar.** L08 hace
doce operaciones por año y se queda corta por un factor de veintiocho como ventaja. Como test de
mecanismo es la más potente del inventario, **porque el panel de diez monedas multiplica la muestra
por diez y no hay que operar ninguna de las diez**.

Ése es el principio que reordena todo: **los filtros de pocos eventos y pocos instrumentos aplican a
operar, no a probar.**

**El segundo es de grado C, y eso es una virtud y no un defecto.** Los propios autores de L03
publicaron en 2022 que la deriva se debilita cuando se corta el acceso anticipado, y en Estados
Unidos hubo cortes equivalentes en 2013 y 2014, justo al final de su muestra. **La pregunta "¿siguió
existiendo en el ES entre 2016 y 2019?" tiene ahora una hipótesis previa concreta y un resultado
informativo en las dos direcciones.** Un efecto que ya sabemos que se debilitó es mejor sujeto de
prueba que uno del que no sabemos nada.

**M02 no tiene t porque no es un test de significación**, es una comparación entre dos formas de
etiquetar el mismo día. Va sexto en esta lista y **primero en costo**: no necesita datos nuevos y se
corre en una tarde. Ver la nota de orden práctico abajo.

**Los dos últimos no tienen t derivable y lo digo así.** Para L04 los resultados publicados están en
unidades de desvíos de flujo sobre acciones individuales; para L07 el paper describe la forma del
pico cualitativamente y no tabula un estadístico que se pueda escalar. **Un número inventado ahí
sería peor que ninguno.**

---

## Orden práctico, que no es el mismo que el de potencia

La lista de arriba ordena por lo que enseña. La de abajo agrega lo que cuesta.

| orden de ejecución | test | por qué acá |
|---|---|---|
| **1º** | **M02** | **cero datos nuevos, una tarde, y su resultado cambia si hace falta comprar el eje caro para todo lo demás** |
| 2º | M01-e y M01-d (L02 y L01) | cero datos nuevos. Baja potencia, pero el costo también es cero |
| 3º | M01-c (L10) | falta una serie diaria de bonos, gratis |
| 4º | M01-b (L03) | falta el calendario y el consenso de pronóstico, gratis, medio día de recolección |
| 5º | **M01-a (L08)** | **el más potente, y el único que exige comprar datos**: diez pares de divisas intradiarios más diez índices bursátiles diarios |

**Lo barato primero no es lo mismo que lo importante primero, y las dos listas están separadas a
propósito para que la decisión sea de Roberto y no quede escondida en un orden.**

---

## La condición que convierte todo esto en gasto de cartucho

Ninguno de estos ocho busca una ventaja, ninguno corre un estadístico contra un α para elegir entre
candidatas, y ninguno decide operar. Con ese argumento —el mismo que usaron la Compuerta 1 y el censo
de instrumentos— **no gastan cartucho y K se queda en 261**.

**Pero si el resultado de cualquiera de ellos se usa después para decidir CUÁL candidata medir,
entonces seleccionó, y ahí el cartucho se gasta.**

La forma de evitarlo es la de siempre y es de orden, no de técnica: **declarar antes de mirar qué se
va a hacer con cada resultado posible.** Cada test de esta lista tiene sus resultados posibles
escritos en `M01` o en `M02` antes de correrse.

**Quien ejecute tiene que sostener ese argumento en su propio pre-registro. No alcanza con citar este
documento.**
