# P09 — Pedido a la VENTANA G: verificar la cañería, no la hipótesis

**VENTANA L. NO GASTA CARTUCHO. K sigue en 261.**

**La distinción SE PUEDE hacer limpio con el código como está.** Leí `juez.py` para averiguarlo, y
abajo está por qué, con las dos partes que sí se pueden verificar sin costo y **la que no**.

---

# 1. Por qué se puede, leído del código

```
juzgar()  línea 701:   validar(cand)          ← primero, y es puro
          línea 702+:  hash, timestamps, caja sellada
          línea 731+:  mapear a barras         ← acá recién aparecen los datos
```

**`validar(cand)` es una función pura del JSON del candidato.** No toca el mercado, no toca el
registro, no calcula nada. Y `main()` la alcanza sólo después de `cargar_mercado()`, pero **eso es un
accidente del orden en `main`, no una dependencia de `validar`.**

Lo que `validar()` sí verifica, leído de las líneas 162-207:

- campos obligatorios presentes;
- `instrumento` conocido;
- `variantes_probadas ≥ 1`;
- `clase_ventaja` dentro de los valores permitidos;
- `contratos` y `limite_contratos ≥ 1`;
- `regla_salida.tipo` es `bracket` o `tiempo`, y trae los campos que ese tipo necesita;
- hay operaciones, y cada una tiene `ts` y `lado` válidos.

Y **el rechazo por clave que suena a resultado** (líneas 142-152) recorre el JSON entero y también es
puro.

## Lo que NO escribe nada

**`anotar()` se llama dentro de `juzgar()` y desde `main()` en el camino de NO MEDIBLE. `validar()`
no llama a `anotar()`.** Confirmado: **verificar el formato no deja rastro en el registro encadenado
y por lo tanto no gasta cartucho.**

---

# 2. El pedido concreto

**Correr sólo esto, sobre los dos archivos de `P07` y `P08`:**

```python
from juez import validar, sin_resultados
import json
for ruta in ("L11_borrador.json", "L10_borrador.json"):
    cand = json.load(open(ruta, encoding="utf-8"))
    sin_resultados(cand)     # el rechazo por clave
    validar(cand)            # el resto de la puerta
    print(ruta, "PASA LA PUERTA")
```

**Sin `cargar_mercado()`, sin `juzgar()`, sin `anotar()`.** Es probar la cañería.

## Lo que hay que confirmar, en tres preguntas

1. **¿Pasan la puerta?** Formato, campos obligatorios, `clase_ventaja` leído correctamente.
2. **¿`clase_ventaja: "direccional"` es un valor aceptado tal como lo escribí?** El documento lo dice
   pero quiero que lo confirme el código, no la documentación.
3. **¿`regla_salida.tipo: "tiempo"` con `n_barras` grande es aceptado, o hay un tope?** No encontré
   un límite superior en `validar()`, pero puede haberlo más adelante.

---

# 3. LO QUE NO SE PUEDE VERIFICAR SIN COSTO, y lo digo en vez de forzarlo

**Dos cosas quedan afuera de la puerta y no se pueden probar sin datos:**

**a) Que los instantes caigan sobre barras reales.** El chequeo vive en el mapeo a barras, después de
la puerta, y necesita el mercado cargado. El juez tiene la categoría **NO MEDIBLE por "entradas fuera
de los datos"** justamente para eso. **Mis timestamps de las 15:00 hora central podrían no coincidir
con una barra en días de cierre anticipado o feriado**, y eso no lo sé hasta que alguien lo mire.

**b) Cuántas barras de un minuto hay entre dos cierres consecutivos.** Puse `n_barras: 1380` y **es
mi cuenta, no la verifiqué**. Depende de cómo el juez cuente el corte nocturno.

**Las dos se resuelven con un script de tres líneas que cargue `m = cargar_mercado()` y consulte el
índice sin llamar a `juzgar()`.** Eso técnicamente toca los datos, pero **no calcula ningún retorno,
ningún desenlace y ninguna nula: sólo pregunta si un instante existe en el índice y cuántas barras
hay entre dos**.

**Si la VENTANA G considera que eso ya es medir, no lo hace y lo dejamos anotado como pendiente.** No
fuerzo la distinción: la línea la traza quien es dueño del juez, no yo. **Lo que sí afirmo es que la
parte del formato (sección 2) es inequívocamente gratis.**

---

# 4. Lo que este pedido NO es

**No es una corrida del juez.** No devuelve veredicto, no toca el registro, no permite inferir nada
sobre los datos ni sobre las candidatas.

**Y no habilita nada.** Que los archivos pasen la puerta no acerca la decisión sobre el cartucho: la
aritmética de `P07` y `P08` ya dice que ninguna de las dos conviene registrarse sola. **Esta
verificación existe para que, si alguna vez se registra algo, no se pierda un cartucho por una coma.**
