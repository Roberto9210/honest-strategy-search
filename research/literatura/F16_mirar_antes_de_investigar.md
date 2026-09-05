# F16 — Antes de investigar un hecho sobre la configuración propia de Roberto, preguntar si Roberto puede simplemente MIRAR

**VENTANA L. NO MIDE NADA. K sigue en 261.**

> ## **REGLA F16. Si el hecho que hace falta es sobre la plataforma, la cuenta, el feed, la latencia o el reglamento de la firma DE ROBERTO, no se investiga: se le pide que mire. Su configuración es observación directa. Investigarla en fuentes de terceros es reconstruir por afuera lo que él tiene adelante.**

---

# El caso que la descubrió

**`D10`, ronda 14.** Hacía falta saber cuántos niveles del libro del ES ve la plataforma de Roberto.
Fui a la guía de Globex, a las preguntas frecuentes de DataMine, a Fett y Haynes, a un sitio de
reseñas de firmas de fondeo, y dos veces a la página de ayuda de la firma, que devolvió 403.
**Resultado: tres fuentes que dicen cuánto ve "un participante chico", una secundaria sobre la firma,
una afirmación no verificada sobre Nivel 2, y dos rondas de trabajo.**

**Lo que Roberto tiene que hacer para saberlo: abrir el DOM y contar filas. Diez segundos.**

Y la autocrítica (b) del reporte lo dijo antes que la regla: *seis documentos miden cuánto ve el
chico; ninguno mide qué ve la plataforma de Roberto.* **La regla es esa frase, dada vuelta.**

# Por qué es una regla y no una anécdota

**Hay una asimetría estructural:** para el mercado, la fuente es externa y hay que buscarla. Para la
configuración propia, **la fuente está en la máquina de Roberto**, y ninguna fuente externa la
describe mejor, porque las fuentes externas describen al participante típico y Roberto no es el
participante típico: es una cuenta concreta con un contrato concreto de una firma concreta.

**Corolario que ya apareció dos veces en `H01`:** una fuente externa sobre "lo que ve el chico" está
ponderada por observación o por participante, y el factor entre las dos puede ser de 25. **Mirar la
propia pantalla no tiene ese problema.**

# Cómo se aplica

1. Antes de abrir una búsqueda, preguntar: **¿este hecho es del mercado o de la configuración de
   Roberto?**
2. Si es de la configuración: **escribir qué tiene que mirar, dónde, y qué anotar.** Una línea.
3. **La respuesta de Roberto entra como hecho medido por la casa**, con fecha, y desplaza cualquier
   fuente secundaria que dijera otra cosa.
4. Si lo que hace falta requiere una herramienta y no sólo mirar —medir la latencia, por ejemplo—,
   sigue siendo observación directa; **pasa a G sólo si Roberto no puede hacerlo solo.**

---

# LA LISTA: hechos sobre la configuración de Roberto que hoy están en fuente secundaria o sin verificar

Revisé `D10`, `H01`, `F8`, `PISO_Y_CONVERSION`, el censo de instrumentos de G y `CIERRE_VENTANA_G`.
**Lo que G ya leyó de la página de la firma con fecha (comisión de índices, política de bots, límite de
tiempo, drawdown) NO está en la lista: es fuente primaria.** Lo que sigue, sí.

| # | hecho | dónde está apoyado hoy | dónde lo mira Roberto | a qué afecta |
|---|---|---|---|---|
| 1 | **cuántos niveles del libro muestra su DOM**, en contado y de noche | `D10`: guía de Globex + un sitio de reseñas | **el DOM, contar filas** | el estudio de entrada pasiva de G |
| 2 | **si muestra precios agregados u órdenes individuales** | `D10`: no verificado | el mismo DOM | si la cola FIFO que G reconstruyó es visible en vivo |
| 3 | **si el Nivel 2 se puede comprar y a qué precio** | `D10`: **no verificado**, 403 | la pantalla de suscripción de datos de la plataforma | costo del dato en vivo, va al piso |
| 4 | **qué proveedor de datos alimenta su plataforma** | en ningún lado. `H01` dice "el router de la firma" | la ventana de conexión de la plataforma | latencia y profundidad |
| 5 | **la latencia de su máquina a la firma**, el escalón 3 de `H01` | **sin medir, por nadie** | el registro de órdenes de la plataforma: instante de envío contra instante de confirmación | candidatas que reaccionen a eventos; la calidad de la salida de L03 (`D11`) |
| 6 | **si la firma permite operar los micros que el censo de G usa** | `salida_censo.txt`: *"permiso de Tradeify NO VERIFICADO"* | la lista de instrumentos de su cuenta | toda la tabla de holgura de `F8` |
| 7 | **si la firma permite 6J y 6E** | en ningún lado | la misma lista | **L07 y L08 enteras** |
| 8 | **si la firma restringe operar alrededor de publicaciones económicas** | **en ningún lado del repo.** G leyó la sección de bots de las guías de la firma, no ésta | las guías de la firma, un minuto | **L03 y L11 enteras**: las dos entran o salen alrededor de un dato |
| 9 | **si se puede mantener posición a través de las 16:00-17:00 CT y de noche**, y con qué límite | `CIERRE_VENTANA_G` modela el drawdown nocturno; la regla de la firma sobre posiciones nocturnas no está citada | las guías de la firma | L10 con retorno del día siguiente; cualquier salida por tiempo que cruce el corte |
| 10 | **la comisión de divisas** | `PARA_VENTANA_L.md` §4: "falta, una lectura" | la página de comisiones de la firma | la ficha de calibración de 6E/6J |

> ## **Las filas 7 y 8 son las que más valen: cada una puede cerrar dos candidatas enteras, y ninguna requiere más que leer una página que Roberto ya tiene abierta al operar.**

---

# LA LISTA ORDENADA POR PODER DE CIERRE, y quién resuelve cada una

**Resultado del ordenamiento, dicho primero: las diez se resuelven con Roberto mirando algo. Ninguna
necesita investigación mía.** Eso no es una casualidad: es lo que la regla predice. Lo que me queda
para investigar tiene poder de cierre **cero** y va al final.

| orden | fila | hecho | **candidatas que puede cerrar** | quién |
|---|---|---|---|---|
| 1 | 8 | restricción alrededor de publicaciones | **hasta 2: L03 y L11** (`R03` rama 2) | **Roberto mira** |
| 2 | 7 | 6J y 6E permitidos | **2: L07 y L08**, sin apelación (`R03` rama 1) | **Roberto mira** |
| 3 | 9 | posición a través del corte y de noche | **1: L11** en su forma publicada (`R03` rama 3) | **Roberto mira** |
| 4 | 6 | micros permitidos | 0; cambia la palanca de tamaño de `F8` para L10 y L11 | Roberto mira |
| 5 | 10 | comisión de divisas | 0; condición para medir L07 y L08 | Roberto mira |
| 6 | 5 | latencia del escalón 3 | 0 hoy; calidad de la salida de L03 (`D11`); bloquea candidatas futuras que reaccionen | Roberto mira su registro de órdenes |
| 7 | 1, 2 | niveles del DOM, precios u órdenes | 0; el estudio de entrada pasiva de G | Roberto mira |
| 8 | 3 | precio del Nivel 2 | 0; una línea del piso | Roberto mira |
| 9 | 4 | proveedor del feed | 0; contexto de 5 y 7 | Roberto mira |

**Investigación mía pendiente, ordenada por poder de cierre —que es cero en las dos—:** la fecha en que
el canal público del ES pasó de cinco a diez niveles (`D10`), y los números de Andersen y Bollerslev
que no pude extraer (`T02`). **Ninguna cierra nada; se hacen si sobra tiempo y no antes.**

## ESTADO — 2026-09-05, después de que Roberto miró

| fila | resultado | fuente | consecuencia |
|---|---|---|---|
| **8** publicaciones | **sin ninguna restricción**, *"free reign"*, política completa verificada | help.tradeify.co, Roberto, 2026-09-05 | nadie muere (`R03` rama 2) |
| **7** 6J y 6E | **en la tabla de tarifas**: 6J $6,20, 6E $6,20, M6E $1,60 ida y vuelta | idem | L07 y L08 no mueren; siguen bloqueadas por plomería |
| **9** noche | **prohibido**: todo cerrado 16:45 del este, 12:59 en cierre temprano, lo cierran ellos | idem | **L11 publicada MUERTA** (`R03` rama 3) |
| **10** comisión de divisas | $6,20 ida y vuelta | idem | resuelta |
| **6** micros | 40 micros o 4 minis en $50k; la lista de productos no se reportó todavía | idem, parcial | pendiente la lista |
| 1, 2, 3, 4, 5 | **sin reportar** | — | pendientes |
| **11, nueva** | **¿se puede abrir y cerrar operaciones en la sesión de Globex de la tarde-noche, entre las 18:00 y las 16:45 del este?** No es lo mismo que "nada abierto a las 16:45". Decide la operabilidad de L07 (19:50-21:00 del este) | — | **pendiente; agujero de `R03`** |

**Y tres reglas nuevas que salieron de la misma lectura y no estaban en la lista:** microscalping (más del
50 % de las operaciones y de la ganancia en operaciones de más de 10 s; bloquea el retiro), *"No HFT
bots"* sin definición numérica, y consistencia (ningún día > 40 / 35 / 20 % de la ganancia según la
cuenta). G ya las metió en el juez como cerraduras (`f5d129f`, `6d4bc1c`). Van adentro de `F17`.

## Para pegarle a Roberto tal cual: dónde mirar y qué anotar

1. **Publicaciones (fila 8).** En el centro de ayuda de la firma, la página de reglas para operadores
   (la misma que G leyó el 2026-09-03 para la sección de bots) y cualquier página que diga *news*,
   *high impact* o *economic releases*. **Anotar textual:** si prohíbe **tener posición** o **enviar
   órdenes**; cuántos minutos antes y después; y **la lista** de publicaciones o el calendario que usa.
   Mirar si aparecen ISM y ventas de viviendas.
2. **6J y 6E (fila 7).** La lista de productos operables de la cuenta, en la plataforma o en la página
   de productos de la firma. **Anotar:** si aparecen 6J, 6E, y si sólo aparecen los micros M6E.
3. **Noche y corte (fila 9).** Misma página de reglas: *overnight*, *holding positions*, hora límite
   para cerrar. **Anotar:** la hora exacta y si aplica en evaluación y en fondeada.
4. **Micros (fila 6).** Misma lista de productos: cuáles de MES, MNQ, M2K, MYM, MGC, MCL aparecen.
5. **Comisión de divisas (fila 10).** La página de comisiones (G leyó la de índices el 2026-09-04): la
   fila de futuros de moneda, ida y vuelta.
6. **Latencia (fila 5).** En el registro de órdenes de la plataforma, para cinco órdenes cualesquiera:
   instante de envío e instante de confirmación. **Anotar** la diferencia en milisegundos.
7. **DOM (filas 1 y 2).** A las 10:00 y a las 03:00 del este: **contar** las filas de precio a cada
   lado del mejor precio, y anotar si cada fila muestra **un número** (precios agregados) o **varias
   órdenes** con su tamaño.
8. **Nivel 2 (fila 3).** La pantalla de suscripción de datos de la plataforma: si existe la línea
   *Level 2* o *market depth* y su precio mensual.
9. **Proveedor (fila 4).** La ventana de conexión: el nombre del proveedor de datos y de órdenes.

**Costos:** dinero cero, cartuchos cero, K en 261. **Tiempo de Roberto: diez segundos en el DOM, dos
minutos en la lista de instrumentos, cinco minutos en las guías de la firma.** Es la lista de
verificación más barata del proyecto.
