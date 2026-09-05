# P10 — Pedido a la VENTANA G: medir el desvío del que cuelgan cinco documentos

**VENTANA L. NO GASTA CARTUCHO. K sigue en 261.**

**Los 60 puntos básicos que uso como desvío de cierre a cierre son una estimación mía, no una
medición.** Aparecen en `P01`, `P03`, `P07`, `P08` y en la tabla de `FILTROS`, y **toda la aritmética
de potencia del inventario cuelga de ese número.**

**Y probablemente lo estimé bajo, lo que empeoraría las cuentas. Lo pido igual.**

---

# 1. De dónde salió mi estimación, para que se vea qué hay que reemplazar

De la Compuerta 1: la mediana del movimiento nocturno absoluto es **8,75 puntos**. Convertida a un
desvío suponiendo normalidad da 12,97 puntos, que a un nivel de índice de 2.600 son **49,9 puntos
básicos**. Redondeé a **60** para dejar margen por la cola.

**Y la serie tiene cola gorda medida: el percentil 99 es 71,81 puntos contra una mediana de 8,75.**
En una normal ese cociente sería 3,45 y acá es 8,2. **La conversión desde la mediana subestima el
desvío verdadero.**

---

# 2. Qué medir, exactamente

## La variable

```
r(t)  =  log( C(t) / C(t-1) )      en PUNTOS BASICOS del nivel del indice
```

donde `C(t)` es el precio del ES en la barra de un minuto del **cierre de la sesión**, y `C(t-1)` el
de la sesión anterior. **Es el retorno de cierre a cierre de una sesión, que es la ventana de las
dos candidatas.**

**En puntos básicos y no en puntos de índice**, porque el nivel del ES sube de ~1.900 a ~3.200 en el
período y un desvío en puntos mezcla dos escalas distintas. **La VENTANA G ya tomó esa decisión para
el eje de régimen (`juez_regimen_bps.py`), así que es la unidad de la casa.**

## Sobre qué fechas — y son cuatro conjuntos, no uno

| conjunto | qué es | para qué |
|---|---|---|
| **A — todas** | las 1.007 sesiones de 2016-2019 | referencia general |
| **B — días de anuncio** | las sesiones donde cae un anuncio macro programado | el `σ` de **L11** |
| **C — últimos días hábiles de mes** | 48 sesiones | el `σ` de **L10** |
| **D — el complemento de B** | sesiones sin anuncio | el contraste |

**B y C son los que importan. A y D existen para ver si B y C son distintos del resto**, que es
justamente lo que sospecho.

**Si las fechas de B todavía no están recolectadas** (`P07` sección 1 explica por qué no las
transcribí), **medir A y C igual: A es inmediato y C se calcula del calendario sin ninguna fuente
externa.**

## Con qué estimador

**Tres, y los tres reportados juntos:**

1. **Desvío muestral clásico.** Es el que entra en la fórmula de potencia.
2. **Desviación absoluta mediana escalada por 1,4826.** Robusto a la cola.
3. **Rango intercuartílico dividido por 1,349.** Segundo robusto, para contraste.

**Los tres, porque la diferencia entre ellos ES el resultado.** Si el clásico es mucho mayor que los
robustos, la cola domina, y entonces la fórmula de potencia que uso —que supone que el desvío resume
la dispersión— está mal aplicada y hay que decirlo.

**Y el conteo de sesiones de cada conjunto, siempre**, para que la raíz de n de mis cuentas se pueda
verificar.

---

# 3. Por qué esto NO destapa nada

**La dispersión de un retorno no depende del signo que una regla predice.** Se puede medir sobre el
valor absoluto y sobre todas las sesiones sin mirar ninguna candidata, ninguna fecha de entrada y
ningún lado.

**No hay operaciones, no hay nulas, no hay veredicto y no se toca el registro encadenado.** Es el
mismo estatus que los hechos medidos del ES que ya están en `HECHOS_MEDIDOS_ES.md`: propiedades del
mercado, no ventaja.

---

# 4. Qué se hace con el resultado, declarado antes

| resultado | consecuencia |
|---|---|
| `σ(B)` y `σ(C)` cerca de 60 pb | las cuentas de `P01`, `P07` y `P08` quedan como están |
| **`σ` mayor que 60** | **las candidatas necesitan todavía más de su magnitud publicada.** Es lo que espero, porque los días de anuncio son días de volatilidad alta |
| `σ` menor que 60 | mejoran, y hay que rehacer las tablas de potencia de los cinco documentos |
| clásico ≫ robustos | la fórmula de potencia no aplica limpio y hay que reemplazarla por una que no dependa del desvío |

**Ninguna de las cuatro ramas cambia una decisión sobre un cartucho por sí sola. Cambian los números
con los que Roberto decide.**

---

# 5. Lo que este pedido reconoce

**Escribí cinco documentos con tablas de potencia apoyadas en un número que no medí.** Los marqué
como estimación en cada uno, pero marcar no alcanza cuando toda una cadena cuelga de ahí.

**Ninguno de los once filtros del inventario detecta esto.** No hay nada que pregunte "¿de cuántos
números sin medir depende esta conclusión?". **Es el agujero que este pedido tapa para un caso y deja
abierto en general.**
