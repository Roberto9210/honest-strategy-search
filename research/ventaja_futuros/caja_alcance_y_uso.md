# La caja fuerte: alcance, uso y dónde muerde la deuda — Ventana D, 2026-09-03

Tres preguntas de Roberto antes de decidir qué se hace con el único tiro. Ninguna gasta nada:
la caja sigue cerrada, H2d sigue congelada y en pie, nada se corrió sobre 2020 en adelante.

Fuente leída: `factory/spec_fase2.md` en su último commit `e17cde9` (2026-08-24), `factory/harness.py`
y `factory/experiments_ledger.jsonl` (114 líneas) del HEAD de este repo. Las citas van textuales,
con número de línea de la spec. La lectura va separada de la cita y rotulada como lectura.

## 1 · ¿La caja es de ES o es de fechas?

### Citas

- §3.3, línea 351: **"La parte B, 2020-01-01 → 2026-08-19, sigue sellada. Un solo uso para TODO el programa."**
- §7.1, línea 806: **"2020-01-01 → 2026-08-19 sigue sellada. Un solo uso para todo el programa."** Y línea
  808–811: "Lo único que se puede consultar de la parte B sin abrirla es su **calendario** (cuántas
  sesiones, cuántos meses tiene) — que es una propiedad de las fechas, no de los precios [...]. Cualquier
  otra lectura de B es una violación de la spec y se registra como tal en el ledger."
- §4.4 declara dos series y solo dos, cada una con su parte B:
  - Diario, línea 590–593: "**Serie:** `data/es_daily.csv` (ES=F diario, Yahoo [...]). Parte B = 2020-01-02 → 2026-08-19 (**1.669 sesiones**)."
  - Intradía, línea 611–614: "**Serie:** `data/es_1min_databento.csv` [...]. Parte B = 2020-01-02 → 2026-08-18 (**1.669 sesiones**)."
- §4.5, requisito 4 para incorporar cualquier instrumento nuevo, línea 682–683: **"La misma frontera de
  partición 2020-01-01, para que la caja fuerte siga siendo un objeto único y coherente entre instrumentos."**
- §4.4, línea 646–651: "El criterio de admisión de esta sección selecciona la ventana de **desarrollo**;
  **nunca recorta la caja fuerte.**"
- §4.4, línea 667–669: "Si aun así se decide ampliar una ventana, la ampliación **es una fase nueva**: spec
  propia, presupuesto propio, y el contador heredado (§1.6)."

### Lectura, separada de las citas

La definición de la caja es por **fechas**: las dos frases que la definen (§3.3 y §7.1) nombran un
intervalo y no nombran instrumento. Las únicas series que la spec admite hoy son dos, las dos de ES.
Para cualquier instrumento nuevo, §4.5.4 exige la misma frontera "para que la caja fuerte siga siendo
un objeto único [...] entre instrumentos": la spec dice con todas las letras que hay **una** caja y que
los instrumentos entran en ella, no que cada instrumento trae la suya.

Estado del tercer tipo, escrito como tal: la spec **no dice** qué pasa con una raíz que nunca fue
admitida (NQ, GC, MGC desde 2020). Lo que sí dice es que para admitirla hay que darle la frontera
2020-01-01 y que la caja es un objeto único entre instrumentos. La lectura "NQ 2020+ es población sin
gastar" no encuentra una frase que la sostenga y encuentra una que la contradice (§4.5.4). La lectura
"todo lo posterior a 2020-01-01 de cualquier instrumento admitido es la misma caja" encuentra dos. Si
Roberto quiere que una raíz no admitida quede fuera de la caja, eso se escribe como fase nueva por
§4.4 línea 667, con el contador heredado. **No es un solo tiro por ES; es un solo tiro por programa.**

Dos hechos del código que conviene saber, no interpretados:

- El docstring de `factory/harness.py` (línea 5–7) todavía dice "**B se toca UNA vez por candidata**".
  Es texto de la Fase 1; la spec de la Fase 2 lo reemplaza en su tabla §3.4 línea 400: "Usos de la caja
  fuerte | uno por candidata | **uno para todo el programa**". El docstring está desactualizado.
- `VaultViolation` (harness línea 166) solo se dispara al evaluar sobre B sin `examen_final=True`. **Nada
  en el código cuenta los usos**: el "un solo uso" vive en la spec y en el ledger, no en una comprobación.
  El ledger tiene un único acceso a B, el autotest de la Fase 1 (línea 2), exento por nombre en §9.5.

## 2 · ¿Qué significa "un solo uso"?

### Citas

- §3.3, línea 351–353: "**Un solo uso para TODO el programa.** No una vez por candidata: **una vez, y se
  acabó.** La abre **la primera candidata** que pase las compuertas 1 y 2, y solo por el camino
  `harness.run_on(..., examen_final=True)`, que la registra en el ledger."
- §3.3, tabla de la vara, línea 359: "Significancia | p ≤ 0.05 bilateral (**prueba única pre-registrada;
  la multiplicidad ya se pagó en A**)".
- §3.1–3.2 (líneas 300–341): la compuerta 1 se pasa en la parte A con |t_A| ≥ 3.726 (α/257 de entonces),
  la compuerta 2 exige potencia proyectada ≥ 80 % en B: "Si la potencia proyectada es < 80%, la candidata
  NO se rechaza y NO se aprueba: se ARCHIVA [...] y **la caja fuerte no se abre.**"
- §8.1, línea 1033: "**Examen final fallado:** una candidata abrió la caja fuerte y no pasó la compuerta 3.
  La fase cierra **inmediatamente**".
- Ledger, línea 106 (CAMBIO_DE_REGLAS del 2026-08-25, ENDURECE): "Inequivoco: la prueba sobre B NO
  arrastra la penalidad de la busqueda; esa vive en la compuerta 1 [...] y no se cobra dos veces." Y:
  "(c) la caja queda gastada en los dos casos (§7.1, un solo uso para todo el programa)."

### Lectura, separada de las citas

La spec está escrita para **una candidata**: "la primera candidata", "prueba única pre-registrada",
"una candidata abrió la caja fuerte". No hay ninguna frase que contemple k hipótesis pre-registradas
evaluadas juntas en la misma apertura, ni para permitirlo ni para prohibirlo. **Ambigua en ese punto,
tercer estado.** Si se quiere la apertura conjunta, se escribe como cambio de reglas al ledger
(§9.5c, con dirección declarada), no se interpreta.

Y hay algo más importante que la k, que la pregunta de Roberto da por supuesto y la spec contradice:
en el protocolo de la spec **la multiplicidad no se paga en la caja**. Se paga en A (compuerta 1, α/K)
y la caja se examina a **0,05 bilateral**. La caja no vale "k respuestas a 0,05/(261+k)"; vale una
respuesta a 0,05 para una candidata que ya pagó K en A. Mi Enmienda 2 pre-registró lo contrario para
H2d: α = 0,05/262 sobre el intocado, con el mirado usado solo para controles. Los dos protocolos, con
los N de H2d y sin correr nada (`potencia_terreno_condicional.txt` §6):

| protocolo | dónde se paga K | prueba en A (851) | prueba en B (1.687) | acierto mínimo al 80 % |
|---|---|---|---|---|
| spec §3.1–3.3 | en A | t ≥ 3,73 (cruza desde 56,4 %; potencia 80 % desde 57,9 %) | 0,05 bilateral | 57,9 % en A, después 53,5 % en B |
| Enmienda 2 | en B | ninguna (solo controles) | 0,05/262 bilateral | 55,6 % en B |

La compuerta 2 no muerde aquí: con n_B > n_A el mínimo es max(3,726; 1,99) y manda la compuerta 1,
el caso "intradía" de la tabla de §3.2. Son dos protocolos distintos y no son equivalentes: el de la
spec pide más en A y menos en B; el de la enmienda no pide nada en A y más en B. **Cuál rige para H2d
lo decide Roberto**; yo no lo cambio solo. Lo que sí queda dicho: mi enmienda no siguió la letra de la
spec en dónde se cobra la multiplicidad, y eso tenía que estar escrito antes de que se abra nada.

## 3 · Dónde están los efectos grandes: ¿la deuda muerde igual a un factor?

Salida cruda en `potencia_terreno_condicional.txt` (commit `62e9040`). El script no define ninguna
condición ni corre ninguna: mide la dispersión incondicional de log(excursión adversa) sobre las
971 sesiones ya barridas de 2016–2019 y calcula, para una partición f / 1−f que todavía no existe,
el factor mínimo detectable al 80 % con α = 0,05/262 a dos colas.

**La respuesta corta: la deuda muerde exactamente igual por unidad de efecto, y los efectos de terreno
son diez veces más grandes que la unidad.** La deuda multiplica el efecto mínimo en escala log por
1,63 en las dos formas de pregunta, porque es el mismo (z_α + z_β) en las dos fórmulas. Lo que cambia
no es el precio, es lo que hay para comprar.

Factor mínimo detectable (media geométrica condicionado / resto), 971 sesiones:

| ventana | σ_log | f = 0,5 | f = 0,33 | f = 0,2 | f = 0,1 | f = 0,5 a α 0,05 |
|---|---|---|---|---|---|---|
| T23 largo | 1,235 | 1,44× | 1,47× | 1,57× | 1,83× | 1,25× |
| RTH largo | 1,208 | 1,43× | 1,46× | 1,56× | 1,81× | 1,24× |
| H1 largo | 1,101 | 1,38× | 1,41× | 1,50× | 1,71× | 1,22× |
| M15 largo | 0,997 | 1,34× | 1,37× | 1,44× | 1,63× | 1,20× |
| hora 23:00 largo | 0,931 | 1,31× | 1,34× | 1,41× | 1,58× | 1,18× |
| hora 08:00 largo | 1,071 | 1,37× | 1,40× | 1,48× | 1,69× | 1,21× |

La misma deuda en unidades direccionales, para comparar: con 971 sesiones el acierto mínimo
detectable es 57,5 %, que son odds de 1,35×; con 1.687, 55,6 % = 1,25×. Un factor de 1,4× en la
excursión y odds de 1,35× en el acierto son **el mismo tamaño de efecto** en la escala en que la
prueba lo ve. Ahí termina la simetría.

Lo que las mediciones de terreno ya mostraron, sin buscar nada: la hora más barata contra la de la
apertura es un factor 4 a 5 (p50 0,19); un stop de 2 toca 87 % y uno de 20 toca 21 %, factor 4;
contrato grande contra micro, factor 10. Sesiones por grupo (50/50) que hacen falta con el α heredado:

| factor | T23 largo | H1 largo | M15 largo | hora 23:00 |
|---|---|---|---|---|
| 1,25× | 1.281 | 1.018 | 835 | 728 |
| 1,5× | 388 | 308 | 253 | 220 |
| 2× | 133 | 105 | 87 | 75 |
| 4× | 33 | 26 | 22 | 19 |

Un factor 2 se paga con 75 a 133 sesiones por grupo; un factor 4 con 19 a 33. La P-escalera tiene 971.
En su forma binaria (toque del stop), en T23 largo con D = 10 la tasa base 46,2 % tendría que subir a
60,9 % (1,32×) para verse con f = 0,5; en H1 con D = 10, de 16,6 % a 27,5 % (1,66×). Todo en el mirado,
sin tocar la caja.

### Lo que esto no dice, escrito antes de que alguien lo use

- **No dice que una pregunta condicional sea gratis en K.** Cada pregunta pre-registrada es una
  configuración y paga K_D. La deuda no baja: el efecto mínimo sube 1,63× en log igual que siempre.
  Lo que cambia es que hay efectos de ese tamaño en el terreno y no los hay en la dirección.
- **Las sesiones no son independientes.** La volatilidad se agrupa; una condición sobre "el día
  anterior" corre en serie con lo que mide, y el n efectivo es menor que 971. Los números de arriba
  son de planificación con n nominal, como los de `potencia_heredada.py`. Un pre-registro real tiene
  que declarar cómo trata la dependencia antes de correr.
- **La dispersión dentro de la condición no es la incondicional.** Condicionar por volatilidad reduce
  σ_log dentro de cada grupo, lo que ayuda; la tabla usa la incondicional y por eso es conservadora.
- **Que la excursión sea mayor después de un día de rango grande es conocimiento público**
  (agrupamiento de volatilidad, Engle 1982 y toda la familia GARCH). Confirmarlo no es una ventaja:
  es terreno. Una pregunta condicional que valga K tiene que ser una cuya respuesta cambie qué se hace
  con el stop, la hora o el tamaño, y cuyo tamaño de efecto no sea el que el GARCH ya predice.
- **El mirado está barrido para dirección, no para estas preguntas.** Barrido significa que ya
  contribuyó a K, no que sus respuestas condicionales sean gratis ni que estén contaminadas: nadie las
  buscó. Pero cualquier pregunta que se elija después de haber visto la escalera de horas y la de
  stops se elige con esos datos vistos, y eso se declara en el pre-registro.

### Lo que sí dice

Si la búsqueda cambia de forma, de "qué dirección" a "cuánto y cuándo", el α heredado deja de ser la
pared: con 971 sesiones se ven factores de 1,4× a 50/50 y de 1,8× en un decil, y el terreno ya mostró
factores de 4. Esa es una decisión distinta de abrir la caja y la toma Roberto. Ninguna hipótesis
condicional queda formulada acá.
