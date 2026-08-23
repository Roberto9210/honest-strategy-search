# SPEC de búsqueda — FASE 2

*Se aprueba ANTES del primer backtest de la Fase 2 y no se cambia a mitad de camino. Igual que la v1:
los criterios se fijan antes para que los resultados no nos tienten a moverlos. La diferencia con la
v1 es que ahora sabemos qué nos falló: no la disciplina de escribir la vara, sino la de **contar
cuántas veces preguntamos**.*

**Estado:** borrador para aprobación de Roberto. Nada corre hasta que esté firmada.
**Antecedentes obligatorios:** `spec_busqueda_estrategia.md` (v1), `veredicto_fase1.md`,
`botc_potencia_f4.md`, `experiments_ledger.jsonl` (60 líneas, cadena verificada).

---

## 0. El problema que esta spec resuelve

Roberto quiere buscar **30 minutos por día, de forma indefinida**. Ese es un plan perfectamente
razonable y también la forma más eficiente conocida de fabricar un descubrimiento falso.

El motivo es aritmético, no moral. Bajo la hipótesis de que **ninguna** de las configuraciones que
probás tiene ventaja, el mejor p-valor de K pruebas sale, en promedio, en **1/(K+1)**. Con K = 57 eso
da 0.0172 — y ese número es exactamente el que mató a F4, cuyo p de 0.0212 era *peor que el azar
buscando la misma cantidad de veces*. Buscando 30 minutos por día durante un año, K llega fácil a
varios cientos: la línea de la suerte baja a 0.002, y cualquier cosa que "aparezca" con p = 0.01 va a
verse como un hallazgo y no va a serlo.

Una búsqueda diaria sin límite declarado **siempre** termina encontrando algo. Esta spec es lo único
que separa un método de una máquina de fabricar hallazgos.

Los cinco puntos que la spec tiene que fijar antes del primer backtest, y dónde están:

| | Qué | Sección |
|---|---|---|
| 1 | Presupuesto TOTAL de configuraciones (un número) | §2 |
| 2 | La barra en datos intactos, neta de costos | §3 |
| 3 | La corrección por multiplicidad acumulada, con fórmula | §1 |
| 4 | Qué entra y en qué orden: familias e instrumentos | §4 |
| 5 | La línea de parada | §8 |
| + | Ventana de datos por régimen, declarada antes | §4.4 |
| + | QC publicado antes del backtest, por instrumento | §4.5 |

Más las dos tentaciones concretas de esta fase, escritas para que nadie las borronee:
**alcance ≠ barra** (§5) y **F4 ya gastó su oportunidad** (§6).

---

## 1. El contador que nunca se reinicia

### 1.1 Qué se cuenta

**K = toda configuración de estrategia que alguna vez se evaluó contra datos de mercado en este
proyecto, desde la primera línea del ledger.** No se reinicia por cambio de fase, de familia, de
instrumento, de objetivo ni de persona.

- **K₁ = 57** — Fase 1. Es el conteo verificado del ledger publicado: 60 líneas = 57 configuraciones
  de estrategia (F1 20, F2 14, F4 10, F5 7, F3 6) + 2 autotests del harness con datos sintéticos + 1
  línea META del veredicto. Los 2 autotests no cuentan porque no evaluaron precios reales; están
  nombrados acá para que la resta sea auditable y no un ajuste conveniente.
- **K₂ = 200** — presupuesto declarado de la Fase 2 (§2).
- **K_total = K₁ + K₂ = 257.** Este número queda congelado en el momento de la firma.

Cuentan como configuración, sin excepción: las que ganan, las que pierden, las que dan cero
operaciones, **las que estaban mal diseñadas** (la Fase 1 gastó 3 cartuchos en un filtro roto y los
cobró igual), las que corre otra persona, las que propone un amigo, las que se corren "para ver", y
cada celda de cualquier barrido de parámetros.

### 1.2 La línea de decisión (Bonferroni sobre el conteo acumulado)

Una candidata solo se considera estadísticamente distinguible del ruido si, en la parte A y **neta de
costos**:

```
p_crudo  ≤  α / K_total
```

con **α = 0.05** declarada acá y para todo el programa, y **K_total = 257**:

```
p_crudo  ≤  0.05 / 257  =  1.9455 × 10⁻⁴      ⟺      |t|  ≥  3.726
```

El estadístico, definido acá para que no se pueda cambiar después:

```
t = media(neto_por_operación) / ( desvío(neto_por_operación, ddof=1) / √n )
p_crudo = erfc(|t| / √2)          (bilateral, aproximación normal)
```

Es exactamente el cálculo de `factory/botc_f4_reverify.py` §3. **No se sustituye por otro estadístico
después de ver los resultados** (ni bootstrap, ni Sharpe anualizado, ni "el t de las operaciones
ganadoras"). Si se quiere otro, se cambia acá y antes.

### 1.3 La línea de la suerte (el diagnóstico que se imprime siempre)

Al lado de todo resultado se reporta:

```
p_suerte(K) = 1 / (K + 1)        (p-valor esperado del MEJOR de K bajo la hipótesis nula global)
```

Con K_total = 257 ⇒ **p_suerte = 0.00388**.

No es la línea de decisión: es el espejo. Un candidato con p = 0.004 no es un hallazgo, es
*literalmente el promedio de lo que produce el azar habiendo buscado 257 veces*. La relación entre
las dos líneas es fija y vale la pena entenderla: `(α/K) / (1/(K+1)) ≈ α`, o sea **la línea de
decisión está 20 veces por debajo de la línea de la suerte**. Esa es la distancia entre "mi mejor
resultado" y "una evidencia".

### 1.4 Por qué el denominador es el presupuesto DECLARADO y no lo corrido

Si el denominador fuera "configuraciones corridas hasta hoy", el día 3 —con K = 60— la barra sería
`0.05/60`, y el día 60 —con K = 200— sería `0.05/200`. Eso crea un incentivo perverso y concreto:
**parar de buscar en el instante en que aparece algo bonito, porque frenar afloja tu propia barra.**
Es la misma trampa que el peeking al hold-out, con otro disfraz.

Por eso: **el denominador es 257 desde el día uno y hasta el final, se corran 200 configuraciones o
se corran 40.** Si la fase cierra con presupuesto sin usar, el sobrante **se pierde y se queda en el
denominador para siempre**. No hay devolución. La barra no puede aflojarse por buen comportamiento.

### 1.5 Sin ajuste por "pruebas efectivas"

Bonferroni sobre 257 configuraciones correlacionadas es conservador, y es verdad. `botc_potencia_f4.md`
§3 ya lo dice. **No se permite ningún ajuste que reduzca el denominador después de ver resultados**
(número efectivo de pruebas, componentes principales, "en realidad eran 8 ideas"). El motivo: el
tamaño de esa reducción es infalsificable a posteriori y siempre resulta ser justo el que hacía falta.

El remedio contra la sobre-conservadurización existe, y está disponible **antes**: **correr menos
configuraciones.** Declarar un presupuesto de 80 en vez de 200 es una decisión legítima que se toma
hoy, con la cara. Descubrir en noviembre que las 200 "eran realmente 30" no lo es.

### 1.6 Herencia

Cualquier fase futura empieza con **K = 257** y le suma su propio presupuesto declarado. La Fase 3, si
existe, dividirá α entre 257 + K₃. El contador es acumulativo hacia adelante, para siempre, y esa es
la única razón por la que los números de este proyecto significan algo.

---

## 2. Presupuesto total

> **K₂ = 200 configuraciones. Total, para toda la Fase 2. No por día, no por semana, no por
> familia renovable.**

Reparto por familia, declarado ahora (§4 explica cada una):

| Familia | Presupuesto |
|---|---|
| G1 — Prima nocturna / partición de sesión | 40 |
| G2 — Momento y reversión multi-día | 40 |
| G3 — Condicionamiento por régimen de volatilidad | 30 |
| G4 — Bordes de sesión intradía | 40 |
| G5 — Condicionamiento cruzado entre instrumentos | 30 |
| G6 — Reglas propuestas por terceros (los amigos traders) | 20 |
| **Total** | **200** |

**El presupuesto no usado de una familia no se transfiere a otra.** Si G3 se cierra por goleada en 8
configuraciones, las 22 restantes se pierden — no se convierten en 22 intentos más de G1. (La Fase 1
ya funcionó así: F3 cerró en 6/20 y F5 en 7/20, y nadie reclamó el resto.)

### Por qué 200 y no 50 ni 1000

El costo estadístico de un presupuesto grande es **sorprendentemente bajo**, y conviene verlo para
que la elección del número no parezca un regateo:

| K_total | α/K | \|t\| requerido | línea de la suerte |
|---|---|---|---|
| 57 (solo Fase 1) | 8.77 × 10⁻⁴ | 3.327 | 0.01724 |
| 107 | 4.67 × 10⁻⁴ | 3.499 | 0.00926 |
| 157 | 3.19 × 10⁻⁴ | 3.600 | 0.00633 |
| **257 (esta spec)** | **1.95 × 10⁻⁴** | **3.726** | **0.00388** |
| 557 | 8.98 × 10⁻⁵ | 3.917 | 0.00179 |
| 1057 | 4.73 × 10⁻⁵ | 4.070 | 0.00095 |

Cuadruplicar el presupuesto de 257 a 1057 sube el |t| exigido de 3.73 a 4.07: **un 9%.** La cola
normal es así de plana. Conclusión que hay que decir en voz alta: **lo que mata no es buscar mucho,
es buscar sin contar.** Un presupuesto de 1000 contado honestamente es infinitamente mejor que uno de
20 con tres barridos "que no cuentan".

**Y por eso mismo el presupuesto NO es un instrumento estadístico. Es un instrumento de DISCIPLINA.**

Esto hay que dejarlo escrito con toda claridad, porque el día que alguien quiera "ampliar un poco el
presupuesto" va a argumentar con la aritmética — y **la aritmética le va a dar la razón.** Va a
mostrar esta misma tabla y va a decir, correctamente, que pasar de 200 a 400 configuraciones cuesta
apenas unas centésimas de |t|. Va a tener razón en el número y va a estar equivocado en todo lo demás.

Porque lo que hace el presupuesto no es cambiar la aritmética: es **hacer que gastar un cartucho
duela lo suficiente como para pensar antes de gastarlo.** Un tope de 200 obliga a que cada
configuración sea una hipótesis con un mecanismo detrás, escrita en una línea antes de correrla. Un
tope de 2.000 no obliga a nada: se agota con un `for` anidado en una tarde, sin que nadie haya
pensado una sola vez. Los dos topes producen casi el mismo |t| exigido y **producen búsquedas
completamente distintas** — una hecha de hipótesis, la otra de barrido.

De ahí sale el número, y no de la tabla de arriba:

- **A un máximo de 5 configuraciones por sesión (§7.4), 200 son como mínimo 40 sesiones de trabajo**
  — unas 8 semanas de búsqueda real, que es el orden de magnitud de tiempo en el que un humano puede
  pensar 200 hipótesis distintas de verdad.
- **Un número que se agota con un `for` anidado no cumple ninguna función.** Ése es el criterio que
  descarta 2.000 tanto como descarta 20.

Corolario operativo, para que no haya que discutirlo en caliente: **el argumento "estadísticamente
cuesta muy poco ampliarlo" es verdadero y es irrelevante, y no alcanza para ampliar el presupuesto.**
Ampliar el presupuesto es cambiar la spec, y la spec se cambia antes de una fase, nunca durante — y
mucho menos en la semana en que una candidata quedó cerca.

---

## 3. La barra

Tres compuertas en serie. Una candidata que falla cualquiera de las tres **no es candidata**. Todos
los números son **netos de fricción** (§7.3), siempre, sin excepción ni nota al pie.

### 3.1 Compuerta 1 — parte A (desarrollo)

| Criterio | Vara |
|---|---|
| Pre-registro | La configuración está en el ledger **antes** de conocer su resultado (§7.2) |
| Operaciones | n_A ≥ 100 |
| Significancia corregida | \|t_A\| ≥ **3.726** (= p_crudo ≤ 0.05/257) |
| Rentabilidad | Factor de ganancia neto ≥ **1.3** |
| Robustez de parámetros | Vecindad declarada (±20%, o ±1 en enteros chicos): **ninguna celda pierde plata**, y la mediana de la vecindad tiene PF ≥ 1.15 |
| Robustez a valores extremos | Recalculado **quitando el mejor 1% de las operaciones**, \|t_A\| sigue ≥ 3.726 |
| No solapamiento | Una posición por vez; las operaciones son unidades no solapadas |

Dos notas que cierran agujeros conocidos:

- **El "quitar el mejor 1%"** es la vacuna contra el resultado tipo "PF 23.7 con 9 operaciones en 19
  años" que la Fase 1 encontró en F2 y correctamente llamó exposición al índice, no estrategia.
- **El no solapamiento** no es burocracia: posiciones solapadas producen operaciones correlacionadas
  entre sí, el desvío se subestima y el t se infla. Una configuración que no puede expresarse en
  unidades no solapadas queda excluida.

### 3.2 Compuerta 2 — potencia (se calcula ANTES de abrir nada)

Esta compuerta no existía en la Fase 1 y es la lección más cara que dejó `botc_potencia_f4.md`:
**el examen final solo sirve si puede responder la pregunta.**

Con δ̂ = media/desvío del neto por operación medido en A, y n_B = operaciones que la candidata
producirá en la parte B —**estimadas del calendario**, nunca de los precios de B:

```
n_B  ≥  (z_{α/2} + z_{1-β})² / δ̂²  =  (1.95996 + 0.84162)² / δ̂²  =  7.8489 / δ̂²
```

con **α_B = 0.05 bilateral y potencia mínima 1-β = 0.80.**

Equivalente y más útil en la práctica, porque se puede chequear apenas se tiene el t de A:

```
|t_A|  ≥  2.8016 × √(n_A / n_B)
```

Con las particiones de este proyecto (contadas del índice de fechas, sin leer un solo precio de B):

| Régimen | n_A disponible | n_B disponible | \|t_A\| mínimo para 80% de potencia |
|---|---|---|---|
| Diario / overnight (A = 2000-09-18→2019-12-31, 4.875 sesiones; B = 2020-01-02→2026-08-19, 1.669 sesiones) | 4.875 | 1.669 | **4.788** |
| Intradía (A = 2016–2019, 1.004 sesiones; B = 1.669 sesiones) | 1.004 | 1.669 | **2.173** |

**Consecuencia que hay que leer dos veces:** para una familia diaria, la caja fuerte es **un tercio**
del tamaño del set de desarrollo, así que pasar la compuerta 1 con lo justo (t = 3.73) **no alcanza**
— hace falta t_A ≥ 4.79. Para una familia intradía pasa lo contrario: la caja fuerte es **más grande**
que el set de desarrollo, y la compuerta 1 es la que manda.

Por lo tanto, la barra efectiva en A es:

```
|t_A|  ≥  max( 3.726 ,  2.8016 × √(n_A / n_B) )
```

⇒ **4.788 para familias diarias/overnight, 3.726 para familias intradía** (recalculado con el n_B real
de cada candidata, no con el ratio de sesiones, cuando la frecuencia de operación difiera entre A y B).

**Si la potencia proyectada es < 80%, la candidata NO se rechaza y NO se aprueba: se ARCHIVA** como
*"no decidible con los datos existentes"*, con su cálculo escrito, y **la caja fuerte no se abre.**
Ese es el destino de F4, ahora convertido en regla general en vez de en excepción.

Y una advertencia obligatoria en todo informe que use esta compuerta: **δ̂ medido en A está inflado
por selección** (es el ganador de una búsqueda). La potencia calculada con δ̂ es un **techo**, no una
estimación. Todo informe debe además reportar la potencia recalculada en el extremo inferior del
intervalo de confianza del 90% de δ̂ — como número informativo, no como compuerta.

### 3.3 Compuerta 3 — el examen final (la caja fuerte, un solo uso)

**La parte B, 2020-01-01 → 2026-08-19, sigue sellada. Un solo uso para TODO el programa.** No una vez
por candidata: **una vez, y se acabó.** La abre la primera candidata que pase las compuertas 1 y 2, y
solo por el camino `harness.run_on(..., examen_final=True)`, que la registra en el ledger.

Vara declarada ahora, antes de mirar nada:

| Criterio | Vara |
|---|---|
| Significancia | p ≤ 0.05 bilateral (prueba única pre-registrada; la multiplicidad ya se pagó en A) |
| Factor de ganancia neto | ≥ 1.3 |
| Degradación | La media neta por operación en B ≥ **50%** de la medida en A |
| Consistencia anual | ≥ 5 de los 7 años calendario positivos (se reporta el conteo completo, pase o no) |
| Peor racha | Drawdown ≤ 2× la mejor racha de ganancia equivalente |
| **Publicación año por año** | **Obligatoria, completa, pase o no pase** (ver abajo) |

**Si falla, muere.** No se re-ajusta, no se prueba "la variante de al lado", no se busca una ventana
mejor. Si falla, la Fase 2 cierra con veredicto negativo (§8) aunque quede presupuesto sin usar.

#### Contrapeso obligatorio del 5/7: el registro año por año se publica siempre

El 5/7 es la **única** celda de esta spec más blanda que la Fase 1, en una fase que sigue a un
fracaso, y el veredicto publicado dice textualmente *"rentabilidad positiva en cada año"*. Un lector
externo va a mirar justo ahí, y tiene razón en mirar ahí.

Por eso: **toda candidata que llegue al examen final publica su registro año por año, completo, pase
o no pase.** Para cada año calendario de la parte B y para cada año de la parte A: operaciones, neto,
factor de ganancia y drawdown. Sin resumir, sin agregar, sin "los años flojos fueron 2022 y 2024".

El motivo es explícito y va en el informe: **así cualquiera que quiera aplicar el criterio 7/7 lo hace
con nuestros propios números, sin pedirnos permiso.** No nos escondemos detrás de una barra más
blanda — publicamos exactamente el dato que permite imponer la más dura, y que el lector saque su
propia conclusión.

Si una candidata pasa 5/7 pero no 7/7, el informe **lo dice en el resumen, no en un apéndice**: *"pasa
la vara de la Fase 2 (≥5/7); no habría pasado la vara de la Fase 1 (7/7); acá están los siete años"*.
Esa frase es obligatoria.

### 3.4 Fase 2 no es una barra más blanda que la Fase 1

Se dice acá, antes de tener resultados, para que después no se pueda discutir:

| Criterio | Fase 1 | Fase 2 |
|---|---|---|
| Significancia estadística | **ninguna** | p ≤ 0.05/257 (t ≥ 3.726) |
| Multiplicidad | contada, no penalizada | penalizada, contador acumulado que no se reinicia |
| Suficiencia del examen | proxy: ≥ 200 operaciones en B | compuerta de potencia ≥ 80% (a F4 le habría exigido 342, no 200) |
| Potencia del examen final | no se calculaba | se calcula **antes** de abrir; sin 80% no se abre |
| PF neto ≥ 1.3 | en B | en A **y** en B |
| Robustez | vecindad ±20% | vecindad ±20% + caída del mejor 1% + no solapamiento |
| Usos de la caja fuerte | uno por candidata | **uno para todo el programa** |
| Años positivos en B | los 7 | ≥ 5 de 7 |
| Alcance | sin posiciones nocturnas | con posiciones nocturnas, declarado antes (§5) |

**Una sola celda es más blanda: los años positivos.** El motivo, escrito antes de ver un dato:
"todos los años positivos" es un criterio de comodidad económica, no estadístico, y aplicado a una
ventana de 7 años rechaza efectos verdaderos con alta probabilidad — un δ que apenas pasa la
compuerta de potencia tiene años negativos con toda naturalidad. En la Fase 1 el criterio era
gratuito porque **ninguna candidata llegó nunca al examen**; acá podría costar un hallazgo real. Todo
lo demás es estrictamente más duro, y las dos compuertas nuevas (significancia corregida y potencia)
son las que la Fase 1 no tenía y las que efectivamente mataron a su mejor candidata.

---

## 4. Qué entra, y en qué orden

### 4.1 El alcance de esta fase

- **Sí entran** posiciones nocturnas y de varios días. Es una ampliación de **alcance**, declarada de
  antemano, con el contador arrastrado, y está explicada en §5. El objetivo ya no es una prop firm
  con reglas de cierre diario, es cuenta propia (`botc_potencia_f4.md` §0).
- **No entran**: cajas negras, aprendizaje automático, indicadores comprados, reglas que no quepan en
  una página auditable. Igual que la v1.
- **No entra** nada de la lista de exclusión permanente (§6).

### 4.2 Familias, en este orden

Se corren **en orden**. Una familia no empieza hasta que la anterior está cerrada (por presupuesto
agotado, por goleada, o por candidata que pasa la compuerta 1).

**G1 — Prima nocturna / partición de sesión (40).**
Descomponer el retorno en cierre→apertura y apertura→cierre, y operar solo uno de los dos tramos,
condicionado por características explícitas del día previo (rango, dirección, volumen). *Mecanismo
previo declarado:* compensación por el riesgo de mantener exposición con el mercado cerrado.
*Por qué primera:* es la familia que la ampliación de alcance habilita directamente, produce ~1
operación por sesión (n_A ≈ 4.875, n_B ≈ 1.669) y por lo tanto es de las pocas con potencia real.

**G2 — Momento y reversión multi-día (40).**
Reversión o continuación después de k sesiones consecutivas en la misma dirección, o después de un
desplazamiento de m desvíos, con tenencia fija de N días. *Mecanismo previo:* provisión de liquidez a
flujo forzado (reversión) o rezago de difusión de información (continuación); la familia prueba las
dos direcciones y ambas cuentan.

**G3 — Condicionamiento por régimen de volatilidad (30).**
No es una estrategia: es un **estado** aplicado sobre una regla base explícita ya declarada. Ejemplo:
"G1 solo cuando la volatilidad realizada de 20 días está en su cuartil inferior". *Regla dura:* cada
combinación regla-base × definición-de-estado × umbral es **una configuración** y consume un cartucho.
Esta es la familia que más fácil se convierte en un barrido; el presupuesto de 30 es deliberadamente
chico por eso.

**G4 — Bordes de sesión intradía (40).**
Los primeros y últimos 30 minutos de la sesión regular sobre la serie de 1 minuto de Databento
(2016–2026). *Mecanismo previo:* concentración de órdenes en la apertura y en el cierre de subasta.
*Nota de potencia:* acá la parte B (1.669 sesiones) es **más grande** que la parte A (1.004), lo cual
es una ventaja estructural — la única familia del plan donde el examen final es más poderoso que el
desarrollo.

**G5 — Condicionamiento cruzado entre instrumentos (30).**
Una serie externa como estado de una regla sobre ES (estructura temporal de volatilidad, tasas,
un índice no correlacionado). **No corre hasta que su serie tenga informe de QC publicado** (§4.5) y su ventana declarada (§4.4).

**G6 — Reglas propuestas por terceros (20).**
Las estrategias de los amigos traders que el veredicto de la Fase 1 dejó en el banco de suplentes.
**Regla explícita:** una regla que te pasó otra persona **consume presupuesto exactamente igual**. No
es "la búsqueda de otro": en el momento en que la evaluás, es una hipótesis tuya, sale del mismo α y
entra al mismo contador. Este es un portillo obvio y queda cerrado acá.

### 4.3 Instrumentos

- **Primario: ES / MES.** Es el único instrumento con datos en mano y QC publicado.
- **SPY diario: solo control cruzado, nunca confirmación independiente.** El QC mide correlación de
  retornos diarios ES/SPY de **0.976**. Un resultado que "también funciona en SPY" no agrega evidencia
  independiente; agrega la comprobación de que el efecto está en el índice y no en una rareza del
  contrato. `botc_f4_reverify.py` §5 ya lo dice y esta spec lo hace obligatorio en todo informe.
- **Cualquier instrumento o serie nueva** (G5, o un instrumento adicional) entra por §4.5, sin
  excepciones y sin atajos.

### 4.4 Ventana de datos por régimen — declarada AHORA

La Fase 1 tiró 2010–2015 porque los datos **intradiarios** estaban colapsados en una barra diaria.
Pero ese defecto es de **resolución intradiaria**: para estrategias diarias/overnight esos mismos días
pueden servir perfectamente, porque su calidad diaria es otra cosa y se mide aparte. Entonces las dos
ventanas son distintas, y las dos se declaran acá, antes del primer backtest.

#### Régimen DIARIO / OVERNIGHT — familias G1, G2, G3, G5

- **Serie:** `data/es_daily.csv` (ES=F diario, Yahoo, front-month continuo sin ajustar por roll).
- **Ventana admitida: 2000-09-18 → 2026-08-19** (6.544 filas).
  Parte A = 2000-09-18 → 2019-12-31 (**4.875 sesiones**). Parte B = 2020-01-02 → 2026-08-19
  (**1.669 sesiones**).
- **Criterio de calidad que la habilita**, todo del QC ya publicado (`qc/data_quality_yahoo.md`):
  0 huecos > 3 días hábiles · 0 filas con `high < low` · 0 precios ≤ 0 · 0 saltos cierre-a-cierre
  > 20 % · 0 NaN en OHLC · índice monótono sin duplicados.
- **Exclusiones fijas:** las **10 filas con OHLC incoherente** (8 de ellas terceros viernes
  trimestrales — artefacto de roll de Yahoo), igual que en la Fase 1. Las **11 filas con volumen cero**
  se conservan porque sus precios son coherentes, **pero toda configuración que use volumen como
  entrada tiene que excluirlas** — G1 declara el volumen del día previo entre sus posibles filtros, así
  que esto no es hipotético.
- **Esta ventana YA es la máxima disponible en esta fuente.** 2000-09-18 es la primera fila que Yahoo
  tiene de ES=F: **no hay histórico diario que "extender"**. Cualquier ampliación exige una fuente
  nueva y entra por §4.5.
- **Prohibición explícita:** SPY — que sí llega hasta 1993-01-29 — **no es una serie de desarrollo.**
  Usar SPY 1993–1999 para "alargar la parte A" es cambiar de instrumento, y entra por §4.5, declarado
  antes, jamás después de una candidata.

#### Régimen INTRADÍA — familia G4

- **Serie:** `data/es_1min_databento.csv` (Databento `GLBX.MDP3`, `ohlcv-1m`, `ES.n.0`).
- **Ventana admitida: 2016-01-01 → 2026-08-18.**
  Parte A = 2016-01-01 → 2019-12-31 (**1.004 sesiones**). Parte B = 2020-01-02 → 2026-08-18
  (**1.669 sesiones**).
- **Criterio de calidad que la habilita.** Un año es admisible para el régimen intradía solo si cumple
  **los tres**, medidos en el QC publicado (`qc/data_quality_es_1min_databento.md`):
  1. **Sesiones comprimidas < 1 %** de los días de negociación (día con una barra que carga > 30 % del
     volumen del día — el defecto de los flat files pre-2017).
  2. **Barras por día ≥ 1.300** en promedio (una sesión completa son ~1.380 minutos).
  3. **Correlación anual ≥ 0.90** de los retornos diarios reconstruidos del 1-min contra la referencia
     diaria independiente (Yahoo).
- Lo que dicen los datos ya publicados, y por qué el corte cae en 2016:

  | año | % días con sesión comprimida | barras/día | corr vs diario | admisible |
  |---|---|---|---|---|
  | 2010 | 92.0 | 397 | 0.319 | no |
  | 2011 | 86.5 | 467 | 0.320 | no |
  | 2012 | 71.2 | 614 | 0.635 | no |
  | 2013 | 24.4 | 1.057 | 0.846 | no |
  | 2014 | 26.0 | 1.042 | 0.797 | no |
  | 2015 | 17.0 | 1.151 | 0.863 | no |
  | **2016** | **0.0** | **1.352** | **0.980** | **sí** |
  | 2017 | 0.0 | 1.340 | 0.972 | sí |
  | 2018 | 0.4 (1 día) | 1.347 | 0.978 | sí |
  | 2019 | 0.0 | 1.354 | 0.974 | sí |

  **No es una pelea de umbrales, es un escalón:** entre 2015 y 2016 el defecto pasa de 17.0 % de los
  días a 0.0 %, las barras por día de 1.151 a 1.352 y la correlación de 0.863 a 0.980. Movés los tres
  umbrales a donde quieras dentro de un rango razonable y el corte sigue cayendo en 2016.
- **Exclusiones fijas:** los **31 días marcados `degraded`** por Databento, y el único día de 2018 con
  barra comprimida (2018-08-05). Igual que la Fase 1.
- **2010–2015 no se re-habilita.** Si una re-curación futura de Databento arreglara esos años, eso es
  de hecho una fuente nueva: exige QC regenerado y publicado, y **declaración antes de que exista la
  candidata que se beneficiaría**.

#### La parte B entra entera

El criterio de admisión de esta sección selecciona la ventana de **desarrollo**; **nunca recorta la
caja fuerte.** Con el QC ya publicado, los siete años de B cumplen los tres criterios — el más
ajustado es 2024, con correlación 0.9046. Si una revisión futura de datos degradara un año de B por
debajo del criterio, **ese hecho se publica pero B no se vuelve a cortar**: re-cortar el hold-out
después de los hechos es exactamente lo que el sello existe para impedir.

#### La regla anti-trampa, que es el motivo entero de esta sección

**Las ventanas de arriba quedan congeladas al firmar.** Está prohibido ampliarlas, recortarlas o
cambiarles la fuente **después de** que haya corrido una sola configuración.

Dentro de tres semanas, justo después de una candidata que quede cerca de la barra, alguien va a
proponer "extender el histórico diario" o "recuperar 2013–2015 para intradía ahora que sabemos que el
defecto era parcial". **Va a tener razón técnicamente y va a estar haciendo trampa**, porque la
ventana elegida después de ver un resultado es un parámetro más de la búsqueda — uno que no está
contado en K y que nadie va a contar. Por eso se declara hoy, cuando todavía no hay ninguna candidata
a la que le convenga una respuesta u otra.

Si aun así se decide ampliar una ventana, la ampliación **es una fase nueva**: spec propia,
presupuesto propio, y el contador heredado (§1.6). No es una corrección técnica de la Fase 2.

### 4.5 QC antes del backtest, por instrumento

**Ninguna configuración corre sobre una serie que no tenga su informe de control de calidad generado
y publicado en `qc/` primero.** Sin excepciones, sin "después lo genero", sin "es la misma fuente que
la otra".

Requisitos para incorporar cualquier instrumento o serie nueva, en este orden:

1. **Costo consultado y aprobado antes de comprar.** Como en la Fase 1, donde `databento_estimate.py`
   cotizó $17.90 con una llamada de metadata (gratis) **antes** de ordenar nada.
2. **QC generado y publicado en `qc/`, ANTES del primer backtest sobre esa serie.**
3. **Publicado tal como sale del script.** Nada se corrige, se rellena ni se suaviza; todo lo raro se
   informa como se encontró. Es la regla que ya rige en `qc/README.md` y se mantiene.
4. **La misma frontera de partición 2020-01-01**, para que la caja fuerte siga siendo un objeto único
   y coherente entre instrumentos.
5. **Su ventana admitida y su criterio de calidad declarados en §4.4** antes de correr, igual que las
   dos que ya están.

**Una configuración corrida sobre una serie sin QC publicado es una violación de spec:** se registra
como tal en el ledger, con su resultado, y **consume presupuesto igual.**

El motivo es la lección más cara de la Fase 1: seis años de datos intradiarios comprados y tirados,
porque el QC los revisó **antes** de que produjeran un solo número. Si el mismo defecto hubiera
aparecido después de una ruptura de rango rentable en 2011, nadie lo habría ido a buscar. Por eso el
enunciado va textual, y es la frase que gobierna esta sección entera:

> **Un defecto encontrado antes del backtest es un problema de datos; el mismo defecto encontrado
> después de un backtest rentable es un descubrimiento que nadie hace.**

**Congelamiento de datos (trabajo del día 0):** se registra en el ledger, como entrada `meta`, el
SHA-256 de cada archivo de datos que la Fase 2 va a usar. Yahoo revisa su historia y Databento re-cura
días degradados; si un archivo cambia a mitad de fase, eso se detecta en vez de contaminar
silenciosamente los resultados. Los datos no se publican (los términos de Yahoo y Databento no lo
permiten); los hashes sí.
---

## 5. Alcance ≠ barra (la primera tentación de esta fase)

Esta distinción es la que decide si la Fase 2 es honesta o es un truco, así que va con nombres
propios.

**Una BARRA es un criterio que un resultado tiene que superar.** Mover una barra después de ver los
resultados es fraude, punto. Es lo que la Fase 1 no hizo ni una vez, y es lo único que hace valer su
veredicto negativo.

**Un ALCANCE es el conjunto de cosas que estás dispuesto a probar.** La Fase 1 excluyó las posiciones
nocturnas porque el objetivo de entonces era operar en una prop firm, y las prop firms exigen cerrar
al final del día. Eso fue una restricción **operativa derivada del objetivo**, no una afirmación
sobre la evidencia.

**Ampliar el alcance en una fase NUEVA, declarada de antemano y con el contador de multiplicidad
arrastrado, es honesto.** Estás comprando hipótesis nuevas a precio completo: entran al ledger antes
de conocer su resultado, consumen cartuchos, y se miden contra un α dividido por un K que incluye
todo lo que ya preguntaste. No hay ninguna ganancia gratis en la operación.

**Lo deshonesto sería contar retroactivamente a F4 como un éxito de la Fase 1.** El razonamiento
tentador suena así: *"F4 fue excluida por alcance; ahora el alcance cambió; entonces F4 pasa."* Es
falso, y se puede verificar en un renglón: F4 tenía **dos** causas de exclusión y el cambio de
alcance solo elimina una.

| | F4, aplicando la barra de HOY con el alcance de HOY | ¿Pasa? |
|---|---|---|
| t en parte A | 2.304 (p = 0.0212) | — |
| Línea de decisión con el K de la Fase 1 SOLA (57) | requiere \|t\| ≥ 3.327 | **NO** |
| Línea de decisión con K_total = 257 | requiere \|t\| ≥ 3.726 | **NO** |
| Línea de la suerte de la Fase 1 sola, 1/58 | 0.0172 — F4 sacó 0.0212, **peor que el azar** | **NO** |
| Compuerta de potencia (80 vueltas de mes en B, δ̂ = 0.1515) | potencia 27.3%; harían falta 342 operaciones ≈ 28 años | **NO** |

**La prueba que se aplica siempre que alguien invoque un cambio de alcance:** *"si el alcance hubiera
sido amplio desde el día uno, ¿esta candidata habría pasado la barra?"* Para F4 la respuesta es no,
por cuatro caminos distintos, **incluso usando el denominador más generoso posible.** El cambio de
alcance no le agrega ni un dato.

Corolario general: **un cambio de alcance abre puertas hacia adelante, nunca hacia atrás.** Habilita
hipótesis que todavía no se probaron. No re-puntúa las que ya se probaron y perdieron.

---

## 6. F4 está muerto (la segunda tentación, con nombre y apellido)

**F4 — vuelta de mes / turn-of-month — ya gastó su oportunidad.** Perdió contra la multiplicidad
(§5), y una fase nueva no lo resucita. Queda en **lista de exclusión permanente**.

### 6.1 Qué está excluido, con nombre

- La función `turn_of_month` de `factory/familias_4_5.py` y **cualquier** configuración suya
  (incluidas, pero no limitadas a, las tres del ledger publicado: `{n_before:4, m_after:3}`,
  `{2,2}`, `{5,5}`). *Nota de precisión:* `botc_potencia_f4.md` y `botc_f4_reverify.py` llaman
  "línea 16" a la configuración `{4,3}`; ese es su índice base-0. Contando líneas del archivo desde 1
  es la **línea 17**. Se identifica por configuración, no por número, para que la referencia no
  dependa de esa convención.
- **Cualquier regla cuyo momento de entrada o salida esté definido principalmente por la distancia a
  un borde de mes o de trimestre**, se llame como se llame: fin de mes, vuelta de mes, ventana de
  rebalanceo, semana de liquidación, efecto de fin de trimestre, "T-4/T+3", "últimos N días hábiles",
  "primeros M días del mes", o cualquier renombre futuro.
- La prueba a aplicar, para que la etiqueta no importe: **¿el calendario del mes es lo que determina
  cuándo opera esta regla?** Si la respuesta es sí, está excluida — sin importar el instrumento, los
  parámetros, la familia bajo la que se presente, ni quién la propuso.

### 6.2 Las cuatro puertas traseras, cerradas una por una

1. **Como "hallazgo nuevo".** Si dentro de tres semanas alguien redescubre el efecto de cambio de mes,
   **no es un hallazgo nuevo: es el mismo candidato muerto con otra ropa.** No entra al ledger como
   configuración de la Fase 2, no consume presupuesto, no se reporta.
2. **Como filtro o estado dentro de otra familia** (por ejemplo, "G1, pero solo durante la vuelta de
   mes"). Excluido: es F4 usando a G1 de vehículo.
3. **Como estrategia "de un amigo" en G6.** Excluido. El origen no lava el historial.
4. **Vía la caja fuerte.** La parte B **no es para F4**. F4 no puede pasar la compuerta de potencia
   (27.3%), así que por construcción nunca llega a la compuerta 3. Abrirla para él sería quemar un
   recurso de un solo uso en una prueba que ya sabemos que no puede responder.

### 6.3 Lo único que quedaría, y por qué no es esto

Existe **una** vía teóricamente válida para F4, y está en `botc_potencia_f4.md` §6: un estudio
**confirmatorio pre-registrado con n = 1 hipótesis** sobre **mercados nuevos** (no sobre la parte B,
que es el mismo mercado y la misma época). Eso **no es una búsqueda y no es la Fase 2**:

- Va en su propio documento (`protocolo_confirmatorio_f4.md`), no acá.
- No consume presupuesto de la Fase 2, no abre esta caja fuerte, y **no puede reportarse jamás como
  un hallazgo de la Fase 2.**
- Exige medir **antes** la matriz de correlación de los retornos de vuelta de mes entre mercados (no
  de los retornos diarios), porque los índices bursátiles globales no son independientes y el n
  efectivo va a ser muy inferior al nominal. Sin esa medición previa, el estudio no empieza.
- Su informe tiene que abrir diciendo que es la re-prueba de una candidata que ya falló.

Y si alguna vez se hace un forward test de F4 en simulador, rige la advertencia de
`botc_potencia_f4.md` §6: el **Simulated Data Feed** de NinjaTrader genera un mercado aleatorio
interno sin correlación con datos reales, y un walk-forward sobre esos precios se vería idéntico a
uno real en todos los reportes. **El informe tiene que nombrar qué feed produjo los precios.** Sin esa
línea, el resultado no es interpretable.

---

## 7. Reglas inviolables

### 7.1 La caja fuerte

**2020-01-01 → 2026-08-19 sigue sellada. Un solo uso para todo el programa.** Se abre únicamente
cuando una candidata pasó las compuertas 1 y 2 (§3), y solo por `harness.run_on(examen_final=True)`,
que deja registro. Lo único que se puede consultar de la parte B sin abrirla es su **calendario**
(cuántas sesiones, cuántos meses tiene) — que es una propiedad de las fechas, no de los precios,
exactamente como hizo `botc_f4_reverify.py` §4. Cualquier otra lectura de B es una violación de la
spec y se registra como tal en el ledger.

### 7.2 Pre-registro: al ledger antes de conocer el resultado

**Toda configuración entra al ledger antes de correrse.** El harness actual registra *después* de
correr (`run_on` llama a la estrategia y luego a `log_experiment`), lo cual es suficiente para contar
pero no para probar que no hubo cribado previo. Cambio requerido antes del primer backtest de la
Fase 2 (§9):

1. `preregister(family, config, note)` escribe una entrada con `result: null` y devuelve su hash.
2. `run_on` **exige** un pre-registro abierto que coincida con `(family, config)` y enlaza el
   resultado a su hash.
3. Un resultado sin pre-registro previo es una violación de spec: se registra como tal, con el
   resultado incluido, y **la configuración consume presupuesto igual**.

**Los errores de diseño también consumen presupuesto.** La Fase 1 gastó 3 cartuchos en un filtro mal
diseñado (la ventana nocturna hasta las 09:29, que producía 0–1 operaciones) y los cobró igual. Una
configuración rota que se re-corre arreglada es **una configuración más**, no la misma otra vez. Una
búsqueda que re-corre gratis sus propios errores no está midiendo nada.

**Barridos y vecindades.** Cada celda de un barrido de parámetros es una configuración. La única
excepción, y es estrecha: la **vecindad de robustez** de una configuración **ya pre-registrada**, si
(i) se declaró como vecindad de robustez en el pre-registro, y (ii) **ninguna de sus celdas puede
adoptarse como la candidata**. Si se escanea la vecindad y después se adopta la mejor celda, eso es
selección y **las celdas cuentan todas**. Caso concreto y publicado, para que se entienda el filo del
cuchillo: en el bloque 3×3 de F4, la celda (4,2) daba PF 1.691 contra el 1.507 de la publicada (4,3).
Adoptar (4,2) habría sido gastar 9 cartuchos, no cero.

### 7.3 Los costos van adentro de cada número, nunca en una nota al pie

- Fricción base, sin cambios respecto de la v1: **$3.90 por operación ida y vuelta por contrato**
  ($1.40 de comisión + 2 ticks de slippage a $1.25). La descuenta `harness.evaluate_trades`, no el
  código de la estrategia, para que ninguna estrategia pueda olvidarse.
- **Costo de roll (nuevo, y necesario por la ampliación de alcance):** la serie diaria es de contrato
  continuo front-month. Toda tenencia que atraviese un roll de contrato **paga una fricción
  adicional completa ($3.90)**. Se declara ahora, antes de que exista una candidata multi-día a la
  que le convenga la otra respuesta. Las 10 filas de artefacto de roll identificadas en el QC de
  Yahoo quedan excluidas, como en la Fase 1.
- **Margen nocturno:** mantener MES fuera del horario de day-trading exige margen inicial, muy
  superior al margen intradía. **Ese número no se inventa acá.** Antes de correr la primera
  configuración de G1 se copia a este documento el requisito vigente, con **fecha y fuente**, y se
  declara con qué tamaño de cuenta la familia sería operable. **Si el número no está, G1 no corre.**
  (Regla de la casa: falta un dato de riesgo ⇒ bloqueo con motivo explícito, nunca un default
  plausible.)
  - **Cuál número.** El del **bróker**, no el de CME. El de la bolsa es el piso; el que te van a
    exigir de verdad para sostener la posición de un día para el otro es el del bróker, y suele ser
    más alto. Usar el de CME porque es el que se encuentra citado más fácil es subestimar el capital
    necesario justo en la familia que abre esta fase.
  - **Cómo se lee.** En NinjaTrader: `Tools → Instruments`, buscar **MES**, ahí figura el requisito.
    Se anota el valor **y la fecha en que se leyó** — eso es lo que la spec pide como "fuente".
  - **Lo que NO cuenta como fuente:** un número inferido de la base local de NT8, una cifra de CME
    puesta "mientras tanto", o cualquier valor sin fecha. Un requisito de margen guardado en una
    instalación local puede ser un default viejo y no lo que el bróker exige hoy; ponerlo igual sería
    exactamente el modo de falla que esta regla existe para impedir.
- Ningún resultado bruto se reporta en ningún documento. Si un número aparece sin costos, es un error
  de redacción, no una variante de presentación.

### 7.4 La sesión diaria de 30 minutos

Orden fijo, y nada se corre fuera de una sesión:

1. Verificar la cadena del ledger (`harness.verify_ledger()` ⇒ `True`). Si da `False`, la sesión se
   suspende y se investiga; no se corre nada.
2. Escribir el **pre-registro** de las configuraciones del día, con su hipótesis en una línea.
3. Recién entonces, correr.
4. Anexar resultados y el diagnóstico obligatorio: `t`, `p_crudo`, `α/K_total`, línea de la suerte
   `1/(K_total+1)`, y `K_usado / 200`.
5. Cerrar la sesión anotando el contador.

**Máximo 5 configuraciones por sesión.** Una sesión en la que no se registra nada es una sesión
válida y no hay que compensarla al día siguiente. El presupuesto es un techo, no una cuota.

### 7.5 Ledger

Append-only, encadenado por hash, verificable por terceros (`harness.verify_ledger()`), nunca
editado, nunca reordenado. Se verifica al abrir y al cerrar cada sesión. Es la misma pieza que hace
que el veredicto de la Fase 1 signifique algo.

---

## 8. La línea de parada

### 8.1 Qué la dispara (lo que ocurra primero)

1. **Presupuesto agotado:** 200 configuraciones de Fase 2 registradas.
2. **Calendario:** **2027-02-28.**
3. **Familias cerradas:** las seis familias cerradas por presupuesto o por goleada.
4. **Examen final fallado:** una candidata abrió la caja fuerte y no pasó la compuerta 3. La fase
   cierra **inmediatamente**, quede el presupuesto que quede.

### 8.2 Qué se escribe

`factory/veredicto_fase2.md`, con esto y en este orden:

- K_total declarado (257), K efectivamente corrido, y el sobrante perdido.
- La cadena del ledger verificada, con el hash de la última línea.
- Tabla por familia: presupuesto, configuraciones usadas, mejor resultado neto, causa de cierre.
- **El mejor p-valor obtenido en toda la fase, comparado explícitamente contra la línea de decisión
  (1.95 × 10⁻⁴) y contra la línea de la suerte (0.00388).** Si el mejor p queda por encima de la línea
  de la suerte, se dice esa frase: *el mejor resultado de la búsqueda es peor que lo que produce el
  azar preguntando la misma cantidad de veces.*
- Las candidatas archivadas como **"no decidibles con los datos existentes"**, con su cálculo de
  potencia.
- **El registro año por año, completo**, de toda candidata que haya llegado al examen final — pase o
  no pase (§3.3). Si pasó con 5/7 y no con 7/7, esa frase va en el resumen, no en un apéndice.
- Las ventanas de datos usadas por régimen y la confirmación de que no se movieron (§4.4), más el
  contraste de los SHA-256 de los archivos de datos contra los congelados el día 0 (§4.5).
- **Si la caja fuerte se abrió o no**, y si no, la afirmación explícita de que sigue sellada.
- Los errores propios de la fase, cobrados al presupuesto, como hizo el veredicto de la Fase 1.

### 8.3 Qué se publica y qué se cierra

Se publica: el veredicto, el ledger completo y los QC nuevos, en el repositorio, con el README
actualizado — igual que la Fase 1, sin edición de las derrotas.

Se cierra: **no hay Fase 3 de búsqueda sobre ES/MES.** No se agregan familias "solo una más", no se
afloja la vara, no se re-corre nada con otra ventana. Los recursos vuelven al plan de ingresos
(distribución de deadman, auditorías, guardián para traders de prop firms), como manda la §8 de la
v1. Cualquier búsqueda futura necesita **spec nueva, documento nuevo, y hereda K = 257** (§1.6).

### 8.4 Un veredicto negativo no es un fracaso

Ya lo escribió el veredicto de la Fase 1 y sigue siendo cierto: es exactamente el dato que al
proyecto de origen le costó meses y dinero real obtener sin spec. Y hay un segundo producto que no
depende del resultado: **el ledger.** En un nicho saturado de backtests falsificados, un registro
encadenado de fracasos con el denominador adentro es el argumento de credibilidad más fuerte
disponible — y a esta altura ya tiene 257 líneas de denominador.

---

## 9. Trabajo del día 0 (antes del primer backtest, sin excepción)

1. `harness.preregister()` + `run_on` exigiendo pre-registro coincidente (§7.2).
2. `harness.stat_test(trades)` que devuelva `t`, `p_crudo`, `α/K_total`, `1/(K_total+1)` y el veredicto
   contra la línea de decisión — para que el diagnóstico sea automático y no una decisión de quien
   escribe el informe.
3. `harness.power_check(delta_hat, n_b_proyectado)` implementando §3.2, y `run_on(examen_final=True)`
   **negándose a correr** si no hay un `power_check` aprobado previo en el ledger para esa candidata.
   La compuerta 2 tiene que estar en el código, no en la buena voluntad.
4. `PASS_BAR_F2` con los valores de §3, y `passes_bar` devolviendo las razones de falla, como ya hace.
5. Entrada `meta` en el ledger con: apertura de Fase 2, K₁ = 57, K₂ = 200, K_total = 257, α = 0.05,
   y los SHA-256 de los archivos de datos congelados (§4.5).
6. Copiar a §7.3 el margen nocturno vigente de MES, con fecha y fuente. **Sin ese número, G1 no corre.**
7. `harness.WINDOWS` con las dos ventanas de §4.4 cableadas por régimen (diario/overnight e intradía),
   con sus exclusiones fijas (las 10 filas de OHLC incoherente, los 31 días `degraded`, 2018-08-05), y
   `run_on` **negándose a correr** sobre fechas fuera de la ventana de su régimen. La ventana tiene que
   estar en el código, no en la memoria de quien corre el backtest.
8. `harness.report_per_year(result)` que emita el registro año por año exigido por §3.3, para que
   publicarlo sea el camino por defecto y no un acto de voluntad.

---

*Borrador v1 de la Fase 2 — 22 de agosto de 2026. Para aprobar o corregir por Roberto antes de correr
nada. Una vez firmada, los números de las §1, §2, §3 y §4 no se tocan hasta el veredicto.*
