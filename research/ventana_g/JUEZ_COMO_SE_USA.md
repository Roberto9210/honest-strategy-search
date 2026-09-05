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
  el stop (`media_exceso.py`) y la corrección de contabilidad aplicada **sólo en la dirección
  conservadora** (`o = 0,0642 ± 7,6%`; nadie la cobra eligiendo el bracket) con su error propagado.
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
- **LO QUE ESTE VEREDICTO NO CUBRE**, obligatorio. Entre otras: el deslizamiento de entrada se trata
  como cero; la consistencia de las firmas no está modelada; y **el falso negativo estructural**: un
  candidato cuya ventaja sea sólo de sincronización muere contra la nula de signo aunque sea real.

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
puesta (y se muestra sin la defensa, para ver que hace falta); y ventaja sólo en tendencias bajistas
→ APUESTA AL REGIMEN, la prueba de que cerrar el eje de dirección no dejó un agujero. Salida en
`salida_juez_controles.txt`.
