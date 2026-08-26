# Ronda de falsación — veredicto único, y cierre de BOT C

**Fecha:** 26 de agosto de 2026, cinco días antes del corte del lunes 31. **Orden de los hechos:**
cuatro pre-registros en el ledger (K 258–261) y predicciones firmadas commiteadas (`9943509`) → una
corrida por prueba → crudo commiteado sin interpretar (`38ab3ff`) → este documento. ES no participó de
nada; su caja fuerte sigue sellada.

---

## LA CONCLUSIÓN: **EL MECANISMO AGUANTA.**

Las cuatro predicciones firmadas se cumplieron — la primera tanda de predicciones del proyecto que se
cumple entera. F4 sigue siendo lo que creíamos: **un residuo real de flujo de rebalanceo de fin de mes,
y sigue siendo chica.** Nada de esta ronda la hace más grande; lo que hace es dejarla mejor entendida
y con las tres firmas que un artefacto no tendría.

| # | prueba | criterio pre-declarado | medido | veredicto |
|---|---|---|---|---|
| 1 | placebo de calendario | δ̂ < 0,0509 | **0,0417** (z 0,69) | **PASA** |
| 2 | el contado como testigo | δ̂ bruto > 0 en los tres | **0,0909 / 0,1534 / 0,0873** | **PASA** |
| 3 | concentración en la frontera | participación ≥ 0,60 | **0,6454** | **PASA** |
| 4 | el signo del rebalanceo | brecha ≥ 0,02 | **0,1523** | **PASA** |

Y las predicciones en magnitud, no solo en veredicto: P1 predijo [−0,02, +0,05] → 0,0417 adentro; P2
predijo contado dentro de ±0,05 del futuro bruto → diferencias −0,008 / +0,016 / **−0,0005** (el par
Nikkei clavado al medio punto porcentual de σ); P3 predijo ~65 % → 64,54 %; P4 predijo brecha ≥ 0,05 →
0,152, el triple.

## Por qué cada prueba dice lo que dice

**P2 es la más limpia de las cuatro.** El efecto existe en los índices de contado — sin fricción, sin
roll, sin contrato — con casi la misma magnitud estandarizada que en los futuros. Un artefacto de
futuro (roll, base, microestructura del contrato) no puede producir eso. La explicación "es un fenómeno
del índice" queda de pie; la explicación "es un fenómeno del instrumento" queda muerta.

**P4 es la que más enseña.** Tras un mes en baja, δ̂ = **0,195** (n = 308, z = 2,07 — el subgrupo solo
es más significativo que la prueba entera); tras un mes en alza, 0,043. Un fondo balanceado compra
acciones después de que caen: la firma del rebalanceo está, con el signo correcto y cuatro veces el
tamaño mínimo exigido. **Y la prohibición pre-escrita rige:** esto explica, no habilita. Operar "sólo
tras meses en baja" sería una estrategia nueva con su propia K y su propio pre-registro. No se hace.

**P3 confirma la forma:** los tres pasos centrales cargan el 64,5 % del efecto con el 50 % de las
sesiones. No es deriva uniforme con disfraz de calendario.

**P1 pasó — y es la que hay que reportar con menos triunfalismo.** Los detalles incómodos, todos del
crudo:

- El agregado pasó (0,0417 < 0,0509), pero **por mercado el placebo de NQ (0,076) y de YM (0,103) NO
  es chico** — son ~3/4 del efecto bruto de vuelta de mes de esos mercados. El agregado queda bajo el
  umbral en buena parte porque el placebo de NKD es **negativo** (−0,044).
- Partido por bloques, el placebo dibuja el mapa entero: **bloque A: TOM 0,064 contra placebo 0,058 —
  indistinguibles.** En el calendario del descubrimiento, F4 no se distingue de la deriva de mitad de
  mes. **Bloque B: TOM 0,204 contra placebo −0,001.** En el calendario que ninguna búsqueda vio, el
  efecto de vuelta de mes existe y la deriva placebo no.
- Caveat de muestra, declarado y no perseguido: el placebo 8→14 choca con la banda de roll en los
  meses trimestrales (NQ pierde 103, YM 97), así que compara meses no-trimestrales contra la muestra
  completa de F4. Resolverlo exigiría datos nuevos y esta ronda no los toca.

**La lectura conjunta de P1 y de la prueba única es la frase más importante del cierre:** la evidencia
del bloque A — el 73 % del n efectivo — se parece a deriva; la evidencia del bloque B — donde δ̂
triplica al A y el placebo da cero — es donde el mecanismo vive. El resultado agregado de la prueba
única (p = 0,047) está sostenido por la parte de la muestra que menos sospecha merece. Eso es lo
contrario de lo que una réplica de suerte de selección produciría, y es coherente con P4: el
rebalanceo es más grande cuando hay más que rebalancear.

## Las dos observaciones que no cuestan K (encargo, textual)

1. **El bloque B salió más fuerte que el A.** Contradice el patrón de "resto que el mercado va
   arbitrando" — el que este proyecto encontró en el funding de PAXG y en el efecto de inclusión en
   índices — pero es consistente con flujo de rebalanceo, porque el dinero indexado creció enormemente
   desde 2000. **La tensión queda escrita y no se resuelve con datos nuevos:** o el flujo creció más
   rápido de lo que el arbitraje lo come, o el bloque B tuvo suerte (SE 0,165 la permite de sobra).
   Las dos caben en lo medido; elegir una sería inventar.
2. **La grilla 3×3 del ledger muestra (4,2) con PF 1,691, por encima de (4,3) con 1,507.** La meseta
   es real y ya está pagada. No se re-corre, no se amplía, y (4,2) no se adopta: sería la búsqueda
   entrando por la ventana.

## Lo que este cierre autoriza y lo que no

Nada nuevo. Lo único autorizado sigue siendo lo que la rama 3 de §g autorizó: **UN forward test
pre-registrado en Sim101 con datos de mercado reales y feed nombrado — nunca dinero.** La ronda de
falsación no lo amplía (no puede: ningún resultado hace a F4 más grande) y no lo revoca (las cuatro
pruebas pasaron). K queda en **261** y no se reinicia.

## Puertas declaradas — y acá se quedan

1. **El placebo alto de NQ/YM** (0,076/0,103) y su choque de muestra con los meses trimestrales.
   Si alguna vez alguien reabre algo, esto es lo primero que tiene que mirar: cuánta de la vuelta de
   mes de los índices de EE.UU. es deriva de mes no-trimestral. No se mira hoy.
2. **La condicionalidad de P4 como estrategia** ("comprar la vuelta sólo tras mes en baja",
   δ̂ 0,195, z 2,07 en el subgrupo). Es la puerta más tentadora del proyecto entero y queda
   **cerrada con nombre**: estrategia nueva ⇒ K propia, pre-registro propio, y otra década de datos.
   Escribirla acá es la manera de no fingir después que no se vio.
3. **Los índices de bonos** (extensión de duración a fin de mes, spec §b.2): otro mecanismo, otra
   fase, si alguna vez se abre.
4. **La fragilidad NKD** (§h): la fase entera descansó en el mercado de peores datos. El forward, si
   corre, la hereda.

---

## BOT C queda CERRADO.

No hay ronda siguiente, ni quinta prueba, ni variante. El encargo del 21-ago — *"encontrá la manera de
crear un bot que genere ganancia real, no te detengas hasta intentarlo"* — se intentó hasta el final:
una búsqueda que cerró negativa (Fase 1-2), un veredicto aritmético que la detuvo (`botc_potencia_f4`),
una fase multi-mercado pre-registrada que confirmó al filo (p = 0,047), y una ronda de falsación que el
mecanismo aguantó entera. El resultado neto es una hipótesis viva, chica, entendida, con un forward
autorizado de década — **y ningún bot con dinero, porque nada de lo medido autoriza uno.** Ésa es la
respuesta honesta al encargo, y es la definitiva de esta ventana.
