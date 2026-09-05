# R02 — El dominio se fija sobre 2016-2019 POR CONSTRUCCIÓN. Cierra el agujero de marzo de 2020 antes de que se abra la caja. SELLADA.

**VENTANA L. NO MIDE NADA. K sigue en 261.**

> ## SELLADO
>
> **La caja sellada (ES 2020-01-02 → 2026-08-19, un solo uso) no se ha abierto.** Esta regla se
> commitea antes de que nadie mire un solo dato de ese período, y el historial es la prueba. Se
> escribe en la misma forma que `R01`: la regla, la razón, y la lectura de las dos versiones antes de
> mirar nada.

---

# 1. El agujero, con su nombre

`R01` dice: *"un evento cuya volatilidad ex-ante excede el máximo observado en el período de
calibración del eje está fuera del dominio."* **Y yo mismo nombré la circularidad en el reporte:
depende de con qué período se calibra el eje.** Si el eje se recalibra con 2020 adentro, marzo de
2020 queda en el dominio; si no, queda fuera. **Decidir eso después de abrir la caja es elegir el
resultado.** Roberto: "si se decide hoy es una regla; si se decide después de abrir es elegir."

# 2. (a) ¿Con qué período está calibrado hoy el eje de la VENTANA G?

**Lo leí en el código, no lo supuse:**

| | |
|---|---|
| **medida** | rango medio de la barra de un minuto de la **sesión anterior**, dividido por el precio medio de esa sesión, en puntos básicos. *"Conocible al entrar"* |
| **período de calibración** | **ES 1-min 2016-2019, 1.007 sesiones.** Los cortes de tercil se calculan sobre esa muestra |
| **fuente** | `juez.py` líneas 259-266 (`tercil_exante`); `juez_regimen_bps.py` encabezado: *"Medición descriptiva sobre muestra ya recogida (ES 1-min 2016-2019)"* |

**O sea: hoy el eje está calibrado sobre 2016-2019 y sólo sobre 2016-2019, porque la caja está
cerrada y G no puede usar otra cosa.** Eso no es una decisión sellada: es una circunstancia. **La
regla no puede apoyarse en una circunstancia.**

# 3. (b) La regla, escrita para que NO dependa de esa elección

> ## **REGLA R02. El dominio de volatilidad del proyecto se calcula UNA sola vez sobre las sesiones de 2016-2019, con la definición de abajo, y NO SE RECALIBRA NUNCA con datos posteriores a 2019-12-31, se abra o no la caja, cambie o no la VENTANA G su eje. Un evento cuya medida ex-ante cae fuera de ese dominio se excluye por regla y se lista con su valor.**

## La definición, fijada acá y no en otro lado

**`R01` decía "con la misma definición que usa el eje de G". Eso hay que corregirlo, y es una
corrección a mí mismo (`F13` 6a):** la medida de G usa **barras de un minuto**, y la caja sellada
es una serie **diaria**. Una regla que no se puede calcular sobre el dato que va a juzgar no es
una regla.

| | **definición R02** |
|---|---|
| **medida ex-ante `v`** | `(máximo − mínimo) de la sesión anterior / cierre de la sesión anterior × 10.000`, en puntos básicos. Sesión = sesión completa del CME (ETH), la misma que usa el resto del repo |
| **por qué ésta** | es el análogo diario exacto de la de G —rango sobre precio, sesión anterior, puntos básicos, conocible al entrar—, y **se calcula igual sobre barras de un minuto, sobre diarios, y sobre los dos precios por evento de 1987-1996** |
| **dominio** | `[ mín(v), máx(v) ]` sobre las **1.006 sesiones de 2016-2019** con retorno cierre a cierre |
| **quién calcula los dos bordes** | la VENTANA G, una vez, y los escribe en este documento con el hash del script. **Son una función determinista de datos ya públicos: no hay nada que elegir** |
| **criterio** | un evento entra si y sólo si su `v` está dentro del dominio, bordes incluidos |

**Con esto la elección de período que G haga para SU eje deja de importar: R02 tiene su propio
dominio, fijado por construcción, y G puede recalibrar sus terciles como quiera para sus fines sin
que la regla se mueva.** (b) se puede hacer, así que (c) no hace falta.

## Lo que la regla hace que hay que decir antes

1. **Marzo de 2020 sale.** El fin de mes de marzo de 2020 tiene como sesión anterior el 30 de marzo,
   con un rango diario que ningún día de 2016-2019 —ni el 5 de febrero de 2018, ni diciembre de
   2018— alcanzó. **No lo sé por haber mirado la caja: lo sé por lo que fue público en los diarios
   de todo el mundo.** Y probablemente salen **febrero y abril de 2020** también. **Cuántos salen se
   reporta al abrir, con sus valores, y no se ajusta el borde para que salgan menos.**
2. **La regla es de UNA sesión.** Una sola sesión extraordinaria antes de un fin de mes normal lo
   excluye. Es deliberado: una medida de varias sesiones sería más suave y **tendría un parámetro
   más para elegir**. Prefiero la regla áspera sin parámetro.
3. **Excluir los meses más volátiles quita ruido y baja el umbral de detección**, igual que en
   `R01`. Si algo pasa sólo con la regla puesta, se dice así: *pasa en el régimen que el dominio
   cubre*.
4. **La regla vale para CUALQUIER prueba que se corra en la caja, no sólo para L10.** La caja tiene
   un solo uso; lo que se corra ahí hereda R02.
5. **El borde inferior casi nunca muerde**, pero se declara simétrico para que no haya que decidir
   después si un día muerto cuenta.

# 4. Las dos versiones, cuando se mire

| versión | qué incluye |
|---|---|
| **A — con R02** | sólo los eventos con `v` dentro del dominio 2016-2019. **Principal** |
| **B — sin R02** | todos los eventos del período mirado |

**Lectura, fijada ahora:**
- A y B dan lo mismo → los atípicos no mandan; robusto.
- A pasa y B no → **el resultado vive en el régimen que el dominio cubre**, y así se dice.
- **B pasa y A no → el resultado lo producen los atípicos, y NO cuenta.**

# 5. Relación con R01

`R01` queda en pie con **dos enmiendas**, que se anotan acá y no se reescriben allá: **(i)** la medida
es la de R02, no la de G; **(ii)** el dominio es el de R02, fijado sobre 2016-2019 y no "el período de
calibración del eje". **El argumento del mismo objeto de `R01` §3 no cambia.**

# 6. Costos

| | |
|---|---|
| **dinero** | cero |
| **cartuchos** | cero. Es una regla de construcción. K en 261 |
| **tiempo de Roberto** | leer esto |
| **tiempo de G** | calcular dos números sobre 2016-2019 y pegarlos acá con el hash |
