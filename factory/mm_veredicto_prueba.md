# Veredicto de la prueba única multi-mercado — F4 sobre NQ, YM, NKD

**Fecha:** 26 de agosto de 2026, dentro del corte del 28. **Orden de los hechos:** pre-registro en el
ledger (`8129df0c2170b9fe`) y predicción sellada (`9456128`) → una sola corrida → resultado crudo
commiteado sin interpretar (`8e337ff`) → este documento. La caja fuerte de ES no se leyó: ES no
participa de la prueba.

## El resultado, aplicando el criterio pre-registrado

| | n | δ̂ | z | p bilateral |
|---|---|---|---|---|
| **PRUEBA ÚNICA (los tres juntos)** | 778 | **0,1018** | **1,9824** | **0,0474** |
| bloque A (≤ 2019-11, calendario del descubrimiento) | 566 | 0,0635 | 1,88 | 0,0601 |
| bloque B (2019-12 →, calendario nunca buscado) | 212 | **0,2038** | 1,236 | 0,2165 |

Por mercado (δ̂ estandarizado, neto de fricción): NQ **0,0948** · YM **0,1272** · NKD **0,0729**.
Los tres positivos.

> **CONFIRMA: |z| = 1,9824 ≥ 1,959964, p = 0,0474 ≤ 0,05.** Una regla congelada, elegida en ES y
> jamás ajustada, superó una prueba única pre-registrada sobre tres índices que ninguna búsqueda había
> tocado. **Y confirma por un margen de 1,1 % en z** — lo que sigue es la parte que la spec obliga a
> decir con la misma tipografía.

## El filo, dicho entero

**El diagnóstico de diseño quedó del otro lado de la línea.** `z_diseño = δ̂·√361,3 = 1,9344 < 1,96`.
Las dos varianzas — la agrupada por período (la prueba primaria, fijada en §j.1 ANTES de correr) y la
implicada por el n efectivo pre-registrado — caen una a cada lado del umbral. La primacía se declaró
antes de conocer ningún número, así que el veredicto formal es CONFIRMA; pero un resultado que cambia
de signo según el estimador de varianza es un resultado **al filo**, y se trata como tal: con más
sospecha, no con menos. La predicción 5 pedía |z_diseño − z| < 0,4; dio 0,048 — las dos maquinarias
están de acuerdo en la magnitud y discrepan solo en el borde.

Segundo filo: δ̂ = 0,1018 quedó **por debajo** del 0,1515 pre-registrado, exactamente donde la
maldición del ganador decía que iba a estar (predicción 1: 0,05–0,12 ✓). El efecto multi-mercado es
~2/3 del que ES prometía.

## Qué rama de §g toca — por la definición escrita, no por la que convenga

- **No es NEGATIVO** (p ≤ 0,05).
- **No es la rama 2** ("positivo empujado por el bloque A, con el bloque B sin acompañar ni en signo
  ni en magnitud"): el bloque B acompaña en signo **y** en magnitud — δ̂_B = 0,2038, el triple del
  bloque A. La significancia agrupada está sostenida en más de la mitad por las 212 vueltas que
  ninguna búsqueda vio (aportan 0,0555 de los 0,1018).
- **Es la rama 3 por su definición escrita** — "mismo signo y magnitud comparable en las 212 vueltas
  que ninguna búsqueda vio" — con una honestidad obligatoria: el rótulo de esa rama decía "sobrevive
  en el bloque B **por separado**", y B por separado **no es significativo** (z = 1,24, p = 0,22, con
  ~32 % de potencia no podía serlo casi nunca). La definición operativa entre paréntesis es la que se
  escribió y es la que se aplica; la tensión entre rótulo y definición queda anotada como imprecisión
  de la spec, no se resuelve a favor del resultado.

> **Lo que la rama 3 AUTORIZA, textual:** UN forward test pre-registrado en Sim101 con datos de
> mercado REALES — jamás el Simulated Data Feed, y el reporte tiene que nombrar el feed — **y NUNCA
> dinero.** El pre-registro del forward fija su propia vara antes de encenderse. La cuenta ya está
> hecha y no se re-estima de memoria: 14,40 efectivas/año, 342 efectivas = **23,7 años** — el forward
> es acumulación lenta de evidencia, no un examen que se aprueba.
>
> **Lo que NO autoriza:** construir un bot con dinero; tocar la caja fuerte de ES; re-correr, extender
> o subdividir esta prueba; agregar mercados; ninguna búsqueda nueva. K = 257 heredado, intacto.

## La predicción, contrastada — 3 de 5, y las dos falladas son las importantes

| predicho (`mm_prediccion_prueba.md`) | medido | ¿cumple? |
|---|---|---|
| δ̂ en 0,05–0,12 | 0,1018 | **sí** |
| la prueba NO llega a p ≤ 0,05 (60 % negativo / 30 % rama 2 / 10 % rama 3) | confirmó — ocurrió la rama del **10 %** | **no** |
| δ̂_A > δ̂_B (el bloque A hereda la suerte de la selección) | δ̂_B = 0,2038 **triplica** a δ̂_A = 0,0635 | **no — al revés** |
| los tres positivos; NQ ≈ YM (±0,04); NKD el más chico | 0,0948 / 0,1272 / 0,0729; \|NQ−YM\| = 0,032 | **sí** |
| \|z_diseño − z\| < 0,4 | 0,048 | **sí** |

La falla de la predicción 3 es la información más valiosa del día: la estructura "el bloque compartido
manda y el nuevo está chato" era la firma esperada de una réplica de suerte de selección, **y salió la
contraria**. Eso no convierte el resultado en verdad — 212 vueltas con z 1,24 no alcanzan para nada por
sí solas — pero es exactamente la asimetría que un efecto real produciría y una réplica espuria no
tendería a producir. Dicho con el freno puesto: δ̂_B = 0,2038 es una estimación con error estándar
0,165; su intervalo es enorme; la palabra correcta es "alentador", no "confirmado".

## Lo que este veredicto afirma y lo que no

**Afirma:** una prueba única pre-registrada (K = 1), con la multiplicidad de la búsqueda original ya
pagada en ES, sobre mercados jamás usados para seleccionar nada, con los costos adentro de cada
número, dio p = 0,0474 — y el efecto medido, 0,1018, es coherente con un residuo real de flujo de
rebalanceo ~2/3 del tamaño que el máximo sesgado de ES sugería.

**No afirma:** que δ̂ = 0,1018 sea una estimación insesgada del rendimiento futuro (la prueba se hizo
porque el efecto podía existir; los que confirman al filo están, en promedio, inflados); que F4 sea
operable con dinero (nada de hoy lo autoriza); que el resultado sobreviviera con la otra varianza
(no sobrevivió: 1,9344). **Y no reabre nada:** esto era una regla de parada. Paramos de buscar igual —
la diferencia es que se para con una hipótesis viva y un forward autorizado, en vez de con un cierre.

**Fragilidad heredada, vigente:** la apertura de la fase dependía de NKD (§h: sin NKD la compuerta 2
no pasaba) y NKD sigue siendo el dato de peor calidad. Si un defecto de datos lo tumba, la fase entera
queda inválida — la consecuencia ya estaba pre-declarada y no cambia ahora que el resultado es
conocido.

**La caja fuerte de ES (2020-2026) sigue sellada.** Sexta vez que se escribe en esta fase; sigue
siendo cierta.
