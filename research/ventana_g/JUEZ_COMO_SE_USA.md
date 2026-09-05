# EL JUEZ — cómo se usa

Para alguien que no vivió la semana. **No gasta cartucho. K = 261. Construir la herramienta no es
usarla.** Usarla sobre un candidato real sí puede gastar: contá contra K.

## Qué hace

Toma un candidato —**entradas y reglas, nunca resultados**— y calcula contra ES 1-min 2016-2019
cuánto rinde en dólares por sesión, neto de comisión y deslizamiento medidos, y si ese rendimiento
viene de información o del patrón. Devuelve un veredicto de cuatro valores:

| veredicto | qué significa |
|---|---|
| **SUPERA** | da dólares positivos, bate las dos nulas y la pasiva, y **aguanta en los tres regímenes** de volatilidad |
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
  `MBO_DISENO_entrada_pasiva.md`; la consistencia de las firmas no está modelada; y **el falso
  negativo estructural**: un candidato cuya ventaja sea sólo de sincronización muere contra la nula de
  signo aunque sea real.

## El registro y el contador

`REGISTRO_JUEZ.jsonl`, una línea por juicio, **encadenada con hash**: borrar o editar una línea rompe
la cadena y el juez lo avisa en cada corrida siguiente. Cuenta intentos de la misma familia y sube
el umbral. **Defiende contra el descuido, no contra alguien motivado:** se puede correr en otra
copia del repo o con otro registro. Agujero conocido y marcado.

## El agujero mayor, dicho en la cara

El juez **no puede ver la búsqueda que ocurrió antes** de que el candidato llegara. Por eso exige la
declaración de variantes y la imprime en el veredicto. Si la declaración miente, el veredicto no
vale, y no hay código que lo detecte.

## Controles

`python juez_controles.py` corre siete controles con condición de falla escrita contra resultados
publicados: sin ventaja → NO SUPERA; ventaja inyectada → SUPERA y recupera la magnitud; pocas
operaciones → NO MEDIBLE; entrada con resultados → RECHAZADA; ventaja en un solo régimen (tercil alto
de volatilidad) → APUESTA AL REGIMEN; el candidato solo-largo de 2017 → NO SUPERA con la defensa
puesta (y se muestra sin la defensa, para ver que hace falta); ventaja sólo en tendencias bajistas
→ APUESTA AL REGIMEN, la prueba de que cerrar el eje de dirección no dejó un agujero; y un candidato
en el **borde** entre modos → NO SUPERA en cruce / REQUIERE MEDICION en pasivo, nunca SUPERA. Los ocho
se corren en los **dos modos**, y se verifica que el modo pasivo nunca devuelve SUPERA. Salida en
`salida_juez_controles.txt`.

---

# CIERRE — el juez está terminado

**Versión final, 2026-09-04.** `juez.py` + `juez_controles.py` + `mbo_lib.py`. No queda trabajo
pendiente **que no requiera un candidato real**.

## Los ocho controles, en los dos modos (8/8 y 8/8)

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

**Ningún control devuelve SUPERA en modo pasivo**, y no puede: `techo_pasivo` lo convierte por
construcción. C8 quedó recalibrado con `c8_semillas.py` (12 semillas × 3 valores de ventaja): a
q=0,56 sólo el 42% de las semillas caía en el borde y 5 de 12 quedaban **por encima** (SUPERA en
cruce); a **q=0,545** las 12 dan NO SUPERA en cruce y **9 de 12 (75%) cruzan hacia arriba** en pasivo,
sin ninguna llegar a SUPERA. El suite usa una semilla dedicada para que el borde no dependa del sorteo.

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

**El punto ciego de timing es TOTAL, no parcial.** Una ventaja de timing de +$403/sesión, medida y
recuperada al 98% por la nula de rotación, se descarta igual, porque el "informativo" es el **mínimo**
de las tres nulas y la de signo la ve al −1%. Cualquier ventaja de timing pura, **del tamaño que sea**,
recibe NO SUPERA. La de tamaño, en cambio, el juez la ve bien (91-95%).

Por eso el juez ahora **detecta la firma** (rotación alta, signo ~0) y la imprime: un candidato con
ventaja de timing recibe NO SUPERA **con el aviso de que le falta el instrumento**, no un rechazo mudo.

No se agregó una tercera forma: la que faltaría es una ventaja de **salida** (cuándo cerrar), y el juez
la prohíbe por construcción — la regla de salida se declara y se aplica igual a todas las operaciones.

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
posición pasiva, exige que la ventaja aguante en los tres terciles de volatilidad **ex-ante en bps**,
devuelve P(pasar) por la cadena eval × fondeada **al tamaño declarado**, la resolución, y avisa cuándo
a esa ventaja conviene capital propio. Registro encadenado con hash y huella de familia a tres cubetas.

**Qué NO mide** (va impreso en cada veredicto): la búsqueda anterior al candidato (se declara, es
inverificable); la regla de consistencia de las firmas; el deslizamiento de entrada **pasiva
por-candidato** (hoy calibrado al azar); 2020+ (caja sellada); el costo de oportunidad del capital.

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
