# A01 — Auditoría de fechas: el conteo de eventos corregido

**VENTANA L. NO MIDE CANDIDATAS; corre CONTROLES DEL INSTRUMENTO desde el 2026-09-05 (rol ampliado por Roberto, ver `INDICE`). K sigue en 261.**

**Las dos fechas rotas las encontró la VENTANA G.** Este documento las revisa y extiende la revisión
a todo el rango.

---

# 0. QUÉ CALENDARIO USÉ, y de dónde salió

> **El calendario del CME Group para productos de índice bursátil, NO el de la bolsa de acciones de
> Nueva York. No son el mismo calendario y confundirlos era la forma de hacer mal esta tarea.**

**Fuente:** calendario de feriados y horarios de CME Group, `cmegroup.com/trading-hours.html`.

**Lo que confirma, y es lo que importa acá:**

- **Viernes Santo: los futuros de índice bursátil NO operan.** Es cierre completo, no cierre
  anticipado.
- **Existe una excepción documentada:** en los años en que el informe de empleo cae en Viernes Santo,
  los productos de índice abren una **sesión matutina abreviada** alrededor de la publicación,
  mientras el resto de los productos sigue cerrado, y esas operaciones liquidan contra las marcas del
  jueves.
- **El día después de Acción de Gracias y la Nochebuena son cierres ANTICIPADOS**, no cierres
  completos: cierran alrededor de las 12:00 hora central.

**La excepción de Viernes Santo no se aplica a 2016-2019.** El informe de empleo sale el primer
viernes del mes y los Viernes Santo del período fueron 25/3/2016, 14/4/2017, 30/3/2018 y 19/4/2019;
ninguno coincidió. **Los cuatro fueron cierre completo para índices.**

---

# 1. Los días sin sesión y los cierres anticipados, 2016-2019

| tipo | fechas en el rango |
|---|---|
| **cierre completo — Viernes Santo** | 2016-03-25 · 2017-04-14 · **2018-03-30** · 2019-04-19 |
| cierre completo — Año Nuevo, Memorial, Independencia, Trabajo, Acción de Gracias, Navidad | las habituales de cada año |
| **cierre anticipado** | día después de Acción de Gracias: 2016-11-25 · 2017-11-24 · 2018-11-23 · **2019-11-29** |
| cierre anticipado | Nochebuena y víspera de Independencia de cada año |
| **horario modificado — duelo nacional** | **2018-12-05**, por el funeral de George H. W. Bush |

**Juneteenth no aplica: es feriado del CME desde 2022, o sea dentro de la caja sellada, no en nuestro
rango.**

---

# 2. L10 — el conteo corregido

**De 48 a 46.**

| # | fecha | qué pasó | efecto |
|---|---|---|---|
| 1 | **2018-03-30** | **Viernes Santo. El CME no operó.** El último día hábil del CME de marzo de 2018 fue el jueves 29 | **evento ELIMINADO** |
| 2 | **2019-12-31** | la entrada está en rango, pero **la salida es el cierre siguiente, 2020-01-02, que está DENTRO de la caja sellada** | **evento ELIMINADO** |

```
48  meses de 2016-2019
−1  Viernes Santo 2018-03-30
−1  salida dentro de la caja (entrada 2019-12-31)
= 46 eventos
```

## Por qué el de Viernes Santo se elimina en vez de moverse al 29

**Mover la entrada al jueves 29 conserva el evento pero cambia la ventana de exposición**: la salida
sería el lunes 2 de abril, o sea **cuatro días** en vez de uno, cruzando el feriado y el fin de
semana. **`F1'` mide la exposición y ésa sería otra.** Eliminarlo es la opción consistente con el
filtro. **Es una decisión declarada, no una obligación aritmética.**

## Un hallazgo que la auditoría destapó y que no venía en el encargo

**La ventana de exposición de L10 NO es de un día para todos los eventos.** La regla del paper es
*"el retorno del día siguiente"*, y cuando el fin de mes cae **viernes**, el día siguiente es el
lunes: **la exposición es de tres días, cruzando el fin de semana.**

**Eso pasa en alrededor de una quinta parte de los eventos**, y uno de ellos —**2019-11-29**— es
además **cierre anticipado**, así que la entrada no es a las 15:00 hora central sino alrededor de las
12:00.

**No lo corrijo, porque la heterogeneidad está en la regla del paper y no en nuestra construcción.
Lo dejo escrito porque `F1'` y `F8` razonan sobre una exposición de un día y para una quinta parte de
los eventos es de tres.**

---

# 3. L11 — el conteo NO se puede cerrar, y digo por qué

**No transcribí las fechas de anuncio** (`P07`, sección 1: una fecha mal copiada dentro de un
documento que habilita un cartucho es un error que no se detecta). **Sin la lista, no puedo dar un
conteo corregido.**

**Lo que sí puedo dejar es la regla de auditoría, escrita para aplicarse cuando la lista se arme:**

1. **Ningún anuncio cae en día sin sesión**, porque las agencias publican en días hábiles. **El riesgo
   está en la ENTRADA**, que es el cierre de la sesión anterior.
2. **Si la sesión anterior fue cierre completo, el evento se elimina** por el mismo motivo que el de
   Viernes Santo: la entrada se correría a un cierre más lejano y la exposición dejaría de ser de una
   sesión.
3. **Si la sesión anterior fue cierre anticipado, el evento se conserva y la marca temporal cambia**
   a la hora real de cierre. Aplica a los días después de Acción de Gracias, Nochebuena y víspera de
   Independencia.
4. **2018-12-05 tuvo horario modificado por duelo nacional.** Cualquier anuncio del 5 o del 6 de
   diciembre de 2018 necesita revisión manual.
5. **Ningún anuncio de 2016 puede tener su entrada antes del comienzo de los datos.** La Compuerta 1
   trabaja con pares de noches desde **2016-01-05**; un anuncio del 4 o 5 de enero de 2016 podría no
   tener cierre previo disponible.
6. **Ningún evento puede tener su salida dentro de la caja sellada.** Para L11 entrada y salida caen
   el mismo par de sesiones, así que sólo un anuncio del 2 de enero de 2020 en adelante lo violaría;
   no hay ninguno en el rango. **La regla queda escrita igual.**

**Cota superior del ajuste: los cierres completos que caen en la sesión previa a un anuncio son a lo
sumo unos pocos por año. El conteo de 128 a 176 se moverá poco, y eso NO cambia el veredicto de
`P07`, que ya era "no registrar".**

---

# 4. ¿Cambia algún veredicto ya escrito?

| veredicto | ¿cambia? |
|---|---|
| `P08`: **no registrar L10 sola** | **NO.** Con 46 eventos en vez de 48 y el desvío medido, empeora: ver abajo |
| `P07`: **no registrar L11 sola** | **NO.** El ajuste de conteo es chico y va en la misma dirección |
| `D05`: **cerrar `P01`** | **NO, y lo refuerza.** Menos eventos es menos potencia |
| `F8`: la exposición de cierre a cierre es indefendible en ES | **NO**, pero ahora se sabe que para una quinta parte de los eventos de L10 es **peor** de lo supuesto: tres días |

## El número de `P08`, recalculado con las dos correcciones

```
antes:  m = 17,0 pb   σ = 60 (estimado)   n = 48   →  t(θ=1) = 1,96   θ mínimo = 2,04
ahora:  m = 17,0 pb   σ = 82,8 (MEDIDO)   n = 46   →  t(θ=1) = 1,39   θ mínimo = 2,87
```

**L10 sola necesitaría el 287 % de su magnitud publicada, no el 204 %.** El veredicto no cambia; el
número sí, y va corregido en `P08`.

---

# 4-bis. L11, CERRADA — 2026-09-05

**Aplico las seis reglas sin la lista completa de fechas, y alcanza para cerrar.**

## Un impacto cierto, identificado por estructura

**El informe de empleo sale el primer viernes del mes. La entrada es el cierre del jueves anterior.**

**El 4 de julio de 2019 fue jueves, y el viernes 5 de julio fue el primer viernes: el informe de
empleo de junio salió ese día.** La entrada caería en el **4 de julio, con el mercado cerrado**.

**Por la regla 2 —si la sesión anterior fue cierre completo, el evento se elimina— ese evento se
cae.** La alternativa sería entrar el 3 de julio, que además fue cierre anticipado, con una
exposición de dos días cruzando el feriado.

**Los otros tres años no tienen el problema:** el 4 de julio cayó lunes en 2016, martes en 2017 y
miércoles en 2018, y en ninguno el primer viernes fue el día siguiente.

## Lo que no puedo enumerar sin la lista

**Las publicaciones del índice de precios caen a mediados de mes sin día fijo**, así que podrían
seguir a un lunes feriado —el de Martin Luther King, el de los Presidentes, el de la Memoria o el del
Trabajo—. **Sin las fechas exactas no puedo contarlas.** Por estructura son pocas: hacen falta dos
coincidencias, que la publicación caiga en martes y que ese lunes sea feriado.

**Las reuniones del comité de política monetaria son martes y miércoles y evitan feriados**, así que
no aportan casos.

## Por qué la auditoría se cierra igual

> ## **L11 es CIEGA con la magnitud ENTERA (`D06`): su umbral es 18,54 puntos básicos y su magnitud publicada 11,4. Toda corrección de fechas REDUCE `n`, y reducir `n` SUBE el umbral.**

**Cualquier enumeración exacta sólo la haría más ciega. No existe un conteo de fechas que cambie su
veredicto.**

**Enumerar las fechas restantes sería trabajo cuyo resultado no puede cambiar nada, que es
exactamente lo que `F12` prohíbe — aplicado a mi propio trabajo.**

**La auditoría de L11 se cierra por veredicto, no por enumeración.** Las seis reglas quedan escritas
y se aplican intactas el día que la lista se arme por otro motivo.

---

# 5. Lo que esta auditoría deja como advertencia

**Las dos fechas rotas las encontró la VENTANA G, no yo.** Yo había escrito en `P09` que *"mis
timestamps de las 15:00 hora central podrían no coincidir con una barra en días de cierre
anticipado"* y **lo dejé como pendiente en vez de resolverlo**, porque pensé que necesitaba los datos.

**No los necesitaba: el calendario del CME es público y la auditoría se podía hacer sin tocar un
precio.** Marqué un riesgo y no lo cerré teniendo la herramienta a mano. **Queda anotado.**
