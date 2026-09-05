# EL JUEZ — cómo se usa

Para alguien que no vivió la semana. **No gasta cartucho. K = 261. Construir la herramienta no es
usarla.** Usarla sobre un candidato real sí puede gastar: contá contra K.

## Qué hace

Toma un candidato —**entradas y reglas, nunca resultados**— y calcula contra ES 1-min 2016-2019
cuánto rinde en dólares por sesión, neto de comisión y deslizamiento medidos, y si ese rendimiento
viene de información o del patrón. Devuelve un veredicto de cuatro valores:

| veredicto | qué significa |
|---|---|
| **SUPERA** | da dólares positivos, bate las nulas **válidas para su clase de ventaja** y la pasiva, y **aguanta en los tres regímenes** de volatilidad |
| **APUESTA AL REGIMEN** | bate todo, pero la ventaja vive en un solo tercil de volatilidad. Categoría propia, no un aprobado con asterisco |
| **NO SUPERA** | no da dólares, o no bate alguna nula, o no bate la posición pasiva equivalente |
| **NO MEDIBLE** | el juez se niega: pocas operaciones, bracket sin sesgo caracterizado, ventana demasiado angosta para rotar, entradas fuera de los datos |

Un juez que siempre da un número es peor que ninguno.

## Correrlo

    cd research/ventana_g
    python juez.py candidato.json
    python juez.py candidato.json --verificar          # segunda corrida: muestra 2019
    python juez.py candidato.json --pasivo             # entrada pasiva en vez de cruzar el spread

**Modo entrada (`--pasivo`).** Por defecto el juez cobra la entrada por **mercado** (cruzás el spread,
~+0,13 pt = ~$6,5/mini). Con `--pasivo` la entrada **descansa en el mejor precio**: en vez del
medio-spread se aplica el markout medido (astilla positiva ~+0,04 pt) y sólo se llena ~47-51% de las
señales. El piso de referencia baja fuerte (de +$78/+$93 a +$15/+$32 por sesión). **Pero el modo
imprime, en el veredicto, una advertencia obligatoria:** está calibrado sobre **entradas al azar**; para
un candidato **direccional** el markout puede darse vuelta (sus llenados están seleccionados por su
propia señal), así que el piso pasivo es una **cota optimista** hasta medirlo sobre el candidato real
(el hook `medir_pasivo_candidato`, el paso que sigue, sin correr todavía). El modo **no cambia el
veredicto** de ningún control: mueve el observado y las nulas juntos, sólo baja el nivel del piso.

**El período reservado.** 2016-2018 es trabajo, 2019 es verificación. La primera corrida juzga
2016-2018 y **anota** el veredicto en el registro; el resultado de 2019 se **retiene**. Sólo una
corrida posterior con `--verificar`, cuando el de trabajo ya está anotado, muestra 2019. Es
pre-registro real: el registro está encadenado con hash y la fecha queda antes de mirar.

**La caja sellada (2020-2026)** se niega por defecto. Sólo se abre con `--caja --prerregistro
<archivo>` y el archivo tiene que estar **commiteado en git antes de la corrida**, sin cambios
locales. Nada intermedio. Y aun así este juez no carga datos de 2020+: abrir la caja es otra corrida
con otro replicador, a propósito.

## El archivo de entrada

```json
{
  "nombre": "mi_candidato",
  "instrumento": "ES",
  "contratos": 1,
  "limite_contratos": 4,
  "variantes_probadas": 3,
  "clase_ventaja": "direccional",
  "familia": "reversion_apertura",
  "regla_salida": {"tipo": "bracket", "objetivo_pt": 5, "stop_pt": 20},
  "operaciones": [
    {"ts": "2017-03-06T14:31:00", "lado": "largo"},
    {"ts": "2017-03-06T15:02:00", "lado": "corto"}
  ]
}
```

- `instrumento`: `ES` o `MES` (las únicas dos con comisión medida).
- `contratos` por operación y `limite_contratos` de la cuenta: el juez calcula la exposición
  simultánea máxima con la tenencia que dan los datos y **rechaza** si excede el límite.
- `variantes_probadas`: **obligatorio.** Cuántas variantes de esta idea se probaron antes de traer
  esta. El juez no puede verlo; por eso se declara. Es inverificable, y por eso el silencio no se
  acepta: el umbral de desvíos se ajusta a esa cifra (3,0 con una variante; 3,7 con diez; 4,3 con
  cien) y el veredicto lo dice en su cara: **"este número supone que se probaron N variantes; si
  fueron más, no vale"**.
- `clase_ventaja`: **obligatorio.** `direccional` (la ventaja está en *qué lado*) o `timing` (está en
  *cuándo* entrar; el lado es indiferente o aleatorio). Se declara **antes** de correr, porque de eso
  depende **qué nula es válida** para este candidato — ver *La clase de ventaja* más abajo. Declarar
  mal no es gratis y declarar `timing` no compra nada: el juez mide la firma y la contrasta.
- `familia` (opcional): nombre de la idea. El registro cuenta intentos por familia declarada **y** por
  huella de entradas a tres tamaños de cubeta, para que no se esquive con esperas.
- `regla_salida`: `bracket` (objetivo y stop en puntos) o `tiempo` (`n_barras`). Se declara; el juez
  no la adivina. El bracket tiene que estar dentro del rango donde el sesgo de contabilidad está
  medido (span 20–35 puntos, p entre 0,15 y 0,85); si no, NO MEDIBLE.
- `operaciones`: instante de entrada (coincide con una barra de un minuto, sin redondeo) y lado.

**Ejemplo válido:** `ejemplos_juez/valido.json`. **Ejemplo rechazado:** `ejemplos_juez/rechazado.json`
(trae un campo `pnl`; el juez lo rechaza en la puerta con el motivo escrito).

### Lo que se rechaza, y por qué

Cualquier campo que huela a resultado —`pnl`, `profit`, `precio_salida`, `win`, `mae`, `ts_salida`…—
rechaza la entrada entera. No es una comodidad que se le saca al usuario: el juez calcula los
desenlaces él mismo, y eso es lo único que hace **imposibles** la censura, la selección de
ganadoras y el sesgo de supervivencia, en vez de evitables.

## La clase de ventaja — por qué se declara, y por qué no es una puerta trasera

Las dos nulas no son intercambiables. La de **signo** destruye *qué lado* y por lo tanto **no puede
ver** una ventaja que esté en *cuándo*: contra una ventaja de timing pura devuelve −1% de lo
inyectado. Como el "informativo" es el **mínimo** de las tres, una ventaja de timing de cualquier
tamaño moría en la nula que no la mide. Ése era un falso negativo **estructural**, no un umbral duro.

El mínimo se queda —es lo que defiende del ataque A1, y sacarlo abriría el juez de par en par—. Lo que
cambia es **cuáles** nulas entran al mínimo, y el orden lo decide todo:

1. El candidato **declara** `clase_ventaja` en la entrada, antes de correr.
2. El juez **mide la firma** sobre los desvíos de las dos nulas: rotación alta con signo ≈ 0 →
   `timing`; las dos altas → `direccional`; cualquier otra cosa → `indefinida`.
3. La nula de signo se omite **sólo si la firma medida CONFIRMA lo declarado**. En cualquier otro caso
   se aplica el mínimo estricto de las tres.
4. Si declarado y medido **no coinciden**, sale **BANDERA ROJA** en el veredicto, con los dos desvíos.

**Las tres nulas se informan siempre**, se usen o no; la omitida sale impresa con el motivo. La
declaración queda en el registro (`clase_declarada` y `firma_medida`), así que cambiarla después de
ver el resultado deja rastro.

**Por qué declarar `timing` no alcanza para pasar:** la relajación no se gana declarando, se gana con
la firma medida. Un candidato **sin ventaja** que declare `timing` tiene rotación ≈ 0, su firma sale
`indefinida`, no confirma nada, y recibe el mínimo estricto: **NO SUPERA** (control C10, en los dos
modos). Lo que la declaración compra es que, cuando la ventaja *sí* está y *sí* es de cuándo, no la
mate el instrumento que no la puede ver.

### Cuántas veces la firma se equivoca — medido, no argumentado

La firma **sólo puede contradecir, nunca confirmar**: un candidato nulo que sea falso positivo de la
rotación saldría con firma `timing` y se le quitaría la nula de signo justo cuando más falta hacía.
C10 no toca ese caso (su firma es `indefinida`, aprueba por el camino fácil), así que se midió aparte
con **20.000 candidatos nulos** (`juez_firma_falso_positivo.py`):

| medida | 1.000 nulos | 20.000 nulos |
|---|---|---|
| `zA ≥ 3,0` (falso positivo de la rotación **sola**) | 0,20% | **0,15%** |
| **firma `timing`** (`zA ≥ 3,0` **y** `\|zB\| < 1,0`) | 0,000% | **0,000%** — IC95 arriba **0,019%** |
| firma `direccional` | 0,00% | 0,03% |
| nulos que **llegarían a aprobación** declarando `timing` | 0 | **0 de 20.000** |

**Por qué sale tan bajo, y la razón es estructural:** bajo la nula `zA` y `zB` están correlacionadas
**+0,91** — miden el mismo observado contra dos nulas centradas en lo mismo. Un nulo que por azar
queda alto contra la rotación queda alto también contra el signo, y entonces su firma es
`direccional`, no `timing`. La firma de timing exige la combinación **rara**: alto contra una y
neutro contra la otra.

**Y hay un segundo cerrojo que nunca se abre:** la relajación quita **una** de las tres nulas. La
**pasiva no se omite jamás**, así que un falso positivo de firma todavía tiene que batir
`min(rotación, pasiva) ≥ 3,0`. Ninguno de los 20.000 lo hizo. El costo del arreglo, medido en falsos
positivos, es **cero sobre 20.000**.

*La tabla se hizo viable con una **tabla de desenlaces** precomputada por barra y por lado (1,02 M
barras), verificada contra `J.resolver` en 3.000 ranuras de los dos lados antes de usarse: sin eso,
20.000 × 200 rotaciones serían días de cómputo.*

Esto vale **también en el chequeo por régimen**: dentro de cada tercil se compara contra la nula
válida para la clase confirmada, no siempre contra la de signo. Sin eso el punto ciego volvía a entrar
por la ventana del régimen (ver el CIERRE).

## Qué devuelve, y en qué unidades

- **Dólares por sesión, neto**, con comisión (help.tradeify.co, 2026-09-03), deslizamiento medio en
  el stop (`media_exceso.py`), **deslizamiento de ENTRADA** —el medio-spread por cruzar, ~0,13 pt por
  operación, medido por régimen en `microestructura_tbbo.py`, antes tratado como cero— y la corrección
  de contabilidad aplicada **sólo en la dirección conservadora** (`o = 0,0642 ± 7,6%`; nadie la cobra
  eligiendo el bracket) con su error propagado. Cobrar la entrada movió el piso de referencia
  +$35/sesión (5pt:20pt) y +$20/sesión (20pt:10pt): es del orden de la comisión.
- **Las dos nulas**: rotación (destruye *cuándo*; **sólo dentro del rango de fechas del candidato**)
  y signo (destruye *qué lado*; conserva las ranuras). Y un **tercer punto**: una posición pasiva de
  la misma exposición neta promedio sobre el mismo intervalo. Van las tres.
- **Error por permutación, nunca binomial.** El binomial se muestra al lado con el factor "ganado".
- **La resolución**, siempre: ±33% de la ventaja con ~5.000 operaciones. *"No detectó nada"* no es
  *"no hay nada"*.
- **Por régimen**: terciles de volatilidad **en puntos básicos** (rango/precio) de la **sesión
  anterior** — un eje **conocible al entrar** y **comparable entre épocas** (verificado en
  `juez_regimen_bps.py`: el piso es monótono y el cociente alto/bajo es 13,1× en 5pt:20pt y 4,4× en
  20pt:10pt, contra la vara de ≥3×; sólo 23% de las sesiones cambian de etiqueta contra el eje en
  puntos). Se juzga en bps porque un bracket de 20 puntos es 1,1% del precio en 2016 y 0,26% en 2026:
  en puntos el eje conflacionaría nivel de precio con volatilidad. La volatilidad de la sesión
  *entera* en puntos incluye lo que pasó después de cada entrada; ese eje se llama **hindsight**,
  sólo **describe** el piso (`juez_regimen.py`) y se imprime aparte. La ventaja tiene que aguantar
  en los tres terciles ex-ante:
  positiva y a **≥ 1,5 desvíos** contra la nula de signo dentro del tercil (un tercil sin datos
  —menos de 20 sesiones— cuenta como no verificado y bloquea SUPERA). Ese umbral es permisivo a
  propósito, porque cada tercil tiene un tercio de las sesiones; un tercil nulo lo cruza por ruido
  ~7% de las veces, y sólo importa cuando el global ya pasó.
- **P(pasar) por la cadena eval × fondeada** (Tradeify Growth 50K): lo que el producto paga. Una
  media positiva con cola izquierda gorda fracasa igual.
- **La regla del vehículo**: si la ventaja medida supera el piso, avisa que a esa ventaja conviene
  capital propio y no la evaluación (el cruce cae en el propio piso, `vehiculo_ventaja.py`).
- **LO QUE ESTE VEREDICTO NO CUBRE**, obligatorio. Entre otras: el deslizamiento de entrada ahora se
  **cobra** (medio-spread por mercado), pero supone entrada por mercado —una entrada **pasiva** no lo
  paga y en cambio corre no-ejecución y selección adversa, la pregunta de mbo diseñada sin correr en
  `MBO_DISENO_entrada_pasiva.md`; la consistencia de las firmas no está modelada; y **qué clases de
  ventaja ve**: la direccional y la de tamaño se recuperan al 91-95%; la de **timing** sólo si se
  declara y la firma la confirma; una ventaja de **salida** (cuándo cerrar) es inexpresable por
  construcción, porque la regla de salida se declara y se aplica igual a todas las operaciones.

## El registro y el contador

`REGISTRO_JUEZ.jsonl`, una línea por juicio, **encadenada con hash**: borrar o editar una línea rompe
la cadena y el juez lo avisa en cada corrida siguiente. Cuenta intentos de la misma familia y sube
el umbral. Guarda también `clase_declarada` y `firma_medida`, para que cambiar la clase entre corridas
deje rastro. **Defiende contra el descuido, no contra alguien motivado:** se puede correr en otra
copia del repo o con otro registro. Agujero conocido y marcado.

**La clase declarada está DENTRO de la huella, y antes no lo estaba.** `hash_candidato` incluye ahora
`clase_ventaja`. Lo que había antes era peor de lo que se creía: el mismo candidato reclasificado daba
**el mismo hash**, y el bucle de hermanos saltea las filas con hash igual ("es el mismo candidato en
otro período") — o sea que correrlo como `direccional`, ver NO SUPERA y volver como `timing` **no
contaba como intento ni subía el umbral**. Era gratis. Con la clase adentro: la segunda corrida es un
candidato distinto con huella de entradas idéntica → cuenta como hermano, el umbral sube, sale un
bloque **RECLASIFICACIÓN** en el veredicto con la fecha y el veredicto anterior, y el candado de 2019
**se re-cierra** (`ya_anotado` mira ese hash, así que reclasificar no destapa el período reservado).

**El registro commiteado abre con dos líneas del ejemplo.** Son las dos corridas de `valido.json` que
ejercitan la CLI (cruce y pasivo), candidato sintético, no un candidato real. **No se borran:** la
cadena es de sólo-agregar desde su primera línea, y resetearla a mano sería exactamente el gesto que
el diseño dice que nadie puede hacer. El efecto sobre un candidato futuro es **conservador** —si su
huella se parece a la del ejemplo, cuentan como dos hermanos y el umbral **sube**, nunca baja—.

## El agujero mayor, dicho en la cara

El juez **no puede ver la búsqueda que ocurrió antes** de que el candidato llegara. Por eso exige la
declaración de variantes y la imprime en el veredicto. Si la declaración miente, el veredicto no
vale, y no hay código que lo detecte.

## Controles

`python juez_controles.py` corre **diez** controles con condición de falla escrita contra resultados
publicados: sin ventaja → NO SUPERA; ventaja inyectada → SUPERA y recupera la magnitud; pocas
operaciones → NO MEDIBLE; entrada con resultados → RECHAZADA; ventaja en un solo régimen (tercil alto
de volatilidad) → APUESTA AL REGIMEN; el candidato solo-largo de 2017 → NO SUPERA con la defensa
puesta (y se muestra sin la defensa, para ver que hace falta); ventaja sólo en tendencias bajistas
→ APUESTA AL REGIMEN, la prueba de que cerrar el eje de dirección no dejó un agujero; un candidato
en el **borde** entre modos → NO SUPERA en cruce / REQUIERE MEDICION en pasivo, nunca SUPERA; una
**ventaja de timing declarada bien** → SUPERA; y la **puerta trasera**, un candidato sin ventaja que
declara `timing` → NO SUPERA igual. Los diez se corren en los **dos modos**, y se verifica que el modo
pasivo nunca devuelve SUPERA. Salida en `salida_juez_controles.txt`.

Otras corridas, cada una con su salida commiteada:
`juez_verificar_prueba.py` (el candado de 2019 en las dos direcciones),
`juez_rutas_nunca_corridas.py` (el detector de firma por `informe()` y el juez por **línea de
comandos**, en subproceso real), `juez_particion_potencia.py` (la partición trabajo/verificación),
`juez_firma_falso_positivo.py` (20.000 nulos contra la firma de timing) y
`calibrar_por_regimen.py` (el inventario de calibración por instrumento y la vara por régimen).

---

# CIERRE — el juez está terminado

**Versión final, 2026-09-05.** `juez.py` + `juez_controles.py` + `mbo_lib.py`. No queda trabajo
pendiente **que no requiera un candidato real**.

## Los diez controles, en los dos modos (10/10 y 10/10)

| control | qué prueba | CRUCE | PASIVO |
|---|---|---|---|
| C1 | sin ventaja | NO SUPERA | NO SUPERA |
| C2 | ventaja inyectada, recupera la magnitud | **SUPERA** | **REQUIERE MEDICION** |
| C3 | pocas operaciones | NO MEDIBLE | NO MEDIBLE |
| C4 | entrada con resultados | RECHAZADA | RECHAZADA |
| C5 | ventaja en un solo régimen | APUESTA AL REGIMEN | APUESTA AL REGIMEN |
| C6 | el ataque A1 (solo-largo 2017) | NO SUPERA | NO SUPERA |
| C7 | ventaja sólo bajista | APUESTA AL REGIMEN | APUESTA AL REGIMEN |
| C8 | candidato en el **borde** entre modos | NO SUPERA | **REQUIERE MEDICION** |
| C9 | **ventaja de timing** — verifica **la nula aplicada**, no el veredicto | **SUPERA** | **REQUIERE MEDICION** |
| C10 | **la puerta trasera**: nulo declarando `timing` | NO SUPERA | NO SUPERA |

**C9 dejó de mirar sólo el veredicto, y el motivo era un agujero real.** En modo pasivo
REQUIERE MEDICION es lo que `techo_pasivo` devuelve para *cualquier cosa que superaría*, así que el
control pasaba **sin distinguir si la nula correcta se había aplicado**: el arreglo de timing estaba
ejercitado en cruce solamente. Ahora C9 chequea cuatro cosas, iguales en los dos modos: (1) la firma
confirma la clase declarada; (2) omitir la de signo **cambia el número** (`z_info > z_estricto`);
(3) **sin** el arreglo el candidato no pasaría (`z_estricto < z_req`); (4) **con** el arreglo pasa.
Medido: en pasivo `z_info = +22,8` contra un estricto de `+0,1` — el arreglo hace todo el trabajo, y
ahora el control lo dice. *Falla si el veredicto es el esperado pero `z_info == z_estricto`.*

**Ningún control devuelve SUPERA en modo pasivo**, y no puede: `techo_pasivo` lo convierte por
construcción. C8 quedó recalibrado con `c8_semillas.py` (12 semillas × 3 valores de ventaja): a
q=0,56 sólo el 42% de las semillas caía en el borde y 5 de 12 quedaban **por encima** (SUPERA en
cruce); a **q=0,545** las 12 dan NO SUPERA en cruce y **9 de 12 (75%) cruzan hacia arriba** en pasivo,
sin ninguna llegar a SUPERA. El suite usa una semilla dedicada para que el borde no dependa del sorteo.

**C9 aísla el timing del régimen a propósito.** La ventaja se inyecta en el mejor tercio **dentro de
cada tercil** de volatilidad, no en el mejor tercio global. Con selección global el mismo candidato da
**APUESTA AL REGIMEN**: el juez sí ve la ventaja, pero informa que vive concentrada en un régimen. Son
dos cosas distintas y conviene no confundirlas al leer un veredicto.

## El candado de 2019, ejercitado en las dos direcciones

Era la única parte del juez **escrita pero nunca corrida**. Probada (`juez_verificar_prueba.py`), 4/4:

| prueba | resultado |
|---|---|
| `--verificar` con registro limpio (trabajo NO anotado) | **se niega**, retiene 2019 |
| sin `--verificar` | juzga trabajo, lo anota, retiene 2019 y dice cómo verlo |
| `--verificar` con el trabajo ya anotado | **muestra 2019**, veredicto propio |
| el informe de verificación | completo: veredicto, tabla de dólares, las tres nulas, régimen |

Un candado probado sólo abriéndolo con la llave correcta no está probado; éste se probó cerrado y
abierto. **"Escrito" y "alguna vez ejercitado" ya son el mismo número.**

## El punto ciego, medido — no declarado

Todos los controles inyectaban la misma forma de ventaja (elegir el lado). Se inyectaron dos formas
nuevas (`juez_formas_ventaja.py`) y se midió qué recupera el instrumento:

| forma | inyectada | rotación recupera | signo recupera | veredicto |
|---|---|---|---|---|
| **TIMING** (sabe cuándo, lado al azar) | +$403,04/sesión | **98%** (+22,2σ) | **−1%** (−0,2σ) | **NO SUPERA** |
| **TAMAÑO** (acierta 50%, arriesga más al acertar) | +$559,75/sesión | 91% (+11,1σ) | 95% (+11,6σ) | **SUPERA** |

**El punto ciego de timing era TOTAL, no parcial.** Una ventaja de timing de +$403/sesión, medida y
recuperada al 98% por la nula de rotación, se descartaba igual, porque el "informativo" es el
**mínimo** de las tres nulas y la de signo la ve al −1%. Cualquier ventaja de timing pura, **del tamaño
que sea**, recibía NO SUPERA. La de tamaño, en cambio, el juez la ve bien (91-95%).

## El punto ciego, ARREGLADO — con la clase declarada por adelantado

La salida es la clase de ventaja declarada y **verificada contra la firma medida** (ver *La clase de
ventaja*). El mismo candidato de +$403, declarando `timing`, ahora da **SUPERA** en cruce con los tres
terciles aguantando (+11,6σ / +12,7σ / +15,6σ). Y un candidato **sin ventaja** que declare `timing`
sigue dando **NO SUPERA** en los dos modos: no hay puerta trasera, porque la relajación la habilita la
firma medida, no la declaración.

**El arreglo estaba a medias y C9 lo expuso.** La primera versión omitía la nula de signo del
informativo **global** pero el chequeo por **régimen** seguía comparando siempre contra la de signo:
las ventajas por tercil daban ≈ +$1 en vez de +$417 y el veredicto caía en APUESTA AL REGIMEN. El punto
ciego volvía a entrar por la ventana del régimen. Se guarda ahora la nula de rotación **por sesión**
(`VA`) y `regimen()` elige la nula válida para la clase confirmada. Recién con eso C9 pasa.

No se agregó una tercera forma: la que faltaría es una ventaja de **salida** (cuándo cerrar), y el juez
la prohíbe por construcción — la regla de salida se declara y se aplica igual a todas las operaciones.

## Las dos rutas que estaban escritas y nunca corridas (5/5)

`juez_rutas_nunca_corridas.py`:

| ruta | resultado |
|---|---|
| el **detector de firma** por `informe()` (timing declarado `direccional`) | imprime la BANDERA ROJA (rotación +22,4, signo +0,1) |
| CLI sin argumentos | código **2** + el uso |
| CLI con `rechazado.json` | código **1** + el motivo del rechazo |
| CLI con `valido.json` | código **0** + el veredicto |
| CLI con `valido.json --pasivo` | código **0** + el veredicto, `[MODO PASIVO]` |

La CLI es la capa que va a tocar un lanzador de doble clic, y era la única sin una corrida encima. Se
ejercita en **subproceso real**, no importando el módulo, para que los códigos de salida cuenten.

## La partición trabajo / verificación, calculada al revés — y NO aplicada

`juez_particion_potencia.py` calcula qué fracción habría que reservar para que la verificación tenga
**la misma resolución** que el trabajo. Da **54% / 46%**, corte en **2018-02-21**. El intercambio: el
piso de detección del trabajo sube **+10%** ($20,54 → $22,55) y el de la verificación baja −4%
($25,84 → $24,74).

**DECISIÓN TOMADA (Roberto, 2026-09-05): NO se reparticiona. Queda 3/1** — trabajo 2016-2018,
verificación 2019 — **y la verificación queda declarada SUBPOTENCIADA. El número se publica:**

> **La verificación de 2019 tiene resolución ±72% de la ventaja de referencia, contra ±33% del
> período de trabajo: es 1,26× más gruesa (MDE $25,84 contra $20,54 por sesión). 2019 solo NO PUEDE
> confirmar un efecto del tamaño que el juez exige en trabajo.** Cualquier lectura de un resultado de
> verificación tiene que llevar esa cifra al lado.

El motivo de no repartir es la **cobertura de régimen**: el corte de igual potencia cae en 2018-02-21,
y un trabajo que empiece a cortarse ahí pierde el tercil alto de volatilidad, que sólo 2018 aporta. La
restricción que manda es la cobertura, no el conteo de sesiones.

**CORRECCIÓN (2026-09-05) al motivo que se publicó primero.** El hallazgo de "la MDE no es monótona"
—salta de $8,56 con 501 sesiones a $22,55 con 541, porque el desvío por año iría de $36 a $368— es
cierto **para la serie que usó ese script** (flujo secuencial con los dos lados **promediados**, que
se cancelan casi enteros y dejan un residuo que la cola de 2018 domina) y **no se traslada al error
con el que el juez decide**. Medido en `calibrar_por_regimen.py` sobre el flujo con el que se calibró
el juez: el desvío por año va de $791 a $1.095 (factor 1,4) y **el desvío de la nula de permutación
—que es el error que el juez usa— da $48/$42/$55/$51 por año, baja monótono en todo el barrido**. La
recomendación de no reparticionar se sostiene, pero **por la cobertura de régimen y no por la
no-monotonía**: el motivo bueno era el segundo.

## Otros instrumentos: la calibración se separó de la maquinaria

El juez aceptaba **ES y MES y nada más**, y eso resultó ser el problema equivocado de resolver
primero: la VENTANA L trajo once candidatas y las más fuertes son de **divisas** o necesitan flujo de
órdenes, o sea que las mejores son justo las que el juez no puede juzgar. Fue un error de **orden** —
se construyó la herramienta antes de saber qué había que medir.

Lo que se hizo es hacer explícita la frontera, en `instrumentos.py`:

**MAQUINARIA — no depende del instrumento, se queda en `juez.py`:** las dos nulas y la comparación
pasiva; la clase de ventaja y la firma; el eje de régimen por terciles y la exigencia de los tres;
que el modo pasivo nunca apruebe; los seis veredictos; el registro encadenado y la huella; el umbral
por multiplicidad; la caja sellada; el candado de 2019; la puerta de entrada.

**CALIBRACIÓN — depende del instrumento, vive en la ficha, cada constante con su ORIGEN:**

| origen | qué es | qué cuesta |
|---|---|---|
| **ESPEC** | valor del punto, tick, equivalencia en micros, horario de sesión | **gratis** — especificación oficial del CME |
| **REGLA** | comisión de ida y vuelta | **gratis** — lista de precios. *Para divisas NO está leída: la página que tenemos cubre índices.* |
| **MEDIDO** | deslizamiento de entrada por régimen (tbbo) · markout y llenado pasivos (mbo, **sólo si se usa modo pasivo**) · exceso en el stop y la constante `o` (**sólo si la regla es un bracket**) · los cortes de tercil en bps (barras diarias, casi nada) | **hay que comprar datos** |
| **FALTA** | no está | el juez **se niega** |

**Sustituir la calibración de un instrumento por la de otro está prohibido en el código.** Un
medio-spread de ES aplicado a 6E devuelve un número con cara de veredicto. `calibracion()` levanta
`NoCalibrado` y el juez rechaza la entrada listando exactamente qué falta y de dónde saldría. La
única herencia permitida es MES ← ES, declarada **como herencia** en la propia ficha (mismo
subyacente, mismo libro, mismo tick en puntos).

**Y esto abarata a las candidatas de la VENTANA L:** L07 y L08 **no usan bracket** —miden el retorno
de una ventana declarada—, así que se caen los dos ítems más caros (sobrepaso y exceso en el stop).
Para juzgarlas en modo cruce alcanza con punto y tick (gratis), comisión (una lectura),
medio-spread por régimen (tbbo, poco) y los cortes de tercil (barras diarias).

**Qué costaría llenar las fichas de divisas** (`databento_cotizar_divisas.py`, cotizado
2026-09-05, **sin comprar**): el paquete entero —L08 (6 símbolos × 48 fechas × 4 h, `ohlcv-1m`), L07
plan B (6J × 286 fechas gotobi), `tbbo` de 6E en tres días (uno por tercil) y `ohlcv-1d` de los seis
símbolos 2016-2019— sale **USD 0,87** contra los USD 98,92 de crédito. Ningún ítem se acerca al tope
de USD 3,00. La calibración de 6E que el juez necesita para dejar de negarse cuesta **USD 0,55** de
ese total.

**Cómo calibrar sin repetir el error de 2018** (`calibrar_por_regimen.py`): el **piso** y la
**resolución** no se comportan igual entre regímenes. El piso varía **13×** entre el tercil alto y el
bajo (publicado en `juez_regimen_bps.py`); la **dispersión** varía **1,3×** entre terciles y 1,2×
entre años. Conclusión: **el piso se calibra por régimen, la resolución se agrupa** — separar la
resolución sólo tira potencia. *Esto contradijo la mitad de la hipótesis con la que se abrió ese
archivo, y la condición de falla estaba escrita antes; queda anotada como fallada.* Y el piso del ES
**no hay que recalcularlo** — ya está por tercil; lo que hay que corregir es **cómo se cita**: "el
piso del ES es $X" con un solo número promedia regímenes que difieren 13×.

## Los seis veredictos

**SUPERA** (sólo cruce o medición por-candidato) · **APUESTA AL REGIMEN** · **NO SUPERA** ·
**REQUIERE MEDICION PASIVA POR CANDIDATO** (sólo pasivo) · **NO MEDIBLE** · **RECHAZADA**.

El registro **cuenta los REQUIERE MEDICION sin resolver** y el juez imprime, al emitir uno, cuántos
lleva acumulados; a partir del tercero avisa que se están juntando cotas optimistas que nadie convirtió
en veredicto firme.

## Las tres deudas abiertas — las tres necesitan un candidato

1. **El markout pasivo por-candidato.** Calibrado sobre entradas al azar; para un candidato direccional
   puede darse vuelta.
2. **El 53% no llenado por-candidato.** Se supone neutral (cierto al azar); para un candidato el
   no-llenado está seleccionado por su señal.
3. **El régimen alto de 2026 lo cubre sólo 2018.** Ningún día posterior a la caja cae en el tercil alto.

Las tres las salda el mismo hook, `medir_pasivo_candidato`: el sim FIFO sobre las entradas **reales**
de un candidato. No se puede correr contra nada inventado.

## Lo que se podría mejorar sin candidato — nombrado, NO hecho

Queda escrito para que Roberto decida si vale la pena, en vez de seguir puliendo:

- **Comprar un día de régimen alto posterior a la caja** cuando exista (re-correr el auxiliar hasta que
  una sesión supere 2,62 bps ex-ante, ~$1,70-2,50). Saldaría la deuda 3 sin candidato.
- **Un segundo día por tercil** para saber cuánto varía el spread dentro de un mismo régimen (~$3,50).
- **Cobrar también el cruce de salida** (hoy sólo se cobra la entrada); requiere medir si las salidas
  en el objetivo se llenan por límite o cruzando.
- **Barrer el umbral por tercil** (hoy 2,0σ) sobre semillas, como se hizo con C8, para saber con qué
  frecuencia un tercil nulo lo cruza.

---

## Estado final del juez

**Qué mide.** Dólares por sesión, netos, de un candidato que entrega entradas y reglas (nunca
resultados), contra ES 1-min 2016-2019: comisión medida, deslizamiento del stop medido, deslizamiento
de entrada por régimen (cruce) o markout/llenado (pasivo), y el sesgo de contabilidad restado sólo en
la dirección conservadora. Lo compara con dos nulas de permutación (rotación en rango + signo) más una
posición pasiva —las tres informadas siempre, y **cuáles entran al mínimo lo decide la clase de
ventaja declarada, sólo si la firma medida la confirma**—, exige que la ventaja aguante contra la nula
válida en los tres terciles de volatilidad **ex-ante en bps**,
devuelve P(pasar) por la cadena eval × fondeada **al tamaño declarado**, la resolución, y avisa cuándo
a esa ventaja conviene capital propio. Registro encadenado con hash y huella de familia a tres cubetas.

**Qué NO mide** (va impreso en cada veredicto): la búsqueda anterior al candidato (se declara, es
inverificable); **si la clase de ventaja declarada es sincera** —la firma la contrasta y la contradice
con bandera roja, pero una firma `indefinida` no prueba nada en ninguna dirección—; la regla de
consistencia de las firmas; el deslizamiento de entrada **pasiva por-candidato** (hoy calibrado al
azar); una ventaja de **salida**, inexpresable por construcción; 2020+ (caja sellada); el costo de
oportunidad del capital; y **cualquier instrumento que no sea ES o MES** — hay ficha empezada para 6E
y 6J, y el juez **se niega** con la lista de lo que falta hasta que esté completa.

**Y lo que la verificación no puede hacer, publicado y no escondido:** 2019 tiene resolución **±72%**
de la ventaja de referencia contra **±33%** del trabajo (MDE $25,84 contra $20,54). **Está
subpotenciada por construcción** y la partición 3/1 se mantiene igual, por cobertura de régimen.

**Veredictos posibles.**
- **SUPERA** — sólo en modo cruce (o en la futura medición por-candidato). Aprobación firme.
- **APUESTA AL REGIMEN** — rentable e informativo, pero la ventaja vive en un solo tercil. No es un pase.
- **NO SUPERA** — no rentable, o no informativo, o no aguanta las nulas. Firme en los dos modos.
- **REQUIERE MEDICION PASIVA POR CANDIDATO** — sólo en modo pasivo, cuando superaría la cota optimista.
  El modo pasivo **nunca aprueba**: una cota optimista sólo sirve para rechazar.
- **NO MEDIBLE** — pocas operaciones, bracket sin sesgo caracterizado, ventana angosta, fuera de datos.
- **RECHAZADA** — la entrada trae resultados, o excede el límite de contratos declarado.

**Las tres deudas abiertas.**
1. **El markout pasivo por-candidato.** El modo pasivo usa un markout calibrado sobre entradas al
   azar; para un candidato direccional puede darse vuelta. Lo salda `medir_pasivo_candidato` (el sim
   FIFO sobre sus entradas reales), sin correr todavía.
2. **El 53% no llenado por-candidato.** La fracción que no se llena se supone neutral (cierto al azar);
   para un candidato el no-llenado está seleccionado por su señal y podría ser sus ganadores. Mismo
   hook lo salda.
3. **El régimen alto de 2026 está cubierto sólo por 2018.** Ningún día posterior a la caja sellada cae
   en el tercil alto de volatilidad; cualquier conclusión sobre régimen alto reciente es extrapolación.
