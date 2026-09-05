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

**Costos:** dinero cero, cartuchos cero, K en 261. **Tiempo de Roberto: diez segundos en el DOM, dos
minutos en la lista de instrumentos, cinco minutos en las guías de la firma.** Es la lista de
verificación más barata del proyecto.
