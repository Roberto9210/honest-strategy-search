# D03 — El recorte de Harvey y Liu, aplicado a las magnitudes objetivo

**VENTANA L. NO MIDE CANDIDATAS; corre CONTROLES DEL INSTRUMENTO desde el 2026-09-05 (rol ampliado por Roberto, ver `INDICE`). K sigue en 261.**

Continuación de la línea que abrieron `P02` y `P03`: **el remedio publicado para un resultado
preseleccionado es recortar la magnitud esperada, no bajar la vara.**

**Harvey, Campbell R.; Liu, Yan (2015). "Backtesting."** *Journal of Portfolio Management*.
SSRN 2345489. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2345489

---

# 1. La limitación, adelante y no al final

**El recorte se calibra con el número de intentos del backtest, y para papers ajenos ese número es
exactamente el que no conocemos.** Es el mismo desconocido que hace de `variantes_probadas` una
conjetura.

**Por eso muestro el resultado con DOS supuestos distintos**, para que se vea cuánto depende de esa
elección y no de la aritmética.

| supuesto | `N` | de dónde sale | qué representa |
|---|---|---|---|
| **estrecho** | **30** | el conteo de variantes visibles que ya declaro en cada ficha | *"el autor probó lo que se ve en su paper"* |
| **amplio** | **316** | los **316 factores publicados** que catalogan Harvey, Liu y Zhu (*RFS* 2016) | *"la profesión entera probó, y este paper es uno de esos intentos"* |

**El supuesto amplio es el que la propia literatura defiende.** Harvey, Liu y Zhu construyen el
umbral contando todas las pruebas de la profesión, no las de un autor.

---

# 2. El método, escrito para que se pueda auditar

Uso la versión **Bonferroni** del ajuste, que es la más severa de las tres que proponen y la única
que puedo calcular de forma transparente sin su código:

```
p        = 2 · ( 1 − Φ(t_publicado) )        p-valor a dos colas del t publicado
p_ajust  = mín( 1 , N · p )                  ajuste por multiplicidad
t_ajust  = Φ⁻¹( 1 − p_ajust / 2 )            de vuelta a un t
recorte  = t_ajust / t_publicado             el factor que multiplica la magnitud
```

**Harvey y Liu proponen tres métodos y un promedio. Bonferroni es el más duro, así que estos
recortes son una cota inferior de la magnitud, o sea el caso conservador.**

---

# 3. El resultado, y confirma la no linealidad

Sólo puedo aplicarlo donde el paper publica un `t` que sirva.

| ficha | `t` publicado | fuente | recorte con **N = 30** | recorte con **N = 316** |
|---|---|---|---|---|
| **L03** | **6,10** | Kurov et al., coef. 0,104 con error 0,017 | **×0,907** | **×0,836** |
| **L08** | **5,05** | Melvin y Prins, `F = 25,52` | ×0,861 | ×0,754 |
| **L01** | **4,78** | Baltussen et al., Tabla 12, `rROD` sobre el índice | ×0,845 | ×0,722 |
| **L02** | **4,08** | Gao et al., Tabla 1, `r1` sobre `r13` | **×0,784** | **×0,600** |
| L10, L11, L07, L06, L09 | — | **el paper no publica un `t` utilizable** | **no aplicable** | **no aplicable** |

## La no linealidad, verificada sobre nuestros propios números

**El `t` más alto recibe el recorte más chico y el más bajo el más grande**, exactamente como
describen Harvey y Liu:

| | `t` | recorte con N = 316 |
|---|---|---|
| el más alto, L03 | 6,10 | pierde **16 %** |
| el más bajo, L02 | 4,08 | pierde **40 %** |

**Con el supuesto estrecho la diferencia es de 9 % contra 22 %.**

## CORRECCIÓN A `D01`, argumento 2

**En `D01` ataqué nuestro filtro de magnitud diciendo que quedarse con los efectos más grandes es
quedarse con los más inflados por la maldición del ganador. La tabla de arriba muestra que ese
argumento es más flojo de lo que lo escribí.**

Harvey y Liu establecen lo contrario: **las magnitudes altas se penalizan poco porque son las que
más probablemente son descubrimientos verdaderos.** Nuestro filtro `F4`, que descarta lo chico,
**selecciona hacia el lado que el recorte castiga menos**.

**No lo borro de `D01` porque el argumento no es nulo —seguimos seleccionando sobre una variable de
resultado— pero queda corregido: es un argumento de segundo orden, no uno de los fuertes.** Y no
cambia el veredicto de `D02`, que se apoyó en el argumento de las fechas de muestra.

---

# 4. Qué le hace al inventario

**Lo empeora, que es lo esperado y probablemente la señal de que es correcto.**

## La prueba agrupada de `P01`

De las tres candidatas del grupo, **sólo L08 tiene un `t` publicado**. Su contribución baja:

| | contribución de L08 | total | `t(θ=1)` | **θ mínimo detectable** |
|---|---|---|---|---|
| sin recorte | 11,83 | 22,02 | 4,69 | **0,64** |
| recorte N = 30 | 8,77 | 18,96 | 4,35 | **0,69** |
| recorte N = 316 | 6,73 | 16,92 | 4,11 | **0,73** |

**Y eso recortando UNA de tres.** Si L10 y L11 publicaran un `t`, el deterioro sería mayor.

## Las dos que preparé hasta el borde

**No se pueden recortar**, porque ni Savor y Wilson ni Harvey, Mazzoleni y Melone publican un `t` que
sirva para esto. **Sus conclusiones de `P07` y `P08` —que no conviene registrarlas solas— no cambian,
y sólo podrían empeorar.**

---

# 5. Lo que este ejercicio deja como resultado, y no es el número

**El remedio que la literatura recomienda es inaplicable a la mayoría de nuestro inventario, por
falta de estadísticos publicados.**

Siete de once no traen un `t` utilizable. **Eso no es un defecto de los papers: la mayoría no reporta
un `t` de estrategia porque no proponen una estrategia.** Pero significa que **el mejor remedio
disponible sólo se puede aplicar donde el paper ya venía siendo cuantitativamente más generoso.**

**Y hay que decir lo incómodo de eso: recortar sólo a los que publican `t` los castiga por ser más
transparentes.** No tengo solución para esa asimetría y no la invento.
