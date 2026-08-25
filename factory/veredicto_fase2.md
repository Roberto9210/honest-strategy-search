# Veredicto de la Fase 2

**Fecha de cierre:** 2026-08-25 · **Apertura:** 2026-08-24 13:31 UTC (acta `66693079f2c03099`) ·
**Última entrada:** 2026-08-25 02:03 UTC (`d306d0016d212767`) · **Duración: 12 h 32 min.**

Escrito según `spec_fase2.md` §8.2, en el orden que esa sección exige.

---

## El veredicto, en dos líneas

> **Como búsqueda: negativa.** Ninguna de las 4 configuraciones corridas se acercó a la vara. El mejor
> p-valor de toda la fase es **peor que la línea de la suerte**, y ninguna candidata llegó a la puerta
> del examen final.
>
> **Como medición: concluyente, y es lo que sobrevive.** La fase midió `c` —la calidad de las hipótesis
> que sabemos generar— en **+0,0203 ± 0,0233** (2 mecanismos), contra un umbral de 80 % de potencia de
> **0,068577**. Y midió algo más valioso: **el reparto A/B heredado hacía que esta fase no pudiera
> correr una prueba justa**, cosa que era computable el día cero y nadie computó.

---

## 1. Qué disparó la línea de parada: **ninguno de los cuatro gatillos**

§8.1 lista cuatro: presupuesto agotado (no: 4 de 200), calendario 2027-02-28 (no), las seis familias
cerradas (no: cuatro siguen con presupuesto), examen final fallado (no: nunca se abrió).

**La fase cierra por decisión explícita de Roberto**, tomada sobre el hallazgo de §16, no por un gatillo
de §8.1. Se dice acá para que nadie lea un gatillo donde hubo una decisión. Las consecuencias de §8.3 se
aplican igual y en su totalidad.

## 2. Presupuesto: 257 declarado, 4 corrido, 40 perdido, 156 sin usar

| | |
|---|---|
| **K_total declarado** | **257** (K₁ = 57 de la Fase 1 + K₂ = 200 de la Fase 2) |
| **K efectivamente corrido** | **4** configuraciones, todas en G2-multidía |
| **Perdidos por salida de alcance** | **40** (G1-nocturna, §5 de este veredicto) |
| **Sin usar al cierre** | **156** |

**El denominador no se mueve.** Los 40 perdidos no se retiran de 257 ni se reasignan (§1.4 + §2), y los
156 sin usar tampoco lo bajan: la línea de decisión de esta fase fue y sigue siendo **α/257 = 1,9455 ×
10⁻⁴ (|t| ≥ 3,726)**, calculada sobre el presupuesto **declarado**, nunca sobre el corrido. Cualquier
búsqueda futura **hereda K = 257** (§1.6).

## 3. La cadena del ledger

```
verify_ledger()  ->  True
líneas totales   ->  106     (60 de la Fase 1 + 46 de la Fase 2)
última línea     ->  d306d0016d212767   (CAMBIO_DE_REGLAS)
cierre Fase 1    ->  0020451ba0e4842b
acta Fase 2      ->  66693079f2c03099   (encadenada directamente al cierre de la Fase 1)
```

Las 60 líneas de la Fase 1 están **intactas y verificadas**: se comprueba en cada corrida de la suite,
que además falla si alguna cambió.

## 4. Tabla por familia

| Familia | Presupuesto | Usadas | Mejor resultado neto | Causa de cierre |
|---|---|---|---|---|
| **G1-nocturna** | 40 | 0 | — | **FUERA DE ALCANCE** (`9f6b4be689c3f061`): la hipótesis que el mapeo CME habilitaría tampoco cruza la frontera. **40 cartuchos perdidos.** |
| **G2-multidía** | 40 | **4** | **+$3.418,40** (reversión k=3, h=3) | Cierre de la fase con 36 sin usar |
| **G3-régimen** | 30 | 0 | — | Cierre de la fase; ninguna configuración pre-registrada |
| **G4-bordes** | 40 | 0 | — | **SOLO_MEDICIÓN** (`c8ce3fdea198d39a`): NO VALIDABLE para buscar; nunca gastó |
| **G5-cruzado** | 30 | 0 | — | Cierre de la fase; ninguna configuración pre-registrada |
| **G6-terceros** | 20 | 0 | — | Cierre de la fase — **y nunca tuvo criba de medibilidad**, así que no podría haber gastado un cartucho ni queriendo (§3.5 lo exige antes del primero) |

Las cuatro corridas, completas:

| # | Configuración | n | Neto | PF | Drawdown | t | p crudo |
|---|---|---|---|---|---|---|---|
| 1 | reversión k=3, h=3 | 244 | **+$3.418,40** | 1,276 | −$1.552,50 | +1,3075 | 0,1910 |
| 2 | reversión k=1, h=1 | 1.510 | −$252,75 | 0,994 | −$2.351,15 | −0,0767 | 0,9389 |
| 3 | momento k=1, h=1 | 1.718 | −$7.341,45 | 0,852 | −$8.168,80 | −2,3214 | 0,0203 |
| 4 | reversión σ, m=0,25, h=1 | 1.221 | −$338,15 | 0,991 | −$2.412,10 | −0,1055 | 0,9160 |

## 5. El mejor p-valor contra las dos líneas

```
línea de decisión  α/257  = 0,00019455      (|t| ≥ 3,726)
línea de la suerte 1/(K+1) = 0,00387597      (el mejor tiro esperado del azar en 257 intentos)

mejor p de la fase, cualquier signo : 0,020263  (cartucho 3, y su efecto es NEGATIVO: t = −2,32)
mejor p con efecto POSITIVO         : 0,191039  (cartucho 1)
```

Los dos quedan por encima de la línea de la suerte, así que la frase que §8.2 obliga a escribir va
escrita:

> **El mejor resultado de la búsqueda es peor que lo que produce el azar preguntando la misma cantidad
> de veces.**

Y la aclaración que impide leerla mal: el p más chico pertenece a una regla que **perdió plata**
($−7.341,45). Un p chico con la media del lado equivocado no es media victoria — es una regla que
pierde de forma más consistente que el azar.

## 6. Candidatas no decidibles con los datos existentes, con su cálculo de potencia

Ninguna configuración fue archivada bajo esa etiqueta formal, porque las cuatro murieron antes, en la
compuerta 1. Pero el cálculo de potencia se hace igual y es el dato que cierra la fase — **con la
ocupación real adentro**, que es la corrección que este veredicto agrega:

| # | n_A | ocupa A | n_B proyectado | ocupa B | z esperado | **potencia real** |
|---|---|---|---|---|---|---|
| 1 | 244 | **15,0 %** | 84 | 15,1 % | 0,767 | **11,6 %** |
| 2 | 1.510 | 31,0 % | 518 | 31,0 % | 0,045 | **5 %** |
| 3 | 1.718 | 35,3 % | 589 | 35,3 % | 1,359 | **27 %** |
| 4 | 1.221 | 25,1 % | 419 | 25,1 % | 0,062 | **5 %** |

**De dónde sale cada corrección**, sobre el cartucho 1, que es el mejor de los cuatro:

| escalón | supuesto | potencia |
|---|---|---|
| c **bruto** 0,0618, ocupación plena de las 1.669 sesiones | ninguno de los dos correcto | 71 % |
| c **neto** 0,048337, ocupación plena | `c` es bruto por definición; el examen mide **neto** | 51 % |
| c **neto**, **ocupación real 15,1 %** | la regla opera ~12 veces por año, no 1.669 | **11,6 %** |

`θ = z/√S_B = 0,068577` supone que la candidata está en el mercado **las 1.669 sesiones**. La identidad
`t = c·√(n·h)` usa las sesiones **ocupadas**. θ sigue siendo válida como **frontera** —cota optimista de
lo alcanzable— pero aplicada a una regla concreta que opera el 15 % del tiempo la halaga por un factor
2,6 en z.

> **Ninguno de los cuatro cartuchos podía abrir la caja fuerte de forma útil: ni pasando la puerta, ni
> si la puerta no existiera.** Y el cierre limpio: con la multiplicidad de la búsqueda la potencia del
> cartucho 1 daba 11,5 %; sin ella, bien calculada, da **11,6 %**. **Ganar la discusión sobre la
> multiplicidad no compró nada.** Lo que ata no es la penalidad de haber buscado: es que la regla opera
> doce veces por año.

## 7. Registro año por año de las candidatas que llegaron al examen final

**Ninguna llegó.** No hay registro que publicar, y no hay ninguna frase de "pasa 5/7 pero no 7/7" que
escribir. El contrapeso de §3.3 queda **sin usar y sin gastar**: sigue vigente para cualquier fase
futura tal como está escrito.

## 8. Ventanas de datos y SHA-256

**No se movieron.** Las declaradas en §4.4 el día 0 son las que corrieron:

| Régimen | Parte A | Parte B (sellada) |
|---|---|---|
| Diario / overnight | 2000-09-18 → 2019-12-31 (4.875 sesiones) | 2020-01-02 → 2026-08-19 (1.669) |
| Intradía | 2016-01-01 → 2019-12-31 (1.004) | 2020-01-02 → 2026-08-18 (1.669) |

Contraste de los SHA-256 contra los congelados en el acta (§4.5): **los tres idénticos.**

| Archivo | SHA-256 (acta = hoy) | bytes |
|---|---|---|
| `es_daily.csv` | `e2b84813…d7a1165` | 322.655 |
| `es_1min_databento.csv` | `7512c1ec…3efe1b0` | 327.741.114 |
| `spy_daily.csv` | `e246029…a5fb6ba` | 704.246 |

El test §27 verifica además que A y B no se tocan en ninguno de los dos regímenes, y que **ninguna
entrada de la Fase 2 corrió sobre la parte B**.

## 9. La deriva de reglas

```
huella en el acta : f4a9ea3539554c43
huella al cierre  : 8f3b5ed63f167483        -> HUBO DERIVA, y acá está
```

| Archivo | ¿cambió? |
|---|---|
| `factory/harness.py` | **No.** Byte a byte idéntico desde el acta, verificado en cada corrida |
| `factory/harness_f2.py` | **Sí** — `e38c36b3…` → `25bbaebf…` |
| `factory/spec_fase2.md` | **Sí** — `4dc9c7ea…` → `10b91311…`, +210 líneas |

**Todos los cambios están clasificados y ninguno es silencioso** (§12). La spec creció en tres commits
posteriores al acta —`b2b8997`, `13f494f`, `e17cde9`— con la criba de medibilidad, la política de
asignación, la vara de filtros como función y el bloque del estimador. Cada entrada del ledger lleva
sellada **la huella de reglas vigente al momento de escribirse**, así que para cualquier resultado se
puede recuperar exactamente bajo qué reglas se corrió.

## 10. Estado final de cada bloqueante (§7.6)

| Bloqueante | Estado al cierre | Vence | Consecuencia declarada |
|---|---|---|---|
| `margen_nocturno_mes` | **VIGENTE, sin resolver** | 2026-09-07 | La fase no puede pronunciarse sobre la **operabilidad** de ninguna candidata overnight, y eso se publica con cada una. El presupuesto no se toca. |
| `mapeo_dia_cme` | **SIN RELOJ** (su turno no llegó) | — | G4 saldría fuera de alcance con sus 40 perdidos |

**Ninguno venció**, así que no hay acta de consecuencia que escribir. El margen sigue sin dato: no se
inventó un número plausible para desbloquear nada, que era exactamente la tentación que §7.3 existe para
impedir. Ninguna candidata de esta fase fue declarada operable.

## 11. Criba de medibilidad por familia (§3.5)

Todas comparan **bruto contra bruto**, contra la referencia δ = 0,1749 (F4 en bruto, la mejor ventaja
que el proyecto midió jamás). Ninguna consumió presupuesto.

| Familia | Techo n_B | σ/op | Potencia exige | Fricción cuesta | **Bruto exigido** | Manda | Veredicto |
|---|---|---|---|---|---|---|---|
| G1-nocturna | 1.669 | $81,06 | 0,0686 | 0,0481 | 0,1167 | potencia | VALIDABLE |
| G2-multidía | 589 | $81,06 | 0,1154 | 0,0481 | 0,1636 | potencia | VALIDABLE |
| G3-régimen | 834 | $81,06 | 0,0970 | 0,0481 | 0,1451 | potencia | VALIDABLE |
| **G4-bordes** | 3.338 | $22,08 | 0,0485 | **0,1766** | **0,2251** | **fricción** | **NO VALIDABLE** |
| G5-cruzado | 834 | $81,06 | 0,0970 | 0,0481 | 0,1451 | potencia | VALIDABLE |
| **G6-terceros** | — | — | — | — | — | — | **NUNCA SE CRIBÓ** |

G4 es el único que la fricción mata: en tramos de ~30 minutos el peaje fijo de $3,90 pesa 0,1766 σ, y
ninguna ventaja que el proyecto haya medido lo paga. **Sus 40 cartuchos no se perdieron** — pasó a
SOLO_MEDICIÓN (§12), y al cierre sigue sin gastar ninguno.

**G6 no tiene criba y eso es un dato del método, no un olvido menor:** la familia "señales de terceros"
nunca llegó a tener reglas concretas que cribar. Sus 20 cartuchos quedan sin usar y **sin haber sido
nunca gastables**.

## 12. Los 19 `CAMBIO_DE_REGLAS`, con su dirección

**18 ENDURECEN. 1 AFLOJA.** Ninguno tocó una constante congelada: `assert_frozen_constants()` pasa al
cierre.

| # | Dirección | Resumen |
|---|---|---|
| 1 | ENDURECE | Criba de medibilidad por familia antes del primer cartucho |
| 2 | ENDURECE | Combinar estrategias es una búsqueda nueva, con presupuesto propio |
| 3 | ENDURECE | Criba por CONFIGURACIÓN dentro de `preregister()`, y clasificación ENDURECE/AFLOJA de todo cambio |
| 4 | ENDURECE | La criba incluye la fricción: compara BRUTO contra BRUTO |
| 5 | ENDURECE | Tope de concentración 40 % por mecanismo **y** por familia, cobertura de tenencias, mecanismo y h obligatorios |
| **6** | **AFLOJA** | **Estado SOLO_MEDICIÓN** (abajo, destacado) |
| 7 | ENDURECE | La vara de los filtros pasa de tabla a **función** de (φ, h_residuo); G3 y G5 declaran tres números |
| 8 | ENDURECE | Estimador de c: modelo (DL, punto por inversa de varianza) y distribución (t, df = m−1) declarados |
| 9 | ENDURECE | Migración de etiqueta de mecanismo con cita textual obligatoria |
| 10 | ENDURECE | n EFECTIVO dentro de un mecanismo: una operación se cuenta una sola vez |
| 11 | ENDURECE | El tope de concentración se evalúa con configs NOMINALES, evaluables antes de correr |
| 12 | ENDURECE | Supuesto de independencia declarado, y meta de mecanismos derivada del estimador vigente |
| 13 | ENDURECE | Dependencia medida sobre calendario común completo, y el filo del tope declarado |
| 14 | ENDURECE | Los DOS topes se verifican juntos; limitación de independencia cerrada con su IC |
| 15 | ENDURECE | **Análisis de potencia obligatorio ANTES de abrir una fase**, y prohibición del lenguaje de ausencia |
| 16 | ENDURECE | c se calcula con el σ OBSERVADO: procedencia fijada por test |
| 17 | ENDURECE | Ninguna extensión de la caja fuerte sin pre-registro sellado; **una sesión de A no entra jamás a B** |
| 18 | ENDURECE | **Piso del dataset `z·√(2/N)` y reparto A/B derivado del prior** |
| 19 | ENDURECE | θ es el umbral de 80 % de potencia, **no** un piso de detectabilidad; las tres ramas del examen final |

### El único que AFLOJÓ, destacado como manda §8.2

**`a38808eb29325ad1` — SOLO_MEDICIÓN para G4-bordes. Aprobado por: Roberto.**

> *"Fuera de alcance para BUSCAR no es inútil para MEDIR: una config de G4 no puede pasar la barra jamás
> pero SÍ da una estimación insesgada de c en el estrato h < 1, el único sin ningún dato. AFLOJA porque
> permite un gasto que las reglas de hoy prohíben. NO afloja la barra: esas configs nunca pueden ser
> candidatas ni abrir la caja fuerte, bloqueado en código. Cinco condiciones: (1) estado propio
> bloqueado en código; (2) consume cartucho igual, porque una corrida de sólo-medición SÍ revela
> rentabilidad; (3) la config queda vedada para siempre para la búsqueda; (4) su c entra al estimador en
> su propio estrato; (5) advertencia escrita: un resultado de acá que se vea ganador es señal de que algo
> anda mal en la MEDICIÓN, no un hallazgo."*

Al cierre **no gastó ni un cartucho**: la puerta se abrió y nadie la cruzó.

## 13. Configuraciones rechazadas por medibilidad antes de cobrar (§3.5b)

**Cero en el ledger real.** Las preguntas que decidimos no hacer están instrumentadas y probadas
—el test §14 verifica que una config demasiado infrecuente se rechaza **sin gastar cartucho**, y el
contrafactual documentado es que **el cartucho 1 no habría pasado esa criba** (n_B 84 contra 342
exigidos)— pero la criba por configuración entró en vigor **después** de que el cartucho 1 se corriera.
Se dice así y no de otra manera: la regla existe, es ejecutable, y llegó tarde para el único caso al que
le habría aplicado.

## 14. La caja fuerte

```
vault_uses()  ->  []
entradas de Fase 2 con part = "B"  ->  0   (de 46)
```

> **La caja fuerte NO se abrió. La parte B —2020-01-02 → 2026-08-19, 1.669 sesiones— sigue sellada, con
> su uso único intacto, disponible para quien siga.** No se tocó ni un archivo, ni una fila, ni un
> chequeo de integridad. Lo único que se consultó de B en toda la fase fue **su calendario** —cuántas
> sesiones tiene— que es una propiedad de las fechas y no de los precios, exactamente como §7.1 permite.

## 15. Los errores propios de la fase, cobrados al presupuesto

Como hizo el veredicto de la Fase 1, y sin editarlos.

| # | Error | Qué costó |
|---|---|---|
| 1 | **La fórmula publicada sin el factor 2.** Se publicó `z(0,05/257)/z(0,05/177)` como origen del 2,62 %; leída como está escrita da 2,88 %. Los z eran bilaterales y el documento no lo decía | **0 cartuchos.** Corregido a `z(0,05/(2·257))/…` + un test que **ejecuta la fórmula tal como está escrita en el documento** |
| 2 | **El estimador mezclaba dos estimadores**: punto por media simple, error estándar por DerSimonian-Laird | **0 cartuchos.** c pasó de 0,022455 a 0,023700 y el t de −1,686 a −1,6422 |
| 3 | **La distribución de referencia nunca se declaró.** Se usaba la normal por omisión | **0 cartuchos, pero 2 mecanismos de trabajo mal dirigido.** Declarada t con df = m−1, el p pasó de 0,1005 a 0,3482 y la meta de mecanismos de 3 a 6, después recalculada a 5/4 |
| 4 | **El cartucho 4 con 87,6 % de operaciones ya contadas** en el cartucho 2 (ρ = +1,0000 en la submuestra compartida) | **1 cartucho, el cuarto**, que compró mucha menos información de la que aparentaba: el error estándar del mecanismo estaba subestimado por 1,20× |
| 5 | **El conteo falso de aserciones** (abajo, con nombre) | **0 cartuchos, y un mensaje de commit falso durante 40 minutos** |
| 6 | **El bucket heredado del contador**: `estrato_de` clasificaba h = 1 como "intradía" porque la cota superior era inclusiva | **0 cartuchos.** Corregido a [0 , 0,999] antes de que ninguna cobertura se evaluara — la regla de cobertura recién ata en el cartucho 20 |

### El error nº 5, con nombre y con cómo se detectó

El commit `016148d` dice **"326 assertions, 0 failures"**. Era **falso al momento de escribirlo**: la
suite reportaba 325 OK y **1 falla**. El 326/0 se había medido **antes** de anexar la adenda que
introdujo la falla, y el commit pasó porque la suite corría **entubada a `tail`**, así que la shell leyó
el estado de salida de `tail` y no el de la suite.

Se detectó **leyendo la salida del test después de haber commiteado** —la línea `FALLA` estaba a la
vista, el estado de salida no— y se corrigió en un **commit nuevo, `e0e78de`, no enmendando**, para que
el registro muestre lo que pasó. El arreglo no fue "correr sin entubar", que es una costumbre: fue
`pipefail` + `PIPESTATUS` explícito en `tests/fase2/correr.sh`, **el veredicto escrito a un archivo** que
ninguna tubería puede tapar, y un test que **reproduce el bug como control** (una suite que falla,
entubada, sin `pipefail`, da 0 — y con `pipefail` no).

**Es el que mejor habla del método**, y por eso va con nombre: el sistema no evitó el error, pero lo
dejó a la vista, lo hizo reproducible y lo convirtió en una prueba que no lo deja volver.

### Un séptimo que no fue error, y se registra igual

Se afirmó que un bug del contador **había costado un cartucho**. Se verificó contra el ledger: en el
pre-registro del cartucho 4 sólo había 3 gastados y el tope arranca en el 5, así que **no pudo haber
disparado**. La afirmación se retiró. Vale la misma disciplina para los hallazgos propios que para los
ajenos: **si no se verifica, no es cierto.**

## 16. La causa raíz: **el reparto**, no el dataset, no la fricción, no los mecanismos

El día cero era computable, sin un solo backtest:

```
θ_B  = z/√S_B = 2,801585/√1669           = 0,068577      el umbral de 80 % de potencia
prior disponible  c(F4) = 0,174903/√7    = 0,066107      lo mejor medido en 58 configuraciones
piso del DATASET  z·√(2/N), N = 6.544    = 0,048978      hallar Y validar, ambos lados
```

**El prior superaba el piso del dataset y no superaba θ_B.** Es decir: **la fase era viable con estos
datos, y no lo era con este reparto.** Lo que ata no es θ_A ni θ_B por separado sino `max(θ_A, θ_B)`,
porque hay que hallar *y* validar, y ese máximo se minimiza exactamente en **50/50**:

| reparto | S_A | S_B | θ_A | θ_B | **el que ata** | prior 0,0661 |
|---|---|---|---|---|---|---|
| **74,5/25,5** (el real, heredado) | 4.875 | 1.669 | 0,040125 | **0,068577** | **0,068577** | **NO pasa** |
| 60/40 | 3.926 | 2.618 | 0,044712 | 0,054754 | 0,054754 | pasa |
| **50/50** | 3.272 | 3.272 | 0,048978 | 0,048978 | **0,048978** | **pasa** |
| 40/60 | 2.618 | 3.926 | 0,054754 | 0,044712 | 0,054754 | pasa |

Con el reparto real θ_B quedó **3,74 % por encima** del prior. **60/40 y hasta 40/60 también habrían
servido:** no hacía falta acertarle al óptimo, sólo no dejar θ_B arriba del prior.

> **El reparto 74,5/25,5 se heredó de la Fase 1 —donde la pregunta era "¿sobrevive alguna candidata al
> examen final?"— y no se volvió a mirar cuando la pregunta cambió a "¿cuánto vale c?". Un reparto
> heredado es un supuesto heredado. Nadie mintió y nadie se equivocó en una cuenta: el parámetro que
> decidía el resultado nunca entró en la discusión.**

### La precisión que no se puede perder

El piso de 50/50 (0,048978) **lo pasan el prior del día cero (0,066107) y el cartucho 1 (0,0618, que es
el MÁXIMO de cuatro y por lo tanto está sesgado hacia arriba)**. **NO lo pasa ninguna de las tres
estimaciones insesgadas**: liquidez CONSERVADORA 0,0419, liquidez GENEROSA 0,03315, estimador global
0,020260.

> **Por lo tanto la causa raíz es "la fase no pudo correr una prueba justa", y NUNCA "la fase se perdió
> un borde real". Lo segundo no se puede afirmar con esta evidencia.** El reparto correcto habría
> comprado una prueba justa; qué habría concluido, **no lo sabemos**.

**Y no se arregla retroactivamente.** Las 4.875 sesiones de la parte A ya se buscaron, y la regla §27 —
escrita en esta misma fase— prohíbe que una sesión que fue parte A entre a la parte B. Reciclar datos
buscados como si fueran caja fuerte sería la falsificación más grande que este programa podría cometer.
Esto va como causa raíz y como lección. **No como acción.**

## 17. La lección de método, que es lo que sobrevive a la fase

> **Ninguna fase se pre-registra sin publicar antes:**
> **(a)** su **efecto mínimo detectable**;
> **(b)** el **tamaño de efecto que espera encontrar**, con su fuente;
> **(c)** el **reparto A/B derivado de (b)**, con la cuenta que lo justifica.
>
> Si **(b) < el piso del dataset** `z·√(2/N)`, **la fase no se abre**: no hay reparto que la salve.
> Si el reparto propuesto pone **θ_B por encima de (b)**, **el reparto está mal, no la fase.**
> Cuando el objetivo es descubrir y después validar con la misma potencia de los dos lados, **el reparto
> óptimo es 50/50**, porque ambos lados necesitan el mismo `(z/c)²`. Un 70/30 optimiza el descubrimiento
> a costa de la validación — exactamente al revés cuando **la validación es la restricción que ata**.

Y la regla de lenguaje, que es la misma disciplina aplicada a cómo se escriben los resultados:

> **"No detectado" no es "no existe".** Con el umbral en 0,068577 y los efectos medidos entre 0,0139 y
> 0,0618, esta fase nunca tuvo forma de distinguir *ausencia de borde* de *borde real con muestra
> insuficiente*: las dos hipótesis producen exactamente los mismos datos.
>
> **Y θ es el umbral de 80 % de POTENCIA, no un piso de detectabilidad.** Un efecto apenas menor no es
> indetectable: es **menos probable de detectar**, y la redacción correcta lleva el número al lado
> ("detectable con 71 % de potencia", no "por debajo del piso").

Las dos están **cableadas en la suite**: `tests/fase2/test_dia0.py` §25 falla si aparece una formulación
de ausencia de efecto fuera de una cita tachada, y falla si aparece "no detectable" sin su cifra de
potencia al lado. Con sus controles, y con presupuesto de tachado para que la excepción no sea una
puerta trasera.

## 18. Un veredicto negativo no es un fracaso (§8.4, entero)

> Ya lo escribió el veredicto de la Fase 1 y sigue siendo cierto: es exactamente el dato que al proyecto
> de origen le costó meses y dinero real obtener sin spec. Y hay un segundo producto que no depende del
> resultado: **el ledger.** En un nicho saturado de backtests falsificados, un registro encadenado de
> fracasos con el denominador adentro es el argumento de credibilidad más fuerte disponible — y a esta
> altura ya tiene 257 líneas de denominador.

Ese párrafo se escribió **antes de conocer el resultado**. Se cumple al pie: el ledger cierra con **106
líneas encadenadas y verificadas**, 4 corridas, 40 cartuchos perdidos que **no se retiraron del
denominador**, 19 cambios de reglas cada uno con su dirección, 1 aflojada con su aprobación y su
argumento completo, seis errores propios cobrados sin editar, y una caja fuerte que **sigue sellada**.

## 19. Qué se cierra (§8.3)

**No hay Fase 3 de búsqueda sobre ES/MES.** No se agregan familias "sólo una más", no se afloja la vara,
no se re-corre nada con otra ventana. Los recursos vuelven al plan de ingresos —distribución de
`deadman`, auditorías, guardián para traders de prop firms—. Cualquier búsqueda futura necesita **spec
nueva, documento nuevo, y hereda K = 257** (§1.6), más los tres requisitos de §17 antes de pre-registrar
nada.

**Se publica**, sin edición de las derrotas: este veredicto, el ledger completo, los QC, el análisis de
frontera (`frontera_factibilidad.md`, 17 adendas con sus correcciones **en el lugar donde se
cometieron**), la spec y la suite.

---

*Cerrado el 2026-08-25. `verify_ledger() -> True`. Última línea: `d306d0016d212767`. La parte B nunca
se abrió.*
